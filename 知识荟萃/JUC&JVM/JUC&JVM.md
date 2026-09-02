```ad-important
### 一、无锁机制的基础场景（最常见）

如果直接通过常规工具（如 `vim` 普通模式、`nano`、FTP 直接编辑、Windows 远程桌面共享文件）修改同一文件，会出现两种典型问题：

1. **后保存者覆盖先保存者的修改**
    
    - 假设主机 A 和主机 B 同时打开 `/etc/nginx/nginx.conf`：
        - 主机 A 先修改了端口为 `8080` 并保存；
        - 主机 B 此时看到的还是修改前的端口 `80`，接着修改了根目录为 `/usr/local/html` 并保存；
    - 最终文件只会保留主机 B 的修改，主机 A 的端口修改会被**完全覆盖**，导致 A 的变更丢失。
    - 本质原因：常规编辑工具是**先读取文件到本地缓存**，保存时直接用本地缓存覆盖服务器文件，不会感知其他用户的修改。
2. **文件内容错乱（二进制 / 大文件场景）**
    
    - 若修改的是二进制文件（如图片、视频、数据库文件）或超大文本文件，多用户同时写入时，文件会出现**内容拼接 / 乱码**：
        - 比如主机 A 写入字节段 `[01,02,03]`，主机 B 同时写入 `[04,05,06]`，最终文件可能变成 `[01,04,02,05,03,06]` 这类错乱数据，直接导致文件失效。

### 二、有基础锁机制的场景（部分工具支持）

部分编辑工具内置了**文件锁**或**版本提示**，能降低覆盖风险，但无法完全避免：

1. **`vim` 的交换文件锁**
    
    - 当主机 A 用 `vim` 打开文件时，会自动生成一个**交换文件**（如 `.nginx.conf.swp`），标记文件为 “已编辑”；
    - 若主机 B 再用 `vim` 打开同一文件，会收到提示：`Swap file ".nginx.conf.swp" already exists!`，并给出选项（只读打开、恢复、退出等）；
    - 但这种锁是**弱锁**：如果主机 B 强制选择 “删除交换文件并编辑”，依然会覆盖主机 A 的修改；且如果主机 A 异常退出（如断网），交换文件会残留，导致后续编辑报错。
2. **部分 IDE / 协作工具的版本提示**
    
    - 一些远程开发 IDE（如 VS Code Remote）会监测文件的**修改时间戳**：如果本地缓存的文件版本早于服务器文件的最新版本，会提示 “文件已被外部修改”，询问是否重载最新版本；
    - 但该机制仅能提醒，无法阻止用户强行覆盖，若用户选择 “不重载并保存本地版本”，依然会覆盖他人修改。
```

# Juc基础

## 并发控制

在并发编程中，保持并发控制的核心是**协调多个线程对共享资源的访问**，避免数据错乱或不一致。常见的办法可以按「控制粒度」和「实现机制」分为以下几类，涵盖从基础到高级的解决方案：


### 一、基于锁机制（最常用）
通过「加锁」限制同一时间只有一个/部分线程访问共享资源，是最经典的并发控制方式。

1. ** synchronized 关键字（Java 内置）**  
   - 作用：修饰方法或代码块，保证同一时间只有一个线程执行被修饰的内容。  
   - 原理：依赖 JVM 内置锁（对象监视器 `monitor`），自动实现加锁/释放锁（无需手动操作）。  
   - 场景：简单的同步场景（如单例模式、简单计数器），但锁粒度较粗（锁整个对象或类），高并发下可能影响性能。

2. **显式锁（Lock 接口）**  
   - 代表类：`ReentrantLock`（可重入锁）、`ReentrantReadWriteLock`（读写锁）。  
   - 特点：需手动调用 `lock()` 加锁、`unlock()` 释放锁（通常配合 `try-finally`），支持更灵活的控制（如超时锁、中断锁、公平锁）。  
   - 优势：  
     - 读写锁（`ReadWriteLock`）支持「多线程读、单线程写」，适合读多写少场景（比 `synchronized` 更高效）；  
     - 可实现公平锁（按线程等待顺序获取锁），避免线程饥饿。

3. **分布式锁（跨进程场景）**  
   - 适用：多台服务器（进程）共享资源（如分布式缓存、数据库）时的并发控制。  
   - 实现方式：  
     - 基于 Redis：用 `SET NX` 命令抢锁，`EXPIRE` 设置超时时间；  
     - 基于 Zookeeper：通过临时节点和Watcher机制实现锁的获取与释放；  
     - 基于数据库：用 `SELECT ... FOR UPDATE` 行锁或唯一索引实现。  


### 二、基于原子操作（无锁机制）
通过「CAS（Compare And Swap，比较并交换）」实现无锁并发控制，避免锁的开销，适用于简单变量的更新。

1. **原子类（Java `java.util.concurrent.atomic` 包）**  
   - 代表类：`AtomicInteger`、`AtomicLong`、`AtomicReference` 等。  
   - 原理：利用 CPU 底层指令（如 `cmpxchg`）实现原子操作，无需加锁：  
     1. 读取当前值 `V`；  
     2. 计算目标值 `N`（基于 `V`）；  
     3. 若当前值仍为 `V`，则更新为 `N`，否则重试（自旋）。  
   - 场景：计数器、序号生成器等简单共享变量的并发更新，性能优于锁机制。

2. **Unsafe 类（底层支持）**  
   - 提供 CAS 操作的底层 API（如 `compareAndSwapInt`），是原子类的实现基础，需谨慎使用（直接操作内存，不安全）。


### 三、基于并发工具类（高级协调机制）
通过 JDK 提供的工具类实现线程间的协作，而非直接控制资源访问。

1. **信号量（Semaphore）**  
   - 作用：限制同时访问共享资源的线程数量（类似“许可证”机制）。  
   - 用法：初始化时指定许可证数量，线程通过 `acquire()` 获取许可证，`release()` 释放，无许可证时线程阻塞。  
   - 场景：控制并发连接数（如数据库连接池限制最大连接数）。

2. **倒计时器（CountDownLatch）**  
   - 作用：让主线程等待多个子线程完成后再继续执行（类似“发令枪”）。  
   - 用法：初始化时指定倒计时次数，子线程完成后调用 `countDown()` 减 1，主线程调用 `await()` 阻塞等待计数归 0。  
   - 场景：并发任务汇总（如多个线程加载数据，全部完成后主线程处理结果）。

3. **循环屏障（CyclicBarrier）**  
   - 作用：让多个线程到达某个屏障点后再同时继续执行（可重复使用）。  
   - 用法：初始化时指定参与线程数，线程到达后调用 `await()` 等待，所有线程到达后一起执行后续逻辑。  
   - 场景：分阶段任务（如多个线程先完成第一阶段计算，再同时开始第二阶段）。

4. **线程池（ExecutorService）**  
   - 作用：通过控制线程数量避免线程过多导致的资源耗尽，间接实现并发控制。  
   - 核心：通过线程池的核心线程数、最大线程数、队列等参数，限制并发执行的线程数量，避免线程切换开销过大。  


### 四、基于数据结构（规避并发冲突）
使用线程安全的数据结构，从底层避免并发问题，无需手动加锁。

1. **线程安全集合（JDK 提供）**  
   - `List`：`CopyOnWriteArrayList`（读多写少）；  
   - `Map`：`ConcurrentHashMap`（高并发键值对）；  
   - `Queue`：`ConcurrentLinkedQueue`（无锁队列）、`BlockingQueue`（阻塞队列，用于生产者-消费者模型）。  

2. **不可变对象（Immutable Objects）**  
   - 原理：对象创建后状态不可修改（所有字段 `final`），天然线程安全（无需同步）。  
   - 场景：共享配置、常量数据等，如 `String`、`Integer` 等包装类。  


### 五、基于分布式协调（跨进程/服务）
在分布式系统中，通过中间件实现多节点的并发控制，解决跨机器的资源竞争。

1. **分布式锁（如 Redis、Zookeeper，前文已提）**  
2. **分布式事务（保证跨服务数据一致性）**  
   - 实现方式：2PC（两阶段提交）、TCC（Try-Confirm-Cancel）、Saga 模式等，确保多个服务的操作要么全成功，要么全失败。  
3. **消息队列（异步解耦 + 顺序控制）**  
   - 通过消息队列的「单消费者」或「分区顺序消费」保证并发请求的有序处理（如 Kafka 分区内消息有序）。  


### 总结：选择原则
- **简单同步场景**：用 `synchronized` 或 `ReentrantLock`；  
- **读多写少场景**：用 `ReadWriteLock` 或 `CopyOnWriteArrayList`；  
- **简单变量更新**：用原子类（`AtomicXxx`）；  
- **多线程协作**：用 `CountDownLatch`、`Semaphore` 等工具类；  
- **高并发集合操作**：用 `ConcurrentHashMap` 等线程安全集合；  
- **分布式系统**：用分布式锁、消息队列或分布式事务。  





![image-20251004184800268](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004184800268.png)

## Synchronized



`synchronized` 是 Java 的**内置互斥锁（monitor / intrinsic lock）**。

它保证三件事：

1. **原子性**：同一时刻只有一个线程能进入被锁定的代码块/方法。
2. **可见性**：一个线程释放锁时，对共享变量的修改会刷新到主内存，随后获取同一锁的线程能看到这些变化。
3. **有序性**：`synchronized` 构成 `happens-before` 关系，防止一些重排序导致的不一致。

用法三种：**实例方法（锁 `this`）、静态方法（锁类对象 `Class`）**、代码块（锁任意对象 `synchronized(lock)`）。

**这种就是 针对锁的范围粒度了**

![image-20251005004753804](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20251005004753804.png)

**对于代码块**

| 写法                        | 锁的对象          | 锁的范围                 | 常见场景                   |
| --------------------------- | ----------------- | ------------------------ | -------------------------- |
| `synchronized (this)`       | 当前实例对象      | 当前对象内的同步方法互斥 | 实例级同步，如用户余额更新 |
| `synchronized (类名.class)` | 类对象（JVM唯一） | 所有该类的实例共享       | 静态变量或全局配置修改     |
| `synchronized (lockObj)`    | 自定义锁对象      | 根据自定义粒度可灵活控制 | 控制局部同步或分区锁       |



## synchronized和reentrantlock区别

**synchronized 和 ReentrantLock 都是 Java 中提供的==可重入锁==：**

**用法不同：**synchronized 可用来修饰**普通方法、静态方法和代码块**，而 ReentrantLock 只能用在**代码块上。**

**获取锁和释放锁方式不同：**synchronized 会自动加锁和释放锁，当进入 synchronized 修饰的代码块之后会自动加锁，当离开 synchronized 的代码段之后会自动释放锁。而 ReentrantLock 需要手动加锁和释放锁

**锁类型不同**：synchronized 属于**非公平锁**，而 ReentrantLock 既可以是**公平锁**也可以是**非公平锁。**

**响应中断不同：**ReentrantLock 可以响应中断，解决死锁的问题，而 synchronized 不能响应中断。

​	![image-20251005021644553](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005021644553.png)

**底层实现不同**：synchronized 是 JVM 层面通过监视器实现的，而 **ReentrantLock 是基于 AQS 实现的**





## 可重入锁 reentrantlock

~~~java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();
}
~~~





可重入锁是指同一个线程在获取了锁之后，可以再次重复获取该锁而不会造成死锁或其他问题。当一个线程持有锁时，如果再次尝试获取该锁，就会成功获取而不会被阻塞。

ReentrantLock实现可重入锁的机制是基于线程持有锁的计数器。

当一个线程第一次获取锁时，计数器会加1，表示该线程持有了锁。在此之后，如果同一个线程再次获取锁，计数器会再次加1。每次线程成功获取锁时，都会将计数器加1。
当线程释放锁时，计数器会相应地减1。只有当计数器减到0时，锁才会完全释放，其他线程才有机会获取锁。
这种计数器的设计使得同一个线程可以多次获取同一个锁，而不会造成死锁或其他问题。每次获取锁时，计数器加1；每次释放锁时，计数器减1。只有当计数器减到0时，锁才会完全释放。

ReentrantLock通过这种计数器的方式，实现了可重入锁的机制。它允许同一个线程多次获取同一个锁，并且能够正确地处理锁的获取和释放，**避免了自死锁和其他并发问题**

~~~java
public synchronized void outer() {
    inner(); // 这个方法也加了synchronized
}

public synchronized void inner() {
    // do something
}

~~~

`ynchronized` 是可重入的。`outer()` 已经获得了锁，如果它在执行中又调用了一个也加了同一把锁的 `inner()` 方法，那么**同一个线程**会再次尝试加锁。
 如果锁不可重入，那么这个线程会被自己挡在门外：
 它已经持有锁，但再次申请锁又被阻塞——**这就是“自死锁”**。



### ==非公平锁吞吐量比公平锁大==

**公平锁执行流程：获取**锁时，先将线程自己添加到等待队列的队尾并休眠，当某线程用完锁之后，会去唤醒等待队列中队首的线程尝试去获取锁，锁的使用顺序也就是队列中的先后顺序，在整个过程中，线程会从运行状态切换到休眠状态，再从休眠状态恢复成运行状态**，但线程每次休眠和恢复都需要从用户态转换成内核态，而这个状态的转换是比较慢的，所以公平锁的执行速度会比较慢。**

---



**非公平锁执行流程：**当线程获取锁时，**会先通过 CAS 尝试获取锁**，如果获取成功就直接拥有锁，如果获取锁失败才会进入等待队列，等待下次唤醒尝试获取锁。这样做的好处是，获取锁不用遵循先到先得的规则，从而避免了线程休眠和恢复的操作，这样就加速了程序的执行效率。

休眠的线程被唤醒后，并不会“立即执行”，而是重新进入一轮 **CAS 抢锁竞争**。如果这时别的线程（比如新来的 T6）刚好插队抢到了锁，那么唤醒的 T2 又要回去睡。

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005020543357.png" alt="image-20251005020543357" style="zoom: 67%;" />

**核心：CAS 并不等同于自旋。它本身只是一个 原子操作，只是负责“比较并交换内存值”。****





## ==Syncronized 锁升级的过程==







## 死锁问题 如何解决

**所以反过来想，只要破坏一个条件就可以解决死锁问题了**

![image-20251005011218081](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005011218081.png)

避免死锁问题就只需要破环其中一个条件就可以，最常见的并且可行的就是使用**资源有序分配法，**来破环环路等待条件。

那什么是资源有序分配法呢？线程 A 和 线程 B 获取资源的顺序要一样，当线程 A 是先尝试获取资源 A，然后尝试获取资源 B 的时候，线程 B 同样也是先尝试获取资源 A，然后尝试获取资源 B。也就是说，线程 A 和 线程 B 总是以相同的顺序申请自己想要的资源。

---

## ==AQS==

AQS全称为AbstractQueuedSynchronizer，是Java中的一个抽象类。 AQS是一个用于构建锁、同步器、协作工具类的工具类（框架）。



## ==CAS 与 AQS 关系==



## ==AQS 与 可重入锁==



## Atomic 原子类(基于CAS)

**原子类：**

AtomicInteger：原子整数类，提供了对整数类型的原子操作，如自增、自减、比较并交换等。通过硬件级别的原子指令来保证操作的原子性和线程安全性，避免了使用锁带来的性能开销，在多线程环境下对整数进行计数、状态标记等操作非常方便。

AtomicReference：原子引用类，用于对对象引用进行原子操作。可以保证在多线程环境下，对对象的更新操作是原子性的，即要么全部成功，要么全部失败，不会出现数据不一致的情况。常用于实现无锁数据结构或需要对对象进行原子更新的场景。

~~~scala
// 原子更新基本数据类型
Atomiclnteger
AtomicLong
AtomicBoolean
// 原子更新引用类型
AtomicReference
AtomicStampedReference
AtomicMarkableReference
// 原子更新数组
AtomicIntegerArray
AtomicLongArray
AtomicReferenceArray
//原子更新对象属性
AtomicIntegerFieldUpdater 
AtomicLongFieldUpdater
AtomicReferenceFieldUpdater
~~~

## ==CAS==



CAS 本身是 CPU 提供的原子指令。

它保证了“比较+更新”这两步操作**在 CPU 层面不可被打断**，所以本质上是**原子操作**

![image-20251005015154740](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005015154740.png)



![image-20251005015616518](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005015616518.png)

CAS操作是基于==循环重试==的机制，如果CAS操作一直未能成功，线程会一直自旋重试，占用CPU资源。在高并发情况下，大量线程自旋会导致CPU资源浪费



  CAS 的 ABA 问题是并发编程中一个**经典陷阱**，即使使用了 CAS（Compare-And-Swap）这样的原子操作，也可能引发**数据一致性问题**。

**变量值从 A 变为 B，再变回 A，CAS 操作无法发现这个变化**，从而误以为它“从未变过”

因为 CAS 只比较“当前值是否等于期望值”，**不会关心变量是否被其他线程改过，只要值一致就通过。**

如何解决 ABA 问题？ 使用带版本号的引用

<img src="C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250720003309783.png" alt="image-20250720003309783" style="zoom: 33%;" />

<img src="C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250720005051317.png" alt="image-20250720005051317" style="zoom:50%;" />

**AQS 是一个用于构建锁和同步器的底层框架如：ReentrantLock、Semaphore信号量、CountDownLatch 、ReentrantReadWriteLock 都基于它实现。**

锁的**可重入性（Reentrancy）\**是指\**同一个线程在已经持有某个锁的情况下，可以再次获取该锁而不会导致死锁或阻塞**。简单来说，线程可以“重复进入”被该锁保护的代码区域，而不会被自己持有的锁挡住。

![image-20250720012400490](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250720012400490.png)



不会重试 ！ 所以AQS 内部有两个队列 专门存放加锁失败的线程 他们会阻塞等待

**同步队列：**锁的等待队列

AQS 内部维护一个 FIFO（先进先出）的 **双向同步队列**（CLH 队列），当线程获取锁失败时会被包装成 `Node` 节点加入该队列中等待唤醒。

```java
abstract class AbstractQueuedSynchronizer {
    private transient volatile Node head;
    private transient volatile Node tail;
    // ...
}

```

每个 `Node` 包含以下重要字段：

- `Thread thread`：当前节点代表的线程

- `Node prev`、`next`：前后节点

- `int waitStatus`：表示等待状态（如：SIGNAL、CANCELLED 等）

- `Node nextWaiter`：支持共享/独占模式切换

  



当锁释放的时候与要是还有一个非队列中的线程也要获取锁：

​																										尝试直接 CAS 抢占 state（非公平会无视队列，先抢再说）

​																										抢不到就封装为 `Node` 节点加入同步队列尾部（尾插法）

​																										挂起（`LockSupport.park()`）自己，等待前驱节点释放锁并唤醒



**条件队列：**线程在等待特定条件时进入的队列 只有满足条件线程才能转义到同步队列 真正等待锁的释放

 

---

## 乐观锁和悲观锁

![image-20251005015125057](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005015125057.png)



## 进程与线程 与==协程==

程序由指令和数据组成，但这些指令要运行，数据要读写，就必须将指令加载至CPU,数据加载至内存。在指令运行过程中还需要用到磁盘、网络等设备。进程就是用来加载指令、管理内存、管理IO的。

当一个程序被运行，从磁盘加载这个程序的代码至内存，这时就开启了一个进程。

**一个线程**就是一个**指令流，**将指令流中的一条条指令以一定的顺序交给CPU执行

一   个进程之内可以分为一到多个线程。

![image-20250701092125322](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701092125322.png)

**并行与并发**

![image-20250701092234263](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701092234263.png)

![image-20250701092303150](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701092303150.png)

## 线程创建的方式有哪些

~~~java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName() + " 正在执行任务");
    }

    public static void main(String[] args) {
        MyThread t1 = new MyThread();
        t1.start(); // 启动线程
    }
}
// ——————————————————————————————————————————————————————————————————————————————————————————
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName() + " 正在执行任务");
    }

    public static void main(String[] args) {
        MyRunnable task = new MyRunnable();
        Thread t1 = new Thread(task, "线程A");
        t1.start();
    }
}
// ——————————————————————————————————————————————————————————————————————————————————————————

public class MyCallable implements Callable<Integer> {
    @Override
    public Integer call() {
        System.out.println(Thread.currentThread().getName() + " 正在计算...");
        return 123; // 带返回值
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        MyCallable task = new MyCallable();
        FutureTask<Integer> futureTask = new FutureTask<>(task);
        Thread t = new Thread(futureTask);
        t.start();

        // 获取结果（阻塞等待）
        System.out.println("结果：" + futureTask.get());
    }
}

~~~

采用线程池方式：

**缺点：**线程池增加了程序的复杂度，特别是当涉及线程池参数调整和故障排查时。错误的配置可能导致死锁、资源耗尽等问题，这些问题的诊断和修复可能较为复杂。
**优点：**线程池可以重用预先创建的线程，避免了线程创建和销毁的开销，显著提高了程序的性能。对于需要快速响应的并发请求，线程池可以迅速提供线程来处理任务，减少等待时间。并且，线程池能够有效控制运行的线程数量，防止因创建过多线程导致的系统资源耗尽（如内存溢出）。通过合理配置线程池大小，可以最大化CPU利用率和系统吞吐量。







![image-20250701092342824](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250701092342824.png)



在 Java 中，一个线程可能会**主动让出 CPU**，等待某个事件发生（比如定时、等待结果、等待锁）。

这种状态我们称为：

> **阻塞状态（Blocked / Waiting / Timed Waiting）**

例如：

| 阻塞原因           | 方法               | 状态          |
| ------------------ | ------------------ | ------------- |
| 睡眠等待时间结束   | `Thread.sleep(ms)` | TIMED_WAITING |
| 等待另一个线程结束 | `join()`           | WAITING       |
| 等待被唤醒         | `wait()`           | WAITING       |

当线程处于这些状态时，它**没有在执行任何业务代码**，而是在等待操作系统信号或对象锁。

在 Java 中，**线程不能被强制杀死**。
 这是因为线程可能：

- 正在持有锁；
- 正在执行 I/O；
- 正在写数据库；
- 正在修改共享数据。

如果你直接“暴力终止”，可能造成：

> 数据不一致、死锁、资源泄漏。

所以，Java 提供了一个**“中断标志位机制”** ——
 让线程**“自愿停止”**，不是被强制干掉。

![image-20251004223915808](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004223915808.png)

**可运行就是没有办法马上真的中断（除非是本来就在阻塞的）**

轮询中断状态”的目的，是**持续监听这个标志位的变化**。

---



**万一有事没做好呢**

**在检测到中断后，我们通常会：**

1️⃣ **设置退出标志**，告诉线程 “该准备退出了”；
 2️⃣ **清理资源（cleanup）**：关闭文件流、数据库连接、线程池；
 3️⃣ **保存状态**：如果任务可恢复，就把进度写入磁盘或缓存；
 4️⃣ **记录日志**：保证运维能追踪退出原因；
 5️⃣ **退出主循环**

---

## Sleep 和 wait 的区别

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004224820006.png" alt="image-20251004224820006" style="zoom: 50%;" />



**sleep会释放cpu吗？**
**是的，调用 Thread.sleep() 时，线程会释放 CPU，但不会释放持有的锁。**

当线程调用 sleep() 后，会主动让出 CPU 时间片，进入 TIMED_WAITING 状态。此时操作系统会触发调度，将 CPU 分配给其他处于就绪状态的线程。这样其他线程（无论是需要同一锁的线程还是不相关线程）便有机会执行。

sleep() 不会释放线程已持有的任何锁（如 synchronized 同步代码块或方法中获取的锁）。因此，如果有其他线程试图获取同一把锁，它们仍会被阻塞，直到原线程退出同步代码块。

![image-20251004224424512](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004224424512.png)

---

## Thread Local

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004232028053.png" alt="image-20251004232028053" style="zoom:33%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004232118551.png" alt="image-20251004232118551" style="zoom:33%;" />

### ==**ThreadLocal内存溢出问题**==

**link to JVM 弱引用**



## Synchronized 与 Volatile 区别

 

**Synchronized解决了多线程访问共享资源时可能出现的竞态条件和数据不一致的问题，保证了线程安全性。Volatile解决了变量在多线程环境下的可见性和有序性问题，确保了变量的修改对其他线程是可见的。**

**Synchronized:** Synchronized是一种排他性的同步机制，保证了多个线程访问共享资源时的互斥性，即同一时刻只允许一个线程访问共享资源。通过对代码块或方法添加Synchronized关键字来实现同步。

**Volatile:** Volatile是一种轻量级的同步机制，用来保证变量的可见性和禁止指令重排序。当一个变量被声明为Volatile时，线程在读取该变量时会直接从内存中读取，而不会使用缓存，同时对该变量的写操作会立即刷回主内存，而不是缓存在本地内存中。

---



## Volatile 关键字

`happens-before` 就是 **Java 内存模型规定的“可见性+有序性”契约**。
 它告诉 JVM：
 **哪些操作可以被重排，哪些必须按顺序执行，哪些写入必须对其他线程可见。**

**保证可见性**

- 当一个线程修改了 `volatile` 变量的值，其他线程能立即看到这个变化。
- **原因：写入 volatile 变量会刷新到主内存，读取 volatile 变量会从主内存获取最新值。**

**禁止指令重排（有序性保证）**

- 编译器和 CPU 在优化时可能会对指令进行重排。

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004234258117.png" alt="image-20251004234258117" style="zoom: 50%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004234355055.png" alt="image-20251004234355055" style="zoom: 50%;" />

**不保证原子性**

- `volatile` 只保证 **读/写是原子性的**
- **复合操作**（如 `count++`、`i = i + 1`）是 **读- -写** 三步：
  1. 读当前值
  2. 修改值
  3. 写回主内存

即便 `count` 是 volatile，也可能被其他线程同时修改，导致丢失更新。



## juc 包常用类

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004234900402.png" alt="image-20251004234900402" style="zoom:67%;" />

## ==如何保证多线程安全==

![image-20251004235113520](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004235113520.png)

## CyclicBarrier  

![image-20251005000018449](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005000018449.png)

## Semaphore 信号量





## CountDownLatch



## 并发集合包



## Lock接口及其实现类





---



## ==线程间通信==

线程间通信方式有哪些？
**1、Object 类的 wait()、notify() 和 notifyAll() 方法。这是 Java 中最基础的线程间通信方式，基于对象的监视器（锁）机制。**

**wait()：使当前线程进入等待状态，直到其他线程调用该对象的 notify() 或 notifyAll() 方法。**
**notify()：唤醒在此对象监视器上等待的单个线程。**
**notifyAll()：唤醒在此对象监视器上等待的所有线程。**

```java
class SharedObject {
    public synchronized void consumerMethod() throws InterruptedException {
        while (/* 条件不满足 */) {
            wait();
        }
        // 执行相应操作
    }
public synchronized void producerMethod() {
    // 执行相应操作
    notify(); // 或者 notifyAll()
}
    }
```

**2、Lock 和 Condition 接口。Lock 接口提供了比 synchronized 更灵活的锁机制，Condition 接口则配合 Lock 实现线程间的等待 / 通知机制。**

**await()：使当前线程进入等待状态，直到被其他线程唤醒。**
**signal()：唤醒一个等待在该 Condition 上的线程。**
**signalAll()：唤醒所有等待在该 Condition 上的线程。**

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class SharedResource {
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();
    public void consumer() throws InterruptedException {
        lock.lock();
        try {
            while (/* 条件不满足 */) {
                condition.await();
            }
            // 执行相应操作
        } finally {
            lock.unlock();
        }
    }

    public void producer() {
        lock.lock();
        try {
            // 执行相应操作
            condition.signal(); // 或者 signalAll()
        } finally {
            lock.unlock();
        }
    }
    }
```

**3、volatile 关键字。volatile 关键字用于保证变量的可见性，即当一个变量被声明为 volatile 时，它会保证对该变量的写操作会立即刷新到主内存中，而读操作会从主内存中读取最新的值。**



```java
class VolatileExample {
    private volatile boolean flag = false;

    public void writer() {
        flag = true;
    }

    public void reader() {
        while (!flag) {
            // 等待
        }
        // 执行相应操作
    }
}
}
```

**4、CountDownLatch。CountDownLatch 是一个同步辅助类，它允许一个或多个线程等待其他线程完成操作。**

**CountDownLatch(int count)：构造函数，指定需要等待的线程数量。**
**countDown()：减少计数器的值。**
**await()：使当前线程等待，直到计数器的值为 0。**

```java
import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        int threadCount = 3;
        CountDownLatch latch = new CountDownLatch(threadCount);  
	for (int i = 0; i < threadCount; i++) {
        new Thread(() -> {
            try {
                // 执行任务
                System.out.println(Thread.currentThread().getName() + " 完成任务");
            } finally {
                latch.countDown();
            }
        }).start();
    }

    latch.await();
    System.out.println("所有线程任务完成");
}
    }
```


**5、CyclicBarrier。CyclicBarrier 是一个同步辅助类，它允许一组线程相互等待，直到所有线程都到达某个公共屏障点。**

**CyclicBarrier(int parties, Runnable barrierAction)：构造函数，指定参与的线程数量和所有线程到达屏障点后要执行的操作。**
**await()：使当前线程等待，直到所有线程都到达屏障点。**

```java
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierExample {
    public static void main(String[] args) {
        int threadCount = 3;
        CyclicBarrier barrier = new CyclicBarrier(threadCount, () -> {
            System.out.println("所有线程都到达屏障点");
        });    
    for (int i = 0; i < threadCount; i++) {
        new Thread(() -> {
            try {
                // 执行任务
                System.out.println(Thread.currentThread().getName() + " 到达屏障点");
                barrier.await();
                // 继续执行后续任务
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
    }
```
6**、Semaphore。Semaphore 是一个计数信号量，它可以控制同时访问特定资源的线程数量。**

**Semaphore(int permits)：构造函数，指定信号量的初始许可数量。**
**acquire()：获取一个许可，如果没有可用许可则阻塞。**
**release()：释放一个许可。**

```java
import java.util.concurrent.Semaphore;

public class SemaphoreExample {
    public static void main(String[] args) {
        int permitCount = 2;
        Semaphore semaphore = new Semaphore(permitCount);    
    for (int i = 0; i < 5; i++) {
        new Thread(() -> {
            try {
                semaphore.acquire();
                System.out.println(Thread.currentThread().getName() + " 获得许可");
                // 执行任务
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                semaphore.release();
                System.out.println(Thread.currentThread().getName() + " 释放许可");
            }
        }).start();
    }
}
```
## 锁机制和无锁机制  来实现线程同步





![image-20251005004538031](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005004538031.png)







---

## 阻塞与中断

![image-20251005021206145](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005021206145.png)

![image-20251005021333350](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005021333350.png)





## 线程的生命周期（状态切换）

Java进程比较特殊 是JVM进程 



| 对比维度       | Java 进程                           | 普通本地进程（如 C/C++）       |
| -------------- | ----------------------------------- | ------------------------------ |
| **可执行文件** | `.jar` 或 `.class`（字节码）        | `.exe` 或 ELF（机器码）        |
| **执行方式**   | 借助 JVM 间接执行                   | 直接由操作系统加载并运行       |
| **跨平台性**   | ✅ 强：一次编译，到处运行            | ❌ 差：编译后只能在特定平台运行 |
| **启动命令**   | `java MyApp`（启动 JVM）            | `./myapp` 或点击 EXE           |
| **内存结构**   | Java 特有结构：堆、方法区、虚拟栈等 | 通常为 C 程序内存模型          |
| **执行时依赖** | 必须依赖 JVM                        | 可直接由 OS 支持运行           |
| **调优复杂度** | JVM 启动参数众多，可细粒度调优      | 可调部分有限或需要操作系统支持 |

###  JVM 的核心职责：

| 功能                    | 描述                                            |
| ----------------------- | ----------------------------------------------- |
| **加载类**              | 从 `.class` 或 `.jar` 文件中加载字节码          |
| **字节码解释/编译执行** | 将字节码翻译成机器码执行（解释器 + JIT 编译器） |
| **内存管理**            | 提供独立的堆空间、方法区、栈等结构              |
| **垃圾回收（GC）**      | 自动释放无用内存，避免内存泄漏                  |
| **异常处理**            | 提供运行时异常机制                              |
| **安全沙箱**            | 提供权限控制、防止恶意代码执行（早期 Applet）   |
| **平台抽象**            | 屏蔽不同操作系统差异，实现跨平台运行能力        |

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704152031379.png" alt="image-20250704152031379" style="zoom:50%;" />

![image-20250704152420645](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704152420645.png)

一旦调用了start 当前程序的**栈中**就多了一个栈，这味着当前程序多了一个**线程**

**`RUNNABLE` 表示逻辑上“可运行”**，但**实际是否正在运行是由 JVM 和操作系统的调度器决定的 **  `RUNNABLE = Ready + Running` 合并状态



![image-20250704153033835](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704153033835.png)

**如何将任务交给线程：**

![image-20250704153127576](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704153127576.png)

前两个没有返回值， 第三个使用了**线程间通信**



一个线程啥时候结束，其他线程确实不知道呀

子线程跟主线程一样，都是独立可运行的个体，相互之间是不知道对方的情况的

线程间本就是独立的，想要把返回值或者异常让其他线程知道就需要跟其他线程通信


  <img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704154030624.png" alt="image-20250704154030624" style="zoom:50%;" />

只要是函数式接口就能通过lambda函数简化

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704154300932.png" alt="image-20250704154300932" style="zoom:50%;" />

好处是我们可以在主线程中获取子线程的**返回值**，也可以在主线程中获取子线程发生的**异常**

 `FutureTask.get()` 会**阻塞当前线程**，直到：

- 后台任务执行完毕
- 得到结果后返回
- 或者抛出异常

## 线程按==顺序==执行 

![image-20250704155415228](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704155415228.png)



![image-20250704160109564](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704160109564.png)

thenCompose()方法的作用是把前面任务的结果交给下一个异步任务 

![image-20250704160225313](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704160225313.png)

`thenApply` 像是把 **数据映射成一个新值**

`thenApply` 的参数 

~~~java
<U> CompletableFuture<U> thenApply(Function<? super T,? extends U> fn)
// 参数 fn 是一个 《函数式接口》 Function<T, U>
    
~~~

| 输入（参数类型）      | 输出（返回类型）    |
| --------------------- | ------------------- |
| T（上一个阶段的结果） | U（映射后的新结果） |

`thenCompose` 像是把 **数据变成一个新的==异步任务==**，然后**接上这个新任务**



![image-20250704162057517](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704162057517.png)

thenApply就是把前面异步任务的结果交给后面的Function

| 方法               | 是否异步执行       | 执行线程在哪                                            |
| ------------------ | ------------------ | ------------------------------------------------------- |
| `thenApply()`      | ❌ 否，**同步执行** | 默认继续使用上一个阶段的线程                            |
| `thenApplyAsync()` | ✅ 是，**异步执行** | 默认使用 **ForkJoinPool.commonPool** 或你自定义的线程池 |





![image-20250704163539170](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704163539170.png)

![image-20250704164046844](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704164046844.png)



**不仅仅是学三个API而是学三种解决问题的思路 学习不仅仅要学用法更要学思想**



对于以上这五个API（除了exceptionally）

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704172159288.png" alt="image-20250704172159288" style="zoom:50%;" />









<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704172738826.png" alt="image-20250704172738826" style="zoom: 33%;" />



![image-20250704173105082](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704173105082.png)

当作一个任务提交到线程池

---

![image-20250704173131513](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704173131513.png)



 

---



## 线程池

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005012413386.png" alt="image-20251005012413386" style="zoom: 67%;" />



**corePoolSize：线程池核心线程数量。默认情况下，线程池中线程的数量如果 <= corePoolSize，那么即使这些线程处于空闲状态，那也不会被销毁**

| 多线程方案              | 描述                          | 适用场景                           |
| ----------------------- | ----------------------------- | ---------------------------------- |
| `Thread` 类             | 直接创建线程                  | 简单临时任务，不推荐大规模使用     |
| `Runnable` / `Callable` | 提交任务对象（实现接口）      | 比Thread更灵活，但仍需自己管理线程 |
| **线程池（Executor）✅** | 使用`ExecutorService`提交任务 | 推荐：高性能、可控、适合大并发     |

1. **复用线程，避免频繁创建销毁**

- Java中创建线程代价高（涉及系统调用、内存分配等）
- 线程池可以复用已有线程，节省资源



2. **控制并发量，防止系统过载**

- 线程池可以设置最大线程数、队列长度，避免无限制地开线程导致OOM或CPU打满



3. **支持任务调度与线程管理**

- 支持任务排队（阻塞队列）
- 支持线程回收、超时、命名、优先级等高级控制



 4. **便于监控与扩展**

- 可以结合监控工具、定制ThreadFactory、RejectedExecutionHandler进行运维和调优





![image-20250704174518703](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704174518703.png)

**线程工厂：**

给线程起统一的名字（方便调试）

设置为守护线程

自定义线程优先级 



**拒绝策略：**

当线程池满了（线程数 + 队列都满），再提交任务，就会被“拒绝执行”。



线程池中的“工作队列”实际上就是使用“阻塞队列”实现的，只不过“工作队列”强调的是用途和角色，而“阻塞队列”是具体的数据结构。

| 方法                        | 是否有返回值 | 是否能捕获异常               | 返回类型    | 使用场景                        |
| --------------------------- | ------------ | ---------------------------- | ----------- | ------------------------------- |
| `execute(Runnable)`         | ❌ 没有返回值 | ❌ 异常无法捕获（只能靠日志） | `void`      | 执行任务不关心结果              |
| `submit(Runnable/Callable)` | ✅ 有返回值   | ✅ 异常会包装进 `Future` 中   | `Future<T>` | 需要获取执行结果 / 控制任务状态 |

**6核12线程** 指的是这个 CPU 有 **6 个物理核心**，**每个核心支持 2 个线程** （Intel 的**超线程技术**）

一个物理核心可以模拟两个逻辑核心（线程）

![image-20250704180527857](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704180527857.png)

如何提升性能 就是要在线程池中的最大线程数和核心线程数 上 根据环境有几核几线程来设计

这个数量没有办法在一开始就知道 可以先通过瞬时的任务的数量去估算  最佳实践：**线上长期的观测**

![image-20250704181211600](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704181211600.png)



**线程池中的线程 默认是前台线程**   所以线程池用完要关闭这个资源

也可定义线程池中使里面的线程变为守护线程 



一台机器一段时间内 具体能承受多少任务 取决于 **机器配置**和 **任务需要多少资源**

---



  **什么是“六核”？**

- 六个**物理核心**（Physical Cores）：

  - 每个核心可以独立完成计算任务。
  - 是 CPU 的真正计算单元，拥有独立的算术逻辑单元（ALU）、浮点单元（FPU）、缓存（L1/L2）等。

  ---

  

**什么是“十二线程”？**

- 十二个**逻辑线程**（Logical Threads）：
  - 是通过每个物理核心**运行两个线程**实现的。
  - 这些逻辑线程**共享同一个核心的资源**，并不能等价于“12 个核心”。

---



- 现代 CPU 执行任务时，经常会因为：
  - 等内存读写（延迟）
  - 等分支预测结果
  - 等 I/O 返回数据
- 导致**部分执行资源空闲**

于是设计者想：**让一个核心在等待的时候，不如顺便再处理另一个线程的任务。**

于是就把一个物理核心“拆成两个逻辑线程”供操作系统调度。

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250704225913355.png" alt="image-20250704225913355" style="zoom: 25%;" />

## 阻塞队列

**线程通信： 本质就是控制线程的运行状态**

线程只有在 不活跃的状态 下被中断 才会触发 IE（中断异常）

多个线程在修改同一份数据 且线程间互相不知道（无法通信） 就会有问题



**阻塞队列功能**

1、队列需要有一个固定的容量
2、如果队列是空的
			自然是取不出来东西，需要等到有元素为止
3、如果队列是满的
			自然是放不进去东西，需要等到有空位为止

| 方法            | 是否阻塞     | 队列为空时        |
| --------------- | ------------ | ----------------- |
| `poll()`        | ❌ 不阻塞     | 立刻返回 `null`   |
| `poll(timeout)` | ⏳ 阻塞一会儿 | 超时后返回 `null` |
| `take()`        | ✅ 一直阻塞   | 等待直到有元素    |

`LinkedBlockingQueue` 默认使用**非公平锁**，容易在高并发下发生“线程插队”而导致不公平
什么是<公平>？
先来的消费者一定先取出来
先来的生产者一定先放进去

| 维度         | `LinkedBlockingQueue`                             | `ArrayBlockingQueue`                   |
| ------------ | ------------------------------------------------- | -------------------------------------- |
| **底层结构** | 链表（每个元素一个节点）                          | 数组（固定长度）                       |
| **容量**     | 默认 Integer.MAX\_VALUE，除非指定                 | 必须在构造函数中指定容量               |
| **内存分配** | 每插入一个元素创建一个节点（堆内存多）            | 创建时一次性分配好数组（内存开销可控） |
| **性能**     | 在高并发下较好（因为用两个锁）                    | 单锁，简单快速，但竞争高时性能差些     |
| **锁机制**   | **双锁机制**：`putLock` 和 `takeLock`，读写更独立 | 单锁机制：同一把锁处理 put 和 take     |
| **适合场景** | 高并发、大量数据、吞吐更重要的场景                | 任务数量可预估，内存敏感、轻量场景     |

SynchronousQueue

每个 `put` 操作必须等待一个对应的 `take` 操作同步完成，才能继续。

**生产者线程和消费者线程直接“交接”元素**。

| 特点     | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| 容量     | 0，不能存储元素，必须同步交换                                |
| 作用     | 线程间直接传递数据（点对点交接）                             |
| 典型应用 | 在线程池中用作任务传递（如 `ThreadPoolExecutor` 的工作队列） |
| 是否公平 | 支持公平和非公平模式，构造函数可指定                         |

![image-20250705001531218](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250705001531218.png)

**PriorityBlockingQueue  ---->适用于 **多线程环境中带有优先级的任务处理场景**（如定时调度、抢单系统、任务中心等）。**

使用前提：元素必须可比较

实现 `Comparable` 接口，或

在构造 `PriorityBlockingQueue` 时提供 `Comparator` ==**比较器**==

| 接口             | 中文含义       | 排序定义在哪里                        | 是否<span style="color:#FF0000;">侵入</span>类本身 | 是否能定义多个排序 |
| ---------------- | -------------- | ------------------------------------- | -------------------------------------------------- | ------------------ |
| `**Comparable**` | 自己可以比自己 | 类**内部**（实现 `compareTo()` 方法） | ✅ 是                                               | ❌ 只能一个         |
| `**Comparator**` | 外部比较器     | 类**外部**（传入 `compare()` 方法）   | ❌ 否                                               | ✅ 可以多个         |





![image-20250705004346595](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250705004346595.png)

| 返回值 | 意义             | 排序顺序                     |
| ------ | ---------------- | ---------------------------- |
| `< 0`  | **左边比右边小** | `o1`（或 `this`）排在前面    |
| `= 0`  | 相等             | 相对位置不变（通常保留原序） |
| `> 0`  | **左边比右边大** | `o1`（或 `this`）排在后面    |



假设你希望按照**年龄升序排序**（年轻的在前面）：

```java
Comparator<User> byAge = (u1, u2) -> Integer.compare(u1.age, u2.age);
```

- 如果 `u1.age = 18`，`u2.age = 25` → 返回 `< 0` → `u1` 排在前面
- 如果 `u1.age = 30`，`u2.age = 18` → 返回 `> 0` → `u1` 排在后面

---

 ## 拒绝策略

![image-20251005011549570](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005011549570.png)

## 线程池参数设置策略

![image-20251005012203683](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251005012203683.png)

CPU密集型任务中，所有线程都在争夺 CPU 的执行权。
 而操作系统的调度器会让这些线程“轮流上 CPU”，每切换一次线程都要进行：

- 上下文切换（context switch）
- CPU 缓存失效（cache miss）

这两个操作都代价很高。

所以最优策略是：

> 每个核心只安排一个线程
>
> 不然一直线程切换状态 保存恢复上下文 性能开销大



---



IO密集型任务的大部分时间在等：

- 等网络响应
- 等磁盘IO
- 等数据库

CPU在这段时间其实是空闲的。

举个例子：

- 线程A 等磁盘
- 线程B 等Redis
- 线程C 等数据库

此时 CPU 是完全闲的。那怎么办？

> 再开一些线程，让 CPU 有别的活干。

每次线程从**运行态 ↔ 阻塞/等待态**，操作系统需要：

- 保存当前线程上下文（寄存器、栈指针等）
- 切换 CPU 执行其它线程
- 后续恢复上下文

这确实有开销，特别是线程数量过多时，会出现 **频繁上下文切换（Context Switch）**。

- 上下文切换太频繁 → CPU 大量时间花在切换而不是计算 → 反而吞吐下降。
- 所以不能无限增加线程数

---





## ==线程池种类==

除了建议手动声明线程池以外，我还建议用一些监控手段来观察线程池的状态。线程池这个组件往往会表现得任劳任怨、默默无闻，除非是出现了拒绝策略，否则压力再大都不会抛出一个异常。如果我们能提前观察到线程池队列的积压，或者线程数量的快速膨胀，往往可以提早发现并解决问题。







## 锁机制

![image-20251004235141050](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251004235141050.png)

### ==如何在实践中使用锁==

**java提供了多种锁的实现，包括synchronized关键字、java.util.concurrent.locks包下的Lock接口及其具体实现如ReentrantLock、ReadWriteLock等**





---



保证线程安全问题 ： **原子性 有序性 可见性**

锁宏观上分为两大类：共享锁（读锁）和排他锁（写锁） (读锁不互斥，写锁互斥，并且**写锁会阻塞读锁和其他写锁**)

加锁会存在性能问题

**加锁的本质：**

![image-20250504184004630](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250504184004630.png)

mutex 这个是属于操作系统（提供的实现互斥的一种机制，可以通过内核线程去调用这个内核指令）层面的东西 也就是内核指令 

这个切换会占用cpu资源  而且还需要保存当前运行线程执行的指令的上下文  同时又要切换到内核线程去执行这个指令



**线程上下文**（Thread Context）是线程在运行时的全部**运行状态**信息，主要包括：

| 类别                   | 示例（取决于操作系统和硬件）                 |
| ---------------------- | -------------------------------------------- |
| CPU 寄存器状态         | 程序计数器（PC）、栈指针（SP）、通用寄存器等 |
| 栈信息                 | 调用栈、局部变量、返回地址                   |
| 线程私有数据           | TLS（Thread Local Storage）中保存的变量等    |
| 程序执行状态           | 当前正在执行哪条指令、执行位置               |
| CPU 缓存（上下文扩展） | 某些 CPU 还可能保存部分缓存状态              |

所以这里就会涉及到**线程的阻塞/唤醒** 和 **上下文的保存** 这个地方就会消耗性能





**上下文切换（Context Switch）**

> **从当前线程切换到另一个线程运行的全过程**，包括：

- 保存当前线程上下文
- 恢复下一个线程的上下文
- CPU 权交接给另一个线程



![image-20250504193555546](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250504193555546.png)

![image-20250504194031397](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250504194031397.png)

![image-20250504194205450](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250504194205450.png)

**偏向锁 / 轻量级锁/重量级锁 ：就是让线程阻塞减少了锁的竞争**



由于**阻塞会导致上下文的保存 会消耗性能** 所以加自旋锁**（轻量级锁）**



假设有一个共享资源，需要保证同一时刻只能有一个线程访问。

如果线程 A 获取了锁，线程 B 来了，发现锁已被占用，就不断检查锁是否释放（这就是“自旋”）。

一旦线程 A 释放锁，线程 B 就立即获取并进入临界区。

主要原因在于：**线程切换的代价很高，而锁等待时间可能非常短**。



✅ 自旋锁适用于以下场景：

1. **锁持有时间很短**：
   - 如果进入临界区的时间非常短，等待线程与其切换上下文，不如在原地稍微“转一转”，说不定就等到了。
   - 避免了操作系统进行线程上下文切换（这会涉及内核态切换，代价大）。
2. **资源争用不激烈**：
   - 多个线程争锁的概率较低，自旋一次能成功进入临界区的可能性较大。

❌ 不适用于以下场景：

- 如果锁持有时间较长，线程就会白白浪费 CPU，一直自旋等待，非常低效。
- 线程越多，自旋浪费的 CPU 时间越多，反而降低系统性能。

---



**对于性能优化：**

<span style="color:#CC0000; font-weight:bold;">乐观锁（无锁编程）/悲观锁：</span>cas->原子性/可见性

`CAS`（**Compare-And-Swap** 或 Compare-And-Set）是一种 cpu**原子操作**，在多线程编程中用于实现线程安全的 **无锁并发算法**。

CAS 的作用是：
 👉 **“只有当内存中的值是预期的值时，才更新它。”**
 否则不做任何操作。

---



- 它是一种**无锁机制（lock-free）**
- 比传统的 `synchronized` 更快
- 在 Java 中，很多并发类（如 `AtomicInteger`）都是通过 CAS 实现的

---





<span style="color:#CC0000; font-weight:bold;">偏向锁 ：</span>

- **特点**：假设锁总是由同一线程获取，消除同步开销。
- **原理**：
  - 第一次获取锁时，记录线程ID（偏向模式）。
  - 后续同一线程直接进入同步块，无需CAS操作。
- **适用场景**：单线程重复访问同步块的场景。
- **升级**：当其他线程尝试竞争时，升级为轻量级锁

<span style="color:#CC0000; font-weight:bold;">轻量级锁：</span>

- **特点**：通过CAS操作竞争锁，避免直接阻塞线程。
- **原理**：
  - 线程在栈帧中创建锁记录（Lock Record），拷贝对象头中的Mark Word。
  - 通过CAS将对象头指向锁记录，成功则获取锁。
- **适用场景**：低竞争、多线程交替执行的场景。
- **升级**：CAS失败（竞争激烈）时，膨胀为重量级锁

<span style="color:#CC0000; font-weight:bold;">重量级锁：</span>

**特点**：依赖操作系统互斥量（Mutex）实现，线程阻塞和唤醒成本高。

**原理**：

- 竞争失败的线程进入阻塞队列，由操作系统调度。

**适用场景**：高竞争、长时间持有锁的场景。

<span style="color:#CC0000; font-weight:bold;">锁消除/锁膨胀（编译器层面的优化）</span>

**<span style="color:#CC0000; font-weight:bold;">读写锁：</span>**这也是一种优化 ，也就是针对特殊场景（读多写少）做特定的处理 进行优化 

<span style="color:#CC0000; font-weight:bold;">公平锁和非公平锁（减少了线程的阻塞唤醒）</span>：

**1. 公平锁（Fair Lock）**

- **定义**：按照线程请求锁的顺序分配（先到先得）。
- **优点**：避免线程饥饿。
- **缺点**：上下文切换频繁，性能较低。
- **实现**：`ReentrantLock(true)`。



**2. 非公平锁（Nonfair Lock）**

- **定义**：允许插队，新线程可直接尝试获取锁。
- **优点**：
  - **减少线程阻塞/唤醒**：新线程可能直接获取锁，避免进入阻塞队列。
  - **吞吐量更高**：减少上下文切换开销。
- **缺点**：可能导致线程饥饿。
- **实现**：`ReentrantLock(false)`（默认）。

---



对于锁的特性：

<span style="color:#CC0000; font-weight:bold;">**（**ReentrantLock**）可重入锁（防止死锁，java大部分都是可重入锁）/不可重入锁**</span>

线程可以重复获取已持有的锁，避免死锁

---

### 锁的主要分类维度

- 公平性
- 可重入性
- 读写分离
- 加锁方式（显式 / 隐式）
- 阻塞行为（阻塞 / 非阻塞）
- 乐观 / 悲观
- 粒度（对象 / 类）
- 可中断性
- 实现方式（软件 / 硬件）

---



---



# JVM

## 内存模型



## 类初始化和类加载





## 垃圾回收

