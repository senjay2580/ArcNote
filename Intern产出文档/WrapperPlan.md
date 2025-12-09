```ad-attention
1.你们组的业务是什么 组有几个人 团队如何合作的 你负责什么 你的工作内容是什么

2.你在实习期间参与的项目是为了解决什么问题的？

3.从技术角度上讲，他是如何解决这个问题的？

技术是聊出来的！

大家一定先是朋友，再是老师。一开始不要什么都扯着个大嘴问，先自己思考，大家没有这个义务帮你解答你自己在工作中的困惑。

1.这个需求的产生背景是什么？这个需求开发完了之后能带来什么提升？能不能找到对应的PRD？

2.这个需求的技术选型是怎么做的？为什么在这里用了A技术？除了A技术之外自己能不能思考一下是否可以用其他的技术写出来？那么做这个需求的员工使用A技术的原因是什么？（方案调研+技术选型）

3.这个需求的对应PR有吗？能不能找到具体的代码。自己要细看一遍代码。

一般来讲大家遇到线上事故之后都会写复盘文档的。可以看一看这些复盘文档。从复盘文档中侧重学习两个东西：

1.是什么操作引起了这个线上事故？

2.当线上事故发生了之后，事故负责人是如何解决的？解决不仅仅包括事后对于相关代码的修改，更包括当这个事故发生在线上的时候，线上的处理方法是什么？


人都是有思维盲点的，有些很常见的问题可能你在公司偷产出的时候就是没有考虑到。	因此我们要找一个面试官来拷打我们的实习内容，不要害怕被面试官拷打。为什么？
因为我们现在还在公司！所有不会的问题都可以在公司中和mt/实习生的交流来获得答案。因此不要等到你离职了之后才开始写简历和面试。
```




# NEWLAND

1、调用统一综合门户提供用户、角色、群组的基础数据接口实现统一综合门户接入访问 -- 门户关于统一的权限 其他子系统使用这个权限 外部接口对接方案 (**单点登录**)

[单点登录教程 包含Oauth2](https://cloud.iocoder.cn/oauth2/#%E5%AE%9E%E6%88%98%E4%B8%80-%E5%9F%BA%E4%BA%8E%E6%8E%88%E6%9D%83%E7%A0%81%E6%A8%A1%E5%BC%8F-%E5%AE%9E%E7%8E%B0-sso-%E5%8D%95%E7%82%B9%E7%99%BB%E5%BD%95)

数据清理聚合分析 	**治理** 大数据 ETL datawork    数仓





# HND

数据统计大数据量优化 包装·

**定时任务 + 预聚合表” 替代实时全表计算（离线计算思维）**

1. **用 “MySQL 分区表 + 历史数据归档” 解决存储问题（分层存储思维）**
   - 技术实现：“将原始订单表按‘年’做 RANGE 分区，同时开发 Java 归档工具：每年初将前 2 年的分区数据导出为 Parquet 文件（用 Java 的 Apache Parquet 库），存储到 MinIO（轻量对象存储），MySQL 仅保留近 1 年数据；如需查询历史数据，通过工具从 MinIO 读取并解析，再与 MySQL 近 1 年数据合并计算”；
   - 效果：“MySQL 磁盘占用从 100GB 降至 30GB，历史数据查询虽延迟至秒级，但满足低频分析需求，存储成本降低 70%”。

- “后续当数据量突破 1 亿行，计划引入：
  - 数据采集：用 Canal（Java 开发的 Binlog 同步工具）实时同步 MySQL 数据到 Kafka，避免直接访问主库；
  - 实时计算：用 Flink Java API 开发实时统计任务，计算‘实时交易额’等核心指标，结果写入 ClickHouse；
  - 离线分析：用 Spark SQL（Java API）处理历史数据，生成周 / 月报表，结果存 Hive，通过 Presto 对接 BI 工具；
  - 最终形成‘实时 + 离线’的双层统计架构，支撑高并发查询和深度数据分析”。

系统：

**统计sql慢接口优化 历程 和sql 优化各种 操作** 要体现思考的流程 

sse 实时更新统计信息

锁优化

配置线程池异步发送短信

**状态机** 审批流程 要体现 自研和优化 历程

**RBAC** 

未来优化 缓存 和 索引 消息队列（线程池问题）

# EDNOVA

RBAC 定制 数据权限 多租户



多数据源 AOP 



**分布式锁**

# Archat
接口开发流程熟悉--敏感词过滤接口实战

**理论到代码架构的实现与实践 如 Rbac Oauth2**

**云岚到家**项目文档熟悉一下

**AI 探索** coltea and **agent**

配置ai规则 ide 网页 dia浏览器 （目前是由mac 看看win有无插件什么的） 飞书玩法！！ 特别是 API 集成 工作流继续探索
用户在线状态可以用缓存来维护
多数据源 archat 功能；特别是AI很重要；
mongo db 持久化ai消息 多数据源 ~~
AI 沟通洞察 分析你的沟通模式，建议更好的表达方式。智能理解上下文，预测下一步该说什么，让对话更加高效。 
多端同步 在所有设备上无缝同步你的笔记、通话和 AI 对话，实时更新。 
内置文档协作 集成的文档工具和工作流自动化，旨在提高生产力，简化团队协作。

结合blinko 再结合自己的方式 AI 笔记tag ai整理笔记内容也可生成笔记 分享外链 导出pdf 开发自己的API 允许外部系统调用这个接口


**concurrenthashmap 八股**

~~~java
public class MsgHandlerFactory {
    // 使用了普通的 HashMap
    private static final Map<Integer, AbstractMsgHandler> STRATEGY_MAP = new HashMap<>();
    
    public static void register(Integer code, AbstractMsgHandler strategy) {
        // 检查是否已存在
        if (STRATEGY_MAP.containsKey(code)) {
            throw new IllegalArgumentException("重复注册消息处理器: " + code);
        }
        // 如果不存在，则放入 Map
        STRATEGY_MAP.put(code, strategy);
    }
}
~~~



## 优化点

为什么要使用netty

策略模式 (Strategy Pattern) 注册式工厂

**使用场景**: 消息处理、频率控制

- ✅ 支持动态注册策略
- ✅ 代码扩展性好
- ✅ 符合开闭原则

- ❌ 缺少策略验证机制
- ❌ 工厂类职责过重

- ❌ 线程安全问题 (HashMap非线程安全)
- ❌ 缺少重复注册检查
- ❌ 没有提供注销机制



**模板方法模式 (Template Method Pattern)**

~~~java
public abstract class AbstractMsgHandler<MsgType> {
    @Transactional
    public Long checkAndSaveMsg(ChatMessageReq request, Long uid) {
        // 1. 统一校验
        MsgType body = this.toBean(request.getBody());
        AssertUtil.allCheckValidateThrow(body);
        
        // 2. 子类扩展校验
        checkMsg(body, request.getRoomId(), uid);
        
        // 3. 统一保存
        Message insert = MessageAdapter.buildMsgSave(request, uid);
        messageDao.save(insert);
        
        // 4. 子类扩展保存
        saveMsg(insert, body);
        
        return insert.getId();
    }
    
    // 抽象方法由子类实现
    protected abstract void checkMsg(MsgType body, Long roomId, Long uid);
    public abstract void saveMsg(Message msg, MsgType body);
}
~~~



### 1. 消息发送流程

基于事件驱动架构实现敏感词过滤和消息异步处理，确保内容安全合规。 **ddd 领域**

**当前流程**:

```
1. 接收消息请求 (ChatController)
2. 权限校验 (ChatServiceImpl.check)
3. 获取消息处理器 (MsgHandlerFactory)
4. 校验并保存消息 (AbstractMsgHandler.checkAndSaveMsg)
5. 发布消息事件 (ApplicationEventPublisher)
6. 异步推送消息 (MsgSendConsumer)
```

**问题分析**:

- ❌ **事务边界不清晰**: 消息保存和推送在不同事务中
- ❌ **失败重试机制**: 缺少消息发送失败的重试逻辑
- ❌ **消息去重**: 没有防止重复消息的机制
- ❌ **限流策略**: 频率控制实现复杂

---



**好友申请流程**

- ❌ **状态管理复杂**: 好友状态转换逻辑分散



**缓存架构**

**当前问题**:

- ❌ **缓存策略单一**: 只使用Redis
- ❌ **缓存一致性**: 缺少缓存更新策略
- ❌ **缓存穿透**: 没有防护机制



**监控告警** - 完善系统监控体系



数据库索引优化 还有 各种数据库优化操作



~~~java
// 1. 消息归档
@Component
public class MessageArchiveService {
    
    @Scheduled(cron = "0 0 2 * * ?") // 每天凌晨2点执行
    public void archiveOldMessages() {
        // 归档3个月前的消息到历史表
    }
}

// 2. 数据分析
@Component
public class ChatAnalyticsService {
    
    public void analyzeUserBehavior() {
        // 分析用户聊天行为
    }
    
    public void generateDailyReport() {
        // 生成日报
    }
}
~~~





**优化建议：**

- **使用SonarQube进行代码质量检查**
- **实施代码审查机制**
- **编写单元测试和集成测试**

- **定期安全扫描**
- **实施安全编码规范**
- **建立安全事件响应机制**



- **采用渐进式重构策略**
- **实施蓝绿部署**
- **建立完善的CI/CD流程**



- **集成APM工具（如SkyWalking）**
- **建立性能基线**
- **实施性能测试自动化**





---



**参考ednova** 

异步线程池 问题解决 利用装饰器解决上下文问题 还有异常问题



各种线程池八股使用 并发安全 线程依赖（任务编排）等等 



分布式异步任务问题  **分布式锁**

---



多级缓存 缓存一致性 caffeine   + redis + spring cache

敏感词定制



限流接口开发



多数据源切换 实现mysql 和 mongodb 多个表 适配各自适合的业务场景



# Coltea - icon

- 把好几个模型的调用全都写进同一个接口里，用适配器来转换  **是不是可以用AOP -我的想法**
- 但是根本找不到这种综合大模型的调用接口，只能几个大模型缝起来
- 这个路由就很难做了





- 主导 SQL Server 国产数据库 PolarDB 的迁移，优化视图定义，迁移过程耗时一周并实现零数据丢失

- 基于 Easy Excel 解决 40W 条数据导出 Excel 文件时出现的 JVM 堆内存溢出问题，导出时间缩短至 90s

- 通过定制开发 Spring Security 的 AuthenticationProvider 实现类，建立短信验证码登录体系
- 设计并实现 [功能]，通过添加 Mysql 索引、优化 SQL 查询、引入批处理机制，将处理时间从 15h 压缩至 30s

- 基于 FFmpeg 进行视频转码，结合 XXLJob 分片广播任务调度，构建分布式并行处理架构，使转码任务吞吐量提升 5 倍

- 集成 Minio 实现分块上传与断点续传，确保视频上传的稳定性并显著提高了大文件上传的速度
- 应用 RabbitMQ 实现核心业务（如支付成功通知）的异步解耦，通过消息确认、持久化等机制保障消息的可靠传递与最终一致性

- 使用 Redisson **分布式锁，**解决了数字内容缓存信息缓存击穿问题
- redis 数据结构 geo set共同好友 setnx




---



他不管你是公司不好，还是个人能力不行，在生产环境学不到东西，这都是不被认可的。这个时候就要用一些特殊的方法了，第一个项目中含金量不错，有数据迁移，还有大数据量的相关内容，可以把这部分包装到自己的实习经历中，只要能和你的业务讲通，不被发现就行，不要耻于不敢包装，大家都包装，你不包装的话，那会落后别人很多。

**实习经历，至少要写 5，6 条，并且前 2 到 3 条是含金量要高的**，可以把你的项目经历包装进去，比如你用某两个技术实现了一个和业务相关的一个亮点，**然后再加一些数字进去，像大数据量或者是性能优化，或者是 QPS 的提升，这样包装完后，面试绝对不会少**

