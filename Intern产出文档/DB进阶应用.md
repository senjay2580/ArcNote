

# 数据库连接池-==单例==

在本机资源管理器或者IE浏览器输入ftp地址,例如：ftp://localhost:220/或者ftp://192.168.146.140:220/

**ftp://192.168.0.103:2121** 

**\\\192.168.0.103 (SMB 协议)**

---



**对象存储、文件存储、块存储**

**适配接口的好处-  适配器模式**

S3 协议（Amazon Simple Storage Service API）是亚马逊为其 S3 云存储服务定义的一套**标准化的 HTTP 接口规范**，简单说就是「操作对象存储的通用 “语言”」。

它规定了如何通过 HTTP/HTTPS 协议上传、下载、删除、查询文件（对象），包括请求的 URL 格式、参数、头部信息、签名验证方式等。只要遵循这套规范，任何对象存储服务（比如 MinIO、阿里云 OSS、腾讯云 COS 等）都能被同一套代码操作。

MinIO 就相当于 自己部署的对象存储 （aliyun Oss）





### Druid 的核心定位与特点

1. **基础连接池功能**

   和 HikariCP、C3P0 等一样，Druid 的核心作用是管理数据库连接：维护连接池、复用连接以减少创建 / 销毁开销、控制最大连接数防止数据库过载等，满足连接池的基本需求。

2. **增强特性（区别于普通连接池）**

   - **内置监控**：提供可视化监控页面（如 SQL 执行效率、连接池状态、慢查询统计），支持通过`druid-stat.html`页面实时查看系统运行状态。
   - **SQL 防护**：内置 SQL 注入检测、黑名单拦截等功能，增强数据库访问安全。
   - **丰富的统计数据**：记录 SQL 执行次数、耗时、事务成功率等，便于性能分析和问题排查。
   - **扩展能力**：支持自定义过滤器（如加密数据源密码、日志记录），适配复杂业务场景。

### 在 Spring Boot 中使用 Druid

由于 Spring Boot 默认使用 HikariCP，若要切换为 Druid，需手动引入依赖并配置（以 Maven 为例）：

1. 引入 Druid Starter：

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.8</version> <!-- 版本号可根据最新稳定版调整 -->
</dependency>
```

1. 配置连接池参数（`application.yml`）：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
    druid:  # Druid专属配置
      initial-size: 5  # 初始化连接数
      max-active: 20   # 最大连接数
      min-idle: 5      # 最小空闲连接数
      max-wait: 60000  # 获取连接的最大等待时间（毫秒）
      # 监控配置
      stat-view-servlet:
        enabled: true   # 开启监控页面
        login-username: admin  # 监控页面登录用户名
        login-password: 123456 # 监控页面登录密码
      filter:
        stat:
          enabled: true # 开启SQL统计过滤
          slow-sql-millis: 2000 # 慢SQL阈值（毫秒，超过则记录）
```

1. 访问监控页面：启动项目后，通过`http://localhost:8080/druid`访问监控界面，输入配置的用户名密码即可查看连接池状态、SQL 执行详情等。

### 与 HikariCP 的对比

- **性能**：HikariCP 以轻量、高效著称，性能略优于 Druid（尤其在高并发短连接场景）。
- **功能**：Druid 胜在监控、安全等增强特性，适合需要精细化管理和监控的生产环境。
- **适用场景**：简单业务或对性能极致追求时用 HikariCP；复杂系统、需要监控和安全防护时用 Druid。



| 组件           | 作用                               | 类比              |
| -------------- | ---------------------------------- | ----------------- |
| 应用软件       | 提出数据读写需求（业务逻辑）       | 寄件人            |
| MyBatis        | 管理 SQL、参数、结果映射，简化代码 | 快递单 + 流程规范 |
| **数据库驱动** | 建立连接、发送 SQL、转换数据格式   | 钥匙 + 配送车     |
| 数据库软件     | 存储数据、执行 SQL                 | 仓库              |

不同数据库的 SQL 语法存在差异（如 MySQL 的`LIMIT`、Oracle 的`ROWNUM`、PostgreSQL 的`SERIAL`自增等），这是 “数据库方言” 问题。MyBatis 和数据库驱动通过各自的机制协同解决，确保在多数据库场景下代码能兼容运行。\



驱动是连接应用与数据库的 “专属翻译官”，会根据数据库类型处理底层通信细节：

- 不同数据库需要对应驱动（如 MySQL 用`mysql-connector-j`，Oracle 用`ojdbc8`），驱动内部已适配数据库的协议和基础语法。

MyBatis 的核心功能是 “SQL 映射”（把 Java 方法映射到 SQL 语句），它本身不解析 SQL 语法，也不关心你用的是哪种数据库。无论你写的是 MySQL、Oracle 还是 PostgreSQL 的 SQL，MyBatis 都会原样交给数据库驱动。

所以主要看的是**驱动**



# 多数据源-工厂模式

**数据源：**

**DataSource** 是 Java 提供的一个标准接口（`javax.sql.DataSource`），它的职责是：

> 提供数据库连接对象（`Connection`）给应用程序使用。



经验推广：多数据源和单数据源 配置的问题 
**第三方类/自定义Bean** 读取**配置文件前缀注意问题**  层级！

**见yudao文档**

​	

---



核心原因是 **“不同数据的存储需求不同”**，单一数据库难以满足所有场景，举例：

1. **数据类型差异：**
   - 结构化数据（如用户信息、订单记录）适合用 MySQL 等关系型数据库（强事务、强一致性）；
   - 非结构化 / 半结构化数据（如日志、用户行为、复杂嵌套的 JSON 数据）适合用 MongoDB 等 NoSQL 数据库（灵活扩展、高写入性能）。
2. **业务隔离：**
   - 核心业务（如支付）和非核心业务（如统计报表）分开存储，避免互相影响（比如报表查询不占用核心库的资源）。
3. **历史系统兼容：**
   - 新项目可能需要对接多个旧系统的数据库，需同时操作不同数据源。



工厂模式是一种**创建型设计模式**，核心思想是：**“用工厂类统一负责对象的创建，而不是让用户直接通过 `new` 关键字创建”**。

它的作用是：

- 隐藏对象创建的复杂逻辑（比如数据库连接需要处理 URL、账号、驱动加载等）；
- 让用户无需关心 “具体创建哪个类的实例”，只需告诉工厂 “想要什么类型的对象”；
- 便于扩展（新增一种对象类型时，只需修改工厂，无需修改使用方代码）。

从简单到复杂，分为**简单工厂模式**、**工厂方法模式**、**抽象工厂模式**。



多数据源场景中，框架对不同驱动和连接的管理逻辑，其实暗合了**工厂模式**的设计思想——通过一个“工厂”统一创建不同类型的“产品”（如MySQL连接、MongoDB连接），隐藏创建细节。下面详细解释工厂模式：


### 一、什么是工厂模式？  
工厂模式是一种**创建型设计模式**，核心思想是：**“用工厂类统一负责对象的创建，而不是让用户直接通过 `new` 关键字创建”**。  

它的作用是：  
- 隐藏对象创建的复杂逻辑（比如数据库连接需要处理URL、账号、驱动加载等）；  
- 让用户无需关心“具体创建哪个类的实例”，只需告诉工厂“想要什么类型的对象”；  
- 便于扩展（新增一种对象类型时，只需修改工厂，无需修改使用方代码）。  


### 二、工厂模式的三种类型  
从简单到复杂，分为**简单工厂模式**、**工厂方法模式**、**抽象工厂模式**。  


#### 1. 简单工厂模式（Simple Factory）  
最基础的工厂模式，由一个工厂类根据传入的参数，决定创建哪个具体类的实例。  

**结构**：  
- **产品接口**：定义所有产品的通用方法；  
- **具体产品**：实现产品接口的具体类（如MySQL连接、MongoDB连接）；  
- **工厂类**：提供静态方法，根据参数创建对应的具体产品实例。  

**代码示例**（模拟数据库连接工厂）：  
```java
// 1. 产品接口：数据库连接
public interface Connection {
    void connect(); // 连接数据库
}

// 2. 具体产品1：MySQL连接
public class MySQLConnection implements Connection {
    @Override
    public void connect() {
        System.out.println("连接MySQL数据库（使用MySQL驱动）");
    }
}

// 3. 具体产品2：MongoDB连接
public class MongoDBConnection implements Connection {
    @Override
    public void connect() {
        System.out.println("连接MongoDB数据库（使用MongoDB驱动）");
    }
}

// 4. 简单工厂类：创建连接
public class ConnectionFactory {
    // 静态方法：根据类型创建对应连接
    public static Connection createConnection(String type) {
        if ("mysql".equals(type)) {
            return new MySQLConnection();
        } else if ("mongodb".equals(type)) {
            return new MongoDBConnection();
        } else {
            throw new IllegalArgumentException("不支持的数据库类型");
        }
    }
}

// 使用方式
public class Main {
    public static void main(String[] args) {
        // 无需直接new，通过工厂创建
        Connection mysqlConn = ConnectionFactory.createConnection("mysql");
        mysqlConn.connect(); // 输出：连接MySQL数据库（使用MySQL驱动）

        Connection mongoConn = ConnectionFactory.createConnection("mongodb");
        mongoConn.connect(); // 输出：连接MongoDB数据库（使用MongoDB驱动）
    }
}
```

**特点**：  
- 优点：用户无需关心对象创建细节，只需调用工厂方法；  
- 缺点：如果新增产品（如Oracle连接），需要修改工厂类的 `createConnection` 方法，违反“开闭原则”（对扩展开放，对修改关闭）。  


#### 2. 工厂方法模式（Factory Method）  
为了解决简单工厂的“开闭原则”问题，工厂方法模式将**工厂抽象化**，每个具体产品对应一个具体工厂，新增产品时只需新增对应的工厂，无需修改原有代码。  

**结构**：  
- **产品接口**：定义产品通用方法；  
- **具体产品**：实现产品接口；  
- **工厂接口**：定义创建产品的方法（抽象方法）；  
- **具体工厂**：实现工厂接口，负责创建对应的具体产品。  

**代码示例**（改进数据库连接工厂）：  
```java
// 1. 产品接口（同上）
public interface Connection {
    void connect();
}

// 2. 具体产品（同上）
public class MySQLConnection implements Connection { ... }
public class MongoDBConnection implements Connection { ... }

// 3. 工厂接口：定义创建连接的方法
public interface ConnectionFactory {
    Connection createConnection(); // 抽象方法，由具体工厂实现
}

// 4. 具体工厂1：创建MySQL连接
public class MySQLFactory implements ConnectionFactory {
    @Override
    public Connection createConnection() {
        return new MySQLConnection();
    }
}

// 5. 具体工厂2：创建MongoDB连接
public class MongoDBFactory implements ConnectionFactory {
    @Override
    public Connection createConnection() {
        return new MongoDBConnection();
    }
}

// 使用方式
public class Main {
    public static void main(String[] args) {
        // 想要MySQL连接，就用MySQL工厂
        ConnectionFactory mysqlFactory = new MySQLFactory();
        Connection mysqlConn = mysqlFactory.createConnection();
        mysqlConn.connect();

        // 想要MongoDB连接，就用MongoDB工厂
        ConnectionFactory mongoFactory = new MongoDBFactory();
        Connection mongoConn = mongoFactory.createConnection();
        mongoConn.connect();
    }
}
```

**特点**：  
- 优点：新增产品时，只需新增“具体产品类”和“具体工厂类”，无需修改原有代码，符合开闭原则；  
- 缺点：每增加一个产品，就需要新增两个类（产品+工厂），类数量会增多。  


#### 3. 抽象工厂模式（Abstract Factory）  
当需要创建**一系列相互关联的产品族**时（比如“MySQL连接+MySQL语句”“MongoDB连接+MongoDB命令”），抽象工厂模式可以一次性创建一整套产品，保证产品之间的兼容性。  

**结构**：  
- **产品接口族**：多个相关的产品接口（如连接接口、命令接口）；  
- **具体产品族**：实现接口族的具体产品（如MySQL连接+MySQL语句）；  
- **抽象工厂接口**：定义创建一整套产品的方法（每个方法对应一个产品接口）；  
- **具体工厂**：实现抽象工厂，负责创建对应的产品族。  

**代码示例**（数据库连接+命令的产品族）：  
```java
// 1. 产品接口族
public interface Connection { void connect(); } // 连接接口
public interface Command { void execute(); }    // 命令接口（如SQL/BSON）

// 2. 具体产品族1：MySQL系列
public class MySQLConnection implements Connection {
    @Override
    public void connect() { System.out.println("MySQL连接成功"); }
}
public class MySQLCommand implements Command {
    @Override
    public void execute() { System.out.println("执行MySQL SQL语句"); }
}

// 3. 具体产品族2：MongoDB系列
public class MongoDBConnection implements Connection {
    @Override
    public void connect() { System.out.println("MongoDB连接成功"); }
}
public class MongoDBCommand implements Command {
    @Override
    public void execute() { System.out.println("执行MongoDB BSON命令"); }
}

// 4. 抽象工厂接口：定义创建一整套产品的方法
public interface DatabaseFactory {
    Connection createConnection(); // 创建连接
    Command createCommand();       // 创建命令
}

// 5. 具体工厂1：创建MySQL产品族
public class MySQLDatabaseFactory implements DatabaseFactory {
    @Override
    public Connection createConnection() { return new MySQLConnection(); }
    @Override
    public Command createCommand() { return new MySQLCommand(); }
}

// 6. 具体工厂2：创建MongoDB产品族
public class MongoDBFactory implements DatabaseFactory {
    @Override
    public Connection createConnection() { return new MongoDBConnection(); }
    @Override
    public Command createCommand() { return new MongoDBCommand(); }
}

// 使用方式
public class Main {
    public static void main(String[] args) {
        // 使用MySQL工厂，一次性获取配套的连接和命令
        DatabaseFactory mysqlFactory = new MySQLDatabaseFactory();
        Connection mysqlConn = mysqlFactory.createConnection();
        Command mysqlCmd = mysqlFactory.createCommand();
        mysqlConn.connect();   // MySQL连接成功
        mysqlCmd.execute();    // 执行MySQL SQL语句

        // 使用MongoDB工厂，获取配套的连接和命令
        DatabaseFactory mongoFactory = new MongoDBFactory();
        Connection mongoConn = mongoFactory.createConnection();
        Command mongoCmd = mongoFactory.createCommand();
        mongoConn.connect();   // MongoDB连接成功
        mongoCmd.execute();    // 执行MongoDB BSON命令
    }
}
```

**特点**：  
- 优点：能保证同一工厂创建的产品是“配套”的（比如MySQL连接只能搭配MySQL命令），适合有产品族的场景；  
- 缺点：如果需要新增产品族中的某个产品（如新增“事务”接口），所有工厂都需要修改，扩展性较差。  


### 三、工厂模式的应用场景  
1. **对象创建复杂，需要隐藏细节**  
   比如数据库连接（需要处理驱动、URL、账号密码）、线程池（需要设置核心线程数、队列大小）等，用工厂封装创建逻辑。  

2. **需要根据条件动态创建不同类型的对象**  
   比如日志框架（根据配置动态创建“文件日志”或“控制台日志”对象）、支付系统（根据支付方式创建“支付宝”或“微信支付”对象）。  

3. **避免用户直接依赖具体类，降低耦合**  
   用户只依赖产品接口和工厂接口，不关心具体实现类，后续替换实现类时无需修改用户代码。  

4. **框架中的应用**  
   - Spring 的 `BeanFactory`：通过工厂模式创建和管理所有 Bean 对象；  
   - JDBC 的 `DriverManager`：本质是简单工厂，根据 URL 自动创建对应数据库的 `Connection`；  
   - 日志框架 SLF4J：通过工厂模式适配不同的日志实现（如 Logback、Log4j）。  

### 四、注册工厂模式与传统工厂模式的关系

- **属于工厂模式的扩展**：它本质上还是工厂模式（通过工厂创建对象，隐藏创建细节），只是增加了 “动态注册” 的机制，解决了传统工厂模式扩展性不足的问题。
- 与简单工厂的区别：简单工厂的产品类型是硬编码在工厂中的（`if-else`），而注册工厂的产品类型是动态注册的（运行时可修改）。
- 与工厂方法的区别：工厂方法通过 “新增工厂类” 扩展产品，而注册工厂通过 “注册新的创建器” 扩展产品，更灵活（无需新增类）。



---



**系统中存在多个独立的数据连接（DataSource）**，无论是不是同一种数据库引擎

在 Java / Spring 中，`DataSource` 本质上就是一个数据库连接池对象，比如：

- HikariDataSource
- DruidDataSource
- BasicDataSource（DBCP）



## 多数据源具体配置

**“配置多数据源→建立数据源标识→动态路由数据源→业务层指定使用”**，通过 Spring 的 AOP 切面实现数据源的灵活切换

**核心目标：**

在同一项目中同时连接多个数据库（如主库写、从库读），业务层可通过注解或手动方式，指定方法 / 类使用哪个数据源，实现 “读写分离” 或 “多库协同”。



# 多数据源配置全流程分析（基于Ruoyi框架）
整个流程的核心是 **“配置多数据源→建立数据源标识→动态路由数据源→业务层指定使用”**，通过Spring的AOP切面实现数据源的灵活切换，以下是分步拆解：

## 一、核心目标
在同一项目中同时连接多个数据库（如主库写、从库读），业务层可通过注解或手动方式，指定方法/类使用哪个数据源，实现“读写分离”或“多库协同”。

## 二、全流程拆解（对应你提供的5个步骤）
### 1. 第一步：配置从库数据源（application-druid.yml）
- **作用**：告诉项目“从库的连接信息”，并提供开关控制是否启用。
- 关键细节：
  - `slave.enabled: true`：开启从库数据源（默认关闭，需要时手动打开）。
  - `url/username/password`：从库的JDBC连接地址、账号密码（和主库配置格式一致，仅连接目标不同）。
  - 主库配置默认已存在（框架自带），这里新增从库配置，形成“主+从”双数据源。

### 2. 第二步：添加数据源枚举（DataSourceType类）
- **作用**：给每个数据源一个“唯一标识”，方便后续代码中指定使用哪个数据源。
- 逻辑：
  - 原有枚举可能只有`MASTER`（主库），新增`SLAVE`（从库）。
  - 枚举的核心是“统一标识”，避免代码中写硬编码字符串（如直接写"slave"容易出错）。

### 3. 第三步：配置从库数据源Bean（DruidConfig类）
- **作用**：通过Spring注解，将yml中的从库配置“实例化”为DataSource对象（Druid连接池的数据源实例）。
- 关键注解解释：
  - `@Bean`：将方法返回的DataSource对象交给Spring容器管理，成为一个可注入的Bean。
  - `@ConfigurationProperties("spring.datasource.druid.slave")`：自动读取yml中该前缀下的配置（url、username等），赋值给DataSource对象。
  - `@ConditionalOnProperty(...)`：条件注解，只有当`slave.enabled=true`时，才创建这个从库数据源Bean（避免无用实例）。
- 补充：主库数据源Bean已在框架中默认配置，这里新增从库Bean，容器中会有两个DataSource实例（master、slave）。

### 4. 第四步：注册数据源到动态路由（DruidConfig的dataSource方法）
- **作用**：将主库、从库数据源统一交给“动态数据源路由”管理，让框架知道“哪个标识对应哪个数据源”。
- 关键逻辑：
  - `targetDataSources`是一个Map，key是数据源标识（如`DataSourceType.SLAVE.name()`，即"SLAVE"），value是对应的DataSource Bean（如`slaveDataSource`）。
  - 调用`setDataSource(...)`方法，将从库标识和从库数据源Bean的映射关系存入Map。
  - 最终会创建一个`DynamicDataSource`（动态数据源）对象，作为项目的“统一数据源入口”，替代原来的单一数据源。

### 5. 第五步：业务层指定数据源（注解/手动切换）
这是最终“使用”多数据源的环节，核心是通过某种方式告诉框架“当前方法要使用哪个数据源”。

#### 方式1：注解方式（推荐）
- 类级别注解：`@DataSource(value = DataSourceType.SLAVE)`加在Service类上，意味着该类中所有方法默认使用从库。
- 方法级别注解：加在单个方法上（如`selectUserList`），优先级高于类级别注解（方法注解会覆盖类注解）。
- 原理：框架通过AOP切面（`DataSourceAspect`）拦截被`@DataSource`注解的方法，在方法执行前切换到指定数据源，执行后恢复默认数据源。

#### 方式2：手动切换（灵活场景）
- 适用场景：方法内需要切换多个数据源（如先查从库，再查主库）。
- 关键API：
  - `DynamicDataSourceContextHolder.setDataSourceType(...)`：设置当前线程的数据源标识（如"SLAVE"），后续数据库操作会使用该数据源。
  - `DynamicDataSourceContextHolder.clearDataSourceType()`：清空当前线程的数据源标识，恢复默认数据源（通常是主库）。
- 注意：必须手动清空，否则会导致线程复用（如Tomcat线程池）时数据源错乱。

## 三、核心底层逻辑（DataSourceAspect切面）
这是多数据源能生效的“核心引擎”，隐藏在框架底层，作用是：
1. 拦截被`@DataSource`注解的方法（或类）。
2. 从注解中获取目标数据源标识（如"SLAVE"）。
3. 通过`DynamicDataSourceContextHolder`将标识存入当前线程的上下文（ThreadLocal）。
4. `DynamicDataSource`（动态数据源）会从ThreadLocal中获取标识，路由到对应的真实数据源（如从库DataSource）。
5. 方法执行完毕后，清空ThreadLocal中的标识，避免线程污染。

## 四、关键注意事项
1. `@DataSource`注解失效的解决：
   - 原因：Spring AOP只能拦截“外部调用”的方法，若Service内部方法调用（如A方法调用本类的B方法），注解会失效。
   - 解决：用`SpringUtils.getAopProxy(this).xxxxxx(xxxx)`，通过Spring的AOP代理对象调用方法，让切面能拦截到。

2. 多数据源支持扩展：
   - 新增从库（如SLAVE2）：只需重复步骤1（配置yml）、步骤2（加枚举）、步骤3（配置Bean）、步骤4（注册路由），即可支持N个数据源。
   - 不同数据库类型：只要JDBC驱动正确（如Oracle的驱动jar），url格式符合对应数据库要求，即可混合使用（Mysql+Oracle）。

3. 默认数据源：
   - 未加`@DataSource`注解的方法，会使用默认数据源（通常是主库MASTER），确保写操作（insert/update/delete）默认走主库，符合“读写分离”规范。



## 配置参考

还可排除三方框架jar中的 自动配置 为什么呢

![image-20251106111907251](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20251106111907251.png)





---



1. <span style="color:#FF0000; font-size:1.5em;">**MyBatis 与 Hibernate 的 ORM 自动化程度差异**</span>

MyBatis 是半自动的 ORM 框架，而 Hibernate 则是全自动的 ORM 框架。
ORM，全称 Object Relational Mapping，即对象关系映射；直白来说，是 Java 对象的属性和数据库表字段之间的映射。
全自动的 ORM 框架除了维护映射关系外，还能帮我们生成数据库 CRUD 操作的接口；反观半自动的 ORM 框架仅维护映射关系，不会生成数据库 CRUD 操作的接口。当然，MyBatis 官方提供的 generator 项目也可完成类似功能。

2. <span style="color:#FF0000; font-size:1.5em;">**数据库移植能力对比**</span>

MyBatis 的数据库移植能力不如 Hibernate。
因为 Hibernate 是全自动的 ORM 框架，CRUD 操作的接口由框架统一生成，底层 SQL 会匹配各种数据库方言的语法，所以它的数据库移植能力更好。

3. **<span style="color:#FF0000; font-size:1.5em;">复杂 SQL 优化的灵活性对比</span>**

复杂 SQL 的优化 MyBatis 比 Hibernate 更灵活。
MyBatis 支持自定义 SQL 来操作数据库，且支持动态 SQL 等特性，所以在复杂 SQL 的优化方面，MyBatis 的灵活性更好。

4. **<span style="color:#FF0000; font-size:1.5em;">缓存机制对比</span>**

MyBatis 的缓存机制不如 Hibernate 强大。
对于二级缓存中的脏数据，Hibernate 框架会报错并提示；而 MyBatis 框架则不会有任何提示，所以如果不能完全确定数据更新操作的波及范围，请谨慎使用二级缓存。

5. **<span style="color:#FF0000; font-size:1.5em;">开发工作量对比</span>**

MyBatis 在开发的工作量上要远大于 Hibernate。
MyBatis 作为半自动的 ORM 框架，在代码开发的工作量上要远大于 Hibernate，特别是在字段较多、多表关联查询时，更是如此！

6. **<span style="color:#FF0000; font-size:1.5em;">应用场景差异</span>**

两个框架的应用场景不同。
如果对于性能、响应速度要求较高，或者业务逻辑比较复杂的系统建议使用 MyBatis 框架；反之，则可以考虑使用 Hibernate 框架。





---



# 事务



### 声明式事务

**注意事项：**

@Transactional注解只能应用到public可见度的方法上

`Spring`的默认的事务规则是遇到运行异常`（RuntimeException）`和程序错误`（Error）`才会回滚。如果想针对检查异常进行事务回滚，可以在`@Transactional`注解里使用 `rollbackFor`属性明确指定异常。



 在业务层捕捉异常后，发现事务不生效。 这是许多新手都会犯的一个错误，在业务层手工捕捉并处理了异常，你都把异常“吃”掉了，`Spring`自然不知道这里有错，更不会主动去回滚数据。

`Transactional`注解的常用属性表：

| 属性          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| propagation   | 事务的传播行为，默认值为 REQUIRED。                          |
| isolation     | 事务的隔离度，默认值采用 DEFAULT                             |
| timeout       | 事务的超时时间，默认值为-1，不超时。如果设置了超时时间(单位秒)，那么如果超过该时间限制了但事务还没有完成，则自动回滚事务。 |
| read-only     | 指定事务是否为只读事务，默认值为 false；为了忽略那些不需要事务的方法，比如读取数据，可以设置 read-only 为 true。 |
| rollbackFor   | 用于指定能够触发事务回滚的异常类型，如果有多个异常类型需要指定，各类型之间可以通过逗号分隔。{xxx1.class, xxx2.class,……} |
| noRollbackFor | 抛出 no-rollback-for 指定的异常类型，不回滚事务。{xxx1.class, xxx2.class,……} |
| ....          |                                                              |

> 事务的传播机制是指如果在开始当前事务之前，一个事务上下文已经存在，此时有若干选项可以指定一个事务性方法的执行行为。 即:在执行一个@Transactinal注解标注的方法时，开启了事务；当该方法还在执行中时，另一个人也触发了该方法；那么此时怎么算事务呢，这时就可以通过事务的传播机制来指定处理方式。



`TransactionDefinition`传播行为的常量：

| 常量                                            | 含义                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| TransactionDefinition.PROPAGATION_REQUIRED      | 如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。这是默认值。 |
| TransactionDefinition.PROPAGATION_REQUIRES_NEW  | 创建一个新的事务，如果当前存在事务，则把当前事务挂起。       |
| TransactionDefinition.PROPAGATION_SUPPORTS      | 如果当前存在事务，则加入该事务；如果当前没有事务，则以非事务的方式继续运行。 |
| TransactionDefinition.PROPAGATION_NOT_SUPPORTED | 以非事务方式运行，如果当前存在事务，则把当前事务挂起。       |
| TransactionDefinition.PROPAGATION_NEVER         | 以非事务方式运行，如果当前存在事务，则抛出异常。             |
| TransactionDefinition.PROPAGATION_MANDATORY     | 如果当前存在事务，则加入该事务；如果当前没有事务，则抛出异常。 |
| TransactionDefinition.PROPAGATION_NESTED        | 如果当前存在事务，则创建一个事务作为当前事务的嵌套事务来运行；如果当前没有事务，则该取值等价于TransactionDefinition.PROPAGATION_REQUIRED。 |





### 编程式事务

| 实现方案                              | 技术依赖                | 核心 API / 组件                               | 优点具体表现                                                 | 缺点具体表现                                                 | 典型用场景                                   |
| ------------------------------------- | ----------------------- | --------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------- |
| **原生 JDBC 事务**                    | JDK 自带 JDBC API       | java.sql.Connection                           | 1. 无额外依赖，轻量级实现2. 完全底层控制，无封装黑盒3. 适合极简场景 | 1. 代码冗余，需重复编写 try-catch-rollback 模板2. 事务属性（隔离级别等）配置繁琐3. 不支持复杂事务传播 | 简单单体应用、无框架依赖的场景               |
| **Spring TransactionTemplate**        | Spring Context 模块     | TransactionTemplate、TransactionCallback      | 1. 模板化封装，减少重复代码2. 回调函数隔离业务与事务逻辑3. 支持声明式事务属性配置 | 1. 仍需显式编写事务模板代码2. 依赖 Spring 框架3. 复杂分支事务控制能力有限 | Spring 环境下的中等复杂度事务场景            |
| **Spring PlatformTransactionManager** | Spring Transaction 模块 | PlatformTransactionManager、TransactionStatus | 1. 支持最复杂的事务传播行为2. 可动态调整事务属性3. 多数据源事务协调能力强 | 1. 代码侵入性最高，事务逻辑与业务深度耦合2. 学习成本高，需理解事务状态管理3. 调试复杂度增加 | 分布式事务、嵌套事务、动态事务边界等复杂场景 |

### 分布式事务

在使用 Spring `@Transactional` 声明的事务中，无法进行数据源的切换，此时有 3 种解决方案：

① 拆分成多个 Spring 事务，每个事务对应一个数据源。如果是【写】场景，可能会存在多数据源的事务不一致的问题。

② 引入 Seata 框架，提供完整的分布式事务的解决方案，可学习 [《Seata 极简入门 》 (opens new window)](https://www.iocoder.cn/Seata/install/?yudao)文章。

③ 使用 Dynamic Datasource 提供的 [`@DSTransactional` (opens new window)](https://github.com/baomidou/dynamic-datasource/blob/master/dynamic-datasource-spring/src/main/java/com/baomidou/dynamic/datasource/annotation/DSTransactional.java)注解，支持多数据源的切换，不提供绝对可靠的多数据源的事务一致性（强于 ① 弱于 ②）



事务一共有 3 种解决方案，分别是：

- 单机 + 单数据源：`@Transactional` 注解
- 单机 + 多数据源：`@DSTransactional` 注解
- 多机 + 单/多数据源：Seata 分布式事务





# 索引





# sql优化

~~~xml
<dependency>
    <groupId>p6spy</groupId>
    <artifactId>p6spy</artifactId>
    <version>3.9.1</version>
</dependency>

~~~



**功能定位：**
 SQL 日志代理工具，用于打印格式化 SQL、参数值、执行耗时。

在 MyBatis-Plus 项目中，P6Spy 是一个常规“增强型 SQL 日志输出器”。
 对性能分析、SQL 调优特别有用。



**spy.properties 是干嘛的**

这个文件就是 **P6Spy 的配置文件**，告诉它“怎么拦截”、“拦截哪些日志”、“日志输出到哪儿”。

路径通常在：

```
src/main/resources/spy.properties
```

当项目启动时，P6Spy 会自动加载这个配置文件
