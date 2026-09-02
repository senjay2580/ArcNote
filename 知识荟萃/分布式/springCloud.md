单体架构 -> 集群架构 -> 分布式架构

**分布式：一个大型应用被拆分成很多小应用分布部署在各个机器；工作方式**

**集群：物理形态**



**对于集群：**

![image-20250629105558939](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629105558939.png)



**对于分布式架构：**

![image-20250629105440481](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629105440481.png)

服务熔断（**Circuit Breaker**）是**微服务架构中一种用于提升系统稳定性和容错能力的机制**。它的核心思想来自于电路中的“保险丝”或“断路器”：当检测到某个服务频繁出错或响应超时，就**临时中断对该服务的调用请求**，==**避免系统资源被错误请求持续占用**==，进一步导致系统雪崩。

在分布式系统中，服务间常常互相调用：

- 如果某个下游服务（例如用户服务）因故障变得**响应慢**或**不可用**；
- 但上游服务（如订单服务）还在**持续发起请求**；
- 就可能导致线程阻塞、资源耗尽；
- 最终导致整个系统雪崩式崩溃。



---



在微服务中，每个服务对外请求一般有**线程池**或**连接池限制**（例如 Tomcat 的线程数、Hystrix 的隔离线程池）。

如果持续调用故障服务，会把线程都卡住（等待响应），造成**线程耗尽**。

熔断后不会再走阻塞路径，从而保住这些资源。





![image-20250629111425793](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629111425793.png)

**分布式事务**是指一个业务操作需要**跨越多个数据库或服务**，而这些参与者需要**保证整体事务的一致性**（ACID），就需要用到分布式事务控制。

**在单体系统中：**

- 所有模块都访问同一个数据库；
- 使用本地事务（如 JDBC 的事务、Spring 的 `@Transactional`）即可；
- 一个方法里插入订单表 + 扣减库存表，是**同一个数据库连接、同一个事务**。





由于业务拆分成了多个服务，比如：

| 服务     | 操作     | 使用数据库 |
| -------- | -------- | ---------- |
| 订单服务 | 创建订单 | order_db   |
| 库存服务 | 扣减库存 | stock_db   |
| 支付服务 | 扣款记录 | payment_db |



一个完整操作涉及多个微服务、多个数据库，于是就**不是同一个数据库连接**了。

> ➤ 这时候传统的本地事务就无法保证一致性了，**事务控制范围“跨了服务边界”**，这就形成了**分布式事务问题**。



数据库如何“分布式”？

主从复制（读写分离）

📌 1. 概念说明：

- **主库（Master）**：负责**写入操作**（INSERT / UPDATE / DELETE）
- **从库（Slave）**：负责**读取操作**（SELECT）
- **主库变动的数据**会自动同步给所有从库



| 微服务   | 数据库名   | 所在服务器（或主机组）     |
| -------- | ---------- | -------------------------- |
| 用户服务 | user_db    | 192.168.10.11              |
| 商品服务 | product_db | 192.168.10.12              |
| 订单服务 | order_db_x | 192.168.10.13 / 14（分库） |
| 库存服务 | stock_db   | 192.168.10.15              |
| 支付服务 | payment_db | 192.168.10.16              |

**任何项目的依赖管理都要版本适配要兼容**

![image-20250629112556113](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629112556113.png)

![image-20250629113842898](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629113842898.png)



![image-20250629112759957](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629112759957.png)



~~~xml
<packaging>pom</packaging> 是一种特殊的打包类型，用于聚合（管理）多个子模块项目
一般是在 作为父项目作为统一依赖管理使用的！！！
~~~

| 打包类型 | 用途说明                                   |
| -------- | ------------------------------------------ |
| `jar`    | 打包成 JAR 文件（Java 类库）               |
| `war`    | 打包成 WAR 文件（Web 应用）                |
| `pom`    | **不打包任何代码，仅作为父模块或聚合模块** |

![image-20250629113234392](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629113234392.png)

![image-20250629113348570](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629113348570.png)

**services也是管理子项目所以也不写代码**

**service就是放公共依赖**

**然后最上层的父项目就是仅仅管理==依赖版本==的**



---







![image-20250325200948720](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325200948720.png)



-mysql

​	-conf

​	-init

用于镜像提供初始化数据

**端口映射:**在运行 MySQL 容器时使用了-p参数将容器内部的 MySQL端口(通常是 3306)映射到虚拟机的外部端口。例如，docker run-p 3306:3306会将虚拟机的 3306端口与容器的 3306 端口连接起来从而允许外部设备通过虚拟机的IP 地址和端口访问 MySQL。

![image-20250325200950430](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325200950430.png)



# Maven POM文件re

父子工程继承的问题：

**`dependencyManagement`的作用**

- **功能**：`dependencyManagement`用于**声明依赖及其版本**，但不会直接引入依赖到子模块。它仅提供版本管理，子模块需要**显式声明依赖**（但可省略版本号）。
- **优点**：
  - **统一版本管理**：所有子模块可以共享父工程中定义的依赖版本，避免版本冲突。
  - **按需引入**：子模块仅声明需要的依赖，减少冗余。







---





type ： pom文件类型

import ： 导入这个pom文件 使用这个pom文件定义的依赖

**注意properties 标签和dependencyManagement标签**



![image-20250325202145655](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325202145655.png)







![image-20250325201158228](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325201158228.png)

![image-20250325201147436](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325201147436.png)

不要去改代码这里的active属性 不然就属于侵入式了

![image-20250325201247997](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325201247997.png)

如果代码量庞大，那每次修改编译的话 需要非常长的时间

然后如果有非常多用户对一个接口在同一时间段内访问的话，会导致这个接口并发过高然后Tomcat的资源就占用完了

最后导致用户访问其他接口的速度都变得慢了





![image-20250325201345927](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325201345927.png)

每个功能和模块都部署到了不同的服务上去 **都有自己的服务器和数据库去进行处理**

![image-20250325201913389](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250325201913389.png)

**springcloud最新版一般支持Springboot3这个依赖jdK17所以要明白版本之间的管理是否兼容**



# 微服务拆分

![image-20250328170414844](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328170414844.png)

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328170428951.png)



微服务工程结构：

![image-20250328170522658](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328170522658.png)

**一project 多 modules（maven聚合）**

一文件夹多project（独立project）

---



IDE中设置环境变量是会自动找到系统中对应的不用自己在本机中配置 但是部署的时候需要指定他是固定路径的（IDE会去找对应的）

~~~xml
		<dependency>
			<groupId>com.heima</groupId>
			<artifactId>hm-common</artifactId>
			<version>1.0.0</version>
		</dependency>
<!--		引入自己的依赖项-->
如何创建自己的maven依赖工程呢
~~~



**拆分注意：最重要的就是配置文件的配置 以及项目文件结构布局 还有项目文件的配置和代码 逻辑 以及pom文件的配置**

**还有启动项的问题 （以什么环境启动 端口有没有被占用）**



~~~java
// 启动类中写
package com.hmall.item;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan("com.hmall.item.mapper")  // 扫描
@SpringBootApplication
public class ItemApplication {
    public static void main(String[] args) {
        SpringApplication.run(ItemApplication.class, args);
    }
}
~~~



**传统方法：手动加 `@Mapper`**

你可以在每个 `Mapper` 接口上手动加 `@Mapper`，例如：

```java
@Mapper
public interface ItemMapper {
    Item selectById(Long id);
}
```

但是如果有很多 `Mapper`，每个都要加 `@Mapper`，就很麻烦。

也可以在配置文件中指定

---



配置文件中配置日志文件保存配置 whereby 让**不同的微服务日志**保存在**不同的目录**下

~~~yaml
logging:
  level:
    com.hmall: debug
  pattern:
    dateformat: HH:mm:ss:SSS
  file:
    path: "logs/${spring.application.name}"
~~~



~~~yaml
spring:
  application:
    name: item-service # 服务名称 服务注册要用来做服务发现 每一个微服务都有自己的名字
  profiles:
    active: dev
  datasource: 
    url: jdbc:mysql://${hm.db.host}:3306/hmall/item?useUnicode=true&characterEncoding=UTF-8&autoReconnect=true&serverTimezone=Asia/Shanghai
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: ${hm.db.pw}
~~~

每个**微服务**都对应一个数据库服务器（DBMS） 但在学习中我们对应每一个数据库（Database） 所以上面的url要对应着修改一下



这里的active 不要在这个配置文件中修改

**alt  + 8**  service 配置 中修改**启动** 的时候会以这个为准 



# 远程调用（RPC）

![image-20250328181641415](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328181641415.png)



也就是用一个微服务调用另一个微服务 whereby 每一服务单一职责 不要内容耦合

这个调用就是利用java代码发起HTTP请求



---



注入到spring的bean当中去

![image-20250328181859626](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328181859626.png)



会将查到的json字符串反序列化为java对象

但是这种带泛型的就不行了 因为字节码中没有泛型 

所以这种情况就无法传字节码了

![image-20250328191921169](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328191921169.png)



将集合转化为逗号隔开的字符串

请求有可能失败

查询到的参数有可能指针涉空



![image-20250328192345835](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328192345835.png)









---



lombok @RequiredArgsConstructor

作用就是只 only 仅仅 给加了final 的成员变量依赖注入

cause 相比于 @Autowired 使用构造函数依赖注入更好 为了方便不用写构造函数就用上面的注解即可

---

# Nacos



![image-20250328192440973](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328192440973.png)



**配置nacos（docker）**



~~~conf
PREFER_HOST_MODE=hostname
MODE=standalone
SPRING_DATASOURCE_PLATFORM=mysql
MYSQL_SERVICE_HOST=192.168.254.128
MYSQL_SERVICE_DB_NAME=nacos
MYSQL_SERVICE_PORT=3307
MYSQL_SERVICE_USER=root
MYSQL_SERVICE_PASSWORD=123456
MYSQL_SERVICE_DB_PARAM=characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai
~~~

将custom.env 放到目录 然后在当前目录：

~~~bash
docker run -d \
--name nacos \
--env-file ./nacos/custom.env \
-p 8848:8848 \
-p 9848:9848 \
-p 9849:9849 \
--restart=always \
nacos/nacos-server:v2.1.0-slim
~~~

## 服务注册



![image-20250328205614951](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328205614951.png)



~~~yaml
spring:
  application:
    name: cart-service # 服务名称 服务注册要用来做服务发现
  cloud:
    nacos:
      server-addr: 192.168.254.128:8848
#      server-addr: ${hm.nacos.host}:${hm.nacos.port} 从不同环境读取不同配置
~~~

![image-20250328213214093](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328213214093.png)



ide 中**模拟多服务实例** 实际上这个都是请求到同一个服务器

**一般是多个服务器或者多个容器中**

**“实例"**是同一个微服务的运行拷贝，每个实例独立运行但功能相同。这些实例通常会分布在不同的主机上，或者在同一主机的多个容器中。
**目的:**
**a.高可用性:如果某个实例宕机，其他实例仍然可以继续服务，避免系统中断。**
**b.负载分担:通过负载均衡将流量分配给多个实例，减少单个实例的压力。**
**c.横向扩展:在高峰期快速增加实例数量以应对流量增长。**



**注意：**

容器**内部端口**:每个 Docker 容器内部的端口(例如 80)可以相同，因为容器之间是隔离的。

主机绑定端口:当容器的**端口暴露到主机**时，必须确保主机端口**唯一**，否则会导致冲突。

---



## 服务发现和负载均衡

![image-20250629174713386](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629174713386.png)

**generateAllsetter  Plugin**

![image-20250629174856636](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629174856636.png)



即使都继承了同一个父模块，它们 **彼此之间是没有依赖关系的**。

想访问其他子模块的类，必须 **在 `pom.xml` 中添加依赖声明**

但是这样 会有强依赖

**“两个模块需要互相调用怎么办？”**
 答：可以将公共接口提取到 `common-api` 模块中，两个模块都依赖 `common-api`，然后通过接口解耦（典型 DDD 思维）。

~~~pgsql
my-project/
├── pom.xml                  <-- 父模块
├── user-api/                <-- 公共接口（供其他模块调用）
│   ├── UserDTO.java
│   └── UserClient.java      <-- 对外接口
├── user-service/            <-- 用户服务，提供接口实现
│   └── UserServiceImpl.java
├── order-service/           <-- 订单服务，调用 user-api 接口
│   └── OrderService.java

~~~



e.g.  关键点：如何注入 `UserClient`？

**方案一：**Spring 容器中由 `user-service` 注入 `UserClientImpl`

- **前提：所有模块在同一个服务中运行（单体模块化项目）**

Spring 的依赖注入是基于当前进程的 Bean 容器，`@Autowired` 只能注入同一个服务（JVM 进程）中的 Bean。

**方案二：**微服务间远程调用（如使用 Feign）

#### user-api 中定义：

```java
@FeignClient(name = "user-service")
public interface UserClient {
    @GetMapping("/user/{id}")
    UserDTO getUserById(@PathVariable("id") Long id);
}
```

- `order-service` 引入 `user-api`，不再关心实现细节，**由 Spring Cloud Feign 自动生成远程代理实现**。

----

如果多个微服务需要共享数据模型，应该将模型抽取成一个独立的公共模块（如 `common-model`），**各服务通过依赖该模块来复用数据结构，从而避免服务间的耦合和模型不一致问题。**

**将公共数据模型抽取为独立模块，如 `common-model`**

推荐**公共模型 + 服务内独立模型共存**，即允许一定程度的冗余。公共模型（DTO）用于服务间通信，服务内部仍保留自己的业务实体模型（Entity/DO），这样做可以降低耦合、增强服务自治性，并为领域演进保留灵活性。

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328215349914.png" alt="image-20250328215349914" style="zoom: 200%;" />



![image-20250328215524282](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328215524282.png)

###  RestTemplate（远程调用の老方式）

```java
@Autowired
private RestTemplate restTemplate;

UserDTO user = restTemplate.getForObject("http://user-service/user/{id}", UserDTO.class, 1L);
```

![image-20250629183253888](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629183253888.png)

**推荐使用OpenFeign**



## 实体类分析（数据库属性分析）



~~~Java
@Data
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
@TableName("pay_order")
public class PayOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * id
     */
    @TableId(value = "id", type = IdType.ASSIGN_ID)
    private Long id;
   // 指定 id 为主键，并使用 MyBatis-Plus 的 ASSIGN_ID 策略（类似于 Snowflake 算法自动生成 ID）。


    /**
     * 业务订单号
     */
    private Long bizOrderNo;
    // business Order number

    /**
     * 支付单号
     */
    private Long payOrderNo;

    /**
     * 支付用户id
     */
    private Long bizUserId;
   

    /**
     * 支付渠道编码
     */
    private String payChannelCode;

    /**
     * 支付金额，单位分
     */
    private Integer amount;

    /**
     * 支付类型，1：h5,2:小程序，3：公众号，4：扫码，5：余额支付
     */
    private Integer payType;

    /**
     * 支付状态，0：待提交，1:待支付，2：支付超时或取消，3：支付成功
     */
    private Integer status;

    /**
     * 拓展字段，用于传递不同渠道单独处理的字段
     */
    private String expandJson;

    /**
     * 第三方返回业务码
     */
    private String resultCode;

    /**
     * 第三方返回提示信息
     */
    private String resultMsg;

    /**
     * 支付成功时间
     */
    private LocalDateTime paySuccessTime;

    /**
     * 支付超时时间
     */
    private LocalDateTime payOverTime;

    /**
     * 支付二维码链接
     */
    private String qrCodeUrl;

    /**
     * 创建时间
     */
    private LocalDateTime createTime;

    /**
     * 更新时间
     */
    private LocalDateTime updateTime;

    /**
     * 创建人
     */
    private Long creater;

    /**
     * 更新人
     */
    private Long updater;

    /**
     * 逻辑删除
     */
    private Boolean isDelete;


}

~~~

==**业务分析：**==



![90be0d44536d8501bfd059ada00d88e](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/90be0d44536d8501bfd059ada00d88e.jpg)

~~~java
@Service
@RequiredArgsConstructor
public class PayOrderServiceImpl extends ServiceImpl<PayOrderMapper, PayOrder> implements IPayOrderService {
    private final UserClient userClient;
    private final TradeClient tradeClient;

    @Override
    public String applyPayOrder(PayApplyDTO applyDTO) {
        // 1.幂等性校验
        PayOrder payOrder = checkIdempotent(applyDTO);
        // 2.返回结果
        return payOrder.getId().toString();
    }

    @Override
    @Transactional
    public void tryPayOrderByBalance(PayOrderFormDTO payOrderFormDTO) {
        // 1.查询支付单
        PayOrder po = getById(payOrderFormDTO.getId());
        // 2.判断状态
        if(!PayStatus.WAIT_BUYER_PAY.equalsValue(po.getStatus())){
            // 订单不是未支付，状态异常
            throw new BizIllegalException("交易已支付或关闭！");
        }
        // 3.尝试扣减余额


        userClient.deductMoney(payOrderFormDTO.getPw(), po.getAmount());


        // 4.修改支付单状态
        boolean success = markPayOrderSuccess(payOrderFormDTO.getId(), LocalDateTime.now());
        if (!success) {
            throw new BizIllegalException("交易已支付或关闭！");
            // Spring 默认会对 未捕获的 RuntimeException 或 Error 进行回滚
        }

        tradeClient.markOrderPaySuccess(po.getBizOrderNo());



    }

    public boolean markPayOrderSuccess(Long id, LocalDateTime successTime) {
        return lambdaUpdate()
                .set(PayOrder::getStatus, PayStatus.TRADE_SUCCESS.getValue())
                .set(PayOrder::getPaySuccessTime, successTime)
                .eq(PayOrder::getId, id)
                // 支付状态的乐观锁判断
                .in(PayOrder::getStatus, PayStatus.NOT_COMMIT.getValue(), PayStatus.WAIT_BUYER_PAY.getValue())
                .update();
    }


    private PayOrder checkIdempotent(PayApplyDTO applyDTO) {
        // 1.首先查询支付单
        PayOrder oldOrder = queryByBizOrderNo(applyDTO.getBizOrderNo());
        // 2.判断是否存在
        if (oldOrder == null) {
            // 不存在支付单，说明是第一次，写入新的支付单并返回
            PayOrder payOrder = buildPayOrder(applyDTO);
            payOrder.setPayOrderNo(IdWorker.getId());
            save(payOrder);
            return payOrder;
        }
        // 3.旧单已经存在，判断是否支付成功
        if (PayStatus.TRADE_SUCCESS.equalsValue(oldOrder.getStatus())) {
            // 已经支付成功，抛出异常
            throw new BizIllegalException("订单已经支付！");
        }
        // 4.旧单已经存在，判断是否已经关闭
        if (PayStatus.TRADE_CLOSED.equalsValue(oldOrder.getStatus())) {
            // 已经关闭，抛出异常
            throw new BizIllegalException("订单已关闭");
        }
        // 5.旧单已经存在，判断支付渠道是否一致
        if (!StringUtils.equals(oldOrder.getPayChannelCode(), applyDTO.getPayChannelCode())) {
            // 支付渠道不一致，需要重置数据，然后重新申请支付单
            PayOrder payOrder = buildPayOrder(applyDTO);
            payOrder.setId(oldOrder.getId());
            payOrder.setQrCodeUrl("");
            updateById(payOrder);
            payOrder.setPayOrderNo(oldOrder.getPayOrderNo());
            return payOrder;
        }
        // 6.旧单已经存在，且可能是未支付或未提交，且支付渠道一致，直接返回旧数据
        return oldOrder;
    }

    private PayOrder buildPayOrder(PayApplyDTO payApplyDTO) {
        // 1.数据转换
        PayOrder payOrder = BeanUtils.toBean(payApplyDTO, PayOrder.class);
        // 2.初始化数据
        payOrder.setPayOverTime(LocalDateTime.now().plusMinutes(120L));
        payOrder.setStatus(PayStatus.WAIT_BUYER_PAY.getValue());
        payOrder.setBizUserId(UserContext.getUser());
        return payOrder;
    }
    public PayOrder queryByBizOrderNo(Long bizOrderNo) {
        return lambdaQuery()
                .eq(PayOrder::getBizOrderNo, bizOrderNo)
                .one();
    }
}

~~~

主键一般是自增的

**这里的支付订单id是随机生成算法生成的 所以不适合作为主键**  

# Nacos 配置中心

![image-20250629183534942](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629183534942.png)

![image-20250629185318758](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629185318758.png)

告诉 Spring Boot：

- 要从 Nacos 读取名为 `service-order.properties` 的配置
- 从地址 `127.0.0.1:8848` 加载

会自动把这个文件中的配置合并进当前配置环境中（就像 `application.properties` 一样）



**yaml文件：**

 ~~~yaml
spring:
  config:
    import: nacos:service-order.yaml
  cloud:
    nacos:
      server-addr: 127.0.0.1:8848

 ~~~



---





**必须在加 `@RefreshScope`** 才能在运行时动态刷新 Bean

如何获取配置文件中的配置值

使用 @Value 注解（适合少量简单配置）

~~~java
@RestController
@RefreshScope // 支持配置变更自动刷新
public class TestController {

    @Value("${user.name}")
    private String name;

    @GetMapping("/user-name")
    public String getUserName() {
        return name;
    }
}

~~~

---



**使用 `@ConfigurationProperties`（推荐方式）**

![image-20250629190008987](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629190008987.png)

![image-20250629185516880](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629185516880.png)

| 术语          | 含义                                            |
| ------------- | ----------------------------------------------- |
| **Data ID**   | 配置文件的唯一标识（如 `service-a.yaml`）       |
| **Group**     | 用于分组管理（如 `DEFAULT_GROUP`、`dev-group`） |
| **Namespace** | 用于环境隔离（如 dev/test/prod）                |
| **配置格式**  | 支持 `.properties`, `.yaml`, `.json` 等         |

~~~json
user:
  name: Senjay
  age: 25

~~~

![image-20250629185627743](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629185627743.png)

**就是禁用了默认行为 ： 因为引入了配置中心依赖就会自动导入配置 但是有些微服务没有配置**

---



**为什么需要bootstrap.yaml**

因为某些配置（如：配置中心、注册中心、加密配置）**必须在 Spring Boot 容器初始化之前就加载生效**，而 `application.yaml` 加载得太晚，来不及了，所以需要更早阶段的配置文件：**`bootstrap.yaml`。**



**配置监听：**

~~~java
@Configuration
public class NacosListenerConfig {

    @Bean
    public ApplicationRunner applicationRunner(NacosConfigManager nacosConfigManager) {
        return args -> {
            ConfigService configService = nacosConfigManager.getConfigService();

            configService.addListener("service-order.properties", "DEFAULT_GROUP", new Listener() {
                @Override
                public Executor getExecutor() {
                    // 这里返回线程池，用于异步处理配置变更
                    return Executors.newFixedThreadPool(2);
                }

                @Override
                public void receiveConfigInfo(String configInfo) {
                    // 监听到配置变更时触发
                    System.out.println("========== 配置变更内容 ==========");
                    System.out.println(configInfo);
                }
            });
        };
    }
}
// receiveConfigInfo(String configInfo) 是 Nacos 配置客户端触发的回调方法，这个回调是由 Nacos 长轮询线程池内部调用的。

// 如果你在这个方法中执行耗时操作（比如 IO、发送邮件、复杂计算），就会阻塞长轮询线程，影响 Nacos 监听的性能和及时性。
~~~





![image-20250629225549206](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629225549206.png)

也可以书写公共配置 然后直接在其他配置中导入这样就不用重复在配置中心写**重复配置**了



![image-20250629225618869](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629225618869.png)

# 数据隔离

![image-20250629234842978](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250629234842978.png)



![image-20250629234914903](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629234914903.png)



<span style="font-size:1.5em;">**<span style="color:#FF3333; font-size:1.1em;">标准配置文件书写格式：</span>**</span>
`---` 是 **YAML 中的文档分隔符**，表示**多个独立的配置段落**

![image-20250630000646120](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630000646120.png)

~~~yaml
# ======================== 基础配置（默认激活 test 环境） ========================
server:
  port: 8000  # 启动端口

spring:
  application:
    name: service-order  # 应用名称，用于注册到 nacos、配置加载等
  profiles:
    active: test  # 当前激活环境，可选值：dev、test、prod，对应下方段落
  cloud:
    nacos:
      server-addr: 127.0.0.1:8848  # Nacos 服务地址
      config:
        # Nacos 的命名空间 namespace，根据激活环境动态设置（例如 test）
        namespace: ${spring.profiles.active:dev}

# ======================== dev 环境专属配置 ========================
---
spring:
  config:
    activate:
      on-profile: dev  # 只有在 dev 环境下才激活这一段
    import:
      # 引入 Nacos 的配置文件（Data ID）
      - nacos:common.properties?group=order
      - nacos:database.properties?group=order

# ======================== test 测试环境专属配置 ========================
---
spring:
  config:
    activate:
      on-profile: test  # 只有在 test 环境下才激活这一段
    import:
      - nacos:common.properties?group=order
      - nacos:database.properties?group=order
      - nacos:haha.properties?group=order  # 额外配置文件，仅 test/prod 环境下加载

# ======================== prod 生产环境专属配置 ========================
---
spring:
  config:
    activate:
      on-profile: prod  # 只有在 prod 环境下才激活这一段
    import:
      - nacos:common.properties?group=order
      - nacos:database.properties?group=order
      - nacos:haha.properties?group=order

~~~





---





![image-20250629234930202](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250629234930202.png)

---



# ==Nacos面试题==

如何实现服务注册和发现

健康检查的机制是什么

自我保护的原理是什么

事件监听是如何设计的

Nacos 是怎么保障高可用的

Nacos在设计上有上面缺陷



# ==配置管理 面试题==



# OpenFeign

**也可以使用OpenFeign 调用第三方Api**

~~~java
@FeignClient(value = "weather-client", url = "http://aliv18.data.moji.com")
public interface WeatherFeignClient {

    @PostMapping("/whapi/json/alicityweather/condition")
    String getWeather(
        @RequestHeader("Authorization") String auth,
        @RequestParam("token") String token,
        @RequestParam("cityId") String cityId
    );
}

~~~

加了 `url`，Feign 就**不会使用注册中心查地址**，而是直接请求这个 URL。

`value="weather-client"` 只是起个名字，方便日志、分组、监控使用

**此时即使 Nacos 里没有 `weather-client` 这个服务也不会报错**

| 风格       | 特点                     | 你关心的是         |
| ---------- | ------------------------ | ------------------ |
| 编程式编程 | 手动控制流程、逻辑       | **怎么做**（How）  |
| 声明式编程 | 通过配置或注解让框架代劳 | **要什么**（What） |



![image-20250630000727103](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630000727103.png)

**简化http客户端操作**

**具体就是简化了==远程调用==和==负载均衡==**

![image-20250328215532860](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328215532860.png)

![image-20250328215631820](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328215631820.png)







当你在 `pom.xml` 中引入一个依赖，例如：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

它的 **`pom.xml`** 可能会包含：

```xml
<dependencies>
    <dependency>
        <groupId>io.github.openfeign</groupId>
        <artifactId>feign-core</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-loadbalancer</artifactId>
    </dependency>
</dependencies>
```

那么你在项目里引入 `spring-cloud-starter-openfeign`，就 **自动继承** 了 `feign-core` 和 `spring-cloud-starter-loadbalancer` 这些依赖，这就是 **传递依赖**。

## **确保 `@EnableFeignClients` 已启用**

`@FeignClient` 需要 Feign 组件的支持，你需要在 Spring Boot 启动类（`@SpringBootApplication` 标注的类）上加上：

```java
@EnableFeignClients(basePackages = "com.hmall.api.client")
```

或者：

```java
@EnableFeignClients
```

这样 Spring 才能扫描 `UserClient` 并注册为 Bean。



---



## **依赖范围（Scope）影响继承**

在 `pom.xml` 里，依赖可能会有不同的 `scope`（作用范围）：

- **`compile`（默认）**：会被 **继承**，在**编译、测试、运行时**都可用。
- **`provided`**：不会被继承，只在编译和测试时可用，运行时需要环境提供。
- **`runtime`**：不会在编译时继承，但在运行时需要。
- **`test`**：不会被继承，只在测试时可用。

---



在 `@FeignClient` 中，`value` 指定的服务名用于 **从服务注册中心查找对应的微服务**，然后通过 Feign 进行远程调用。

![image-20250630001853873](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630001853873.png)




![image-20250328215702449](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328215702449.png)

**实现远程调用直接 就通过spring管理的feignclient 接口 调用这个接口的方法** 



**就是再写一遍接口 然后远程调用者调用这个接口对应的方法！**



**用这个Collection 就可以不用转化 集合了** 

**所有集合都可以用！**

```Java
@FeignClient("cart-service")
public interface CartClient {
    @DeleteMapping("/carts")
    void deleteCartItemByIds(@RequestParam("ids") Collection<Long> ids);
}
```

**对比差异**



![image-20250328221209504](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328221209504.png)





## 👻feighClient 问题

![1743593689466](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1743593689466.png)

![1743593705666](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1743593705666.png)



~~~java
// 位于trade微服务中 的 OrderServiceImpl

List<OrderDetailDTO> detailDTOS = orderFormDTO.getDetails();
// 需要修改OrderFormDTO（trade微服务） 中的details类导入路径
~~~



```java
itemClient.deductStock(detailDTOS); // 这个DTO 是api 那边的 路径是api那里的 不是trade微服务路径的
```



```java
//ItemClient的deductStock方法要OrderDetailDTO，hm-api总不能从trade-service导这个类型吧。
// 那hm-api模块里有这个DTO，其他微服务模块调用这个远程调用时，传入的DTO就必须与hm-api 是相同类型（路径也要相同）
```

就算是名字一样也不行 要保证路径一致 







---



**HTTP 请求参数以逗号分割的处理**

在 Web 开发中，我们可能会遇到**前端以逗号分隔参数**的需求，比如：

- 传递多个 ID：`http://example.com/api/users?ids=1,2,3,4`
- 传递多个标签：`http://example.com/api/tags?names=java,python,javascript`

**📌 1. 前端如何构造请求？**

在前端，构造以**逗号分隔**的请求参数可以这样做：

**🟢 JavaScript 示例**

```javascript
const ids = [1, 2, 3, 4];
const url = `http://localhost:8080/api/users?ids=${ids.join(",")}`;

fetch(url)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
```

🔹 `ids.join(",")` 会将数组转换为 `"1,2,3,4"`，形成 `?ids=1,2,3,4`

**📌 2. 后端如何接收请求？**

**🟢 Java Spring Boot 处理逗号分隔的参数**

在 Spring Boot 后端，可以使用 **`@RequestParam`** 接收参数，并转换为 `List<String>` 或 `List<Integer>`。

**（1）基本处理：手动拆分**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public ResponseEntity<List<Integer>> getUsers(@RequestParam String ids) {
        List<Integer> idList = Arrays.stream(ids.split(","))
                                     .map(Integer::parseInt)
                                     .collect(Collectors.toList());
        return ResponseEntity.ok(idList);
    }
}
```

📌 **测试 URL**

```
http://localhost:8080/api/users?ids=1,2,3,4
```

📌 **返回结果**

```json
[1, 2, 3, 4]
```

**（2）自动转换：使用 `List<>`**

Spring Boot 允许 `@RequestParam` 直接转换为 `List<>`：

```java
@GetMapping
public ResponseEntity<List<Integer>> getUsers(@RequestParam List<Integer> ids) {
    return ResponseEntity.ok(ids);
}
```

📌 **这样，Spring Boot 会自动把 `?ids=1,2,3,4` 转换为 `List<Integer>`！**



---



这个是最原始的 不涉及**远程调用** 或是 **openfeign**

~~~java
 @Override
    public List<CartVO> queryMyCarts() {
        // 1.查询我的购物车列表
        List<Cart> carts = lambdaQuery().eq(Cart::getUserId, UserContext.getUser()).list();
        if (CollUtils.isEmpty(carts)) {
            return CollUtils.emptyList();
        }

        // 2.转换VO
        List<CartVO> vos = BeanUtils.copyList(carts, CartVO.class);

        // 3.处理VO中的商品信息
        handleCartItems(vos);

        // 4.返回
        return vos;
    }

    private void handleCartItems(List<CartVO> vos) {
        // 1.获取商品id
        Set<Long> itemIds = vos.stream().map(CartVO::getItemId).collect(Collectors.toSet());
        // 2.查询商品
        List<ItemDTO> items = itemService.queryItemByIds(itemIds);
        if (CollUtils.isEmpty(items)) {
            return;
        }
        // 3.转为 id 到 item的map
        Map<Long, ItemDTO> itemMap = items.stream().collect(Collectors.toMap(ItemDTO::getId, Function.identity()));
        // 4.写入vo
        for (CartVO v : vos) {
            ItemDTO item = itemMap.get(v.getItemId());
            if (item == null) {
                continue;
            }
            v.setNewPrice(item.getPrice());
            v.setStatus(item.getStatus());
            v.setStock(item.getStock());
        }
    }
~~~





## openfeign 的最佳实践

以上的方法 如果要远程调用某个微服务那都要写这东西（而且都是写一样的openfeign 万一接口逻辑变了 就要全部修改） 很麻烦 解决方案有两种：

根据**微服务两种结构**来定：

一文件夹多project

![image-20250328221845847](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250328221845847.png)





一project多modules



![image-20250329090830319](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329090830319.png)



**依赖传递：**

在api 模块的pom文件中先导入openfeign的依赖 

然后这个模块的类以及所有东西（依赖）都可以被  导入api模块的模块使用

~~~xml
		<dependency>
			<groupId>com.heima</groupId>
			<artifactId>hm-api</artifactId>
			<version>1.0.0</version>
			<scope>compile</scope>
		</dependency>
~~~



**扫描包问题：**

 ![image-20250329104443827](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329104443827.png)

推荐第一种



## openfeign日志输出

![image-20250329120921995](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329120921995.png)

![image-20250630091616914](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630091616914.png)



![image-20250329121305706](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329121305706.png)



feignclient 就是 某个微服务的RPC 方法

其他微服务要调用这个微服务的方法只需要 使用这个feignclient即可

调试的时候再配置即可！！！



## 超时控制

![image-20250630091859552](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630091859552.png)

![image-20250630092124919](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630092124919.png)

## 超时配置

**类比打电话**

```yaml
# application.yaml
spring:
  profiles:
    active: dev
    include: common
```

🔍 解释：

- 表示先激活 `dev` 配置；
- 再“顺带”加载 `application-common.yaml` 的配置。

~~~yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            logger-level: FULL
            connect-timeout: 1000
            read-timeout: 2000
          service-product:
            logger-level: FULL
            connect-timeout: 3000
            read-timeout: 5000

~~~



---



## 重试机制

![image-20250630095754238](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630095754238.png)



![image-20250630100017258](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630100017258.png)

> **Spring Cloud OpenFeign** 默认不会自动提供某些 Bean（如 `Retryer`、`Logger.Level` 等），那你在配置文件 `application.yaml` 中写的配置是怎么生效的？有没有关系？

**✅ 1. `application.yaml` 中的配置 ≠ 直接注册 Bean**

配置文件是通过 Spring Boot **属性绑定机制**注入到某些组件里，但这些组件 **并不是所有情况下都默认被创建**。
 也就是说：

- 有些配置项能自动生效，**是因为有内置 Bean 会读取这些配置；**
- 
- 有些组件（如 `Retryer`）**必须你手动提供 Bean，它才会启用，即使你写了配置项也不会生效。**

## 拦截器

![image-20250630103812871](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630103812871.png)

[OpenFeign传递用户](###网关传递用户)





---

# ==OpenFeign面试题==









# 网关

![image-20250630173220904](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630173220904.png)

![image-20250630173301129](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630173301129.png)







![image-20250329130047614](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329130047614.png)

路由（判断这个请求到底由哪个服务去进行处理 ）确定路径 转发就是通过这个路径发送

**（微服务中可能有多个实例 所以使用负载均衡算法挑选一个合适的实例）**

![image-20250329130330618](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329130330618.png)

## 网关路由

**网关本质也是一个微服务** 所以也是一个模块 所以也得导入nacos 服务注册/ 服务发现（在启动类中写@Enable…… 注解）





![image-20250329144857482](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329144857482.png)

![image-20250630183333411](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630183333411.png)

![image-20250630184023451](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630184023451.png)







~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>hmall</artifactId>
        <groupId>com.heima</groupId>
        <version>1.0.0</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>hm-gateway</artifactId>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
    <dependencies>
        <!--common-->
        <dependency>
            <groupId>com.heima</groupId>
            <artifactId>hm-common</artifactId>
            <version>1.0.0</version>
        </dependency>
        <!--网关-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
        </dependency>
        <!--nacos discovery-->
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <!--负载均衡-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-loadbalancer</artifactId>
        </dependency>
    </dependencies>
    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
~~~

![image-20250329145249010](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329145249010.png)



**配置路由**

~~~yaml
server:
  port: 8080
spring:
  application:
    name: gateway
  cloud:
    nacos:
      server-addr: 192.168.150.101:8848
    gateway:
      routes:
        - id: item # 路由规则id，自定义，唯一
          uri: lb://item-service # 路由的目标服务，lb代表负载均衡，会从注册中心拉取服务列表
          predicates: # 路由断言，判断当前请求是否符合当前规则，符合则路由到目标服务
            - Path=/items/**,/search/** # 这里是以请求路径作为判断规则
        - id: cart
          uri: lb://cart-service
          predicates:
            - Path=/carts/**
        - id: user
          uri: lb://user-service
          predicates:
            - Path=/users/**,/addresses/**
        - id: trade
          uri: lb://trade-service
          predicates:
            - Path=/orders/**
        - id: pay
          uri: lb://pay-service
          predicates:
            - Path=/pay-orders/**

~~~

## 路由属性

![image-20250329151932480](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329151932480.png)

**断言的属性** （根据这些属性的值来断言是否使用对应的服务）

![image-20250329151945860](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329151945860.png)









  **这个 断言下属性的写法有==长短==两种写法**

~~~yaml
spring:
  cloud:
    gateway:
      routes:
        # 示例1：路径匹配 + 负载均衡
        - id: user-service
          uri: lb://user-service      # 服务注册中心中的服务名
          predicates:
            - Path=/api/user/**
          filters:
            - StripPrefix=1           # 去掉前缀 `/api/user`

        # 示例2：多条件组合
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/order/**
            - Method=POST
            - Query=source,mobile
            - After=2023-01-01T00:00:00+08:00

        # 示例3：权重路由
        - id: weight-high
          uri: lb://inventory-service
          predicates:
            - Weight=inventory-group, 70
        - id: weight-low
          uri: lb://inventory-service-backup
          predicates:
            - Weight=inventory-group, 30
~~~

**长写法**

~~~yaml
spring:
  cloud:
    gateway:
      routes:
        # 示例1：路径匹配 + 负载均衡
        - id: user-service
          uri: lb://user-service
          predicates:
            - name: Path
              args:
                pattern: /api/user/**
          filters:
            - name: StripPrefix
              args:
                parts: 1

        # 示例2：多条件组合
        - id: order-service
          uri: lb://order-service
          predicates:
            - name: Path
              args:
                pattern: /api/order/**
            - name: Method
              args:
                methods: POST
            - name: Query
              args:
                param: source
                regexp: mobile
            - name: After
              args:
                datetime: 2023-01-01T00:00:00+08:00

        # 示例3：权重路由
        - id: weight-high
          uri: lb://inventory-service
          predicates:
            - name: Weight
              args:
                group: inventory-group
                weight: 70

        - id: weight-low
          uri: lb://inventory-service-backup
          predicates:
            - name: Weight
              args:
                group: inventory-group
                weight: 30

~~~

### 自定义断言

只需要判断参数是否存在或正则匹配，`Query` 完全足够；但一旦你需要“业务逻辑判断”、“上下文联合判断”或“复杂解析”，就必须自定义断言。

**不能用 `Query` 处理的（必须自定义）：**

- 判断 `?price=xxx` 是否大于 1000
- 请求参数中含有 JSON 字符串，要解析后判断里面的字段值
- `Query=id=xxx`，但要判断此 id 是否在白名单数据库里
- 参数加密了，必须解密才能比对

![image-20250630192840191](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250630192840191.png)

**注意前缀 名字不能随便写**

~~~java
@Component
public class VipRoutePredicateFactory extends AbstractRoutePredicateFactory<VipRoutePredicateFactory.Config> {


    public VipRoutePredicateFactory() {
        super(Config.class);
    }

    @Override
    public Predicate<ServerWebExchange> apply(Config config) {
        return new GatewayPredicate() {
            @Override
            public boolean test(ServerWebExchange serverWebExchange) {
                // localhost/search?q=haha&user=leifengyang
                ServerHttpRequest request = serverWebExchange.getRequest();

                String first = request.getQueryParams().getFirst(config.param);

                return StringUtils.hasText(first) && first.equals(config.value);
            }
        };
    }

    @Override
    public List<String> shortcutFieldOrder() {
        return Arrays.asList("param", "value");
    }

    /**
     * 可以配置的参数
     */
    @Validated
    public static class Config {

        @NotEmpty
        private String param;


        @NotEmpty
        private String value;

        public @NotEmpty String getParam() {
            return param;
        }

        public void setParam(@NotEmpty String param) {
            this.param = param;
        }

        public @NotEmpty String getValue() {
            return value;
        }

        public void setValue(@NotEmpty String value) {
            this.value = value;
        }
    }
}

~~~




~~~yaml
spring:
  cloud:
    gateway:
      globalcors:
        cors-configurations:
          '[/**]':
            allowed-origin-patterns: '*'
            allowed-headers: '*'
            allowed-methods: '*'

      routes:
        - id: bing-route
          uri: https://cn.bing.com/
          predicates:
            - name: Path
              args:
                patterns: /search
            - name: Query
              args:
                param: q
                regexp: haha
#            - Vip=user,leifengyang
            - name: Vip
              args:
                param: user
                value: leifengyang
                # 这两个是config里的字段
          order: 10
          metadata:
            hello: world
        - id: order-route
          uri: lb://service-order
          predicates:
            - name: Path
              args:
                patterns: /api/order/**
                matchTrailingSlash: true
          filters:
            - RewritePath=/api/order/?(?<segment>.*), /$\{segment}
            - OnceToken=X-Response-Token, jwt
          order: 1
        - id: product-route
          uri: lb://service-product
          predicates:
            - Path=/api/product/**
          filters:
            - RewritePath=/api/product/?(?<segment>.*), /$\{segment}
          order: 2
      default-filters:
        - AddResponseHeader=X-Response-Abc, 123
~~~

---



### 过滤器

![image-20250630224412744](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630224412744.png)

**路径重写**



![image-20250630225958284](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630225958284.png)



**对请求/响应做一些前置/后置的处理**

![image-20250630231144400](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630231144400.png)

![image-20250329152109896](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329152109896.png)



---





## 网关登录校验

![image-20250329153639498](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329153639498.png)







![image-20250329153939381](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329153939381.png)

> `default-filters` 是作用于**所有路由的局部过滤器**，而 **GlobalFilter** 是作用于整个网关生命周期的**全局组件**，执行粒度更广、可编程性更强。



![image-20250329154715595](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329154715595.png)



~~~yaml
spring:
  cloud:
    gateway:
      default-filters:
        - AddRequestHeader=X-Global, global
        - StripPrefix=1
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/user/**
          filters:
            - AddRequestHeader=X-Route, user-route

~~~







### **自定义过滤器：**





![image-20250329155259367](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329155259367.png)

<span style="font-size:1.3em; background:#990000; color:#FFFFFF;">**自定义GlobalFilter：**</span>



![image-20250329160515426](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329160515426.png)





Ctrl + H 类/方法 查看**继承链（层次）**

![image-20250329161248479](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329161248479.png)

~~~pgp
ServerWebExchange
├── ServerHttpRequest    // 请求对象
│   └── headers、uri、path、body 等
├── ServerHttpResponse   // 响应对象
│   └── 设置状态码、响应体

~~~



~~~java
@Component
@Slf4j
public class RtGlobalFilter implements GlobalFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        ServerHttpResponse response = exchange.getResponse();

        String uri = request.getURI().toString();
        long start = System.currentTimeMillis();
        log.info("请求【{}】开始：时间：{}",uri,start);
        //========================以上是前置逻辑=========================


        Mono<Void> filter = chain.filter(exchange)
                .doFinally((result)->{
                    //=======================以下是后置逻辑=========================
                    long end = System.currentTimeMillis();
                    log.info("请求【{}】结束：时间：{}，耗时：{}ms",uri,end,end-start);
                }); //放行   10s



        return filter;
    }

    @Override
    public int getOrder() {
        return 0;
    }
}

~~~



<span style="font-size:1.3em; background:#990000; color:#FFFFFF;">**自定义GatewayFilter过滤器：**</span>

**和自定义断言类似：注意命名问题 前缀 核心就是模仿官方类**

![image-20250630235024628](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630235024628.png)





~~~java
/**
 * 自定义 GatewayFilterFactory，作用是：
 * 在每次响应完成前，往响应头中添加一个一次性令牌（如 uuid、jwt）
 *
 * 使用方式：
 * 在 application.yml 的 route 中配置：
 *   filters:
 *     - name: OnceToken
 *       args:
 *         name: X-Once-Token
 *         value: uuid
 */
@Component
public class OnceTokenGatewayFilterFactory extends AbstractNameValueGatewayFilterFactory {

    /**
     * 这是过滤器的核心实现
     * @param config 自动绑定 name 和 value 配置参数
     * @return 返回一个 GatewayFilter 逻辑
     */
    @Override
    public GatewayFilter apply(NameValueConfig config) {

        // 返回一个匿名 GatewayFilter（核心逻辑）
        return new GatewayFilter() {

            @Override
            public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
                // 先执行下一个过滤器链
                return chain.filter(exchange)
                        // 当请求处理完（响应准备返回）时执行回调逻辑
                        .then(Mono.fromRunnable(() -> {

                    // 获取响应对象
                    ServerHttpResponse response = exchange.getResponse();
                    HttpHeaders headers = response.getHeaders();

                    // 获取配置中的 value 值（比如 uuid、jwt）
                    String value = config.getValue();

                    // 如果是 uuid，生成一个新的 UUID 作为令牌
                    if ("uuid".equalsIgnoreCase(value)) {
                        value = UUID.randomUUID().toString();
                    }

                    // 如果是 jwt，写入一个固定 JWT 字符串（可改为动态生成）
                    if ("jwt".equalsIgnoreCase(value)) {
                        value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                               + "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6..."
                               + "TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ";
                    }

                    // 向响应头中添加：如 "X-Once-Token: uuid"
                    headers.add(config.getName(), value);
                }));
            }
        };
    }
}

~~~

~~~ceylon
1. 当前过滤器收到请求（如 GET /order）
2. 调用 chain.filter(exchange) → 把请求“交给下一个过滤器或最终转发到下游服务”
3. 下一个链路全部执行完（请求成功或异常），就会进入 then(...) 中的回调
4. then(...) 执行的 Mono 用于“响应发出之前”的额外操作，比如：添加响应头

~~~



| 对比点               | `then(...)`                            | `doFinally(...)`                       |
| -------------------- | -------------------------------------- | -------------------------------------- |
| **作用阶段**         | 请求成功后继续执行（只处理“成功响应”） | 无论成功、失败、取消，**最终一定执行** |
| **是否处理异常**     | ❌ 不处理异常，请求异常时不会进入       | ✅ 一定会执行（异常、正常、取消都处理） |
| **是否可修改响应头** | ✅ 一般可以（响应未 commit）            | ❌ 通常不可以（响应可能已发送）         |
| **适合场景**         | 添加响应头、记录成功日志、业务后置处理 | 记录总耗时、释放资源、记录失败信息     |
| **是否一定执行**     | ❌ 只有成功才执行                       | ✅ 一定执行                             |

`then(...)` **在响应写出之前执行**

`doFinally(...)` **在响应生命周期彻底结束之后执行**，**响应已经写出**  apply to **日志/耗时统计 清理资源/记录结束状态**

~~~css
客户端请求 ─▶ [前置过滤器 A]
               │
               └▶ [前置过滤器 B]
                      │
                      └▶ 转发到后端服务
                            │
                            └─▶ 返回响应
                                      │
                            ◀─────────┘
                      ◀── [后置过滤器 B]
               ◀──── [后置过滤器 A]
客户端响应 ◀──────────

~~~





---

微服务架构中，如果你在“**网关层**”（比如 Spring Cloud Gateway）做统一处理，一定要用**过滤器（Filter）**，而不是传统的拦截器（Interceptor）。
 拦截器只能在“**服务内部**”的 Spring MVC 中使用，不适合网关这种全局路由分发结构。

配置类是用于加载配置文件中的属性的 （如果这些属性有用到的地方就要去加载）

---



**JWT的组成：**

~~~pgp
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VySWQiOjEyMywibmFtZSI6InpoYW5nc2FuZyIsImV4cCI6MTcwMDAwMDAwMH0.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk

~~~

被 `.` 分为三段，分别是：

| 段落          | 说明                                    | 示例内容（解码后）                |
| ------------- | --------------------------------------- | --------------------------------- |
| **Header**    | 头部：说明加密算法、Token类型           | `{"alg": "HS256", "typ": "JWT"}`  |
| **Payload**   | 载荷：实际数据（用户信息、过期时间）    | `{"userId":123,"exp":1700000000}` |
| **Signature** | 签名：防止数据被篡改，基于前两段 + 密钥 | 哈希值（不可逆）                  |



| 术语     | JJWT（常见库）                         | Hutool（当前用的库）                  |
| -------- | -------------------------------------- | ------------------------------------- |
| Claims   | Payload 的一个 JSONMap，包含 key-value | 没有 `Claims` 类型，直接使用 Payload  |
| Payload  | JWT 的中间部分（Base64 编码的 JSON）   | 直接用 `.setPayload(key, value)` 添加 |
| 获取字段 | `claims.get("userId")`                 | `jwt.getPayload("user")`              |
| 使用习惯 | 面向对象，强类型                       | 灵活简洁，直接操作 M                  |

~~~xml
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-jwt</artifactId>
    <version>对应版本号</version>
</dependency>
<!--————————————————————————————————————————————————————————————————————————————————————————————————————————————————————-->



<!-- JJWT 核心依赖 -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.11.5</version>
</dependency>

<!-- 用于签名的实现（必要） -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>

<!-- 用于序列化 payload（使用 Jackson） -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>

~~~

---



**登录校验过滤器**

~~~java
// 登录校验
@Component
@RequiredArgsConstructor
public class AuthGlobalFilter implements GlobalFilter, Ordered {
    private final AuthProperties authProperties;
    private final JwtTool jwtTool;


    // 这个是外部提供的工具类 如果要像上面那样DI 也可以但需要配置spring容器
    private final AntPathMatcher antPathMatcher = new AntPathMatcher();



    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        // 有些路径不需要拦截
        if(isExclude(request.getPath().toString())){
            return chain.filter(exchange);
        }
        // 获取请求头
        List<String> authorization = request.getHeaders().get("Authorization");
        String token = null;
        if(  authorization != null  &&  !authorization.isEmpty()){ // 防止空指针 先判断非空指涉
            token = authorization.get(0);
        }
        Long userId = null;
        try {
            // 解析token
            userId = jwtTool.parseToken(token);
        }catch (UnauthorizedException e){ // 这个就是自定义的异常
            ServerHttpResponse response = exchange.getResponse();
            // 设置响应码 这个HttpStatus不是自己写的
            response.setStatusCode(HttpStatus.UNAUTHORIZED);
            // 不会继续往下执行，直接返回
            return response.setComplete();
        }
        // 放行
        // 传递用户信息(将用户信息放到请求头中 然后放到serverwebexchange中继续传递) 见下述
            String userInfo = userId.toString();
        ServerWebExchange swe = exchange.mutate()
                .request(builder -> builder.header("user-info", userInfo))
                .build();

        return chain.filter(swe);

    }


    @Override
    public int getOrder() {
        return 0;
    }

    private boolean isExclude(String path){
        for(String excludePath:authProperties.getExcludePaths()){
            if(antPathMatcher.match(excludePath, path))
                return true;
        }
        return false;
    }
}

~~~

**对于当前的JWT**

~~~java
/**
     * 解析token
     *
     * @param token token
     * @return 解析刷新token得到的用户信息
     */
    public Long parseToken(String token) {
        // 1.校验token是否为空
        if (token == null) {
            throw new UnauthorizedException("未登录");
        }
        // 2.校验并解析jwt
        JWT jwt;
        try {
            jwt = JWT.of(token).setSigner(jwtSigner);
        } catch (Exception e) {
            throw new UnauthorizedException("无效的token", e);
        }
        // 2.校验jwt是否有效
        if (!jwt.verify()) {
            // 验证失败
            throw new UnauthorizedException("无效的token");
        }
        // 3.校验是否过期
        try {
            JWTValidator.of(jwt).validateDate();
        } catch (ValidateException e) {
            throw new UnauthorizedException("token已经过期");
        }
        // 4.数据格式校验
        Object userPayload = jwt.getPayload("user");
        if (userPayload == null) {
            // 数据为空
            throw new UnauthorizedException("无效的token");
        }

        // 5.数据解析
        try {
           return Long.valueOf(userPayload.toString());
        } catch (RuntimeException e) {
            // 数据格式有误
            throw new UnauthorizedException("无效的token");
        }
    }
~~~





**网关相关配置：**

~~~yaml
server:
  port: 8080
spring:
  application:
    name: gateway
  cloud:
    nacos:
      server-addr: 192.168.254.128:8848
    gateway:
      routes:
        - id: item # 路由规则id，自定义，唯一
          uri: lb://item-service # 路由的目标服务，lb代表负载均衡，会从注册中心拉取服务列表
          predicates: # 路由断言，判断当前请求是否符合当前规则，符合则路由到目标服务
            - Path=/items/**,/search/** # 这里是以请求路径作为判断规则
        - id: cart
          uri: lb://cart-service
          predicates:
            - Path=/carts/**
        - id: user
          uri: lb://user-service
          predicates:
            - Path=/users/**,/addresses/**
        - id: trade
          uri: lb://trade-service
          predicates:
            - Path=/orders/**
        - id: pay
          uri: lb://pay-service
          predicates:
            - Path=/pay-orders/**
hm:
  jwt:
    location: classpath:hmall.jks
    alias: hmall
    password: hmall123
    tokenTTL: 30m
  auth:
    excludePaths:
      - /search/**
      - /users/login
      - /items/**
      - /hi
~~~

~~~java
@Component
@Data
@ConfigurationProperties(prefix = "hm.auth")
public class AuthProperties {
    private List<String> includePaths;
    private List<String> excludePaths;
}

~~~



### 网关传递用户

拦截器：简化操作（每个微服务都去写获取请求头保存用户信息很麻烦）

![image-20250329183557869](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329183557869.png)

![image-20250329185236398](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329185236398.png)



![image-20250329201426315](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329201426315.png)



**把拦截器写在了公共模块（common 模块）并被其他微服务依赖了**，Spring Boot 会 **自动扫描并注册这些公共模块中声明的 Bean**，这其实是 Spring Boot 的一项特性 —— **自动组件扫描和 Bean 装配机制**。

**<span style="color:#FF0000; font-size:1.3em;">每个微服务都有自己的 Spring 容器，Bean 是彼此隔离的。</span>**

![image-20250701082237636](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701082237636.png)

区别是：这里不用做拦截 因为真正的拦截已经在网关过滤器做过了

~~~java
// 拦截器要想生效，必须要写配置类
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new UserInfoInterceptor());

    }
}


------------------------------------------------------------------------
// 拦截器
public class UserInfoInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(javax.servlet.http.HttpServletRequest request, javax.servlet.http.HttpServletResponse response, Object handler) throws Exception {
         String userInfo = request.getHeader("user-info");
         if(StrUtil.isNotBlank(userInfo)) {
             UserContext.setUser(Long.valueOf(userInfo));
         }
         return true;


    }
    @Override
    public void afterCompletion(javax.servlet.http.HttpServletRequest request, javax.servlet.http.HttpServletResponse response, Object handler, Exception ex) throws Exception {
        UserContext.removeUser();
    }
}
~~~



这个**配置类**也得被 扫描到！！！



---



### springboot 扫描

这个就是我们为什么引入==**第三方包**==的时候会自动的把那些类，bean自动的放到ioc容器中的原因  （**自动配置文件**）

#### 把common模块做成Spring Boot Starter

- common模块做成starter，写自动配置类并在 `META-INF/spring.factories` 中声明
- 微服务只需依赖common starter，无需配置扫描，自动生效



<span style="font-size:1.3em; color:#CC0000;">key：**每个微服务是独立的 Spring Boot 应用，拥有自己的 IoC 容器，彼此隔离**</span>



![image-20250403231030296](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250403231030296.png)

<span style="color:#FF0000; font-size:1.1em;">**由于WebMvcConfigurer 底层是mvc** </span>

<span style="color:#FF0000; font-size:1.1em;">**而（这里使用的是响应式网关）网关底层不是mvc 是响应式客户端** (重点是要看使用的是那种网关)</span>

**所以现在需求就是要让一个配置类在指定的地方不生效** How

 

conditonal  on xxx

~~~java
// 拦截器要想生效，必须要写配置类
@Configuration
@ConditionalOnClass(DispatcherServlet.class)
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new UserInfoInterceptor());

    }
}
~~~

![image-20250404095801197](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404095801197.png)



---





### OpenFeign传递用户



**问题：微服务通过openfeign 调用其他微服务的时候 用户的信息如何传递呢**



![image-20250403230951877](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250403230951877.png)

![image-20250403230930685](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250403230930685.png)







~~~java
public class DefaultConfiguration {

    @Bean
    public RequestInterceptor requestInterceptor() {
        return new RequestInterceptor() {
            @Override
            public void apply(RequestTemplate requestTemplate) {
                Long userId = UserContext.getUser();
                if (userId != null) {
                    // 数据类型转化基本方法
                    requestTemplate.header("userId", String.valueOf(userId));
                }

            }
        };
    }
}

~~~



![image-20250403233210957](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250403233210957.png)

网关 --> trade-service（使用openfeign 所以会进入拦截器 （要想让这个配置生效就要指名））-->其他微服务

用户点击xx按钮 触发网关接口 -> 触发**网关层的过滤器**（过滤器进行身份校验 然后再通过请求头封装用户信息 来进行传递到微服务中）->  进入**MVC 拦截器**（在这里微服务获取请求头封装用户信息（threadlocal） 不然每个微服务都得单独写一遍？）

对于微服务之间呢  ：

**OpenFeign 是客户端工具**：负责构造和发送 HTTP 请求 到微服务中 （本质就是客户端工具 就是发起http请求的）

- **服务端拦截器的触发**：仅取决于是否有 HTTP 请求到达服务端，与客户端实现方式无关。

~~~markdown
Spring MVC 拦截器的触发时机
Spring MVC 的拦截器（HandlerInterceptor）会在请求处理流程的特定阶段触发，具体分为以下三个核心方法：

1. preHandle 方法
触发时机：在请求进入 Controller 方法之前执行。

典型用途：权限校验、请求日志记录、参数预处理等。

返回值：

true：继续执行后续拦截器和 Controller 方法。

false：中断请求，直接返回响应。

2. postHandle 方法
触发时机：在 Controller 方法执行之后，视图渲染（View Rendering）之前执行。

典型用途：修改模型数据（ModelAndView）、记录请求处理时间等。

3. afterCompletion 方法
触发时机：在整个请求处理完成之后触发（视图渲染完毕，响应已返回客户端）。

典型用途：资源清理（如数据库连接释放）、全局异常日志记录等。
~~~



问题汇总：

​	**spring 自动装配的扫描问题**

- **`hmall-common` 的角色**：它是一个**公共库模块**，而非独立运行的微服务。它的代码和配置文件会被打包为 JAR 文件，供其他微服务依赖。
- 当其他微服务（如 `service-order`）依赖 `hmall-common` 时，构建工具（Maven/Gradle）会将 `hmall-common` 的 JAR 包添加到 `service-order` 的类路径中。此时，`hmall-common` 中的 `spring.factories` 和配置类对 `service-order` **完全可见**。

~~~markdown
核心原因：Spring Boot 的自动配置机制依赖 类路径扫描 和 模块化设计
你提到的 common 模块（如 hmall-common）中定义的 spring.factories 文件，本质上是一个 “配置清单”，它告诉 Spring Boot：“当应用启动时，自动加载这些配置类”。而其他微服务能生效的关键在于 模块依赖的传递性 和 类路径的共享性。以下是分步解释：

一、模块化设计与依赖传递
假设你的项目结构如下：

hmall-common（公共模块）
  ├─ src/main/resources/META-INF/spring.factories  # 声明公共配置类
  └─ 包含 MyBatisConfig、JsonConfig、WebMvcConfig 等类

service-order（订单微服务）
  └─ 依赖 hmall-common
模块依赖

当 service-order 微服务在 pom.xml 或 build.gradle 中声明依赖 hmall-common 时，构建工具（Maven/Gradle）会将 hmall-common 的 JAR 包包含到 service-order 的类路径中。

传递性：这意味着 hmall-common 的代码和资源文件（包括 META-INF/spring.factories）对 service-order 是可见的。

类路径共享

service-order 启动时，JVM 会加载所有依赖模块的类路径内容，包括 hmall-common 的 META-INF/spring.factories 文件。

Spring Boot 会扫描所有类路径下的 spring.factories 文件，读取其中定义的配置类（如 MyBatisConfig），并自动加载它们。
~~~

**为什么需要显式声明？**

- **设计哲学**：Spring Boot 遵循“约定优于配置”原则，但为了避免类路径中所有 `@Configuration` 类被无差别加载（可能导致冲突），它要求开发者通过 `spring.factories` **显式声明需要自动加载的配置类**。
- **安全性**：显式声明确保只有明确指定的配置类会被加载，避免意外引入不需要的 Bean。



![image-20250404091911523](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404091911523.png)



**组合注解：**

![1743731865390](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1743731865390.png)



类似

~~~java
@EnableFeignClients(basePackages = "com.hmall.api.client")
// 帮你自动扫描并注册 @FeignClient 注解的接口。
//
//配置 basePackages：
//指定要扫描的 Feign 接口包路径。
@MapperScan("com.hmall.cart.mapper")
@SpringBootApplication
public class CartApplication {
    public static void main(String[] args) {
        SpringApplication.run(CartApplication.class, args);
    }
}
~~~





---



​	**feignClient 配置文件有什么用呢**

当某个 FeignClient 需要**复用一组固定配置**（如**自定义编解码器、拦截器、错误处理**器等），可以通过 `defaultConfiguration` 指定默认配置类，避免在每个方法或子类中重复配置。

（注意feignclient 有多个）



# ==网关面试题==





# 微服务保护(Sentinel)

## 服务保护

![image-20250630105107834](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630105107834.png)

![image-20250630105140308](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630105140308.png)

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630113852917.png)

**违反抛出异常后的处理方式和 ==资源==如何定义的有关**



![image-20250630125102567](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630125102567.png)

异常何时会抛给==Spring Boot全局异常处理==

**`@SentinelResource` 注解未配置降级方法**

- **场景**：方法使用 `@SentinelResource` 但**未定义** `blockHandler` 或 `fallback`





---



为什么自定义 `BlockExceptionHandler` 会覆盖默认实现？

通过分析 **Sentinel 1.8+ 的源码**和 **Spring Cloud Alibaba 的自动配置机制**，覆盖原因如下：

1. **核心机制：Spring 的条件装配（`@ConditionalOnMissingBean`）**

在 `spring-cloud-starter-alibaba-sentinel` 的自动配置类中，默认的 `BlockExceptionHandler` 是通过 **条件装配** 注入的：

```java
// 源码位置：SentinelWebAutoConfiguration
@Bean
@ConditionalOnMissingBean(BlockExceptionHandler.class) // 关键条件
public BlockExceptionHandler sentinelBlockExceptionHandler() {
    return new DefaultBlockExceptionHandler();
}
```

- **`@ConditionalOnMissingBean` 含义**：
  仅当 Spring 容器中 **不存在** 任何 `BlockExceptionHandler` 类型的 Bean 时，才会创建默认的 `DefaultBlockExceptionHandler`。

2. **自定义 Bean 的优先级**

当您通过 `@Component` 声明自定义实现时：

```java
@Component // 将自定义处理器注册为 Spring Bean
public class MyBlockExceptionHandler implements BlockExceptionHandler { ... }
```

Spring 容器会检测到已存在 `BlockExceptionHandler` 类型的 Bean（即您的 `MyBlockExceptionHandler`），**自动跳过默认实现的创建**，导致：

- 默认的 `DefaultBlockExceptionHandler` **不会被实例化**
- 所有限流/降级异常由您的自定义处理器处理

---

`@SentinelResource` 是 Sentinel 提供的一个注解，**主要用于保护方法级资源**

**一般是保护非controller 方法**

~~~java
@SentinelResource(
    value = "createOrder",
    blockHandler = "createOrderFallback"
)
@Override
public Order createOrder(Long productId, Long userId) {
    // 使用 Feign 完成远程调用
    Product product = productFeignClient.getProductById(productId);

    Order order = new Order();
    order.setId(1L);
    // 计算总金额 = 单价 × 数量
    order.setTotalAmount(product.getPrice().multiply(new BigDecimal(product.getNum())));
    order.setUserId(userId);
    order.setNickName("zhangsan");
    order.setAddress("arc");

    // 商品列表（只有一个商品）
    order.setProductList(Arrays.asList(product));

    return order;
}

// Sentinel 限流兜底方法（必须与原方法参数保持一致，并多一个 BlockException 参数）
public Order createOrderFallback(Long productId, Long userId, BlockException e) {
    Order order = new Order();
    order.setId(0L);
    order.setTotalAmount(new BigDecimal("0"));
    order.setUserId(userId);
    order.setNickName("未知用户");
    order.setAddress("限流触发，异常信息：" + e.getClass().getSimpleName());

    return order;
}

~~~



---



确保在配置文件中开启 Sentinel 对 Feign 的支持：

```yaml
feign:
  sentinel:
    enabled: true
```



~~~java
@FeignClient(
    value = "service-product", // 调用的服务名（注册中心中的服务）
    fallback = ProductFeignClientFallback.class // 指定降级处理类
)
public interface ProductFeignClient {

    // 发送 GET 请求，映射到目标服务的 /product/{id} 接口
    @GetMapping("/product/{id}")
    Product getProductById(@PathVariable("id") Long id);
}
@Component
public class ProductFeignClientFallback implements ProductFeignClient {

    @Override
    public Product getProductById(Long id) {
        System.out.println("兜底回调...");

        Product product = new Product();
        product.setId(id);
        product.setPrice(new BigDecimal("0")); // 默认价格
        product.setProductName("未知商品");
        product.setNum(0); // 数量为 0

        return product;
    }
}

~~~





---



### 使用Sentinel





![image-20250404101730973](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101730973.png)



Sentinel 的使用可以分为两个部分:

- **核心库**（Jar包）：不依赖任何框架/库，能够运行于 Java 8 及以上的版本的运行时环境，同时对 Dubbo / Spring Cloud 等框架也有较好的支持。在项目中引入依赖即可实现服务限流、隔离、熔断等功能。
- **控制台**（Dashboard）：Dashboard 主要负责管理推送规则、监控、管理机器信息等。

为了方便监控微服务，我们先把Sentinel的控制台搭建出来。

1）下载jar包

下载地址：

https://github.com/alibaba/Sentinel/releases

2）运行

将jar包放在任意非中文、不包含特殊字符的目录下，重命名为`sentinel-dashboard.jar`：

**然后运行如下命令启动控制台：**

cmd写法 一行

```Shell
java -Dserver.port=8090 
-Dcsp.sentinel.dashboard.server=localhost:8090 -Dproject.name=sentinel-dashboard 
-jar sentinel-dashboard-1.8.6.jar
```

pwsh**分行输入**

~~~sh
& java `
  "-Dserver.port=8090" `
  "-Dcsp.sentinel.dashboard.server=localhost:8090" `
  "-Dproject.name=sentinel-dashboard" `
  "-jar" "sentinel-dashboard-1.8.6.jar"

~~~



**这个是独立于 我们的项目的**

**所以需要微服务进行整合**



**我们在`cart-service`模块中整合sentinel，连接`sentinel-dashboard`控制台，步骤如下：**

 **1）引入sentinel依赖**

```XML
<!--sentinel-->
<dependency>
    <groupId>com.alibaba.cloud</groupId> 
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>
```

**2）配置控制台**

修改application.yaml文件，添加下面内容：

```YAML
spring:
  cloud: 
    sentinel:
      transport:
        dashboard: localhost:8090
```

3）访问`cart-service`的任意端点

重启`cart-service`，然后访问查询购物车接口，sentinel的客户端就会将服务访问的信息提交到`sentinel-dashboard`控制台。并展示出统计信息：

![img](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/asynccode)

点击簇点链路菜单，会看到下面的页面：

![image-20250404102238828](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404102238828.png)

所谓簇点链路，就是单机调用链路，是一次请求进入服务后经过的每一个被`Sentinel`监控的资源。默认情况下，`Sentinel`会监控`SpringMVC`的每一个`Endpoint`（接口）。

因此，我们看到`/carts`这个接口路径就是其中一个簇点，我们可以对其进行限流、熔断、隔离等保护措施。

不过，需要注意的是，我们的SpringMVC接口是按照Restful风格设计，因此购物车的查询、删除、修改等接口全部都是`/carts`路径：

![image-20250404102305766](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404102305766.png)

默认情况下Sentinel会把路径作为簇点资源的名称，**无法区分路径相同但请求方式不同的接口**，查询、删除、修改等都被识别为一个簇点资源，这显然是不合适的。

所以我们可以选择打开Sentinel的请求方式前缀，把**`请求方式 + 请求路径`作为簇点资源名**：

首先，在`cart-service`的`application.yml`中添加下面的配置：

```YAML
spring:
  cloud:
    sentinel:
      transport:
        dashboard: localhost:8090
      http-method-specify: true # 开启请求方式前缀
```

然后，重启服务，通过页面访问购物车的相关接口，可以看到sentinel控制台的簇点链路发生了变化：

![image-20250404102323002](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404102323002.png)



本质就是要避免微服务故障 然后 避免传递这个影响

![image-20250404101411966](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101411966.png)

也称**级联失败**

![image-20250404101525092](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101525092.png)



### 请求限流

![image-20250404101623321](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101623321.png)

![image-20250404105046459](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404105046459.png)



**请求限流：设置qps阈值 也就是限制每秒的并发**

| 指标           | 含义                                     |
| -------------- | ---------------------------------------- |
| **QPS**        | 每秒通过的请求数（速率控制）             |
| **并发线程数** | 某一时刻“同时在处理”的请求数（并发控制） |



QPS：控制每秒可以进多少请求 ✅

并发：控制“同时”能有多少个请求正在处理中 ✅

~~~markdown
1. QPS 限流 类比：每秒最多放多少人进窗口排队
QPS 就像工作人员每秒只放固定数量的人进入售票区

设定 QPS = 5 ⇒ 每秒只能放 5 个人进窗口区排队

超过的人就得等下一秒再放进去

目的：防止短时间内人涌入太多，冲垮窗口系统

📌 这个时候排队的系统看的是“单位时间的进入量”。

2. 并发线程数限流 类比：售票窗口最多同时服务几个人
并发线程数就像售票窗口数量有限，同时最多只能服务 N 个人

比如设置最大并发 = 3 ⇒ 同时只有 3 个窗口在服务

第 4 个人进来就要排队等前面的人办完离开，才轮到自己

目的：防止服务窗口超载，系统崩溃 / **防止其他服务窗口不够用！**

📌 这个时候控制的是“同一时刻能同时服务的人数”
~~~

![image-20250630143546642](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630143546642.png)

#### 流控模式



![image-20250630143114124](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630143114124.png)

#### 流控效果

![image-20250630150125978](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630150125978.png)

![image-20250630150138578](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630150138578.png)

![image-20250630151622543](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630151622543.png)

**==使用时结合官方文档解释==**



---



### 线程隔离

![image-20250404101656615](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101656615.png)

tomcat是有资源限制的

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404110245168.png)



![image-20250404110621934](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404110621934.png)

---



**tomcat也可以设置这些配置！！！**

需要注意的是，默认情况下SpringBoot项目的tomcat最大线程数是200，允许的最大连接是8492，单机测试很难打满。

所以我们需要配置一下cart-service模块的application.yml文件，修改tomcat连接：

```YAML
server:
  port: 8082
  tomcat:
    threads:
      max: 50 # 允许的最大线程数
    accept-count: 50 # 最大排队等待数量
    max-connections: 100 # 允许的最大连接
```





修改cart-service模块的application.yml文件，开启Feign的sentinel功能：

```YAML
feign:
  sentinel:
    enabled: true # 开启feign对sentinel的支持
```

这样就可以让feignClient 也变成一个簇点资源

!Sentinel控制台支持热更新功能。通过 Sentinel控制台，你可以动态地加载和更新规则，而无需重启应用。这种动态规则的加载和更新对于快速响应系统变化、应对突发流量和维护系统的稳定性非常重要





#### Fallbck

![image-20250404132414920](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404132414920.png)

![image-20250404132442683](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404132442683.png)



![image-20250404132501246](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404132501246.png)

返回这个client对象 并且要实现所有client方法的失败逻辑





**编写这个接口方法如果异常执行的逻辑**

这个方法就是feignclient 中的方法 也就是对应着远程调用的接口方法



![image-20250404132510380](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404132510380.png)



错误处理逻辑 ：不处理的话就是抛出限流异常 

处理的话可以返回给用户一些 友好的数据 如空值 或者 默认值（根据返回值 和 业务逻辑而定）





~~~java
@Slf4j
public class ItemClientFallbackFactory implements FallbackFactory<ItemClient> {
    @Override
    public ItemClient create(Throwable cause) {
        return new ItemClient() {
            @Override
            public void deductStock(List<OrderDetailDTO> items) {
                log.error("扣减商品库存失败");
                throw new RuntimeException(cause);
                // 有些业务不知道如何处理的就直接抛出异常就行了 由调用者来处理即可
                
            }

            @Override
            public List<ItemDTO> getItemsByIds(Collection<Long> ids) {
                log.error("查询商品失败");
                return CollUtils.emptyList();

            }
        }

    }
}

~~~





~~~java
    @Bean
    public ItemClientFallbackFactory itemClientFallbackFactory() {
        return new ItemClientFallbackFactory();
    }

//————————————————————————————————————————————————————————————————————————————————————

@FeignClient(value = "item-service",fallbackFactory = ItemClientFallbackFactory.class)
public interface ItemClient {

    @GetMapping("/items")
    List<ItemDTO> getItemsByIds(@RequestParam("ids") Collection<Long> ids);

    @PutMapping("/items/stock/deduct")
    public void deductStock(@RequestBody List<OrderDetailDTO> items);


}
~~~





### 服务熔断

![image-20250630163842326](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630163842326.png)

![image-20250630164040395](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630164040395.png)

**最小请求数：样本量要上去才有统计的必要**

![image-20250630164314488](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630164314488.png)



![image-20250630164916995](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630164916995.png)





![image-20250404101704226](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101704226.png)



![image-20250404144023481](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404144023481.png)



![image-20250404144033368](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404144033368.png)



![image-20250404144041677](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404144041677.png)



熔断了所有请求也是走fallback逻辑

![image-20250404101711369](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250404101711369.png)



# 热点规则

![image-20250630165150182](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630165150182.png)

![image-20250630165515882](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630165515882.png)



![image-20250630165455587](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630165455587.png)

**注意是==目前==**

**只要是用fallback的兜底回调方法签名一定要写 Throwable 异常**

![image-20250630172157585](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250630172157585.png)

| **特性**         | `fallback`                                                   | `blockHandler`                                               |
| :--------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **触发条件**     | <span style="color:#FF0000;">处理**所有异常**（包括业务异常）</span> | <span style="color:#0000CC;">仅处理 Sentinel 规则触发的 `BlockException`（限流/熔断/系统保护）</span> |
| **适用场景**     | 通用降级（如数据库异常、远程调用失败）                       | 流量控制（如 QPS 超限、慢调用熔断）                          |
| **方法签名要求** | 必须包含 `Throwable` 参数                                    | 必须包含 `BlockException` 参数                               |
| **执行优先级**   | 低于 `blockHandler`（若同时配置）                            | 优先于 `fallback`                                            |
| **典型应用**     | Feign 客户端降级、业务逻辑兜底                               | Sentinel 资源规则的快速失败响应                              |

`Throwable` 是 Java 中所有**错误（Error）和异常（Exception）的顶级父类**



# ==Sentinel面试题==







---



# ==Seata（分布式事务）== 

[项目中使用Seata](https://www.bilibili.com/video/BV1XtMyznEnb/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36)



![image-20250702001415903](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702001415903.png)

---

# Seata的四种事务模式详解

Seata提供了四种分布式事务模式，每种模式适用于不同的业务场景，具有不同的实现方式和特点。

## 1. AT模式（Automatic Transaction，自动补偿型事务）
**用途**：最常用的模式，适用于大多数业务场景，对代码侵入性小。

**实现原理**：
- **一阶段**：业务数据和回滚日志（undo_log）在同一个本地事务中提交
- **二阶段**：
  - 成功：异步删除undo_log
  - 失败：通过undo_log生成反向SQL进行补偿

**特点**：
- 使用`@GlobalTransactional`注解即可开启
- 依赖数据库的本地ACID特性
- 需要创建undo_log表存储回滚数据

**示例代码**：
```java
@GlobalTransactional
public void purchase() {
    // 业务逻辑
    orderService.create();
    storageService.deduct();
    accountService.debit();
}
```

## 2. TCC模式（Try-Confirm-Cancel）
**用途**：适用于需要高一致性保证的业务，如金融支付等。

**实现原理**：
- **Try**：预留业务资源（如冻结金额）
- **Confirm**：确认执行业务操作（如扣减冻结金额）
- **Cancel**：取消预留（如解冻金额）

**特点**：
- 需要手动实现三个接口
- 无全局锁，性能较好
- 业务侵入性强

**示例代码**：
```java
public interface TccAction {
    @TwoPhaseBusinessAction(name = "prepare", commitMethod = "commit", rollbackMethod = "rollback")
    boolean prepare(BusinessActionContext actionContext, 
                   @BusinessActionContextParameter(paramName = "param") String param);
    
    boolean commit(BusinessActionContext actionContext);
    boolean rollback(BusinessActionContext actionContext);
}
```

## 3. Saga模式
**用途**：适用于长事务场景，如跨多个服务的业务流程。

**实现原理**：
- 将长事务拆分为多个本地事务
- 每个本地事务有对应的补偿操作
- 失败时按相反顺序执行补偿

**特点**：
- 无锁设计，适合长时间运行的事务
- 不保证隔离性
- 需要设计完善的补偿机制

**示例实现**：
```java
@SagaStart
public void travelBooking() {
    flightBooking();
    hotelBooking();
    carRental();
}
```

## 4. XA模式
**用途**：适用于需要强一致性的传统应用。

**实现原理**：
- 基于数据库的XA协议
- 两阶段提交（2PC）
- 依赖数据库厂商的XA实现

**特点**：
- 强一致性
- 性能较差（同步阻塞）
- 数据锁定时间长

**示例配置**：

```properties
# 数据源配置
seata.enable-auto-data-source-proxy=true
seata.data-source-proxy-mode=XA
```

## 各模式对比

| 特性         | AT模式   | TCC模式  | Saga模式   | XA模式   |
| ------------ | -------- | -------- | ---------- | -------- |
| **一致性**   | 最终一致 | 最终一致 | 最终一致   | 强一致   |
| **性能**     | 高       | 中       | 高         | 低       |
| **侵入性**   | 低       | 高       | 中         | 低       |
| **隔离性**   | 部分隔离 | 无隔离   | 无隔离     | 完全隔离 |
| **适用场景** | 常规业务 | 金融支付 | 长流程业务 | 传统应用 |

`@GlobalTransactional`注解主要用于AT模式和XA模式，是Seata最常用的编程方式。选择哪种模式取决于业务对一致性、性能和复杂度的要求。



---





**XA协议的2pc与3pc**

优点：能利用数据库自身的功能进行本地事务的提交和回滚，不会侵入业务代码，完全由数据库完成

缺点： 1.阻塞：当所有事务参与者收到命令后，就会执行事务相关操作，但是不提交事务。在这个期间，如果有更多相同的请求进来，此时因为没有提交事务，那么这些请求都会被阻塞(阻塞的原因：增删改都是一种当前读，所以在进行增删改时会先读取数据，读取的是记录的最新版本，同时会对读取的记录进行加锁，这样那些相同的请求自然无法执行事务就会被阻塞) 

2.资源浪费：如果某一个参与者已经挂了，那么第一阶段，其他参与者接受到准备命令，就会执行事务操作，因为一个参与者不可用，那么这些已经执行的事务操作肯定就会回滚，，那之前执行的事务操作就是一种资源浪费



3PC在2PC的基础多了一个询问阶段，准备、预提交和提交三个阶段

**第一阶段：**准备阶段用来判断每个参与者是否正常，防止出现某一个参与者已经挂了，其他的参与者还在执行事务操作

第二阶段：预提交阶段就是2PC的准备阶段，事务协调者发送一个预提交命令，每个事务参与者收到命令后，就会执行事务相关操作，但是不提交事务（除了提交事务之外所有事都做了)，然后参与者返回响应，告诉协调者是否准备成功

**第三阶段：**提交阶段和2PC的提交阶段一样，如果所有参与者响应的是准备成功，就发送给所有参与者一个提交命令，如果有任何一个参与者响应的是准备失败，就发送给所有参与者一个回滚命令

**总结：**2PC和3PC都是分布式事务中强一致性的体现，3PC虽然是为了解决2PC的些问题才出现的，**但是多一个阶段也多了一次通讯的开销**，**而且参与者挂的概率很低**，所以多数都是无用的通讯。所以基于XA协议的2PC和3PC,除非是对**强一致性**有极高要求的系统，比如金融系统，为了保证资金的安全，**会使用这种强一致性的方案**



**AT模式（就是二阶提交协议）**

**AT模式是基于最终一致性的技术方案，也是Seata最流行和最常用的事务模式(默认方案)，因为它对业务代码的侵入性很小，并且能够提供良好的性能诅**

 **AT模式的核心思想是基于UNDO LOG的最终一致性。这个UNDO LOG记录了数据的原始值，也就是数据快照，用于在事务回滚时恢复数据，可以分为两个阶段**

**第一阶段：每个事务参与者执行事务相关操作，并且直接把事务提交，同时把数据的原始值记录在undo log中，最后返回事务状态**

**第二阶段：协调者根据所有参与者的执行结果，如果所有参与者结果是成功，。就通知参与者异步删除undolog;如果有参与者的结果是失败，就通知参与者根据undo log,恢复成数据的原始值，然后再删除undo log**

![image-20250702002425676](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702002425676.png)



**TCC模式**

![image-20250702002815302](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702002815302.png)



**Saga模式**

![image-20250702002849227](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702002849227.png)

**本地消息：**

![image-20250702003228011](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702003228011.png)

**事务消息:**

![image-20250702003440740](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702003440740.png)





**本地消息表和消息队列对代码侵入度比较高就是要写很多业务代码**

---



也可以用消息队列实现一致性 主要SeaTa原理要知道就行了



![image-20250701224058908](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701224058908.png)

`@GlobalTransactional` 只发起全局事务（由 Seata 的 TM 控制）

**被调用服务必须明确声明自己的本地事务（@Transactional）**

否则该服务的数据库操作将不会被 Seata 的 RM（Resource Manager）识别参与事务协调



1. **事务发起阶段**
   - TM向TC发起"开始全局事务"请求
   - TC生成全局唯一的XID(事务ID)
2. **分支事务注册**
   - 业务执行过程中，各RM向TC注册分支事务
   - RM将XID绑定到本地事务上
3. **业务执行阶段**
   - 各微服务执行自己的业务逻辑
   - RM管理本地事务资源
   - 各RM定期向TC报告分支事务状态
4. **全局事务决议**
   - 业务逻辑完成后，TM向TC发起全局提交或回滚请求
   - TC根据所有分支事务状态决定最终操作
5. **分支事务提交/回滚**
   - TC向所有RM发送提交或回滚指令
   - 各RM执行相应操作并反馈结果

---

**Seata 服务器 （TC）**

~~~xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
</dependency>

~~~

**每个微服务都需要引入一个conf文件  配置seata服务器等等参数 一般就是将这个配置存到nacos中**



@Transactional（Spring 本地事务）声明一个 **本地事务**（在单个服务、单个数据库内控制事务提交与回滚）

 **注意事项：**

- **异常必须是 RuntimeException（非检查异常）** 才会触发回滚
- 默认只在当前方法内部有效（跨类调用无效）



@GlobalTransactional（Seata 分布式事务） 声明一个 **Seata 全局事务**，用于管理**多个微服务之间的事务一致性**（例如多个服务/数据库操作必须同时成功或同时回滚）



![image-20250701234704806](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701234704806.png)

### 二阶提交协议



![image-20250701235442067](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701235442067.png)



==**全局锁**== 是一个**逻辑上的概念**，强调“全系统只能有一个线程访问某资源”；
 ==**分布式锁**== 是**实现全局锁的一种技术手段**，在 **多台服务器** 中协调资源访问。

![image-20250702000815661](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702000815661.png)







# ==分布式事务 面试题==

---



# MQ入门

MQ就是用于异步通信的

![image-20250329213216428](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329213216428.png)



![image-20250329213657928](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329213657928.png)



## 同步调用

<span style="font-size:1.3em; background:#990000; color:#FFFFFF;">**开闭原则：**</span>

**对扩展开放（Open for extension）**

- 允许对已有系统进行扩展，以满足新的需求，而不需要修改已有代码。
- 通过增加新的代码（如新的类或方法）来增强功能，而不是修改原有代码。

**对修改关闭（Closed for modification）**

- 一旦一个类、模块或函数经过测试并投入使用，就不应该频繁修改其内部实现，否则可能引入新的错误。
- 现有代码不应因新需求而被改动，而是通过 **新增代码** 来适应变化。

---

![image-20250329214504567](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329214504567.png)

## 异步调用

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329214805035.png)





![image-20250329223157238](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329223157238.png)









## MQ技术选型

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329230541290.png)

官网：https://www.rabbitmq.com/

安装：

- 15672：RabbitMQ提供的**管理控制台**的端口
- 5672：RabbitMQ的**消息发送处理接口**

~~~bash
docker run \  # 启动一个新的容器
  -e RABBITMQ_DEFAULT_USER=senjay \      # 设置默认登录用户名为 senjay
  -e RABBITMQ_DEFAULT_PASS=123321 \      # 设置默认登录密码为 123321
  -v mq-plugins:/plugins \               # 将名为 mq-plugins 的 Docker 卷挂载到容器内 /plugins 目录（可用于插件）
  --name mq \                            # 给容器命名为 mq，方便管理
  --hostname mq \                        # 设置容器主机名为 mq（对集群和内部通信有用）
  -p 15672:15672 \                       # 映射管理后台端口（宿主机15672 → 容器15672），Web UI用
  -p 5672:5672 \                         # 映射AMQP协议端口（宿主机5672 → 容器5672），供客户端连接
   # --network hm-net\
  -d \                                   # 以守护进程（后台）方式运行容器
  rabbitmq:3.8-management                # 使用 RabbitMQ 3.8 带管理插件版本的官方镜像

~~~





![image-20250329234319297](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329234319297.png)

---

**交换机不存储消息只是负责转发**

多个项目共享 这个RabbitMQ Server

防止冲突，隔离操作。





![image-20250329234428484](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250329234428484.png)







## RabbitMQ 的java客户端

![image-20250330124451858](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330124451858.png)

![image-20250330125259550](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330125259550.png)

## 生产者配置





![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330125306417.png)

![image-20250330125601171](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330125601171.png)

**这边是直接向队列发送！！！**（不是向交换机发送 ）



![image-20250330130530293](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330130530293.png)







---



**WorkQueue：**

一个生产者（Producer）将任务消息放入队列，多个消费者（Worker）从同一个队列中轮流取出任务并处理。

它的目标是负载均衡，比如后台处理图片、视频转码、邮件发送等耗时操作时，把任务排队分发给多个后台 worker 处理。

![image-20250330132922472](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330132922472.png)





![image-20250330132904694](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330132904694.png)



---

**消费者配置：**



![image-20250330132935856](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330132935856.png)

---

**使用==交换机==**

 ## Fanout交换机

- ‌**Fan-in（扇入）**‌：指一个模块或逻辑门允许的输入端数量，即**有多少个上级模块或信号可以调用它**。（被调入）
- ‌**Fan-out（扇出）**‌：指一个模块或逻辑门能够驱动的下级模块或信号数量，即其输出端可以连接的负载数量。 （反之）

多扇入少扇出！！！过高的扇出会增加管理复杂性，可通过增加中间层次优化。

![image-20250330140005200](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330140005200.png)



![image-20250330140717058](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330140717058.png)

---



## Direct交换机

![image-20250330141222439](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330141222439.png)

![image-20250702114828778](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702114828778.png)



也可有一样的BindingKey 这样所有队列都可以收到同个RoutingKey的消息

  交换机可以和队列绑定多个key

  ![image-20250330142852275](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330142852275.png)

**==交换机==根据消息的==RouteKey==  ==转发消息==到相应队列中**

**消费者监听==消息队列== 接收消息**

![image-20250702115111719](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702115111719.png)



![image-20250330142910328](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330142910328.png)

## Topic交换机

bindingKey决定**交换机**如何路由消息到**消息队列**

**生产者 通过交换机根据bindingKey 决定发送消息到哪个消息队列中**

**而消费者就是监听某一个消息队列的**

![image-20250330143216056](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330143216056.png)











---



**SUM：**

| 类型     | 路由规则                              | 应用场景                                | 是否支持模糊匹配 |
| -------- | ------------------------------------- | --------------------------------------- | ---------------- |
| `fanout` | 广播：**所有绑定的队列都收到消息**    | 群发通知、广播消息，如：系统公告        | ❌                |
| `direct` | 精确匹配：`routingKey` 完全相等       | 一对一/一对多精确路由，如：订单状态通知 | ❌                |
| `topic`  | 模糊匹配：`routingKey` 支持通配符匹配 | 日志系统、业务模块分发等                | ✅                |

## ==代码中声明队列&交换机==

### 基于Bean

(*用到在补充)

配置类中 声明

代码复杂不够优雅

![image-20250702173921780](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702173921780.png)



---



### 基于注解



![image-20250330144605372](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330144605372.png)

`durable = "true"` 的作用是：**声明队列/交换机为持久化的。**

它会让 RabbitMQ 在**服务重启之后**，依然**保留这个队列/交换机的元信息**，不会丢失



## 消息转换器

![image-20250330150152912](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330150152912.png)



message 可以是Object 但是网络传输发送时需要发送的是字节 所以 这个方法名叫转换并发送

转换就是由消息转换器来转换的

| 概念                            | 说明                                                       |
| ------------------------------- | ---------------------------------------------------------- |
| **序列化（Serialization）**     | 把对象转换成可存储/可传输的格式（如字节数组、JSON 字符串） |
| **反序列化（Deserialization）** | 把这种格式的数据再还原成原始对象（内存中的类实例）         |

![image-20250330152146281](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330152146281.png)

![image-20250702132253339](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702132253339.png)



![ ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250330152155560.png)

在==**发送/接收**== RabbitMQ 消息时，**使用 JSON 格式进行序列化/反序列化**，而不是默认的 Java 序列化（jdk序列化）。”

> **JSON 是一种数据格式**，
>  **Jackson 是一个 Java 框架/工具，用来处理 JSON 格式的数据。**



**ctrkl + H 展示类层级**

![image-20250702133534430](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702133534430.png)

![image-20250702133816523](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702133816523.png)

---



# RabbitMQ 在项目中的实际应用

**<span style="color:#CC0000;">带有<span style="color:#00994C;">  事务性 </span> 的操作，用 mq 提高性能，<span style="color:#3333FF;">线程池适用于 1.异步不影响主线程 2.多线程执行任务（任务之间无协同关系）</span></span>**



# ==消息队列面试题==



**服务解耦 异步调用 削峰填谷**

 ![image-20250702134933935](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702134933935.png)

## 如何保证消息不丢失

<span style="color:#FF007F;">注意是==<span style="color:#0000FF;">rabbitMQ</span>== 还是 ==springAMQP== 的**机制**</span>

### 生产者可靠性

![image-20250703115241769](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703115241769.png)



![image-20250702135126086](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702135126086.png)





![image-20250702175508531](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702175508531.png)



![ ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703103038620.png)

![image-20250703103428528](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703103428528.png)



~~~java
@Test
void testPublisherConfirm() throws InterruptedException {
    // 1,创建CorrelationData
    CorrelationData cd = new CorrelationData(UUID.randomUUID().toString());

    // 2.FutureCorirmCallback
    cd.getFuture().addCallback(new ListenableFutureCallback<CorrelationData.Confirm>() {
        @Override
        public void onFailure(Throwable ex) {
            // 2.1 Future发生异常时的处理逻辑，基本不会触发
            log.error("handle message ack fail", ex);
        }

        @Override
        public void onSuccess(CorrelationData.Confirm result) {
            // Future:接收到回执的处理逻辑，参数中的result.就是回执内容
            if (result.isAck()) {
                // 2.2 result,isAck(),boolean类型，true代表ack回执，false代表nack回
                log.debug("发送消息成功，收到ack!");
            } else {
                // result.getReason(),String.类型，返回hack时的异常捕述
                log.error("发送消息失败，收到nack,reason:{}", result.getReason());
            }
        }
    });

    // 3.发送消息
    rabbitTemplate.convertAndSend("hmall.direct", "redi", "hello", cd);
}

~~~







| **机制**         | **`publish-confirm`**              | **`publish-return`**                              |
| :--------------- | :--------------------------------- | :------------------------------------------------ |
| **作用**         | 确认消息是否被 Broker **成功接收** | 处理消息**无法路由到队列**的情况                  |
| **触发条件**     | Broker 接收消息后返回 `ack/nack`   | 消息无法路由到任何队列（需设置 `mandatory=true`） |
| **适用阶段**     | 生产者 → Broker（Exchange）        | Exchange → Queue（路由失败时）                    |
| **是否默认开启** | 需手动调用 `confirmSelect()`       | 需设置 `mandatory=true`                           |
| **典型用途**     | 确保消息到达 Broker                | 处理路由键（`routingKey`）错误或队列不存在的情况  |



---

### MQ的可靠性

**这种版本不一样得确认一下 特性**



![image-20250702135635000](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702135635000.png)

**普通队列 + 消息持久化** 与 LazyQueue 性能差异

![image-20250703110837891](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703110837891.png)



![image-20250703104932104](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703104932104.png)

![image-20250703110352742](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703110352742.png)

---



### 消费者可靠性

**ack**nowledge(告知收悉)

![image-20250703111948449](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703111948449.png)

**当业务出现异常时，根据异常判断返回不同结果：**
◆如果是业务异常，会自动返回nack
◆如果是**消息处理或校验**  异常，自动返回reject



![image-20250703114331942](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703114331942.png)

#### 失败重试机制





![ ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702135921495.png)



![image-20250703115402417](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703115402417.png)

![image-20250703121522745](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703121522745.png)

![   ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703121737650.png)







![image-20250702140448974](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702140448974.png)









---

## 消息的重复消费问题如何解决





### 🎯 为什么会出现重复消费？

RabbitMQ（或其他 MQ，如 Kafka、RocketMQ）在以下情况下会**重复投递消息**：

| 情况                         | 原因                                         |
| ---------------------------- | -------------------------------------------- |
| 消费端处理失败未 ack         | RabbitMQ 认为消费失败，会**重新投递**        |
| 消费端超时没 ack             | 超过一定时间没 ack，也会被认为消费失败重新发 |
| 消费端业务抛出异常           | RabbitMQ 不知道业务是否成功，就再发一次      |
| 网络波动/客户端掉线          | ack 没成功发出去，RabbitMQ 重新投递          |
| RabbitMQ 集群 failover       | 容错切换期间可能产生消息重复                 |
| 手动重试、消息堆积异常消费等 | 系统恢复后自动重试了多次                     |

**业务幂等性设计！！！**（保证非幂等的业务 幂等性）

![image-20250703183858553](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703183858553.png)



![image-20250703184110629](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703184110629.png)



这个方案性能会有损失

可以使用**业务判断保证幂等**

 ![image-20250703184730465](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703184730465.png)



---





![image-20250702141646764](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702141646764.png)







## Rabbit中的死信交换机 & 延迟队列

**死信交换机（Dead Letter Exchange, DLX）和死信队列（Dead Letter Queue, DLQ）**

都是RabbitMQ中用于处理**“失败消息”**的机制，但作用不同：

| **概念**     | **死信交换机（DLX）**                              | **死信队列（DLQ）**                      |
| :----------- | :------------------------------------------------- | :--------------------------------------- |
| **定义**     | 专门接收“死信”的交换机                             | 存储“死信”的队列                         |
| **作用**     | 决定死信的路由规则                                 | 存储被标记为死信的消息                   |
| **绑定关系** | 需要绑定到队列（通过`x-dead-letter-exchange`参数） | 需要绑定到死信交换机                     |
| **消息来源** | 来自普通队列（消息变成死信后自动转发）****         | **来自死信交换机**                       |
| **用途**     | 提供灵活的路由（如按原因分发给不同队列）           | 存储死信，供后续处理（如人工干预或重试） |



![image-20250702142632557](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702142632557.png)

![image-20250702143532567](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702143532567.png)

~~~java
@Bean
public Queue ttlQueue() {
    return QueueBuilder.durable("simple.queue") // 指定队列名称，并设置为持久化
        .ttl(18088)                              // 设置队列中的消息过期时间（单位毫秒）
        .deadLetterExchange("dl.direct")         // 设置死信交换机，当消息过期或被拒绝时转发到此交换机
        .build();                                // 构建最终的队列对象
}


// 可用注解
@RabbitListener(
    bindings = @QueueBinding(
        value = @Queue(
            value = "simple.queue",         // 队列名称
            durable = "true",               // 持久化
            arguments = {
                @Argument(name = "x-message-ttl", value = "18088", type = "java.lang.Integer"), // TTL：18秒
                @Argument(name = "x-dead-letter-exchange", value = "dl.direct") // 指定死信交换机
            }
        ),
        exchange = @Exchange(value = "my.direct", type = ExchangeTypes.DIRECT),
        key = "my.key" // 绑定的 routing key
    )
)
public void listen(String msg) {
    System.out.println("接收到消息: " + msg);
}

~~~

1. `QueueBuilder.durable("simple.queue")`

- 创建一个名为 `simple.queue` 的**持久化队列**
- 持久化意味着：**RabbitMQ 重启后队列依然存在**



2. `.ttl(18088)`

- 设置该队列内的消息的**统一过期时间**
- 单位是毫秒（ms）→ `18088 ms ≈ 18 秒`
- **队列级别的 TTL**：所有进入该队列的消息，超时未被消费就会“死掉”（变成死信）



3. `.deadLetterExchange("dl.direct")`

- 设置**死信交换机**（Dead Letter Exchange，DLX）
- 如果消息在 `simple.queue` 中变成死信（例如：过期、被拒绝），会被 RabbitMQ 自动转发到这个交换机
- 后续可以通过绑定死信队列来专门处理这些“异常消息”

![image-20250702183645733](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702183645733.png)

**延迟队列 = TTL + 死信交换机**

 ~~~tiki wiki
 1️⃣ 生产者发送消息
      ↓
 2️⃣ 投递到一个「没有消费者」的延迟队列（delay.queue）
      ↓   （设置 TTL = 想延迟的时间，例如 30 秒）
 3️⃣ 消息在 delay.queue 中等待 TTL 到期
      ↓
 4️⃣ TTL 到期后消息会变成“死信” 被自动转发到死信交换机（DLX）
      ↓
 5️⃣ 死信交换机根据 routing key 将消息路由到真正的业务处理队列（real.queue）
      ↓
 6️⃣ real.queue 被消费者监听并消费
 
 ~~~



**还可以通过延迟队列插件来使用延迟队列**

![image-20250702183943191](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702183943191.png)

![image-20250702184101981](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702184101981.png)

我们当时一个什么业务使用到了延迟队列（超时订单、限时优惠、定时发布.…)·

其中延迟队列就用到了死信交换机和TTL(消息存活时间)实现的·

消息超时未消费就会变成死信（死信的其他情况：拒绝被消费，队列满了）



延迟队列插件实现延迟队列DelayExchange声明一个交换机，添加delayed属性为true发送消息时，添加x-delay头，值为超时时间





### 消息堆积如何解决

![image-20250702184823085](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702184823085.png)



![image-20250702185338788](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702185338788.png)





## RabbitMQ的高可用机制

在生产环境下，使用集群（cluster）来保证高可用性

普通集群、==**镜像集群**==、仲裁队列

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702215403446.png)

  镜像队列是旧版 RabbitMQ 的高可用机制，**从 RabbitMQ 3.10 起被官方标记为废弃（deprecated）**，建议新项目改用 **仲裁队列（Quorum Queue）**



![image-20250702215510279](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702215510279.png)

![image-20250702215635107](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250702215635107.png)

| 角色                         | 描述                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| 🟢 主节点（Master / Leader）  | 负责接收生产者发布的消息、向消费者投递消息，是唯一的“活跃节点” |
| 🔵 从节点（Slave / Follower） | 不接收消息，只同步主节点的数据，用于备份和故障转移           |
| 🔴🔁 故障转移                  | 主节点挂掉时，从节点中自动选出新的主节点接管服务             |

🟢🔵🔴



# Kafka

kafka是分布式系统，通常以集群的方式部署：
也就是说会同时存在多个Broker实例，这些实例一般部署在不同的服务器上

![image-20250719231048858](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719231048858.png)

**副本**是分区的另一种表现方式 **实际消息的读写交互都在副本上！ 副本分为leader 和 follower**



 ![image-20250719231147218](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719231147218.png)



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719231515993.png" alt="image-20250719231515993" style="zoom: 33%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719231549614.png" alt="image-20250719231549614" style="zoom: 33%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719231633545.png" alt="image-20250719231633545" style="zoom:33%;" />

一个kafka实例中可以有多个分区 

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719232010256.png" alt="image-20250719232010256" style="zoom:33%;" />

**关系类比：**

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719232149224.png" alt="image-20250719232149224" style="zoom:33%;" />

## ZooKeeper（2.8 后引入 KRaft）

在 Kafka 2.8 及更早版本中，ZooKeeper 主要用来协调 Kafka 的各个 Broker（Broker 注册与发现、选举分区副本 leader），以及存储 **Kafka 中的元数据**（例如主题、分区、副本）即协调中心和元数据仓库。具体作用如下：

### 1. 存储 Kafka 的元数据

Kafka Broker 在启动过程中，会把所有元信息（Topic 的信息、分区的信息等、Broker 的注册信息）在 ZooKeeper 注册并保持相关的元数据更新。

由于 ZooKeeper 提供了监听机制，生产者或消费者程序会在 ZooKeeper 上注册相关的监听器，一旦 ZooKeeper 中记录的元信息发生变化，生产者或消费者能够及时感知并进行相应调整。这样就保证了在实现集群的动态扩容或缩容的过程中，各个 Broker 间仍能自动实现负载均衡，并能感知集群的变化。同时，ZooKeeper 利用监听的机制监听 Broker 和 Leader 副本的存活性。

### 2. 管理 Broker

在 Kafka Broker 启动成功后，会向 ZooKeeper 注册 Broker 的信息，从而实现服务器正常运行下的水平拓展。

不仅可以实现 Broker 的负载均衡，而且当增加 Broker 或某个 Broker 故障时，ZooKeeper 会通知生产者和消费者，这样可以保证整个系统正常运转。

同时，当我们成功创建 Topic 后，ZooKeeper 也会维护 Topic 与 Broker 之间的对应关系，这是通过 `/brokers/topics/topic.name` 节点来记录的。

### 3. 管理消费者

消费者可以使用 Consumer Group（消费者组）的形式消费 Kafka 集群中的消息数据。消费者在启动的过程中需要指定一个 Consumer Group 的 ID，这个 ID 会被 ZooKeeper 记录和维护，以保证同一份数据可以被同一个 Consumer Group 的不同消费者多次消费。

同时 ZooKeeper 管理消费者的偏移量用于跟踪当前消费者消费的位置。

### 4. ZooKeeper 对生产者的意义

生产者在启动过程中，会向 ZooKeeper 中注册监听器，从而帮助生产者了解 Topic 中的分区信息，包括分区的增加、减少、副本的选举等。同时生产者通过动态了解运行情况实现负载均衡。

## Kafka KRaft 模式

从 Kafka 2.8 开始引入了 **KRaft** 模式，旨在最终取代 ZooKeeper，将元数据管理功能集成到 Kafka Broker 内部，进一步简化部署和运维，对比 ZooKeeper 优势：

1. 简化集群部署和管理 —— 不在需要 zookeeper，简化了 Kafka 集群的部署和管理工作，资源占用更小
2. 提高可扩展性和弹性 —— 单个集群中的分区数量可以扩展到百万个。集群重启和故障恢复时间更短
3. 更高效的元数据传播 —— 基于日志、事件驱动的元数据传播提高了 Kafka 许多核心功能的性能

目前 KRaft 只适用于新建集群，将现有的集群从 zookeeper 模式迁移到 KRaft 模式，需要等到 3.5 版本，Kafka 4.0（2025 年 3 月发布）将完全删除 zookeeper 模式，仅支持 KRaft 模式。 [kafka 4.0 文档]

所以截止目前 2025 年，除了一些新项目外，Kafka 在大部分项目中用的依旧是 **zookeeper 来作为 Kafka 的协调中心和元数据仓库**

------

### 参考文档：

- https://kafka.apache.org/downloads#3.3.1
- https://kafka.apache.org/documentation/#kraft
- https://developer.confluent.io/learn-kafka/architecture/control-plane/
- https://www.confluent.io/blog/why-replace-zookeeper-with-kafka-raft-the-log-of-all-logs/

---



**同一个消费者组里 无法/不能  有两个消费者对 同一个分组消费消息**

![image-20250719233052743](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719233052743.png)



**只要控制消费者 在组里的组成关系 就可以实现以下两种消息模型**

![image-20250719233321283](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719233321283.png)





![image-20250719233522102](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719233522102.png)

![image-20250719233528734](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719233528734.png)

Kafka 的消费是“自己决定何时拉消息”，支持海量数据处理，常用于日志、数据管道。

**kafka不仅可以作为消息队列使用**

**rabbitmq是Broker 主动推送消息到消费者。**

---



**日志**

**消息中心 推送 如发布订阅 关注粉丝的模式**





![image-20250719234154740](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719234154740.png)

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719234931147.png" alt="image-20250719234931147" style="zoom:33%;" />

# Kafka面试题



