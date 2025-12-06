[20问](https://www.bilibili.com/video/BV1Ys4y1J7iY/?spm_id_from=333.337.search-card.all.click&vd_source=9570fc9c9829e70449f020506364bf36)

# 表设计



日志表（api表）

数据字典表 存储一些文档信息、说明信息、规则信息等



表名前缀直接区分表所属的业务模块，明确表的功能范围：

1. **系统管理模块所有表：`SYS_`**
2. **业务字典代码表：`DICT_`**
   - 存储系统中通用的字典数据（如状态、类型、分类等固定选项），供其他业务表引用。
   - 示例：`DICT_ORDER_STATUS`（订单状态字典：待支付 / 已发货 / 已完成等）、`DICT_USER_TYPE`（用户类型字典：个人 / 企业等）。

# Sql 思维题

分组的用法

as别名的用法

case 这种逻辑语句的应用

## 如何对比sql性能



> **数据统计SQL**

~~~sql
SELECT
    age_group,
    COALESCE(SUM(total), 0) AS total,
    COALESCE(SUM(CASE WHEN status = 8 THEN total END), 0) AS check_in,
    COALESCE(SUM(CASE WHEN sex = 1 THEN total END), 0) AS female,
    COALESCE(SUM(CASE WHEN sex = 2 THEN total END), 0) AS male,
    COALESCE(SUM(CASE WHEN nursing_area = 1 THEN total END), 0) AS self,
    COALESCE(SUM(CASE WHEN nursing_area = 2 THEN total END), 0) AS half,
    COALESCE(SUM(CASE WHEN nursing_area = 3 THEN total END), 0) AS full
FROM (
         SELECT
             COUNT(1) AS total,  -- 子组计数
             sex,
             status,
             nursing_area,
             -- 子查询中定义年龄分组别名
             CASE
                 WHEN age < 60 THEN 1
                 WHEN age BETWEEN 60 AND 69 THEN 2
                 WHEN age BETWEEN 70 AND 79 THEN 3
                 WHEN age BETWEEN 80 AND 89 THEN 4
                 WHEN age BETWEEN 90 AND 99 THEN 5
                 WHEN age >= 100 THEN 6
                 END AS age_group
         FROM `wait_application`
         WHERE status != 0
           AND apply_type = 1
           AND create_at >= '2023-01-01'
           AND create_at < '2024-01-01'
         -- 子查询 GROUP BY 直接使用别名，消除重复 CASE
         GROUP BY age_group, sex, status, nursing_area
     ) AS a
GROUP BY age_group;  -- 主查询同样使用别名
~~~

**优化：**

~~~sql
SELECT
    -- 先定义年龄分组的别名 age_group
    CASE
        WHEN age < 60 THEN 1
        WHEN age BETWEEN 60 AND 69 THEN 2
        WHEN age BETWEEN 70 AND 79 THEN 3
        WHEN age BETWEEN 80 AND 89 THEN 4
        WHEN age BETWEEN 90 AND 99 THEN 5
        WHEN age >= 100 THEN 6
        END AS age_group,
    -- 总数量
    COALESCE(COUNT(1), 0) AS total,
    -- 状态为8的数量
    COALESCE(SUM(CASE WHEN status = 8 THEN 1 ELSE 0 END), 0) AS check_in,
    -- 其他指标...
    COALESCE(SUM(CASE WHEN sex = 1 THEN 1 ELSE 0 END), 0) AS female,
    COALESCE(SUM(CASE WHEN sex = 2 THEN 1 ELSE 0 END), 0) AS male,
    COALESCE(SUM(CASE WHEN nursing_area = 1 THEN 1 ELSE 0 END), 0) AS self,
    COALESCE(SUM(CASE WHEN nursing_area = 2 THEN 1 ELSE 0 END), 0) AS half,
    COALESCE(SUM(CASE WHEN nursing_area = 3 THEN 1 ELSE 0 END), 0) AS full
FROM `wait_application`
WHERE status != 0
  AND apply_type = 1
  AND create_at >= '2023-01-01'
  AND create_at < '2024-01-01'
-- 直接使用别名分组，消除冗余
GROUP BY age_group;
~~~



# mysql 基础

## sql标签

`<trim>` 标签：灵活处理 SQL 片段的前后缀

- **核心作用**：自定义添加或删除 SQL 片段的前缀、后缀，比 `<where>` 更灵活（`<where>` 是 `<trim>` 的特殊场景）。

`<where>` 标签：智能处理 WHERE 子句的前缀

- **核心作用**：自动补全 `WHERE` 关键字，同时去掉条件最前面多余的 `and` 或 `or`，避免出现 `where and ...` 这种语法错误。

`<foreach>` 标签：循环遍历集合，生成批量 SQL

- **核心作用**：遍历数组、List 等集合，把集合元素拼接到 SQL 中（比如 `in` 条件、批量插入的 values 等）。

- 常用属性：

  - `collection`：要遍历的集合名称（如参数中的 list、array）；
  - `item`：遍历到的单个元素的别名；
  - `separator`：元素之间的分隔符（如 `,`）；
  - `open`：循环开始时拼接的字符串（如 `(`）；
  - `close`：循环结束时拼接的字符串（如 `)`）。

  

  

`<choose>` + `<when>` 标签：多条件 “二选一 / 多选一”

- **核心作用**：类似 Java 的 `switch-case`，只执行第一个满足条件的 `<when>`，不满足则执行 `<otherwise>`（可选），避免多条件冲突。
- **场景**：多个条件中只能生效一个（比如 “按姓名查” 和 “按手机号查” 二选一）。



## sql片段

像mybatis 的 exmaple就被动态sql 和mybatisplus 条件构造器  取代了 所以使用最好要自己评估 就和评估ai一样 如何评估呢 不能单单从简单考虑

include标签引入

SQL 片段是可复用的 SQL 语句片段（如查询条件、字段列表、子查询等）

**常常和动态sql结合**

## SQL 可能会返回 NULL 的情况

1. **聚合函数，聚合某个数据集是空的（特别的如count 不会）**
2. **字段无 NOT NULL 约束**
3. **子查询返回无结果**
4. **外连接的时候**

---



NoSQL指非关系型数据库 ，主要代表：MongoDB，Redis。NoSQL 数据库逻辑上提供了不同于二维表的存储方式，存储方式可以是JSON文档、哈希表或者其他方式。

![image-20250925224046152](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925224046152.png)



![image-20250928091049532](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250928091049532.png)



![image-20250925224048110](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250925224048110.png)

**第一范式（1NF）：要求数据库表的每一列都是不可分割的原子数据项。**

第二范式需要确保数据库表中的每一列都和主键相关，而不能只与主键的某一部分相关（主要针对联合主键而言）。

**第三范式需要确保数据表中的每一列数据都和主键直接相关，而不能间接相关。**

---

![image-20250925225206141](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925225206141.png)

**如何避免重复插入数据？**

选择哪种方法取决于具体的需求：

如果需要保证全局唯一性，使用UNIQUE约束是最佳做法。
如果需要插入和更新结合可以使用ON DUPLICATE KEY UPDATE。
对于快速忽略重复插入，INSERT IGNORE是合适的选择。



`INT(1)` 和 `INT(10)` 的区别主要在于 **显示宽度** 也就是 zerofill 补零显示

外键约束的作用是维护表与表之间的关系，确保数据的完整性和一致性。





**MySQL的关键字in和exist**

**在MySQL中，IN 和 EXISTS** 都是用来处理子查询的关键词，但它们在功能、性能和使用场景上有各自的特点和区别。

![image-20250925233459744](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925233459744.png)


对于普通子查询：

~~~sql
SELECT name
FROM student
WHERE class_id IN (SELECT class_id FROM class);
~~~



MySQL 会先执行子查询，把结果生成一个临时集合，例如 `{101, 102}`

然后外层表 student 的每一行去 **匹配这个集合**

---





子查询涉及外部查询等等每一行判断是什么意思

![image-20250925234253415](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925234253415.png)

## 思考……推广

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925231820858.png" alt="image-20250925231820858" style="zoom: 50%;" />





## 基本函数



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925231532204.png" alt="image-20250925231532204" style="zoom: 67%;" />





<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925231539772.png" alt="image-20250925231539772" style="zoom:67%;" />



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925231549213.png" alt="image-20250925231549213" style="zoom:67%;" />



**聚合函数最重要**

**连接 过滤    分组 聚合函数（计算） 分组过滤   投影 去重  排序 分页**

- 有`GROUP BY`时：聚合函数作用于**每个分组**，每个分组返回一行统计结果（比如按 age_group 分组后，每个年龄段算一个 total）；
- 无`GROUP BY`时：聚合函数作用于**整个查询结果集**（所有满足 WHERE 条件的记录视为 “一个大组”），最终只返回一行统计结果。

![image-20250925230943455](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925230943455.png)

## Mysql 执行计划



# ==存储引擎==

![image-20250926085606782](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250926085606782.png)

![image-20250926085620133](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250926085620133.png)

![image-20250926085631401](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250926085631401.png)

![image-20250926085639918](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250926085639918.png)



# ==索引==

**本质就是优化 插入 删除 更新 查询 时数据结构的效率**

**堆**

- 常见的是**二叉堆**（Binary Heap）。
- 是一棵**完全二叉树**（每层都尽量填满，节点靠左对齐）。
- 满足堆序性质：
  - 大顶堆：任意节点 ≥ 其子节点。
  - 小顶堆：任意节点 ≤ 其子节点。
- **特点**：父子有序，但兄弟之间无序。

**二叉搜索树（BST）**

- 左子树所有节点 < 根节点 < 右子树所有节点。
- 没有形状限制，可以是偏斜的（不一定是完全二叉树）。
- **特点**：整棵树有序，中序遍历得到升序序列



可能会失衡成**链表**

----

**平衡二叉树**（AVL 树）

查找插入构建删除的过程和二叉搜索树一致 

**区别唯一的就是 失去平衡的时候需要调整**‘

旋转操作调整：左旋、右旋



---

**红黑树**

也是对二叉搜索树进行平衡 但是平衡的策略不一样

![image-20250927102031669](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927102031669.png)



任意结点到所有叶子结点路径的黑色结点数量都是相同的

![image-20250927102314012](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927102314012.png)

---

以上的数据都是在**内存**当中处理的 所以数据量通常不会很大

 <img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927102821736.png" alt="image-20250927102821736" style="zoom: 25%;" />

![image-20250927102955587](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927102955953.png)

**B树（B-树）**

本质也是一种平衡搜索树--- 多叉平衡搜索树

![image-20250927103233554](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927103233554.png)

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927103721259.png" alt="image-20250927103721259" style="zoom: 50%;" />



![image-20250927104710080](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927104710080.png)

**插入：上溢出**

**删除：下溢出**





**B+树**

![image-20250927110134054](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927110134054.png)



 一个元素就对应着一个分支 （所以就没有左右子树的概念了）

 每一层都是对下一层的索引

所以b+树就是一个多级索引结构

![image-20250927110831372](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927110831372.png)



![image-20250927110929229](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927110929229.png)

b+树的查找最后一定会落在叶子结点上

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927152646703.png" alt="image-20250927152646703" style="zoom:50%;" />

![image-20250927153016423](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927153016423.png)

![image-20250927153205491](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927153205491.png)

![image-20250927153948044](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927153948044.png)



![image-20250927154112628](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927154112628.png)

![image-20250927154612855](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927154612855.png)

---



这个问题是数据库索引为什么用 **B+ 树** 的灵魂之问，咱们拆开聊：



* **内存访问**：纳秒级。
* **磁盘 I/O**：毫秒级，差了 10⁶ 倍。
  数据库检索的瓶颈通常在磁盘读写，所以 **索引结构必须减少磁盘访问次数**。



* **B 树**：
  每个节点都存 **键 + 数据（记录）**，叶子和非叶子节点都可以存数据。
  查找一个范围时，可能要在多层节点里“到处扫”。

* **B+ 树**：

  * **非叶子节点只存键，不存数据**，所以一个节点能放下更多的键。
  * 所有数据都存放在叶子节点，并且 **叶子节点之间用链表相连**。

---



**更高的分支因子（fan-out）**

* 因为非叶子节点只存 key，不存 value，所以同样大小的磁盘页可以容纳更多的 key。
* 结果是 **树的高度更低**。
* 高度低 = 查找路径上的磁盘访问次数更少。

1. **顺序访问更高效**

   * B+ 树的叶子节点链表，让范围查询、排序查询只需要顺着链表扫描。
   * 避免了 B 树在多层节点中“跳来跳去”，大大减少磁盘随机 I/O。

2. **更适合磁盘页存储**

   * 数据库的存储单元通常是 **页（page）**，比如 4KB。
   * B+ 树节点可以恰好映射到一个页，I/O 时整页读写。
   * 高扇出 + 页优化，使得磁盘访问次数大幅下降。



假设一个磁盘页能放下 100 条 key：

* **B 树**：每层节点还要存 value，能放的 key 可能 < 50，树高更大。
* **B+ 树**：非叶子节点只存 key，每层能放 100 个 key，分支更宽，树高更低。

查找 1000 万条数据时：

* B 树可能需要访问 **3~4 次磁盘**。
* B+ 树只需要 **2~3 次磁盘**。

![image-20250927155222553](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927155222553.png)

---

### 索引分类



![image-20250927155304449](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927155304449.png)



![image-20250927155629846](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927155629846.png)



![image-20250927160032304](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927160032304.png)



![image-20250927160106074](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927160106074.png)



### 覆盖索引、超大分页优化

![image-20250927160534494](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927160534494.png)

![image-20250927160602584](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927160602584.png)

### 

![image-20250927161037919](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927161037919.png)



**延迟关联：**

![image-20250927163827202](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927163827202.png)





### 索引创建的原则

![image-20250927164331590](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927164331590.png)

**对于第7点：**就是不要让优化器额外消耗性能判断是否为NULL

### 什么情况下索引会失效

**对于联合索引：最左列决定了树的分支方向。**

~~~css
             [李四,30]
            /        \
      [张三,25]      [王五,28]
      /      \       /      \
[张三,20] [张三,25] [王五,22] [王五,28]

~~~

![image-20250927164857853](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927164857853.png)



![image-20250927164949516](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927164949516.png)

![image-20250927165037367](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165037367.png)



![image-20250927165053229](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165053229.png)

![image-20250927165119558](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165119558.png)



![image-20250927165147371](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165147371.png)

![image-20250927165201310](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165201310.png)

### sql优化的经验

![image-20250927165219881](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165219881.png)

`UNION` 会 **自动去重**

`UNION ALL` **不去重**，保留所有重复记录

![image-20250927165820682](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927165820682.png)



![image-20250927170000824](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927170000824.png)



---

# 事务

![image-20250925232327816](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925232327816.png)



MySQL 服务端是允许多个客户端连接的，这意味着 MySQL 会出现同时处理多个事务的情况。

那么在同时处理多个事务的时候，就可能出现**脏读（dirty read）、不可重复读（non-repeatable read）、幻读（phantom read）**的问题。

![image-20250925232406534](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925232406534.png)



![image-20250925232415217](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925232415217.png)



![image-20250925232424095](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925232424095.png)





![image-20250925232454946](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925232454946.png)

mysql的默认级别是 **可重复读**



==**mysql的是怎么解决并发问题的？**==
**锁机制：**Mysql提供了多种锁机制来保证数据的一致性，包括行级锁、表级锁、页级锁等。通过锁机制，可以在读写操作时对数据进行加锁，确保同时只有一个操作能够访问或修改数据。

**事务隔离级别：**Mysql提供了多种事务隔离级别，包括**读未提交、读已提交、可重复读和串行化**。通过设置合适的事务隔离级别，可以在多个事务并发执行时，控制事务之间的**隔离程度**，**以避免数据不一致的问题。**

**MVCC（多版本并发控制）**：Mysql使用MVCC来管理并发访问，它通过在数据库中保存不同版本的数据来实现不同事务之间的隔离。**在读取数据时，Mysql会根据事务的隔离级别来选择合适的数据版本，从而保证数据的一致性。**



# 锁

![image-20250925235118859](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235118859.png)





![image-20250925235212834](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235212834.png)



![image-20250925235219048](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235219048.png)

# ==日志==

![image-20250925235315787](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235315787.png)





# ==性能调优==



![image-20250925235421276](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235421276.png)



![image-20250925235434153](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925235434153.png)

![image-20250927170036787](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927170036787.png)

![image-20250927171322421](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927171322421.png)



 ![image-20250927171642128](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927171642128.png)

![image-20250927171713869](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927171713869.png)



# ==架构==



## ==MVCC==

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927171750163.png)







## 主从同步原理

![image-20250927175354517](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927175354517.png)

![image-20250927175416242](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927175416242.png)

## ==分库分表==

