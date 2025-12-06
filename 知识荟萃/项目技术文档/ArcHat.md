# 后端 

## Maven 依赖

**依赖传递** ：Maven 定义了六种标准的作用域：`compile（可传递依赖）`, `provided`, `runtime（可传递依赖 但是只有在运行时可见）`, `test`, `system`, 和 `import（常用于微服务）`

**依赖冲突**：最短路径优先、先声明优先 （也可**手动**排除依赖  使用exclusion 标签/ optional标签（这样也不会传递））） 因为冲突很多情况下就是由传递导致的

**父子工程**：packaging ：pom（父工程用这个）、jar、war

**依赖继承**：在父工程的dependencies 标签内定义的依赖，都会被无条件继承到子模块当中 （很少使用）一般父工程就只管理依赖版本就行

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
< project xmlns = "http://maven.apache.org/POM/4.0.0" xmlns: xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsi: schemaLocation = "http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" >
    <modelVersion> 4.0.0 </modelVersion>
    <groupId> com.senjay </groupId>
    <artifactId> arcwater </artifactId>
    <version> 0.0.1-SNAPSHOT </version>
    <name> Arcwater </name>
    <description> Arcwater </description>
    <properties>
        <java.version> 11 </java.version>
        <project.build.sourceEncoding> UTF-8 </project.build.sourceEncoding>
        <project.reporting.outputEncoding> UTF-8 </project.reporting.outputEncoding>
        <spring-boot.version> 2.6.13 </spring-boot.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId> org.springframework.boot </groupId>
            <artifactId> spring-boot-starter </artifactId>
        </dependency>
        <dependency>
            <groupId> com.github.xiaoymin </groupId>
            <artifactId> knife4j-openapi2-spring-boot-starter </artifactId>
            <version> 4.1.0 </version>
        </dependency>
        <dependency>
            <groupId> org.springframework.boot </groupId>
            <artifactId> spring-boot-starter-web </artifactId>
        </dependency>
<!--        web依赖一定要有 不然就会像普通的java程序一样直接运行完就退出-->


        <dependency>
            <groupId> org.springframework.boot </groupId>
            <artifactId> spring-boot-starter-test </artifactId>
            <scope> test </scope>
        </dependency>

        <dependency>
            <groupId> org.projectlombok </groupId>
            <artifactId> lombok </artifactId>
            <version> 1.18.24 </version>
        </dependency>

<!--        数据库依赖-->
        <!--引入mybatis依赖-->
        <dependency>
            <groupId> org.mybatis.spring.boot </groupId>
            <artifactId> mybatis-spring-boot-starter </artifactId>
            <version> 2.3.0 </version> <!-- 兼容 Spring Boot 2.6.x -->
        </dependency>

        <dependency>
            <groupId> mysql </groupId>
            <artifactId> mysql-connector-java </artifactId>
            <version> 8.0.25 </version>
        </dependency>
<!--        Java连接MySQL数据库的JDBC驱动-->

        <dependency>
            <groupId> org.springframework.boot </groupId>
            <artifactId> spring-boot-starter-validation </artifactId>
        </dependency>
<!--        分页插件-->
        <dependency>
        <groupId> com.github.pagehelper </groupId>
        <artifactId> pagehelper-spring-boot-starter </artifactId>
        <version> 1.4.6 </version>
    </dependency>
    <!--    阿里云对象存储相关    -->
    <dependency>
        <groupId> com.aliyun.oss </groupId>
        <artifactId> aliyun-sdk-oss </artifactId>
        <version> 3.17.4 </version>
    </dependency>

    <dependency>
        <groupId> javax.xml.bind </groupId>
        <artifactId> jaxb-api </artifactId>
        <version> 2.3.1 </version>
    </dependency>
    <dependency>
        <groupId> javax.activation </groupId>
        <artifactId> activation </artifactId>
        <version> 1.1.1 </version>
    </dependency>
    <!-- no more than 2.3.3-->
    <dependency>
        <groupId> org.glassfish.jaxb </groupId>
        <artifactId> jaxb-runtime </artifactId>
        <version> 2.3.3 </version>
    </dependency>
    <!--      /阿里云对象存储相关-->

<!--        分页插件-->
        <dependency>
            <groupId> com.github.pagehelper </groupId>
            <artifactId> pagehelper-spring-boot-starter </artifactId>
            <version> 1.4.6 </version>
        </dependency>

    </dependencies>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId> org.springframework.boot </groupId>
                <artifactId> spring-boot-dependencies </artifactId>
                <version>${spring-boot.version}</version >
                <type> pom </type>
                <scope> import </scope>
            </dependency>
        </dependencies>




    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId> org.apache.maven.plugins </groupId>
                <artifactId> maven-compiler-plugin </artifactId>
                <version> 3.8.1 </version>
                <configuration>
                    <source> 11 </source>
                    <target> 11 </target>
                    <encoding> UTF-8 </encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId> org.springframework.boot </groupId>
                <artifactId> spring-boot-maven-plugin </artifactId>
                <version>${spring-boot.version}</version >
                <configuration>
                    <mainClass> com.senjay.ArcwaterApplication </mainClass>
<!--                    <skip> true </skip>-->
                </configuration>
                <executions>
                    <execution>
                        <id> repackage </id>
                        <goals>
                            <goal> repackage </goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>

~~~

## springboot 项目依赖 maven

这份 `pom.xml` 是一个 **Spring Boot 多模块 Maven 项目的聚合父模块（parent aggregator module）**，结构规范清晰，关键在于 **模块划分、依赖管理、版本集中定义、依赖继承与传递**。

下面我带你 **逐段解释** 内容和作用，最后再讲清楚 **依赖传递和继承是如何生效的**。

🧩 一、项目头部声明部分（版本、命名空间）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
```

这段是 Maven 标准 XML 头，指定使用 Maven POM 4.0.0 格式，没啥特别，所有 Maven 项目都长这样。

🧱 二、项目基础信息

```xml
<modelVersion>4.0.0</modelVersion>
<parent>
    <artifactId>spring-boot-starter-parent</artifactId>
    <groupId>org.springframework.boot</groupId>
    <version>2.7.3</version>
</parent>
```

✅ 作用：

- 继承 Spring Boot 官方父项目的配置（默认插件版本、依赖版本管理、属性、打包方式等）
- 所有子模块也会 **间接继承这个配置**

比如你用：

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

你 **不需要指定 `<version>`**，因为父项目已经管理好了依赖的版本号。

🏷️ 三、当前模块的身份定义

```xml
<groupId>com.sky</groupId>
<artifactId>sky-take-out</artifactId>
<packaging>pom</packaging>
<version>1.0-SNAPSHOT</version>
```

✅ 解释：

| 标签                         | 含义                                         |
| ---------------------------- | -------------------------------------------- |
| `<groupId>`                  | 公司或组织的标识                             |
| `<artifactId>`               | 模块名，Maven 坐标的一部分                   |
| `<packaging>pom</packaging>` | 表示这是一个 **父模块**，本身不会打成 jar 包 |
| `<version>`                  | 当前项目版本                                 |

🧩 四、模块聚合

```xml
<modules>
    <module>sky-common</module>
    <module>sky-pojo</module>
    <module>sky-server</module>
</modules>
```

✅ 作用：

- 声明这是一个 **多模块项目**
- 子模块的 `pom.xml` 会被一并构建、编译
- 父模块执行 `mvn install` 会自动构建这些子模块

🧰 五、统一版本管理（properties）

```xml
<properties>
    <mybatis.spring>2.2.0</mybatis.spring>
    <lombok>1.18.20</lombok>
    ...
</properties>


<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>${lombok}</version>
</dependency>




```

✅ 作用：

- 集中定义各个依赖的版本号，**方便统一维护**
- **子模块也可以使用 `${lombok}` 形式引用这些版本**

📦 六、依赖管理（dependencyManagement）

```xml
<dependencyManagement>
  <dependencies>
    ...
  </dependencies>
</dependencyManagement>
```

✅ 作用：

- **定义依赖的版本，但不自动引入依赖**
- 子模块如果需要用这些依赖，只需写 `<artifactId>`，不需要再写 `<version>`，版本自动继承父模块
- <span style="font-size:1.1em; color:#FF0000;">**避免版本冲突，是多模块项目最关键的机制之一**</span>

📚 七、子模块中如何继承父模块依赖？

子模块的 `pom.xml` 中一般这样写：

```xml
<parent>
  <groupId>com.sky</groupId>
  <artifactId>sky-take-out</artifactId>
  <version>1.0-SNAPSHOT</version>
</parent>
```

这样就 **继承了整个父模块**：

- 继承了 Spring Boot 的父项目配置（通过爷爷级 `spring-boot-starter-parent`）
- **继承了你定义的 `<properties>` 和 `<dependencyManagement>`**
- **可以直接使用 `mybatis-spring` 等依赖，而不用指定版本！**

---

### BOM 是什么



**BOM（Bill Of Materials）** 是一种 Maven 技术，用来管理依赖的“版本一致性”。

你可以把它理解成：

> “Spring Boot 官方帮你把所有兼容的 starter 和相关依赖的版本都配好了”，你只需要添加 `<groupId>` 和 `<artifactId>`，不用自己写版本。

这样避免你：

- 自己一个个手动查版本
- 引入不兼容的 jar 包（版本冲突）



---



对于Import 作用域

**出现位置**：只能出现在 `<dependencyManagement>` 里，不能直接出现在普通 `<dependencies>` 里。

**作用**：导入一个 **BOM（Bill of Materials）** 文件，相当于把那份 BOM 里定义的依赖版本统一拉进来。

**本质**：`import` 并不会引入实际依赖，而是引入一个版本控制清单。你仍然要在 `<dependencies>` 中写依赖，只是不用重复写 `<version>`



**BOM（Bill of Materials，物料清单）** 就像一个“依赖版本对照表”，它本质上是一个 **POM 文件**，里面通常只定义了 `<dependencyManagement>` 部分，列出了很多依赖的 groupId、artifactId、version

---



**这句依赖：**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

**之所以不需要写 `<version>`**，是因为它也在你前面引入的这个 BOM 文件里：

```xml
<dependencyManagement>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring-boot.version}</version> <!-- = 2.6.13 -->
        <type>pom</type>
        <scope>import</scope>
    </dependency>
</dependencyManagement>
```

### 

Spring Boot 的 `spring-boot-dependencies` 这个 BOM 是一个庞大的 "依赖版本清单"，它 **提前帮你定义好了一整套兼容版本**，包括：

- `spring-boot-starter-validation`
- `spring-boot-starter-web`
- `mysql-connector-java`
- `mybatis-spring-boot-starter`
- `lombok`
- 甚至是 `jackson`, `logback`, `hibernate-validator`，等等！

也就是说：

> 你只要通过 BOM 管理了 `spring-boot-dependencies`，就可以放心地不写 Spring 相关依赖的版本，它们自动使用 BOM 中的版本。







## MAVEN 不知道该用什么 依赖冲突 问题

1. **Spring Boot 版本**：
   - 你使用的是 `Spring Boot 2.6.13`（对应 `spring-boot-dependencies` 版本也是 `2.6.13`）
   - **Spring Boot 2.x 系列** 默认支持 **Java 8~17**，但 **MyBatis Starter 3.x** 是专为 **Spring Boot 3.x** 设计的。
2. **MyBatis 依赖冲突**：
   - 你引入了 `mybatis-spring-boot-starter:3.0.0`，该版本要求 **Spring Boot 3.x+**，但你的项目基于 Spring Boot 2.6.x，导致 `ArticleMapper` 无法注入。

## 项目结构

![image-20250524213534930](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250524213534930.png)



![image-20250524213609100](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250524213609100.png)

![image-20250524213622781](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250524213622781.png)



![image-20250524214142913](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250524214142913.png)



## 数据库

## ==E-R 图==




### 数据库建表

| 问题                             | 解答                                                     |
| -------------------------------- | -------------------------------------------------------- |
| 为什么每次访问数据库是网络请求？ | 因为数据库是独立服务，JDBC 是通过 TCP 套接字连接数据库的 |
| 本地数据库也算网络请求吗？       | 是的，通过 `localhost` 的网络通信                        |
| 有不需要网络的数据库吗？         | 有，如 H2、SQLite（嵌入式数据库）                        |
| 每次操作都建立连接吗？           | 不是，连接池会复用连接，但每次 SQL 都会走网络            |







### 数据封装类

一般 vo 需要使用@Builder 注解使用 builder 构建对象

使用 DAO 的话就是使用 mybatis plus 无 sql 操作然后 mapper 里不写 sql 语句

| 项目                       | DTO / Request（请求）     | Entity（实体）           | VO / Response（返回）  | DAO（数据库访问）   |
| -------------------------- | ------------------------- | ------------------------ | ---------------------- | ------------------- |
| **用途**                   | 接收前端参数              | 映射数据库表字段         | 返回前端展示信息       | 操作数据库          |
| **字段来源**               | 表单/接口请求 JSON        | 数据库表字段             | Entity 或 Service 加工 | SQL 查询结果        |
| **是否带 ID**              | ❌ 通常无 id（新增）       | ✅ 必须有主键 id          | ✅ 需要时返回           | ✅ 通常有            |
| **敏感字段**               | ❌ 不建议传密码明文等      | ✅ 保留完整数据           | ❌ 不暴露敏感字段       | ✅                   |
| **注解使用**               | `@NotNull` 等 **校验注解** | `@Table`、`@Column`      | 通常无数据库注解       | MyBatis 或 JPA 注解 |
| **是否带逻辑字段**         | ✅ 可有控制参数            | ✅ 可有如 status、deleted | ✅ 通常有加工结果字段   | ✅                   |
| **是否可以与其它对象嵌套** | ✅ 常用嵌套表单结构        | ✅ 外键可关联对象或 ID    | ✅ 可包含子列表或对象   | ❌ 通常为纯表结构    |

~~~java
// entity

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder // User user = User.builder().id(1L).name("张三").build(); 建造者模式
@EqualsAndHashCode(callSuper = false) // @EqualsAndHashCode(callSuper = false)
@TableName(value = "user", autoResultMap = true) // 默认是 false  如果你有字段是枚举、List、JSON 类型，
// 必须加这个，MyBatis-Plus 才会用你的自定义 TypeHandler。
public class User {
    @TableId(value = "id", type = IdType.AUTO)
    Long id;
    @TableField("username")
    String username;
    @TableField("password")
    String password;
    @TableField("avatar")
    String avatar;
//    分析后期是不是可以扩展如果明确是只有两个状态就可使用 boolean
    @TableField("status")
    Boolean status;
    @TableField("create_time")
    LocalDateTime createTime;
    @TableField("exep")
    Integer exep;
}

~~~



### 实体类是否必须实现 `Serializable`？

| 场景                                                   | 是否必须实现 `Serializable` | 说明                                                         |
| ------------------------------------------------------ | --------------------------- | ------------------------------------------------------------ |
| **MyBatis-Plus 基本功能（增删改查）**                  | ❌ **不强制**                | MyBatis-Plus 不强制要求实体类序列化。只要你不涉及缓存、分布式传输等，一般可以不实现。 |
| **使用分布式框架（如 Dubbo、Spring Cloud）传输实体类** | ✅ **必须实现**              | 网络传输需要对象可序列化。                                   |
| **存入缓存（Redis、Ehcache 等）**                      | ✅ **必须实现**              | 对象缓存时需要可序列化（或使用 JSON 序列化替代）。           |
| **写入 Session**                                       | ✅ **建议实现**              | Session 会序列化对象，尤其是在集群环境中。                   |

```
// 快捷键 ctrl + B  entry from interface to impl or find useage
```



~~~java
// enum
package com.senjay.archat.common.user.domain.enums;


import lombok.AllArgsConstructor;
import lombok.Getter;


@Getter  // 不需要 set 函数
@AllArgsConstructor 
public enum UserStatusEnum {
    ONLINE(1, "在线"),
    OFFLINE(0, "离线")
    ;
    private final Integer code;
    private final String desc;


}

~~~

### 实体类校验

~~~java
// DTO / Request （Req）
// DTO 是接收前端数据的 所以一般就是在这里进行校验逻辑
// 用户基本信息
// controller 层接收 req/DTO 服务层进行封装信息为 entity 到 DAO 层, 然后 DAO 层就利用 mybatis plus 操作 与数据库对于的实体类 --entity
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
// 还有自定义校验 以及分组校验功能 @NotNull @NotEmpty @Email
//@Pattern(regexp = "正则表达式", message = "错误提示")

public class UserInfoDTO {
    @NotBlank
    @Size(min = 5, max = 20)
    private String  userName;

    @NotBlank()
    @Size(min = 6, max = 20)
    private String password;
}

~~~

~~~java
package com.senjay.archat.common.user.domain.vo;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
// VO/Response （Res）
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserProfileVO {
    private Long id;
    private String username;
    private String avatar;
    private Integer exep;
    private LocalDateTime createTime;
}

~~~







---



~~~java
// Result
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result <T> {
    // 自定义逻辑状态码
    private int code;
    private String msg;
    // 返回体
    private T result;



    public static <T> Result <T> success(T result) {
        return new Result <T>(200, "执行成功", result);
    }
    public static Result success(String msg){
        return new Result <>(200, msg, null);
    }
    public static Result success() {
        return new Result(200, "执行成功", null);
    }



    // 查表 阿里 java 开发手册 1
    public static <T> Result <T> fail(int code, String msg){
        return new Result <T>(code, msg, null);
    }
    // 500 不明确错误
    public static  Result fail(String msg){
        return new Result(500, msg, null);
    }

}

~~~









### DML

| 操作                  | 记录不存在时       | 是否抛异常 | 该怎么办   |
| --------------------- | ------------------ | ---------- | ---------- |
| MySQL UPDATE          | 不报错，影响行数 0 | 否         | 判断返回值 |
| MySQL DELETE          | 不报错，影响行数 0 | 否         | 判断返回值 |
| MyBatis update/delete | 返回 0             | 否         | 判断返回值 |

`PUT` 通常 **语义上是“整体更新”**，按规范应该提供 **完整资源**，否则可能会导致部分字段被清空。但你可以根据实际需要实现成“部分更新”。





---



## 配置文件

Spring Boot 项目中常见的一种“**配置绑定 + 工具类 Bean 注册**”的写法，目的就是：

> **将配置文件中的 OSS 信息封装成 Java 对象，并通过配置类自动生成工具类（AliOssUtil）的单例，供全项目调用。**

✅ 一、`AliOssProperties`：封装配置文件中的 Aliyun OSS 参数

```java
@Component
@ConfigurationProperties(prefix = "sky.alioss")
@Data
public class AliOssProperties {
    private String endpoint;
    private String accessKeyId;
    private String accessKeySecret;
    private String bucketName;
}
```

🌟 作用：

- 从配置文件中（比如 `application.yml`）读取如下内容：

```yaml
sky:
  alioss:
    endpoint: xxx.aliyuncs.com
    access-key-id: abc123
    access-key-secret: def456
    bucket-name: my-bucket
```

- 自动将这些值注入到 Java 对象中：
  - `endpoint` → `aliOssProperties.getEndpoint()`
  - `accessKeyId` → `aliOssProperties.getAccessKeyId()` ...

📌 为什么要这么做？

- **集中配置**：所有敏感信息和配置统一在 `.yml` 文件中管理。
- **便于维护**：改配置不改代码。
- **类型安全**：你可以直接获取字段而不是 `env.get("xxx")` 这种字符串查值。

✅ 二、`OssConfiguration`：Spring 容器中的 Bean 工厂类

```java
@Configuration
@Slf4j
public class OssConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public AliOssUtil aliOssUtil(AliOssProperties aliOssProperties){
        return new AliOssUtil(
            aliOssProperties.getEndpoint(),
            aliOssProperties.getAccessKeyId(),
            aliOssProperties.getAccessKeySecret(),
            aliOssProperties.getBucketName()
        );
    }
}
```

🌟 作用：

1. **创建并注册一个 `AliOssUtil` 工具类的单例 Bean**。
2. **自动注入配置类 `AliOssProperties` 的内容**。

---

# ==BUG==

Spring 在扫描 `@Controller`, `@RestController`, `@Service`, `@Component` 等注解的时候：

- 默认会将类名首字母小写作为 Bean 名称
- 所以两个类叫 `CategoryController`，都默认生成了 `categoryController` 这个 Bean 名
- ⚠️ Spring 容器里 **Bean 名不能重复**，否则就会报错！



🛠️ 解决方案

✅ 方案一：**给其中一个类手动指定唯一的 Bean 名称**

```java
@RestController("userCategoryController")
@RequestMapping("/user/category")
public class CategoryController {
    ...
}
@RestController("adminCategoryController")
@RequestMapping("/admin/category")
public class CategoryController {
    ...
}
```

加上 `("xxx")` 就是手动起名，避免冲突。



## 编码 Tips

Spring Boot 会自动扫描带有注解的接口，并将其@Mapper 注册为 Spring Bean。

可以不加 Mapper 注解但是要在启动类上加 

~~~java
@SpringBootApplication
@MapperScan({" com.senjay.archat.common.**.mapper "})
public class ArchatApplication {

    public static void main(String [] args) {
        SpringApplication.run(ArchatApplication.class, args);
    }

}

~~~



# ==各种功能实现==

# maven 打包技巧

```bash
mvn clean package -DskipTests
```

- `mvn`: 启动 Maven 构建工具。
- `clean`: 执行 `clean` 生命周期阶段，删除之前构建生成的所有文件（通常是 `target` 目录下的内容）。
- `package`: 执行 `package` 生命周期阶段，将编译好的代码打包成 JAR 或 WAR 文件。
- `-DskipTests`: 这是一个 Maven 参数，用于在执行 `package` 阶段时 **跳过所有测试**。这在 CI/CD 或本地快速构建时非常有用，可以节省大量时间。

### 枚举类缓存的使用

~~~java
/**
 * Description: 角色枚举
 */
@AllArgsConstructor
@Getter
public enum RoleEnum {
    GROUP_OWNER(1, "群主"),
    ADMIN(2, "群聊管理"),
    MEMBER(3, "群成员")
    ;

    private final Integer code;
    private final String desc;
    private static Map <Integer, RoleEnum> cache;

    static {
     
        cache = Arrays.stream(RoleEnum.values()).collect(Collectors.toMap(RoleEnum:: getCode, Function.identity()));
        // 
    }
    // 静态方法
    public static RoleEnum of(Integer code) {
        return cache.get(code);
    }
}

~~~

toMap/toxxx 接收**函数式接口** （可用lambda/方法引用简写）

 ![image-20250929210009726](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250929210009726.png)



![image-20250929211110168](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250929211110168.png)

~~~java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}

~~~



函数式接口只有一个抽象方法



## Knife4j 配置自定义

**函数式接口 ：定制化接口内部的抽象方法 （由框架自动地去调用这个接口内部的抽象方法）**

~~~java
@Configuration
public class OpenApiConfig {
    @Bean
    
    public OpenApiCustomizer globalHeaderCustomizer() {
        return openApi -> {
            Parameter tokenHeader = new Parameter()
                    .in(ParameterIn.HEADER.toString())
                    .schema(new StringSchema())
                    .name("Authorization")
                    .description("认证令牌")
                    .required(false);

//            Parameter requestIdHeader = new Parameter()
//                    .in(ParameterIn.HEADER.toString())
//                    .schema(new StringSchema())
//                    .name("X-Request-ID")
//                    .description("请求唯一标识")
//                    .required(false);
            // 添加到每个接口
            openApi.getPaths().values().forEach(pathItem ->
                    pathItem.readOperations().forEach(operation -> {
                        operation.addParametersItem(tokenHeader);
//                        operation.addParametersItem(requestIdHeader);
                    }));
        };
    }
}
~~~



## Json 对象转换器工具类

 JSON ↔ 对象

很多时候我们会把一些动态配置、规则、模板放在数据库里，用 **JSON 字段存储**。

- 查询出来时是 **字符串**
- 业务逻辑需要时，就转成 **对象/Map/List** 来用。

~~~java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
public class JsonUtils {
    private static final ObjectMapper jsonMapper = new ObjectMapper();
    
// JSON 字符串 → Java 对象   Class ：一个具体的 Java 类（非泛型或单一对象）
    public static <T> T toObj(String str, Class <T> clz) {
        try {
            return jsonMapper.readValue(str, clz);
        } catch (JsonProcessingException e) {
            throw new UnsupportedOperationException(e);
        }
    }
// 泛型在java 运行的时候会被擦除 支持泛型和嵌套类型：List<User>、Map<String, List<User>>   内部通过匿名类保留了 泛型信息，Jackson 能正确解析


    public static <T> T toObj(String str, TypeReference <T> clz) {
        try {
            return jsonMapper.readValue(str, clz);
        } catch (JsonProcessingException e) {
            throw new UnsupportedOperationException(e);
        }
    }

    
    public static <T> List <T> toList(String str, Class <T> clz) {
        try {
            return jsonMapper.readValue(str, new TypeReference <List<T> >() {
            });
        } catch (JsonProcessingException e) {
            throw new UnsupportedOperationException(e);
        }
    }
// 只想拿 JSON 的某些字段，而不想把整个 JSON 映射成对象。
    public static JsonNode toJsonNode(String str) {
        try {
            return jsonMapper.readTree(str);
        } catch (JsonProcessingException e) {
            throw new UnsupportedOperationException(e);
        }
    }
// json node 结构比较人性化 比起字符串
    public static <T> T nodeToValue(JsonNode node, Class <T> clz) {
        try {
            return jsonMapper.treeToValue(node, clz);
        } catch (JsonProcessingException e) {
            throw new UnsupportedOperationException(e);
        }
    }

    // 对象转json
    public static String toStr(Object t) {
        try {
            return jsonMapper.writeValueAsString(t);
        } catch (Exception e) {
            throw new UnsupportedOperationException(e);
        }
    }

}

~~~



**json node** （树结点）

~~~json
{
  "name": "Tom",
  "age": 20,
  "address": {
    "city": "Beijing",
    "zip": "100000"
  },
  "hobbies": ["reading", "swimming"]
}

~~~





# Java SPI 和 Spring SPI

**静态加载**：编译时就知道具体实现类

**动态加载**：在运行时才决定用哪个实现类，通常通过 **反射** 或 **依赖注入** 实现





**Java SPI（Service Provider Interface）**：

- **定义**：Java 内置的服务发现机制，基于 java.util.ServiceLoader，允许在运行时动态加载接口的实现类。
- **位置**：实现类在 META-INF/services 目录下的配置文件中指定（如 com.example.MyInterface 文件列出实现类）。
- **使用场景**：如 JDBC 驱动加载，框架扩展。

**Spring SPI**：

- **定义**：Spring 框架提供的服务发现机制，基于 spring.factories 配置文件，集成在 Spring Boot 的自动配置中。
- **位置**：实现类在 META-INF/spring.factories 文件中通过键值对配置。
- **使用场景**：Spring Boot 的 starter 模块、自动配置加载。

---

---

### **Java SPI 在 JDBC 中的使用**

#### **概念**
Java SPI 是 JDK 提供的一种服务发现机制，允许通过 `ServiceLoader` 动态加载服务实现。它在 JDBC 中主要用于加载数据库驱动（`java.sql.Driver`）。JDBC 4.0 引入了 SPI 机制，允许自动发现数据库驱动，无需显式调用 `Class.forName()`。

**实现方式**

- **SPI 配置**：数据库驱动的 JAR 包中需要在 `META-INF/services` 目录下创建一个文件，文件名是服务接口的全限定名（例如 `java.sql.Driver`），文件内容是实现类的全限定名。
  
  - 示例：MySQL 驱动 JAR 包中，`META-INF/services/java.sql.Driver` 文件内容可能是：
    ```
    com.mysql.cj.jdbc.Driver
    ```
- **加载过程**：
  
  1. 应用程序调用 `DriverManager.getConnection()`。
  2. `DriverManager` 使用 `ServiceLoader` 扫描类路径下所有 JAR 包中的 `META-INF/services/java.sql.Driver` 文件。
  3. 根据文件中声明的实现类，加载并注册驱动。
- **代码示例**：
  ```java
  Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", "user", "password");
  ```
  在 JDBC 4.0 及以上版本，无需显式调用 `Class.forName("com.mysql.cj.jdbc.Driver")`，因为 SPI 会自动加载驱动。

**是否需要手动写配置信息？**

- **不需要**：使用 Java SPI 时，驱动的提供者（例如 MySQL、PostgreSQL）已经在 JAR 包中提供了 `META-INF/services/java.sql.Driver` 文件，开发者无需手动编写配置信息。
- **例外**：如果驱动不支持 JDBC 4.0（如早期版本），或 SPI 配置缺失，则需要手动调用 `Class.forName()` 加载驱动。

**优点**

- 自动发现驱动，简化代码。
- 标准化的服务发现机制，适用于所有支持 SPI 的驱动。

**缺点**

- 缺乏灵活性，SPI 只支持简单的服务发现，无法处理复杂的依赖注入或配置。
- 如果类路径中有多个驱动实现，加载顺序不可控，可能导致冲突。

---

### **Spring SPI 在 JDBC 中的使用**

**概念**

Spring SPI 并不是一个正式的 SPI 机制，而是 Spring 框架内部基于其依赖注入（DI）和自动配置机制实现的类似 SPI 的功能。在 JDBC 场景中，Spring SPI 通常指 Spring Boot 的自动配置功能，用于简化数据库连接的配置，例如通过 `spring-boot-starter-data-jdbc` 或 `spring-boot-starter-jpa`。

**实现方式**

- **自动配置**：Spring Boot 使用 `@Conditional` 注解和 `spring.factories` 文件（位于 `META-INF/spring.factories`）来实现自动配置。
  - 例如，`spring-boot-starter-data-jdbc` 的 `spring.factories` 文件可能包含：
    ```
    org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
    org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
    ```
  - 当 Spring Boot 检测到类路径中有特定的数据库驱动（例如 MySQL 或 H2），`DataSourceAutoConfiguration` 会自动配置 `DataSource` Bean。
- **配置方式**：
  - 开发者在 `application.properties` 或 `application.yml` 中提供数据库连接信息：
    ```properties
    spring.datasource.url=jdbc:mysql://localhost:3306/test
    spring.datasource.username=user
    spring.datasource.password=password
    spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
    ```
  - Spring Boot 会根据这些配置自动创建 `DataSource` Bean，并注入到 JDBC 模板（如 `JdbcTemplate`）或 JPA 相关组件中。
- **代码示例**：
  ```java
  @Autowired
  private JdbcTemplate jdbcTemplate;
  
  public void query() {
      jdbcTemplate.query("SELECT * FROM users", (rs, rowNum) -> rs.getString("name"));
  }
  ```
  Spring Boot 自动配置了 `DataSource` 和 `JdbcTemplate`，开发者无需手动创建。

**是否需要手动写配置信息？**

- **需要部分配置**：虽然 Spring Boot 的自动配置极大简化了配置，但开发者仍需在 `application.properties` 或 `application.yml` 中提供数据库连接信息（如 URL、用户名、密码等）。
- **例外**：如果使用嵌入式数据库（如 H2），Spring Boot 可以自动配置默认的连接信息，甚至无需手动配置。

**优点**

- 高度集成，自动配置 `DataSource`、`JdbcTemplate` 等组件，减少样板代码。
- 支持复杂的依赖注入和配置管理，适合企业级应用。
- 可通过 `application.properties` 灵活调整配置。

**缺点**

- 依赖 Spring 生态，增加了框架复杂度。
- 需要手动配置 `application.properties`，对配置文件的正确性有一定要求。

**Java SPI 和 Spring SPI 在 JDBC 中的主要区别**

| **方面**       | **Java SPI**                           | **Spring SPI**                                          |
| -------------- | -------------------------------------- | ------------------------------------------------------- |
| **定义**       | JDK 提供的标准服务发现机制             | Spring Boot 的自动配置机制，基于 `spring.factories`     |
| **适用场景**   | 加载 JDBC 驱动（如 `java.sql.Driver`） | 配置 `DataSource`、JDBC 模板、JPA 等                    |
| **配置文件**   | `META-INF/services/java.sql.Driver`    | `META-INF/spring.factories` 和 `application.properties` |
| **配置需求**   | 无需开发者手动配置（驱动提供者已配置） | 需要在 `application.properties` 中配置连接信息          |
| **灵活性**     | 简单，功能有限，仅支持驱动加载         | 高度灵活，支持复杂依赖注入和自动配置                    |
| **依赖性**     | 无需额外框架，纯 JDK 实现              | 依赖 Spring Boot 框架                                   |
| **使用复杂度** | 低，直接使用 `DriverManager`           | 较高，需熟悉 Spring Boot 配置和依赖注入                 |

---



**使用了 SPI 是不是就不用自己写配置信息？**

- **Java SPI**：
  - **答案：是**。在 JDBC 4.0 及以上版本中，Java SPI 自动加载驱动，开发者无需手动编写配置信息（如 `META-INF/services` 文件），因为这些文件由驱动提供者（如 MySQL、PostgreSQL）在 JAR 包中提供。
  - **注意**：如果驱动不支持 SPI（例如旧版本驱动），仍需手动调用 `Class.forName()`。

- **Spring SPI**：
  - **答案：否**。Spring Boot 的自动配置虽然简化了 `DataSource` 等组件的配置，但开发者通常需要在 `application.properties` 或 `application.yml` 中提供数据库连接信息（如 URL、用户名、密码等）。只有在特定场景（如使用嵌入式数据库 H2）下，Spring Boot 可能完全自动配置，无需手动干预。

---

Spring SPI（即 Spring Boot 的自动配置机制）并不是简单地替代 Java SPI，而是通过 Spring 框架的 **依赖注入（DI）** 和 **自动配置** 功能，极大地简化了复杂应用的配置工作。

Spring Boot 的自动配置机制虽然利用了 Java SPI 来发现数据库驱动，但它在配置 DataSource 时需要明确知道使用哪个驱动类，原因如下：

**确保正确的驱动类加载**

- **Java SPI 的局限性**：Java SPI 通过 ServiceLoader 加载所有类路径中声明的 java.sql.Driver 实现，但如果类路径中存在多个数据库驱动（例如 MySQL 和 PostgreSQL 的 JAR 包同时存在），SPI 无法确定应该优先使用哪个驱动。Spring Boot 需要明确的驱动类名来避免歧义，确保 DataSource 使用正确的驱动。
- **显式配置的可靠性**：通过 spring.datasource.driver-class-name，Spring Boot 明确知道要加载的驱动类，避免了依赖 SPI 加载顺序的不可预测性。



---

**Spring Boot Starter 本身就是利用 Spring SPI（自动配置机制）实现的。开发一个插件时，你通常会创建一个类似于 Starter 的模块，包含自动配置逻辑和必要的依赖，供其他应用引入。**



> <span style="font-size:1.3em;">**<span style="color:#00FF80;">为了让插件支持用户配置，创建一个属性类，使用 @ConfigurationProperties 注解</span>**</span>

**支持多个实现类**：插件提供一个服务接口（如 GreetingService），并支持多个实现类（例如 SimpleGreetingService、AdvancedGreetingService）。

**用户按需选择**：通过配置属性（application.properties 或 application.yml）或**自定义 Bean 让用户选择具体实现 return。**



> 如果这些实现类都需要上下文 或者其他需要用户配置的字段怎么办 是要再创建一个类还是再接口中定义呢





---



## 自定义 starter

**Spring Boot Starter** 本质是一个 Maven 模块，包含：

1. 自动配置类（@Configuration + @ConditionalOnXxx）

2. 配置属性类（用来绑定 application.yml 的属性）

3. 需要的依赖（第三方 SDK、自定义组件、依赖集合、工具包等）

4. resources 中的自动注册文件：
   `META-INF/spring.factories` 或 

   `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（Spring Boot 2.x vs 3.x）

   
   
   在 **Spring Boot 2.x** 里，自动配置类（`xxxAutoConfiguration`）是这样声明的：
   
   ```
   org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
   com.example.autoconfig.FooAutoConfiguration,\
   com.example.autoconfig.BarAutoConfiguration
   ```
   
   - 这个 key 是固定的：`org.springframework.boot.autoconfigure.EnableAutoConfiguration`。
   - 意思是：Spring Boot 启动时扫描所有 jar 包，找到这些类，然后由 `@EnableAutoConfiguration` 注解触发加载。
   - 所以 **它是专门用来列出自动配置类的**。
   
   ~~~css
   spring 2：一键多值对写法 + \ 换行写法    
   spring 3：类路径就可以了
   
   ~~~
   
   ~~~
   org.springframework.context.ApplicationContextInitializer=\
   org.springframework.boot.autoconfigure.SharedMetadataReaderFactoryContextInitializer,\
   org.springframework.boot.autoconfigure.logging.ConditionEvaluationReportLoggingListener
   ~~~
   
   

~~~markdown
创建 Maven 模块
添加 pom.xml 配置 !!!  
编写配置属性类 Properties
编写自动**配置类**
编写自定义工具类（可选）
注册自动配置（Spring Boot 3+）
Spring Boot 3.x 使用 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
~~~



**使用 stater**

~~~markdown
引入依赖（本地项目引入或发布到私服/远程）
配置 application.yml
注入使用
~~~



注意配置属性类和 配置文件

~~~java
@ConfigurationProperties(prefix = "senjay.log")
public class MyLogProperties {
    private Boolean enabled = true;
    private String prefix = "[Senjay-Log]";
}

senjay:
  log:
    enabled: true
    prefix: "[自定义日志]"

~~~

 **可选功能增强**

| 功能           | 示例                                       |
| -------------- | ------------------------------------------ |
| 多环境配置     | `@ConditionalOnClass` 判断第三方类是否存在 |
| 支持 SPI 扩展  | 用 Java SPI 扩展机制                       |
| 多模块 Starter | 拆分成 `xxx-core`、`xxx-autoconfig`        |
| 发布到私服     | 使用 `nexus` 或 `github packages`          |

**条件注解**



| 注解                         | 条件                            | 用法示例                                                     | 说明                                    |
| ---------------------------- | ------------------------------- | ------------------------------------------------------------ | --------------------------------------- |
| `@ConditionalOnClass`        | 某个类在 classpath 中存在       | `@ConditionalOnClass(RedisTemplate.class)`                   | 判断 Redis 是否已引入                   |
| `@ConditionalOnMissingClass` | 某个类在 classpath 中 **不存在** | `@ConditionalOnMissingClass("com.xx.RedisClient")`           | 避免与其他 starter 冲突                 |
| `@ConditionalOnBean`         | 容器中存在某个 Bean             | `@ConditionalOnBean(RedisTemplate.class)`                    | 依赖其他组件                            |
| `@ConditionalOnMissingBean`  | 容器中不存在某个 Bean           | `@ConditionalOnMissingBean(UserService.class)`               | 防止重复注入（推荐用于 starter）        |
| `@ConditionalOnProperty`     | 配置项满足条件                  | `@ConditionalOnProperty(name="arc.sign.enable", havingValue="true")` | 动态控制开关，配合 application.yml 使用 |

~~~java
@Bean
@ConditionalOnProperty(prefix = "ip", name = "mode", havingValue = "online")
@ConditionalOnProperty(prefix = "ip", name = "region", havingValue = "cn")
public IpHelperService ipHelperService(...) {
    ...
}

~~~

~~~java
@Component
@ConditionalOnMissingBean(EmbeddingModel.class)  // 当没有其他 EmbeddingModel Bean 时使用  不一定在配置类里加！
public class DefaultEmbeddingModel implements EmbeddingModel {
    @Override
    public void doEmbedding(String text) {
        System.out.println("使用默认 EmbeddingModel，文本: " + text);
    }
}
~~~

~~~java
@Configuration
@EnableConfigurationProperties(EmbeddingModelProperties.class)
public class EmbeddingModelAutoConfiguration {

    @Bean
    @ConditionalOnProperty(prefix = "embedding-model", name = "base-url")  // 只要配置了 base-url 就生效
    public EmbeddingModel embeddingModel(EmbeddingModelProperties properties) {
        return new ConfiguredEmbeddingModel(properties);
    }
}

~~~



---



<span style="color:#FF0000;">**无状态工具类的定义**</span>

- **不包含任何 ==成员变量==（或者只有 `static final` 常量）**

成员变量 **（Member Variable），也称为实例变量或属性，是指定义在类内部、方法外部的变量，用来描述类的状态或对象的属性。**

- **所有方法通常是 `static` 静态方法**
- 只依赖输入参数进行计算，不依赖或改变任何内部状态
- 调用时不需要实例化对象，直接用类名调用即可

<span style="color:#FF0000; font-size:1.3em;">**这种无需让 bean 容器管理 ** 如 RediUtils ！！！</span>

---



| 概念       | 作用                                                         |
| ---------- | ------------------------------------------------------------ |
| `groupId`  | Maven 构建用的逻辑命名空间，发布依赖时区分项目身份（不影响 Spring 扫描） |
| Java 包名  | 编译后的类的组织结构，**Spring Boot 启动时的扫描路径就基于这个** |
| 启动类位置 | 决定了 Spring Boot 默认的 `@ComponentScan` 范围              |

如果你主项目和 starter 都是 `com.senjay` 包路径

并且你在主项目启动类上用了 `@SpringBootApplication`

那么 Spring 会从 `com.senjay` 包开始扫描所有子包的 `@Component`, `@Service`, `@Repository`, `@Configuration` 等类

结果是：**主项目也会扫描到 starter 中的注解类，并注册进 Spring 容器**



修改了主项目启动类的包名，不影响 `groupId`，也不会影响 Maven 构建；
 但会直接影响 Spring Boot 的组件扫描路径，进而影响是否能扫描到 starter 中的 Bean。



---



**🔸 主项目（业务项目）**

| 类型       | 示例                                | 说明                          |
| ---------- | ----------------------------------- | ----------------------------- |
| groupId    | `com.senjay`                        | 公司或组织维度，建议稳定      |
| artifactId | `arcwater-server` or `arcwater-app` | 项目名 + 功能名（短横线分隔） |

**🔸 Starter 模块命名（规范严格推荐）**

| 类型                                                         | 示例                             | 说明                                           |
| ------------------------------------------------------------ | -------------------------------- | ---------------------------------------------- |
| groupId                                                      | `com.senjay`                     | 与主项目一致，方便管理                         |
| artifactId                                                   | `arc-common-spring-boot-starter` | 必须以 `-spring-boot-starter` 结尾（官方推荐） |
| <span style="color:#FF0000; font-size:1.2em; font-weight:bold;">包结构</span> | `com.senjay.arcstarter.*`        | 不要和主项目重合，防止扫描路径冲突             |

**<span style="color:#FF0000; font-size:1.6em;">为什么要避免包冲突？</span>**

- Spring Boot 会自动扫描 `@Component`, `@Configuration`, `@RestController` 等注解类。
- 如果你的 starter 和主项目在同一个包（如都在 `com.senjay.arcwater`）下，可能会：
  - **重复注册 Bean**（尤其是 RestTemplate、ObjectMapper）
  - **导致配置类冲突**（两个 `@Configuration` 被重复执行）
  - **性能下降**（扫描路径增大）

| 注解                                          | 是否自动注册为 Bean | 说明                                                         |
| --------------------------------------------- | ------------------- | ------------------------------------------------------------ |
| `@Component`                                  | ✅ 是                | 所有被扫描到的 `@Component` 类都会注册为 Bean（基础注解）    |
| `@Service` / `@Repository` / `@Controller`    | ✅ 是                | 是 `@Component` 的语义注解，作用一样，只是表示不同层级       |
| `@RestController`                             | ✅ 是                | 等于 `@Controller + @ResponseBody`，专用于 REST 控制器       |
| `@Configuration`                              | ✅ 是                | 表示配置类，会被扫描为 Bean，并能注册 `@Bean` 方法           |
| `@Bean`（方法级）                             | ✅ 是                | 手动注册 Bean，通常写在 `@Configuration` 类中                |
| `@ControllerAdvice` / `@RestControllerAdvice` | ✅ 是                | 会被扫描并注册为全局增强 Bean（异常、参数绑定）              |
| `@Aspect`                                     | ✅ 是                | AOP 切面类，需和 AOP 配置一起使用（比如开启 `@EnableAspectJAutoProxy`） |
| `@Mapper`                                     | ❌ 否                | 不是 Spring 注解，需要配合 `@MapperScan` 才能注册            |
| `@Entity`                                     | ❌ 否                | 只是 ORM 元数据，不是 Spring Bean，不会被容器注册            |
| `@ConfigurationProperties`                    | ❌ 否                | 需要配合 `@EnableConfigurationProperties` 或 `@Component`    |
| `@EnableXxx`                                  | ❌ 否                | 不是 Bean 注解，它是个组合注解，通常通过 `@Import` 注册配置类 |

**`@EnableConfigurationProperties` 是 Spring Boot 中的一个注解，用于启用一个或多个使用 `@ConfigurationProperties` 注解的配置类，让它们能够被 Spring 容器识别并注入。**

![image-20250711131021063](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250711131021063.png)

~~~org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.senjay.config.IpAutoConfiguration
com.senjay.config.RestTemplateAutoConfiguration
~~~

**服务/工具类**

~~~java
package com.senjay.service;


import com.senjay.domain.IpDetail;
import com.senjay.properties.IpProperties;

import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;

public class IpHelperService {
    private final IpProperties ipProperties;
    private final RestTemplate restTemplate;
    public IpHelperService(IpProperties ipProperties, RestTemplate restTemplate) {
        this.ipProperties = ipProperties;
        this.restTemplate = restTemplate;
    }
    public IpDetail getIpDetail(String ip) {
//        读取配置文件 apiKey
        String apiKey = ipProperties.getApiKey();
        String baseUrl = ipProperties.getBaseUrl();
        URI uri = UriComponentsBuilder
                .fromHttpUrl(baseUrl + ip)
                .queryParam("access_key", apiKey)
                .build()
                .encode() // 防止中文被破坏
                .toUri();
        return restTemplate.getForObject(uri, IpDetail.class);
    }
}

~~~

**配置属性类**

~~~java
package com.senjay.properties;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

@Data
@ConfigurationProperties(prefix = "arc.senjay")
public class IpProperties {
    private String baseUrl;
    private String apiKey;

}

~~~

**配置类**

~~~java
@Configuration
@EnableConfigurationProperties(IpProperties.class) // 启用一个配置属性类（将 IpProperties 注入到容器中，并绑定配置文件里的属性 也可以在 配置属性类当中 声明@Component 注解）。
public class IpAutoConfiguration {
//    当被 spring 容器扫描到, 这意味着 Spring 会创建一个 IpHelperService 实例，使用容器中的 IpProperties 和 RestTemplate 自动注入构造参数
    @Bean
    @ConditionalOnBean(RestTemplate.class)
    public IpHelperService ipHelperService(IpProperties ipProperties, RestTemplate restTemplate) {
        return new IpHelperService(ipProperties, restTemplate);
    }
}


@Configuration
public class RestTemplateAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean(RestTemplate.class)
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

~~~

~~~bash
mvn clean install 打包到.m2 仓库中
~~~

| 位置/设置                     | 作用范围                            | 是否影响编译 | 是否影响运行 | 是否影响 Maven        |
| ----------------------------- | ----------------------------------- | ------------ | ------------ | --------------------- |
| `Project Structure > Project` | **整个项目默认 JDK**                | ✅            | ✅            | ❌（不自动影响 Maven） |
| `Project Structure > Modules` | **每个模块的编译用 JDK**            | ✅            | ❌            | ❌                     |
| `Run Configuration > JDK`     | **运行时使用的 JDK**                | ❌            | ✅            | ❌                     |
| `Project Structure > SDKs`    | 添加可选 JDK（可供其他处选择）      | ❌            | ❌            | ❌                     |
| `Build Tools > Maven > JDK`   | Maven 命令使用的 JDK（编译 & 依赖） | ✅            | ✅            | ✅                     |





---



## AOP 以及自定义注解

| 类型      | 含义                                 | 举例                             | 能不能通过反射读取？ |
| --------- | ------------------------------------ | -------------------------------- | -------------------- |
| `SOURCE`  | 只保留在源码中，编译后丢弃           | Lombok 的 `@Getter`、`@Data` 等  | ❌ 不行               |
| `CLASS`   | 编译进 `.class` 文件，但运行时不保留 | 默认值                           | ❌ 不行               |
| `RUNTIME` | 编译进 `.class`，运行时依然可用      | 自定义注解（限流、日志、权限）等 | ✅ 可以反射获取       |

真正让注解起作用的，是运行时代码通过 **“反射”** 去读取这个注解，然后执行某些行为。

### 业务异常

**枚举类也可实现一个接口**

**业务异常** 是指程序在业务处理过程中，因业务规则不满足而产生的异常。

它反映的是 **业务逻辑层面的错误**，比如：用户余额不足、订单状态非法、数据校验失败等。

不是程序代码的 BUG，也不是系统资源的错误（比如空指针、数据库连接失败那种），而是 **业务场景中合理的错误状态**。

~~~java
/**
 * Description: 业务校验异常码
 */
@AllArgsConstructor
@Getter
public enum BusinessErrorEnum implements ErrorEnum {
    //==== ==== ==== ==== ==== ==== ==== ==== ==common== ==== ==== ==== ==== ==== ==== ==== ====
    BUSINESS_ERROR(1001, "{0}"),
    //==== ==== ==== ==== ==== ==== ==== ==== ==user== ==== ==== ==== ==== ==== ==== ==== ====
    //==== ==== ==== ==== ==== ==== ==== ==== ==chat== ==== ==== ==== ==== ==== ==== ==== ====
    SYSTEM_ERROR(1001, " 系统出小差了，请稍后再试哦~~"),
    ;
    private Integer code;
    private String msg;

    @Override
    public Integer getErrorCode() {
        return code;
    }

    @Override
    public String getErrorMsg() {
        return msg;
    }
}

@Getter
@AllArgsConstructor
public enum CommonErrorEnum implements ErrorEnum{
    SYSTEM_ERROR(-1, " 系统出小差了，请稍后再试哦~~"),
    PARAM_VALID(-2, "参数校验失败{0}"),
    FREQUENCY_LIMIT(-3, " 请求太频繁了，请稍后再试哦~~"),
    LOCK_LIMIT(-4, " 请求太频繁了，请稍后再试哦~~"),
    ;
;
    private final Integer code;
    private final String msg;
    @Override
    public Integer getErrorCode() {
        return this.code;
    }

    @Override
    public String getErrorMsg() {
        return this.msg;
    }
    // 面向接口编程 用于以下的功能
//
//    public UserException(ErrorEnum error) {
//        super(error.getErrorMsg());//    覆盖错误信息
//        this.errorCode = error.getErrorCode();
//        this.errorMsg = error.getErrorMsg();
//    }
}
~~~





| 方面           | `CommonErrorEnum`                                     | `BusinessErrorEnum`                           |
| -------------- | ----------------------------------------------------- | --------------------------------------------- |
| **定位**       | 系统级别的通用错误，跨业务通用的基础错误              | 业务相关的校验错误和业务异常                  |
| **错误范围**   | 系统错误、参数校验失败、限流等基础设施或通用错误      | 业务流程中具体业务错误，如业务规则不满足      |
| **错误码设计** | 负数错误码，如 -1，-2，-3，表示系统级别错误           | 正数错误码，如 1001，表示具体业务错误         |
| **错误信息**   | 常见系统提示，泛化的错误描述                          | 业务错误提示，可包含业务场景相关的信息        |
| **示例错误**   | `SYSTEM_ERROR(-1, "系统出小差了")`，`FREQUENCY_LIMIT` | `BUSINESS_ERROR(1001, "{0}")`，可动态填充参数 |



### 方法引用 与 自定义函数式接口

`joinPoint::proceed` 是 Java 中的方法引用语法，它实际上等价于一个 **Lambda 表达式：`() -> joinPoint.proceed()`**。

方法引用 `joinPoint::proceed` 如何被接收呢？

<span style="color:#FF0000;">**<span style="font-size:1.2em;">“方法引用作为方法参数”的场景，通常是在Java中用函数式接口（functional interface）来接收。</span>**</span>

它要被“接收”或“赋值”，必须 **符合目标函数式接口的签名**

用 `Supplier<T>` 接收 **无参有返回值** 的方法引用

~~~java
import java.util.function.Supplier;

public class Demo {
    public static void main(String [] args) {
        // 调用 test，传入方法引用
        String result = test(Demo:: hello);
        System.out.println(result);
    }

    public static String hello() {
        return "hello world";
    }

    // 使用函数式接口 接收方法引用 Supplier <T> 中的 T 就是 方法引用或 lambda 表达式的返回值类型。
    public static <T> T test(Supplier <T> supplier) {
        return supplier.get(); // 执行传入的函数 ，获得这个返回值！！
    }
}

~~~



**为什么要自定义？**

标准的 `java.util.function.Supplier<T>` **不允许抛异常**，而你业务方法可能会抛异常。

所以自定义这个接口，可以方便地在 Lambda 或方法引用中处理有异常的方法。

~~~java
@FunctionalInterface
// 自定义函数式接口 接收方法签名中的返回值类型
    public interface SupplierThrowWithoutParam <T> {
        T get() throws Throwable; /
    }
~~~



`joinPoint.proceed()` 方法签名是：

```java
Object proceed() throws Throwable;
```





## ==具体应用：==

#### 防刷/限流



##### 注解 与 注解容器

~~~java
@PostMapping("/msg")
@ApiOperation("发送消息")
@FrequencyControl(time = 5, count = 3, target = FrequencyControl.Target.UID)
@FrequencyControl(time = 30, count = 5, target = FrequencyControl.Target.UID)
@FrequencyControl(time = 60, count = 10, target = FrequencyControl.Target.UID)
    public ApiResult <ChatMessageResp> sendMsg(@Valid @RequestBody ChatMessageReq request) {
        Long msgId = chatService.sendMsg(request, RequestHolder.get().getUid());
        //返回完整消息格式，方便前端展示
        return ApiResult.success(chatService.getMsgResp(


/**
 * 频控注解
 * @author 33813
 */
@Repeatable(FrequencyControlContainer.class)//可重复
@Retention(RetentionPolicy.RUNTIME)//运行时生效
@Target(ElementType.METHOD)//作用在方法上
public @interface FrequencyControl {

    String prefixKey() default "";


    Target target() default Target.EL;


    String spEl() default "";


    int time();


    TimeUnit unit() default TimeUnit.SECONDS;



    int count();

    enum Target {
        UID, IP, EL
    }
}



@Retention(RetentionPolicy.RUNTIME)//运行时生效
@Target(ElementType.METHOD)//作用在方法上
public @interface FrequencyControlContainer {
    FrequencyControl [] value();
}

            
            
            
~~~

~~~java
// 接收注解参数类
@Data
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
/** 限流策略定义
 *
 */
public class FrequencyControlDTO {
    /**
     * 代表频控的 Key 如果 target 为 Key 的话 这里要传值用于构建 redis 的 Key 
     target 为 Ip 或者 UID 的话会从上下文取值 Key 字段无需传值
     */
    private String key;
    /**
     * 频控时间范围，默认单位秒
     *
     * @return 时间范围
     */
    private Integer time;

    /**
     * 频控时间单位，默认秒
     *
     * @return 单位
     */
    private TimeUnit unit;

    /**
     * 单位时间内最大访问次数
     *
     * @return 次数
     */
    private Integer count;
}
s
~~~



##### 切面

**！！！切面表达式**

指定注解方式（最常用）

指定包下的所有方法

拦截特定方法名、返回值、参数类型

拦截某个类/接口的所有方法



~~~java
@Slf4j
@Aspect
@Component
public class FrequencyControlAspect {

    @Around("@annotation(com.senjay.archat.common.annotation.FrequencyControl)||@annotation(com.senjay.archat.common.annotation.FrequencyControlContainer)")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {

        //        获取当前执行的方法 Method 对象；
        Method method = ((MethodSignature) joinPoint.getSignature()).getMethod();
//        读取方法上所有的 @FrequencyControl 注解（支持多个）。
        FrequencyControl [] annotationsByType = method.getAnnotationsByType(FrequencyControl.class);

        Map <String, FrequencyControl> keyMap = new HashMap <>();

        for (int i = 0; i < annotationsByType.length; i++) {
            FrequencyControl frequencyControl = annotationsByType [i];
            // 生成前缀（默认使用 方法签名 + 注解顺序 支持多个注解在同一个方法，防止冲突通过 :index:i 作为区分。
            String prefix = StrUtil.isBlank(frequencyControl.prefixKey()) ? SpElUtils.getMethodKey(method) + ":index:" + i : frequencyControl.prefixKey();
// key : 限流的标识符 , 区分不同用户/请求的限流规则，确保限流逻辑能“按人”、“按 IP”、“按表达式(自定义资源限流！)”生效。
            String key = "";
            // 根据限流目标类型构造 key
            switch (frequencyControl.target()) {
                case EL:
                    key = SpElUtils.parseSpEl(method, joinPoint.getArgs(), frequencyControl.spEl());
                    break;
//                case IP:
//                    key = RequestHolder.get().getIp();
//                    break;
                case UID:
                    key = UserHolder.get().getId().toString();
            }
            keyMap.put(prefix + ":" + key, frequencyControl);
        }
        // 将注解的参数转换为编程式调用需要的参数
        List <FrequencyControlDTO> frequencyControlDTOS = keyMap.entrySet().stream().map(entrySet -> buildFrequencyControlDTO(entrySet.getKey(), entrySet.getValue())).collect(Collectors.toList());
        // 调用编程式注解
        return FrequencyControlUtil.executeWithFrequencyControlList(
                // 限流策略控制器
                TOTAL_COUNT_WITH_IN_FIX_TIME_FREQUENCY_CONTROLLER,
                // 所有限流规则的参数
                frequencyControlDTOS,
                // ← 传入原方法引用
                // 目标方法的执行逻辑（通过 Lambda 传递）
                joinPoint:: proceed
        );
    }

    /**
     * 将注解参数转换为编程式调用所需要的参数
     *
     * @param key              频率控制 Key
     * @param frequencyControl 注解
     * @return 编程式调用所需要的参数-FrequencyControlDTO
     */
    private FrequencyControlDTO buildFrequencyControlDTO(String key, FrequencyControl frequencyControl) {
        FrequencyControlDTO frequencyControlDTO = new FrequencyControlDTO();
        frequencyControlDTO.setCount(frequencyControl.count());
        frequencyControlDTO.setTime(frequencyControl.time());
        frequencyControlDTO.setUnit(frequencyControl.unit());
        frequencyControlDTO.setKey(key);
        return frequencyControlDTO;
    }
}

~~~

`joinPoint` 是 `ProceedingJoinPoint` 类型的对象（用于 `@Around` 通知），它表示 **被拦截方法的“连接点”信息**，你可以通过它获取被增强方法的各种元数据，比如参数、方法名、目标对象等等。

| 中文 | 英文                                 | 解释                     |
| ---- | ------------------------------------ | ------------------------ |
| 形参 | **Parameter**（或 Formal Parameter） | 在方法定义中声明的变量名 |
| 实参 | **Argument**（或 Actual Argument）   | 在调用方法时传入的实际值 |



| 方法名           | 作用                                 |
| ---------------- | ------------------------------------ |
| `getArgs()`      | 获取方法参数（数组）                 |
| `getSignature()` | 获取方法签名信息                     |
| `getTarget()`    | 获取目标对象（被代理对象）           |
| `getThis()`      | 获取当前 AOP 代理对象                |
| `proceed()`      | 执行被拦截的方法                     |
| `getKind()`      | 获取连接点类型（如 method-execution) |

---



##### 频控工具类

~~~java
/**
 * 限流工具类 提供编程式的限流调用方法
 */
public class FrequencyControlUtil {

    /**
     * 单限流策略的调用方法-编程式调用
     *
     * @param strategyName     策略名称
     * @param frequencyControl 单个频控对象
     * @param supplier         服务提供着
     * @return 业务方法执行结果
     * @throws Throwable
     */
    public static <T, K extends FrequencyControlDTO> T executeWithFrequencyControl(String strategyName, K frequencyControl, AbstractFrequencyControlService.SupplierThrowWithoutParam <T> supplier) throws Throwable {
        AbstractFrequencyControlService <K> frequencyController = FrequencyControlStrategyFactory.getFrequencyControllerByName(strategyName);
        return frequencyController.executeWithFrequencyControl(frequencyControl, supplier);
    }

    public static <K extends FrequencyControlDTO> void executeWithFrequencyControl(String strategyName, K frequencyControl, AbstractFrequencyControlService.Executor executor) throws Throwable {
        AbstractFrequencyControlService <K> frequencyController = FrequencyControlStrategyFactory.getFrequencyControllerByName(strategyName);
        frequencyController.executeWithFrequencyControl(frequencyControl, () -> {
            executor.execute();
            return null;
        });
    }


    /**
     * 多限流策略的编程式调用方法调用方法 在这里决定调用哪个限流策略
     *
     * @param strategyName         策略名称
     * @param frequencyControlList 频控列表 包含每一个频率控制的定义以及顺序
     * @param supplier             函数式入参-代表每个频控方法执行的不同的业务逻辑
     * @return 业务方法执行的返回值
     * @throws Throwable 被限流或者限流策略定义错误
     */
    public static <T, K extends FrequencyControlDTO> T executeWithFrequencyControlList(
        String strategyName,                                                                                   List <K> frequencyControlList,                                                                            AbstractFrequencyControlService.SupplierThrowWithoutParam <T> supplier) throws Throwable {
        
		boolean existsFrequencyControlHasNullKey = frequencyControlList.stream()
    				.anyMatch(frequencyControl -> ObjectUtils.isEmpty(frequencyControl.getKey()));
     
        AssertUtil.isFalse(existsFrequencyControlHasNullKey, "限流策略的 Key 字段不允许出现空值");
        // 面向接口/抽象类
        AbstractFrequencyControlService <K> frequencyController = 	FrequencyControlStrategyFactory.getFrequencyControllerByName(strategyName);
        
        return frequencyController.executeWithFrequencyControlList(frequencyControlList, supplier);             
    }

    /**
     * 构造器私有
     */
    private FrequencyControlUtil() {

    }

}

~~~



##### 策略注册式工厂 

**（注册式工厂是一种将“产品类”事先注册到“工厂容器”中，允许通过标识（如字符串、枚举）动态获取实例）**

~~~java
// 注册式工厂
public class FrequencyControlStrategyFactory {

    public static final String TOTAL_COUNT_WITH_IN_FIX_TIME_FREQUENCY_CONTROLLER = "TotalCountWithInFixTime";

//    保存所有的策略名称和对应的策略实现类的映射关系。
    static Map <String, AbstractFrequencyControlService<?> > frequencyControlServiceStrategyMap = new ConcurrentHashMap <>(8);

//    <K extends FrequencyControlDTO> 泛型声明 告诉编译器：后面的参数中使用了泛型 K
    public static <K extends FrequencyControlDTO> void registerFrequencyController(String strategyName, AbstractFrequencyControlService <K> abstractFrequencyControlService) {
        frequencyControlServiceStrategyMap.put(strategyName, abstractFrequencyControlService);
    }


    @SuppressWarnings("unchecked")
    public static <K extends FrequencyControlDTO> AbstractFrequencyControlService <K> getFrequencyControllerByName(String strategyName) {
        return (AbstractFrequencyControlService <K>) frequencyControlServiceStrategyMap.get(strategyName);
    }

    private FrequencyControlStrategyFactory() {

    }
}

~~~



<span style="color:#FF0000; font-size:1.6em; font-weight:bold;">抽象类和接口的使用区别 和注意事项：</span>

| 比较维度               | 抽象类                             | 接口                                 |
| ---------------------- | ---------------------------------- | ------------------------------------ |
| 关键字                 | `abstract class`                   | `interface`                          |
| 继承机制               | 只能继承一个抽象类（单继承）       | 可以实现多个接口（多继承）           |
| 是否可以有构造函数     | ✅ 可以                             | ❌ 不可以                             |
| 是否可以有字段（属性） | ✅ 可以有成员变量                   | ✅ 只能有 `public static final` 常量  |
| 是否可以有方法实现     | ✅ 可以有 **实现方法** 和 **抽象方法** | ✅ Java 8 以后支持 `default` 方法实现 |
| 是否可以有静态方法     | ✅ 可以                             | ✅ Java 8 后也可以                    |
| 是否有访问修饰符       | ✅ 支持各种访问修饰符               | ❌ 所有方法默认 `public`              |
| 适合的场景             | **父类中有共用代码（模板）**       | 多种功能复用（能力）                 |

| 类型   | 注意事项                                                     |
| ------ | ------------------------------------------------------------ |
| 抽象类 | 🔸 不能被实例化（不能 new）<br><span style="color:#FF0000;">🔸 **子类必须实现其抽象方法**<br/></span>🔸 可以有构造函数供子类调用 |
| 接口   | 🔸 只能定义常量字段（`public static final`）<br>🔸 所有方法默认 `public`<br>🔸 一个类可以实现多个接口 |

##### 抽象限流策略

~~~java

@Slf4j
public abstract class AbstractFrequencyControlService <K extends FrequencyControlDTO> {

//    使用 @PostConstruct 注解，表示 Spring 容器在创建子类 Bean 后自动执行此方法。
//    作用是：自动将限流策略实现类注册到工厂 FrequencyControlStrategyFactory 中，按策略名绑定起来。
    @PostConstruct
    protected void registerMyselfToFactory() {
        FrequencyControlStrategyFactory.registerFrequencyController(getStrategyName(), this);
    }

    /**
     *
     * @param frequencyControlMap
     * @param supplier
     * @return
     * @param <T>
     * @throws Throwable
     */
    private <T> T executeWithFrequencyControlMap(Map <String, K> frequencyControlMap, SupplierThrowWithoutParam <T> supplier) throws Throwable {
        // 根据策略实现类的不同策略执行
        if (reachRateLimit(frequencyControlMap)) {
            throw new FrequencyControlException(CommonErrorEnum.FREQUENCY_LIMIT);
        }
        try {
//            执行传入的函数，并将它的返回值返回出去
            return supplier.get();
        } finally {
            //不管限流接口是成功还是失败，都增加次数 根据策略实现类的不同策略执行
            addFrequencyControlStatisticsCount(frequencyControlMap);
        }
    }



    @SuppressWarnings("unchecked")
    public <T> T executeWithFrequencyControlList(List <K> frequencyControlList, SupplierThrowWithoutParam <T> supplier) throws Throwable {
//        如果列表中有任意一个 frequencyControl 的 key 为空，则为 true；否则为 false。
        boolean existsFrequencyControlHasNullKey = frequencyControlList.stream().anyMatch(frequencyControl -> ObjectUtils.isEmpty(frequencyControl.getKey()));
        AssertUtil.isFalse(existsFrequencyControlHasNullKey, "限流策略的 Key 字段不允许出现空值");

        Map <String, FrequencyControlDTO> frequencyControlDTOMap = frequencyControlList.stream()
                .collect(Collectors.groupingBy(FrequencyControlDTO:: getKey,
                        Collectors.collectingAndThen(Collectors.toList(),
                                list -> list.get(0))
                ));
        return executeWithFrequencyControlMap((Map <String, K>) frequencyControlDTOMap, supplier);
    }

    public <T> T executeWithFrequencyControl(K frequencyControl, SupplierThrowWithoutParam <T> supplier) throws Throwable {
        return executeWithFrequencyControlList(Collections.singletonList(frequencyControl), supplier);
    }


    @FunctionalInterface
    public interface SupplierThrowWithoutParam <T> {
        T get() throws Throwable;
    }

    @FunctionalInterface
    public interface Executor {


        void execute() throws Throwable;
    }


    protected abstract boolean reachRateLimit(Map <String, K> frequencyControlMap);


    protected abstract void addFrequencyControlStatisticsCount(Map <String, K> frequencyControlMap);


    protected abstract String getStrategyName();

}

~~~

##### 具体限流策略

~~~java

import static com.senjay.archat.common.util.frequencycontrol.FrequencyControlStrategyFactory.TOTAL_COUNT_WITH_IN_FIX_TIME_FREQUENCY_CONTROLLER;


/**
 * 抽象类频控服务 -使用 redis 实现 固定时间内不超过固定次数的限流类
 *

 */
@Slf4j
@Service
public class TotalCountWithInFixTimeFrequencyController extends AbstractFrequencyControlService <FrequencyControlDTO> {


    /**
     * 是否达到限流阈值 子类实现 每个子类都可以自定义自己的限流逻辑判断
     *
     * @param frequencyControlMap 定义的注解频控 Map 中的 Key-对应 redis 的单个频控的 Key Map 中的 Value-对应 redis 的单个频控的 Key 限制的 Value
     * @return true-方法被限流 false-方法没有被限流
     */
    @Override
    protected boolean reachRateLimit(Map <String, FrequencyControlDTO> frequencyControlMap) {
        //批量获取 redis 统计的值
        List <String> frequencyKeys = new ArrayList <>(frequencyControlMap.keySet());
        List <Integer> countList = RedisUtils.mget(frequencyKeys, Integer.class);
        for (int i = 0; i < frequencyKeys.size(); i++) {
            String key = frequencyKeys.get(i);
            Integer count = countList.get(i);
//            获取当前限流规则的设定最大访问次数
            int frequencyControlCount = frequencyControlMap.get(key).getCount();
            if (Objects.nonNull(count) && count >= frequencyControlCount) {
                //频率超过了
                log.warn("frequencyControl limit key:{}, count:{}", key, count);
                return true;
            }
        }
        return false;
    }

    /**
     * 增加限流统计次数 子类实现 每个子类都可以自定义自己的限流统计信息增加的逻辑
     *
     * @param frequencyControlMap 定义的注解频控 Map 中的 Key-对应 redis 的单个频控的 Key Map 中的 Value-对应 redis 的单个频控的 Key 限制的 Value
     */
    @Override
    protected void addFrequencyControlStatisticsCount(Map <String, FrequencyControlDTO> frequencyControlMap) {
        frequencyControlMap.forEach((k, v) -> RedisUtils.inc(k, v.getTime(), v.getUnit()));
    }


    @Override
    protected String getStrategyName() {
        return TOTAL_COUNT_WITH_IN_FIX_TIME_FREQUENCY_CONTROLLER;
    }
}

~~~



##### Redis 工具类 & lua 脚本（具体见 Redis 工具类.md）


​     Redis 的 Lua 脚本调用规范里，所有的 key 都必须通过参数传递给脚本，而且必须分开传。

​      Spring Data Redis 执行 Lua 脚本的接口是：
~~~java	
      <T> T execute(RedisScript <T> script, List <String> keys, Object... args);      
~~~

keys 是一个 List <String>，代表所有传给脚本的 Redis key（对应 Lua 脚本里的 KEYS 数组）。
      其余参数是非 key 的普通参数（对应 Lua 脚本里的 ARGV 数组）。
      也就是说，即使只有一个 key 也必须用 List 的形式传递，不能直接传字符串。

~~~java
public class RedisUtils {

    private static StringRedisTemplate stringRedisTemplate;

    static {
        RedisUtils.stringRedisTemplate = SpringUtil.getBean(StringRedisTemplate.class);
    }

    //    lua 脚本
    private static final String LUA_INCR_EXPIRE = "" "
            local key, ttl = KEYS [1], ARGV [1]

            if redis.call('EXISTS', key)== 0 then
              redis.call('SETEX', key, ttl,1)
              return 1
            else
              return tonumber(redis.call('INCR', key))
            end
            "" ";


  
                
    public static Long inc(String key, int time, TimeUnit unit) {
                
//        创建了一个 RedisScript 对象，用于封装要执行的 Lua 脚本。Long.class 告诉脚本返回结果是 Long 类型。
        RedisScript <Long> redisScript = new DefaultRedisScript <>(LUA_INCR_EXPIRE, Long.class);
                
//        String.valueOf(unit.toSeconds(time))：将过期时间转换为秒字符串，传给 Lua 脚本作为参数 ttl。
        return stringRedisTemplate.execute(redisScript, Collections.singletonList(key), String.valueOf(unit.toSeconds(time)));
    }
    
    
 	 public static <T> List <T> mget(Collection <String> keys, Class <T> tClass) {
        List <String> list = stringRedisTemplate.opsForValue().multiGet(keys);
        if (Objects.isNull(list)) {
            return new ArrayList <>();
        }
        return list.stream().map(o -> toBeanOrNull(o, tClass)).collect(Collectors.toList());
    }   
}
~~~







##### EL 表达式解析工具

~~~java
public class SpElUtils {

//   SpEL 表达式解析器。
    private static final ExpressionParser PARSER = new SpelExpressionParser();
    /**
     * 在 Java 中，通过反射可以获取一个方法的参数类型，但默认情况下无法获取参数名（也就是 String uid 中的 uid）。
     * 这时候就需要 “发现器” 来“发现”这些参数名 ——
     * Spring 提供的 ParameterNameDiscoverer 接口，就是专门干这个事情的。
     * 而 DefaultParameterNameDiscoverer 是它的一个实现类，用来从 方法签名 中智能提取参数名。
     */
    private static final DefaultParameterNameDiscoverer PARAMETER_NAME_DISCOVERER = new DefaultParameterNameDiscoverer();

    /**
     *
     * @param method
     * @param args
     * @param spEl
     * @return
     */
    public static String parseSpEl(Method method, Object [] args, String spEl) {
        // 解析参数名 (注意是名字 不是类型 反射拿不到参数名字的)  Optional 的使用！！！
        String [] params = Optional.ofNullable(PARAMETER_NAME_DISCOVERER.getParameterNames(method)).orElse(new String []{});
        /**
         * 这里创建了一个 SpEL 表达式计算时的上下文对象。
         * EvaluationContext 是 SpEL 提供的接口，里面可以放变量（比如方法参数），表达式在执行时可以从这里取值。
         * StandardEvaluationContext 是其默认实现，支持设置变量、方法解析等。
         * 这一步是为表达式的计算准备环境。
         */
        EvaluationContext context = new StandardEvaluationContext();

        for (int i = 0; i < params.length; i++) {
            // 所有参数都作为原材料扔进去
           // 把方法参数的名字（params [i]）和实际传进来的参数值（args [i]）一一对应，放进 SpEL 的上下文对象（context）中作为变量，让表达式解析器后面可以通过 #参数名 的方式访问到。
            context.setVariable(params [i], args [i]);
        }
             // 用 SpelExpressionParser 把字符串 spEl（比如："#uid + ':' + #msg.type"）解析成一个可执行的表达式对象。表达式还没执行，只是“编译”好准备执行了。
        Expression expression = PARSER.parseExpression(spEl);

        //使用刚刚创建好的表达式对象 expression，并给它一个执行环境 context。它会把 #uid、#msg.type 等变量从 context 中拿出来，用实际值进行替换，并执行表达式。String.class 表示期望返回的结果是一个字符串类型。最终返回值是表达式执行的结果。
        return expression.getValue(context, String.class);
    }
//  为某个方法生成一个全局唯一的标识符
    public static String getMethodKey(Method method) {
        return method.getDeclaringClass() + "#" + method.getName();
    }
}

~~~





---



[见 java 基础 md 注解目录](../Java/Java基础.md)

### ==AOP 的实际应用==

<span style="color:#FF0000; font-size:1.4em;">**✅ 1. `@CheckFriend` —— 检查好友关系**</span>

🎯 目的：

发送私聊消息前，确保两人是好友，否则禁止发送。

👇 使用方式：

```java
@CheckFriend
@PostMapping("/msg/private")
public Result<?> sendPrivateMessage(@RequestBody MsgDTO dto) {
    return chatService.sendPrivateMsg(dto);
}
```

✅ 注解处理逻辑（AOP）：

- 解析参数中的 senderId / receiverId
- 检查是否是好友（查数据库或缓存）
- 不是好友时，直接返回异常

---



<span style="color:#FF0000; font-size:1.4em;">✅ 2. `@LimitFrequency` —— 接口限流（防刷）</span>

🎯 目的：

防止用户恶意刷接口，比如频繁发消息、频繁点赞。

👇 使用方式：

```java
@LimitFrequency(key = "chat:msg", limit = 5, time = 3)
@PostMapping("/msg/send")
public Result<?> sendMessage(@RequestBody MsgDTO dto) {
    return chatService.sendMessage(dto);
}
```

✅ 注解逻辑：

- 用 Redis 对用户请求计数
- 超过限制返回“请求过快”
- 可配置粒度（IP、用户 ID）

---



<span style="color:#FF0000; font-size:1.4em;">✅ 3. `@CurrentUser` —— 自动注入当前登录用户信息</span>

🎯 目的：

避免每个接口手动获取 token、解析用户信息。

👇 使用方式：

```java
@GetMapping("/profile")
public Result<UserVO> getProfile(@CurrentUser UserInfo user) {
    return Result.success(userService.getUserProfile(user.getId()));
}
```

✅ 注解逻辑：

- 从请求中获取 token
- 从 Redis 或 JWT 中解析用户信息
- 注入方法参数中

---



<span style="color:#FF0000; font-size:1.4em;">✅ 4. `@SensitiveFilter` —— 消息内容自动过滤敏感词</span>

🎯 目的：

发送消息时自动过滤或替换敏感词（如“暴力”、“敏感政治词”等）

👇 使用方式：

```java
@SensitiveFilter
@PostMapping("/msg/send")
public Result<?> send(@RequestBody MsgDTO dto) {
    return chatService.sendMessage(dto);
}
```

✅ 注解逻辑：

- 拦截请求体中的字符串
- 使用 Trie 树或敏感词库过滤/替换
- 再传给真正的业务逻辑

---



<span style="color:#FF0000; font-size:1.4em;">✅ 5. `@OperateLog` —— 自动记录用户操作行为（打点日志）</span>

🎯 目的：

记录用户发送消息、添加好友、进入房间等关键行为，方便审计或埋点。

👇 使用方式：

```java
@OperateLog(action = "SEND_MSG", content = "#dto.content")
@PostMapping("/msg/send")
public Result<?> send(@RequestBody MsgDTO dto) {
    return chatService.sendMessage(dto);
}
```

✅ 注解逻辑：

- 使用 SpEL 解析参数值
- 将操作内容写入数据库 / Kafka / ElasticSearch

---





## 过滤器

- **执行时机**：最早执行，在请求进入 `DispatcherServlet` 之前。
- 使用 `@Order` 注解（值越小优先级越高）。

## 拦截器

- **执行时机**：在 `DispatcherServlet` 之后，Controller 方法之前。
- **控制顺序**：在 `WebMvcConfigurer.addInterceptors()` 中按添加顺序执行。



### 过滤器拦截器执行链



~~~java
package com.abin.mallchat.common;

//每个请求的 tid（Trace ID）和用户 uid（User ID）是分开存储但关联使用的，通过组合这两个字段可以精准定位某个用户的请求链路。以下是具体实现逻辑和实际应用方式：
public interface MDCKey {
    String TID = "tid";
    String UID = "uid";
}

~~~

**拦截器配置**

```java
/**
 * Description: 配置所有拦截器
 * Author: <a href="https://github.com/zongzibinbin">abin</a>
 * Date: 2023-04-05
 */
@Configuration
public class InterceptorConfig implements WebMvcConfigurer {

    @Autowired
    private TokenInterceptor tokenInterceptor;
    @Autowired
    private CollectorInterceptor collectorInterceptor;
    @Autowired
    private BlackInterceptor blackInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(tokenInterceptor)
                .addPathPatterns("/capi/**");
        registry.addInterceptor(collectorInterceptor)
                .addPathPatterns("/capi/**");
        registry.addInterceptor(blackInterceptor)
                .addPathPatterns("/capi/**");
    }
}
```



~~~java
@Slf4j
@WebFilter(urlPatterns = "/*")
public class HttpTraceIdFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        String tid = UUID.randomUUID().toString();
        MDC.put(MDCKey.TID, tid);
        chain.doFilter(request, response);
        MDC.remove(MDCKey.TID); // 防止内存泄漏。
    }

}

~~~



~~~java
@Order(-2)
@Slf4j
@Component
public class TokenInterceptor implements HandlerInterceptor {

    public static final String AUTHORIZATION_HEADER = "Authorization";
    public static final String AUTHORIZATION_SCHEMA = "Bearer ";
    public static final String ATTRIBUTE_UID = "uid";

    @Autowired
    private LoginService loginService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //获取用户登录 token
        String token = getToken(request);
        Long validUid = loginService.getValidUid(token);
        if (Objects.nonNull(validUid)) {//有登录态
            request.setAttribute(ATTRIBUTE_UID, validUid);
        } else {
            boolean isPublicURI = isPublicURI(request.getRequestURI());
            if (! isPublicURI) {//又没有登录态，又不是公开路径，直接 401
                HttpErrorEnum.ACCESS_DENIED.sendHttpError(response);
                return false;
            }
        }
        MDC.put(MDCKey.UID, String.valueOf(validUid));
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        MDC.remove(MDCKey.UID);
    }

    /**
     * 判断是不是公共方法，可以未登录访问的
     *
     * @param requestURI
     */
    private boolean isPublicURI(String requestURI) {
        String [] split = requestURI.split("/");
        return split.length > 2 && "public".equals(split [3]);
    }

    private String getToken(HttpServletRequest request) {
        String header = request.getHeader(AUTHORIZATION_HEADER);
        return Optional.ofNullable(header)
                .filter(h -> h.startsWith(AUTHORIZATION_SCHEMA))
                .map(h -> h.substring(AUTHORIZATION_SCHEMA.length()))
                .orElse(null);
    }
}
~~~





~~~java
/**
 * 信息收集的拦截器
 */
@Order(1)
@Slf4j
@Component
public class CollectorInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        RequestInfo info = new RequestInfo();
        info.setUid(Optional.ofNullable(request.getAttribute(TokenInterceptor.ATTRIBUTE_UID)).map(Object:: toString).map(Long:: parseLong).orElse(null));
        info.setIp(ServletUtil.getClientIP(request));
        RequestHolder.set(info);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        RequestHolder.remove();
    }

}

~~~





~~~java
/**
 * 黑名单拦截
 */
@Order(2)
@Slf4j
@Component
public class BlackInterceptor implements HandlerInterceptor {

    @Autowired
    private UserCache userCache;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        Map <Integer, Set<String> > blackMap = userCache.getBlackMap();
        RequestInfo requestInfo = RequestHolder.get();
        if (inBlackList(requestInfo.getUid(), blackMap.get(BlackTypeEnum.UID.getType()))) {
            HttpErrorEnum.ACCESS_DENIED.sendHttpError(response);
            return false;
        }
        if (inBlackList(requestInfo.getIp(), blackMap.get(BlackTypeEnum.IP.getType()))) {
            HttpErrorEnum.ACCESS_DENIED.sendHttpError(response);
            return false;
        }
        return true;
    }

    private boolean inBlackList(Object target, Set <String> blackSet) {
        if (Objects.isNull(target) || CollectionUtil.isEmpty(blackSet)) {
            return false;
        }
        return blackSet.contains(target.toString());
    }

}
~~~



## ThreadLocal

~~~java
public class RequestHolder {

//    RequestInfo
//    @Data
//    public class RequestInfo {
//        private Long uid;
//        private String ip;
//    }



    private static final ThreadLocal <RequestInfo> threadLocal = new ThreadLocal <>();

    public static void set(RequestInfo requestInfo) {
        threadLocal.set(requestInfo);
    }

    public static RequestInfo get() {
        return threadLocal.get();
    }

    public static void remove() {
        threadLocal.remove();
    }
}

~~~



## 全局异常处理器



~~~java
// 不要都把异常处理写在 controller 中这样太臃肿了
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class) // 这里写能够处理的异常类型
    public Result handlerException(Exception e) {
        e.printStackTrace();
        return Result.error(StringUtils.hasLength(e.getMessage()) ? e.getMessage() : "操作失败");// 有些异常并没有封装异常信息
    }
}

~~~



~~~java
/**
 * 全局异常处理器，处理项目中抛出的业务异常
@ControllerAdvice // 标识为全局异常处理器
@ResponseBody     // 直接返回 JSON 数据（可省略，若类上有 @RestControllerAdvice）
 */
@RestControllerAdvice 
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 捕获业务异常
     * @param ex
     * @return
     */
    @ExceptionHandler
    public Result exceptionHandler(BaseException ex){
        log.error("异常信息：{}", ex.getMessage());
        return Result.error(ex.getMessage());
    }

    // 处理 SQL 异常
    public Result excepitionHandler(SQLIntegrityConstraintViolationException ex) {
        String message = ex.getMessage();
        if(message.contains("Duplicate entry")) {
            // 处理唯一性异常
            String [] split = message.split(" ");
            String msg = split [2] + MessageConstant.ALREADY_EXIST;
            return Result.error(msg);
        }else {
            return Result.error(MessageConstant.UNKNOWN_ERROR); // 暂时输出“未知信息”
        }
    }


}

~~~

~~~java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * validation 参数校验异常
     */
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(value = MethodArgumentNotValidException.class)
    public ApiResult methodArgumentNotValidExceptionExceptionHandler(MethodArgumentNotValidException e) {
        StringBuilder errorMsg = new StringBuilder();
        e.getBindingResult().getFieldErrors().forEach(x -> errorMsg.append(x.getField()).append(x.getDefaultMessage()).append(","));
        String message = errorMsg.toString();
        log.info("validation parameters error！The reason is:{}", message);
        return ApiResult.fail(CommonErrorEnum.PARAM_VALID.getErrorCode(), message.substring(0, message.length() - 1));
    }

    /**
     * validation 参数校验异常
     */
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(value = BindException.class)
    public ApiResult bindException(BindException e) {
        StringBuilder errorMsg = new StringBuilder();
        e.getBindingResult().getFieldErrors().forEach(x -> errorMsg.append(x.getField()).append(x.getDefaultMessage()).append(","));
        String message = errorMsg.toString();
        log.info("validation parameters error！The reason is:{}", message);
        return ApiResult.fail(CommonErrorEnum.PARAM_VALID.getErrorCode(), message.substring(0, message.length() - 1));
    }

    /**
     * 处理空指针的异常
     */
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler(value = NullPointerException.class)
    public ApiResult exceptionHandler(NullPointerException e) {
        log.error("null point exception！The reason is: ", e);
        return ApiResult.fail(CommonErrorEnum.SYSTEM_ERROR);
    }

    /**
     * 未知异常
     */
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler(value = Exception.class)
    public ApiResult systemExceptionHandler(Exception e) {
        log.error("system exception！The reason is：{}", e.getMessage(), e);
        return ApiResult.fail(CommonErrorEnum.SYSTEM_ERROR);
    }

    /**
     * 自定义校验异常（如参数校验等）
     */
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(value = BusinessException.class)
    public ApiResult businessExceptionHandler(BusinessException e) {
        log.info("business exception！The reason is：{}", e.getMessage(), e);
        return ApiResult.fail(e.getErrorCode(), e.getMessage());
    }

    /**
     * http 请求方式不支持
     */
    @ResponseStatus(HttpStatus.METHOD_NOT_ALLOWED)
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ApiResult <Void> handleException(HttpRequestMethodNotSupportedException e) {
        log.error(e.getMessage(), e);
        return ApiResult.fail(-1, String.format("不支持'%s'请求", e.getMethod()));
    }

    /**
     * 限流异常
     */
    @ResponseStatus(HttpStatus.TOO_MANY_REQUESTS)
    @ExceptionHandler(value = FrequencyControlException.class)
    public ApiResult frequencyControlExceptionHandler(FrequencyControlException e) {
        log.info("frequencyControl exception！The reason is：{}", e.getMessage(), e);
        return ApiResult.fail(e.getErrorCode(), e.getMessage());
    }
}

~~~





### 自定义异常 与 错误枚举类

~~~java
package com.abin.mallchat.common.common.exception;

import lombok.Data;

@Data
public class BusinessException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    /**
     *  错误码
     */
    protected Integer errorCode;

    /**
     *  错误信息
     */
    protected String errorMsg;

    public BusinessException() {
        super();
    }

    public BusinessException(String errorMsg) {
        super(errorMsg);
        this.errorMsg = errorMsg;
    }

    public BusinessException(Integer errorCode, String errorMsg) {
        super(errorMsg);
        this.errorCode = errorCode;
        this.errorMsg = errorMsg;
    }

    public BusinessException(Integer errorCode, String errorMsg, Throwable cause) {
        super(errorMsg, cause);
        this.errorCode = errorCode;
        this.errorMsg = errorMsg;
    }

    public BusinessException(ErrorEnum error) {
        super(error.getErrorMsg());
        this.errorCode = error.getErrorCode();
        this.errorMsg = error.getErrorMsg();
    }

    @Override
    public String getMessage() {
        return errorMsg;
    }

    @Override
    public synchronized Throwable fillInStackTrace() {
        return this;
    }
}
/**
🌟 默认情况下，Java 每次抛出异常时，都会调用 fillInStackTrace() 方法：
它会收集当前线程的调用栈信息（stack trace）

然后存入 Throwable 中，供打印 e.printStackTrace() 时查看

这是一个性能开销较大的操作

❗ 问题：在高并发下抛很多异常时，这个栈信息收集会很慢！
比如我们定义的 BusinessException 只是用来提示“用户名已存在”、“手机号已注册”这种业务错误，并不需要每次都生成完整堆栈轨迹。

于是：

✅ 通过 重写 fillInStackTrace() 返回 this，可以跳过栈轨迹构建过程，大大提高性能！
**/

~~~

`Throwable cause` 表示：**引发这个异常的原始异常（根本原因）**。

Java 的异常机制允许你链式抛出异常，也就是说：

> A 方法调用 B 方法，B 抛出异常，A 捕获后包装成另一个异常抛出，但仍然保留原始异常。



~~~java
@AllArgsConstructor
@Getter
public enum BusinessErrorEnum implements ErrorEnum {
    //==== ==== ==== ==== ==== ==== ==== ==== ==common== ==== ==== ==== ==== ==== ==== ==== ====
    BUSINESS_ERROR(1001, "{0}"),
    //==== ==== ==== ==== ==== ==== ==== ==== ==user== ==== ==== ==== ==== ==== ==== ==== ====
    //==== ==== ==== ==== ==== ==== ==== ==== ==chat== ==== ==== ==== ==== ==== ==== ==== ====
    SYSTEM_ERROR(1001, " 系统出小差了，请稍后再试哦~~"),
    ;
    private Integer code;
    private String msg;

    @Override
    public Integer getErrorCode() {
        return code;
    }

    @Override
    public String getErrorMsg() {
        return msg;
    }
}

~~~

## ==消息队列使用场景==

### ==用户上线推送消息==

#### 发布事件

~~~java
  @Operation(summary = "测试详细队列 和 listener")
    @GetMapping("mqAndListener")
    public void testMq() {
        User user = userDao.lambdaQuery().eq(User:: getId, 3).one();
        applicationEventPublisher.publishEvent(new UserOnlineEvent(this, user));

    }
~~~

#### 监听到了事件

~~~java
// 事件的定义
@Getter
public class UserOnlineEvent extends ApplicationEvent {
    private final User user;
    public UserOnlineEvent(Object source, User user) {
        super(source);
        this.user = user;
    }
}

// 事件的监听
@Component
@RequiredArgsConstructor
// 用户上线推送 给在线的所有 好友
public class UserOnlineListener {
    private final WebSocketService webSocketService;
    private final PushService pushService;
    private final FriendService friendService;
    private final WSAdapter wsAdapter;

    @Async
    @EventListener(classes = UserOnlineEvent.class)
    public void pushNotice(UserOnlineEvent event) {
        User user = event.getUser();
        pushService.sendPushMsg(wsAdapter.buildOnlineNotifyResp(user));
    }
}
~~~



#### ==消息适配器==

~~~java
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class WSOnlineOfflineNotify {

    //新的上下线用户
    private List <ChatMemberResp> changeList = new ArrayList <>();

    //在线人数
    private Long onlineNum;
}
~~~

~~~java
@Service
@RequiredArgsConstructor
public class ChatMemberHelper {

    public ChatMemberStatisticResp getMemberStatistic() {
        ChatMemberStatisticResp resp = new ChatMemberStatisticResp();
        ConcurrentHashMap <Channel, WSChannelExtraDTO> onlineMap = WebSocketServiceImpl.getOnlineMap();
        resp.setOnlineNum((long) onlineMap.size());
        return resp;
    }

}

~~~



~~~java
@Component
@RequiredArgsConstructor
//它相当于一个“数据适配器”或“消息模板工厂”，用于把 Java 中的业务数据（比如用户对象、状态等）转换成统一格式的 WebSocket 响应对象 WSBaseResp <T>，然后你可以通过 WebSocket 发给前端。
public class WSAdapter {
    private final ChatMemberHelper chatMemberHelper;

    public static WSBaseResp <WSLoginSuccess> buildLoginSuccessResp(User user, String token, boolean hasPower) {
        WSBaseResp <WSLoginSuccess> wsBaseResp = new WSBaseResp <>();
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
    public static WSBaseResp <WSLoginSuccess> buildInvalidateTokenResp() {
        WSBaseResp <WSLoginSuccess> wsBaseResp = new WSBaseResp <>();
        wsBaseResp.setType(WSRespTypeEnum.INVALIDATE_TOKEN.getType());
        return wsBaseResp;
    }


//    用户上下线 ws 消息通知
    public WSBaseResp <WSOnlineOfflineNotify> buildOnlineNotifyResp(User user) {
        WSBaseResp <WSOnlineOfflineNotify> wsBaseResp = new WSBaseResp <>();
        wsBaseResp.setType(WSRespTypeEnum.ONLINE_OFFLINE_NOTIFY.getType());
        WSOnlineOfflineNotify onlineOfflineNotify = new WSOnlineOfflineNotify();
//        Collections.singletonList(...)
//        用这个单个在线用户信息对象，创建一个只包含这一个元素的不可变列表（List）。
//        这个方法会返回一个长度为 1 的列表，里面只有这个用户的在线信息。

        onlineOfflineNotify.setChangeList(Collections.singletonList(buildOnlineInfo(user)));
        assembleNum(onlineOfflineNotify);
//        将 在线人数总数 和 新上线的人（列表） 赋给这个对象作为 ws 消息通知返回
        wsBaseResp.setData(onlineOfflineNotify);
        return wsBaseResp;
    }

//    收集统计人数
    private void assembleNum(WSOnlineOfflineNotify onlineOfflineNotify) {
        ChatMemberStatisticResp memberStatistic = chatMemberHelper.getMemberStatistic();
        onlineOfflineNotify.setOnlineNum(memberStatistic.getOnlineNum());
    }
//    构造上线用户的详情信息
    private static ChatMemberResp buildOnlineInfo(User user) {
        ChatMemberResp info = new ChatMemberResp();
        BeanUtil.copyProperties(user, info);
        info.setUid(user.getId());
        info.setActiveStatus(UserStatusEnum.ONLINE .getCode());
        return info;
    }

}

~~~

#### 推送服务

**根据构造函数传过来的参数决定 消息封装类型**

然后消息队列接收到不同消息类型决定如何推送 **控制参数（类型）**

~~~java

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PushMessageDTO implements Serializable {
    /**
     * 推送的 ws 消息
     */
    private WSBaseResp <?> wsBaseMsg;
    /**
     * 推送的 uid
     */
    private List <Long> uidList;

    /**
     * 推送类型 1 个人 2 全员
     *
     */
    private Integer pushType;

    public PushMessageDTO(Long uid, WSBaseResp <?> wsBaseMsg) {
        this.uidList = Collections.singletonList(uid);
        this.wsBaseMsg = wsBaseMsg;
        this.pushType = WSPushTypeEnum.USER.getType();
    }
// 推送给多个指定用户
    public PushMessageDTO(List <Long> uidList, WSBaseResp <?> wsBaseMsg) {
        this.uidList = uidList;
        this.wsBaseMsg = wsBaseMsg;
        this.pushType = WSPushTypeEnum.USER.getType();
    }
// 推送给所有用户
    public PushMessageDTO(WSBaseResp <?> wsBaseMsg) {
        this.wsBaseMsg = wsBaseMsg;
        this.pushType = WSPushTypeEnum.ALL.getType();
    }
}
~~~



~~~java
// 这个服务调用 消息队列生产者 使用消息队列发送 ws 类型的响应消息
@Service
public class PushService {
    @Autowired
    private MQProducer mqProducer;
//    public void sendPushMsg(WSBaseResp <?> msg, List <Long> uidList) {
//        mqProducer.sendMsg(MQConstant.PUSH_EXCHANGE, new PushMessageDTO(uidList, msg));
//    }
//
//    public void sendPushMsg(WSBaseResp <?> msg, Long uid) {
//        mqProducer.sendMsg(MQConstant.PUSH_EXCHANGE, new PushMessageDTO(uid, msg));
//    }

    public void sendPushMsg(WSBaseResp <?> msg) {
        mqProducer.sendMsg(MQConstant.PUSH_EXCHANGE, MQConstant.ONLINE_BINDING_KEY, new PushMessageDTO(msg));
    }
}

~~~



#### 消息队列命名

~~~java
package com.senjay.archat.common.constant;


public class MQConstant {

    private static final String PREFIX = "archat.";
//    项目前缀 -- 交换机
    public static final String PUSH_EXCHANGE = PREFIX + "push.exchange";

    public static final String PUBLIC_PUSH_QUEUE = "public.push.queue";
    public static final String ONLINE_BINDING_KEY = "online";
}
~~~

**将默认的 jdk 序列化转化为 json 序列化**

~~~java
@Configuration
public class MessageConfiguration {
    @Bean
    public MessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }
}
~~~

**消息转换器**

~~~xml

<dependency>
    <groupId> com.fasterxml.jackson.core </groupId>
    <artifactId> jackson-databind </artifactId>
</dependency>
~~~



#### 生产者

~~~java
@Service
@RequiredArgsConstructor
public class MQProducer { 
// 实际消息队列生产者 只负责传递消息的
    private final RabbitTemplate rabbitTemplate;
// 为了高可扩展性 接收统一的类型 由特定的业务服务调用使用
    public void sendMsg(String exchange, String bindingKey, Object body) {
//        topic 对应交换机
//        msg 对应消息体
        Message <Object> build = MessageBuilder.withPayload(body).build();
        rabbitTemplate.convertAndSend(exchange, bindingKey, build);
    }
}

~~~



#### 消费者

Spring AMQP 的 `@RabbitListener` 支持 **自动将消息反序列化为方法参数类型**，比如这里是 `PushMessageDTO`。

这意味着：
 当 RabbitMQ 队列收到的消息体是 JSON 格式（或者其他可识别格式）时，Spring 会 **自动用消息转换器（MessageConverter）将字节流转换成 `PushMessageDTO` 对象**。

~~~java
// 消息队列消费者
@Component
public class PushConsumer {
    @Autowired
    private WebSocketService webSocketService;
    @RabbitListener(bindings = @QueueBinding(
            value = @Queue(name = MQConstant.PUBLIC_PUSH_QUEUE),
            exchange = @Exchange(name = MQConstant.PUSH_EXCHANGE, type = ExchangeTypes.DIRECT),
            key = {MQConstant.ONLINE_BINDING_KEY}

    ))
    public void listenOnlinePush(PushMessageDTO message) {
s
        System.out.println(message);
    }
}

~~~

### ==群聊发送消息==

~~~java
 AbstractMsgHandler <?> msgHandler = MsgHandlerFactory.getStrategyNoNull(chatMessageReq.getMsgType());
~~~



~~~java
/**
 * Description: 消息处理器的模板抽象父类
 */
public abstract class AbstractMsgHandler <MsgType> {
//    只需要子类 也就是实现类是 bean 就可以了 接口和抽象类不需要被 bean 容器管理 !!!!!
    @Autowired
    private MessageDao messageDao;
// 泛型参数 MsgType 的 Class 类型信息

    private Class <MsgType> bodyClass;

    /**
     * Class <?>：普通类，如 String.class, Integer.class*
     * ParameterizedType：带泛型的类型，如 List <String>
     * TypeVariable：类型变量，如 T
     * WildcardType：通配符类型，如 ? extends Number
     * GenericArrayType：泛型数组，如 T [], List <String> []
      */
//使用 @PostConstruct 注解，表示 Spring 容器在创建子类 Bean 后自动执行此方法。 常用于依赖注入完成后的额外初始化操作
    @PostConstruct
    private void init() {
//        获取当前对象的  父类泛型类型信息
        ParameterizedType genericSuperclass = (ParameterizedType) this.getClass().getGenericSuperclass();
//      getActualTypeArguments() 会返回一个泛型参数数组
//      从父类的泛型信息中反射获取出当前类真正的泛型类型（如 TextMsg），并保存为 Class <MsgType> 类型，以便后续类型转换用。
        this.bodyClass = (Class <MsgType>) genericSuperclass.getActualTypeArguments()[0];
//        在这里注册
        MsgHandlerFactory.register(getMsgTypeEnum().getType(), this);
    }

    /**
     * 消息类型 a
     */
//    抽象方法必须实现
    abstract MessageTypeEnum getMsgTypeEnum();
//    具体方法不强制实现
    protected void checkMsg(MsgType body, Long roomId, Long uid) {

    }
//    这里进行校验和保存
// 思想 先统一再特判处理
    @Transactional
    public Long checkAndSaveMsg(ChatMessageReq request, Long uid) {
        MsgType body = this.toBean(request.getBody());
        //统一校验
        AssertUtil.allCheckValidateThrow(body);
        //子类扩展校验
        checkMsg(body, request.getRoomId(), uid);
        //构建消息实体
        Message insert = MessageAdapter.buildMsgSave(request, uid);
        //统一保存
        messageDao.save(insert);
        //子类扩展保存
        saveMsg(insert, body);
        //返回消息 Id
        return insert.getId();
    }
//传入的 body Object 对象安全地转换为泛型类型 MsgType 的对象
//    body.getClass()：获取传入对象的运行时实际类型；
    private MsgType toBean(Object body) {
        if (bodyClass.isAssignableFrom(body.getClass())) {
            return (MsgType) body;
        }
//        将 Object 类型的 body 对象转换为泛型类型 MsgType 的实例。
        return BeanUtil.toBean(body, bodyClass);
    }

// 子类扩展·保存
    protected abstract void saveMsg(Message message, MsgType body);

//  不同的业务场景下“展示消息”
    /**
     * 展示消息
     */
    public abstract Object showMsg(Message msg);

    /**
     * 被回复时——展示的消息
     */
    public abstract Object showReplyMsg(Message msg);

    /**
     * 会话列表——展示的消息
     */
    public abstract String showContactMsg(Message msg);

}

~~~



~~~java
/**
 * Description: 图片消息

 */
@Component
// 继承了 AbstractMsgHandler <ImgMsgDTO> 
public class ImgMsgHandler extends AbstractMsgHandler <ImgMsgDTO> {
    @Autowired
    private MessageDao messageDao;

    @Override
    MessageTypeEnum getMsgTypeEnum() {
        return MessageTypeEnum.IMG;
    }

    @Override
    public void saveMsg(Message msg, ImgMsgDTO body) {
        MessageExtra extra = Optional.ofNullable(msg.getExtra()).orElse(new MessageExtra());
        Message update = new Message();
        update.setId(msg.getId());
        extra.setImgMsgDTO(body);
        update.setExtra(extra);
        messageDao.updateById(update);
    }

    @Override
    public Object showMsg(Message msg) {
        return msg.getExtra().getImgMsgDTO();
    }

    @Override
    public Object showReplyMsg(Message msg) {
        return "图片";
    }

    @Override
    public String showContactMsg(Message msg) {
        return "[图片]";
    }
}

~~~

所以 上面是

~~~java
  //获取当前对象的  父类泛型类型信息
        ParameterizedType genericSuperclass = (ParameterizedType) this.getClass().getGenericSuperclass();
~~~





![image-20250804144040833](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250804144040833.png)

**判断非 null** 

~~~java
Objects.nonNull(msgHandler)
~~~



好的，我们在你这条时序的基础上，再加上 *“事务回滚”* 分支，让你彻底搞明白 `@TransactionalEventListener` 是怎么处理的 👍

#### ✅ 情况一
保存成功 → 事务提交 → 事件监听器执行
```
sendMsg() 方法开始（事务开始）
 ① checkAndSaveMsg() → 执行 SQL，放入事务缓存
 ② publishEvent() → Spring 把事件加入事件缓冲队列
 ③ return
④ sendMsg() 结束 → Spring 决定 commit 事务
⑤ 事务真正 commit（写入数据库）
⑥ Spring 执行 @TransactionalEventListener 对应的监听方法 messageRoute()
```

✅ **监听器会执行** → MQ 推送消息成功

---

#### ❌ 情况二
中途抛异常 → 事务回滚 → 事件监听器不会执行
```
sendMsg() 方法开始（事务开始）
 ① checkAndSaveMsg() → SQL 执行
 ② publishEvent() → Spring 把事件加入事件缓冲队列
 ③ return 前发生异常（或者 return 后抛出了未捕获异常）
④ Spring 捕获异常 → 决定回滚事务 （rollback）
⑤ 数据库回滚 → 刚刚 insert 的那条记录作废
⑥ Spring 检测事务是 rollback 的 → 丢弃事件，不执行 @TransactionalEventListener 的监听方法
```

❌ **监听器不会执行** → 不会发送 MQ，不会推脏数据

---

####  情况三

**spring 事务的注意事项！**

 **try/catch 捕获异常**，但是方法返回正常 → **事务仍然提交 → 监听器会执行**

```java
try {
  checkAndSaveMsg();
  publishEvent();
} catch (Exception e) {
   // 你 catch 住异常，但没让事务回滚
}
return ...;
```

```
① sendMsg() 开始事务
② 异常被 catch 住，方法继续正常 return
③ Spring 判断事务没有异常 → commit 事务
④ Spring 执行监听器（messageRoute）
```

⚠️ 所以如果用了 `try/catch`，**一定记得配合 `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` 强制回滚**，否则监听器会执行！

---





## ==策略模式多模态消息==





---



## ==线程池使用场景==

![image-20250525203346736](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250525203346736.png)




![image-20250525203428495](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250525203428495.png)



**还有一个 configuration 注解（cause 是 配置类）**

![image-20250525203816235](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250525203816134.png)



![image-20250525204134584](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250525204134584.png)

`@Bean` 注解的作用

```java
@Bean
//@Bean("customUserService") 指定名称
public MyService myService() {
    return new MyServiceImpl();
}
```

- 表示将该方法的返回值注册为 Spring 容器中的一个 **Bean 实例**。
- 方法名默认作为 Bean 的 **名称**（id）。
- 如果你写 `@Bean("xxx")`，就是指定 Bean 的名称为 `xxx`。

<span style="color:#FF0000;">**注意开启了多线程环境 一定要注意线程安全问题！！！！**</span>



**乐观锁 CAS**

![image-20250525204405537](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250525204405537.png)





### 线程池高级使用场景

**扩展接口**：定义了一个获取 **“安全调用线程池”** 的默认方法。

接口默认实现返回 `null`，实现类可以重写它来返回真正的线程池。

使用 `default` 修饰的方法，可以 **提供一个默认实现**，这样实现类就 **可以选择重写，也可以不重写**。

~~~java
public interface SecureInvokeConfigurer {
    @Nullable
    default Executor getSecureInvokeExecutor() {
        return null;
    }
}

~~~

实现 `AsyncConfigurer` 接口

实现后作用：所有使用 `@Async` 的方法，都会使用你配置的 `mallchatExecutor()` 执行，而不是用默认的线程池！

| 方法                                 | 作用                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| `getAsyncExecutor()`                 | 设置 `@Async` 注解使用哪个线程池                             |
| `getAsyncUncaughtExceptionHandler()` | 设置 `@Async` 方法发生异常时统一处理方式（只适用于返回值为 `void` 的方法） |

~~~java
/**
 * Description: 线程池配置

 */
@Configuration
@EnableAsync  // 也可在启动类中声明这个注解！！！
public class ThreadPoolConfig implements AsyncConfigurer, SecureInvokeConfigurer {
    /**
     * 项目共用线程池
     */
    public static final String ARCHAT_EXECUTOR = "archatExecutor";


    /**
     * websocket 通信线程池
     */
    public static final String WS_EXECUTOR = "websocketExecutor";


    public static final String AICHAT_EXECUTOR = "aichatExecutor";

    @Override
    public Executor getAsyncExecutor() {
        return archatExecutor();
    }

    @Override
    public Executor getSecureInvokeExecutor() {
        return archatExecutor();
    }

    @Bean(ARCHAT_EXECUTOR)
    @Primary  // （@Primary 表示：多个线程池时，如果未指定，用这个作为默认的异步线程池（比如 @Async 默认用它））
    public ThreadPoolTaskExecutor archatExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(200);
        executor.setThreadNamePrefix("archat-executor-");
        // 满了调用线程执行，认为重要任务
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setThreadFactory(new MyThreadFactory(executor));
        executor.initialize();
        return executor;
    }

    @Bean(WS_EXECUTOR)
    public ThreadPoolTaskExecutor websocketExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(16);
        executor.setMaxPoolSize(16);
        // 支持同时推送 1000 人
        executor.setQueueCapacity(1000);
        executor.setThreadNamePrefix("websocket-executor-");
        // 满了直接丢弃，默认为不重要消息推送
        // 并发量设置高（最大线程数 16，队列容量 1000） 采用 DiscardPolicy：任务满就丢弃（推送类任务可接受丢失）
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.DiscardPolicy());
        executor.setThreadFactory(new MyThreadFactory(executor));
        executor.initialize();
        return executor;
    }

    @Bean(AICHAT_EXECUTOR)
    public ThreadPoolTaskExecutor chatAiExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(15);
        executor.setThreadNamePrefix("aichat-executor-");
        // 满了直接丢弃，默认为不重要消息推送
        // 适合处理 GPT/AI 类任务设置了小队列（最多 15），代表处理压力可控使用 DiscardPolicy（因为 AI 任务丢了也不影响主业务）

        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.DiscardPolicy());
        executor.setThreadFactory(new MyThreadFactory(executor));
        return executor;
    }
}

~~~



**自定义线程工厂 **

~~~java
@Slf4j
@AllArgsConstructor
public class MyThreadFactory implements ThreadFactory {
    private final ThreadFactory factory;

    @Override
    public Thread newThread(Runnable r) {
        Thread thread = factory.newThread(r);
        // 给每个线程设置一个统一的异常处理器（很关键！）
        thread.setUncaughtExceptionHandler(GlobalUncaughtExceptionHandler.getInstance()); 
        return thread;
    }
}

~~~

###  饿汉式单例（Eager Initialization Singleton）

`private` 构造函数：防止外部创建新实例。

`INSTANCE` 是唯一的全局实例，保证全局只有一个处理器（**单例模式**）。

~~~java
@Slf4j
// 实现 Java 提供的接口，用于处理线程未捕获异常
public class GlobalUncaughtExceptionHandler implements Thread.UncaughtExceptionHandler {

    private static final GlobalUncaughtExceptionHandler INSTANCE = new GlobalUncaughtExceptionHandler();

    private GlobalUncaughtExceptionHandler() {
    }

    @Override
    public void uncaughtException(Thread t, Throwable e) {
        log.error("Exception in thread {} ", t.getName(), e);
    }

    public static GlobalUncaughtExceptionHandler getInstance() {
        return INSTANCE;
    }

}

~~~



### **使用线程池**

 **使用 `@Async`（Spring 提供）**

```java
@Async
public void doSomethingAsync() {
    // 异步逻辑
}
```

- `@EnableAsync`
- 实现 `AsyncConfigurer` 或使用 `@Async("xxxExecutor")` 指定线程池

✅ **优点**：简单清晰、整合 Spring 生命周期
 **⚠️ 注意：只能用在 `public` 方法上**



---



**Spring 中注入线程池 Bean**

~~~java
@Autowired
@Qualifier("aichatExecutor")
private ThreadPoolTaskExecutor executor;

executor.execute(() -> doWork());

~~~



`@Configuration` 中通过 `@Bean` 自定义线程池

配合统一异常处理器、自定义线程工厂

✅ **优点**：高可控、线程隔离、支持可配置
 ✅ **场景**：不同业务逻辑使用不同线程池

---



**使用 `CompletableFuture`**

~~~java
CompletableFuture.supplyAsync(() -> {
    return someRemoteCall();
}, executor).thenApply(result -> {
    return process(result);
});

~~~

可搭配线程池使用，支持链式异步操作。

✅ 优点：结构清晰、支持链式、组合异步任务
 ✅ 场景：高并发、异步数据依赖场景（如多个接口聚合）



### 拒绝策略

| 策略名                | 行为描述                                         | 适用场景                                         |
| --------------------- | ------------------------------------------------ | ------------------------------------------------ |
| `AbortPolicy` (默认)  | 抛出 `RejectedExecutionException` 异常，拒绝任务 | 任务必须执行，不能丢失，需调用方处理异常         |
| `CallerRunsPolicy`    | 由调用线程执行任务，避免任务丢失，降低提交速率   | 希望平滑降压，避免任务丢失，允许调用线程承担压力 |
| `DiscardPolicy`       | 直接丢弃任务，不抛异常                           | 任务可丢弃，且不影响系统整体运行                 |
| `DiscardOldestPolicy` | 丢弃队列里最老的任务，尝试接受新任务             | 任务可丢弃，但新任务优先级更高                   |

---



## HTTP 客户端

| 名称             | 作用                                                         |
| ---------------- | ------------------------------------------------------------ |
| **RestTemplate** | Spring 提供的一个用于简化 HTTP 请求的客户端工具，封装了底层 HTTP 请求逻辑，适合调用 RESTful 接口。 |
| **HttpClient**   | Apache 提供的强大、底层的 HTTP 客户端库，支持更细粒度的 HTTP 请求控制，适合需要自定义请求细节的情况。 |

还有一些更强大的工具！ 用到了在学 先了解有这个东西即可！

## 调用第三方 api -- API 文档！！！

![image-20250505153101275](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250505153101275.png)

序列化：Java 对象 ➜ JSON 字符串（返回给前端）

反序列化：JSON 字符串 ➜ Java 对象（接收前端或第三方传来的数据）

| 场景                | 问题原因                       | 解决方法                              |
| ------------------- | ------------------------------ | ------------------------------------- |
| 反序列化失败        | 字段名不匹配，缺少 setter 方法 | 用 `@JsonProperty` 或加 `@Data`       |
| 序列化时字段为 null | 没有 getter 方法               | 加 `@Data` 或手动写 `getX()` 方法     |
| JSON 中字段为大写   | Java 字段为小写                | 用 `@JsonProperty("大写名")` 显式指定 |

~~~java
package com.senjay.domain.dto;
// 这三个注解确实不会应用到内部类
//@JsonProperty("Date")
// java 命名规范 字段首字母小写 如果第三方 api 返回字段首字母大写

@Data
@AllArgsConstructor
@NoArgsConstructor
public class WeatherDTO {
    @JsonProperty("DailyForecasts")
    private List <DailyForecast> dailyForecasts;
////    内部类
@Data
@AllArgsConstructor
@NoArgsConstructor
    public static class DailyForecast {
    @JsonProperty("Date")
        private String date;
    @JsonProperty("Temperature")
        private TemperatureDTO temperature;
    @JsonProperty("Day")
        private DayAndNight.Day day;
    @JsonProperty("Night")
        private DayAndNight.Night night;

        // getters/setters
    }
}

// ------------
package com.senjay.controller.user;
@RestController
@RequestMapping("/user")
public class WeatherController {
//    远程调用工具 类似 HttpClient 工具
    private final RestTemplate restTemplate;
    private final AccuWeatherApiProperties accuWeatherApiProperties;

    public WeatherController(AccuWeatherApiProperties accuWeatherApiProperties , RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        this.accuWeatherApiProperties = accuWeatherApiProperties;
    }

    @GetMapping("/forecasts")
    public Result <WeatherDTO> forecasts(String days, String locationKey, String language) {
//        使用 http 客户端工具调用第三方 api 后封装到数据里返回前端
        URI uri = UriComponentsBuilder
                .fromHttpUrl(accuWeatherApiProperties.getBaseUrl() + "/forecasts/v1/daily/" + days + "/" + locationKey)
                .queryParam("apikey", accuWeatherApiProperties.getApiKey())
                .queryParam("language", language)
                .build()
                .encode() // 防止中文被破坏
                .toUri();
        WeatherDTO weatherDTO = restTemplate.getForObject(uri, WeatherDTO.class);
        return Result.success(weatherDTO);
    }

}

~~~

### RestTemplate 高级用法

~~~java
 @ApiOperation("获取时事")
    @PostMapping ("/news")
    public Result <NewsVO> getNews(@Valid @RequestBody NewsDTO newsDTO) {


        // 构造请求 URL（带查询参数）
        UriComponentsBuilder builder = UriComponentsBuilder
                .fromHttpUrl(newsApiProperties.getBaseUrl() + "/search-news")
                .queryParamIfPresent("authors", Optional.ofNullable(newsDTO.getAuthor()))
                .queryParamIfPresent("earliest-publish-date", Optional.ofNullable(newsDTO.getEarliestPublishDate()))
                .queryParamIfPresent("latest-publish-date", Optional.ofNullable(newsDTO.getLatestPublishDate()))
                .queryParamIfPresent("language", Optional.ofNullable(newsDTO.getLanguage()))
                .queryParamIfPresent("location-filter", Optional.ofNullable(newsDTO.getLocationFilter()))
                .queryParamIfPresent("news-sources", Optional.ofNullable(newsDTO.getNewsSources()))
                .queryParamIfPresent("number", Optional.ofNullable(newsDTO.getNewsCount()))
                .queryParamIfPresent("offset", Optional.ofNullable(newsDTO.getOffset()))
                .queryParamIfPresent("sort", Optional.ofNullable(newsDTO.getSort()));

        URI uri = builder.build().encode().toUri();

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.set("apikey", newsApiProperties.getApiKey());

        HttpEntity <Void> entity = new HttpEntity <>(headers);

        // 发起 GET 请求
        ResponseEntity <NewsVO> response = restTemplate.exchange(
                uri,
                HttpMethod.GET,
                entity,
                NewsVO.class
        );

        return Result.success(response.getBody()) ;
    }
~~~



## 关于 Servlet & ==IP== 以及各种请求/相应参数

~~~java
/**
 * IP 详情响应实体类
 *  -> 2025-07-10 14:14:08
 */
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class) // 指定该类及内部字段使用下划线转驼峰命名策略，方便 Jackson 自动映射 JSON 字段
@Data // Lombok 注解，自动生成 getter/setter、toString、equals 等
public class IpDetail {
    private String ip;               // IP 地址
    private String hostname;         // 主机名
    private String type;             // IP 类型，如 ipv4、ipv6
    private String continentCode;    // 大洲代码，例如 NA
    private String continentName;    // 大洲名称，例如 North America
    private String countryCode;      // 国家代码，例如 US
    private String countryName;      // 国家名称，例如 United States
    private String regionCode;       // 省/州代码，例如 CA
    private String regionName;       // 省/州名称，例如 California
    private String city;             // 城市，例如 Los Angeles
    private String zip;              // 邮政编码，例如 90013
    private Double latitude;         // 纬度，例如 34.0655
    private Double longitude;        // 经度，例如-118.2405
    private String msa;              // 大都市统计区代码（如果有）
    private String dma;              // 设计市场区域代码（如果有）
    private Object radius;           // 半径，可能为 null，类型不固定
    private Object ipRoutingType;    // IP 路由类型，可能为 null
    private Object connectionType;   // 连接类型，可能为 null
    private Location location;       // 详细地理位置信息，嵌套类
    private TimeZoneInfo timeZone;   // 时区信息，嵌套类
    private Currency currency;       // 货币信息，嵌套类
    private Connection connection;   // 网络连接信息，嵌套类
    private Security security;       // 安全相关信息，嵌套类

    /**
     * 地理位置信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class) // 内部类也要加注解，保证 JSON 映射一致
    @Data
    public static class Location {
        private Long geonameId;               // 地理名称 ID
        private String capital;               // 首都名称
        private List <Language> languages;    // 语言列表，内部另一个嵌套类
        private String countryFlag;           // 国家旗帜图片 URL
        private String countryFlagEmoji;      // 国家旗帜 Emoji
        private String countryFlagEmojiUnicode;// 国家旗帜 Emoji Unicode 编码
        private String callingCode;           // 国际电话区号
        private Boolean isEu;                 // 是否欧盟成员国
    }

    /**
     * 语言信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    @Data
    public static class Language {
        private String code;      // 语言代码，例如 en
        private String name;      // 语言名称，例如 English
        private String nativeLang; // 语言本地名称，字段名 native 是 Java 关键字，改为 nativeLang
    }

    /**
     * 时区信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    @Data
    public static class TimeZoneInfo {
        private String id;               // 时区 ID，例如 America/Los_Angeles
        private String currentTime;      // 当前时间，格式 ISO8601
        private Integer gmtOffset;       // GMT 偏移秒数，例如 -25200
        private String code;             // 时区简称，例如 PDT
        private Boolean isDaylightSaving; // 是否夏令时
    }

    /**
     * 货币信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    @Data
    public static class Currency {
        private String code;          // 货币代码，例如 USD
        private String name;          // 货币名称，例如 US Dollar
        private String plural;        // 货币复数形式，例如 US dollars
        private String symbol;        // 货币符号，例如 $
        private String symbolNative;  // 本地货币符号
    }

    /**
     * 连接信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    @Data
    public static class Connection {
        private Integer asn;              // 自治系统号
        private String isp;               // 互联网服务提供商名称
        private String sld;               // 第二级域名
        private String tld;               // 顶级域名
        private String carrier;           // 运营商
        private Object home;              // 主页，未知类型，通常 null
        private Object organizationType; // 组织类型
        private Object isicCode;          // 行业代码
        private Object naicsCode;         // 北美行业分类系统代码
    }

    /**
     * 安全信息内部类
     */
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    @Data
    public static class Security {
        private Boolean isProxy;             // 是否为代理 IP
        private Object proxyType;            // 代理类型
        private Boolean isCrawler;           // 是否为爬虫
        private Object crawlerName;          // 爬虫名称
        private Object crawlerType;          // 爬虫类型
        private Boolean isTor;               // 是否为 Tor 网络节点
        private String threatLevel;          // 威胁等级，例 low
        private Object threatTypes;          // 威胁类型
        private Object proxyLastDetected;    // 代理最后检测时间
        private Object proxyLevel;           // 代理级别
        private Object vpnService;           // VPN 服务标识
        private Object anonymizerStatus;     // 匿名状态
        private Boolean hostingFacility;     // 是否为托管设施 IP
    }
}

~~~

~~~java
@RestController
@RequestMapping("/ip")
@RequiredArgsConstructor
// 测试获取 IP 地址
public class IpController {
    private final RestTemplate restTemplate;

    @ApiOperation("查询 ip")
    @GetMapping
    public Result <IpDetail> getIp(HttpServletRequest request) {
        String [] headers = {
                "X-Forwarded-For",
                "Proxy-Client-IP",
                "WL-Proxy-Client-IP",
                "HTTP_CLIENT_IP",
                "HTTP_X_FORWARDED_FOR"
        };
        for (String header : headers) {
            String ip = request.getHeader(header);
            System.out.println(ip);
            if (ip != null && ip.length() != 0 && ! "unknown".equalsIgnoreCase(ip)) {
                // 防止多个 IP 串，用第一个
                System.out.println(ip.split(",")[0].trim());
            }
        }
        String apiKey = "a73116188191fd9b42e538ae81454d0f";
        String ip = "112.49.193.35";
        String baseUrl = "http://api.ipstack.com/";
//        调用 api
        URI uri = UriComponentsBuilder
                .fromHttpUrl(baseUrl + ip)
                .queryParam("access_key", apiKey)
                .build()
                .encode() // 防止中文被破坏
                .toUri();

        return Result.success(restTemplate.getForObject(uri, IpDetail.class));
    }

}

~~~

## 编程式事务&声明式事务

声明式事务它有失效场景 具体看 **面试题**

@Transactional 它是通过 AOP 来控制事务的，如果方法当中有异常抛出，那事务就回滚。

声明式事务的粒度问题，因为它要作用在方法上面，但是有的时候我们方法中一般在写操作之前都会有很多读操作以及各种内存的计算之类的，而这些方法其实是没有必要放到事务当中的，粒度太大会拉长整个事务变长就会占用数据库的连接，导致连接无法释放，一旦请求量变大，那有可能会把数据库给拖垮。

声明式事务其实不够明显，很多开发者会无意中在事务方法里做一些 **本不该放进去的操作**，比如耗时操作或远程调用（RPC、HTTP 接口请求等）



**事务一旦开启，数据库连接、锁、资源等都会被占用，直到事务提交或回滚。**



如果你在事务中调用远程服务，这个过程可能 **网络延迟很高、服务不可用、阻塞时间长**，就会导致数据库事务 **一直不提交，甚至连接被耗尽**（出现“连接池耗尽”错误），拉长了本地事务执行时间。

事务只能保证 **本地数据库** 的一致性，无法保证 **远程服务** 的调用成功。









## 日志 logback

### **日志记录的策略**

**能不打就不打、打就打准、错打必追踪、日志不敏感、上线不调试。**

不能够阻断业务代码流程 e.g. 打印变量 NPE 异常就会阻断正常的流程

**使用占位符**

~~~java
log.error("出现严重错误：{}", e);
log.warn("警告：用户配置信息为空");
log.info("服务启动成功，端口号：{}", port);
log.debug("开始执行方法：{}", methodName);
log.trace("变量 x 当前值为：{}", x);

~~~

不要使用 e.printStackTrace()

打印 e.getMessage() 描述信息也不利于排查问题 

~~~java 
//最好是 log.error("出现严重错误：{}", e);
~~~

不要打印不带任何 **业务信息** 的日志 要带上便于排查问题的 **变量**

调用外部系统（如第三方 API）**调用前后打点**

配置加载失败、环境不一致  **提醒但不影响主流程 warn**

**重要方法 入参 和出参 分支时 重要逻辑判断时**



如果 `user` 是一个对象（如 User 类的实例），调用 `log.info("user={}", user)` **底层会自动调用 `user.toString()` 方法**，而 `toString()` 的实现可能非常不合理，甚至包含敏感数据或报错，造成日志污染或性能问题。

日志内应该禁止使用 JSON 工具的序列化对象啊。像 fastjson 等序列化组件其实是通过调用对象的 get 方法将对象进行序列化的，那如果对象的某些 get 方法被覆盖，也就是被重写了，那可能存在抛出异常的风险啊。那如果抛出了异常，咱们正常的业务流程就会被阻断了，就影响咱们正常业务流程的执行。

---



### 使用 AOP 处理日志

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720204338671.png" alt="image-20250720204338671" style="zoom: 80%;" />

**自定义注解**

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720204255477.png" alt="image-20250720204255477" style="zoom: 80%;" />

**切面类**



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720204306447.png" alt="image-20250720204306447" style="zoom:67%;" />

**记录日志方法**



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720204313494.png" alt="image-20250720204313494" style="zoom: 67%;" />



~~~java
// Controller 以外的地方（比如：Service 层、工具类、拦截器、AOP 切面、定时任务等），是没有办法直接通过方法参数拿到 HttpServletRequest 的。
public static HttpServletRequest getHttpServletRequest() {
    return ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
}

~~~



~~~java
import jakarta.servlet.http.HttpServletRequest;
import org.apache.commons.lang3.StringUtils;

public class IpUtils {

    /**
     * 获取客户端真实 IP 地址，支持多代理情况。
     * 
     * @param request HttpServletRequest 对象
     * @return 客户端 IP 地址，若无法获取则返回空字符串
     */
    public static String getIpAddr(HttpServletRequest request) {
        if (request == null) {
            return "";
        }

        String ip = null;

        // 1. 常见的代理请求头，顺序很重要
        String [] headerKeys = {
            "X-Forwarded-For",
            "Proxy-Client-IP",
            "WL-Proxy-Client-IP",
            "HTTP_CLIENT_IP",
            "HTTP_X_FORWARDED_FOR",
            "X-Real-IP"
        };

        for (String header : headerKeys) {
            ip = request.getHeader(header);
            if (isValidIp(ip)) {
                // X-Forwarded-For 可能有多个 IP，用第一个非 unknown 的作为真实 IP
                if ("X-Forwarded-For".equalsIgnoreCase(header)) {
                    ip = extractFirstIp(ip);
                }
                if (isValidIp(ip)) {
                    return ip;
                }
            }
        }

        // 2. 如果代理头没获取到，再获取远程地址
        ip = request.getRemoteAddr();

        // 3. 兼容本地测试环境 IPv6
        if ("0:0:0:0:0:0:0:1".equals(ip) || ":: 1".equals(ip)) {
            ip = "127.0.0.1";
        }

        return ip != null ? ip : "";
    }

    /**
     * 判断 IP 是否有效（非空，非 unknown）
     */
    private static boolean isValidIp(String ip) {
        return StringUtils.isNotBlank(ip) && ! "unknown".equalsIgnoreCase(ip);
    }

    /**
     * 从多重代理头中获取第一个真实 IP（逗号分隔的多个 IP）
     * 
     * @param ipHeader IP 字符串，可能含多个逗号分隔 IP
     * @return 第一个有效 IP
     */
    private static String extractFirstIp(String ipHeader) {
        if (ipHeader == null) {
            return null;
        }
        String [] ips = ipHeader.split(",");
        for (String ip : ips) {
            ip = ip.trim();
            if (isValidIp(ip)) {
                return ip;
            }
        }
        return null;
    }
}

~~~



---



### ==MDC 请求链路追踪==

**MDC（Mapped Diagnostic Context**）是为了在日志中自动记录与“当前线程上下文”相关的关键信息，便于日志排查与请求追踪。

**日志的核心问题是：**

- 日志量大、请求多、并发高，**单条日志很难看出“属于哪个用户”“属于哪次请求”**
- 同一时间多个请求并发，日志会交叉混杂，**无法准确还原一次请求过程**

| 目的             | 描述                                        | 举例                                         |
| ---------------- | ------------------------------------------- | -------------------------------------------- |
| ✅ 日志“打标签”   | 为每条日志打上“上下文身份信息”标签          | traceId、userId、ip                          |
| ✅ 提升日志可读性 | 多线程并发时，能分辨不同请求的日志          | 一个接口被多个用户调用，MDC 能区分日志属于谁 |
| ✅ 不修改业务代码 | 不需要在每个 `log.info()` 中重复拼接参数    | 统一配置日志格式自动注入                     |
| ✅ 方便问题定位   | 可以通过 traceId 快速搜索完整的请求链日志   | 排查 bug 或异常路径时非常关键                |
| ✅ 日志追踪链路   | 和链路追踪（如 Sleuth、SkyWalking）结合使用 | 贯穿多个微服务                               |







---



~~~xml
    <!-- Spring Boot 已包含 logback-classic -->
    <dependency>
        <groupId> org.springframework.boot </groupId>
        <artifactId> spring-boot-starter-web </artifactId>
    </dependency>
    
    <!-- 如需 JSON 日志 -->
    <dependency>
        <groupId> net.logstash.logback </groupId>
        <artifactId> logstash-logback-encoder </artifactId>
        <version> 7.4 </version>
    </dependency>
~~~

✅ 常见日志级别（从高到低，最常用的五级）：

| 等级    | 描述                                             |
| ------- | ------------------------------------------------ |
| `ERROR` | 发生错误，程序出现异常（需要立刻修复）           |
| `WARN`  | 警告，可能导致问题（但程序还能运行）             |
| `INFO`  | 信息，正常业务操作日志（用户登录成功等）         |
| `DEBUG` | 调试用日志，开发人员用于排查问题（变量值、流程） |
| `TRACE` | 更详细的调试日志（几乎每一行都输出，极少用）     |

<span style="color:#FF0000; font-weight:bold;">日志系统只会输出**级别 ≥ 当前配置**的日志。</span>

```yml
#    开启mybatis sql 日志
# 日志相关配置 ！！！ 重要
logging:
  level:
#    默认级别是info 用户提示级别
    com.senjay.mapper: DEBUG
    org.springframework.web: DEBUG
    com.senjay.controller.admin: DEBUG
    com.senjay.controller.user: DEBUG
  file:
    name: logs/app.log
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd} %-5level [%thread] %logger{36} - %msg%n"
#    日志文件的滚动策略（也就是防止日志无限变大）
  logback:
    rollingpolicy:
      max-file-size: 5KB
#      当日志文件大于 1MB 时，会创建新文件
      max-history: 7
#      最多保留最近 7 天的日志文件，旧的会被删除
      file-name-pattern: logs/app.%d{yyyy-MM-dd}.%i.zip
```

~~~java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyService {
    private static final Logger logger = LoggerFactory.getLogger(MyService.class);

    public void process() {
        logger.trace("这是 trace 日志");
        logger.debug("这是 debug 日志");
        logger.info("这是 info 日志");
        logger.warn("这是 warn 日志");
        logger.error("这是 error 日志");
    }
}

~~~



logback 配置 xml 文件

**. 当前项目文件夹**

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!--日志路径 -->
    <!-- 1. 定义日志路径和文件名 --> 
    <property name="LOG_PATH" value="./data/logs/mallchat-chat-server"/>  
    <property name="LOG_FILE" value="mallchat-chat-server"/>
    <!-- 格式化-->
     <!-- 2. 定义控制台日志格式 -->
    < property name = "CONSOLE_LOG_PATTERN"
              value = "|%level|%d{yyyy-MM-dd HH:mm:ss.SSS}|%thread|%X{tid}|uid =%X{uid}|%msg|%X{callChain}%n"/>

    
     <!--引入官方默认配置-->
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    <include resource="org/springframework/boot/logging/logback/console-appender.xml"/>

    
    
    
     <!--控制台日志-->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern >
        </encoder>
    </appender>
        
        
    <!-- 全部日志的配置-->
    <appender name="fileAppender" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file> ${LOG_PATH}/${LOG_FILE}.log </file>
        <append> true </append>
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern >
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 按天生成日志文件 -->
            <fileNamePattern>
                ${LOG_PATH}/archived/${LOG_FILE}.%d{dd-MM-yyyy}.log
            </fileNamePattern>
            <!--保留天数-->
            <maxHistory> 30 </maxHistory>
            <!--单个文件的大小-->
            <totalSizeCap> 5GB </totalSizeCap>
        </rollingPolicy>

    </appender>
    <!-- error日志的配置-->
    <appender name="fileError" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level> ERROR </level>
            <onMatch> ACCEPT </onMatch>
            <onMismatch> DENY </onMismatch>
        </filter>
        <file> ${LOG_PATH}/${LOG_FILE}.error.log </file>
        <append> true </append>
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern >
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>
                ${LOG_PATH}/archived/${LOG_FILE}.%d{dd-MM-yyyy}.error.log
            </fileNamePattern>
            <maxHistory> 30 </maxHistory>
            <totalSizeCap> 2GB </totalSizeCap>
        </rollingPolicy>
    </appender>
            
<!--全局日志级别：INFO（只输出 INFO 及以上级别）。 只有info以上(包括info)的信息 才会被输出到以下引用-->
           
    <root level="info">
        <!--文件输出-->
        <appender-ref ref="fileAppender"/>
        <appender-ref ref="fileError"/>
        <!--控制台输出-->
        <appender-ref ref="STDOUT"/>
    </root>

</configuration>
~~~

```yml
level:
  org.springframework.web: INFO
  com.github.binarywang.demo.wx.mp: DEBUG
  me.chanjar.weixin: DEBUG
  
```



有些框架模块会自带日志 里面可能内含 info error debug 可以指定级别过滤输出的部分

| 包路径                             | 日志级别 | 效果                                                         |
| :--------------------------------- | :------- | :----------------------------------------------------------- |
| `org.springframework.web`          | `INFO`   | Spring MVC 框架的日志（如请求处理、控制器调用）仅输出 `INFO` 及以上级别 |
| `com.github.binarywang.demo.wx.mp` | `DEBUG`  | 指定业务代码包的日志输出 `DEBUG` 级别（显示详细调试信息）      |
| `me.chanjar.weixin`                | `DEBUG`  | 微信官方 SDK 的日志输出 `DEBUG` 级别（显示微信 API 调用细节）      |



## 接口文档 Swagger



http://localhost: 8080/doc.html

访问接口文档

配置信息：

~~~yml
knife4j:
  enable: true
  openapi:
    title: arcWater 接口文档
    description: "arcWater 接口文档"
    email: 3381335358@qq.com
    concat: senjay
    url: https://www.arcwater.top
    version: v1.0.0
    group:
      default:
        group-name: default
        api-rule: package
        api-rule-resources:
          - com.senjay.controller.admin
          - com.senjay.controller.user
          

~~~

~~~xml
knife4j swagge 接口文档的 ui 增强版   
<dependency>
            <groupId> com.github.xiaoymin </groupId>
            <artifactId> knife4j-openapi2-spring-boot-starter </artifactId>
            <version> 4.1.0 </version>
        </dependency>
~~~





![image-20250505155242744](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250505155242744.png)





## 定时任务

~~~java
@EnableAsync   // 开启异步执行支持
@EnableScheduling // 开启定时任务支持
@SpringBootApplication
public class Application { ... }


~~~

~~~java
@Component
public class MyTask {

    // 开启异步任务（加 @Async）
	@Async
	@Scheduled(cron = "0/5 * * * * ?")
    public void runTask() {
        System.out.println("定时任务执行时间：" + System.currentTimeMillis());
    }
}

~~~

**注意事项：**

定时任务方法不能是 `static` 的。

定时任务所在类需要被 Spring 管理（用 `@Component`、`@Service`、`@Configuration` 等标注）。

如果有多个定时任务，它们是 **默认串行** 执行的，如需并行可使用 `@Async`

---



**加了 @Async 之后：**
**Spring 会使用一个异步线程池来执行这个任务。** （可自定义线程池）

**不再阻塞其他任务的执行（并发）。**

方法体在新线程中执行，不占用默认调度线程。

**@Scheduled 参数详解**

| 参数           | 说明                                                       |
| -------------- | ---------------------------------------------------------- |
| `fixedRate`    | 上一次任务开始后 **隔多长时间** 再执行下一次（单位：毫秒） |
| `fixedDelay`   | 上一次任务 **执行完毕后**，隔多久再执行下一次               |
| `initialDelay` | 延迟多久再开始第一次执行                                   |
| `cron`         | 使用 cron 表达式指定时间点执行                             |

---





## ==Event & Listener  事件和监听器==

- **事件（Event）** 是程序运行中发生的一个动作或状态改变，比如这里的 `UserOnlineEvent` 表示用户上线了。
- **监听器（Listener）** 是用来监听某个事件发生后要执行的逻辑。

当该 **事件发布（applicationEventPublisher.publishEvent（new xxxEvent））时**，监听器会执行相应的方法，比如保存在线状态到缓存、数据库，以及推送通知。

e.g.

加上 `@Async` 后，**Spring 会把监听方法放到线程池中异步执行，事件发布者线程不会被阻塞**，提升系统响应速度和吞吐量。

~~~java
@Getter
public class MessageSendEvent extends ApplicationEvent {
    private Long msgId;

    public MessageSendEvent(Object source, Long msgId) {
        super(source);
        this.msgId = msgId;
    }
}



 @TransactionalEventListener(classes = MessageSendEvent.class, fallbackExecution = true)
    public void handlerMsg(@NotNull MessageSendEvent event) {
        Message message = messageDao.getById(event.getMsgId());
        Room room = roomCache.get(message.getRoomId());
        if (isHotRoom(room)) {
            openAIService.chat(message);
        }
    }



 //发布消息发送事件
        applicationEventPublisher.publishEvent(new MessageSendEvent(this, insert.getId()));
~~~



# 单元测试

![image-20250719205752629](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719205752629.png)

ctrl + shift + t 创建 测试类 

![image-20250719210123445](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719210123445.png)

![image-20250719214942600](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719214942600.png)

> 单元测试的目标是：**验证一个方法的逻辑正确性**，而不是测试整个流程。

- **“单元”**：粒度小，只测某个方法。
- **不启动 Spring 容器、数据库、缓存、RPC、HTTP 等外部依赖**。
- **只关注本方法内的逻辑**，依赖内容用 Mock 模拟。

### 常见错误的“单元测试”其实是集成测试：

| 错误做法                     | 问题                                  |
| ---------------------------- | ------------------------------------- |
| 启动整个项目                 | 浪费时间，启动慢                      |
| 调用真实数据库/缓存/HTTP 服务 | 测试依赖外部环境，难以控制，容易 fail |
| 入参写死/改数据表            | 难维护，不可重复执行                  |
| Mock 不彻底                  | 依赖太多，无法聚焦测试目标            |

**重复测试方法** 应尽可能简化为 **参数化测试**

**单元测试覆盖率**（Code Coverage）

| 覆盖类型                  | 含义                               |
| ------------------------- | ---------------------------------- |
| **行覆盖率（Line）**      | 每一行代码是否被执行               |
| **分支覆盖率（Branch）**  | `if/else`、`switch` 等是否都走到了 |
| **条件覆盖（Condition）** | 表达式的 **每个条件** 是否都为真/假  |
| **路径覆盖（Path）**      | 所有可能的执行路径是否走到         |

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720002731357.png" alt="image-20250720002731357" style="zoom:200%;" />

---



**mock （模拟）** 

`MockMvc` 是 **Spring Framework（主要是 Spring MVC）提供的一个测试工具**，用于在 **不启动服务器的情况下** 测试你的 Spring MVC 控制器（Controller）层逻辑。它可以模拟 HTTP 请求，验证返回值、状态码、视图名、响应体、重定向等内容。 这个一般就是 **==接口测试== 了**

**Mockito** 是 Java 领域最流行的 **Mock 框架**，用于创建“虚拟”的对象（模拟对象，Mock 对象），用来替代真实依赖，帮助你专注测试代码的“核心逻辑”。

| 测试类型 |                             说明                             |
| :------: | :----------------------------------------------------------: |
| 单元测试 | 测试单个类或方法的功能，通常只测试业务逻辑，不涉及外部依赖。 |
| 集成测试 | 测试多个模块协作，比如 Service 调用 DAO，或者 Web 层和 Service 层联动 |





---



## 图床(对象存储)

Spring Boot 会根据请求头中 `Content-Type: multipart/form-data` 自动使用内置的 `MultipartResolver`（通常是 `StandardServletMultipartResolver`）来解析请求体。

只要你配置了 `spring-boot-starter-web`（Spring MVC）并在 `application.yml` 中启用了上传功能（默认开启），Spring 就会自动完成这些事情：

1. 检查请求是否是 `multipart/form-data`
2. 解析请求体中的每一个字段（包括文件字段）
3. 把字段名为 `file` 的文件内容封装成 `MultipartFile` 对象
4. 注入到你的控制器方法参数中

---

**`@ConfigurationProperties` 的属性类先被实例化和填充**

- `AliOssProperties` 被扫描到（因为加了 `@Component`），Spring 创建它的 Bean。
- 根据配置文件中 `archat.alioss.*` 的值，Spring 自动将这些属性注入进去。
- 此时它的 `endpoint`、`accessKeyId` 等字段已经有值了。

**然后执行 `OssConfiguration` 配置类**

- Spring 扫描到 `OssConfiguration` 类（有 `@Configuration` 注解）。
- 发现了一个 `@Bean` 方法：`aliOssUtil(...)`
- Spring 检查这个方法的参数：`AliOssProperties`
- Spring 容器中已经有这个 Bean（上一步创建的），于是注入进来。
- 方法被执行，返回 `AliOssUtil` 实例，并注册为 Bean。



| 组件               | 创建时机 | 说明                                                         |
| ------------------ | -------- | ------------------------------------------------------------ |
| `AliOssProperties` | **先**   | 被 `@Component` 注册为 Bean，读取 `application.yml` 中配置值 |
| `AliOssUtil`       | **后**   | 作为 `@Bean` 在配置类中创建，需要依赖前面的配置属性          |

<span style="letter-spacing:3pt; font-size:1.3em; color:#FF0000;">**注意版本 不要一味无脑复制 看看是不是被弃用/升级了**</span>

~~~xml
<!--    阿里云对象存储相关    -->
		<dependency>
			<groupId> com.aliyun.oss </groupId>
			<artifactId> aliyun-sdk-oss </artifactId>
			<version> 3.17.4 </version>
		</dependency>

		<dependency>
			<groupId> javax.xml.bind </groupId>
			<artifactId> jaxb-api </artifactId>
			<version> 2.3.1 </version>
		</dependency>
		<dependency>
			<groupId> javax.activation </groupId>
			<artifactId> activation </artifactId>
			<version> 1.1.1 </version>
		</dependency>
		<!-- no more than 2.3.3-->
		<dependency>
			<groupId> org.glassfish.jaxb </groupId>
			<artifactId> jaxb-runtime </artifactId>
			<version> 2.3.3 </version>
		</dependency>
		<!--      /阿里云对象存储相关-->
~~~

~~~java
  @ApiOperation("用户上传头像")
    @PostMapping("/upload/avatar")
    public Result <String> uploadAvatar(@RequestParam("file") MultipartFile file) throws IOException {
        String originalFilename = file.getOriginalFilename();
        String fileName = UUID.randomUUID().toString() + originalFilename.substring(originalFilename.lastIndexOf("."));
        String url = aliOssUtil.upload(file.getBytes(), fileName);

        return Result.success(url);
    }
~~~



~~~java
@Data
@AllArgsConstructor
@Slf4j
public class AliOssUtil {
//    要注入 AliOssUtil 就需要让它被 spring 管理 可以用一个配置类 直接将参数传进去就不用一直 new new
    private String endpoint;
    private String accessKeyId;
    private String accessKeySecret;
    private String bucketName;

    public String upload(byte [] bytes, String objectName) {

        // 创建 OSSClient 实例。
        OSS ossClient = new OSSClientBuilder().build(endpoint, accessKeyId, accessKeySecret);

        try {
            // 创建 PutObject 请求。
            ossClient.putObject(bucketName, objectName, new ByteArrayInputStream(bytes));
        } catch (OSSException oe) {
            System.out.println("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            System.out.println("Error Message:" + oe.getErrorMessage());
            System.out.println("Error Code:" + oe.getErrorCode());
            System.out.println("Request ID:" + oe.getRequestId());
            System.out.println("Host ID:" + oe.getHostId());
        } catch (ClientException ce) {
            System.out.println("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            System.out.println("Error Message:" + ce.getMessage());
        } finally {
            if (ossClient != null) {
                ossClient.shutdown();
            }
        }

        //文件访问路径规则 https://BucketName.Endpoint/ObjectName
        StringBuilder stringBuilder = new StringBuilder("https://");
        stringBuilder
                .append(bucketName)
                .append(".")
                .append(endpoint)
                .append("/")
                // 这里就是文件修改过后呢 name
                .append(objectName);

        log.info("文件上传到:{}", stringBuilder.toString());

        return stringBuilder.toString();
    }
}


~~~

~~~java
// 读取配置文件中的配置 组装成配置类 Bean
@Component
@ConfigurationProperties(prefix = "archat.alioss")
@Data
public class AliOssProperties {

    private String endpoint;
    private String accessKeyId;
    private String accessKeySecret;
    private String bucketName;

}

~~~





~~~java
// 将 AliOssUtil 注入 Bean 并依赖注入配置自定义内部字段
@Configuration
@Slf4j
public class OssConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public AliOssUtil aliOssUtil(AliOssProperties aliOssProperties){
        return new AliOssUtil(aliOssProperties.getEndpoint(), aliOssProperties.getAccessKeyId(), aliOssProperties.getAccessKeySecret(), aliOssProperties.getBucketName());
    }
}

~~~



~~~yaml
~~~

## 



---





# 项目指标

✅ 一、项目开发阶段的指标

| 指标名称         | 含义与作用                                   |
| ---------------- | -------------------------------------------- |
| **开发成本**     | 人员工资 + 工时投入 + 资源使用（如服务器等） |
| **开发周期**     | 从需求确认到系统上线所需的总时间             |
| **人力资源投入** | 项目中需要多少人参与（开发、测试、管理）     |
| **功能完成度**   | 实现需求的完整程度（比如 MVP vs 完整版）     |

✅ 二、系统运行阶段的指标（运维/产品角度）

1. **性能指标**

| 指标名         | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| **响应时间**   | 接口、系统响应的快慢（ms）                                   |
| **吞吐量**     | 单位时间内系统能处理多少请求                                 |
| **并发能力**   | 能同时支持多少用户请求而不崩溃                               |
| **系统可用性** | 系统在规定时间内可用的比例，目标常是 99.99%（即年宕机时间不超过 52 分钟） |

2. **维护性指标**

| 指标名         | 描述                                         |
| -------------- | -------------------------------------------- |
| **维护成本**   | 修复 bug、更换接口、调整业务逻辑的难度与代价 |
| **可读性**     | 代码和文档的清晰程度，是否容易理解           |
| **可测试性**   | 能否方便地编写和执行自动化测试               |
| **可部署性**   | 能否方便地构建、上线、回滚系统               |
| **技术债务量** | 快速上线时留下的潜在风险和设计问题           |
| **依赖稳定性** | 是否依赖版本易变或不维护的库和组件           |

✅ 三、架构层面的质量指标（系统设计维度）

| 指标             | 含义                                       |
| ---------------- | ------------------------------------------ |
| **扩展性**       | 是否能方便地添加新功能（如新模块、新业务） |
| **可复用性**     | 代码、组件能否在其他项目中直接使用         |
| **可配置性**     | 是否能通过配置文件而不是改代码来调整行为   |
| **松耦合高内聚** | 模块之间独立性强，内部功能紧密协作         |
| **容错性**       | 一部分组件出错，系统是否仍能继续工作       |

✅ 四、项目管理类指标（PM 和团队管理）

| 指标名               | 说明                             |
| -------------------- | -------------------------------- |
| **需求变更率**       | 需求变动频繁会增加开发和测试成本 |
| **Bug 修复时间**     | 平均解决一个 bug 所花时间        |
| **上线次数**         | 反映项目活跃程度和运维流程成熟度 |
| **CI/CD 自动化程度** | 自动构建、测试、部署是否完善     |

🧠 实例应用：维护成本受哪些因素影响？

举个例子，如果你说“这个项目维护成本很高”，可能是因为：

- 代码结构混乱，逻辑难懂（降低可读性）
- 模块之间耦合太高，改一处影响很多（耦合性太强）
- 没有注释、文档或自动化测试（可维护性低）
- 配置散乱且难以修改（可配置性差）
- 依赖旧版本库，不支持升级（依赖风险）



# ==编码技巧==

类似 **策略模式字典**（link to 多模态文件类型处理器） 这个是对于同一类型的

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720205346408.png)

分支逻辑 --》 字典存储

**使用 Stream 流优化**

![image-20250720205515053](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720205515053.png)

![image-20250720205542178](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720205542178.png)

**过滤逻辑（合适的留下来 不合适的提前返回/或者排除 类似清洗数据） -》stream流优化**

**Optional 优化**

优化各种判空处理

![image-20250720205606873](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720205606873.png)

![image-20250720205621901](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720205621901.png)



**状态模式：**

e.g. **电梯行为**

~~~java
public class Main {
    public static void main(String [] args) {
        // 0: 关闭状态 1: 开启状态
        // 抽象类无法实现
        ElevatorContext ect = new ElevatorContext();
        ect.openGate();
        ect.setElevatorState(new OnElevator());
        ect.openGate();

    }
}

~~~



~~~java
public abstract class AbstractElevator {

    public abstract void onElevatorGate();

    public abstract  void offElevatorGate();

}


public class ElevatorContext {
    private AbstractElevator elevator;

    public ElevatorContext() {
        // 初始为停止状态
        this.elevator = new OffElevator();
    }
    public void setElevatorState(AbstractElevator elevator) {
        this.elevator = elevator;
    }

    public void openGate() {
        elevator.onElevatorGate();
    }
    public void closeGate() {
        elevator.offElevatorGate();
    }
}


public class OnElevator extends AbstractElevator {
    @Override
    public void onElevatorGate() {
        System.out.println("电梯门已经处于开启状态");
    }

    @Override
    public void offElevatorGate() {
        System.out.println("正在关闭电梯门");

    }
}
public class OffElevator extends AbstractElevator {
    @Override
    public void onElevatorGate() {
        System.out.println("正在打开电梯门");
    }

    @Override
    public void offElevatorGate() {
        System.out.println("电梯门已经处于关闭状态");
    }
}

~~~



