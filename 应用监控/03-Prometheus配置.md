# Prometheus 配置详解

## 📋 文档导航
[← 上一篇：02-环境准备与安装](./02-环境准备与安装.md) | [下一篇：04-Grafana配置与仪表盘 →](./04-Grafana配置与仪表盘.md)

---

## 🎯 本章目标

- ✅ 理解 Prometheus 工作原理
- ✅ 掌握 PromQL 查询语言
- ✅ 学会配置采集规则
- ✅ 掌握告警规则编写

---

## 📖 Prometheus 核心概念

### 1. 时序数据库原理

**类比**: Prometheus 就像一个「智能体检中心」
```
传统体检(手动查询):               Prometheus 体检(自动采集):
你→ 去医院 → 测量 → 拿报告        医院 → 定时找你 → 自动记录 → 随时查看历史
```

**时序数据特点**:
- **时间戳**: 每个数据点都有精确时间
- **指标名**: 如 `cpu_usage`、`memory_used`
- **标签**: 多维度区分,如 `{instance="server1", env="prod"}`

**数据模型示例**:
```
node_cpu_seconds_total{cpu="0",mode="idle",instance="server1"} 12345.67 @1635840000
                       ↑                    ↑                      ↑         ↑
                    指标名                 标签                   值      时间戳
```

### 2. Pull vs Push 模式

#### Pull 模式(Prometheus 采用)
```
Prometheus (主动抓取)
    ↓ HTTP GET /metrics
Target (被动暴露指标)
```
✅ **优势**:
- 目标服务无感知,不需要知道监控系统地址
- Prometheus 控制采集频率,避免数据风暴
- 目标服务重启不影响采集

#### Push 模式(如 InfluxDB)
```
Application (主动推送)
    ↓ HTTP POST
Monitoring System (被动接收)
```
❌ **劣势**:
- 应用需要配置监控地址,耦合度高
- 无法控制推送频率,可能压垮监控系统

### 3. 指标类型(Metric Types)

| 类型 | 说明 | 适用场景 | 示例 |
|-----|------|---------|-----|
| **Counter** | 只增不减的计数器 | 请求总数、错误总数 | `http_requests_total` |
| **Gauge** | 可增可减的瞬时值 | CPU使用率、内存使用量 | `node_memory_used_bytes` |
| **Histogram** | 分布统计(分桶) | 响应时间分布 | `http_request_duration_seconds` |
| **Summary** | 分位数统计 | P50/P90/P99延迟 | `http_request_duration_seconds_summary` |

**Counter vs Gauge 区别**:
```
Counter (累加器):
时间: 10:00  10:01  10:02  10:03
值:   100    150    220    300   (只会增加)

Gauge (温度计):
时间: 10:00  10:01  10:02  10:03
值:   70%    85%    60%    90%   (可涨可跌)
```

---

## ⚙️ Prometheus 配置文件详解

### 完整配置结构
```yaml
global:              # 全局配置
scrape_configs:      # 采集配置
rule_files:          # 告警规则
alerting:            # 告警管理器配置
remote_write:        # 远程写入(可选)
remote_read:         # 远程读取(可选)
```

### 1. 全局配置(global)

```yaml
global:
  # 采集间隔(默认1分钟,推荐15秒)
  scrape_interval: 15s
  
  # 评估告警规则间隔
  evaluation_interval: 15s
  
  # 请求超时时间
  scrape_timeout: 10s
  
  # 全局标签(所有指标都会带上)
  external_labels:
    cluster: 'archat-prod'       # 集群标识
    env: 'production'            # 环境标识
    region: 'cn-beijing'         # 区域标识
```

**🎯 最佳实践**:
- `scrape_interval`: 15s-30s 平衡精度与存储
- `external_labels`: 多环境区分,方便聚合查询

### 2. 采集配置(scrape_configs)

#### 基础采集配置
```yaml
scrape_configs:
  - job_name: 'my-service'           # Job 名称(必填)
    scrape_interval: 15s             # 覆盖全局配置(可选)
    scrape_timeout: 10s              # 单次采集超时(可选)
    metrics_path: '/metrics'         # 指标路径(默认 /metrics)
    scheme: http                     # 协议(http/https)
    
    static_configs:                  # 静态目标配置
      - targets:                     # 目标列表
          - 'localhost:9100'
          - '192.168.1.10:9100'
        labels:                      # 自定义标签
          env: 'prod'
          team: 'backend'
```

#### 服务发现(高级)
```yaml
scrape_configs:
  # 基于文件的服务发现
  - job_name: 'file-sd'
    file_sd_configs:
      - files:
          - '/etc/prometheus/targets/*.json'
        refresh_interval: 5m

  # 基于 Kubernetes 的服务发现
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

#### 标签重写(relabel_configs)
```yaml
scrape_configs:
  - job_name: 'spring-boot'
    static_configs:
      - targets: ['app1:8080', 'app2:8080']
    
    # 标签重写规则
    relabel_configs:
      # 1. 删除不需要的标签
      - source_labels: [__address__]
        regex: '.*:8080'
        action: drop
      
      # 2. 替换实例标签
      - source_labels: [__address__]
        target_label: instance
        replacement: 'my-app'
      
      # 3. 保留特定标签
      - source_labels: [env]
        regex: 'prod'
        action: keep
```

**常用 action**:
- `replace`: 替换标签值
- `keep`: 保留匹配的目标
- `drop`: 丢弃匹配的目标
- `labelmap`: 批量重命名标签

---

## 🔍 PromQL 查询语言

### 1. 基础查询

#### 即时查询(瞬时值)
```promql
# 查询当前 CPU 使用率
node_cpu_seconds_total

# 带标签过滤
node_cpu_seconds_total{mode="idle"}

# 多标签过滤
node_cpu_seconds_total{instance="server1",mode="idle"}

# 正则匹配
node_cpu_seconds_total{mode=~"idle|iowait"}

# 反向匹配
node_cpu_seconds_total{mode!="idle"}
```

#### 范围查询(时间范围)
```promql
# 最近5分钟的数据
node_cpu_seconds_total[5m]

# 常用时间单位
[1m]   # 1分钟
[5m]   # 5分钟
[1h]   # 1小时
[1d]   # 1天
```

### 2. 聚合函数

```promql
# 求和
sum(node_cpu_seconds_total)

# 平均值
avg(node_memory_used_bytes)

# 最大值/最小值
max(node_filesystem_avail_bytes)
min(node_filesystem_avail_bytes)

# 计数
count(up{job="node-exporter"})

# 分位数
quantile(0.95, http_request_duration_seconds)
```

#### 分组聚合(by/without)
```promql
# 按实例分组求和
sum(node_cpu_seconds_total) by (instance)

# 按模式分组求平均
avg(node_cpu_seconds_total) by (mode)

# 排除某些标签
sum(node_cpu_seconds_total) without (cpu)
```

### 3. 速率计算(rate/irate)

**Counter 类型必须用 rate/irate**,因为它是累加值

#### rate (平均速率)
```promql
# HTTP 请求每秒速率(最近5分钟平均)
rate(http_requests_total[5m])

# 公式: (最新值 - 最旧值) / 时间跨度
```

#### irate (瞬时速率)
```promql
# HTTP 请求每秒速率(最近2个点)
irate(http_requests_total[5m])

# 公式: (最新值 - 前一个值) / 时间间隔
```

**🎯 选择建议**:
- `rate`: 用于告警(平滑波动)
- `irate`: 用于图表展示(灵敏度高)

#### CPU 使用率计算(经典案例)
```promql
# CPU 使用率 = 100% - 空闲率
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 拆解:
# 1. irate(...[5m])      → 每秒空闲时间增量
# 2. avg by(instance)    → 按实例求平均
# 3. * 100               → 转换为百分比
# 4. 100 - ...           → 反转得到使用率
```

### 4. 算术运算

```promql
# 加减乘除
node_memory_total_bytes - node_memory_available_bytes  # 已用内存
node_memory_available_bytes / node_memory_total_bytes * 100  # 可用内存百分比

# 比较运算
node_cpu_seconds_total > 1000  # 大于1000的指标
up == 1  # 服务在线

# 逻辑运算
up == 1 and on(instance) node_load1 > 5  # 服务在线且负载>5
```

### 5. 实战查询案例

#### 案例1: MySQL 慢查询增长率
```promql
# 每秒慢查询数
rate(mysql_global_status_slow_queries[5m])

# 最近1小时总慢查询
increase(mysql_global_status_slow_queries[1h])
```

#### 案例2: Redis 内存使用率
```promql
# 内存使用率
redis_memory_used_bytes / redis_memory_max_bytes * 100

# 内存碎片率
redis_mem_fragmentation_ratio
```

#### 案例3: 接口响应时间 P99
```promql
# 假设 histogram 类型指标
histogram_quantile(0.99, 
  rate(http_request_duration_seconds_bucket[5m])
)
```

#### 案例4: 服务可用率(SLA)
```promql
# 最近1小时可用率
avg_over_time(up{job="my-service"}[1h]) * 100
```

---

## 📏 告警规则配置

### 1. 告警规则结构

```yaml
groups:                              # 告警组
  - name: example_alerts             # 组名
    interval: 30s                    # 评估间隔(可选)
    rules:                           # 规则列表
      - alert: HighCPUUsage          # 告警名称
        expr: |                      # PromQL 查询
          100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m                      # 持续时间(避免抖动)
        labels:                      # 自定义标签
          severity: warning
          team: backend
        annotations:                 # 告警描述
          summary: "{{ $labels.instance }} CPU使用率过高"
          description: "当前CPU使用率: {{ $value }}%"
```

### 2. 告警级别设计

```yaml
groups:
  - name: cpu_alerts
    rules:
      # 警告级别(80%)
      - alert: HighCPUUsage_Warning
        expr: cpu_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU使用率超过80%"
      
      # 严重级别(90%)
      - alert: HighCPUUsage_Critical
        expr: cpu_usage > 90
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "CPU使用率超过90%,需立即处理!"
```

### 3. 完整告警规则示例

#### MySQL 告警规则
创建文件: `monitoring/prometheus/rules/mysql_alerts.yml`
```yaml
groups:
  - name: mysql_alerts
    interval: 30s
    rules:
      # MySQL 服务不可用
      - alert: MySQLDown
        expr: mysql_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "MySQL {{ $labels.instance }} 不可用"
          description: "MySQL 服务已停止或无法连接"

      # 慢查询增长率过高
      - alert: MySQLSlowQueries
        expr: rate(mysql_global_status_slow_queries[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.instance }} 慢查询过多"
          description: "每秒慢查询数: {{ $value }}"

      # 连接数过多
      - alert: MySQLTooManyConnections
        expr: mysql_global_status_threads_connected > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.instance }} 连接数过多"
          description: "当前连接数: {{ $value }}"

      # InnoDB 缓冲池命中率过低
      - alert: MySQLInnoDBBufferPoolHitRate
        expr: |
          (mysql_global_status_innodb_buffer_pool_read_requests / 
          (mysql_global_status_innodb_buffer_pool_read_requests + 
           mysql_global_status_innodb_buffer_pool_reads)) * 100 < 90
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.instance }} InnoDB 缓冲池命中率低"
          description: "当前命中率: {{ $value }}%"
```

#### Redis 告警规则
创建文件: `monitoring/prometheus/rules/redis_alerts.yml`
```yaml
groups:
  - name: redis_alerts
    rules:
      # Redis 服务不可用
      - alert: RedisDown
        expr: redis_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Redis {{ $labels.instance }} 不可用"

      # 内存使用率过高
      - alert: RedisHighMemory
        expr: redis_memory_used_bytes / redis_memory_max_bytes * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Redis {{ $labels.instance }} 内存使用过高"
          description: "当前使用率: {{ $value }}%"

      # 拒绝连接数增长
      - alert: RedisRejectedConnections
        expr: rate(redis_rejected_connections_total[5m]) > 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Redis {{ $labels.instance }} 拒绝连接"
          description: "可能达到最大连接数限制"

      # 缓存命中率过低
      - alert: RedisLowHitRate
        expr: |
          rate(redis_keyspace_hits_total[5m]) / 
          (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) * 100 < 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Redis {{ $labels.instance }} 命中率低"
          description: "当前命中率: {{ $value }}%"
```

#### 应用告警规则
创建文件: `monitoring/prometheus/rules/app_alerts.yml`
```yaml
groups:
  - name: app_alerts
    rules:
      # 应用不可用
      - alert: ApplicationDown
        expr: up{job="spring-boot"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "应用 {{ $labels.application }} 不可用"

      # JVM 堆内存使用率过高
      - alert: HighJVMHeapUsage
        expr: |
          (jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"}) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.application }} JVM堆内存使用过高"
          description: "当前使用率: {{ $value }}%"

      # GC 频繁
      - alert: HighGCRate
        expr: rate(jvm_gc_pause_seconds_count[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.application }} GC过于频繁"
          description: "每秒GC次数: {{ $value }}"

      # 接口错误率过高
      - alert: HighErrorRate
        expr: |
          rate(http_server_requests_seconds_count{status=~"5.."}[5m]) / 
          rate(http_server_requests_seconds_count[5m]) * 100 > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.application }} 接口错误率过高"
          description: "当前错误率: {{ $value }}%"

      # 接口响应时间过长
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, 
            rate(http_server_requests_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.application }} 接口响应慢"
          description: "P99延迟: {{ $value }}s"
```

### 4. 告警规则测试

```bash
# 1. 检查规则语法
docker exec archat_prometheus promtool check rules /etc/prometheus/rules/*.yml

# 2. 热加载规则
curl -X POST http://localhost:9090/-/reload

# 3. 查看当前告警
http://localhost:9090/alerts
```

---

## 🎯 性能优化

### 1. 存储优化

```yaml
# 启动参数
prometheus:
  command:
    # 数据保留时间(默认15天)
    - '--storage.tsdb.retention.time=15d'
    
    # 按大小限制(二选一)
    - '--storage.tsdb.retention.size=50GB'
    
    # 压缩
    - '--storage.tsdb.min-block-duration=2h'
    - '--storage.tsdb.max-block-duration=2h'
```

### 2. 采集优化

```yaml
scrape_configs:
  - job_name: 'high-frequency'
    scrape_interval: 10s         # 高频采集
    metrics_path: '/metrics'
    
    # 指标过滤(只采集需要的)
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'go_.*|process_.*'   # 丢弃 Go runtime 指标
        action: drop
```

### 3. 查询优化

**❌ 低效查询**:
```promql
# 全量扫描,非常慢
sum(rate(http_requests_total[5m]))
```

**✅ 高效查询**:
```promql
# 指定标签过滤,减少扫描范围
sum(rate(http_requests_total{job="api-server"}[5m]))
```

---

## 📚 PromQL 速查表

### 常用函数

| 函数 | 说明 | 示例 |
|-----|------|-----|
| `rate()` | 每秒平均增长率 | `rate(requests[5m])` |
| `irate()` | 瞬时增长率 | `irate(requests[5m])` |
| `increase()` | 时间范围内增量 | `increase(requests[1h])` |
| `sum()` | 求和 | `sum(cpu) by (instance)` |
| `avg()` | 平均值 | `avg(memory)` |
| `max()/min()` | 最大/最小值 | `max(latency)` |
| `count()` | 计数 | `count(up == 1)` |
| `topk()` | 取前N个最大值 | `topk(5, cpu)` |
| `bottomk()` | 取前N个最小值 | `bottomk(5, memory)` |
| `abs()` | 绝对值 | `abs(delta)` |
| `ceil()/floor()` | 向上/下取整 | `ceil(value)` |
| `clamp_max()/clamp_min()` | 限制最大/小值 | `clamp_max(cpu, 100)` |

### 时间函数

| 函数 | 说明 | 示例 |
|-----|------|-----|
| `time()` | 当前时间戳 | `time()` |
| `hour()/minute()` | 提取小时/分钟 | `hour()` |
| `day_of_week()` | 星期几(0=周日) | `day_of_week()` |
| `day_of_month()` | 几号 | `day_of_month()` |

---

## 🐛 常见问题

### 问题1: 查询返回 empty query result

**原因**: 
- 指标不存在
- 标签过滤错误
- 数据还未采集

**排查**:
```promql
# 1. 检查指标是否存在
{__name__=~".*cpu.*"}  # 模糊搜索

# 2. 检查采集目标
up

# 3. 查看所有标签
node_cpu_seconds_total
```

### 问题2: 告警一直触发

**原因**: `for` 持续时间设置过短

**解决**:
```yaml
# 增加持续时间
- alert: HighCPU
  expr: cpu > 80
  for: 10m  # 从5m改为10m
```

### 问题3: 查询超时

**原因**: 查询范围过大、无标签过滤

**优化**:
```promql
# ❌ 慢查询
sum(rate(http_requests_total[1h]))

# ✅ 优化后
sum(rate(http_requests_total{job="api"}[5m]))
```

---

## 📈 下一步

Prometheus 配置完成! 现在可以:
- 👉 [04-Grafana配置与仪表盘](./04-Grafana配置与仪表盘.md) - 可视化你的指标
- 👉 [05-应用集成指南](./05-应用集成指南.md) - 让 Spring Boot 暴露指标

---

**记住**: PromQL 是核心技能,多练习才能熟练!
