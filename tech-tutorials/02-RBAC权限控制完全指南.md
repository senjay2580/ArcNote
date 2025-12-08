# RBAC 权限控制完全指南

## 一、为什么需要 RBAC？

### 1.1 核心问题

**业务痛点：**
- 权限管理混乱：每个用户单独配置权限，维护成本极高
- 安全风险：权限分配不规范，容易出现越权访问
- 扩展性差：新增功能需要逐个用户配置权限

**实际场景：**
```
企业管理系统：500名员工，每人权限不同
- 新员工入职：需要配置50+项权限
- 员工调岗：需要重新配置所有权限
- 员工离职：需要逐项撤销权限
维护成本：极高，容易出错
```

### 1.2 解决方案

**RBAC（Role-Based Access Control）基于角色的访问控制**

```
用户（User）→ 角色（Role）→ 权限（Permission）→ 资源（Resource）

示例：张三（用户）→ 财务经理（角色）→ 查看财务报表（权限）
```

---

## 二、RBAC 模型详解

### 2.1 数据库设计

```sql
CREATE TABLE sys_user (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    real_name VARCHAR(50),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sys_role (
    role_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    status TINYINT DEFAULT 1
);

CREATE TABLE sys_permission (
    permission_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    permission_name VARCHAR(50) NOT NULL,
    permission_code VARCHAR(100) NOT NULL UNIQUE,
    resource_type VARCHAR(20) COMMENT 'menu/button/api',
    resource_path VARCHAR(200),
    parent_id BIGINT DEFAULT 0
);

CREATE TABLE sys_user_role (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    UNIQUE KEY uk_user_role (user_id, role_id)
);

CREATE TABLE sys_role_permission (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    UNIQUE KEY uk_role_permission (role_id, permission_id)
);
```

### 2.2 后端实现

**权限服务：**
```java
@Service
public class PermissionService {
    
    @Autowired
    private UserMapper userMapper;
    
    public Set<String> getUserPermissions(Long userId) {
        List<Role> roles = userMapper.selectRolesByUserId(userId);
        
        Set<String> permissions = new HashSet<>();
        for (Role role : roles) {
            List<Permission> rolePermissions = roleMapper.selectPermissionsByRoleId(role.getRoleId());
            permissions.addAll(
                rolePermissions.stream()
                    .map(Permission::getPermissionCode)
                    .collect(Collectors.toSet())
            );
        }
        
        return permissions;
    }
    
    public boolean hasPermission(Long userId, String permissionCode) {
        Set<String> permissions = getUserPermissions(userId);
        return permissions.contains(permissionCode);
    }
}
```

**注解式权限控制：**
```java
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface RequirePermission {
    String[] value();
}

@Aspect
@Component
public class PermissionAspect {
    
    @Autowired
    private PermissionService permissionService;
    
    @Around("@annotation(requirePermission)")
    public Object checkPermission(ProceedingJoinPoint joinPoint, 
                                 RequirePermission requirePermission) throws Throwable {
        
        Long userId = getCurrentUserId();
        String[] requiredPermissions = requirePermission.value();
        
        boolean hasPermission = Arrays.stream(requiredPermissions)
            .anyMatch(perm -> permissionService.hasPermission(userId, perm));
        
        if (!hasPermission) {
            throw new PermissionDeniedException("无权限访问");
        }
        
        return joinPoint.proceed();
    }
}

@RestController
@RequestMapping("/api/user")
public class UserController {
    
    @GetMapping("/list")
    @RequirePermission("user:view")
    public Result<List<User>> list() {
        return Result.success(userService.list());
    }
    
    @PostMapping("/add")
    @RequirePermission("user:add")
    public Result<Void> add(@RequestBody User user) {
        userService.save(user);
        return Result.success();
    }
}
```

### 2.3 前端实现

**权限指令（Vue3）：**
```typescript
import { Directive } from 'vue'
import { useUserStore } from '@/stores/user'

export const permission: Directive = {
  mounted(el: HTMLElement, binding) {
    const { value } = binding
    const userStore = useUserStore()
    const permissions = userStore.permissions
    
    if (value && value instanceof Array) {
      const hasPermission = value.some(permission => 
        permissions.includes(permission)
      )
      
      if (!hasPermission) {
        el.parentNode?.removeChild(el)
      }
    }
  }
}
```

**使用示例：**
```vue
<template>
  <el-button v-permission="['user:add']" @click="handleAdd">
    新增用户
  </el-button>
  
  <el-button v-permission="['user:delete']" type="danger" @click="handleDelete">
    删除
  </el-button>
</template>
```

**路由守卫：**
```typescript
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth) {
    if (!userStore.token) {
      next('/login')
      return
    }
    
    if (to.meta.permissions) {
      const hasPermission = userStore.hasAnyPermission(to.meta.permissions)
      
      if (!hasPermission) {
        next('/403')
        return
      }
    }
  }
  
  next()
})
```

---

## 三、前后端协作流程

**完整流程：**
```
1. 用户登录
   前端 → POST /api/login → 后端返回Token

2. 获取用户信息和权限
   前端 → GET /api/user/info → 后端返回权限列表

3. 获取用户菜单
   前端 → GET /api/user/menus → 后端返回菜单树

4. 前端权限控制
   - 路由守卫：检查页面访问权限
   - 指令控制：隐藏无权限按钮
   - 菜单渲染：只显示有权限的菜单

5. 后端权限验证
   - 拦截器：验证API访问权限
   - 注解：方法级权限控制
```

**API 设计：**
```java
@RestController
@RequestMapping("/api")
public class AuthController {
    
    @PostMapping("/login")
    public Result<LoginVO> login(@RequestBody LoginDTO dto) {
        String token = authService.login(dto.getUsername(), dto.getPassword());
        return Result.success(new LoginVO(token));
    }
    
    @GetMapping("/user/info")
    public Result<UserInfoVO> getUserInfo() {
        Long userId = SecurityUtils.getCurrentUserId();
        UserInfoVO vo = new UserInfoVO();
        vo.setUserInfo(userService.getById(userId));
        vo.setPermissions(permissionService.getUserPermissions(userId));
        return Result.success(vo);
    }
    
    @GetMapping("/user/menus")
    public Result<List<MenuVO>> getUserMenus() {
        Long userId = SecurityUtils.getCurrentUserId();
        List<MenuVO> menus = permissionService.getUserMenus(userId);
        return Result.success(menus);
    }
}
```

---

## 四、常见问题与解决方案

### 4.1 权限缓存问题

**问题：** 修改用户权限后，需要重新登录才能生效

**解决方案：**
```java
@Service
public class PermissionCacheService {
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    public Set<String> getUserPermissions(Long userId) {
        String key = "permission:user:" + userId;
        Set<String> permissions = (Set<String>) redisTemplate.opsForValue().get(key);
        
        if (permissions == null) {
            permissions = permissionService.getUserPermissions(userId);
            redisTemplate.opsForValue().set(key, permissions, 3600, TimeUnit.SECONDS);
        }
        
        return permissions;
    }
    
    public void refreshUserPermissions(Long userId) {
        String key = "permission:user:" + userId;
        redisTemplate.delete(key);
    }
}
```

### 4.2 数据权限问题

**问题：** 用户只能查看自己部门的数据

**解决方案：**
```java
@Aspect
@Component
public class DataScopeAspect {
    
    @Around("@annotation(dataScope)")
    public Object dataScope(ProceedingJoinPoint joinPoint, DataScope dataScope) throws Throwable {
        Long userId = SecurityUtils.getCurrentUserId();
        User user = userService.getById(userId);
        
        String scope = user.getDataScope();
        
        if ("dept".equals(scope)) {
            String sql = " AND dept_id = " + user.getDeptId();
            DataScopeContext.set(sql);
        } else if ("self".equals(scope)) {
            String sql = " AND create_user_id = " + userId;
            DataScopeContext.set(sql);
        }
        
        try {
            return joinPoint.proceed();
        } finally {
            DataScopeContext.remove();
        }
    }
}
```

---

## 五、最佳实践

### 5.1 设计准则

1. **最小权限原则**：用户只拥有完成工作所需的最小权限
2. **职责分离**：关键操作需要多个角色协作
3. **权限分层**：菜单权限、按钮权限、数据权限分层管理
4. **定期审计**：定期检查用户权限是否合理

### 5.2 注意事项

**设计风险：**
- 角色爆炸：角色过多难以管理
- 权限粒度：过细影响性能，过粗不够灵活
- 缓存一致性：权限修改后缓存未及时更新

**解决方案：**
- 合理规划角色层次
- 根据业务场景确定权限粒度
- 实现缓存刷新机制

### 5.3 其他方案

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| RBAC | 简单易用，易于管理 | 灵活性不足 | 通用企业系统 |
| ABAC | 灵活性高，支持复杂规则 | 实现复杂 | 复杂权限场景 |
| ACL | 精确控制 | 维护成本高 | 小规模系统 |

---

## 六、核心总结

### 核心问题
传统的用户直接分配权限方式维护成本高、扩展性差、容易出错。

### 方案解析
通过 **RBAC 模型**，在用户和权限之间引入角色层，实现：
- 用户通过角色获得权限
- 批量管理用户权限
- 降低维护成本

### 关键补充

**最佳实践：**
- 合理规划角色体系
- 实现多级缓存提升性能
- 前后端双重权限验证

**注意事项：**
- 避免角色爆炸问题
- 处理权限缓存一致性
- 实现数据权限控制

**扩展方向：**
- 结合ABAC实现更灵活的权限控制
- 实现动态权限配置
- 集成SSO单点登录
