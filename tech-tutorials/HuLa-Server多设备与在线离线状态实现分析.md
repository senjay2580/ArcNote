# HuLa-Server 多设备实现与在线离线状态管理分析

## 项目概述

HuLa-Server 是一款基于 SpringCloud、SpringBoot3、Netty、MyBatis-Plus 和 RocketMQ 构建的即时通讯系统服务端。本文档详细分析其多设备管理和在线离线状态的实现逻辑。

## 一、核心架构设计

### 1.1 技术栈
- **WebSocket服务**: 基于 Spring WebFlux + Netty 的响应式架构
- **缓存**: Redis 用于存储路由信息和在线状态
- **服务注册**: Nacos 用于节点管理和服务发现
- **消息队列**: RocketMQ 用于跨节点消息推送

### 1.2 核心模块
- **luohuo-ws**: WebSocket 服务，负责长连接管理
- **luohuo-presence**: 在线状态服务
- **luohuo-router**: 路由服务，管理用户设备与节点的映射关系

## 二、多设备管理实现

### 2.1 设备标识体系

#### 设备唯一标识（clientId）
每个设备通过 `clientId`（设备指纹）进行唯一标识，格式为：
```
uid:clientId
```

#### 三级映射关系
系统维护了三级映射关系来管理多设备：

1. **用户 → 设备 → 会话集合**（本地内存）
   ```java
   ConcurrentHashMap<Long, Map<String, Set<WebSocketSession>>> USER_DEVICE_SESSION_MAP
   ```

2. **设备 → 节点映射**（Redis Hash）
   ```
   Key: luohuo:router:device-node-mapping
   Field: {uid}:{clientId}
   Value: {nodeId}
   ```

3. **节点 → 设备集合**（Redis Set）
   ```
   Key: luohuo:router:node-devices:{nodeId}
   Value: Set<{uid}:{clientId}>
   ```

### 2.2 会话注册流程

#### 核心类：SessionManager.registerSession()

```java
public void registerSession(WebSocketSession session, String clientId, Long uid) {
    // 1. 设备级会话注册（本地内存）
    USER_DEVICE_SESSION_MAP.compute(uid, (key, deviceMap) -> {
        if (deviceMap == null) deviceMap = new ConcurrentHashMap<>();
        deviceMap.compute(clientId, (k, sessions) -> {
            if (sessions == null) sessions = new HashSet<>();
            sessions.add(session);
            return sessions;
        });
        return deviceMap;
    });

    // 2. 反向索引更新
    SESSION_USER_MAP.put(session.getId(), uid);
    SESSION_CLIENT_MAP.put(session.getId(), clientId);

    // 3. 首次连接设备时触发路由注册
    boolean isFirstSession = ...;
    if (isFirstSession) {
        nacosSessionRegistry.addUserRoute(uid, clientId);
        syncOnline(uid, clientId, true); // 同步设备在线状态
    }
}
```


#### 路由注册：NacosSessionRegistry.addUserRoute()

```java
public void addUserRoute(Long uid, String clientId) {
    String deviceField = uid + ":" + clientId;

    // 1. 设备指纹→节点映射（Redis Hash）
    cachePlusOps.hSet(RouterCacheKeyBuilder.buildDeviceNodeMap(deviceField), nodeId);

    // 2. 节点→设备指纹映射（Redis Set）
    cachePlusOps.sAdd(RouterCacheKeyBuilder.buildNodeDevices(nodeId), deviceField);

    // 3. 更新节点元数据
    Map<String, String> metadata = nodeInstance.getMetadata();
    metadata.put("lastActive", Instant.now().toString());
    nodeInstance.setMetadata(metadata);
}
```

### 2.3 多设备并发处理

#### 同一用户多设备同时在线
- 每个设备维护独立的 WebSocket 会话集合
- 同一设备可能有多个会话（如网络重连时）
- 使用 `ConcurrentHashMap` 和 `Set` 保证线程安全

#### 设备级别的消息推送
```java
public Mono<Void> sendToDevice(Long uid, String clientId, WsBaseResp<?> resp) {
    Map<String, Set<WebSocketSession>> deviceMap = USER_DEVICE_SESSION_MAP.get(uid);
    if (deviceMap == null) return Mono.empty();

    Set<WebSocketSession> sessions = deviceMap.get(clientId);
    if (CollUtil.isEmpty(sessions)) return Mono.empty();

    return Flux.fromIterable(sessions)
        .filter(WebSocketSession::isOpen)
        .flatMap(session -> session.send(...))
        .then();
}
```

## 三、在线离线状态管理

### 3.1 缓存键设计

#### PresenceCacheKeyBuilder 提供的缓存键


1. **全局在线设备 ZSet**
   ```
   Key: luohuo:presence:global-devices-online
   Member: {uid}:{clientId}
   Score: timestamp（毫秒）
   ```

2. **全局在线用户 ZSet**
   ```
   Key: luohuo:presence:global-users-online
   Member: {uid}
   Score: timestamp（毫秒）
   ```

3. **群组在线成员 Set**
   ```
   Key: luohuo:presence:group-members-online:id:{roomId}
   Value: Set<uid>
   ```

4. **用户在线群组 Set**
   ```
   Key: luohuo:presence:users-group-online:groups:{uid}
   Value: Set<roomId>
   ```

### 3.2 在线状态同步流程

#### 核心方法：SessionManager.syncOnline()

```java
@RedissonLock(prefixKey = "syncOnline:", key = "#uid")
public void syncOnline(Long uid, String clientId, boolean online) {
    // 1. 生成用户设备key、全局在线状态key
    String deviceKey = uid + ":" + clientId;
    String onlineDevicesKey = PresenceCacheKeyBuilder.globalOnlineDevicesKey().getKey();
    String onlineUsersKey = PresenceCacheKeyBuilder.globalOnlineUsersKey().getKey();

    // 2. 获取用户所有群组
    List<Long> roomIds = getRoomIds(uid);

    // 3. 检查设备状态（是否是首个或最后一个设备）
    boolean noOtherDevices = isFirstOrLastDevice(uid, deviceKey);


    if (online) {
        // 4. 上线逻辑
        long millis = System.currentTimeMillis();
        cachePlusOps.zAdd(onlineDevicesKey, deviceKey, millis);
        
        // 仅首个设备登录时才添加用户在线状态
        if (noOtherDevices) {
            cachePlusOps.zAdd(onlineUsersKey, uid, millis);
            updateGroupPresence(roomIds, uid, true);
            pushDeviceStatusChange(roomIds, uid, clientId, WSRespTypeEnum.ONLINE.getType(), onlineUsersKey);
        }
    } else {
        // 5. 下线逻辑
        cachePlusOps.zRemove(onlineDevicesKey, deviceKey);
        
        // 所有设备都下线之后移除用户的在线状态
        if (noOtherDevices) {
            cachePlusOps.zRemove(onlineUsersKey, uid);
            updateGroupPresence(roomIds, uid, false);
            pushDeviceStatusChange(roomIds, uid, clientId, WSRespTypeEnum.OFFLINE.getType(), onlineUsersKey);
        }
    }
}
```

### 3.3 多设备在线状态判断

#### isFirstOrLastDevice() 方法

```java
private boolean isFirstOrLastDevice(Long uid, String excludeDeviceKey) {
    String onlineDevicesKey = PresenceCacheKeyBuilder.globalOnlineDevicesKey().getKey();
    String prefix = uid + ":";

    // 分批获取设备
    int batchSize = 1000;
    long total = cachePlusOps.zCard(onlineDevicesKey);

    for (int i = 0; i < total; i += batchSize) {
        Set<Object> batchDevices = cachePlusOps.zRangeByScoreWithScores(...);
        
        for (Object deviceObj : batchDevices) {
            String device = deviceObj.toString();
            if (device.startsWith(prefix) && !device.equals(excludeDeviceKey)) {
                return false; // 发现其他设备
            }
        }
    }
    return true; // 没有其他设备
}
```

**关键逻辑**：
- 只有当用户的第一个设备上线时，才将用户标记为在线
- 只有当用户的最后一个设备下线时，才将用户标记为离线
- 中间设备的上下线不影响用户的整体在线状态


### 3.4 群组在线状态管理

#### updateGroupPresence() 方法

```java
private void updateGroupPresence(List<Long> roomIds, Long uid, boolean online) {
    if (CollUtil.isEmpty(roomIds)) return;

    // 1. 批量更新群组在线状态
    roomIds.forEach(roomId -> {
        CacheKey onlineGroupKey = PresenceCacheKeyBuilder.onlineGroupMembersKey(roomId);
        if (online) {
            cachePlusOps.sAdd(onlineGroupKey, uid);
        } else {
            cachePlusOps.sRem(onlineGroupKey, uid);
        }
    });

    // 2. 更新用户群组在线映射
    CacheKey onlineUserGroupsKey = PresenceCacheKeyBuilder.onlineUserGroupsKey(uid);
    if (online) {
        roomIds.forEach(roomId -> cachePlusOps.sAdd(onlineUserGroupsKey, roomId));
    } else {
        roomIds.forEach(roomId -> cachePlusOps.sRem(onlineUserGroupsKey, roomId));
    }
}
```

## 四、消息推送与路由

### 4.1 精准路由推送

#### PushService.sendAsync() 核心流程

```java
public CompletableFuture<Void> sendAsync(WsBaseResp<?> msg, List<Long> uids, Long cuid) {
    // 1. 构建三级映射: 节点 → 设备指纹 → 用户ID
    Map<String, Map<String, Long>> nodeDeviceUser = routerService.findNodeDeviceUser(uids);

    // 2. 并行发送到所有节点
    List<CompletableFuture<Void>> futures = new ArrayList<>();
    nodeDeviceUser.forEach((nodeId, deviceUserMap) -> {
        CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
            if (this.nodeId.equals(nodeId)) {
                // 本地节点直接推送
                localPush(deviceUserMap, msg);
            } else {
                // 远程节点通过MQ转发
                sendToNodeViaMQ(nodeId, msg, deviceUserMap, cuid);
            }
        }, getExecutorForNode(nodeId));
        futures.add(future);
    });

    return CompletableFuture.allOf(futures.toArray(CompletableFuture[]::new));
}
```


### 4.2 路由查询优化

#### NacosRouterService.findNodeDeviceUser()

```java
public Map<String, Map<String, Long>> findNodeDeviceUser(List<Long> uids) {
    // 1. 提取目标UID集合
    Set<Long> targetUids = new HashSet<>(uids);

    // 2. 获取全局设备-节点映射（使用HSCAN分批加载）
    CacheHashKey deviceNodeMap = RouterCacheKeyBuilder.buildDeviceNodeMap("");
    Map<String, Map<String, Long>> result = new ConcurrentHashMap<>();

    // 3. 过滤活跃节点
    Set<String> activeNodes = getAllActiveNodes();

    // 4. 使用HSCAN游标分批遍历
    ScanOptions options = ScanOptions.scanOptions().count(500).build();
    try (Cursor<Map.Entry<Object, Object>> cursor = redisTemplate.opsForHash().scan(...)) {
        while (cursor.hasNext()) {
            Map.Entry<Object, Object> entry = cursor.next();
            
            String field = (String) entry.getKey();  // uid:clientId
            String nodeId = (String) entry.getValue();
            
            if (!activeNodes.contains(nodeId)) continue;

            String[] parts = field.split(":");
            Long uid = Long.parseLong(parts[0]);
            String clientId = parts[1];

            if (!targetUids.contains(uid)) continue;

            // 构建映射：节点 → 设备 → UID
            result.computeIfAbsent(nodeId, k -> new ConcurrentHashMap<>())
                  .put(clientId, uid);
        }
    }
    return result;
}
```

**优化点**：
- 使用 HSCAN 避免 HGETALL 阻塞
- 分批加载，每批 500 条
- 过滤非活跃节点
- 只返回目标用户的路由信息

### 4.3 本地推送优化

```java
private void localPush(Map<String, Long> deviceUserMap, WsBaseResp<?> msg) {
    // 按设备数动态调整并行度, 最大32线程并发
    int parallelism = Math.min(deviceUserMap.size(), 32);

    Flux.fromIterable(deviceUserMap.entrySet())
        .parallel(parallelism)
        .runOn(localPushScheduler)
        .flatMap(entry ->
            sessionManager.sendToDevice(entry.getValue(), entry.getKey(), msg)
                .timeout(Duration.ofSeconds(5))
                .onErrorResume(e -> {
                    log.error("设备推送超时: {}", entry.getKey());
                    return Mono.empty();
                })
        ).subscribe(...);
}
```


## 五、状态变更通知

### 5.1 好友在线状态推送

#### pushDeviceStatusChange() 方法

```java
private void pushDeviceStatusChange(List<Long> roomIds, Long uid, String clientId, 
                                    String type, String onlineKey) {
    // 1. 获取反向好友列表（需要知道该用户在线状态的uid）
    CacheKey reverseFriendsKey = FriendCacheKeyBuilder.reverseFriendsKey(uid);
    Set<Long> friends = cachePlusOps.sMembers(reverseFriendsKey)...;

    for (Long friendUid : friends) {
        // 1.1 获取该好友的全部好友列表
        CacheKey friendsKey = FriendCacheKeyBuilder.userFriendsKey(friendUid);
        List<Long> hisFriends = cachePlusOps.sMembers(friendsKey)...;

        // 1.2 管道批量查询分数（在线状态）
        List<Object> scores = cachePlusOps.getZSetScores(onlineKey, hisFriends);

        // 1.3 计算当前好友的在线数量
        long onlineCount = scores.stream().filter(Objects::nonNull).count();

        // 1.4 构建推送消息
        WsBaseResp resp = new WsBaseResp();
        resp.setType(type);
        resp.setData(new WSOnlineNotify(uid, clientId, TimeUtils.getTime(), 
                                        onlineCount, 2));

        // 1.5 定向推送
        pushService.sendPushMsg(resp, friendUid, uid);
    }
}
```

**关键设计**：
- 使用反向好友列表（谁关注了我）
- 批量查询在线状态，减少 Redis 请求
- 推送时携带在线好友总数

### 5.2 群组在线状态推送

```java
// 推送给用户的所有群
for (Long roomId : result.keySet()) {
    CacheKey cacheKey = PresenceCacheKeyBuilder.onlineGroupMembersKey(roomId);

    // 拿到在线群成员
    List<Long> memberIdList = cachePlusOps.sMembers(cacheKey)...;

    WsBaseResp resp = new WsBaseResp();
    resp.setType(type);
    resp.setData(new WSOnlineNotify(roomId, uid, clientId, TimeUtils.getTime(), 
                                    result.get(roomId), 1));

    // 定向分批发送（每批200人）
    int pageSize = 200;
    for (int i = 0; i < memberIdList.size(); i += pageSize) {
        List<Long> page = memberIdList.subList(i, Math.min(i+pageSize, memberIdList.size()));
        pushService.sendPushMsg(resp, page, uid);
    }
}
```


## 六、节点管理与容错

### 6.1 节点注册与心跳

#### NacosSessionRegistry 初始化

```java
@PostConstruct
public void init() {
    // 初始化节点实例
    nodeInstance = createNodeInstance();
    registerNodeInstance();
}

private Instance createNodeInstance() {
    Instance instance = new Instance();
    instance.setIp(nodeIp);
    instance.setPort(nodePort);
    instance.setHealthy(true);
    instance.setEphemeral(true);

    Map<String, String> metadata = new HashMap<>();
    metadata.put("nodeId", nodeId);
    metadata.put("startTime", Instant.now().toString());
    instance.setMetadata(metadata);
    return instance;
}
```

#### 定时心跳更新

```java
@Scheduled(fixedRate = 5000)
public void updateNodeMetrics() {
    try {
        // 更新元数据
        Map<String, String> metadata = new HashMap<>(nodeInstance.getMetadata());
        metadata.put("lastHeartbeat", Instant.now().toString());
        metadata.put("sessionCount", String.valueOf(sessionManager.getSessionCount()));

        // 添加客户端ID列表
        List<String> clientIds = sessionManager.getClientIds();
        if (!clientIds.isEmpty()) {
            metadata.put("clientIds", String.join(",", 
                        clientIds.subList(0, Math.min(10, clientIds.size()))));
        }

        // 重新注册更新后的实例
        nodeInstance.setMetadata(metadata);
        namingService.registerInstance("ws-cluster", "WS_GROUP", nodeInstance);
    } catch (NacosException e) {
        log.error("心跳更新失败", e);
    }
}
```

### 6.2 节点下线处理

#### NodeDownMessageListener 监听器

```java
@Component
public class NodeDownMessageListener extends AbstractRedisChannelMessageListener<NodeDownMessage> {

    @Override
    public void onMessage(NodeDownMessage message) {
        log.warn("收到节点下线通知: {}", message.getNodeId());
        migrateSessions(message.getNodeId());
    }

    private void migrateSessions(String downNodeId) {
        try {
            // 1. 获取受影响用户
            Map<Long, List<String>> deviceMap = routerService.getDevicesByNode(downNodeId);

            deviceMap.forEach((uid, clientIds) ->
                clientIds.forEach(clientId -> {
                    // 标记设备下线
                    sessionManager.syncOnline(uid, clientId, false);
                    
                    // 通知重连
                    sessionManager.sendToDevice(uid, clientId, new WsBaseResp<>());

                    // 清理路由
                    routerService.removeDeviceRoute(uid, clientId, downNodeId);
                })
            );

            // 删除节点设备集合
            redisTemplate.delete(RouterCacheKeyBuilder.buildNodeDevices(downNodeId).getKey());
        } catch (Exception e) {
            log.error("处理节点下线失败", e);
        }
    }
}
```


### 6.3 残留路由清理

#### 定时清理任务

```java
@Scheduled(fixedDelay = 30000)
public void cleanStaleRoutes() {
    // 1. 获取所有需要对比的ID集合
    Set<String> activeNodes = getAllActiveNodeIds();  // 从Nacos获取
    Set<String> redisNodes = getAllRedisNodeIds();    // 从Redis获取

    // 2. 计算需要清理的节点ID
    Set<String> staleNodes = redisNodes.stream()
        .filter(node -> !activeNodes.contains(node))
        .collect(Collectors.toSet());

    // 3. 批量清理
    staleNodes.forEach(node -> {
        log.info("发现残留节点数据，开始清理: {}", node);
        try {
            cleanupNodeRoutes(node);
            cleanNodeCompletely(node);
        } catch (Exception e) {
            log.error("节点清理失败: {}", node, e);
        }
    });
}

private void cleanNodeCompletely(String nodeId) {
    // 1. 获取节点所有设备
    CacheKey nodeDevicesKey = RouterCacheKeyBuilder.buildNodeDevices(nodeId);
    Set<String> deviceFields = redisTemplate.opsForSet()
        .members(nodeDevicesKey.getKey())...;

    if (CollectionUtils.isEmpty(deviceFields)) {
        return;
    }

    // 2. 准备在线状态清理数据
    Map<Long, Set<String>> uidToClients = deviceFields.stream()
        .map(field -> field.split(":"))
        .filter(parts -> parts.length == 2)
        .collect(Collectors.groupingBy(
            parts -> Long.parseLong(parts[0]),
            Collectors.mapping(parts -> parts[1], Collectors.toSet())
        ));

    // 3. 执行原子化清理
    uidToClients.forEach((uid, clients) -> 
        clients.forEach(client -> sessionManager.syncOnline(uid, client, false))
    );
}
```

## 七、会话清理与资源释放

### 7.1 单个会话清理

#### SessionManager.cleanupSession()

```java
public void cleanupSession(WebSocketSession session) {
    if (session != null && !session.isOpen()) {
        session.close(CloseStatus.GOING_AWAY)
            .subscribeOn(Schedulers.boundedElastic())
            .doAfterTerminate(() -> {
                String sessionId = session.getId();

                // 1. 获取反向索引
                String clientId = SESSION_CLIENT_MAP.remove(sessionId);
                Long uid = SESSION_USER_MAP.remove(sessionId);

                if (clientId != null && uid != null) {
                    // 2. 原子化清理设备指纹级核心映射
                    boolean isLastSession = cleanDeviceSession(uid, clientId, sessionId);

                    // 3. 若设备无会话，清理路由
                    if (isLastSession) {
                        nacosSessionRegistry.removeDeviceRoute(uid, clientId);
                        syncOnline(uid, clientId, false); // 通知下线
                    }
                }
            })
            .subscribe();
    }
}
```


#### 原子化设备会话清理

```java
private boolean cleanDeviceSession(Long uid, String clientId, String sessionId) {
    AtomicBoolean isLastSession = new AtomicBoolean(false);
    USER_DEVICE_SESSION_MAP.compute(uid, (u, deviceMap) -> {
        if (deviceMap == null) return null;
        deviceMap.compute(clientId, (c, sessions) -> {
            if (sessions != null) {
                sessions.removeIf(s -> s.getId().equals(sessionId));
                if (sessions.isEmpty()) {
                    // 标记为最后会话
                    isLastSession.set(true);
                    // 移除设备条目
                    return null;
                }
            }
            return sessions;
        });
        return deviceMap.isEmpty() ? null : deviceMap;
    });
    return isLastSession.get();
}
```

### 7.2 节点关闭清理

#### SessionManager.clean()

```java
public void clean() {
    // 0. 标记服务不可用状态
    setAcceptingNewConnections(false);
    nacosSessionRegistry.deregisterNode();

    // 1. 收集所有设备信息
    Map<Long, Set<String>> offlineDevices = new HashMap<>();
    USER_DEVICE_SESSION_MAP.forEach((uid, deviceMap) -> 
        offlineDevices.put(uid, new HashSet<>(deviceMap.keySet()))
    );

    // 2. 批量关闭会话 + 等待完成（超时控制）
    List<Mono<Void>> closeTasks = USER_DEVICE_SESSION_MAP.values().stream()
        .flatMap(deviceMap -> deviceMap.values().stream())
        .flatMap(Collection::stream)
        .filter(WebSocketSession::isOpen)
        .map(session ->
            session.close(CloseStatus.GOING_AWAY)
                .timeout(Duration.ofSeconds(3))
                .onErrorResume(e -> {
                    log.warn("强制关闭会话失败: {}", session.getId(), e);
                    return Mono.empty();
                })
        )
        .collect(Collectors.toList());

    Mono.when(closeTasks).block(Duration.ofSeconds(10)); // 阻塞等待最多10秒

    // 3. 同步清理所有设备状态
    offlineDevices.forEach((uid, clientIds) -> 
        clientIds.forEach(clientId -> syncOnline(uid, clientId, false))
    );

    // 4. 清空本地映射
    SESSION_USER_MAP.clear();
    SESSION_CLIENT_MAP.clear();
    USER_DEVICE_SESSION_MAP.clear();

    // 5. 清理路由与节点
    nacosSessionRegistry.cleanupNodeRoutes("");
}
```

## 八、核心流程图

### 8.1 用户上线流程

```
1. 客户端建立WebSocket连接
   ↓
2. ReactiveWebSocketHandler.handle()
   - 提取 clientId 和 uid
   ↓
3. SessionManager.registerSession()
   - 本地内存注册会话
   - 更新反向索引
   ↓
4. 判断是否首个设备
   ↓
5. NacosSessionRegistry.addUserRoute()
   - Redis Hash: 设备→节点映射
   - Redis Set: 节点→设备映射
   ↓
6. SessionManager.syncOnline(uid, clientId, true)
   - 添加到全局在线设备 ZSet
   - 如果是首个设备，添加到全局在线用户 ZSet
   - 更新群组在线状态
   ↓
7. pushDeviceStatusChange()
   - 推送给所有好友
   - 推送给所有群成员
```


### 8.2 用户下线流程

```
1. WebSocket连接断开
   ↓
2. SessionManager.cleanupSession()
   - 关闭会话
   - 移除反向索引
   ↓
3. cleanDeviceSession()
   - 原子化清理设备会话
   - 判断是否最后一个会话
   ↓
4. 如果是最后一个会话
   ↓
5. NacosSessionRegistry.removeDeviceRoute()
   - 清理 Redis Hash 映射
   - 清理 Redis Set 映射
   ↓
6. SessionManager.syncOnline(uid, clientId, false)
   - 从全局在线设备 ZSet 移除
   - 如果是最后一个设备，从全局在线用户 ZSet 移除
   - 更新群组在线状态
   ↓
7. pushDeviceStatusChange()
   - 推送离线通知给所有好友
   - 推送离线通知给所有群成员
```

### 8.3 消息推送流程

```
1. PushService.sendAsync(msg, uids, cuid)
   ↓
2. NacosRouterService.findNodeDeviceUser(uids)
   - HSCAN 遍历全局设备-节点映射
   - 过滤活跃节点
   - 构建：节点 → 设备 → 用户 映射
   ↓
3. 按节点分组并行推送
   ↓
4a. 本地节点：localPush()
    - 响应式并行推送
    - 超时控制（5秒）
    ↓
4b. 远程节点：sendToNodeViaMQ()
    - RocketMQ 发送到节点专属主题
    - 主题格式：websocket_push_{nodeId}
    ↓
5. 目标节点消费MQ消息
   ↓
6. SessionManager.sendToDevice()
   - 查找本地会话映射
   - 推送到具体 WebSocket 会话
```

## 九、性能优化策略

### 9.1 缓存优化

1. **分层缓存**
   - 本地内存：会话映射（ConcurrentHashMap）
   - Redis：路由信息和在线状态

2. **批量操作**
   - 使用 Redis Pipeline 批量查询
   - 群组推送分批处理（每批200人）

3. **游标扫描**
   - 使用 HSCAN 代替 HGETALL
   - 使用 SCAN 代替 KEYS
   - 避免阻塞 Redis

### 9.2 并发优化

1. **响应式编程**
   - WebFlux + Reactor 异步非阻塞
   - 动态并行度调整（最大32线程）

2. **线程池隔离**
   - 每个节点独立线程池
   - 有界队列防止 OOM
   - CallerRunsPolicy 拒绝策略

3. **原子操作**
   - ConcurrentHashMap.compute() 保证原子性
   - Redisson 分布式锁（syncOnline）

### 9.3 网络优化

1. **精准路由**
   - 避免广播风暴
   - 直接推送到目标节点
   - 减少网络开销

2. **消息压缩**
   - 批量推送合并
   - 减少 MQ 消息数量

3. **超时控制**
   - 推送超时 5 秒
   - 会话关闭超时 3 秒
   - 节点清理超时 10 秒


## 十、容错与高可用

### 10.1 节点故障处理

1. **心跳检测**
   - Nacos 健康检查（5秒间隔）
   - 节点元数据实时更新

2. **故障转移**
   - NodeDownMessageListener 监听节点下线
   - 自动清理残留路由
   - 通知客户端重连

3. **残留数据清理**
   - 定时任务（30秒）对比 Nacos 和 Redis
   - 清理僵尸节点数据

### 10.2 会话恢复

1. **客户端重连**
   - 携带原 clientId
   - 自动恢复路由信息

2. **状态同步**
   - 重连后重新同步在线状态
   - 推送未读消息

### 10.3 数据一致性

1. **分布式锁**
   - syncOnline 使用 Redisson 锁
   - 防止并发状态冲突

2. **原子操作**
   - Redis 事务保证
   - ConcurrentHashMap 原子更新

3. **最终一致性**
   - 定时清理任务兜底
   - 异步推送失败重试

## 十一、关键技术点总结

### 11.1 多设备管理

| 特性 | 实现方式 |
|------|---------|
| 设备标识 | uid:clientId 组合键 |
| 会话管理 | 三级映射：用户→设备→会话集合 |
| 路由存储 | Redis Hash + Set 双向映射 |
| 并发控制 | ConcurrentHashMap + 原子操作 |

### 11.2 在线状态管理

| 特性 | 实现方式 |
|------|---------|
| 状态存储 | Redis ZSet（带时间戳） |
| 多设备判断 | 首个设备上线/最后设备下线 |
| 群组状态 | Redis Set 存储在线成员 |
| 状态推送 | 反向好友列表 + 批量推送 |

### 11.3 消息路由

| 特性 | 实现方式 |
|------|---------|
| 路由查询 | HSCAN 游标扫描 |
| 本地推送 | Reactor 响应式并行 |
| 跨节点推送 | RocketMQ 节点专属主题 |
| 性能优化 | 精准路由 + 批量操作 |

### 11.4 容错机制

| 特性 | 实现方式 |
|------|---------|
| 节点监控 | Nacos 健康检查 + 心跳 |
| 故障恢复 | 节点下线监听器 |
| 数据清理 | 定时任务 + 残留路由清理 |
| 会话恢复 | 客户端重连 + 状态同步 |

## 十二、性能对比

### 12.1 广播模式 vs 精准路由模式

| 指标 | 广播模式 | 精准路由模式 | 提升倍数 |
|------|---------|-------------|---------|
| 网络消息数 | O(N) | O(k) | 10-100倍 |
| CPU消耗 | 高 | 低 | 5-20倍 |
| 内存占用 | 全节点缓存 | 仅目标节点 | 3-10倍 |
| 延迟时间 | 不稳定 | 稳定低延迟 | 2-5倍 |
| 平均延迟 | >100ms | <50ms | - |

**说明**：
- N：总节点数
- k：目标用户所在节点数（通常 k << N）

### 12.2 系统扩展性

1. **用户增长**：增加用户不会增加单个消息的复杂度
2. **节点扩展**：增加节点不会增加单消息的推送成本
3. **流量增长**：系统吞吐量随节点数线性增长

## 十三、最佳实践建议

### 13.1 部署建议

1. **节点配置**
   - 每个节点配置唯一 nodeId
   - 合理设置线程池参数
   - 监控节点健康状态

2. **Redis 配置**
   - 使用 Redis Cluster 提高可用性
   - 设置合理的过期时间
   - 定期清理过期数据

3. **Nacos 配置**
   - 配置健康检查间隔
   - 设置合理的心跳超时
   - 启用持久化实例

### 13.2 监控指标

1. **会话指标**
   - 在线用户数
   - 设备连接数
   - 会话创建/销毁速率

2. **性能指标**
   - 消息推送延迟
   - Redis 操作耗时
   - 线程池队列长度

3. **故障指标**
   - 节点下线次数
   - 会话异常断开率
   - 路由清理次数

### 13.3 优化建议

1. **减少 Redis 访问**
   - 使用本地缓存
   - 批量操作
   - Pipeline 优化

2. **优化推送策略**
   - 合并相同消息
   - 延迟批量推送
   - 压缩消息体

3. **提升并发能力**
   - 增加节点数量
   - 优化线程池配置
   - 使用响应式编程

## 十四、总结

HuLa-Server 的多设备和在线离线状态管理采用了以下核心设计：

1. **三级映射体系**：用户→设备→会话，实现精细化管理
2. **双向路由存储**：设备→节点 + 节点→设备，快速查询
3. **首尾设备判断**：只在首个设备上线和最后设备下线时更新用户状态
4. **精准路由推送**：避免广播风暴，直接推送到目标节点
5. **响应式架构**：WebFlux + Reactor 实现高并发低延迟
6. **完善的容错机制**：节点监控、故障转移、数据清理

这套架构在保证功能完整性的同时，实现了高性能、高可用和良好的扩展性。
