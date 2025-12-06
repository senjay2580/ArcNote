#  JVM JDK JRE



Java 虚拟机（Java Virtual Machine, JVM）是运行 Java 字节码的虚拟机。JVM 有针对不同系统的特定实现（Windows，Linux，macOS），目的是使用相同的字节码，它们都会给出相同的结果。字节码和不同系统的 JVM 实现是 Java 语言“一次编译，随处可以运行”的关键所在。

（**JVM 并不是只有一种！只要满足 JVM 规范（virtual machine specification），每个公司、组织或者个人都可以开发自己的专属 JVM。** 也就是说我们平时接触到的 HotSpot VM 仅仅是是 JVM 规范的一种实现而已。）



**JDK（Java Development Kit）**是一个功能齐全的 Java 开发工具包，供开发者使用，用于创建和编译 Java 程序。它包含了 JRE（Java Runtime Environment），以及编译器 javac 和其他工具，如 javadoc（文档生成器）、jdb（调试器）、jconsole（监控工具）、javap（反编译工具）等。

**JRE** 是运行已编译 Java 程序所需的环境，主要包含以下两个部分：

1. **JVM** : 也就是我们上面提到的 Java 虚拟机。
2. **Java 基础类库（Class Library）**：一组标准的类库，提供常用的功能和 API（如 I/O 操作、网络通信、数据结构等）

在 Java 中，JVM 可以理解的代码就叫做字节码（即扩展名为 `.class` 的文件），它不面向任何特定的处理器，只面向虚拟机。Java 语言通过字节码的方式，在一定程度上解决了传统解释型语言执行效率低的问题，同时又保留了解释型语言可移植的特点。所以， Java 程序运行时相对来说还是高效的（不过，和 C、 C++，Rust，Go 等语言还是有一定差距的），而且，由于字节码并不针对一种特定的机器，因此，Java 程序无须重新编译便可在多种不同操作系统的计算机上运行。



![image-20250510102145501](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510102145501.png)

根据**二八定律**，消耗大部分系统资源的只有那一小部分的代码（热点代码），而这也就是 JIT 所需要编译的部分。JVM 会根据代码每次被执行的情况收集信息并相应地做出一些优化，因此执行的次数越多，它的速度就越快。

![image-20250510102809525](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510102809525.png)

JIT 与 AOT，两者各有优点，只能说 AOT 更适合当下的云原生场景，对微服务架构的支持也比较友好。除此之外，AOT 编译无法支持 Java 的一些动态特性，如反射、动态代理、动态加载、JNI（Java Native Interface）等。然而，很多框架和库（如 Spring、CGLIB）都用到了这些特性。如果只使用 AOT 编译，那就没办法使用这些框架和库了，或者说需要针对性地去做适配和优化。举个例子，CGLIB 动态代理使用的是 ASM 技术，而这种技术大致原理是运行时直接在内存中生成并加载修改后的字节码文件也就是 .class 文件，如果全部使用 AOT 提前编译，也就不能使用 ASM 技术了。为了支持类似的动态特性，所以选择使用 JIT 即时编译器

---



Java 和 C++ 都是**面向对象**的语言

Java 不提供指针来直接访问内存，程序内存更加安全

Java 的类是单继承的，C++ 支持多重继承；虽然 Java 的类不可以多继承，但是接口可以多继承。

Java 有自动内存管理垃圾回收机制(GC)，不需要程序员手动释放无用内存。

C ++同时支持方法重载和操作符重载，但是 Java 只支持方法重载（操作符重载增加了复杂性，这与 Java 最初的设计思想不符）。



~~~java
/**
 *文档注释
 * 直接使用 /** + Enter
 */

public class Basic {


}

~~~





---

**移位运算符**
移位运算符是最基本的运算符之一，几乎每种编程语言都包含这一运算符。移位操作中，被操作的数据被视为二进制数，移位就是将其向左或向右移动若干位的运算。

移位运算符在各种框架以及 JDK 自身的源码中使用还是挺广泛的，HashMap（JDK1.8） 中的 hash 方法的源码就用到了移位运算符：



使用移位运算符的主要原因：

高效：移位运算符直接对应于处理器的移位指令。**现代处理器具有专门的硬件指令来执行这些移位操作**，这些指令通常在一个时钟周期内完成。相比之下，乘法和除法等算术运算在硬件层面上需要更多的**时钟周期**来完成。
节省内存：通过移位操作，可以使用一个整数（如 int 或 long）来存储多个布尔值或标志位，从而节省内存。

移位运算符最常用于快速乘以或除以 2 的幂次方。除此之外，它还在以下方面发挥着重要作用：

**位字段管理：**例如存储和操作多个布尔值。
**哈希算法和加密解密：**通过移位和与、或等操作来混淆数据。
**数据压缩：**例如霍夫曼编码通过移位运算符可以快速处理和操作二进制数据，以生成紧凑的压缩格式。
**数据校验：**例如 CRC（循环冗余校验）通过移位和多项式除法生成和校验数据完整性。。
**内存对齐：**通过移位操作，可以轻松计算和调整数据的对齐地址。
掌握最基本的移位运算符知识还是很有必要的，这不光可以帮助我们在代码中使用，还可以帮助我们理解源码中涉及到移位运算符的代码。

**Java 中有三种移位运算符：**

`<<` :左移运算符，向左移若干位，高位丢弃，低位补零。`x << n`,相当于 x 乘以 2 的 n 次方(不溢出的情况下)。

`>>` :带符号右移，向右移若干位，高位补符号位，低位丢弃。正数高位补 0,负数高位补 1。`x >> n`,相当于 x 除以 2 的 n 次方。

`>>>` :无符号右移，忽略符号位，空位都以 0 补齐。



由于 double，float 在二进制中的表现比较特殊，因此不能来进行移位操作。

移位操作符实际上支持的类型只有**int和long**，编译器在对short、byte、char类型进行移位前，都会将其转换为**int类型**再操作。

---



# 基本数据类型/引用数据类型/包装类型

![image-20250510104412891](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510104412891.png)

**注意：**

1. Java 里使用 `long` 类型的数据一定要在数值后面加上 **L**，否则将作为整型解析。
2. Java 里使用 `float` 类型的数据一定要在数值后面加上 **f 或 F**，否则将无法通过编译。 （默认的小数（浮点字面量）是 **`double` 类型**）
3. `char a = 'h'`char :单引号，`String a = "hello"` :双引号。

这八种基本类型都有对应的包装类分别为：`Byte`、`Short`、`Integer`、`Long`、`Float`、`Double`、`Character`、`Boolean` 

---



### 基本类型和包装类型的区别？



- **用途**：除了定义一些常量和局部变量之外，我们在其他地方比如方法参数、对象属性中很少会使用基本类型来定义变量。并且，包装类型可用于泛型，而基本类型不可以。
- **存储方式**：基本数据类型的局部变量存放在<span style="color:#CC0000;"> Java 虚拟机栈</span>中的局部变量表中，<span style="color:#CC0000;">基本数据类型的成员变</span>量（未被 `static` 修饰 ）存放在 Java 虚拟机的堆中。包装类型属于对象类型，**我们知道几乎所有对象实例都存在于堆中**。
- **占用空间**：相比于包装类型（对象类型）， 基本数据类型占用的空间往往非常小。
- **默认值**：成员变量包装类型不赋值就是 `null` ，而基本类型有默认值且不是 `null`。
- **比较方式**：对于基本数据类型来说，`==` 比较的是值。对于包装数据类型来说，`==` 比较的是对象的内存地址。所有整型包装类对象之间值的比较，全部使用 `equals()` 方法。

**为什么说是几乎所有对象实例都存在于堆中呢？** 这是因为 HotSpot 虚拟机引入了 JIT 优化之后，会对对象进行逃逸分析，如果发现某一个对象并没有逃逸到方法外部，那么就可能通过**标量替换**<span style="color:#FF0000;">（**标量替换（Scalar Replacement）**：</span>

- <span style="color:#FF0000;">如果对象不会逃逸，JVM 甚至可以**不创建这个对象**，而是将其拆解为若干个字段，直接以局部变量方式存在于栈中。</span>

<span style="color:#FF0000;">）</span>**来实现栈上分配，而避免堆上分配内存**





 `Point` 对象 **只在 `foo()` 方法内部被使用，没有泄露到外部方法或线程中**，这就是“没有逃逸”。

如果逃逸分析判断对象不会逃出方法，则可将其分配在栈上。

随着方法结束，栈帧销毁，对象也随之销毁，无需 GC 管理。

好处：减少堆内存使用、降低 GC 压力、提升性能。

---



⚠️ 注意：**基本数据类型存放在栈中是一个常见的误区！** 基本数据类型的存储位置取决于它们的作用域和声明方式。如果它们是**局部变量，那么它们会存放在栈中；**如果它们是**成员变量，那么它们会存放在堆/方法区/元空间中。**

------

### 包装类型的缓存机制

Java 基本数据类型的包装类型的大部分都用到了缓存机制来提升性能。

`Byte`,`Short`,`Integer`,`Long` 这 4 种包装类 （**`Float`,`Double` 并没有实现缓存机制**）默认创建了数值 **[-128，127]** 的相应类型的缓存数据，`Character` 创建了数值在 **[0,127]** 范围的缓存数据，`Boolean` 直接返回 `TRUE` or `FALSE`。

**包装类的范围与其对应的基本类型完全一致**

~~~java
Integer i1 = 40; // 自动装箱 使用的是 缓存中的  等价于Integer i1=Integer.valueOf(40)
Integer i2 = new Integer(40);
System.out.println(i1==i2); // False
~~~





### 包装类的类型转化

**toString parseInt (parseLong parseDouble parseXXX)**



---



### 自动装箱/拆箱

- **装箱**：将基本类型用它们对应的引用类型包装起来；
- **拆箱**：将包装类型转换为基本数据类型；

~~~java
Integer i = 10;  //装箱
int n = i;   //拆箱
~~~

c语言编译成**汇编语言** 

java 编译成**字节码** 这两个语法都很相似

---



### 浮点数运算 会有精度丢失的风险

~~~java
float a = 2.0f - 1.9f;
float b = 1.8f - 1.7f;
System.out.printf("%.9f",a);// 0.100000024
System.out.println(b);// 0.099999905
System.out.println(a == b);// false
~~~



在计算机中，`float` 是遵循 IEEE 754 标准的 32 位浮点数表示，其底层是**二进制小数**，而有些十进制数（比如 0.1）在二进制中是 **无限循环的**，就像十进制中 `1/3 = 0.333...` 一样。

例如：

```

0.1 (十进制) = 0.0001100110011001100110011... (二进制)
```

**浮点数没有办法用二进制精确表示**

`BigDecimal` 可以实现对浮点数的运算，不会造成精度丢失。通常情况下，大部分需要浮点数精确运算结果的业务场景（比如涉及到钱的场景）都是通过 `BigDecimal` 来做的。



```java
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("1.00");
BigDecimal c = new BigDecimal("0.8");

BigDecimal x = a.subtract(c);
BigDecimal y = b.subtract(c);

System.out.println(x); /* 0.2 */
System.out.println(y); /* 0.20 */
// 比较内容，不是比较值
System.out.println(Objects.equals(x, y)); /* false */  // 也就是比较值 + 精度
// 比较值相等用相等compareTo，相等返回0
System.out.println(0 == x.compareTo(y)); /* true */
```

------

**这种特殊的封装类型<span style="color:#CC0000;"> 基本运算</span>的实现都是通过某种函数 而不是基本运算符**

### 超过long的大数据如何表示

使用BigInteger**对象封装** + **内部数组模拟任意大整数**

~~~java
BigInteger x = new BigInteger("100000000000000000000");
BigInteger y = new BigInteger("99999999999999999999");

BigInteger sum = x.add(y);            // 加法
BigInteger diff = x.subtract(y);      // 减法
BigInteger prod = x.multiply(y);      // 乘法
BigInteger quot = x.divide(y);        // 除法
BigInteger mod = x.mod(y);            // 取模

System.out.println("Sum: " + sum);

~~~

**但是这个<span style="color:#FF0000;">运算性能</span>就很差了**



## 变量

###  成员变量和局部变量

**语法形式**：从语法形式上看，成员变量是属于类的，而局部变量是在代码块或方法中定义的变量或是方法的参数；成员变量可以被 `public`,`private`,`static` 等修饰符所修饰，而局部变量不能被访问控制修饰符及 `static` 所修饰；但是，成员变量和局部变量都能被 `final` 所修饰。

**存储方式**：从变量在内存中的存储方式来看，如果成员变量是使用 `static` 修饰的，那么这个成员变量是属于类的，如果没有使用 `static` 修饰，这个成员变量是属于实例的。而对象存在于堆内存，局部变量则存在于栈内存。

**生存时间**：从变量在内存中的生存时间上看，成员变量是对象的一部分，它随着对象的创建而存在，而局部变量随着方法的调用而自动生成，随着方法的调用结束而消亡。

**默认值**：从变量是否有默认值来看，成员变量如果没有被赋初始值，则会自动以类型的默认值而赋值（一种情况例外:被 `final` 修饰的成员变量也必须显式地赋值），而局部变量则不会自动赋值。

---





### 静态变量

静态变量也就是被 `static` 关键字修饰的变量。它可以被类的所有实例共享，无论一个类创建了多少个对象，它们都共享同一份静态变量。也就是说，静态变量<span style="color:#FF0000;">只会被分配一次内存，即使创建多个对象，这样可以节省内存。</span>

------





### 字符型常量  &  字符串常量

- **形式** : 字符常量是单引号引起的一个字符，字符串常量是双引号引起的 0 个或若干个字符。
- **含义** : 字符常量相当于一个整型值( ASCII 值),可以参加表达式运算; 字符串常量代表一个地址值(该字符串在内存中存放位置)。
- **占内存大小**：字符常量只占 2 个字节; 字符串常量占若干个字节。

⚠️ 注意 `char` 在 Java 中占**两个字节。**

## 方法

### <span style="color:#FF9933;">静态方法为什么不能调用非静态成员</span>?

这个需要结合 JVM 的相关知识，主要原因如下：

1. 静态方法是属于类的，在类加载的时候就会分配内存，可以通过类名直接访问。而非静态成员属于实例对象，只有在对象实例化之后才存在，需要通过类的实例对象去访问。
2. 在类的非静态成员不存在的时候静态方法就已经存在了，此时调用在内存中还不存在的非静态成员，属于非法操作。

------



> 重载就是同样的一个方法能够根据输入数据的不同，做出不同的处理
>
> 重写就是当子类继承自父类的相同方法，输入数据一样，但要做出有别于父类的响应时，你就要覆盖父类方法

在 Java 中，**方法名相同**，但**参数列表不同**（参数类型、顺序、个数不同），就构成方法重载（Overloading），**与返回值类型、修饰符、异常等无关**。

![image-20250510120758548](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510120758548.png)

**就是说 遇到不存在 初始化 找不到 找错 等问题 要考虑 生命周期 也就是发生在哪一个时期<span style="color:#CC0000;">（编译器 运行期）</span>**



| 访问修饰符   | 可访问范围          |
| ------------ | ------------------- |
| `private`    | 当前类内部          |
| 默认（包内） | 同一个包中          |
| `protected`  | 同包 + 不同包的子类 |
| `public`     | 所有地方都能访问    |







---

## 🧱 SOLID 五大原则总览

| 英文名                              | 中文名       | 缩写字母 |
| ----------------------------------- | ------------ | -------- |
| Single Responsibility Principle     | 单一职责原则 | S        |
| Open-Closed Principle               | 开放封闭原则 | O        |
| **Liskov Substitution Principle**   | 里氏替换原则 | L        |
| **Interface Segregation Principle** | 接口隔离原则 | I        |
| Dependency Inversion Principle      | 依赖倒置原则 | **D**    |

> **一个类应该仅有一个引起它变化的原因。**

- 每个类应该只负责一项职责。
- 修改某一职责，不应该影响其他职责。
- 举例：订单管理类不要同时负责日志、打印、数据库等多个功能。



> **软件实体（类、模块、函数）应该对扩展开放，对修改封闭。**

- 在不修改已有代码的情况下，通过**扩展**（如继承、实现接口）来增加新功能。
- 利于系统的可扩展性和稳定性。
- 举例：使用接口+多态来新增支付方式，而不是频繁修改原有代码。

🧑‍💻 举个例子

问题：支付系统的新增支付方式

假设你设计了一个支付系统，最开始支持支付宝支付。你的支付功能在最开始的实现可能是这样：

```java
class PaymentService {
    public void payByAliPay(double amount) {
        System.out.println("支付 " + amount + " 元，通过支付宝完成！");
    }
}
```

但随着需求的变化，现在你需要在支付系统中新增其他支付方式，如微信支付。按照常规方法，如果每次新增支付方式时都修改 `PaymentService` 类中的代码，就会频繁地修改原有代码，违反了**开放封闭原则**。每次修改都会引入潜在的错误。

**符合开放封闭原则的设计：**

根据 **开放封闭原则**，我们通过 **接口和多态** 来扩展支付功能，而不修改原有代码。

1. 定义一个 `PaymentMethod` 接口：

```java
interface PaymentMethod {
    void pay(double amount);
}
```

1. 各种支付方式实现这个接口：

```java
class AliPay implements PaymentMethod {
    @Override
    public void pay(double amount) {
        System.out.println("支付 " + amount + " 元，通过支付宝完成！");
    }
}

class WeChatPay implements PaymentMethod {
    @Override
    public void pay(double amount) {
        System.out.println("支付 " + amount + " 元，通过微信支付完成！");
    }
}
```

1. `PaymentService` 类无需修改，只需要接受 `PaymentMethod` 接口作为依赖：

```java
class PaymentService {
    private PaymentMethod paymentMethod;

    public PaymentService(PaymentMethod paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    public void pay(double amount) {
        paymentMethod.pay(amount);  // 委托给传入的支付方式
    }
}
```

1. 新增支付方式时，不需要修改原有代码，只需要新增实现类即可：

```java
public class Main {
    public static void main(String[] args) {
        PaymentService aliPayService = new PaymentService(new AliPay());
        aliPayService.pay(100);

        PaymentService weChatPayService = new PaymentService(new WeChatPay());
        weChatPayService.pay(200);
    }
}
```

**为什么符合开放封闭原则？**

- **对扩展开放**：你可以通过新增实现 `PaymentMethod` 接口的类来扩展支付方式，而不需要修改现有代码。比如你可以继续新增其他支付方式（如银行卡支付、Apple Pay 等）。
- **对修改封闭**：现有的 `PaymentService` 类已经封闭，不再需要修改。新增支付方式时，只需要创建新的支付方式类，并通过构造器注入即可。

---



> **子类对象必须能替换父类对象，并且行为一致。**
>
> **只要父类能使用的地方，子类就应该能替代并正常使用，且行为一致。**

- 子类不能违背父类的行为约定。
- 否则会破坏继承体系，使多态失效。
- 举例：不能用不能飞的 `Ostrich extends Bird` 来替换 `Bird`，否则调用 `fly()` 时程序出错。

---



> **不应该强迫一个类依赖它不使用的接口。**

- 接口应该尽量小而精，不要设计“胖接口”。
- 使用多个**专门接口**，比一个**臃肿接口**更好。
- 举例：打印机接口不应强制所有设备实现扫描、复印等方法。
- 各类设备只实现自己需要的功能；

  更清晰的职责分离，**增强代码的可维护性和可扩展性**；

  遵守了接口隔离原则，**不会引入“空实现”或“异常实现”**。

也就是说：不要让实现类去实现它用不上的方法，接口应该精细化，避免臃肿。

---



> **高层模块不应该依赖低层模块，二者都应该依赖于抽象；抽象不应该依赖于细节，细节应该依赖于抽象。**

- 核心思想：**程序要面向接口编程，而不是面向实现编程**。
- 高层模块（如业务逻辑）通过接口与底层模块（如数据访问）解耦。  **controller**  **通过service接口和service业务层进行交互**
-  举例：`Service` 层依赖于 `UserDao` 接口，而不是 `UserDaoImpl` 的具体实现。

假设你有一个 **用户服务（`UserService`）** 和一个 **数据访问层（`UserDao`）**。

1. **不符合 DIP 原则的设计**：

```java
// 高层模块：UserService（业务逻辑层）
class UserService {
    private UserDaoImpl userDao = new UserDaoImpl();  // 依赖于具体实现

    public void addUser(User user) {
        userDao.save(user);  // 调用具体实现
    }
}

// 低层模块：UserDaoImpl（数据访问层）
class UserDaoImpl {
    public void save(User user) {
        // 数据库操作
    }
}
```

- 这种设计违背了 **依赖倒置原则**，因为 `UserService` 直接依赖了 `UserDaoImpl` 的具体实现。假如要更换为其他数据存储方式（比如换成 NoSQL 数据库），你需要修改 `UserService` 类中的实现，造成了高耦合，**不利于扩展**。

2. **符合 DIP 原则的设计**：

```java
// 高层模块：UserService（业务逻辑层）
interface UserDao {
    void save(User user);
}

class UserService {
    private UserDao userDao;

    // 通过构造器注入依赖，依赖于抽象接口
    public UserService(UserDao userDao) {
        this.userDao = userDao;
    }

    public void addUser(User user) {
        userDao.save(user);  // 调用抽象接口
    }
}

// 低层模块：UserDaoImpl（具体实现）
class UserDaoImpl implements UserDao {
    @Override
    public void save(User user) {
        // 数据库操作
    }
}
```

在这个设计中，`UserService` 不再依赖于 `UserDaoImpl` 的具体实现，而是依赖于 `UserDao` 接口（抽象）。

- `UserDaoImpl` 是对 `UserDao` 接口的具体实现。
- 通过 **构造器注入**的方式将具体实现传递给 `UserService`，`UserService` 只关心数据存储的抽象接口，而不关心具体的存储方式。

---



### 什么是可变长参数？

从 Java5 开始，Java 支持定义可变长参数，所谓可变长参数就是允许在调用方法时传入不定长度的参数。就比如下面这个方法就可以接受 0 个或者多个参数。



```java
public static void method1(String... args) {
   //......
}
```

另外，可变参数只能作为函数的最后一个参数，但其前面可以有也可以没有任何其他参数。



```java
public static void method2(String arg1, String... args) {
   //......
}
```

**遇到方法重载的情况怎么办呢？会优先匹配固定参数还是可变参数的方法呢？**

答案是会优先匹配固定参数的方法，因为固定参数的方法匹配度更高。

---

### 面向对象和面向过程的区别

面向过程编程（Procedural-Oriented Programming，POP）和面向对象编程（Object-Oriented Programming，OOP）是两种常见的编程范式，两者的主要区别在于解决问题的方式不同：

- **面向过程编程（POP）**：面向过程把解决问题的过程拆成一个个方法，通过一个个方法的执行解决问题。
- **面向对象编程（OOP）**：面向对象会先抽象出对象，然后用对象执行方法的方式解决问题。

相比较于 POP，OOP 开发的程序一般具有下面这些优点：

- **易维护**：由于良好的结构和封装性，OOP 程序通常更容易维护。
- **易复用**：通过继承和多态，OOP 设计使得代码更具复用性，方便扩展功能。
- **易扩展**：模块化设计使得系统扩展变得更加容易和灵活。
- ![image-20250510123609737](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510123609737.png)



在选择编程范式时，性能并不是唯一的考虑因素。代码的可维护性、可扩展性和开发效率同样重要。

现代编程语言基本都支持多种编程范式，既可以用来进行面向过程编程，也可以进行面向对象编程。

---

## 对象引用



new 运算符，new 创建对象实例（对象实例在堆内存中），对象引用指向对象实例（对象引用存放在栈内存中）。

- 一个对象引用可以指向 0 个或 1 个对象实例（一根绳子可以不系气球，也可以系一个气球）；
- 一个对象实例可以有 n 个对象引用指向它（可以用 n 条绳子系住一个气球）



<span style="color:#FF0000;">**关于继承如下 3 点请记住：**</span>

<span style="color:#FF0000;">子类拥有父类对象所有的属性和方法（包括私有属性和私有方法），但是父类中的私有属性和方法子类是**无法访问**，只是**拥有**。</span>
子类可以拥有自己属性和方法，即子类可以对父类进行扩展。
子类可以用自己的方式实现父类的方法。（以后介绍）



~~~java
 Balloon balloon1（对象引用） = null;  // 引用没有指向任何对象，绳子没有系气球
        Balloon balloon2 = new Balloon("Red");  // 引用指向一个气球，绳子系住了一个气球 



Balloon balloon = new Balloon("Blue");  // 创建一个气球
        Balloon balloon1 = balloon;  // 引用 balloon1 和 balloon 都指向同一个气球
        Balloon balloon2 = balloon;  // 引用 balloon2 和 balloon 都指向同一个气球
~~~



---



#### 接口和抽象类的区别

- **设计目的**：接口主要用于对类的行为进行约束，你实现了某个接口就具有了对应的行为。**抽象类主要用于代码复用，强调的是所属关系。**

- **继承和实现**：<span style="color:#FF0000; background:#606060;">一个类只能继承一个类（包括抽象类），因为 Java 不支持多继承。但一个类可以实现多个接口，一个接口也可以继承多个其他接口。</span>

- **成员变量**：接口中的成员变量只能是 `public static final` 类型的，不能被修改且必须有初始值。抽象类的成员变量可以有任何修饰符（`private`, `protected`, `public`），可以在子类中被重新定义或赋值。

- 方法

  ： 

  - Java 8 之前，接口中的方法默认是 `public abstract` ，也就是只能有方法声明。自 Java 8 起，可以在接口中定义 `default`（默认） 方法和 `static` （静态）方法。 自 Java 9 起，接口可以包含 `private` 方法。
  - 抽象类可以包含抽象方法和非抽象方法。抽象方法没有方法体，必须在子类中实现。非抽象方法有具体实现，可以直接在抽象类中使用或在子类中重写。

**<span style="background:#CC0000;">Java 8 引入的`default` 方法用于提供接口方法的<span style="color:#FFFFFF;">默认实现</span>，<span style="color:#FFFFFF;">可以在实现类中被覆</span>盖</span>。这样就可以在不修改实现类的情况下向现有接口添加新功能，从而增强接口的扩展性和向后兼容性。**



```java
public interface MyInterface {
    default void defaultMethod() {
        System.out.println("This is a default method.");
    }
}
```

Java 8 引入的`static` 方法无法在实现类中被覆盖，只能通过接口名直接调用（ `MyInterface.staticMethod()`），类似于类中的静态方法。`static` 方法通常用于定义一些通用的、与接口相关的工具方法，一般很少用。



---



### 深拷贝 & 浅拷贝

**浅拷贝：**创建一个新的对象，但**里面的引用成员变量还是指向原来的对象**

**深拷贝：**不仅复制对象本身，还**复制它内部引用的对象**（即递归复制）。

复制后完全独立，互不影响。



![image-20250510125850867](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510125850867.png)






## Object

<span style="color:#FF0000;">因为 Java **只有值传递**</span>，所以，对于 == 来说，不管是比较基本数据类型，<span style="color:#FF0000;">还是引用数据类型的变量，其本质比较的都是值，</span><span style="color:#990000;">**只是引用类型变量存的值是对象的地址。**</span>

`native` 是一个 **关键字**，用于声明一个 **本地方法**（native method），也叫做 **本机方法**。本地方法的实现不是用 Java 编写的，而是用 **C、C++ 等其他语言**编写，并通过 **Java 本地接口（JNI, Java Native Interface）**与 Java 交互。

`hashCode()` 的作用是获取哈希码（`int` 整数），也称为散列码。这个哈希码的作用是确定该对象在哈希表中的索引位置。

![hashCode() 方法](https://oss.javaguide.cn/github/javaguide/java/basis/java-hashcode-method.png)

`hashCode()` 定义在 JDK 的 `Object` 类中，这就意味着 Java 中的任何类都包含有 `hashCode()` 函数。另外需要注意的是：`Object` 的 `hashCode()` 方法是本地方法，也就是用 C 语言或 C++ 实现的。



> 当你把对象加入 `HashSet` 时，`HashSet` 会先计算对象的 `hashCode` 值来判断对象加入的位置，同时也会与其他已经加入的对象的 `hashCode` 值作比较，如果没有相符的 `hashCode`，`HashSet` 会假设对象没有重复出现。但是如果发现有相同 `hashCode` 值的对象，这时会调用 `equals()` 方法来检查 `hashCode` 相等的对象是否真的相同。如果两者相同，`HashSet` 就不会让其加入操作成功。如果不同的话，就会重新散列到其他位置。这样我们就大大减少了 `equals` 的次数，相应就大大提高了执行速度。

<span style="color:#FF0000;">其实， `hashCode()` 和 `equals()`都是用于比较两个对象是否相等</span>。





如果两个对象的`hashCode` 值相等，那这两个对象不一定相等<span style="color:#990000;">（哈希碰撞）。</span>

如果两个对象的`hashCode` 值相等并且`equals()`方法也返回 `true`，我们才认为这两个对象相等。

<span style="color:#990000;">如果两个对象的`hashCode` 值不相等，我们就可以直接认为这两个对象不相等。</span>







**对于equals方法！一般情况下，我们比较的是：**

> 对象的**关键属性是否相等**，而不是地址是否相等。

~~~java

import java.util.Objects;

public class User {
    private int id;
    private String name;

    public User(int id, String name) {
        this.id = id;
        this.name = name;
    }

    // 重写 equals 方法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;  // 同一个对象
        if (obj == null || getClass() != obj.getClass()) return false;  // 不同类

        User user = (User) obj;
        return id == user.id && Objects.equals(name, user.name);
    }

    // 重写 hashCode 方法
    @Override
    public int hashCode() {
        return Objects.hash(id, name);  // 保证只要 id 和 name 一样，hashCode 就一样
    }

    // 方便打印
    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "'}";
    }
}

~~~







### 为什么重写 equals() 时必须重写 hashCode() 方法

因为两个相等的对象的 `hashCode` 值必须是相等。也就是说如果 `equals` 方法判断两个对象是相等的，那这两个对象的 `hashCode` 值也要相等。

重写 `equals()` 时没有重写 `hashCode()` 方法的话就可能会导致 `equals` 方法判断是相等的两个对象，`hashCode` 值却不相等。

**哈希容器（如 HashMap、HashSet）就会出现逻辑错误**

---



**🧪 一个自定义类（未重写 `hashCode()`**）：

```java
class Person {
    String name;
    int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Person)) return false;
        Person other = (Person) obj;
        return this.age == other.age && this.name.equals(other.name);
    }

    // 注意：没有重写 hashCode()
}
```

**测试代码：**

```java
import java.util.HashSet;

public class Test {
    public static void main(String[] args) {
        Person p1 = new Person("Alice", 18);
        Person p2 = new Person("Alice", 18);

        System.out.println(p1.equals(p2)); // true

        HashSet<Person> set = new HashSet<>();
        set.add(p1);
        set.add(p2);

        System.out.println(set.size()); // ❌ 输出 2（错误！应该是 1）
    }
}
```

虽然 `p1.equals(p2)` 是 `true`，**但由于两个对象的 `hashCode()` 是不同的（ 如果没有重写！！！<span style="color:#FF0000;">就是继承自 Object，默认根据地址就是对象的地址生成</span>**），所以 `HashSet` 认为它们是两个不同的对象。

**四、正确做法：重写 `hashCode()`**

```java
@Override
public int hashCode() {
    return Objects.hash(name, age);
}
```

------



## String 

### String    StringBuffer    StringBuilder

`String` 是不可变的（后面会详细分析原因）。

`StringBuilder` 与 `StringBuffer` 都继承自 `AbstractStringBuilder` 类，在 `AbstractStringBuilder` 中也是使用字符数组保存字符串，不过没有使用 `final` 和 `private` 关键字修饰，最关键的是这个 `AbstractStringBuilder` 类还提供了很多修改字符串的方法比如 `expandCapacity、append、insert、indexOf` 方法。

每次对 `String` 类型进行改变的时候，都会生成一个新的 `String` 对象，然后将指针指向新的 `String` 对象。`StringBuffer` 每次都会对 `StringBuffer` 对象本身进行操作，而不是生成新的对象并改变对象引用。相同情况下使用 `StringBuilder` 相比使用 `StringBuffer` 仅能获得 10%~15% 左右的性能提升，但却要冒多线程不安全的风险。



**对于三者使用的总结：**

- 操作少量的数据: 适用 `String`

**大量数据：**

- **单线程**操作字符串缓冲区下操作**大量数据**: 适用 `StringBuilder`  线程不安全
- **多线程操作字符串缓冲区下操作大量数据: 适用 `StringBuffer`   （线程安全 因为加了同步锁 但由于就是加了锁 导致影响了性能）**





![image-20250510141640522](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510141640522.png)



Java 语言本身并不支持运算符重载（py等支持）

`String` 中的 `equals` 方法是被重写过的，比较的是 String 字符串的值是否相等。 `Object` 的 `equals` 方法是比较的对象的内存地址

**字符串常量池** 是 JVM 为了提升性能和**减少内存消耗**针对字符串（String 类）专门开辟的一块区域，**主要目的是为了避免字符串的重复创建。**

将常量池中的字符串对象引用赋值给变量

~~~java
// 在字符串常量池中创建字符串对象 ”ab“
// 将字符串对象 ”ab“ 的引用赋值给 aa
String aa = "ab";
// 直接返回字符串常量池中字符串对象 ”ab“，赋值给引用 bb
String bb = "ab";
System.out.println(aa==bb); // true
~~~

![image-20250510142229180](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510142229180.png)、

1、如果字符串常量池中不存在字符串对象 “abc”，那么它首先会在字符串常量池中创建字符串对象 "abc"，然后在堆内存中再创建其中一个字符串对象 "abc"。

**示例代码（JDK 1.8）：**

~~~java
String s1 = new String("abc");
~~~



**对应的字节码：**

~~~java
// 在堆内存中分配一个尚未初始化的 String 对象。
// #2 是常量池中的一个符号引用，指向 java/lang/String 类。
// 在类加载的解析阶段，这个符号引用会被解析成直接引用，即指向实际的 java/lang/String 类。
0 new #2 <java/lang/String>
// 复制栈顶的 String 对象引用，为后续的构造函数调用做准备。
// 此时操作数栈中有两个相同的对象引用：一个用于传递给构造函数，另一个用于保持对新对象的引用，后续将其存储到局部变量表。
3 dup
// JVM 先检查字符串常量池中是否存在 "abc"。
// 如果常量池中已存在 "abc"，则直接返回该字符串的引用；
// 如果常量池中不存在 "abc"，则 JVM 会在常量池中创建该字符串字面量并返回它的引用。
// 这个引用被压入操作数栈，用作构造函数的参数。
4 ldc #3 <abc>
// 调用构造方法，使用从常量池中加载的 "abc" 初始化堆中的 String 对象
// 新的 String 对象将包含与常量池中的 "abc" 相同的内容，但它是一个独立的对象，存储于堆中。
6 invokespecial #4 <java/lang/String.<init> : (Ljava/lang/String;)V>
// 将堆中的 String 对象引用存储到局部变量表
9 astore_1
// 返回，结束方法
10 return
~~~



**ldc (load constant) 指令**的确是从常量池中加载各种类型的常量，包括字符串常量、整数常量、浮点数常量，甚至类引用等。对于字符串常量，ldc 指令的行为如下：

从**常量池加载字符串**：ldc 首先检查字符串常量池中是否已经有内容相同的字符串对象。
复用已有字符串对象：如果字符串常量池中已经存在内容相同的字符串对象，**ldc 会将该对象的引用加载到操作数栈上。**
**没有则创建新对象并加入常量池：**如果字符串常量池中没有相同内容的字符串对象，JVM 会在常量池中创建一个新的字符串对象，并将其引用加载到操作数栈中。

---



2、如果字符串常量池中已存在字符串对象“abc”，则只会在堆中创建 1 个字符串对象“abc”。

**示例代码（JDK 1.8）：**

~~~java
// 字符串常量池中已存在字符串对象“abc”
String s1 = "abc";
// 下面这段代码只会在堆中创建 1 个字符串对象“abc”
String s2 = new String("abc");
~~~



**对应的字节码：**

~~~java
0 ldc #2 <abc>
2 astore_1
3 new #3 <java/lang/String>
6 dup
7 ldc #2 <abc>
9 invokespecial #4 <java/lang/String.<init> : (Ljava/lang/String;)V>
12 astore_2
13 return
~~~



这里就不对上面的字节码进行详细注释了，7 这个位置的 ldc 命令不会在堆中创建新的字符串对象“abc”，这是因为 0 这个位置已经执行了一次 ldc 命令，已经在堆中创建过一次字符串对象“abc”了。7 这个位置执行 ldc 命令会直接返回字符串常量池中字符串对象“abc”对应的引用。

---

`String.intern()` 是一个 `native` (本地) 方法，用来处理字符串常量池中的字符串对象引用。它的工作流程可以概括为以下两种情况：

1. **常量池中已有相同内容的字符串对象**：如果字符串常量池中已经有一个与调用 `intern()` 方法的字符串内容相同的 `String` 对象，`intern()` 方法会直接返回常量池中该对象的引用。
2. **常量池中没有相同内容的字符串对象**：如果字符串常量池中还没有一个与调用 `intern()` 方法的字符串内容相同的对象，`intern()` 方法会将当前字符串对象的引用添加到字符串常量池中，并返回该引用。

总结：

- `intern()` 方法的主要作用是确保字符串引用在常量池中的唯一性。
- 当调用 `intern()` 时，如果常量池中已经存在相同内容的字符串，则返回常量池中已有对象的引用；否则，将该字符串添加到常量池并返回其引用。



`String s1 = new String("hello");`，实际上并不会在字符串常量池中创建对象，而是在堆内存中创建了一个新的字符串对象。

`String s = "hello ";` 会在字符串常量池中创建一个 `"hello "` 字符串对象，并且变量 `s` 会引用这个字符串常量池中的对象。



~~~java

String s1 = new String("hello");  
String s2 = s1.intern();

// s1 和 s2 并不是同一个对象


String s1 = new String("hello");
String s2 = s1;

~~~



---



## 异常



### 自定义异常

~~~java
public class MyCustomException extends RuntimeException {
// 各种构造函数 接收异常对象 和 自定义异常信息
    public MyCustomException() {
        super();
    }

    public MyCustomException(String message) {
        super(message);
    }

    public MyCustomException(String message, Throwable cause) {
        super(message, cause);
    }

    public MyCustomException(Throwable cause) {
        super(cause);
    }
}

// ————————————————————————————————————————————————————————————————————————————————————————————————————————
    public void processData(int value) {
        try {
            if (value < 0) {
                throw new IllegalArgumentException("Value cannot be negative: " + value);
            }
            // 其他处理逻辑
        } catch (IllegalArgumentException e) {
            // 捕获 IllegalArgumentException，并包装成 MyCustomException 抛出
            throw new MyCustomException("Invalid value encountered", e);
        }
    }

// e 是通过Throwable类来接收的对象 也就是异常对象 而对于Throwable 有以下方法
// getMessage（） 返回异常的详细描述信息。通常是通过异常的构造方法传入的字符串
// getCause（）返回异常的原因（也称为根异常）。通常是在构造异常时传递的另一个异常。
~~~



![image-20250510142843342](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510142843342.png)

**`Exception`** :程序本身可以处理的异常，可以通过 `catch` 来进行捕获。`Exception` 又可以分为 Checked Exception (受检查异常，必须处理) 和 Unchecked Exception (不受检查异常，可以不处理)。

**`Error`**：`Error` 属于程序无法处理的错误 不建议通过`catch`捕获 。例如 Java 虚拟机运行错误（`Virtual MachineError`）、虚拟机内存不够错误(`OutOfMemoryError`)、类定义错误（`NoClassDefFoundError`）等 。这些异常发生时，Java 虚拟机（JVM）一般会选择线程终止。



**Checked Exception** 即 受检查异常 ，Java 代码在编译过程中，如果受检查异常没有被 `catch`或者`throws` 关键字处理的话，就没办法通过编译。

常见的受检查异常有：IO 相关的异常、`ClassNotFoundException`、`SQLException`...。


**Unchecked Exception** 即 **不受检查异常** ，Java 代码在编译过程中 ，我们即使不处理不受检查异常也可以正常通过编译。

`RuntimeException` 及其子类都统称为非受检查异常，常见的有（建议记下来，日常开发中会经常用到）：

- `NullPointerException`(空指针错误)
- `IllegalArgumentException`(参数错误比如方法入参类型错误)
- `NumberFormatException`（字符串转换为数字格式错误，`IllegalArgumentException`的子类）
- `ArrayIndexOutOfBoundsException`（数组越界错误）
- `ClassCastException`（类型转换错误）
- `ArithmeticException`（算术错误）
- `SecurityException` （安全错误比如权限不够）
- `UnsupportedOperationException`(不支持的操作错误比如重复创建同一用户)
- ……

---

### [Throwable 类常用方法有哪些？](#throwable-类常用方法有哪些)

- `String getMessage()`: 返回异常发生时的详细信息
- `String toString()`: 返回异常发生时的简要描述
- `String getLocalizedMessage()`: 返回异常对象的本地化信息。使用 `Throwable` 的子类覆盖这个方法，可以生成本地化信息。如果子类没有覆盖该方法，则该方法返回的信息与 `getMessage()`返回的结果相同
- `void printStackTrace()`: 在控制台上打印 `Throwable` 对象封装的异常信息

### [try-catch-finally 如何使用？](#try-catch-finally-如何使用)

- `try`块：用于捕获异常。其后可接零个或多个 `catch` 块，如果没有 `catch` 块，则必须跟一个 `finally` 块。
- `catch`块：用于处理 try 捕获到的异常。
- `finally` 块：无论是否捕获或处理异常，`finally` 块里的语句都会被执行。当在 `try` 块或 `catch` 块中遇到 `return` 语句时，`finally` 语句块将在方法返回之前被执行。

！！！**不要在 finally 语句块中使用 return!** 



~~~java
try {
    System.out.println("Try to do something");
    throw new RuntimeException("RuntimeException");
} catch (Exception e) {
    System.out.println("Catch Exception -> " + e.getMessage());
    // 终止当前正在运行的Java虚拟机
    System.exit(1);  //虚拟机被终止运行
} finally {
    System.out.println("Finally");
}
// finally 之前虚拟机被终止运行的话，finally 中的代码就不会被执行。
~~~



---



### 如何使用 `try-with-resources` 代替`try-catch-finally`？

1. **适用范围（资源的定义）：** 任何实现 `java.lang.AutoCloseable`或者 `java.io.Closeable` 的对象
2. **关闭资源和 finally 块的执行顺序：** 在 `try-with-resources` 语句中，任何 catch 或 finally 块在声明的资源关闭后运行

<span style="color:#990000;">**try(声明资源)**</span>

面对须要关闭的资源，我们总是应该优先使用 `try-with-resources` 而不是`try-finally`。随之产生的代码更简短，更清晰，产生的异常对我们也更有用。`try-with-resources`语句让我们更容易编写必须要关闭的资源的代码，若采用`try-finally`则几乎做不到这点

Java 中类似于`InputStream`、`OutputStream`、`Scanner`、`PrintWriter`等的资源都需要我们调用`close()`方法来手动关闭，一般情况下我们都是通过`try-catch-finally`语句来实现这个需求，如下:

~~~java
//读取文本文件的内容
Scanner scanner = null;
try {
    scanner = new Scanner(new File("D://read.txt"));
    while (scanner.hasNext()) {
        System.out.println(scanner.nextLine());
    }
} catch (FileNotFoundException e) {
    e.printStackTrace();
} finally {
    if (scanner != null) {
        scanner.close();
    }
}
~~~

使用 Java 7 之后的 `try-with-resources` 语句改造上面的代码:

~~~java
try (Scanner scanner = new Scanner(new File("test.txt"))) {
    while (scanner.hasNext()) {
        System.out.println(scanner.nextLine());
    }
} catch (FileNotFoundException fnfe) {
    fnfe.printStackTrace();
}

try (BufferedInputStream bin = new BufferedInputStream(new FileInputStream(new File("test.txt")));  // 分号分割
     BufferedOutputStream bout = new BufferedOutputStream(new FileOutputStream(new File("out.txt")))) {
    int b;
    while ((b = bin.read()) != -1) {
        bout.write(b);
    }
}
catch (IOException e) {
    e.printStackTrace();
}
~~~







---



### [异常使用有哪些需要注意的地方？](#异常使用有哪些需要注意的地方)

- <span style="color:#990000;">不要把异常定义为静态变量</span>，因为这样会导致异常栈信息错乱。每次手动抛出异常，我们都需要手动 new 一个异常对象抛出。
- 抛出的异常信息一定要**<span style="color:#990000;">有意义。</span>**
- 建议抛出**<span style="color:#990000;">更加具体的异常</span>**，比如字符串转换为数字格式错误的时候应该抛出`NumberFormatException`**而不是其父类`IllegalArgumentException`。**
- <span style="color:#990000;">避免重复记录日志：如果在捕获异常的地方已经记录了足够的信息（包括异常类型、错误信息和堆栈跟踪等），那么在业务代码中再次抛出这个异常时，就不应该再次记录相同的错误信息。重复记录日志会使得日志文件膨胀，并且可能会掩盖问题的实际原因，使得问题更难以追踪和解决。</span>
- <span style="color:#990000;">……</span>

---

## ==泛型==

编译器可以对泛型参数进行检测，并且通过泛型参数可以指定传入的对象类型。比如 `ArrayList<Person> persons = new ArrayList<Person>()` 这行代码就指明了该 `ArrayList` 对象只能传入 `Person` 对象，如果传入其他类型的对象就会报错。

**泛型类**、**泛型接口**、**泛型方法**

![image-20250510143617858](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510143617858.png)





![image-20250510143624843](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510143624843.png)



![image-20250510143633068](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510143633068.png)



![image-20250510143647605](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510143647605.png)

泛型和 `Object` 的区别在于 **编译期类型安全 + 可读性 + 避免强转**



### 泛型(**Generics**)其他用法

- 泛型只在编译时有效，运行时类型信息被**擦除。**
- 无法直接通过反射获取泛型类型（但可通过`ParameterizedType`间接获取）

## 反射



**反射（Reflection）** 是指程序在运行时动态地查看、修改和调用类、方法、属性的机制。

![image-20250925211147341](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925211147341.png)

私有方法和 字段值都是可以访问/调用的 

类的信息可以运行时获取

对象可以不知道类的具体硬编码名字就可创建实例化了

![image-20250925211946141](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250925211946141.png)

本质就是配置文件通过反射拿到配置类的元数据 和各种信息 然后将属性注入





---





**`List<String>` 和 `List<Object>` 有什么关系？**

- 无继承关系！`List<String>`不是`List<Object>`的子类（泛型不可变）。
- 如果需要兼容，使用通配符：`List<? extends Object>`。

~~~java
// 上限通配符（? extends T）：只能读取，不能写入（Producer Extends）
public void printList(List<? extends Number> list) {
    for (Number num : list) {  // 安全读取
        System.out.println(num);
    }
    // list.add(1);  // 编译错误！
}

// 下限通配符（? super T）：只能写入，读取为Object（Consumer Super）
public void addNumbers(List<? super Integer> list) {
    list.add(1);  // 安全写入
    // Integer num = list.get(0);  // 编译错误！
}



~~~







## 注解

![image-20250510143721738](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510143721738.png)



<span style="color:#FF0000;">**注解生效前提是一定要被解析**    </span>

**📘 常见的三种 Retention 策略**

源码级 编译级 运行级别

| RetentionPolicy   | 描述                                                   | 使用场景示例                                          |
| ----------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| `SOURCE`          | **只在源代码中存在**，编译后丢弃，不进入 `.class` 文件 | `@Override`, `@SuppressWarnings`                      |
| `CLASS`（默认值） | 编译时保留在 `.class` 文件中，但运行时不可访问         | 编译工具/注解处理器使用，例如 Lombok                  |
| `RUNTIME`         | **运行时仍然保留**，可通过反射获取                     | 框架注解，如 Spring 的 `@Autowired`、JPA 的 `@Entity` |

**❌ `CLASS` 级别的注解在运行时无法读取**

`@Retention(RetentionPolicy.CLASS)` 表示这个注解：

- 在 **编译后保留到 `.class` 文件中**；
- **但 JVM 在运行时不会加载它**，所以你**无法通过反射获取它**；
- **==因此对程序的运行逻辑没有任何直接影响。==**

**自定义注解：**

~~~java
package com.sky.annotation;
// 自定义注解，用于标识某个方法需要进行功能字段自动填充处理
@Target(ElementType.METHOD) // 指定注解的作用目标为方法
@Retention(RetentionPolicy.RUNTIME) // 指定注解的生命周期为运行时
public @interface AutoFill {
    // 指定数据库操作类型
    OperationType value(); // 注解的属性，类型为 OperationType 枚举类型
}
~~~

### 注解的应用 AOP

~~~~java
package com.sky.enumeration;

/**
 * 数据库操作类型
 */
public enum OperationType {

    /**
     * 更新操作
     */
    UPDATE,

    /**
     * 插入操作
     */
    INSERT

}

// 注解的使用
//
//@AutoFill(value = OperationType.INSERT)
//void insert(Dish dish);
~~~~





### 枚举类的基本用法

~~~java
public enum HttpStatus {
    OK(200, "Success"),
    NOT_FOUND(404, "Resource Not Found"),
    SERVER_ERROR(500, "Internal Server Error");

    private final int code;      // 枚举属性
    private final String desc;   // 枚举属性

    // 构造方法（默认private）
    HttpStatus(int code, String desc) {
        this.code = code;
        this.desc = desc;
    }

    // Getter方法
    public int getCode() { return code; }
    public String getDesc() { return desc; }
}

HttpStatus status = HttpStatus.OK;
System.out.println(status.getCode());  // 输出: 200
~~~

**枚举类替代常量类**

![image-20250510144753246](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510144753246.png)



---





### 注解 应用在切面类中





| 通知类型  | 执行时机                               | 是否能控制目标方法执行 | 是否能修改返回值或异常 |
| --------- | -------------------------------------- | ---------------------- | ---------------------- |
| `@Before` | 在目标方法执行**之前**                 | ❌ 不能阻止             | ❌ 不能修改             |
| `@After`  | 在目标方法执行**之后**（无论是否异常） | ❌ 不能阻止             | ❌ 不能修改             |
| `@Around` | **包裹目标方法**执行（前后都能插入）   | ✅ 可以控制是否执行     | ✅ 可以修改             |

~~~java
package com.sky.aspect;

@Aspect  // 表明是个 切面类
@Component
@Slf4j  // @Slf4j 是 Lombok 提供的一个注解  swagger 是 knife4j
public class AutoFillAspect {
    // 指定切入点
    @Pointcut("execution(* com.sky.mapper.*.*(..)) && @annotation(com.sky.annotation.AutoFill)") // 用Pointcut注解中的属性来指定对哪些方法进行增强 也就是指定增强哪些方法
    public void autoFillPointCut(){}


    // 通知 就是对代码进行增强的部分
    @Before("autoFillPointCut()")
    public void autoFill(JoinPoint joinPoint){ // 就是那些实际业务中被增强的方法
        // 获取到当前被拦截的方法上的数据库操作类型
        MethodSignature signature = (MethodSignature) joinPoint.getSignature(); // 方法签名对象（签名对象的子接口）
        AutoFill autoFillAnnotation = signature.getMethod().getAnnotation(AutoFill.class);// 获取方法上的注解对象
        OperationType value = autoFillAnnotation.value();// 获取数据库操作类型

        // 获取实体对象（也就是被拦截（加强）方法的参数） 然后准备 数据 对这些实体对象 赋值  通过反射操作
        Object[] args = joinPoint.getArgs(); // 这里是获取所有参数
        if(args == null || args.length == 0) return ;

        Object entity = args[0]; // 这里做好约定 第一个参数就是实体对象（when someone coding）  使用object来接收 因为 实体对象可能存在很多类型（有多个业务多个实体类的）
        LocalDateTime now = LocalDateTime.now();
        Long currentId = BaseContext.getCurrentId();
        // 根据不同的操作类型不同的处理逻辑
        if(value == OperationType.INSERT) {
            // 通过反射赋值
            // 这种经常用的常量就不要硬编码了容易出错而且耦合
            try {
                // 获取方法 方法名+参数类型
                Method setCreateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_CREATE_TIME, LocalDateTime.class);
                Method setUpdateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_TIME, LocalDateTime.class);
                Method setCreateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_CREATE_USER, Long.class);
                Method setUpdateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_USER, Long.class);

                // 开始调用方法
                setCreateTime.invoke(entity,now); // 这里的两个参数分别是 被增强的方法的实体对象 和 方法的参数
                setUpdateTime.invoke(entity,now);
                setCreateUser.invoke(entity,currentId);
                setUpdateUser.invoke(entity,currentId);

            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }else if(value == OperationType.UPDATE) {
            try {
                Method setUpdateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_TIME, LocalDateTime.class);
                Method setUpdateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_USER, Long.class);
                setUpdateTime.invoke(entity,now);
                setUpdateUser.invoke(entity,currentId);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }

        }
    }

}

~~~

~~~java
@Around("execution(* UserService.login(..))")
public Object aroundLogin(ProceedingJoinPoint joinPoint) throws Throwable {
    System.out.println("【Around - 前】开始登录校验");

    Object result = joinPoint.proceed();  // 继续执行目标方法

    System.out.println("【Around - 后】登录结果：" + result);
    return result;
}
// 环绕通知可以控制被增强方法 和扩展代码的执行结构 以及自定义返回数据
~~~





---



## <span style="color:#990000;">重要知识点</span>

### 值传递

- **实参（实际参数，Arguments）**：用于**传递**给函数/方法的参数，必须有确定的值。
- **形参（形式参数，Parameters）**：用于**定义函数/方法，接收实参**，不需要有确定的值

这里传递的还是值，不过，这个值是实参的地址罢了！

也就是说 `change` 方法的参数拷贝的是 `arr` （实参）的地址，因此，它和 `arr` 指向的是同一个数组对象。这也就说明了为什么方法内部对形参的修改会影响到实参。

为了更强有力地反驳 Java 对引用类型的参数采用的不是引用传递，我们再来看下面这个案例！

~~~java
  public static void main(String[] args) {
      int[] arr = { 1, 2, 3, 4, 5 };
      System.out.println(arr[0]);
      change(arr);
      System.out.println(arr[0]);
  }

  public static void change(int[] array) {
      // 将数组的第一个元素变为0
      array[0] = 0;
  }
~~~

![image-20250510155919014](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510155919014.png)

~~~java
public class Person {
    private String name;
   // 省略构造函数、Getter&Setter方法
}

public static void main(String[] args) {
    Person xiaoZhang = new Person("小张");
    Person xiaoLi = new Person("小李");
    swap(xiaoZhang, xiaoLi);
    System.out.println("xiaoZhang:" + xiaoZhang.getName());
    System.out.println("xiaoLi:" + xiaoLi.getName());
}

public static void swap(Person person1, Person person2) {
    Person temp = person1;
    person1 = person2;
    person2 = temp;
    System.out.println("person1:" + person1.getName());
    System.out.println("person2:" + person2.getName());
}

// output:
person1:小李
person2:小张
xiaoZhang:小张
xiaoLi:小李
~~~

![image-20250510155913507](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510155913507.png)









- 如果参数是基本类型的话，很简单，传递的就是基本类型的字面量值的拷贝，会创建副本。
- 如果参数是引用类型，传递的就是实参所引用的对象在堆中地址值的拷贝，同样**也会创建副本。**



---

### ==Java 8 新特性==

![image-20251203203042077](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251203203042077.png)



![image-20251203203730448](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251203203730448.png)



## Future 和 completableFuture 区别



---



## NIO 与 BIO

### 高并发时，NIO 怎么扛住？

假设突然来了 1000 个客户端同时发请求（高并发）：

- **BIO 的骚操作**：必须启动 1000 个线程，每个线程堵在那等数据，内存和 CPU 直接炸穿（线程切换成本太高）。

- NIO 的骚操作

  ：

  1. 1 个 Selector 线程盯着这 1000 个连接，轮询谁的数据准备好了（非阻塞，绝不傻等）。
  2. 假设同时有 50 个连接的数据就绪了，Selector 线程把这 50 个任务分给一个包含 20 个线程的线程池（比如用`ExecutorService`）。
  3. 20 个线程分工处理这 50 个任务（比如每个线程处理 2-3 个），处理完就回池子里待命，等着 Selector 再分配新任务。

“每个连接占一个线程、从头到尾堵着”（也就是 BIO 的多线程模式），高并发时会直接把系统干崩，具体惨状分这几步：

### 1. 线程资源被榨干，内存直接爆掉

线程本身是很 “重” 的资源：

- 每个 Java 线程默认要占**1MB 左右的栈内存**（可通过`-Xss`调整，但再小也有成本）。
- 如果同时有 10000 个连接，就得开 10000 个线程，光栈内存就至少占 10GB—— 普通服务器内存根本扛不住，直接触发`OutOfMemoryError`（内存溢出）。

### 2. CPU 被线程切换 “吃” 光，啥正事都干不了

操作系统切换线程需要保存 / 恢复线程上下文（寄存器、程序计数器等），这是有开销的：

- 假设 1 秒内切换 1000 次线程，每次切换花 10 微秒，光切换成本就占 1% 的 CPU；
- 要是有 10000 个线程，1 秒可能切换几万次，CPU 的 90% 算力都在 “线程切换” 上打转，真正用来处理业务的时间几乎没有 —— 系统会变得巨卡，请求响应慢到超时。

### 3. 连接被 “饿死”，系统彻底失去响应

线程数太多时，操作系统的线程调度器会忙不过来：

- 新的连接请求来了，系统没能力再开新线程，直接拒绝连接；
- 已有的线程排队等着被调度，哪怕数据早就准备好了，也得等几百毫秒才能轮到处理 —— 用户这边看到的就是 “请求超时”“连接失败”，系统彻底瘫痪。

### 序列化 与 反序列化

如果我们需要**持久化 Java 对象比如将 Java 对象保存在文件中，或者在网络传输 Java 对象，这些场景都需要用到序列化。**

简单来说：

- **序列化**：将**数据结构或对象转换成可以存储或传输的形式，通常是二进制字节流，也可以是 JSON, XML 等文本格式**
- **反序列化**：将在序列化过程中所生成的数据转换为原始数据结构或者对象的过程

下面是序列化和反序列化常见应用场景：

- 对象在进行网络传输（比如远程方法调用 RPC 的时候）之前需要先被序列化，接收到序列化的对象之后需要再进行反序列化；
- 将对象存储到文件之前需要进行序列化，将对象从文件中读取出来需要进行反序列化；
- **将对象存储到数据库（如 Redis）之前需要用到序列化，将对象从缓存数据库中读取出来需要反序列化；**
- 将对象存储到内存之前需要进行序列化，从内存中读取出来之后需要进行反序列化

**序列化的主要目的是通过网络传输对象或者说是将对象存储到文件系统、数据库、内存中。**

![image-20250510160136897](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510160136897.png)

**我们知道网络通信的双方必须要采用和遵守相同的协议。TCP/IP 四层模型是下面这样的，序列化协议属于哪一层呢？**

![image-20250510160239555](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510160239555.png)





#### ==常见的序列化协议==

JDK 自带的序列化方式一般不会用 ，因为**序列化效率低并且存在安全问题**。比较常用的序列化协议有 **Hessian、Kryo、Protobuf、ProtoStuff，这些都是基于二进制的序列化协议。**

**像 JSON 和 XML 这种属于文本类序列化方式。虽然可读性比较好，但是性能较差，一般不会选择。**

##### jdk自带的序列化

我们很少或者说几乎不会直接使用 JDK 自带的序列化方式，主要原因有下面这些原因：

- **不支持跨语言调用** : 如果**调用的是其他语言开发的服务**的时候就不支持了。
- **性能差**：相比于其他序列化框架性能更低，主要原因是序列化之后的**字节数组体积较大**，导致传输成本加大。
- **存在安全问题**：序列化和反序列化本身并不存在问题。但当输入的反序列化的数据**可被用户控制**，那么攻击者即可通过**构造恶意输入**，让反序列化产生非预期的对象，在此过程中执行构造的任意代码。



---

##### Kryo



##### Protobuf





##### ProtoStuff





##### Hessian







---



### ==Java代理模式==

代理模式是一种比较好理解的设计模式。简单来说就是 **我们使用代理对象来代替对真实对象(real object)的访问，这样就可以在不修改原目标对象的前提下，提供额外的功能操作，扩展目标对象的功能。**

**代理模式的主要作用是扩展目标对象的功能，比如说在目标对象的某个方法执行前后你可以增加一些自定义的操作。**



**代理模式有静态代理和动态代理**

两者之间的差别：

**灵活性**：动态代理更加灵活，不需要必须实现接口，可以直接代理实现类，并且可以不需要针对每个目标类都创建一个代理类。另外，静态代理中，接口一旦新增加方法，目标对象和代理对象都要进行修改，这是非常麻烦的！

**JVM 层面**：静态代理在编译时就将接口、实现类、代理类这些都变成了一个个实际的 class 文件。而动态代理是在运行时动态生成类字节码，并加载到 JVM 中的



#### 静态代理

静态代理实现步骤:

1. 定义一个接口及其实现类；
2. 创建一个代理类**同样**实现这个接口
3. 将**目标对象注入进代理类**，然后在代理类的对应方法调用目标类中的对应方法。这样的话，我们就可以通过代理类屏蔽对目标对象的访问，**并且可以在目标方法执行前后做一些自己想做的事情。**

---

![image-20250510202644067](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510202644067.png)

![image-20250510202651126](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510202651126.png)

~~~bash
output：
before method send()
send message:java
after method send()
~~~

---




#### 动态代理

相比于静态代理来说，动态代理更加灵活。我们**不需要针对每个目标类**都单独创建一个代理类，并且也**不需要我们必须实现接口**，我们可以**直接代理实现类**( *CGLIB 动态代理机制*)。

**从 JVM 角度来说，动态代理是<span style="color:#FF0000;">在运行时</span>动态生成类字节码，并加载到 JVM 中的。**

说到动态代理，**<span style="color:#FF0000;">Spring AOP、RPC 框架</span>**应该是两个不得不提的，它们的实现都依赖了动态代理。

**动态代理在我们日常开发中使用的相对较少，但是在框架中的几乎是必用的一门技术。学会了动态代理之后，对于我们理解和学习各种框架的原理也非常有帮助。**

就 Java 来说，动态代理的实现方式有很多种，比如 **JDK 动态代理**、**CGLIB 动态代理**等等。

[guide-rpc-framework](https://github.com/Snailclimb/guide-rpc-framework) 使用的是 JDK 动态代理，我们先来看看 JDK 动态代理的使用。

另外，虽然 [guide-rpc-framework](https://github.com/Snailclimb/guide-rpc-framework) 没有用到 **CGLIB 动态代理** ，我们这里还是简单介绍一下其使用以及和**JDK 动态代理**的对比

---

#### JDK动态代理机制





#### CGLIB 动态代理机制



---



### BigDecimal

![image-20250510160739880](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510160739880.png)



![image-20250510160742474](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510160742474.png)



<span style="color:#0000CC;">up</span>  <span style="color:#FF0000;">down</span> <span style="color:#006600;">ceiling</span> <span style="color:#FF8000;">floor </span>



![image-20250510161052923](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510161052923.png)





![image-20250510161258724](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510161258724.png)

![image-20250510161315504](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510161315504.png)

#### BigDecimal 工具类

~~~java
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * 简化BigDecimal计算的小工具类
 */
public class BigDecimalUtil {

    /**
     * 默认除法运算精度
     */
    private static final int DEF_DIV_SCALE = 10;

    private BigDecimalUtil() {
    }

    /**
     * 提供精确的加法运算。
     *
     * @param v1 被加数
     * @param v2 加数
     * @return 两个参数的和
     */
    public static double add(double v1, double v2) {
        BigDecimal b1 = BigDecimal.valueOf(v1);
        BigDecimal b2 = BigDecimal.valueOf(v2);
        return b1.add(b2).doubleValue();
    }

    /**
     * 提供精确的减法运算。
     *
     * @param v1 被减数
     * @param v2 减数
     * @return 两个参数的差
     */
    public static double subtract(double v1, double v2) {
        BigDecimal b1 = BigDecimal.valueOf(v1);
        BigDecimal b2 = BigDecimal.valueOf(v2);
        return b1.subtract(b2).doubleValue();
    }

    /**
     * 提供精确的乘法运算。
     *
     * @param v1 被乘数
     * @param v2 乘数
     * @return 两个参数的积
     */
    public static double multiply(double v1, double v2) {
        BigDecimal b1 = BigDecimal.valueOf(v1);
        BigDecimal b2 = BigDecimal.valueOf(v2);
        return b1.multiply(b2).doubleValue();
    }

    /**
     * 提供（相对）精确的除法运算，当发生除不尽的情况时，精确到
     * 小数点以后10位，以后的数字四舍五入。
     *
     * @param v1 被除数
     * @param v2 除数
     * @return 两个参数的商
     */
    public static double divide(double v1, double v2) {
        return divide(v1, v2, DEF_DIV_SCALE);
    }

    /**
     * 提供（相对）精确的除法运算。当发生除不尽的情况时，由scale参数指
     * 定精度，以后的数字四舍五入。
     *
     * @param v1    被除数
     * @param v2    除数
     * @param scale 表示表示需要精确到小数点以后几位。
     * @return 两个参数的商
     */
    public static double divide(double v1, double v2, int scale) {
        if (scale < 0) {
            throw new IllegalArgumentException(
                    "The scale must be a positive integer or zero");
        }
        BigDecimal b1 = BigDecimal.valueOf(v1);
        BigDecimal b2 = BigDecimal.valueOf(v2);
        return b1.divide(b2, scale, RoundingMode.HALF_EVEN).doubleValue();
    }

    /**
     * 提供精确的小数位四舍五入处理。
     *
     * @param v     需要四舍五入的数字
     * @param scale 小数点后保留几位
     * @return 四舍五入后的结果
     */
    public static double round(double v, int scale) {
        if (scale < 0) {
            throw new IllegalArgumentException(
                    "The scale must be a positive integer or zero");
        }
        BigDecimal b = BigDecimal.valueOf(v);
        BigDecimal one = new BigDecimal("1");
        return b.divide(one, scale, RoundingMode.HALF_UP).doubleValue();
    }

    /**
     * 提供精确的类型转换(Float)
     *
     * @param v 需要被转换的数字
     * @return 返回转换结果
     */
    public static float convertToFloat(double v) {
        BigDecimal b = new BigDecimal(v);
        return b.floatValue();
    }

    /**
     * 提供精确的类型转换(Int)不进行四舍五入
     *
     * @param v 需要被转换的数字
     * @return 返回转换结果
     */
    public static int convertsToInt(double v) {
        BigDecimal b = new BigDecimal(v);
        return b.intValue();
    }

    /**
     * 提供精确的类型转换(Long)
     *
     * @param v 需要被转换的数字
     * @return 返回转换结果
     */
    public static long convertsToLong(double v) {
        BigDecimal b = new BigDecimal(v);
        return b.longValue();
    }

    /**
     * 返回两个数中大的一个值
     *
     * @param v1 需要被对比的第一个数
     * @param v2 需要被对比的第二个数
     * @return 返回两个数中大的一个值
     */
    public static double returnMax(double v1, double v2) {
        BigDecimal b1 = new BigDecimal(v1);
        BigDecimal b2 = new BigDecimal(v2);
        return b1.max(b2).doubleValue();
    }

    /**
     * 返回两个数中小的一个值
     *
     * @param v1 需要被对比的第一个数
     * @param v2 需要被对比的第二个数
     * @return 返回两个数中小的一个值
     */
    public static double returnMin(double v1, double v2) {
        BigDecimal b1 = new BigDecimal(v1);
        BigDecimal b2 = new BigDecimal(v2);
        return b1.min(b2).doubleValue();
    }

    /**
     * 精确对比两个数字
     *
     * @param v1 需要被对比的第一个数
     * @param v2 需要被对比的第二个数
     * @return 如果两个数一样则返回0，如果第一个数比第二个数大则返回1，反之返回-1
     */
    public static int compareTo(double v1, double v2) {
        BigDecimal b1 = BigDecimal.valueOf(v1);
        BigDecimal b2 = BigDecimal.valueOf(v2);
        return b1.compareTo(b2);
    }

}
~~~





---



### ==java魔法类Unsafe==



### ==java SPI机制  与  API==





### java 语法糖

[java语法糖.md](java语法糖.md)

