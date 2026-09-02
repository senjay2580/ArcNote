<center> **<font color="red" size="28"> 数据结构 </font>** </center>



# 0、时间复杂度

## 1.频率最高的语句（执行深度最深的 /阶数最多的）

## 2. 语句执行次数和问题规模 n 的关系

## 3. 忽略常数

### 为什么O(1)的空间复杂度不是指空间的而是指辅助空间的？

当提到O(1)的空间复杂度时，通常指的是**辅助空间复杂度**为O(1)，即算法所需的额外空间是固定的，与输入规模无关。例如，一个仅使用几个变量的算法，其辅助空间复杂度为O(1)。

**注意**：如果输入数据本身占用O(n)空间，总空间复杂度为O(n)，但辅助空间复杂度仍为O(1)。

---

## 递归的时间复杂度和空间复杂度 如何计算



![image-20260828171626807](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260828171626807.png)

![image-20260828172318323](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260828172318323.png)



直接假设 最深的执行了k次 然后看看一次 变量会怎么样 2次会怎么样 再到 k次 然后比较看看 k 与 n的关系 也就是 次数和量级的关系

![image-20241017210952655](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017210952655.png)

![image-20250821220052977](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220052977.png)

**递归的时间复杂度：画树即可**

结点数就是时间复杂度 但如果每个结点里面也就是每个递归里还有嵌套的话就要看==多重循环==的解题思路



空间复杂度 = 算法运行期间【临时占用】的存储空间，与问题规模 n 的关系

**不算的**：输入数据本身（题目给你的数组、链表、邻接矩阵、树） 

**要算的**：你自己定义的变量、malloc 的空间、辅助数组、栈/队列、**递归栈**

① 圈出所有「额外」声明的东西 —— 输入参数不圈
② 逐个判断：**大小是常数，还是随 n 增长？**
③ **如果是递归 —— 加上「递归树的最大深度」**
④ **取所有项里最大的那一个**



注意：递归、malloc、自己额外定义的变量





---



# 数组、矩阵存储和广义表

**核心问题：数组在内存中怎么存？给定下标怎么快速算出地址？！！！特殊矩阵怎么省空间？**

广义表在研究什么

**核心问题：线性表的元素只能是单元素，如果元素本身还可以是表，怎么定义和操作？**

## ==特殊矩阵==的压缩存储

![image-20250109214904823](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109214904823.png)

分为按行优先和按列优先存储 

注意点 ： ==一维数组默认从 0 下标开始==

`array [n][m]` n 个数组（==0~n-1==），每个数组里都有 m（0 ~ m-1）个元素

![image-20241124175558277](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124175558277.png)

**行/列/页优先**

二维数组在内存中是**一维连续存放**的，行优先和列优先就是**按什么顺序把二维 "摊平" 成一维**。 本质就是内存中如何存的

！！！



核心其实就是看重复（对称 0这些）

### ==对称矩阵== 的压缩存储



![image-20241124175822092](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124175822092.png)

**以……为顺序将 二维数组的一部分存储在一维数组当中**	

### 三角矩阵



![image-20241124180025625](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180025625.png)

**多一个就去存那个固定的 c 值**

注意三角矩阵行优先和列优先

![image-20260827175010051](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827175010051.png)

![image-20241124181356800](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124181356800.png)

**c == 0 就是线性代数里比较特殊的上/下三角矩阵 **

###  对角矩阵

![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180339303.png)

**以对角线的顺序存储**

![image-20260827172853057](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827172853057.png)

![image-20260827172913992](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827172913992.png)

其实最终的一维数组我也可以 从1开始 如果从0 开始我就平移而已啊 往左平移

比如这个我算出来就是 88 然后减去1 就是 87 

### 稀疏矩阵

![image-20241124180403044](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180403044.png)

**密度小于 0.05 （非零元素少时）**

![image-20241124181712867](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124181712867.png)

![image-20241124181757465](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124181757465.png)

### 十字链表存储稀疏矩阵

![image-20241124181839495](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124181839495.png)

![image-20241124181929350](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124181929350.png)

![image-20241124182002045](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124182002045.png)



## SUM

# 矩阵

**对称矩阵：** 主对角线（左-> 右）数值无规律 上下部对称 所以存上/下 + 对角线上的值即可

**三角矩阵：** 对角线以上/下（不包括对角线） 的元素都是常数 c 存 n(n+1)/2 + 1（常数 c）

**对角矩阵**：三、四、五对角矩阵

---



**稀疏矩阵**：矩阵中大都是零（（非零元素个数）/ （m X n）<= 0.05 ）的时候

**存储原则：** 使用三元组存储 非零元素的行、列、值

**缺点：** 无法 **随机存取**

## 广义表

![image-20241124180457077](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180457077.png)



![image-20241124180545920](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180545920.png)

![image-20241230182154988](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241230182154988.png)

![image-20241124180625820](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180625820.png)

![image-20241124180728470](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241124180728470.png)

核心就是注意 空表 和 原子（元素）

表或者子表都是加一个（） 的 不加（）的是元素

![image-20260827175609768](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827175609768.png)

空表也算一个表啊 所以他有深度 

如果**空表是子表** （**空表套空表**） 和 **只有空表（空表）**也要区分 

表头表尾都有可能是空表

![image-20260827175600890](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827175600890.png)

![image-20260827175558915](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260827175558915.png)





**三对角矩阵概念！**

![image-20241017211021475](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017211021475.png)



![825357dbaf9fecd541cf159647cf60a](https://raw.githubusercontent.com/kasahuki/os_test/main/img/825357dbaf9fecd541cf159647cf60a.jpg)

**m~ij~ 的 i j 取决于 按行/列优先存储**



| 操作              | 操作前先检查什么            | 核心操作                     | length 是否变化 |
| ----------------- | --------------------------- | ---------------------------- | --------------- |
| 初始化 `InitList` | 一般不用检查                | `length = 0`                 | 变成 0          |
| 尾插 `ListAppend` | **是否已满**                | 放到 `data[length]`          | `+1`            |
| 插入 `ListInsert` | **位置是否合法 + 是否已满** | 后面的元素右移，再插入       | `+1`            |
| 删除 `ListDelete` | **位置是否合法** 是否空的   | 保存被删元素，后面的元素左移 | `-1`            |
| 修改 `ListChange` | **位置是否合法**            | 直接修改对应元素             | 不变            |
| 判空 `ListEmpty`  | 不需要额外检查              | 判断 `length == 0`           | 不变            |



# <font size=25 color=red> 一、链表 </font>

==增操作 ： 构建链表！==

## 顺序表（数组实现）：

> 使用数组，静态分配。

```c
#define MaxSize 10
typedef struct {
    int data[MaxSize];      /* 存放顺序表元素 */
    int length;             /* 顺序表当前长度 */
} SqList;

/* 初始化 */
void InitList(SqList &L) {
    L.length = 0;
}

/* 尾部追加。原代码写的是 data[++l.length]，下标从 1 开始，
   与 C 数组下标从 0 的惯例冲突，且没有判满；这里统一为下标从 0 */
bool ListAppend(SqList &L, int x) {
    if (L.length >= MaxSize) return false;      /* 原代码缺判满 */
    L.data[L.length++] = x;
    return true;
}

/* 按位序 i 插入（i 从 1 计），后面的元素整体后移 */
bool ListInsert(SqList &L, int i, int x) {
    if (i < 1 || i > L.length + 1) return false;
    if (L.length >= MaxSize) return false;
    for (int j = L.length; j >= i; j--)          /* 从后往前挪，否则覆盖 */
        L.data[j] = L.data[j - 1];
    L.data[i - 1] = x;
    L.length++;
    return true;
}

/* 按位序 i 删除，用 e 带回被删元素 */
bool ListDelete(SqList &L, int i, int &e) {
    if (i < 1 || i > L.length) return false;
    e = L.data[i - 1];
    for (int j = i; j < L.length; j++)           /* 从前往后挪 */
        L.data[j - 1] = L.data[j];
    L.length--;
    return true;
}

/* 改：把第 i 个元素改成 x */
bool ListChange(SqList &L, int i, int x) {
    if (i < 1 || i > L.length) return false;
    L.data[i - 1] = x;
    return true;
}

bool ListEmpty(SqList L) {
    return L.length == 0;
}
```



## 链表（链式实现）

> 使用 new/malloc ，delete/free 动态分配内存空间！

### ==创+初始化==

`malloc` 可以把它理解成：

**向堆区申请一块指定字节数的内存**

malloc 内部表述要申请多少字节

![image-20260828183341903](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260828183341903.png)

**sizeof(int) == 4**

~~~c
申请数组
int *p = malloc(10 * sizeof(int));


~~~

因为 `malloc` 返回的是：

```
void *
```

也就是“通用指针”。

用完以后要 `free`

~~~c
/* 单链表结点。C 里结构体内部引用自身必须写 struct LNode*，
   因为此时 typedef 的新名字还没生效；C++ 的构造函数在 C 中不存在，
   改用 malloc + 手动赋值 */
typedef struct LNode {
    int data;
    struct LNode *next;
} LNode, *LinkList;
/* LNode   —— 结点类型
   LinkList —— 指向结点的指针类型，两个名字等价于 struct LNode 和 struct LNode* */

/* 初始化：建立带头结点的空表 */
bool InitList(LinkList &L) {
    L = (LNode *)malloc(sizeof(LNode));   /* C++ 的 new LNode 对应这一句 */
    if (L == NULL) return false;          /* 内存不足 */
    L->next = NULL;
    return true;
}
~~~

### 销毁链表

这个要一个一个释放的不是一起释放

~~~c
/* 销毁链表：连头结点一起释放 */
void DestroyList(LinkList &L) {
    LNode *p;
    while (L != NULL) {
        p = L;
        L = L->next;      /* 先走再释放，否则 p 释放后取不到 next */
        free(p);          /* C++ 的 delete 对应 free */
    }
    L = NULL;             /* 原代码未置空，留下野指针 */
}
~~~



### ==构建链表==

#### 头插法

~~~c
/* 头插法：新结点永远插在头结点之后 —— 结果是逆序，相当于栈 */
bool ListInsertHead(LinkList &L, int x) {
    LNode *s = (LNode *)malloc(sizeof(LNode));
    if (s == NULL) return false;
    s->data = x;
    s->next = L->next;    /* 先接后面 */
    L->next = s;          /* 再接前面，顺序不能反 */
    return true;
}
~~~

#### 尾插法

~~~c
/* 尾插法：每次从头找到尾再插，O(n)。结果保序 */
bool ListInsertTail(LinkList &L, int x) {
    LNode *r = L;
    while (r->next != NULL)
        r = r->next;                      /* 找到尾结点 */
    LNode *s = (LNode *)malloc(sizeof(LNode));
    if (s == NULL) return false;
    s->data = x;
    s->next = NULL;                       /* 原代码漏了这句，新尾结点的 next 是垃圾值 */
    r->next = s;
    return true;
}

/* 建表时若要连续尾插，应在外面维护尾指针 r，把上面这个 O(n) 降成 O(1)：
   LNode *r = L;
   for (i = 0; i < n; i++) {
       LNode *s = (LNode *)malloc(sizeof(LNode));
       s->data = a[i]; s->next = NULL;
       r->next = s; r = s;                原代码在函数内写 tail = s 是给局部变量赋值，出了函数就没了
   }                                                                              */
~~~

#### 按指定位置插入新节点

~~~c
/* 在第 i 个位置插入（i 从 1 计，即插到第 i-1 个结点之后） */
bool ListInsert(LinkList &L, int i, int x) {
    if (i < 1) return false;
    LNode *p = L;                 /* p 指向头结点，看作第 0 个结点 */
    int j = 0;
    while (p != NULL && j < i - 1) {   /* 找第 i-1 个结点，即插入位置的前驱 */
        p = p->next;
        j++;
    }
    if (p == NULL) return false;       /* i 越界。原代码在这种情况下已 malloc 出结点却不释放，会内存泄漏 */
    LNode *s = (LNode *)malloc(sizeof(LNode));
    if (s == NULL) return false;
    s->data = x;
    s->next = p->next;
    p->next = s;
    return true;
}
/* 有了头结点，i == 1 不需要特判，头插就是这里 p 停在头结点的情形 */
~~~

### ==查找==

#### 按位查找

~~~c
/* 按位序查找：返回第 i 个结点的指针，找不到返回 NULL（i 从 1 计） */
LNode *GetElem(LinkList L, int i) {
    if (i < 1) return NULL;
    LNode *p = L;
    int j = 0;
    while (p != NULL && j < i) {
        p = p->next;
        j++;
    }
    return p;                  /* 循环正常结束时 p 就是第 i 个结点 */
}

/* 若题目要的是"第 i 个结点的值"，再取一次 data 即可：
   LNode *p = GetElem(L, i);
   return (p == NULL) ? -1 : p->data;                                */
~~~



#### 按值查找

~~~c
/* 按值查找：返回第一个值为 x 的结点指针，找不到返回 NULL
   注意参数用 LinkList L 传值而不是 &L —— 函数内要移动 L，
   传引用会把调用者的头指针改掉 */
LNode *LocateElem(LinkList L, int x) {
    LNode *p = L->next;             /* 从第一个数据结点开始，跳过头结点 */
    while (p != NULL && p->data != x)
        p = p->next;
    return p;
}

/* 若题目要的是位序（从 1 计，找不到返回 0） */
int LocateIndex(LinkList L, int x) {
    LNode *p = L->next;
    int pos = 1;
    while (p != NULL) {
        if (p->data == x) return pos;
        p = p->next;
        pos++;
    }
    return 0;
}
~~~

### ==删除== 指定位置的结点

~~~c
/* 删除第 k 个结点（k 从 1 计） */
bool ListDelete(LinkList &L, int k, int &e) {
    if (k < 1) return false;
    LNode *p = L;                       /* 找第 k-1 个结点，即被删结点的前驱 */
    int j = 0;
    while (p != NULL && j < k - 1) {
        p = p->next;
        j++;
    }
    if (p == NULL || p->next == NULL) return false;   /* k 越界 */
    LNode *q = p->next;                 /* q 是真正要删的结点 */ 先定位取出来再说
    e = q->data; 
    p->next = q->next;
    free(q);                            /* 原代码只改指针不释放，内存泄漏 */ 注意要释放
    return true;
}

/* 删除所有值为 x 的结点。要点：删完之后 pre 不能前进 */
void ListDeleteAll(LinkList &L, int x) {
    LNode *pre = L, *p = L->next, *q;
    while (p != NULL) {
        if (p->data == x) {
            q = p;
            pre->next = p->next;
            p = p->next;                /* p 前进，pre 原地不动 */
            free(q);
        } else {
            pre = p;
            p = p->next;
        }
    }
}
~~~

### ==判空&计算长度==

~~~c
/* 判空：带头结点的链表，头结点后面没东西就是空 */
bool ListEmpty(LinkList L) {
    return L->next == NULL;
}
~~~

~~~c
/* 求表长（不含头结点）。
   参数用传值 LinkList L：函数内要移动指针，传 &L 会把调用者的头指针弄丢。
   —— 凡是"只读遍历"的函数，一律传值 */
int ListLength(LinkList L) {
    int len = 0;
    LNode *p = L->next;          /* 直接从第一个数据结点起算，就不用最后减 1 */
    while (p != NULL) {
        len++;
        p = p->next;
    }
    return len;
}
~~~

<font color='red' size=6>！！注意问题：不要随便移动初始的头节点（哨兵结点，固定，），要固定住，然后使用步进结点步进去遍历  。 遍历时要防止空指针异常，特判极端（极小极大/一般）边界情况 </font>

---



## ！循环链表(环形链表，！但指向 ==表头==)

###  ==循环单链表== 和 ==循环双链表== 

**<font size='16' color='red'> 循环是有<u>作用</u>的 </font>**

![image-20240924231426150](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231426150.png)

![image-20240924231442290](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231442290.png)

### **初始化：** ![image-20241013213720089](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013213720089.png)



![image-20241013213147658](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013213147658.png)

**删除也同理！**

![image-20240924231456953](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231456953.png)

![image-20240924231510937](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231510937.png)

一般来说先后再前减轻记忆负担



![image-20240924231537034](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231537034.png)

![image-20240924231552815](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240924231552815.png)



> 可设置头尾指针（类似带头尾结点！

![Screenshot_2024-10-10-12-52-26-019_net.csdn.csdnplus](https://raw.githubusercontent.com/kasahuki/os_test/main/img/Screenshot_2024-10-10-12-52-26-019_net.csdn.csdnplus.png)



![image-20241013213814034](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013213814034.png)

![image-20241013213906802](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013213906802.png)

## <u>双链表（带头结点）</u>

### 创+初始化

~~~c
/* 双链表结点 */
typedef struct DNode {
    int data;
    struct DNode *prior, *next;
} DNode, *DLinkList;

/* 初始化：建立带头结点的空双链表 */
bool InitDList(DLinkList &L) {
    L = (DNode *)malloc(sizeof(DNode));
    if (L == NULL) return false;
    L->prior = NULL;        /* 头结点的 prior 永远为 NULL */
    L->next = NULL;         /* 空表时 next 也为 NULL */
    return true;
}

/* 原代码建了首尾两个哨兵结点后没有把 a->prior / b->next 置空，
   这两个域是 malloc 出来的垃圾值，遍历时会跑飞 */
~~~

### 在 p 结点之后插入 s 结点

~~~c
/* 在 p 结点之后插入 s 结点 */
bool InsertNextDNode(DNode *p, DNode *s) {
    if (p == NULL || s == NULL) return false;
    s->next = p->next;
    if (p->next != NULL)          /* 原代码直接写 p->next->prior = s，
                                     当 p 是尾结点时 p->next 为 NULL，空指针崩溃 */
        p->next->prior = s;
    s->prior = p;
    p->next = s;                  /* 这一句必须放最后，否则 p->next 已被改掉 */
    return true;
}

/* 四句话的顺序口诀：先接 s 的两头，再改后继的 prior，最后改 p 的 next */
~~~



### 双链表的删除（按位删除）

删除一定要考虑释放\

判空一定要注意！！！

```c
/* 删除结点 p 本身 */
bool DeleteDNode(DNode *p) {
    if (p == NULL) return false;
    if (p->prior != NULL) p->prior->next = p->next;
    if (p->next  != NULL) p->next->prior = p->prior;
    free(p);                      /* C++ 的 delete 对应 free */
    return true;
}

/* 删除 p 的后继结点（更常考的写法） */
bool DeleteNextDNode(DNode *p) {
    if (p == NULL) return false;
    DNode *q = p->next;
    if (q == NULL) return false;              /* p 没有后继 */
    p->next = q->next;
    if (q->next != NULL) q->next->prior = p;  /* q 是尾结点时要跳过这句 */
    free(q);
    return true;
}
```

### 双链表查找指定结点

#### 按值查找

~~~c
/* 按值查找。参数传值，理由同单链表 */
DNode *LocateElem(DLinkList L, int x) {
    DNode *p = L->next;           /* 原代码从 L 开始，会把头结点里的垃圾值也拿来比较 */
    while (p != NULL && p->data != x)
        p = p->next;
    return p;
}
~~~

#### 按位查找

~~~c
/* 按位序查找，i 从 1 计 */
DNode *GetElem(DLinkList L, int i) {
    if (i < 1) return NULL;
    DNode *p = L;
    int j = 0;
    while (p != NULL && j < i) {
        p = p->next;
        j++;
    }
    return p;
}
~~~



### 双链表的遍历（可向 ==前== 也可向 ==后==）



![image-20250821220106630](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220106630.png)



# basic：==数组== 的缺陷和链表的区别

~~~c
#define MaxSize 20
typedef struct {
    int data[MaxSize];
    int length;
} SqList;
/* 原代码写的是 typedef struct sqlist { ... };  —— 结尾没给类型名，
   C 里这句既没定义 typedef 名也无法用 sqlist 声明变量，编译不过 */

void InitList(SqList &L) {
    L.length = 0;
    /* 原代码这里有一个 for(i=0; i<l.length; i++) 给 data 清零，
       但 length 刚被置 0，循环一次都不执行 —— 是段无效代码。
       顺序表靠 length 界定有效范围，本来也不需要清零 */
}

/* 在下标 k 处插入 x（k 从 0 计） */
bool ListInsert(SqList &L, int k, int x) {
    if (k < 0 || k > L.length) return false;
    if (L.length >= MaxSize) return false;   /* 原代码先 length++ 再判满，
                                                判满失败时 length 已被改坏 */
    for (int i = L.length; i > k; i--)
        L.data[i] = L.data[i - 1];
    L.data[k] = x;
    L.length++;
    return true;
}

/* 删除下标 k 处的元素 */
bool ListDelete(SqList &L, int k) {
    if (k < 0 || k >= L.length) return false;
    for (int i = k; i < L.length - 1; i++)
        L.data[i] = L.data[i + 1];
    L.length--;
    return true;
}

void PrintList(SqList L) {
    for (int i = 0; i < L.length; i++)
        printf("%d ", L.data[i]);
    printf("\n");
}
~~~



## 应用 ： 多项式的 -存储-  &&  多项式的 -相加-





~~~c
~~~





---





~~~c
~~~







---

# 二、栈与队列

---

入出栈序列 

栈在括号匹配 表达式求值 递归 的应用

队列 双端队列 循环队列 层次遍历

已经他们顺序和链式存储结构

### 静态链表

~~~c
#define MAXSIZE 100

typedef struct {
    int data;
    int next;
} SLinkList[MAXSIZE];

void InitList(SLinkList L) {
    L[0].next = -1;
}


~~~



## 栈

### 顺序栈

~~~c
#define MaxSize 25
typedef struct {
    int data[MaxSize];
    int top;            /* 栈顶指针 */
} SqStack;

/* 约定：top 指向栈顶元素，初值 -1（进栈先移动再赋值）
   另一种约定是 top 指向栈顶的下一个位置，初值 0（进栈先赋值再移动）
   两种都对，但判空判满的条件不同，一道题里必须自始至终用同一种 */
void InitStack(SqStack &S) {
    S.top = -1;
    /* 原代码 for(i = 0; i <= maxsize; i++) 给数组清零，i 取到 maxsize 时越界；
       而且顺序栈靠 top 界定有效范围，本来就不需要清零 */
}

bool StackEmpty(SqStack S) {
    return S.top == -1;
}

bool StackFull(SqStack S) {
    return S.top == MaxSize - 1;
}

/* 进栈 */
bool Push(SqStack &S, int x) {
    if (StackFull(S)) return false;      /* 原代码没有判满 */
    S.data[++S.top] = x;                 /* 先移动再赋值 */
    return true;
}

/* 出栈，用 x 带回栈顶元素 */
bool Pop(SqStack &S, int &x) {
    if (StackEmpty(S)) return false;     /* 原代码没有判空 */
    x = S.data[S.top--];                 /* 先取值再移动 */
    return true;
}
/* 原代码写的是 st.val[st.top--];  —— 这是一条取值后丢弃的表达式语句，
   元素没被带出来，只有指针动了 */

/* 读栈顶但不出栈 */
bool GetTop(SqStack S, int &x) {
    if (StackEmpty(S)) return false;
    x = S.data[S.top];
    return true;
}

int StackLength(SqStack S) {
    return S.top + 1;
}

/* 从栈顶到栈底依次输出。传值不传引用，输出完不影响调用者的栈 */
void PrintStack(SqStack S) {
    while (!StackEmpty(S))
        printf("%d ", S.data[S.top--]);
    printf("\n");
}
~~~

### 链栈

> ### 带头结点

#### 创&初始化：new 方法

#### 入栈 ： 单链表头插法

#### 出栈 ：单链表头（存数据的头）删

#### 判空 ：st-> next == nullptr

#### 查值：st-> next-> val

#### 计（算）长（度）：遍历计算



## 应用 ：

### 中缀表达式 与前后缀表达式互转



**后缀表达式消除了括号方便计算机算** 避免优先级复杂的比较计算

![847e1b809704afe7753aa9ed6cf31c3](https://raw.githubusercontent.com/kasahuki/os_test/main/img/847e1b809704afe7753aa9ed6cf31c3.jpg)



![74faa91f7c6b97c09701cd0ae5542e5](https://raw.githubusercontent.com/kasahuki/os_test/main/img/74faa91f7c6b97c09701cd0ae5542e5.jpg)





##  表达式求值 





**结合队列可求杨辉三角！**

~~~c
/* 中缀表达式求值：两个栈，一个存运算符一个存操作数。
   408 考纲要求理解过程，代码题考的概率极低；这里用数组模拟栈，
   不用 C++ 的 stack / unordered_map / string */
#define MaxSize 100

char opStack[MaxSize];   int opTop  = -1;   /* 运算符栈 */
int  numStack[MaxSize];  int numTop = -1;   /* 操作数栈 */

/* 运算符优先级，数字越大越优先 */
int Prec(char c) {
    if (c == '+' || c == '-') return 1;
    if (c == '*' || c == '/') return 2;
    return 0;                                /* '(' 返回 0，保证谁也压不过它 */
}

/* 弹出两个操作数和一个运算符，算完把结果压回去 */
void Eval(void) {
    int b = numStack[numTop--];              /* 先弹出的是右操作数 */
    int a = numStack[numTop--];
    char c = opStack[opTop--];
    int ans = 0;
    if (c == '+') ans = a + b;
    if (c == '-') ans = a - b;               /* 注意是 a-b 不是 b-a */
    if (c == '*') ans = a * b;
    if (c == '/') ans = a / b;
    numStack[++numTop] = ans;
}

/* s 是以 '\0' 结尾的表达式串，返回计算结果 */
int Evaluate(char s[]) {
    opTop = numTop = -1;
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] >= '0' && s[i] <= '9') {         /* 多位数字要连着读完 */
            int x = 0;
            while (s[i] >= '0' && s[i] <= '9') {
                x = x * 10 + (s[i] - '0');
                i++;
            }
            i--;                                   /* for 还会 i++，这里退一格 */
            numStack[++numTop] = x;
        } else if (s[i] == '(') {
            opStack[++opTop] = s[i];
        } else if (s[i] == ')') {
            while (opTop >= 0 && opStack[opTop] != '(')
                Eval();
            opTop--;                               /* 弹掉左括号 */
        } else {                                   /* 运算符 */
            while (opTop >= 0 && Prec(opStack[opTop]) >= Prec(s[i]))
                Eval();                            /* 把优先级不低于它的先算掉 */
            opStack[++opTop] = s[i];
        }
    }
    while (opTop >= 0) Eval();
    return numStack[numTop];
}
~~~

#### 注意点：

**判空 扫尾操作  双指针闪现（防止延迟！）**



#### 栈与递归

**最外层的调用也算的！！！**



![image-20250821220112619](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220112619.png)

---



## 队列

~~~c
#define MaxSize 50

typedef struct {
    int data[MaxSize];
    int front, rear;
} SqQueue;
~~~

最常见约定是：

```c
front：指向队头元素
rear ：指向队尾元素的下一个位置
```

初始化：

```c
Q.front = 0;
Q.rear = 0;
```







> ### 带头结点

> 这里讨论的是只可队尾插入队头弹出的队列（非 真·双端队列和 `假·双端队列`）

#### 初始化 （利用结构体的嵌套）

~~~c
/* 链队：结点结构体 + 队列结构体（front / rear 两个指针） */
typedef struct LNode {
    int data;
    struct LNode *next;
} LNode;
/* 原代码写的是 typedef struct ListNode { ... };  结尾没给类型名，
   C 里这句无法用来声明变量；而且 C 结构体没有构造函数 */

typedef struct {
    LNode *front, *rear;      /* 队头指针、队尾指针 */
} LinkQueue;

/* 初始化：建立带头结点的空队，front 和 rear 都指向头结点 */
void InitQueue(LinkQueue &Q) {
    Q.front = Q.rear = (LNode *)malloc(sizeof(LNode));
    Q.front->next = NULL;     /* 原代码没有置空，头结点的 next 是垃圾值 */
}
~~~



<font size=25 color=red> 这个头指针是不存值的（也即是带头节点）--> 与以上同理 </font>

<font size=25 color=red> **结点结构体正常搞** </font>

<font size=25 color=red> **给链队设置头尾指针** 这样可以访问到头尾元素 </font>



#### 入队 (使用尾插法)

~~~c
/* 入队：尾插 */
bool EnQueue(LinkQueue &Q, int x) {
    LNode *s = (LNode *)malloc(sizeof(LNode));
    if (s == NULL) return false;
    s->data = x;
    s->next = NULL;           /* 原代码漏了这句，新尾结点的 next 是垃圾值，
                                 遍历时会跑飞 */
    Q.rear->next = s;
    Q.rear = s;               /* 更新队尾 */
    return true;
}
~~~

#### 出队（头删法）

~~~c
/* 出队：头删，用 x 带回队头元素 */
bool DeQueue(LinkQueue &Q, int &x) {
    if (Q.front == Q.rear) return false;      /* 队空 */
    LNode *p = Q.front->next;                 /* p 是真正的队头元素结点 */
    x = p->data;
    Q.front->next = p->next;
    if (Q.rear == p)                          /* ★ 原代码缺这个判断：
                                                 队里只剩一个元素时，删掉它以后
                                                 rear 还指着已释放的结点，变野指针 */
        Q.rear = Q.front;
    free(p);                                  /* 原代码只改指针不释放，内存泄漏 */
    return true;
}
~~~

#### 判空

~~~c
/* 判空：带头结点的链队，front 和 rear 重合就是空 */
bool QueueEmpty(LinkQueue Q) {
    return Q.front == Q.rear;
}
~~~

#### 打印

~~~c
/* 打印整个队列。传值，不影响调用者 */
void PrintQueue(LinkQueue Q) {
    LNode *p = Q.front->next;        /* 跳过头结点 */
    while (p != NULL) {
        printf("%d--> ", p->data);
        p = p->next;
    }
    printf("NULL\n");
}
~~~



#### 双端队列（两端都可进出）

~~~c
/* 队头插入（双端队列才需要）。
   注意：空队时插入之后 rear 也要跟着变 */
bool PushFront(LinkQueue &Q, int x) {
    LNode *s = (LNode *)malloc(sizeof(LNode));
    if (s == NULL) return false;
    s->data = x;
    s->next = Q.front->next;
    Q.front->next = s;
    if (Q.rear == Q.front)          /* ★ 原代码缺这句：原来是空队，
                                       插完之后 rear 仍指着头结点，队尾丢失 */
        Q.rear = s;
    return true;
}

/* 队尾删除在单链表上做不了 O(1)——找不到 rear 的前驱，
   必须从 front 走一遍，所以真·双端队列要用双链表实现 */
~~~

#### 循环队列

**% mod 操作就是对于环也就是圆圈（钟）轮转**

~~~c
#define MaxSize 100
typedef struct {
    int data[MaxSize];   /* 循环队列必须用数组实现 */
    int front;           /* 队头下标 */
    int rear;            /* 队尾下标：指向队尾元素的下一个位置 */
} SqQueue;

/* 初始化：front == rear 表示队空 */
void InitQueue(SqQueue &Q) {
    Q.front = Q.rear = 0;
}

bool QueueEmpty(SqQueue Q) {
    return Q.front == Q.rear;
}

/* 判满：牺牲一个存储单元。
   不牺牲的话，队空和队满都是 front == rear，分不清 */
bool QueueFull(SqQueue Q) {
    return (Q.rear + 1) % MaxSize == Q.front;
}

/* 入队 */
bool EnQueue(SqQueue &Q, int x) {
    if (QueueFull(Q)) return false;
    Q.data[Q.rear] = x;
    Q.rear = (Q.rear + 1) % MaxSize;      /* 取模实现"循环" */
    return true;
}

/* 出队，用 x 带回队头元素。
   原代码是 int dequeue(...) 直接 return 元素值，队空时 return 0 ——
   可 0 本身也可能是合法数据，调用者分不清"取到了 0"还是"队空"。
   408 的标准写法是：返回值表示成败，元素用引用参数带回 */
bool DeQueue(SqQueue &Q, int &x) {
    if (QueueEmpty(Q)) return false;
    x = Q.data[Q.front];
    Q.front = (Q.front + 1) % MaxSize;
    return true;
}

/* 队列当前长度：不能直接写 rear - front，会出现负数 */
int QueueLength(SqQueue Q) {
    return (Q.rear - Q.front + MaxSize) % MaxSize;
}

void PrintQueue(SqQueue Q) {             /* 传值，销毁的是副本 */
    int x;
    while (DeQueue(Q, x))
        printf("%d ", x);
    printf("\n");
}
~~~

![image-20241015132005982](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015132005982.png)

![image-20241015132014127](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015132014127.png)

**图 1and  3 是空位不同的循环队列**

**图 2 是判断队列的长度！！！** 

![image-20250109213857935](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109213857935.png)

启示：对这个数据结构进行操作/判断时注意这个数据结构此时状态的==可能性==）——联系韦恩图

![image-20250109214217313](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109214217313.png)

## 链表栈队列 阶段性总结

- **初始化/销毁**
- **判空/满**
- **增删 特定位置 和 特定位置周围的增删** 
- **改查 - 涉及遍历 按位查找 按值查找**
- **其余结构特性的操作** 

# 三、串（String）

**会暴力和 KMP就可以了**



## 数组和指针基础

~~~c
/* 数组名作参数时会退化成指针，下面两种写法完全等价 */
void PrintArr(int arr[]) {      /* 等价于 void PrintArr(int *arr) */
    printf("%d", arr[1]);       /* arr[1] 等价于 *(arr + 1) */
}
/* 所以：数组的 [] 本质就是"偏移 + 解引用"。
   也正因为退化成了指针，函数内部 sizeof(arr) 得到的是指针大小，
   拿不到数组长度 —— 长度必须另外用参数传进来 */

void PrintArrN(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}
~~~

arr 就是 ==首地址== *arr 首地址的* *解引用**

应用：

~~~c
/* 依据密码子 codon[] 查出氨基酸名写入 AA[]
   —— 演示 C 字符串必须用库函数比较和赋值，不能用 == 和 = */
void SearchCodon(char codon[], char AA[]) {
    for (int i = 0; i < 64; i++) {
        /* 为什么不能写 codonTable[i][0] == codon ？
           因为两边都是 char*，比的是【地址】不是【内容】。
           比内容必须用 strcmp，相等时返回 0 */
        if (strcmp(codonTable[i][0], codon) == 0) {
            strcpy(AA, codonTable[i][1]);   /* 同理，赋值也不能用 =，要用 strcpy */
            return;                          /* 找到就走，别再往下写 */
        }
    }
    strcpy(AA, "unknown");
    /* 原代码把 strcpy(AA,"unknown") 写在 for 循环【里面】，
       于是每轮没匹配上都会覆盖一次 AA，虽然最终结果碰巧对，
       但逻辑是错的，而且做了 64 次无用的字符串拷贝 */
}

/* 常用的 C 字符串库函数（#include <string.h>）
   int   strcmp (const char *s1, const char *s2);   相等返回 0
   char *strcpy (char *dest, const char *src);      把 src 拷进 dest
   size_t strlen(const char *s);                    不含 '\0' 的长度
   char *strcat (char *dest, const char *src);      拼接                */
~~~



 

![image-20240925153840008](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925153840008.png)

**如果经常用到拼接（长度经常扩展变化）就要使用动态存储结构！**

![image-20240925153922279](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925153922279.png)

==清空串和销毁串不一样，前者内存空间中还有剩余，后者不是；==

####  1.串的比较

![image-20240925154140041](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154140041.png)

> **`按照字典序排序优先看每个字母，如果前缀都一样就要看长度！`**

拓展：采用不同的编码方式，每个字符所占空间不同，考研中只需默认每个字符占 ==1B== 即可



#### 2.串的顺序存储

![image-20240925154440498](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154440498.png)

**销毁这个串： free 释放内存空间！**

![image-20240925154450549](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154450549.png)

**==如果用数组空间去存的话，一个空间是一字节，一字节的空间只能存 0-255（整型）==**

![image-20240925154455828](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154455828.png)

![image-20240925155500570](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925155500570.png)

#### 3.串的链式存储



![image-20240925154500645](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154500645.png)



#### 4.串的基本操作

##### (1) 截取子串

![image-20240925154506513](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154506513.png)

##### (2) 比较字符串

![image-20240925154515710](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154515710.png)

##### (3) 索引字符串



![image-20240925154526505](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240925154526505.png)

##### (4)其他

判空：length

拷贝：遍历赋值

清空：令 length = 0；

~~~c
/* 用链表存串：每个结点存一个字符（结点大小=1，存储密度低，
   408 里更常考的是定长顺序串 char ch[MAXLEN]，这里只是练指针操作） */
typedef struct SNode {
    char ch;
    struct SNode *next;
} SNode, *SString;
/* 原代码的 char val[4] 里只用了 val[0]，其余三个字节始终是 '\0'，
   纯属浪费；而且 typedef struct StringNode{...}*Sstring; 只定义了指针别名，
   没定义结点类型别名，C 里后面只能写 struct StringNode */

/* 建一个只有头结点的空串 */
SString InitString(void) {
    SString S = (SNode *)malloc(sizeof(SNode));
    S->ch = '#';           /* 头结点不存有效字符 */
    S->next = NULL;
    return S;
}

/* 尾部追加一个字符 */
void AppendChar(SString S, char c) {
    SNode *r = S;
    while (r->next != NULL) r = r->next;
    SNode *s = (SNode *)malloc(sizeof(SNode));
    s->ch = c;
    s->next = NULL;
    r->next = s;
}

void PrintString(SString S) {
    SNode *p = S->next;              /* 跳过头结点 */
    while (p != NULL) {
        printf("%c", p->ch);
        p = p->next;
    }
    printf("\n");
}
/* 原代码的 print 函数少了一个右花括号，整段编译不过 */
~~~





#### 注意点

~~~c
/* 拼接两个串，返回一个新串（不破坏 a 和 b） */
SString ConcatString(SString a, SString b) {
    SString res = InitString();      /* 新串的头结点 */
    SNode *r = res;

    for (SNode *p = a->next; p != NULL; p = p->next) {
        SNode *s = (SNode *)malloc(sizeof(SNode));
        s->ch = p->ch;               /* 复制字符，新建结点 */
        s->next = NULL;
        r->next = s;
        r = s;
    }
    for (SNode *p = b->next; p != NULL; p = p->next) {
        SNode *s = (SNode *)malloc(sizeof(SNode));
        s->ch = p->ch;
        s->next = NULL;
        r->next = s;
        r = s;
    }
    return res;
}

/* 对照原代码注释掉的那个版本：它是直接把 a、b 的【原结点】挂到 res 上，
   不新建结点。那样做 a 和 b 会被"接管"——调用后 a 的尾部接上了 b，
   打印 a 会打出 a+b 的内容。这就是原注释里说的"a 变成 cbgfj"的原因。
   要不要复制结点，取决于题目允不允许破坏原串 */
~~~



~~~c
/* 上面几个函数的用法示意 —— 这是【语句片段】，要放进 main 或别的函数里才能编译 */
SString a = InitString();
AppendChar(a, 'c');
AppendChar(a, 'b');
AppendChar(a, 'g');
AppendChar(a, 'f');

SString b = InitString();
AppendChar(b, 'j');

SString ans = ConcatString(a, b);
PrintString(a);       /* cbgf  —— 因为 ConcatString 复制了结点，a 没被改动 */
PrintString(ans);     /* cbgfj */
~~~

> **返回字符串基本都是带#头节点的和单链表统一！！**
>
> ##### 如果按照注释那样会使得 a 为 cbgfj

## BF 算法（暴力匹配）

![image-20241017200841618](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017200841618.png)

直接使用双重循环

或是双指针

![image-20241017200920166](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017200920166.png)

### 时间复杂度分析

![image-20241017200939277](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017200939277.png)





# 四、KMP 算法

> 主要就是前缀数组 next

~~~c
/* KMP。下标从 1 开始，p 是模式串，s 是主串，
   ne[i] 表示 p[1..i] 中最长的"相等前后缀"的长度 */
#define N 100010
#define M 1000010

char p[N], s[M];        /* 注意：串从下标 1 开始存，p[0]、s[0] 空着不用 */
int ne[N];              /* next 数组 */
int n, m;               /* n = 模式串长度，m = 主串长度 */

/* 求 next 数组 */
void GetNext(char p[], int n, int ne[]) {
    ne[1] = 0;                                  /* 第一个字符没有真前后缀 */
    for (int i = 2, j = 0; i <= n; i++) {
        while (j > 0 && p[i] != p[j + 1])
            j = ne[j];                          /* 失配就回退到更短的前后缀 */
        if (p[i] == p[j + 1]) j++;              /* 匹配上就伸长一位 */
        ne[i] = j;
        /* while 和 if 的顺序不能换：必须先退到能匹配的位置，再判断 */
    }
}

/* 在主串 s 中找模式串 p，输出所有匹配的起始位置（从 1 计） */
void KMP(char s[], int m, char p[], int n, int ne[]) {
    for (int i = 1, j = 0; i <= m; i++) {
        while (j > 0 && s[i] != p[j + 1])
            j = ne[j];
        if (s[i] == p[j + 1]) j++;
        if (j == n) {                            /* 整个模式串匹配完成 */
            printf("%d ", i - n + 1);            /* 匹配起点（下标从 1 计） */
            j = ne[j];                           /* 不停下，继续找下一处匹配 */
        }
    }
}

/* ⚠ 408 代码题从未考过 KMP，遇到串匹配写暴力解法即可（见 BF 算法一节）。
   next 数组的手算是选择题必考，代码只需看懂 */
~~~



# 五、树

树的概念

二叉树 定义和特征 顺序链式存储结构 遍历 线索二叉树概念与构造

树和森林

应用：哈夫曼树 并查集 堆





![image-20250109215214848](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215214848.png)



<span style="color:#FF00FF; font-size:1.9em;">x>=h h如果不是整数 那么就是向上取整h 小于等于的话就是向下取整</span> 



![image-20250104215224421](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104215224421.png)



![image-20250104215228606](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104215228606.png)



注意区分树的总度数（每个结点的分支数）和图的度数（离散数学握手定理） 不要搞混了

**总度数** 就是边的总数 就是结点的孩子结点的总和**n-1**







## SUM

![image-20240929191740657](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240929191740657.png)

## ==树的存储结构== (也可用于 森林的存储结构！！！ 注意区分就可以了)

![image-20260829163936813](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829163936813.png)

### 1、双亲表示法



![image-20240929191601508](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240929191601508.png)

**增**：无需按照层序插入新结点



**删除结点**：

有 **两种** 方案 ，**第一种** 使双亲指针设置为-1  

第二种将尾部数据移到该位置将其覆盖！！（good）



缺点 ： 如果删除的不是叶子结点的话就会有问题 ，因为要删除儿子结点，这就涉及到了查询操作，

所以要 **从头开始遍历**，如果用第一个删除，还要判断这个无效数据，就更慢了



### 2、孩子表示法（邻接表）--> hash 表&树/图的存储

[hash 表](#十五、哈希表(散列查找))

**就是邻接表！！！**

![image-20260829163221907](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829163221907.png) 



### **<font color=red size=25> 3、孩子兄弟表示法 </font>**

![image-20260829163546861](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829163546861.png)



<img src="https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240929193349960.png" alt="image-20240929193349960" style="zoom:150%;" />



#### 初始化

~~~c
/* 孩子兄弟表示法（把任意树转成二叉树来存）
   左指针 = 第一个孩子，右指针 = 下一个兄弟 */
typedef struct CSNode {
    int data;
    struct CSNode *firstchild, *nextsibling;
} CSNode, *CSTree;

/* ★ 原代码写的是  CSNode * firstSon, rightBrother;
   C 里 * 只作用于紧跟它的那一个变量，所以 rightBrother 被声明成了
   CSNode 类型（不是指针）—— 结构体在定义自己的时候就包含一个完整的自己，
   是 incomplete type，编译直接报错。
   两个指针必须各写一个星号：*firstchild, *nextsibling                */

/* 记忆锚点：右指针是"同辈"不是"下一层"。
   所以凡是和层数/深度有关的递归，右边一律不加 1：
   高度 = max(1 + Height(firstchild), Height(nextsibling))            */
~~~

**树与森林都可以转化为二叉树 然后操作就如 [二叉树](#二叉树)**



## 树与二叉树的转化 

![image-20250821220121022](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220121022.png)







## 森林和二叉树的转化

![image-20241017201857035](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017201857035.png)



![image-20241017202042876](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017202042876.png)

## SUM



![image-20241017202110296](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017202110296.png)

### 树的遍历

#### 先根遍历

**第一次经过就访问！**



![image-20241017203219748](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203219748.png)

#### 后根遍历

**最后一次经过才访问**

![image-20241017203304337](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203304337.png)

**等效于二叉树的中序遍历**

#### 层次遍历

![image-20241017203331994](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203331994.png)

**先根后根都是 dfs**

**层次是 bfs**





### 森林的遍历

#### 先序遍历

![image-20241017203434814](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203434814.png)

#### 中序遍历

![image-20241017203438865](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203438865.png)

![image-20241017203442009](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203442009.png)

**以下为等效遍历**

### SUM



![image-20241017203448919](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017203448919.png)

**问题：如何使用代码将森林和树转化为二叉树！**

Todo：

~~~c
/* 孩子兄弟表示法的建树与遍历 */
typedef struct CSNode {
    int data;
    struct CSNode *firstchild, *nextsibling;
} CSNode, *CSTree;

CSNode *NewNode(int x) {
    CSNode *p = (CSNode *)malloc(sizeof(CSNode));
    p->data = x;
    p->firstchild = p->nextsibling = NULL;   /* C 没有构造函数，手动置空 */
    return p;
}

/* 给 parent 添加一个孩子：挂到"最后一个兄弟"的后面 */
void AddChild(CSTree parent, int x) {
    CSNode *s = NewNode(x);
    if (parent->firstchild == NULL) {
        parent->firstchild = s;              /* 还没有孩子，当第一个孩子 */
    } else {
        CSNode *p = parent->firstchild;
        while (p->nextsibling != NULL)       /* 沿兄弟链走到最后 */
            p = p->nextsibling;
        p->nextsibling = s;
    }
}

/* 先根遍历：等价于把它当作二叉树做先序遍历 */
void PreOrder(CSTree T) {
    if (T == NULL) return;
    printf("%d ", T->data);
    PreOrder(T->firstchild);        /* 先走孩子 */
    PreOrder(T->nextsibling);       /* 再走兄弟 */
}

/* 求叶子结点个数 —— 注意和二叉链表版的两处差别 */
int CountLeaf(CSTree T) {
    if (T == NULL) return 0;
    if (T->firstchild == NULL)                      /* 差别1：只看左指针为空 */
        return 1 + CountLeaf(T->nextsibling);       /* 差别2：自己是叶子，
                                                       但右兄弟那一支还没算 */
    return CountLeaf(T->firstchild) + CountLeaf(T->nextsibling);
}

/* 求树的高度 */
int Height(CSTree T) {
    if (T == NULL) return 0;
    int hc = Height(T->firstchild) + 1;    /* 孩子在下一层，要 +1 */
    int hs = Height(T->nextsibling);       /* 兄弟在同一层，不 +1 */
    return hc > hs ? hc : hs;
}
~~~



## ==二叉树==

![image-20250109215318637](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215318637.png)

**二叉树的遍历顺序就是 以根结点为基准 然后 左优先**

### 完全二叉树

### 判断是否是完全二叉树

**使用 bfs 存 存第一个 NULL（也可以存别的东西等效替代 如正无穷） 如果 null 之后队列还有数的话就说明不是完全二叉树！！**

![image-20241017163824454](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017163824454.png)

### ==顺序存储==

#### 初始化

~~~c
/* 二叉树的顺序存储：下标从 1 开始，Size 是实际结点数
   结点 i 的左孩子 = 2i，右孩子 = 2i+1，双亲 = i/2（向下取整）
   —— 这套公式只在【下标从 1 开始】时成立 */
#define MaxSize 100
int tree[MaxSize];      /* tree[0] 空着不用 */
int Size;               /* 实际结点个数 */

/* 读入 n 个结点值（考场不用写读入，这里只是说明下标约定） */
void BuildFromArray(int a[], int n) {
    Size = n;
    for (int i = 1; i <= Size; i++)
        tree[i] = a[i - 1];
}
/* 若下标从 0 开始，公式变成：左孩子 2i+1、右孩子 2i+2、双亲 (i-1)/2
   两套下标不能混用，一道题里认准一套 */
~~~

#### 求树的深度

~~~c
/* 求高度（顺序存储）*/
int Height(int u) {
    if (u > Size) return 0;                 /* 越界 = 空结点 */
    int l = Height(2 * u);
    int r = Height(2 * u + 1);
    return 1 + (l > r ? l : r);             /* 取左右较大者 +1 */
}

/* 原代码只递归了左边：height = dfs(u*2) + 1;
   这在【完全二叉树】上碰巧对（左边总是最深的），
   但只要树不是完全二叉树就会算错，比如只有右孩子的链会返回 1。
   通用写法必须取 max，也就是原代码注释掉的那一行 */
~~~

#### 求树的遍历顺序

~~~c
/* 先序遍历（顺序存储）*/
void PreOrder(int u) {
    if (u > Size) return;          /* 越界即空，直接回来 */
    printf("%d ", tree[u]);        /* 访问根 */
    PreOrder(2 * u);               /* 左 */
    PreOrder(2 * u + 1);           /* 右 */
}

/* 中序、后序只是把 printf 换个位置 */
void InOrder(int u) {
    if (u > Size) return;
    InOrder(2 * u);
    printf("%d ", tree[u]);
    InOrder(2 * u + 1);
}

void PostOrder(int u) {
    if (u > Size) return;
    PostOrder(2 * u);
    PostOrder(2 * u + 1);
    printf("%d ", tree[u]);
}

/* 原代码的第一个版本用 if(u*2 > Size) 当出口，判的是"有没有左孩子"，
   于是右孩子那一支会被漏掉；第二个版本 if(u > Size) 才是对的 */
~~~

### ==链式存储==

#### 初始化

~~~c
/* 二叉树的链式存储（二叉链表）*/
typedef struct BiTNode {
    int data;
    struct BiTNode *lchild, *rchild;
} BiTNode, *BiTree;
/* BiTNode  —— 结点类型
   BiTree   —— 指向结点的指针类型
   原代码 }*ListTree; 只定义了指针别名，没定义结点类型别名 */

/* C 没有构造函数，新建结点写成一个函数 */
BiTNode *NewNode(int x) {
    BiTNode *p = (BiTNode *)malloc(sizeof(BiTNode));
    p->data = x;
    p->lchild = p->rchild = NULL;
    return p;
}
~~~



#### 构造树（bfs）

~~~c
/* 用层序遍历的方式往树上加结点，保证长成完全二叉树
   —— 找到第一个"缺孩子"的结点，把新结点挂上去 */
#define MaxSize 100

void InsertLevelOrder(BiTree T, int x) {
    BiTNode *Q[MaxSize];
    int front = 0, rear = 0;
    Q[rear++] = T;                              /* 根入队 */

    while (front < rear) {                      /* 队不空 */
        BiTNode *t = Q[front++];                /* 出队 */
        if (t->lchild != NULL) Q[rear++] = t->lchild;
        else {
            t->lchild = NewNode(x);             /* ★ 找到空位才 malloc，
                                                   原代码在循环外先建好结点，
                                                   万一没插进去就内存泄漏 */
            return;
        }
        if (t->rchild != NULL) Q[rear++] = t->rchild;
        else {
            t->rchild = NewNode(x);
            return;
        }
    }
}
/* 原代码用的是 C++ 的 queue<listTreeNode*> 和 auto，
   408 里一律换成【数组 + front/rear 两个下标】——
   考场上写 BiTNode *Q[MaxSize]; int front=0, rear=0; 就行 */
~~~

#### 前序遍历

~~~c
/* 先序遍历（链式存储）*/
void PreOrder(BiTree T) {
    if (T == NULL) return;
    printf("%d ", T->data);      /* 访问根 */
    PreOrder(T->lchild);
    PreOrder(T->rchild);
}

/* 中序 / 后序：把 printf 挪到中间 / 最后即可 */
void InOrder(BiTree T) {
    if (T == NULL) return;
    InOrder(T->lchild);
    printf("%d ", T->data);
    InOrder(T->rchild);
}

void PostOrder(BiTree T) {
    if (T == NULL) return;
    PostOrder(T->lchild);
    PostOrder(T->rchild);
    printf("%d ", T->data);
}
~~~

#### 计算深度

~~~c
/* 求二叉树的高度 */
int Height(BiTree T) {
    if (T == NULL) return 0;               /* 空树高度 0 */
    int l = Height(T->lchild);
    int r = Height(T->rchild);
    return 1 + (l > r ? l : r);            /* ★ 必须取左右【较大者】 */
}

/* 原代码写的是：
       if (l->lchild == NULL) return 1;
       return height(l->lchild) + 1;
   两个问题：
   ① 只递归左子树，右子树完全没算，只有右孩子的树会返回 1
   ② 出口判的是"没有左孩子"而不是"结点为空"，传入 NULL 会直接崩   */

/* 层序遍历版（不想用递归时）*/
int HeightLevel(BiTree T) {
    if (T == NULL) return 0;
    BiTNode *Q[MaxSize];
    int front = 0, rear = 0, h = 0;
    Q[rear++] = T;
    while (front < rear) {
        int size = rear - front;           /* 本层结点数 —— 分层的命门 */
        h++;
        while (size--) {
            BiTNode *p = Q[front++];
            if (p->lchild) Q[rear++] = p->lchild;
            if (p->rchild) Q[rear++] = p->rchild;
        }
    }
    return h;
}
~~~



#### 测试数据

~~~c
/* 上面几个函数的用法示意（考场只写核心函数，不用写这段）
   按层序依次插入 n 个值，建成一棵完全二叉树 */
BiTree BuildComplete(int a[], int n) {
    if (n <= 0) return NULL;
    BiTree T = NewNode(a[0]);             /* 第一个值当根 */
    for (int i = 1; i < n; i++)
        InsertLevelOrder(T, a[i]);
    return T;
}

/* 调用：
   int a[] = {1, 2, 3, 4, 5};
   BiTree T = BuildComplete(a, 5);
   PreOrder(T);                                                  */
~~~

## 树的前序/中序/后序遍历 构建树

**因为同一个单一遍历序列一样的 不能就确定二叉树的形态**

一定要有中序的

![image-20250109215404348](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215404348.png)



![ed920753c7a08a17beb24f10c9edb5c](https://raw.githubusercontent.com/kasahuki/os_test/main/img/ed920753c7a08a17beb24f10c9edb5c.jpg)

**在先/后 序列找根结点 然后回到中序找左右子树 各对左右子树再找根结点**



---



## 树的非递归形式输出前序/中序/后序遍历序列

![image-20241206142828150](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241206142828150.png)

~~~c
typedef struct BiTNode {
    char data;
    struct BiTNode *lchild, *rchild;
} BiTNode, *BiTree;

#define MaxSize 100        /* 非递归遍历用的栈容量 */
/* 原代码 typedef struct biotree{...};  结尾没给类型名，C 里编译不过；
   构造函数也要去掉 */

/* 按先序序列建树，'#' 表示空结点。
   例如输入 AB#D##C## 建出的树：A 的左孩子 B，B 的右孩子 D，A 的右孩子 C */
BiTree CreateTree(char s[], int *i) {
    char c = s[(*i)++];
    if (c == '#') return NULL;
    BiTNode *p = (BiTNode *)malloc(sizeof(BiTNode));
    p->data = c;
    p->lchild = CreateTree(s, i);       /* 用返回值往回接 */
    p->rchild = CreateTree(s, i);
    return p;
}
/* i 必须传【指针】：下标要随着递归持续往前走，不能回退。
   传值的话每层各改各的，回到上一层就退回去了 */

/* 中序遍历，非递归 */
void InOrderNoRec(BiTree T) {
    if (T == NULL) return;
    BiTNode *st[MaxSize];
    int top = -1;
    BiTNode *p = T;
    while (p != NULL || top >= 0) {
        if (p != NULL) {
            st[++top] = p;              /* 只压栈，先不访问 */
            p = p->lchild;              /* 一路向左 */
        } else {
            p = st[top--];              /* 左边走到头了，弹出栈顶 */
            printf("%c ", p->data);     /* ★ 弹出时才访问 —— 这就是"中序" */
            p = p->rchild;              /* 转向右子树 */
        }
    }
}

/* 先序非递归只要把 printf 挪到压栈那一步：
       if (p != NULL) { printf("%c ", p->data); st[++top] = p; p = p->lchild; }
       else           { p = st[top--]; p = p->rchild; }
   —— 三种非递归里，中序和先序共用这一个模板，只差 printf 的位置    */
~~~

**输入：ABC#D##E##FG##H## （==前序==）**
**输出：C D B E A G F H  （==中序==）**

存到栈里就相当于是进入 ==递归下一层==



 <font size=6 color =red > **弹出栈就是返回上一层** </font>

**旧知识推新知识非常重要**





## 线索二叉树

线索二叉树本质上就是：

> **把普通二叉树中原本没用的空指针，拿来存某种遍历顺序下的“前驱”和“后继”。**

它出现的原因，就是为了让二叉树遍历时，**不必每次都靠递归或栈去寻找下一个结点**。

**启示：做完一道检验所有选项不要无脑看到关键词就上起码要所有选项看过去 思路要清晰画图**

![image-20250109220859790](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109220859790.png)

### 	线索二叉树的中序/前序/后序遍历序列

 <font size=5 color =red > n 个结点的完全二叉树 的空链域为 n+1 条 </font>

**分别分析 n 奇数偶数的情况即可**！！！！

**前驱和后继 是基于 遍历序列决定的！**

​	![image-20241110190454478](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110190454478.png)

### 问题 ：如果从某个节点开始能否开始中序遍历整颗二叉树？

![image-20241110190859359](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110190859359.png)

## 中序~线索二叉树的存储

利用 ==左右指针的空链域== 来存储线索   

**特别地 使用 ltag 和 rtag 来标明是否是线索**

![image-20241110190938336](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110190938336.png)

**左前右后**

**==指向前驱和后继的指针就是线索==**

![image-20241110191122369](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191122369.png)

![image-20241110191135518](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191135518.png)

### 找中序前驱

#### 土方法：





![image-20241110191154758](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191154758.png)

==**双变量轮序迭代**==

#### 线索化查找：

**要处理最后一个结点的后继 因为 每个结点的后继处理都是利用 pre 指向 q（当前结点） 但是当 q == null 就停止了 所以要单独对 pre（最后 pre 和 q 同指向 也就是都指向最后一个结点）**  

### 中序线索化：



其实不用检查因为这个是 左根右的顺序  中序遍历 注意

最后一个肯定没有右孩子了

![image-20241110191321314](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191321314.png)

### 

![image-20241110191324208](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191324208.png)



### 先序线索化



**主要问题**：左指前 要先判断 ==是不是线索== 非线索再继续遍历！

**为什么就先序因为先序的左孩子结点已经确定前驱了 所以如果不判断就又回去了！！**

循环问题！！！

![image-20241110191358251](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191358251.png)

![image-20241110191401045](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191401045.png)



### 后序线索化： post- 前缀 就是后的意思





![image-20241110191435896](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191435896.png)

| 遍历方式    | 最后访问的结点         | 最后结点的 `rchild` |
| ----------- | ---------------------- | ------------------- |
| 先序 根左右 | 最右下方最后访问的结点 | **一定是 NULL**     |
| 中序 左根右 | 最右边的结点           | **一定是 NULL**     |
| 后序 左右根 | **根结点**             | **可能不为 NULL**   |





# ==《通过线索二叉树找前驱/后继》==

这里的核心问题就是 有可能左孩子 不是前驱或者右孩子不是后继



### 找中序后继：

Xtag = 0 就说明一定是不是空链域 ，说明一定有孩子！

![image-20241110191643405](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191643405.png)

![image-20241110191752039](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191752039.png)

### 找中序前驱：



![image-20241110191808466](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191808466.png)

![image-20241110191814016](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191814016.png)

### 找先序后继：



![image-20241110191825685](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191825685.png)

### 找先序前驱:



![image-20260829202206515](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829202206515.png)

这个是基于三叉链表的

![image-20241110191839090](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191839090.png)

### 找后序前驱：

![image-20250821220130213](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220130213.png)

### 找后序后继：



![image-20241110191904128](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191904128.png)

![image-20241110191916949](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241110191916949.png)

这个就和前序前驱联系一下



![image-20260829202913876](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829202913876.png)

![image-20260829202856803](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829202856803.png)

 ![image-20260829202836514](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829202836514.png)



## 哈夫曼树 （特殊二叉树）

![image-20260829173731514](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829173731514.png)

![image-20260829173853248](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829173853248.png)

![image-20260829173927581](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829173927581.png)







**哈夫曼树中不存在度为 1 的节点，即每个节点要么是叶子节点，要么有两个子节点**。



### WPL 概念

 WPL   （**总的**） 是指树中所有叶子节点的带权路径长度之和。==带权路径长度== 是指从 **根节点到某个叶子节点的路径长度（即经过的边数）** 乘以 ==该叶子节点的权重==。

![image-20250103150550008](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103150550008.png)

![image-20260829174149983](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829174149983.png)



![image-20260829175010685](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829175010685.png)

![image-20260829175202635](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829175202635.png)



![image-20260829175239141](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829175239141.png)







![ ](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103153625506.png)

### SUM



![image-20241017211415016](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017211415016.png)



# 六、并查集

合并 和 查

![image-20260829175932726](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829175932726.png)

![image-20260829180119517](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180119517.png)



![image-20260829180230827](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180230827.png)

![image-20260829180302867](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180302867.png)

![image-20260829180318053](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180318053.png)

![image-20260829180431111](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180431111.png)

![image-20260829180502310](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180502310.png)



![image-20260829180516962](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180516962.png)

![image-20260829180525699](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180525699.png)



### 并查集的终极优化

![image-20260829180647849](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180647849.png)

![image-20260829180708512](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829180708512.png)

![image-20260829181658281](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829181658281.png)

![image-20260829181737509](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20260829181737509.png)

# 七、图

图的基本概念 

图的存储和基本操作 邻接矩阵 邻接表 邻接多重表 十字链表

图的遍历 dfs bfs 

图的应用 最小生成树 最短路径 拓扑排序 关键路径



[邻接表入门](#五、树)

#### 图的基本知识

![image-20250109215841503](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215841503.png)

![image-20250109215853168](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215853168.png)

![image-20250109215859276](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215859276.png)

![image-20250109215907230](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215907230.png)

![image-20250109215915809](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109215915809.png)

生成树一般是对于无向图而言的！！

**带权图：网**

有向边：弧

连通图是对于无向图的
强弱连通是对于有向图的

### 重点注意 ： 树的度和图的度不一样 树的度就是指孩子结点 图上面的也算！~





![image-20250109220351354](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109220351354.png)

## 1.图的存储

#### 1.邻接矩阵（适用于 稠密图 ）

**边如果很少（稀疏图）就会有很多空间浪费**



![image-20241009213321006](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213321006.png)

##### 定义

~~~c
/* 邻接矩阵：适合稠密图。空间 O(n^2)，判断两点是否相邻 O(1) */
#define MaxVex 100

typedef struct {
    char vex[MaxVex];             /* 顶点表，也可以换成结构体 */
    int  edge[MaxVex][MaxVex];    /* 邻接矩阵。无权图存 0/1，带权图存权值 */
    int  vexnum, arcnum;          /* 顶点数、边数 */
} MGraph;

/* 初始化：矩阵必须显式清零。
   MGraph g; 是局部变量，edge 里全是垃圾值，不清零后面全错 */
void InitMGraph(MGraph &G, int n) {
    G.vexnum = n;
    G.arcnum = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            G.edge[i][j] = 0;
}
~~~

![image-20241009213547037](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213547037.png)

~~~c
/* 加一条无向边 a—b */
void AddEdge(MGraph &G, int a, int b) {
    G.edge[a][b] = 1;
    G.edge[b][a] = 1;             /* 无向图对称；有向图只写第一句 */
    G.arcnum++;
}

/* 求顶点 i 的度 */
int Degree(MGraph G, int i) {                     /* 无向图 */
    int d = 0;
    for (int j = 0; j < G.vexnum; j++)
        if (G.edge[i][j]) d++;
    return d;
}

int OutDegree(MGraph G, int i) {                  /* 有向图出度：第 i 【行】 */
    int d = 0;
    for (int j = 0; j < G.vexnum; j++)
        if (G.edge[i][j]) d++;
    return d;
}

int InDegree(MGraph G, int i) {                   /* 有向图入度：第 i 【列】 */
    int d = 0;
    for (int j = 0; j < G.vexnum; j++)
        if (G.edge[j][i]) d++;
    return d;
}
/* ★ 行看出度，列看入度 —— 2021、2023 真题都靠这一条 */

/* 无向图总边数 = 矩阵中 1 的个数 / 2 */
int EdgeCount(MGraph G) {
    int cnt = 0;
    for (int i = 0; i < G.vexnum; i++)
        for (int j = 0; j < G.vexnum; j++)
            if (G.edge[i][j]) cnt++;
    return cnt / 2;
}
~~~



##### 带权图（网）的存储



![image-20241009213558354](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213558354.png)



**带权图先初始化所有边是 0 或者正无穷的都是可以的！**

![image-20241009213605823](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213605823.png)







> 涉及线性代数和矩阵的存储
>
> ![image-20241009214016575](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009214016575.png)
>
> 



##### 邻接矩阵的性质（涉及压缩矩阵的存储） --- 离散数学！！！

**n 阶的就是两点之间的路径长度为 n 个的有几条！！**



![image-20241009213628105](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213628105.png)





![image-20241009213635502](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213635502.png)

![image-20241009213642866](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009213642866.png)

#### 2.邻接表（适用于稀疏图）

![image-20241009220501867](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009220501867.png)

---





![image-20241009220508380](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009220508380.png)

---





![image-20241009220514633](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241009220514633.png)



> **vertices 顶点集（合）**
>
> **vertex 顶点**

与树同理， 一条边对应指向的点

![image-20250104104125048](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104104125048.png)

##### 初始化&&定义

~~~c
/* 邻接表：适合稀疏图。空间 O(n+e) */
#define MaxVex 1000

typedef struct ArcNode {          /* 边表结点 */
    int adjvex;                   /* 这条边指向的顶点编号 */
    struct ArcNode *next;         /* ★ C 里必须写 struct ArcNode*，
                                     此时 typedef 的新名字还没生效 */
} ArcNode;

typedef struct {                  /* 顶点表结点 */
    int data;                     /* 顶点信息 */
    ArcNode *first;               /* 指向第一条依附于该顶点的边 */
} VNode;

typedef struct {
    VNode adjlist[MaxVex];        /* 顶点表数组 */
    int vexnum, arcnum;
} ALGraph;
/* 原代码把顶点表写成 typedef struct{...} adjList[N]; ——
   typedef 一个"数组类型"在 C 里合法，但读起来很绕，
   而且 sizeof、传参的行为都容易踩坑，建议按上面这样拆成两层 */

/* 初始化：所有 first 必须置空 */
void InitALGraph(ALGraph &G, int n) {
    G.vexnum = n;
    G.arcnum = 0;
    for (int i = 0; i < n; i++)
        G.adjlist[i].first = NULL;
}
~~~

##### 添加边结点

~~~c
/* 插入无向边 a—b：两个方向各挂一个边结点（头插法，O(1)）*/
void AddEdge(ALGraph &G, int a, int b) {
    ArcNode *s = (ArcNode *)malloc(sizeof(ArcNode));
    s->adjvex = b;
    s->next = G.adjlist[a].first;      /* 头插：先接后面 */
    G.adjlist[a].first = s;            /*       再接前面 */

    ArcNode *t = (ArcNode *)malloc(sizeof(ArcNode));
    t->adjvex = a;
    t->next = G.adjlist[b].first;
    G.adjlist[b].first = t;

    G.arcnum++;
}
/* 有向图只保留前半段（a→b 只挂在 a 的边表上）。
   注意顶点表里没有虚拟头结点，first 直接指向第一个边结点 */
~~~

##### 传参和基本操作注意（c 语言和 c++特性区别）

~~~c
/* 遍历顶点 x 的所有邻接点（= 出边） */
void PrintNeighbors(ALGraph G, int x) {
    for (ArcNode *p = G.adjlist[x].first; p != NULL; p = p->next)
        printf("%d ", p->adjvex);
    printf("\n");
}

/* 顶点 x 的出度 / 无向图的度：数边表结点个数 */
int OutDegree(ALGraph G, int x) {
    int d = 0;
    for (ArcNode *p = G.adjlist[x].first; p != NULL; p = p->next)
        d++;
    return d;
}

/* 释放整张图的边表（题目要求"销毁"时才写） */
void DestroyALGraph(ALGraph &G) {
    for (int i = 0; i < G.vexnum; i++) {
        ArcNode *p = G.adjlist[i].first, *q;
        while (p != NULL) {
            q = p;
            p = p->next;       /* 先走再释放 */
            free(q);
        }
        G.adjlist[i].first = NULL;
    }
}
~~~

##### 对于 有向图 枚举 入边 和 出边（简单）

~~~c
/* 求顶点 x 的入度（有向图 + 邻接表）
   —— 邻接表求入度很麻烦：必须扫遍所有顶点的边表，看谁指向 x
   时间 O(n + e)，这也是邻接表的主要缺点 */
int InDegree(ALGraph G, int x) {
    int d = 0;
    for (int i = 0; i < G.vexnum; i++) {
        if (i == x) continue;
        for (ArcNode *p = G.adjlist[i].first; p != NULL; p = p->next)
            if (p->adjvex == x) d++;
    }
    return d;
}

/* 如果一道题要反复求入度，更好的做法是先扫一遍建出 indeg[] 数组：
   for (i) for (p = first; p; p = p->next) indeg[p->adjvex]++;
   拓扑排序就是这么干的                                            */
~~~



## 2.==图的基本操作==（对于邻接表和邻接矩阵）

> **注意：有无向图有向图之分！！！**

### 判断图是否存在边 `<x,y>` 有向边（弧） （x, y） 无向边

对于邻接表：遍历链表 时间复杂度：O(1)~O(|V|)  （考虑最好和最坏情况）

![image-20241010224253432](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224253432.png)

---





![image-20241010224311616](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224311616.png)
---

---





![image-20241010224337676](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224337676.png)

---

![image-20241010224346968](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224346968.png)

**邻接矩阵的删除**

---



![image-20241010224404081](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224404081.png)

**邻接表的删除**

---



 ![image-20241010224512653](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224512653.png)

**有向图的删除**

---

![image-20241010224520701](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224520701.png)

**对于邻接表直接头插法即可！！**

---

![image-20241010224528077](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224528077.png)



---



![image-20241010224535557](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224535557.png)

---

![image-20241010224543631](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224543631.png)

---



**带权图的权值获取和查询**

![image-20241010224550180](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241010224550180.png)

---



## 3. 图的遍历

### 1.图的 BFS 遍历

> **对于  <无向图>  && <邻接表>  的 bfs**

~~~c
#define MaxVex 1000

int visited[MaxVex];        /* ★ 定义成【全局】数组，自动初始化为 0。
                               原代码写的是函数内的 bool st[N]，
                               局部数组是垃圾值，visited 判断会随机失效 —— 真 bug */

/* 从顶点 v 出发的广度优先遍历（邻接表版）*/
void BFS(ALGraph G, int v) {
    int Q[MaxVex], front = 0, rear = 0;        /* 数组模拟队列 */
    printf("%d ", v);                           /* ★ 起点自己也要访问，
                                                   原代码只在循环里访问邻接点，把起点漏了 */
    visited[v] = 1;
    Q[rear++] = v;

    while (front < rear) {                      /* 队不空 */
        int t = Q[front++];                     /* 出队 */
        for (ArcNode *p = G.adjlist[t].first; p != NULL; p = p->next) {
            int w = p->adjvex;
            if (!visited[w]) {
                printf("%d ", w);
                visited[w] = 1;                 /* 入队时就标记，不是出队时 */
                Q[rear++] = w;
            }
        }
    }
}

/* 邻接矩阵版：只有内层找邻接点的方式不同。
   MGraph 的定义见前面"1.邻接矩阵"一节 */
void BFS_Matrix(MGraph G, int v) {
    int Q[MaxVex], front = 0, rear = 0;
    printf("%d ", v);
    visited[v] = 1;
    Q[rear++] = v;
    while (front < rear) {
        int t = Q[front++];
        for (int w = 0; w < G.vexnum; w++)      /* 扫第 t 行 */
            if (G.edge[t][w] && !visited[w]) {
                printf("%d ", w);
                visited[w] = 1;
                Q[rear++] = w;
            }
    }
}
~~~



#### 如果图不止一个连通块

#### --> 就无法遍历完所有顶点!!!\

>  **所要添加的操作是：**

~~~c
/* 一次 BFS 只能遍历【一个连通分量】。
   要遍历整张图，必须对每个还没访问过的顶点各发起一次 */
void BFSTraverse(ALGraph G) {
    for (int i = 0; i < G.vexnum; i++)
        visited[i] = 0;                 /* 每次遍历前统一清零 */

    for (int i = 0; i < G.vexnum; i++)
        if (!visited[i]) {
            BFS(G, i);
            printf("\n------\n");       /* 每换一个连通分量打一条分隔线 */
        }
}

/* 由此得到两个高频结论：
   ① 外层 for 里调用 BFS/DFS 的【次数】= 连通分量的个数
   ② 只调用一次就能访问到全部顶点 ⇔ 这是一个连通图
      —— "判断图是否连通"就是这么写的：调一次 BFS，再检查 visited 是否全为 1 */
~~~

### 复杂度分析

![image-20241011192142663](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011192142663.png)

### **为什么是 O(V + E) 而不是 O(V × E)？**

#### 1. **邻接表的存储方式**

- 在邻接表中，每个顶点存储一个链表，链表中包含与该顶点直接相连的所有边。
- 例如，顶点 `v` 的邻接表包含所有以 `v` 为起点的边。

#### 2. **BFS 的执行过程**

- BFS 会访问每个顶点一次，并遍历每个顶点的所有邻接边。
- 由于邻接表中每条边只会被访问一次，因此总的时间复杂度是 **O(V + E)**。

#### 3. **为什么不是 O(V × E)？**

- 如果时间复杂度是 O(V × E)，意味着对于每个顶点，都需要遍历所有边的总数。
- 但实际上，BFS 在邻接表中的实现是：
  - 访问每个顶点一次：O(V)。
  - 遍历每条边一次：O(E)。
- 因此，总时间复杂度是 **O(V + E)**，而不是 O(V × E)。



---

### 广度优先生成树

![image-20250104145016688](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104145016688.png)

**就是根据层次遍历构建树（但不一定是二叉树！！！！！）**

![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011192137652.png)

### 广度优先生成树应用



#### **1. 最短路径问题（无权图）**

- **作用**：
  - 在 **无权图** 中，BFS 生成树可以用于找到从起点到其他所有顶点的 **最短路径**。
  - 因为 BFS 是按层次遍历的，所以生成树中的路径长度就是最短路径长度。
- **示例**：
  - 在社交网络中，BFS 生成树可以用于找到两个人之间的最短关系链。

------

#### **2. 网络分层与层级分析**

- **作用**：
  - BFS 生成树将图按层次划分，可以清晰地表示图的 **层级结构**。
  - 适用于分析网络中的层级关系，例如组织结构、通信网络等。
- **示例**：
  - 在组织架构中，BFS 生成树可以表示从 CEO 到各级员工的层级关系。

------

#### **3. 连通性分析**

- **作用**：
  - **BFS 生成树可以用于判断图的连通性**。
  - 如果 BFS 生成树包含所有顶点，则图是连通的；否则，图是非连通的。
- **示例**：
  - 在计算机网络中，BFS 生成树可以用于分析网络的连通性。

------

#### **4. 最小生成树的基础**

- **作用**：
  - 在 **无权图** 中，BFS 生成树本身就是一种生成树。
  - 在 **带权图** 中，BFS 生成树可以为最小生成树算法（如 Prim 算法）提供基础。
- **示例**：
  - 在通信网络中，BFS 生成树可以用于初步设计网络拓扑。

------

#### **5. 图的遍历与路径规划**

- **作用**：
  - BFS 生成树可以用于系统地遍历图的所有顶点，确保不遗漏任何顶点。
  - 适用于路径规划问题，例如迷宫求解、机器人导航等。
- **示例**：
  - 在迷宫求解中，BFS 生成树可以找到从起点到终点的最短路径。



#### 2.图的 DFS 遍历

> 针对于 无向图 和 邻接表的 dfs 遍历

~~~c
/* 深度优先遍历（邻接表版）*/
void DFS(ALGraph G, int v) {
    printf("%d ", v);                  /* ★ 一进来就访问自己 */
    visited[v] = 1;                    /*    并立刻标记 */
    for (ArcNode *p = G.adjlist[v].first; p != NULL; p = p->next)
        if (!visited[p->adjvex])
            DFS(G, p->adjvex);         /* 对每个未访问的邻接点递归下去 */
}

/* 原代码把"访问 + 标记"写在 for 里面的 if 中，只处理邻接点，
   起点 v 自己既没被打印也没被标记 —— 结果是起点会被重复访问，
   还得靠调用方在外面补一句 st[v]=1。
   规范写法就是上面这样：进函数先访问自己，责任落在函数内部 */

/* 邻接矩阵版：只有找邻接点的方式不同 */
void DFS_Matrix(MGraph G, int v) {
    printf("%d ", v);
    visited[v] = 1;
    for (int w = 0; w < G.vexnum; w++)
        if (G.edge[v][w] && !visited[w])
            DFS_Matrix(G, w);
}
~~~

#### 如果图不止一个连通块

#### --> 就无法遍历完所有顶点!!!

~~~c
/* 遍历整张图：对每个未访问顶点各发起一次 DFS */
void DFSTraverse(ALGraph G) {
    for (int i = 0; i < G.vexnum; i++)
        visited[i] = 0;                 /* 统一清零 */

    for (int i = 0; i < G.vexnum; i++)
        if (!visited[i]) {
            DFS(G, i);                  /* 标记的事交给 DFS 内部做，
                                           原代码在这里又写了一次 st[i]=1，
                                           和 DFS 内部重复，容易看晕 */
            printf("\n--------\n");
        }
}

/* DFS 的空间复杂度 = 递归栈深度 = O(n)（最坏是一条链）
   BFS 的空间复杂度 = 队列长度   = O(n)
   两者时间复杂度都是：邻接表 O(n+e)，邻接矩阵 O(n^2) */
~~~



### 复杂度分析

![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011210933645.png)

**思维：dfs 找全部解，一旦 tle 了就记忆化，剪枝或者改为 bfs（最短路），实在不行就 dp！！**



![image-20241011211122218](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211122218.png)

**访问过的就不会再访问了所以和 bfs 时间复杂度一样！！**

---



![image-20241011211157535](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211157535.png)

![image-20241011211202359](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211202359.png)

---



### 深度优先生成树/森林

![image-20250821220137055](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220137055.png)



![image-20241011211207045](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211207045.png)

![image-20241011211211264](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211211264.png)

![image-20241011211215101](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211215101.png)

---









## *最短路

### 0.bfs  （✓） （win + .）



### 1.dijkstra

![image-20241013142449294](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013142449294.png)

![image-20241013142453353](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013142453353.png)

```c
/* Dijkstra：单源最短路，不能有负权边。邻接矩阵版，顶点编号 1..n */
#define MaxVex 510
#define INF 0x3f3f3f3f              /* 用 0x3f3f3f3f 当无穷大：
                                       两个相加不会溢出，memset 也能按字节铺 */

int g[MaxVex][MaxVex];              /* 邻接矩阵，存权值 */
int dist[MaxVex];                   /* dist[i] = 源点到 i 的当前最短距离 */
int final_[MaxVex];                 /* final_[i] = 1 表示 i 的最短路已确定 */
int path[MaxVex];                   /* path[i] = i 在最短路上的前驱，用来还原路径 */
int n;

void Dijkstra(int v0) {
    for (int i = 1; i <= n; i++) {
        dist[i]   = g[v0][i];                       /* 初始就是直连距离 */
        final_[i] = 0;
        path[i]   = (dist[i] < INF) ? v0 : -1;
    }
    dist[v0] = 0;  final_[v0] = 1;  path[v0] = -1;

    for (int k = 1; k < n; k++) {                   /* 还要确定 n-1 个顶点 */
        int t = -1, min = INF;
        for (int j = 1; j <= n; j++)                /* 在未确定的点里挑 dist 最小的 */
            if (!final_[j] && dist[j] < min) { min = dist[j]; t = j; }

        if (t == -1) break;         /* ★ 剩下的点都不可达，必须退出。
                                       原代码没有这个判断，t 保持 -1 就去访问
                                       dist[-1]、g[-1][j]，直接数组越界 */
        final_[t] = 1;

        for (int j = 1; j <= n; j++)                /* 松弛：用 t 更新别人 */
            if (!final_[j] && dist[t] + g[t][j] < dist[j]) {   /* ★ 原代码漏了 !final_[j] */
                dist[j] = dist[t] + g[t][j];
                path[j] = t;                        /* 记住是从 t 过来的 */
            }
    }
}

/* 建图时的初始化（有重边取小的） */
void InitGraph(int n) {
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            g[i][j] = (i == j) ? 0 : INF;
}
void AddEdge(int a, int b, int c) {
    if (c < g[a][b]) g[a][b] = c;       /* 防重边 */
}

/* 还原 v0 → v 的路径（path 是反向的，用递归正序输出） */
void PrintPath(int v0, int v) {
    if (v == v0) { printf("%d ", v0); return; }
    if (path[v] == -1) { printf("不可达\n"); return; }
    PrintPath(v0, path[v]);
    printf("%d ", v);
}
```

### 时间复杂度（与 prim 极其类似）

### 2.floyd



**key：中转点**

![image-20241013140817638](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013140817638.png)

![image-20241013140846502](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013140846502.png)







~~~c
/* Floyd：所有点对最短路。可以有负权边，但不能有负权回路 */
#define MaxVex 110
#define INF 0x3f3f3f3f

/* 注意：下面的 A / fpath 与上一节 Dijkstra 的 dist / path 是两套独立的数组，
   Floyd 的 fpath 是二维的，存的语义也不同（中转点 vs 前驱） */
int A[MaxVex][MaxVex];        /* A[i][j] = i 到 j 的当前最短距离 */
int fpath[MaxVex][MaxVex];    /* fpath[i][j] = i 到 j 路径上的【中转点】，-1 表示直连 */

void Floyd(int g[][MaxVex], int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            A[i][j] = (i == j) ? 0 : g[i][j];
            fpath[i][j] = -1;
        }

    for (int k = 0; k < n; k++)                  /* ★ 中转点 k 必须在【最外层】 */
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (A[i][k] + A[k][j] < A[i][j]) {
                    A[i][j] = A[i][k] + A[k][j];
                    fpath[i][j] = k;             /* 记下中转点 */
                }
}
/* k 放内层就是错的。理解：外层每做完一轮 k，
   A[i][j] 的含义是"只允许经过前 k 个点中转时的最短路" */

/* 还原路径：path 存的是【中转点】不是前驱，所以要【递归地往两边劈】 */
void PrintFloydPath(int i, int j) {
    if (fpath[i][j] == -1) {         /* 没有中转点，i 和 j 直连 */
        printf("%d->%d ", i, j);
        return;
    }
    int k = fpath[i][j];
    PrintFloydPath(i, k);            /* 先走 i→k */
    PrintFloydPath(k, j);            /* 再走 k→j */
}

/* 原代码的还原写成 while (ed != st) { ed = path[st][ed]; }，
   那是把 path 当【前驱数组】在用 —— 但 Floyd 的 path 存的是中转点，
   一路 path[st][ed] 跳下去既不会收敛到 st，输出的也不是真实路径。
   Dijkstra 的 path 才是前驱，可以那样回溯                        */
~~~

**时空复杂度：0(v3 次方) o(v2 次方)**

**floyd 可以解决带负权边的问题！**



![image-20241013141204822](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013141204822.png)



![image-20241013141213311](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013141213311.png)

**时空复杂度具体还是得看图的存储结构**

---

# 拓扑排序（可判断回路）

**key ： 拓扑排序一定是有向无环图！**



![image-20241013143603689](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013143603689.png)

![image-20241013143703056](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013143703056.png)

### 邻接矩阵法

~~~c
/* 拓扑排序（邻接矩阵版）。用栈存放当前入度为 0 的顶点 */
#define MaxVex 100

int g[MaxVex][MaxVex];      /* 邻接矩阵 */
int indeg[MaxVex];          /* 各顶点入度 */
int n;

/* 返回 1 表示排序成功（无环），排好的序列放在 order 中；返回 0 表示有环 */
int TopoSort(int order[]) {
    int st[MaxVex], top = -1;      /* 栈，装的全是入度为 0 的顶点 */
    int cnt = 0;                   /* 已输出的顶点数 */

    for (int i = 1; i <= n; i++)   /* 先把所有入度为 0 的点入栈 */
        if (indeg[i] == 0) st[++top] = i;

    while (top != -1) {
        int t = st[top--];         /* 出栈 */
        order[cnt++] = t;
        for (int i = 1; i <= n; i++)
            if (g[t][i]) {                     /* t → i 这条边要"删掉" */
                if (--indeg[i] == 0)           /* 减完变 0 就入栈 */
                    st[++top] = i;
            }
    }
    return cnt == n;               /* 没输出完 = 图中有环 */
}

/* 统计入度：第 j 【列】非零元素的个数 */
void CalcIndegree(void) {
    for (int i = 1; i <= n; i++) indeg[i] = 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            if (g[i][j]) indeg[j]++;
}

/* 说明：
   ① 原代码用 C++ 的 vector<int> ans 收结果，408 里换成 int order[] + cnt
   ② 辅助结构用栈还是队列都行，得到的拓扑序列可能不同，但都合法
   ③ 栈里的元素在任何时刻都满足"入度为 0"——这是这个算法的不变式
   ④ 原代码的 cnt 是全局变量且从不清零，第二次调用就会算错          */
~~~

### 邻接表写法

~~~c
/* 拓扑排序（邻接表版）—— 邻接表更省事：删边只需遍历该顶点的边表 */
#define MaxVex 100010

typedef struct ArcNode {
    int adjvex;
    struct ArcNode *next;
} ArcNode;

typedef struct {
    int data;
    ArcNode *first;
} VNode;

typedef struct {
    VNode adjlist[MaxVex];
    int vexnum, arcnum;
} ALGraph;

int indeg[MaxVex];      /* 与上一块（邻接矩阵版）的 indeg 是两套独立实现，
                           看笔记时二选一，不要把两块拼在一起编译 */

/* 建有向边 a → b */
void AddEdge(ALGraph &G, int a, int b) {
    ArcNode *s = (ArcNode *)malloc(sizeof(ArcNode));
    s->adjvex = b;
    s->next = G.adjlist[a].first;
    G.adjlist[a].first = s;
}

/* 统计入度：扫一遍所有边表，被指向的那个顶点入度 +1 */
void CalcIndegree(ALGraph G) {
    for (int i = 1; i <= G.vexnum; i++) indeg[i] = 0;
    for (int i = 1; i <= G.vexnum; i++)
        for (ArcNode *p = G.adjlist[i].first; p != NULL; p = p->next)
            indeg[p->adjvex]++;
}

int TopoSort(ALGraph G, int order[]) {
    int st[MaxVex], top = -1, cnt = 0;

    CalcIndegree(G);
    for (int i = 1; i <= G.vexnum; i++)
        if (indeg[i] == 0) st[++top] = i;

    while (top != -1) {
        int t = st[top--];
        order[cnt++] = t;
        for (ArcNode *p = G.adjlist[t].first; p != NULL; p = p->next)
            if (--indeg[p->adjvex] == 0)
                st[++top] = p->adjvex;
    }
    return cnt == G.vexnum;
}

/* 原代码的 main 里，真正的拓扑排序整段被注释掉了，
   只剩一句 cout << inedge[2]; 的调试输出 —— 这段代码当时没写完 */

/* 判定拓扑序列【唯一】（2024 真题）：把上面改成
   每一轮检查"入度为 0 的顶点是不是恰好只有 1 个"，
   有 0 个说明有环，有 ≥2 个说明这一步可以任选，序列就不唯一 */
~~~

**注意点：初始化问题 nullptr 一定！！**

**删除边问题**



### 逆拓扑排序（使用 dfs）

### 对于逆序 考虑 dfs（递归栈）

#### 整体

~~~c
/* 逆拓扑排序（DFS 版）：DFS 结束时才输出，得到的正好是逆拓扑序列 */
#define MaxVex 100010

int visited[MaxVex];
int result[MaxVex], rcnt;      /* 收集输出，倒过来就是拓扑序列 */

void DFS(ALGraph G, int v) {
    visited[v] = 1;            /* ★ 一进来就标记自己。
                                  原代码只在 for 里给邻接点标记，
                                  起点没标记 → 会被重复访问 */
    for (ArcNode *p = G.adjlist[v].first; p != NULL; p = p->next)
        if (!visited[p->adjvex])
            DFS(G, p->adjvex);

    result[rcnt++] = v;        /* ★ 关键：递归【结束后】才记录，
                                  这就是"逆拓扑" —— 所有后继都处理完了才轮到自己 */
}

void DFSTraverse(ALGraph G) {
    for (int i = 1; i <= G.vexnum; i++) visited[i] = 0;
    rcnt = 0;
    for (int i = 1; i <= G.vexnum; i++)
        if (!visited[i]) DFS(G, i);
}

/* 用法：
   DFSTraverse(G);
   result[0..rcnt-1]              是【逆】拓扑序列
   倒着输出 result[rcnt-1..0]      就是拓扑序列                */
void PrintTopo(void) {
    for (int i = rcnt - 1; i >= 0; i--)
        printf("%d ", result[i]);
    printf("\n");
}

/* 对照记忆：
   · 普通 DFS —— 进入时输出（printf 在递归【前】）
   · 逆拓扑   —— 退出时输出（printf 在递归【后】）
   只差一行位置                                                */
~~~

#### 核心代码

~~~c
/* 核心就这两个函数，其余都是建图的样板。
   ⚠ 这两段与上一块【完全相同】，只是单独摘出来方便记忆，不是新代码 */
void DFS(ALGraph G, int v) {
    visited[v] = 1;                                  /* 进来先标记自己 */
    for (ArcNode *p = G.adjlist[v].first; p != NULL; p = p->next)
        if (!visited[p->adjvex])
            DFS(G, p->adjvex);
    result[rcnt++] = v;                              /* 出去时才记录 → 逆拓扑 */
}

void DFSTraverse(ALGraph G) {
    for (int i = 1; i <= G.vexnum; i++) visited[i] = 0;
    rcnt = 0;
    for (int i = 1; i <= G.vexnum; i++)
        if (!visited[i]) DFS(G, i);                  /* 标记交给 DFS 内部，
                                                        外面不用再写一次 */
}
~~~

![image-20241013170231676](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241013170231676.png)

# 关键路径(可以运用到实践！！！)

**网：带权边图**



![image-20250104152648586](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104152648586.png)

必须是 ==有向无环图==

![image-20250104153331492](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104153331492.png)

普通活动：可以拖延的活动！

### 求关键路径

**步骤：先求点（事件 == 就是== 活动 == 完成后的一个状态），在求边（活动） ---> 最早/晚开始时间 **  

**ve，vl**

**e , l**



**求 ve 拓扑排序（入度为零） 取 ==最大==** 

**求 vl 逆拓扑（出度为零） 取 ==最小==**

key：当前事件要达到 入度（活动）都要删除（完成）

![image-20250104155038735](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104155038735.png)

![image-20250104155329424](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104155329424.png)

![image-20250104155444586](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104155444586.png)

**时间余量：最晚开始时间- 最早开始时间 （可以拖延的时间）！！！！**

# 八、最小生成树(一般是针对无向图的)

**连通图概念：从一个顶点可以到达任意一个顶点（都有路径）**

生成树：表示所有顶点均由边连接在一起，但 **不存在回路** 的图

![image-20250104160033803](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104160033803.png)

## 1.prim 算法（找点为核心）

![image-20250104160302843](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104160302843.png)

**点亮的部分 ：当前的最小生成树**  每次都在没点亮的点中找   距离点亮的点  中最近（距离最短）的点点亮（加入最小生成树）



![image-20241011211526962](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211526962.png)

![image-20241011211542709](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211542709.png)

![image-20241011211551109](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211551109.png)

---



## prim 实现操作

![image-20241011211950682](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211950682.png)

![image-20241011212001654](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212001654.png)

![image-20241011212008783](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212008783.png)

![image-20241011212123191](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212123191.png)

![image-20241011212129170](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212129170.png)

---







​	



## 2. kruskal 算法（找边为核心）



![image-20250821220148476](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220148476.png)

**每次找最短的边连接 连接之前有条件 ： 就是这条边的两个端点是否连通（不一定是 ==直连==）**

![image-20241011211618541](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211618541.png)

![image-20241011211634355](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211634355.png)

## kruskal 实现操作（并查集）



![image-20241011212138688](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212138688.png)

![image-20241011212205046](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212205046.png)

![image-20241011212208675](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212208675.png)

![image-20241011212211415](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011212211415.png)



## ==sum==

![image-20241011211648769](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241011211648769.png)



# 有向无环图 的表达式求值

![image-20241015164413069](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164413069.png)



![image-20241015164423599](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164423599.png)

![image-20241015164431523](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164431523.png)

![image-20241015164437958](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164437958.png)



# ==-------《查找》--------==



**查找长度的概念：对比关键字的次数！**

## 查找的基本概念

![image-20250104162840604](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104162840604.png)



![image-20241016211125959](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016211125959.png)

---



![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016211217831.png)

## 查找算法的效率分析

![image-20241016211256652](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016211256652.png)

## 平均查找长度公式：

![image-20241016211347984](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016211347984.png)

**注意：ASL 的数量级反映了这个查找算法的时间复杂度！**



# 1^o^   顺序查找

![image-20250104163557792](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104163557792.png)

**查找概率看 ==元素权重==**

![image-20241017192820102](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017192820102.png)

**带哨兵与不带哨兵 仅有微妙的区别 重点在于 查找成功和查找失败的情况**

ASL = （每个点 **查找次数** 乘上 **查找概率** ）之和

**通过 有序 来优化算法**

### 查找失败主要针对失败结点！！！

![image-20250104174837063](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104174837063.png)

**分子：每个失败结点的查找次数之和**



![image-20241017193115000](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017193115000.png)



![image-20241017193548148](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017193548148.png)





# 2^o^   折半查找（二分）--必须数组且有序



1. **ASL**：反映整体查找效率，是所有元素查找长度的加权平均。
2. **每个点的查找长度**：反映单个元素的查找效率，具体到某个元素的比较次数。

---



## 构造二分查找判定树

<span style="color:#FF00FF;">**失败的ASL就是   每个查找的次数之和/失败结点（前提是概率一样）**</span>



**key： 失败和成功都和树高有关系**



**将收尾下标（从 1 开始）相加除以二 然后取这个位置作为根节点递归处理**



![image-20241017193951847](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017193951847.png)

---



![image-20241017193935293](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017193935293.png)

**查找失败的分母就是失败结点的个数**



## 折半查找判定树的树高 h：



![image-20241017195049820](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017195049820.png)

**观察树满足什么性质 判断树的种类 确定计算方法！！！** 

![image-20241017195110393](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017195110393.png)

---

## 时间复杂度

![image-20241017195225185](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017195225185.png)

---

**这个时间复杂度怎么来的？**





## 查找成功与查找失败

**二分查找判定树  是个 ==二叉排序树 + 二叉平衡树==**



## sum

![image-20241017194037958](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017194037958.png)

**不对称的分为左/右多的两种情况**

![image-20241017210430792](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241017210430792.png)



**正常做法直接画图就行 ： 根据判定树逆向画集合序列 然后判断是向上取整还是向下取整如果矛盾了就是错的！**



---



# 3^o^   分块查找

**特征：块间有序--- 块内无序**

**查找存储结构** 最大值和上下界

![image-20250109221246273](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250109221246273.png)

![image-20250104204502785](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250104204502785.png)

# 九、二叉排序树（二叉搜索树）

## 堆与二叉排序树的区别



#### **堆**

- 堆是一种 **完全二叉树**。
- 堆分为 **最大堆** 和 **最小堆**：
  - **最大堆**：每个节点的值都大于或等于其子节点的值。
  - **最小堆**：每个节点的值都小于或等于其子节点的值。
- 堆的根节点是最大值（最大堆）或最小值（最小堆）。
- 堆通常用于实现 **优先队列**。

#### **二叉排序树（BST）**

- 二叉排序树是一种二叉树，满足以下性质：
  - 左子树的所有节点的值都小于根节点的值。
  - 右子树的所有节点的值都大于根节点的值。
  - 左右子树也分别是二叉排序树。
- BST 的中序遍历结果是一个 **有序序列**。
- BST 通常用于动态集合的查找、插入和删除操作。



---



## 二叉搜索树的定义(与折半查找树类似)

### 折半查找和二叉排序树的时间复杂度关系





![308062505289bd26cd75ce60b260b36](https://raw.githubusercontent.com/kasahuki/os_test/main/img/308062505289bd26cd75ce60b260b36.png)



![image-20241015164542843](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164542843.png)

**进行中序遍历得到最终的有序序列**

## 查找



![image-20250821220154592](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250821220154592.png)



##  插入

## ![image-20241015164737288](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164737288.png)

## 构造



![image-20241015164756645](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164756645.png)

## 删除分三种情况

### 1.结点是叶子结点 

**直接删除**

### 2.结点只有一边的子树（代替）



![image-20241015164836591](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015164836591.png)

### 3.结点两边都有子树！！！！！

**相当于找中序遍历的前驱/后继 （因为中序遍历二叉排序树就是一个有序序列）**

#### 又分为两种做法 ： 处理 后继和前驱 

![image-20241015165111380](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015165111380.png)

**根据二叉排序树的特性进行的措施！**

![image-20241015165124001](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015165124001.png)

## 查找效率分析

**插入主要就是查找的过程！！**

![image-20250105144240339](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105144240339.png)

###  查找成功

![image-20241015165339468](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015165339468.png)

**最好情况：二叉树的高度为 log2^n+1  平均查找长度为 O (log2^（n+1）)**

**最坏情况：每个结点有且仅有一个分支 树高 h = 结点数 n  ==退化为链表== , 平均查找长度为 o(n)**

**原因就是构造时的问题**

**解决方法：构造时构造 ==平衡二叉树！==**

### 查找失败

![image-20241015165750084](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241015165750084.png)

# 十、平衡二叉树（AVL 树）

**当二叉搜索树本来就有序的时候二叉搜索树就会退化为链表**

**所以引入 ————>    ==<平衡二叉树>==** 

**平衡二叉树：是一种特殊的二叉搜索树（二叉排序树）**

![image-20250105144313925](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105144313925.png)

![image-20250105151205375](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105151205375.png)

### 旋转操作 ==(调整失衡)==



![image-20250105151219618](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105151219618.png)

**确定失衡因子 ：** 确定是 ==哪个孩子== 的 ==哪个子树== 上

如图就是 ==LL 型==

![image-20250105165259938](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105165259938.png)





![image-20250105165725423](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105165725423.png)

![image-20250105165818401](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105165818401.png)



![ ](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105165826570.png)



### 四种失衡情况 



![image-20250105165113988](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105165113988.png)

**和构建二叉排序树一样 但是多了一步 也就是在增删改的过程中如果导致失衡了就要进行平衡操作！**

### 平衡二叉树操作

**插入&构建：**

![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105170221788.png)

**删除**:

**删除结点后可能导致多个地方失衡了**

**需要依次沿着祖先向上检查和调整**

![image-20250105170536270](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105170536270.png)

# 十一、红黑树













# 十二、B 树



# 十三、B+树





# ==十四、堆==

**堆一定是一颗完全二叉树**



![image-20250105144257762](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105144257762.png)

## up 和 down 逻辑



~~~c
/* 小根堆。下标从 1 开始：结点 u 的双亲是 u/2，孩子是 2u 和 2u+1 */
#define MaxSize 100010
int h[MaxSize];       /* 堆数组 */
int Size;             /* 当前元素个数 */

/* C 没有 std::swap，自己写一个 */
void Swap(int *a, int *b) {
    int t = *a; *a = *b; *b = t;
}

/* 向上调整：新插入的元素往上冒，直到比双亲大 */
void Up(int u) {
    while (u / 2 > 0 && h[u] < h[u / 2]) {    /* u/2 > 0 保证没越过根 */
        Swap(&h[u], &h[u / 2]);
        u /= 2;
    }
}

/* 向下调整：在 u 和它两个孩子里挑最小的换上来，递归往下 */
void Down(int u) {
    int t = u;                                        /* t 记录三者中最小的下标 */
    if (2 * u     <= Size && h[2 * u]     < h[t]) t = 2 * u;
    if (2 * u + 1 <= Size && h[2 * u + 1] < h[t]) t = 2 * u + 1;
    /* 两个 if 都要写，且都要先判越界再取值 */
    if (t != u) {
        Swap(&h[t], &h[u]);
        Down(t);                                      /* 继续往下沉 */
    }
}

/* 大根堆只需把两个 < 改成 > */
~~~

**堆是完全二叉树，下标是不会变化的，变化的仅有数据**

## 建堆

~~~c
/* 建堆：从最后一个【非叶结点】开始，逐个向下调整 */
void BuildHeap(int n) {
    Size = n;
    for (int i = n / 2; i >= 1; i--)      /* n/2 就是最后一个非叶结点（下标从 1 计） */
        Down(i);
}

/* 为什么从 n/2 开始而不是从 n 开始？
   叶结点没有孩子，本身就满足堆的性质，不需要调整。

   ★ 下标从 0 开始时，最后一个非叶结点是 (n-2)/2，公式不一样，别记混：
       下标从 1：孩子 2i / 2i+1，建堆起点 n/2
       下标从 0：孩子 2i+1 / 2i+2，建堆起点 (n-2)/2

   建堆的时间复杂度是 O(n)，不是 O(n log n) ——
   底层结点多但要下沉的层数少，加权求和后是线性的 */
~~~



## 操作

### 1.插入一个数

~~~c
/* 插入：放到数组末尾，然后向上调整 */
void Insert(int x) {
    h[++Size] = x;
    Up(Size);
}
/* 时间复杂度 O(log n)，即树高 */
~~~



### 2.求堆顶

`h[1]`

### 3.删除堆顶

~~~c
/* 删除堆顶：用最后一个元素覆盖堆顶，Size--，再把它向下调整 */
void DeleteTop(void) {
    if (Size < 1) return;               /* 原代码没判空，空堆时 Size 会变成 -1 */
    h[1] = h[Size--];
    Down(1);
}

/* 读堆顶（不删）：直接返回 h[1]，O(1) */
int GetTop(void) {
    return h[1];
}
~~~



### 4.删除任意一个元素

~~~c
/* 删除任意位置 k 的元素 */
void DeleteAt(int k) {
    if (k < 1 || k > Size) return;
    if (k == Size) { Size--; return; }  /* ★ 删的就是最后一个，直接缩短即可。
                                           原代码在这种情况下会 h[k]=h[k] 后 Size--，
                                           然后对已经不在堆里的位置 k 做 up/down */
    h[k] = h[Size--];                   /* 用最后一个元素填到 k 的位置 */
    Up(k);
    Down(k);                            /* 新值可能比双亲小，也可能比孩子大，
                                           所以两个方向都要试；两者最多只有一个会真正动 */
}
~~~



### 5.修改任意一个元素

~~~c
/* 修改任意位置 k 的值为 x */
void Change(int k, int x) {
    if (k < 1 || k > Size) return;
    h[k] = x;
    Up(k);
    Down(k);        /* 同上：改大了要下沉，改小了要上浮，写两个最省事 */
}
~~~





# 十五、哈希表(散列查找)

**处理冲突的方法 ； 拉链法 开放寻址法**

**散列表的构造： 除留余数法 直接定址法 平方取中法 数字分析法**

# 一、 拉链法



[树的相关知识](#五、树)

![image-20241016195939589](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016195939589.png)

**==特别的==：注意题目 如果位置上都没有数的话 就无需判断(无需比较关键字)，也就是查找长度是 ==0== ！**

**冲突越多 查找效率越低**

![image-20241016202801877](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016202801877.png)





## 散列表的构造

**！！！！**

**要不大于散列表长度的 才行**

**如果散列表长度 15 mod 19 可能会被映射到大于 16 小于 18 的范围内**

---



![image-20241016202753965](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016202753965.png)

## 1.除留余数法

### 使用数组模拟

~~~c
/* 散列表 · 拉链法（数组模拟链表，竞赛常用写法）
   N 取一个比数据量稍大的质数，冲突更少 */
#define N 100003

int h[N];          /* h[k] = 第 k 条链的头结点下标，-1 表示空链 */
int e[N], ne[N];   /* e[i] 存值，ne[i] 存下一个结点下标 —— 这是"静态链表" */
int idx;           /* 下一个可用的结点下标 */

void InitHash(void) {
    for (int i = 0; i < N; i++) h[i] = -1;   /* 必须初始化为 -1 */
    idx = 0;
}

void Insert(int x) {
    int k = (x % N + N) % N;      /* 先 +N 再取模，保证负数也落在 [0, N) */
    e[idx] = x;
    ne[idx] = h[k];               /* 头插 */
    h[k] = idx++;
}

int Find(int x) {
    int k = (x % N + N) % N;
    for (int i = h[k]; i != -1; i = ne[i])
        if (e[i] == x) return 1;
    return 0;
}

/* 408 更常考的是【顺序表 + 除留余数 + 线性探测】，见"开放寻址法"一节；
   拉链法在真题里主要考手画表和算 ASL，写代码的概率很低 */
~~~

![image-20241016202329672](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016202329672.png)

![image-20241016203135175](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016203135175.png)

**但是使用 mod 素数法也不一定是最优的 如果如上是 ==连续== 的就不是最优的了 （具体题目具体分析！**）

此邻接表也可用于 ==建图== ！！ 

## Create Graph

==**h 存的都是下标指针一类的！！**==

~~~c
/* 邻接表的"数组模拟"写法（不用 malloc，竞赛里常见）
   和上面的拉链法是同一套结构：h[] 是表头，e[]/ne[] 是链上的结点 */
#define N 100010

int h[N];              /* h[a] = 顶点 a 的第一条边的下标，-1 表示没有边 */
int e[N], ne[N], w[N]; /* e[i] 边指向的顶点，ne[i] 下一条边，w[i] 权值 */
int idx;

void InitGraph(int n) {
    for (int i = 0; i <= n; i++) h[i] = -1;
    idx = 0;
}

/* 加有向边 a → b，权值 weight */
void AddEdge(int a, int b, int weight) {
    e[idx] = b;
    w[idx] = weight;
    ne[idx] = h[a];        /* 头插 */
    h[a] = idx++;
}
/* 无向边就正反各调用一次：AddEdge(a,b,w); AddEdge(b,a,w); */

/* 遍历顶点 a 的所有出边： */
void PrintEdges(int a) {
    for (int i = h[a]; i != -1; i = ne[i])
        printf("%d(w=%d) ", e[i], w[i]);
    printf("\n");
}

/* ⚠ 这是竞赛写法，408 答题时用【结构体 + 指针】的邻接表更贴合教材，
   见前面"邻接表"一节。两者是同一个数据结构的两种实现 */
~~~



### 使用拉链法（就是散列表）

~~~c
/* 散列表 · 拉链法（结构体 + 指针版，贴合教材写法）*/
#define N 10003        /* 取质数 */

typedef struct HNode {
    int data;
    struct HNode *next;
} HNode;

typedef struct {
    HNode *first;      /* 每个槽位挂一条链 */
} Slot;

typedef struct {
    Slot slot[N];
    int count;         /* 已存元素个数，用来算装填因子 */
} HashTable;

/* ★ 初始化极其重要：所有 first 必须置空。
   HashTable p; 是局部变量，不初始化的话 first 全是垃圾值 */
void InitHash(HashTable &H) {
    for (int i = 0; i < N; i++)
        H.slot[i].first = NULL;
    H.count = 0;
}

int Hash(int x) {
    return (x % N + N) % N;        /* 先 +N 再取模，负数也能落进 [0, N) */
}

void Insert(HashTable &H, int x) {
    int k = Hash(x);
    HNode *s = (HNode *)malloc(sizeof(HNode));
    s->data = x;
    s->next = H.slot[k].first;     /* 头插，O(1) */
    H.slot[k].first = s;
    H.count++;
}

int Search(HashTable H, int x) {
    int k = Hash(x);
    for (HNode *p = H.slot[k].first; p != NULL; p = p->next)
        if (p->data == x) return 1;
    return 0;
}

/* 原代码里有两处直接导致编译失败：
   ① return 1；   用的是中文全角分号，不是 ASCII 的 ;
   ② 函数之间插了一行 ------------------------ 分隔线，
      它不是注释，会被当成代码解析
   写笔记时分隔线要放在代码块【外面】 */
~~~





## 2.直接定址法 （适合连续的元素）

## 

![image-20241016203346967](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016203346967.png)

## 3. 平方取中法

**选定散列函数时不一定知道关键字的全部情况 取其中某几位也不一定合适**

都不均匀的情况

![image-20250105123548408](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105123548408.png)

## 4.数字分析法 // 如电话号码 

适用条件 ： **必须事先知道 ==所有关键字== 的每一位上的各种数字的分布情况**

如 135xxxxx……这种 135 就 ==不均匀== 分布比较多



## ![image-20250105123623761](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105123623761.png)



**key：就是尽可能的减小冲突，也有可能完全避免冲突的（具体问题具体分析！！！**



![image-20241016203421863](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016203421863.png)

# 二、开放寻址法

<font size=8> ==**! 注意：  m 表示散列表表长度**== </font>



**key ： 如果偏移时超过散列表长度了就mod也就是等效作环**

## 1.线性探测法（最重要！！）

![image-20250105130337305](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105130337305.png)

![image-20250105130543287](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105130543287.png)

 

### 缺点

![img](https://raw.githubusercontent.com/kasahuki/os_test/main/img/%7B2FE42FCB-10B0-4D5A-8718-B194A7B0CCEC%7D)

![image-20241016204343928](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20241016204343928.png)

**导致遇到逻辑删除的位置还是要一直查询！**

## 2.平方探测法

**弥补了以上问题**

> ![image-20250105130854543](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105130854543.png)
>
> 
>
> 

## 3.伪随机探测法

![image-20250105131922185](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105131922185.png)



## 4.双散列法（准备多个散列表）

![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105131823291.png)



## 删除一个元素

![image-20250105132155895](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105132155895.png)



![image-20250105132449143](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105132449143.png)



![](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105132613736.png)



# 十六、排序

## 排序分类：

![image-20250103170109778](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103170109778.png)

**复杂度分析！！！！**



> 对于递归 画树更好理解！		
>
> 稳定 插帽龟 and  统计鸡

## 算法的稳定性

![image-20240927221330046](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240927221330046.png)



## 1.归并排序

~~~c
/* 二路归并排序。B 是辅助数组，必须和 A 一样长 */
#define MaxSize 100010
int B[MaxSize];

/* 把 A[low..mid] 和 A[mid+1..high] 两段有序区合并成一段 */
void Merge(int A[], int low, int mid, int high) {
    for (int k = low; k <= high; k++)
        B[k] = A[k];                       /* 先整体拷进辅助数组 */

    int i = low, j = mid + 1, k = low;
    while (i <= mid && j <= high)
        A[k++] = (B[i] <= B[j]) ? B[i++] : B[j++];   /* ★ <= 才稳定，写 < 会破坏稳定性 */
    while (i <= mid)  A[k++] = B[i++];      /* 剩下的直接搬过来 */
    while (j <= high) A[k++] = B[j++];      /* 这两个 while 只会执行一个 */
}

void MergeSort(int A[], int low, int high) {
    if (low >= high) return;                /* 只剩一个元素，天然有序 */
    int mid = (low + high) / 2;
    MergeSort(A, low, mid);
    MergeSort(A, mid + 1, high);
    Merge(A, low, mid, high);               /* 先分到底，再往回合并 */
}

/* 时间 O(n log n)（最好/最坏/平均都是），空间 O(n)，稳定。
   原代码把辅助数组的下标 k 从 0 开始，回写时再用 j 对齐，
   容易和 low 搞混；直接让 B 和 A 用同一套下标更不容易错 */
~~~

## 2.快速排序

思路 ： 任选一个元素作为 枢轴（pivot	）量 然后让两边 分别小于/大于这个元素

![image-20250105100449314](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105100449314.png)

这样需要额外开一个数组！！



---

这个方法 第一次先让 right 从右往左走！！！ 

![image-20250103171534948](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103171534948.png)

**划分完成：**



![image-20250103171543490](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103171543490.png)

**递归处理：**



![image-20250103171639513](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103171639513.png)

### 递归的时空复杂度分析

每次划分枢轴都刚好是中间值 的话就是效率最好的情况

![image-20250103172242296](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103172242296.png)

**递归会占用系统栈空间 所以会有辅助空间的开销**

**最坏情况**：本来就有序，而且每次枢轴量取当前区间的第一个元素

**如果每次取中间有可能也会达到最差性能**

![image-20250103172601011](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103172601011.png)

**辅助空间的复杂度最坏下也是 O(n) （因为递归层数是 O(n)）!!!**

~~~c
/* 快速排序 —— 教材版 partition（挖坑法）*/
int Partition(int A[], int low, int high) {
    int pivot = A[low];                     /* 用第一个元素当枢轴，坑位在 low */
    while (low < high) {
        while (low < high && A[high] >= pivot) high--;
        A[low] = A[high];                   /* 右边找到小的，填到左坑 */
        while (low < high && A[low]  <= pivot) low++;
        A[high] = A[low];                   /* 左边找到大的，填到右坑 */
    }
    A[low] = pivot;                         /* 相遇处就是枢轴的最终位置 */
    return low;
}

void QuickSort(int A[], int low, int high) {
    if (low >= high) return;                /* ★ 必须是 >=。原代码写的是 l == r，
                                               当 l > r 时不返回，会无限递归到栈溢出 */
    int p = Partition(A, low, high);
    QuickSort(A, low, p - 1);
    QuickSort(A, p + 1, high);
}

/* 时间：平均 O(n log n)，最坏 O(n^2)（每次枢轴都取到最值，比如序列已有序）
   空间：递归栈，平均 O(log n)，最坏 O(n)
   不稳定。
   改进：枢轴取"三数取中"（首、中、尾三者的中间值），避开最坏情况

   ★ partition 是 408 最值钱的一段代码 ——
   凡是"把序列分成满足某条件的两部分"（奇偶分离、找第 k 小、
   2016 集合划分、2022 找最小的 10 个），都是改它的两行 while 条件 */
~~~



## 3.选择排序

**key：一次交换涉及三次移动！！**

![image-20250103224726113](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103224726113.png)

 <font size=6 color = red> 选择排序原代码有问题！！！！！</font>

问题虽然可以排序成功但是效率极其低因为交换次数过多

**测试数据：**

5
64, 25, 12, 22, 11

**why :** 

~~~c
/* 简单选择排序：每趟从无序区【选】出最小的，放到有序区末尾 */
void SelectSort(int A[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;                        /* 先假定 i 就是最小的 */
        for (int j = i + 1; j < n; j++)     /* 在无序区里找真正最小的下标 */
            if (A[j] < A[min]) min = j;
        if (min != i) {                     /* ★ 一趟只交换一次 */
            int t = A[i]; A[i] = A[min]; A[min] = t;
        }
    }
}

/* 原代码写的是：
       for (i...) for (j = i+1...) if (a[j] < a[i]) swap(a[i], a[j]);
   这【不是】选择排序 —— 它每发现一个更小的就立刻交换，
   一趟里可能交换很多次，移动次数是 O(n^2) 而不是 O(n)。
   选择排序的特点恰恰是"比较多、移动少"，一趟最多换 1 次。
   （原代码里声明的 int min; 也一直没被用上）

   时间 O(n^2)，且与初始序列【无关】（比较次数固定 n(n-1)/2）
   空间 O(1)，不稳定 */

/* 这个内层循环单独拿出来，就是 O(n) 找最值的通用写法 —— 代码题里用得最多 */
int FindMin(int A[], int n) {
    int min = 0;
    for (int i = 1; i < n; i++)
        if (A[i] < A[min]) min = i;
    return min;                             /* 返回下标 */
}
~~~

 <font size=5 color =red > 正确写法 </font>

~~~c++
#include <iostream>
using namespace std;
int a [10];
int main()
{
    int n;
    cin >> n;
    int cn = 0; // 比较次数
    int mn = 0; // 移动次数
    
```c
/* 带比较/移动次数统计的版本（用来验证复杂度） */
void SelectSortCount(int A[], int n, int *cmp, int *mov) {
    *cmp = *mov = 0;
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++) {
            (*cmp)++;                       /* 比较一次 */
            if (A[j] < A[min]) min = j;
        }
        if (min != i) {
            int t = A[i]; A[i] = A[min]; A[min] = t;
            *mov += 3;                      /* 一次交换 = 3 次移动 */
        }
    }
}

/* 结论：
   比较次数恒为 n(n-1)/2，和初始序列无关
   移动次数最少 0（已有序），最多 3(n-1) —— 这是选择排序的最大优点 */
```
}
~~~



### 性能分析

![image-20240927221540776](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20240927221540776.png)

## 4.冒泡排序

每轮都从前往后以此比较相邻的两个数，逆序就交换

这里的一次交换也是 ==三次== 移动（temp 操作）

~~~c
/* 冒泡排序：相邻两个比较，逆序就交换 */
void BubbleSort(int A[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int flag = 0;                       /* 本趟有没有发生过交换 */
        for (int j = n - 1; j > i; j--)     /* 从后往前扫，小的往前"冒" */
            if (A[j] < A[j - 1]) {
                int t = A[j]; A[j] = A[j - 1]; A[j - 1] = t;
                flag = 1;
            }
        if (flag == 0) return;              /* ★ 一趟下来没换过 = 已经有序，提前结束 */
    }
}

/* 时间：最好 O(n)（已有序，靠 flag 提前退出），最坏/平均 O(n^2)
   空间 O(1)，稳定（相等时不交换）

   原代码把数组开成 int a[10] 却按输入的 n 来读，n > 10 就越界了 ——
   数组长度要么用宏定义开够，要么按题目给的上界开 */
~~~



## 5.堆排序

~~~c
/* 堆排序（升序结果 → 用【大根堆】）
   下标从 1 开始：结点 k 的孩子是 2k 和 2k+1 */
#define MaxSize 100010

/* 把以 k 为根、长度为 len 的子树调整成大根堆 */
void SiftDown(int A[], int k, int len) {
    A[0] = A[k];                                    /* A[0] 当暂存单元 */
    for (int i = 2 * k; i <= len; i *= 2) {
        if (i < len && A[i] < A[i + 1]) i++;        /* 取较大的那个孩子 */
        if (A[0] >= A[i]) break;                    /* 父亲已经最大，停 */
        A[k] = A[i];                                /* 孩子上移 */
        k = i;
    }
    A[k] = A[0];                                    /* 最后把暂存的值放到位 */
}

void BuildMaxHeap(int A[], int len) {
    for (int i = len / 2; i >= 1; i--)              /* 从最后一个非叶结点开始 */
        SiftDown(A, i, len);
}

void HeapSort(int A[], int len) {
    BuildMaxHeap(A, len);                           /* 建堆 O(n) */
    for (int i = len; i > 1; i--) {
        int t = A[i]; A[i] = A[1]; A[1] = t;        /* 堆顶（最大值）换到末尾 */
        SiftDown(A, 1, i - 1);                      /* 剩下的重新调整，长度减 1 */
    }
}

/* 时间 O(n log n)（建堆 O(n) + n 次调整 O(log n)），空间 O(1)，不稳定

   原代码实现的其实是"输出前 m 小的数"（小根堆 + 弹 m 次），
   不是完整的堆排序 —— 那种写法叫 Top-K，见下面的注 */

/* Top-K 的口诀（反直觉，别记反）：
   找前 k 个【最大】→ 建大小为 k 的【小】根堆，比堆顶大就顶掉堆顶
   找前 k 个【最小】→ 建大小为 k 的【大】根堆                        */
~~~



## 6.基数排序 (非比较排序算法)

​	**基数 ： 进制 e.g 二进制基数就是 2**

操作：逐位进行 ==分配== 和 ==收集==（从最低位开始 ，从最高的话比较复杂涉及 **递归处理**）

每个桶内部用链表（链式队列）这个数据结构存数据 （用数组的话会比较浪费空间）

**分配：**（按照位数 第一轮就是个位 ，第二轮就是十位 …… 以此类推）

 ![image-20250103164530664](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103164530664.png)

**收集**：
**枚举桶、从桶里拿出来收集成一个单链表！**

---

**效率：**

![image-20250103165218390](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103165218390.png)

![image-20250103165253057](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250103165253057.png)



---







## 7.直插排序 (移位赋值操作)



### 简单插入排序

操作：依次将每个元素插入到前面有序的部分当中

先拿当前元素和有有序区最后一个数进行比较 如果大于就无需排序直接加入有序区即可 如果小于呢 就把这个数先使用 temp 变量临时存起来 然后依次和有序区的每一个元素比较 

![image-20250105162033781](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105162033781.png)



移动次数除了比较的时候移动还有 当前元素移动到 temp 再从 temp 移动到插入的位置



![image-20250105162401059](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105162401059.png)



![image-20250105162522499](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105162522499.png)

~~~c
/* 直接插入排序（带哨兵）。A[0] 是哨兵，数据存在 A[1..n] */
void InsertSort(int A[], int n) {
    for (int i = 2; i <= n; i++)                /* A[1] 视为已有序，从 A[2] 开始 */
        if (A[i] < A[i - 1]) {                  /* 比前一个小才需要挪，否则原地不动 */
            A[0] = A[i];                        /* 存哨兵，否则后移时会被覆盖 */
            int j;
            for (j = i - 1; A[0] < A[j]; j--)   /* 边比边后移 */
                A[j + 1] = A[j];
            A[j + 1] = A[0];                    /* 插到位 */
        }
}

/* 哨兵的作用：内层循环的条件不用写 j > 0。
   因为 A[0] 就是待插入的值，走到 j == 0 时 A[0] < A[0] 为假，自然停下 ——
   省掉一次边界判断，这是"哨兵"这个技巧的全部意义

   时间：最好 O(n)（已有序，if 一次都不进），最坏/平均 O(n^2)
   空间 O(1)，稳定，可以用于链表 */
~~~

### 二分优化（a bit）

### 折半插入排序

对有序区进行折半查找

小于的话就 right = mid-1

大于等于的话就 left = mid+1

**直到 left 大于 right**

然后插入在 left 的位置



~~~c
/* 折半插入排序：用二分找插入位置，只减少【比较】次数，移动次数一点没少 */
void BInsertSort(int A[], int n) {
    for (int i = 2; i <= n; i++) {
        A[0] = A[i];                            /* 暂存 */
        int low = 1, high = i - 1;
        while (low <= high) {                   /* ★ 必须是 <=，且 low/high 都要动 */
            int mid = (low + high) / 2;
            if (A[mid] > A[0]) high = mid - 1;
            else                low = mid + 1;  /* ★ 相等时也往右，保证稳定 */
        }
        for (int j = i - 1; j >= low; j--)      /* 循环结束时 low 就是插入位置 */
            A[j + 1] = A[j];
        A[low] = A[0];
    }
}

/* 原代码的二分写成 while (l < r) 且 r = mid-1 / l = mid+1，
   区间收缩和终止条件对不上，会漏判边界；
   所以后面才不得不打一个补丁 if (a[l] > a[0]) l = 0; 硬掰回来。
   标准写法 while (low <= high) 结束后 low 天然就是插入位置，不用补丁

   时间：比较 O(n log n)，但移动仍是 O(n^2)，所以整体还是 O(n^2)
   空间 O(1)，稳定。
   ⚠ 因为要随机访问取中点，折半插入【不能用于链表】 */
~~~



## 8.希尔（shell）排序

**与开放寻址法的避免冲突类似都有一个增量**（Δ 变化量）

![image-20250105164405234](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105164405234.png)

**如图增量是 2！**

**优化的插入排序**

思路：

**增量依次折半**

![image-20250105164535770](https://raw.githubusercontent.com/kasahuki/os_test/main/img/image-20250105164535770.png)



~~~c
/* 希尔排序：按增量 d 分组，组内做直接插入排序，d 逐步缩小到 1 */
void ShellSort(int A[], int n) {
    for (int d = n / 2; d >= 1; d /= 2)             /* 增量序列，最后一趟 d 必须是 1 */
        for (int i = d + 1; i <= n; i++)
            if (A[i] < A[i - d]) {                  /* 和【同组】的前一个比 */
                A[0] = A[i];                        /* 这里 A[0] 只是暂存，不是哨兵 */
                int j;
                for (j = i - d; j > 0 && A[j] > A[0]; j -= d)   /* ★ j > 0 不能省 */
                    A[j + d] = A[j];
                A[j + d] = A[0];
            }
}

/* 和直接插入排序对比：把所有的 1 换成 d 就是希尔排序。
   区别在于这里 A[0] 不能当哨兵用（分组后走不到下标 0），
   所以内层循环必须显式写 j > 0

   时间：取决于增量序列，约 O(n^1.3)，最坏 O(n^2)
   空间 O(1)，【不稳定】（分组会让相等元素跨组跳跃）
   ⚠ 需要随机访问，【不能用于链表】 */
~~~





