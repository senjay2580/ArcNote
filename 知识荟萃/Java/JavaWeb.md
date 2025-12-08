**based on 408 计网**

#   <font size=8 color =red >主要内容由 《servlet》（Tomcat）、《HTTP协议》、《docker与k8s基础入门》、《web发展史与现代web开发技术流程》、《云服务使用》！ 构成</font>

# ==Web==

物理服务器本质上是一台高性能计算机，但需要**服务器软件（Web 服务器、数据库服务器等）**来处理和响应请求。原因如下：

- **操作系统本身不会直接处理 Web 请求**，需要 Web 服务器软件（如 Apache、Nginx）解析 HTTP 请求。
- **Web 服务器提供 HTTP 解析、静态文件托管、反向代理等功能**，使用户能访问网站。
- **服务器软件（如 MySQL、Redis）管理数据库、缓存，提高网站性能。**



#### **前后端分离时代（2010s）**

- 代表技术：**JavaScript（AJAX、jQuery）、前端框架（React、Vue）、后端 API（Node.js、Django、Spring Boot）**
- 主要特点：
  - 前端和后端分离，前端通过 AJAX 或 API 请求后端数据。
  - RESTful API、GraphQL 等成为主流。
  - 部署方式：
    - **前端**：静态资源（HTML、CSS、JS）放在 CDN 或 Nginx。
    - **后端**：API 服务器（Node.js、Django、Spring Boot）运行在云端。

**云计算 & 容器化时代（2020s---？ ）**

- 代表技术：**Docker、Kubernetes、Serverless、微服务架构**

- 主要特点：

  - Web 应用采用 **容器化（Docker）**，通过 Kubernetes 进行自动扩展。

  - 无服务器（Serverless）架构，如 AWS Lambda、Vercel 让前端和后端资源更灵活部署。

  - 前端框架（如 Next.js、Nuxt.js）支持静态生成（SSG）和服务器渲染（SSR）。

  - 部署方式

    ：

    - **前端**：托管到 CDN（如 Cloudflare、Vercel、Netlify）。
    - **后端**：运行在 Docker 容器或 Kubernetes 集群。



#### **容器化运行在云服务器上**

- **容器化的应用** 需要托管在虚拟化或物理的 **云服务器** 上。通过云服务器提供的计算、存储和网络资源，容器能够快速启动并高效运行。
- **容器管理平台（如 Kubernetes）** 也运行在云服务器上，管理集群中的容器和资源分配，确保容器的弹性伸缩、负载均衡和高可用性。



是的，**用户最终使用的 Web 服务**通常是由运维人员（或 DevOps 工程师）部署的 Docker 镜像，经过一系列构建、测试和部署的流程。

# Docker 与Kubernetes基本关系

![image-20250203224739767](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250203224739767.png)

docker 就是打包这些环境 

操作系统分为==内核空间==和==用户空间==（应用程序就运行在这里）所以可以阉割操作系统，只需要利用用户空间

 ![image-20250203225221552](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250203225221552.png)

CLI（命令行接口）-Server 架构是一种通过命令行接口与服务进行交互的架构模式。在这种架构下，用户通过命令行工具（CLI）与后端的服务器进行通信，提交命令并获得结果。

- **CLI**：用户通过终端（如 Bash 或 PowerShell）输入命令来与系统交互。这些命令通常是操作系统或应用程序的接口，用来管理、查询或配置系统。
- **Server**：是提供实际服务的应用或系统，通常是处理业务逻辑、数据存储或其他后台功能。Server 负责处理来自 CLI 的请求，执行相应的操作并返回结果。

**集群**（Cluster）指的是由多个计算机或计算资源组成的一个集合，这些计算资源协同工作，以提供高可用性、负载均衡、扩展性等特点。集群中的节点（计算机、服务器、虚拟机等）通常彼此相互连接，并共同完成某项任务或服务。

集群的核心特征是 **资源共享** 和 **协调工作**，各个节点之间可以通过网络进行通信并协同工作，形成一个统一的系统。



**k8s 就是一个中间件==中间件类似代理这也是个常见的   业务处理思路==**

pod是k8s 的**最小调度单位**



### **1. 开发阶段**

1. **开发人员创建代码**：开发人员在本地或开发环境中编写应用代码。
2. **Docker 镜像构建**：开发人员基于自己的开发环境，通过 `Dockerfile` 构建出一个镜像。这个镜像包含了应用代码及其所有依赖（如操作系统、数据库客户端、库、环境变量等）。
3. **镜像推送到镜像仓库**：开发人员将镜像推送到一个中央的镜像仓库（如 Docker Hub、私有仓库等），这样运维人员可以从镜像仓库中拉取镜像并进行部署。

### **2. 测试阶段**

1. **测试环境镜像**：运维人员在 **测试环境** 中拉取镜像，进行集成测试、负载测试等。
2. **镜像验证与修复**：如果测试中发现问题，开发人员可能会修改代码，并重新构建镜像，推送到镜像仓库，直到通过测试。
3. **验证镜像一致性**：由于镜像是不可变的，测试和生产环境使用的镜像是一致的，确保在生产环境中不会出现与开发环境不同的问题。

### **3. 生产环境部署**

1. **运维人员拉取镜像**：当镜像在测试环境中通过验证后，运维人员会从镜像仓库拉取经过验证的镜像。
2. **部署到生产环境**：运维人员将镜像部署到 **生产环境** 中，通过 Docker 容器运行它。生产环境中的 Web 服务实际上就是这个容器中的应用。

### **4. 用户访问 Web 服务**

- 用户通过浏览器访问 Web 服务时，实际上是与运行在 **生产环境** 中的 Docker 容器交互。用户访问的应用就是通过运维人员部署的镜像和容器提供的 Web 服务。
- 这个镜像和开发环境中使用的镜像一致，只是部署环境和配置可能有所不同（例如生产环境可能需要更高的性能配置或进行安全加固等）。



---

### **Docker 决定生产环境配置：**

- Docker 在生产环境中决定了配置：
  - 在 **生产环境** 中运行的 Web 应用是通过 Docker 容器来管理的。在这个环境中，**Docker 镜像** 会封装所有的依赖、运行时环境和应用代码。
  - 生产环境中的 Web 应用在 **Docker 容器内**运行时，Docker 会确保应用和其运行时环境（比如 Java 版本、依赖库等）是固定一致的，**与用户的本地配置无关**。
  - 因此，**生产环境中 Docker 里的 Java 版本** 是由运维人员、开发团队或者 DevOps 团队在 Docker 镜像中指定的，而不是用户决定的。用户访问时，只会接触到 Web 服务的功能和表现，而 Docker 容器内的配置是隔离的。

### **用户决定的版本（本地环境）：**

- **用户本地环境（客户端）**：
  - 如果说 **用户** 是指访问 Web 应用的终端用户（比如使用浏览器的用户），那么他们的本地环境（如浏览器版本、操作系统、Java 版本等） **不会直接影响 Docker 容器内的 Java 版本**。
  - 用户通过浏览器访问 Web 应用时，浏览器会向 Web 服务器发起请求，服务器端的响应和计算是在 **服务器的 Docker 容器** 中进行的，**与用户本地的配置无关**。
- **用户的本地 Docker 配置**（开发者环境）：如果用户自己在本地开发、调试或者运行 Docker 容器，那么他们可以选择自己本地的 Docker 环境配置，包括指定容器中运行的 Java 版本（例如 Java 8 或 Java 17）。在这种情况下，Docker 容器内的配置由本地 Docker 环境和 Dockerfile 来决定。



# ==应用程序打包==

### 1. **应用程序代码**

- **源代码或已编译的二进制文件**：对于 Java 程序，这通常是 `.class` 文件或者 `.jar` 文件；对于其他语言（如 Python、Node.js 等），则是脚本或编译后的代码。
- 代码可以是一个单独的应用程序或多个模块/组件的组合。

### 2. **依赖库**

- 应用程序往往依赖于一些外部库（如 Java 的 `*.jar` 文件、Python 的第三方模块、Node.js 的 `node_modules` 目录等）。打包时，需要将这些依赖包含在内。
- 有些工具（如 **Maven**、**Gradle**、**npm**、**pip**）能够自动管理依赖，并将它们打包到应用中（例如 **Fat JAR** 或 **Uber JAR**）。

### 3. **配置文件**

- 应用程序可能需要一些配置文件来定制其运行环境，例如：
  - **数据库配置**：例如数据库连接字符串、用户名和密码等。
  - **日志配置**：日志文件路径、日志级别等。
  - **环境设置**：如应用的运行环境（开发、测试、生产等）配置。
  - **外部API密钥或认证信息**等。
- 配置文件可以包括 `.xml`、`.json`、`.properties`、`.yml` 等格式。

### 4. **静态资源**

- 如果是 Web 应用程序，静态资源如 HTML、CSS、JavaScript 文件、图像、字体等通常会被打包。
- 对于桌面应用，可能包含 UI 资源，如图标、模板、用户界面设计文件等。

### 5. **本地依赖和运行时环境**

- 一些应用程序==需要==特定的运行时环境或本地依赖，如 JDK、Node.js、Python 解释器等。**在 Docker 中打包时，这些运行时环境可以包含在镜像内。**

- 例如：

  - **Java 程序**：可能包含特定版本的 **JRE** 或 **JDK**。
  - **Node.js 应用**：可能包括 **Node.js** 和必要的 **npm** 包。
  - **Python 应用**：可能包括必要的 Python 库。

  

  - **Docker 容器中的运行环境**是独立于宿主机的，所以即使宿主机（本地环境）使用的是 **Java 8**，如果 Docker 容器中包含 **Java 17**，那么容器会使用 **Java 17** 来运行应用程序。

    具体来说，Docker 是通过 **容器隔离** 来确保每个容器都有自己独立的运行时环境。容器内的依赖、配置和运行时环境（如 JDK）是容器内部定义的，和宿主机的环境相互独立。

### 6. **平台特定的依赖**

- 如果你的应用需要特定的系统库或外部服务，你可能需要包括操作系统依赖项，或者在安装过程中下载它们。例如，某些库可能依赖于操作系统的本地库文件，如 `.dll`（Windows）或 `.so`（Linux）文件。
- 对于桌面应用程序，可能还需要依赖于操作系统提供的服务或特定的 API，如 Windows 的 COM 组件、Linux 的某些系统库等。

### 7. **可执行文件**

- 如果应用程序是需要执行的文件（例如 Java 的 `.jar` 文件、Python 的 `.py` 文件，或甚至是原生的可执行文件），那么打包后的应用通常会包含一个启动入口，用户可以直接执行。
- 对于 Java 项目，可能是一个可执行的 `.jar` 文件，或者使用 **Spring Boot** 打包的嵌入式 Web 服务器（包括所有依赖）。
- 对于 Node.js 应用，通常是一个 `index.js` 文件，或者使用工具打包成独立的可执行文件。
- 对于原生应用，可能是 `.exe` 文件（Windows）或 `.app` 文件（Mac）等。

### 8. **Dockerfile 或容器配置**

- 如果应用程序是基于 Docker 的，打包时可能会包括 **Dockerfile**，这是用于创建 Docker 镜像的脚本，定义了容器内的环境、依赖项、启动命令等。

- 例如，

  Dockerfile

   可能包含如下内容：

  ```dockerfile
  FROM openjdk:11
  COPY myapp.jar /app/myapp.jar
  CMD ["java", "-jar", "/app/myapp.jar"]
  ```

### 9. **脚本和工具**

- 一些应用程序可能包括启动、部署、安装或清理的脚本。对于 Java 应用，这可能是一个用于启动应用的脚本，如 `startup.sh` 或 `start.bat`。
- 对于 Web 应用，可能有数据库迁移脚本、备份脚本、日志轮转脚本等。
- 对于桌面应用，可能包括安装程序（例如 **.msi** 或 **.dmg** 文件）。

### 10. **授权与许可证文件**

- 如果应用程序使用了第三方库或是商业软件，打包时需要包括相关的授权文件或许可证。
- 通常，这些文件会被放在包的根目录，并包含应用程序的许可证信息。

### 11. **测试和文档**

- 有时打包还会包括单元测试、集成测试和相关的测试框架配置，尤其是用于开发、CI/CD 流程时。
- 打包时可能还会包括应用程序的文档、帮助文件或 README 文件。

当用户拉取镜像并运行容器时，容器会从 Docker 镜像中加载需要的依赖。这些依赖已经包含在镜像内，且会在容器启动时自动提供。例如：

- 如果镜像使用 `openjdk:8-jdk` 作为基础镜像，那么这个镜像会包含 Java 8 的运行时环境，容器启动后，Java 8 会被用来运行容器中的应用。
- 如果应用依赖其他库或工具，这些也会在镜像构建时包含进去。





**动态链接（Dynamic Linking）** 是一种程序链接方式，在程序运行时，将所需的库或模块与程序进行连接，而不是在编译时将所有依赖直接嵌入到可执行文件中。与 **静态链接** 相比，动态链接使得程序的可执行文件更加轻量化，并且可以共享系统中的库文件，从而节省存储空间和内存。

**exe 和 dll 文件 都是PE文件**

**组成结构如下**

![image-20250203211909346](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250203211909346.png)

# vpn 与系统代理

在使用 VPN 时，系统代理的开启状态会影响网络流量的路径和访问某些网站的方式，这主要涉及到网络流量的路由和代理设置：

1. **不开启系统代理**：

   当系统代理关闭时，通常网络流量直接经过你的本地网络设置，通过本地的路由器和==互联网服务提供商（ISP）==提供的网络路径来访问互联网。

   VPN 连接会建立一个加密的==隧道==，将你的流量通过 VPN 服务器进行路由，隐藏你的真实 IP 地址，同时提供更安全的连接。

2. **开启系统代理**：

   当系统代理开启时，你的操作系统会通过==代理服务器==来发送和接收网络请求。这可能是公司或组织内部的代理服务器，或者是一些公共代理服务（如翻墙软件常用的代理服务器）。

   如果你在使用 VPN 的同时开启系统代理，那么流量可能会先经过系统代理服务器，然后再通过 VPN 隧道发送到 VPN 服务器，最终访问互联网。这种情况下，系统代理服务器和 VPN 服务器之间的路由可能会影响一些网站的访问能力，特别是那些对访问来源有特定要求或限制的网站。

   ~~~ceylon
   系统代理的影响： 系统代理的开启状态会影响你的网络流量走向，可能会经过另外的代理服务器或者公司的内部网络。某些网站可能根据代理服务器的 IP 地址或网络识别出你的访问来源，这可能导致一些网站在系统代理开启时可以访问，而在关闭时无法访问。 网站的访问策略和识别： 有些网站使用复杂的访问控制策略，可能会根据多个因素来决定是否允许访问，包括 IP 地址、用户代理（User-Agent）、Cookies 等。开启或关闭 VPN 和系统代理可能改变这些因素，从而影响你的访问结果。
   ~~~

## 代理的on/off

没有开启代理，而单纯使用 VPN 连接，访问国内没有被墙的网站会有以下情况：

**这和全局有点像**

1. **流量路由**：

   所有的网络流量都会通过 VPN 提供的加密隧道发送到 VPN 服务器。这意味着国内没有被墙的网站的访问流量也会经过 VPN 连接。

2. **访问效果**：

   VPN 连接可能会引入一定的延迟，因为流量需要经过 VPN 服务器路由。对于国内网站，这种延迟可能会导致访问速度稍微变慢一些，特别是如果 VPN 服务器位置远离你的实际位置。

3. **隐私和安全**：

   使用 VPN 可以提供加密和隐私保护，确保你的网络流量在公共网络中不易被截获或窃取。即使是访问国内网站，VPN 也可以保护你的数据传输安全，尤其是在使用不安全的公共 Wi-Fi 网络时尤为重要。

**流量路由**：

如果代理设置的优先级高于 VPN 或者单独使用代理，你的网络流量会通过代理服务器发送而不经过 VPN 隧道。

这意味着国内没有被墙的网站的访问流量不会通过 VPN 提供的加密通道，而是直接通过代理服务器发送和接收数据。

**访问速度和稳定性**：

使用代理服务器可能会影响访问速度和稳定性，具体取决于代理服务器的性能和网络质量。有时候使用代理可能会提高访问速度，尤其是对于国内网站，因为可以避免 VPN 所带来的额外延迟。

**隐私和安全**：

如果代理服务器未经过适当配置或管理，可能会存在隐私和安全风险，因为数据不会经过 VPN 提供的加密保护。这可能暴露你的真实 IP 地址和数据内容，尤其是对于敏感信息的传输。

# Vps 和 云服务器

VPS（Virtual Private Server）和云服务器（Cloud Server）都属于虚拟化技术，但它们有一些关键的区别：

### 1. **虚拟化方式和资源分配**

   - **VPS**：
     - VPS 是在一台物理服务器上创建多个虚拟服务器，每个 VPS 都有独立的操作系统和资源（如 CPU、内存、存储等）。
     - VPS 通常使用 **基于虚拟化技术**（如 KVM、OpenVZ 等）来实现资源分配。
     - 资源分配是固定的，即购买了多少资源就能使用多少。

   - **云服务器**：
     - 云服务器是基于云计算架构的，通常由多个物理服务器和存储设备组成，利用 **虚拟化技术和分布式计算**来动态分配资源。
     - 云服务器的资源（如 CPU、内存、存储）通常是按需分配的，可以随时扩展和缩减，具有较强的弹性。
     - 云服务器通常还提供多区域和多可用区的支持，使得服务具有高可用性和容错能力。

### 2. **弹性和扩展性**

   - **VPS**：
     - 扩展性较差，资源分配较为固定，增加或减少资源（如 CPU 或内存）往往需要手动操作，甚至需要迁移到另一台物理服务器。
     - VPS 的扩展通常比较复杂，无法像云服务器那样灵活地按需增加资源。

   - **云服务器**：
     - 云服务器提供高度的弹性和按需扩展功能，可以随时根据负载需求增加或减少资源，不需要迁移，能迅速响应变化的需求。
     - 云服务器还支持负载均衡、自动扩展等功能，适应大规模、高并发的应用场景。

### 3. **管理方式**

   - **VPS**：
     - 通常由用户自己管理和维护，用户需要自行配置操作系统、安装软件、处理安全问题等。
     - 比较适合需要定制化配置和有一定技术能力的用户。

   - **云服务器**：
     - 提供更多的自动化管理功能，比如自动备份、自动扩展、监控和警报等。云服务提供商通常会为用户提供更多的管理工具和服务。
     - 适合需要高可用性、可靠性和自动化管理的用户。

### 4. **可靠性和高可用性**

   - **VPS**：
     - VPS 受限于物理服务器，一旦物理服务器出现故障，可能会影响多个 VPS。
     - 高可用性和容错能力较弱，通常需要手动搭建高可用架构。

   - **云服务器**：
     - 云平台通常在多个数据中心之间分布，支持高可用性和自动容错。即使某个节点出现问题，云服务器可以自动迁移到其他节点，确保服务不间断。
     - 提供多区域、跨区域的部署选项，保障服务的可靠性和灾难恢复能力。

### 5. **价格**

   - **VPS**：
     - 通常价格较为固定和便宜，适合低预算的项目或个人使用。
     - 定价相对简单，按月或按年付费。

   - **云服务器**：
     - 通常价格较高，尤其是资源使用弹性较大的情况。但也支持按需计费，可以按小时或按流量收费，灵活性更高。
     - 可以根据实际使用量收费，适合流量波动大或需要动态扩展的应用场景。

### 总结：

- **VPS** 更适合小型网站、开发测试、预算有限的用户，资源相对固定，适合对性能要求较为简单的场景。
- **云服务器** 更适合需要高可用、弹性扩展、大流量应用的用户，具有更强的扩展性和高可靠性，支持按需计费，适合企业级应用。

希望这能帮助你理解两者的区别！如果有更多问题，欢迎继续问！



---

# 项目部署





---





# **1. Web 网络拓扑规划**

Web 系统的网络拓扑主要取决于**业务规模**和**安全需求**，一般分为**单层架构、小型架构、中大型分布式架构**等。

## **① 单服务器架构（适用于小型网站）**

**特点**：

- 所有功能（Web 服务器、数据库、应用逻辑）集中在**同一台服务器**上。
- 适用于个人博客、小型网站。
- 易部署、成本低，但**性能和安全性较差**。

**拓扑结构**：

```
用户  →  Web 服务器（包含应用+数据库）
```

**缺点**：

- **单点故障**：服务器崩溃，整个网站无法访问。
- **性能瓶颈**：无法应对高并发请求。

------

## **② 双机架构（应用与数据库分离，适用于中小型网站）**

**特点**：

- **Web 服务器** 和 **数据库服务器** 分离，提升性能和安全性。
- Web 服务器处理用户请求，数据库服务器存储数据。

**拓扑结构**：

```
用户 → Web 服务器 → 数据库服务器
```

**优点**：

- **数据库服务器独立**，提高数据安全性。
- **Web 服务器可横向扩展**（添加更多服务器）。

**缺点**：

- **数据库仍然是单点故障**（可用主从复制提高可用性）。

------

## **③ 负载均衡架构（适用于大流量网站）**

**特点**：

- 采用 **负载均衡（Load Balancer）** 将流量分发给多个 Web 服务器，避免单点瓶颈。
- 可水平扩展，支持**高并发**。

**拓扑结构**：

```
用户 → 负载均衡（Nginx、HAProxy） → 多台 Web 服务器 → 数据库服务器（主从复制）
```

**优势**：

- **高可用性**：某个 Web 服务器宕机，其他服务器可继续提供服务。
- **扩展性强**：可增加更多服务器应对流量增长。

**缺点**：

- 需要额外的负载均衡设备或服务（如 Nginx、CDN、云负载均衡）。

------

## **④ 分布式架构（适用于超大规模网站）**

**特点**：

- 采用 **CDN、微服务架构、缓存集群**，支持全球访问。
- 适用于**电商、社交媒体、搜索引擎等超大流量网站**。

**拓扑结构**：

```
用户 → CDN（缓存静态资源）→ 负载均衡 → 多台 Web 服务器 → 微服务（多个 API 服务）→ 数据库集群（分片 + 读写分离）
```

**优化组件**：

- **CDN（内容分发网络）**：减少服务器负担，提高访问速度。
- **Redis/Memcached**：缓存热点数据，减少数据库查询压力。
- **消息队列（Kafka、RabbitMQ）**：处理异步任务，提高系统吞吐量。

------

# **2. Web 安全防护措施**

Web 安全防护涉及**网络层、服务器层、应用层**的多种策略，主要包括**防攻击、防数据泄露、防入侵**等。

## **① 网络层安全**

**防护目标**：防止 DDoS 攻击、端口扫描、流量劫持。

- **CDN 防护**：隐藏真实服务器 IP，抵御 DDoS 攻击。
- **WAF（Web 应用防火墙）**：拦截 SQL 注入、XSS 攻击等恶意请求。
- **DDoS 保护**：云防护（如 Cloudflare、阿里云 DDoS 高防）。

------

## **② 服务器安全**

**防护目标**：防止服务器被黑客入侵、提升系统安全性。

- **最小化开放端口**：关闭不必要的端口（只开放 80/443/22）。
- **SSH 访问安全**：禁止 root 登录，使用密钥认证。
- **防止暴力破解**：使用 fail2ban 限制 SSH 登录失败次数。
- **日志监控**：实时监测异常访问（如异常 IP、登录失败）。

------

## **③ 应用层安全**

**防护目标**：防止 SQL 注入、XSS、CSRF、弱密码攻击等。

- SQL 注入防护

  ：

  - 使用**预处理 SQL 语句（Prepared Statements）**。

  - 禁止动态拼接 SQL 语句，如：

    ```sql
    sql
    -- 不安全
    SELECT * FROM users WHERE username = '" + input + "'";
    
    -- 安全
    SELECT * FROM users WHERE username = ?;
    ```

- XSS（跨站脚本攻击）防护

  ：

  - 过滤或转义 HTML 输入，防止用户提交 `<script>alert("XSS")</script>`。
  - 使用 `Content Security Policy (CSP)` 限制 JavaScript 执行权限。

- CSRF（跨站请求伪造）防护

  ：

  - 在表单请求中使用 CSRF Token。

  - 限制 Cookie 的 SameSite 属性：

    ```js
    Set-Cookie: session_id=abcd1234; HttpOnly; Secure; SameSite=Strict
    ```

------

## **④ 认证与权限管理**

**防护目标**：防止未经授权的访问，确保身份验证安全。

- **强密码策略**：要求用户使用**复杂密码**（8+ 位，包含大小写、数字、特殊字符）。

- **多因素认证（MFA）**：增加手机验证码、指纹识别等额外验证方式。

- 最小权限原则（Principle of Least Privilege）

  ：

  - 只有管理员才能执行敏感操作（删除用户、修改配置）。
  - API 访问需身份验证（OAuth 2.0、JWT）。

------

## **⑤ 数据安全**

**防护目标**：防止数据泄露、加密敏感信息。

- HTTPS 传输加密

  ：

  - 启用 TLS（SSL）证书，防止流量被劫持。

  - 服务器配置 HSTS，强制 HTTPS 访问：

    ```nginx
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    ```

- 数据库加密

  ：

  - 用户密码存储时**使用哈希加密**（如 `bcrypt` 而不是 `MD5/SHA1`）。
  - 数据库敏感信息（如用户银行卡号）**使用 AES 加密**。



---



# HTTP协议



## 特点： 

![image-20241109172609983](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109172609983.png)

```ceylon
 HTTP协议的无状态（Stateless）是指服务器不会保存客户端的任何信息，每次请求都是独立和分离的。让我详细解释一下：
 
 1. 无状态的含义：
 
 - 每次请求都是独立的，互不关联
 - 服务器不会记住之前的请求信息
 - 每次请求都需要携带必要的信息
 
 2. 无状态的优点：
 
 - 服务器不需要存储客户端信息，减少服务器开销
 - 服务器可以更快地处理大量请求
 - 更容易实现服务器的水平扩展
 
 3. 无状态带来的挑战：
 
 - 难以实现用户登录状态的保持
 - 购物车等功能实现较复杂
 - 需要重复传输一些相同的信息
 
 4. 解决方案：
 
 - Cookie：在客户端保存状态信息
 - Session：在服务器端保存状态信息
 - Token：使用令牌机制维护状态
 - LocalStorage：在浏览器本地存储数据
```

## HTTP ——请求数据

![image-20241109173542257](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109173542257.png)

![image-20241109173551884](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109173551884.png)

![image-20241109173905741](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109173905741.png)

## HTTP ——响应数据

![image-20241109174613471](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109174613471.png)

![image-20241109174616983](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109174616983.png)

![image-20241109174631636](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109174631636.png)

**就是资源放在服务器的不同位置上或是另一台服务器上 所以要重定向找到资源**

## 响应状态码

![image-20241109175006354](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241109175006354.png)



 # Tomcat & Servlet

### **为什么需要部署应用服务器？**

- **Web 项目** 通常是一个打包好的应用程序（如 WAR 文件或 JAR 文件），它需要运行在一个 **应用服务器** 或 **Web 服务器** 中。
- 应用服务器提供了运行环境，支持 Web 项目的核心功能，例如：
  - 处理 HTTP 请求和响应。
  - 管理 Servlet、JSP、EJB 等组件。
  - 提供数据库连接池、事务管理等功能。
- 如果没有应用服务器，Web 项目无法运行。

**version complicable  extension** 版本兼容异常  （tomcat11 与jdk1.8 不兼容！！！）<font color=red size=6>(VC)</font> ****

**可推广：可延申思考** ==Extendable==  <font color=red size=6>(E+)</font>

**指涉判空！！：** Referrance  Empty **<font color=red size=6>(RE)</font>**

安装tomcat 配置环境变量 JAVA_HOME value=jdk目录

如何找jdk --> where java 命令

**打开bin/startup.bat 启动tomcat服务器 或者在idea中run启动**

## Tomcat 的目录结构（可推广）

**Extendable: 编译器中的功能分类树**





![image-20241123150104197](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123150104197.png)





## JSP 和html

~~~ceylon
JSP和HTML有以下主要区别：

动态与静态
JSP是动态网页，可以包含Java代码，能够动态生成内容
HTML是静态网页，内容是固定的，不能动态生成
    
执行方式
JSP需要在服务器端执行，经过编译后转换为Servlet
HTML直接在浏览器中解释执行
    
功能特点
JSP可以访问数据库、执行业务逻辑
JSP可以使用内置对象(request、response等)
HTML只能显示静态内容和超链接
    
语法结构
JSP包含Java代码、JSP标签、HTML标签
HTML只包含HTML标签

    
运行环境
JSP需要Web服务器支持(如Tomcat)
HTML只需要浏览器即可运行

   
    
    
应用场景
JSP适合开发动态网站，需要与数据库交互的场景
HTML适合制作静态网页，展示固定内容
性能
JSP需要服务器解析，性能相对较低
HTML直接显示，性能较好
维护性
JSP可以实现业务逻辑与显示的分离，便于维护
HTML将内容和显示混在一起，维护相对困难
~~~

请求（request）：客户端发送数据给服务端

响应（response）：服务端返回数据给客户端

![image-20241123135208955](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123135208955.png)

~~~css
Tomcat服务器：

定义：
Tomcat是一个开源的Java Servlet容器和Web服务器，由Apache软件基金会开发。
软件性质：
Tomcat是一个软件应用程序，不是物理硬件。
主要用途：
运行Java Servlets和JavaServer Pages (JSP)  也就是一个<--容器-->
作为Web应用服务器，处理HTTP请求
托管Java Web应用程序
使用场景：
开发和测试Java Web应用
部署小到中型的Java Web项目
作为轻量级的应用服务器
特点：
轻量级，易于配置和使用
支持Java EE规范的一个子集
可以独立运行，也可以集成到其他应用服务器中
~~~

**客户端axios可与服务端servelet & JSP 协作**

## 基本写法

~~~java
    @WebServlet("/sr1") //        一定不要忘记写 '/'
    public class Servlet01 extends HttpServlet {
        @Override
        protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
            System.out.println("hello Lunafreya !");
            Writer writer = response.getWriter();
            writer.write("hello Lunafreya !");
        }
    }

~~~

了解即可：

![image-20241123151418786](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123151418786.png)

**URL：http://localhost:8080/myArtifact1/sr1 本机服务器 项目 项目下的资源**

Tomcat服务器下可有多个项目 在配置中查看

---

针对表单：

**GET 请求**

- **特点**：

  - 表单数据会附加在 URL 后面，以查询字符串的形式传递。
  - 例如：`http://example.com/submit?name=John&age=25`。
  - 数据在 URL 中可见，不适合传输敏感信息（如密码）。
  - 有长度限制（取决于浏览器和服务器，通常为 2048 字符）。

  ```html
  <form action="/submit (目标URL)" method="GET">
      <label for="name">Name:</label>
      <input type="text" id="name" name="name">
      <label for="age">Age:</label>
      <input type="number" id="age" name="age">
      <button type="submit">Submit</button>
  </form>
  ```

  

  运行 HTML

  - 提交后，URL 会变成：`http://example.com/submit?name=John&age=25`。

  ---

  

**POST 请求**

- **特点**：

  - 表单数据会放在 HTTP 请求体中，不会显示在 URL 中。
  - 适合传输敏感信息或大量数据。
  - 没有长度限制。

  运行 HTML

  - 提交后，URL 不会改变，数据在请求体中传输。

### 

如果没有指定 `method` 属性，表单默认使用 **GET** 请求：



## Servlet 生命周期



![image-20241123152020822](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123152020822.png)

**销毁：服务器关闭或应用程序停止**

incept : 开始

**service 方法可以执行多次**

![image-20241123152222238](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123152222238.png)

## HttpServletRequest对象

![image-20241123153102809](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123153102809.png)、

### 常用方法

~~~java
@WebServlet("/sr2")
public class Servlet2 extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println(request.getRequestURI()); // /myArtifact1/sr2
        System.out.println(request.getRequestURL()); // http://localhost:8080/myArtifact1/sr2
        System.out.println(request.getQueryString()); // ?name=Senjay&age=25
        System.out.println(request.getParameter("name")); // Senjay
        System.out.println(request.getParameter("age"));// 25
        System.out.println(request.getMethod()); // GET
        System.out.println(request.getProtocol()); // HTTP/1.1
        System.out.println(request.getContextPath()); //获取webapp名字 // /myArtifact1
    }
}

~~~

### 获取请求参数

~~~java
@WebServlet("/sr3")
public class servlet3 extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println(request.getParameter("name"));
        String [] grades = request.getParameterValues("grade");// 使用grades数组存贮 键为grade的多个值
        System.out.println(Arrays.toString(grades));
        // ?name= & grade= & grade= ……
        // 注意如果拿不到数组的话访问（如:遍历）数组就会空指针异常！！！
        // 指涉判空！！

    }
}
~~~

![image-20241123160145280](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123160145280.png)

~~~java

@WebServlet("/wr1")
public class WriterDemo1 extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
//        PrintWriter out = response.getWriter();
//        out.write("Hello world");
        //字符数据
        // 不能同时使用
        ServletOutputStream sos = response.getOutputStream();
        sos.write("<h1 style=\"color:red;\">Hello World</h1>".getBytes());
        // 二进制数据
        

    }
}

~~~



### 请求乱码（Messey code）问题

编码格式 ≠ 解码格式 -->==“乱码”==

![image-20241123160825056](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123160825056.png)

![image-20241123160827925](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123160827925.png)

![image-20241123160830293](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123160830293.png)





## 请求转发（只有一个请求）和request作用域

![image-20241123161259247](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123161259247.png)

![image-20241123171400601](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123171400601.png)

![image-20241123171416989](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123171416989.png)



![image-20241123180713283](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123180713283.png)

**请求转发可以将请求跳转到html jsp 以及其他servlet对象中**



- **HTML页面无法直接访问 `request` 对象**：

  - 由于HTML是静态文件，无法直接访问Servlet的 `request` 对象。因此，需要使用JavaScript或模板引擎（如Thymeleaf、JSP）来动态渲染数据。

- **模板引擎**：

  - 如果你使用JSP或Thymeleaf等模板引擎，可以直接在HTML中嵌入动态数据。例如：

    html

    复制

    ```jsp
    <h1>提交成功！</h1>
    <p>姓名: ${name}</p>
    <p>年龄: ${age}</p>
    ```

### 域对象

本质就是键值对!

**键一定是字符串 值可以是任何数据类型**

**s05跳转s06**

![image-20241123181029124](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123181029124.png)

要同一个请求 目的地才能拿到域对象

需要：

```java
request.getRequestDispatcher("sr06").forward(request,response);
```

![image-20241123180934795](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123180934795.png)





| form 的 action 属性                                          | 表单元素的 name 属性                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `action` 属性定义了表单提交时,数据应该发送到哪个URL进行处理。它指定了处理表单数据的服务器脚本的路径。 | `name` 属性为表单元素提供一个名称,这个名称会在表单提交时与该元素的值一起发送到服务器。它用于在服务器端识别不同的表单数据。 |

~~~java
@WebServlet("/test1")
public class MessyCode extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println(request.getParameter("name"));
        // get 不会messycode
        // 试试post
        System.out.println(request.getParameter("age")); // 表单提交本质和get里请求行一样 只是和数据的敏感性以及数据的数量有关
        System.out.println(request.getParameter("grade"));

    }
}
~~~

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="test1" method="post">
    <input type="text" name="age">
    <br>
    <input type="text" name="grade">
    <button>点击提交</button>
</form>
</body>
</html>
~~~



## HttpServletReponse对象

`HttpServletResponse` 是 Java Servlet API 中的一个接口，专门用于处理 HTTP 响应。它提供了一系列方法，使开发人员能够控制响应头、响应状态以及响应体的内容。以下是关于 `HttpServletResponse` 的详细解释，包括它的作用、主要内容和常用方法。

### 1. 定义和作用

- **定义**：`HttpServletResponse` 是 `javax.servlet.http` 包中的一个接口，继承自 `ServletResponse` 接口。它提供了对 HTTP 响应的访问和操作。
- **作用**：`HttpServletResponse` 的主要作用是向客户端（如浏览器）发送响应数据。这包括设置响应状态码、内容类型、响应头，以及将响应体中的数据写回客户端。

### 2. 主要内容

`HttpServletResponse` 的内容可以分为几个部分：

1. **响应状态**：
   - HTTP 响应状态码，指示请求的结果。例如，200 表示成功，404 表示未找到，500 表示服务器错误等。
2. **响应头**：
   - 包含关于响应的信息，例如内容类型（`Content-Type`）、内容长度（`Content-Length`）、缓存控制（`Cache-Control`）、设置 Cookie 等。
   - ==Content-Type: text/html; charset=UTF-8==
3. **响应体**：
   - 实际返回给客户端的数据内容，例如 HTML 文档、JSON 数据、图像、文件下载等。

### 3. 常用方法

`HttpServletResponse` 提供了多种方法来设置响应的各个部分。以下是一些常用方法的说明：

#### 1. 设置响应状态

- **`setStatus(int sc)`**：设置响应状态码。

  

  ```java
  response.setStatus(HttpServletResponse.SC_OK); // 设置状态码为 200
  ```

- **`sendError(int sc, String msg)`**：发送错误响应。

  

  ```java
  response.sendError(HttpServletResponse.SC_NOT_FOUND, "Page not found"); // 设置状态码为 404
  ```

#### 2. 设置响应头

- **`setHeader(String name, String value)`**：设置指定名称的响应头。

  

  ```java
  response.setHeader("Cache-Control", "no-cache"); // 设置缓存控制
  ```

- **`addHeader(String name, String value)`**：添加一个响应头。

  

  ```java
  response.addHeader("Set-Cookie", "sessionId=abc123; Path=/; HttpOnly");
  ```

- **`setContentType(String type)`**：设置响应的内容类型（MIME 类型）。

  

  ```java
  response.setContentType("text/html; charset=UTF-8"); // 设置内容类型为 HTML
  ```

#### 3. 获取输出流

- **`getWriter()`**：获取一个 `PrintWriter` 对象，用于向响应体写入字符数据。

  

  ```java
  PrintWriter out = response.getWriter();
  out.println("<html><body><h1>Hello, World!</h1></body></html>");
  ```

- **`getOutputStream()`**：获取一个 `ServletOutputStream` 对象，用于向响应体写入二进制数据。

  

  ```java
  ServletOutputStream out = response.getOutputStream();
  out.write(...); // 写入二进制数据
  ```

![image-20241123220948364](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123220948364.png)

| 特性         | `getWriter()`                                                | `getOutputStream()`                                          |
| :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 类型         | 返回 `PrintWriter`，用于字符输出                             | 返回 `ServletOutputStream`，用于二进制输出                   |
| 用途         | 适用于输出文本（HTML、JSON、XML等）                          | 适用于输出二进制数据（图像、文件等）                         |
| 字符编码     | 需要设置字符编码（如 UTF-8）                                 | 不涉及字符编码                                               |
| 不能混合使用 | 如果调用了 `getWriter()`，则不能再调用 `getOutputStream()`，反之亦然 | 如果调用了 `getOutputStream()`，则不能再调用 `getWriter()`，反之亦然 |

**与io流网络编程流类似** 结合复习

**这里是通过HttpservletResponse 对象的方法获取字节输出流或者字符输出流**

---

==联系文件/网络IO流==

| 特性         | **PrintWriter**                          | **ServletOutputStream**              |
| :----------- | :--------------------------------------- | :----------------------------------- |
| **数据类型** | 主要用于字符流（文本数据）               | 主要用于二进制流（如图像、文件等）   |
| **适用场景** | 生成 HTML、JSON、XML 和纯文本响应        | 发送压缩数据、图像、PDF 等二进制内容 |
| **输出方式** | 使用 `println()`、`print()` 方法输出字符 | 使用 `write()` 方法输出字节          |
| **性能**     | 对于文本数据，性能较好，但不适合大文件   | 对于大文件和流式传输，性能更佳       |
| **互斥性**   | 不能与 `getOutputStream()` 一起使用      | 不能与 `getWriter()` 一起使用        |

~~~java
@WebServlet("/wr1")
public class WriterDemo1 extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
//        PrintWriter out = response.getWriter();
//        out.write("Hello world");
        // 不能同时使用
        ServletOutputStream sos = response.getOutputStream();
        sos.write("<h1 style=\"color:red;\">Hello World</h1>".getBytes());

    }
~~~





## 响应乱码问题

### MIME类型

| MIME 类型                           | 描述                           |
| :---------------------------------- | :----------------------------- |
| `text/plain`                        | 普通文本文件                   |
| `text/html`                         | HTML 文件                      |
| `text/css`                          | CSS 文件                       |
| `text/javascript`                   | JavaScript 文件                |
| `application/json`                  | JSON 数据                      |
| `application/xml`                   | XML 数据                       |
| `application/pdf`                   | PDF 文件                       |
| `application/octet-stream`          | 二进制数据（一般用于下载文件） |
| `image/jpeg`                        | JPEG 图像                      |
| `image/png`                         | PNG 图像                       |
| `image/gif`                         | GIF 图像                       |
| `audio/mpeg`                        | MPEG 音频                      |
| `video/mp4`                         | MP4 视频                       |
| `application/zip`                   | ZIP 压缩文件                   |
| `application/x-www-form-urlencoded` | 表单数据编码类型               |





![image-20241123221524023](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123221524023.png)

**响应数据 ： 服务器端编码 客户端解码**

==**响应头发送信息告知这是一个什么样的数据**==

**encode 编码**



## 重定向

![image-20241123231650371](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123231650371.png)

**也可重定向到其他servlet去**

## 请求转发和重定向的区别

![image-20241123231926410](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123231926410.png)





![image-20241123223731618](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123223731618.png)

## cookie

![image-20241123232412728](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241123232412728.png)

### HTTP 的无状态性与 Cookie 的关系





| 无状态性：                                                   | Cookie 的作用：                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 由于 HTTP 是无状态的，服务器在处理每个请求时并不知道前一个请求的任何信息。这种设计使得 HTTP 协议更简单，但也导致了需要一种机制来管理用户会话和状态。 | Cookie 用于克服 HTTP 的无状态性。通过在客户端存储一些信息（如用户 ID、会话 ID 等），服务器可以在后续请求中识别用户并维持会话状态。每当客户端发起请求时，浏览器会自动将相关的 Cookie 发送给服务器，从而使服务器能够识别用户。 |

### Cookie 的创建和添加

~~~java
@WebServlet("/sr7")
public class Cookies extends HttpServlet {
    @Override
    public void service(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        Cookie cookie = new Cookie("uname","senjay");
        res.addCookie(cookie);

    }
}
~~~

### Cookie 的获取

![image-20250111164244964](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111164244964.png)



### Cookie的存活时间 maxAge

![image-20250111164419219](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111164419219.png)

**cookie.setMaxAge(-1)**

### Cookie 注意问题

![image-20250111164554753](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111164554753.png)



cookie大小数量都有限制



### Cookie路径问题

![image-20250111164851667](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111164851667.png)

![image-20250111164834652](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111164834652.png)

## session

![image-20241124145048770](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124145048770.png)

session是对象

![image-20250111165956895](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111165956895.png)

![image-20250111170133376](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111170133376.png)

### session域对象和 request域对象的区别

对于请求转发 两者都有效

但是对于重定向只有session域对象有用

### session的销毁

![image-20250111170826760](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111170826760.png)



![image-20250111170830522](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250111170830522.png)

### **数据存储位置**

| 特性         | Cookie                     | Session                    |
| :----------- | :------------------------- | :------------------------- |
| **存储位置** | 客户端（浏览器）           | 服务器端                   |
| **存储内容** | 键值对数据（通常是字符串） | 对象（可以是任意Java对象） |
| **安全性**   | 较低（数据存储在客户端）   | 较高（数据存储在服务器端） |

- **Cookie**：数据存储在客户端浏览器中，每次请求时会自动发送到服务器。
- **Session**：数据存储在服务器端，客户端只保存一个 `Session ID`（通常通过Cookie存储）。



## Token

[cookie 、sesson、Token 区别](https://www.bilibili.com/video/BV1ob4y1Y7Ep/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36)









---

# Java 网络编程

见javaSE 基础

### Socket （套接字） ：



套接字（Socket）和端口（Port）是两个不同概念，但它们在网络通信中密切相关：

### 套接字（Socket）网络编程

1. **定义**：
   - 套接字是一种用于**进程间通信**的抽象概念，允许**不同进程**在**同一台计算机或通过网络（client and server ）进行数据交换**。
   - 在操作系统中，套接字被实现为一种特殊的文件类型（套接字文件 文件内没有实际数据），用于在进程间传输数据。
2. **特点**：
   - 套接字通常通过套接字 API（如 POSIX 的 socket API 或 Windows 的 Winsock API）来创建和使用。
   - 可以创建不同类型的套接字，包括面向连接的套接字（如 TCP 套接字）和无连接的套接字（如 UDP 套接字）。
3. **用途**：
   - 用于在**同一台计算机内部的进程间通信（UNIX 域套接字**）。
   - 用于在网络上**不同计算机间**的进程通信（网络套接字）

---



# 虚拟机网络模式











