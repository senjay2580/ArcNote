

Oauth2.0

redis 集群 缓存问题（

- 使用Jedis连接池
- 集群模式部署
- 6个节点负载均衡）

网络波动 可靠性？

RBAC 前后端如何协作 ？ ABAC？

sso

多端问题

分布式rpc框架 ？

每次请求都刷新Redis过期时间,会导致大量写操作

密码加密 密码学



# 架构全景图



```
┌─────────────────────────────────────────────────────────────┐
│                      前端应用层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Web前端    │  │  移动端App   │  │  第三方应用   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    API网关层（Zuul）                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  • 统一入口（8290端口）                                │ │
│  │  • 路由转发                                            │ │
│  │  • 跨域处理                                            │ │
│  │  • 日志记录                                            │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────┬──────────────────────┬──────────────────────────┘
           │                      │
           ▼                      ▼
┌──────────────────┐    ┌──────────────────┐
│   SSO服务        │    │  SysManage服务   │
│  (5001端口)      │◄───┤  (5000端口)      │
│                  │    │                  │
│  • 用户认证      │    │  • 用户管理      │
│  • Token管理     │    │  • 权限管理      │
│  • 会话管理      │    │  • 组织管理      │
│  • 权限加载      │    │  • 字典管理      │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │      Redis集群        │
         │  • 会话存储           │
         │  • 缓存管理           │
         │  • 分布式锁           │
         └───────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │    达梦数据库         │
         │  • 用户数据           │
         │  • 权限数据           │
         │  • 业务数据           │
         └───────────────────────┘

         ┌───────────────────────┐
         │    RPC框架（可选）     │
         │  • 服务注册           │
         │  • 服务发现           │
         │  • 远程调用           │
         └───────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │     Zookeeper         │
         │  • 服务注册中心       │
         └───────────────────────┘
```



# SystemManage

## **功能模块：**

~~~css
### 2.1 系统管理（sysmanage）

负责系统基础配置和权限管理：

#### 主要功能

- **用户管理** (`SysUserController`)
  - 用户增删改查
  - 用户状态管理（启用/禁用/锁定）
  - 用户密码管理
  - 用户权限分配

- **角色管理** (`SysRoleController`)
  - 角色定义与维护
  - 角色权限配置
  - 角色用户关联

- **部门管理** (`SysDeptController`)
  - 组织架构树形管理
  - 部门层级关系维护
  - 部门用户关联

- **菜单管理** (`SysModuleController`)
  - 菜单树形结构维护
  - 菜单权限配置
  - 按钮权限管理 (`SysModuleBtnController`)

- **字典管理** (`SysDictController`)
  - 系统字典维护
  - 字典项配置

- **日志管理**
  - 登录日志 (`SysLoginLogController`)
  - 操作日志 (`SysOperLogController`)
  - 异常日志 (`SysExceptionLogController`)
  - 应用日志 (`SysAppLogController`)

### 2.2 数字身份管理（digitalIdentityManagement）

与数字身份服务管理平台对接：

#### 主要功能

- **用户同步** (`SyncUserFromDigitalIdentityController`)
  - 从数字身份平台同步用户信息
  - 用户数据映射与转换
  - 定时同步任务 (`SyncDiDataTask`)

- **部门同步** (`SyncDeptFromDigitalIdentityService`)
  - 组织架构同步
  - 部门层级关系维护

- **加密工具** (`Sm4Utils`)
  - SM4国密算法支持
  - 数据加解密处理

### 2.3 信息发布管理（dismanage）

负责系统内信息发布与展示：

#### 主要功能

- **通知公告** (`DisNoticeController`)
  - 通知发布与管理
  - 通知阅读状态跟踪

- **新闻资讯** (`DisNewsController`)
  - 新闻发布管理
  - 新闻分类管理

- **问答管理** (`DisQaController`)
  - 常见问题维护
  - 问答分类管理

- **待办事项** (`DisTodoItemController`)
  - 待办任务管理
  - 任务状态跟踪

- **问题反馈** (`DisProblemFeedbackController`)
  - 用户问题收集
  - 问题处理跟踪

- **系统访问权限申请** (`DisSystemAccessRightsApplyController`)
  - 权限申请流程
  - 申请审批管理

### 2.4 邮件管理（email）

提供邮件收发功能：

#### 主要功能

- **邮件收发** (`MailController`)
  - 邮件发送
  - 草稿箱管理
  - 邮件附件处理

### 2.5 第三方集成

#### 闽政通集成（mzt/mztOauth2）

- **OAuth2认证** (`MztOauth2Controller`)
  - 闽政通OAuth2登录
  - 用户信息获取
  - Token管理

- **传统认证** (`MZTController`)
  - 闽政通传统登录方式
  - 回调处理

### 2.6 开放API（openapi）

对外提供API接口：

#### 主要功能

- **数据接收** (`DigitalIdentityServiceManagementPlatformDataReceiveController`)
  - 接收数字身份平台推送数据
  - 数据验证与处理

- **限流控制** (`LimiterController`)
  - API访问频率限制
  - 防刷机制

- **开放接口** (`SysOpenApiController`)
  - 对外开放的标准API
  - 接口鉴权
~~~



| 方案                      | 核心定位     | 触发时机                                 | 作用范围                                           |
| ------------------------- | ------------ | ---------------------------------------- | -------------------------------------------------- |
| 拦截器（后端）            | 被动兜底拦截 | 用户发起接口请求后，后端处理前           | 仅覆盖 “后端接口请求”（比如访问 `/svc/user/list`） |
| logincheckUrl（前端调用） | 主动提前校验 | 用户切换菜单 / 刷新页面 / 长时间无操作后 | 覆盖 “前端交互场景”（比如页面渲染前、菜单点击后）  |

系统必然会经历「开发环境 → 测试环境 → 生产环境」，不同环境的接口地址、Redis 地址等参数完全不同：

| 环境     | loginUrl 示例               | Redis 服务器示例             |
| -------- | --------------------------- | ---------------------------- |
| 开发环境 | http://127.0.0.1:8290/...   | 10.1.12.191:8379（内网测试） |
| 测试环境 | http://10.1.10.50:8290/...  | 10.1.20.88:8379（测试集群）  |
| 生产环境 | http://10.1.30.100:8290/... | 172.16.5.20:8379（生产集群） |

如果 URL 硬编码在代码里：

- 每次切换环境，都要修改代码中的 URL（比如把 `127.0.0.1` 改成 `10.1.30.100`）；
- 改完代码需要重新编译、打包、测试，极易出错（比如漏改某个 URL 导致生产环境调用开发接口）；
- 开发、测试、生产的代码版本会混在一起，难以管理。



**解耦**

preLoginUrl 是 UIPMP 门户登录流程的 “安全前置环节”，核心价值是：

- **安全兜底**：通过非对称加密、防重放参数，杜绝密码泄露、暴力破解等攻击；
- **体验优化**：提前校验账号有效性，减少用户无效操作；
- **逻辑解耦**：把登录前的预处理和核心登录逻辑分离，便于维护和扩展。





- **含义**：系统后台配置一个「定时任务」（比如每小时执行一次，或每天凌晨 2 点执行），自动触发身份同步流程，无需人工操作。
- **作用**：保证数据的 “定期更新”，避免门户数据和身份平台数据长期不一致（比如员工入职 / 离职 / 调岗后，门户能自动同步，不用管理员手动改）。

- 同步完成后，记录详细的同步日志到 UIPMP 数据库 / 日志文件，日志内容至少包含：

  - 同步时间、触发方式（定时任务）；
  - 拉取数据总量、成功同步量、失败量；
  - 失败原因（比如某用户解密失败、字段转换错误）；
  - 操作人（系统定时任务）。

  

  1. 审计合规：满足等保 “操作可追溯” 的要求，审计时能查看到每一次同步的详情；
  2. 问题排查：同步失败时，管理员可通过日志快速定位原因（比如 “用户 EMP002 解密失败，原因是 SM4 密钥不匹配”）；
  3. 数据对账：若发现 UIPMP 数据异常，可通过日志核对同步记录，确认是哪一次同步出了问题。



# SSO 模块

~~~css
sso/
├── nl-sso/                  # SSO核心模块
│   ├── nl-sso-core/        # SSO核心组件
│   ├── nl-sso-server/      # SSO服务端
│   └── nl-sso-demo/        # SSO示例
├── nl-rpc/                  # RPC框架（详见RPC模块文档）
└── nl-registry/             # 服务注册中心
~~~



## **功能模块**

~~~css
redis配置管理（conf）
会话存储（SsoLoginStore）
登录助手（SsoTokenLoginHelper）
工具类
- **JedisUtil**: Redis操作工具
- **StringUtils**: 字符串工具
- **Md5Utils**: MD5加密工具
~~~

## 请求优化

```
┌──────────────────────────────────────────┐
│          请求优化策略                     │
│                                          │
│  1. 接口合并                              │
│     - 减少HTTP请求次数                    │
│     - 一次性获取所需数据                  │
│                                          │
│  2. 数据压缩                              │
│     - Gzip压缩响应                       │
│     - 减少传输数据量                      │
│                                          │
│  3. 异步处理                              │
│     - 非关键业务异步执行                  │
│     - 提升响应速度                        │
│                                          │
│  4. 批量操作                              │
│     - 批量查询                            │
│     - 批量更新                            │
│     - 减少数据库交互                      │
└──────────────────────────────────────────┘
```

## 多层防护体系

```
┌──────────────────────────────────────────────────────┐
│                  安全防护层次                         │
│                                                      │
│  第一层：网关层（Zuul）                               │
│    ├─> CORS跨域控制                                  │
│    ├─> 请求日志记录                                  │
│    └─> 基础参数验证                                  │
│         │                                            │
│         ▼                                            │
│  第二层：认证层（SSO）                                │
│    ├─> Token验证                                     │
│    ├─> 会话管理                                      │
│    ├─> 账号锁定                                      │
│    └─> IP锁定                                        │
│         │                                            │
│         ▼                                            │
│  第三层：权限层（SysManage）                          │
│    ├─> 菜单权限验证                                  │
│    ├─> 按钮权限验证                                  │
│    ├─> 数据权限验证                                  │
│    └─> XSS防护                                       │
│         │                                            │
│         ▼                                            │
│  第四层：数据层                                       │
│    ├─> SQL注入防护                                   │
│    ├─> 数据加密（国密SM4）                           │
│    └─> 审计日志                                      │
└──────────────────────────────────────────────────────┘
```

## 日志体系

```
┌──────────────────────────────────────────┐
│            日志分类与用途                 │
│                                          │
│  访问日志 (Access Log)                   │
│    - 记录所有HTTP请求                     │
│    - 用于流量分析                        │
│                                          │
│  业务日志 (Business Log)                 │
│    - 记录关键业务操作                     │
│    - 用于业务审计                        │
│                                          │
│  错误日志 (Error Log)                    │
│    - 记录系统异常                        │
│    - 用于问题排查                        │
│                                          │
│  性能日志 (Performance Log)              │
│    - 记录接口耗时                        │
│    - 用于性能优化                        │
│                                          │
│  安全日志 (Security Log)                 │
│    - 记录安全事件                        │
│    - 用于安全审计                        │
└──────────────────────────────────────────┘
```

## 多端管控

| 管控模式             | 适用场景                 | 核心逻辑                                                |
| -------------------- | ------------------------ | ------------------------------------------------------- |
| 单端独占登录（默认） | 企业内网门户、高安全场景 | 同一账号新渠道登录→自动踢掉所有旧渠道登录态             |
| 多端允许登录         | 普通办公场景             | 同一账号可在 PC + 小程序 + APP 同时登录，各端登录态独立 |
| 精准踢下线           | 安全管控场景             | 管理员可指定 “某设备 / 某渠道” 踢下线，不影响其他端     |



# UIPMP-Zuul 模块

## 功能模块

~~~css
路由配置
请求过滤
闽政通集成
日志审计
~~~







# Oauth2.0具体

~~~mermaid
sequenceDiagram
    participant U as 用户浏览器
    participant F as 农业云前端
    participant B as 农业云后端
    participant R as Redis
    participant M as 闽政通OAuth2平台

    %% 1. 访问首页 & 检测未登录
    U->>F: 1. 访问首页
    F-->>U: 2. 检测未登录（无token）

    %% 2. 构造授权URL
    U->>F: 3. 请求授权URL
    F->>B: POST /mzt/oauth2/authorize-url
    B-->>F: 4. 构造授权URL<br/>返回：https://iam.e-govt.cn:8901/login?<br/>response_type=code&appId=xxx&<br/>redirect_uri=http://xxx/cwb/index.html&<br/>state=xxx
    F->>U: 返回授权URL

    %% 3. 闽政通登录授权
    U->>M: 5. 重定向到闽政通登录页
    M-->>U: 6. 显示登录页面
    U->>M: 7. 用户输入账号密码
    M-->>U: 8. 验证成功，返回授权码<br/>重定向：http://xxx/cwb/index.html?code=AUTH_CODE&state=xxx

    %% 4. 授权码换Token流程
    U->>F: 9. 携带code回调前端
    F->>B: 10. 用code换token<br/>POST /mzt/oauth2/login {code, userType}
    
    %% 4.1 获取App Token并缓存
    B->>M: 11. 获取App Token<br/>POST /outside/oauth2/getAppToken<br/>{appId, appSecret}+SM3签名+一体化签名
    M-->>B: 12. 返回App Token {app_token, expires_in}
    B->>R: 13. 缓存App Token<br/>SET app-token
    R-->>B: 缓存成功

    %% 4.2 用code换Access Token
    B->>M: 14. 用code换Access Token<br/>POST /outside/oauth2/token<br/>Header: App-Token
    M-->>B: 15. 返回Access Token {access_token, refresh_token, expires_in}

    %% 4.3 获取并解密用户信息
    B->>M: 16. 获取用户信息<br/>GET /outside/oauth2/getUserInfo<br/>Header: Authorization=access_token
    M-->>B: 17. 返回加密的用户信息 {userInfoStr: "AES加密数据"}
    B-->>B: 18. AES解密用户信息（姓名/身份证/手机号等）

    %% 4.4 生成本地Token并缓存会话
    B-->>B: 19. 生成本地Token<br/>token = "mzt-oauth2-" + SHA256(userId+access_token)
    B->>R: 20. 存储会话到Redis<br/>SET 10000:SSO:ENV_SSO_{token} {用户信息}<br/>TTL: 1800秒
    R-->>B: 存储成功

    %% 5. 返回Token并验证
    B-->>F: 21. 返回本地Token {status:200, data:token}
    F->>U: 22. 重定向带token<br/>index.html?token=xxx
    
    U->>F: 23. 验证token
    F->>B: POST /mzt/valid
    B->>R: 24. 从Redis获取用户信息<br/>GET ENV_SSO_xxx
    R-->>B: 返回用户信息
    B-->>F: 25. 返回用户信息
    F-->>U: 26. 登录成功，显示用户名

    note over U,M: 核心流程：OAuth2.0授权码模式 + 本地会话管理
~~~





~~~mermaid
flowchart LR
    RO[Resource Owner<br/>资源所有者/用户]
    Client[Client<br/>客户端应用]
    AS[Authorization Server<br/>授权服务器]
    RS[Resource Server<br/>资源服务器]
    
    RO -- 授权 --> Client
    Client -- 请求授权码/令牌 --> AS
    AS -- 认证用户+颁发令牌 --> Client
    Client -- 携带令牌请求资源 --> RS
    RS -- 验证令牌+返回资源 --> Client
    
    style RO fill:#e8f4f8,stroke:#2196f3,stroke-width:2px
    style Client fill:#f3e5f5,stroke:#9c27b0,stroke-width
~~~



---



~~~mermaid
sequenceDiagram
    participant RO as 用户浏览器<br/>(Resource Owner)
    participant Client as 客户端应用<br/>(Client)
    participant AS as 授权服务器<br/>(Authorization Server)
    participant RS as 资源服务器<br/>(Resource Server)

    %% ========== 第一步：初始访问应用 & 重定向授权 ==========
    RO->>Client: 1.访问应用
    Note over Client: 2.检测未授权<br/>需要用户授权
    Client->>RO: 3.重定向到授权页面<br/>(带上client_id, redirect_uri,<br/>scope, state)
    RO->>AS: 4.请求授权页面<br/>GET /authorize?<br/>  response_type=code&<br/>  client_id=CLIENT_ID&<br/>  redirect_uri=CALLBACK_URL&<br/>  scope=read_user&<br/>  state=RANDOM_STRING
    AS->>RO: 5.显示登录页面<br/>(要求用户输入账号密码)
    RO->>AS: 6.用户输入账号密码<br/>POST /login<br/>  username=user@example.com<br/>  password=******
    Note over AS: 7.验证用户身份<br/>(查询数据库)
    AS->>RO: 8.显示授权确认页面<br/>"某应用想要访问你的：<br/> ☑ 基本信息 ☑ 头像<br/> [同意] [拒绝]"
    RO->>AS: 9.用户点击"同意"<br/>POST /authorize/confirm
    Note over AS: 10.生成授权码<br/>code=AUTH_CODE<br/>(有效期10分钟)
    AS->>RO: 11.重定向回客户端<br/>(带上授权码)<br/>302 Redirect<br/>Location: CALLBACK_URL?<br/>  code=AUTH_CODE&<br/>  state=RANDOM_STRING

    %% ========== 第二步：授权码换 Access Token ==========
    RO->>Client: 12.访问回调地址<br/>GET /callback?<br/>  code=AUTH_CODE&<br/>  state=xxx
    Note over Client: 13.验证state<br/>(防CSRF攻击)
    Client->>AS: 14.用授权码换取访问令牌<br/>POST /token<br/>  grant_type=authorization_code<br/>  code=AUTH_CODE<br/>  client_id=CLIENT_ID<br/>  client_secret=CLIENT_SECRET<br/>  redirect_uri=CALLBACK_URL
    Note over AS: 15.验证授权码<br/>- 检查code是否有效<br/>- 检查client_id和secret<br/>- 检查redirect_uri是否匹配
    Note over AS: 16.生成访问令牌<br/>access_token (2小时有效)<br/>refresh_token (30天有效)
    AS->>Client: 17.返回令牌<br/>{<br/>  "access_token": "ACCESS_TOKEN",<br/>  "token_type": "Bearer",<br/>  "expires_in": 7200,<br/>  "refresh_token": "REFRESH_TOKEN",<br/>  "scope": "read_user"<br/>}
    Note over Client: 18.存储令牌<br/>(Session/DB)
    Client->>RO: 19.登录成功<br/>显示用户信息

    %% ========== 第三步：使用 Access Token 访问资源 ==========
    RO->>Client: 20.访问需要授权的功能
    Client->>RS: 21.使用访问令牌获取用户资源<br/>GET /api/user<br/>Authorization: Bearer ACCESS_TOKEN
    Note over RS: 22.验证令牌<br/>- 检查签名<br/>- 检查过期时间<br/>- 检查权限范围
    RS->>Client: 23.返回用户资源<br/>{<br/>  "id": "123",<br/>  "name": "张三",<br/>  "avatar": "http://..."<br/>}
    Client->>RO: 24.展示用户数据

    %% ========== 第四步：Refresh Token 刷新令牌 ==========
    Note over Client: 1.access_token过期
    Client->>AS: 2.使用refresh_token刷新<br/>POST /token<br/>  grant_type=refresh_token<br/>  refresh_token=REFRESH_TOKEN<br/>  client_id=CLIENT_ID<br/>  client_secret=CLIENT_SECRET
    Note over AS: 3.验证refresh_token
    AS->>Client: 4.返回新的令牌<br/>{<br/>  "access_token": "NEW_ACCESS_TOKEN",<br/>  "expires_in": 7200,<br/>  "refresh_token": "NEW_REFRESH_TOKEN"<br/>}
~~~

