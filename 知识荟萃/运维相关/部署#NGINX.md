# nginx 



## 部署管理端程序 --- 内网/公网相关

**✅ 企业安全组和端口配置最佳实践总览**

| 分类     | 目标                               | 推荐配置                      |
| -------- | ---------------------------------- | ----------------------------- |
| 云服务器 | 限制入站访问来源，避免被扫或被攻击 | 开放最少必要端口，仅对特定 IP |
| 数据库   | 防止被外部访问入侵                 | 禁止公网访问，仅允许内网      |
| 项目系统 | 控制访问来源，保护后端接口         | 接口服务限内网，前端通过反代  |
| 管理后台 | 防止被爆破登录或扫接口             | 限 IP、账号登录、强密码策略   |

![image-20250503095118912](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250503095118912.png)

![image-20250503095439538](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250503095439538.png)



在宝塔面板中，`/www/wwwroot` 是一个专门用于存放网站和应用程序文件的**标准化目录**，其设计目的是为了统一管理Web服务资源。以下是详细解析：

------

### **一、目录作用与设计逻辑**

#### 1. **核心功能**

- **集中管理**：所有网站/应用文件（前端HTML、后端JAR、PHP项目等）统一存放，避免文件分散。
- **权限控制**：宝塔自动为每个站点分配独立的`www`用户组权限，防止越权访问。
- **一键操作**：与宝塔的「网站」功能深度集成，支持可视化创建站点、SSL证书部署等。

#### 2. **典型内容**

bash



复制



下载

```nginx
/www/wwwroot/
├── example.com/       # 前端项目（Vue/React打包的dist）
│   ├── index.html
│   └── static/
├── api.example.com/   # 后端Java项目
│   └── app.jar        # Spring Boot可执行JAR
└── wordpress/         # PHP项目
    ├── wp-admin/
    └── wp-config.php
```

------

### **二、为什么前后端都放这里？**

#### 1. **Nginx代理的统一入口**

- **前端项目**：
  Nginx直接托管静态文件（通过`root`指向`/www/wwwroot/example.com`）。

  ```nginx
  server {
      listen 80;
      server_name example.com;
      root /www/wwwroot/example.com; # 指定前端文件路径
      index index.html;
  }
  ```
  
- **后端Java项目**：
  Nginx反向代理到JAR包运行的端口（如8080）。

  ```nginx
  location /api/ {
      proxy_pass http://127.0.0.1:8080; # 转发到后端JAR
  }
  ```

#### 2. **宝塔的自动化管理**

- **Java项目**：
  通过宝塔的「Java项目」模块，可自动：
  - 将JAR包放入`/www/wwwroot/api.example.com`
  - 生成管理脚本（启动/停止）
  - 绑定域名和SSL证书

#### 3. **安全性隔离**

- 每个子目录独立权限，避免跨站点访问：

  ```bash
  drwxr-x--- 5 www www 4096 Jun 10 10:00 example.com/
  drwxr-x--- 4 www www 4096 Jun 10 10:01 api.example.com/
  ```

------

### **三、与传统部署的区别**

| **对比项**     | **宝塔（/www/wwwroot）**      | **传统部署**                   |
| :------------- | :---------------------------- | :----------------------------- |
| **路径标准化** | 所有项目强制归类到统一目录    | 可能分散在`/var/www`、`/opt`等 |
| **权限管理**   | 自动设置`www`用户组，权限严格 | 需手动`chown`和`chmod`         |
| **Nginx配置**  | 面板自动生成，与目录绑定      | 手动编辑`nginx.conf`           |
| **备份/恢复**  | 一键操作（整合目录和数据库）  | 需单独处理文件和数据库         |

------

### **四、注意事项**

1. **路径冲突问题**

   - 若前端和后端共用一个域名（如`example.com`），需通过Nginx的`location`区分：

     ```nginx
     location / {
         root /www/wwwroot/example.com; # 前端
         try_files $uri /index.html;
     }
     location /api/ {
         proxy_pass http://localhost:8080; # 后端
     }
     ```

2. **Java项目的运行权限**

   - 确保JAR文件可执行：

     ```bash
     chmod +x /www/wwwroot/api.example.com/app.jar
     ```

3. **资源隔离建议**

   - 生产环境建议前后端分开放置：

     ```nginx
     /www/wwwroot/
     ├── frontend/  # 前端
     └── backend/   # 后端JAR
     ```

------

### **五、为什么不是`/usr/share/nginx/html`？**

- **系统目录保护**：`/usr/share/nginx`属于系统路径，直接修改可能影响Nginx稳定性。
- **权限复杂**：系统目录通常需要`root`操作，而`/www/wwwroot`允许非特权用户管理。
- **宝塔生态整合**：面板功能（如日志分析、防火墙）依赖标准化路径。



---



**临时生效**（仅当前终端）：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

**永久生效**：

1. 编辑 `~/.bashrc` 或 `/etc/profile`：	

   ```bash
   nano ~/.bashrc
   ```

2. 在文件末尾添加：

   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   export PATH=$JAVA_HOME/bin:$PATH
   ```

3. 使配置生效：

   ```bash
   source ~/.bashrc
   ```

| **特性**       | **Linux**                                 | **Windows**                  |
| :------------- | :---------------------------------------- | :--------------------------- |
| **配置文件**   | `~/.bashrc`, `~/.profile`, `/etc/profile` | 图形化系统属性 → 环境变量    |
| **生效方式**   | 需执行 `source ~/.bashrc` 或重新登录      | 修改后立即生效（部分需重启） |
| **路径分隔符** | 冒号 `:`                                  | 分号 `;`                     |
| **变量引用**   | `$PATH`                                   | `%PATH%`                     |

### linux 环境变量

环境变量就是当前设备的全局变量

一般要将保密数据 保存在环境变量当中 让程序去读取

至于springboot的配置文件 就可以通过**命令行** 的方式 对指定参数进行 **覆盖（如果有）/ 添加（如果没有**） 

**其他程序都有自己的配置文件 配置文件就决定了应用程序的行为、连接参数和功能特性**（用户自定义个性化）

无需重启程序 重载配置文件即可

![image-20250503000707579](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250503000707579.png)

​	

linux 安装一般 是 默认的安装目录（系统指定） or 当前目录 or 可以自己指定

docker容器的环境变量：

![image-20250503001809709](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250503001809709.png)



#### 1. **动态配置应用程序**

- <span style="color:#FF0000;">**不同环境差异化**：</span>
  <span style="color:#FF0000;">同一镜像通过不同环境变量即可适配开发、测试、生产环境，无需修改镜像</span>本身。

  ```dockerfile
  # 开发环境
  docker run -e "APP_MODE=dev" -e "DEBUG=true" my-app
  
  # 生产环境
  docker run -e "APP_MODE=prod" -e "DEBUG=false" my-app
  ```

#### <span style="color:#FF0000;">2. **传递敏感信息**</span>

- <span style="font-size:1.1em;">**安全注入密码/密钥**：</span>
  <span style="font-size:1.1em; color:#FF0000;">**避免将敏感数据硬编码到镜像中，可通过环境变量动态传递（结合 `--env-file` 或 Secrets 更安全）。**</span>

  ```dockerfile
  docker run -e "DB_PASSWORD=$(cat /secrets/db_password)" mysql
  ```

#### 3. **定义容器行为**

- **控制服务参数**：
  <span style="color:#FF0000;">**如数据库镜像通过环境变量初始化 root 密码、数据库名称等。**</span>

  ```dockerfile
  docker run -e "MYSQL_ROOT_PASSWORD=123456" -e "MYSQL_DATABASE=app_db" mysql
  ```

#### 4. **服务发现与通信**

- **微服务间连接**：
  动态指定依赖服务的地址（如其他容器的 IP 或域名）。

  ```dockerfile
  docker run -e "USER_SERVICE_URL=http://user-service:8000" app-backend
  ```



---



任何一个项目 运行 都需要有**运行时环境** 

**java ： jdk** 

**mysql管理器 ：phpmyadmin->php**

**反向代理：nginx**

**vue： js -->node.js**

---



springboot中需要 配置不同环境的配置文件 

然后通过**--spring.profiles.active =prod/dev/test**

来指定不同环境的变量

![image-20250502231125399](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250502231125399.png)



mysql中数据 同步！！！！ 注意不同环境不同的数据库 所以数据是不一样的 

可以使用sql脚本 将字段和数据同步导入 或者 使用同步功能？

~~~fileStructure
/
├── bin         # 基础命令二进制文件
├── boot        # 启动相关文件
├── dev         # 设备文件
├── etc         # 系统配置文件
├── home        # 用户主目录
├── lib         # 系统库文件
├── lib64       # 64位系统库
├── media       # 可移动媒体挂载点
├── mnt         # 临时挂载点
├── opt         # 可选应用软件包
├── proc        # 进程和内核信息
├── root        # root用户主目录
├── run         # 运行时数据
├── sbin        # 系统管理命令
├── srv         # 服务数据
├── sys         # 系统设备信息
├── tmp         # 临时文件
├── usr         # 用户程序
└── var         # 可变数据（日志、缓存等）
~~~

**java项目部署**

mvn clean package -> 打包为jar包 

**见下方**

选择文件夹放置jar包 然后可以配置环境变量 或者是命令行指定参数运行 

或者 可以 定义为systemctl 中的服务 就可以使用这个命令 实现 自启动 启动 重载 关闭了



## 日志查看 排查错误



~~~bash
curl http://localhost:8080/admin/category // 本机测试接口
~~~



![image-20250502213555637](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250502213555637.png)

![image-20250502225655312](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250502225655312.png)





## NGINX



## **同源策略（Same-Origin Policy，SOP）是什么？**
**同源策略（SOP）** 是浏览器的一种**安全机制**，它**限制不同源的网页**之间**相互访问数据**，以防止**恶意网站窃取用户敏感信息**。

---

## **1. 什么是“同源”？**
**同源（Same-Origin）** 指的是**两个 URL 必须满足以下三个部分完全相同**：
- **协议（Protocol）**
- **域名（Host）**
- **端口（Port）**

### **示例：**
**同源（允许访问）**

```link
http://example.com:80/page1.html
http://example.com:80/page2.html
```
**不同源（受限制）**
```link
http://example.com:80/page1.html  ≠  https://example.com/page2.html   // 不同协议
http://example.com:80/page1.html  ≠  http://sub.example.com/page2.html  // 不同子域名
http://example.com:80/page1.html  ≠  http://example.com:8080/page2.html  // 不同端口
```

**总结**：

- **`http://a.com` 和 `http://a.com:80` 是同源**（默认 80 端口）。
- **`http://a.com` 和 `https://a.com` 不是同源**（协议不同）。
- **`http://a.com` 和 `http://b.com` 不是同源**（域名不同）。
- **`http://a.com:3000` 和 `http://a.com:8080` 不是同源**（端口不同）。

---

## **2. 同源策略的限制**
同源策略主要影响 **JavaScript** 在浏览器中的行为，限制**不同源的网页**访问彼此的数据：
### **（1）禁止跨源的 AJAX 请求**
```javascript
fetch('http://api.anotherdomain.com/data') // 失败！跨域被拦截
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```
浏览器会报 **CORS 错误**：
```error
Access to fetch at 'http://api.anotherdomain.com/data' from origin 'http://example.com'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```
👉 **解决方案**：服务器设置 `CORS` 允许跨域访问（见后面）。

---

### **（2）禁止跨源访问 Cookie、LocalStorage、SessionStorage**
```javascript
document.cookie = "username=John";  // 仅能访问当前域的 cookie
localStorage.setItem("token", "abc123"); // 仅限当前域访问
```
如果 `http://example.com` 试图访问 `http://another.com` 的 Cookie：
```javascript
fetch('http://another.com/api/data', { credentials: 'include' });
```
🚫 **被浏览器拦截！**

---

### **（3）禁止跨源操作 DOM**
如果 `http://example.com` 试图访问 `http://another.com` 的 `iframe`：
```javascript
const iframe = document.querySelector("iframe");
console.log(iframe.contentDocument.body.innerHTML); // 🚫 被拦截！
```
🚫 **错误：** `Uncaught DOMException: Blocked a frame from accessing a cross-origin frame.`

---

## **3. 如何解决跨域问题？**
### **✅ 方法 1：使用 CORS（跨域资源共享）**
**后端服务器可以在 HTTP 响应头中添加 `Access-Control-Allow-Origin` 允许跨域**：
```http
Access-Control-Allow-Origin: *
```
或者指定允许的源：
```http
Access-Control-Allow-Origin: http://example.com
```
示例（Node.js Express 服务器）：
```javascript
const express = require('express');
const app = express();
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://example.com");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  next();
});
app.get('/api/data', (req, res) => {
  res.json({ message: "跨域成功！" });
});
app.listen(8080);
```

---

### **✅ 方法 2：使用 JSONP（仅限 GET 请求）**
JSONP 利用 `<script>` 标签不受同源策略限制的特点：
```html
<script src="http://api.anotherdomain.com/data?callback=myCallback"></script>
<script>
  function myCallback(data) {
    console.log(data); // 成功获取跨域数据
  }
</script>
```
👉 但 **JSONP 只能用于 `GET` 请求**，不推荐现代开发使用。

---

### **✅ 方法 3：使用 Nginx 代理**
在 Nginx 配置文件 `/etc/nginx/nginx.conf` 添加：
```nginx
server {
    listen 80;
    server_name example.com;

    location /api/ {
        proxy_pass http://backend-server:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
👉 这样前端请求 `/api/`，Nginx 代理到后端 `http://backend-server:8080/`，避免跨域问题。



![image-20250419161838776](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250419161838776.png)



![image-20250419162320536](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250419162320536.png)



所以vue中request.js 中 baseurl 才需要 这样

~~~js
import axios from 'axios'
// TODO:拦截器的写法

import {ElMessage} from 'element-plus'
import router from '@/router'

// 创建请求实例
const baseURL = '/api'
const instance = axios.create({ baseURL })
// 跨域问题


// 添加响应拦截器 在后端返回给前端数据之前执行 
instance.interceptors.response.use(
  response => {
    const res = response.data
    // 判断业务状态码
    if (res.code === 200) {
      return res
    }

    // 操作失败
    ElMessage.error(res.msg || '服务异常')
    console.log('API Error Response:', res)

    // 异步操作的状态转换为失败
    return Promise.reject(res)
  },
  error => {
    // 处理网络错误
    if (!error.response) {
      ElMessage.error('网络异常，请检查网络连接')
      return Promise.reject(error)
    }

    // 处理HTTP状态码
    switch (error.response.status) {
      case 401:
        ElMessage.error('请先登录')
        router.push('/login')
        break
      case 403:
        ElMessage.error('没有权限访问')
        break
      case 404:
        ElMessage.error('请求的资源不存在')
        break
      case 500:
        ElMessage.error('服务器内部错误')
        break
      default:
        ElMessage.error('服务异常')
    }

    return Promise.reject(error)
  }
)


export default instance;
~~~



---

### **✅ 方法 4：使用 Vite 代理（适用于开发环境）**
在 `vite.config.js` 里设置代理：
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```
👉 这样前端请求 `/api/users`，会被代理到 `http://localhost:8080/users`，避免跨域问题。

---

## **4. 总结**
| **限制内容**          | **同源策略的影响**         | **解决方案**               |
| --------------------- | -------------------------- | -------------------------- |
| AJAX 请求             | 不能请求不同源的 API       | CORS / JSONP / 代理        |
| Cookie / LocalStorage | 不同源不能访问             | CORS 允许 `credentials`    |
| DOM 操作              | 不能访问 `iframe` 内部 DOM | `postMessage` 进行跨域通信 |
| WebSocket             | 需要同源                   | 可用 `wss://` 进行跨域     |

**同源策略是一种安全机制**，防止恶意网站窃取用户数据。  
如果你需要跨域访问，可以通过 **CORS、代理、JSONP** 等方式来解决。

👉 **如果你是前端开发者，建议使用 Vite 代理或后端 CORS 解决跨域问题！** 🚀

如果有不明白的地方，可以继续问我！ 😊



nginx 初始目录结构取决于操作系统的不同

e.g. vue 打包 npm run build 打包

![ad1f8f51cba65fad2d6d4bfb684665d](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/ad1f8f51cba65fad2d6d4bfb684665d.jpg)

入门项目没有使用nginx 为什么呢 

Vite 前端项目**在开发环境下**不需要 Nginx 代理，主要是因为 Vite 内置了一个开发服务器，并且已经在 `vite.config.js` 中配置了 `server.proxy` 来代理 API 请求。

~~~js
// vite-config,js

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    proxy:{
      '/api':{
          target:'http://localhost:8080',
          changeOrigin:true,
          rewrite:(path) => path.replace(/^\/api/,'')
      }
    }
  }
})

~~~







~~~nginx
// 点评 - nginx.conf
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/json;

    sendfile        on;
    
    keepalive_timeout  65;

    server {
        listen       8080;
        server_name  localhost; // 实际使用的域名 或者 ip地址
        # 指定前端项目所在的位置
        location / {
            root   html/hmdp;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }


        location /api {  
            default_type  application/json;
            #internal;  
            keepalive_timeout   30s;  
            keepalive_requests  1000;  
            #支持keep-alive  
            proxy_http_version 1.1;  
            rewrite /api(/.*) $1 break;  
            proxy_pass_request_headers on;
            #more_clear_input_headers Accept-Encoding;  
            proxy_next_upstream error timeout;  
            proxy_pass http://127.0.0.1:8081;
            #proxy_pass http://backend;
        }
    }

    upstream backend {
        server 127.0.0.1:8081 max_fails=5 fail_timeout=10s weight=1;
        #server 127.0.0.1:8082 max_fails=5 fail_timeout=10s weight=1;
    }  
}

~~~







~~~nginx
// take-out 项目 nginx.conf


#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
	
	map $http_upgrade $connection_upgrade{
		default upgrade;
		'' close;
	}

	upstream webservers{
	  server 127.0.0.1:8080 weight=90 ;
	  #server 127.0.0.1:8088 weight=10 ;
	}

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html/sky;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # 反向代理,处理管理端发送的请求
        location /api/ {
			proxy_pass   http://localhost:8080/admin/;
            #proxy_pass   http://webservers/admin/;
        }
		
		# 反向代理,处理用户端发送的请求
        location /user/ {
            proxy_pass   http://webservers/user/;
        }
		
		# WebSocket
		location /ws/ {
            proxy_pass   http://webservers/ws/;
			proxy_http_version 1.1;
			proxy_read_timeout 3600s;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "$connection_upgrade";
        }

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}

~~~



# 快速开始



~~~yaml
  server {
        listen 8001;
        server_name localhost;
        location / {
            root   html/TodoList;
            index  index.html index.htm;
        }
    }

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html/sky;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }




        # 反向代理,处理管理端发送的请求
        location /api/ {
			proxy_pass   http://localhost:8080/admin/;
            #proxy_pass   http://webservers/admin/;
        }
		
		# 反向代理,处理用户端发送的请求
        location /user/ {
            proxy_pass   http://webservers/user/;
        }
		
		# WebSocket
		location /ws/ {
            proxy_pass   http://webservers/ws/;
			proxy_http_version 1.1;
			proxy_read_timeout 3600s;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "$connection_upgrade";
        }

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }
~~~



# 项目打包部署

Vue（无论是 Vue 2 还是 Vue 3）使用的是 **SPA（单页面应用 Single Page Application）** 架构。

所以打包后的目录结构一般是这样：

```nginx
dist/
├── index.html
├── js/
│   ├── app.[hash].js
│   ├── chunk-vendors.[hash].js
├── css/
│   └── app.[hash].css
└── assets/
    └── ...
```

虽然顶层只有一个 `index.html`，但它是 **SPA** 的入口，**实际所有的页面、逻辑、组件都被打包进了 JS 文件里。**

## location 

Nginx 的 `location` 块支持多种匹配模式，通过不同的符号标识匹配规则：

| **语法格式**          | **匹配规则**                                                 | **优先级** |
| :-------------------- | :----------------------------------------------------------- | :--------- |
| `location = /path`    | **精确匹配**：URI 必须完全等于 `/path`                       | 最高       |
| `location ^~ /path`   | **前缀匹配**：URI 以 `/path` 开头，且**不检查正则表达式**    | 次高       |
| `location ~ pattern`  | **正则匹配（区分大小写）**：URI 符合正则表达式 `pattern`     | 中         |
| `location ~* pattern` | **正则匹配（不区分大小写）**：URI 符合正则表达式 `pattern`   | 中         |
| `location /path`      | **普通前缀匹配**：URI 以 `/path` 开头，但**会继续检查其他正则表达式** | 低         |
| `location /`          | **通用匹配**：所有未匹配到其他规则的请求                     | 最低       |

**nginx -s reload 是一个命令，用来优雅地重新加载 Nginx 配置文件，不需要重启 Nginx 服务**

(~ref) 某些应用程序也是无需重启 直接加载配置文件就行（前提是没有修改代码只修改了配置文件）





在 Nginx 的配置中，root 指令用于指定服务器上的根目录路径，但在不同的上下文中，其作用有所不同：

root 在 server 块中的作用：

在 server 块中，root 指令用于定义整个虚拟主机的根目录。所有属于该虚拟主机的 location 块如果没有另外指定 root，将会继承自 server 块的 root 设置。

示例：

 

```nginx
server {
    listen 80;
    server_name example.com;
    root /path/to/root;

location / {
    # root 默认会继承自 server 块
    index index.html;
    try_files $uri $uri/ /index.html;
}
```
}
在上面的示例中，所有 / 路径下的请求都会使用 /path/to/root 作为根目录。

root 在 location 块中的作用：

在 location 块中，root 指令用于重写 server 块中指定的根目录。这允许您为特定的请求路径设置不同的根目录，而不是使用全局设置。

示例：

​    

```nginx
server {
    listen 80;
    server_name example.com;
    root /path/to/root;

location /app {
    # 使用 /path/to/another/root 作为根目录
    root /path/to/another/root;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```
}
在上面的示例中，所有 /app 路径下的请求将使用 /path/to/another/root 作为根目录，而不是全局设置的 /path/to/root







---



Nginx 配置中的 `try_files $uri $uri/ /index.html;` 主要用于支持前端单页应用（SPA）的路由机制，确保用户直接访问非根路径时仍能正确加载应用。以下是逐层解析：



**一、指令功能**

`try_files` 会按顺序尝试查找文件或目录，直到找到第一个匹配项并返回。若所有尝试均失败，则返回最后一个参数指定的文件（通常为前端入口文件）。

**二、参数解析**

```nginx
try_files $uri $uri/ /index.html;
```

1. **`$uri`**
   - 直接匹配用户请求的原始路径对应的文件。
   - **示例**: 用户访问 `/about` → 检查是否存在 `/about` 文件（如 `about.html`）。
2. **`$uri/`**
   - 检查请求路径是否为目录，并尝试访问目录下的默认索引文件（由 `index` 指令定义，如 `index.html`）。
   - **示例**: 用户访问 `/blog/` → 检查是否存在 `/blog/index.html`。
3. **`/index.html`**
   - 前两项均未找到时，内部重定向到 `/index.html`（最终由前端处理路由）。
   - **示例**: 用户访问 `/user/123` → 返回 `index.html`，前端解析路由并渲染对应页面。

---

~~~js
// 创建请求实例
const baseURL = '/api/user/'
const instance = axios.create({ baseURL })
// 跨域问题

~~~

~~~nginx
location / {
        index index.html;
        try_files $uri $uri/ /index.html;
    }


location /api/ {
        # 反向代理到后端服务器
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 可选项，更改代理后返回头信息中的服务器名
        # proxy_set_header Server $host;
    }
~~~

/api/user/category --> http://localhost:8080/user/category

~~~nginx
问题场景模拟
假设你有一个 Vue.js 单页应用（SPA），部署在 Nginx 服务器上，前端路由如下：

/ → 首页

/user/profile → 用户个人页

/about → 关于页

用户操作流程
用户打开浏览器访问 https://example.com
→ Nginx 返回 index.html → 前端路由加载首页。

用户点击导航栏的「个人主页」按钮
→ 前端路由（Vue Router）更新 URL 为 https://example.com/user/profile，不向服务器请求新页面，而是直接渲染 Profile.vue 组件。

用户手动刷新页面（或直接输入 https://example.com/user/profile 访问）
→ 浏览器会向服务器请求 /user/profile 这个路径的资源 → 如果 Nginx 配置错误，会返回 404！

为什么会出现 404？
Nginx 默认行为是查找服务器上是否存在 /user/profile 这个文件或目录。

但 SPA 只有一个入口文件 index.html，所有路由均由前端 JavaScript 处理，服务器根本没有 /user/profile 这个物理文件。

解决方案：Nginx 的 try_files
nginx
location / {
    root /var/www/html/myapp;  # 前端文件存放目录
    index index.html;          # 默认入口文件
    try_files $uri $uri/ /index.html;
}
try_files 的工作流程（以访问 /user/profile 为例）
检查 $uri
Nginx 先尝试查找 /var/www/html/myapp/user/profile 文件 → 不存在。

检查 $uri/
再尝试查找 /var/www/html/myapp/user/profile/ 目录 → 不存在。

回退到 /index.html
最后返回 /var/www/html/myapp/index.html，交给前端路由处理 → Vue Router 解析 /user/profile 并渲染对应页面。


~~~

**页面如果都无法渲染的话更别题页面逻辑中的api调用了**






