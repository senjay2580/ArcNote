> - 
> - ~~**CI（持续集成）**：代码提交→自动测试→构建打包
> - **CD（持续部署）**：构建完成→自动部署→健康检查



- 用 Jenkins 构建一次镜像并推送到 **Docker Hub** 后，测试环境可以拉取这个镜像部署测试，预发布和生产环境也能直接使用 **同一个镜像**。

## Jenkins CI/CD配置

### 1. Jenkins安装与配置

#### Docker方式安装Jenkins

```bash
# 创建Jenkins数据目录
sudo mkdir -p /opt/jenkins_home
sudo chown 1000:1000 /opt/jenkins_home

# 启动Jenkins容器

docker run -d \
  --name MyJenkins \
  -e TZ=Asia/Shanghai \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts


# 获取初始密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### 必需插件安装

1. **Pipeline插件**：支持Jenkinsfile
2. **Git插件**：Git仓库集成
3. **Docker插件**：Docker构建支持
4. **NodeJS插件**：前端构建支持
5. **Maven插件**：后端构建支持
6. **SSH Agent插件**：服务器部署
7. **Blue Ocean插件**：现代化UI

### 2. Jenkinsfile配置

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DEPLOY_SERVER = 'your-server.com'
        MYSQL_ROOT_PASSWORD = credentials('mysql-root-password')
        REDIS_PASSWORD = credentials('redis-password')
    }
    
    tools {
        nodejs '18.0.0'
        maven '3.9.0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('前端测试') {
            steps {
                dir('Client-site') {
                    sh 'npm ci'
                    sh 'npm run test:run'
                    sh 'npm run test:coverage'
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'Client-site/coverage',
                        reportFiles: 'index.html',
                        reportName: '前端测试覆盖率报告'
                    ])
                }
            }
        }
        
        stage('后端测试') {
            steps {
                dir('ARCHAT/archat-server') {
                    sh 'mvn clean test'
                }
            }
            post {
                always {
                    junit 'ARCHAT/archat-server/target/surefire-reports/*.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'ARCHAT/archat-server/target/site/jacoco',
                        reportFiles: 'index.html',
                        reportName: '后端测试覆盖率报告'
                    ])
                }
            }
        }
        
        stage('构建镜像') {
            parallel {
                stage('构建前端镜像') {
                    steps {
                        dir('Client-site') {
                            script {
                                def frontendImage = docker.build("${DOCKER_REGISTRY}/archat-frontend:${IMAGE_TAG}")
                                docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                                    frontendImage.push()
                                    frontendImage.push('latest')
                                }
                            }
                        }
                    }
                }
                
                stage('构建后端镜像') {
                    steps {
                        dir('ARCHAT/archat-server') {
                            script {
                                def backendImage = docker.build("${DOCKER_REGISTRY}/archat-backend:${IMAGE_TAG}")
                                docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                                    backendImage.push()
                                    backendImage.push('latest')
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('集成测试') {
            steps {
                script {
                    sh '''
                        # 启动测试环境
                        docker-compose -f docker-compose.test.yml up -d
                        
                        # 等待服务启动
                        sleep 30
                        
                        # 运行集成测试
                        cd Client-site
                        npm run test:e2e
                        
                        # 清理测试环境
                        docker-compose -f docker-compose.test.yml down
                    '''
                }
            }
        }
        
        stage('部署到生产环境') {
            when {
                branch 'main'
            }
            steps {
                sshagent(['deploy-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no root@${DEPLOY_SERVER} "
                            cd /opt/archat && \
                            git pull origin main && \
                            export IMAGE_TAG=${IMAGE_TAG} && \
                            export MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} && \
                            export REDIS_PASSWORD=${REDIS_PASSWORD} && \
                            ./scripts/deploy.sh
                        "
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            script {
                if (env.BRANCH_NAME == 'main') {
                    // 发送成功通知
                    sh '''
                        curl -X POST -H 'Content-type: application/json' \
                        --data '{"text":"🎉 ArcHat部署成功！\n版本: '${IMAGE_TAG}'\n提交: '${GIT_COMMIT_SHORT}'\n分支: '${BRANCH_NAME}'"}' \
                        ${SLACK_WEBHOOK_URL}
                    '''
                }
            }
        }
        failure {
            // 发送失败通知
            sh '''
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"❌ ArcHat部署失败！\n版本: '${IMAGE_TAG}'\n提交: '${GIT_COMMIT_SHORT}'\n分支: '${BRANCH_NAME}'\n查看详情: '${BUILD_URL}'"}' \
                ${SLACK_WEBHOOK_URL}
            '''
        }
    }
}
```

### 3. Jenkins凭据配置

在Jenkins管理界面配置以下凭据：

1. **mysql-root-password**：MySQL root密码
2. **redis-password**：Redis密码
3. **docker-registry-credentials**：Docker镜像仓库凭据
4. **deploy-ssh-key**：服务器SSH私钥
5. **slack-webhook-url**：Slack通知webhook



---



### 部署脚本

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装"
        exit 1
    fi
    
    log_info "依赖检查通过"
}

# 备份当前版本
backup_current() {
    log_info "备份当前版本..."
    
    if [ -d "/opt/your-app/backup" ]; then
        rm -rf /opt/your-app/backup
    fi
    
    mkdir -p /opt/your-app/backup
    docker-compose -f docker-compose.prod.yml config > /opt/your-app/backup/docker-compose.yml
    
    # 备份数据库
    docker exec mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} > /opt/your-app/backup/database.sql
    
    log_info "备份完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost/health &> /dev/null; then
            log_info "健康检查通过"
            return 0
        fi
        
        log_warn "健康检查失败，重试 $attempt/$max_attempts"
        sleep 10
        ((attempt++))
    done
    
    log_error "健康检查失败，开始回滚"
    rollback
    exit 1
}

# 回滚函数
rollback() {
    log_warn "开始回滚..."
    
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f /opt/your-app/backup/docker-compose.yml up -d
    
    # 恢复数据库
    docker exec -i mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} < /opt/your-app/backup/database.sql
    
    log_info "回滚完成"
}

# 主部署流程
main() {
    log_info "开始部署..."
    
    check_dependencies
    backup_current
    
    # 拉取最新代码
    log_info "拉取最新代码..."
    git pull origin main
    
    # 构建并启动服务
    log_info "构建并启动服务..."
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml pull
    docker-compose -f docker-compose.prod.yml up -d --build
    
    # 健康检查
    health_check
    
    log_info "部署完成！"
}

main "$@"
```

---

## 监控与运维

### 健康检查端点

```java
// 后端健康检查
@RestController
public class HealthController {
    
    @Autowired
    private DataSource dataSource;
    
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> status = new HashMap<>();
        
        try {
            // 检查数据库连接
            dataSource.getConnection().close();
            status.put("database", "UP");
        } catch (Exception e) {
            status.put("database", "DOWN");
            return ResponseEntity.status(503).body(status);
        }
        
        try {
            // 检查Redis连接
            redisTemplate.opsForValue().get("health-check");
            status.put("redis", "UP");
        } catch (Exception e) {
            status.put("redis", "DOWN");
            return ResponseEntity.status(503).body(status);
        }
        
        status.put("status", "UP");
        status.put("timestamp", System.currentTimeMillis());
        
        return ResponseEntity.ok(status);
    }
}
```

### 日志配置

```yaml
# docker-compose.prod.yml 日志配置
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
  frontend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 监控脚本

```bash
#!/bin/bash
# scripts/monitor.sh

# 检查服务状态
check_services() {
    echo "=== 服务状态检查 ==="
    docker-compose -f docker-compose.prod.yml ps
    
    echo -e "\n=== 健康检查 ==="
    curl -s http://localhost/health | jq .
    
    echo -e "\n=== 资源使用情况 ==="
    docker stats --no-stream
}

# 检查日志
check_logs() {
    echo "=== 最近错误日志 ==="
    docker-compose -f docker-compose.prod.yml logs --tail=50 | grep -i error
}

# 主函数
main() {
    check_services
    check_logs
}

main "$@"
```



### 备份策略

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/opt/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# 备份数据库
docker exec mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} --all-databases > $BACKUP_DIR/mysql_backup.sql

# 备份Redis数据
docker exec redis redis-cli --rdb $BACKUP_DIR/redis_backup.rdb

# 备份应用代码
tar -czf $BACKUP_DIR/app_backup.tar.gz /opt/your-app

# 清理旧备份（保留7天）
find /opt/backups -type d -mtime +7 -exec rm -rf {} \;
```

这套CI/CD流程实现了：

1. **自动化测试**：代码提交触发单元测试、集成测试
2. **自动化部署**：测试通过后自动部署到生产环境
3. **健康检查**：部署后自动验证服务可用性
4. **故障回滚**：出现问题自动回滚到上一版本
5. **监控告警**：实时监控服务状态和性能

**关键优势**：

- 从代码提交到上线只需5分钟
- 零停机部署
- 自动化测试保证质量
- 一键回滚降低风险
- 标准化流程提升效率



### 流水线—Jenkins前端构建流程分析

~~~bash
Started by user senjay

Obtained Jenkinsfile from git https://github.com/senjay2580/ArcHat.git
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins
 in /var/jenkins_home/workspace/Archat-client-site
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
The recommended git tool is: git
No credentials specified
 > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/Archat-client-site/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/senjay2580/ArcHat.git # timeout=10
Fetching upstream changes from https://github.com/senjay2580/ArcHat.git
 > git --version # timeout=10
 > git --version # 'git version 2.47.3'
 > git fetch --tags --force --progress -- https://github.com/senjay2580/ArcHat.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision ee188aae878b32f387a6f30b4233720b71651f51 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f ee188aae878b32f387a6f30b4233720b71651f51 # timeout=10
Commit message: "fix: 修正服务器IP地址格式错误"
 > git rev-list --no-walk ee188aae878b32f387a6f30b4233720b71651f51 # timeout=10
[Pipeline] }
[Pipeline] // stage
[Pipeline] withEnv
[Pipeline] {
[Pipeline] withCredentials
Masking supported pattern matches of $DOCKERHUB_CREDENTIALS or $DOCKERHUB_CREDENTIALS_PSW
[Pipeline] {
[Pipeline] withEnv
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Get Git Info)
[Pipeline] echo
📋 获取Git信息...
[Pipeline] script
[Pipeline] {
[Pipeline] sh
+ git log -1 --pretty=%B
[Pipeline] sh
+ git log -1 --pretty=%an
[Pipeline] }
[Pipeline] // script
[Pipeline] echo
📝 前端提交信息: fix: 修正服务器IP地址格式错误

- 去掉IP地址中的http://前缀和结尾斜杠
- 修正为纯IP地址格式: 8.138.168.72
- 解决SSH连接hostname解析失败问题
[Pipeline] echo
👤 提交者: senjay
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build Frontend)
[Pipeline] echo
🎨 构建前端项目...
[Pipeline] sh
+ echo 📦 检查或安装 Node.js...
📦 检查或安装 Node.js...
+ [ ! -d ./node-v20.18.0-linux-x64 ]
+ echo ✅ 使用缓存的 Node.js
✅ 使用缓存的 Node.js
+ export PATH=/var/jenkins_home/workspace/Archat-client-site/node-v20.18.0-linux-x64/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
+ echo 📦 Node.js版本信息:
📦 Node.js版本信息:
+ node --version
v20.18.0
+ npm --version
10.8.2
+ echo 📦 当前工作目录:
📦 当前工作目录:
+ pwd
/var/jenkins_home/workspace/Archat-client-site
+ ls -la package.json
-rw-r--r-- 1 jenkins jenkins 1924 Nov 28 13:33 package.json
+ echo 📥 安装依赖...
📥 安装依赖...
+ npm config set registry https://registry.npmmirror.com
+ npm config set cache /var/jenkins_home/workspace/Archat-client-site/.npm-cache
+ npm install --prefer-offline --no-audit


up to date in 34s

114 packages are looking for funding
  run `npm fund` for details
+ echo 🏗️ 构建生产版本...
🏗️ 构建生产版本...
+ npm run build


> client-site@0.0.0 build
> vite build


[36mvite v6.3.5 [32mbuilding for production...[36m[39m
transforming...

[32m✓[39m 4385 modules transformed.
rendering chunks...

+ echo ✅ 前端构建完成!
✅ 前端构建完成!
+ ls -la dist/
total 76
drwxr-xr-x 1 jenkins jenkins  4096 Nov 28 22:56 .
drwxr-xr-x 1 jenkins jenkins  4096 Nov 28 22:52 ..
drwxr-xr-x 1 jenkins jenkins  4096 Nov 28 22:56 assets
-rw-r--r-- 1 jenkins jenkins 67799 Nov 28 22:56 favicon.ico
-rw-r--r-- 1 jenkins jenkins  1451 Nov 28 22:56 heartbeat-worker.js
-rw-r--r-- 1 jenkins jenkins   633 Nov 28 22:56 index.html
Post stage
[Pipeline] archiveArtifacts
Archiving artifacts

Recording fingerprints

[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Docker Build & Deploy)

[Pipeline] parallel
[Pipeline] { (Branch: Build & Push Docker)
[Pipeline] { (Branch: Prepare Server)
[Pipeline] stage
[Pipeline] { (Build & Push Docker)
[Pipeline] stage

[Pipeline] { (Prepare Server)
[Pipeline] echo
🐳 构建前端Docker镜像...
[Pipeline] script
[Pipeline] {
[Pipeline] echo
🔧 准备服务器环境...
[Pipeline] script
[Pipeline] {

[Pipeline] sshagent
[ssh-agent] Using credentials root (服务器ssh密钥)
$ ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-RLlrgVqHbGQx/agent.6974
SSH_AGENT_PID=6979
Running ssh-add (command line suppressed)
Identity added: /var/jenkins_home/workspace/Archat-client-site@tmp/private_key_5279336533245081751.key (root@iZ7xv86t3qfdnsa9qwgz7mZ)
[ssh-agent] Started.
[Pipeline] {
[Pipeline] sh
[Pipeline] isUnix
[Pipeline] withEnv
+ echo 🔍 检查服务器状态...
🔍 检查服务器状态...
+ ssh -o StrictHostKeyChecking=no root@8.138.168.72 
                                        cd /opt/archat && 
                                        echo '服务器准备就绪'
                                    
[Pipeline] {

[Pipeline] sh
+ docker build -t arclighting/archat-frontend:33 .

#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 479B 0.1s done
#1 DONE 0.1s

#2 [internal] load metadata for docker.io/library/node:18-slim
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/nginx:alpine
#3 DONE 0.0s

#4 [internal] load .dockerignore
#4 transferring context: 1.12kB 0.1s done
#4 DONE 0.1s

#5 [build-stage 1/4] FROM docker.io/library/node:18-slim
#5 DONE 0.0s

#6 [stage-1 1/3] FROM docker.io/library/nginx:alpine
#6 DONE 0.0s

#7 [internal] load build context

服务器准备就绪

[Pipeline] }
$ ssh-agent -k
unset SSH_AUTH_SOCK;
unset SSH_AGENT_PID;
echo Agent pid 6979 killed;
[ssh-agent] Stopped.
#7 transferring context: 10.22MB 2.8s done
#7 DONE 2.8s

#8 [build-stage 2/4] WORKDIR /app
#8 CACHED

#9 [build-stage 3/4] COPY . .
#9 CACHED

#10 [build-stage 4/4] RUN npm install && npm run build
#10 CACHED

#11 [stage-1 2/3] COPY --from=build-stage /app/dist /usr/share/nginx/html
#11 CACHED

#12 [stage-1 3/3] COPY nginx.conf /etc/nginx/nginx.conf
#12 CACHED

#13 exporting to image
#13 exporting layers done
#13 writing image sha256:19826c4949ca0289f809a65bc127418c5d85849248cab88f404577dee7c3a2de done
#13 naming to docker.io/arclighting/archat-frontend:33 done
#13 DONE 0.0s
[Pipeline] // sshagent

[Pipeline] }
[Pipeline] }

[Pipeline] // script
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] withEnv

[Pipeline] {
[Pipeline] withDockerRegistry
$ docker login -u arclighting -p ******** https://registry.hub.docker.com
WARNING! Using --password via the CLI is insecure. Use --password-stdin.

WARNING! Your password will be stored unencrypted in /var/jenkins_home/workspace/Archat-client-site@tmp/61631b52-6f48-4d79-9409-bc6a9cc2e2e8/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[Pipeline] {

[Pipeline] isUnix
[Pipeline] withEnv
[Pipeline] {
[Pipeline] sh
+ docker tag arclighting/archat-frontend:33 registry.hub.docker.com/arclighting/archat-frontend:33

[Pipeline] }
[Pipeline] // withEnv
[Pipeline] isUnix
[Pipeline] withEnv
[Pipeline] {

[Pipeline] sh
+ docker push registry.hub.docker.com/arclighting/archat-frontend:33
The push refers to repository [registry.hub.docker.com/arclighting/archat-frontend]

35b9a05e2d3d: Preparing
b47e76de39cf: Preparing
0d853d50b128: Preparing
947e805a4ac7: Preparing
811a4dbbf4a5: Preparing
b8d7d1d22634: Preparing
e244aa659f61: Preparing
c56f134d3805: Preparing
d71eae0084c1: Preparing
08000c18d16d: Preparing
b8d7d1d22634: Waiting
c56f134d3805: Waiting
d71eae0084c1: Waiting
08000c18d16d: Waiting
e244aa659f61: Waiting

811a4dbbf4a5: Layer already exists
0d853d50b128: Layer already exists
947e805a4ac7: Layer already exists
b47e76de39cf: Layer already exists
35b9a05e2d3d: Layer already exists

c56f134d3805: Layer already exists
d71eae0084c1: Layer already exists
b8d7d1d22634: Layer already exists
08000c18d16d: Layer already exists
e244aa659f61: Layer already exists

33: digest: sha256:f5debc8212da157c52fc48b3e990298fdeab6b8fbb8038026dc781b84d50f19e size: 2408

[Pipeline] }
[Pipeline] // withEnv
[Pipeline] isUnix
[Pipeline] withEnv
[Pipeline] {

[Pipeline] sh
+ docker tag arclighting/archat-frontend:33 registry.hub.docker.com/arclighting/archat-frontend:latest
[Pipeline] }

[Pipeline] // withEnv
[Pipeline] isUnix
[Pipeline] withEnv
[Pipeline] {

[Pipeline] sh
+ docker push registry.hub.docker.com/arclighting/archat-frontend:latest
The push refers to repository [registry.hub.docker.com/arclighting/archat-frontend]

35b9a05e2d3d: Preparing
b47e76de39cf: Preparing
0d853d50b128: Preparing
947e805a4ac7: Preparing
811a4dbbf4a5: Preparing
b8d7d1d22634: Preparing
e244aa659f61: Preparing
c56f134d3805: Preparing
d71eae0084c1: Preparing
08000c18d16d: Preparing
e244aa659f61: Waiting
c56f134d3805: Waiting
d71eae0084c1: Waiting
b8d7d1d22634: Waiting
08000c18d16d: Waiting

811a4dbbf4a5: Layer already exists
b47e76de39cf: Layer already exists
0d853d50b128: Layer already exists
947e805a4ac7: Layer already exists
35b9a05e2d3d: Layer already exists

08000c18d16d: Layer already exists
d71eae0084c1: Layer already exists
b8d7d1d22634: Layer already exists
c56f134d3805: Layer already exists

e244aa659f61: Layer already exists

latest: digest: sha256:f5debc8212da157c52fc48b3e990298fdeab6b8fbb8038026dc781b84d50f19e size: 2408

[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }

[Pipeline] // withDockerRegistry
[Pipeline] }

[Pipeline] // withEnv
[Pipeline] echo
✅ 前端镜像推送完成: arclighting/archat-frontend:33
[Pipeline] }

[Pipeline] // script
[Pipeline] }
[Pipeline] // stage
[Pipeline] }

[Pipeline] // parallel
[Pipeline] }

[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Deploy to Server)
[Pipeline] echo
🚀 部署到服务器...
[Pipeline] script
[Pipeline] {

[Pipeline] sshagent
[ssh-agent] Using credentials root (服务器ssh密钥)
$ ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-MadnNlHwou0S/agent.7174
SSH_AGENT_PID=7177
Running ssh-add (command line suppressed)
Identity added: /var/jenkins_home/workspace/Archat-client-site@tmp/private_key_6475450249466881708.key (root@iZ7xv86t3qfdnsa9qwgz7mZ)
[ssh-agent] Started.
[Pipeline] {
[Pipeline] sh

+ echo 📦 更新前端镜像版本...
📦 更新前端镜像版本...
+ FRONTEND_IMAGE_FULL=arclighting/archat-frontend:33
+ ssh -o StrictHostKeyChecking=no root@8.138.168.72 
                                cd /opt/archat && 
                                ./deploy.sh update-frontend-image 'arclighting/archat-frontend:33' &&
                                ./deploy.sh restart-frontend
                            

[0;34m[INFO][0m 更新前端镜像: arclighting/archat-frontend:33
[0;32m[SUCCESS][0m 前端镜像版本更新完成
[0;34m[INFO][0m 重启前端服务...
time="2025-11-28T22:57:39+08:00" level=warning msg="/opt/archat/docker-compose.prod.yml: `version` is obsolete"
 frontend Pulling 

 frontend Pulled 
time="2025-11-28T22:57:44+08:00" level=warning msg="/opt/archat/docker-compose.prod.yml: `version` is obsolete"
 Container mysql  Running
 Container archat_redis  Running
 Container archat_rabbitmq  Running
 Container archat-backend  Running
 Container archat-frontend  Recreate
 Container archat-frontend  Recreated
 Container archat-frontend  Starting
 Container archat-frontend  Started
[0;32m[SUCCESS][0m 前端服务重启完成
+ echo ✅ 前端更新完成!
✅ 前端更新完成!
[Pipeline] }
$ ssh-agent -k
unset SSH_AUTH_SOCK;
unset SSH_AGENT_PID;
echo Agent pid 7177 killed;
[ssh-agent] Stopped.

[Pipeline] // sshagent
[Pipeline] }
[Pipeline] // script
[Pipeline] }

[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Frontend Health Check)
[Pipeline] echo

🏥 前端健康检查...
[Pipeline] script
[Pipeline] {
[Pipeline] sshagent
[ssh-agent] Using credentials root (服务器ssh密钥)
$ ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-dtSTTBGStUZI/agent.7198
SSH_AGENT_PID=7201
Running ssh-add (command line suppressed)
Identity added: /var/jenkins_home/workspace/Archat-client-site@tmp/private_key_8644180890348118408.key (root@iZ7xv86t3qfdnsa9qwgz7mZ)
[ssh-agent] Started.
[Pipeline] {

[Pipeline] sh
+ echo ⏳ 等待前端服务启动...
⏳ 等待前端服务启动...
+ sleep 15

+ echo 🌐 检查前端服务...
🌐 检查前端服务...
+ ssh -o StrictHostKeyChecking=no root@8.138.168.72 curl -f http://localhost:80 > /dev/null 2>&1

+ echo ✅ 前端服务正常
✅ 前端服务正常
[Pipeline] }
$ ssh-agent -k
unset SSH_AUTH_SOCK;
unset SSH_AGENT_PID;
echo Agent pid 7201 killed;
[ssh-agent] Stopped.

[Pipeline] // sshagent
[Pipeline] }

[Pipeline] // script
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)

[Pipeline] echo
🎉 前端部署成功!
[Pipeline] script
[Pipeline] {
[Pipeline] echo

🎉 ArcChat前端部署成功!

📋 构建信息:
• 构建号: 33
• Git提交: fix: 修正服务器IP地址格式错误

- 去掉IP地址中的http://前缀和结尾斜杠
- 修正为纯IP地址格式: 8.138.168.72
- 解决SSH连接hostname解析失败问题
• 前端镜像: arclighting/archat-frontend:33

[Pipeline] }

[Pipeline] // script
[Pipeline] }
[Pipeline] // stage
[Pipeline] }

[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // withCredentials
[Pipeline] }

[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // node

[Pipeline] End of Pipeline

Finished: SUCCESS

~~~



根据Jenkins日志文件的内容，我将前端构建流程按顺序分析如下：

#### 1. 初始化阶段
- **启动触发**: 由用户senjay手动触发构建
- **获取代码**: 从GitHub仓库 `https://github.com/senjay2580/ArcHat.git` 签出代码
- **检出分支**: 检出main分支，提交ID为`ee188aae`，提交信息为"fix: 修正服务器IP地址格式错误"

#### 2. 获取Git信息阶段 (Get Git Info)
- 获取最近的Git提交信息
- 记录提交者信息（senjay）和提交信息详情

#### 3. 前端构建阶段 (Build Frontend)
- **环境准备**:
  - 检查Node.js环境（使用缓存的Node.js v20.18.0）
  - 显示Node.js (v20.18.0)和npm (10.8.2)版本信息
- **依赖安装**:
  - 配置npm镜像为`https://registry.npmmirror.com`
  - 配置npm缓存路径
  - 使用`npm install --prefer-offline --no-audit`安装依赖
- **构建生产版本**:
  - 执行`npm run build`命令构建生产版本
  - Vite构建过程转换了4385个模块
  - 生成了多个静态资源文件（CSS、图片、音频等）

#### 4. Docker构建和部署阶段 (Docker Build & Deploy)
此阶段包含两个并行执行的分支：

##### 分支1: 构建和推送Docker镜像
- **构建Docker镜像**:
  - 使用Dockerfile从当前目录构建Docker镜像
  - 基于node:18-slim（构建阶段）和nginx:alpine（最终镜像）
  - 将构建产物复制到Nginx服务目录
- **推送Docker镜像**:
  - 登录Docker Hub（使用凭据）
  - 标记镜像为`arclighting/archat-frontend:33`
  - 标记镜像为`arclighting/archat-frontend:latest`
  - 将两个标签的镜像推送到Docker Hub

##### 分支2: 准备服务器环境
- 通过SSH连接到目标服务器（IP：8.138.168.72）
- 检查服务器状态和环境准备情况

#### 5. 部署到服务器阶段 (Deploy to Server)
- 通过SSH连接到服务器
- 执行部署脚本更新前端镜像版本
- 重启前端服务
  - 拉取新的Docker镜像
  - 重新创建前端容器
  - 启动前端服务

#### 6. 前端健康检查阶段 (Frontend Health Check)
- 等待15秒让前端服务完全启动
- 通过curl请求检查前端服务是否正常运行（检查http://localhost:80）
- 确认前端服务正常工作

#### 7. 完成阶段
- 输出构建成功信息，包括：
  - 构建号：33
  - Git提交信息
  - 前端镜像标签：`arclighting/archat-frontend:33`

#### 总结

整个Jenkins前端构建流程可以概括为以下顺序：
1. 代码签出和初始化
2. 获取Git提交信息
3. 安装依赖和构建前端项目
4. 构建Docker镜像并推送到Docker Hub仓库
5. 准备服务器环境
6. 在服务器上部署并重启前端服务
7. 进行健康检查确保服务正常
8. 输出构建结果信息

整个流程实现了前端代码的自动化构建、打包、镜像创建和部署，形成了一个完整的CI/CD流程。构建过程中的每个步骤都有清晰的日志输出，便于监控和调试。

---



## 流水线—Jenkins后端构建流程分析后端

~~~
# 后端Jenkinsfile分析

下面是对后端Jenkinsfile的详细分析：

## 1. 基础配置

- **执行环境**: 使用任意可用的Jenkins代理节点（`agent any`）
- **环境变量设置**:
  - Docker Hub凭据和用户名
  - 后端镜像名称和标签（使用构建号）
  - 部署服务器SSH凭据和路径
  - Maven配置选项

## 2. 构建流程（按顺序）

### 阶段1: 检出后端代码（Checkout Backend）
- 从版本控制系统检出代码（`checkout scm`）
- 获取最新提交信息和提交者
- 输出Git提交信息和提交者姓名

### 阶段2: 构建后端项目（Build Backend）
- 显示Maven版本信息
- 执行Maven构建流程:
  1. `mvn clean compile -DskipTests`: 清理并编译项目（跳过测试）
  2. `mvn test`: 运行单元测试
  3. `mvn package -DskipTests`: 打包项目（跳过测试）
- 列出构建产出物（`archat-server/target/`目录）
- **后置操作**:
  - 发布测试结果（来自`surefire-reports`）
  - 归档构建产物（JAR文件）

### 阶段3: 构建和推送Docker镜像（Build & Push Backend Docker）
- 在`archat-server`目录中执行
- 构建Docker镜像: `${BACKEND_IMAGE}:${IMAGE_TAG}`
- 登录Docker Hub并推送镜像:
  - 推送特定版本标签
  - 推送latest标签
- 输出镜像推送完成信息

### 阶段4: 更新服务器后端镜像（Update Backend on Server）
- 使用SSH连接到部署服务器
- 执行部署脚本:
  1. `./deploy.sh update-backend-image '${BACKEND_IMAGE_FULL}'`: 更新后端镜像版本
  2. `./deploy.sh restart-backend`: 重启后端服务
- 输出后端更新完成信息

### 阶段5: 后端健康检查（Backend Health Check）
- 等待30秒让后端服务完全启动
- 通过HTTP请求检查后端服务健康状态
  - 检查端点: `http://localhost:8180/actuator/health`
  - 如果请求成功，输出"后端服务正常"
  - 如果请求失败，输出"后端服务异常"并使流程失败

## 3. 完成后处理

- **成功情况**:
  - 输出"后端部署成功"信息
  - 显示构建信息（构建号、Git提交信息、后端镜像）
- **失败情况**:
  - 输出"后端部署失败"信息


~~~

