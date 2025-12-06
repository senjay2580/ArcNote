# 语法速查表（核心用法汇总）

| 语法分类        | 示例                        | 说明                               |
| --------------- | --------------------------- | ---------------------------------- |
| 基础字面量      | `'hello'`、`123`、`true`    | 直接表示值                         |
| 变量访问        | `#user.name`、`#this`       | 访问上下文变量或当前元素           |
| 运算符          | `a + b`、`a ?: b`、`a?.b`   | 算术、逻辑、空安全等               |
| 集合操作        | `list[0]`、`list.?[age>18]` | 列表/Map的访问、过滤、转换         |
| 静态方法        | `T(Math).max(1,2)`          | 访问类的静态方法/常量              |
| Spring 配置访问 | `environment['app.name']`   | 通过Environment获取配置            |
| Spring Bean访问 | `@userService.getName()`    | 访问容器中的Bean及方法             |
| 简化配置占位符  | `${app.name:default}`       | `@Value`中简化配置访问，支持默认值 |




### 一、基础语法（通用表达式）
#### 1. 字面量（直接量）
直接表示基本数据类型、字符串、布尔值等，无需额外修饰。
```css
// 字符串（单引号包裹）
'hello world'

// 数值（整数、小数、科学计数法）
100          // 整数
3.14         // 小数
1e3          // 1000（科学计数法）

// 布尔值
true / false

//  null值
null
```


#### 2. 变量与对象访问
通过 `#变量名` 访问上下文变量，通过 `.` 访问对象属性/方法。
```css
// 访问变量（如方法参数、上下文对象）
#user                // 访问名为user的变量
#user.name           // 访问user对象的name属性
#user.getAge()       // 调用user对象的getAge()方法

// 访问当前对象（迭代/集合场景）
#this                // 指代当前元素（如集合过滤时的每个元素）
```


#### 3. 运算符
支持算术、逻辑、比较、三元等运算符，与 Java 语法一致。
```css
// 算术运算
10 + 20 * 3          // 70
(100 - 50) / 5       // 10
5 % 3                // 2（取余）

// 逻辑运算
true && false        // false
!true                // false
(true || false)      // true

// 比较运算
10 > 5               // true
"a" == 'a'           // true（字符串内容比较）
3 != 3               // false

// 三元运算符（条件表达式）
#user.age > 18 ? '成年' : '未成年'

// 空安全运算符（避免NullPointerException）
#user?.address?.city // 若user或address为null，返回null而非报错
```


#### 4. 集合操作
支持列表、映射（Map）的访问与过滤，语法简洁。
```css
// 列表（List）访问
list[0]              // 取列表第一个元素（索引从0开始）
list[list.size() - 1]// 取列表最后一个元素

// 列表过滤与转换（类似Stream API）
list.?[age > 18]     // 过滤出age>18的元素（返回子列表）
list.![name]         // 提取所有元素的name属性（返回新列表，类似map()）
list.^[age > 18]     // 取第一个age>18的元素（^表示首元素）
list.$[age > 18]     // 取最后一个age>18的元素（$表示尾元素）

// 映射（Map）访问
map['key']           // 取map中key为'key'的value
map.key              // 等价于map['key']（key无特殊字符时可用）
map.?[value > 100]   // 过滤value>100的键值对（返回子Map）
```


#### 5. 类型与静态方法访问
通过 `T(全类名)` 访问类的静态属性/方法。
```css
// 访问静态方法
T(java.lang.System).currentTimeMillis()  // 调用System.currentTimeMillis()
T(java.lang.Math).max(10, 20)            // 调用Math.max()

// 访问静态常量
T(java.lang.Integer).MAX_VALUE           // 取Integer的最大值
T(com.example.Constants).DEFAULT_PAGE_SIZE // 访问自定义类的静态常量
```


### 二、Spring 环境特有语法（结合 Spring 容器）
在 Spring 项目中，SpEL 可直接访问容器内资源，以下是高频用法：

#### 1. 访问 Spring 环境配置（`environment` 对象）
`environment` 是 Spring 内置的 `Environment` 实例，可访问配置文件、环境变量等。
```css
// 访问配置文件中的key（如application.properties中的app.name）
environment['app.name']
environment.getProperty('server.port')  // 等价写法

// 配置项默认值（结合三元运算符）
environment['app.mode'] ?: 'dev'       // 若app.mode未配置，返回'dev'
```


#### 2. 访问 Spring 容器中的 Bean
通过 `@Bean名称` 或 `beanName` 直接访问容器中的 Bean。
```css
// 访问名为userService的Bean
@userService                // 推荐：@明确标识Bean
userService                 // 等价写法（无歧义时）

// 调用Bean的方法
@userService.getCurrentUser()  // 调用userService的getCurrentUser()方法
@orderMapper.count()           // 调用MyBatis mapper的count()方法
```


#### 3. 与 `@Value` 注解结合的简化语法
`@Value` 中可混合使用 `${}` 占位符（简化配置访问）和 SpEL 表达式。
```css
// 简化配置访问（等价于environment['app.name']）
${app.name}

// 配置值+SpEL运算
${app.maxSize} * 2           // 配置值乘以2

// 配置默认值（${}语法的简化默认值）
${app.timeout:3000}          // 若app.timeout未配置，用3000
```


#### 4. 条件判断（结合 `@ConditionalOnExpression`）
在自动配置类中，用于动态判断是否创建 Bean。
```css
// 当配置项feature.enabled为true且环境是prod时生效
${feature.enabled:true} && ${spring.profiles.active} == 'prod'

// 安全处理null值（避免spring.profiles.active为null时报错）
${spring.profiles.active?:''} == 'test'  // 若未配置环境，默认空字符串
```


#### 5. Spring Security 权限表达式
在 `@PreAuthorize` 等注解中，用于动态权限判断。
```css
// 判断当前用户是否有ADMIN角色
hasRole('ADMIN')

// 当前用户ID与参数userId是否一致
#userId == authentication.principal.id

// 复杂条件：角色为ADMIN或用户等级>5
hasRole('ADMIN') or #user.level > 5
```


### 三、特殊语法与高级特性
#### 1.  正则匹配（`matches` 运算符）
用于字符串正则校验，返回布尔值。
```css
'123456' matches '\\d+'        // true（匹配数字）
'abc@example.com' matches '^[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z0-9]+$'  // 邮箱格式校验
```

~~~java
// 场景1：@PreAuthorize 中校验参数格式（仅允许手机号格式的 userId）
@PreAuthorize("#userId matches '^1[3-9]\\d{9}$'")
@GetMapping("/user/{userId}")
public User getUser(@PathVariable String userId) {
    return userService.getById(userId);
}

// 场景2：@Value 中校验配置文件的邮箱格式（不合法则启动失败）
@Value("#{'${admin.email}' matches '^[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z0-9]+$'}")
private boolean isAdminEmailValid;
~~~



#### 2.  模板表达式（字符串拼接）

用 `#{}` 包裹表达式，嵌入到字符串中（类似 `String.format()`）。
```css
// 拼接字符串与变量
"用户#{#user.name}的年龄是#{#user.age}"  // 结果："用户张三的年龄是20"
```

~~~java
@Component
public class AppInfo {
    // 场景1：拼接配置项和 Bean 属性
    @Value("应用名称：${app.name}，当前管理员：#{@userService.getAdmin().name}")
    private String appDesc;

    // 场景2：拼接表达式计算结果
    @Value("服务器地址：http://#{${server.ip}}:#{${server.port}+100}")
    private String serverUrl;
}
~~~



#### 3.  集合投影与选择（复杂过滤）--类似数据库操作

结合多个操作符实现复杂集合处理。
```css
// 从订单列表中，过滤出金额>1000的订单，并提取其ID
orders.?[amount > 1000].![id]  // 结果：[1001, 1002, ...]
```

~~~java
@Component
public class OrderService {
    // 假设容器中有一个 OrderRepository Bean，提供 getALlOrders() 方法（返回 List<Order>）
    @Autowired
    private OrderRepository orderRepository;

    // 场景1：@Value 中提取“金额>1000的订单ID列表”
    @Value("#{@orderRepository.getAllOrders()?.[amount > 1000]!.id}")
    private List<Long> highAmountOrderIds;

    // 场景2：@PreAuthorize 中校验“用户的订单中是否有未支付且金额>500的订单”
    @PreAuthorize("#user.orders?.[status == 'UNPAID' and amount > 500].size() > 0")
    public void remindPayment(User user) {
        // 发送支付提醒
    }
}
~~~

