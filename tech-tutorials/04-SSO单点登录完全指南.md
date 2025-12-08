# SSO 单点登录完全指南

## 一、为什么需要 SSO？

### 1.1 核心问题

**业务痛点：**
- **多次登录困扰**：用户需要在多个系统中重复登录
- **账号管理混乱**：每个系统维护独立的用户账号
- **安全风险**：密码分散存储，增加泄露风险
- **用户体验差**：频繁输入用户名密码
- **维护成本高**：多套用户系统难以统一管理

**实际场景举例：**

**场景1：企业内部系统**
```
问题：公司有10个内部系统
- OA办公系统
- HR人事系统
- 财务管理系统
- 项目管理系统
- 客户关系系统
- ...

传统方式：
- 员工需要记住10套用户名密码
- 每天上班需要登录10次
- 修改密码需要改10个系统
- 员工离职需要在10个系统中删除账号

用户抱怨：太麻烦了！
```

**场景2：互联网产品矩阵**
```
问题：公司有多个产品
- 主站（www.example.com）
- 商城（mall.example.com）
- 社区（bbs.example.com）
- 移动APP

需求：
- 用户在主站登录后，访问商城无需再次登录
- 用户在APP登录后，打开网页版自动登录
- 用户在任一端退出，所有端同步退出
```

**场景3：多端统一登录**
```
问题：用户使用多种设备
- PC网页端
- 移动网页端
- iOS APP
- Android APP
- 小程序

需求：一次登录，全端通用
```

### 1.2 解决方案

**SSO（Single Sign-On）单点登录**

```
核心思想：
用户只需登录一次，即可访问所有相互信任的应用系统

┌─────────────────────────────────────┐
│         SSO 认证中心                 │
│    (统一认证、统一授权)              │
└─────────────┬───────────────────────┘
              │
      ┌───────┼───────┬───────┐
      │       │       │       │
   系统A    系统B   系统C   系统D
```

---

## 二、SSO 实现方案

### 2.1 CAS 协议

**CAS（Central Authentication Service）中央认证服务**

**核心流程：**
```
1. 用户访问系统A
2. 系统A检查是否已登录
3. 未登录，重定向到CAS认证中心
4. 用户在CAS输入用户名密码
5. CAS验证成功，生成TGT（Ticket Granting Ticket）
6. CAS重定向回系统A，携带ST（Service Ticket）
7. 系统A拿ST到CAS验证
8. 验证成功，系统A创建本地会话
9. 用户访问系统B
10. 系统B检查是否已登录
11. 未登录，重定向到CAS
12. CAS检查到TGT存在，直接生成ST
13. 重定向回系统B，携带ST
14. 系统B验证ST，创建本地会话
15. 完成单点登录
```

**时序图：**
```
用户      系统A      CAS中心      系统B
 │         │          │           │
 ├─访问───→│          │           │
 │         ├─未登录──→│           │
 │         │          │           │
 │←────────┴─重定向───┤           │
 │                    │           │
 ├─输入用户名密码────→│           │
 │                    │           │
 │←─────重定向+ST─────┤           │
 │         │          │           │
 ├─访问+ST→│          │           │
 │         ├─验证ST──→│           │
 │         │←─验证通过┤           │
 │         │          │           │
 │←─登录成功┤          │           │
 │         │          │           │
 ├─访问─────┴─────────┴──────────→│
 │                                │
 │←──────────重定向+ST────────────┤
 │                    │           │
 │                    ├─验证ST───→│
 │                    │←─验证通过─┤
 │                                │
 │←─────────登录成功──────────────┤
```

### 2.2 JWT 方案

**JWT（JSON Web Token）**

**核心流程：**
```
1. 用户登录认证中心
2. 认证成功，生成JWT Token
3. 返回JWT给客户端
4. 客户端访问系统A，携带JWT
5. 系统A验证JWT签名
6. 验证成功，允许访问
7. 客户端访问系统B，携带同一个JWT
8. 系统B验证JWT签名
9. 验证成功，允许访问
```

**JWT 结构：**
```
Header.Payload.Signature

Header（头部）：
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload（载荷）：
{
  "userId": 1001,
  "username": "zhangsan",
  "exp": 1735689600
}

Signature（签名）：
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

**Java 实现：**
```java
import io.jsonwebtoken.*;
import java.util.Date;

@Service
public class JwtService {
    
    private static final String SECRET_KEY = "your-secret-key-min-256-bits";
    private static final long EXPIRATION_TIME = 86400000;
    
    public String generateToken(Long userId, String username) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + EXPIRATION_TIME);
        
        return Jwts.builder()
            .setSubject(userId.toString())
            .claim("username", username)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
            .compact();
    }
    
    public Claims parseToken(String token) {
        try {
            return Jwts.parser()
                .setSigningKey(SECRET_KEY)
                .parseClaimsJws(token)
                .getBody();
        } catch (ExpiredJwtException e) {
            throw new TokenExpiredException("Token已过期");
        } catch (JwtException e) {
            throw new InvalidTokenException("无效的Token");
        }
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(SECRET_KEY).parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
    
    public Long getUserIdFromToken(String token) {
        Claims claims = parseToken(token);
        return Long.parseLong(claims.getSubject());
    }
}

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    
    @Autowired
    private JwtService jwtService;
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/login")
    public Result<LoginVO> login(@RequestBody LoginDTO dto) {
        User user = userService.authenticate(dto.getUsername(), dto.getPassword());
        
        if (user == null) {
            return Result.error("用户名或密码错误");
        }
        
        String token = jwtService.generateToken(user.getUserId(), user.getUsername());
        
        LoginVO vo = new LoginVO();
        vo.setToken(token);
        vo.setUserInfo(user);
        
        return Result.success(vo);
    }
    
    @GetMapping("/verify")
    public Result<UserVO> verifyToken(@RequestHeader("Authorization") String token) {
        if (token.startsWith("Bearer ")) {
            token = token.substring(7);
        }
        
        if (!jwtService.validateToken(token)) {
            return Result.error("Token无效");
        }
        
        Long userId = jwtService.getUserIdFromToken(token);
        User user = userService.getById(userId);
        
        return Result.success(new UserVO(user));
    }
}
```

### 2.3 OAuth 2.0 方案

**适用场景：第三方应用授权**

**授权码模式流程：**
```
1. 用户访问客户端应用
2. 客户端重定向到授权服务器
3. 用户登录并授权
4. 授权服务器返回授权码
5. 客户端用授权码换取Access Token
6. 客户端用Access Token访问资源服务器
```

**Spring Security OAuth2 实现：**
```java
@Configuration
@EnableAuthorizationServer
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {
    
    @Autowired
    private AuthenticationManager authenticationManager;
    
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
            .withClient("client-app")
            .secret("{noop}secret")
            .authorizedGrantTypes("authorization_code", "refresh_token")
            .scopes("read", "write")
            .redirectUris("http://localhost:8081/callback");
    }
    
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }
}
```

---

## 三、多端统一登录实现

### 3.1 多端登录架构

**架构设计：**
```
┌─────────────────────────────────────┐
│         SSO 认证中心                 │
│    - 用户认证                        │
│    - Token 生成                      │
│    - Token 验证                      │
└─────────────┬───────────────────────┘
              │
      ┌───────┼───────┬───────┬───────┐
      │       │       │       │       │
   PC Web  Mobile  iOS APP Android  小程序
```

### 3.2 Token 管理策略

**多设备Token管理：**
```java
@Service
public class MultiDeviceTokenService {
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    private static final String TOKEN_PREFIX = "token:user:";
    private static final long TOKEN_EXPIRE_SECONDS = 86400 * 7;
    
    public String generateToken(Long userId, String deviceType, String deviceId) {
        String token = UUID.randomUUID().toString().replace("-", "");
        
        String key = TOKEN_PREFIX + userId;
        
        Map<String, Object> tokenInfo = new HashMap<>();
        tokenInfo.put("token", token);
        tokenInfo.put("deviceType", deviceType);
        tokenInfo.put("deviceId", deviceId);
        tokenInfo.put("createTime", System.currentTimeMillis());
        
        redisTemplate.opsForHash().put(key, deviceType + ":" + deviceId, tokenInfo);
        redisTemplate.expire(key, TOKEN_EXPIRE_SECONDS, TimeUnit.SECONDS);
        
        redisTemplate.opsForValue().set("token:" + token, userId, TOKEN_EXPIRE_SECONDS, TimeUnit.SECONDS);
        
        return token;
    }
    
    public Long getUserIdByToken(String token) {
        return (Long) redisTemplate.opsForValue().get("token:" + token);
    }
    
    public List<Map<String, Object>> getUserDevices(Long userId) {
        String key = TOKEN_PREFIX + userId;
        Map<Object, Object> devices = redisTemplate.opsForHash().entries(key);
        
        return devices.values().stream()
            .map(obj -> (Map<String, Object>) obj)
            .collect(Collectors.toList());
    }
    
    public void logout(String token) {
        Long userId = getUserIdByToken(token);
        
        if (userId != null) {
            redisTemplate.delete("token:" + token);
        }
    }
    
    public void logoutAllDevices(Long userId) {
        String key = TOKEN_PREFIX + userId;
        Map<Object, Object> devices = redisTemplate.opsForHash().entries(key);
        
        for (Object value : devices.values()) {
            Map<String, Object> tokenInfo = (Map<String, Object>) value;
            String token = (String) tokenInfo.get("token");
            redisTemplate.delete("token:" + token);
        }
        
        redisTemplate.delete(key);
    }
    
    public void logoutDevice(Long userId, String deviceType, String deviceId) {
        String key = TOKEN_PREFIX + userId;
        String field = deviceType + ":" + deviceId;
        
        Map<String, Object> tokenInfo = (Map<String, Object>) 
            redisTemplate.opsForHash().get(key, field);
        
        if (tokenInfo != null) {
            String token = (String) tokenInfo.get("token");
            redisTemplate.delete("token:" + token);
            redisTemplate.opsForHash().delete(key, field);
        }
    }
}

@RestController
@RequestMapping("/api/auth")
public class MultiDeviceAuthController {
    
    @Autowired
    private MultiDeviceTokenService tokenService;
    
    @PostMapping("/login")
    public Result<LoginVO> login(@RequestBody LoginDTO dto,
                                 @RequestHeader("Device-Type") String deviceType,
                                 @RequestHeader("Device-Id") String deviceId) {
        
        User user = userService.authenticate(dto.getUsername(), dto.getPassword());
        
        if (user == null) {
            return Result.error("用户名或密码错误");
        }
        
        String token = tokenService.generateToken(user.getUserId(), deviceType, deviceId);
        
        LoginVO vo = new LoginVO();
        vo.setToken(token);
        vo.setUserInfo(user);
        
        return Result.success(vo);
    }
    
    @GetMapping("/devices")
    public Result<List<DeviceVO>> getDevices() {
        Long userId = SecurityUtils.getCurrentUserId();
        List<Map<String, Object>> devices = tokenService.getUserDevices(userId);
        
        List<DeviceVO> deviceVOs = devices.stream()
            .map(device -> {
                DeviceVO vo = new DeviceVO();
                vo.setDeviceType((String) device.get("deviceType"));
                vo.setDeviceId((String) device.get("deviceId"));
                vo.setCreateTime((Long) device.get("createTime"));
                return vo;
            })
            .collect(Collectors.toList());
        
        return Result.success(deviceVOs);
    }
    
    @PostMapping("/logout")
    public Result<Void> logout(@RequestHeader("Authorization") String token) {
        if (token.startsWith("Bearer ")) {
            token = token.substring(7);
        }
        
        tokenService.logout(token);
        
        return Result.success();
    }
    
    @PostMapping("/logout/all")
    public Result<Void> logoutAll() {
        Long userId = SecurityUtils.getCurrentUserId();
        tokenService.logoutAllDevices(userId);
        
        return Result.success();
    }
    
    @PostMapping("/logout/device")
    public Result<Void> logoutDevice(@RequestBody LogoutDeviceDTO dto) {
        Long userId = SecurityUtils.getCurrentUserId();
        tokenService.logoutDevice(userId, dto.getDeviceType(), dto.getDeviceId());
        
        return Result.success();
    }
}
```

### 3.3 前端集成

**Web端（Vue3）：**
```typescript
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const api = axios.create({
  baseURL: 'https://sso.example.com/api'
})

api.interceptors.request.use(config => {
  const userStore = useUserStore()
  
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  
  config.headers['Device-Type'] = 'web'
  config.headers['Device-Id'] = getDeviceId()
  
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

function getDeviceId() {
  let deviceId = localStorage.getItem('deviceId')
  
  if (!deviceId) {
    deviceId = generateUUID()
    localStorage.setItem('deviceId', deviceId)
  }
  
  return deviceId
}

export default api
```

**移动端（React Native）：**
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage'
import DeviceInfo from 'react-native-device-info'

class AuthService {
  async login(username, password) {
    const deviceId = await DeviceInfo.getUniqueId()
    const deviceType = Platform.OS
    
    const response = await fetch('https://sso.example.com/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Device-Type': deviceType,
        'Device-Id': deviceId
      },
      body: JSON.stringify({ username, password })
    })
    
    const data = await response.json()
    
    if (data.code === 200) {
      await AsyncStorage.setItem('token', data.data.token)
      await AsyncStorage.setItem('userInfo', JSON.stringify(data.data.userInfo))
    }
    
    return data
  }
  
  async logout() {
    const token = await AsyncStorage.getItem('token')
    
    await fetch('https://sso.example.com/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    await AsyncStorage.removeItem('token')
    await AsyncStorage.removeItem('userInfo')
  }
}

export default new AuthService()
```

---

## 四、常见问题与解决方案

### 4.1 跨域问题

**问题：** SSO认证中心与业务系统不同域，Cookie无法共享

**解决方案1：CORS + withCredentials**
```java
@Configuration
public class CorsConfig {
    
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.addAllowedOriginPattern("*");
        config.setAllowCredentials(true);
        config.addAllowedHeader("*");
        config.addAllowedMethod("*");
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        
        return new CorsFilter(source);
    }
}
```

**解决方案2：使用Token代替Cookie**
```
前端将Token存储在localStorage
每次请求在Header中携带Token
```

### 4.2 Token刷新

**问题：** Token过期后用户需要重新登录

**解决方案：Refresh Token机制**
```java
@Service
public class TokenRefreshService {
    
    public TokenPair generateTokenPair(Long userId) {
        String accessToken = generateAccessToken(userId);
        String refreshToken = generateRefreshToken(userId);
        
        redisTemplate.opsForValue().set(
            "refresh:" + refreshToken,
            userId,
            30,
            TimeUnit.DAYS
        );
        
        return new TokenPair(accessToken, refreshToken);
    }
    
    public String refreshAccessToken(String refreshToken) {
        Long userId = (Long) redisTemplate.opsForValue().get("refresh:" + refreshToken);
        
        if (userId == null) {
            throw new TokenExpiredException("Refresh Token已过期");
        }
        
        return generateAccessToken(userId);
    }
}
```

### 4.3 单点退出

**问题：** 用户在一个系统退出，其他系统仍然登录

**解决方案：**
```java
@Service
public class SsoLogoutService {
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    public void logout(String token) {
        Long userId = getUserIdByToken(token);
        
        redisTemplate.delete("token:" + token);
        
        Set<String> allTokens = (Set<String>) redisTemplate.opsForSet().members("user:tokens:" + userId);
        
        if (allTokens != null) {
            for (String t : allTokens) {
                redisTemplate.delete("token:" + t);
            }
            
            redisTemplate.delete("user:tokens:" + userId);
        }
    }
}
```

---

## 五、最佳实践

### 5.1 设计准则

1. **Token安全**：使用HTTPS传输，Token加密存储
2. **过期策略**：Access Token短期，Refresh Token长期
3. **设备管理**：支持查看和管理登录设备
4. **单点退出**：一处退出，全部退出

### 5.2 注意事项

**设计风险：**
- Token泄露风险
- 跨域Cookie问题
- Token过期处理不当

**解决方案：**
- 使用HTTPS + Token加密
- 使用Token代替Cookie
- 实现Refresh Token机制

---

## 六、核心总结

### 核心问题
用户需要在多个系统中重复登录，账号管理混乱，用户体验差。

### 方案解析
通过 **SSO 单点登录**，实现一次登录，全系统通用：
- 统一认证中心
- Token统一管理
- 多端设备支持

### 关键补充

**最佳实践：**
- 使用JWT或CAS协议
- 实现多设备Token管理
- 支持Token刷新机制

**注意事项：**
- 处理跨域问题
- Token安全传输
- 实现单点退出

**扩展方向：**
- 集成OAuth2.0第三方登录
- 实现扫码登录
- 支持生物识别登录
