# 评分要点3：Admin管理功能和路由分离配置（10分）

## 评分标准
使用 FrontRoutes 和 AdminRoutes 路由类对应前台功能和后端功能，实现路由分离配置。

## 项目符合情况：✅ 完全符合

本项目实现了完整的前后台路由分离：
- **FrontRoutes** - 前台用户功能路由
- **AdminRoutes** - 后台管理功能路由

---

## 一、路由分离配置

### 1. 主配置类

#### 文件位置：`docflow/src/main/java/com/docflow/common/DocflowConfig.java`

```java
package com.docflow.common;

import com.jfinal.config.*;

public class DocflowConfig extends JFinalConfig {

    @Override
    public void configRoute(Routes me) {
        // 设置视图基础路径
        me.setBaseViewPath("/webapp");
        
        // 前台路由 - 用户功能
        me.add(new FrontRoutes());
        
        // 后台路由 - 管理功能
        me.add(new AdminRoutes());
    }
    
    // ... 其他配置
}
```

### 2. 前台路由配置（FrontRoutes）

#### 文件位置：`docflow/src/main/java/com/docflow/common/FrontRoutes.java`

```java
package com.docflow.common;

import com.docflow.controller.*;
import com.jfinal.config.Routes;

/**
 * 前台路由配置
 * 注：登录拦截已在各Controller上使用@Before注解配置
 */
public class FrontRoutes extends Routes {

    @Override
    public void config() {
        // 首页 (重定向到登录或文档列表)
        add("/", IndexController.class);
        
        // 用户模块 (登录/注册/登出) - 无需登录
        add("/user", UserController.class);
        
        // 文档模块 - Controller上已配置@Before(LoginInterceptor.class)
        add("/doc", DocumentController.class);
        
        // 文件夹模块
        add("/folder", FolderController.class);
        
        // 共享模块
        add("/share", ShareController.class);
        
        // 上传模块
        add("/upload", UploadController.class);

        // 转发分享链接模块
        add("/forward", ForwardController.class);
    }
}
```

### 3. 后台路由配置（AdminRoutes）

#### 文件位置：`docflow/src/main/java/com/docflow/common/AdminRoutes.java`

```java
package com.docflow.common;

import com.docflow.controller.admin.*;
import com.docflow.interceptor.AdminInterceptor;
import com.jfinal.config.Routes;

/**
 * 后台管理路由配置
 * 所有后台路由统一使用 AdminInterceptor 进行权限拦截
 */
public class AdminRoutes extends Routes {

    @Override
    public void config() {
        // 设置后台视图基础路径
        setBaseViewPath("/view/admin");
        
        // 添加管理员权限拦截器（所有后台路由都需要管理员权限）
        addInterceptor(new AdminInterceptor());
        
        // 后台首页/仪表盘
        add("/admin", AdminIndexController.class, "");
        
        // 用户管理
        add("/admin/user", AdminUserController.class, "");
        
        // 文档管理
        add("/admin/doc", AdminDocController.class, "");
        
        // 分享链接管理
        add("/admin/forward", AdminForwardController.class, "");
    }
}
```

---

## 二、前台控制器

### 1. 首页控制器

#### 文件位置：`docflow/src/main/java/com/docflow/controller/IndexController.java`

```java
package com.docflow.controller;

import com.jfinal.core.Controller;

public class IndexController extends Controller {
    
    public void index() {
        // 已登录则跳转到文档列表，否则跳转到登录页
        if (getSessionAttr("loginUser") != null) {
            redirect("/doc/list");
        } else {
            redirect("/user/login");
        }
    }
}
```

### 2. 用户控制器（登录/注册）

#### 文件位置：`docflow/src/main/java/com/docflow/controller/UserController.java`

```java
package com.docflow.controller;

import com.docflow.model.User;
import com.docflow.validator.LoginValidator;
import com.docflow.validator.RegisterValidator;
import com.jfinal.aop.Before;
import com.jfinal.core.Controller;
import com.jfinal.kit.Ret;

public class UserController extends Controller {
    
    // 登录页面
    public void login() {
        if (getSessionAttr("loginUser") != null) {
            redirect("/doc/list");
            return;
        }
        render("/view/login.html");
    }
    
    // 登录处理
    @Before(LoginValidator.class)
    public void doLogin() {
        String username = getPara("username");
        String password = getPara("password");
        
        User user = User.dao.login(username, password);
        if (user != null) {
            setSessionAttr("loginUser", user);
            renderJson(Ret.ok("msg", "登录成功"));
        } else {
            renderJson(Ret.fail("msg", "账号或密码错误"));
        }
    }
    
    // 注册页面
    public void register() {
        if (getSessionAttr("loginUser") != null) {
            redirect("/doc/list");
            return;
        }
        render("/view/register.html");
    }
    
    // 注册处理
    @Before(RegisterValidator.class)
    public void doRegister() {
        String username = getPara("username");
        String password = getPara("password");
        String nickname = getPara("nickname");
        
        if (User.dao.isUsernameExist(username)) {
            renderJson(Ret.fail("msg", "用户名已存在"));
            return;
        }
        
        User user = new User();
        user.set("username", username);
        user.set("password", password);
        user.set("nickname", nickname != null ? nickname : username);
        user.set("role", User.ROLE_USER);
        user.set("status", User.STATUS_NORMAL);
        
        if (user.save()) {
            renderJson(Ret.ok("msg", "注册成功"));
        } else {
            renderJson(Ret.fail("msg", "注册失败"));
        }
    }
    
    // 退出登录
    public void logout() {
        removeSessionAttr("loginUser");
        redirect("/user/login");
    }
}
```

### 3. 文档控制器（前台业务）

#### 文件位置：`docflow/src/main/java/com/docflow/controller/DocumentController.java`

```java
package com.docflow.controller;

import com.docflow.interceptor.LoginInterceptor;
import com.docflow.model.Document;
import com.docflow.model.User;
import com.docflow.validator.DocumentValidator;
import com.jfinal.aop.Before;
import com.jfinal.core.Controller;
import com.jfinal.kit.Ret;
import com.jfinal.plugin.activerecord.Page;

@Before(LoginInterceptor.class)  // 需要登录才能访问
public class DocumentController extends Controller {
    
    // 文档列表
    public void list() {
        User user = getAttr("loginUser");
        int pageNumber = getParaToInt("page", 1);
        Page<Document> docPage = Document.dao.search(pageNumber, 10, user.getId(), 
            getPara("keyword"), getParaToInt("folderId"), getPara("docType"));
        setAttr("docPage", docPage);
        setAttr("nav", "mydoc");
        render("/view/mydoc.html");
    }
    
    // 收藏列表
    public void starred() {
        User user = getAttr("loginUser");
        Page<Document> docPage = Document.dao.paginateStarred(getParaToInt("page", 1), 10, user.getId());
        setAttr("docPage", docPage);
        setAttr("nav", "starred");
        render("/view/mydoc.html");
    }
    
    // 回收站
    public void trash() {
        User user = getAttr("loginUser");
        Page<Document> docPage = Document.dao.paginateDeleted(getParaToInt("page", 1), 10, user.getId());
        setAttr("docPage", docPage);
        setAttr("nav", "trash");
        setAttr("isTrash", true);
        render("/view/mydoc.html");
    }
    
    // 新建文档页面
    public void add() {
        render("/view/edit.html");
    }
    
    // 编辑文档页面
    public void edit() {
        Integer id = getParaToInt("id");
        Document doc = Document.dao.findById(id);
        setAttr("doc", doc);
        render("/view/edit.html");
    }
    
    // 保存文档
    @Before(DocumentValidator.class)
    public void save() {
        // ... 保存逻辑
    }
    
    // 删除、恢复、收藏等操作
    public void delete() { /* ... */ }
    public void restore() { /* ... */ }
    public void toggleStar() { /* ... */ }
}
```

---

## 三、后台管理控制器

### 1. 后台首页控制器

#### 文件位置：`docflow/src/main/java/com/docflow/controller/admin/AdminIndexController.java`

```java
package com.docflow.controller.admin;

import com.jfinal.core.Controller;

public class AdminIndexController extends Controller {
    
    public void index() {
        render("index.html");
    }
}
```

### 2. 用户管理控制器

#### 文件位置：`docflow/src/main/java/com/docflow/controller/admin/AdminUserController.java`

```java
package com.docflow.controller.admin;

import com.docflow.model.User;
import com.jfinal.core.Controller;
import com.jfinal.kit.Ret;
import com.jfinal.plugin.activerecord.Page;

/**
 * 用户管理控制器（后台管理）
 */
public class AdminUserController extends Controller {
    
    // 用户列表（分页）
    public void index() {
        int pageNumber = getParaToInt("page", 1);
        int pageSize = 10;
        String keyword = getPara("keyword");
        
        String select = "SELECT *";
        StringBuilder from = new StringBuilder("FROM user WHERE 1=1 ");
        
        if (keyword != null && !keyword.trim().isEmpty()) {
            from.append("AND (username LIKE '%").append(keyword).append("%' ");
            from.append("OR nickname LIKE '%").append(keyword).append("%') ");
        }
        from.append("ORDER BY create_time DESC");
        
        Page<User> userPage = User.dao.paginate(pageNumber, pageSize, select, from.toString());
        setAttr("userPage", userPage);
        setAttr("keyword", keyword);
        render("user_list.html");
    }
    
    // 禁用/启用用户
    public void toggleStatus() {
        Integer id = getParaToInt("id");
        User user = User.dao.findById(id);
        
        User loginUser = getAttr("loginUser");
        if (user.getId().equals(loginUser.getId())) {
            renderJson(Ret.fail("msg", "不能禁用自己"));
            return;
        }
        
        int newStatus = user.getStatus() == 1 ? 0 : 1;
        user.set("status", newStatus);
        
        if (user.update()) {
            renderJson(Ret.ok("msg", newStatus == 1 ? "已启用" : "已禁用"));
        }
    }
    
    // 删除用户
    public void delete() {
        Integer id = getParaToInt("id");
        User user = User.dao.findById(id);
        
        User loginUser = getAttr("loginUser");
        if (user.getId().equals(loginUser.getId())) {
            renderJson(Ret.fail("msg", "不能删除自己"));
            return;
        }
        
        if (user.isAdmin()) {
            renderJson(Ret.fail("msg", "不能删除管理员"));
            return;
        }
        
        if (user.delete()) {
            renderJson(Ret.ok("msg", "删除成功"));
        }
    }
    
    // 重置密码
    public void resetPassword() {
        Integer id = getParaToInt("id");
        User user = User.dao.findById(id);
        
        user.set("password", "123456");
        if (user.update()) {
            renderJson(Ret.ok("msg", "密码已重置为: 123456"));
        }
    }
}
```