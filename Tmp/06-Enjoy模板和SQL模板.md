# 评分要点6：Enjoy模板和SQL模板（10分）

## 评分标准
1. `#define` 指令的应用（5分）
2. `#sql` 指令的应用（5分）

## 项目符合情况：✅ 完全符合

---

## 一、#define 指令的应用（5分）

### 1. 公共布局模板

#### 文件位置：`docflow/src/main/webapp/view/common/_layout.html`

```html
<!-- 公共布局模板 -->

<!-- 定义主布局模板 -->
#define layout()
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#(title ?? 'DocFlow - 在线文档协作平台')</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Remix Icon -->
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <!-- 设计系统 -->
    <link rel="stylesheet" href="/view/common/design-system.css">
    <!-- 自定义样式 -->
    <style>
        /* 全局样式... */
    </style>
    <!-- 调用子模板定义的 head 部分 -->
    #@head()
</head>
<body>
    <!-- 移动端菜单按钮 -->
    <button class="mobile-menu-btn" id="mobileMenuBtn" onclick="toggleMobileMenu()">
        <i class="ri-menu-line"></i>
    </button>
    
    <!-- 全局加载动画 -->
    <div class="loading-overlay" id="globalLoading">
        <div class="loading-spinner"></div>
    </div>
    
    <!-- 调用子模板定义的 body 部分 -->
    #@body()
    
    <!-- Toast 容器 -->
    <div class="toast-container"></div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
    <!-- 公共JS -->
    <script>
        // Toast 消息提示
        function showToast(message, type = 'info') { /* ... */ }
        // AJAX 封装
        function ajax(url, data, success) { /* ... */ }
    </script>
    <!-- 调用子模板定义的 script 部分 -->
    #@script()
</body>
</html>
#end

<!-- 定义默认的空模板块（子模板可覆盖） -->
#define head()
#end

#define body()
#end

#define script()
#end

<!-- 定义侧边栏组件 -->
#define sidebar()
<aside class="sidebar" id="sidebar">
    <a href="/" class="brand">
        <img src="/favicon.svg" alt="DocFlow" style="width: 32px; height: 32px;">
        <span>DocFlow</span>
    </a>

    <div class="nav-group">
        <a href="/doc/list" class="nav-item #if(nav == 'mydoc') active #end">
            <i class="ri-file-list-line"></i>
            <span>我的文件库</span>
        </a>
        <a href="/share/list" class="nav-item #if(nav == 'share' && listType == 'toMe') active #end">
            <i class="ri-inbox-line"></i>
            <span>共享给我</span>
        </a>
        <a href="/doc/starred" class="nav-item #if(nav == 'starred') active #end">
            <i class="ri-star-line"></i>
            <span>收藏夹</span>
        </a>
    </div>

    <div class="nav-group">
        <div class="nav-label">系统</div>
        <a href="/doc/trash" class="nav-item #if(nav == 'trash') active #end">
            <i class="ri-delete-bin-line"></i>
            <span>回收站</span>
        </a>
        #if(loginUser != null && loginUser.role == 'admin')
        <a href="/admin" class="nav-item">
            <i class="ri-settings-3-line"></i>
            <span>管理后台</span>
        </a>
        #end
    </div>

    #if(loginUser != null)
    <div class="user-menu">
        <div class="nav-item" id="userDropdown" data-bs-toggle="dropdown">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--primary-500);">
                #(loginUser.username.substring(0, 1).toUpperCase())
            </div>
            <span>#(loginUser.nickname ?? loginUser.username)</span>
        </div>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" onclick="confirmLogout()">退出登录</a></li>
        </ul>
    </div>
    #end
</aside>
#end
```

### 2. 子模板继承布局

#### 文件位置：`docflow/src/main/webapp/view/mydoc.html`

```html
<!-- 继承公共布局 -->
#@layout()

<!-- 覆盖 head 部分，添加页面特定样式 -->
#define head()
<style>
    /* 自定义滚动条 */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
    
    /* 现代化头部 */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 32px;
    }
    
    /* 表格样式 */
    .data-table {
        width: 100%;
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--radius-xl);
        overflow: hidden;
    }
    
    /* ... 更多样式 */
</style>
#end

<!-- 覆盖 body 部分，定义页面内容 -->
#define body()
#if(nav == null) #set(nav = 'mydoc') #end
<!-- 调用侧边栏组件 -->
#@sidebar()

<main class="main-content">
    <div class="page-header">
        <h1>
            #if(nav == 'starred')
            <i class="ri-star-line" style="color:#F7BA2A"></i>
            #elseif(isTrash)
            <i class="ri-delete-bin-line" style="color:#EF4444"></i>
            #else
            <i class="ri-folder-open-line" style="color:#3b82f6"></i>
            #end
            #(pageTitle ?? '我的文件库')
        </h1>
        <div class="header-actions">
            <form action="/doc/list" method="get" class="search-box">
                <i class="ri-search-line"></i>
                <input type="text" name="keyword" placeholder="搜索文件..." value="#(keyword ?? '')">
            </form>
            #if(!isTrash)
            <button class="btn-action btn-create" onclick="showCreateModal()">
                <i class="ri-add-line"></i> 新建
            </button>
            #end
        </div>
    </div>
    
    <!-- 文档列表 -->
    <div class="data-table">
        #for(doc : docPage.list)
        <div class="table-row" data-doc-id="#(doc.id)">
            <div class="file-name">
                <span class="file-title">#(doc.title)</span>
            </div>
            <div>#date(doc.update_time, "yyyy-MM-dd HH:mm")</div>
        </div>
        #end
    </div>
    
    <!-- 分页 -->
    #if(docPage != null && docPage.totalPage > 1)
    <nav class="mt-4">
        <ul class="pagination justify-content-center">
            <li class="page-item #if(docPage.pageNumber == 1) disabled #end">
                <a class="page-link" href="?page=#(docPage.pageNumber - 1)">上一页</a>
            </li>
            <li class="page-item active">
                <span class="page-link">#(docPage.pageNumber)</span>
            </li>
            <li class="page-item #if(docPage.pageNumber == docPage.totalPage) disabled #end">
                <a class="page-link" href="?page=#(docPage.pageNumber + 1)">下一页</a>
            </li>
        </ul>
        <div class="text-center text-muted">
            第 #(docPage.pageNumber) 页 / 共 #(docPage.totalPage) 页，共 #(docPage.totalRow) 条
        </div>
    </nav>
    #end
</main>
#end

<!-- 覆盖 script 部分，添加页面特定脚本 -->
#define script()
<script>
    var currentFolderId = '#(folderId)';
    
    function openDoc(id) {
        window.location.href = '/doc/edit?id=' + id;
    }
    
    function createDoc(type) {
        var url = '/doc/add?type=' + type;
        if (currentFolderId) {
            url += '&folderId=' + currentFolderId;
        }
        window.location.href = url;
    }
    
    // ... 更多脚本
</script>
#end
```

### 3. #define 指令使用总结

| 模板文件 | #define 指令 | 用途 |
|----------|--------------|------|
| _layout.html | `#define layout()` | 定义主布局模板 |
| _layout.html | `#define head()` | 定义默认空的 head 块 |
| _layout.html | `#define body()` | 定义默认空的 body 块 |
| _layout.html | `#define script()` | 定义默认空的 script 块 |
| _layout.html | `#define sidebar()` | 定义侧边栏组件 |
| mydoc.html | `#define head()` | 覆盖 head，添加页面样式 |
| mydoc.html | `#define body()` | 覆盖 body，定义页面内容 |
| mydoc.html | `#define script()` | 覆盖 script，添加页面脚本 |
| edit.html | `#define head()` | 覆盖 head，添加编辑器样式 |
| edit.html | `#define body()` | 覆盖 body，定义编辑器内容 |

---

## 二、#sql 指令的应用（5分）

### 1. SQL模板配置

#### 文件位置：`docflow/src/main/java/com/docflow/common/DocflowConfig.java`

```java
@Override
public void configPlugin(Plugins me) {
    // ... 数据库连接配置
    
    // ActiveRecord 插件
    ActiveRecordPlugin arp = new ActiveRecordPlugin(dp);
    arp.setDevMode(PropKit.getBoolean("devMode", true));
    arp.setShowSql(PropKit.getBoolean("devMode", true));
    
    // 加载SQL模板文件（从classpath加载）
    arp.getEngine().setSourceFactory(new com.jfinal.template.source.ClassPathSourceFactory());
    arp.addSqlTemplate("sql/all.sql");
    
    // Model映射
    _MappingKit.mapping(arp);
    me.add(arp);
}
```

### 2. SQL模板文件

#### 文件位置：`docflow/src/main/resources/sql/all.sql`

```sql
-- ============================================
-- DocFlow SQL 模板文件
-- 用于 JFinal ActiveRecord SQL 模板功能
-- ============================================

-- 文档命名空间
#namespace("document")

    -- 根据用户ID查询文档列表（使用 #para 参数化查询）
    #sql("findByUserId")
        SELECT n.*, c.content, c.doc_type, c.is_starred, c.is_deleted, c.view_count
        FROM fs_node n
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE n.user_id = #para(userId) AND n.node_type = 'file'
        #if(isDeleted != null)
            AND c.is_deleted = #para(isDeleted)
        #end
        ORDER BY n.update_time DESC
    #end

    -- 分页查询文档（动态条件）
    #sql("pageByUserId")
        SELECT n.*, c.content, c.doc_type, c.is_starred, c.is_deleted, c.view_count
        FROM fs_node n
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE n.user_id = #para(userId) AND n.node_type = 'file'
        #if(isDeleted != null)
            AND c.is_deleted = #para(isDeleted)
        #end
        #if(isStarred != null)
            AND c.is_starred = #para(isStarred)
        #end
        ORDER BY n.update_time DESC
    #end

    -- 搜索文档（支持关键词模糊查询）
    #sql("search")
        SELECT n.*, c.content, c.doc_type, c.is_starred, c.is_deleted, c.view_count
        FROM fs_node n
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE n.user_id = #para(userId) AND n.node_type = 'file'
        AND (n.name LIKE CONCAT('%', #para(keyword), '%') OR c.content LIKE CONCAT('%', #para(keyword), '%'))
        ORDER BY n.update_time DESC
    #end

#end

-- 用户命名空间
#namespace("user")

    -- 分页查询用户（动态条件）
    #sql("page")
        SELECT * FROM user
        #if(keyword != null && keyword != '')
            WHERE username LIKE CONCAT('%', #para(keyword), '%')
            OR nickname LIKE CONCAT('%', #para(keyword), '%')
        #end
        ORDER BY create_time DESC
    #end

    -- 根据用户名查询
    #sql("findByUsername")
        SELECT * FROM user WHERE username = #para(username) LIMIT 1
    #end

#end

-- 共享命名空间
#namespace("share")

    -- 查询分享给我的文档（多表关联）
    #sql("sharedToMe")
        SELECT s.*, n.name as doc_name, u.nickname as from_user_name, c.doc_type
        FROM share s
        LEFT JOIN fs_node n ON s.document_id = n.id
        LEFT JOIN user u ON s.from_user_id = u.id
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE s.to_user_id = #para(userId)
        ORDER BY s.create_time DESC
    #end

    -- 查询我分享的文档
    #sql("sharedByMe")
        SELECT s.*, n.name as doc_name, u.nickname as to_user_name, c.doc_type
        FROM share s
        LEFT JOIN fs_node n ON s.document_id = n.id
        LEFT JOIN user u ON s.to_user_id = u.id
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE s.from_user_id = #para(userId)
        ORDER BY s.create_time DESC
    #end

#end

-- 文件系统节点命名空间
#namespace("fsNode")

    -- 查询子节点（动态条件处理NULL）
    #sql("findChildren")
        SELECT * FROM fs_node
        WHERE user_id = #para(userId)
        #if(parentId != null)
            AND parent_id = #para(parentId)
        #else
            AND parent_id IS NULL
        #end
        ORDER BY node_type DESC, name ASC
    #end

    -- 递归查询所有子节点ID（MySQL CTE语法）
    #sql("findAllChildIds")
        WITH RECURSIVE cte AS (
            SELECT id FROM fs_node WHERE id = #para(nodeId)
            UNION ALL
            SELECT n.id FROM fs_node n INNER JOIN cte ON n.parent_id = cte.id
        )
        SELECT id FROM cte
    #end

#end

-- 转发/分享链接命名空间
#namespace("forward")

    -- 分页查询用户的分享链接（聚合统计）
    #sql("pageByUserId")
        SELECT f.*, COUNT(fi.id) as item_count
        FROM forward f
        LEFT JOIN forward_item fi ON f.id = fi.forward_id
        WHERE f.user_id = #para(userId)
        GROUP BY f.id
        ORDER BY f.create_time DESC
    #end

    -- 根据分享key查询
    #sql("findByShareKey")
        SELECT * FROM forward WHERE share_key = #para(shareKey) LIMIT 1
    #end

    -- 查询分享链接包含的文件
    #sql("findItems")
        SELECT n.*, c.doc_type
        FROM forward_item fi
        LEFT JOIN fs_node n ON fi.fs_node_id = n.id
        LEFT JOIN document_content c ON n.id = c.node_id
        WHERE fi.forward_id = #para(forwardId)
    #end

#end
```

### 3. SQL模板指令说明

| 指令 | 说明 | 示例 |
|------|------|------|
| `#namespace("name")` | 定义SQL命名空间，用于组织SQL | `#namespace("document")` |
| `#sql("name")` | 定义一个SQL模板 | `#sql("findByUserId")` |
| `#para(name)` | 参数占位符，防止SQL注入 | `#para(userId)` |
| `#if(condition)` | 条件判断，动态拼接SQL | `#if(keyword != null)` |
| `#else` | 条件分支 | `#else` |
| `#end` | 结束指令块 | |

### 4. SQL模板特性

#### 动态SQL示例（条件查询）

```sql
#sql("pageByUserId")
    SELECT n.*, c.content, c.doc_type, c.is_starred, c.is_deleted, c.view_count
    FROM fs_node n
    LEFT JOIN document_content c ON n.id = c.node_id
    WHERE n.user_id = #para(userId) AND n.node_type = 'file'
    
    -- 动态条件：如果指定了删除状态则添加筛选
    #if(isDeleted != null)
        AND c.is_deleted = #para(isDeleted)
    #end
    
    -- 动态条件：如果指定了收藏状态则添加筛选
    #if(isStarred != null)
        AND c.is_starred = #para(isStarred)
    #end
    
    ORDER BY n.update_time DESC
#end
```

#### 动态SQL示例（NULL值处理）

```sql
#sql("findChildren")
    SELECT * FROM fs_node
    WHERE user_id = #para(userId)
    
    -- 动态处理NULL：parentId为空时查询根节点
    #if(parentId != null)
        AND parent_id = #para(parentId)
    #else
        AND parent_id IS NULL
    #end
    
    ORDER BY node_type DESC, name ASC
#end
```

#### 多表关联查询示例

```sql
#sql("sharedToMe")
    SELECT 
        s.*,                                    -- 共享记录字段
        n.name as doc_name,                     -- 文档名称
        u.nickname as from_user_name,           -- 分享者昵称
        c.doc_type                              -- 文档类型
    FROM share s
    LEFT JOIN fs_node n ON s.document_id = n.id     -- 关联文件节点表
    LEFT JOIN user u ON s.from_user_id = u.id       -- 关联用户表
    LEFT JOIN document_content c ON n.id = c.node_id -- 关联文档内容表
    WHERE s.to_user_id = #para(userId)              -- 接收者是当前用户
    ORDER BY s.create_time DESC                     -- 按共享时间倒序
#end
```

#### 聚合统计查询示例

```sql
#sql("pageByUserId")
    SELECT f.*, COUNT(fi.id) as item_count      -- 统计分享包含的文件数
    FROM forward f
    LEFT JOIN forward_item fi ON f.id = fi.forward_id
    WHERE f.user_id = #para(userId)
    GROUP BY f.id                               -- 按分享链接分组
    ORDER BY f.create_time DESC
#end
```

#### 递归查询示例（MySQL CTE）

```sql
#sql("findAllChildIds")
    WITH RECURSIVE cte AS (
        SELECT id FROM fs_node WHERE id = #para(nodeId)
        UNION ALL
        SELECT n.id FROM fs_node n INNER JOIN cte ON n.parent_id = cte.id
    )
    SELECT id FROM cte
#end
```

---

## 三、#define 和 #sql 指令对照表

### #define 指令使用

| 文件 | 指令 | 用途 |
|------|------|------|
| _layout.html | `#define layout()` | 主布局模板 |
| _layout.html | `#define head()` | 默认 head 块 |
| _layout.html | `#define body()` | 默认 body 块 |
| _layout.html | `#define script()` | 默认 script 块 |
| _layout.html | `#define sidebar()` | 侧边栏组件 |
| mydoc.html | `#define head()` | 页面样式 |
| mydoc.html | `#define body()` | 页面内容 |
| mydoc.html | `#define script()` | 页面脚本 |

### #sql 指令使用

| 命名空间 | SQL名称 | 用途 |
|----------|---------|------|
| document | findByUserId | 查询用户文档 |
| document | pageByUserId | 分页查询文档（动态条件） |
| document | search | 搜索文档（关键词模糊查询） |
| user | page | 分页查询用户 |
| user | findByUsername | 根据用户名查询 |
| share | sharedToMe | 查询共享给我的文档 |
| share | sharedByMe | 查询我分享的文档 |
| fsNode | findChildren | 查询子节点（动态NULL处理） |
| fsNode | findAllChildIds | 递归查询所有子节点 |
| forward | pageByUserId | 分页查询分享链接（聚合统计） |
| forward | findByShareKey | 根据分享key查询 |
| forward | findItems | 查询分享包含的文件 |

---

## 四、总结

| 特性 | 实现情况 | 分值 |
|------|----------|------|
| #define 指令 | ✅ 定义布局模板、组件、可覆盖块 | 5分 |
| #sql 指令 | ✅ 定义SQL模板、动态条件、参数化查询 | 5分 |
| #namespace 组织 | ✅ 按业务模块组织SQL（document/user/share/fsNode/forward） | - |
| #para 防注入 | ✅ 使用参数占位符 | - |
| #if/#else 动态SQL | ✅ 条件拼接SQL、NULL值处理 | - |
| 多表关联查询 | ✅ JOIN查询、聚合统计 | - |
| 递归查询 | ✅ MySQL CTE语法 | - |

**评分：满分 10 分**