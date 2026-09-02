# Tez-测试

**重视测试**



![image-20251028201736015](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251028201736015.png)



一个环境有bug 另一个环境可能就没有bug了

![image-20251030222806129](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251030222806129.png)	



![image-20251030222921064](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251030222921064.png)





![image-20251030223147349](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251030223147349.png)

![image-20251030223740846](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251030223740846.png)



## ==单元测试==

在单元测试时，由于单元本身不是一个独立的程序，一个完整的可运行的软件系统并没有构成，所以需要设置一些辅助测试单元，辅助测试单元有两种，一种是驱动单元，另外一种是桩单元。

**1、驱动单元（Driver）**：用来模拟被测单元的上层单元，相当于被测函数的主函数，如main函数。所以驱动单元主要完成以下4个步骤：

（1）接受测试数据，包含测试用例输入和预期输出；

（2）把测试用例输入传送给被测单元，驱动被测单元测试；

（3）将被测单元的实际输出和预期输出进行比较，得到测试结果；

（4）将测试结果输出到指定位置。

**2、桩单元（Stub）**：用来代替被测单元工作过程中调用的子单元。

桩单元模拟的单元可能是自定义函数：这些自定义函数可能尚未编写完成，为了测试被测单元，需要构造桩单元来代替它们，可能存在错误，会影响测试结果，所以需要构造正确无误的桩单元来达到隔离的目的。

驱动单元和桩单元都是额外的开销，虽然在单元测试的时候必须写，但是并不需要作为最终的产品提供给客户。





---



# DevOps

不输入端口 **http 默认就是80端口** 

**https就是  443**

![s](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251028203327670.png)

![image-20251028211802120](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251028211802120.png)

## CI/CD

![image-20251028204126861](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251028204126861.png)

# 日志与监控平台 （云服务 VS 本地）

## 日志

**日志收集、分析、可视化平台**

![image-20251030205614557](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251030205614557.png)

| 组件                                         | 作用                                                         | 常见使用场景                                                 |
| -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Sleuth（Spring Cloud Sleuth）**            | Spring 官方提供的链路追踪框架，负责在日志中自动注入 TraceId / SpanId，让同一请求的日志能被串起来。 | 适合 Spring Cloud 微服务体系。通常搭配 Zipkin、ELK 或 SkyWalking 使用。 |
| **ELK（Elasticsearch + Logstash + Kibana）** | 不是专门的链路追踪框架，而是一整套日志采集、存储和可视化解决方案。<br>你可以把 Sleuth 生成的 TraceId 日志送入 ELK，用 Kibana 查询同一 Trace 的完整日志流。 | 主要用于集中式日志分析和可视化。                             |
| **SkyWalking**                               | 国产开源的分布式追踪 + 性能监控平台。可自动埋点、采样、上报 Trace 信息，不依赖日志系统。<br>能在 UI 上直接展示调用拓扑图、响应时间、错误率等。 | 比 ELK 更“智能”的 APM（应用性能监控）工具。                  |

MDC 本质就是个**日志系统**里的**“线程上下文变量存储器”**

Sleuth 生效的前提是：

1. **Spring 容器加载时，自动注册 AOP 切面**
   - 对 `@RestController`、`@Async`、`RestTemplate`、`FeignClient`、`RabbitTemplate` 等类进行增强。
2. **通过 `brave.Tracer` 管理 Trace 上下文**
   - Sleuth 内部依赖了 Brave 库，它负责生成 TraceId、SpanId 并将它们放入 MDC。
3. **Logback/Log4j2 输出时读取 MDC 信息**
   - 所以日志里会出现 traceId、spanId。

---



Spring Boot 的 **`/actuator/loggers`** 端点是一个**动态调整日志级别**的管理接口。

- 无需重启应用，就能在线改变包或类的日志级别，比如从 `INFO` 切到 `DEBUG`。
- 通常结合 Spring Boot Admin 或 Prometheus 管控平台使用。



Elasticsearch 经常需要**被前端页面（浏览器端）直接调用 API**，而浏览器有 “同源策略” 限制（只有协议、域名、端口完全一致的请求才被允许）。



## 监控平台

Java Agent 是 Java 提供的一种**字节码增强技术**，本质是一个特殊的 Java 程序（`.jar` 文件），通过 `-javaagent` 命令参数在目标 JVM 启动时或运行中加载，能够在不修改目标应用源码的前提下，对其字节码进行修改、增强或监控。

它的核心能力是**在类加载阶段拦截并修改类的字节码**（基于 Instrumentation API），实现对目标应用的 “无侵入式” 增强。

**Jrebel 热部署插件**



---



 **Java Agent 的作用**

- **无侵入监控**：收集应用运行数据（如方法调用耗时、异常信息、线程状态），用于性能分析、链路追踪（如 SkyWalking、Pinpoint）。
- **字节码增强**：动态修改类逻辑（如添加日志、权限校验、缓存逻辑），无需修改源码。
- **热部署 / 热更新**：运行时替换类的字节码，实现代码更新不重启应用。
- **安全审计**：拦截敏感操作（如文件读写、数据库访问），记录审计日志。



| 类型                     | 代表组件                                                   | 主要作用                                               | 优势                                 | 局限                                                      |
| ------------------------ | ---------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------ | --------------------------------------------------------- |
| **指标监控（Metrics）**  | **Prometheus + Grafana**                                   | 采集、存储**系统指标**（CPU、内存、QPS、延迟）并可视化 | 高效、拉模式采集、安全性好、社区强大 | 时序数据存储占空间，历史数据持久化需远端存储（如 Thanos） |
| **日志监控（Logs）**     | **ELK / EFK**（Elasticsearch + Logstash/Fluentd + Kibana） | **收集、集中化存储和检索日志**                         | 支持全文检索、聚合分析、界面直观     | 资源占用大、Elasticsearch 集群维护复杂                    |
| **链路追踪（Traces）**   | **SkyWalking / Zipkin / Jaeger**                           | **跟踪分布式请求路径，分析调用链性能瓶颈**             | 端到端可视化、可与 Prometheus 集成   | 初期接入成本高，Trace 数据量庞大                          |
| **系统监控（Infra）**    | **Node Exporter / cAdvisor / Zabbix / Nagios**             | **监控主机、网络、硬盘、服务状态**                     | 成熟稳定、适合传统架构               | 与云原生环境整合度较低                                    |
| **APM（应用性能监控）**  | **SkyWalking / Pinpoint / NewRelic / Datadog**             | **自动追踪 JVM、SQL、HTTP 性能指标**                   | 提供性能瓶颈分析、智能告警           | 企业版或 SaaS 成本较高                                    |
| **告警系统（Alerting）** | **Alertmanager / Grafana Alert / Zabbix Alert**            | **将异常指标转化为消息通知**                           | 支持自定义规则、Webhook 集成         | 规则复杂度高，调优门槛大                                  |