在终端（shell）中，有许多快捷操作可以提高效率，尤其是 **Bash** 和 **Zsh**（以及它们的增强版，如 `oh-my-zsh`）。以下是一些高效的终端快捷键和操作方式：  

---

## **1. 基本 Shell 快捷键**
### **光标移动**
| 快捷键     | 作用                        |
| ---------- | --------------------------- |
| `Ctrl + A` | 移动光标到行首              |
| `Ctrl + E` | 移动光标到行尾              |
| `Ctrl + U` | 删除光标前的所有内容        |
| `Ctrl + K` | 删除光标后的所有内容        |
| `Ctrl + W` | 删除光标前的一个单词        |
| `Ctrl + Y` | 粘贴上次删除的文本          |
| `Alt + F`  | 光标向前移动一个单词        |
| `Alt + B`  | 光标向后移动一个单词        |
| `Ctrl + L` | 清屏（相当于 `clear` 命令） |

---

### **命令历史**
| 快捷键       | 作用                                     |
| ------------ | ---------------------------------------- |
| `↑` (上箭头) | 上一条命令                               |
| `↓` (下箭头) | 下一条命令                               |
| `Ctrl + R`   | 搜索历史命令（输入关键字）               |
| `Ctrl + G`   | 退出历史搜索                             |
| `!!`         | 执行上一条命令                           |
| `!$`         | 获取上一条命令的最后一个参数             |
| `!n`         | 执行历史中的第 `n` 条命令                |
| `^old^new`   | 在上一条命令中替换 `old` 为 `new` 并执行 |

示例：
```bash
$ echo Hello World
$ !!  # 重新执行 echo Hello World
$ echo "File not found"
$ ^not^exists  # 变成 echo "File exists"
```

---

### **进程管理**
| 快捷键       | 作用                                |
| ------------ | ----------------------------------- |
| `Ctrl + C`   | 终止当前进程                        |
| `Ctrl + Z`   | 挂起当前进程（暂停）                |
| `fg`         | 恢复到前台                          |
| `bg`         | 让挂起的任务在后台运行              |
| `jobs`       | 查看当前后台任务                    |
| `kill <PID>` | 终止进程（通过 `jobs -l` 查看 PID） |
| `Ctrl + D`   | 退出终端（相当于 `exit`）           |

---

## **2. 目录导航**
| 命令           | 作用                             |
| -------------- | -------------------------------- |
| `cd -`         | 在当前目录和上一个目录之间切换   |
| `pushd <目录>` | 进入目录并保存当前目录           |
| `popd`         | 返回上一个 `pushd` 目录          |
| `dirs -v`      | 显示目录栈                       |
| `ls -lh`       | 显示详细文件信息（人类可读格式） |

---

## **3. 文件操作**
| 命令              | 作用                           |
| ----------------- | ------------------------------ |
| `cp -r`           | 递归复制目录                   |
| `mv -i`           | 移动/重命名（有交互提示）      |
| `rm -rf`          | 强制删除目录（谨慎使用）       |
| `cat file`        | 显示文件内容                   |
| `tac file`        | 反向显示文件内容               |
| `less file`       | 分页查看文件                   |
| `head -n 10 file` | 查看文件前 10 行               |
| `tail -n 10 file` | 查看文件后 10 行               |
| `tail -f file`    | 实时查看文件变化（常用于日志） |

---

## **4. 高效补全**
如果你使用的是 **Bash/Zsh**，可以开启自动补全：
- `Tab` → 自动补全命令、文件、目录
- `Tab` + `Tab` → 列出所有可能补全的选项

Zsh 用户可以安装 **oh-my-zsh** 以增强补全功能：
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

---

## **5. 终端多任务**
| 命令            | 作用                       |
| --------------- | -------------------------- |
| `&`             | 让命令在后台运行           |
| `nohup <cmd> &` | 让命令在退出终端后继续运行 |
| `disown -h %1`  | 让后台任务不受终端关闭影响 |
| `tmux`          | 终端多任务管理器           |

示例：
```bash
$ python script.py &   # 让 Python 脚本在后台运行
$ jobs  # 查看任务
$ disown -h %1  # 让任务不受终端关闭影响
```

---

## **6. 进阶技巧**
### **别名**
可以用 `alias` 定义快捷命令：
```bash
alias ll='ls -alh'  # `ll` 等价于 `ls -alh`
alias gs='git status'
```
要永久保存，写入 `~/.bashrc` 或 `~/.zshrc`。

### **使用 `find` 搜索文件**
```bash
find /path -name "*.txt"
find . -type f -size +100M  # 查找大于 100MB 的文件
```

### **使用 `grep` 搜索内容**
```bash
grep "error" /var/log/syslog  # 搜索日志中的错误信息
ps aux | grep nginx  # 查找 nginx 进程
```









---

# Java与JavaScript的对比 （集合与stream流）



| **功能** | **Java**                                  | **JavaScript**                |
| -------- | ----------------------------------------- | ----------------------------- |
| 过滤     | `filter()`                                | `filter()`                    |
| 映射     | `map()`                                   | `map()`                       |
| 归约     | `reduce()`                                | `reduce()`                    |
| 遍历     | `forEach()`                               | `forEach()`                   |
| 去重     | `distinct()`                              | 无直接方法，可使用`new Set()` |
| 限制结果 | `limit()`                                 | 无直接方法，需手动截取        |
| 排序     | `sorted()`                                | `sort()`                      |
| 检查元素 | `allMatch()`, `anyMatch()`, `noneMatch()` | 无直接方法，需手动实现        |





# ==vue3 速看==

一般都是在main.js 中注册全局 css样式或者是全局组件 component



![image-20250602194216497](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602194216497.png)



![image-20250602194305514](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602194305514.png)



定制请求request.js 以及 **vue ** **生命周期**钩子函数使用

指令修饰符
通过".”指明一些指令 后缀，不同 后缀 封装了不同的处理操作一 简化代码

**@keyup.enter    v-model.trim**
**转数字v-model.number**
**阻止冒泡@事件名.stop**
**@事件名.prevent →阻止默认行为**



---

v-bind:src = " "   语法糖 :src=" " 

watch监听器 简单数据 / 复杂数据 （嵌套对象） 可添加额外配置型  



js / vue3 监听事件的处理 e.g 鼠标/键盘 聚焦/失焦 加载 

**vue3中event 事件的使用 以及 ref 的使用 还有在模板和脚本中 如何使用 内置函数 比如路由跳转什么的**



axios 中有config属性就是专门配置http请求的各种参数信息的

---



**动态导入/延迟加载/懒加载 打破循环依赖**

**循环依赖指的是两个或多个模块相互依赖，形成一个闭环。例如:**
**模块 A 依赖模块 B。**
**模块 B 又依赖模块 A。**

**axios 中 get/post/delete/put（全部）/patch(部分) 等各种参数写法**  注意post的默认行为

axios.head()  获取响应头信息，不返回 body





**可以把 Promise 想象成一个“快递包裹”**

`Promise` 是 JavaScript 中的一种 **异步编程解决方案**。

- 你下了订单（发出请求），快递还没来（任务未完成）。
- 快递送达（任务完成）：你就可以处理里面的数据。

**Promise 有三种状态：**

| 状态        | 描述                           |
| ----------- | ------------------------------ |
| `pending`   | 等待中（还没完成）             |
| `fulfilled` | 成功完成                       |
| `rejected`  | 失败（例如网络错误、请求失败） |

**请求报文/响应报文**

---



**js/vue3**`${}` 模板字符串（将变量嵌入到字符串中）



**<span style="color:#FF3333;">最重要 父子组件传值</span>**  以及 插槽！！！

事件派发（`emit`）

![image-20250602200400259](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602200400259.png)



**[elmentUI Plus ](https://cn.element-plus.org/zh-CN/component/overview.html)这样的组件库 直接用的时候看就行**



**js解构和  剩余参数的使用**

| 用法场景            | 名称                 | 示例                       | 作用                       |
| ------------------- | -------------------- | -------------------------- | -------------------------- |
| 函数参数中          | 剩余参数（rest）     | `function fn(...args) {}`  | 把传入的多个参数收集成数组 |
| **对象/数组使用时** | 展开运算符（spread） | `{ ...obj }` 或 `[...arr]` | 把对象/数组展开为元素      |





---

**整数值绑定 (`:label="1"` 和 `:label="0"`)**：

- 使用整数值 `1` 和 `0` 绑定到 `<el-radio>` 的 `label` 属性上。这意味着在 Vue 的数据模型中，`articleForm.isPublic` 将会被设置为整数类型的 `1` 或 `0`，而不是字符串类型。
- Vue 在处理表单输入时，会根据 `label` 的值来设置和获取 `<el-radio>` 组件的状态，因此 `v-model="articleForm.isPublic"` 应该是一个能够接受整数类型的变量。

**字符串值绑定 (`:label="'1'"` 和 `:label="'0'"`)**：

- 如果你使用 `:label="'1'"` 和 `:label="'0'"`，则将字符串 `"1"` 和 `"0"` 绑定到 `<el-radio>` 的 `label` 属性上。这种情况下，`articleForm.isPublic` 将会是字符串类型的 `"1"` 或 `"0"`。
- 这种方式在处理表单时需要确保 `v-model="articleForm.isPublic"` 是一个字符串类型的变量



**`:label="..."`（动态绑定）**：

- 使用 `:label` 表示在 Vue.js 中进行动态数据绑定。你可以在 `:label` 后面使用 Vue 实例中的变量、表达式或者方法返回值。这种方式适用于需要根据数据动态设置属性值的场景。
- 示例：`<el-radio :label="1">公开</el-radio>` 中的 `:label` 绑定了整数 `1`，实现了动态绑定。

**`label="..."`（静态绑定）**：

- 使用 `label` 表示静态地将字符串或者其他字面值直接赋值给属性。这种方式适用于不需要动态更新属性值的场景，通常用于传递固定的文本或值。
- 示例：`<el-radio label="true">公开</el-radio>` 中的 `label` 直接赋值了字符串 `"true"`。

~~~vue
 <!-- 抽屉 - 表单 -->
  <el-drawer v-model="drawer2" :direction="direction">
    <template #header>
      <h4>{{ title }}</h4>
    </template>
    <el-form ref="ruleFormRef" :model="articleForm" label-width="120px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="articleForm.title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="分类" prop="category">
        <el-select-v2 v-model="value" :options="options" placeholder="" />
      </el-form-item>
      <el-form-item label="编辑内容" prop="content">
        <!-- blinko模仿 -->
      </el-form-item>

      <el-form-item label="是否公开" prop="isPublic">
        <el-radio-group v-model="articleForm.isPublic">
          <el-radio :label="1">公开</el-radio>
          <el-radio :label="0">私有</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>

        <el-button type="primary" color="#1f2f5f" @click="resetForm(ruleFormRef)">Reset</el-button>
      </el-form-item>
    </el-form>

    <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">cancel</el-button>
        <el-button type="primary" @click="confirmClick">confirm</el-button>
      </div>
    </template>
  </el-drawer>
~~~



## 跨域配置问题 正则表达式

~~~js
import axios from 'axios'
// TODO:拦截器的写法

import {ElMessage} from 'element-plus'

// 创建请求实例
const baseURL = '/api'
const instance = axios.create({ baseURL })
// 跨域问题

export default instance; 

//————————————————————————————————————————————————

 server: {
    port: 3000,
    proxy:{
      '/api':{
        target:'http://localhost:8080/admin',
        changeOrigin:true,
        rewrite:(path) => path.replace(/^\/api/,'')
      }
    }
  
  },
      
      
      
~~~

1. `port: 3000`

- **作用**：设置开发服务器的运行端口为 `3000`
- **访问方式**：浏览器通过 `http://localhost:3000` 访问前端应用
- **典型场景**：解决端口冲突或需要指定固定端口时使用

2. `proxy`

- **核心作用**：在开发阶段将 API 请求代理到其他服务器，解决跨域问题
- **典型场景**：前端运行在 `3000` 端口，后端 API 服务运行在 `8080` 端口

3. `target: 'http://localhost:8080'`

- **功能**：指定代理目标服务器地址
- **请求流程**：
  1. 浏览器请求 `http://localhost:3000/api/user`
  2. 开发服务器将请求转发到 `http://localhost:8080/api/user`

4. `changeOrigin: true`

- **功能**：修改 HTTP 请求头中的 `Origin` 字段

- **原始请求头**：

  

  ```
  Origin: http://localhost:3000
  ```

- **修改后请求头**：

  

  ```
  Origin: http://localhost:8080
  ```

- **必要性**：绕过某些服务器的源检查（如 Spring Security）

5. `rewrite: (path) => path.replace(/^\/api/, '')`

- **功能**：重写请求路径（类似 URL 重定向）
- **示例**：
  - 原始请求路径：`/api/user`
  - 重写后路径：`/user`
  - 实际转发地址：`http://localhost:8080/user`
- **典型场景**：统一去除 API 前缀，适配后端路由



## axios api 写法

~~~js
export const articleListService = (params) => {
  return request.get('/article', { params: params })
}

params：你传进去的查询参数对象（query string）。

{ params: params }：axios 会自动将这个对象拼接到 URL 后面


//字符串模板拼接
export const articleDetailService = (id) => {
  return request.get(`/article/${id}`)
    // 路径参数
}
~~~



## 拦截器

~~~js
~~~



~~~js
// 添加响应拦截器 在后端返回给前端数据之前执行 
instance.interceptors.response.use(
  result => {
      //判断业务状态码
      if(result.data.code === 200){
          // console.log(result)
          return result.data;
      }

      //操作失败
      // alert(result.data.msg?result.data.msg:'服务异常')
      ElMessage.error(result.data.msg?result.data.msg:'服务异常')
      console.log(result)

      //异步操作的状态转换为失败
      return Promise.reject(result.data)
      
  },
  err => {
      //判断响应状态码,如果为401,则证明未登录,提示请登录,并跳转到登录页面
      if(err.response.status===401){
          ElMessage.error('请先登录')
          router.push('/login')
      }else{
          ElMessage.error('服务异常')
      }
     
      return Promise.reject(err);//异步的状态转化成失败的状态 
  }
)

~~~





## 表单相关



~~~vue
  
<!--radio-->
<el-radio-group v-model="search.filterCondition" size="small">
              <el-radio-button :label="1">按时间</el-radio-button>
              <el-radio-button :label="0">按热度</el-radio-button>
            </el-radio-group>

<!--下拉框-->
<el-select-v2 v-model="search.isPublic" :options="status" placeholder="" />


const status = ref([
  { value: '1', label: '公共' },
  { value: '0', label: '私有' }
]);
~~~





## 工具类相关

~~~js
import dayjs from 'dayjs'
使用插槽格式化时间：
<el-table-column label="CreateTime" align="center">
  <template #default="{ row }">
    {{ dayjs(row.createTime).format('YYYY-MM-DD HH:mm:ss') }}
  </template>
</el-table-column>

<el-table-column label="UpdateTime" align="center">
  <template #default="{ row }">
    {{ dayjs(row.updateTime).format('YYYY-MM-DD HH:mm:ss') }}
  </template>
</el-table-column>
~~~

## 插槽



[Vue 3 的具名插槽语法（`v-slot` 简写）](https://blog.csdn.net/qq_52697994/article/details/118226918?ops_request_misc=&request_id=&biz_id=102&utm_term=%E7%99%BD%E7%91%95%20%E6%8F%92%E6%A7%BD&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-118226918.142^v102^pc_search_result_base9&spm=1018.2226.3001.4187)

![image-20250602201538385](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602201538385.png)

![image-20250602201545119](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602201545119.png)



![image-20250602201551986](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250602201551986.png)



 js 中各种集合的使用  （类比javastream流）

setTimeout setInterval 定时器用法



# 接口问题



~~~js
// 传多个值过去
export const articleCountService = (ids) => {
  return request.get('article/count',{params:ids})
}
~~~



~~~js
import { categoryListService } from "@/api/category"


export const getCategories = async () => {
  let res = await categoryListService()
  res = res.data
  return res
}
categories.value = getCategories()
我这个使用外部函数返回值赋值为什么失败了
~~~

![image-20250419181824922](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250419181824922.png)

# 路由

**<keep-alive> 有什么用？**

- 性能优化：切换组件时不销毁实例，避免重复创建/销毁，提升性能。

- 状态保留：组件的本地状态（如表单输入、滚动位置、tab页等）会被保留，切换回来时还在。

- 生命周期钩子：被缓存的组件不会触发 destroyed/unmounted，而是触发 deactivated/activated。

**适合场景**

- 需要频繁切换的页面（如 tab 页、聊天窗口、表单页等），希望切换回来时保留原有状态。

- 需要优化性能，避免组件频繁销毁和重建。





父子组件传值 问题

父子组件都需要某个数据库穿过来的 数据 那就需要写函数 

但是这样重复度高

所以使用父组件获取 然后传值到子组件



~~~js
{
  path: '/category/:slug',
  name: 'Category',
  component: CategoryPage
}

import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const slug = route.params.slug

    console.log('slug is:', slug)

    return { slug }
  }
}

~~~

## 同一页面路由传值 刷新 监听问题

~~~js
watch(() => route.params.id, async (newId) => {
  if (newId) {
    console.log('文章变化，加载新文章：', newId)

    // 重置状态
    tocItems.value = []
    relatedArticles.value = []
    popularArticles.value = []
    article.value = {}
    articleId.value = newId
    // 获取新文章信息
    await getArticleDetail()
    await getCategoryName()
    await getRelatedArticles()

  }
}, { immediate: true })


 {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail
    
  },
      const articleId = ref(route.params.id || 1)
      
      route 和router 不一样
      userRoute()  userRouter()
~~~







# 标签属性

~~~html
    <el-menu-item v-for="item in categories" :key="item.id" :index="`/category/${item.id}`">
~~~

标签属性 “ ” 中也可以使用模板字符串



# 组合式api

~~~js
//要让 pageParams.date 在 selectedYear 和 selectedMonth 改变时自动响应并更新，把整个 pageParams 变成一个计算属性。
const pageParams = computed(() => ({
  categoryId: route.params.slug,
  pageNum: pageNum.value,
  pageSize: pageSize.value,
  filterCondition: filterCondition.value,
  title: searchQuery.value,
  date: formatToLocalDate(selectedYear.value, selectedMonth.value)
}))

~~~





# Pinia

~~~js
 # npm install pinia-plugin-persistedstate

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createPinia } from 'pinia'
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
const app = createApp(App)


app.use(pinia)

// 使用
import { useCategoryStore } from '@/stores/categoryStore'
const categoryStore = useCategoryStore()


import { defineStore } from 'pinia'
// 唯一id category
// state 放数据
// action 放函数
export const useCategoryStore = defineStore('category',{
  state: () => ({
    categories: [],
  }),
  actions: {
    setCategories(categories) {
      this.categories = categories
    }
},
persist: true // 持久化
}
)
~~~



# 无限滚动

~~~js
import { ElInfiniteScroll } from 'element-plus';
// 在 main.js 里注册
app.use(ElInfiniteScroll);



~~~

~~~html
<div
  class="scroll-wrapper"
  v-infinite-scroll="loadMore"
  :infinite-scroll-disabled="isLoading || noMoreData"
  :infinite-scroll-distance="20"
  style="height: 200px; overflow-y: auto;"
>
  <div v-for="item in list" :key="item.id">{{ item.name }}</div>
  <div v-if="isLoading">加载中...</div>
  <div v-if="noMoreData">没有更多了</div>
</div>
~~~

~~~js
const list = ref([]);
const query = ref({ page: 1, pageSize: 2 });
const isLoading = ref(false);
const noMoreData = ref(false);

const loadMore = async () => {
  if (isLoading.value || noMoreData.value) return;
  isLoading.value = true;
  query.value.page++;
  // 调用API获取下一页
  const res = await api(query.value);
  if (res.data.length < query.value.pageSize) noMoreData.value = true;
  list.value = list.value.concat(res.data);
  isLoading.value = false;
};

// 初始加载第一页
onMounted(async () => {
  isLoading.value = true;
  const res = await api(query.value);
  list.value = res.data;
  isLoading.value = false;
});
~~~



# 父子路由通信  props 

~~~vue
      <!-- 第三部分：主内容区（只保留默认内容） -->
      <el-main class="main-content" >
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <keep-alive>
              <component :is="Component" :friend-list="friendList" :group-list="groupList" />
            </keep-alive>
          </transition>
        </router-view>
      </el-main>
~~~

~~~~js
const props = defineProps({
  friendList: {
    type: Array,
    default: () => []
  },
  groupList: {
    type: Array,
    default: () => []
  }
});

const groups = computed(() => props.groupList.map(group => ({
  id: group.roomId,
  name: group.name,
  avatar: group.avatar,
  memberCount: group.memberCount || 0,
  createTime: group.createTime || '',
  owner: group.owner || '',
  announcement: group.groupDesc || '',
  members: group.members || []
})));

~~~~



# 组件复用 思想 

注意全局说明 设计理念 要存档 定义主题风格 适合项目刚开始 

注意封装组件思想 注意组件/api 的**可扩展性 和可复用性** --> 可整理一个组件库

**prompt:**

**好的现在需要你给我一个接口文档包含所有接口的对接方式成功和失败的返回值，放在一个文件里**
**方便我复制给==前端对接==。**

![image-20250708212244800](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708212244800.png)

# vscode4vue

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/e437cb877b1d5419e46b582c780909e.jpg" style="zoom:50%;" />





# 前后端交互

**判断当前请求是不是 Ajax 请求（比如前端用 `fetch` 或 `axios` 调用接口）**



对于一些特殊情况，如接口需要返回`json`，页面请求返回`html`可以使用如下方法：

```java
@ExceptionHandler(LoginException.class)
public Object loginException(HttpServletRequest request, LoginException e)
{
	log.error(e.getMessage(), e);

	if (ServletUtils.isAjaxRequest(request))
	{
		return AjaxResult.error(e.getMessage());
	}
	else
	{
		return new ModelAndView("/error/500");
	}
}
```
