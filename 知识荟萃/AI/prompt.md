# Cursor 的使用

# .cursorrules 文件（位置在项目根目录）的编写和使用

主要构成：你让cursor扮演的角色，需要实现的目标以及分步骤编写代码的要求(其中就包括技术的选择)

e.g:

![image-20250327201152592](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327201152592.png)

**然后再编写 核心业务需求 （实现了解耦）**

~~~markdowm
**！warning：**

别被cursor牵着走生成太多轮代码后再去测试否则很可能出现测试报错但因为代码太多很难定位的情况 

就是当cursor生成代码后，一定要记得点savedll或者accept all
~~~



测试MVP（最小可行性产品）



在正式测试前:使用@codebase （`@Codebase` 功能允许您针对整个代码库提出问题，）

**e.g  @codebase 在正式测试验证前，你可以先全盘检查下代码**

完成代码优化后就可以进入**测试环节**(如果不知道怎么测试浏览器插件，同样可以把问题抛给cursor)



非代码编写相关的问题  用chat就好 快速解决**单元unit问题**





<span style="color:#FF0000; font-size:1.4em; font-weight:bold;">**如何编写：**</span>

[参考：](cursor.directory/rules)



<span style="color:#FF0000; font-size:1.4em; font-weight:bold;"> **模板：**</span>
![521bb9e0051cf4478b30b06de070ce0](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/521bb9e0051cf4478b30b06de070ce0.jpg)                                                                



<span style="color:#FF0000; font-size:1.4em; font-weight:bold;">范例集工具：</span>







---

数据分析工具：

利用**爬虫**  （Dressionpage playright）爬来的数据然后进行分析 （也可生成可视化图表直观）

![image-20250327202528325](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327202528325.png)

![image-20250327202524746](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327202524746.png)



**前端UI：**

问题就是参考图 + AI Prompt

![image-20250327203123593](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327203123593.png)

## UI生成：

### AI直接生成UI



![image-20250327203206013](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327203206013.png)



or 使用cursor 生成html 页面用于描述UI/UX

需要注意的是，把APP所有交互页面的代码都用一个html文件承载大概率会出现代码行数超出Cursor的单次上下文限制而停止生成的情这时候就需要我们手动回复 Cursor“继续”

大概经过几轮“继续”回复后就可以得到一个用**html文件承载的完整原型图**

如下：

！！！

**当然，如果你想要的不仅仅是低保真原型图还可以在提示词里增加这么一句话…引入Tailwind css 来完成，而不是变成style样式，图片使用unsplash”**



![image-20250327211858148](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327211858148.png)



但大家可以把这些UIUX截图发给Cursor、"v0、bolt这种工具进行复刻
**真正转成APP能用的代码**

由于生成的产品原型图和UI稿都是用html进行承载如果要转成可用的代码，需要再截图丢给**Cursor去二次生成**

借助**Vercel**和一个**figma插件**就能将 html直接转成**可编辑的figma设计稿**

然后再利用这个figma 给ai生成代码

![image-20250327212132042](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327212132042.png)



**第二步:** 

在github上创建项目 然后在cursor 终端 git 推送上去 

将第一步得到的html网站免费部署到Vercel.

之所以要先部署网站
是因为步骤三用Figma插件将html转成设计稿,需要用到线上地址

使用前面注册好的GitHub账号登录Vercel这样就能实现两个账号仓库的快速互通

接着在Vercel上创建一个新项目导人(import)刚才在GitHub上的项目

![image-20250327212440768](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327212440768.png)



![image-20250327212454476](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327212454476.png)

![image-20250327221452170](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327221452170.png)







### 文字描述





![image-20250327203915065](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327203915065.png)

![image-20250327203919152](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327203919152.png)



## ProjectRoles

![image-20250327212947860](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327212947860.png)



![image-20250327213029320](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327213029320.png)

![image-20250327213039789](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327213039789.png)



![image-20250327213056204](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327213056204.png)

不仅如此，Auto Attach还可以指定持定路径的文件 两种方式，都是帮助我们更精准地锁定目标文件

配置完 Description 和 Auto Attach最后就是最关键的 Rule Content

![image-20250327213157429](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250327213157429.png)

---





# PROMPTS

~~~pt
你是顶级前端工程师，现就职于apple.把前端显示变得更精致，
更丝滑的动态效果,感觉用户需要付费20元每月的绝美天气app的前端显示
~~~

