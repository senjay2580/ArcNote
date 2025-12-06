| 类型         | 阻塞 IO（传统 HTTP 请求）                     | 非阻塞 IO（异步）                       |
| ------------ | --------------------------------------------- | --------------------------------------- |
| 是否阻塞线程 | 是                                            | 否                                      |
| 性能         | 每个请求占用一个线程                          | 更高效（更少线程）                      |
| 常见实现     | `HttpURLConnection`, `OkHttp`, `RestTemplate` | `WebClient`, `Netty`, `AsyncHttpClient` |

一个channel 就对应着一个在线的用户连接

根据用户id 拿到通道channel 然后 就用 channel writeAndFlush到缓冲区 ==》客户端

问题就是将uid 和 channel连接绑定！！！





![69ae0c22511300bfc94ff8c850b6db4](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/69ae0c22511300bfc94ff8c850b6db4.png)

这个问题问得太好了！我给你理一个 **典型的前后端使用 WebSocket 聊天的流程**，从登录到上线，再到聊天，什么时候触发 WebSocket 连接、数据怎么流转，流程都清晰说明。

---

# 🌐 WebSocket 聊天系统的前后端流程示例

---

## 1. 用户打开客户端（浏览器或App）

* 这个时候，用户还没登录，前端一般显示登录界面。

---

## 2. 用户填写账号密码，点击登录（HTTP 请求）

* **前端**通过 HTTP POST 请求调用后端登录接口，提交用户名和密码。
* **后端**验证用户名和密码：

  * 成功：返回一个登录令牌（如 JWT token）或会话 ID。
  * 失败：返回错误信息。

---

## 3. 登录成功后，前端保存登录状态

* 前端拿到 token 后，一般存在 `localStorage` 或内存里，标记用户“已登录”状态。
* 这时还没有 WebSocket 连接。

---

## 4. 触发 WebSocket 连接（用户上线）

* **前端**拿到 token 后，主动打开 WebSocket 连接，通常写在登录成功回调里：

```js
const token = localStorage.getItem("token");
const ws = new WebSocket(`ws://example.com/ws?token=${token}`);
```

* 也可以把 token 放在请求头（浏览器里比较麻烦，需要额外封装），URL 参数是最常见方式。

---

## 5. 后端接收到 WebSocket 握手请求

* 后端 Netty 的 `HttpHeadersHandler` 或其他 Handler 拿到握手请求（HTTP Upgrade 请求）。
* **从 URL 或请求头中解析出 token，验证 token 合法性。**
  * **合法：允许握手，建立 WebSocket 连接。**
  * **不合法：拒绝握手，关闭连接。**

---

## 6. WebSocket 连接建立完成

* **后端给这个连接分配一个 `Channel`，并绑定用户身份（token、UID、IP等）。**   <span style="color:#FF0000;">**绑定！！！！**</span>
* 前端和后端都进入“在线”状态。
* 后端可以广播通知其他用户，告诉他们这个用户上线了。<span style="color:#FF0000;">**事件通知**</span>

---

## 7. 用户开始聊天（WebSocket 消息收发）

* **<span style="color:#FF0000;">前端通过 `ws.send()` 发送聊天消息。</span>**
* **<span style="color:#FF0000;">后端收到 WebSocket 消息，在对应的 `ChannelHandler` 里处理：</span>**
  * **<span style="color:#FF0000;">解析消息内容。</span>**
  * **<span style="color:#FF0000;">判断发送目标（私聊还是群聊）。</span>**
  * **<span style="color:#FF0000;">转发消息给目标用户的 `Channel`。</span>**
* **<span style="color:#FF0000;">目标用户的前端接收到 WebSocket 消息事件，显示聊天内容。</span>**

---

## 8. 用户关闭页面或登出

* **前端**关闭 WebSocket 连接，或者调用登出接口。
* **后端**收到连接关闭事件，清理 `Channel` 绑定信息，通知其他用户该用户离线。

---

# 📋 关键时机总结

| 时机           | 动作                            | 通信协议       |
| -------------- | ------------------------------- | -------------- |
| 登录请求       | HTTP POST 提交账号密码          | HTTP/HTTPS     |
| 登录成功后     | 保存 token，触发 WebSocket 连接 | WebSocket      |
| 建立连接       | 服务器验证 token，握手成功      | WebSocket      |
| 聊天消息收发   | 双向消息实时传输                | WebSocket      |
| 关闭连接或登出 | 断开连接，清理状态              | WebSocket/HTTP |

---

# 💡 额外提示

* **为什么登录和 WebSocket 连接分开？**
  登录用 HTTP 请求，流程简单，适合鉴权。WebSocket 负责长连接，实时通信。

* **token 作用**
  作为鉴权凭证，防止未授权用户连接。

* **重连机制**
  如果 WebSocket 断开，前端一般会尝试自动重连。

---



前端通过 监听 WebSocket 消息（onmessage 事件） 来接收服务端发送过来的 JSON 格式的响应，并根据消息中的 type 字段判断响应类型，从而决定要执行什么操作。

~~~java
package com.senjay.archat.common.service.adapter;

import com.senjay.archat.common.chat.domain.enums.WSRespTypeEnum;
import com.senjay.archat.common.chat.domain.vo.response.WSBaseResp;
import com.senjay.archat.common.chat.domain.vo.response.WSLoginSuccess;
import com.senjay.archat.common.chat.domain.vo.response.WSLoginUrl;
import com.senjay.archat.common.user.domain.entity.User;

//它相当于一个“数据适配器”或“消息模板工厂”，用于把 Java 中的业务数据（比如用户对象、状态等）转换成统一格式的 WebSocket 响应对象 WSBaseResp<T>，然后你可以通过 WebSocket 发给前端。
public class WSAdapter {

    public static WSBaseResp<WSLoginSuccess> buildLoginSuccessResp(User user, String token, boolean hasPower) {
        WSBaseResp<WSLoginSuccess> wsBaseResp = new WSBaseResp<>();
        wsBaseResp.setType(WSRespTypeEnum.LOGIN_SUCCESS.getType());
        WSLoginSuccess wsLoginSuccess = WSLoginSuccess.builder()
                .avatar(user.getAvatar())
                .name(user.getUsername())
                .token(token)
                .uid(user.getId())
                .build();
        wsBaseResp.setData(wsLoginSuccess);
        return wsBaseResp;
    }
    public static WSBaseResp<WSLoginSuccess> buildInvalidateTokenResp() {
        WSBaseResp<WSLoginSuccess> wsBaseResp = new WSBaseResp<>();
        wsBaseResp.setType(WSRespTypeEnum.INVALIDATE_TOKEN.getType());
        return wsBaseResp;
    }
}

~~~

~~~java
/**
 * Description: ws的基本返回信息体

 */
@Data
public class WSBaseResp<T> {
    /**
     * ws推送给前端的消息  就和result 类似
     *
     */
    private Integer type;
    private T data;
}


/**
 * Description: ws前端请求类型枚举
 * Author: <a href="https://github.com/zongzibinbin">abin</a>
 * Date: 2023-03-19
 */
@AllArgsConstructor
@Getter
public enum WSRespTypeEnum {
    LOGIN_URL(1, "登录二维码返回", WSLoginUrl.class),
    LOGIN_SCAN_SUCCESS(2, "用户扫描成功等待授权", null),
    LOGIN_SUCCESS(3, "用户登录成功返回用户信息", WSLoginSuccess.class),
    MESSAGE(4, "新消息", WSMessage.class),
    ONLINE_OFFLINE_NOTIFY(5, "上下线通知", WSOnlineOfflineNotify.class),
    INVALIDATE_TOKEN(6, "使前端的token失效，意味着前端需要重新登录", null),
    BLACK(7, "拉黑用户", WSBlack.class),
    MARK(8, "消息标记", WSMsgMark.class),
    RECALL(9, "消息撤回", WSMsgRecall.class),
    APPLY(10, "好友申请", WSFriendApply.class),
    MEMBER_CHANGE(11, "成员变动", WSMemberChange.class),
    ;

    private final Integer type;
    private final String desc;
    private final Class dataClass;

    private static Map<Integer, WSRespTypeEnum> cache;

    static {
        cache = Arrays.stream(WSRespTypeEnum.values()).collect(Collectors.toMap(WSRespTypeEnum::getType, Function.identity()));
    }

    public static WSRespTypeEnum of(Integer type) {
        return cache.get(type);
    }
}

~~~



---



非常好的问题！**结合消息队列与消息推送系统**可以极大提升系统的**可扩展性、稳定性与解耦性**，这是大型系统（如 MallChat、企业 IM、直播弹幕系统）常用的架构方式。

---

![image-20250608234037527](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250608234037527.png)

![image-20250608234130148](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250608234130148.png)

![image-20250608234609138](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250608234609138.png)

![image-20250608235124513](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250608235124513.png)



---



## 🎯==消息队列相关==

> **用户发送消息 → 写入消息队列（MQ） → 异步消费 → 推送消息 + 写数据库 + 发通知 等后续操作**

---

## 🧱 架构图概览

```
                ┌────────────┐
                │  用户前端  │
                └─────┬──────┘
                      │
              WebSocket / HTTP
                      │
              ┌───────▼────────┐
              │  网关 / 接收层 │
              └───────┬────────┘
                      │
        ┌─────────────▼──────────────┐
        │   发送消息请求入消息队列   │ ← RabbitMQ / Kafka / RocketMQ
        └─────────────┬──────────────┘
                      │
          ┌───────────▼────────────┐
          │    消息消费模块（异步） │
          └────┬────────────┬──────┘
               │            │
       ┌───────▼───┐   ┌────▼─────────┐
       │ 写入数据库 │   │ 推送在线好友 │
       └───────────┘   └──────────────┘
```

---

## 📦 实际 Java 开发中各模块说明

### 1. 用户发送消息 → 写入 MQ

用户通过 WebSocket 发消息：

```json
{
  "type": 4,
  "data": {
    "toUserId": 2,
    "msg": "你好！"
  }
}
```

后端接收后只做一件事：

```java
ChatMessage chatMsg = new ChatMessage(...);
rabbitTemplate.convertAndSend("chat.exchange", "chat.route", chatMsg);
```

> ✅ 好处：避免业务耦合/阻塞，后续操作全部交给“消息消费者”。

---

### 2. 消费者异步消费消息（Consumer）

```java
@RabbitListener(queues = "chat.queue")
public void onMessage(ChatMessage msg) {
    // 写入数据库
    chatMessageService.save(msg);

    // 推送给接收人（在线才推）
    pushToOnlineUser(msg.getToUserId(), msg);

    // 可以附带发通知、发邮件等
}
```

---

### 3. 推送在线好友（Netty 维持在线通道）

通过后端保存的 `Map<Long, List<Channel>> onlineMap` 推送：

```java
List<Channel> channels = OnlineHolder.getChannels(msg.getToUserId());
if (channels != null) {
    for (Channel ch : channels) {
        ch.writeAndFlush(new TextWebSocketFrame(JSONUtil.toJsonStr(msg)));
    }
}
```

---

## ✅ 为什么要用消息队列？

| 目标     | 是否达成 | 说明                                      |
| -------- | -------- | ----------------------------------------- |
| 解耦     | ✅        | 前端发送 → MQ，写库、推送、日志等完全分离 |
| 异步处理 | ✅        | 不阻塞用户请求，低延迟体验                |
| 容错     | ✅        | 消息可以重试、持久化、防丢失              |
| 可扩展   | ✅        | 多个消费者集群并行处理，支持高并发        |

---

## 💡 可选增强

1. **幂等性处理**（防重复消费）
2. **ACK 确认机制**：推送成功后用户客户端发回“收到”
3. **离线消息落库**：若用户不在线 → 存 redis / mysql
4. **消息状态更新**：如“未读、已读”标识
5. **消息撤回/删除功能**

---



# 



