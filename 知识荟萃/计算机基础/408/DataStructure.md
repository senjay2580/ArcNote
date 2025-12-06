<center> **<font color="red" size="28"> 数据结构 </font>** </center>



# 0、时间复杂度

## 1.频率最高的语句（执行深度最深的 /阶数最多的）

## 2. 语句执行次数和问题规模 n 的关系

## 3. 忽略常数

### 为什么O(1)的空间复杂度不是指空间的而是指辅助空间的？

当提到O(1)的空间复杂度时，通常指的是**辅助空间复杂度**为O(1)，即算法所需的额外空间是固定的，与输入规模无关。例如，一个仅使用几个变量的算法，其辅助空间复杂度为O(1)。

**注意**：如果输入数据本身占用O(n)空间，总空间复杂度为O(n)，但辅助空间复杂度仍为O(1)。

---



![image-20241017210952655](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017210952655.png)

![image-20250821220052977](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220052977.png)

**递归的时间复杂度：画树即可**

结点数就是时间复杂度 但如果每个结点里面也就是每个递归里还有嵌套的话就要看==多重循环==的解题思路

---



# 数组、矩阵存储和广义表



## 特殊矩阵的压缩存储

![image-20250109214904823](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109214904823.png)

分为按行优先和按列优先存储 

注意点 ： ==一维数组默认从 0 下标开始==

`array [n][m]` n 个数组（==0~n-1==），每个数组里都有 m（0 ~ m-1）个元素

![image-20241124175558277](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124175558277.png)

**行/列/页优先**



### ==对称矩阵== 的压缩存储



![image-20241124175822092](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124175822092.png)

**以……为顺序将 二维数组的一部分存储在一维数组当中**	

### 三角矩阵



![image-20241124180025625](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180025625.png)

**多一个就去存那个固定的 c 值**

![image-20241124181356800](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124181356800.png)

**c == 0 就是线性代数里比较特殊的上/下三角矩阵 **

###  对角矩阵

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180339303.png)

**以对角线的顺序存储**



### 稀疏矩阵

![image-20241124180403044](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180403044.png)

**密度小于 0.05 （非零元素少时）**

![image-20241124181712867](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124181712867.png)

![image-20241124181757465](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124181757465.png)

### 十字链表存储稀疏矩阵

![image-20241124181839495](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124181839495.png)

![image-20241124181929350](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124181929350.png)

![image-20241124182002045](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124182002045.png)



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

![image-20241124180457077](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180457077.png)



![image-20241124180545920](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180545920.png)

![image-20241230182154988](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241230182154988.png)

![image-20241124180625820](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180625820.png)

![image-20241124180728470](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241124180728470.png)

**三对角矩阵概念！**

![image-20241017211021475](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017211021475.png)



![825357dbaf9fecd541cf159647cf60a](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/825357dbaf9fecd541cf159647cf60a.jpg)

**m~ij~ 的 i j 取决于 按行/列优先存储**







# <font size=25 color=red> 一、链表 </font>

==增操作 ： 构建链表！==

## 顺序表（数组实现）：

> 使用数组，静态分配。

```c++
#include<iostream>
using namespace std;
#define max_size 10
typedef struct 
{
    int data[max_size];//顺序表最大长度
    int length;//顺序表当前长度
    
}Sqlist;
void init(Sqlist &l)//创
{
    
    l.length=0;//当前长度为0

    
}
void add(Sqlist &l,int x)//增
{
    l.data[++l.length]=x;
    
}
// void del(Sqlist &l,int idx)//删
// {
   
// }
void change(Sqlist &l,int idx,int x)//改
{
    l.data[idx]=x;//包含了查找
    
}
bool isEmpty(Sqlist &l)
{
    if(l.length)
    return 0;
    else
    return 1;
}
int main()
{
    Sqlist l;
     init(l);
     add(l,5);
     add(l,3);
     change(l,2,8);
     for(int i=1;i<=l.length;i++)
     cout<<l.data[i]<<' ';//查
     cout<<endl<<isEmpty(l);
     
     
}
```



## 链表（链式实现）

> 使用 new/malloc ，delete/free 动态分配内存空间！

### ==创+初始化==

~~~c++
typedef struct ListNode
{
    int val;
    ListNode *next;
    ListNode(): next(nullptr){}//无参构造
    ListNode(int x): val(x), next(nullptr){}//初始化
    
}*list;


 ListNode *a = new ListNode(-1);//a 是指针(地址)//创
    list b = new ListNode(2);
~~~

### 销毁链表

~~~c++
void destroyList(listNode *head) {
    while (head) {
        listNode *temp = head;
        head = head-> next;
        delete temp; // 释放节点内存
    }
}


~~~



### ==构建链表==

#### 头插法

~~~c++
void add_head(list &l, int x)//头插法  --> 栈--> 头节点就是栈顶
{
    ListNode *newnode = new ListNode(x);//新结点
    newnode-> next = l-> next;
    l-> next = newnode;
    
}
~~~

#### 尾插法

~~~c++
void add_tail(list &l, int x)//尾插法  
{
    ListNode *tail = l;//定义一个尾结点
    while(tail-> next!= nullptr)
        tail = tail-> next;//找到 end 位置(不是 null)
        
    ListNode *s = new ListNode(x);//创建新结点
    
    tail-> next = s;
    tail = s;//更新尾指针位置
        
    
    
}
~~~

#### 按指定位置插入新节点

~~~c++
void insert(list &l, int idx, int x)//在链表指定位置插入结点
{
    if(idx == 0)
    return ;  
    if(idx == 1)
    {
        add_head(l, x);
        return ;
    }
    list tmp = l;//步进结点, 替代原有的链表
    int pos = 0;
    ListNode *newnode = new ListNode(x);//创建新结点
  
    while(tmp!= nullptr)
    {
        if(pos == idx-1)//如果找到了前驱结点
        {
            newnode-> next = tmp-> next;
            tmp-> next = newnode;
            return ;
       
        }
        pos++;
     
        tmp = tmp-> next;
    }
    
}

~~~

### ==查找==

#### 按位查找

~~~c++
int query_value(list l, int x)//按位查找值
{
    int idx = 1;
 
    while(l!= nullptr)
    {
        l = l-> next;//不管头节点
        if(l == nullptr)//边界条件
        break;
        
       
        if(idx == x)
        return l-> val;
        idx++;
        
    }
    return -1;
    
    
}

~~~



#### 按值查找

~~~c++
int query_index (list l, int x)//按值查找, 不能加 list &l 防止步进时修改链表的头节点
{
    int pos = 1;//标记位置
    while(l!= nullptr)
    {
         l = l-> next;
         if(l == nullptr)//防止空指针访问异常
         return -1;
         
        if(l-> val == x)
        {
            return pos;
        } 
        pos++;
        
    }
    return -1;
    
}
~~~

### ==删除== 指定位置的结点

~~~c++
void del(list &l, int k)//删除第 k 个结点, 头节点表示第 0 个位置
{
   
    //特判
    if(k == 0)
    return ;//头节点不删
   
    
    list tmp = l;//步进结点, 替代原有的链表
    int pos = 0;
    while(tmp-> next!= nullptr)
    {
        if(pos == k-1)//找到了这个结点的前驱结点才删除
        {
           tmp-> next = tmp-> next-> next;  
           return ;
        }
        
         tmp = tmp-> next;
         pos++;
    }
    return ;
    
}
~~~

### ==判空&计算长度==

~~~c++
bool isEmpty(list l)
{
    if(l-> next == nullptr)
    return 1;
    else
    return 0;
    
}
~~~

~~~c++
int countLen(list l)//统计链表长度, 如果加了地址符链表当前头节点的位置就会变化
//如果不是修改原链表最好不要地址传参 或者可以用一个结点复制原  头结点 （反正有头节点就可以访问整个链表了）
{
    int len = 0;
    while(l!= nullptr)
    {
        l = l-> next;
        len++;
    }
    return len-1;
}
~~~

<font color='red' size=6>！！注意问题：不要随便移动初始的头节点（哨兵结点，固定，），要固定住，然后使用步进结点步进去遍历  。 遍历时要防止空指针异常，特判极端（极小极大/一般）边界情况 </font>

---



## ！循环链表(环形链表，！但指向 ==表头==)

###  ==循环单链表== 和 ==循环双链表== 

**<font size='16' color='red'> 循环是有<u>作用</u>的 </font>**

![image-20240924231426150](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231426150.png)

![image-20240924231442290](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231442290.png)

### **初始化：** ![image-20241013213720089](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013213720089.png)



![image-20241013213147658](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013213147658.png)

**删除也同理！**

![image-20240924231456953](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231456953.png)

![image-20240924231510937](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231510937.png)

![image-20240924231537034](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231537034.png)

![image-20240924231552815](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240924231552815.png)



> 可设置头尾指针（类似带头尾结点！

![Screenshot_2024-10-10-12-52-26-019_net.csdn.csdnplus](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/Screenshot_2024-10-10-12-52-26-019_net.csdn.csdnplus.png)



![image-20241013213814034](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013213814034.png)

![image-20241013213906802](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013213906802.png)

## <u>双链表（带头结点）</u>

### 创+初始化

~~~C++
//初始化（构造函数）
typedef struct bioListNode
{
    int val;
    bioListNode *next;
    bioListNode *prior;
    bioListNode(int x): val(x), next(nullptr), prior(nullptr){}
    
}*bioList;

//创
   bioListNode *a = new bioListNode(-1);
    bioListNode *b = new bioListNode(-1);
    a-> next = b;
    b-> prior = a;//初始化定义头结点和尾结点（都是不存真正的值的）
//这样 《头插法》 和 《尾插法》 就更容易了
~~~

### 在 p 结点之后插入 s 结点

~~~c++
void insert(bioListNode *p, bioListNode * s)//传入两个结点, 在 p 结点之后插入一个新的结点
{
    s-> next = p-> next;
    p-> next-> prior = s;
    s-> prior = p;
    p-> next = s;
}
~~~



### 双链表的删除（按位删除）

```cpp
void del(bioListNode *p) // 删除结点p
{
    if (p == nullptr) return;

    if (p->prior != nullptr) {
        p->prior->next = p->next;
    }
    if (p->next != nullptr) {
        p->next->prior = p->prior;
    }
    delete p;
}
```

### 双链表查找指定结点

#### 按值查找

~~~C++
bioListNode* find_by_value(bioList l, int value) {
    while (l != nullptr) {
        if (l-> val == value) {
            return l; // 找到值为 value 的节点
        }
        l = l-> next;
    }
    return nullptr; // 未找到值为 value 的节点
}
~~~

#### 按位查找

~~~C++
bioListNode* find_by_index(bioList l, int index) {
    int current_index = 0;
    while (l != nullptr) {
        if (current_index == index) {
            return l; // 找到索引为 index 的节点
        }
        l = l-> next;
        current_index++;
    }
    return nullptr; // 未找到索引为 index 的节点
}
~~~



### 双链表的遍历（可向 ==前== 也可向 ==后==）



![image-20250821220106630](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220106630.png)



# basic：==数组== 的缺陷和链表的区别

~~~C++
#include <iostream>
using namespace std;
const int N = 1e3+10;
#define Maxsize 20
int a [N];

typedef struct sqlist
{
  int data [Maxsize];
  int length;
  
};

void init(sqlist &l)//初始化
{
    l.length = 0;
    for(int i = 0; i < l.length; i++)l.data [i] = 0;
    
}
void insert(sqlist &l, int k, int x)//在指定位置插入元素
{
    l.length++;
    if(l.length >= Maxsize)
    return ;
    for(int i = l.length; i > k; i--) l.data [i] = l.data [i-1];
    l.data [k] = x;
    
}
void del(sqlist &l, int k)//在指定位置删除元素
{
    if(k >= l.length)
    return ;
    for(int i = k; i < l.length-1; i++)l.data [i] = l.data [i+1];
    l.length--;
       
       
    
    
}
void print(sqlist l)
{
    for(int i = 0; i < l.length; i++)cout << l.data [i] <<' ';
    cout << endl;
}
int main()
{
    sqlist l;
    init(l);
    insert(l,0,5);
    insert(l,0,8);
    insert(l,1,9);
    insert(l,2,9);
    print(l);
    del(l,2);
    print(l);
    cout << l.length;
    
    
    
    return 0;
}
~~~



## 应用 ： 多项式的 -存储-  &&  多项式的 -相加-





~~~C++
~~~





---





~~~C++
~~~







---

# 二、栈与队列

---



## 栈

### 顺序栈

~~~c++
#include <iostream>
using namespace std;
const int maxsize = 25;
typedef struct 
{
    int val [maxsize];
    int top;//栈顶指针
    
}stack;
void init(stack &st)//初始化
{
    st.top = 0;//表示没有元素
    for(int i = 0; i <= maxsize; i++)
        st.val [i] = 0;
}
void add(stack &st, int x)//增
{
    st.val [++st.top] = x;
}
void pop(stack &st)
{
    st.val [st.top--];
}
bool isEmpty(stack st)
{
    if(! st.top)return 1;
    else return 0;
}
int countLen(stack st)
{
    return st.top;
}
void print(stack st)
{
    while(st.top)
    cout << st.val [st.top--] <<
{
    stack st;//创 " ";
    
}
int main()
    init(st);
    add(st,8);
    add(st,5);
    add(st,6);
    add(st,4);
    add(st,6);
    add(st,3);
    pop(st);
    cout << st.val [st.top];//查
    cout << endl << countLen(st)<< endl;
    print(st);
    // (3) 6 4 6 5 8
    
    return 0;
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

![847e1b809704afe7753aa9ed6cf31c3](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/847e1b809704afe7753aa9ed6cf31c3.jpg)



![74faa91f7c6b97c09701cd0ae5542e5](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/74faa91f7c6b97c09701cd0ae5542e5.jpg)





##  表达式求值 





**结合队列可求杨辉三角！**

~~~C++
#include <iostream>
#include <stack>
#include <unordered_map>
using namespace std;
stack <char> op;
stack <int> num;
unordered_map <char,int> h{{'+',1},{'-',1},{'/',2},{'*',2}};
void eval()
{
    int num1 = num.top();
    num.pop();
    int num2 = num.top();
    num.pop();//注意要弹出
    char c = op.top();
    op.pop();
    int ans = 0;
    if(c =='+')ans = num1+num2;
    if(c =='-')ans = num2-num1;
    if(c =='/')ans = num2/num1;//注意栈是倒着存的
    if(c =='*')ans = num1* num2;
    num.push(ans);


    
}
int main()
{
    string s;
    cin >> s;
    for(int i = 0; i < s.size(); i++)
    {
        if(s [i] >='0'&&s [i] <='9')
        {
            int x = 0, j = i;
            while(j <s.size()&&(s[j]> ='0'&&s [j] <='9'))
            {   
                x = x*10+s [j]-'0';
                j++;
            }
           
            num.push(x); 
            i = j-1;
        }
        else if(s [i] =='(')
            op.push(s [i]);
            
        else if(s [i] ==')')
        {
            while(op.top()!='(')//这里不用判空
            {
                eval();
            }
            op.pop();
        }
        else
        {
            while(op.size()&&h [s[i]]<= h [op.top()])
            eval();//要判空 （特判！）
            
            op.push(s [i]);
        }
        
    }
    while(op.size())eval();
    
    cout << num.top();
    return 0;
    
    
}
~~~

#### 注意点：

**判空 扫尾操作  双指针闪现（防止延迟！）**



#### 栈与递归

**最外层的调用也算的！！！**



![image-20250821220112619](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220112619.png)

---



## 队列

> ### 带头结点

> 这里讨论的是只可队尾插入队头弹出的队列（非 真·双端队列和 `假·双端队列`）

#### 初始化 （利用结构体的嵌套）

~~~c++
#include <iostream>
using namespace std;
typedef struct ListNode// 结点结构体 --> 结构体变量 里面存有 int 值还有一个 next 指针（地址）
{
    int val;
    ListNode *next;
    ListNode(int val)
    {
        this-> val = val;
        this-> next = nullptr;
    }//初始化
};

typedef struct 
{
   ListNode *front,* rear;//有两个结点结构体，里面存有 next 指针（地址）和值
}listQueue;
int main()
{
    //创建带头节点的链队
    listQueue l;//l 是个 结构体对象 不能使用-> 来引用！
   l.front = l.rear = new ListNode(-1);
    return 0;
}
~~~



<font size=25 color=red> 这个头指针是不存值的（也即是带头节点）--> 与以上同理 </font>

<font size=25 color=red> **结点结构体正常搞** </font>

<font size=25 color=red> **给链队设置头尾指针** 这样可以访问到头尾元素 </font>



#### 入队 (使用尾插法)

~~~c++
void add_tail(listQueue &l, int x)//尾插法
{
    ListNode *newNode = new ListNode(x);
    l.rear-> next = newNode;
    l.rear = newNode;
    
}
void print(listQueue l)
{
    ListNode *head = l.front-> next;
    while(head!= nullptr)
    {
        cout <<head-> val <<"--> ";
        head = head-> next;
    }
    cout << "NULL";
    cout << endl;
}
~~~

#### 出队（头删法）

~~~c++
void pop_front(listQueue &l)
{
    
    ListNode *head = l.front;
    if(head-> next == nullptr)return ;
    head-> next = head-> next-> next;
}
~~~

#### 判空

~~~C++
bool isEmpty(listQueue l)
{
    if(l.front == l.rear)return 1;
    else return 0;
    
}
~~~

#### 打印

~~~C++
void print(listQueue l)
{
    ListNode *head = l.front-> next;
    while(head!= nullptr)
    {
        cout <<head-> val <<"--> ";
        head = head-> next;
    }
    cout << "NULL";
    cout << endl;
}
~~~



#### 双端队列（两端都可进出）

~~~c++
// void pop_rear(listQueue &l)//尾删法
// {
//     ListNode *tail = l.rear;
    
    
// }


void add_head(listQueue &l, int x)//头插
{
    ListNode *head = l.front;
    ListNode *newNode = new ListNode(x);
    newNode-> next = head-> next;
    head-> next = newNode;
}

~~~

#### 单调队列

~~~c++
#include <iostream>
#include <deque>
using namespace std;
const int N = 1e6+10;
int a [N];
int n, k;
int main()
{
    cin >> n >> k;
    for(int i = 1; i <=n;i++)cin> > a [i];
    deque <int> q;
    //找最小值
   for(int i = 1; i <= n; i++)//枚举每一个点
    {
        //i 起码要大于窗口长度
       if(i > k&&a [i-k] == q.front())q.pop_front();//如果滑出窗口的话（一定要保证窗口元素个数不大于 k）
       
       while(q.size()&&a [i] < q.back())q.pop_back();
        q.push_back(a [i]);
       
        if(i >= k)
        cout << q.front()<<' ';
        
    }
    cout << endl;
    q.clear();
     for(int i = 1; i <= n; i++)//枚举每一个点
    {
        while(q.size()&&a [i] > q.back())q.pop_back();
        q.push_back(a [i]);//队列存值
        //若队头滑出了窗口，则弹出队头，保持窗口的元素在 k 之内
        if(i-k >= 1&&a [i-k] == q.front())
        q.pop_front();
        
        //窗口形成
        if(i >= k)cout << q.front()<< " ";
        
        
    }
    
    return 0;
}
~~~



==**存下标**==

~~~C++
 for(int i = 1; i <= n; i++)
    {
        //不可 q.size()>= k
        if(i > k&&i-k == q.front())q.pop_front();
        while(q.size()&&a [q.back()] > a [i])q.pop_back();
        q.push_back(i);
        if(i >= k)cout << a [q.front()] <<' ';
    }
~~~

#### 循环队列

**% mod 操作就是对于环也就是圆圈（钟）轮转**

~~~C++
#include <iostream>
using namespace std;
#define max_size 100
// typedef struct cq //如果此处写了下面一定要写 根据 c++版本决定要不要 写 考研看清楚是什么版本的
// {

// }circular_queue;
typedef struct 
{
  int data [max_size]; // 循环队列只能用数组！！！！
  int front;
  int rear;// 表示数组下标

}circular_queue;
void init (circular_queue *q)
{
  q-> front = q-> rear = 0; // 头尾一开始都指向空（自己留一个空的空间）
}
bool isEmpty(circular_queue *q)
{
  if(q-> front == q-> rear)
    return 1;
  else
    return 0;

}
bool isFull(circular_queue *q)
{
  if((q-> rear+1)%max_size == q-> front)
    return 1;
  else 
    return 0;

}
int dequeue(circular_queue *q)
{
  int x;
  if(isEmpty(q))
    return 0;
  else
  {
    x = q-> data [q-> front];
    q-> front =(q-> front+1)%max_size;
  }
  return x;


}
bool enqueue(circular_queue *q, int x)
{
  if(isFull(q))
    return 0;
  else
  {
    q-> data [q-> rear] = x;
    q-> rear =(q-> rear+1)%max_size;

  }
  return 1;

  
}
void print(circular_queue *q)
{
  while(! isEmpty(q))
  {
    cout << dequeue(q)<<' ';
  }
}
int main()
{
  circular_queue q;
  init(&q);
  int n;
  cin >> n;
  for(int i = 0; i < n; i++)
  {
    int x;
    cin >> x;
    enqueue(&q, x);
  }
  print(&q);
  cout << q.data [q.front] << " " << q.data [q.rear-1]; //输出队头和队尾

  return 0;
}
~~~

![image-20241015132005982](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015132005982.png)

![image-20241015132014127](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015132014127.png)

**图 1and  3 是空位不同的循环队列**

**图 2 是判断队列的长度！！！** 

![image-20250109213857935](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109213857935.png)

启示：对这个数据结构进行操作/判断时注意这个数据结构此时状态的==可能性==）——联系韦恩图

![image-20250109214217313](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109214217313.png)

# 三、串（String）

## 数组和指针基础

~~~c++
#include <iostream>
using namespace std;
void print(int arr []) // 等价 print(int *arr)
{
  cout << arr [1]; // 等价*(arr+1)
  // 数组的 【】 就是 解引用  也就是 *
  
}
int main ()
{
  int a [2] ={1,5};
  print(a);
  return 0;
}
~~~

arr 就是 ==首地址== *arr 首地址的* *解引用**

应用：

~~~c++
//**** **** *** 密码子查找（依据密码子 codon []，确定氨基酸 AA [] *** **** ****//
void SearchCodon(char codon [], char AA []){
//**** **** **** **** **** **** **** *****//
	for(int i = 0; i < 64; i++)
	{
		if(strcmp(codonTable [i][0], codon) == 0) // 为什么不能 codonTable == codon
		{
            //int strcmp(const char *str1, const char * str2);
			strcpy(AA, codonTable [i][1]);  
			return ;
		}
		strcpy(AA, "unknown"); // char *strcpy(char * dest, const char *src);
        // strcpy 函数会将源字符串 src 的内容复制到目标字符串 dest 所指向的位置，直到遇到源字符串的空字符 \0（字符串结束标志）为止。它返回指向目标字符串 dest 的指针。
		
	}
    
    // SerachCodon(codon, AA);
    // 函数调用
    // char codon [3], AA [3];
~~~



 

![image-20240925153840008](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925153840008.png)

**如果经常用到拼接（长度经常扩展变化）就要使用动态存储结构！**

![image-20240925153922279](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925153922279.png)

==清空串和销毁串不一样，前者内存空间中还有剩余，后者不是；==

####  1.串的比较

![image-20240925154140041](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154140041.png)

> **`按照字典序排序优先看每个字母，如果前缀都一样就要看长度！`**

拓展：采用不同的编码方式，每个字符所占空间不同，考研中只需默认每个字符占 ==1B== 即可



#### 2.串的顺序存储

![image-20240925154440498](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154440498.png)

**销毁这个串： free 释放内存空间！**

![image-20240925154450549](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154450549.png)

**==如果用数组空间去存的话，一个空间是一字节，一字节的空间只能存 0-255（整型）==**

![image-20240925154455828](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154455828.png)

![image-20240925155500570](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925155500570.png)

#### 3.串的链式存储



![image-20240925154500645](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154500645.png)



#### 4.串的基本操作

##### (1) 截取子串

![image-20240925154506513](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154506513.png)

##### (2) 比较字符串

![image-20240925154515710](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154515710.png)

##### (3) 索引字符串



![image-20240925154526505](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240925154526505.png)

##### (4)其他

判空：length

拷贝：遍历赋值

清空：令 length = 0；

~~~c++
#include <iostream>
using namespace std;
typedef struct StringNode
{
    char val [4];
    StringNode *next;
    StringNode(char c)///构造函数
    {
        val [0] = c;  // 初始化第一个字符
        val [1] = '\0';  // 确保字符串终止符存在
        val [2] = '\0';  // 初始化其余字符为终止符
        val [3] = '\0';  // 初始化其余字符为终止符
        next = nullptr;
    }
    
    
}*Sstring;

void print(StringNode *s)
{
    while(s!= nullptr)
    {
        cout <<s-> val [0];
        s = s-> next;
        
    }

~~~





#### 注意点

~~~c++
// StringNode * catString(StringNode * a, StringNode *b)//拼接字符串
// {
    
//     StringNode *res = new StringNode('#');
//     StringNode *cur = res;
   
//   while(a!= nullptr)
//   {
//       cur-> next = a;
//       a = a-> next;
//       cur = cur-> next;
//   }
//   while(b!= nullptr)
//   {
//       cur-> next = b;
//       b = b-> next;
//       cur = cur-> next;
//   }
//   return res-> next;//传回地址
    
// }
StringNode * catString(StringNode * a, StringNode *b) {
    // 创建一个新的头节点
    StringNode *res = new StringNode('#');
    StringNode *cur = res;

    // 遍历 a，复制节点
    StringNode *tempA = a-> next; // 跳过 a 的头节点
    while (tempA != nullptr) {
        cur-> next = new StringNode(tempA-> val [0]); // 创建新节点
        cur = cur-> next;
        tempA = tempA-> next;
    }

    // 遍历 b，复制节点
    StringNode *tempB = b-> next; // 跳过 b 的头节点
    while (tempB != nullptr) {
        cur-> next = new StringNode(tempB-> val [0]); // 创建新节点
        cur = cur-> next;
        tempB = tempB-> next;
    }

    return res; // 返回新的链表
}
~~~



~~~C++

int main()
{
    int n;
    cin >> n;
    StringNode *a = new StringNode('#');//初始化 创造一个字符串
    
    for(int i = 0; i < n; i++)//存住字符串
    {
        char c;
        cin >> c;
        StringNode *tmp = new StringNode(c);//创建一个结点
        a = append(a, tmp);
       
    //   输入 c b g f  
    }
    StringNode *b = new StringNode('j');
    StringNode *ans = catString(a, b);
    
    print(a);
    //如果按照注释那样会使得 a 为 cbgfj
    return 0;
}
~~~

> **返回字符串基本都是带#头节点的和单链表统一！！**
>
> ##### 如果按照注释那样会使得 a 为 cbgfj

## BF 算法（暴力匹配）

![image-20241017200841618](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017200841618.png)

直接使用双重循环

或是双指针

![image-20241017200920166](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017200920166.png)

### 时间复杂度分析

![image-20241017200939277](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017200939277.png)





# 四、KMP 算法

> 主要就是前缀数组 next

~~~C++
#include <iostream>
const int N = 1e5+10, M = 1e6+10;
char p [N], s [M];
int n, m;
int ne [N];
using namespace std;
int main()
{
    cin >> n >> p+1 >> m >> s+1;
    //构造 ne 数组
    for(int i = 2, j = 0; i <= n; i++)
    {
        while(j && p [i]!= p [j+1])j = ne [j];
        if(p [i] == p [j+1])j++;
        //while if 不可替换位置
        ne [i] = j;
    }
    for(int i = 1, j = 0; i <= m; i++)
    {
        while(j&&s [i]!= p [j+1])j = ne [j];
        if(s [i] == p [j+1])j++;
        if(j == n)
        {
            cout << i-n << " ";
            j = ne [j];//？
        }
    }
    return 0;
}
~~~



# 五、树



![image-20250109215214848](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215214848.png)



<span style="color:#FF00FF; font-size:1.9em;">x>=h h如果不是整数 那么就是向上取整h 小于等于的话就是向下取整</span> 



![image-20250104215224421](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104215224421.png)



![image-20250104215228606](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104215228606.png)



注意区分树的总度数（每个结点的分支数）和图的度数（离散数学握手定理） 不要搞混了

**总度数** 就是边的总数 就是结点的孩子结点的总和**n-1**







## SUM

![image-20240929191740657](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240929191740657.png)

## ==树的存储结构==

### 1、双亲表示法



![image-20240929191601508](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240929191601508.png)

**增**：无需按照层序插入新结点



**删除结点**：

有 **两种** 方案 ，**第一种** 使双亲指针设置为-1  

第二种将尾部数据移到该位置将其覆盖！！（good）



缺点 ： 如果删除的不是叶子结点的话就会有问题 ，因为要删除儿子结点，这就涉及到了查询操作，

所以要 **从头开始遍历**，如果用第一个删除，还要判断这个无效数据，就更慢了



### 2、孩子表示法（邻接表）--> hash 表&树/图的存储

[hash 表](#十五、哈希表(散列查找))

**就是邻接表！！！**

### **<font color=red size=25> 3、孩子兄弟表示法 </font>**

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240929193349960.png" alt="image-20240929193349960" style="zoom:150%;" />



#### 初始化

~~~c++
//左第一个儿子
//右兄弟
typedef struct CSNode
{
    int val;
    CSNode * firstSon, rightBrother;//层次不一样！！ 类比 leftchild 和 rightchild
    // key ---> 关键是针对非叶子结点
    
}*CSTree;
~~~

树与森林都可以转化为二叉树 然后操作就如 [二叉树](#二叉树)

## 树与二叉树的转化

![image-20250821220121022](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220121022.png)







## 森林和二叉树的转化

![image-20241017201857035](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017201857035.png)



![image-20241017202042876](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017202042876.png)

## SUM



![image-20241017202110296](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017202110296.png)

### 树的遍历

#### 先根遍历

**第一次经过就访问！**



![image-20241017203219748](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203219748.png)

#### 后根遍历

**最后一次经过才访问**

![image-20241017203304337](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203304337.png)

**等效于二叉树的中序遍历**

#### 层次遍历

![image-20241017203331994](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203331994.png)

**先根后根都是 dfs**

**层次是 bfs**





### 森林的遍历

#### 先序遍历

![image-20241017203434814](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203434814.png)

#### 中序遍历

![image-20241017203438865](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203438865.png)

![image-20241017203442009](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203442009.png)

**以下为等效遍历**

### SUM



![image-20241017203448919](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017203448919.png)

**问题：如何使用代码将森林和树转化为二叉树！**

Todo：

~~~C++
#include <iostream>
using namespace std;

struct Tree {
    int data;
    Tree *first_child;  // 第一个孩子
    Tree *self_bro;     // 兄弟节点

    // 构造函数
    Tree(int x) : data(x), first_child(nullptr), self_bro(nullptr) {}
};

// 添加孩子节点
void addChild(Tree *parent, int x) {
    Tree *newNode = new Tree(x);
    
    // 如果 parent 还没有孩子，就直接添加为第一个孩子
    if (parent-> first_child == nullptr) {
        parent-> first_child = newNode;
    } else {
        // 如果已经有孩子，找到最后一个兄弟节点，将新节点作为它的兄弟
        Tree *child = parent-> first_child;
        while (child-> self_bro != nullptr) {
            child = child-> self_bro;
        }
        child-> self_bro = newNode;
    }
}

// 前序遍历树（孩子兄弟表示法）
void preOrder(Tree *root) {
    if (root == nullptr) return;

    // 打印当前节点
    cout << root-> data << " ";

    // 先递归遍历第一个孩子
    preOrder(root-> first_child);
    
    // 再递归遍历兄弟节点
    preOrder(root-> self_bro);
}

int main() {
    // 创建根节点
    Tree *root = new Tree(1);
    
    // 添加子节点和兄弟节点
    addChild(root, 2);  // 2 作为 1 的孩子
    addChild(root, 3);  // 3 作为 1 的孩子的兄弟
    addChild(root, 4);  // 4 作为 1 的孩子的兄弟
    
    // 给 2 节点添加孩子
    addChild(root-> first_child, 5);   // 5 作为 2 的孩子
    addChild(root-> first_child, 6);   // 6 作为 5 的兄弟
    addChild(root-> first_child, 7);   // 7 作为 6 的兄弟

    // 前序遍历树，验证结构
    cout << "Pre-order traversal of the tree: ";
    preOrder(root);
    cout << endl;

    return 0;
}
~~~



## ==二叉树==

![image-20250109215318637](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215318637.png)

**二叉树的遍历顺序就是 以根结点为基准 然后 左优先**

### 完全二叉树

### 判断是否是完全二叉树

**使用 bfs 存 存第一个 NULL（也可以存别的东西等效替代 如正无穷） 如果 null 之后队列还有数的话就说明不是完全二叉树！！**

![image-20241017163824454](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017163824454.png)

### ==顺序存储==

#### 初始化

~~~C++
//tree []
//Size
    int n;
    cin >> n;
    Size = n;
    for(int i = 1; i <=Size;i++)cin> > tree [i];//构造
~~~

#### 求树的深度

~~~c++
int dfs(int u)//返回树的深度
{
    if(u*2 > Size)
    return 1;
     height = dfs(u*2)+1;//符合 完全二叉树/满二叉树
    //max(dfs(u *2), dfs(u* 2+1))+1;//普通树
    
    return height;
 
}
~~~

#### 求树的遍历顺序

~~~C++
void trace(int u)//输出递归路线
{
    if(u*2 > Size)//当到达树的叶子结点时
    {
        cout << u <<' ';
        return ;
    }
    
    cout << u <<' ';//到达每一层的操作
    
    trace(u*2);
    //返回后做操作
    trace(u*2+1);
    //返回后做操作
    
}

//OR---------------------------------------------------------------------------------------------------

 void trace(int u)//输出递归路线
{
    if(u > Size)return ;//溢出深度时
    
    cout << u <<' ';
    
    trace(u*2);
    //返回后做操作
    trace(u*2+1);
    //返回后做操作
}
   
~~~

### ==链式存储==

#### 初始化

~~~C++
typedef struct listTreeNode
{
    int val;
    listTreeNode *lchild;
    listTreeNode *rchild;
    
    listTreeNode(int x): val(x), lchild(nullptr), rchild(nullptr){}
    
}*ListTree;
~~~



#### 构造树（bfs）

~~~C++
//利用 层序遍历 构造完全二叉树(bfs)
void creatNode(int x, listTreeNode *l)//传入根节点
{
    queue <listTreeNode*> q;
    q.push(l);//让根结点入队
    listTreeNode *newNode = new listTreeNode(x);
    
    while(! q.empty())//队列不空
    {
     auto t = q.front();//提取队头
     q.pop();//弹出队头
     //寻找当前队头的邻居，并加入队列
    if(t-> lchild!= nullptr) q.push(t-> lchild);
    else 
    {
        t-> lchild = newNode;
        return ;
        
    }
    
    if(t-> rchild!= nullptr)q.push(t-> rchild);
    else 
    {
        t-> rchild = newNode;
        return ;
        
    }
    
    }
  
}
~~~

#### 前序遍历

~~~C++
void trace(ListTree t)
{
    if(t == nullptr)
    return ;
    
   cout <<t-> val <<' ';//visit(u)
   
    trace(t-> lchild);
  
    trace(t-> rchild);
      
    
}
~~~

#### 计算深度

~~~C++
int height(listTreeNode *l)
{
    if(l-> lchild == nullptr)
    return 1;
    
    return height(l-> lchild)+1;
    
}
~~~



#### 测试数据

~~~c++
int main()
{
    int n;
    cin >> n;
    listTreeNode *l = new listTreeNode(0);
    for(int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        if(i == 0)
        {
         l-> val = x;   
         continue;
        }
        
        
        creatNode(x, l);
        
    }
    trace(l);
    
    
    
    return 0;
}
~~~

## 树的前序/中序/后序遍历 构建树

![image-20250109215404348](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215404348.png)



![ed920753c7a08a17beb24f10c9edb5c](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/ed920753c7a08a17beb24f10c9edb5c.jpg)

**在先/后 序列找根结点 然后回到中序找左右子树 各对左右子树再找根结点**



---



## 树的非递归形式输出前序/中序/后序遍历序列

![image-20241206142828150](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241206142828150.png)

~~~c++
#include <iostream>
using namespace std;
// global
typedef struct biotree
{
    char data;
    biotree *lc;
    biotree *rc;
    biotree(char val): data(val), lc(nullptr), rc(nullptr){};
    
};
biotree* createTree() //返回从根节点开始的整棵树
{
    char c;
    cin >> c;
    if(c == '#')
        return nullptr;
    else
        {
            biotree *newnode = new biotree(c);
            newnode-> lc = createTree(); // 利用返回值连接 --》 思考
            newnode-> rc = createTree();
            return newnode;
            
        }
}

void middleTraveler(biotree *root)
{
    
    if(root == nullptr)
    return ;
    
    int top = -1;
    biotree *nodestack [100];
    // 先将根节点弹入栈顶
    biotree *p = root;
    while(p || top >= 0)
    {
        if(p)
        {
            nodestack [++top] = p;
            p = p-> lc;
            // 优先往左边找
        }
        else // 如果当前结点的左边是空（说明已经是最左边的一个了）就到当前结点的右边
        {
          cout <<nodestack[top]-> data <<' ';
          p = nodestack [top--]-> rc; // 再去右子树中找最左边的结点
          
        }
    }
}
int main()
{
    
    
    biotree *root = createTree();
    middleTraveler(root);
    
  
    
    return 0;
}
~~~

**输入：ABC#D##E##FG##H## （==前序==）**
**输出：C D B E A G F H  （==中序==）**

存到栈里就相当于是进入 ==递归下一层==



 <font size=6 color =red > **弹出栈就是返回上一层** </font>

**旧知识推新知识非常重要**





## 线索二叉树

**启示：做完一道检验所有选项不要无脑看到关键词就上起码要所有选项看过去 思路要清晰画图**

![image-20250109220859790](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109220859790.png)

### 	线索二叉树的中序/前序/后序遍历序列

 <font size=5 color =red > n 个结点的完全二叉树 的空链域为 n+1 条 </font>

**分别分析 n 奇数偶数的情况即可**！！！！

**前驱和后继 是基于 遍历序列决定的！**

​	![image-20241110190454478](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110190454478.png)

### 问题 ：如果从某个节点开始能否开始中序遍历整颗二叉树？

![image-20241110190859359](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110190859359.png)

## 中序~线索二叉树的存储

利用 ==左右指针的空链域== 来存储线索 

**特别地 使用 ltag 和 rtag 来标明是否是线索**

![image-20241110190938336](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110190938336.png)

**左前右后**

**==指向前驱和后继的指针就是线索==**

![image-20241110191122369](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191122369.png)

![image-20241110191135518](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191135518.png)

### 找中序前驱

#### 土方法：





![image-20241110191154758](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191154758.png)

==**轮序迭代**==

#### 线索化查找：

**要处理最后一个结点的后继 因为 每个结点的后继处理都是利用 pre 指向 q（当前结点） 但是当 q == null 就停止了 所以要单独对 pre（最后 pre 和 q 同指向 也就是都指向最后一个结点）**  

### 中序线索化：



![image-20241110191321314](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191321314.png)

### 

![image-20241110191324208](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191324208.png)

### 先序线索化

**主要问题**：左指前 要先判断 ==是不是线索== 非线索再继续遍历！

**为什么就先序因为先序的左孩子结点已经确定前驱了 所以如果不判断就又回去了！！**



![image-20241110191358251](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191358251.png)

![image-20241110191401045](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191401045.png)



### 后序线索化： post- 前缀 就是后的意思





![image-20241110191435896](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191435896.png)

# ==《通过线索二叉树找前驱/后继》==



### 找中序后继：

Xtag = 0 就说明一定是不是空链域 ，说明一定有孩子！

![image-20241110191643405](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191643405.png)

![image-20241110191752039](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191752039.png)

### 找中序前驱：



![image-20241110191808466](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191808466.png)

![image-20241110191814016](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191814016.png)

### 找先序后继：



![image-20241110191825685](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191825685.png)

### 找先序前驱:

![image-20241110191839090](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191839090.png)

### 找后序前驱：

![image-20250821220130213](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220130213.png)

### 找后序后继：



![image-20241110191904128](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191904128.png)

![image-20241110191916949](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241110191916949.png)















## 哈夫曼树 （特殊二叉树）

**哈夫曼树中不存在度为 1 的节点，即每个节点要么是叶子节点，要么有两个子节点**。

### WPL 概念

 WPL   （**总的**） 是指树中所有叶子节点的带权路径长度之和。==带权路径长度== 是指从 **根节点到某个叶子节点的路径长度（即经过的边数）** 乘以 ==该叶子节点的权重==。

![image-20250103150550008](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103150550008.png)

### 代码实现

![image-20250103154747067](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103154747067.png)

![image-20250103154758733](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103154758733.png)

![image-20250103154808449](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103154808449.png)

~~~C++
~~~

![image-20250103153625506](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103153625506.png)

### SUM



![image-20241017211415016](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017211415016.png)

## trie 树（拓展）

~~~C++
~~~



# 六、并查集

![image-20241009203612672](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009203612672.png)

## 简单方法

~~~C++
#include <iostream>
using namespace std;
//----------------------------------------------------------------------
#define size 13 //初始化结点个数
int UFset [size];//节点编号
int val [size];//结点值 
//------------------------------------------------------------------------field
int find(int s [], int x)//返回 x 所属的根节点
{
    while(s [x] >= 0) x = s [x];
    return x;
    
}

void Union(int s [], int root1, int root2)//合并集合
{
    if(root1 == root2)return ;
    else s [root1] = root2;
    
}
//---------------------------------------------------------------------function
int main()
{
    int n;
    cin >> n;
    
    for(int i = 0; i < size; i++)UFset [i] =-1;//只有 s [x] 是 -1 的才是 根结点 ---initialize
    for(int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        val [i] = x;//--------------------//赋值（assignment）
    }
    
    cout << val [find(UFset,4)] << endl;//一开始都是离散的点根节点都是本身
    
    Union(UFset, find(UFset,0), find(UFset,1));
    Union(UFset, find(UFset,1), find(UFset,2));
    Union(UFset, find(UFset,3), find(UFset,4));
    if(find(UFset,3)== find(UFset,2))cout << 1;
    else cout << 0;

    
    
    return 0;
}
~~~

**==缺点==： union 操作有可能会使大树合并到小树上导致树的深度增加，导致下次 find 时要耗费很长时间**

## 时间复杂度：

union 内部操作为 O(1)（前提是已经查到了 root）;

而一次 find 操作最差情况的时间复杂度 是 O(n) 在 n 个结点且深度刚好为 n 的情况下、

---



## 优化 union

**==主要思路==：  就是将小树并到大树上避免树的深度越来越深**

**操作：让 s [root] 不存-1 而是存 -（该 root 树下面的结点数包括自身）**

~~~C++}
void Union(int s [], int root1, int root2)//优化
{
    if(root1 == root2)return ;
    
    if(s [root2] < s [root1])//注意是负数
    {
       
        s [root2]+= s [root1]; 
        s [root1] = root2;
    }
    else
    {
        // s [root2] = root1;
        s [root1]+= s [root2]; w
        s [root2] = root1;
        //注意顺序问题
    }
    
}
~~~

最坏时间情况为 O(logn)

## （压缩路径）

~~~C++
int find(int x)//找到编号为 x 的结点的根节点
{
    if(x!= p [x])
        p [x] = find(p [x]);
        
        //return x; 不能
         return p [x];
        
}
//p【root】= root
~~~

时间复杂度 为 O (logn)

**递的过程找到根结点**

**归的时候让所有结点指向根结点**

![image-20241009211307951](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009211307951.png)



![image-20241009211933606](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009211933606.png)

## ’终极‘优化（不是按深度来比较的！）

**而是按结点总数来比较的！**

**结合压缩路径和小树合并到大树！**

（按 size 结点大小）

~~~C++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int p [N];
int find(int x)
{
    return p [x] >= 0?p [x] = find(p [x]): x;
}

int main()
{
  int n;
  cin >> n;
  
  for(int i = 1; i <= n; i++)p [i] =-1;//只有根的 p [root] 才是负数 并且绝对值等于这个集合的结点数

  int u;
  cin >> u;
  while(u--)//并 主要是在这个操作优化
  {
    int a, b;
    cin >> a >> b;
    int pa = find(a);
    int pb = find(b);
    if(pa == pb)
    continue;
    if(p [pa] < p [pb])//注意负数
    {
       
        p [pa]+= p [pb];
         p [pb] = pa;
    }
    else
    {
      p [pb]+= p [pa];
       p [pa] = pb;
    }
  }
  int q;
  cin >> q;
  while(q--)
  {
    int a, b;
    cin >> a >> b;
    if(find(a)== find(b))
      puts("Yes");
    else
      puts("No");
    
  } 

  return 0;
}
~~~

![image-20241015213454839](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015213454839.png)

**如果是按 size 比较的话 就将深度高的接到深度低的上了 就会增加深度**

## 真·终极优化（按深度）

~~~C++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int p [N];
int height [N];//高度只存在根节点上
int find(int x)
{
    return p [x]!= x?p [x] = find(p [x]): x;
}

int main()
{
  int n;
  cin >> n;
  
  for(int i = 1; i <= n; i++)
  {
    p [i] = i;
    height [i] = 1;
  }
  int u;
  cin >> u;
  while(u--)//并
  {
    int a, b;
    cin >> a >> b;
    int pa = find(a);
    int pb = find(b);
    if(pa == pb)
    continue;
    if(height [pa] < height [pb])
      p [pa] = pb;
    else if(height [pa] > height [pb])
      p [pb] = pa;
    else
    {
      p [pa] = pb;
      height [pb]++;
    }
    
    
  }
  int q;
  cin >> q;
  while(q--)
  {
    int a, b;
    cin >> a >> b;
    if(find(a)== find(b))
      puts("Yes");
    else
      puts("No");
    
  } 
  for(int i = 1; i <= n; i++)
  {
      cout << height [i] <<' ';
  }


 

  return 0;
}
~~~

**将深度小的接到深度高的上面去！！！！**

（使用数组存 height 深度）



# 七、图

[邻接表入门](#五、树)

#### 图的基本知识

![image-20250109215841503](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215841503.png)

![image-20250109215853168](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215853168.png)

![image-20250109215859276](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215859276.png)

![image-20250109215907230](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215907230.png)

![image-20250109215915809](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109215915809.png)

生成树一般是对于无向图而言的！！

**带权图：网**

有向边：弧

连通图是对于无向图的
强弱连通是对于有向图的

### 重点注意 ： 树的度和图的度不一样 树的度就是指孩子结点 图上面的也算！~





![image-20250109220351354](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109220351354.png)

## 1.图的存储

#### 1.邻接矩阵（适用于 稠密图 ）

**边如果很少（稀疏图）就会有很多空间浪费**



![image-20241009213321006](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213321006.png)

##### 定义

~~~C++
typedef struct 
{
    char vex [N];//顶点信息可以是结构体
    int edge [N][N];//边  无权图的话可以是 bool 类型
    int vexnum , arcnum;
    //存储这个图的点个数和边个数
}graph;
~~~

![image-20241009213547037](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213547037.png)

~~~C++

int main()
{
    int n;//n 个顶点
    cin >> n;
    graph g;
    for(int i = 0; i <n;i++)cin> > g.vex [i];
    //edge [a][b] a-> b;
    int q;
    cin >> q;
    while(q--)
    {
        int a, b;//连接两个顶点
        cin >> a >> b;//输入两个顶点的编号
        g.edge [a][b] = 1;
        g.edge [b][a] = 1;
    }//建立图的关系
    int ans = 0;//记录这个图的度
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
             if(g.edge [i][j])
             ans++;
            cout << g.edge [i][j] << " ";
        }
        cout << endl;
    }
        cout << ans/2;//度的数量
    
    return 0;
}
~~~



##### 带权图（网）的存储



![image-20241009213558354](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213558354.png)



**带权图先初始化所有边是 0 或者正无穷的都是可以的！**

![image-20241009213605823](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213605823.png)







> 涉及线性代数和矩阵的存储
>
> ![image-20241009214016575](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009214016575.png)
>
> 



##### 邻接矩阵的性质（涉及压缩矩阵的存储） --- 离散数学！！！

**n 阶的就是两点之间的路径长度为 n 个的有几条！！**



![image-20241009213628105](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213628105.png)





![image-20241009213635502](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213635502.png)

![image-20241009213642866](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009213642866.png)

#### 2.邻接表（适用于稀疏图）

![image-20241009220501867](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009220501867.png)

---





![image-20241009220508380](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009220508380.png)

---





![image-20241009220514633](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241009220514633.png)



> **vertices 顶点集（合）**
>
> **vertex 顶点**

与树同理， 一条边对应指向的点

![image-20250104104125048](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104104125048.png)

##### 初始化&&定义

~~~C++
const int N = 1e3;
int n;

typedef struct Arcnode  // 弧/边
{
    int adjvex;//指向的（vex）顶点的编号（index）
    Arcnode *next;
    
}Arcnode;//相当于是链表结点
//好习惯

typedef struct Vnode //顶点结构体结点 (存每个结点的信息)
{
    int val;//结点的值
    Arcnode *first;//存这个结点的头指针位置  
}adjList [N];//存每个结点 也是一个结构体（也就是数据类型）

//存图结构体
typedef struct 
{
  adjList vertices;// 数组类型 顶点集合   
    // Vnode 就相当于一个数据类型 
  int vexnum, arcnum;//顶点总和和边/弧总数
}graph;


void initialize(graph *g)//传入地址
{
    for(int i = 0; i <n;i++)g-> vertices [i].first = nullptr;
}
~~~

##### 添加边结点

~~~C++
void add(graph *g, int a, int b)//传入结点编号   ~~不带头结点的
{
  Arcnode *newNode = new Arcnode; // 新建一个边结点
  newNode-> adjvex = b; // 这个边是 b 出发的！！！
    
  newNode-> next = g-> vertices [a].first; // 头插法
  g-> vertices [a].first = newNode;// 不是虚拟头节点注意！！！
  // a-> b
  
  Arcnode *newNode_reverse = new Arcnode;
  newNode_reverse-> adjvex = a;
  newNode_reverse-> next = g-> vertices [b].first;
  g-> vertices [b].first = newNode_reverse;
  // b-> a

  
}//功能：a <-> b 插入(无向图)
~~~

##### 传参和基本操作注意（c 语言和 c++特性区别）

~~~C++
    graph g; //注意 c 语言和 c++区别
    cin >> n;//结点个数 
    initialize(&g);//c 语言特性 传参函数形参那边不允许写& 所以尽量写指针形式
    for(int i = 0; i <n;i++)cin> > g.vertices [i].val;//输入结点值
   
    int q;
    cin >> q;
    while(q--)
    {
        int a, b;
        cin >> a >> b;
        //连接结点
        add(&g, a, b);
    
        
    }
    int x = 0;
    while(cin >> x)
    {
        for(Arcnode *i = g.vertices [x].first; i!= nullptr; i = i-> next)
            cout <<i-> adjvex <<' ';
         //枚举类型注意
         //注意释放内存（when）
         
    }
~~~

##### 对于 有向图 枚举 入边 和 出边（简单）

~~~C++
    //枚举入边
    int x;
    cin >> x;
    for(int i = 0; i < n; i++)//枚举每一个编号
    {
        if(i == x)
            continue;
        for(Arcnode *j = g.vertices [i].first; j!= nullptr; j = j-> next)
        {
           if(j-> adjvex == x)
            cout << i <<' ';//此为入边的结点
        }
        cout << endl;
    }  
~~~



## 2.==图的基本操作==（对于邻接表和邻接矩阵）

> **注意：有无向图有向图之分！！！**

### 判断图是否存在边 <x,y> 有向边（弧） （x, y） 无向边

对于邻接表：遍历链表 时间复杂度：O(1)~O(|V|)  （考虑最好和最坏情况）

![image-20241010224253432](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224253432.png)

---





![image-20241010224311616](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224311616.png)
---

---





![image-20241010224337676](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224337676.png)

---

![image-20241010224346968](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224346968.png)

**邻接矩阵的删除**

---



![image-20241010224404081](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224404081.png)

**邻接表的删除**

---



 ![image-20241010224512653](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224512653.png)

**有向图的删除**

---

![image-20241010224520701](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224520701.png)

**对于邻接表直接头插法即可！！**

---

![image-20241010224528077](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224528077.png)



---



![image-20241010224535557](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224535557.png)

---

![image-20241010224543631](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224543631.png)

---



**带权图的权值获取和查询**

![image-20241010224550180](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241010224550180.png)

---



## 3. 图的遍历

### 1.图的 BFS 遍历

> **对于  <无向图>  && <邻接表>  的 bfs**

~~~C++
#include <iostream>
using namespace std;
const int N = 1e3;
int n;

int q [N];

typedef struct Arcnode  // 弧/边
{
    int adjvex;//指向的顶点的编号
    Arcnode *next;
    
}Arcnode;//相当于是链表结点
//好习惯

typedef struct Vnode //顶点结构体结点 (存每个结点的信息)
{
    int val;//结点的值
    Arcnode *first;//存这个结点的头指针位置
    
}adjList [N];//存每个结点

//存图结构体
typedef struct 
{
  adjList vertices;// 数组类型 顶点集合
  int vexnum, arcnum;//顶点总和和边/弧总数
}graph;

void add(graph *g, int a, int b)//传入结点编号   ~~不带头结点的
{
  Arcnode *newNode = new Arcnode;
  newNode-> adjvex = b;
  newNode-> next = g-> vertices [a].first;
  g-> vertices [a].first = newNode;
  
  Arcnode *newNode_reverse = new Arcnode;
  newNode_reverse-> adjvex = a;
  newNode_reverse-> next = g-> vertices [b].first;
  g-> vertices [b].first = newNode_reverse;
  
}//功能：a <-> b 插入(无向图)
void initialize(graph *g)//传入地址
{
    for(int i = 0; i <n;i++)g-> vertices [i].first = nullptr;
}
void bfs(graph *g, int v)//从结点 v 开始的 bfs 遍历
{
    //初始化
    bool st [N];//标记是否访问过
    int hh = 0, tt =-1;
    q [++tt] = v;
    st [v] = 1;
    
    while(tt >= hh)//队列不空
    {
        int t = q [hh++];//取弹队头
        for(Arcnode *i = g-> vertices [t].first; i!= nullptr; i = i-> next)
        {
           if(! st [i-> adjvex])
           {
               cout <<i-> adjvex << " ";
               st [i-> adjvex] = 1;
               q [++tt] = i-> adjvex;
               
           }
           
        }
    }
    
}
int main()
{
    graph g;
  
    cin >> n;//结点个数 
    initialize(&g);
    for(int i = 0; i <n;i++)cin> > g.vertices [i].val;//输入结点值
    
  
    
    int q;
    cin >> q;
    while(q--)
    {
        int a, b;
        cin >> a >> b;
        //连接结点
        add(&g, a, b);
    
        
    }
    bfs(&g,0);
  
  
    
    return 0;
}
~~~



#### 如果图不止一个连通块

#### --> 就无法遍历完所有顶点!!!\

>  **所要添加的操作是：**

~~~C++
void bfs(graph *g, int v)//从结点 v 开始的 bfs 遍历
{
    //初始化
    cout << v << " ";
    int hh = 0, tt =-1;
    q [++tt] = v;
    st [v] = 1;
    
    while(tt >= hh)//队列不空
    {
        int t = q [hh++];//取弹队头
        for(Arcnode *i = g-> vertices [t].first; i!= nullptr; i = i-> next)
        {
           if(! st [i-> adjvex])
           {
               cout <<i-> adjvex << " ";
               st [i-> adjvex] = 1;
               q [++tt] = i-> adjvex;
               
           }
           
        }
    }
    
}

void bfsTraveler(graph *g)
{
  for(int i = 0; i < n; i++)st [i] = 0;
  //先初始化

  for(int i = 0; i < n; i++)
  {
      if(! st [i])
      {
         bfs(g, i); 
         cout << endl << "-------" << endl;
      }
       
       
  }
  
    
}
~~~

### 复杂度分析

![image-20241011192142663](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011192142663.png)

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

![image-20250104145016688](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104145016688.png)

**就是根据层次遍历构建树（但不一定是二叉树！！！！！）**

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011192137652.png)

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

~~~C++
void dfs(graph *g, int v)
{
    
    for(Arcnode *i = g-> vertices [v].first; i!= nullptr; i = i-> next) // 结合循环横向遍历
    {
      
        if(! st [i-> adjvex])
        {   
            cout <<i-> adjvex <<' ';
            st [i-> adjvex] = 1;
            dfs(g, i-> adjvex);
        }
    }
    
}
~~~

#### 如果图不止一个连通块

#### --> 就无法遍历完所有顶点!!!

~~~C++
void dfs(graph *g, int v)
{
    cout << v << " ";//为什么结点处理放这里可以（一定满足）
    
    for(Arcnode *i = g-> vertices [v].first; i!= nullptr; i = i-> next)
    {
        if(! st [i-> adjvex])
        {   
            st [i-> adjvex] = 1;
            dfs(g, i-> adjvex);
        }
    }
    
}


void dfstravel(graph *g)
{
       
    
    for(int i = 0; i < n; i++)st [i] = 0;//初始化
  

    for(int i = 0; i < n; i++)
    {
        
        if(! st [i])
        {
          st [i] = 1;
          dfs(g, i);  
          cout << endl << "--------" << endl;
        }
            
    }
}
~~~



### 复杂度分析

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011210933645.png)

**思维：dfs 找全部解，一旦 tle 了就记忆化，剪枝或者改为 bfs（最短路），实在不行就 dp！！**



![image-20241011211122218](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211122218.png)

**访问过的就不会再访问了所以和 bfs 时间复杂度一样！！**

---



![image-20241011211157535](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211157535.png)

![image-20241011211202359](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211202359.png)

---



### 深度优先生成树/森林

![image-20250821220137055](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220137055.png)



![image-20241011211207045](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211207045.png)

![image-20241011211211264](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211211264.png)

![image-20241011211215101](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211215101.png)

---









## *最短路

### 0.bfs  （✓） （win + .）



### 1.dijkstra

![image-20241013142449294](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013142449294.png)

![image-20241013142453353](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013142453353.png)

```C++
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 510;

int n, m;
int g[N][N];
int dist[N];//记录最短路径！！
bool st[N];//标记是否找到最短路

int dijkstra()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;//标记起点

    for (int i = 0; i < n - 1; i ++ )
    {
        int t = -1;
        for (int j = 1; j <= n; j ++ )
            if (!st[j] && (t == -1 || dist[t] > dist[j]))// 找到当前未标记的节点中距离最小的节点
                t = j;

        for (int j = 1; j <= n; j ++ )
            dist[j] = min(dist[j], dist[t] + g[t][j]);// 更新邻接节点的距离

        st[t] = true;
    }

    if (dist[n] == 0x3f3f3f3f) return -1;
    return dist[n];
}

int main()
{
    scanf("%d%d", &n, &m);

    memset(g, 0x3f, sizeof g);
    while (m -- )
    {
        int a, b, c;
        scanf("%d%d%d", &a, &b, &c);

        g[a][b] = min(g[a][b], c);//防止重边
    }

    printf("%d\n", dijkstra());

    return 0;
}


```

### 时间复杂度（与 prim 极其类似）

### 2.floyd



**key：中转点**

![image-20241013140817638](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013140817638.png)

![image-20241013140846502](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013140846502.png)







~~~C++
#include <iostream>
#include <cstring>
using namespace std;
const int N = 1e3+10;
int mp [N][N];
int vex [N];
int n;
int path [N][N];
void floyd()
{
    for(int i = 0; i < n; i++)//枚举中转点
        for(int j = 0; j < n; j++)
            for(int k = 0; k < n; k++)
                if(mp [j][k] > mp [j][i]+mp [i][k])
                {
                    mp [j][k] = mp [j][i]+mp [i][k];
                    path [j][k] = i;//类似 bfs 中的 last 数组记录路径
                }      
     
}

int main()
{
  
    cin >> n;
    memset(mp,0x3f, sizeof mp);//0x3f3f3f3f
    memset(path,-1, sizeof path);
   int x;
   cin >> x;
    while(x--)
    {
      int a, b, val;
      cin >> a >> b >> val;
      mp [a][b] = mp [b][a] = val;//两个连等号
      
    }
    floyd();
  
    int st, ed;
    cin >> st >> ed;
    while(ed!= st)
    {
        cout << ed <<' ';
        ed = path [st][ed];
        
    }
    return 0;
}
~~~

**时空复杂度：0(v3 次方) o(v2 次方)**

**floyd 可以解决带负权边的问题！**



![image-20241013141204822](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013141204822.png)



![image-20241013141213311](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013141213311.png)

**时空复杂度具体还是得看图的存储结构**

---

# 拓扑排序（可判断回路）

**key ： 拓扑排序一定是有向无环图！**



![image-20241013143603689](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013143603689.png)

![image-20241013143703056](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013143703056.png)

### 邻接矩阵法

~~~C++
#include <iostream>
#include <vector>
using namespace std;
const int N = 10000;
int g [N][N];
int st [N];
int top = 0;
int cnt;//记录当前的顶点数
int n;
int inedge [N];
vector <int> ans;
int bfs()
{
       while(top)
    {
        ans.push_back(st [top]);
        int t = st [top];
        cnt++;
        top--;
        for(int i = 1; i <= n; i++)
        {
            if(g [t][i])
            {
              inedge [i]--;  
                   
            if(inedge [i] == 0)
            {
              st [++top] = i;  
              g [t][i] = 0;//删去这条边
            }
            
            }
        }
        
        
    }
    if(cnt < n)
        return 0;
    else
        return 1;
}
int main()
{
 
    cin >> n;
    int x;
    cin >> x;
    while(x--)
    {
        int a, b;
        cin >> a >> b;
       
        if(! g [a][b])//防止重边重复计数
        inedge [b]++;//统计入边  
        g [a][b] = 1;//表明有边
    }
    for(int i = n; i >= 1; i--)
    {
        if(inedge [i] == 0) 
            st [++top] = i;
    }
    //先存储入度为 0 的点
    if(bfs())
        for(int i = 0; i < n; i++)
            cout << ans [i] <<' ';
    else
        cout <<-1;

//  for(int i = 1; i <= n; i++)cout << inedge [i] <<' '; 
    
}
~~~

### 邻接表写法

~~~C++
#include <iostream>
#include <vector>
using namespace std;
const int N = 1e5+10;
vector <int> ans;
int st [N];
int top;
int inedge [N];

int n;
typedef struct ArcNode
{
    int adjvex;
    ArcNode *next;
}ArcNode;

typedef struct vexNode
{
    int val;
    ArcNode *first;//头结点
}verlist [N];
typedef struct graph
{
    verlist vertices;//顶点集
    int numvex, numedge;
   
    
}graph;
void add(graph *g, int a, int b)
{
    ArcNode *n1 = new ArcNode();
    n1-> adjvex = b;
    n1-> next = g-> vertices [a].first;
    g-> vertices [a].first = n1;
    
}
int bfs(graph *g)
{
    int cnt = 0;
    while(top)
    {
        int t = st [top--];//这里就是对队列中的元素处理
        cnt++;
        ans.push_back(t);
        for(ArcNode *i = g-> vertices [t].first; i!= nullptr; i = i-> next)
        {
            inedge [i-> adjvex]--;//因为在这个循环中把所有出边都删除了
            if(inedge [i-> adjvex] == 0)
            {
                st [++top] = i-> adjvex;
                
            }
        }
        
    }
    if(cnt < n)return 0;
    else
    return 1;
}
int main()
{
    graph g;

    cin >> n;
    for(int i = 1; i <= n; i++)g.vertices [i].first = nullptr;//一定要初始化
    int x;
    cin >> x;
   
    while(x--)
    {
        int a;
        int b;
        cin >> a >> b;
     
            add(&g, a, b); 
    }
    for(int i = 1; i <= n; i++)
    {
      for(ArcNode *h = g.vertices [i].first; h!= nullptr; h = h-> next)
      {
          inedge [h-> adjvex]++;
      }
    }
    // for(int i = 1; i <= n; i++)
    //     if(inedge [i] == 0)
    //         st [++top] = i;
    // if(bfs(&g))
    //     for(auto c: ans)
    //         cout << c <<' ';
    // else
    //     cout <<-1;
        cout << inedge [2];
 
    
}

~~~

**注意点：初始化问题 nullptr 一定！！**

**删除边问题**



### 逆拓扑排序（使用 dfs）

### 对于逆序 考虑 dfs（递归栈）

#### 整体

~~~c++

    #include <iostream>
    #include <vector>
    using namespace std;
    const int N = 1e5+10;
    vector <int> ans;
    bool flag [N];
    int n;
    typedef struct ArcNode
    {
        int adjvex;
        ArcNode *next;
    }ArcNode;
    
    typedef struct vexNode
    {
        int val;
        ArcNode *first;//头结点
    }verlist [N];
    typedef struct graph
    {
        verlist vertices;//顶点集
        int numvex, numedge;
       
        
    }graph;
    void add(graph *g, int a, int b)
    {
        ArcNode *n1 = new ArcNode();
        n1-> adjvex = b;
        n1-> next = g-> vertices [a].first;
        g-> vertices [a].first = n1;
        
    }
    
      void dfs(graph *g, int v)//起点
    {
        for(ArcNode *i = g-> vertices [v].first; i!= nullptr; i = i-> next)
        {
            if(! flag [i-> adjvex])
            {
              flag [i-> adjvex] = 1;
              dfs(g, i-> adjvex);  
              
            }
            
        }
        cout << v <<' ';
        
    }
    
    
    
    void dfstravel(graph *g)
    {
        for(int i = 1; i <= n; i++)
        flag [i] = 0;
        //初始化
        for(int i = 1; i <= n; i++)//从入度为零的点开始
        {
            if(! flag [i])
            {
            
                dfs(g, i);
            }
            
        }
        
    }
  
    int main()
    {
        graph g;
    
        cin >> n;
        for(int i = 1; i <= n; i++)g.vertices [i].first = nullptr;//一定要初始化
        int x;
        cin >> x;
       
        while(x--)
        {
            int a;
            int b;
            cin >> a >> b;
         
            add(&g, a, b); 
        }
        dfstravel(&g);
        
            
      
        
    }

~~~

#### 核心代码

~~~C++
 
      void dfs(graph *g, int v)//起点
    {
        for(ArcNode *i = g-> vertices [v].first; i!= nullptr; i = i-> next)
        {
            if(! flag [i-> adjvex])
            {
              flag [i-> adjvex] = 1;
              dfs(g, i-> adjvex);  
              
            }
            
        }
        cout << v <<' ';
        
    }
    
    
    
    void dfstravel(graph *g)
    {
        for(int i = 1; i <= n; i++)
        flag [i] = 0;
        //初始化
        for(int i = 1; i <= n; i++)//从入度为零的点开始
        {
            if(! flag [i])
            {
            
                dfs(g, i);
            }
            
        }
        
    }

~~~

![image-20241013170231676](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241013170231676.png)

# 关键路径(可以运用到实践！！！)

**网：带权边图**



![image-20250104152648586](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104152648586.png)

必须是 ==有向无环图==

![image-20250104153331492](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104153331492.png)

普通活动：可以拖延的活动！

### 求关键路径

**步骤：先求点（事件 == 就是== 活动 == 完成后的一个状态），在求边（活动） ---> 最早/晚开始时间 **  

**ve，vl**

**e , l**



**求 ve 拓扑排序（入度为零） 取 ==最大==** 

**求 vl 逆拓扑（出度为零） 取 ==最小==**

key：当前事件要达到 入度（活动）都要删除（完成）

![image-20250104155038735](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104155038735.png)

![image-20250104155329424](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104155329424.png)

![image-20250104155444586](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104155444586.png)

**时间余量：最晚开始时间- 最早开始时间 （可以拖延的时间）！！！！**

# 八、最小生成树(一般是针对无向图的)

**连通图概念：从一个顶点可以到达任意一个顶点（都有路径）**

生成树：表示所有顶点均由边连接在一起，但 **不存在回路** 的图

![image-20250104160033803](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104160033803.png)

## 1.prim 算法（找点为核心）

![image-20250104160302843](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104160302843.png)

**点亮的部分 ：当前的最小生成树**  每次都在没点亮的点中找   距离点亮的点  中最近（距离最短）的点点亮（加入最小生成树）



![image-20241011211526962](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211526962.png)

![image-20241011211542709](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211542709.png)

![image-20241011211551109](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211551109.png)

---



## prim 实现操作

![image-20241011211950682](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211950682.png)

![image-20241011212001654](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212001654.png)

![image-20241011212008783](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212008783.png)

![image-20241011212123191](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212123191.png)

![image-20241011212129170](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212129170.png)

---







​	



## 2. kruskal 算法（找边为核心）



![image-20250821220148476](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220148476.png)

**每次找最短的边连接 连接之前有条件 ： 就是这条边的两个端点是否连通（不一定是 ==直连==）**

![image-20241011211618541](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211618541.png)

![image-20241011211634355](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211634355.png)

## kruskal 实现操作（并查集）



![image-20241011212138688](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212138688.png)

![image-20241011212205046](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212205046.png)

![image-20241011212208675](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212208675.png)

![image-20241011212211415](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011212211415.png)



## ==sum==

![image-20241011211648769](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241011211648769.png)



# 有向无环图 的表达式求值

![image-20241015164413069](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164413069.png)



![image-20241015164423599](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164423599.png)

![image-20241015164431523](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164431523.png)

![image-20241015164437958](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164437958.png)



# ==-------《查找》--------==



**查找长度的概念：对比关键字的次数！**

## 查找的基本概念

![image-20250104162840604](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104162840604.png)



![image-20241016211125959](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016211125959.png)

---



![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016211217831.png)

## 查找算法的效率分析

![image-20241016211256652](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016211256652.png)

## 平均查找长度公式：

![image-20241016211347984](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016211347984.png)

**注意：ASL 的数量级反映了这个查找算法的时间复杂度！**



# 1^o^   顺序查找

![image-20250104163557792](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104163557792.png)

**查找概率看 ==元素权重==**

![image-20241017192820102](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017192820102.png)

**带哨兵与不带哨兵 仅有微妙的区别 重点在于 查找成功和查找失败的情况**

ASL = （每个点 **查找次数** 乘上 **查找概率** ）之和

**通过 有序 来优化算法**

### 查找失败主要针对失败结点！！！

![image-20250104174837063](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104174837063.png)

**分子：每个失败结点的查找次数之和**



![image-20241017193115000](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017193115000.png)



![image-20241017193548148](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017193548148.png)





# 2^o^   折半查找（二分）--必须数组且有序



1. **ASL**：反映整体查找效率，是所有元素查找长度的加权平均。
2. **每个点的查找长度**：反映单个元素的查找效率，具体到某个元素的比较次数。

---



## 构造二分查找判定树

<span style="color:#FF00FF;">**失败的ASL就是   每个查找的次数之和/失败结点（前提是概率一样）**</span>



**key： 失败和成功都和树高有关系**



**将收尾下标（从 1 开始）相加除以二 然后取这个位置作为根节点递归处理**



![image-20241017193951847](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017193951847.png)

---



![image-20241017193935293](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017193935293.png)

**查找失败的分母就是失败结点的个数**



## 折半查找判定树的树高 h：



![image-20241017195049820](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017195049820.png)

**观察树满足什么性质 判断树的种类 确定计算方法！！！** 

![image-20241017195110393](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017195110393.png)

---

## 时间复杂度

![image-20241017195225185](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017195225185.png)

---

**这个时间复杂度怎么来的？**





## 查找成功与查找失败

**二分查找判定树  是个 ==二叉排序树 + 二叉平衡树==**



## sum

![image-20241017194037958](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017194037958.png)

**不对称的分为左/右多的两种情况**

![image-20241017210430792](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241017210430792.png)



**正常做法直接画图就行 ： 根据判定树逆向画集合序列 然后判断是向上取整还是向下取整如果矛盾了就是错的！**



---



# 3^o^   分块查找

**特征：块间有序--- 块内无序**

**查找存储结构** 最大值和上下界

![image-20250109221246273](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250109221246273.png)

![image-20250104204502785](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250104204502785.png)

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





![308062505289bd26cd75ce60b260b36](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/308062505289bd26cd75ce60b260b36.png)



![image-20241015164542843](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164542843.png)

**进行中序遍历得到最终的有序序列**

## 查找



![image-20250821220154592](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250821220154592.png)



##  插入

## ![image-20241015164737288](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164737288.png)

## 构造



![image-20241015164756645](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164756645.png)

## 删除分三种情况

### 1.结点是叶子结点 

**直接删除**

### 2.结点只有一边的子树（代替）



![image-20241015164836591](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015164836591.png)

### 3.结点两边都有子树！！！！！

**相当于找中序遍历的前驱/后继 （因为中序遍历二叉排序树就是一个有序序列）**

#### 又分为两种做法 ： 处理 后继和前驱 

![image-20241015165111380](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015165111380.png)

**根据二叉排序树的特性进行的措施！**

![image-20241015165124001](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015165124001.png)

## 查找效率分析

**插入主要就是查找的过程！！**

![image-20250105144240339](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105144240339.png)

###  查找成功

![image-20241015165339468](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015165339468.png)

**最好情况：二叉树的高度为 log2^n+1  平均查找长度为 O (log2^（n+1）)**

**最坏情况：每个结点有且仅有一个分支 树高 h = 结点数 n  ==退化为链表== , 平均查找长度为 o(n)**

**原因就是构造时的问题**

**解决方法：构造时构造 ==平衡二叉树！==**

### 查找失败

![image-20241015165750084](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241015165750084.png)

# 十、平衡二叉树（AVL 树）

**当二叉搜索树本来就有序的时候二叉搜索树就会退化为链表**

**所以引入 ————>    ==<平衡二叉树>==** 

**平衡二叉树：是一种特殊的二叉搜索树（二叉排序树）**

![image-20250105144313925](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105144313925.png)

![image-20250105151205375](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105151205375.png)

### 旋转操作 ==(调整失衡)==



![image-20250105151219618](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105151219618.png)

**确定失衡因子 ：** 确定是 ==哪个孩子== 的 ==哪个子树== 上

如图就是 ==LL 型==

![image-20250105165259938](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105165259938.png)





![image-20250105165725423](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105165725423.png)

![image-20250105165818401](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105165818401.png)



![ ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105165826570.png)



### 四种失衡情况 



![image-20250105165113988](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105165113988.png)

**和构建二叉排序树一样 但是多了一步 也就是在增删改的过程中如果导致失衡了就要进行平衡操作！**

### 平衡二叉树操作

**插入&构建：**

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105170221788.png)

**删除**:

**删除结点后可能导致多个地方失衡了**

**需要依次沿着祖先向上检查和调整**

![image-20250105170536270](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105170536270.png)

# 十一、红黑树













# 十二、B 树



# 十三、B+树





# ==十四、堆==

**堆一定是一颗完全二叉树**



![image-20250105144257762](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105144257762.png)

## up 和 down 逻辑



~~~c++
void up(int u)
{
    while(u/2 > 0&&h [u] < h [u/2])//指涉不为空
    {
        swap(h [u], h [u/2]);
        u/= 2;//步进
    }
}
void down(int u)
{
    int t = u;//当前结点 cur
    
    //比较三个值（前提是指涉不为空）
    if(u *2 <= Size&&h [u*2] < h [t])t = u* 2;
    if(u *2+1 <= Size&&h [u*2+1] < h [t])t = u* 2+1;
    //两个 if 都要判断
    
    if(t!= u)//如果确实要改变
    {
        swap(h [t], h [u]);
        down(t);//直到 down 到满足条件
    }
}
~~~

**堆是完全二叉树，下标是不会变化的，变化的仅有数据**

## 建堆

~~~C++
 cin >> n; 
    Size = n;
    for(int i = 1; i <=Size;i++)cin> > h [i];//传入时都是离散的每一个点
    //!
    for(int i = n/2; i; i--)down(i);//从最后一个父节点开始建堆(建小根堆)
~~~



## 操作

### 1.插入一个数

~~~c++
void insert(int x)
{
    h [++Size] = x;
    up(Size);
    
}
~~~



### 2.求堆顶

`h[1]`

### 3.删除堆顶

~~~c++
void del()
{
    h [1] = h [Size--];
    down(1);
}
~~~



### 4.删除任意一个元素

~~~c++
void supDel(int k)//下标
{
    h [k] = h [Size--];
    //!
    up(k);
    down(k);
}
~~~



### 5.修改任意一个元素

~~~C++
void change(int k, int x)
{
    h [k] = x;
    //!
    up(k);
    down(k);
}
~~~





# 十五、哈希表(散列查找)

**处理冲突的方法 ； 拉链法 开放寻址法**

**散列表的构造： 除留余数法 直接定址法 平方取中法 数字分析法**

# 一、 拉链法



[树的相关知识](#五、树)

![image-20241016195939589](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016195939589.png)

**==特别的==：注意题目 如果位置上都没有数的话 就无需判断(无需比较关键字)，也就是查找长度是 ==0== ！**

**冲突越多 查找效率越低**

![image-20241016202801877](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016202801877.png)





## 散列表的构造

**！！！！**

**要不大于散列表长度的 才行**

**如果散列表长度 15 mod 19 可能会被映射到大于 16 小于 18 的范围内**

---



![image-20241016202753965](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016202753965.png)

## 1.除留余数法

### 使用数组模拟

~~~C++
#include <iostream>
#include <cstring>
using namespace std;
const int N = 100003;//第一个比长度大的质数（可以相等--> 尽可能接近）
int e [N], idx, h [N], ne [N];
void add(int x)
{
  int hash =(x%N+N)%N;
  e [idx] = x;
  ne [idx] = h [hash];
  h [hash] = idx++;


}
int find(int x)
{
  int hash =(x%N+N)%N;
  for(int i = h [hash]; i!=-1; i = ne [i])
  {
    if(e [i] == x)
      return 1;
  }
  return 0;
}
int main()
{
  memset(h,-1, sizeof h); //初始化为-1
  int n;
  cin >> n;
  while(n--)
  {
    int x;
    cin >> x;
    add(x);
  }
  int x;
  cin >> x;
  cout << find(x);
  

  return 0;
}
~~~

![image-20241016202329672](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016202329672.png)

![image-20241016203135175](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016203135175.png)

**但是使用 mod 素数法也不一定是最优的 如果如上是 ==连续== 的就不是最优的了 （具体题目具体分析！**）

此邻接表也可用于 ==建图== ！！ 

## Create Graph

==**h 存的都是下标指针一类的！！**==

~~~C++
#include <iostream>
#include <cstring>
using namespace std;
const int N = 1e5+10;
int e [N], ne [N], h [N], w [N];
int idx;
void add(int a, int b, int weight)// a-> b
{
  ne [idx] = h [a];
  h [a] = idx;
  e [idx] = b;
  w [idx++] = weight;

}
int main()
{
  memset(h,-1, sizeof h);//都要先初始化为-1；

  return 0;
}
~~~



### 使用拉链法（就是散列表）

~~~C++
#include <iostream>
using namespace std;
const int N = 10003;

typedef struct ArcNode  
{
    int adjvex;//结点值
    ArcNode *next;//链表
}ArcNode;

typedef struct VNode
{
  int val;
  ArcNode *first;//h []

}vexlist [N];
typedef struct graph
{
  vexlist vextices;//顶点 set
  int numvex, numedge;//no-usage
}graph;
//下面的只是别名  上面的是它本名！！！
void add(int x, graph *g)
{
  int hash =(x%N+N)%N;
  ArcNode *newNode = new ArcNode();
  newNode-> adjvex = x;
  newNode-> next = g-> vextices [hash].first;
  g-> vextices [hash].first = newNode;


}
int find_is_exist(int x, graph *g)
{
  int hash =(x%N+N)%N;
  for(ArcNode *i = g-> vextices [hash].first; i!= nullptr; i = i-> next)
  {
      if(i-> adjvex == x)
        return 1；
  }
  return 0;
}
--------------------------------
void init(graph *g)
{
  for(int i = 0; i < N; i++) 
    g-> vextices [i].first = nullptr;
}
--------------------------------// --> 初始化很重要 <--
int main()
{
  graph p;
  init(&p);
  int n;
  cin >> n;
  while(n--)
  {
    int x;
    cin >> x;
    add(x,&p);
  }
  int q;
  cin >> q;
  while(q--)
  {
    int x;
    cin >> x;
    cout << find_is_exist(x,&p)<< endl;
  }
  return 0;
}
~~~





## 2.直接定址法 （适合连续的元素）

## 

![image-20241016203346967](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016203346967.png)

## 3. 平方取中法

**选定散列函数时不一定知道关键字的全部情况 取其中某几位也不一定合适**

都不均匀的情况

![image-20250105123548408](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105123548408.png)

## 4.数字分析法 // 如电话号码 

适用条件 ： **必须事先知道 ==所有关键字== 的每一位上的各种数字的分布情况**

如 135xxxxx……这种 135 就 ==不均匀== 分布比较多



## ![image-20250105123623761](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105123623761.png)



**key：就是尽可能的减小冲突，也有可能完全避免冲突的（具体问题具体分析！！！**



![image-20241016203421863](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016203421863.png)

# 二、开放寻址法

<font size=8> ==**! 注意：  m 表示散列表表长度**== </font>



**key ： 如果偏移时超过散列表长度了就mod也就是等效作环**

## 1.线性探测法（最重要！！）

![image-20250105130337305](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105130337305.png)

![image-20250105130543287](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105130543287.png)

 

### 缺点

![img](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/%7B2FE42FCB-10B0-4D5A-8718-B194A7B0CCEC%7D)

![image-20241016204343928](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20241016204343928.png)

**导致遇到逻辑删除的位置还是要一直查询！**

## 2.平方探测法

**弥补了以上问题**

> ![image-20250105130854543](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105130854543.png)
>
> 
>
> 

## 3.伪随机探测法

![image-20250105131922185](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105131922185.png)



## 4.双散列法（准备多个散列表）

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105131823291.png)



## 删除一个元素

![image-20250105132155895](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105132155895.png)



![image-20250105132449143](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105132449143.png)



![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105132613736.png)



# 十六、排序

## 排序分类：

![image-20250103170109778](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103170109778.png)

**复杂度分析！！！！**



> 对于递归 画树更好理解！		
>
> 稳定 插帽龟 and  统计鸡

## 算法的稳定性

![image-20240927221330046](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240927221330046.png)



## 1.归并排序

~~~c++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int a [N];
int res [N];
void merge(int q [], int l, int r)
{
    if(l == r)//只有一个点到时候返回
    return ;
    int mid = l+r >> 1;
    merge(q, l, mid);
    merge(q, mid+1, r);
    
    int i = l, j = mid+1;
    int k = 0;
    while(i <= mid&&j <= r)
    {
        if(q [i] < q [j]) res [k++] = q [i++];
        else res [k++] = q [j++];
        
    }
    while(i <= mid)res [k++] = q [i++];
    while(j <= r)res [k++] = q [j++];
    //!!!
    for(int i = l, j = 0; i <= r; i++, j++)
    {
        q [i] = res [j];
    }
    
    
}
int main()
{
    int n;
    cin >> n;
    for(int i = 0; i <n;i++)cin> > a [i];
    merge(a,0, n-1);
    for(int i = 0; i < n; i++)cout << a [i] <<' ';
    
    return 0;
}
~~~

## 2.快速排序

思路 ： 任选一个元素作为 枢轴（pivot	）量 然后让两边 分别小于/大于这个元素

![image-20250105100449314](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105100449314.png)

这样需要额外开一个数组！！



---

这个方法 第一次先让 right 从右往左走！！！ 

![image-20250103171534948](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103171534948.png)

**划分完成：**



![image-20250103171543490](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103171543490.png)

**递归处理：**



![image-20250103171639513](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103171639513.png)

### 递归的时空复杂度分析

每次划分枢轴都刚好是中间值 的话就是效率最好的情况

![image-20250103172242296](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103172242296.png)

**递归会占用系统栈空间 所以会有辅助空间的开销**

**最坏情况**：本来就有序，而且每次枢轴量取当前区间的第一个元素

**如果每次取中间有可能也会达到最差性能**

![image-20250103172601011](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103172601011.png)

**辅助空间的复杂度最坏下也是 O(n) （因为递归层数是 O(n)）!!!**

~~~C++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int a [N];
void quick(int a [], int l , int r)
{
    if(l == r)
    return ;
    
    int x = a [l+r >> 1];
    int i = l-1, j = r+1;
    while(i < j)
    {
        //注意这个 while 不能就一个 不然会嵌入下行的 除非 while 下面跟着语句
        
        while(a [++i] < x);
        while(a [--j] > x);//不能等
        //!
        if(i < j)swap(a [i], a [j]);
    }
    quick(a, l, j);//不能 mid 相遇在 i/j 而不一定是 mid
    quick(a, j+1, r);
}
int main()
{
    int n;
    cin >> n;
    for(int i = 0; i <n;i++)cin> > a [i];
    quick(a,0, n-1);
    for(int i = 0; i < n; i++)cout << a [i] <<' ';
    return 0;
}
~~~



## 3.选择排序

**key：一次交换涉及三次移动！！**

![image-20250103224726113](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103224726113.png)

 <font size=6 color = red> 选择排序原代码有问题！！！！！</font>

问题虽然可以排序成功但是效率极其低因为交换次数过多

**测试数据：**

5
64, 25, 12, 22, 11

**why :** 

~~~c++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int a [N];
int main()
{
    int n;
    cin >> n;
    for(int i = 0; i <n;i++)cin> > a [i];
    int min;
    for(int i = 0; i < n-1; i++)
        for(int j = i+1; j < n; j++)
        {
            if(a [j] < a [i])swap(a [i], a [j]);
        }
        
    
    for(int i = 0; i < n; i++)cout << a [i] << " ";
    
    return 0;
}
~~~

 <font size=5 color =red > 正确写法 </font>

#include <iostream>
using namespace std;
int a [10];
int main()
{
    int n;
    cin >> n;
    int cn = 0; // 比较次数
    int mn = 0; // 移动次数
    
```c++
for(int i=0;i<n;i++) cin>>a[i];

int min_index;
for(int i=0;i<n-1;i++)
{
     min_index = i; // 最小的值的下标
    for(int j=i+1;j<n;j++)
    {
        cn++;
       // 每次找最小值
       if(a[j]<a[min_index])
       {
           min_index = j;
       } //  找的过程中不改变原序列  
    }
    if(min_index !=i)
    {
        swap(a[min_index],a[i]);
        mn+=3;
    }
    
}

for(int i=0;i<n;i++)cout<<a[i]<<" ";
cout<<endl;
cout<<"比较次数: "<<cn<<endl;
cout<<"移动次数："<<mn<<endl;

return 0;
```
}



### 性能分析

![image-20240927221540776](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20240927221540776.png)

## 4.冒泡排序

每轮都从前往后以此比较相邻的两个数，逆序就交换

这里的一次交换也是 ==三次== 移动（temp 操作）

~~~C++
#include <iostream>
using namespace std;
int main()
{
    int n;
    cin >> n;
    int a [10];
    for(int i = 0; i <n;i++)cin> > a [i];
        
    for(int i = 0; i < n-1; i++)
    {
        //每一趟都设置为 0
        bool flag = 0;//如果有交换就设为 true  没有交换了就说明已经有序了！
        for(int j = n-1; j > i; j--)
        {
            if(a [j] < a [j-1]) // 逆序遍历
            {
                flag = 1;
                swap(a [j], a [j-1]);
            }
        }
        if(flag == 0)
        break;
    }
    
    for(int i = 0; i < n; i++)cout << a [i] << " ";
    
    return 0;
}
~~~



## 5.堆排序

~~~c++
#include <iostream>
using namespace std;
const int N = 1e5+10;
//需要什么
int h [N];
int Size;
int n, m;
void up(int u)
{
    while(u/2 > 0&&h [u] < h [u/2])//指涉不为空
    {
        swap(h [u], h [u/2]);
        u/= 2;//步进
    }
}
void down(int u)
{
    int t = u;//当前结点 cur
    
    //比较三个值
    if(u *2 <= Size&&h [u*2] < h [t])t = u* 2;
    if(u *2+1 <= Size&&h [u*2+1] < h [t])t = u* 2+1;
    
    if(t!= u)
    {
        swap(h [t], h [u]);
        down(t);//直到 down 到满足条件
    }
}

int main()
{
    cin >> n >> m; 
    Size = n;
    for(int i = 1; i <=n;i++)cin> > h [i];//传入时都是离散的每一个点
    //!
    for(int i = n/2; i; i--)down(i);//从最后一个父节点开始建堆
   
    
    while(m--)
    {
        cout << h [1] << " ";
        h [1] = h [Size--];//覆盖
        down(1);
        
    }
    
    return 0;
}
~~~



## 6.基数排序 (非比较排序算法)

​	**基数 ： 进制 e.g 二进制基数就是 2**

操作：逐位进行 ==分配== 和 ==收集==（从最低位开始 ，从最高的话比较复杂涉及 **递归处理**）

每个桶内部用链表（链式队列）这个数据结构存数据 （用数组的话会比较浪费空间）

**分配：**（按照位数 第一轮就是个位 ，第二轮就是十位 …… 以此类推）

 ![image-20250103164530664](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103164530664.png)

**收集**：
**枚举桶、从桶里拿出来收集成一个单链表！**

---

**效率：**

![image-20250103165218390](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103165218390.png)

![image-20250103165253057](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250103165253057.png)



---







## 7.直插排序 (移位赋值操作)



### 简单插入排序

操作：依次将每个元素插入到前面有序的部分当中

先拿当前元素和有有序区最后一个数进行比较 如果大于就无需排序直接加入有序区即可 如果小于呢 就把这个数先使用 temp 变量临时存起来 然后依次和有序区的每一个元素比较 

![image-20250105162033781](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105162033781.png)



移动次数除了比较的时候移动还有 当前元素移动到 temp 再从 temp 移动到插入的位置



![image-20250105162401059](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105162401059.png)



![image-20250105162522499](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105162522499.png)

~~~C++
#include <iostream>
using namespace std;
const int N = 1010;
int a [N];
int main()
{
    int n;
    cin >> n;
    //a [0] 哨兵结点
    for(int i = 1; i <=n;i++)cin> > a [i];
    if(n == 1)
    {
        cout << a [1];
        return 0;
    }
    int j;
    for(int i = 2; i <= n; i++)//每次在遍历时都保证了前面是有序的了
    {
        if(a [i] < a [i-1])
        {
            a [0] = a [i];//复制当前元素到哨兵结点
            //判断条件不需要 j > 0 因为 a [0] 本身，到本身一定会停下来
            for(j = i-1; a [0] < a [j]; j--) a [j+1] = a [j];//右移空间, 因为会覆盖所以要用哨兵存起来
            
            //直到满足条件 j 就会停下来
            a [j+1] = a [0];
        }
    }
    for(int i = 1; i <= n; i++)cout << a [i] << " ";
    return 0;
}
~~~

### 二分优化（a bit）

### 折半插入排序

对有序区进行折半查找

小于的话就 right = mid-1

大于等于的话就 left = mid+1

**直到 left 大于 right**

然后插入在 left 的位置



~~~C++
#include <iostream>
using namespace std;
const int N = 1010;
int a [N];
int main()
{
    int n;
    cin >> n;
    
    for(int i = 1; i <=n;i++)cin> > a [i];
    if(n == 1)
    {
        cout << a [1];
        return 0;
    }
    int j;
    int l, r;
    for(int i = 2; i <= n; i++)//每次在遍历时都保证了前面是有序的了
    {
       if(a [i] < a [i-1])//一旦发现不满足的就二分查找能插入的位置
       {
           a [0] = a [i];
         l = 1, r = i-1;
           while(l < r)
           {
               int mid = l+r >> 1;
               if(a [mid] > a [0])//二分逻辑注意
                r = mid-1;
               else 
               l = mid+1;
           }//如果找不到
          if(a [l] > a [0])//也就是都比之前小的话
            l = 0;
            
            //统一后移让出位置
              for(j = i-1; j >= l+1; j--)
              a [j+1] = a [j];
               
              a [j+1] = a [0];
           
       }
  
     
      
       
    }
    for(int i = 1; i <= n; i++)cout << a [i] << " ";
    return 0;
}
~~~



## 8.希尔（shell）排序

**与开放寻址法的避免冲突类似都有一个增量**（Δ 变化量）

![image-20250105164405234](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105164405234.png)

**如图增量是 2！**

**优化的插入排序**

思路：

**增量依次折半**

![image-20250105164535770](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250105164535770.png)



~~~C++
#include <iostream>
using namespace std;
const int N = 1e5+10;
int a [N];
int main()
{
    int n;
    cin >> n;
    for(int i = 1; i <=n;i++)cin> > a [i];
    int j;
    for(int d = n/2; d >= 1; d/= 2)
    {
        for(int i = d+1; i <= n; i++)
        {
            if(a [i] < a [i-d])//一旦发现子集中有一个大于 a [0]
            {
                a [0] = a [i];//暂存这个值
                //插入排序步骤
                for(j = i-d; j > 0&&a [j] > a [0]; j-= d)//枚举这个子集
                a [j+d] = a [j];
                a [j+d] = a [0];
                
            }
        }
    }


    for(int i = 1; i <= n; i++)cout << a [i] <<' ';
    return 0;
}
~~~





