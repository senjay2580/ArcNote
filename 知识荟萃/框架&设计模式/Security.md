权限可以分成三类：功能权限、数据权限、**字段权限。**

# 功能权限

 **RBAC + Feature Flags（功能开关）+ 订阅状态检查”** 的混合模型。



# 数据权限



# 用户体系





# Cookie Session Token





# JWT







![image-20251011215924818](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251011215924818.png)

![image-20251011220048453](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251011220048453.png)

![image-20251011220633901](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251011220633901.png)





---

# ==方案 1：纯 JWT（不使用 Redis）==

✅ 核心特点

- **完全无状态**：服务端不存储任何 token 信息  
- **仅靠 JWT 自身签名和过期时间验证**  
- **无法主动使 token 失效**



#### 步骤 1：用户登录

```http
POST /api/login
Content-Type: application/json

{
  "username": "alice",
  "password": "123456"
}
```

**后端处理：**
```java
// 1. 验证用户名密码
User user = userService.findByUsername("alice");
if (!passwordEncoder.matches("123456", user.getPassword())) {
    throw new BadCredentialsException("密码错误");
}

// 2. 生成 JWT（有效期 2 小时）
String token = Jwts.builder()
    .setSubject(user.getId().toString())
    .claim("role", "USER")
    .setIssuedAt(new Date())
    .setExpiration(new Date(System.currentTimeMillis() + 7200_000)) // 2h
    .signWith(SignatureAlgorithm.HS256, "secret-key")
    .compact();

// 3. 直接返回 token（不存任何地方！）
return ResponseEntity.ok(Map.of("token", token));
```

✅ **响应：**
```json
{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx" }
```

> 📌 **关键：服务端没有保存这个 token！**

---

#### 步骤 2：前端存储 token

```js
// 前端（如 Vue）
localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx');
```

---

#### 步骤 3：访问受保护接口

```http
GET /api/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
```

**后端拦截器验证：**
```java
// 1. 从 Header 取 token
String token = request.getHeader("Authorization").replace("Bearer ", "");

// 2. 验证签名 + 检查是否过期（仅靠 JWT 自身）
Claims claims = Jwts.parser()
    .setSigningKey("secret-key")
    .parseClaimsJws(token)
    .getBody();

// 3. 从 claims 获取用户 ID
Long userId = Long.valueOf(claims.getSubject());

// 4. 直接放行（不查库、不查缓存！）
// → 执行 Controller 逻辑
```

✅ **只要 token 未过期且签名正确，就认为合法！**

---

#### 步骤 4：用户点击“退出登录”

```js
// 前端
localStorage.removeItem('token');
// 跳转到登录页
```

**但！问题来了：**

- 服务端 **不知道用户已退出**
- 如果有人 **窃取了这个 token**，仍然可以在 2 小时内继续使用！
- 即使用户 **修改了密码**，旧 token 依然有效！

> ❌ **无法实现真正的“登出”或“强制下线”**

---

### ⚠️ 方案 1 的安全风险总结

| 风险                   | 说明                           |
| ---------------------- | ------------------------------ |
| **Token 泄露长期有效** | 一旦泄露，在过期前可无限使用   |
| **无法登出**           | 退出只是前端删除，服务端无感知 |
| **无法踢下线**         | 用户换设备登录，旧设备仍可操作 |
| **密码修改无效**       | 改密后旧 token 仍能访问系统    |

> 📌 **仅适用于：内部工具、测试环境、低安全要求场景**

---

# ==方案 2：JWT + Redis（推荐方案）==

✅ 核心思想

- JWT 仍用于 **携带用户信息和验签**
- **Redis 存储“当前有效的 token”**（白名单模式）
- 登出 = 从 Redis 删除 token
- 请求验证 = 验签 + 检查 Redis 是否存在该 token



#### 步骤 1：用户登录

```http
POST /api/login
{ "username": "alice", "password": "123456" }
```

**后端处理：**
```java
// 1. 验证用户（同方案1）
User user = ...;

// 2. 生成 JWT（同方案1）
String token = Jwts.builder()...compact();

// 3. ✅ 关键：将 token 存入 Redis！
String redisKey = "auth:token:" + user.getId(); // 每个用户一个 key
redisTemplate.opsForValue().set(
    redisKey, 
    token, 
    Duration.ofHours(2) // 与 JWT 过期时间一致
);

// 4. 返回 token
return ResponseEntity.ok(Map.of("token", token));
```

> 📌 **Redis 中：`auth:token:123 → "eyJhbGci..."`**

---

#### 步骤 2：前端存储 token（同方案 1）

```js
localStorage.setItem('token', 'eyJhbGci...');
```

---

#### 步骤 3：访问受保护接口

```http
GET /api/profile
Authorization: Bearer eyJhbGci...
```

**后端拦截器验证：**
```java
// 1. 解析 JWT 获取用户 ID
Claims claims = Jwts.parser()...parseClaimsJws(token).getBody();
Long userId = Long.valueOf(claims.getSubject());

// 2. ✅ 关键：从 Redis 获取该用户的当前有效 token
String validToken = redisTemplate.opsForValue().get("auth:token:" + userId);

// 3. 比较：请求中的 token 是否等于 Redis 中存储的？
if (validToken == null || !validToken.equals(token)) {
    throw new AccessDeniedException("Token 已失效或已被登出");
}

// 4. 放行 → 执行业务逻辑
```

> ✅ **只有“当前最新登录的 token”才有效！**

---

#### 步骤 4：用户点击“退出登录”

```http
POST /api/logout
Authorization: Bearer eyJhbGci...
```

**后端处理：**
```java
// 1. 从 token 解析 userId
Long userId = getUserIdFromToken(token);

// 2. ✅ 关键：删除 Redis 中的 token
redisTemplate.delete("auth:token:" + userId);

// 3. 返回成功
return ResponseEntity.ok("已退出");
```

**前端：**
```js
localStorage.removeItem('token');
router.push('/login');
```

> ✅ **此时即使有人持有旧 token，也无法通过验证！**

---

#### 步骤 5：用户修改密码（增强安全）

```java
// 修改密码成功后
public void changePassword(Long userId, String newPassword) {
    // 1. 更新数据库密码
    user.setPassword(passwordEncoder.encode(newPassword));
    userRepository.save(user);
    
    // 2. ✅ 强制所有设备下线：删除 token
    redisTemplate.delete("auth:token:" + userId);
}
```

> ✅ **旧 token 立即失效，防止账号被盗用**

---

#### 步骤 6：实现“单点登录”（同一账号只允许一个设备）

- 登录时，**无论是否已有 token，都覆盖 Redis 中的值**
- 旧设备下次请求时，token 与 Redis 不匹配 → 自动失效

```java
// 登录时直接 set（覆盖旧值）
redisTemplate.opsForValue().set("auth:token:" + userId, newToken, ...);
```

> ✅ **天然支持“踢下线”功能**

---

### ✅ 方案 2 的优势总结

| 能力              | 是否支持 | 说明                            |
| ----------------- | -------- | ------------------------------- |
| 主动登出          | ✅        | 删除 Redis 即可                 |
| 强制下线          | ✅        | 修改密码/管理员操作时删除 token |
| 单点登录          | ✅        | 新登录覆盖旧 token              |
| 防 token 泄露滥用 | ✅        | 泄露后可立即登出使其失效        |
| 无状态优势保留    | ✅        | JWT 仍携带用户信息，减少查库    |



当然可以！下面我将 **全面、深入、分步骤** 地详细说明 **方案三：JWT + Refresh Token（双 Token 机制）**，这是目前 **高安全性、高用户体验** 的前后端分离项目中 **最推荐的认证方案**，尤其适用于金融、电商、SaaS 等对安全和体验都有较高要求的场景。

---

## ==一、为什么需要方案三？==

回顾前两个方案的痛点：

| 方案                     | 问题                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **方案 1（纯 JWT）**      | 无法登出、token 一旦泄露危害大（有效期长）                   |
| **方案 2（JWT + Redis）** | 虽可登出，但若 access_token 有效期设太短（如 30 分钟），用户频繁重新登录，体验差 |

### ✅ 方案三的核心思想：

> **用两个 Token 分工协作：**
>
> - **Access Token**：短期有效（如 15~30 分钟），用于 **日常 API 请求**
> - **Refresh Token**：长期有效（如 7~30 天），仅用于 **换取新的 Access Token**

这样既 **限制了 Access Token 的泄露风险**，又实现了 **用户无感续期**（不用频繁输密码）。



| Token 类型        | 有效期           | 存储位置                              | 用途                                    | 安全要求                        |
| ----------------- | ---------------- | ------------------------------------- | --------------------------------------- | ------------------------------- |
| **Access Token**  | 短（15~60 分钟） | 前端内存 / localStorage               | 调用业务 API（如 `/api/user`）          | 可泄露，但危害小（很快过期）    |
| **Refresh Token** | 长（7~30 天）    | **HttpOnly Cookie**（推荐）或安全存储 | 仅用于 `/refresh` 接口换新 Access Token | **必须严格保护**（防 XSS/CSRF） |

> 🔒 **关键安全设计：Refresh Token 不应出现在前端 JavaScript 可访问的地方！**

**场景设定：**

- 用户首次登录
- Access Token 过期后自动续期
- 用户主动登出
- Refresh Token 过期需重新登录

---

### 步骤 1：用户首次登录

```http
POST /api/login
Content-Type: application/json

{
  "username": "alice",
  "password": "123456"
}
```

#### 后端处理逻辑：

```java
// 1. 验证用户名密码
User user = userService.validate(username, password);

// 2. 生成 Access Token（短有效期）
String accessToken = JwtUtil.createAccessToken(user.getId(), 30); // 30分钟

// 3. 生成 Refresh Token（长有效期 + 唯一ID）
String refreshToken = JwtUtil.createRefreshToken(user.getId(), 7 * 24 * 60); // 7天

// 4. ✅ 将 Refresh Token 存入 Redis（用于登出和验证）
String redisKey = "refresh_token:" + user.getId();
redisTemplate.opsForValue().set(redisKey, refreshToken, Duration.ofDays(7));

// 5. 响应：
//    - Access Token 放在 JSON 中
//    - Refresh Token 放在 HttpOnly Cookie 中（更安全！）
ResponseCookie refreshCookie = ResponseCookie.from("refresh_token", refreshToken)
    .httpOnly(true)          // 禁止 JS 访问（防 XSS）
    .secure(true)            // 仅 HTTPS 传输
    .path("/api")            // 作用路径
    .maxAge(Duration.ofDays(7))
    .build();

return ResponseEntity.ok()
    .header(HttpHeaders.SET_COOKIE, refreshCookie.toString())
    .body(Map.of("access_token", accessToken));
```

#### 前端收到：

- JSON：`{ "access_token": "xxx" }`
- Cookie：`refresh_token=yyy; HttpOnly; Secure; Path=/api`

> ✅ **前端只能拿到 access_token，refresh_token 被浏览器安全保管**

---

### 步骤 2：前端调用业务接口（使用 Access Token）

```http
GET /api/profile
Authorization: Bearer <access_token>
```

#### 后端验证（同方案 2）：

- 验签 + 检查过期
- （可选）查 Redis 确认 access_token 未被提前吊销（一般不需要，因有效期短）

✅ **只要 access_token 有效，就放行**

---

### 步骤 3：Access Token 过期 → 自动续期

当 access_token 过期（返回 401），前端 **自动调用刷新接口**：

```http
POST /api/refresh
Cookie: refresh_token=yyy  // 浏览器自动带上
```

> 📌 **前端不需要、也无法读取 refresh_token！**

#### 后端 `/refresh` 接口逻辑：

```java
@PostMapping("/refresh")
public ResponseEntity<?> refresh(HttpServletRequest request) {
    // 1. 从 Cookie 获取 Refresh Token
    String refreshToken = getCookieValue(request, "refresh_token");
    if (refreshToken == null) {
        throw new BadCredentialsException("Refresh token missing");
    }

    // 2. 验证 Refresh Token 签名和过期时间
    Claims claims = JwtUtil.parseToken(refreshToken, "refresh-secret");
    Long userId = Long.valueOf(claims.getSubject());

    // 3. ✅ 关键：检查 Redis 中是否还存在该 refresh token（是否已被登出？）
    String storedRefreshToken = redisTemplate.opsForValue().get("refresh_token:" + userId);
    if (!refreshToken.equals(storedRefreshToken)) {
        throw new BadCredentialsException("Refresh token invalid or revoked");
    }

    // 4. 生成新的 Access Token（Refresh Token 不变）
    String newAccessToken = JwtUtil.createAccessToken(userId, 30);

    // 5. 返回新 Access Token
    return ResponseEntity.ok(Map.of("access_token", newAccessToken));
}
```

#### 前端处理：

```js
// Axios 拦截器
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      try {
        // 自动刷新
        const res = await axios.post('/api/refresh');
        const newToken = res.data.access_token;
        localStorage.setItem('access_token', newToken);
        // 重发原请求
        error.config.headers['Authorization'] = 'Bearer ' + newToken;
        return axios(error.config);
      } catch (refreshError) {
        // 刷新失败 → 跳转登录
        router.push('/login');
      }
    }
    return Promise.reject(error);
  }
);
```

✅ **用户无感知！页面不跳转，请求自动重试**

---

### 步骤 4：用户主动登出

```http
POST /api/logout
Cookie: refresh_token=yyy  // 自动带上
Authorization: Bearer <access_token>
```

#### 后端处理：

```java
@PostMapping("/logout")
public ResponseEntity<?> logout(HttpServletRequest request) {
    // 1. 从 Cookie 取 refresh token
    String refreshToken = getCookieValue(request, "refresh_token");
    
    // 2. 解析用户 ID
    Long userId = JwtUtil.getUserIdFromRefreshToken(refreshToken);
    
    // 3. ✅ 删除 Redis 中的 refresh token（使其失效）
    redisTemplate.delete("refresh_token:" + userId);
    
    // 4. 清除 Cookie（可选）
    ResponseCookie clearCookie = ResponseCookie.from("refresh_token", "")
        .httpOnly(true)
        .secure(true)
        .path("/api")
        .maxAge(0) // 立即过期
        .build();
    
    return ResponseEntity.ok()
        .header(HttpHeaders.SET_COOKIE, clearCookie.toString())
        .body("Logged out");
}
```

#### 前端：

```js
localStorage.removeItem('access_token');
// Cookie 由后端清除，前端无需操作
router.push('/login');
```

> ✅ **登出后，即使 access_token 未过期，也无法续期，且 refresh token 已失效**

---

### 步骤 5：Refresh Token 过期

- 7 天后，refresh token 过期
- 调用 `/refresh` 会失败（JWT 过期异常）
- 前端跳转到登录页，**用户需重新输入账号密码**

## 



### 1. **Refresh Token 必须用 HttpOnly Cookie**

 **HttpOnly 不影响浏览器正常发送 Cookie，只阻止前端 JS 访问**

- 防止 XSS 攻击窃取
- 配合 `Secure`（仅 HTTPS）、`SameSite=Strict`（防 CSRF）

### 2. **Refresh Token 绑定设备/会话（可选）**

- 在 JWT 中加入 `jti`（唯一 ID）或 `device_fingerprint`
- Redis 存储时带上设备信息，防止 token 被复制到其他设备使用

### 3. **Refresh Token 一次性使用（高级）**

- 每次刷新后，**生成新的 refresh token** 并更新 Redis
- 旧 refresh token 立即失效（类似 OAuth2 的 rotation 机制）
- 可防重放攻击，但实现复杂

### 4. **敏感操作仍需二次验证**

- 如修改密码、支付，即使有有效 token，也要求输入密码或短信验证码

---

## 方案三 vs 方案二 对比

| 能力                  | 方案二（JWT + Redis）                       | 方案三（JWT + Refresh Token）                  |
| --------------------- | ------------------------------------------- | ---------------------------------------------- |
| 登出支持              | ✅                                           | ✅                                              |
| 强制下线              | ✅                                           | ✅                                              |
| 无感续期              | ❌（需频繁登录）                             | ✅（自动刷新）                                  |
| Access Token 泄露风险 | 中（若设 2 小时）                           | **低**（仅 30 分钟）                           |
| 前端存储安全          | access_token 在 localStorage（有 XSS 风险） | access_token 仍存在风险，但 refresh_token 安全 |
| 实现复杂度            | 中                                          | **较高**（需处理刷新逻辑）                     |
| 适合场景              | 一般企业应用                                | **高安全 + 高体验要求系统**                    |



---



# Spring Security 

**Spring Security 的登录拓展起来不方便，例如说验证码、三方登录等等。**

各种版本可能语法、操作、功能都不一样，这种如何学习呢 --重点学设计思路本质原理来学

java web 三大组件 listener fliter servlet 

 

**SpringSecurity 的核心其实就是 Filter   下面看一下它的设计演化**

![image-20251019081911735](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019081911735.png)

![image-20251019081928897](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019081928897.png)



---



![image-20251019083302650](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019083302650.png)

~~~
官网: https://docs.spring.io/spring-security/reference/5.8/servlet/authentication/passwords/in-memory.html
SpringSecurity 内置案例核心 API

InMemoryUserDetailsManager: 内置账户信息管理类，是 UserDetailsService 的子类
UserDetailsService: SpringSecurity 用户信息管理类的核心接口, 管理用户信息来源(数据库还是内存以及其他...)
UserDetails: SpringSecurity 封装用户信息的核心接口，给 SpringSecurity 送用户信息时 SpringSecurity 只认 UserDetails

以上的 API 是内置认证的简单 API

~~~





## 认证运行原理

![image-20251019083953447](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019083953447.png)

~~~sql
-- 当前流行的权限控制系统 RBAC 模式, 所以数据库表设计基于 RBAC

-- 创建数据库
CREATE DATABASE rbac DEFAULT CHARACTER SET utf8;

-- 用户表
CREATE TABLE user(
    user_id     BIGINT          NOT NULL    PRIMARY KEY     AUTO_INCREMENT      COMMENT '用户 ID 主键',
    phone       VARCHAR(50)     NOT NULL    UNIQUE                              COMMENT '手机号，唯一',
    password    VARCHAR(255)    NOT NULL                                        COMMENT '密码',
    username    VARCHAR(100)    NOT NULL                                        COMMENT '用户名'
)AUTO_INCREMENT = 1000 DEFAULT charset = utf8 COMMENT ='用户表';
-- 角色表
CREATE TABLE role(
    role_id     BIGINT          NOT NULL    PRIMARY KEY     AUTO_INCREMENT      COMMENT '角色 ID 主键',
    role_name   VARCHAR(100)    NOT NULL                                        COMMENT '角色名'
)AUTO_INCREMENT = 1000 DEFAULT charset = utf8 COMMENT ='角色表';
-- 权限表
CREATE TABLE permission(
    permission_id     BIGINT          NOT NULL    PRIMARY KEY     AUTO_INCREMENT      COMMENT '权限 ID 主键',
    permission_name   VARCHAR(100)    NOT NULL                                        COMMENT '权限名'
)AUTO_INCREMENT = 1000 DEFAULT charset = utf8 COMMENT ='权限表';
-- 用户角色关联表
CREATE TABLE user_role(
    user_id     BIGINT  NOT NULL   COMMENT '用户 ID',
    role_id     BIGINT  NOT NULL   COMMENT '角色 ID',
    PRIMARY KEY (user_id, role_id)
) DEFAULT charset = utf8 COMMENT ='用户角色关联表';
-- 角色权限关联表
CREATE TABLE role_permission(
    role_id             BIGINT  NOT NULL   COMMENT '角色 ID',
    permission_id       BIGINT  NOT NULL   COMMENT '权限 ID',
    PRIMARY KEY (role_id, permission_id)
) DEFAULT charset = utf8 COMMENT ='角色权限关联表';

~~~

> **UserDetails 接口实现, 封装用户信息(给 SpringSecurity 送数据)**
>
> 锁定和不可用

~~~java
/**
 * 封装用户信息
 * SpringSecurity 规定给他传递的用户信息必须是 UserDetails 接口的子类实例对象进行封装
 */
@Data
public class LoginUserDetails implements UserDetails {
    private User user;
    public LoginUserDetails() {
    }
    public LoginUserDetails(User user) {
        this.user = user;
    }
    /**
     * 暂时只实现认证, 不实现授权, 所以这边权限给空集合
     */
    @Override
    public Collection <? extends GrantedAuthority> getAuthorities() {
        return new ArrayList <>();
    }
    //装配密码
    @Override
    public String getPassword() {
        return user.getPassword();
    }
    //装配账户, 这里用手机号作为登录账号
    @Override
    public String getUsername() {
        return user.getPhone();
    }
    //账号是否过期, 在数据库中没有设置, 给默认值不过期
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    //账号是否锁定, 在数据库中没有设置, 给默认值不锁定
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }
    //密码是否过期, 在数据库中没有设置, 给默认值不过期
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    //账号是否可用, 在数据库中没有设置, 给默认值可用
    @Override
    public boolean isEnabled() {
        return true;
    }
}

~~~

替换 InMemoryUserDetailsManager 实现 UserDetailsService 方法

~~~java
/**
 * UserDetailsService 是 Spring Security 提供的从数据库获取数据的核心接口
 * 实现 UserDetailsService 重写里面的 loadUserByUsername 方法, 替换默认从内存中获取用户信息
 * 具体 loadUserByUsername 方法中的逻辑可以参考 InMemoryUserDetailsManager 实现
 */
@Service
public class UserDetailsServiceImpl implements UserDetailsService {
    @Resource
    private UserMapper userMapper;
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        //通过用户名从数据库中查询用户信息(这个用户名从前端传递过来时可以使用手机号，邮箱或者其他用户账号)
        User user = userMapper.getUserByPhone(username);
        //判断当前账号是否存在
        if(Objects.isNull(user)){
            //如果为空，直接抛出异常
            throw new UsernameNotFoundException(username);
        }
        /*
         * 不为空说明数据库中存在, 将信息送到 SpringSecurity 上下文中
         * 参考 InMemoryUserDetailsManager 类中的 loadUserByUsername 方法逻辑
         */
        return new LoginUserDetails(user);
    }
}

~~~


~~~css
1. 创建配置类
2. 将 BCryptPasswordEncoder 加入到 IOC 容器中，SpringSecurity 自动生效

~~~



**区分认证（authentication）和授权（authorization）**

## ==认证==

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019091721713.png)

- **`SecurityContext`**：是一个 **对象**，用来 **存储当前用户的认证信息（Authentication）**。
- **`SecurityContextHolder`**：是一个 **工具类/持有者（Holder）**，用来 **获取或设置当前线程的 `SecurityContext`**。

~~~css
根据登录流程图介绍登录相关 API

SecurityFilterChain: SpringSecurity 核心过滤器, SpringSecurity 默认会自动创建一个此对象，用来支持自带的登录，现在采用前后端分离，登录逻辑发生变化，所以需要我们自己创建 SpringSecurity 来覆盖默认的。

UsernamePasswordAuthenticationToken: 封装前端页面传递过来的用户名和密码，封装好后通过 AuthenticationManager 传递给 SpringSecurity 上下文

AuthenticationManager: SpringSecurity 的认证管理器，见名知意，用来进行认证

Authentication: 认证实例，认证成功后，里面封装认证成功后的信息

流程图总的其它 API 暂时使用不上，不做介绍

~~~

覆盖默认的 **SecurityFilterChain**

![image-20251019093337251](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019093337251.png)

![image-20251019095104362](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019095104362.png)

~~~java
@RestController
public class LoginController {
    @Resource
    private AuthenticationManager authenticationManager;
    /**
     * 登录
     * @param phone    手机号
     * @param password 密码
     * @return 响应结果
     */
    @PostMapping(value = "/login")
    public Result login(String phone, String password){
        /*
         * SpringSecurity 的认证逻辑
         * 默认情况 SpringSecurity 内置了登录页面, 内置了从页面获取数据, 并将其数据送到 SpringSecurity 上下文的方式
         * 当前前后端分离的逻辑，数据不再从页面获取，所以不能再使用内置逻辑，需要程序员自己实现将数据送到 SpringSecurity 上下文中
         * 官网地址: https://docs.spring.io/spring-security/reference/5.8/servlet/authentication/passwords/form.html
         */
        //封装用户名(手机号作为用户名)和密码
        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(phone, password);
        //调用认证管理中的认证方法，调用后可能出现异常，所以需要 try...catch
        try {
            Authentication authenticate = authenticationManager.authenticate(authenticationToken);
            //如果认证成功 Authentication 中就会有用户信息, 否则为空
            if(Objects.isNull(authenticate)){
                //认证失败
                return Result.error("认证失败, 用户名或密码错误");
            }
        }catch (RuntimeException e){
            e.printStackTrace();
            //认证失败
            return Result.error("认证失败, 用户名或密码错误");
        }
        return Result.ok();
    }
}

~~~

**AuthenticationEntryPoint**

~~~java
/**
 * 在未认证或者认证错误的情况下访问需要认证的资源时的处理类
 */
@Component  //加入到 IOC 容器
public class LoginUnAuthenticationEntryPointHandler implements AuthenticationEntryPoint {
    /*
     * 当访问一个需要认证的资源时因为当前用户没有认证或者认证失败，直接访问资源会交给此函数进行处理
     * 因为架构是前后端分离的项目, 所以给客户端的提示保持和控制器的返回值格式相同
     */
    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authException) throws IOException, ServletException {
        response.setCharacterEncoding("utf-8");
        response.setContentType("application/json");
        Result result = Result.error("用户未认证或登录已过期，请重新登录后再访问");
        //将消息 json 化
        String json = JSONUtil.toJsonStr(result);
        //送到客户端
        response.getWriter().print(json);
    }
}

~~~

![image-20251019093633450](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019093633450.png)



~~~css
传统前后端不分离的架构采用 Session+Cookie 机制

现在前后端分离架构，采用 token 令牌方式

token 生成采用 JWT 工具生成和校验, 使用 Redis 数据库进行保存

~~~



思考：这个 chain 是过滤器链条 如何分别设置 各个过滤器的逻辑呢



**Redis + JWT**

**推荐“UUID（RedisKey） 作 Token + Redis 存状态”**，这是最平衡安全、功能、性能的方案。



​            **在复杂系统中，开发者通常不会完全信任 “上游流程的输出”。**

~~~java
@RestController
public class LoginController {
    @Resource
    private AuthenticationManager authenticationManager;
    @Resource
    private RedisClient redisClient;
    /**
     * 登录
     * @param phone    手机号
     * @param password 密码
     * @return 响应结果
     */
    @PostMapping(value = "/login")
    public Result login(String phone, String password){
        /*
         * SpringSecurity 的认证逻辑
         * 默认情况 SpringSecurity 内置了登录页面, 内置了从页面获取数据, 并将其数据送到 SpringSecurity 上下文的方式
         * 当前前后端分离的逻辑，数据不再从页面获取，所以不能再使用内置逻辑，需要程序员自己实现将数据送到 SpringSecurity 上下文中
         * 官网地址: https://docs.spring.io/spring-security/reference/5.8/servlet/authentication/passwords/form.html
         */
        //封装用户名(手机号作为用户名)和密码
        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(phone, password);
        //调用认证管理中的认证方法，调用后可能出现异常，所以需要 try...catch
        try {
            Authentication authenticate = authenticationManager.authenticate(authenticationToken);
            //如果认证成功 Authentication 中就会有用户信息, 否则为空
            if(Objects.isNull(authenticate)){
                //认证失败
                return Result.error("认证失败, 用户名或密码错误");
            }

            //登录成功将用户信息保存到 redis 中, 以 token 作为 key
            LoginUserDetails principal = (LoginUserDetails) authenticate.getPrincipal();
            if(Objects.isNull(principal)){
                return Result.error("认证失败, 用户名或密码错误");
            }
            //将用户信息 json 化
            String json = JSONUtil.toJsonStr(principal);
            //使用 token 作为 redis 的 key 格式为 login: token
            String token = JwtUtils.sign(principal.getUsername(), 1000 * 60 * 60 * 24 * 7L);//过期时间为 7 天
            //将用户信息 json 化后保存到 redis 中
            redisClient.set("login:token:"+token, json,1000 *60 * 60 * 24 * 7L); //过期时间 7 天
            Map <String,Object> map = new HashMap <>();
            map.put("token", token);
            return Result.ok(map);
        }catch (RuntimeException e){
            e.printStackTrace();
            //认证失败
            return Result.error("认证失败, 用户名或密码错误");
        }
    }
}

~~~

~~~css
客户端发送的所有请求都需要带 token，在进行登录时单独进行 token 的校验，如果登陆过，刷新 token

在登录中添加一个校验逻辑，删除原来的 key

~~~



![image-20251019100627576](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019100627576.png)





![image-20251019101725930](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019101725930.png)

**Spring Security 上下文（`SecurityContext`）是 Spring Security 用来存储“当前用户是谁、有什么权限”的一个临时容器，每个 HTTP 请求独享一个。**

~~~java
/**
 * 自定义过滤器，实现 token 令牌的判断
 */
@Component
public class JwtAuthenticationTokenFilter extends OncePerRequestFilter {
    @Resource
    private RedisClient redisClient;
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        //获取请求头
        String token = request.getHeader("token");
        if(StringUtils.hasLength(token)){
            //redis 中获取用户信息
            String key = "login:token:"+token;
            String json = redisClient.get(key);
            if(StringUtils.hasLength(json)){
                //反序列化
                LoginUserDetails user = JSONUtil.toBean(json, LoginUserDetails.class);
                if(Objects.nonNull(user)){
                    //封装用户信息, 送到下一个过滤器  UsernamePasswordAuthenticationFilter
                    UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                    //将 Redis 数据库中的信息送到 SpringSecurity 上下文中
                    SecurityContextHolder.getContext().setAuthentication(authenticationToken);
                }else {
                    SecurityContextHolder.getContext().setAuthentication(null);
                }
            }
        }
        //放行, 后面交给 Spring Security 框架
        filterChain.doFilter(request, response);
    }
}

~~~



~~~java
/**
 * Spring Security 配置
 */
@Configuration
public class SecurityConfig {

    @Resource
    private LoginUnAuthenticationEntryPointHandler loginUnAuthenticationEntryPointHandler;
    @Resource
    private JwtAuthenticationTokenFilter jwtAuthenticationTokenFilter;
    /*
     * 密码加密和解密工具
     */
    @Bean
    public PasswordEncoder generalPasswordEncoder(){
        return new BCryptPasswordEncoder();
    }
    /**
     * SpringSecurity 过滤器
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf().disable() //防止跨站请求伪造
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS) //取消 session
                .and()
                .authorizeRequests()
                .antMatchers("/login").permitAll() //登陆和未登录的人都可以访问访问
                .anyRequest().authenticated();//除了上面设置的地址可以匿名访问, 其它所有的请求地址需要认证访问
        //将自定义的过滤器注册到 SpringSecurity 过滤器链中, 并且设置到 UsernamePasswordAuthenticationFilter 前面
        http.addFilterBefore(jwtAuthenticationTokenFilter, UsernamePasswordAuthenticationFilter.class);
        //注册自定义的处理器(未认证用户访问需要认证资源的处理器)
        http.exceptionHandling().authenticationEntryPoint(loginUnAuthenticationEntryPointHandler);
        return http.build();
    }
    /**
     * SpringSecurity 认证管理器
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }
}

~~~



## ==授权（权限控制）==

> **授权的意义就是当一个用户登录成功后，此账户本身拥有的权限(例如 当前用户用哪些角色, 当前角色都能干什么 [删除|更新等])**

~~~css
从数据库中将用户信息送到上下文 在 UserDetailsService 接口的实现类中

实现步骤:
第一步: mapper 提供查询方法, 将用户相关的权限信息查询到封装到 UserDetails 的对象中
	通过用户 ID 查询角色名称列表
	通过角色 ID 查询权限名称列表
第二步: 在 UserDetailsService 中进行封装
	在 UserDetailsService 中调用 mapper 并且封装传递给 SpringSecurity 上下文，修改 UserDetails 结构添加属性等
第三步: 在控制器层进行注解控制(配置文件)
第四步: 开启注解配置否则不生效
第五步: 权限不够的处理器

~~~

![image-20251019101029892](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019101029892.png)

**角色：就是粗粒度权限**



~~~java
/**
 * 封装用户信息
 * SpringSecurity 规定给他传递的用户信息必须是 UserDetails 接口的子类实例对象进行封装
 */
@Data
public class LoginUserDetails implements UserDetails {

    // 用户类
    private User user;

    // 权限类
    
    //角色名称列表，用于授权
    private List <String> roleNames;
    //权限名称列表，用户授权
    private List <String> permissionNames;

    public LoginUserDetails(User user, List <String> roleNames, List <String> permissionNames) {
        this.user = user;
        this.roleNames = roleNames;
        this.permissionNames = permissionNames;
    }


    @Override
    public Collection <? extends GrantedAuthority> getAuthorities() {
        List <GrantedAuthority> authorities = new ArrayList <>();
        //添加角色
        if(! CollectionUtils.isEmpty(roleNames)){
            //将角色设置到 GrantedAuthority 中，官网要求角色要加上前缀 ROLE_xxx 区分其它权限
            for (String roleName : roleNames) {
                authorities.add(new SimpleGrantedAuthority("ROLE_"+roleName));
            }
        }
        //添加权限
        if(! CollectionUtils.isEmpty(permissionNames)){
            //将权限设置到 GrantedAuthority 中
            for (String permissionName : permissionNames) {
                authorities.add(new SimpleGrantedAuthority(permissionName));
            }
        }
        return authorities;
    }
    //装配密码
    @Override
    public String getPassword() {
        return user.getPassword();
    }
    //装配账户, 这里用手机号作为登录账号
    @Override
    public String getUsername() {
        return user.getPhone();
    }
    //账号是否过期, 在数据库中没有设置, 给默认值不过期
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    //账号是否锁定, 在数据库中没有设置, 给默认值不锁定
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }
    //密码是否过期, 在数据库中没有设置, 给默认值不过期
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    //账号是否可用, 在数据库中没有设置, 给默认值可用
    @Override
    public boolean isEnabled() {
        return true;
    }
}

~~~



~~~java
/**
 * UserDetailsService 是 Spring Security 提供的从数据库获取数据的核心接口
 * 实现 UserDetailsService 重写里面的 loadUserByUsername 方法, 替换默认从内存中获取用户信息
 * 具体 loadUserByUsername 方法中的逻辑可以参考 InMemoryUserDetailsManager 实现
 */
@Service
public class UserDetailsServiceImpl implements UserDetailsService {
    @Resource
    private UserMapper userMapper;
    @Resource
    private UserRoleMapper userRoleMapper;
    @Resource
    private RoleMapper roleMapper;
    @Resource
    private RolePermissionMapper rolePermissionMapper;
    @Resource
    private PermissionMapper permissionMapper;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        //通过用户名从数据库中查询用户信息(这个用户名从前端传递过来时可以使用手机号，邮箱或者其他用户账号)
        User user = userMapper.getUserByPhone(username);
        //判断当前账号是否存在
        if(Objects.isNull(user)){
            //如果为空，直接抛出异常
            throw new UsernameNotFoundException(username);
        }
        /*
         * 不为空说明数据库中存在, 将信息送到 SpringSecurity 上下文中
         * 参考 InMemoryUserDetailsManager 类中的 loadUserByUsername 方法逻辑
         */
        List <UserRole> userRoles = userRoleMapper.getUserRolesByUserId(user.getUserId());
        //角色名称列表
        List <String> roleNames = new ArrayList <>();
        //权限名称列表
        List <String> permissionNames = new ArrayList <>();
        if(! CollectionUtils.isEmpty(userRoles)){
            List <Long> roleIds = userRoles.stream().map(UserRole:: getRoleId).collect(Collectors.toList());
            if(! CollectionUtils.isEmpty(roleIds)){
                //查询角色信息
                List <Role> roles = roleMapper.batchGetRolesByRoleIds(roleIds);
                if(! CollectionUtils.isEmpty(roles)){
                    List <String> roleNameList = roles.stream().map(Role:: getRoleName).collect(Collectors.toList());
                    roleNames.addAll(roleNameList);
                }
                //查询权限
                List <RolePermission> rolePermissions = rolePermissionMapper.getRolePermissionsByRoleIds(roleIds);
                if(! CollectionUtils.isEmpty(rolePermissions)){
                    List <Long> permissionIdList = rolePermissions.stream().map(RolePermission:: getPermissionId).collect(Collectors.toList());
                    if(! CollectionUtils.isEmpty(permissionIdList)){
                        List <Permission> permissions = permissionMapper.batchGetPermissionsByPermissionIds(permissionIdList);
                        if(! CollectionUtils.isEmpty(permissions)){
                            List <String> permissionNameList = permissions.stream().map(Permission:: getPermissionName).collect(Collectors.toList());
                            if(! CollectionUtils.isEmpty(permissionNameList)){
                                permissionNames.addAll(permissionNameList);
                            }
                        }
                    }
                }
            }
        }
        return new LoginUserDetails(user, roleNames, permissionNames);
    }
}

~~~

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019133457647.png" alt="image-20251019133457647" style="zoom: 67%;" />



`@PreAuthorize` 中的 `hasRole()`、`hasAuthority()` 依赖于 **当前用户的权限信息**，这些信息通常在登录认证时加载：

**粗细粒度管控**

~~~java
// 在配置文件上添加注解，开启注解校验
//官网地址: https://docs.spring.io/spring-security/reference/5.8/servlet/authorization/method-security.html

/**
 * 测试控制器
 * 验证 SpringSecurity 是否生效
 */
@RestController
public class HelloController {
    /**
     * 测试方法 1 -- 游客访问 -- 不登录也可以访问
     */
    @GetMapping(value = "/test1")
    public Result test1(){
        System.out.println("test1...");
        return Result.ok("test1...");
    }

    /**
     * 测试方法 2 -- 登录后才可以访问
     */
    @GetMapping(value = "/test2")
    public Result test2(){
        System.out.println("test2...");
        return Result.ok("test2...");
    }

    /**
     * 测试方法 3 -- 登录后，具有 admin 角色才能访问
     */
    @PreAuthorize(value = "hasRole('admin')")
    @GetMapping(value = "/test3")
    public Result test3(){
        System.out.println("test3...");
        return Result.ok("test3...");
    }

    /**
     * 测试方法 4 -- 登录后，具有 admin 或者 CEO 角色才能访问
     */
    @PreAuthorize(value = "hasAnyRole('admin','CEO')")
    @GetMapping(value = "/test4")
    public Result test4(){
        System.out.println("test4...");
        return Result.ok("test4...");
    }

    /**
     * 测试方法 5 -- 登录后，同时具有 CTO 和 CFO 角色才能访问
     */
    @PreAuthorize(value = "hasRole('CTO') and hasRole('CEO')")
    @GetMapping(value = "/test5")
    public Result test5(){
        System.out.println("test5...");
        return Result.ok("test5...");
    }
    /**
     * 测试方法 6 -- 登录后，具有 user: add 权限可以访问 
     */
    @PreAuthorize(value = "hasAuthority('user: add')")
    @GetMapping(value = "/test6")
    public Result test6(){
        System.out.println("test6...");
        return Result.ok("test6...");
    }

    /**
     * 测试方法 7 -- 登录后，具有 user: add 或者 user: del 权限可以访问
     */
    @PreAuthorize(value = "hasAnyAuthority('user: add','user: del')")
    @GetMapping(value = "/test7")
    public Result test7(){
        System.out.println("test7...");
        return Result.ok("test7...");
    }

    /**
     * 测试方法 8 -- 登录后，具有 user: add 和 user: del 权限可以访问
     */
    @PreAuthorize(value = "hasAuthority('user: add') and hasAuthority('user: del')")
    @GetMapping(value = "/test8")
    public Result test8(){
        System.out.println("test8...");
        return Result.ok("test8...");
    }
}

~~~

- **`csrf().disable()`**：

  CSRF 是一种攻击方式（攻击者诱导用户在已登录状态下发送恶意请求），但在 **前后端分离项目** 中，通常用 Token（如 JWT）认证，无需依赖 Cookie，因此关闭 CSRF 可简化操作。

  （如果是传统 Session 认证的项目，一般不关闭 CSRF）

- **`sessionCreationPolicy(STATELESS)`**：

  设置会话策略为 “无状态”，即 Spring Security 不创建也不使用 HttpSession，所有认证信息通过 Token 传递（适合 JWT 等无状态认证场景）。

~~~java
/**
 * Spring Security 配置
 */
@Configuration
@EnableMethodSecurity(securedEnabled = true) //开发方法权限验证
public class SecurityConfig {

    @Resource
    private LoginUnAuthenticationEntryPointHandler loginUnAuthenticationEntryPointHandler;
    @Resource
    private JwtAuthenticationTokenFilter jwtAuthenticationTokenFilter;
    @Resource
    private LoginUnAccessDeniedHandler loginUnAccessDeniedHandler;
    /*
     * 密码加密和解密工具
     */
    @Bean
    public PasswordEncoder generalPasswordEncoder(){
        return new BCryptPasswordEncoder();
    }
    /**
     * SpringSecurity 过滤器
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf().disable() //防止跨站请求伪造
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS) //取消 session
                .and()
                .authorizeRequests()
                .antMatchers("/login", "/test1").permitAll() //登陆和未登录的人都可以访问访问
                .anyRequest().authenticated();//除了上面设置的地址可以匿名访问, 其它所有的请求地址需要认证访问
        //将自定义的过滤器注册到 SpringSecurity 过滤器链中, 并且设置到 UsernamePasswordAuthenticationFilter 前面
        http.addFilterBefore(jwtAuthenticationTokenFilter, UsernamePasswordAuthenticationFilter.class);
        //注册自定义的处理器(未认证用户访问需要认证资源的处理器)
        http.exceptionHandling().authenticationEntryPoint(loginUnAuthenticationEntryPointHandler);
        //注册自定义的处理器(认证后的用户访问需要认证资源时因为权限不足走的处理器)
        http.exceptionHandling().accessDeniedHandler(loginUnAccessDeniedHandler);
        return http.build();
    }
    /**
     * SpringSecurity 认证管理器
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }
}

~~~

**AccessDeniedHandler**

~~~java
// 如果登录成功, 使用当前用户进行访问，发现权限不够，报权限错误，定义处理器进行处理

/**
 * 权限不足处理器
 * 用户登录成功，访问某一个资源时因为权限不足，报异常
 */
@Component
public class LoginUnAccessDeniedHandler implements AccessDeniedHandler {
    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException accessDeniedException) throws IOException, ServletException {
        response.setCharacterEncoding("utf-8");
        response.setContentType("application/json");
        Result result = Result.error("权限不足, 请重新授权。");
        //将消息 json 化
        String json = JSONUtil.toJsonStr(result);
        //送到客户端
        response.getWriter().print(json);
    }
}

//自定义权限不足处理器后，需要进行注册，注册到 SecurityConfig 配置文件中

~~~

## 常用注解

![image-20251019134123872](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251019134123872.png)

`Spring Security`提供了`Spring EL`表达式，允许我们在定义接口访问的方法上面添加注解，来控制访问权限。

### 权限方法

`@PreAuthorize`注解用于配置接口要求用户拥有某些权限才可访问，它拥有如下方法

| 方法        | 参数   | 描述                                          |
| ----------- | ------ | --------------------------------------------- |
| hasPermi    | String | 验证用户是否具备某权限                        |
| lacksPermi  | String | 验证用户是否不具备某权限，与 hasPermi逻辑相反 |
| hasAnyPermi | String | 验证用户是否具有以下任意一个权限              |
| hasRole     | String | 判断用户是否拥有某个角色                      |
| lacksRole   | String | 验证用户是否不具备某角色，与 isRole逻辑相反   |
| hasAnyRoles | String | 验证用户是否具有以下任意一个角色，多个        |





> **基于配置自定义权限访问控制**

- ### `@PermitAll` 注解

- ### 配置文件

- ### 配置类





---

