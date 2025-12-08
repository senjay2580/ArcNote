[IO 流简介](#io-流简介)
-----------------

IO 即 `Input/Output`，输入和输出。数据输入到计算机内存的过程即输入，反之输出到外部存储（比如数据库，文件，远程主机）的过程即输出。数据传输过程类似于水流，因此称为 IO 流。IO 流在 Java 中分为输入流和输出流，而根据数据的处理方式又分为字节流和字符流。

**Java IO 流的 40 多个类都是从如下 4 个抽象类基类**中派生出来的。

*   `InputStream`/`Reader`: 所有的输入流的基类，前者是**字节输入流，后者是字符输入流。**
*   `OutputStream`/`Writer`: 所有输出流的基类，前者是**字节输出流，后者是字符输出流。**

[字节流](#字节流)
-----------

### [InputStream（字节输入流）](#inputstream-字节输入流)

`InputStream`用于从源头（通常是文件）读取数据（字节信息）到内存中，`java.io.InputStream`抽象类是所有字节输入流的父类。

`InputStream` 常用方法：

*   `read()`：返回输入流中下一个字节的数据。返回的值介于 0 到 255 之间。如果未读取任何字节，则代码返回 `-1` ，表示文件结束。
*   `read(byte b[ ])` : 从输入流中读取一些字节存储到数组 `b` 中。如果数组 `b` 的长度为零，则不读取。如果没有可用字节读取，返回 `-1`。如果有可用字节读取，则最多读取的字节数最多等于 `b.length` ， 返回读取的字节数。这个方法等价于 `read(b, 0, b.length)`。
*   `read(byte b[], int off, int len)`：在`read(byte b[ ])` 方法的基础上增加了 `off` 参数（偏移量）和 `len` 参数（要读取的最大字节数）。
*   `skip(long n)`：忽略输入流中的 n 个字节 , 返回实际忽略的字节数。
*   `available()`：返回输入流中可以读取的字节数。
*   `close()`：关闭输入流释放相关的系统资源。

从 Java 9 开始，`InputStream` 新增加了多个实用的方法：

*   `readAllBytes()`：读取输入流中的所有字节，返回字节数组。
*   `readNBytes(byte[] b, int off, int len)`：阻塞直到读取 `len` 个字节。
*   `transferTo(OutputStream out)`：将所有字节从一个输入流传递到一个输出流。

`FileInputStream` 是一个比较常用的字节输入流对象，可直接指定文件路径，可以直接读取单字节数据，也可以读取至字节数组中。

`FileInputStream` 代码示例：

```java
try (InputStream fis = new FileInputStream("input.txt")) {
    System.out.println("Number of remaining bytes:"
            + fis.available());
    int content;
    long skip = fis.skip(2);
    System.out.println("The actual number of bytes skipped:" + skip);
    System.out.print("The content read from file:");
    while ((content = fis.read()) != -1) {
        System.out.print((char) content);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

`input.txt` 文件内容：

![](https://oss.javaguide.cn/github/javaguide/java/image-20220419155214614.png)

输出：

```java
Number of remaining bytes:11
The actual number of bytes skipped:2
The content read from file:JavaGuide
```

不过，一般我们是不会直接单独使用 `FileInputStream` ，通常会配合 `BufferedInputStream`（字节缓冲输入流，后文会讲到）来使用。

像下面这段代码在我们的项目中就比较常见，我们通过 `readAllBytes()` 读取输入流所有字节并将其直接赋值给一个 `String` 对象。

```java
// 新建一个 BufferedInputStream 对象
BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream("input.txt"));
// 读取文件的内容并复制到 String 对象中
String result = new String(bufferedInputStream.readAllBytes());
System.out.println(result);
```

`DataInputStream` 用于读取指定类型数据，不能单独使用，必须结合其它流，比如 `FileInputStream` 。

```java
FileInputStream fileInputStream = new FileInputStream("input.txt");
//必须将fileInputStream作为构造参数才能使用
DataInputStream dataInputStream = new DataInputStream(fileInputStream);
//可以读取任意具体的类型数据
dataInputStream.readBoolean();
dataInputStream.readInt();
dataInputStream.readUTF();
```

`ObjectInputStream` 用于从输入流中读取 Java 对象（反序列化），`ObjectOutputStream` 用于将对象写入到输出流 (序列化)。

```java
ObjectInputStream input = new ObjectInputStream(new FileInputStream("object.data"));
MyClass object = (MyClass) input.readObject();
input.close();
```

另外，用于序列化和反序列化的类必须实现 `Serializable` 接口，对象中如果有属性不想被序列化，使用 `transient` 修饰。

### [OutputStream（字节输出流）](#outputstream-字节输出流)

`OutputStream`用于将数据（字节信息）写入到目的地（通常是文件），`java.io.OutputStream`抽象类是所有字节输出流的父类。

`OutputStream` 常用方法：

*   `write(int b)`：将特定字节写入输出流。
*   `write(byte b[ ])` : 将数组`b` 写入到输出流，等价于 `write(b, 0, b.length)` 。
*   `write(byte[] b, int off, int len)` : 在`write(byte b[ ])` 方法的基础上增加了 `off` 参数（偏移量）和 `len` 参数（要读取的最大字节数）。
*   `flush()`：刷新此输出流并强制写出所有缓冲的输出字节。
*   `close()`：关闭输出流释放相关的系统资源。

`FileOutputStream` 是最常用的字节输出流对象，可直接指定文件路径，可以直接输出单字节数据，也可以输出指定的字节数组。

`FileOutputStream` 代码示例：

```java
try (FileOutputStream output = new FileOutputStream("output.txt")) {
    byte[] array = "JavaGuide".getBytes();
    output.write(array);
} catch (IOException e) {
    e.printStackTrace();
}
```

运行结果：

![](https://oss.javaguide.cn/github/javaguide/java/image-20220419155514392.png)

类似于 `FileInputStream`，`FileOutputStream` 通常也会配合 `BufferedOutputStream`（字节缓冲输出流，后文会讲到）来使用。

```java
FileOutputStream fileOutputStream = new FileOutputStream("output.txt");
BufferedOutputStream bos = new BufferedOutputStream(fileOutputStream)
```

**`DataOutputStream`** 用于写入指定类型数据，不能单独使用，必须结合其它流，比如 `FileOutputStream` 。

```java
// 输出流
FileOutputStream fileOutputStream = new FileOutputStream("out.txt");
DataOutputStream dataOutputStream = new DataOutputStream(fileOutputStream);
// 输出任意数据类型
dataOutputStream.writeBoolean(true);
dataOutputStream.writeByte(1);
```

`ObjectInputStream` 用于从输入流中读取 Java 对象（`ObjectInputStream`, 反序列化），`ObjectOutputStream`将对象写入到输出流 (`ObjectOutputStream`，序列化)。

```java
ObjectOutputStream output = new ObjectOutputStream(new FileOutputStream("file.txt")
Person person = new Person("Guide哥", "JavaGuide作者");
output.writeObject(person);
```

[字符流](#字符流)
-----------

不管是文件读写还是网络发送接收，信息的最小存储单元都是字节。 **那为什么 I/O 流操作要分为字节流操作和字符流操作呢？**

个人认为主要有两点原因：

*   字符流是由 Java 虚拟机将字节转换得到的，这个过程还算是比较耗时。
*   如果我们不知道编码类型就很容易出现乱码问题。

乱码问题这个很容易就可以复现，我们只需要将上面提到的 `FileInputStream` 代码示例中的 `input.txt` 文件内容改为中文即可，原代码不需要改动。

![](https://oss.javaguide.cn/github/javaguide/java/image-20220419154632551.png)

输出：

```java
Number of remaining bytes:9
The actual number of bytes skipped:2
The content read from file:§å®¶å¥½
```

可以很明显地看到读取出来的内容已经变成了乱码。

因此，I/O 流就干脆提供了一个直接操作字符的接口，方便我们平时对字符进行流操作。如果音频文件、图片等媒体文件用字节流比较好，如果涉及到字符的话使用字符流比较好。

字符流默认采用的是 `Unicode` 编码，我们可以通过构造方法自定义编码。

Unicode 本身只是一种字符集，它为每个字符分配一个唯一的数字编号，并没有规定具体的存储方式。UTF-8、UTF-16、UTF-32 都是 Unicode 的编码方式，它们使用不同的字节数来表示 Unicode 字符。例如，UTF-8 : 英文占 1 字节，中文占 3 字节。

### [Reader（字符输入流）](#reader-字符输入流)

`Reader`用于从源头（通常是文件）读取数据（字符信息）到内存中，`java.io.Reader`抽象类是所有字符输入流的父类。

`Reader` 用于读取文本， `InputStream` 用于读取原始字节。

`Reader` 常用方法：

*   `read()` : 从输入流读取一个字符。
*   `read(char[] cbuf)` : 从输入流中读取一些字符，并将它们存储到字符数组 `cbuf`中，等价于 `read(cbuf, 0, cbuf.length)` 。
*   `read(char[] cbuf, int off, int len)`：在`read(char[] cbuf)` 方法的基础上增加了 `off` 参数（偏移量）和 `len` 参数（要读取的最大字符数）。
*   `skip(long n)`：忽略输入流中的 n 个字符 , 返回实际忽略的字符数。
*   `close()` : 关闭输入流并释放相关的系统资源。

`InputStreamReader` 是字节流转换为字符流的桥梁，其子类 `FileReader` 是基于该基础上的封装，可以直接操作字符文件。

```java
// 字节流转换为字符流的桥梁
public class InputStreamReader extends Reader {
}
// 用于读取字符文件
public class FileReader extends InputStreamReader {
}
```

`FileReader` 代码示例：

```java
try (FileReader fileReader = new FileReader("input.txt");) {
    int content;
    long skip = fileReader.skip(3);
    System.out.println("The actual number of bytes skipped:" + skip);
    System.out.print("The content read from file:");
    while ((content = fileReader.read()) != -1) {
        System.out.print((char) content);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

`input.txt` 文件内容：

![](https://oss.javaguide.cn/github/javaguide/java/image-20220419154632551.png)

输出：

```java
The actual number of bytes skipped:3
The content read from file:我是Guide。
```

### [Writer（字符输出流）](#writer-字符输出流)

`Writer`用于将数据（字符信息）写入到目的地（通常是文件），`java.io.Writer`抽象类是所有字符输出流的父类。

`Writer` 常用方法：

*   `write(int c)` : 写入单个字符。
*   `write(char[] cbuf)`：写入字符数组 `cbuf`，等价于`write(cbuf, 0, cbuf.length)`。
*   `write(char[] cbuf, int off, int len)`：在`write(char[] cbuf)` 方法的基础上增加了 `off` 参数（偏移量）和 `len` 参数（要读取的最大字符数）。
*   `write(String str)`：写入字符串，等价于 `write(str, 0, str.length())` 。
*   `write(String str, int off, int len)`：在`write(String str)` 方法的基础上增加了 `off` 参数（偏移量）和 `len` 参数（要读取的最大字符数）。
*   `append(CharSequence csq)`：将指定的字符序列附加到指定的 `Writer` 对象并返回该 `Writer` 对象。
*   `append(char c)`：将指定的字符附加到指定的 `Writer` 对象并返回该 `Writer` 对象。
*   `flush()`：刷新此输出流并强制写出所有缓冲的输出字符。
*   `close()`: 关闭输出流释放相关的系统资源。

`OutputStreamWriter` 是字符流转换为字节流的桥梁，其子类 `FileWriter` 是基于该基础上的封装，可以直接将字符写入到文件。

```java
// 字符流转换为字节流的桥梁
public class OutputStreamWriter extends Writer {
}
// 用于写入字符到文件
public class FileWriter extends OutputStreamWriter {
}
```

`FileWriter` 代码示例：

```java
try (Writer output = new FileWriter("output.txt")) {
    output.write("你好，我是Guide。");
} catch (IOException e) {
    e.printStackTrace();
}
```

输出结果：

![](https://oss.javaguide.cn/github/javaguide/java/image-20220419155802288.png)

[字节缓冲流](#字节缓冲流)
---------------

**IO 操作是很消耗性能的，缓冲流将数据加载至缓冲区，一次性读取 / 写入多个字节，从而避免频繁的 IO 操作，提高流的传输效率**。

字节缓冲流这里采用了<span style="color:#FF0000;">**装饰器模式**</span>来增强 `InputStream` 和`OutputStream`子类对象的功能。

举个例子，我们可以通过 `BufferedInputStream`（字节缓冲输入流）来增强 `FileInputStream` 的功能。

**就是用BufferedInputStream 去包装它 增强这个 类的方法的功能**

```java
// 新建一个 BufferedInputStream 对象
BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream("input.txt"));
```

**字节流和字节缓冲流的性能差别主要体现在我们使用两者的时候都是调用 `write(int b)` 和 `read()` 这两个一次只读取一个字节的方法的时候。由于字节缓冲流内部有缓冲区（字节数组），因此，字节缓冲流会先将读取到的字节存放在缓存区，<span style="color:#0000FF;">大幅减少 IO 次数(缓冲区将多次小数据操作合并为一次大数据操作)</span>，提高读取效率。**



<span style="color:#FF0000;">：每次 I/O 操作（如读写磁盘、网络）都需要从用户态切换到内核态，频繁切换会产生性能损耗。缓冲区通过批量处理数据，减少系统调用次数</span>



---



我使用 `write(int b)` 和 `read()` 方法，分别通过字节流和字节缓冲流复制一个 `524.9 mb` 的 PDF 文件耗时对比如下：

```java
使用缓冲流复制PDF文件总耗时:15428 毫秒
使用普通字节流复制PDF文件总耗时:2555062 毫秒
```

两者耗时差别非常大，缓冲流耗费的时间是字节流的 1/165。

测试代码如下:

```java
@Test
void copy_pdf_to_another_pdf_buffer_stream() {
    // 记录开始时间
    long start = System.currentTimeMillis();
    try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream("深入理解计算机操作系统.pdf"));
         BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("深入理解计算机操作系统-副本.pdf"))) {
        int content;
        while ((content = bis.read()) != -1) {
            bos.write(content);
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
    // 记录结束时间
    long end = System.currentTimeMillis();
    System.out.println("使用缓冲流复制PDF文件总耗时:" + (end - start) + " 毫秒");
}

@Test
void copy_pdf_to_another_pdf_stream() {
    // 记录开始时间
    long start = System.currentTimeMillis();
    try (FileInputStream fis = new FileInputStream("深入理解计算机操作系统.pdf");
         FileOutputStream fos = new FileOutputStream("深入理解计算机操作系统-副本.pdf")) {
        int content;
        while ((content = fis.read()) != -1) {
            fos.write(content);
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
    // 记录结束时间
    long end = System.currentTimeMillis();
    System.out.println("使用普通流复制PDF文件总耗时:" + (end - start) + " 毫秒");
}
```

如果是调用 `read(byte b[])` 和 `write(byte b[], int off, int len)` 这两个写入一个字节数组的方法的话，只要字节数组的大小合适，两者的性能差距其实不大，基本可以忽略。

这次我们使用 `read(byte b[])` 和 `write(byte b[], int off, int len)` 方法，分别通过字节流和字节缓冲流复制一个 524.9 mb 的 PDF 文件耗时对比如下：

```java
使用缓冲流复制PDF文件总耗时:695 毫秒
使用普通字节流复制PDF文件总耗时:989 毫秒
```

两者耗时差别不是很大，缓冲流的性能要略微好一点点。

测试代码如下：

```java
@Test
void copy_pdf_to_another_pdf_with_byte_array_buffer_stream() {
    // 记录开始时间
    long start = System.currentTimeMillis();
    try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream("深入理解计算机操作系统.pdf"));
         BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("深入理解计算机操作系统-副本.pdf"))) {
        int len;
        byte[] bytes = new byte[4 * 1024];
        while ((len = bis.read(bytes)) != -1) {
            bos.write(bytes, 0, len);
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
    // 记录结束时间
    long end = System.currentTimeMillis();
    System.out.println("使用缓冲流复制PDF文件总耗时:" + (end - start) + " 毫秒");
}

@Test
void copy_pdf_to_another_pdf_with_byte_array_stream() {
    // 记录开始时间
    long start = System.currentTimeMillis();
    try (FileInputStream fis = new FileInputStream("深入理解计算机操作系统.pdf");
         FileOutputStream fos = new FileOutputStream("深入理解计算机操作系统-副本.pdf")) {
        int len;
        byte[] bytes = new byte[4 * 1024];
        while ((len = fis.read(bytes)) != -1) {
            fos.write(bytes, 0, len);
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
    // 记录结束时间
    long end = System.currentTimeMillis();
    System.out.println("使用普通流复制PDF文件总耗时:" + (end - start) + " 毫秒");
}
```

### [BufferedInputStream（字节缓冲输入流）](#bufferedinputstream-字节缓冲输入流)

`BufferedInputStream` 从源头（通常是文件）读取数据（字节信息）到内存的过程中不会一个字节一个字节的读取，而是会先将读取到的字节存放在缓存区，并从内部缓冲区中单独读取字节。这样大幅减少了 IO 次数，提高了读取效率。

`BufferedInputStream` 内部维护了一个缓冲区，这个缓冲区实际就是一个字节数组，通过阅读 `BufferedInputStream` 源码即可得到这个结论。

```java
public
class BufferedInputStream extends FilterInputStream {
    // 内部缓冲区数组
    protected volatile byte buf[];
    // 缓冲区的默认大小
    private static int DEFAULT_BUFFER_SIZE = 8192;
    // 使用默认的缓冲区大小
    public BufferedInputStream(InputStream in) {
        this(in, DEFAULT_BUFFER_SIZE);
    }
    // 自定义缓冲区大小
    public BufferedInputStream(InputStream in, int size) {
        super(in);
        if (size <= 0) {
            throw new IllegalArgumentException("Buffer size <= 0");
        }
        buf = new byte[size];
    }
}
```

缓冲区的大小默认为 **8192** 字节，当然了，你也可以通过 `BufferedInputStream(InputStream in, int size)` 这个构造方法来指定缓冲区的大小。

### [BufferedOutputStream（字节缓冲输出流）](#bufferedoutputstream-字节缓冲输出流)

`BufferedOutputStream` 将数据（字节信息）写入到目的地（通常是文件）的过程中不会一个字节一个字节的写入，而是会先将要写入的字节存放在缓存区，并从内部缓冲区中单独写入字节。这样大幅减少了 IO 次数，提高了效率

```java
try (BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("output.txt"))) {
    byte[] array = "JavaGuide".getBytes();
    bos.write(array);
} catch (IOException e) {
    e.printStackTrace();
}
```

类似于 `BufferedInputStream` ，`BufferedOutputStream` 内部也维护了一个缓冲区，并且，这个缓存区的大小也是 **8192** 字节。

[字符缓冲流](#字符缓冲流)
---------------

`BufferedReader` （字符缓冲输入流）和 `BufferedWriter`（字符缓冲输出流）类似于 `BufferedInputStream`（字节缓冲输入流）和`BufferedOutputStream`（字节缓冲输入流），内部都维护了一个字节数组作为缓冲区。不过，前者主要是用来操作字符信息。

[打印流](#打印流)
-----------

下面这段代码大家经常使用吧？

```java
System.out.print("Hello！");
System.out.println("Hello！");
```

`System.out` 实际是用于获取一个 `PrintStream` 对象，`print`方法实际调用的是 `PrintStream` 对象的 `write` 方法。

`PrintStream` 属于字节打印流，与之对应的是 `PrintWriter` （字符打印流）。`PrintStream` 是 `OutputStream` 的子类，`PrintWriter` 是 `Writer` 的子类。

```java
public class PrintStream extends FilterOutputStream
    implements Appendable, Closeable {
}
public class PrintWriter extends Writer {
}
```

[随机访问流](#随机访问流)
---------------

这里要介绍的随机访问流指的是支持随意跳转到文件的任意位置进行读写的 `RandomAccessFile` 。

`RandomAccessFile` 的构造方法如下，我们可以指定 `mode`（读写模式）。

```java
// openAndDelete 参数默认为 false 表示打开文件并且这个文件不会被删除
public RandomAccessFile(File file, String mode)
    throws FileNotFoundException {
    this(file, mode, false);
}
// 私有方法
private RandomAccessFile(File file, String mode, boolean openAndDelete)  throws FileNotFoundException{
  // 省略大部分代码
}
```

读写模式主要有下面四种：

*   `r` : 只读模式。
*   `rw`: 读写模式
*   `rws`: 相对于 `rw`，`rws` 同步更新对 “文件的内容” 或“元数据”的修改到外部存储设备。
*   `rwd` : 相对于 `rw`，`rwd` 同步更新对 “文件的内容” 的修改到外部存储设备。

文件内容指的是文件中实际保存的数据，元数据则是用来描述文件属性比如文件的大小信息、创建和修改时间。

`RandomAccessFile` 中有一个文件指针用来表示下一个将要被写入或者读取的字节所处的位置。我们可以通过 `RandomAccessFile` 的 `seek(long pos)` 方法来设置文件指针的偏移量（距文件开头 `pos` 个字节处）。如果想要获取文件指针当前的位置的话，可以使用 `getFilePointer()` 方法。

`RandomAccessFile` 代码示例：

```java
RandomAccessFile randomAccessFile = new RandomAccessFile(new File("input.txt"), "rw");
System.out.println("读取之前的偏移量：" + randomAccessFile.getFilePointer() + ",当前读取到的字符" + (char) randomAccessFile.read() + "，读取之后的偏移量：" + randomAccessFile.getFilePointer());
// 指针当前偏移量为 6
randomAccessFile.seek(6);
System.out.println("读取之前的偏移量：" + randomAccessFile.getFilePointer() + ",当前读取到的字符" + (char) randomAccessFile.read() + "，读取之后的偏移量：" + randomAccessFile.getFilePointer());
// 从偏移量 7 的位置开始往后写入字节数据
randomAccessFile.write(new byte[]{'H', 'I', 'J', 'K'});
// 指针当前偏移量为 0，回到起始位置
randomAccessFile.seek(0);
System.out.println("读取之前的偏移量：" + randomAccessFile.getFilePointer() + ",当前读取到的字符" + (char) randomAccessFile.read() + "，读取之后的偏移量：" + randomAccessFile.getFilePointer());
```

`input.txt` 文件内容：

![](https://oss.javaguide.cn/github/javaguide/java/image-20220421162050158.png)

输出：

```java
读取之前的偏移量：0,当前读取到的字符A，读取之后的偏移量：1
读取之前的偏移量：6,当前读取到的字符G，读取之后的偏移量：7
读取之前的偏移量：0,当前读取到的字符A，读取之后的偏移量：1
```

`input.txt` 文件内容变为 `ABCDEFGHIJK` 。

`RandomAccessFile` 的 `write` 方法在写入对象的时候如果对应的位置已经有数据的话，会将其覆盖掉。

```java
RandomAccessFile randomAccessFile = new RandomAccessFile(new File("input.txt"), "rw");
randomAccessFile.write(new byte[]{'H', 'I', 'J', 'K'});
```

假设运行上面这段程序之前 `input.txt` 文件内容变为 `ABCD` ，运行之后则变为 `HIJK` 。

`RandomAccessFile` 比较常见的一个应用就是实现大文件的 **断点续传** 。何谓断点续传？简单来说就是上传文件中途暂停或失败（比如遇到网络问题）之后，不需要重新上传，只需要上传那些未成功上传的文件分片即可。分片（先将文件切分成多个文件分片）上传是断点续传的基础。

`RandomAccessFile` 可以帮助我们合并文件分片，示例代码如下：

![](https://oss.javaguide.cn/github/javaguide/java/io/20210609164749122.png)

我在[《Java 面试指北》](https://javaguide.cn/zhuanlan/java-mian-shi-zhi-bei.html)中详细介绍了大文件的上传问题。

![](https://oss.javaguide.cn/github/javaguide/java/image-20220428104115362.png)

`RandomAccessFile` 的实现依赖于 `FileDescriptor` (文件描述符) 和 `FileChannel` （内存映射文件）。



## IO模型

**从计算机结构的视角来看的话， I/O 描述了计算机系统与外部设备之间通信的过程。**

**我们再先从应用程序的角度来解读一下 I/O。**

根据大学里学到的操作系统相关的知识：为了保证操作系统的稳定性和安全性，一个进程的地址空间划分为 **用户空间（User space）** 和 **内核空间（Kernel space ）** 。

像我们平常运行的应用程序都是运行在用户空间，只有内核空间才能进行系统态级别的资源有关的操作，比如文件管理、进程通信、内存管理等等。也就是说，<span style="color:#FF0000;">我们想要进行 IO 操作，一定是要依赖内核空间的能力。</span>

并且，<span style="color:#FF0000;">用户空间的程序不能直接访问内核空间。</span>

当想要执行 IO 操作时，由于没有执行这些操作的权限，只<span style="color:#FF0000;">能发起系统调用请求操作系统帮忙完成。</span>

<span style="color:#7F00FF;">因此，用户进程想要执行 IO 操作的话，必须通过 **系统调用** 来间接访问内核空间</span>

我们在平常开发过程中接触最多的就是 <span style="color:#CC0066;">**磁盘 IO（读写文件）** 和 **网络 IO（网络请求和响应）**</span>。

**从应用程序的视角来看的话，我们的应用程序对操作系统的内核发起 IO 调用（系统调用），操作系统负责的内核执行具体的 IO 操作。也就是说，<span style="color:#0000FF;">我们的应用程序实际上只是发起了 IO 操作的调用而已，具体 IO 的执行是由操作系统的内核来完成的</span>。**

**当应用程序发起 I/O 调用后，会经历两个步骤：**

1. <span style="color:#0000CC;">**内核等待 I/O 设备准备好数据**</span>
2. **内核将数据从内核空间<span style="color:#0000FF;">拷贝</span>到用户空间**

---

UNIX 系统下， IO 模型一共有 5 种：**同步阻塞 I/O**、**同步非阻塞 I/O**、**I/O 多路复用**、**信号驱动 I/O** 和**异步 I/O**。它们在处理数据时采用不同的机制和方式

**有不同的效率和不同的性能问题 优缺点并存** 

这也是我们经常提到的 5 种 IO 模型

## Java 当中的IO模型

### ==BIO(Blocking I/O)==

**BIO 属于同步阻塞 IO 模型** 。

![image-20250510205444009](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510205444009.png)

### ==NIO(Non-blocking/New I/O)==

Java 中的 NIO 于 Java 1.4 中引入，对应 `java.nio` 包，提供了 `Channel` , `Selector`，`Buffer` 等抽象。NIO 中的 N 可以理解为 Non-blocking，不单纯是 New。它是支持面向缓冲的，基于通道的 I/O 操作方法。 对于高负载、高并发的（网络）应用，应使用 NIO 。

Java 中的 NIO 可以看作是 **I/O 多路复用模型**。也有很多人认为，Java 中的 NIO 属于同步非阻塞 IO 模型。





### ==AIO(Asynchronous I/O)==

**asynchronous 异步**

**synchronous 同步**



## ==IO 设计模式==





# 集合（结合Stream流 和 数据结构食用）

<mark style="background: #BBFABBA6;">Stream 解决的是批量数据的“声明式计算”，
 Optional 解决的是空指针的不确定性风险，
 函数式接口是“行为参数化”的核心能力。</mark>
没有终止操作，整个链条**不会执行** stream 流不能复用！！！
## 中间操作
| 方法           | 作用      | 面试关注点                        |
| ------------ | ------- | ---------------------------- |
| `filter()`   | 条件过滤    | 是否短路、执行时机                    |
| `map()`      | 元素转换    | 与 `flatMap` 区别               |
| `flatMap()`  | 拍平结构    | 一对多 / 多对一转换                  |
| `distinct()` | 去重      | 依赖 `equals()` + `hashCode()` |
| `sorted()`   | 排序      | 自然序 / 自定义 Comparator         |
| `limit()`    | 截断前 N 条 | 是否短路操作                       |
| `skip()`     | 跳过前 N 条 | 边界场景                         |
| `peek()`     | 中间调试    | 不建议用于业务逻辑                    |
遇到终止操作时，才触发计算。（懒加载）



## 结尾操作

| 方法            | 作用     | 面试关注点           |
| ------------- | ------ | --------------- |
| `forEach()`   | 遍历消费   | 并行流顺序问题         |
| `collect()`   | 收集结果   | `Collectors` 原理 |
| `count()`     | 数量统计   | 性能 vs size()    |
| `reduce()`    | 归约     | 并行安全性           |
| `findFirst()` | 取第一个   | 顺序流 vs 并行流      |
| `findAny()`   | 任意元素   | 并行流优化点          |
| `anyMatch()`  | 是否存在   | 短路行为            |
| `allMatch()`  | 是否全部   | 短路时机            |
| `noneMatch()` | 是否都不满足 | 逻辑反转点           |

## Optional

| 方法              | 作用            | 面试关注点        |
| --------------- | ------------- | ------------ |
| `of()`          | 包装非 null 值    | null 会直接 NPE |
| `ofNullable()`  | 可为空           | 推荐用法         |
| `isPresent()`   | 是否存在          | 不推荐直接用       |
| `ifPresent()`   | 存在则消费         | 更优雅          |
| `orElse()`      | 提供默认值         | 总是执行         |
| `orElseGet()`   | 延迟执行          | 性能优化点        |
| `orElseThrow()` | 抛异常           | 异常类型设计       |
| `map()`         | 值转换           | 链式安全         |
| `flatMap()`     | 防止嵌套 Optional | 常被问          |

## 函数式接口

| 接口              | 输入  | 输出      | 常见应用          |
| --------------- | --- | ------- | ------------- |
| `Function<T,R>` | T   | R       | `map()`       |
| `Consumer<T>`   | T   | 无       | `forEach()`   |
| `Predicate<T>`  | T   | boolean | `filter()`    |
| `Supplier<T>`   | 无   | T       | `orElseGet()` |

---

- ArrayList： 动态数组**，实现了List接口**，支持动态增长。
- LinkedList： **双向链表，也实现了List接口**，支持快速的插入和删除操作。



- HashMap： 基于哈希表的Map实现，存储键值对，通过键快速查找值。
- HashSet： 基于HashMap实现的Set集合，用于存储唯一元素。



- TreeMap： 基于**红黑树**实现的**有序Map集合**，可以按照**键的顺序**进行排序。
- LinkedHashMap： 基于**哈希表和双向链表**实现的Map集合，保持插入顺序或访问顺序。
- PriorityQueue： **优先队列**，可以按照比较器或元素的自然顺序进行排序。

---



![img](https://cdn.xiaolincoding.com//picgo/1717481094793-b8ffe6ae-2ee6-4de5-b61b-8468e32bf269.webp)

### 一、List 接口（有序集合）
- **特性**：允许元素重复，可通过索引精确控制插入位置和访问元素。
- **主要实现类**：
  - **ArrayList**：
    - 底层基于动态数组实现，非线程安全。
    - 支持快速随机访问（通过索引），但插入/删除元素时需移动数组元素，效率较低。
    - 容量不足时自动扩容（创建更大数组并复制原数据）。
  - **LinkedList**：
    - 底层基于双向链表实现，非线程安全。
    - 插入/删除元素时只需修改链表指针，效率较高，但随机访问需遍历链表，速度较慢。
  - **Vector**：
    - 线程安全的动态数组，内部方法多通过 `synchronized` 修饰。
    - 底层使用对象数组，支持自动扩容，性能因同步开销较低，非线程安全场景不推荐。
  - **Stack**：继承自 Vector，实现栈结构（先进后出），已逐步被 `Deque` 替代。


### 二、Set 接口（无序集合，元素唯一）
- **特性**：不允许重复元素，无索引，元素无序（部分实现类除外）。
- **主要实现类**：
  - **HashSet**：
    - 基于 HashMap 实现（元素作为 HashMap 的 Key，Value 为固定常量 `PRESENT`）。
    - 依赖 Key 的哈希值保证唯一性，不保证元素顺序，非线程安全。
  - **LinkedHashSet**：
    - 继承自 HashSet，底层基于 LinkedHashMap 实现。
    - 通过双向链表维护元素插入顺序，兼具哈希表的查询性能和顺序性。
  - **TreeSet**：
    - 基于 TreeMap 实现，元素需实现排序接口（`Comparable`）或通过比较器（`Comparator`）指定排序规则。
    - 插入元素时自动排序，保证集合有序性，非线程安全。


### 三、Map 接口（键值对集合）
- **特性**：存储键值对（Key-Value），Key 唯一且无序，Value 可重复，不继承 `Collection` 接口。
- **主要实现类**：
  - **HashMap**：
    - JDK 1.8 前：数组 + 链表（拉链法解决哈希冲突）。
    - JDK 1.8 后：当链表长度超过阈值（默认 8）时，转为红黑树，优化查询性能。
    - 非线程安全，允许 Key/Value 为 null。
  - **LinkedHashMap**：
    - 继承自 HashMap，底层同 HashMap（数组 + 链表/红黑树）。
    - 额外通过双向链表维护键值对的插入顺序或访问顺序，支持顺序遍历。
  - **Hashtable**：
    - 底层为数组 + 链表，线程安全（方法加 `synchronized` 锁，锁整个对象）。
    - 不允许 Key/Value 为 null，因性能开销大，已被 ConcurrentHashMap 替代。
  - **TreeMap**：
    - 底层基于红黑树（自平衡排序二叉树），Key 需支持排序（同 TreeSet）。
    - 可按 Key 自然顺序或指定比较器排序，非线程安全。
  - **ConcurrentHashMap**：
    - 线程安全的 HashMap 变体，JDK 1.7 用分段锁（Segment），JDK 1.8 改用 `volatile + CAS + synchronized`（锁数组元素），减小锁粒度。
    - 支持高并发读写，性能优于 Hashtable。


### 四、Java 线程安全集合
#### 1. java.util 包中的线程安全类
- **Vector**：线程安全的动态数组（方法加 `synchronized`），性能较低。
- **Hashtable**：线程安全的哈希表（方法加 `synchronized`），不支持 null，性能较差。


#### 2. java.util.concurrent 包中的线程安全集合
- **并发 Map**：
  - **ConcurrentHashMap**：高并发哈希表，锁粒度更细（JDK 1.8 锁数组元素），支持高效并发读写。
  - **ConcurrentSkipListMap**：基于跳表实现的有序 Map，支持并发操作，查询/插入/删除效率为 O(log n)。
- **并发 Set**：
  - **ConcurrentSkipListSet**：基于 ConcurrentSkipListMap 实现的有序 Set，线程安全。
  - **CopyOnWriteArraySet**：基于 CopyOnWriteArrayList 实现的无序 Set，写操作时复制底层数组，读操作无锁，适合读多写少场景。
- **并发 List**：
  - **CopyOnWriteArrayList**：ArrayList 的线程安全变体，写操作（add/set 等）复制底层数组，读操作无阻塞，适合读多写少场景。
- **并发 Queue**：
  - **ConcurrentLinkedQueue**：无锁（CAS）实现的高并发队列，性能优于 BlockingQueue。
  - **BlockingQueue**：支持读写阻塞的队列（如队列空时读阻塞，队列满时写阻塞），简化多线程数据共享。
- **并发 Deque**：
  - **LinkedBlockingDeque**：线程安全的双端队列，基于链表，同一时间仅允许一个线程操作。
  - **ConcurrentLinkedDeque**：无锁实现的无限双端链表，支持高并发插入、删除和访问。



---



`List`(对付顺序的好帮手): 存储的元素是有序的、可重复的。

`Set`(注重独一无二的性质): 存储的元素不可重复的。

`Queue`(实现排队功能的叫号机): 按特定的排队规则来确定先后顺序，存储的元素是有序的、可重复的。

`Map`(用 key 来搜索的专家): 使用键值对（key-value）存储，类似于数学上的函数 y=f(x)，"x" 代表 key，"y" 代表 value，**key 是无序的、不可重复的**，**value 是无序的、可重复的，每个键最多映射到一个值（也就是一个输入只能对应一个输出 函数本质）**



------

**collection 接口** 

list（linkedlist arraylist  vector） queue （priorityqueue  **dequeue**））set（hashset treeset）  

**map接口** 

 hashmap **treemap（sortedmap）**  **hashtable**

有tree的：**元素按照  <span style="color:#FF0000;">自然顺序 </span> 或者指定的  <span style="color:#FF0000;">比较器顺序 </span> 进行排序存储。**

---

![image-20250510210403119](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510210403119.png)





## List

![image-20250927132751480](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927132751480.png)





![image-20250518110040214](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518110040214.png)



**这些集合只能使用 包装类 使用不·了基本数据类型！！！**



`ArrayList` 内部基于**动态数组**实现，比 `Array`（静态数组） 使用起来更加灵活：

- `ArrayList`会根据实际存储的元素**动态地扩容或缩容**，而 `Array` 被创建之后就不能改变它的长度了。
- `ArrayList` 允许你**使用泛型**来确保**类型安全**，`Array` 则不可以。
- `ArrayList` 中只能存储对象。对于基本类型数据，需要使用其对应的包装类（如 Integer、Double 等）。`Array` 可以直接存储基本类型数据，也可以存储对象。
- `ArrayList` 支持插入、删除、遍历等常见操作，并且提供了丰富的 API 操作方法，比如 `add()`、`remove()`等。`Array` 只是一个固定长度的数组，只能按照下标访问其中的元素，不具备动态添加、删除元素的能力。
- `ArrayList`创建时不需要指定大小，而`Array`创建时必须指定大小



![image-20250510222323159](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510222323159.png)

<span style="color:#CC0000;">**并发集合类：ConcurrentHashMap、 CopyWriteArrayList（写操作的时候复制一份数组然后写）**</span>

**size++ 非原子操作** （注意看一些操作是不是原子性操作！！！）

`size++` 实际是三个步骤：**读取值 → 加1 → 写回值**。多线程环境下：

- 两个线程可能读取到相同的 `size` 值，各自加1后写回，导致最终 `size` 比实际少1。

![image-20250510222519779](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510222519779.png)



![image-20250510222527424](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510222527424.png)



![image-20250510222533579](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510222533579.png)

### ArrayList线程安全吗？  
**ArrayList不是线程安全的**。因为它的底层操作（比如add、remove、get）没有加锁或同步机制，多线程同时读写时，容易出现数据错乱（比如元素丢失、数组越界）或并发修改异常（ConcurrentModificationException）。


### 把ArrayList变成线程安全的方法：  
1. **用Collections.synchronizedList包装**  
   通过`Collections`工具类的`synchronizedList`方法，给ArrayList套一层“同步锁外衣”，所有操作都会通过同步代码块保证线程安全：  
   ```java
   List<String> arrayList = new ArrayList<>();
   List<String> synchronizedList = Collections.synchronizedList(arrayList);
   ```

2. **用CopyOnWriteArrayList替代**  
   `CopyOnWriteArrayList`是Java并发包（java.util.concurrent）里的实现，原理是“写时复制”——写操作（add/remove）会复制一份新数组，读操作直接读原数组，读写分离避免冲突，适合读多写少的场景：  
   ```java
   CopyOnWriteArrayList<String> copyOnWriteList = new CopyOnWriteArrayList<>(arrayList);
   ```

3. **用Vector替代**  
   Vector是ArrayList的“老大哥”，底层方法（比如addElement、get）都加了`synchronized`关键字，天然线程安全，但因为是方法级锁，并发效率较低：  
   ```java
   Vector<String> vector = new Vector<>(arrayList);
   ```





### ==ArrayList的扩容机制==

`ArrayList` 的底层是数组队列，相当于动态数组。与 Java 中的数组相比，它的容量能动态增长。在添加大量元素前，应用程序可以使用`ensureCapacity`操作来增加 `ArrayList` 实例的容量。这可以减少递增式再分配的数量。

`ArrayList` 继承于 `AbstractList` ，实现了 `List`, `RandomAccess`, `Cloneable`, `java.io.Serializable` 这些接口。



```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable{

  }
```

- `List` : 表明它是一个列表，支持添加、删除、查找等操作，并且可以通过下标进行访问。
- `RandomAccess` ：这是一个标志接口，表明实现这个接口的 `List` 集合是支持 **快速随机访问** 的。在 `ArrayList` 中，我们即可以通过元素的序号快速获取元素对象，这就是快速随机访问。
- `Cloneable` ：**表明它具有拷贝能力，可以进行深拷贝或浅拷贝操作。**
- `Serializable` : 表明它可以进行序列化操作，也就是可以将对象转换为字节流进行持久化存储或网络传输，非常方便。

~~~css
ArrayList在添加元素时，如果当前元素个数已经达到了内部数组的容量上限，就会触发扩容操作。ArrayList的扩容操作主要包括以下几个步骤：

计算新的容量：一般情况下，新的容量会扩大为原容量的1.5倍（在JDK 10之后，扩容策略做了调整），然后检查是否超过了最大容量限制。
创建新的数组：根据计算得到的新容量，创建一个新的更大的数组。
将元素复制：将原来数组中的元素逐个复制到新数组中。
更新引用：将ArrayList内部指向原数组的引用指向新数组。
完成扩容：扩容完成后，可以继续添加新元素。
ArrayList的扩容操作涉及到数组的复制和内存的重新分配，所以在频繁添加大量元素时，扩容操作可能会影响性能。为了减少扩容带来的性能损耗，可以在初始化ArrayList时预分配足够大的容量，避免频繁触发扩容操作。
~~~

**线程安全的 List， CopyonWriteArraylist是如何实现线程安全的**

也是类似的

看到源码可以知道写入新元素时，首先会先将原来的数组拷贝一份并且让原来数组的长度+1后就得到了一个新数组，新数组里的元素和旧数组的元素一样并且长度比旧数组多一个长度，然后将新加入的元素放置都在新数组最后一个位置后，用新数组的地址替换掉老数组的地址就能得到最新的数据了。

在我们执行替换地址操作之前，读取的是老数组的数据，数据是有效数据；执行替换地址操作之后，读取的是新数组的数据，同样也是有效数据，而且使用该方式能比读写都加锁要更加的效率。

现在我们来看读操作，读是没有加锁的，所以读是一直都能读

~~~java
public boolean add(E e) {
    //获取锁
    final ReentrantLock lock = this.lock;
    //加锁
    lock.lock();
    try {
        //获取到当前List集合保存数据的数组
        Object[] elements = getArray();
        //获取该数组的长度（这是一个伏笔，同时len也是新数组的最后一个元素的索引值）
        int len = elements.length;
        //将当前数组拷贝一份的同时，让其长度加1
        Object[] newElements = Arrays.copyOf(elements, len + 1);
        //将加入的元素放在新数组最后一位，len不是旧数组长度吗，为什么现在用它当成新数组的最后一个元素的下标？建议自行画图推演，就很容易理解。
        newElements[len] = e;
        //替换引用，将数组的引用指向给新数组的地址
        setArray(newElements);
        return true;
    } finally {
        //释放锁
        lock.unlock();
    }
}
~~~

Java 的泛型机制在设计时就只支持引用类型，不支持基本数据类型。

**这么设计的原因是：**

**泛型的类型擦除机制：**Java 泛型在编译后会被**擦除为 Object 类型**，而 Object 只能接收引用类型，不能接收基本数据类型。

通过使用包装类，结合 Java 的**自动装箱（基本类型 → 包装类）和自动拆箱（包装类 → 基本类型）机制，**可以很方便地在泛型集合中操作基本数据类型的数据。

#Map

![ArrayList 类图](https://oss.javaguide.cn/github/javaguide/java/collection/arraylist-class-diagram.png)

### ArrayList 源码分析

![image-20250518102630498](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518102630498.png)





![image-20250518102642341](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518102642341.png)

**1. 将集合转换为数组**

```java
Object[] a = c.toArray();
```

- 无论传入的集合类型如**何，先调用其 `toArray()` 方法转换为 `Object[]` 数组。**
- **潜在问题**：不同集合的 `toArray()` 实现可能返回不同类型的数组（如 `String[]`），后续需处理类型兼容性。

**2. 检查数组是否为空**



```java
if ((size = a.length) != 0) {
    // 处理非空数组
} else {
    elementData = EMPTY_ELEMENTDATA; // 共享空数组实例
}
```

- **空数组优化**：若集合为空，**直接使用预定义的空数组 `EMPTY_ELEMENTDATA`，**避免重复创建空数组，节省内存。

**3. 处理非空数组时的类型判断**

```java
if (c.getClass() == ArrayList.class) {
    elementData = a; // 直接引用原数组
} else {
    elementData = Arrays.copyOf(a, size, Object[].class); // 复制数组
}
```

**为什么需要判断 `c.getClass() == ArrayList.class`？**

- **性能优化**：
  如果传入的集合是 `ArrayList` 实例，其内部数组已经是 `Object[]` 类型，可以直接赋值给 `elementData`，**避免复制数组的开销**。
- **类型安全**：
  若集合不是 `ArrayList`（如 `LinkedList`、`HashSet` 等），其 `toArray()` 返回的数组可能是其他类型（如 `String[]`）。直接赋值会导致 `elementData` 类型不匹配（应为 `Object[]`），可能引发 `ArrayStoreException`。
  通过 `Arrays.copyOf(a, size, Object[].class)` 强制复制为 `Object[]` 类型数组，确保类型一致。

**为什么用 `c.getClass() == ArrayList.class` 而非 `instanceof`？**

`instanceof` 是 **运行时的类型检查工具**，帮助确认对象是不是某个类（或其子类、接口的实现类）的实例



- **精确匹配**：
  `c.getClass() == ArrayList.class` **严格判断集合是 `ArrayList` 类型本身，而非其子类。**
  若子类重写了 `toArray()` 方法，返回的数组类型可能与 `ArrayList` 不同，直接引用会导致类型问题。

**4. 空数组的特殊处理**

```java
elementData = EMPTY_ELEMENTDATA;
```

- **内存优化**：
  `EMPTY_ELEMENTDATA` 是 `ArrayList` 内部预定义的空数组实例。所有空 `ArrayList` 共享此实例，避免频繁创建空数组，减少内存占用。



---



![image-20250518104716280](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518104716280.png)

**数组不会扩容这个情况下:**





![image-20250518105616158](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518105616158.png)

**重点：**

![image-20250518105759249](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518105759249.png)

**Arrays.copyOf(original, newLength)**

创建一个新的数组，把原数组的内容复制进去

### ArrayList 底层的实现原理





![image-20250518105855900](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518105855900.png)

### ArrayList 时如何实现 数组和List 之间的转化的

**本质就是 是拷贝 还是 引用 的操作了**



![image-20250927143123483](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927143123483.png)

![image-20250927143540561](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927143540561.png)

![image-20250927143548896](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927143548896.png)

----



## Set

如果你将对象存储在 `Set` 中（例如 `HashSet` 或 `LinkedHashSet`），**则确实需要重写对象的 `equals()` 和 `hashCode()` 方法。这两个方法是用来确保集合中不存储重复的元素的关键。**



**`Comparable` 接口和 `Comparator` 接口**都是 Java 中用于排序的接口，它们在实现类对象之间比较大小、排序等方面发挥了重要作用：

- `Comparable` 接口实际上是出自`java.lang`包 它有一个 `compareTo(Object obj)`方法用来排序  **A.compareTo(B)**   一个对象可比较
- `Comparator`接口实际上是出自 `java.util` 包它有一个`compare(Object obj1, Object obj2)`方法用来排序   **compare(A,B)**   **比较器 独立于任何比较元素的就是个工具！！！**

一般我们需要对一个集合使用自定义排序时，我们就要重写`compareTo()`方法或`compare()`方法，当我们需要对某一个集合实现两种排序方式，比如一个 `song` 对象中的歌名和歌手名分别采用一种排序方法的话，我们可以重写`compareTo()`方法和使用自制的`Comparator`方法或者以两个 `Comparator` 来实现歌名排序和歌星名排序，第二种代表我们只能使用两个参数版的 `Collections.sort()`.



```java
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o1.compareTo(o2); // 升序
        return o2.compareTo(o1); // 降序
        // sum o1 o2 表示序列中 按顺序的俩个对象 只要返回是负数 就表示 o1 在前
    }
});
```

- **逻辑**：
  - 若 `o2 < o1`，`o2.compareTo(o1)` 返回 `-1` → 但实际返回值是 `-1`，（因为 `compare()` 的规则是负数表示 `o1` 在前，但这里 `o1` 实际上是更大的数）。
- **结果**：列表按 **从大到小** 排列（降序）。

---

### Comparator定制排序

~~~java
ArrayList<Integer> arrayList = new ArrayList<Integer>();
arrayList.add(-1);
arrayList.add(3);
arrayList.add(3);
arrayList.add(-5);
arrayList.add(7);
arrayList.add(4);
arrayList.add(-9);
arrayList.add(-7);
System.out.println("原始数组:");
System.out.println(arrayList);
// void reverse(List list)：反转
Collections.reverse(arrayList);
System.out.println("Collections.reverse(arrayList):");
System.out.println(arrayList);

// void sort(List list),按自然排序的升序排序
Collections.sort(arrayList);
System.out.println("Collections.sort(arrayList):");
System.out.println(arrayList);
// 定制排序的用法
Collections.sort(arrayList, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o2.compareTo(o1);
    }
});
System.out.println("定制排序后：");
System.out.println(arrayList);


原始数组:
[-1, 3, 3, -5, 7, 4, -9, -7]
Collections.reverse(arrayList):
[-7, -9, 4, 7, -5, 3, 3, -1]
Collections.sort(arrayList):
[-9, -7, -5, -1, 3, 3, 4, 7]
定制排序后：
[7, 4, 3, 3, -1, -5, -7, -9]

~~~



### 重写compareTo 方法实现按年龄来排序

~~~java
// person对象没有实现Comparable接口，所以必须实现，这样才不会出错，才可以使treemap中的数据按顺序排列
// 前面一个例子的String类已经默认实现了Comparable接口，详细可以查看String类的API文档，另外其他
// 像Integer类等都已经实现了Comparable接口，所以不需要另外实现了
public  class Person implements Comparable<Person> {
    private String name;
    private int age;

    public Person(String name, int age) {
        super();
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    /**
     * T重写compareTo方法实现按年龄来排序
     */
    @Override
    public int compareTo(Person o) {
        if (this.age > o.getAge()) {
            return 1;
        }
        if (this.age < o.getAge()) {
            return -1;
        }
        return 0;
    }
}

    public static void main(String[] args) {
        TreeMap<Person, String> pdata = new TreeMap<Person, String>();
        pdata.put(new Person("张三", 30), "zhangsan");
        pdata.put(new Person("李四", 20), "lisi");
        pdata.put(new Person("王五", 10), "wangwu");
        pdata.put(new Person("小红", 5), "xiaohong");
        // 得到key的值的同时得到key所对应的值
        Set<Person> keys = pdata.keySet();
        for (Person key : keys) {
            System.out.println(key.getAge() + "-" + key.getName());

        }
    }


5-小红
10-王五
20-李四
30-张三
~~~



---



### [无序性和不可重复性的含义是什么](#无序性和不可重复性的含义是什么)

- <span style="color:#FF0000;">无序性**不等于随机性** ，无序性是指存储的数据在**底层数组中并非按照数组索引的顺序添加** ，而是根据**数据的哈希值**决定的。</span>
- 不可重复性是指添加的元素按照 `equals()` 判断时 ，返回 false，**<span style="color:#FF0000;">！！！需要同时重写 `equals()` 方法和 `hashCode()` 方法。</span>**

### [比较 HashSet、LinkedHashSet 和 TreeSet 三者的异同](#比较-hashset、linkedhashset-和-treeset-三者的异同)

- `HashSet`、`LinkedHashSet` 和 `TreeSet` 都是 `Set` 接口的实现类，都能保证元素唯一，并且都不是线程安全的。
- `HashSet`、`LinkedHashSet` 和 `TreeSet` 的主要区别在于底层数据结构不同。`HashSet` 的底层数据结构是哈希表（基于 `HashMap` 实现）。`LinkedHashSet` 的底层数据结构是链表和哈希表，元素的插入和取出顺序满足 FIFO。`TreeSet` 底层数据结构是红黑树，元素是有序的，排序的方式有自然排序和定制排序。
- 底层数据结构不同又导致这三者的应用场景不同。**`HashSet` 用于不需要保证元素插入和取出顺序的场景，`LinkedHashSet` 用于保证元素的插入和取出顺序满足 FIFO 的场景，`TreeSet` 用于支持对元素自定义排序规则的场景。**



## Queue

### [Queue 与 Deque 的区别](#queue-与-deque-的区别)

`Queue` 是单端队列，只能从一端插入元素，另一端删除元素，实现上一般遵循 **先进先出（FIFO）** 规则。

`Queue` 扩展了 `Collection` 的接口，根据 **因为容量问题而导致操作失败后处理方式的不同** 可以分为两类方法: **一种在操作失败后会抛出异常，另一种则会返回特殊值。**



add - offer

remover - poll



| `Queue` 接口 | 抛出异常  | 返回特殊值 |
| ------------ | --------- | ---------- |
| 插入队尾     | add(E e)  | offer(E e) |
| 删除队首     | remove()  | poll()     |
| 查询队首元素 | element() | peek()     |

`Deque` 是双端队列，在队列的**两端均可以插入或删除元素。**

`Deque` 扩展了 `Queue` 的接口, 增加了在队首和队尾进行插入和删除的方法，同样根据失败后处理方式的不同分为两类：

| `Deque` 接口 | 抛出异常      | 返回特殊值      |
| ------------ | ------------- | --------------- |
| 插入队首     | addFirst(E e) | offerFirst(E e) |
| 插入队尾     | addLast(E e)  | offerLast(E e)  |
| 删除队首     | removeFirst() | pollFirst()     |
| 删除队尾     | removeLast()  | pollLast()      |
| 查询队首元素 | getFirst()    | peekFirst()     |
| 查询队尾元素 | getLast()     | peekLast()      |

**事实上，`Deque` 还提供有 `push()` 和 `pop()` 等其他方法，可用于模拟栈**

---



### [ArrayDeque 与 LinkedList 的区别](#arraydeque-与-linkedlist-的区别)

`ArrayDeque` 和 `LinkedList` 都实现了 `Deque` 接口，两者都具有队列的功能，但两者有什么区别呢？

- `ArrayDeque` 是基于**可变长的数组和双指针来实现，而 `LinkedList` 则通过链表来实现。**
- `ArrayDeque` 不支持存储 `NULL` 数据，但 `LinkedList` 支持。
- `ArrayDeque` 是在 JDK1.6 才被引入的，而`LinkedList` 早在 JDK1.2 时就已经存在。
- `ArrayDeque` 插入时可能存在扩容过程, 不过均摊后的插入操作依然为 O(1)。虽然 `LinkedList` 不需要扩容，但是每次插入数据时均需要申请新的堆空间，均摊性能相比更慢。

从性能的角度上，选用 `ArrayDeque` 来实现队列要比 `LinkedList` 更好。此外，**`ArrayDeque` 也可以用于实现栈。**



### [说一说 PriorityQueue](#说一说-priorityqueue)

`PriorityQueue` 是在 JDK1.5 中被引入的, 其与 `Queue` 的区别在于元素**出队顺序是与优先级相关的，即总是优先级最高的元素先出队。**

这里列举其相关的一些要点：

- `PriorityQueue` 利用了**二叉堆**的数据结构来实现的，底层使用**可变长的数组**来存储数据
- `PriorityQueue` 通过堆元素的上浮和下沉，实现了在 O(logn) 的时间复杂度内插入元素和删除堆顶元素。
- `PriorityQueue` 是**非线程安全**的，且**不支持存储 `NULL` 和 `non-comparable` 的对象。**
- `PriorityQueue` 默认是**小顶堆**，但可以**接收一个 `Comparator` 作为构造参数，从而来自定义元素优先级的先后。**

`PriorityQueue` 在面试中可能更多的会出现在手撕算法的时候，典型例题包括堆排序、求第 K 大的数、带权图的遍历等，所以需要会熟练使用才行

---



**阻塞队列和线程池相关！！！**

![image-20250510231138206](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250510231138206.png)

**<span style="color:#CC0000;">根据底层实现 思考差别</span>**

### [ArrayBlockingQueue 和 LinkedBlockingQueue 有什么区别？](#arrayblockingqueue-和-linkedblockingqueue-有什么区别)

`ArrayBlockingQueue` 和 `LinkedBlockingQueue` 是 Java 并发包中常用的两种阻塞队列实现，它们都是线程安全的。不过，不过它们之间也存在下面这些区别：

- 底层实现：`ArrayBlockingQueue` 基于数组实现，而 `LinkedBlockingQueue` 基于链表实现。
- 是否有界：`ArrayBlockingQueue` 是有界队列，必须在创建时指定容量大小。`LinkedBlockingQueue` 创建时可以不指定容量大小，默认是`Integer.MAX_VALUE`，也就是无界的。但也可以指定队列大小，从而成为有界的。
- 锁是否分离： `ArrayBlockingQueue`中的锁是没有分离的，即生产和消费用的是同一个锁；`LinkedBlockingQueue`中的锁是分离的，即生产用的是`putLock`，消费是`takeLock`，这样可以防止生产者和消费者线程之间的锁争夺。
- 内存占用：`ArrayBlockingQueue` 需要提前分配数组内存，而 `LinkedBlockingQueue` 则是动态分配链表节点内存。这意味着，`ArrayBlockingQueue` 在创建时就会占用一定的内存空间，且往往申请的内存比实际所用的内存更大，而`LinkedBlockingQueue` 则是根据元素的增加而逐渐占用内存空间

## ==Map== (重要！！！)

### 一、非线程安全的 Map 集合
#### 1. HashMap
- **底层实现**：JDK 1.8 及以后基于「数组 + 链表 + 红黑树」实现（哈希表结构），通过键的哈希值存储和获取键值对。
- **线程安全问题**：多线程并发操作时，可能出现数据不一致或死循环：
  - 扩容时多个线程同时修改哈希表结构，可能导致链表成环或数据丢失；
  - 读写操作无同步机制，易出现脏读、覆盖等问题。


#### 2. LinkedHashMap
- **底层实现**：继承自 HashMap，在其基础上通过**双向链表**维护键值对的「插入顺序」或「访问顺序」，迭代时按顺序返回元素。
- **线程安全问题**：因继承自 HashMap，未额外添加同步机制，多线程并发操作时会出现与 HashMap 相同的线程安全问题（如数据错乱）。


#### 3. TreeMap
- **底层实现**：基于**红黑树**（自平衡排序二叉树）实现，可通过键的自然顺序或自定义比较器排序。
- **线程安全问题**：非线程安全，多线程并发插入、删除时可能破坏红黑树结构（如平衡机制失效），导致数据不一致或程序异常。


### 二、线程安全的 Map 集合
#### 1. Hashtable
- **底层实现**：基于「数组 + 链表」的哈希表结构，与早期 HashMap 实现类似。
- **线程安全机制**：通过在所有修改方法（如 `put`、`remove`）上添加 `synchronized` 关键字，保证同一时刻只有一个线程能访问方法，从而实现线程安全。
- **缺点**：锁粒度粗（锁整个对象），高并发下性能较低，且不支持 `null` 键和值，已逐渐被 ConcurrentHashMap 替代。


#### 2. ConcurrentHashMap
- **底层实现**：JDK 1.8 前基于「分段锁（Segment）」，1.8 及以后改为**「数组 + 链表 + 红黑树」+ 精细化锁机制。**
- **线程安全机制**：
  - JDK 1.7：将数据分为多个 Segment（每个 Segment 是一个小哈希表），操作时仅锁定对应 Segment，支持多线程同时访问不同 Segment，提高并发效率；
  - JDK 1.8：取消 Segment，通过 `volatile` 保证数组可见性，结合 CAS 操作（无锁）和 `synchronized` 锁定链表/红黑树的头节点，进一步减小锁粒度，性能更优。
- **优势**：高并发场景下效率远高于 Hashtable，支持并发读写，是线程安全 Map 的首选。



~~~css
了解的哈希冲突解决方法有哪些？
链接法：使用链表或其他数据结构来存储冲突的键值对，将它们链接在同一个哈希桶中。
开放寻址法：在哈希表中找到另一个可用的位置来存储冲突的键值对，而不是存储在链表中。常见的开放寻址方法包括线性探测、二次探测和双重散列。
再哈希法（Rehashing）：当发生冲突时，使用另一个哈希函数再次计算键的哈希值，直到找到一个空槽来存储键值对。
哈希桶扩容：当哈希冲突过多时，可以动态地扩大哈希桶的数量，重新分配键值对，以减少冲突的概率。
~~~



### HashMap 和 Hashtable 的区别

**线程是否安全：** <span style="color:#FF0000;">HashMap 是非线程安全的，Hashtable 是线程安全的</span>,因为 **Hashtable 内部的方法基本都经过synchronized （Mutex机制 操作系统内核）修饰**。（如果你要保证线程安全的话就使用 **ConcurrentHashMap** 吧！）；
**效率：** **因为线程安全的问题，HashMap 要比 Hashtable 效率高一点**。另外，Hashtable 基本被淘汰，不要在代码中使用它；
**对 Null key 和 Null value 的支持：** **HashMap 可以存储 null 的 key 和 value，但 null 作为键只能有一个，null 作为值可以有多个；Hashtable 不允许有 null 键和 null 值，否则会抛出 NullPointerException。**



**初始容量大小和每次扩充容量大小的不同：** ① 创建时如果不指定容量初始值，Hashtable 默认的初始大小为 11，之后每次扩充，容量变为原来的 2n+1。<span style="color:#CC0000;">**HashMap 默认的初始化大小为 16。之后每次扩充，容量变为原来的 2 倍。**</span>② 创建时如果<span style="color:#CC0000;">**给定了容量初始值，那么 Hashtable 会直接使用你给定的大小，而 HashMap 会将其扩充为 2 的幂次方大小**</span>（HashMap 中的tableSizeFor()方法保证，下面给出了源代码）。<span style="color:#0000FF;">也就是说 HashMap 总是使用 2 的幂作为哈希表的大小,后面会介绍到为什么是 2 的幂次方。</span>
**底层数据结构：** JDK1.8 以后的 HashMap 在解决哈希冲突时有了较大的变化，当<span style="color:#FF0000;">链表长度大于阈值（默认为 8）</span>时，<span style="color:#FF0000;">将链表转化为红黑树（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树）</span>，<span style="color:#0000CC;">以减少搜索时间</span>（后文中我会结合源码对这一过程进行分析）。Hashtable 没有这样的机制。
**哈希函数的实现：**<span style="color:#0000CC;">HashMap 对哈希值进行了高位和低位的混合扰动处理以减少冲突，而 Hashtable 直接使用键的 hashCode() 值。</span>



### [HashMap 和 HashSet 区别](#hashmap-和-hashset-区别)

如果你看过 `HashSet` 源码的话就应该知道：<span style="color:#0000CC;">`HashSet` 底层就是基于 `HashMap` 实现的。</span>（`HashSet` 的源码非常非常少，因为除了 `clone()`、`writeObject()`、`readObject()`是 `HashSet` 自己不得不实现之外，其他方法都是直接调用 `HashMap` 中的方法。

|               `HashMap`                |                          `HashSet`                           |
| :------------------------------------: | :----------------------------------------------------------: |
|           实现了 `Map` 接口            |                       实现 `Set` 接口                        |
|               存储键值对               |                          仅存储对象                          |
|     调用 `put()`向 map 中添加元素      |             调用 `add()`方法向 `Set` 中添加元素              |
| `HashMap` 使用键（Key）计算 `hashcode` | `HashSet` 使用成员对象来计算 `hashcode` 值，对于两个对象来说 `hashcode` 可能相同，所以`equals()`方法用来判断对象的相等性 |

------

![image-20250511100213741](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511100213741.png)

`TreeMap` 的底层数据结构是红黑树（Red-Black Tree）。**红黑树是一种自平衡的二叉查找树，它保持着良好的平衡，确保了在最坏情况下的时间复杂度为 O(log n) 的性能。**





~~~java
/**
 * @author shuang.kou
 * @createTime 2020年06月15日 17:02:00
 */
public class Person {
    private Integer age;

    public Person(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }


    public static void main(String[] args) {
        TreeMap<Person, String> treeMap = new TreeMap<>(new Comparator<Person>() {
            @Override
            public int compare(Person person1, Person person2) {
                int num = person1.getAge() - person2.getAge();
                return Integer.compare(num, 0);
            }
        });
        treeMap.put(new Person(3), "person1");
        treeMap.put(new Person(18), "person2");
        treeMap.put(new Person(35), "person3");
        treeMap.put(new Person(16), "person4");
        treeMap.entrySet().stream().forEach(personStringEntry -> {
            System.out.println(personStringEntry.getValue());
        });
    }
}

// 上面，我们是通过传入匿名内部类的方式实现的，你可以将代码替换成 Lambda 表达式实现的方式：
TreeMap<Person, String> treeMap = new TreeMap<>((person1, person2) -> {
  int num = person1.getAge() - person2.getAge();
  return Integer.compare(num, 0);
});
~~~

![img](https://cdn.xiaolincoding.com//picgo/1720684054342-1e3cb2a9-532e-40b8-b5cf-0043811391dc.png)

![image-20251203235329712](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251203235329712.png)

![image-20251204001017200](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20251204001017200.png)

![image-20250511100940263](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511100940263.png)



#### [JDK1.8 之后](#jdk1-8-之后)

相比于之前的版本， JDK1.8 之后在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为 8）（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树）时，将链表转化为红黑树。

这样做的目的是减少搜索时间：链表的查询效率为 O(n)（n 是链表的长度），红黑树是一种自平衡二叉搜索树，其查询效率为 O(log n)。当链表较短时，O(n) 和 O(log n) 的性能差异不明显。但当链表变长时，查询性能会显著下降。

![jdk1.8之后的内部结构-HashMap](https://oss.javaguide.cn/github/javaguide/java/collection/jdk1.8_hashmap.png)

**为什么优先扩容而非直接转为红黑树？**

**<span style="color:#FF0000;">数组扩容能减少哈希冲突的发生概率（即将元素重新分散到新的、更大的数组中），这在多数情况下比直接转换为红黑树更高效</span>。**

**<span style="color:#FF0000;">红黑树需要保持自平衡，维护成本较高。</span>并且，过早引入红黑树反而会增加复杂度。**

**为什么选择阈值 8 和 64？**

1. 泊松分布表明，链表长度达到 8 的概率极低（小于千万分之一）。在绝大多数情况下，链表长度都不会超过 8。阈值设置为 8，可以保证性能和空间效率的平衡。
2. 数组长度阈值 64 同样是经过实践验证的经验值。在小数组中扩容成本低，优先扩容可以避免过早引入红黑树。数组大小达到 64 时，冲突概率较高，此时红黑树的性能优势开始显现。

> TreeMap、TreeSet 以及 JDK1.8 之后的 HashMap 底层都用到了红黑树。红黑树就是为了解决二叉查找树的缺陷，因为二叉查找树在某些情况下会退化成一个线性结构。

我们来**结合源码**分析一下 `HashMap` 链表到红黑树的转换。

#### ==源码分析==

**1、 `putVal` 方法中执行链表转红黑树的判断逻辑。**

~~~java
// 遍历链表
for (int binCount = 0; ; ++binCount) {
    // 遍历到链表最后一个节点
    if ((e = p.next) == null) {
        p.next = newNode(hash, key, value, null);
        // 如果链表元素个数大于TREEIFY_THRESHOLD（8）
        if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
            // 红黑树转换（并不会直接转换成红黑树）
            treeifyBin(tab, hash);
        break;
    }
    if (e.hash == hash &&
        ((k = e.key) == key || (key != null && key.equals(k))))
        break;
    p = e;
}
~~~







**2、`treeifyBin` 方法中判断是否真的转换为红黑树。**

~~~java
final void treeifyBin(Node<K,V>[] tab, int hash) {
    int n, index; Node<K,V> e;
    // 判断当前数组的长度是否小于 64
    if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
        // 如果当前数组的长度小于 64，那么会选择先进行数组扩容
        resize();
    else if ((e = tab[index = (n - 1) & hash]) != null) {
        // 否则才将列表转换为红黑树

        TreeNode<K,V> hd = null, tl = null;
        do {
            TreeNode<K,V> p = replacementTreeNode(e, null);
            if (tl == null)
                hd = p;
            else {
                p.prev = tl;
                tl.next = p;
            }
            tl = p;
        } while ((e = e.next) != null);
        if ((tab[index] = hd) != null)
            hd.treeify(tab);
    }
}
~~~



将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树

---

### HashMap的实现原理

数组  + 链表/红黑树

 ![image-20250511102531003](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511102531003.png)



![image-20250927144425588](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927144425588.png)



 当 HashMap 扩容（`resize()`）之后，哈希分布会更稀疏，红黑树里的一部分节点可能被分散开了。

- 如果某个桶的红黑树拆分后，节点数 **≤ 6**（`UNTREEIFY_THRESHOLD`），那就没必要维持红黑树了，直接退回成链表。

#### HashMap的put方法的具体流程

![image-20250511103052370](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511103052370.png)



![image-20250511103106483](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511103106483.png)

# ==Map源码==

**扩容阈值** 超过这个就触发扩容

![image-20250927145345515](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927145345515.png)



这个key 具体是什么： 就是map 中的key 通过key计算hash值确定位置

![image-20250927150038644](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927150038644.png)

### HashMap的扩容机制

![image-20250927150646740](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927150646740.png)







在 JDK 源码里，出于性能优化，**取模运算用位运算代替** 

`(newCap - 1) & hash` 就是 **高效版的取模运算**，等价于 `hash % newCap`。

![image-20250927151740287](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250927151740287.png)

是原始位置加上oldcap

**红黑树搬迁的时候 如果 红黑树结点数量小于6 就会退化成链表了 (性能上更合适)**



---



### ==HashMap 的寻址算法 和 数组长度为什么是  2 的n次幂==





### ==HashMap在1.7下的多线程死循环的问题==





---



## 集合使用注意事项

### 集合判空

> **判断所有集合内部的元素是否为空，使用 `isEmpty()` 方法，而不是 `size()==0` 的方式。**

这是因为 `isEmpty()` 方法的可读性更好，并且时间复杂度为 `O(1)`。











### 集合转Map



> **在使用 `java.util.stream.Collectors` 类的 `toMap()` 方法转为 `Map` 集合时，一定要注意当 value 为 null 时会抛 NPE 异常。**



```java
class Person {
    private String name;
    private String phoneNumber;
     // getters and setters
}

List<Person> bookList = new ArrayList<>();
bookList.add(new Person("jack","18163138123"));
bookList.add(new Person("martin",null));
// 空指针异常
bookList.stream().collect(Collectors.toMap(Person::getName, Person::getPhoneNumber));
```



**源码分析原因：**

下面我们来解释一下原因。

首先，我们来看 `java.util.stream.Collectors` 类的 `toMap()` 方法 ，可以看到其内部调用了 `Map` 接口的 `merge()` 方法。

~~~java
public static <T, K, U, M extends Map<K, U>>
Collector<T, ?, M> toMap(Function<? super T, ? extends K> keyMapper,
                            Function<? super T, ? extends U> valueMapper,
                            BinaryOperator<U> mergeFunction,
                            Supplier<M> mapSupplier) {
    BiConsumer<M, T> accumulator
            = (map, element) -> map.merge(keyMapper.apply(element),
                                          valueMapper.apply(element), mergeFunction);
    return new CollectorImpl<>(mapSupplier, accumulator, mapMerger(mergeFunction), CH_ID);
}
~~~

`Map` 接口的 `merge()` 方法如下，这个方法是**接口中的默认实现**。

~~~java
default V merge(K key, V value,
        BiFunction<? super V, ? super V, ? extends V> remappingFunction) {
    Objects.requireNonNull(remappingFunction);
    Objects.requireNonNull(value);
    V oldValue = get(key);
    V newValue = (oldValue == null) ? value :
               remappingFunction.apply(oldValue, value);
    if(newValue == null) {
        remove(key);
    } else {
        put(key, newValue);
    }
    return newValue;
}
~~~

`merge()` 方法会先调用 `Objects.requireNonNull()` 方法判断 value 是否为空。

~~~java
public static <T> T requireNonNull(T obj) {
    if (obj == null)
        throw new NullPointerException();
    return obj;
}
~~~

### 集合遍历

泛化（Generalization）

- 是“**继承**”关系的一种。
- 用于 **类与类** 或 **接口与接口**：
  - 类继承类：`class B extends A`
  - 接口继承接口：`interface B extends A`

| 名称            | 类型   | 所在包             | 作用                                                     | 是否可直接使用      | 与谁一起用                          | 示例                                |
| --------------- | ------ | ------------------ | -------------------------------------------------------- | ------------------- | ----------------------------------- | ----------------------------------- |
| `Collection<E>` | 接口   | `java.util`        | **最顶层的集合接口**，是 `List`、`Set`、`Queue` 的父接口 | ❌（不能直接实例化） | 与所有集合类相关（如 `ArrayList`）  | `List<E> list = new ArrayList<>();` |
| `Collections`   | 工具类 | `java.util`        | 提供静态方法操作集合：排序、同步、只读、查找等           | ✅                   | 与 `Collection` 的子类一起使用      | `Collections.sort(list);`           |
| `Collectors`    | 工具类 | `java.util.stream` | 提供多个 `Collector` 实现，如 `toList()`、`toMap()` 等   | ✅                   | 与 `Stream` 和 `Collector` 一起使用 | `Collectors.toMap(...)`             |



**collections 与 collectors**

**使用场景**	集合已经存在，你想对它进行处理	在使用 Stream 流处理时的 .collect(...) 终端操作
**是否依赖 Stream**	❌ 与 Stream 无关	✅ 专门为 Stream API 服务



---



`Iterator<E>`：基本迭代器，有 `hasNext()`、`next()`、`remove()`。

<span style="color:#FF0000;">任何实现了 `Iterable` 的集合都可以通过 `iterator()` 方法获取一个 `Iterator`对象。</span>

`Iterator` 是集合遍历的统一入口，它解耦了集合的具体类型，让你用统一方式、安全地访问、删除集合元素，是 Java 集合框架的核心机制之一。

~~~java
Collection<String> names = List.of("Alice", "Bob", "Charlie");
Iterator<String> iterator = names.iterator();

while (iterator.hasNext()) {
    String name = iterator.next();
    System.out.println(name);
}

~~~

![img](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/2021011818095360.png)



《阿里巴巴 Java 开发手册》的描述如下：

> **不要在 foreach 循环里进行元素的 `remove/add` 操作。remove 元素请使用 `Iterator` 方式，如果并发操作，需要对 `Iterator` 对象加锁。**

通过反编译你会发现 foreach 语法底层其实还是依赖 `Iterator` 。不过， `remove/add` 操作直接调用的是集合自己的方法，而不是 `Iterator` 的 `remove/add`方法

这就导致 `Iterator` 莫名其妙地发现自己有元素被 `remove/add` ，然后，它就会抛出一个 `ConcurrentModificationException` 来提示用户发生了并发修改异常。这就是单线程状态下产生的 **fail-fast 机制**。

> **fail-fast 机制**：多个线程对 fail-fast 集合进行修改的时候，可能会抛出`ConcurrentModificationException`。 即使是单线程下也有可能会出现这种情况，上面已经提到过。
>
> 相关阅读：[什么是 fail-fast](https://www.cnblogs.com/54chensongxia/p/12470446.html) 。

Java8 开始，可以使用 `Collection#removeIf()`方法删除满足特定条件的元素,如



~~~java
List<Integer> list = new ArrayList<>();
for (int i = 1; i <= 10; ++i) {
    list.add(i);
}
list.removeIf(filter -> filter % 2 == 0); /* 删除list中的所有偶数 */
System.out.println(list); /* [1, 3, 5, 7, 9] */
~~~

除了上面介绍的直接使用 **Iterator** 进行遍历操作之外，你还可以：

使用普通的 for 循环
使用 **fail-safe** 的集合类。java.util包下面的所有的集合类都是 fail-fast 的，而java.util.concurrent包下面的所有的类都是 **fail-safe** 的。
……







### 集合去重

**可以利用 `Set` 元素唯一的特性，可以快速对一个集合进行去重操作，避免使用 `List` 的 `contains()` 进行遍历去重或者判断包含操作。**



### 集合转数组

**使用<span style="color:#FF0000;">集合转数组</span>的方法，必须使用集合的 `toArray(T[] array)`，传入的是类型完全一致、长度为 0 的空数组。**



### 数组转集合

#### 1. **`Arrays.asList()` 的陷阱**

```Java
String[] arr = {"a", "b", "c"};
List<String> list = Arrays.asList(arr);
list.add("d"); // 抛出 UnsupportedOperationException
```

- **问题原因**：
  `Arrays.asList()` 返回的是一个**固定大小的 `List` 视图**，底层直接包装原数组，因此不支持结构性修改（如 `add`、`remove`）。
- **原理**：
  返回的 `List` 是 `Arrays` 的内部类 `ArrayList`（非 `java.util.ArrayList`），它直接引用原数组，且未实现 `add` 等方法。

**解决方案**：
使用 `new ArrayList<>(Arrays.asList(arr))` 创建独立 `List`：

```java
List<String> list = new ArrayList<>(Arrays.asList(arr));
list.add("d"); // 正常执行
```

#### 2. **共享底层数组**

```java
String[] arr = {"a", "b", "c"};
List<String> list = Arrays.asList(arr);
arr[0] = "modified";
System.out.println(list.get(0)); // 输出 "modified"
```

- **问题原因**：
  `Arrays.asList()` 生成的 `List` 与原数组共享内存，修改数组会影响 `List`，反之亦然。
- 

**1. List 转数组的底层机制**

Java 的 `List` 接口的 `toArray()` 方法实现（以 `ArrayList` 为例）会**复制元素到新数组**：



```java
public Object[] toArray() {
    return Arrays.copyOf(elementData, size); // 复制有效元素到新数组
}
```

- **新数组与原 List 解耦**：转换后的数组是原 List 元素的**独立副本**，与原 List 的底层存储（如 `ArrayList` 的 `elementData`）无直接关联。
- **数组长度固定**：转换后的数组长度固定为 `List.size()`，即使原 List 后续扩容或缩容，数组也不会自动变化。

---







![image-20250518100433883](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250518100433883.png)

![image-20250511105906554](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511105906554.png)

![image-20250511105916190](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511105916190.png)



![image-20250511105926186](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511105926186.png)



![image-20250511105940271](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511105940271.png)



![image-20250511110007407](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250511110007407.png)

数组 转化为流 因为只有流才可以 collect收集为集合collection







### 集合可以结合stream API 还有数据结构



