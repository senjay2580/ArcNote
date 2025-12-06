# Grafana 配置与仪表盘

## 📋 文档导航
[← 上一篇：03-Prometheus配置](./03-Prometheus配置.md) | [下一篇：05-应用集成指南 →](./05-应用集成指南.md)

---

## 🎯 本章目标

- ✅ 掌握 Grafana 基础操作
- ✅ 导入社区仪表盘
- ✅ 自定义仪表盘制作
- ✅ 变量与模板配置
- ✅ 告警可视化

---

## 🚀 快速开始

### 1. 首次登录

访问 `http://localhost:3000`

**默认账号**:
- 用户名: `admin`
- 密码: `admin123` (或在 docker-compose 中配置的密码)

**首次登录建议**:
1. 修改默认密码(Settings → Profile → Change Password)
2. 设置时区(Settings → Preferences → Timezone: `Asia/Shanghai`)
3. 设置主题(Settings → Preferences → Theme: `Dark/Light`)

---

## 📊 导入社区仪表盘(5分钟上手)

### 方式一: 通过 ID 导入(推荐)

**步骤**:
1. 点击左侧 **"+"** → **Import**
2. 输入仪表盘 ID
3. 点击 **Load**
4. 选择数据源: **Prometheus**
5. 点击 **Import**

### 核心仪表盘推荐

#### 1. Node Exporter Full (ID: 1860)
**监控内容**: Linux 系统全面监控
- CPU 使用率、负载
- 内存使用、Swap
- 磁盘 I/O、使用率
- 网络流量、TCP 连接

**截图预览**: https://grafana.com/grafana/dashboards/1860

#### 2. MySQL Overview (ID: 7362)
**监控内容**: MySQL 核心指标
- 查询 QPS/TPS
- 连接数、线程数
- InnoDB 缓冲池
- 慢查询统计

#### 3. Redis Dashboard (ID: 11835)
**监控内容**: Redis 性能
- 内存使用、碎片率
- 命中率、Key 数量
- 客户端连接数
- 持久化状态

#### 4. Spring Boot 2.1 Statistics (ID: 12900)
**监控内容**: Spring Boot 应用
- JVM 堆内存、GC
- HTTP 请求 QPS
- 数据库连接池
- Tomcat 线程池

#### 5. JVM (Micrometer) (ID: 4701)
**监控内容**: JVM 详细监控
- 堆内存分代使用
- GC 停顿时间分布
- 类加载统计
- 线程状态

### 方式二: 通过 JSON 导入

**使用场景**: 自定义仪表盘备份/迁移

**步骤**:
1. 点击 **Import** → **Upload JSON file**
2. 选择 `.json` 文件
3. 配置变量和数据源
4. 点击 **Import**

---

## 🎨 自定义仪表盘制作

### 1. 创建新仪表盘

**步骤**:
1. 点击左侧 **"+"** → **Dashboard**
2. 点击 **Add new panel**
3. 配置面板

### 2. Panel 类型详解

#### Time series (时间序列图)
**适用场景**: 趋势展示(CPU、内存、QPS)

**配置示例**:
```
Query: rate(http_server_requests_seconds_count[5m])
Legend: {{method}} {{uri}}
```

**显示设置**:
- Graph styles: Lines / Bars / Points
- Line width: 2
- Fill opacity: 10
- Show points: Never

#### Stat (单值面板)
**适用场景**: 当前值展示(在线用户数、当前QPS)

**配置示例**:
```
Query: sum(up{job="node-exporter"})
Calc: Last
Unit: short
```

**阈值设置**:
- 0-3: 红色
- 3-5: 黄色
- 5+: 绿色

#### Gauge (仪表盘)
**适用场景**: 百分比展示(CPU使用率、内存使用率)

**配置示例**:
```
Query: (1 - avg(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
Min: 0
Max: 100
Thresholds: 0,70,85
```

#### Table (表格)
**适用场景**: 多维度数据对比

**配置示例**:
```
Query: topk(10, rate(http_server_requests_seconds_count[5m]))
Format: Table
Transform: Organize fields
```

#### Heatmap (热力图)
**适用场景**: 请求延迟分布

**配置示例**:
```
Query: 
sum(rate(http_server_requests_seconds_bucket[5m])) by (le)
Format: Heatmap
Legend format: {{le}}
```

---

## 🔧 PromQL 查询实战

### 1. 系统资源查询

#### CPU 使用率
```promql
# 总体 CPU 使用率
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 分核心 CPU 使用率
100 - (irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100)

# CPU 负载
node_load1  # 1分钟负载
node_load5  # 5分钟负载
node_load15 # 15分钟负载
```

#### 内存使用率
```promql
# 内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 可用内存
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024  # 转换为 GB

# Swap 使用
node_memory_SwapTotal_bytes - node_memory_SwapFree_bytes
```

#### 磁盘使用率
```promql
# 磁盘使用率
(1 - (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes)) * 100

# 磁盘 I/O
rate(node_disk_read_bytes_total[5m])  # 读速率
rate(node_disk_written_bytes_total[5m])  # 写速率

# IOPS
rate(node_disk_reads_completed_total[5m])
rate(node_disk_writes_completed_total[5m])
```

#### 网络流量
```promql
# 入站流量(MB/s)
rate(node_network_receive_bytes_total[5m]) / 1024 / 1024

# 出站流量(MB/s)
rate(node_network_transmit_bytes_total[5m]) / 1024 / 1024

# TCP 连接数
node_netstat_Tcp_CurrEstab
```

### 2. MySQL 查询

```promql
# MySQL 运行状态
mysql_up

# QPS (每秒查询数)
rate(mysql_global_status_questions[5m])

# TPS (每秒事务数)
rate(mysql_global_status_commands_total{command="commit"}[5m]) + 
rate(mysql_global_status_commands_total{command="rollback"}[5m])

# 慢查询增长率
rate(mysql_global_status_slow_queries[5m])

# 连接数
mysql_global_status_threads_connected

# 最大连接数
mysql_global_variables_max_connections

# 连接使用率
mysql_global_status_threads_connected / mysql_global_variables_max_connections * 100

# InnoDB 缓冲池命中率
(mysql_global_status_innodb_buffer_pool_read_requests / 
(mysql_global_status_innodb_buffer_pool_read_requests + 
 mysql_global_status_innodb_buffer_pool_reads)) * 100

# 表锁等待
rate(mysql_global_status_table_locks_waited[5m])
```

### 3. Redis 查询

```promql
# Redis 运行状态
redis_up

# 内存使用量(MB)
redis_memory_used_bytes / 1024 / 1024

# 内存使用率
redis_memory_used_bytes / redis_memory_max_bytes * 100

# Key 总数
redis_db_keys

# 命中率
rate(redis_keyspace_hits_total[5m]) / 
(rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) * 100

# 客户端连接数
redis_connected_clients

# 每秒操作数
rate(redis_commands_processed_total[5m])

# 网络流量
rate(redis_net_input_bytes_total[5m]) / 1024 / 1024  # 入站 MB/s
rate(redis_net_output_bytes_total[5m]) / 1024 / 1024 # 出站 MB/s

# 内存碎片率
redis_mem_fragmentation_ratio
```

### 4. Spring Boot 应用查询

```promql
# 应用运行状态
up{job="spring-boot"}

# JVM 堆内存使用率
jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"} * 100

# GC 次数
rate(jvm_gc_pause_seconds_count[5m])

# GC 总耗时占比
rate(jvm_gc_pause_seconds_sum[5m]) * 100

# 线程数
jvm_threads_live_threads

# HTTP 请求 QPS
sum(rate(http_server_requests_seconds_count[1m])) by (uri)

# 接口平均响应时间
rate(http_server_requests_seconds_sum[5m]) / 
rate(http_server_requests_seconds_count[5m])

# 接口 P99 响应时间
histogram_quantile(0.99, 
  sum(rate(http_server_requests_seconds_bucket[5m])) by (le, uri)
)

# 接口错误率
sum(rate(http_server_requests_seconds_count{status=~"5.."}[5m])) / 
sum(rate(http_server_requests_seconds_count[5m])) * 100

# 数据库连接池使用率
hikaricp_connections_active / hikaricp_connections * 100

# Tomcat 线程使用率
tomcat_threads_busy_threads / tomcat_threads_config_max_threads * 100
```

---

## 🎛️ 变量与模板

### 1. 为什么需要变量?

**场景**: 多台服务器、多个应用,不想创建多个仪表盘

**解决**: 使用变量动态切换监控对象

### 2. 创建变量

**步骤**:
1. 仪表盘设置(右上角齿轮图标) → **Variables** → **Add variable**

#### 示例1: 实例选择器
```
Name: instance
Label: 服务器
Type: Query
Data source: Prometheus
Query: label_values(node_cpu_seconds_total, instance)
Refresh: On Dashboard Load
Multi-value: true  # 支持多选
Include All: true  # 包含全选选项
```

#### 示例2: 应用选择器
```
Name: application
Label: 应用
Type: Query
Query: label_values(jvm_memory_used_bytes, application)
```

#### 示例3: 接口选择器
```
Name: uri
Label: 接口
Type: Query
Query: label_values(http_server_requests_seconds_count{application="$application"}, uri)
```

### 3. 在查询中使用变量

```promql
# 单个变量
node_cpu_seconds_total{instance="$instance"}

# 多个变量
http_server_requests_seconds_count{application="$application", uri="$uri"}

# 正则匹配(Multi-value)
node_cpu_seconds_total{instance=~"$instance"}

# 全选时的聚合
sum by(instance) (node_cpu_seconds_total{instance=~"$instance"})
```

### 4. 变量链式依赖

**场景**: 先选环境 → 再选应用 → 最后选接口

```
变量1: env
Query: label_values(up, env)

变量2: application
Query: label_values(up{env="$env"}, application)

变量3: uri
Query: label_values(http_server_requests_seconds_count{application="$application"}, uri)
```

---

## 📐 高级配置技巧

### 1. 面板阈值与颜色

**配置路径**: Panel → Overrides → Add field override

**示例: CPU 使用率阈值**
```
Thresholds:
  - 0: Green (正常)
  - 70: Yellow (警告)
  - 85: Red (严重)

Color scheme: From thresholds
```

### 2. 单位格式化

| 数据类型 | 单位设置 | 显示效果 |
|---------|---------|---------|
| 字节 | `bytes(IEC)` | 1024 → 1 KiB |
| 百分比 | `percent(0.0-1.0)` | 0.856 → 85.6% |
| 时间 | `seconds(s)` | 1.5 → 1.5s |
| QPS | `ops/s` | 1234 → 1.23K ops/s |
| 货币 | `currency(CNY)` | 100 → ¥100 |

### 3. 数据转换(Transform)

#### Reduce (聚合)
**场景**: 多个指标取最大值/平均值
```
Transform: Reduce
Calculation: Max / Mean / Last
```

#### Organize fields (字段重组)
**场景**: 隐藏不需要的列、重命名
```
Transform: Organize fields
Hide: __name__, job
Rename: Value → CPU使用率(%)
```

#### Filter by value (值过滤)
**场景**: 只显示错误率>5%的接口
```
Transform: Filter data by value
Condition: Greater than
Value: 5
```

### 4. 告警规则(旧版)

**注意**: Grafana 告警建议迁移到 AlertManager,这里仅做了解

**配置步骤**:
1. Panel 编辑 → Alert 标签页
2. 创建告警规则
   - Evaluate every: 1m
   - For: 5m
   - Condition: `WHEN avg() OF query(A, 5m, now) IS ABOVE 80`
3. 配置通知渠道(Notification channels)

---

## 📊 实战案例: 创建综合监控面板

### 案例: ArcHat 系统总览仪表盘

**面板布局**:
```
┌─────────────────────────────────────────┐
│ Row 1: 系统概览(4个 Stat 面板)            │
├──────────┬──────────┬──────────┬─────────┤
│ 在线服务  │  总QPS   │ 错误率   │ 平均延迟 │
├──────────┴──────────┴──────────┴─────────┤
│ Row 2: 系统资源(2个 Graph 面板)           │
├──────────────────┬──────────────────────┤
│ CPU & 内存        │ 网络流量              │
├──────────────────┴──────────────────────┤
│ Row 3: 数据库监控(2个 Graph 面板)         │
├──────────────────┬──────────────────────┤
│ MySQL QPS/TPS    │ Redis 命中率          │
├──────────────────┴──────────────────────┤
│ Row 4: 应用监控(2个 Graph 面板)           │
├──────────────────┬──────────────────────┤
│ JVM 内存/GC      │ 接口TOP10             │
└──────────────────┴──────────────────────┘
```

### JSON 导出(可复用)

**导出步骤**:
1. 仪表盘右上角 → Share → Export
2. Save to file
3. 备份到 `monitoring/grafana/provisioning/dashboards/`

**自动加载配置** (已在 02 章节配置):
```yaml
# monitoring/grafana/provisioning/dashboards/dashboards.yml
apiVersion: 1
providers:
  - name: 'default'
    folder: ''
    type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

---

## 🔍 常用快捷操作

### 时间范围快捷键
- `t + t`: 时间选择器
- `t + z`: Zoom out
- `t + left/right`: 向前/后移动

### 查看快捷键
- `d + k`: 显示所有快捷键
- `f`: 全屏
- `Ctrl + S`: 保存仪表盘
- `Esc`: 退出全屏/退出编辑

### 查询快捷键
- `Ctrl + Space`: PromQL 自动补全
- `Shift + Enter`: 执行查询

---

## 🎯 性能优化建议

### 1. 查询优化
```
❌ 慢查询:
sum(rate(http_requests_total[1h]))  # 时间范围过长

✅ 优化后:
sum(rate(http_requests_total{job="api"}[5m]))  # 添加标签过滤
```

### 2. 刷新间隔
```
低频数据: 5m-10m (如磁盘使用率)
中频数据: 1m-5m (如CPU、内存)
高频数据: 10s-30s (如QPS、错误率)
```

### 3. 数据点限制
```
Settings → Query options:
Max data points: 1000 (默认值合理)
Min interval: 15s (避免过于频繁查询)
```

---

## 🐛 常见问题

### 问题1: "No data" 或查询超时

**原因**: 查询范围过大、标签过滤不足

**解决**:
1. 添加 `{job="xxx"}` 过滤
2. 缩短时间范围 `[5m]` → `[1m]`
3. 增加查询超时: Data Source Settings → Query timeout: 60s

### 问题2: 仪表盘变量不生效

**排查**:
```
1. 变量查询是否返回结果?
   Settings → Variables → 点击变量 → Preview of values

2. 查询中是否正确使用?
   {instance="$instance"}  ✅
   {instance=$instance}    ❌ (缺少引号)

3. Multi-value 是否正确使用?
   {instance=~"$instance"}  ✅ (需要 =~ 正则匹配)
```

### 问题3: 图表不显示图例

**解决**:
```
Panel → Legend:
  ✅ Show legend
  ✅ Display mode: List / Table
  ✅ Placement: Bottom / Right
```

---

## 📚 进阶学习资源

- **Grafana 官方文档**: https://grafana.com/docs/
- **社区仪表盘**: https://grafana.com/grafana/dashboards/
- **PromQL 教程**: https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Grafana Playground**: https://play.grafana.org/

---

## 📈 下一步

Grafana 配置完成! 现在可以:
- 👉 [05-应用集成指南](./05-应用集成指南.md) - Spring Boot 应用监控集成
- 👉 [06-告警配置](./06-告警配置.md) - 配置告警规则

---

**记住**: 好的仪表盘应该「一目了然」,不要堆砌过多 Panel!
