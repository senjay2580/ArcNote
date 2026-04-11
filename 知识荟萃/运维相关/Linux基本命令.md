![image-20250516140056078](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250516140056078.png)

~~~bash
ls -al 
# -rw-r--r--
│ │  │  │
│ │  │  └── 其他用户（others）的权限：r--（只读）
│ │  └────── 同组用户（group）的权限：r--（只读）
│ └────────── 文件所有者（owner）的权限：rw-（读写）
└──────────── 文件类型：- 表示是普通文件
# d表示是目录
~~~

# 基本命令

**<span style="font-size:1.4em; color:#FF0000;">有些命令可能过时只要知道能干什么就行</span>**

## 查看/搜索

~~~bash
ls 
-a 显示包括隐藏文件
-h human
-l list
~~~



### 文本信息

~~~bash
grep 正则 管道符  ---- 文本搜索工具 在文件中查找符合条件的文本行 也可以从输出流里筛选 利用管道符
awk —— 文本列处理/统计 按列提取数据、统计、格式化输出
sed —— 文本替换/流编辑 对文件或流进行批量替换、删除、插入等操作

echo 在终端中显示参数指定的文字 通常雨重定向一起使用
Linux 允许将命令执行结果 重定向到一个 文件将本应显示在终端上的内容 输出/追加 到指定文件中其中
>表示输出，会覆盖文件原有的内容>>表示追加，会将内容追加到已有文件的末尾
重定向> 和 >> 
~~~



**find（局部递归）**

~~~bash
# 当前目录及子目录查找名为 app.log 的文件
find . -name "app.log"

# 查找所有 .log 文件
find /var/log -type f -name "*.log"

# 查找目录
find /usr/local -type d -name "bin"

find / 如果是根目录就相当于全局查找了（等效利用思想）
~~~

locate **原理**：通过系统事先建立的==索引==（`updatedb`）快速搜索文件名

**用例：**

~~~bash
# 查看日志第2列
awk '{print $2}' /var/log/app.log

# 查看日志中第1列为 WARN 的行
awk '$1=="WARN" {print $0}' /var/log/app.log

# 统计日志中每个用户出现次数
awk '{count[$3]++} END {for(u in count) print u, count[u]}' /var/log/app.log

~~~

~~~bash
# 把日志中 ERROR 替换为 WARN（仅显示，不修改文件）
sed 's/ERROR/WARN/g' /var/log/app.log

# 直接修改文件
sed -i 's/ERROR/WARN/g' /var/log/app.log

# 删除包含 DEBUG 的行
sed '/DEBUG/d' /var/log/app.log

# 显示第10行到第20行
sed -n '10,20p' /var/log/app.log

~~~

#### 实时查看日志

| 命令          | 作用                             | 示例                       |
| ------------- | -------------------------------- | -------------------------- |
| `tail -f**`** | **实时查看文件新增内容**         | `tail -f /var/log/app.log` |
| `less +F`     | 类似 `tail -f`，可以**滚动浏览** | `less +F /var/log/app.log` |

#### ==**统计日志信息**！！！！==

| 命令       | 作用                 | 示例                               |      |
| ---------- | -------------------- | ---------------------------------- | ---- |
| `wc`       | 统计行/单词/字符数   | `wc -l app.log`                    |      |
| `sort`     | 排序                 | `sort app.log`                     |      |
| `uniq**`** | **去重或统计重复**   | `sort app.log           | uniq -c` |      |
| `cut**`**  | **按分隔符提取字段** | `cut -d' ' -f3 app.log`            |      |

#### 查看文件头尾

| 命令   | 作用       | 示例                 |
| ------ | ---------- | -------------------- |
| `head` | 查看前几行 | `head -n 20 app.log` |
| `tail` | 查看后几行 | `tail -n 50 app.log` |

#### ==监控日志变化！！！！==

| 命令          | 作用                                   | 示例                              |
| ------------- | -------------------------------------- | --------------------------------- |
| `watch**`**   | **周期性执行命令**                     | `watch 'tail -n 20 app.log'`      |
| `inotifywait` | 监控文件变化（需要安装 inotify-tools） | `inotifywait -m /var/log/app.log` |

#### ZIP  压缩/处理大日志

| 命令              | 作用                 | 示例                       |
| ----------------- | -------------------- | -------------------------- |
| `gzip` / `gunzip` | **压缩/解压**        | `gzip app.log`             |
| `zcat**`**        | **查看压缩日志内容** | `zcat app.log.gz`          |
| `zgrep**`**       | **在压缩日志中查找** | `zgrep "ERROR" app.log.gz` |

---



### 磁盘信息

~~~bash
df -h （disk free） 剩余空间
du -h [目录名] disk usage 目录下文件大小

# 一般 -h 就是human
~~~

### 进程信息

~~~bash
ps aux process status 查看进程的详细状况 ps 默认只会显示当前用户通过终端启动的应用程序
a：显示终端上的所有进程，包括其他用户的进程
u：显示进程的详细状态
x：显示没有控制终端的进程



top 动态显示运行中的进程并且排序
kill -9 pid 终止指定代号的进程，-9 表示强行终止

~~~

| 功能               | &（后台运行） | nohup + &（后台持久运行） |
| ------------------ | ------------- | ------------------------- |
| 是否立即返回终端   | 是            | 是                        |
| 终端关闭后是否挂掉 | 会挂掉        | 不会挂掉                  |
| 输出默认位置       | 终端          | nohup.out                 |
| 使用场景           | 短任务、调试  | 长任务、服务启动          |





### 查看用户信息

很多都是服务于不同场景的，不要死板

~~~bash
id 用户名 （UID and GID）
who 查看当前所有登录的用户列表
whoami 查看当前登录用户的账户名
~~~

**开发调试时**：用 `&` 即可快速后台运行。

**生产服务器启动服务**：用 `nohup + &` 或者 `systemd`、`supervisord` 管理，保证服务稳定。

### ==网络相关==

## 🧩 一、网络配置与状态查看

| 命令                       | 功能                          | 示例                                |
| -------------------------- | ----------------------------- | ----------------------------------- |
| `ip a` 或 `ip addr`        | 查看 IP 地址                  | `ip a`                              |
| `ip link`                  | 查看/设置网卡状态             | `ip link set eth0 up`               |
| `ip route`                 | 查看路由表                    | `ip route`                          |
| `ifconfig`（旧）           | 查看 IP 和网络接口            | `ifconfig eth0`                     |
| `nmcli`                    | NetworkManager 命令行管理工具 | `nmcli device status`               |
| `hostname` / `hostnamectl` | 查看/设置主机名               | `hostnamectl set-hostname myserver` |
| `ethtool eth0`             | 查看网卡参数（如速率）        | `ethtool eth0`                      |
| `iwconfig`                 | 查看/配置无线网络（WiFi）     | `iwconfig`                          |



------

## 📡 二、连接测试与排查工具

| 命令                     | 功能                                  | 示例                                |
| ------------------------ | ------------------------------------- | ----------------------------------- |
| `ping`                   | 测试连通性                            | `ping baidu.com`                    |
| `traceroute`             | 路由追踪                              | `traceroute google.com`             |
| `mtr`                    | 实时路由诊断（`traceroute` + `ping`） | `mtr baidu.com`                     |
| `telnet`                 | 测试端口是否可达 **测试端口连通性**   | `telnet 192.168.1.1 80`             |
| `nc` / `ncat` / `netcat` | 网络测试工具，连接端口、监听端口      | `nc -vz 192.168.1.1 22`             |
| `curl`                   | 测试 HTTP 请求                        | `curl -I https://example.com`       |
| `wget`                   | 下载文件（也支持测试 HTTP）           | `wget https://example.com/file.zip` |



------

## 🔎 三、端口与服务连接管理

| 命令                                                     | 功能               | 示例            |
| -------------------------------------------------------- | ------------------ | --------------- |
| `ss -tuln`                                               | 查看监听端口       | `ss -tuln`      |
| `ss -anp`                                                | 查看端口与进程关系 | `ss -anp        |
| `netstat -tuln`（旧） **查看网络连接和端口占用**  新的ss | 查看 TCP/UDP 监听  | `netstat -tuln` |
| `lsof -i`                                                | 查看端口占用的进程 | `lsof -i:80`    |



------

## 🔐 四、防火墙与网络安全

### 1. `iptables`（传统防火墙）

| 命令                                            | 功能         |
| ----------------------------------------------- | ------------ |
| `iptables -L`                                   | 查看规则     |
| `iptables -A INPUT -p tcp --dport 80 -j ACCEPT` | 放行 80 端口 |
| `iptables -A INPUT -s 192.168.1.100 -j DROP`    | 屏蔽 IP      |
| `iptables -F`                                   | 清空所有规则 |



> 📝 规则修改后需保存：
>  Ubuntu：`sudo iptables-save > /etc/iptables/rules.v4`

------

### 2. `ufw`（Ubuntu 简化防火墙）

| 命令                            | 功能            |
| ------------------------------- | --------------- |
| `ufw status`                    | 查看状态        |
| `ufw enable` / `ufw disable`    | 启用/禁用防火墙 |
| `ufw allow 22`                  | 允许 SSH 端口   |
| `ufw deny 80`                   | 拒绝 HTTP 端口  |
| `ufw allow from 192.168.1.0/24` | 允许子网访问    |



------

### 3. `firewalld`（CentOS/RHEL）

| 命令                                         | 功能         |
| -------------------------------------------- | ------------ |
| `firewall-cmd --state`                       | 查看状态     |
| `firewall-cmd --list-all`                    | 查看当前规则 |
| `firewall-cmd --add-port=80/tcp --permanent` | 开启端口     |
| `firewall-cmd --reload`                      | 重新加载规则 |



------

## 📦 五、网络抓包与监控

| 命令      | 功能                   | 示例                      |
| --------- | ---------------------- | ------------------------- |
| `tcpdump` | 抓包工具               | `tcpdump -i eth0 port 80` |
| `iftop`   | 实时流量监控（需安装） | `iftop -i eth0`           |
| `nethogs` | 按进程查看流量         | `nethogs`                 |
| `vnstat`  | 查看历史流量统计       | `vnstat`                  |



------

## 🌐 六、DNS/域名工具

| 命令       | 功能        | 示例                 |
| ---------- | ----------- | -------------------- |
| `dig`      | DNS 查询    | `dig google.com`     |
| `nslookup` | DNS 查询    | `nslookup baidu.com` |
| `host`     | 查询域名 IP | `host example.com`   |



------

## 🧳 七、文件传输工具（适合内网/远程）

| 命令    | 功能              | 示例                                          |
| ------- | ----------------- | --------------------------------------------- |
| `scp`   | 安全拷贝文件      | `scp file.txt user@192.168.1.100:/home/user/` |
| `rsync` | 高效同步文件/目录 | `rsync -avz /src/ user@host:/dst/`            |
| `sftp`  | 文件传输（SSH）   | `sftp user@host`                              |
| `ftp`   | FTP 客户端连接    | `ftp 192.168.1.1`                             |





### ==查看日志==

| 命令 / 文件                              | 功能                           | 示例说明                                                   |
| ---------------------------------------- | ------------------------------ | ---------------------------------------------------------- |
| `journalctl`                             | systemd 日志查看（新系统推荐） | `journalctl -xe`、`journalctl -u nginx`                    |
| `/var/log/syslog` 或 `/var/log/messages` | 系统日志                       | `cat /var/log/syslog`                                      |
| `/var/log/auth.log`                      | 登录验证日志                   | `tail -f /var/log/auth.log`                                |
| `/var/log/dmesg`                         | 系统内核日志                   | `dmesg                                                     |
| `/var/log/nginx/`                        | Nginx 访问/错误日志            | `tail -f /var/log/nginx/access.log`                        |
| `/var/log/httpd/`                        | Apache 日志                    | `tail -f /var/log/httpd/error_log`                         |
| `last`                                   | 显示登录历史                   | `last`                                                     |
| `who` / `w`                              | 当前登录用户                   | `who`、`w`                                                 |
| `logrotate`                              | 日志轮转与管理                 | 配置文件：`/etc/logrotate.conf`                            |
| `tail` / `less`                          | 实时查看日志文件               | `tail -f /var/log/syslog`、`less /var/log/nginx/error.log` |





### 查看命令存放位置

~~~bash
which(重要)
# 提示
# /etc/passwd 是用于保存用户信息的文件
# /usr/bin/passwd 是用于修改用户密码的程序which 命令可以查看执行命令所在位置，例如
which ls
# /bin/ls

which useradd
# 输出
# /usr/sbin/useradd
~~~

在 Linux 中，绝大多数可执行文件都是保存在**/bin 、/sbin、/usr/bin、/usr/sbin**
/bin (binary)是二进制执行文件目录，主要用于具体应用  **必须存在，系统启动时可用**
/sbin (system binary)是系统管理员专用的二进制代码存放目录，**主要用于系统管理  包含启动和修复系统的工具**



/usr/bin (user commands for applications后期安装的一些软件  **e.g.常用应用程序和工具，如 `gcc`、`vim`、`python`**
/usr/sbin(super user commands forapplications)超级用户的一些管理程序

---





## 复制/移动（重命名）

~~~bash
cp s d  （src destination）
-l 覆盖文件前提示
-r 递归复制所有子目录和文件

mv s d  （移动文件/目录）  也可以给他们重命名
-i 覆盖文件前提示 
~~~



## 删除

~~~bash
rm 文件/目录
rmdir 删除空目录 不是空目录不删除
-f 强制删除
-r / -R 递归删除
-i 删除前逐个询问确认



~~~

## 



## 正则表达式 

| 正则符号 | 含义说明                                   | 示例       | 匹配内容举例             |
| -------- | ------------------------------------------ | ---------- | ------------------------ |
| `.`      | 匹配任意单个字符（不包括换行）             | `a.b`      | 匹配 `aab`, `acb`        |
| `*`      | 匹配前一个字符0次或多次                    | `lo*l`     | `ll`, `lool`             |
| `+`      | 匹配前一个字符1次或多次（在 `grep -E` 中） | `lo+l`     | `lol`, `loool`           |
| `?`      | 匹配前一个字符0次或1次                     | `lo?l`     | `ll`, `lol`              |
| `^`      | 匹配行开头                                 | `^Hello`   | 匹配以 Hello 开头的行    |
| `$`      | 匹配行结尾                                 | `world$`   | 匹配以 world 结尾的行    |
| `[abc]`  | 匹配集合中任一字符                         | `[aeiou]`  | 匹配元音字母             |
| `[^abc]` | 匹配不在集合中的任一字符                   | `[^0-9]`   | 匹配非数字字符           |
| `[a-z]`  | 匹配范围内的任一字符                       | `[a-zA-Z]` | 匹配字母                 |
| `{n}`    | 匹配前一个字符恰好 n 次                    | `a{3}`     | 匹配 `aaa`               |
| `{n,m}`  | 匹配前一个字符 n 到 m 次                   | `a{2,4}`   | 匹配 `aa`、`aaa`、`aaaa` |

<span style="color:#FF0000;">在脚本或命令中使用时，小心通配符展开导致误操作，建议结合 **`echo` 或 `ls`** 先测试</span>

~~~bash
ls | grep [a-zA-Z]*.txt
~~~

## 压缩/解压缩



~~~bash
# 压缩文件
tar -zcvf 打包文件.tar.gz 被压缩的文件/路径
# 解压缩文件
tar -zxvf 打包文件.tar.gz
# 解压缩到指定路径
tar -zxvf 打包文件.tar.gz -C 目标路径

-z 使用 gzip 进行压缩或解压缩（生成 .gz 格式）
-c 创建压缩包（create）
-x 	解压缩（extract）
-v 显示压缩或解压缩过程（verbose，逐个显示文件名）
-f 	后面跟的是文件名（file）
-C 大写 C：解压时指定解压到的目标目录


~~~



## 用户权限相关命令

### 组管理

**:创建组/删除组 的终端命令都需要通过 sudo执行**

**组信息保存在 /etc/group 文件中**
**etc 目录是专门用来保存 系统配置信息 的目录**

~~~bash
groupadd 组名 
groupdel 组名


cat /etc/group
senjay:x:1000:
组名:密码占位符:GID:组内用户列表




chgrp -R 文件/目录名 递归修改文件/目录的所属组

~~~

### 用户管理

创建用户/删除用户/修改其他用户密码 的终端命令都需要通过 sudo 执行

![image-20250516143515065](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250516143515065.png)

创建用户时，如果忘记添加 **-m选项指定新用户的家目**录 -- 最简单的方法就是删除用户，重新创建
创建用户时，默认会创建一个和用户名同名的组名
用户信息保存在 **/etc/passwd** 文件中



| 用户类型      | 家目录路径     |
| ------------- | -------------- |
| 普通用户      | `/home/用户名` |
| 超级用户 root | `/root`        |

| 作用说明                   | 详细内容                                                    |
| -------------------------- | ----------------------------------------------------------- |
| 1️⃣ 存储用户个人文件         | 包括文档、图片、代码、配置文件等                            |
| 2️⃣ 存放用户配置（隐藏文件） | 如 `.bashrc`, `.profile`, `.ssh/`，用于定义终端行为、别名等 |
| 3️⃣ 作为默认登录路径         | 用户登录 Linux 后默认进入此目录                             |
| 4️⃣ 保障用户隔离             | 每个用户有自己的目录，互不干扰（除非有权限）                |

**主目录**是用户在 Linux 系统中的**主要工作区**。如果**没有主目录**，以下问题可能会出现:
**登录问题:**某些 Linux 配置要求用户登录时必须有主目录，否则可能会导致用户登录失败，特别是在使用图形界面或远程登录(如 SSH)时。
**无法保存用户配置:**用户的配置文件(如.bashrc、.profile)默认存放在主目录中，如果没有主目录，用户的个性化设置(如环境变量、别名等)无法保存。
**影响应用程序运行:**许多应用程序会在主目录下存储临时文件或配置文件(如.vimrc、.ssh/等)，缺少主目录可能导致程序错误运行或无法运行。
**临时使用系统目录:**如果主目录缺失，用户可能被迫将文件保存在系统的其他目录(如/tmp)这会导致数据混乱或安全隐患。





### 用户切换

~~~bash
su - 用户名
exit
~~~



---

## 文件权限

~~~bash
chgrp # chgrp 组名 文件/目录

chown # chown 用户 文件/目录

chmod # chmod 777 文件/目录
4 100 读
2 010 写
1 001 执行


-R 递归修改目录中所有子目录 and 文件

~~~



## 远程管理常用指令

~~~bash
#重新启动操作系统，其中 now 表示现在
$ shutdown -r now

#立刻关机，其中 now 表示现在
$ shutdown now

#系统在今天的 20:25 会关机
$ shutdown 20:25

# 系统再过十分钟后自动关机
$ shutdown +10


# 取消之前指定的关机计划
$shutdown -c


~~~

# ==注意事项！！==

避免直接操作生产服务器:先在测试环境验证  

修改配置前先备份:

**执行命令的时候 一定要考虑会发生什么 不确定久echo 或者 ls 或者 本机快照 测试不要鲁莽**

使用虚拟机开发或者测试的好处就是可以无损测试（因为有快照）





# ==自定义服务 system==

![ac47cf2ea46197fa2fac5f42a5bb64f](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/ac47cf2ea46197fa2fac5f42a5bb64f.jpg)





# ==站长命令==

| 分类        | 命令                           | 功能                            |
| ----------- | ------------------------------ | ------------------------------- |
| 🔧 系统管理  | `top` / `htop`                 | 查看系统资源使用                |
| 🔧 系统服务  | `systemctl`                    | 启动/停止服务（如 nginx/mysql） |
| 🔧 磁盘空间  | `df -h` / `du -sh`             | 查看磁盘/目录占用               |
| 🔧 文件管理  | `tar` / `zip` / `unzip`        | 打包/解压                       |
| 🔧 权限管理  | `chmod` / `chown`              | 修改文件权限                    |
| 🔒 安全      | `ufw` / `iptables`             | 防火墙配置                      |
| 📈 性能监控  | `vmstat` / `iotop` / `iostat`  | 查看 CPU、IO 等性能瓶颈         |
| 📡 网络调试  | `netstat` / `ss` / `lsof -i`   | 查看端口占用情况                |
| 🌐 Web服务器 | `nginx -t` / `nginx -s reload` | 检查配置并重载                  |
| 📦 软件安装  | `apt` / `yum` / `dnf`          | 安装常用工具                    |
| 🐘 数据库    | `mysql` / `psql`               | 登录数据库、管理数据            |
| 📂 站点部署  | `scp` / `rsync` / `git`        | 文件上传同步、版本管理          |

## 建议作为站长安装的工具包

- `htop`：资源监控增强版
- `ncdu`：磁盘使用分析器
- `fail2ban`：SSH 登录防爆破
- `ufw`：简易防火墙
- `nginx` / `apache2`：Web服务器
- `certbot`：HTTPS证书自动管理（Let's Encrypt）

## 站长，可以将以下网络命令常驻掌握：

- `ss -tuln`：端口监听排查
- `iptables` / `ufw`：网络防护配置
- `tcpdump` / `iftop`：网络问题分析
- `ping` / `mtr` / `curl`：网络连通诊断
- `scp` / `rsync`：安全文件同步
- `dig` / `nslookup`：DNS 问题定位



---

# 拓展

![1752068784095](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068784095.png)

![1752068791751](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068791751.png)

![1752068802938](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068802938.png)

![1752068832721](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068832721.png)

![1752068836024](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068836024.png)

![image-20250709215010175](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250709215010175.png)

![1752068846413](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/1752068846413.png)



# 服务器运维

## 安装

~~~bash
ssh username@server_ip
数据库用户 ：'username'@'host'

~~~

安装：包管理器 

配置环境变量 （对于环境）

~~~bash
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
~~~

**启动和配置文件（配置启动策略/后台/密码安全配置/配置文件设置 （如nginx、redis））等等）（对于服务）**





## 项目上传（文件上传）

假设你的项目打包为 **jar**。

### 步骤：

1. 上传 jar：

   Secure Copy

   ```
   scp target/your-app.jar username@server_ip:/home/username/xxx
   ```

2. 启动：

   ```
   nohup java -jar your-app.jar > app.log 2>&1 &
   ```

   - `nohup` 防止退出终端
     - **`> app.log 2>&1` 日志输出**    	
   - `&` 后台运行

3. 查看进程：

   ```
   ps -ef | grep your-app.jar
   ```

4. 停止：

   ```
   kill -9 <PID>
   ```

5. 重启：

   No Hang Up

   ```
   kill -9 <PID>
   nohup java -jar your-app.jar >> app.log 2>&1 &
   ```

**注意重定向和追加**

### 常见问题：

- **端口被占用** → `netstat -tuln | grep 8080` 找到占用进程，`kill -9 PID`。
- **SpringBoot 启动报错** → **检查配置文件（application.yml/properties）数据库和 Redis 地址**

---



**默认 stdout 输出到终端** 

**2>&1**

把 **标准错误（stderr）** 重定向到标准输出（stdout）所在位置（即 app.log）

每个 Linux 进程都会默认打开三个文件描述符（fd）：

| fd   | 名称   | 说明                                    |
| ---- | ------ | --------------------------------------- |
| 0    | stdin  | 程序读取的输入，例如键盘或管道          |
| 1    | stdout | 程序正常输出，例如 `System.out.println` |
| 2    | stderr | 程序错误输出，例如异常信息或报错日志    |

# ==Shell 脚本==

~~~bash
#!/bin/bash
# 1. 注释
echo "Hello, World!"  # 输出文字

# 2. 变量
NAME="SENJAY"
echo "Hello, $NAME"

# 3. 条件判断
if [ -f "/tmp/test.txt" ]; then
  echo "文件存在"
else
  echo "文件不存在"
fi

# 4. 循环
for i in {1..5}; do
  echo "循环 $i"
done

# while 循环
count=1
while [ $count -le 3 ]; do
  echo "count=$count"
  ((count++))  # 自增
done

# 5. 函数
my_func() {
  echo "这是函数"
}
my_func

~~~



**自动拉取代码 → Maven 打包 → 重启应用**

~~~bash
#!/bin/bash
# 部署脚本：pull → maven build → restart

# ======================
# 配置变量
# ======================
APP_NAME="myapp"
APP_DIR="/opt/app/$APP_NAME"
JAR_NAME="myapp.jar"
GIT_REPO="git@github.com:user/project.git"
JAVA_CMD="/usr/bin/java"
MAVEN_CMD="/usr/bin/mvn"
PID_FILE="$APP_DIR/$APP_NAME.pid"

# ======================
# 函数：停止应用
# ======================
stop_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "停止应用 PID $PID"
            kill -9 $PID
        fi
        rm -f $PID_FILE
    else
        echo "应用未运行"
    fi
}

# ======================
# 函数：启动应用
# ======================
start_app() {
    echo "启动应用..."
    nohup $JAVA_CMD -jar $APP_DIR/target/$JAR_NAME > $APP_DIR/nohup.out 2>&1 &
    echo $! > $PID_FILE
    echo "应用已启动 PID $(cat $PID_FILE)"
}

# ======================
# 部署流程
# ======================
echo "====================="
echo "部署开始 $(date)"
echo "====================="

# 进入应用目录
cd $APP_DIR || exit 1

# 拉取代码
echo "拉取最新代码..."
git reset --hard
git pull origin main

# Maven 打包
echo "开始 Maven 打包..."
$MAVEN_CMD clean package -Dmaven.test.skip=true

# 重启应用
stop_app
start_app

echo "====================="
echo "部署完成 $(date)"
echo "====================="

~~~

**自动备份数据库**

~~~bash
#!/bin/bash
# 数据库备份脚本

# ======================
# 配置
# ======================
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASS="yourpassword"
DB_NAME="mydb"
BACKUP_DIR="/opt/backup/mysql"
DATE=$(date +%F_%H%M%S)
RETENTION_DAYS=7

# ======================
# 创建备份目录
# ======================
mkdir -p $BACKUP_DIR

# ======================
# 备份数据库
# ======================
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_$DATE.sql.gz"
echo "开始备份数据库 $DB_NAME 到 $BACKUP_FILE"
mysqldump -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "数据库备份成功"
else
    echo "数据库备份失败" >&2
    exit 1
fi

# ======================
# 清理超过保留天数的备份
# ======================
echo "清理 $RETENTION_DAYS 天前的备份"
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -name "*.sql.gz" -exec rm -f {} \;

~~~

**监控 Java 进程，挂了自动重启**

~~~bash
#!/bin/bash
# Java 进程监控脚本

APP_DIR="/opt/app/myapp"
JAR_NAME="myapp.jar"
JAVA_CMD="/usr/bin/java"
PID_FILE="$APP_DIR/myapp.pid"
CHECK_INTERVAL=60  # 检查间隔（秒）

start_app() {
    echo "$(date) - 启动应用..."
    nohup $JAVA_CMD -jar $APP_DIR/$JAR_NAME > $APP_DIR/nohup.out 2>&1 &
    echo $! > $PID_FILE
    echo "应用已启动 PID $(cat $PID_FILE)"
}

while true; do
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "$(date) - 应用运行正常 PID $PID"
        else
            echo "$(date) - 应用挂掉，自动重启"
            start_app
        fi
    else
        echo "$(date) - PID 文件不存在，启动应用"
        start_app
    fi
    sleep $CHECK_INTERVAL
done

~~~



## ==脚本调试和错误处理==

![image-20251011233945771](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251011233945771.png)





# 查看和分析应用日志（tail、grep ==组合使用==）

**使用场景：**

在 Linux 部署 Java 服务时，日志是**第一手信息来源**：性能瓶颈、异常栈、请求报错、内存溢出……全靠日志定位。

**常见问题与解决**

1. **日志文件太大（几个 G）**
    → 先 `tail -n 1000` 看局部，而不是 `cat` 全部。

2. **日志实时切割（logrotate）看不到历史**  （日志滚动）
    → 去 `logs/` 或 `/var/log/` 下找 `.1`、`.gz` 压缩文件。

   ```
   zcat app.log.1.gz | grep "ERROR"
   ```

3. **权限不足**（！常见问题）
    → 使用 `sudo` 或者修改权限：

   ```
   sudo chmod 644 app.log
   ```

# 定时任务配置（crontab）

Linux 定时任务常用于：

- 定时重启服务
- 定期清理日志
- 定时数据库备份



时间表达式 cron表达式 就是指定时间规则执行脚本 这就是一个定时任务

思路：定时任务如何创建如何查找存储在哪里 如何删除 如何修改 ==cron是否有执行怎么知道呢？==

### 常见问题与解决

**环境问题 和 权限问题**

1. **任务写了但没执行**

   - 问题：crond 服务没启动

   - 解决：

     ```bash
     systemctl start crond
     systemctl enable crond
     ```

2. **命令执行失败**

   - 问题：**cron 不会加载用户的 `~/.bashrc` 环境变量**  （类比就是windows的环境变量）解决：写全路径，比如：

     ```bash
     /usr/bin/java -jar /home/app/demo.jar
     ```

3. **脚本无权限**（常见问题）

   - 解决：

     ```bash
     chmod +x /home/app/restart.sh
     ```



# 防火墙配置和端口开放



1. **firewalld（CentOS7/8, RHEL, Rocky, AlmaLinux 默认）** → `firewall-cmd` 命令
2. **iptables（旧系统或更底层控制）**



* **为什么用**

  * Linux 服务器必须有防火墙，避免所有端口对公网开放。
  * 开发/测试/生产中，常常要临时开放某个端口（如 8080, 3306, 6379）。
* **能做什么**

  * 开启/关闭端口。
  * **限制来源 IP（白名单/黑名单）。**
  * 配置服务（http, https, ssh）。
* **替代方案**

  * **云服务器厂商安全组（阿里云/腾讯云自带）。**
  * **更高级：Nginx/WAF 做应用层防火墙。**

## 

### 🔹 firewalld (`firewall-cmd`)

```bash
# 查看防火墙状态
# 开启防火墙
# 查看已开放端口
# 开放 8080 端口（临时，重启失效）
# 开放 8080 端口（永久，需 reload）
# 移除端口
```



* **问题1**：端口开放了，但还是访问不了。
  ✅ 检查三步：

  1. `ss -tuln | grep 8080` → 服务是否监听？
  2. `firewall-cmd --list-ports` → 端口是否真的开放？
  3. 云服务器安全组是否放行？

* **问题2**：`firewall-cmd: command not found`
  ✅ 安装：`yum install firewalld` 或 `apt install firewalld`。

* **问题3**：规则改了没生效
  ✅ 记得 `firewall-cmd --reload`，iptables 要 `service iptables save`。



* **firewalld** 本质上是 iptables/nftables 的一层封装，提供动态管理规则的接口。
* **iptables** 是 Linux 内核 netfilter 框架的用户态工具，直接操作网络包的流向。
* **为什么有 firewalld**：iptables 配置繁琐且规则一旦应用修改不灵活，firewalld 支持动态规则，便于开发/运维。



* **常见考点**
  * 如何开放 Linux 服务器的端口？
  * firewall-cmd 和 iptables 的区别？
* **追问链路**
1. 你在 Linux 上如何让别人访问你的服务？
* **标准回答**
  * 我会先检查服务是否监听端口，再用 `firewall-cmd --add-port` 开放。
  * firewalld 是 iptables 的封装，动态修改更方便；iptables 更底层，适合复杂策略。



**组合方案：**

开放多端口（例如 Web + 数据库）

只允许某个 IP 访问某个特定服务

端口转发

- **场景**：外网访问 80 端口，内部其实跑在 8080 上

IP 白名单 / 黑名单

- **场景**：只让公司 VPN 出口 IP 访问 SSH，其余全部禁止

限流 / 防暴力破解（Rate Limiting）

日志与审计

- **场景**：监控异常流量，发现被攻击时分析 IP 来源



# 性能排查

**CPU 内存 IO 网络** 

**日志排查**

## CPU 占用高的排查（top + jstack）

### 使用场景

- Java 应用突然 CPU 占用 400%（4 核 CPU 全部打满），导致响应变慢。
- 可能原因：死循环、热点方法执行效率低、GC 线程频繁工作

~~~bash
# 1. 找到 CPU 高的进程
top -c           # 显示进程占用情况，找到 Java 进程 PID

# 2. 查看具体哪个线程占用高
top -Hp <PID>    # H 线程模式，p 指定进程号

jstack <PID> > thread.dump


grep <线程号的十六进制> -A 30 thread.dump

~~~

出现某个方法反复执行 → 热点代码优化。

`GC` 线程反复执行 → 内存不足 / 对象分配过快

## 内存泄漏分析（free + jmap + jhat/VisualVM）

### 使用场景

**启动 JVM 时，OS 会给 JVM 分配虚拟内存空间，JVM 从中划分堆内存（heap）、方法区（Metaspace）、线程栈等。**

**堆之外的 JVM 内存也消耗 OS 内存**





- Java 应用运行一段时间后 **内存逐渐升高**，最后 `OutOfMemoryError`

heap dump 就像拍了一张 JVM 堆的照片，你可以看到每个对象在哪儿、被谁引用、占了多少空间。

~~~bash
# 1. 系统整体内存
free -m

# 2. 生成堆转储（heap dump）
jmap -dump:format=b,file=heap.bin <PID>

# 3. 分析堆文件
jhat heap.bin   # 内置 Web 分析工具（过时）
# 更推荐用 Eclipse MAT 或 VisualVM 打开

~~~

HashMap key 没有释放，导致集合无限增长。

线程池/连接池未正确关闭，导致对象无法回收



## 磁盘 IO 瓶颈（iostat + iotop）

### 使用场景

- 应用响应变慢，但 CPU、内存都正常 → 可能是磁盘 IO 拖慢了。

~~~bash
# 查看 IO 负载
iostat -x 1 5

# 关键指标：
# %util 接近 100% 说明磁盘跑满
# await 越高说明磁盘响应慢

# 实时查看哪个进程 IO 高
iotop

~~~

- 日志写入过多（没做日志切割）。
- MySQL/Redis 落盘慢。
- 磁盘阵列/虚拟机存储性能不足。

## 网络问题排查（netstat + tcpdump 抓包）

### 使用场景

- Java 应用连接数据库超时 / 网络调用失败。

~~~bash
# 查看端口占用情况
netstat -tulnp

# 查看连接数状态
netstat -an | grep 8080 | awk '{print $6}' | sort | uniq -c

# 抓包分析 抓包可用wireshark分析
tcpdump -i eth0 port 3306 -nn -c 100 -w mysql.pcap

~~~

`TIME_WAIT` 太多 → 连接未复用。

数据库端口未放行。

网络丢包/延迟过高

##  日志分析技巧（grep + awk + sort + uniq）

### 使用场景

- 日志文件几百 MB，快速定位错误日志 / 统计请求情况。

~~~bash
# 查看错误日志
grep "ERROR" app.log

# 统计某类错误出现次数
grep "NullPointerException" app.log | wc -l

# 统计日志中请求 IP 排序
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10

# 按时间段过滤日志（10:00 到 11:00）
grep "2025-10-01 10:" app.log > app-10.log

~~~

计某个异常出现次数。

找出攻击来源 IP。

**提取某个接口的请求耗时。**