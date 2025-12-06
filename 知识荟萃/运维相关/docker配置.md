要将你的前后端分离项目部署到 Docker 容器上，分为以下几个步骤：

---

## ✅ 一、项目准备概览

| 模块       | 技术栈                    | 说明                                       |
| ---------- | ------------------------- | ------------------------------------------ |
| 前端       | Vue3                      | 编译成静态文件，Nginx 服务容器运行         |
| 后端       | Spring Boot2 + JDK11      | 打包为 `jar` 文件，运行在 JDK11 镜像容器中 |
| 数据库     | MySQL 8.0.39              | 使用官方 MySQL 容器                        |
| Docker环境 | Windows 11 Docker Desktop | 多容器用 Docker Compose 管理               |

---

## ✅ 二、目录结构（推荐）

```
project-root/
├── backend/                  # Spring Boot 项目目录
│   ├── Dockerfile
│   └── target/app.jar
├── frontend/                 # Vue3 项目目录
│   ├── Dockerfile
│   └── dist/                 # 打包后前端静态文件
├── docker-compose.yml       # Compose 文件
└── .env                      # 环境变量（可选）
```

---

## ✅ 三、配置详解

### 1️⃣ 后端 Dockerfile（backend/Dockerfile）

```Dockerfile
FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

> 注意：你需要将 Spring Boot 项目通过 `mvn clean package` 打成 jar 放到 `target/app.jar`

---

### 2️⃣ 前端 Dockerfile（frontend/Dockerfile）

```Dockerfile
# 构建阶段
FROM node:18 AS build-stage
WORKDIR /app
COPY . .
RUN npm install && npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf 示例（frontend/nginx.conf）：**

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8080/;
        proxy_set_header Host $host;
    }
}
```

> `/api/` 是你前端请求后端的路径前缀

---

### 3️⃣ docker-compose.yml（项目根目录）

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0.39
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: your_db
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    restart: always

  backend:
    build: ./backend
    container_name: backend
    depends_on:
      - mysql
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/your_db?serverTimezone=Asia/Shanghai
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root
    restart: always

  frontend:
    build: ./frontend
    container_name: frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  mysql-data:
```

---

## ✅ 四、构建 & 启动步骤

### 1️⃣ 打包后端

```bash
cd backend
mvn clean package -DskipTests
```

### 2️⃣ 启动所有容器

在项目根目录执行：

```bash
docker-compose up --build -d
```

### 3️⃣ 访问

* 前端地址：[http://localhost/](http://localhost/)
* 后端接口：[http://localhost:8080/](http://localhost:8080/)

---

## ✅ 五、调试建议

* 容器日志查看：

  ```bash
  docker-compose logs -f backend
  docker-compose logs -f frontend
  docker-compose logs -f mysql
  ```
* 进入容器调试：

  ```bash
  docker exec -it backend bash
  ```

---

## ✅ 六、Vue 请求 Spring Boot 接口说明

如果前端请求 URL 是 `/api/**`，Nginx 会代理到后端服务，需要：

### 修改 Vue 配置或请求路径：

```js
axios.get('/api/user/list')  // 请求转发到 backend 容器
```

---

如果你愿意，我也可以：

* 帮你生成完整的 `Dockerfile` 和 `docker-compose.yml`
* 教你如何一步步打包部署、热更新

需要我继续生成具体文件内容吗？

---



你修改了 `docker-compose.yml` 文件，下一步想启动容器，可以直接运行：

```bash
docker-compose up -d
```

这个命令会：

- 读取你最新修改的 `docker-compose.yml` 配置文件
- 创建并启动对应的容器（如果容器已经存在，会根据配置更新容器，但不会重新构建镜像）
- `-d` 表示后台运行容器



# Docker 基础

---

## 1️⃣ Docker 是什么？为什么要用 Docker？

**类比解释**：

* 想象你要在不同的电脑上运行同一个 Java 应用：

  * 电脑 A 有 Java 11，Linux
  * 电脑 B 有 Java 17，Windows
* 直接复制代码过去可能会报错（依赖不同、环境不同）

**Docker 的作用**：

* Docker 就像一个 **“便携的盒子”**，把你的应用、依赖、配置、操作系统环境都打包好
* 不管在哪台电脑，打开盒子就能运行
* 解决了 **环境不一致、依赖管理复杂** 的问题

---

## 2️⃣ 镜像、容器、仓库概念

| 名称                      | 类比           | 说明                                                |
| ------------------------- | -------------- | --------------------------------------------------- |
| **镜像（Image）**         | “菜谱”         | 一个静态模板，包含操作系统 + 应用程序 + 依赖        |
| **容器（Container）**     | “菜做好端上桌” | 镜像运行起来的实例，可以读写，有状态                |
| **仓库（Registry/Repo）** | “食材超市”     | 存放镜像的地方，比如 Docker Hub，可以上传和下载镜像 |

**关系图示**：

```
仓库(Registry)   <- push/pull ->  镜像(Image)  <-run->  容器(Container)
```

---

## 3️⃣ 安装 Docker

### Windows / Mac

1. 下载 [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. 安装后启动 Docker Desktop
3. 打开 PowerShell / CMD / Terminal 测试：

```bash
docker version
```

### Linux（以 Ubuntu 为例）

```bash
# 更新包
sudo apt update
# 安装依赖
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
# 添加 Docker 官方源
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# 安装 Docker
sudo apt update
sudo apt install docker-ce -y
# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
# 测试
docker version
```

---

## 4️⃣ 最基础的 5 个命令

1. **运行容器**（run）

```bash
docker run -it --name mycontainer ubuntu:22.04 bash
```

* 解释：

  * `-it`：**交互模式**
  * `--name mycontainer`：容器名字
  * `ubuntu:22.04`：镜像
  * `bash`：启动 bash 终端

2. **查看正在运行的容器**（ps）

```bash
docker ps
docker ps -a   # 包含已停止的容器
```

3. **查看本地镜像**（images）

```bash
docker images
```

4. **停止容器**（stop）

```bash
docker stop mycontainer
```

5. **删除容器**（rm）

```bash
docker rm mycontainer
```

---

## 5️⃣ 把 Java 项目打包成 Docker 镜像并运行

假设你有一个 Spring Boot 项目，生成的 jar 文件为 `app.jar`。

### 步骤 1：写 Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
# 基础镜像
FROM openjdk:17-jdk-alpine
# 工作目录
WORKDIR /app
# 复制 jar 文件到容器
COPY target/app.jar app.jar
# 容器启动命令
ENTRYPOINT ["java","-jar","app.jar"]
```

---

### 步骤 2：打包镜像

在项目根目录执行：

```bash
docker build -t my-springboot-app:1.0 .
```

* `-t` 给镜像打名字和标签
* `.` 表示 Dockerfile 所在目录

---

### 步骤 3：运行容器

```bash
docker run -d -p 8080:8080 --name springboot-container my-springboot-app:1.0
```

* `-d`：后台运行
* `-p 8080:8080`：把容器端口映射到本机
* `--name`：给容器起名字





#  **🐳 容器运行参数分类**

端口映射 和 数据卷映射都是 **主机--》容器**



**本身属性 和运行 数据和网络 资源与安全监控** 系统变量

1. 基础运行

* `-d`：后台运行容器（detached）
* **`-it`：交互模式（`-i` 保持输入流，`-t` 分配终端）**
* `--name <name>`：指定容器名称
* `--rm`：容器退出后自动删除
* **`--restart=always|on-failure|no`：设置容器重启策略**



2. 网络配置 -- 有很多网络模式根据场景选择

* `-p 主机端口:容器端口`：端口映射
* `--net <network>`：指定**网络模式（bridge、host、none、自定义）**
* `--hostname <name>`：设置容器主机名

---



在 Docker 中使用 `--add-host` 的核心目的是**在容器内部手动添加静态的主机名与 IP 映射**，解决一些 DNS 解析无法覆盖或不适合的场景。它本质是对容器内 `/etc/hosts` 文件的临时修改，优先级高于 DNS 解析，适合简单、固定的网络映射需求

* **`--add-host <host:ip>`：向 `/etc/hosts` 添加条目**    `--add-host` 适合临时、静态的（**主机和IP的映射**）映射（比如固定 IP 的内部服务）

~~~markdown
如果容器需要访问一个没有注册到 DNS 服务器的内部服务（比如测试环境的临时服务器、本地开发的服务），且该服务的 IP 是固定的
覆盖 DNS 解析的错误结果
**容器访问宿主机的特定服务（跨网络场景）**
~~~

**如果要容器访问主机的服务也可以：**

Docker Desktop 内置了一个特殊的 DNS 名称：
 **`host.docker.internal`** → 自动解析到宿主机 IP



**访问服务：ip + 端口**





3. **存储与挂载**

* `-v 主机路径:容器路径`：挂载数据卷或目录

* **`--mount`：更灵活的挂载方式（支持 type=volume/bind/tmpfs）**

* **`--tmpfs`：挂载临时内存文件系统** 

  `tmpfs` 挂载将数据存储在宿主机的内存中（非磁盘），容器停止后数据自动消失，适合存储临时数据、敏感信息（如密码、会话数据）。

4. ==资源限制== **cpu 内存（计算与存储）**

* `-m / --memory`：限制==内存==使用
* `--memory-swap`：限制内存+swap 总和
* `--cpus`：限制==CPU 核数==
* `--cpu-shares`：设置 CPU 权重
* `--cpuset-cpus`：指定容器可以使用的 CPU 核编号

5. **环境与初始化**（项目环境和系统变量）

* **`-e KEY=VALUE`：设置环境变量**
* **`--env-file`：从文件加载环境变量**
* **`--workdir`：设置容器工作目录**
* **`--entrypoint`：覆盖镜像的默认 ENTRYPOINT** （只有这样能覆盖 与cmd区别）
* `--user`：指定容器运行用户

6. **调试与监控（日志与健康检查）**

* `--log-driver`：设置日志驱动
* `--health-cmd`：健康检查命令
* `--health-interval`：健康检查间隔
* `--health-retries`：失败重试次数
* `--health-timeout`：健康检查超时

**这些镜像文件里有些可以设置**

---



步骤 4：访问应用

* 打开浏览器访问：

```
http://localhost:8080
```

* 如果 Spring Boot 正常启动，就能访问





---

明白啦👌，你只想掌握 **Docker 提供哪些功能模块**，不用记死命令。那我帮你把功能分类总结成一个大纲：

---

# 🐳 Docker 功能分类（只看功能，不带命令）

## 1. 容器管理

* 创建容器
* 启动容器
* 停止容器
* 重启容器
* 删除容器
* **查看容器列表（运行中 / 全部）**
* **查看容器日志**
* **在容器中执行命令**
* **查看容器详细信息（配置、网络、挂载卷等）**
* **查看容器内进程**
* **查看容器资源占用（CPU、内存、网络）**

---

## 2. 镜像管理

* **查看镜像列表**
* 拉取镜像（从仓库下载）
* 推送镜像（上传到仓库）
* 构建镜像（通过 Dockerfile）
* 删除镜像
* **查看镜像构建历史**
* **查看镜像详细信息**

---

## 3. 网络管理

* 查看已有网络
* **创建自定义网络**
* 删除网络
* **查看网络详情（子网、网关、已连接容器等）**
* 将容器连接到网络
* 将容器从网络移除

---

## 4. 数据卷管理（Volume，持久化存储）

* 查看数据卷
* 创建数据卷
* 删除数据卷
* **查看数据卷详情（挂载路径、驱动）**

---

## 5. 系统级管理

* 查看磁盘资源使用情况
* **清理无用资源（容器、镜像、卷、网络）**
* 查看 Docker 实时事件（启动、停止、删除等操作日志流）
* 查看 Docker 系统信息（驱动、版本、存储引擎）
* 查看 Docker 版本

---

# docker 发布

~~~bash
docker login/logout

 构建镜像（同时打1.0.0版本和latest标签，指定Dockerfile路径）
docker build -f "D:\Desktop\docUI\docflow\Dockerfile" `
  -t "senjay557/docflow:1.0.0" `
  -t "senjay557/docflow:latest" `
  "D:\Desktop\docUI\docflow""

推送镜像到Docker Hub（先推版本标签，再推latest标签）
docker push "senjay557/docflow:1.0.0"
docker push "senjay557/docflow:latest"
~~~

# docker file

**基础镜像** 是构建其他镜像的起点，它相当于一个“操作系统模板”。

| 分类               | 指令          | 作用                                             | 示例                                            |
| ------------------ | ------------- | ------------------------------------------------ | ----------------------------------------------- |
| **基础与环境定义** | `FROM`        | 指定基础镜像                                     | `FROM openjdk:17-jdk-alpine`                    |
|                    | `ARG`         | 构建阶段可传入的参数                             | `ARG JAR_FILE=target/app.jar`                   |
|                    | `ENV`         | 设置环境变量（容器运行时可见）                   | `ENV JAVA_OPTS="-Xmx512m"`                      |
| **文件与目录**     | `WORKDIR`     | 设置容器内的工作目录                             | `WORKDIR /app`                                  |
|                    | `COPY`        | 复制文件/目录到镜像                              | `COPY target/app.jar app.jar`                   |
|                    | `ADD`         | 类似 COPY，但支持远程 URL 和解压 tar             | `ADD app.tar.gz /app/`                          |
| **软件与依赖安装** | `RUN`         | 在构建时执行命令（生成新层）                     | `RUN apk add --no-cache curl`                   |
| **容器启动配置**   | `EXPOSE`      | 声明容器对外暴露的端口（仅文档化，不会自动映射） | `EXPOSE 8080`                                   |
|                    | `ENTRYPOINT`  | 容器启动时执行的主命令                           | `ENTRYPOINT ["java","-jar","app.jar"]`          |
|                    | `CMD`         | 给 ENTRYPOINT 传默认参数或替代执行命令           | `CMD ["--spring.profiles.active=dev"]`          |
| **用户与权限**     | `USER`        | 指定运行容器的用户                               | `USER appuser`                                  |
|                    | `VOLUME`      | 定义挂载点，供外部存储绑定                       | `VOLUME /data`                                  |
| **构建优化**       | `LABEL`       | 为镜像添加元数据（版本、作者等）                 | `LABEL maintainer="senjay@example.com"`         |
|                    | `SHELL`       | 修改 RUN 的默认 shell                            | `SHELL ["/bin/bash", "-c"]`                     |
| **多阶段构建**     | `FROM … AS`   | 定义构建阶段别名                                 | `FROM maven:3.9 AS builder`                     |
|                    | `COPY --from` | 从前一阶段复制产物                               | `COPY --from=builder /app/target/app.jar /app/` |

**固定和灵活**：

`CMD` 的意义在于**提供 “默认行为的便捷性” 和 “替换的灵活性”**，而 `ENTRYPOINT` 则专注于 “核心功能的固定性”





# ==常见问题排查==

**查看==日志==**

```bash
docker logs -f springboot-app
docker logs -f mysql
docker logs -f redis
```

**进入==容器（内部==执行命令）调试**

```bash
docker exec -it springboot-app /bin/bash
docker exec -it mysql mysql -uroot -p123456
docker exec -it redis redis-cli
```

**确认==网络==互通**

```bash
docker network ls
docker network inspect backend
```

**清理无效==资源==**

```bash
docker system prune -f
```



## **容器数据持久化方案** 

- 三种方式：**数据卷（volume）**、**绑定挂载（bind mount）**、**临时 tmpfs**。
- **核心点：生产上优先用 volume，避免容器删掉导致数据丢失**，MySQL/Redis 一般直接挂卷。

![image-20250930212627491](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930212627491.png)

**bridge**：默认模式，容器通过虚拟网桥通信，常用于多容器互通。（常用这个）

**host**：直接使用宿主机网络，性能高但端口易冲突。

**none**：不配置网络，隔离性最强





把 Docker 镜像想象成 **叠在一起的透明塑料片**：

- 每一条 Dockerfile 指令都会在现有的叠加上“画一层新的内容”，形成新的快照。
- 这些透明片叠在一起，就是最终镜像。





**常见会生成新层的指令**

- `RUN` → 安装软件、修改文件系统
- `COPY` / `ADD` → 把本地文件加进镜像
- `FROM` → 切换基础镜像，会生成新起点层

**不会生成新层的指令**

- `ENV`、`WORKDIR`、`EXPOSE`、`CMD`、`ENTRYPOINT` 等主要是 **设置元信息**，不会占用额外存储层

~~~
层1: 基础镜像（ubuntu）
层2: RUN apt-get update       → 只记录更新操作产生的文件变化
层3: RUN apt-get install curl → 只记录 curl 安装后的新增文件

~~~

UnionFS 负责**把所有只读层叠加成一个“统一视图”**，让容器启动时看到的是完整文件系统。

容器层再加上**最上面的可写层**（container layer），形成最终容器可用的文件系统。

**为什么需要 UnionFS**：因为 Docker 不能把每一层单独展开成完整文件系统再保存一份，否则浪费空间；UnionFS 让你只存增量层，运行时动态叠加，既节省空间又能保持快照独立性。

---



## 拓展

**系统资源调优**和**容器网络隔离**

### 1. 调整 `vm.max_map_count`（内存区域配置）

- **作用**：`vm.max_map_count` 定义了一个进程能拥有的**最大内存映射区域数量，默认值（65536）在一些内存密集型应用（如 Elasticsearch、Kafka 等分布式系统）中可能不足，容易触发内存异常。**
- **操作逻辑**：通过向 `/etc/sysctl.conf` 写入配置并执行 `sysctl -p` 使其生效，将该参数提升到 655360，从而避免因内存映射区域不足导致的服务故障。

### 2. Docker Macvlan 网络模式配置

- **作用**：Macvlan 是 Docker 的一种网络驱动模式**，允许每个容器直接获得宿主机所在物理网络的独立 IP 地址**，实现容器与外部网络的 “平级” 通信（**无需端口映射**），同时保证容器间网络隔离。
- **操作逻辑**：通过 `docker network create` 命令创建 Macvlan 网络，指定子网（`--subnet`）、IP 范围（`--ip-range`）、网关（`--gateway`）和宿主机物理网卡（`-o parent`），让容器能以独立 IP 直接接入物理网络，适用于需要容器对外提供服务且需网络隔离的场景（如多服务并行部署、模拟多主机网络环境等）。



**jenkins 资源耗太大了，部署的时候要注意不要无脑上**



~~~dockerfile
docker run -d --name MyJenkins \
  -e TZ=Asia/Shanghai \
  -p 8180:8080 \
  -p 50000:50000 \
  -v D:/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \  # Docker socket 映射
  --group-add 0 \  # 添加 root 组权限
  jenkins/jenkins:lts
~~~



---



**将宿主机的nginx.conf复制到容器的Nginx配置目录**

docker cp /opt/archat/nginx.conf archat-frontend:/etc/nginx/nginx.conf****

---



**docker-compose restart backend**

**❌ 只是重启容器，不会重新读取 docker-compose.yml 文件**
**❌ 环境变量在容器创建时就固定了，重启不会更新**
2. **docker-compose up -d（不加参数）**

**❌ Docker Compose 会检查容器配置是否变化**
**❌ 如果镜像ID相同，Docker Compose 认为"没有变化"，不会重建容器**
**❌ 即使 docker-compose.yml 更新了环境变量，也不会应用**
**为什么 --force-recreate 有效：**
**docker-compose up -d --force-recreate**

**✅ 强制删除旧容器**
**✅ 使用最新的 docker-compose.yml 配置创建新容器**
**✅ 新容器会重新读取并注入所有环境变量**

