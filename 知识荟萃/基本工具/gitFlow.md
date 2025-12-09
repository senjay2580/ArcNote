

```ad-info
# 一、核心前提：部署架构适配无中断
无中断部署的基础是部署环境支持「灰度发布 / 蓝绿部署 / 滚动更新」，如果是单机裸奔，至少要保证：
服务进程支持热重启（如 Java 的 arthas 热更、Node.js 的 pm2 reload、Python 的 gunicorn reload）；
反向代理（Nginx）配置健康检查，避免流量打到异常实例。
# 二、场景 1：线上问题，需修改代码修复（最常见）
步骤 1：拉取线上分支，本地紧急修复
假设线上运行的是origin/release-1.0分支，先确保本地代码与远程一致：

# 1. 切换到线上分支，拉取最新代码

git checkout release-1.0
git pull origin release-1.0

# 2. 创建临时修复分支（避免直接改主分支，便于追溯）
git checkout -b hotfix-xxx（xxx为问题编号，如hotfix-500报错）

# 3. 本地修改代码，修复问题（测试通过后）
git add .
git commit -m "fix: 紧急修复线上500报错（xxx问题）"

# 4. （可选）推送到远程修复分支，便于团队审核
git push origin hotfix-xxx
步骤 2：合并修复到线上分支（远程更新）
优先用「合并（merge）」而非「强制推送（force push）」（强制推送会覆盖远程历史，风险极高）：
bash
运行
# 1. 切回线上分支，合并修复分支
git checkout release-1.0
git merge --no-ff hotfix-xxx  # --no-ff保留合并记录，便于回溯

# 2. 推送到远程线上分支（核心：更新远程分支）
git push origin release-1.0
步骤 3：无中断部署到线上
根据部署架构选择对应方式，核心是「先启动新实例→切流量→停旧实例」：
方式 A：蓝绿部署（无感知，推荐）
部署「绿环境」：基于更新后的release-1.0分支，部署到备用服务器 / 容器（绿环境）；
验证绿环境：测试接口、日志，确认修复生效；
切换流量：修改 Nginx / 负载均衡配置，将流量从「蓝环境（旧版本）」切到「绿环境（新版本）」；
下线蓝环境：确认流量稳定后，停止旧版本实例。
方式 B：滚动更新（适合 K8s / 容器化）
bash
运行
# 以K8s为例，假设部署文件是deploy.yaml
kubectl apply -f deploy.yaml  # K8s会逐台替换Pod，保留可用实例，无中断
# 验证
kubectl rollout status deployment/xxx
方式 C：单机热重启（无容器 / 集群的兜底方案）
bash
运行
# 示例1：Node.js（pm2）
pm2 reload app.js  # 热重启，不中断连接
# 示例2：Python（gunicorn）
gunicorn -c gunicorn.conf.py app:app --reload  # 平滑重启
# 示例3：Java（SpringBoot）
# 用arthas热更class文件（仅应急，长期需重启）
arthas redefine /path/to/fixed.class
三、场景 2：线上分支代码错误，需回滚到历史版本
如果修复来不及，直接回滚远程分支到上一个稳定版本（禁止直接 git push -f，除非团队明确约定）：
步骤 1：找到稳定版本的 commit ID
bash
运行
# 查看提交历史，找到上一个稳定的commit（比如abc123）
git log --oneline
步骤 2：本地回滚并推送到远程（安全方式）
bash
运行
# 1. 切回线上分支
git checkout release-1.0

# 2. 用revert创建回滚提交（保留历史，可追溯）
git revert abc123  # 生成一个新提交，撤销abc123的修改
# （如果是多个提交，用git revert abc123..def456）

# 3. 推送到远程（无强制，安全）
git push origin release-1.0
步骤 3：无中断部署（同场景 1 的部署步骤）
# 四、绝对禁止的操作（避免服务中断 / 数据丢失）
禁止直接强制推送远程分支：git push -f origin release-1.0会覆盖远程历史，若其他节点拉取代码会导致代码不一致，引发服务异常；
禁止直接停掉所有实例再部署：必须保留至少一个可用实例承接流量；
禁止未测试就部署：本地 / 测试环境验证修复效果后，再推远程 + 部署。
# 五、优化建议（提升紧急修复效率）
提前配置 CI/CD：绑定线上分支，代码推送到远程后自动触发灰度部署，减少手动操作时间；
保留分支版本快照：每次发布后给分支打 tag（git tag v1.0.1），回滚时直接基于 tag 操作；
制定应急流程：明确谁负责改代码、谁审核、谁部署，避免紧急时混乱；
监控兜底：部署后通过监控（如 Prometheus、ELK）观察服务状态，若异常快速切回旧版本。
```



![](https://i-blog.csdnimg.cn/blog_migrate/7a4c9ee492db52f9ccebbf1327c46c5f.png)

**功能分支要求足够细粒度以避免成为长期存在的功能分支，应当小步合并而不是一次合并大量代码。**

注意事项：

Git 切换分支就是把工作区还原到目标分支所指向的最新提交的状态 所以要保证工作区没有未提交的修改不然就无了

冲突解决后必须提交

git pull -rebase 保持线性干净 不会有多余的merge记录



自己：test2优化

他人/远程目前：test2优化1 

pull冲突后合并自己和他人的 提交合并记录

![image-20250930151303538](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930151303538.png)



`merge` 保留分支历史，形成分叉。

`rebase` 让提交记录更直线化，但可能重写历史

**stash 命令**

![image-20250930151628781](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930151628781.png)

**stash 后暂存区和工作区（未提交的修改）都会被保存起来**

---



![image-20250930151713338](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930151713338.png)



回滚代码：

**reset**：本地回退（危险，改历史），常用于本地改错了想丢弃。

| 场景                                   | 使用方式  | 说明                               |
| -------------------------------------- | --------- | ---------------------------------- |
| 本地 commit 错误，但修改需要保留       | `--soft`  | 修改仍在索引，可以直接调整提交信息 |
| 本地 commit 错误，准备重新选择提交内容 | `--mixed` | 修改保留在工作区，索引清空         |
| 本地误操作，需要彻底丢弃               | `--hard`  | 修改和提交都丢弃，慎用             |

**revert**：生成一个新的 commit，抵消某次提交，历史保留，团队协作常用。

**checkout**：切换分支/版本/文件，用于丢弃未提交的修改。

`git checkout` 是 **将工作区（Working Directory）和 HEAD/暂存区（Staging Area）同步到指定目标**：

- 目标可以是：

  - **分支名** → 切换分支

  - **commit ID** → 回到历史版本（游离 HEAD）

  - **文件路径** → 恢复某个文件到 HEAD 或指定 commit

  - `git checkout` 是 **将工作区（Working Directory）和 HEAD/暂存区（Staging Area）同步到指定目标**：

    - 目标可以是：

      - **分支名** → 切换分支
      - **commit ID** → 回到历史版本（游离 HEAD）
      - **文件路径** → 恢复某个文件到 HEAD 或指定 commit

      

```
.gitignore 只影响未跟踪文件，已被跟踪的需要先 git rm --cached
```



​	



![image-20250930153912262](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930153912262.png)



**工作树（Working Tree）**：当前文件系统中的文件，编辑就在这里修改。

**索引 / 暂存区（Index / Staging Area）**：准备提交的快照，`git add` 后进入这里。

**HEAD**：当前检出的分支指针，指向最近一次提交。



**正常情况**：HEAD 指向**某个分支的最新提交**（commit），例如 `main` 或 `dev`。



**游离 HEAD**：HEAD 直接指向 **某个具体 commit**，而不是分支

可以在这个状态下查看、运行、修改代码，但提交默认不会被分支引用。

游离 HEAD 是 Git 提供的“临时沙盒”，用于探索历史或做实验，不影响分支，是安全测试和版本回溯的利器

---

<span style="color:#FF0000;">**解决合并冲突的步骤以及最佳实践是什么**：</span>



1. **经常拉取更新**
   - `git fetch` + `git merge/rebase`，避免长时间分支漂移导致大量冲突
2. **小步提交**
   - 每次修改量小、功能单一
   - 冲突定位和解决更容易
3. **使用分支策略**
   - `feature` 分支开发 → `develop` → `main`
   - 避免多人同时修改同一文件
4. **工具辅助**
   - IDE 内置合并工具（VSCode、IntelliJ、Windsurf 等）
   - 图形化显示冲突，更直观
5. **保留逻辑清晰**
   - 合并时不要随意删除内容
   - 保证最终版本逻辑正确
6. **测试**
   - 合并完成后，务必运行测试
   - 避免因为错误冲突处理导致功能异常

---



**git fetch**：只拉取远程分支更新到本地，不修改工作区。

**从远程仓库拉取最新的提交和引用信息**

**不会修改当前分支的工作区和暂存区**

本质上是 **同步远程分支到本地的远程跟踪分支**

~~~
远程仓库：服务器上的仓库，例如 origin

远程分支：远程仓库上的分支，例如 origin/main、origin/dev

本地远程跟踪分支 (remote-tracking branch)：本地保存的 远程分支快照，表示上一次从远程获取时的状态。
~~~



**git pull**：等于 `git fetch` + `git merge`，会直接把远程更新合并到当前分支

**git log** ：`git log` 用来 **查看 Git 提交历史**，

```bash
git log --graph --oneline --all
```

**图形化显示分支合并情况，常用于查看分支结构**



---



公共的话一定要注意历史，不然到时候别人远程拉取的时候会**冲突**

![image-20250930154319600](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250930154319600.png)

---



🩸 写在前面
-------

在工作场合实施 Git 的时候，有很多种[工作流](https://so.csdn.net/so/search?q=%E5%B7%A5%E4%BD%9C%E6%B5%81&spm=1001.2101.3001.7020)程可供选择，此时反而会让你手足无措。企业团队最常用的一些 Git 工作流程，包括 Centralized Workflow、Feature Branch Workflow、Gitflow Workflow、Forking [Workflow](https://so.csdn.net/so/search?q=Workflow&spm=1001.2101.3001.7020)。

在你开始阅读之前，请记住：这些 Git 工作流程应被视作为指导方针，而非 “铁律”。我们只是想告诉你可能的做法。因此，如果有必要的话，你可以组合使用不同的流程。

---



**SelfThought：**

不能/不应直接推送代码时，就需要**发起 Pull Request。** （发起**Pull Request**（将某个分支的修改合并到目标分支） 是在 代码托管平台上）

![image-20250720212826827](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720212826827.png)

**✅ 方法一：将用户加入你的项目协作者（适合个人仓库）**

适合你拥有个人 GitHub 仓库（不是组织），你想让朋友一起协作开发。

📌 操作步骤：

1. 打开你的 GitHub 仓库页面，例如 `https://github.com/your-name/your-repo`
2. 点击上方的 `⚙️ Settings`（右上角）
3. 在左边导航栏选择 **Collaborators and teams**
4. 点击 **Add collaborator**
5. 输入对方的 GitHub 用户名，然后点击 **Add**（GitHub 会发送邀请）
6. 对方接受邀请后，即可对你的仓库进行 push、创建分支、发 PR 等操作

🔒 默认权限是 **write（写权限）**，可以 push 和合并 PR。



**✅ 方法二：在组织中设置团队权限（适合组织仓库）**

如果你的项目属于一个 GitHub Organization（比如 `github.com/your-org/your-repo`），可以通过**团队**方式细粒度分配权限。

📌 操作步骤：

1. 打开 `github.com/your-org`
2. 点击 `People` → 添加成员到组织（如未加入）
3. 点击 `Teams` → 新建或管理团队
4. 分配该团队对某个仓库的权限：`Read / Write / Admin / Maintain / Triage`

权限说明：

| 权限等级   | 能做什么                         |
| ---------- | -------------------------------- |
| `Read`     | 仅查看代码和 PR                  |
| `Triage`   | 管理 issue/PR 标签、分配、关闭   |
| `Write`    | 提交代码、创建分支、合并 PR      |
| `Maintain` | 管理仓库设置，但不能删除仓库     |
| `Admin`    | 所有操作，包括设置权限、删除仓库 |



**✅ 方法三：设置仓库的 GitHub Actions 权限 / 分支保护（更细粒度）**

你还可以在：

- `Settings → Actions` 设置 CI/CD 权限
- `Settings → Branches → Branch protection rules` 中设置：
  - 哪些人能 push 到主分支
  - 是否必须 Pull Request 才能合并
  - 是否需要 Review 才能合并
  - 是否启用代码签名、CI 校验等

📌 注意事项

- GitHub 免费账户也可以添加协作者（最多3个）；
- 如果你添加的是外部开发者，最好使用 Fork + PR 模式；
- 如果项目比较大，建议使用 GitHub Organization 管理权限更安全清晰；
- 添加协作者后，别忘了在 README 中更新贡献指南。



|                | 有权限（协作者） | 没权限（外部贡献者） |
| -------------- | ---------------- | -------------------- |
| 是否需要 fork  | ❌ 不需要         | ✅ 需要               |
| 分支在哪里创建 | 原仓库           | 你 fork 的仓库       |
| 发起 PR 的目标 | 原仓库的主分支   | 原仓库的主分支       |

| 命令                       | 改历史记录 | 生成新提交       | 是否安全（多人协作） | 适用场景                                |
| -------------------------- | ---------- | ---------------- | -------------------- | --------------------------------------- |
| `git revert`               | ❌ 不改历史 | ✅ 会生成新的提交 | ✅ 安全               | 已经 push 到远程，需回滚错误提交        |
| `git reset`（undo commit） | ✅ 会改历史 | ❌ 不会生成新提交 | ⚠️ 危险（慎用于远程） | 本地撤销提交（尚未 push）或修改提交历史 |

**已经 push 到 GitHub 分支（远程）撤回提交**

~~~bash
git revert <commit-id> `revert保留历史好`
git push origin <branch-name>

~~~

`git cherry-pick <commit-id>` 会把指定提交的**改动内容复制一份**，并作为**新的提交**添加到当前分支。

 **然后选择本地提交 后cherry pick 回到自己push到远程前的工作区状态**



---



**分支是平级关系没有包含关系**

`-u` 是让本地分支和远程分支建立**“跟踪关系”**，之后**可以省略**远程分支名，简化命令。

“跟踪关系”是本地分支与远程分支之间的绑定关系，表示**本地分支**默认跟谁（远程分支）同步（pull/push）

| 本地分支名           | 远程分支名                  | 说明                  |
| -------------------- | --------------------------- | --------------------- |
| `master`             | `origin/master`             | 默认主分支            |
| `dev`                | `origin/dev`                | 开发主线              |
| `feature/login`      | `origin/feature/login`      | 登录功能开发分支      |
| `bugfix/user-avatar` | `origin/bugfix/user-avatar` | 用户头像的 bug 修复   |
| `release/1.0.0`      | `origin/release/1.0.0`      | v1.0.0 版本预发布分支 |

## `git merge` 到底做了什么？

假设你当前分支是 `A`，想合并分支 `B`。

- **Git 会先找到 `A` 和 `B` 最近的共同祖先**（Common Ancestor，也叫 merge base），记为 `O`。
- Git 计算两个分支从 `O` 到 `A` 和从 `O` 到 `B` 的差异（即两条路径上分别的改动）。
- Git 试图将**两个差异合成一个最终结果。**
  - 如果修改的内容不冲突，Git 会自动把改动合并。
  - 如果有冲突（同一行不同修改），**Git 会暂停，提示你手动解决冲突。**
- 自动合并成功后，**Git 创建一个新的提交 `M`：**
  - `M` 有两个父提交：当前分支的最新提交 `A` 和被合并分支的最新提交 `B`。
  - `M` 的内容是合并后的代码快照。
- 当前分支指针指向新提交 `M`，完成合并。

![image-20250719005230940](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250719005230940.png)

一、 GitFlow 介绍
-------------

### 1.1 什么是 GitFlow

**GitFlow** 是一种 Git 工作流，这个工作流程围绕着 project 的发布 (release) 定义了一个严格的如何建立分支的模型。它是团队成员遵守的一种代码管理方案 。

Git 建分支是非常 cheap 的，我们可以任意建立分支，对任意分支再分支，分支开发完后再合并。

比较推荐、多见的做法是特性驱动 (Feature Driven) 的建立分支法(Feature Branch Workflow)。

简而言之，就是每一个特性 (feature) 的开发并不直接在主干上开发，而是在分支上开发，分支开发完毕后再合并到主干上。

这样做的好处是：

1.  还处于半成品状态的 feature 不会影响到主干
    
2.  各个开发人员之间做自己的分支，互不干扰
    
3.  主干永远处于可编译、可运行的状态
    

GitFlow 则在这个基础上更进一步，规定了如何建立、合并分支，如何发布，如何维护历史版本等工作流程。

> 在工作场合实施 Git 的时候，有很多种工作流程可供选择，此时反而会让你手足无措。企业团队最常用的一些 Git 工作流程，包括 Centralized Workflow、Feature Branch Workflow、Gitflow Workflow、Forking Workflow。  
> 在你开始阅读之前，请记住：这些 Git 工作流程应被视作为指导方针，而非 “铁律”。我们只是想告诉你可能的做法。因此，如果有必要的话，你可以组合使用不同的流程。
> 
>   
> 本文主要介绍 Gitflow Workflow，愿以此文抛砖引玉…… 

### 1.2 GitFlow 常用分支说明

<table><thead><tr><th>分支名称</th><th>分支说明</th></tr></thead><tbody><tr><td>Production</td><td>生产分支，即 Master 分支。只能从其他分支合并，不能直接修改</td></tr><tr><td>Release</td><td>发布分支，基于 Develop 分支创建，待发布完成后合并到 Develop 和 Production 分支去</td></tr><tr><td>Develop</td><td>主开发分支，包含所有要发布到下一个 Release 的代码，该分支主要合并其他分支内容</td></tr><tr><td>Feature</td><td>新功能分支，基于 Develop 分支创建，开发新功能，待开发完毕合并至 Develop 分支</td></tr><tr><td>Hotfix</td><td>修复分支，基于 Production 分支创建，待修复完成后合并到 Develop 和 Production 分支去，同时在 Master 上打一个 tag</td></tr></tbody></table>

### 1.3 Git flow 中的分支介绍

Git Flow 的核心就是分支 (Branch），通过在项目的不同阶段对分支的不同操作（包括但不限于创建、合并、变基等）来实现一个完整的高效率的工作流程。Git Flow 模型中定义了**主分支**和**辅助**分支两类分支。其中主分支包含主要分支和开发分支，用于组织与软件开发、部署相关的活动；辅助分支包含功能分支、预发分支、热修复分支以及其他自定义分支，是为了解决特定的问题而进行的各种开发活动。 与主分支不同，这些分支总是有有限的生命时间，因为它们最终将被移除。

> 主分支：master 分支、develop 分支；辅助分支：feature 分支、release 分支、hotfix 分支

#### 1.3.1 主要分支**（Master）**

![](https://i-blog.csdnimg.cn/blog_migrate/b0d58b00fad45c01b2ae001c6ad7c52b.png)

主要分支上存放的是最稳定的正式版本，并且该分支的代码应该是**随时可在生产环境中使用的代码**。当一个版本开发完毕后，产生了一份新的稳定的可供发布的代码时，主要分支上的代码要被更新。同时，每一次更新，都需要在主要分支上打上对应的版本号。

任何人不允许在主要分支上进行代码的直接提交，只接受其他分支的合入。原则上主要分支上的代码必须是合并自经过多轮测试及已经发布一段时间且**线上稳定的预发分支。**

> master 分支只存放历史发布 (release) 版本的源代码。即用于存放对外发布的版本，任何时候在这个分支获取到的都是稳定的已发布的版本。各个版本通过 tag 来标记。上图里的 v0.1 和 v0.2 就是 tag。

#### 1.3.2 开发分支（Develop）

![](https://i-blog.csdnimg.cn/blog_migrate/b0d58b00fad45c01b2ae001c6ad7c52b.png)

开发分支是主开发分支，其上更新的代码始终反映着下一个发布版本需要交付的新功能。**当开发分支到达一个稳定的点并准备好发布时，应该从该点拉取一个==预发分支==并附上发布版本号。**也有人称开发分支为集成分支，因为会基于该分支和持续集成工具做自动化的构建。

开发分支接受其他辅助分支的合入，最常见的就是功能分支，开发一个新功能时拉取新的功能分支，开发完成后再并入开发分支。需要注意的是，合入开发的分支必须保证功能完整，不影响开发分支的正常运行。 

> develop 分支则用来整合各个 feature 分支。开发中的版本的源代码存放在这里。即用于日常开发，存放最新的开发版。

#### 1.3.3 **功能分支（Feature）**

![](https://i-blog.csdnimg.cn/blog_migrate/b9fcc65287cf22042571bde1570d1880.png)

功能分支一般命名为 Feature/xxx，用于开发即将发布版本或未来版本的新功能或者探索新功能。该分支通常存在于开发人员的本地代码库而不要求提交到远程代码库上，除非几个人合作在同一个功能分支开发。关于这点，Thought Works 洞见上有一篇文章 “Git Flow 有害论” 做了非常有意思的阐述，文章下的评论也异常激烈。也许该文章的名字可能有失偏颇，但文章的本意以及评论传达了一个观点：**功能分支要求足够细粒度以避免成为长期存在的功能分支，应当小步合并而不是一次合并大量代码。**

功能分支只能拉取自开发分支，开发完成后要么合并回开发分支，要么因为新功能的尝试不如人意而直接丢弃。

> 每一个特性 (feature) 都必须在自己的分支里开发，feature 分支派生自 develop 分支。  
>  
> 
> feature 分支只存在于开发者本地，不能被提交到远程库。当 feature 开发完毕后，要合并回 develop 分支。feature 分支永远不会和 master 分支打交道。

#### 1.3.4 **预发分支（Release）**

![](https://i-blog.csdnimg.cn/blog_migrate/5a36c34978dd7a162bed70ef580a5036.png)

**预发分支一般命名为 Release/1.2（后面是版本号）**，该分支专为**测试—发布**新的版本而开辟，**<span style="color:#FF0000;">允许做小量级的 Bug 修复和准备发布版本的元数据信息（版本号、编译时间等</span>）**。==**通过创建预发分支，使得开发分支得以空闲出来接受下一个版本的新的功能分支的合入。**==(这个是**核心**)



**预发分支需要提交到服务器上，交由测试工程师进行测试，并由开发工程师==修复 Bug==（所以要合并回 ==开发分支== 和 ==主要分支==）。**同时根据该分支的特性我们可以部署自动化测试以及生产环境代码的自动化更新和部署。

预发分支**只能拉取自开发分**支，**合并回开发分支和主要分支。**

> release 分支不是一个放正式发布产品的分支，你可以将它理解为 “待发布” 分支。
> 
>   
> 我们用这个分支干所有和发布有关的事情，比如：
> 
> 1.  把这个分支打包给测试人员测试
>     
> 2.  在这个分支里修复 bug
>     
> 3.  编写发布文档
>     
> 
> 所以，在这个分支里面**绝对不会添加新的特性**。  
> 当和发布相关的工作都完成后，release 分支合并回 develop 和 master 分支。  
> 单独搞一个 release 分支的好处是，当一个团队在做发布相关的工作时，另一个团队则可以接着开发下一版本的东西。

#### 1.3.5 **热修复分支（Hotfix）**

![](https://i-blog.csdnimg.cn/blog_migrate/72b99d777400f7ce7f1f4b5209744d3c.png)

热修复分支一般命名为 Hotfix/1.2.1（后面是版本号），当生产环境的代码（主要分支上代码）遇到严重到必须立即修复的缺陷时，就需要从主要分支上指定的 tag 版本（比如 1.2）拉取热修复分支进行代码的紧急修复，并附上版本号（比如 1.2.1）。这样做的好处是不会打断正在进行的开发分支的开发工作，能够让团队中负责功能开发的人与负责代码修复的人并行、独立的开展工作。

热修复分支只能主要分支上拉取，测试通过后合并回主要分支和开发分支。

> 一个项目发布后或多或少肯定会有一些 bug 存在，而 bug 的修复工作并不适合在 develop 上做，这是因为
> 
> 1.  develop 分支上包含还未验证过的 feature
>     
> 2.  用户未必需要 develop 上的 feature
>     
> 3.  develop 还不能马上发布，而客户急需这个 bug 的修复。
>     
> 
> 这时就需要新建 hotfix 分支，hotfix 分支派生自 master 分支，仅仅用于修复 bug，当 bug 修复完毕后，马上回归到 master 分支，然后发布一个新版本，比如，v0.1.1。  
> 同时 hotfix 也要合并回 develop 分支，这样 develop 分支就能享受到 bug 修复的好处了。

### 1.4 GitFlow 工作流程

![](https://i-blog.csdnimg.cn/blog_migrate/c727d78386d29e9a13b77f4aa6b82a99.png)​

二、GitFlow 实践
------------

### 2.1 创建 develop 分支

```
# 创建 develop 分支 
git branch develop
# 将 develop 分支推送到远端仓库
git push -u origin develop
```

### 2.2 开始新的 **Feature**

```
# 通过develop新建feaeure分支
git checkout -b Feature分支名 develop
# 可选，将分支推送到远端仓库
git push -u origin Feature分支名
```

### 2.3 编辑 **Feature** 分支

```
# 查看状态
git status
# 添加提交内容
git add XXXfile
# 提交    
git commit
```

### 2.4 完成 **Feature** 分支

```
# 拉取远端仓库 develop 分支合并到本地 develop 分支
git pull origin develop
# 切换到 develop 分支     
git checkout develop
# 将 Feature 分支合并到 develop 分支    
	# --no-ff：不使用 fast-forward 方式合并，保留分支的 commit 历史
	# --squash：使用 squash 方式合并，把多次分支 commit 历史压缩为一次    
git merge --no-ff Feature分支名
# 将分支推送远端仓库 
git push origin develop
# 删除 Feature分支
git branch -d Feature分支名
```

### 2.5 开始 Release

```
# 创建 Relase 分支并切换到 Release 分支上
git checkout -b release-0.1.0 develop
```

### 2.6 完成 Release

```
# 切换到 master 分支上
git checkout master
# 合并 release-0.1.0 分支    
git merge --no-ff release-0.1.0    
# 推送到远端仓库
git push
# 切换到 develop 分支上    
git checkout develop
# 合并 release-0.1.0 分支   
git merge --no-ff release-0.1.0
# 推送到远端仓库   
git push
# 删除 release-0.1.0 分支 
git branch -d release-0.1.0
```

### 2.7 开始 Hotfix

```
# 创建 hotfix 分支并切换到 hotfix 分支上
git checkout -b hotfix-0.1.1 master
```

### 2.8 完成 Hotfix

```
# 切换到 master 分支
git checkout master
# 合并 hotfix-0.1.1 分支
git merge --no-ff hotfix-0.1.1
# 推送到远端仓库
git push
# 切换到 develop 分支
git checkout develop
# 合并 hotfix-0.1.1 分支
git merge --no-ff hotfix-0.1.1
# 推送到远端仓库
git push
# 删除 release-0.1.0 分支    
git branch -d hotfix-0.1.1
# 为主分支打上版本标签
git tag -a v0.1.1 master
# 将标签推送到远端仓库  
git push --tags
```

三、GitFlow 模拟
------------

下面的例子将演示 Gitflow 流程如何被用来管理一次产品发布。假设你已经创建好了一个中央仓库。

### **3.1 创建 develop 分支**

![](https://i-blog.csdnimg.cn/blog_migrate/c8ba70e26fb95aa06a709777dd272d26.webp?x-image-process=image/format,png)

第一步是给默认的 master 配备一个 develop 分支。一种简单的做法是：让一个开发者在本地建立一个空的 develop 分支，然后把它推送到服务器。

```
git branch develop
git push -u origin develop
```

develop 分支将包含项目的所有历史，而 master 会是一个缩减版本。现在，其他开发者应该克隆（clone）中央仓库，并且为 develop 创建一个追踪分支。

```
git clone ssh://user@host/path/to/repo.git
git checkout -b develop origin/develop
```

到现在，所有人都把包含有完整历史的分支（develop）在本地配置好了。

### **3.2 小马和小明开始开发新功能**

**![](https://i-blog.csdnimg.cn/blog_migrate/eff25651b3038117033555ff818a3480.webp?x-image-process=image/format,png)** 

我们的故事从小马和小明要分别开发新功能开始。他们俩各自建立了自己的分支。注意，他们在创建分支时，父分支不能选择 master，而要选择 develop。

```
git status
git add <some-file>
git commit
```

他们俩都在自己的功能开发分支上开展工作。通常就是这种 Git 三部曲：edit，stage，commit：

```
git pull origin develop
git checkout develop
git merge some-feature
git push
git branch -d some-feature
```

### **3.3 小马把她的功能开发好了**

![](https://i-blog.csdnimg.cn/blog_migrate/ddd14d508f5ec5cf59d7c077342c7bd2.webp?x-image-process=image/format,png)

在提交过几次代码之后，小马觉得她的功能做完了。如果她所在的团队使用 “拉拽请求”，此刻便是一个合适的时机——她可以提出一个将她所完成的功能合并入 develop 分支的请求。要不然，她可以自行将她的代码合并入本地的 develop 分支，然后再推送到中央仓库，像这样：

```
git checkout master
git merge release-0.1
git push
git checkout develop
git merge release-0.1
git push
git branch -d release-0.1
```

第一条命令确保了本地的 develop 分支拥有最新的代码——这一步必须在将功能代码合并之前做！注意，新开发的功能代码永远不能直接合并入 master。必要时，还需要解决在代码合并过程中的冲突。

### **3.4 小马开始准备一次发布**

![](https://i-blog.csdnimg.cn/blog_migrate/8bce920e84605faf3fbfb461a761a7ba.webp?x-image-process=image/format,png)

尽管小明还在忙着开发他的功能，小马却可以开始准备这个项目的第一次正式发布了。类似于功能开发，她使用了一个新的分支来做产品发布的准备工作。在这一步，发布的版本号也最初确定下来。

```
git tag -a 0.1 -m"Initial public release" master
git push --tags
```

这个分支专门用于发布前的准备，包括一些清理工作、全面的测试、文档的更新以及任何其他的准备工作。它与用于功能开发的分支相似，不同之处在于它是专为产品发布服务的。

一旦小马创建了这个分支并把它推向中央仓库，这次产品发布包含的功能也就固定下来了。任何还处于开发状态的功能只能等待下一个发布周期。

### **3.5 小马完成了发布**

![](https://i-blog.csdnimg.cn/blog_migrate/42bfc43cebcf6e065f3250d0de412e52.webp?x-image-process=image/format,png)

一切准备就绪之后，小马就要把发布分支合并入 master 和 develop 分支，然后再将发布分支删除。注意，往 develop 分支的合并是很重要的，因为开发人员可能在发布分支上修复了一些关键的问题，而这些修复对于正在开发中的新功能是有益的。再次提醒一下，如果小马所在的团队强调代码评审（Code Review），此时非常适合提出这样的请求。

```
git checkout -b issue-#001 master
\# Fix the bug
git checkout master
git merge issue-#001
git push
```

发布分支扮演的角色是功能开发（develop）与官方发布（master）之间的一个缓冲。无论什么时候你把一些东西合并入 master，你都应该随即打上合适的标签。

```
git checkout develop
git merge issue-#001
git push
git branch -d issue-#001
```

Git 支持钩子（hook）的功能，也就是说，在代码仓库里某些特定的事件发生的时候，可以执行一些预定义的脚本。因此，一种可行的做法是：在服务器端配置一个钩子，当你把 master 推送到中央仓库或者推送标签时，Git 服务器能为产品发布进行一次自动的构建。

### **3.6 用户发现了一个 bug**

![](https://i-blog.csdnimg.cn/blog_migrate/a1ac0f204c21044b121d6a4e805f4d96.webp?x-image-process=image/format,png)

当一次发布完成之后，小马便回去与小明一起开发其他功能了。突然，某个用户提出抱怨说当前发布的产品里有一个 bug。为了解决这个问题，小马（或者小明）基于 master 创建了一个用于维护的分支。她在这个分支上修复了那个 bug，然后把改动的代码直接合并入 master。

```
git flow release finish RELEASE
git push --tags
```

跟用于发布的分支一样，在维护分支上的改动也需要合并入 develop 分支，这一点是很重要的！因此，小马务必不能忘了这一步。随后，她就可以将维护分支删除。

```
git checkout develop
git merge issue-#001
git push
git branch -d issue-#001
```

四、 GitFlow 工具推荐 | 配套工具
----------------------

### 4.1 Git flow script(命令行)

![](https://i-blog.csdnimg.cn/blog_migrate/7222701d84c764ccb18c61ba27249ede.png)​

Git Flow 不仅仅是一种规范，还提供了一套方便的工具。大大简化了执行 Git Flow 的过程。

#### **✔️ 安装**

1. OSX

```
$ brew install git-flow
```

2. Debian/Ubuntu Linux

```
$ apt-get install git-flow
```

3. Windows(cygwin)

```
$ wget -q -O - --no-check-certificate https://github.com/nvie/gitflow/raw/develop/contrib/gitf
```

#### **◼️ 初始化（Initialize）**

对一个 git 仓库配置一下 git flow。主要是一些命名规范，比如 feature 分支的前缀，hotfix 分支的前缀等。一般用默认值就行。

```
git flow init
```

#### **◼️ 功能分支（Feature ）**

**——开始新 Feature:**

Start a new feature

从 develop 开启一个新的分支

```
git flow feature start MYFEATURE
```

这个命令会从 develop 分出一个分支，然后切换到这个分支上面。 

**——Publish 一个 Feature(也就是 push 到远程):**

Publish a feature

如果你想让别人和你一起开发 MYFEATURE 分支，那就把这个分支 push 到服务器上

```
git flow feature publish MYFEATURE
```

**—— 获取 Publish 的 Feature:**

Getting a published feature

获得一个别人 publish 到服务器上的 feature 分支

```
git flow feature pull origin MYFEATURE
```

**—— 完成一个 Feature:**

Finish up a feature

一个 feature 分支开发完毕后，要做以下事情：

*   把 MYFEATURE 合并到 develop
    
*   把这个分支干掉
    
*   切换回 develop 分支
    

```
git flow feature finish MYFEATURE
```

#### **◼️ 预发分支（Release）**

**—— 开始一个 Release:**

Start a release

创建一个 release 分支，派生自 develop 分支。

```
git flow release start RELEASE [BASE]
```

**—— Publish 一个 Release:**

Publish a release

```
git flow release publish RELEASE
```

**—— 发布一个 Release:**

Finish up a release

一个 release 分支结束后，需要做以下工作：

*   把 release 分支合并回 master
    
*   给本次发布打 tag
    
*   同时把 release 分支合并回 develop
    
*   干掉 release 分支
    

```
git flow release finish RELEASE
git push --tags
```

**注：**最后不要忘记把 tag push 到服务器**`git push --tags`** 

#### **◼️ 热修复分支（Hotfix）**

**—— 开始一个 Hotfix:**

git flow hotfix start

开启一个 hotfix 分支

```
git flow hotfix start VERSION [BASENAME]
```

**—— 发布一个 Hotfix:**

Finish a hotfix

结束一个 hotfix 分支，和 release 一样，同时合并回 develop 和 master

```
git flow hotfix finish VERSION
```

### **4.2 Git Flow** [](#31-git-flow-script%E5%91%BD%E4%BB%A4%E8%A1%8C) **SourceTree (图形化)** 

**📥 SourceTree 下载官方：**[Sourcetree | Free Git GUI for Mac and Windows](https://www.sourcetreeapp.com/ "Sourcetree | Free Git GUI for Mac and Windows")

**🎈 大神推荐 SourceTree**：[使用 SourceTree - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/896043488029600/1317161920364578 "使用SourceTree - 廖雪峰的官方网站") 

![](https://i-blog.csdnimg.cn/blog_migrate/8bbcb5e38c74e92257ea8a8c49f99f9f.png)

#### ✔️Gitflow 结合 [SourceTree](https://so.csdn.net/so/search?q=SourceTree&spm=1001.2101.3001.7020) 实践​

1. 创建本地仓库 + 远程仓库

...... 此处略过

2. 打开该仓库 SourceTree 控制界面

![](https://i-blog.csdnimg.cn/blog_migrate/fdc11967e22c4bd67a9404f520bc99ca.png)

3. 添加完成之后点击该按钮

![](https://i-blog.csdnimg.cn/blog_migrate/5dc98cca5a1356222dafcdf2449dc9d6.png)

**注意**： 此处是配置，开发分支，发布分支名称，以及开发功能分支前缀，发布分支前缀，热修复分支前缀，以及版本号前缀。建议使用默认的形式。

4. 初始化完成

![](https://i-blog.csdnimg.cn/blog_migrate/26879802453ea92c028d3efc9d53c42c.webp?x-image-process=image/format,png)

此处会多出 develop 与 master 分支

5. 开发功能模块

点击 gitflow 图标，new 一个 feature 分支，然后输入当前要做的模块名称。

**注意**：此处最好在最新的 develop 分支上，进行创建 feature，这样确保更少的冲突。

![](https://i-blog.csdnimg.cn/blog_migrate/f27f182f5740aa66190163d9f3e92e44.webp?x-image-process=image/format,png)

为该 feature 分支起一个名字

![](https://i-blog.csdnimg.cn/blog_migrate/bb7adb04692bb320b15823d2c8e86070.webp?x-image-process=image/format,png)

完成之后，可见当前分支的情况。

![](https://i-blog.csdnimg.cn/blog_migrate/5fee16189cc35635633a21d82af9a4a8.webp?x-image-process=image/format,png)

6. 完成功能模块

完成开发之后，先 commit 到本地的 feature 分支上。然后点击 gitflow 按钮

![](https://i-blog.csdnimg.cn/blog_migrate/ad8d89d94b3bda76d000b39f170a1489.webp?x-image-process=image/format,png)

**注意**：首先查看 develop 分支有没有其他人提交的记录，如果有需要 pull 下来的，先切回到 develop 分支先 pull 下来。然后切回到 feature 分支下。进行 finish current 操作。

![](https://i-blog.csdnimg.cn/blog_migrate/bb5bd9f66fd1c868991065521e37c0cc.webp?x-image-process=image/format,png)

**注意**：一般的开发完成之后，选择删除当前的 feature 分支，因为此处的分支为本地分支，你也可以选择保留当前 feature 分支，选择 OK 之后，会将当前的 feature 分支的内容合并到本地的 develop 分支上。

如果需要推送到 origin，即可以推送到 origin 对应的分支上。

![](https://i-blog.csdnimg.cn/blog_migrate/21d839e86158331fe96dd5f7fb468062.webp?x-image-process=image/format,png)

7. 进行发布

点击 gitflow 按钮，然后选择 new release

![](https://i-blog.csdnimg.cn/blog_migrate/b87d47a0e02d7c0ab14cc1b70bc33458.webp?x-image-process=image/format,png)

输入需要发布的版本号，此处输入的会将成为版本 Tag 信息。

![](https://i-blog.csdnimg.cn/blog_migrate/2628d6c5a2c3a502fd534ca27def8684.webp?x-image-process=image/format,png)

然后将项目中需要改版本的号的文件进行相对应的提交和修改。完成之后 commit 到当前的 release 分支上。

![](https://i-blog.csdnimg.cn/blog_migrate/f468916344818db3387d037008fa55ab.webp?x-image-process=image/format,png)

8. 完成发布

版本配置文件修改完成之后，进行合并，点击 gitflow 按钮，出现了，然后点击 Finish Current。

![](https://i-blog.csdnimg.cn/blog_migrate/e4ce954f1e785d83e97a4fb0facad029.webp?x-image-process=image/format,png)

**注意**：此处输入的信息，是对当前的 Tag 定制的提交信息。

![](https://i-blog.csdnimg.cn/blog_migrate/e9d1ef0538da5f43c76faf1ce3fecde4.webp?x-image-process=image/format,png)

点击完后后，会将当前的 release 分支合并到 develop，master 分支，是否要推倒 origin，由 coder 自己决定。这样做的好处是，master 分支上的每个节点，都是一个版本。方便查阅。

![](https://i-blog.csdnimg.cn/blog_migrate/5e36f51026b4977b0939259cc42734c8.webp?x-image-process=image/format,png)

**注意**：此处发布时，需要 team 中，负责发布的 coder 去操作，避免多人发布，造成版本号，Tag 混乱。

9. 开始热修复

如果版本发出后，出现了一个 bug，需要紧急的去修改，则需要使用 new 一个 hotfix，去进行开发。

![](https://i-blog.csdnimg.cn/blog_migrate/5d62bb82bc068eb19cb052b7553c26cb.webp?x-image-process=image/format,png)

**注意**：Hotfix 分支是在最新节点的 master 分支上创建的，此处填入的 hotfix 的版本号。

10. 完成热修复

完成 Bug 修复代码工作之后，提交到当前的本地 hotfix 分支上，完后进行 finish 当前的 hotfix 分支，此处操作与 release 相同。

![](https://i-blog.csdnimg.cn/blog_migrate/64e77350cec86b52a66f2b4402c327ac.webp?x-image-process=image/format,png)

完成之后，会自动合并到本地的 master，develop 分支上，至于是否要 push 到 origin 由 Coder 自行决定。  


![](https://i-blog.csdnimg.cn/blog_migrate/08233ca88005e8c25d97622155896886.webp?x-image-process=image/format,png)

**五、Git Flow 模型总结**
-------------------

Git Flow 模型通过不同的分支从源代码管理的角度对软件开发活动进行了约束，为我们的软件开发提供了一个可供参考的管理模型。Git Flow 模型让代码仓库保持整洁，让小组各个成员之间的开发相互隔离，能够有效避免处于开发状态中的代码相互影响而导致的效率低下和混乱。但同时，不同的开发团队存在不同的文化，在不同的项目背景情况下都可能根据该模型进行适当的精简或扩充。防控中心通过合理使用 Git Flow，更好地管理代码仓库，提高工作的效率。 

**文献参考**

[0] [Git Flow - A successful branching model](https://nvie.com/posts/a-successful-git-branching-model/ "Git Flow - A successful branching model")

[1] [Git Flow of Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows "Git Flow of Workflow")

[2] [Another Git Flow introduction](https://docs.syntevo.com/SmartGit/Latest/ "Another Git Flow introduction")

[3] [Git Flow Cheatsheet](http://danielkummer.github.io/git-flow-cheatsheet/ "Git Flow Cheatsheet")

**参考资料**

[Gitflow 工作流程](https://blog.csdn.net/happydeer/article/details/17618935 "Gitflow工作流程") | [Gitflow 应用与 SourceTree 实践](https://www.jianshu.com/p/462d556c320f "Gitflow应用与SourceTree实践")

[Git flow 概念_什么是 gitflow](https://blog.csdn.net/Ann1205/article/details/103664465 "Git flow概念_什么是gitflow") | [Git Flow 工作流模型](https://baijiahao.baidu.com/s?id=1726693863458796523 "Git Flow工作流模型")

