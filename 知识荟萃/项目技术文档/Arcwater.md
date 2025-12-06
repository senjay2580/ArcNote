redis 特性 **单线程 原子性 适用于 实时性的数据读写 响应快 大规模数据存储 半结构化**
数据类型 **string hash set list sortedset**
key：value 如果value是java类型 **就需要序列化为json字符串存储**
**String 结构是将对象序列化位json字符串后存储当需要需要修改对象某个字段的时候很不方便 而适用hash结构 可以将对象中的每个字段独立的存储 可以针对单个字段做crud**

---



key 格式 ： 项目名：业务名：键名(类型)：id(唯一标识）
e.g.   arcwater:login:userId:12323   :    {"username":"senjay","age":12}

---

---

**redis知识点：**数据持久化 内存淘汰策略 缓存击穿/穿透/雪崩解决方案 ……

项目模块：


**redis：**通过缓存策略解决击穿/穿透/雪崩问题,利用分布式锁实现“一人一单“秒杀功能。
**rabbitMq：**异步处理订单 
**减少重复代码：**AOP切面编程
**用户鉴权模块：**jwt token 使用



**hyperloglog  uv :**bitmap实现签到映射

日志记录模块：

数据报表模块：

ai大数据模块：

………………

---

## AOP

### 用户登录/注册日志记录

### 1️⃣ 自定义注解 `@LoginLog`

```java
// com.example.annotation.LoginLog
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LoginLog {
    String value() default "用户登录";
}
```

------

### 2️⃣ 编写切面类 `LoginLogAspect`

```java
// com.example.aspect.LoginLogAspect
@Aspect
@Component
public class LoginLogAspect {

    @Around("@annotation(loginLog)")
    public Object logLogin(ProceedingJoinPoint joinPoint, LoginLog loginLog) throws Throwable {
        // 获取请求信息
        ServletRequestAttributes attributes =
                (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes.getRequest();

        String ip = request.getRemoteAddr();

        // 获取方法参数
        Object[] args = joinPoint.getArgs();

        // 获取方法名
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();

        // 日志信息
        String methodName = signature.getDeclaringTypeName() + "." + signature.getName();

        System.out.println("===== 登录日志 =====");
        System.out.println("操作：" + loginLog.value());
        System.out.println("IP地址：" + ip);
        System.out.println("方法：" + methodName);
        System.out.println("参数：" + Arrays.toString(args));
        System.out.println("时间：" + LocalDateTime.now());
        System.out.println("===================");

        // 执行目标方法
        return joinPoint.proceed();
    }
}
```

------

### 3️⃣ 登录方法上使用注解

```java
// com.example.controller.LoginController

@RestController
public class LoginController {

    @PostMapping("/login")
    @LoginLog("用户登录操作")
    public String login(@RequestParam String username, @RequestParam String password) {
        // 登录逻辑（伪代码）
        if ("admin".equals(username) && "123456".equals(password)) {
            return "登录成功";
        }
        return "登录失败";
    }
}
```

------

## 🔍 示例输出（控制台日志）

```markdown
复制编辑===== 登录日志 =====
操作：用户登录操作
IP地址：127.0.0.1
方法：com.example.controller.LoginController.login
参数：[admin, 123456]
时间：2025-05-17T17:46:02.475
===================
```

## 用户鉴权

**`preHandle` 被调用（在请求处理前）**

**`afterCompletion` 被调用（响应发送给客户端之前）**

![image-20250517141004721](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517141004721.png)

redis存储token好处：快速读写（基于内存）、适合分布式系统（共享数据）

**JWT** 是一种**无状态（****服务器端**不保存任何用户登录会话数据**，<span style="color:#FF0000;">每次请求只通过 JWT 本身来识别用户身份</span>）的身份验证机制**，通过在客户端和服务端**之间传递自包含的加密 Token 实现用户身份验证**，特别适用于**分布式**和前后端分离系统。



![image-20250517141635485](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517141635485.png)



![image-20250517142546275](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517142546275.png)

![image-20250517142557239](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517142557239.png)

## redis缓存

### <span style="color:#FF0000;">缓存什么 策略是什么</span>

**1. 高频访问数据**

- <span style="color:#FF0000;">**热点数据**</span>：如电商中的商品详情、秒杀信息、社交媒体的热门帖子等，避免频繁查询数据库。
- **用户会话（Session）**：存储用户的登录状态、权限信息，支持分布式系统的会话共享。
- **用户信息**：如昵称、头像、配置偏好等，减少对用户表的重复查询。

**2. 动态计算结果**

- **排行榜/计数**：使用 `Sorted Set` 实现实时排名（如游戏积分、热搜榜）。
- **计数器**：文章阅读量、点赞数、限流请求数等，利用 Redis 的原子性操作（`INCR`）。
- **聚合数据**：如统计报表、<span style="color:#FF0000;">实时在线人数</span>，通过内存计算快速响应。

3**<span style="color:#FF0000;">. 临时或时效性数据</span>**

- <span style="color:#FF0000;">**验证码/短信 Token**：设置短有效期（如 5 分钟），自动过期清理。</span>
- <span style="color:#FF0000;">**缓存预热**：提前加载活动页数据，应对瞬时高并发（如双十一）。</span>
- **分布式锁**：通过 `SETNX` 或 `RedLock` 实现服务间协调，避免资源冲突。

**4. <span style="color:#FF0000;">复杂查询结果</span>**

- **数据库查询缓存**：缓存 SQL 或 NoSQL 的复杂查询结果（如 JOIN 结果），降低重复计算。
- **全文索引缓存**：加速搜索服务的检索效率（如商品关键词匹配）。

**5. 系统级数据**

- **配置参数**：如开关配置、黑白名单，支持动态更新和快速读取。
- **服务降级标志**：在系统压力大时，通过缓存标记切换降级策略。

**6. 消息与队列**

- **异步任务队列**：用 `List` 或 `Stream` 实现轻量级消息队列（如订单排队处理）。
- **实时通知**：用户的消息提醒、订阅推送（结合发布订阅模式 `Pub/Sub`）。

**7. 地理位置与实时数据**

- **地理位置（GEO）**：存储附近的商家、用户位置，支持范围查询（如外卖App）。
- **实时监控数据**：<span style="color:#FF0000;">服务器指标、日志流，用于快速分析和告警</span>



---





### redis数据持久化&内存淘汰策略

Redis 是一个高性能的**内存数据库**，既然运行在内存中，就涉及两个关键问题：

1. ✅ **数据怎么持久化到磁盘？（防止重启丢失）**
2. ✅ **内存满了怎么办？（内存淘汰策略）**

在 `redis.conf`配置

| 持久化方式 | 说明                         | 默认是否开启       | 数据安全性             | 推荐用途                     |
| ---------- | ---------------------------- | ------------------ | ---------------------- | ---------------------------- |
| ✅ RDB      | 定时保存整个内存快照到磁盘   | ✅ 是               | 一般（可能丢失几分钟） | 全量备份、冷启动、迁移       |
| ✅ AOF      | 每次写操作都追加到日志文件中 | ❌ 否               | 高（可配置写入频率）   | 高可靠性场景（如电商支付等） |
| ✅ 混合模式 | Redis 4.0+，结合 RDB 和 AOF  | ❌ 否（需手动配置） | 高且效率更好           | 🚀 推荐！生产级环境优先使用   |

持久化机制详细解释：https://javaguide.cn/database/redis/redis-persistence.html





---

### [Redis 内存淘汰策略了解么？](https://javaguide.cn/database/redis/redis-questions-01.html#redis-内存淘汰策略了解么)

相关问题：MySQL 里有 2000w 数据，Redis 中只存 20w 的数据，如何保证 Redis 中的数据都是热点数据?

---



Redis 的内存淘汰策略只有在运行内存达到了配置的最大内存阈值时才会触发，这个阈值是通过 `redis.conf` 的 `maxmemory` 参数来定义的。64 位操作系统下，`maxmemory` 默认为 0，表示不限制内存大小。32 位操作系统下，默认的最大内存值是 3GB。

你可以使用命令 `config get maxmemory` 来查看 `maxmemory` 的值。

```
#define ACTIVE_EXPIRE_CYCLE_KEYS_PER_LOOP 20 /* Keys for each DB loop. */
```

Redis 提供了 6 种内存淘汰策略：

1. **volatile-lru（least recently used）**：从已设置过期时间的数据集（`server.db[i].expires`）中挑选最近最少使用的数据淘汰。
2. **volatile-ttl**：从已设置过期时间的数据集（`server.db[i].expires`）中挑选将要过期的数据淘汰。
3. **volatile-random**：从已设置过期时间的数据集（`server.db[i].expires`）中任意选择数据淘汰。



1. **allkeys-lru（least recently used）**：从数据集（`server.db[i].dict`）中移除最近最少使用的数据淘汰。
2. **allkeys-random**：从数据集（`server.db[i].dict`）中任意选择数据淘汰。
3. **no-eviction**（默认内存淘汰策略）：禁止驱逐数据，当内存不足以容纳新写入数据时，新写入操作会报错。

4.0 版本后增加以下两种：

1. **volatile-lfu（least frequently used）**：从已设置过期时间的数据集（`server.db[i].expires`）中挑选最不经常使用的数据淘汰。
2. **allkeys-lfu（least frequently used）**：从数据集（`server.db[i].dict`）中移除最不经常使用的数据淘汰。

`allkeys-xxx` 表示从所有的键值中淘汰数据，而 `volatile-xxx` 表示从设置了过期时间的键值中淘汰数据。

`config.c` 中定义了内存淘汰策略的枚举数组：

```
# 默认为 10
hz 10
# 默认开启
dynamic-hz yes
```

你可以使用 `config get maxmemory-policy` 命令来查看当前 Redis 的内存淘汰策略。

```
> config get maxmemory
maxmemory
```

可以通过 `config set maxmemory-policy 内存淘汰策略` 命令修改内存淘汰策略，立即生效，但这种方式重启 Redis 之后就失效了<span style="color:#FF0000;">。修改 `redis.conf` 中的 `maxmemory-policy` 参数不会因为重启而失效</span>，不过，需要重启之后修改才能生效。

```
configEnum maxmemory_policy_enum[] = {
    {"volatile-lru", MAXMEMORY_VOLATILE_LRU},
    {"volatile-lfu", MAXMEMORY_VOLATILE_LFU},
    {"volatile-random",MAXMEMORY_VOLATILE_RANDOM},
    {"volatile-ttl",MAXMEMORY_VOLATILE_TTL},
    {"allkeys-lru",MAXMEMORY_ALLKEYS_LRU},
    {"allkeys-lfu",MAXMEMORY_ALLKEYS_LFU},
    {"allkeys-random",MAXMEMORY_ALLKEYS_RANDOM},
    {"noeviction",MAXMEMORY_NO_EVICTION},
    {NULL, 0}
};
```

---



### **需要序列化的场景**

**一切java对象均可转化成json字符串**

| 场景                                   | 需要序列化的原因                       |
| -------------------------------------- | -------------------------------------- |
| **存储对象到 Redis（但不使用 Hash）**  | 需要把对象转成 JSON 或者二进制格式存储 |
| **消息队列（MQ，如 Kafka、RabbitMQ）** | 需要对象传输时保持完整性               |
| **网络通信（RPC、Socket 传输）**       | Java 对象在网络上传输时需要序列化      |
| **存储对象到磁盘（如写入文件）**       | 需要保存 Java 对象状态并恢复           |

### 缓存更新策略

![image-20250517144606318](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517144606318.png)



![image-20250517152209878](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517152209878.png)



**这种线程安全问题一般都是 A线程查询C数据的时候 B线程修改了C数据     然后 然后A线程拿着不一致的数据进行操作就会有问题**

---



### 缓存穿透 （面试）





![image-20250207130831949](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250207130831949.png)







~~~java
@GetMapping("/{id}")
    public Result queryShopById(@PathVariable("id") Long id) {

        try {
            return Result.ok(shopService.queryById(id)); // 利用了mp
        } catch (Exception e) {
            return Result.fail(e.getMessage());
        }
    }



// ---------------------------------
@Override
    public Shop queryById(Long id) throws Exception {
        String key = "cache:shop:" + id; // 不能直接id去查 要有业务：类型：键
        String shopJson = stringRedisTemplate.opsForValue().get(key);
        Shop shop = null;
        if(StrUtil.isNotBlank(shopJson)) // 等价str != null && str.trim().length() > 0
        {
            // 返回反序列化的shop
             shop = JSONUtil.toBean(shopJson, Shop.class);
            return shop; // 尽量使用return 少用else
        }
        // 现在我要让缓存的空值不能用数据库去查而要用缓存去查
        if(shopJson != null) {
            // 所以最好还是在service层里返回一些最终的相应数据 复杂的逻辑都在service层里好
            throw new Exception("店铺不存在"); // 不然这样抛异常有点不优雅 不过也是用异常的一种处理方式 学习！
        }

         shop = getById(id);
        if(shop == null) {
            stringRedisTemplate.opsForValue().set(key, "", CACHE_NULL_TTL, TimeUnit.MINUTES);// 避免缓存击穿
            throw new Exception("店铺不存在");
        }

         // 序列化存储
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop), CACHE_SHOP_TTL, TimeUnit.MINUTES);
        return shop;
    }
~~~

### 缓存雪崩

![image-20250517155141757](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517155141757.png)

### 缓存击穿

![image-20250207134938011](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250207134938011.png)





![image-20250207135736714](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250207135736714.png)



**逻辑上过期并不是真的过期**



![image-20250207135851965](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250207135851965.png)

**一致性和高性能**

[==TODO==]: 先了解这两个方法， 用到在具体学做法

MuteX :互斥锁

LogicalExpire：逻辑过期

passthrough：穿透





---

#### ==互斥锁解决==





#### ==逻辑过期解决==











---



## redis数据结构实现不同功能

### HyperLogLog 统计 UV



**UV（独立访客）** 是互联网数据分析中的一个重要指标，用于统计**在一定时间内访问某个网站或应用的不重复用户数量**。它的核心特点是：
**“去重计数”**——同一个用户多次访问只算 1 次。





**HyperLogLog（HLL）** 是一种**概率型数据结构**，用于**高效估算大规模数据集的基数（Cardinality，即不重复元素的个数）**。它的特点是：

- **占用极小的内存空间**（通常只需几 KB）。
- **支持合并（Mergeable）**，适合分布式计算。
- **牺牲一定精度**（标准误差约 0.81% ~ 2%），但适用于海量数据场景。

```java
@RestController
@RequestMapping("/client/visit")
@RequiredArgsConstructor
public class UserVisitController {
    private final UserVisitService userVisitService;

    @ApiOperation("增加每日访问量")
    @PostMapping("/add")
    public Result addVisitor() {
        String uid = UserHolder.get().getId().toString();
        userVisitService.addVisitor(uid);
        return Result.success();
    }

    @ApiOperation("查看访问量")
    @PostMapping("/count")
    public Result<String> countVisitor(@Valid @RequestBody DateKeyDTO dateKeyDTO) {
        return Result.success(userVisitService.countVisitor(dateKeyDTO.getDateKey()));
    }

}

@Data
public class DateKeyDTO {
    @Pattern(regexp = "^\\d{8}$", message = "日期格式错误，应为yyyyMMdd格式")
    private String dateKey;
}

@Service
@RequiredArgsConstructor
public class UserVisitServiceImpl implements UserVisitService {
    private final StringRedisTemplate stringRedisTemplate;

    @Override
    public void addVisitor(String uid) {
        String dateKey = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        String key = RedisConstant.UV_USER_KEY + dateKey;
        stringRedisTemplate.opsForHyperLogLog().add(key, uid);

    }

//    yyyyMMdd 形式
    @Override
    public String countVisitor(String dateKey) {
        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");
            formatter.parse(dateKey);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("日期格式非法，应为合法的 yyyyMMdd 格式，例如 20250709 表示 2025年7月9日");
        }
        String key = RedisConstant.UV_USER_KEY + dateKey;
        Long visitorCount = stringRedisTemplate.opsForHyperLogLog().size(key);
        return visitorCount.toString();
    }
}
```

### Bitmap 用户签到

![image-20250517180619952](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517180619952.png)

![image-20250517180825225](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517180825225.png)

![image-20250517181317185](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517181317185.png)

![image-20250517181941387](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517181941387.png)、

从哪开始 ？ 读取几位？

返回的是十进制不是二进制！！！ u10 表示10位无符号数！！！

---



**BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]**

- 对位图 key 中指定偏移量的比特位执行多种操作，如读取、设置、增加值等。 （`BITFIELD` 命令允许在一次调用中执行多种操作，例如可以同时进行读取、设置、增加值等操作。）
- 支持多种数据类型和溢出处理方式。
- 用途：支持更复杂的位操作需求，如处理多位比特位、不同数据类型的位操作等。



![image-20250517182035665](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250517182035665.png)









#### 使用示例（在 Controller 中）

```java
// 签到接口
@RestController
@RequiredArgsConstructor
@RequestMapping("/client/signIn")
public class SignInController {
    private final SignInHelperService signInHelperService;

    @ApiOperation("签到")
    @PostMapping
    public Result signIn() {
        signInHelperService.signIn();
        return Result.success();
    }
    @ApiOperation("查询当月的签到情况")
    @GetMapping("/detail")
    public Result<Long> getSignInDetailOfMonth() {
        return Result.success(signInHelperService.getSignInDetailOfMonth());
    }
}
```

~~~java
// TODO：加经验可以用消息队列
@RequiredArgsConstructor
@Service
public class SignInHelperService {

    private final StringRedisTemplate stringRedisTemplate;


    public Boolean checkSignIn() {
        String key = buildSignInKey();
        int day = LocalDate.now().getDayOfMonth() - 1;
        return stringRedisTemplate.opsForValue().getBit(key, day);
    }

    public void signIn() {
        // bitmap offset 从0开始
        if (checkSignIn()) {
            return ;
        }
        LocalDateTime now = LocalDateTime.now();
        int day = now.getDayOfMonth()-1;
        String key = buildSignInKey();
        if (!Boolean.TRUE.equals(stringRedisTemplate.hasKey(key))) {
            // 如果是第一次签到, 要设置过期时间
            stringRedisTemplate.opsForValue().setBit(key, day, true);
            LocalDateTime nextMonthFirstDayStart =now.plusMonths(1)
                    .withDayOfMonth(2)
                    .withHour(0)
                    .withMinute(0)
                    .withSecond(0)
                    .withNano(0);
            Duration expireDuration = Duration.between(now, nextMonthFirstDayStart);
            stringRedisTemplate.expire(key, expireDuration);
        } else {
            // 已存在，直接修改redis数据
            stringRedisTemplate.opsForValue().setBit(key, day, true);
        }

    }

    public Long getSignInDetailOfMonth() {
        String key = buildSignInKey();
        if(key == null) {
            return 0L;
        }
        int month = LocalDate.now().getMonthValue();
        int year = LocalDate.now().getYear();
        int daysInMonth = YearMonth.of(year, month).lengthOfMonth();

        long SignInDetail = 0L;
        for (int i = 0; i < daysInMonth; i++) {
            Boolean bit = stringRedisTemplate.opsForValue().getBit(key, i);
            if (Boolean.TRUE.equals(bit)) {
                SignInDetail |= (1L << i);
            }
        }
        return SignInDetail;
    }


// region 内部方法
    public String buildSignInKey() {
        Long uid = UserHolder.get().getId();
        int month = LocalDate.now().getMonthValue();
        return SIGNIN_USER_KEY + month + uid;
    }
// endregion
}

~~~





---



## RabbitMQ

![image-20250518193445539](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518193445539.png)

- `Exchange` 是 RabbitMQ 的消息分发器。
- 它 **不存储消息**，只负责按照类型和规则将消息路由出去。
- 消息生产者并不会直接将消息投递到队列，而是发送给某个 Exchange。
- Exchange 再根据其类型、路由键（routing key）和绑定关系，决定将消息发送到哪个队列。



**RabbitMQ面试题**：

https://www.bilibili.com/video/BV1P14y1s7CV/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36

**核心应用场景：解耦、异步、削峰**

**点评项目中应用: **

​		**异步处理订单**：

**✅ 同步部分（用户点击提交订单）：**

1. 用户提交订单请求。
2. 服务层做基本校验，如库存、商品有效性、用户状态等。
3. **生成订单编号，写入订单初始数据到数据库。**
4. **将订单消息（包含订单ID等信息）发送到 RabbitMQ。**   

---



**✅ 异步部分（消费者监听队列）：**

1. RabbitMQ 消息队列中，消费者服务监听对应队列。
2. 消费者异步执行以下操作：
   - **库存扣减服务**
   - 积分服务
   - **订单状态更新（从“待处理”到“处理中”）**
   - **发送短信/邮件通知**
   - **推送消息给运营后台**
3. 若消费失败，可重试或将消息转入死信队列（DLX）做后续处理。



**关于解耦：**

![image-20250518192909813](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518192909813.png)







**关于削峰：**

![image-20250518193003021](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518193003021.png)







### 如何选择合适的消息队列



### RabbitMQ如何确保消息不丢失



### 如何解决MQ中的重复消息




### 如何进行  RocketMQ的性能调优



---



RabbitMQ的进阶应用：

https://www.bilibili.com/video/BV12r4y1Z7wW/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36





# Redis秒杀业务





为什么采用分布式锁 项目后期如果水平扩展（就是采用集群部署），就可以采用了分布式锁

分布式锁有三种

**Mysql：**mysql本身就带有锁机制，但是由于mysql性能本身一般，所以采用分布式锁的情况下，其实使用mysql作为分布式锁比较少见

**Redis**：redis作为分布式锁是非常常见的一种使用方式，现在企业级开发中基本都使用redis或者zookeeper作为分布式锁，利用setnx这个方法，如果插入key成功，则表示获得到了锁，如果有人插入成功，其他人插入失败则表示无法获得到锁，利用这套逻辑来实现分布式锁

**Zookeeper：**zookeeper也是企业级开发中较好的一个实现分布式锁的方案，由于本套视频并不讲解zookeeper的原理和分布式锁的实现，所以不过多阐述

![image-20250518195529662](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518195529662.png)





