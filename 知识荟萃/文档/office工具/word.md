# 快捷操作

| 功能键  | 默认作用                                      | Shift / Ctrl / Alt 的组合用途                             |
| ------- | --------------------------------------------- | --------------------------------------------------------- |
| **F2**  | 移动文本（选择后按 F2，再移动光标，按 Enter） | - `Ctrl + F2`：打印预览  - `Alt + F2`：打开“保存为”对话框 |
| **F3**  | 将选中内容转换为自动图文集（AutoText）        | - `Shift + F3`：切换大小写（如 word → Word → WORD）       |
| 🔴**F4** | 重复上一步操作（如格式设置）                  | - `Alt + F4`：关闭 Word                                   |
| **F5**  | 打开“查找与替换”窗口中的“定位”标签            | - `Ctrl + F5`：恢复窗口大小（最大化还原）                 |
| **F8**  | 启动选择模式（按一次选字，按两次选句...）     | - `Shift + F8`：逐步缩小选择范围                          |

`Ctrl + Shift + N`（重置为默认正文样式）。

`Ctrl + F` 在 Word 中不仅仅是“查找”功能，还会**打开左侧的“导航窗格**

`Ctrl + G` 查找替换

# 基本排版

## 标题样式





<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703215425676.png" alt="image-20250703215425676" style="zoom:50%;" />

可自己创建样式（造轮子 复用）

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703215804358.png" alt="image-20250703215804358" style="zoom:50%;" />

通过更多选项 显示视图中缺失的部分



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703220038501.png" alt="image-20250703220038501" style="zoom: 50%;" />

## 多级列表的使用

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703231006444.png" alt="image-20250703231006444" style="zoom:50%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703231044774.png" alt="image-20250703231044774" style="zoom:50%;" />

---

## 题注和引用

**引用--> 题注 以及交叉引用**



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703231845294.png" alt="image-20250703231845294" style="zoom:50%;" />

**word交叉引用：** （**Word 中的“交叉引用”** 是一种让你可以在文档中引用其他内容（如标题、图表、表格、公式、编号段落等）的功能，它能实现自动更新引用内容和页码，是大型文档（如论文、合同、说明书）中**非常关键的排版工具**。）

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703232916846.png" alt="image-20250703232916846" style="zoom:50%;" />

也可修改**题注样式**

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703233306107.png" alt="image-20250703233306107" style="zoom:50%;" />

🟢🔵🔴

> **F9 是 Word 中“更新域（Field）”的快捷键**。
>  而 “域” 是 Word 内部一种 **自动生成、动态更新的特殊内容**，比如页码、目录、图表编号、交叉引用、日期、书签引用等等。

| 功能     | 实际是一个“域”             |
| -------- | -------------------------- |
| 页码     | `{ PAGE }`                 |
| 日期     | `{ DATE \@ "yyyy-MM-dd" }` |
| 目录     | `{ TOC \o "1-3" }`         |
| 图题编号 | `{ SEQ Figure \* ARABIC }` |
| 交叉引用 | `{ REF _Ref1234567 \h }`   |

| 使用场景        | 说明                                  |
| --------------- | ------------------------------------- |
| 更新页码 / 图号 | 文档内容改动后，图表/页码编号自动更新 |
| 更新目录        | 按 `F9` 即可更新整个目录内容          |
| 更新交叉引用    | 引用的标题/图表页码改变时更新显示     |
| 插入日期字段    | 日期域可以每次打开文档时自动更新      |



---

## 设置三线表

表格样式

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703234305272.png)

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703234302804.png" alt="image-20250703234302804" style="zoom:50%;" />

## 插入参考文献



[zotero插入参考文献](https://www.bilibili.com/video/BV14y4y1Z7Uu/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36)



## 生成目录

也可同步更新目录

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703235604500.png" alt="image-20250703235604500" style="zoom: 80%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703235614073.png" alt="image-20250703235614073" style="zoom:50%;" />



## 设置页码

**有个小问题：**如果目录也被作为**页码内容**了，**不要删除**页码列表中的目录项（因为这样更新域代码还是会回来 ）

**最佳实践：**将目录这个标题 改为**正文**不要作为标题**（也就是排除出多级(级别)列表）**然后再重新更新 

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704000031057.png" alt="image-20250704000031057" style="zoom: 33%;" />

<video controls width="600">
  <source src= "https://arcwater.oss-cn-hangzhou.aliyuncs.com//2b64cb35-cdef-44b2-bca1-003ec1efafb9.mp4">
  您的浏览器不支持 HTML5 视频播放。
</video>



## 小功能

分页符隐藏（当插入空白页面的时候）

![image-20250703235213288](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250703235213288.png)
