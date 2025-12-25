# MySQL 数据库备份方案

## 📋 概述

本文档针对 `orphanage` 数据库（数据量小、访问量低、数据重要）提供完整的备份与恢复方案。

---

## 🎯 备份策略

### 推荐方案：全量备份 + Binlog 增量备份

| 备份类型        | 频率        | 保留时间 | 说明       |
| ----------- | --------- | ---- | -------- |
| 每日全量备份      | 每天凌晨 2:00 | 7 天  | 完整数据库快照  |
| Binlog 增量备份 | 每小时       | 7 天  | 记录所有数据变更 |
```ad-info
先给核心结论：同步刷盘和异步刷盘，本质是**数据写入内存后，什么时候刷到磁盘**的两种策略，核心区别在「等不等磁盘写完再返回结果」，直接决定性能和数据安全性，咱们结合开发场景讲清楚，好理解还能直接对应实际使用。

### 一、 先明确前提：为啥要分同步 / 异步刷盘？

不管是数据库（MySQL）、缓存（Redis）、日志（Logback）还是文件操作，数据写入都有个共性：

1. 内存速度（纳秒 / 微秒级）远快于磁盘（毫秒级），差了上万倍；
2. 直接写磁盘会拖慢整体速度，所以默认先写**内存缓冲区**（Buffer），攒一批再一次性写磁盘，这个「攒一批再写」的动作就是**刷盘**；
3. 同步 / 异步，就是决定「刷盘时要不要等磁盘确认写完」。

### 二、 同步刷盘（Sync Flush）

#### 核心定义

发起写请求后，**必须等待数据从内存缓冲区刷到磁盘，且磁盘返回「写入成功」，才给上层（应用 / 用户）返回「操作成功」**。

简单说：写请求 = 写内存 + 刷磁盘（等确认），一步不落，同步等结果。

#### 核心特点

✅ 优点：**数据安全性极高**，只要返回成功，数据一定落地磁盘，就算立刻断电、进程崩溃，数据也不会丢；

❌ 缺点：**性能极低**，每次写都要等磁盘 IO，磁盘的慢速度会直接拖累整个请求响应。

#### 实际开发常用场景（直接对应你会接触的技术）

1. 数据库核心场景：MySQL 的 `innodb_flush_log_at_trx_commit = 1`（默认推荐），事务提交时，redo log 必须同步刷盘，保证事务持久性（ACID 的 D），崩溃不丢数据；
2. 缓存高可靠场景：Redis 的 `appendonlyfsync always`，AOF 日志每次写命令都同步刷盘，最安全但性能最差；
3. 文件操作：Java 的 `FileChannel.force(true)`、Linux 的 `sync()` 命令，强制同步刷盘，确保文件落地。

#### 执行流程（通俗版）

应用写数据 → 写内存 Buffer → 触发同步刷盘 → 等待磁盘写入完成 → 磁盘返回成功 → 应用收到「写成功」响应。

### 三、 异步刷盘（Async Flush）

#### 核心定义

发起写请求后，**只要数据写入内存缓冲区，就直接给上层返回「操作成功」**，刷盘动作交给后台线程异步执行（攒够 Buffer、或到时间再写），不用等磁盘结果。

简单说：写请求 = 写内存（直接返回） + 刷磁盘（后台偷偷做），不等磁盘，先响应再干活。

#### 核心特点

✅ 优点：**性能极高**，摆脱磁盘 IO 的拖累，内存写入就返回，支撑高并发写；

❌ 缺点：**有数据丢失风险**，返回成功后，若没来得及刷盘就断电 / 崩溃，内存里的数据会全部丢失。

#### 实际开发常用场景（对应你接触的技术）

1. 数据库高性能场景：MySQL 的 `innodb_flush_log_at_trx_commit = 0`，事务提交时 redo log 只写内存，后台每秒异步刷盘，性能最好，崩溃最多丢 1 秒数据；
2. 缓存高性能场景：Redis 的 `appendonlyfsync everysec`（默认），AOF 日志每秒异步刷盘，兼顾性能和安全性，最多丢 1 秒数据；`appendonlyfsync no` 则完全依赖系统刷盘，性能最好，丢数据风险最高；
3. 日志输出：Logback/Log4j 的默认输出（非 `immediateFlush=true`），日志先写内存缓冲区，异步刷盘到文件，避免日志 IO 拖慢应用；
4. 消息队列：Kafka/RocketMQ 默认异步刷盘，消息写内存页缓存后返回，后台批量刷盘，支撑高吞吐。

#### 执行流程（通俗版）

应用写数据 → 写内存 Buffer → 立即返回「写成功」→ 后台线程异步判断（Buffer 满 / 到时间）→ 触发刷盘写磁盘 → 磁盘写入完成（应用无需感知）。

### 四、 关键补充：半同步刷盘（折中方案）

实际开发中，纯同步太慢、纯异步太危险，所以大部分中间件都会用「半同步」，本质是**同步 + 异步的折中**，兼顾性能和安全，你大概率会用到，必须提：

1. 核心逻辑：写内存后立即返回，但刷盘有「兜底保障」（比如固定时间 / 固定大小触发），不会无限攒在内存；
2. 典型例子：Redis `everysec`、MySQL `innodb_flush_log_at_trx_commit=2`、Kafka 的`flush.ms`配置，都是半同步，最多丢 1 秒内的数据，是「性能 + 安全」的最优解。
```
### 数据安全保障

```
时间线示例：
凌晨2:00          上午10:00         下午3:00
   │                  │                │
[全量备份]  ──────  [故障] ──────  [恢复]
   │                  │                │
   └── Binlog 记录了这段时间的所有变更 ──┘
                      │
                      ▼
              可以恢复到故障前一刻！
```

---

## 🔧 第一步：开启 MySQL Binlog

### 1.1 修改 MySQL 配置

```bash
# 编辑配置文件
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
# 或
sudo vim /etc/my.cnf
```

添加以下配置：

```ini
[mysqld]
# 开启 binlog
log-bin = /var/log/mysql/mysql-bin
server-id = 1
binlog_format = ROW
expire_logs_days = 7
max_binlog_size = 100M

# 同步刷盘（更安全）
sync_binlog = 1
```

### 1.2 重启 MySQL 并验证

```bash
# 重启 MySQL
sudo systemctl restart mysql

# 验证 Binlog 是否开启
mysql -u root -p -e "SHOW VARIABLES LIKE 'log_bin';"
# 应显示：log_bin | ON
```

---

## 📁 第二步：创建备份脚本

### 2.1 备份脚本 `mysql_backup.sh`

创建文件 `/opt/scripts/mysql_backup.sh`：

```bash
#!/bin/bash
#===============================================================================
# MySQL 全量 + Binlog 增量备份脚本
# 
# 使用方法：
# ./mysql_backup.sh full    # 全量备份 + Binlog 备份
# ./mysql_backup.sh binlog  # 仅 Binlog 增量备份
#===============================================================================

# ==================== 配置区域（请根据实际情况修改） ====================
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASS="123456"           # 生产环境建议使用配置文件
DB_NAME="orphanage"

BACKUP_DIR="/data/backup/mysql"
FULL_DIR="${BACKUP_DIR}/full"
BINLOG_DIR="${BACKUP_DIR}/binlog"
LOG_FILE="${BACKUP_DIR}/backup.log"

# MySQL binlog 目录（根据实际配置修改）
MYSQL_BINLOG_DIR="/var/log/mysql"

# 保留策略
FULL_KEEP_DAYS=7
BINLOG_KEEP_DAYS=7
# ==================== 配置区域结束 ====================

DATE=$(date +%Y%m%d)
TIME=$(date +%H%M%S)
DATETIME=$(date +"%Y-%m-%d %H:%M:%S")

log() {
    echo "[${DATETIME}] $1" | tee -a ${LOG_FILE}
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

# 创建目录
mkdir -p ${FULL_DIR} ${BINLOG_DIR}

# 全量备份（记录 binlog 位置）
do_full_backup() {
    local backup_file="${FULL_DIR}/${DB_NAME}_full_${DATE}_${TIME}.sql.gz"
    local pos_file="${FULL_DIR}/${DB_NAME}_full_${DATE}_${TIME}.pos"
    
    log "开始全量备份..."
    
    mysqldump \
        -h${DB_HOST} \
        -P${DB_PORT} \
        -u${DB_USER} \
        -p${DB_PASS} \
        --single-transaction \
        --master-data=2 \
        --routines \
        --triggers \
        --events \
        --flush-logs \
        ${DB_NAME} 2>/dev/null | gzip > ${backup_file}
    
    if [ $? -eq 0 ] && [ -s ${backup_file} ]; then
        # 提取 binlog 位置信息
        zcat ${backup_file} | grep -m1 "CHANGE MASTER TO" > ${pos_file}
        local size=$(du -h ${backup_file} | cut -f1)
        log "全量备份成功！文件: ${backup_file}, 大小: ${size}"
        log "Binlog 位置已记录到: ${pos_file}"
    else
        rm -f ${backup_file}
        error_exit "全量备份失败！"
    fi
}

# Binlog 增量备份
do_binlog_backup() {
    log "开始 Binlog 增量备份..."
    
    # 刷新 binlog
    mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS} -e "FLUSH LOGS" 2>/dev/null
    
    # 获取当前正在写入的 binlog
    local current_binlog=$(mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS} \
        -e "SHOW MASTER STATUS\G" 2>/dev/null | grep "File:" | awk '{print $2}')
    
    # 复制 binlog 文件（排除当前正在写入的）
    for binlog in ${MYSQL_BINLOG_DIR}/mysql-bin.*; do
        if [ -f "$binlog" ] && [ "$(basename $binlog)" != "$current_binlog" ]; then
            local filename=$(basename $binlog)
            if [ ! -f "${BINLOG_DIR}/${filename}" ]; then
                cp $binlog ${BINLOG_DIR}/
                log "已备份 Binlog: ${filename}"
            fi
        fi
    done
    
    log "Binlog 增量备份完成"
}

# 清理过期备份
cleanup() {
    log "清理过期备份..."
    find ${FULL_DIR} -name "*.sql.gz" -mtime +${FULL_KEEP_DAYS} -delete
    find ${FULL_DIR} -name "*.pos" -mtime +${FULL_KEEP_DAYS} -delete
    find ${BINLOG_DIR} -name "mysql-bin.*" -mtime +${BINLOG_KEEP_DAYS} -delete
    log "清理完成"
}

# 显示统计
show_stats() {
    log "========== 备份统计 =========="
    log "全量备份数量: $(ls -1 ${FULL_DIR}/*.sql.gz 2>/dev/null | wc -l)"
    log "Binlog 文件数量: $(ls -1 ${BINLOG_DIR}/mysql-bin.* 2>/dev/null | wc -l)"
    log "备份目录总大小: $(du -sh ${BACKUP_DIR} | cut -f1)"
    log "=============================="
}

# 主函数
main() {
    BACKUP_TYPE=${1:-full}
    
    log "=============================="
    log "开始 ${BACKUP_TYPE} 备份任务"
    log "=============================="
    
    case ${BACKUP_TYPE} in
        full)
            do_full_backup
            do_binlog_backup
            ;;
        binlog)
            do_binlog_backup
            ;;
        *)
            error_exit "未知类型: ${BACKUP_TYPE}，支持: full, binlog"
            ;;
    esac
    
    cleanup
    show_stats
    log "备份任务完成！"
}

main $@
```

### 2.2 恢复脚本 `mysql_restore.sh`

创建文件 `/opt/scripts/mysql_restore.sh`：

```bash
#!/bin/bash
#===============================================================================
# MySQL 时间点恢复脚本（Point-in-Time Recovery）
# 
# 使用方法：
# ./mysql_restore.sh <全量备份文件> [恢复到的时间点]
# 
# 示例：
# ./mysql_restore.sh /data/backup/mysql/full/orphanage_full_20241225_020000.sql.gz
# ./mysql_restore.sh /data/backup/mysql/full/orphanage_full_20241225_020000.sql.gz "2024-12-25 10:30:00"
#===============================================================================

DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASS="123456"
DB_NAME="orphanage"

BACKUP_DIR="/data/backup/mysql"
BINLOG_DIR="${BACKUP_DIR}/binlog"

FULL_BACKUP=$1
STOP_TIME=$2

if [ -z "$FULL_BACKUP" ]; then
    echo "用法: $0 <全量备份文件> [恢复时间点]"
    echo ""
    echo "示例:"
    echo "  恢复到最新: $0 /path/to/backup.sql.gz"
    echo "  恢复到指定时间: $0 /path/to/backup.sql.gz '2024-12-25 10:30:00'"
    exit 1
fi

if [ ! -f "$FULL_BACKUP" ]; then
    echo "错误: 备份文件不存在: $FULL_BACKUP"
    exit 1
fi

echo "=========================================="
echo "MySQL 时间点恢复"
echo "全量备份: $FULL_BACKUP"
[ -n "$STOP_TIME" ] && echo "恢复到: $STOP_TIME"
echo "=========================================="
read -p "确认恢复？这将覆盖现有数据！(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "步骤 1/3: 恢复全量备份..."
gunzip -c ${FULL_BACKUP} | mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS} ${DB_NAME}

if [ $? -ne 0 ]; then
    echo "错误: 全量备份恢复失败！"
    exit 1
fi
echo "全量备份恢复成功！"

echo ""
echo "步骤 2/3: 获取 Binlog 位置..."
POS_FILE="${FULL_BACKUP%.sql.gz}.pos"
if [ -f "$POS_FILE" ]; then
    BINLOG_FILE=$(cat $POS_FILE | grep -oP "MASTER_LOG_FILE='\K[^']+")
    BINLOG_POS=$(cat $POS_FILE | grep -oP "MASTER_LOG_POS=\K[0-9]+")
    echo "从 Binlog 位置开始: $BINLOG_FILE, 位置: $BINLOG_POS"
else
    echo "警告: 未找到位置文件，将应用所有 Binlog"
    BINLOG_FILE=""
    BINLOG_POS=""
fi

echo ""
echo "步骤 3/3: 应用 Binlog 增量..."
BINLOG_FILES=$(ls -1 ${BINLOG_DIR}/mysql-bin.* 2>/dev/null | sort)

if [ -z "$BINLOG_FILES" ]; then
    echo "没有找到 Binlog 文件，恢复完成（仅全量）"
    exit 0
fi

# 构建 mysqlbinlog 命令
BINLOG_CMD="mysqlbinlog"
[ -n "$BINLOG_FILE" ] && BINLOG_CMD="$BINLOG_CMD --start-position=$BINLOG_POS"
[ -n "$STOP_TIME" ] && BINLOG_CMD="$BINLOG_CMD --stop-datetime='$STOP_TIME'"

# 应用 Binlog
for binlog in $BINLOG_FILES; do
    echo "应用 Binlog: $(basename $binlog)"
    $BINLOG_CMD $binlog | mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS} ${DB_NAME}
done

echo ""
echo "=========================================="
echo "恢复完成！"
[ -n "$STOP_TIME" ] && echo "数据已恢复到: $STOP_TIME"
echo "=========================================="
```

---

## ⚙️ 第三步：部署与配置

### 3.1 创建目录和设置权限

```bash
# 创建脚本目录
sudo mkdir -p /opt/scripts
sudo mkdir -p /data/backup/mysql

# 复制脚本
sudo cp mysql_backup.sh /opt/scripts/
sudo cp mysql_restore.sh /opt/scripts/

# 设置执行权限
sudo chmod +x /opt/scripts/mysql_backup.sh
sudo chmod +x /opt/scripts/mysql_restore.sh

# 设置备份目录权限
sudo chown -R mysql:mysql /data/backup/mysql
```

### 3.2 配置密码文件（推荐，更安全）

```bash
# 创建 MySQL 配置文件
cat > ~/.my.cnf << 'EOF'
[client]
user=root
password=你的密码

[mysqldump]
user=root
password=你的密码
EOF

# 设置权限（仅当前用户可读）
chmod 600 ~/.my.cnf
```

然后修改脚本，移除密码参数：
```bash
# 修改前
mysql -u${DB_USER} -p${DB_PASS} ...

# 修改后（自动读取 ~/.my.cnf）
mysql -u${DB_USER} ...
```


### 3.3 配置定时任务（Crontab）

```bash
# 编辑 crontab
crontab -e

# 添加以下定时任务
# 每天凌晨 2:00 执行全量备份
0 2 * * * /opt/scripts/mysql_backup.sh full >> /data/backup/mysql/cron.log 2>&1

# 每小时执行 Binlog 增量备份
0 * * * * /opt/scripts/mysql_backup.sh binlog >> /data/backup/mysql/cron.log 2>&1
```

验证定时任务：
```bash
# 查看当前用户的定时任务
crontab -l
```

---

## 📖 第四步：使用说明

### 4.1 手动备份操作

```bash
# 执行全量备份（包含 Binlog）
/opt/scripts/mysql_backup.sh full

# 仅执行 Binlog 增量备份
/opt/scripts/mysql_backup.sh binlog
```

### 4.2 恢复操作

#### 场景一：恢复到最新状态

```bash
# 1. 查看可用的全量备份
ls -la /data/backup/mysql/full/

# 2. 选择最近的全量备份进行恢复
/opt/scripts/mysql_restore.sh /data/backup/mysql/full/orphanage_full_20241225_020000.sql.gz
```

#### 场景二：恢复到指定时间点（PITR）

```bash
# 恢复到 2024-12-25 10:30:00 这个时间点
/opt/scripts/mysql_restore.sh /data/backup/mysql/full/orphanage_full_20241225_020000.sql.gz "2024-12-25 10:30:00"
```

#### 场景三：仅恢复全量备份（不应用 Binlog）

```bash
# 直接解压并导入
gunzip -c /data/backup/mysql/full/orphanage_full_20241225_020000.sql.gz | mysql -uroot -p orphanage
```

---

## ✅ 第五步：备份验证

### 5.1 验证备份文件完整性

```bash
# 检查备份文件是否可以正常解压
gunzip -t /data/backup/mysql/full/orphanage_full_*.sql.gz

# 查看备份文件内容（前 50 行）
zcat /data/backup/mysql/full/orphanage_full_*.sql.gz | head -50
```

### 5.2 定期恢复测试（推荐每月一次）

```bash
# 1. 创建测试数据库
mysql -uroot -p -e "CREATE DATABASE orphanage_test;"

# 2. 恢复到测试数据库
gunzip -c /data/backup/mysql/full/orphanage_full_*.sql.gz | mysql -uroot -p orphanage_test

# 3. 验证数据
mysql -uroot -p -e "SELECT COUNT(*) FROM orphanage_test.user;"

# 4. 清理测试数据库
mysql -uroot -p -e "DROP DATABASE orphanage_test;"
```

---

## 📂 备份文件结构

```
/data/backup/mysql/
├── full/                              # 全量备份目录
│   ├── orphanage_full_20241225_020000.sql.gz    # 压缩的全量备份
│   ├── orphanage_full_20241225_020000.pos       # Binlog 位置记录
│   ├── orphanage_full_20241226_020000.sql.gz
│   └── orphanage_full_20241226_020000.pos
├── binlog/                            # Binlog 增量备份目录
│   ├── mysql-bin.000001
│   ├── mysql-bin.000002
│   └── mysql-bin.000003
├── backup.log                         # 备份日志
└── cron.log                           # 定时任务日志
```

---

## ⚠️ 注意事项

### 安全建议

1. **密码安全**：生产环境使用 `~/.my.cnf` 存储密码，避免在脚本中明文存储
2. **权限控制**：备份目录权限设置为 `700`，仅允许备份用户访问
3. **异地备份**：重要数据建议同步到远程存储（如 OSS、S3）

### 常见问题

| 问题 | 解决方案 |
|-----|---------|
| Binlog 未开启 | 检查 MySQL 配置，确保 `log-bin` 已配置 |
| 备份文件为空 | 检查数据库连接参数和权限 |
| 恢复失败 | 确认目标数据库存在，检查用户权限 |
| 磁盘空间不足 | 调整 `FULL_KEEP_DAYS` 和 `BINLOG_KEEP_DAYS` |

### 监控建议

```bash
# 添加到监控脚本，检查最近备份是否成功
LATEST_BACKUP=$(ls -t /data/backup/mysql/full/*.sql.gz 2>/dev/null | head -1)
if [ -z "$LATEST_BACKUP" ]; then
    echo "警告：未找到备份文件！"
elif [ $(find "$LATEST_BACKUP" -mtime +1 | wc -l) -gt 0 ]; then
    echo "警告：最近备份超过 24 小时！"
fi
```

---

## 🔄 快速参考

| 操作 | 命令 |
|-----|------|
| 全量备份 | `/opt/scripts/mysql_backup.sh full` |
| 增量备份 | `/opt/scripts/mysql_backup.sh binlog` |
| 恢复到最新 | `/opt/scripts/mysql_restore.sh <备份文件>` |
| 恢复到指定时间 | `/opt/scripts/mysql_restore.sh <备份文件> "YYYY-MM-DD HH:MM:SS"` |
| 查看备份日志 | `tail -f /data/backup/mysql/backup.log` |
| 查看备份文件 | `ls -la /data/backup/mysql/full/` |
