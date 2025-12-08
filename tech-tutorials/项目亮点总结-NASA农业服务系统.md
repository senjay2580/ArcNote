# NASA农业服务系统 - 项目亮点总结

## 项目概述
**项目名称**：福建省农业服务管理系统（fj-nasa-svc）  
**项目类型**：Spring Cloud微服务架构下的农业信息化管理子系统  
**技术栈**：Spring Boot 2.1.2 + Spring Cloud Greenwich + Nacos + MyBatis + Redis + 达梦数据库  
**项目规模**：30+业务模块，29个Controller，28个Service，涵盖企业管理、报表统计、数据监测等核心业务

---

## 核心技术亮点

### 1. 微服务架构设计与实践
- **服务注册与发现**：基于Alibaba Nacos实现服务注册发现和配置中心，支持多环境动态配置管理
- **分布式架构**：采用Spring Cloud微服务架构，实现服务解耦和独立部署
- **配置管理**：通过Nacos Config实现配置的集中管理和动态刷新，支持多命名空间隔离

### 2. 数据安全与加密传输 ⭐⭐⭐⭐⭐

#### 核心代码实现

**2.1 国密算法工具类 (MgSdkUtil.java)**
```java
@Component
public class MgSdkUtil {
    @Value("${mgzd.appId}")
    private String appId;
    @Value("${mgzd.keyId}")
    private String keyId;
    @Value("${mgzd.url}")
    private String url;

    /**
     * SM3-HMAC 哈希算法 - 用于敏感数据检索
     */
    public String sm3Hmac(String inData) throws Exception {
        ObjectNode params = objectMapper.createObjectNode();
        params.put("appId", appId);
        params.put("tenantId", tenantId);
        params.put("inData", inData);
        params.put("keyId", keyId);
        
        String response = sendPostFormUrlEncoded(
            url + "/apisix/mg1/system/crypto/hmacSM3", params);
        ResponeParam responeParam = objectMapper.readValue(response, ResponeParam.class);
        
        if (responeParam.getResponse().getCode().equals("200")) {
            return (String) responeParam.getResponse().getData();
        }
        throw new BusinessException("获取HMAC值失败");
    }

    /**
     * SM4加密 - 对称加密存储敏感数据
     */
    public String sm4Enc(String inData, String iv) throws IOException {
        ObjectNode params = objectMapper.createObjectNode();
        params.put("appId", appId);
        params.put("inData", inData);
        params.put("keyId", keyId);
        params.put("iv", iv);  // 自定义IV向量
        
        String response = sendPostFormUrlEncoded(
            url + "/apisix/mg1/system/crypto/encrypt", params);
        ResponeParam responeParam = objectMapper.readValue(response, ResponeParam.class);
        
        return (String) responeParam.getResponse().getData();
    }

    /**
     * 批量加密 - 提升性能
     */
    public <T> List<T> batchSm4Enc(List<Object> inDataList, String iv, Class<T> clazz) {
        MgRequestParam requestParam = new MgRequestParam();
        requestParam.setDataList(inDataList);
        requestParam.setIv(iv);
        
        String result = HttpRequestUtil.sendPostJson(
            url + "/apisix/mg1/system/crypto/batchEncrypt", 
            JSON.toJSONString(requestParam));
        
        return JSON.parseArray(result, clazz);
    }
}
```

**2.2 数据传输加解密过滤器 (DataTransferFilter.java)**
```java
@WebFilter(filterName = "DataTransferFilter", urlPatterns = "/*")
@Order(1)
public class DataTransferFilter implements Filter {
    @Autowired
    private SM4Config sm4Config;
    private final SM4Utils sm4 = new SM4Utils();

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, 
                         FilterChain chain) throws IOException, ServletException {
        // 1. 判断是否需要加密（通过请求头smFlag控制）
        String smFlag = ((HttpServletRequest) request).getHeader("smFlag");
        if ("0".equals(smFlag)) {
            chain.doFilter(request, response);
            return;
        }

        // 2. 获取请求体
        String requestBody = getRequestBody((HttpServletRequest) request);
        
        if (StringUtils.isEmpty(requestBody)) {
            // 无请求体，只加密响应
            WrapperResponse wrapResponse = new WrapperResponse((HttpServletResponse) response);
            chain.doFilter(request, wrapResponse);
            
            String responseBody = new String(wrapResponse.getResponseData(), UTF_8);
            String encryptedResponse = sm4.encryptData_ECB(responseBody);
            writeResponse(response, encryptedResponse);
        } else {
            // 3. 验证请求签名（防篡改）
            String sign = ((HttpServletRequest) request).getHeader("sign");
            String decryptedRequest = sm4.decryptData_ECB(requestBody);
            
            // 使用SM3验证签名
            boolean valid = verifyRequestBody(decryptedRequest, sign);
            if (!valid) {
                writeResponse(response, errorRequestBody());
                return;
            }

            // 4. 执行业务逻辑
            WrapperRequest wrapRequest = new WrapperRequest(
                (HttpServletRequest) request, decryptedRequest);
            WrapperResponse wrapResponse = new WrapperResponse(
                (HttpServletResponse) response);
            chain.doFilter(wrapRequest, wrapResponse);

            // 5. 加密响应数据
            String responseBody = new String(wrapResponse.getResponseData(), UTF_8);
            String encryptedResponse = sm4.encryptData_ECB(responseBody);
            writeResponse(response, encryptedResponse);
        }
    }

    private boolean verifyRequestBody(String requestBody, String sign) {
        String targetSign = Sm3Utils.encrypt(requestBody);
        return sign.equalsIgnoreCase(targetSign);
    }
}
```

#### 技术流程分析

**加密流程：**
```
客户端请求 
  ↓
1. 前端使用SM4加密请求数据
  ↓
2. 使用SM3对明文生成签名放入Header
  ↓
3. DataTransferFilter拦截请求
  ↓
4. SM4解密请求体
  ↓
5. SM3验证签名（防篡改）
  ↓
6. 执行业务逻辑
  ↓
7. SM4加密响应数据
  ↓
8. 返回加密响应给客户端
```

**敏感字段存储流程：**
```
业务数据（手机号、身份证）
  ↓
1. SM4加密 → 密文存储到数据库
  ↓
2. SM3-HMAC → 生成哈希值用于检索
  ↓
数据库存储：
  - tel: "BX1Sz2JN4XyuxNIBLUmERg==" (密文)
  - tel_hmac: "a3f5e8..." (哈希索引)
  ↓
查询时：
  - 输入手机号 → SM4加密 → 匹配密文
  - 或 输入手机号 → SM3-HMAC → 匹配哈希索引
```

#### 为什么是亮点

1. **国产化合规**：使用国密SM2/SM3/SM4算法，符合国家密码管理局要求，满足信创政策
2. **透明加解密**：通过Filter实现，业务代码无需关心加解密逻辑，降低开发复杂度
3. **防篡改机制**：SM3签名验证确保数据传输过程中未被篡改
4. **性能优化**：
   - 支持批量加解密，减少网络请求次数
   - HMAC索引优化查询性能，避免全表扫描解密
   - 通过smFlag灵活控制是否加密，内网调用可关闭
5. **安全性高**：
   - 自定义IV向量，增强加密强度
   - 密钥统一管理，支持密钥轮换
   - 敏感数据全生命周期加密

#### 后续优化与拓展建议

**性能优化：**
1. **缓存优化**
   ```java
   // 对频繁查询的加密数据进行缓存
   @Cacheable(value = "encryptedData", key = "#id")
   public String getEncryptedData(String id) {
       return mgSdkUtil.sm4Enc(data, iv);
   }
   ```

2. **异步加密**
   ```java
   // 历史数据批量加密使用异步处理
   @Async("encryptExecutor")
   public CompletableFuture<Void> batchEncryptHistoryData(List<Data> dataList) {
       // 分批处理，每批1000条
       Lists.partition(dataList, 1000).forEach(batch -> {
           mgSdkUtil.batchSm4Enc(batch, iv, Data.class);
       });
       return CompletableFuture.completedFuture(null);
   }
   ```

**功能拓展：**
1. **字段级加密注解**
   ```java
   @Encrypted(algorithm = "SM4", iv = "custom-iv")
   private String phoneNumber;
   
   @Searchable(algorithm = "SM3-HMAC")
   private String idCard;
   ```

2. **加密审计日志**
   ```java
   // 记录所有加解密操作，便于安全审计
   public void logEncryptOperation(String operation, String dataType, String userId) {
       EncryptAuditLog log = new EncryptAuditLog();
       log.setOperation(operation);
       log.setDataType(dataType);
       log.setUserId(userId);
       log.setTimestamp(new Date());
       auditLogMapper.insert(log);
   }
   ```

3. **多租户密钥隔离**
   ```java
   // 不同租户使用不同的密钥ID
   public String sm4Enc(String data, String tenantId) {
       String keyId = keyManager.getKeyIdByTenant(tenantId);
       return mgSdkUtil.sm4Enc(data, keyId);
   }
   ```

4. **密钥轮换机制**
   ```java
   // 定期轮换密钥，重新加密历史数据
   @Scheduled(cron = "0 0 2 1 * ?") // 每月1号凌晨2点
   public void rotateEncryptionKey() {
       String newKeyId = keyManager.generateNewKey();
       List<Data> allData = dataMapper.selectAll();
       
       allData.forEach(data -> {
           String decrypted = mgSdkUtil.sm4Dec(data.getEncryptedField(), oldKeyId);
           String reEncrypted = mgSdkUtil.sm4Enc(decrypted, newKeyId);
           data.setEncryptedField(reEncrypted);
           dataMapper.update(data);
       });
   }
   ```

**安全增强：**
1. **加密数据脱敏展示**
   ```java
   // 查询结果自动脱敏
   public String maskSensitiveData(String decryptedData, String dataType) {
       if ("PHONE".equals(dataType)) {
           return decryptedData.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2");
       }
       return decryptedData;
   }
   ```

2. **加密强度配置化**
   ```yaml
   mgzd:
     encryption:
       algorithm: SM4-CBC  # 支持ECB/CBC/CTR模式切换
       key-length: 256     # 密钥长度
       padding: PKCS7      # 填充方式
   ```

### 3. 数据库适配与国产化改造
- **国产数据库支持**：完成从Oracle到达梦数据库（DM8）的迁移适配工作
- **宝蓝德应用服务器**：集成bes-lite-spring-boot-starter，支持国产应用服务器部署
- **数据库连接池优化**：使用Druid连接池，配置监控和SQL性能分析

### 4. 复杂业务场景处理

#### 企业全生命周期管理
- **企业认证管理**：实现企业信息录入、资质认证、审核流程管理
- **多维度查询**：支持企业信息的综合查询、统计分析和数据导出
- **认证状态管理**：实现企业认证状态流转和权限控制

#### 多类型报表系统
- **年度经济报表**：实现农业企业年度经济经营数据的采集、审核、统计
- **季度报表管理**：支持企业季度数据上报、审核、汇总分析
- **中期监测报表**：实现农业项目中期监测数据的动态跟踪和分析
- **综合查询统计**：提供企业运行情况的多维度查询和可视化展示

#### 畜禽养殖监测系统（lb模块）
- **养殖企业管理**：实现畜禽养殖企业的备案、监测数据采集
- **监测数据处理**：支持养殖数据的批量导入、校验、统计分析
- **数据对比校验**：实现监测数据与备案数据的自动比对和异常提醒

### 5. Excel数据处理能力
- **EasyExcel集成**：使用阿里EasyExcel实现大数据量Excel的高效读写
- **模板导出**：支持基于模板的复杂Excel报表生成
- **批量导入**：实现Excel数据的批量导入、校验、入库
- **数据校验**：自定义校验规则，支持数据格式、业务规则的多层次校验
- **错误反馈**：导入失败数据自动生成错误报告，便于数据修正

### 6. 操作日志与审计 ⭐⭐⭐⭐

#### 核心代码实现

**6.1 自定义操作日志注解**
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface OperationLogDetail {
    // 操作描述，支持占位符 {{参数名}}
    String detail() default "";
    
    // 日志级别：1-普通 2-重要 3-核心 4-导出
    int level() default 1;
    
    // 操作单元（模块）
    OperationUnit operationUnit();
    
    // 操作类型：INSERT/UPDATE/DELETE/SELECT/EXPORT/AGREE/REJECT
    OperationType operationType();
    
    // 详情子字段（用于提取嵌套对象字段）
    String detailSub() default "";
}
```

**6.2 AOP切面实现 (LogAspect.java)**
```java
@Aspect
@Component
public class LogAspect {
    @Autowired
    private OperationLogService operationLogService;
    
    @Autowired
    private UserInfoUtil userInfoUtil;

    @Pointcut("@annotation(com.newland.nasa.aopLog.annotation.OperationLogDetail)")
    public void operationLog() {}

    /**
     * 环绕增强 - 记录方法执行时间和结果
     */
    @Around("operationLog()")
    public Object doAround(ProceedingJoinPoint joinPoint) throws Throwable {
        Object res = null;
        long startTime = System.currentTimeMillis();
        boolean methodSucc = false;
        
        try {
            // 执行目标方法
            res = joinPoint.proceed();
            long executeTime = System.currentTimeMillis() - startTime;
            methodSucc = true;
            return res;
        } finally {
            try {
                if (methodSucc) {
                    // 方法执行成功，记录日志
                    addOperationLog(joinPoint, res, 1, executeTime);
                }
            } catch (Exception e) {
                System.out.println("LogAspect 操作失败：" + e.getMessage());
            }
        }
    }

    /**
     * 异常通知 - 记录异常日志
     */
    @AfterThrowing(pointcut = "operationLog()", throwing = "error")
    public void throwss(JoinPoint jp, Throwable error) {
        long time = System.currentTimeMillis();
        addOperationLog(jp, error.getMessage(), 0, time);
    }

    /**
     * 添加操作日志
     */
    private void addOperationLog(JoinPoint joinPoint, Object res, 
                                  Integer successFlag, long time) {
        // 1. 获取当前请求信息
        HttpServletRequest request = HttpServletUtils.getRequest();
        String token = request.getHeaders("token").nextElement();
        UserBaseInfo userBaseInfo = userInfoUtil.getUserInfo(token);
        
        // 2. 获取方法签名和注解信息
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        OperationLogDetail annotation = signature.getMethod()
            .getAnnotation(OperationLogDetail.class);
        
        // 3. 构建日志对象
        OperationLog operationLog = new OperationLog();
        operationLog.setId(UUID.randomUUID().toString());
        operationLog.setRunTime(time);  // 执行耗时
        operationLog.setReturnValue(JSON.toJSONString(res));  // 返回值
        operationLog.setSuccessFlag(String.valueOf(successFlag));  // 成功标识
        operationLog.setArgs(JSON.toJSONString(joinPoint.getArgs()));  // 方法参数
        operationLog.setCreateTime(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
            .format(new Date()));
        operationLog.setMethod(signature.getDeclaringTypeName() + "." 
            + signature.getName());  // 方法全路径
        
        // 4. 设置用户信息
        operationLog.setUserId(userBaseInfo.getData().getUserid());
        operationLog.setUserName(userBaseInfo.getData().getUsername());
        operationLog.setLoginName(userBaseInfo.getData().getLoginname());
        
        // 5. 设置注解信息
        if (annotation != null) {
            operationLog.setLeveloff(annotation.level());
            operationLog.setDescription(getDetail(
                signature.getParameterNames(), 
                joinPoint.getArgs(), 
                annotation, 
                userBaseInfo.getData().getUsername()));
            operationLog.setOperationType(annotation.operationType().getValue());
            operationLog.setOperationUnit(annotation.operationUnit().getValue());
        }
        
        // 6. 异步保存日志（使用新事务，避免影响主业务）
        operationLogService.saveOperationLog(operationLog);
    }

    /**
     * 处理日志描述中的占位符
     */
    private String getDetail(String[] argNames, Object[] args, 
                            OperationLogDetail annotation, String userName) {
        Map<Object, Object> map = new HashMap<>();
        for (int i = 0; i < argNames.length; i++) {
            map.put(argNames[i], args[i]);
        }

        String detail = userName + "=》" + annotation.detail();
        
        try {
            for (Map.Entry<Object, Object> entry : map.entrySet()) {
                Object k = entry.getKey();
                Object v = entry.getValue();
                
                // 支持提取嵌套对象字段
                if (StringUtils.isNotBlank(annotation.detailSub())) {
                    Map mapParam = (Map) JSON.parse(JSONObject.toJSON(v).toString());
                    detail = detail.replace("{{" + k + "}}", 
                        JSON.toJSONString(mapParam.get(annotation.detailSub())));
                } else {
                    detail = detail.replace("{{" + k + "}}", JSON.toJSONString(v));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return detail;
    }
}
```

**6.3 业务代码使用示例**
```java
@Service
public class QuarterReportServiceImpl implements QuarterReportService {
    
    @Override
    @OperationLogDetail(
        detail = "保存季度报表信息",
        level = 1,
        operationUnit = OperationUnit.NASA_QUARTER_REPORT,
        operationType = OperationType.INSERT
    )
    public long addQuarterReport(String userId, QuarterReportDTO quarterReport) {
        // 业务逻辑
        return quarterReportMapper.insert(quarterReport);
    }

    @Override
    @OperationLogDetail(
        detail = "审核季度报表-通过",
        level = 2,
        operationUnit = OperationUnit.NASA_QUARTER_REPORT,
        operationType = OperationType.AGREE
    )
    public void approvedProcess(String loginName, String backOpinion, long reportId) {
        // 审核通过逻辑
        quarterReportMapper.updateStatus(reportId, "APPROVED");
    }

    @Override
    @OperationLogDetail(
        detail = "审核季度报表-驳回",
        level = 2,
        operationUnit = OperationUnit.NASA_QUARTER_REPORT,
        operationType = OperationType.REJECT
    )
    public void approvalRejection(String loginName, String backOpinion, long reportId) {
        // 驳回逻辑
        quarterReportMapper.updateStatus(reportId, "REJECTED");
    }
}
```

**6.4 日志服务实现**
```java
@Service
@Transactional
public class OperationLogServiceImpl implements OperationLogService {
    
    @Autowired
    private OperationLogMapper operationLogMapper;

    /**
     * 保存操作日志 - 使用新事务，避免影响主业务
     */
    @Override
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveOperationLog(OperationLog operationLog) {
        operationLogMapper.saveOperationLog(operationLog);
    }

    /**
     * 分页查询操作日志
     */
    @Override
    public PageResult<OperationLog> listOperationLog(OperationLog queryCondition) {
        int pageNum = queryCondition.getPageNum();
        int pageSize = queryCondition.getPageSize();
        
        PageHelper.startPage(pageNum, pageSize);
        Page<OperationLog> page = (Page<OperationLog>) 
            operationLogMapper.listOperationLog(queryCondition);
        
        return new PageResult<>(page.getTotal(), page.getResult());
    }
}
```

#### 技术流程分析

```
用户操作请求
  ↓
Controller接收请求
  ↓
Service方法执行（带@OperationLogDetail注解）
  ↓
AOP切面拦截
  ↓
@Around 环绕增强开始
  ↓
记录开始时间
  ↓
执行目标方法 joinPoint.proceed()
  ↓
方法执行成功？
  ├─ 是 → 计算执行时间
  │       ↓
  │     提取方法信息（类名、方法名、参数）
  │       ↓
  │     获取用户信息（从Token解析）
  │       ↓
  │     解析注解信息（操作类型、级别、描述）
  │       ↓
  │     处理描述占位符（替换{{参数名}}）
  │       ↓
  │     构建OperationLog对象
  │       ↓
  │     异步保存到数据库（新事务）
  │       ↓
  │     返回方法执行结果
  │
  └─ 否 → @AfterThrowing 异常通知
          ↓
        记录异常信息
          ↓
        保存异常日志
          ↓
        抛出异常
```

**日志数据结构：**
```sql
CREATE TABLE OPERATION_LOG (
    ID VARCHAR2(50) PRIMARY KEY,
    USER_ID VARCHAR2(50),           -- 操作人ID
    USER_NAME VARCHAR2(100),        -- 操作人姓名
    LOGIN_NAME VARCHAR2(100),       -- 登录名
    OPERATION_UNIT VARCHAR2(50),    -- 操作模块
    OPERATION_TYPE VARCHAR2(20),    -- 操作类型
    DESCRIPTION VARCHAR2(500),      -- 操作描述
    METHOD VARCHAR2(200),           -- 方法全路径
    ARGS CLOB,                      -- 方法参数
    RETURN_VALUE CLOB,              -- 返回值
    RUN_TIME NUMBER,                -- 执行耗时(ms)
    SUCCESS_FLAG VARCHAR2(1),       -- 成功标识 1-成功 0-失败
    LEVELOFF NUMBER,                -- 日志级别
    CREATE_TIME VARCHAR2(20)        -- 创建时间
);
```

#### 为什么是亮点

1. **无侵入性**：通过AOP实现，业务代码只需添加注解，无需手动编写日志代码
2. **灵活配置**：
   - 支持自定义日志级别（普通/重要/核心/导出）
   - 支持占位符动态替换参数值
   - 支持提取嵌套对象字段
3. **完整性**：
   - 记录方法执行时间，便于性能分析
   - 记录方法参数和返回值，便于问题排查
   - 记录异常信息，便于错误追踪
4. **事务隔离**：使用REQUIRES_NEW传播级别，日志保存失败不影响主业务
5. **审计合规**：满足政务系统的审计追溯要求，记录所有关键操作

#### 后续优化与拓展建议

**性能优化：**
1. **异步日志处理**
   ```java
   @Async("logExecutor")
   @Transactional(propagation = Propagation.REQUIRES_NEW)
   public CompletableFuture<Void> saveOperationLogAsync(OperationLog log) {
       operationLogMapper.saveOperationLog(log);
       return CompletableFuture.completedFuture(null);
   }
   ```

2. **批量写入优化**
   ```java
   // 使用队列缓存日志，批量写入数据库
   private BlockingQueue<OperationLog> logQueue = new LinkedBlockingQueue<>(1000);
   
   @Scheduled(fixedRate = 5000)  // 每5秒批量写入一次
   public void batchSaveLogs() {
       List<OperationLog> logs = new ArrayList<>();
       logQueue.drainTo(logs, 100);  // 每次最多100条
       
       if (!logs.isEmpty()) {
           operationLogMapper.batchInsert(logs);
       }
   }
   ```

3. **日志归档策略**
   ```java
   @Scheduled(cron = "0 0 2 * * ?")  // 每天凌晨2点
   public void archiveOldLogs() {
       // 将3个月前的日志归档到历史表
       Date threeMonthsAgo = DateUtils.addMonths(new Date(), -3);
       operationLogMapper.archiveLogs(threeMonthsAgo);
   }
   ```

**功能拓展：**
1. **敏感信息脱敏**
   ```java
   private String maskSensitiveInfo(String args) {
       // 对日志中的手机号、身份证等敏感信息脱敏
       return args.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2")
                  .replaceAll("(\\d{6})\\d{8}(\\d{4})", "$1********$2");
   }
   ```

2. **日志分类存储**
   ```java
   // 根据日志级别存储到不同的表
   public void saveOperationLog(OperationLog log) {
       if (log.getLeveloff() >= 3) {
           // 核心操作日志存储到专门的表
           coreLogMapper.insert(log);
       } else {
           // 普通日志
           operationLogMapper.insert(log);
       }
   }
   ```

3. **实时日志监控**
   ```java
   @Component
   public class LogMonitor {
       @Autowired
       private WebSocketService webSocketService;
       
       @EventListener
       public void onOperationLog(OperationLogEvent event) {
           OperationLog log = event.getLog();
           
           // 重要操作实时推送到监控大屏
           if (log.getLeveloff() >= 2) {
               webSocketService.broadcast("log", log);
           }
           
           // 异常操作发送告警
           if ("0".equals(log.getSuccessFlag())) {
               alertService.sendAlert("操作失败", log);
           }
       }
   }
   ```

4. **日志统计分析**
   ```java
   public Map<String, Object> getLogStatistics(Date startDate, Date endDate) {
       Map<String, Object> stats = new HashMap<>();
       
       // 操作次数统计
       stats.put("totalCount", operationLogMapper.countByDateRange(startDate, endDate));
       
       // 按操作类型统计
       stats.put("byType", operationLogMapper.countByType(startDate, endDate));
       
       // 按用户统计
       stats.put("byUser", operationLogMapper.countByUser(startDate, endDate));
       
       // 平均执行时间
       stats.put("avgRunTime", operationLogMapper.avgRunTime(startDate, endDate));
       
       // 失败率
       stats.put("failureRate", operationLogMapper.getFailureRate(startDate, endDate));
       
       return stats;
   }
   ```

5. **日志查询优化**
   ```java
   // 使用Elasticsearch存储日志，提升查询性能
   @Service
   public class LogSearchService {
       @Autowired
       private ElasticsearchTemplate elasticsearchTemplate;
       
       public Page<OperationLog> searchLogs(LogSearchDTO searchDTO) {
           BoolQueryBuilder query = QueryBuilders.boolQuery();
           
           if (StringUtils.isNotBlank(searchDTO.getUserName())) {
               query.must(QueryBuilders.matchQuery("userName", searchDTO.getUserName()));
           }
           
           if (StringUtils.isNotBlank(searchDTO.getOperationType())) {
               query.must(QueryBuilders.termQuery("operationType", searchDTO.getOperationType()));
           }
           
           NativeSearchQuery searchQuery = new NativeSearchQueryBuilder()
               .withQuery(query)
               .withPageable(PageRequest.of(searchDTO.getPageNum(), searchDTO.getPageSize()))
               .build();
           
           return elasticsearchTemplate.queryForPage(searchQuery, OperationLog.class);
       }
   }
   ```

### 7. 第三方系统集成
- **单点登录集成**：实现与微信SSO、民政厅SSO的单点登录对接
- **WebService调用**：使用Apache Axis实现与外部系统的WebService接口对接
- **数据同步**：实现与上级系统的数据同步和交换

### 8. 性能优化与高可用
- **分页查询优化**：集成PageHelper实现高效的分页查询
- **Redis缓存**：使用Redis缓存热点数据，提升系统响应速度
- **连接池管理**：配置Druid和Commons-Pool2优化数据库和Redis连接
- **异步处理**：使用多线程处理耗时任务，提升系统并发能力

---

## 业务模块覆盖

### 核心业务模块
1. **企业信息管理**：企业基本信息、认证管理、资质审核
2. **报表管理系统**：年度报表、季度报表、中期监测报表
3. **综合查询统计**：企业运行情况查询、数据统计分析
4. **畜禽养殖监测**：养殖企业管理、监测数据采集与分析
5. **村庄信息管理**：乡村振兴相关的村庄基础信息管理
6. **代办人员管理**：农业服务代办人员信息管理
7. **字典管理**：系统字典、区域代码等基础数据管理
8. **用户权限管理**：用户信息、权限控制
9. **操作日志管理**：系统操作日志记录与查询

### 特色功能
- **农民人员管理（nf模块）**：实现农民信息的批量导入、查询、统计、Excel导出
- **数据导入工具**：支持多种格式数据的批量导入和校验
- **表单处理中心**：统一的表单审核、流转处理

---

## 技术难点与解决方案

### 1. 国密算法性能优化
**问题**：SM4加解密影响接口响应时间  
**解决**：
- 通过请求头smFlag控制是否启用加密，灵活配置
- 使用自定义Request/Response包装器，避免重复读取流
- 优化加解密算法实现，减少性能损耗

### 2. 大数据量Excel处理
**问题**：传统POI处理大文件内存溢出  
**解决**：
- 采用EasyExcel基于事件驱动的流式处理
- 分批次读取和写入，控制内存占用
- 实现自定义监听器，支持复杂业务逻辑

### 3. 数据库迁移适配
**问题**：Oracle到达梦数据库的SQL兼容性  
**解决**：
- 梳理SQL差异，修改不兼容的语法
- 调整MyBatis映射文件，适配达梦数据库特性
- 编写数据迁移脚本，确保数据完整性

### 4. 多源数据校验与比对
**问题**：畜禽监测数据与备案数据的自动比对  
**解决**：
- 设计灵活的数据匹配规则引擎
- 实现多维度数据比对算法
- 生成详细的差异报告，支持人工审核

---

## 项目成果与价值

### 业务价值
- 支撑福建省农业企业信息化管理，服务企业数量1000+
- 实现农业数据的数字化采集、统计、分析，提升管理效率
- 为政府决策提供数据支持，助力乡村振兴战略实施

### 技术价值
- 完成系统国产化改造，符合信创要求
- 建立完善的数据安全体系，保障敏感信息安全
- 积累微服务架构实践经验，为后续项目提供参考

### 个人成长
- 深入理解Spring Cloud微服务架构设计与实践
- 掌握国密算法在实际项目中的应用
- 提升大数据量处理和性能优化能力
- 积累复杂业务系统的开发和维护经验

---

## 简历描述建议

### 项目描述模板
```
福建省农业服务管理系统是基于Spring Cloud微服务架构的农业信息化管理平台，
负责企业管理、报表统计、数据监测等核心业务。系统采用Nacos作为注册中心和
配置中心，使用达梦数据库和宝蓝德应用服务器完成国产化改造，集成国密SM4/SM3
算法保障数据安全。项目包含30+业务模块，支撑1000+农业企业的信息化管理。
```

### 工作职责描述
```
1. 负责企业管理、报表统计、畜禽监测等核心模块的开发与维护
2. 实现基于SM4/SM3国密算法的数据加解密和签名验证，保障数据传输安全
3. 完成Oracle到达梦数据库的迁移适配，支持国产化部署
4. 使用EasyExcel实现大数据量Excel的高效导入导出，支持百万级数据处理
5. 基于Spring AOP实现操作日志自动记录，满足审计追溯需求
6. 集成Nacos实现服务注册发现和配置中心，提升系统可维护性
7. 优化数据库查询和Redis缓存策略，提升系统响应速度30%
```

### 技术关键词
```
Spring Boot, Spring Cloud, Nacos, MyBatis, Redis, 达梦数据库, 
国密算法(SM4/SM3), EasyExcel, AOP, 微服务架构, 宝蓝德应用服务器,
数据加密, 操作日志, 分页查询, Druid连接池, Swagger API文档
```

---

## 面试准备要点

### 可能被问到的问题
1. **微服务架构**：如何实现服务注册发现？Nacos的配置管理如何使用？
2. **数据安全**：国密算法的应用场景？如何实现透明加解密？
3. **性能优化**：如何处理大数据量Excel？Redis缓存策略是什么？
4. **国产化改造**：Oracle到达梦数据库迁移遇到哪些问题？如何解决？
5. **AOP应用**：操作日志是如何实现的？切面的执行顺序如何控制？
6. **业务理解**：报表审核流程是怎样的？数据校验规则如何设计？

### 回答思路
- 结合具体代码和业务场景说明
- 强调问题分析和解决过程
- 突出技术选型的合理性
- 展示对业务的深入理解

---

**文档生成时间**：2025年  
**适用场景**：实习/校招简历、技术面试准备
