[微积分本质](https://www.bilibili.com/video/BV1ob411y7L9/?spm_id_from=333.1387.homepage.video_card.click&vd_source=9570fc9c9829e70449f020506364bf36)

[线性代数本质](https://www.bilibili.com/video/BV1ob411y7L9/?spm_id_from=333.1387.homepage.video_card.click&vd_source=9570fc9c9829e70449f020506364bf36)

# 向量本质

在数学和物理中，向量默认都写成**列向量**，因为这样更方便和矩阵做线性变换。

行向量常用在**转置**、**数据表的行表示**，或者机器学习里表示一个样本的特征



# 线性组合 ：张成的空间与基

**数字在线性代数中起到的主要作用就是缩放向量**



**数乘**：一个向量的伸缩。

**线性组合**：很多个数乘之后的向量加法。

![image-20250825142422722](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825142422722.png)

<span style="font-size:1.1em;"> 也就是说它们如何**拉伸或压缩**一个**向量**</span>

<span style="font-size:1.2em; color:#FF0000;">**每当我们用数字描述向量时，它都依赖于我们正在使用的基**</span>

![**image-20250825142537948**](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825142537948.png)





![image-20250825143310716](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825143310716.png)

![image-20250825143326165](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825143326165.png)



所有可以表示为给定向量线性组合的向量的集合 被称为**给定向量** **张成的空间(span)**![image-20250825143515817](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825143515817.png)



当你只考虑一个向量时，就把它看作**箭头**

当你考虑多个向量时，就把它们都看作**点**



一组向量中至少有一个是多余的，没有对张成空间做出任何贡献，你有多个向量，并且可以移除其中一个而不减小张成的空间

**三个向量是线性相关的”**，意思就是：

这三根向量里面，至少有一根是可以用另外两根“拼出来”的。



另一种表述方法是**至少其中一个向量，可以表示为其它向量的线性组合**，因为这个向量已经落在其它向量张成的空间之中



另一方面，如果所有向量都给张成的空间增添了新的维度，它们就被称为是线性无关的





# <span style="color:#FF0000;">矩阵与线性变换</span>

变换 === 函数 接收向量输入 输出向量

![image-20250825145302179](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825145302179.png)



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825145240894.png" alt="image-20250825145240894" style="zoom:33%;" />





只需要记录两个基向量i帽和j帽变换后的位置，其他向量都会随之而动

![image-20250825150932146](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825150932146.png)

![image-20250825150916238](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825150916238.png)



一个二维线性变换仅由四个数字（变换后的 i、j帽坐标）完全确定

![image-20250825151716747](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825151716747.png)



![image-20250825151753413](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825151753413.png)





![image-20250825152101821](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825152101821.png)

<span style="color:#FF0000; font-size:1.2em;">**<span style="font-size:1.2em;">矩阵就是对空间的一种特定的变换 就是描述线性变换的 语言</span>**	</span>





# 矩阵乘法与线性变换复合的联系

![image-20250825153155392](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153155392.png)



![image-20250825153212357](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153212357.png)



因为新矩阵应当捕捉到了旋转然后剪切的相同总体效应

![image-20250825153305447](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153305447.png)

就是先应用右侧的矩阵所描述的变换，再去应用左侧矩阵所描述的变换

类似**复合函数**

![image-20250825153435262](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153435262.png)



![image-20250825153616477](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153616477.png)

![image-20250825153647483](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153647483.png)

![image-20250825153701792](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825153701792.png)





应该养成思考矩阵乘法意义的习惯 这样从本质出发更能理解到其他性质

比如矩阵乘法和顺序是有关系的 	

![image-20250825161209244](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825161209244.png)





# 三维空间的线性变换

![image-20250825161928191](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825161928191.png)

# 行列式

![image-20250825161946178](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825161946178.png)

![image-20250825162125281](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162125281.png)

 ![image-20250825162248316](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162248316.png)



![image-20250825162308982](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162308982.png)



![image-20250825162407682](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162407682.png)

也就被称为这个变换的行列式



对于一个**二维线性变换**的行列式为0的话 因为面积变为了0 （就说明无面了 就是线或是点））

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162508685.png)



**也就是说，只需要检验一个矩阵的行列式是否为0，我们就能了解这个矩阵所代表的变换是否将空间压缩到更小的维度上**、

像如果是三维线性变换 就是被压缩为一个面、线或者点

![image-20250825162754865](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162754865.png)



![image-20250825162814898](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162814898.png)



![image-20250825162822655](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825162822655.png)

**当空间定向改变的情况发生时，行列式为负**

  

对于三维的定向 右手法则

![image-20250825163222654](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825163222654.png)

思考：



![image-20250825163825362](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825163825362.png)

---




# 逆矩阵、列空间、秩与零空间

 ![image-20250825164120329](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825164120329.png)

意味着我们要去寻找 一个向量x 使得它在变换后与V重合 这就是**线性方程组的本质**

![image-20250825164347236](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825164347236.png)

是将空间挤压到一条线或一个点等低维空间，还是保持像初始状态一样的完整二维空间

因此，我们将它们分为两种情况：A的行列式为零和A的行列式不为零



<span style="color:#FF0000; font-size:1.1em;">重要！！！！！！ </span>

<span style="color:#FF0000; font-size:1.5em; font-weight:bold;">对于后者，有且只有一个向量（在变换后）是与v 重合的，并且可以通过逆向进行变换来找到这个向量</span>

也就是通过v（已知的结果的逆向过程也能跟踪到x的逆向过程）





![image-20250825164749809](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825164749809.png)

![image-20250825164820878](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825164820878.png)

![image-20250825164857855](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825164857855.png)

对于前者，如果是这样的话 那么行列式就是为零 

所以就不存在逆矩阵

![image-20250825165348929](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825165348929.png)

![image-20250825165453113](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825165453113.png)

![image-20250825171118337](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825171118337.png)

如果v不在直线上就说明解不存在

![image-20250825174403991](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825174403991.png)

![image-20250825174518787](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825174518787.png)

矩阵的列告诉你基向量变换后的位置, 这些变换后的基向量张成的空间就是所有可能的变换结果

![image-20250825175445905](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825175445905.png)

所以更精确的**秩的定义是列空间的维数**

 满秩：当秩达到最大值时，意味着秩与列数相等



![image-20250825175648479](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825175648479.png)

但是对一个非满秩的矩阵来说，它将空间压缩到一个更低的维度上

变换后落在原点的向量的集合， 被称为矩阵的“零空间”或“核” 

 变换后一些向量落在零向量上，而“零空间正是这些向量所构成的空间

![image-20250825180053106](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825180053106.png)



零空间给出的就是这个向量方程所有可能的解

# 非方阵（几何意义） 不同维度空间之间的线性变换

**重点在输入输出**



![image-20250825180505681](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825180505681.png)

但是这个矩阵还是满秩的 为什么 ： 列空间为二维 所以秩就是2 而这个矩阵最多就两个列

![image-20250825181005738](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825181005738.png)

![image-20250826132340687](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826132340687.png)

**行数m** 决定**输出向量的维度**

如果矩阵有 m 行，那么矩阵乘向量得到的结果就是一个 **m 维向量**

换句话说，每一行对应**输出向量的一个坐标分量**



**列数 n** 决定**输入向量的维度**

如果矩阵有 n 列，那么它可以乘一个 n 维向量

每一列表示**输入向量对应基向量在输出空间的映射**





因为矩阵有两列，表明输入空间有两个基向量

有三行表明每一个基向量在变换后都**用三个独立的坐标来描述。** 





---



![image-20250825181606364](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825181606364.png)



![image-20250825181647245](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825181647245.png)


![image-20250825181859717](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825181859717.png) 


![image-20250825182013171](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825182013171.png)



# ==点积与对偶性==

![image-20250825184014937](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825184014937.png)



![image-20250825184042438](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825184042438.png)





---



# ==叉积==

 ![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825184810857.png)







## 叉积的标准介绍



![image-20250825185032736](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825185032736.png)



![image-20250825185139991](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825185139991.png)



对于平行四边形 当对角线垂直时面积最大

![image-20250825185712866](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825185712866.png)

真正的叉积是通过两个三维向量生成一个新的三维向量

也就是叉积的结果是一个向量而不是一个数	

![image-20250825185914916](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825185914916.png)



![image-20250825185940441](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250825185940441.png)

![image-20250826073906796](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826073906796.png)

## 以线性变换的眼光看叉积

上述公式的意义，与对偶性有关 





---



# 基变换

向量就看作 为缩放基向量的标量 然后之和就是向量



主要问题：一个**向量**在**一个坐标系**中的表示如何在**另一个坐标系**中表示

![image-20250826074614867](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826074614867.png)

![image-20250826074724010](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826074724010.png)

<span style="font-family:serif;">   <span style="color:#FF0000;">注意和**线性变换**的关系</span></span>

<span style="font-family:serif;">**基变换**：换视角（坐标系），世界不动，箭头不动。</span>

<span style="font-family:serif;">**基的像**：世界动了（线性变换作用），箭头真的跑到新位置。</span>



<span style="font-family:serif;">**线性变换**：把向量真的搬动，空间里的箭头换地方。</span>

<span style="font-family:serif;">**基变换**：箭头没动，但你换了坐标系，需要重新算它的坐标。基变化了</span>



<span style="font-family:serif;">线性变换 **会把基向量映射到新的向量**，这组新向量就是“基的像” 但是基是没变的</span>

然后原来的输入向量根据 基的像 生成输出向量 这个输出向量是基于 基的（不是基的像）

**<span style="font-family:serif; color:#FF0000; font-weight:bold; font-size:1.4em;">向量是根据基线性组合的</span>**

---

只是这里的基变换可以理解为一个线性变换 只是这个 是将基线性变换了

这个矩阵的列代表的是用我们的语言表达的其他人的基向量，

将矩阵向量乘法理解为应用一个特定的线性变换

这个矩阵的列代表的是用我们的语言表达的其他人的基向量，变换为其他人的基向量，也就是她眼中的(1,0)和(0,1)

  ![image-20250826075059764](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826075059764.png)



![image-20250826075333356](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826075333356.png)



她那如何描述同样的空间90°旋转呢

<span style="text-decoration:line-through;"></span>

![image-20250826080137015](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826080137015.png)

它接收用她语言描述的向量，并输出用她语言描述的变换后的向量

上述2 -1

​		1  1 矩阵 也就是我们语言描述的她的基向量

![image-20250826080400116](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826080400116.png)

而外侧两个矩阵代表着转移作用，也就是视角上的转化

矩阵乘积仍然代表着同一个变换，只不过是从其他人的角度来看的



# 特征向量与特征值

![image-20250826110325316](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826110325316.png)

![image-20250826110538652](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826110538652.png)

将数乘改为向量乘积的形式 （重要思想！！！）

![image-20250826111120546](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826111120546.png)



![image-20250826111258832](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826111258832.png)

如果v就是零向量这个等式就是恒成立

当且仅当矩阵代表的变换将空间压缩到更低的维度时，才会存在一个**非零向量**，使得矩阵和它的乘积为零向量



当λ在改变时

![](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250826111830374.png)

目标时找到一个 λ 使得这个行列式为零

![image-20250826112241583](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826112241583.png)

计算就和求解线性方程组一样  求出特征向量





![image-20250826112753092](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826112753092.png)



![image-20250826112739269](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826112739269.png)



![image-20250826113116704](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826113116704.png)



![image-20250826113126662](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250826113126662.png)

矩阵的对角元是它们所属的特征值

**特征基**就是由矩阵所有线性无关的特征向量构成的向量空间基

**矩阵对角化**

- 如果矩阵 AAA 可以找到特征基 V=[v1,...,vn]V = [v_1, ..., v_n]V=[v1,...,vn]

- 则有：

  V−1AV=diag(λ1,...,λn)V^{-1} A V = \text{diag}(\lambda_1, ..., \lambda_n)V−1AV=diag(λ1,...,λn)

- 也就是说，矩阵在特征基下变成对角矩阵，计算更简单。

**理解矩阵变换方向**

- 在特征基下，每个向量方向只会被放大或缩小（乘以对应特征值），不会旋转
- 直观上可以把矩阵看成沿特征基方向的“伸缩器

---





