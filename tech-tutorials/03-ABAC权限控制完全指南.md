# ABAC 权限控制完全指南

## 一、为什么需要 ABAC？

### 1.1 核心问题

**RBAC 的局限性：**
- **灵活性不足**：无法表达复杂的权限规则
- **角色爆炸**：需要为每种权限组合创建角色
- **动态场景支持差**：难以处理时间、地点等动态条件
- **细粒度控制困难**：难以实现基于资源属性的权限控制

**实际场景举例：**

**场景1：文档管理系统**
```
需求：
- 文档创建者可以编辑和删除
- 同部门员工可以查看
- 工作日 9:00-18:00 可以下载
- 机密文档只能在公司IP访问

RBAC 实现：需要创建大量角色组合
- 文档创建者_工作时间_公司网络
- 同部门员工_工作时间_公司网络
- ...（角色爆炸）

ABAC 实现：基于属性规则
- IF user.id == document.creator THEN allow edit
- IF user.dept == document.dept THEN allow view
- IF time in 9:00-18:00 AND day in weekdays THEN allow download
- IF document.level == "secret" AND ip in company_ips THEN allow access
```

**场景2：医疗系统**
```
需求：
- 主治医生可以查看和修改患者病历
- 会诊医生只能在会诊期间查看
- 护士只能查看所在科室患者病历
- 患者本人可以查看自己的病历

RBAC 困境：角色无法表达这些复杂关系
ABAC 优势：基于属性动态判断权限
```

**场景3：金融系统**
```
需求：
- 交易金额 < 1万：普通员工审批
- 交易金额 1-10万：主管审批
- 交易金额 > 10万：总监审批
- 异常交易：需要风控部门审批

RBAC 困境：无法基于交易金额动态判断
ABAC 优势：基于资源属性（金额）动态授权
```

### 1.2 解决方案

**ABAC（Attribute-Based Access Control）基于属性的访问控制**

```
权限判断 = f(主体属性, 资源属性, 环境属性, 操作)

主体属性：用户ID、部门、职位、角色
资源属性：创建者、部门、密级、类型
环境属性：时间、地点、IP、设备
操作：查看、编辑、删除、下载
```

---

## 二、ABAC 模型详解

### 2.1 核心概念

**四大要素：**
```
1. Subject（主体）：发起访问的实体
   - 用户属性：ID、姓名、部门、职位、角色
   - 示例：{ userId: 1001, dept: "财务部", role: "经理" }

2. Resource（资源）：被访问的对象
   - 资源属性：ID、类型、创建者、部门、密级
   - 示例：{ docId: 5001, type: "报表", creator: 1001, level: "机密" }

3. Action（操作）：对资源的操作
   - 操作类型：view、edit、delete、download
   - 示例：{ action: "edit" }

4. Environment（环境）：访问时的上下文
   - 环境属性：时间、地点、IP、设备
   - 示例：{ time: "14:30", ip: "192.168.1.100", device: "PC" }
```

**权限策略示例：**
```json
{
  "policyId": "P001",
  "name": "文档编辑策略",
  "description": "文档创建者可以编辑",
  "effect": "allow",
  "rules": [
    {
      "subject": {
        "userId": "${resource.creator}"
      },
      "resource": {
        "type": "document"
      },
      "action": "edit"
    }
  ]
}
```

### 2.2 数据库设计

```sql
CREATE TABLE abac_policy (
    policy_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    policy_name VARCHAR(100) NOT NULL,
    policy_code VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(500),
    effect VARCHAR(10) NOT NULL COMMENT 'allow/deny',
    priority INT DEFAULT 0 COMMENT '优先级，数字越大优先级越高',
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE abac_rule (
    rule_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    policy_id BIGINT NOT NULL,
    rule_type VARCHAR(20) NOT NULL COMMENT 'subject/resource/action/environment',
    attribute_name VARCHAR(50) NOT NULL,
    operator VARCHAR(20) NOT NULL COMMENT 'eq/ne/gt/lt/in/contains',
    attribute_value VARCHAR(500),
    logical_operator VARCHAR(10) COMMENT 'AND/OR',
    FOREIGN KEY (policy_id) REFERENCES abac_policy(policy_id)
);

CREATE TABLE abac_subject_attribute (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    subject_id BIGINT NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value VARCHAR(500) NOT NULL,
    UNIQUE KEY uk_subject_attr (subject_id, attribute_name)
);

CREATE TABLE abac_resource_attribute (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    resource_id VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value VARCHAR(500) NOT NULL,
    UNIQUE KEY uk_resource_attr (resource_id, resource_type, attribute_name)
);
```

### 2.3 Java 实现

**策略引擎核心：**
```java
@Service
public class AbacPolicyEngine {
    
    @Autowired
    private PolicyRepository policyRepository;
    
    public boolean evaluate(AccessRequest request) {
        List<Policy> policies = policyRepository.findApplicablePolicies(
            request.getResourceType(),
            request.getAction()
        );
        
        policies.sort(Comparator.comparing(Policy::getPriority).reversed());
        
        for (Policy policy : policies) {
            if (matchPolicy(policy, request)) {
                return "allow".equals(policy.getEffect());
            }
        }
        
        return false;
    }
    
    private boolean matchPolicy(Policy policy, AccessRequest request) {
        Map<String, Object> context = buildContext(request);
        
        for (Rule rule : policy.getRules()) {
            if (!evaluateRule(rule, context)) {
                return false;
            }
        }
        
        return true;
    }
    
    private boolean evaluateRule(Rule rule, Map<String, Object> context) {
        String attributeName = rule.getAttributeName();
        String operator = rule.getOperator();
        String expectedValue = rule.getAttributeValue();
        
        Object actualValue = getAttributeValue(rule.getRuleType(), attributeName, context);
        
        return compareValues(actualValue, operator, expectedValue);
    }
    
    private boolean compareValues(Object actual, String operator, String expected) {
        switch (operator) {
            case "eq":
                return Objects.equals(actual.toString(), expected);
            case "ne":
                return !Objects.equals(actual.toString(), expected);
            case "gt":
                return Double.parseDouble(actual.toString()) > Double.parseDouble(expected);
            case "lt":
                return Double.parseDouble(actual.toString()) < Double.parseDouble(expected);
            case "in":
                String[] values = expected.split(",");
                return Arrays.asList(values).contains(actual.toString());
            case "contains":
                return actual.toString().contains(expected);
            default:
                return false;
        }
    }
    
    private Map<String, Object> buildContext(AccessRequest request) {
        Map<String, Object> context = new HashMap<>();
        
        context.put("subject", request.getSubjectAttributes());
        context.put("resource", request.getResourceAttributes());
        context.put("action", request.getAction());
        context.put("environment", request.getEnvironmentAttributes());
        
        return context;
    }
}

@Data
public class AccessRequest {
    private Map<String, Object> subjectAttributes;
    private Map<String, Object> resourceAttributes;
    private String action;
    private Map<String, Object> environmentAttributes;
    private String resourceType;
}

@Data
public class Policy {
    private Long policyId;
    private String policyName;
    private String effect;
    private Integer priority;
    private List<Rule> rules;
}

@Data
public class Rule {
    private String ruleType;
    private String attributeName;
    private String operator;
    private String attributeValue;
}
```

**使用示例：**
```java
@RestController
@RequestMapping("/api/document")
public class DocumentController {
    
    @Autowired
    private AbacPolicyEngine policyEngine;
    
    @GetMapping("/{id}")
    public Result<Document> getDocument(@PathVariable Long id) {
        Document document = documentService.getById(id);
        
        AccessRequest request = new AccessRequest();
        request.setSubjectAttributes(getCurrentUserAttributes());
        request.setResourceAttributes(getDocumentAttributes(document));
        request.setAction("view");
        request.setEnvironmentAttributes(getEnvironmentAttributes());
        request.setResourceType("document");
        
        boolean allowed = policyEngine.evaluate(request);
        
        if (!allowed) {
            throw new PermissionDeniedException("无权限查看该文档");
        }
        
        return Result.success(document);
    }
    
    private Map<String, Object> getCurrentUserAttributes() {
        User user = SecurityUtils.getCurrentUser();
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("userId", user.getUserId());
        attrs.put("dept", user.getDept());
        attrs.put("role", user.getRole());
        return attrs;
    }
    
    private Map<String, Object> getDocumentAttributes(Document document) {
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("docId", document.getDocId());
        attrs.put("creator", document.getCreator());
        attrs.put("dept", document.getDept());
        attrs.put("level", document.getLevel());
        return attrs;
    }
    
    private Map<String, Object> getEnvironmentAttributes() {
        HttpServletRequest request = ((ServletRequestAttributes) 
            RequestContextHolder.getRequestAttributes()).getRequest();
        
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("time", LocalTime.now().toString());
        attrs.put("ip", request.getRemoteAddr());
        attrs.put("device", request.getHeader("User-Agent"));
        return attrs;
    }
}
```

### 2.4 策略配置示例

**策略1：文档创建者可以编辑**
```json
{
  "policyName": "文档创建者编辑策略",
  "effect": "allow",
  "priority": 100,
  "rules": [
    {
      "ruleType": "subject",
      "attributeName": "userId",
      "operator": "eq",
      "attributeValue": "${resource.creator}"
    },
    {
      "ruleType": "resource",
      "attributeName": "type",
      "operator": "eq",
      "attributeValue": "document"
    },
    {
      "ruleType": "action",
      "attributeName": "action",
      "operator": "eq",
      "attributeValue": "edit"
    }
  ]
}
```

**策略2：同部门员工可以查看**
```json
{
  "policyName": "同部门查看策略",
  "effect": "allow",
  "priority": 80,
  "rules": [
    {
      "ruleType": "subject",
      "attributeName": "dept",
      "operator": "eq",
      "attributeValue": "${resource.dept}"
    },
    {
      "ruleType": "action",
      "attributeName": "action",
      "operator": "eq",
      "attributeValue": "view"
    }
  ]
}
```

**策略3：工作时间下载限制**
```json
{
  "policyName": "工作时间下载策略",
  "effect": "allow",
  "priority": 90,
  "rules": [
    {
      "ruleType": "environment",
      "attributeName": "time",
      "operator": "gt",
      "attributeValue": "09:00"
    },
    {
      "ruleType": "environment",
      "attributeName": "time",
      "operator": "lt",
      "attributeValue": "18:00"
    },
    {
      "ruleType": "action",
      "attributeName": "action",
      "operator": "eq",
      "attributeValue": "download"
    }
  ]
}
```

---

## 三、RBAC vs ABAC 对比

### 3.1 核心差异

| 维度 | RBAC | ABAC |
|------|------|------|
| **授权方式** | 基于角色 | 基于属性 |
| **灵活性** | 低 | 高 |
| **复杂度** | 简单 | 复杂 |
| **维护成本** | 低 | 中等 |
| **动态性** | 差 | 优秀 |
| **细粒度控制** | 粗粒度 | 细粒度 |
| **适用场景** | 通用企业系统 | 复杂权限场景 |

### 3.2 场景选择

**使用 RBAC 的场景：**
```
✓ 权限规则相对固定
✓ 角色数量可控（< 50个）
✓ 不需要动态权限判断
✓ 团队技术能力有限
✓ 快速开发需求

示例：
- 企业OA系统
- 简单的后台管理系统
- 小型电商系统
```

**使用 ABAC 的场景：**
```
✓ 权限规则复杂多变
✓ 需要细粒度权限控制
✓ 需要基于上下文动态判断
✓ 资源属性影响权限
✓ 高安全性要求

示例：
- 医疗系统
- 金融系统
- 文档管理系统
- 多租户SaaS平台
```

### 3.3 混合使用

**RBAC + ABAC 混合模式：**
```java
@Service
public class HybridAuthorizationService {
    
    @Autowired
    private RbacService rbacService;
    
    @Autowired
    private AbacPolicyEngine abacEngine;
    
    public boolean checkPermission(Long userId, String resource, String action) {
        boolean rbacAllowed = rbacService.hasPermission(userId, resource + ":" + action);
        
        if (!rbacAllowed) {
            return false;
        }
        
        AccessRequest request = buildAccessRequest(userId, resource, action);
        return abacEngine.evaluate(request);
    }
}
```

**使用场景：**
```
1. 基础权限用 RBAC：菜单、按钮权限
2. 细粒度权限用 ABAC：数据行级权限

示例：
- 用户有"查看订单"角色（RBAC）
- 但只能查看自己部门的订单（ABAC）
```

---

## 四、常见问题与解决方案

### 4.1 性能问题

**问题：** 每次请求都需要评估复杂的策略规则，性能差

**解决方案：**
```java
@Service
public class CachedAbacEngine {
    
    private final LoadingCache<String, Boolean> decisionCache;
    
    public CachedAbacEngine() {
        this.decisionCache = Caffeine.newBuilder()
            .maximumSize(10000)
            .expireAfterWrite(5, TimeUnit.MINUTES)
            .build(this::evaluatePolicy);
    }
    
    public boolean checkPermission(AccessRequest request) {
        String cacheKey = buildCacheKey(request);
        
        try {
            return decisionCache.get(cacheKey);
        } catch (Exception e) {
            return false;
        }
    }
    
    private String buildCacheKey(AccessRequest request) {
        return String.format("%s:%s:%s:%s",
            request.getSubjectAttributes().get("userId"),
            request.getResourceType(),
            request.getResourceAttributes().get("resourceId"),
            request.getAction()
        );
    }
}
```

### 4.2 策略冲突

**问题：** 多个策略同时匹配，结果冲突

**解决方案：**
```java
public class ConflictResolutionEngine {
    
    public boolean resolveConflict(List<PolicyResult> results) {
        boolean hasAllow = results.stream().anyMatch(r -> r.getEffect().equals("allow"));
        boolean hasDeny = results.stream().anyMatch(r -> r.getEffect().equals("deny"));
        
        if (hasDeny) {
            return false;
        }
        
        if (hasAllow) {
            return true;
        }
        
        return false;
    }
}
```

---

## 五、最佳实践

### 5.1 设计准则

1. **策略最小化**：避免创建过多策略
2. **优先级管理**：合理设置策略优先级
3. **性能优化**：使用缓存减少计算
4. **策略测试**：充分测试策略规则

### 5.2 注意事项

**设计风险：**
- 策略过于复杂，难以理解和维护
- 性能问题，每次请求都需要评估
- 策略冲突，多个策略结果不一致

**解决方案：**
- 保持策略简单明了
- 实现多级缓存
- 定义清晰的冲突解决规则

---

## 六、核心总结

### 核心问题
RBAC 无法表达复杂的权限规则，难以处理动态场景和细粒度控制。

### 方案解析
通过 **ABAC 模型**，基于主体、资源、环境属性动态判断权限，实现：
- 灵活的权限规则表达
- 细粒度权限控制
- 动态上下文感知

### 关键补充

**最佳实践：**
- 简单场景用 RBAC
- 复杂场景用 ABAC
- 混合使用发挥各自优势

**注意事项：**
- 策略不宜过于复杂
- 注意性能优化
- 处理策略冲突

**扩展方向：**
- 与 RBAC 混合使用
- 集成规则引擎（Drools）
- 实现策略可视化配置
