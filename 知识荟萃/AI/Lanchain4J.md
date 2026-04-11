# Lanchain4j

## 会话功能

~~~xml
<parent>
    <groupId> org.springframework.boot </groupId>
    <artifactId> spring-boot-starter-parent </artifactId>
    <version> 2.7.18 </version> <!-- 可根据需要更换具体版本 -->
</parent>

~~~

**BOM 管理依赖**

~~~xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId> org.springframework.boot </groupId>
      <artifactId> spring-boot-dependencies </artifactId>
      <version> 2.7.18 </version>
      <type> pom </type>
      <scope> import </scope>
    </dependency>
  </dependencies>
</dependencyManagement>

~~~



 ![image-20250627213423420](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627213423420.png)

~~~xml
<dependency>
    <groupId> dev.langchain4j </groupId>
    <artifactId> langchain4j-open-ai </artifactId>
    <version> 1.0.1 </version>
</dependency>

~~~

​	**Spring 整合**

![image-20250627220531507](C:/Users/33813/AppData/Roaming/Typora/typora-user-images/image-20250627220531507.png)

---



![image-20250627221102342](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627221102342.png)

**尽量使用 Bom 管理依赖 同时还要注意版本的兼容性 如 springboot 和 mybatis plus**

~~~xml
	<dependency>
				<groupId> dev.langchain4j </groupId>
				<artifactId> langchain4j-bom </artifactId>
				<version>${langchain4j.version}</version >
				<type> pom </type>
				<scope> import </scope>
			</dependency>
~~~





为了 ==简化== 上述操作：提供了 ==**声明式的使用**==

 ![image-20250627221411722](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627221411722.png)

需要为哪个接口创建代理对象只需要在这个接口上添加这个 AiService 注解即可

hence lanchain4j 会自动地调用 AiService 帮助创建该接口的代理对象 并注入到 ==IOC 容器中==





![image-20250627231232974](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627231232974.png)

> **如何判断一个大语言模型 API 服务使用的是哪种协议（OpenAI 协议？还是别的？）**。
>
> 如果它的接口路径是 `POST /v1/chat/completions`，并且请求/响应结构与 OpenAI 一样，那它就是 **OpenAI 协议兼容**。

~~~yaml
langchain4j:
  open-ai:
    streaming-chat-model:
      base-url: https://openrouter.ai/api/v1/
      api-key: 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
      model-name: deepseek/deepseek-r1: free
      log-request: true
      log-response: true
~~~



~~~xml
<dependency>
    <groupId> org.springframework.boot </groupId>
    <artifactId> spring-boot-starter-webflux </artifactId>
</dependency>

<dependency>
    <groupId> dev.langchain4j </groupId>
    <artifactId> langchain4j-reactor </artifactId>
    <version> 1.0.1-beta6 </version>
</dependency>

~~~



![image-20250627231515379](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627231515379.png)





![image-20250627233221529](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627233221529.png)



![image-20250627233240193](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250627233240193.png)



**@UserMessage**  标记用户的输入消息，自动作为 prompt 内容发送



```java
@AiService
public interface PromptService {
@UserMessage("请用中文回答，{{name}} 喜欢的颜色是什么？")
String askColor(@V("name") String name);
}
```


### 会话记忆

![image-20250628094354790](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628094354790.png)



### 会话记忆隔离

![](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628094635218.png)

![image-20250628095144099](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628095144099.png)

前端 的 **memoryId 可以是时间戳**

### 会话记忆持久化

服务器重启就清空内存了 （而这个会话记忆是存在内存中的）



![image-20250628100919347](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628100919347.png)

官方默认是提供 SingleSlot…… 这个实现类 这个是存在内存里的

官方提供接口的好处 ： 自己提供一个这个接口的实现类 提供一个 将这个 message 保存在 redis 里





**使用数据库持久化 ==会话记忆==**

![image-20250628101018535](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628101018535.png)

@Repository 注解 标注在类上，表示这个类是用于访问数据库的



![image-20250628101234647](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628101234647.png)



![image-20250628101323986](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628101323986.png)



~~~java
@Repository
public class RedisChatMemoryStore implements ChatMemoryStore {
    @Autowired
    private StringRedisTemplate redisTemplate;

    @Override
    public List<ChatMessage> getMessages(Object memoryId) {
        String redisKey = RedisConstant.AI_CHAT_MEMORY_KEY + memoryId.toString();
        String msgJson = redisTemplate.opsForValue().get(redisKey);
        return ChatMessageDeserializer.messagesFromJson(msgJson);
    }

    @Override
    public void updateMessages(Object memoryId, List<ChatMessage> list) {
        String redisKey = RedisConstant.AI_CHAT_MEMORY_KEY + memoryId.toString();
        String msgJson = ChatMessageSerializer.messagesToJson(list);
//        会话记忆保留一天
        redisTemplate.opsForValue().set(redisKey, msgJson, Duration.ofDays(1));
    }

    @Override
    public void deleteMessages(Object memoryId) {
        String redisKey = RedisConstant.AI_CHAT_MEMORY_KEY + memoryId.toString();
        redisTemplate.delete(redisKey);
    }
}
~~~





---



## RAG 知识库



![ ](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628180502082.png)

![image-20250628180625531](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628180625531.png)



![image-20250628181620775](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628181620775.png)



![image-20250628181917225](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628181917225.png)



![image-20250628182025074](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628182025074.png)







![image-20250628190105574](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628190105574.png)

![image-20250628190832179](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628190832179.png)

**retrive 检索**

注意 **自动装配** 中的问题： 名字，类型

![image-20250628195647014](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628195647014.png)

## ==自动装配问题：==

依赖有时候里边已经自动地往容器里边注入了一个 bean 所以这里的要改名



![image-20250628195848351](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628195848351.png)

### 核心 API

ingestor ： **（分割）** 切片 向量化 存储

![image-20250628200345176](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628200345176.png)

<span style="color:#FF0000;">**可加载 服务器磁盘 或者 类路径 或者 url 的 资源**</span>

![image-20250628200417056](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628200417056.png)

解析什么样的文档 **类型**

![image-20250628200605490](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628200605490.png)

  ![image-20250628210122634](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628210122634.png)





文档中的**文字分割策略**

![image-20250628213355355](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628213355355.png)

  ![image-20250628213539551](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628213539551.png)

![image-20250628215329336](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628215329336.png)

**递归：根据参数设置进行切割 直到满足条件** 要理解本质！！！

**`chunkSize` (块大小):** 这个参数定义了每个文档块（chunk）的最大尺寸。它的单位是**字符**。这意味着你的每个文档块最多包含 `chunkSize` 个字符。

- **如果 `chunkSize` 太小：** 文档会被切分成很多小块，可能会导致单个块丢失上下文。例如，一个完整的句子或段落被切断，影响后续的嵌入（embedding）质量和问答效果。
- **如果 `chunkSize` 太大：** 文档块可能包含太多信息，导致模型（如 LLM）在处理时难以集中在关键信息上，甚至可能超过模型的上下文窗口限制。

**`chunkOverlap` (块重叠):** 这个参数定义了相邻两个文档块之间重叠的字符数。

- **作用：** 重叠是为了确保在切分过程中，上下文信息不会丢失。当一个句子或重要短语恰好位于两个块的边界时，重叠部分可以保证这部分信息同时存在于两个块中。
- **配置建议：** 重叠值通常是 `chunkSize` 的 10% 到 20%。如果重叠值太小，可能会导致上下文丢失；如果太大，则会产生很多重复信息，增加处理的复杂性和成本



----

![image-20250628220035604](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628220035604.png)

这个内置向量模型功能不是很强大 所以可以使用模型平台中提供的向量模型 利用 api 来使用

![image-20250628220346629](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628220346629.png)

lanchain4j 会根据配置信息自动往 ioc 容器中注入一个 embeddingModel 对象

**存储与检索中使用**

<span style="color:#FF3333;">**ingestor 和 检索器 中注入这个 模型 （默认是自带的向量模型 反正这种就类似 可插拔 可自定义的 插件）**</span>





![image-20250628220538981](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628220538981.png)

**这个是基于内存的向量数据库 也就是向量都存储在内存当中**

![image-20250628221100857](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628221100857.png)

![image-20250628221948015](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628221948015.png)

```
docker run --name redis-vector -d -p 6379:6379 redislabs/redisearch:latest

# 在docker-compose.yml 中
image: redislabs/redisearch:latest
```

redislabs/redisearch: 这是镜像的名称，指向 Redis Labs 官方提供的 Redis Stack 镜像。Redis Stack 是一个增强版的 Redis，集成了多个模块，包括 RediSearch（用于全文搜索和向量相似性搜索）、RedisJSON（JSON 数据支持）等。这些模块扩展了 Redis 的功能，使其适合存储和查询嵌入向量（如 LangChain4j 的 RedisEmbeddingStore 可能依赖的场景）。

**将 redisembeddingstore 对象（这个对象是根据配置自动注入到 ioc 容器当中的）分别设置给存储和检索**

![image-20250628223740087](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628223740087.png)



![image-20250628223806872](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250628223806872.png)

注意由于模型平台中向量模型的限制 如 ：每次只能将**十个片段发送给向量大模型**  大模型进行处理 将片段**向量化**

**由于每个模型平台限制不同 所以 lanchain4j 需要知道 可以在 lanchain4j  的配置项中 指定 max-segment-per-batch : 10**



由于这个 store 以及将片段向量化并且存储进 redis 了就不要要每次启动后端服务的时候重新读取类路径资源然后切片……向量化存储各种重复操作了

**（<span style="color:#FF0000;">`@Bean` 注解的方法在 Spring Boot 启动时会执行一次</span>**，**用于创建一个 Bean 实例并交给容器管理**，默认是单例。）

所以可以暂时的注释掉 @Bean



**`AiServiceWiringMode.EXPLICIT`**（显式模式）：

- **作用**：当你将这个值设置为 `EXPLICIT` 时，你需要**手动指定**所有要使用的 Bean，就像代码中做的那样。

~~~java
@AiService(
        wiringMode = AiServiceWiringMode.EXPLICIT,
        chatModel = "openAiChatModel",
        streamingChatModel = "openAiStreamingChatModel",
        chatMemoryProvider = "chatMemoryProvider",
        contentRetriever = "contentRetriever"


)
public interface AiChatService {
    @SystemMessage(fromResource = "systemMsg.txt")
    public Flux<String> chat(@UserMessage String message, @MemoryId String memoryId );


}

~~~



~~~yaml
langchain4j:
  community:
    redis:
      host: localhost
      port: 6379
  open-ai:
#    向量模型
    embedding-model:
      base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
      api-key: sk-d0915b28e42a456fabe8a390bbce957f
      model-name: text-embedding-v4
      log-requests: true
      log-responses: true
      max-segments-per-batch: 10

    streaming-chat-model:
      base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
      api-key: sk-d0915b28e42a456fabe8a390bbce957f
      model-name: qwen-plus
      log-requests: true
      log-responses: true

    chat-model:
      base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
      api-key: sk-d0915b28e42a456fabe8a390bbce957f
      model-name: qwen-plus
      log-requests: true
      log-responses: true

~~~



~~~java
/**
 * @author 33813
注入(wire)模式设置为 "显式" 模式，意思是：
我自己手动指定要使用哪个模型，而不是让 Spring 自动注入默认的。
默认是 WiringMode.AUTOMATIC，如果你有多个模型（chatModel、streamingModel 等），就需要显式指定使用哪一个。

 */

@AiService(
        wiringMode = AiServiceWiringMode.EXPLICIT,
        chatModel = "openAiChatModel",
        streamingChatModel = "openAiStreamingChatModel",
        chatMemoryProvider = "chatMemoryProvider"

)
public interface AiChatService {
    @SystemMessage(fromResource = "systemMsg.txt")
    public Flux<String> chat(@UserMessage String message, @MemoryId String memoryId );

}
~~~

**ai 相关配置类**

~~~java
@Configuration
public class AiChatConfig {
    @Autowired
    private ChatMemoryStore redisChatMemoryStore;
//    在配置文件中配置注入了
    @Autowired
    private EmbeddingModel embeddingModel;

    @Autowired
    private RedisEmbeddingStore store;
//    会话记忆提供者
    @Bean
    public ChatMemoryProvider chatMemoryProvider() {
        ChatMemoryProvider chatMemoryProvider = new ChatMemoryProvider() {
            @Override
            public ChatMemory get(Object memoryId) {
                return MessageWindowChatMemory.builder()
                        .id(memoryId)
                        .maxMessages(20)
                        .chatMemoryStore(redisChatMemoryStore)
                        .build();
            }
        };
        return chatMemoryProvider;
    }

//    构建向量数据库 存储对象
    @Bean
    public EmbeddingStore store() {
        List<Document> documents = ClassPathDocumentLoader.loadDocuments("store/knowledge",new ApachePdfBoxDocumentParser());
//        InMemoryEmbeddingStore store = new InMemoryEmbeddingStore();
//        如何配置参数
        DocumentSplitter splitter = DocumentSplitters.recursive(500,100);
        EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
//                .embeddingStore(store) **这个是基于内存的向量数据库 也就是向量都存储在内存当中**
                .embeddingStore(store)
                .documentSplitter(splitter)
                .embeddingModel(embeddingModel)
                .build();
        ingestor.ingest(documents);
        return store;
    }
//    构建向量数据库 检索对象
    @Bean
    public ContentRetriever contentRetriever(EmbeddingStore store) {
        return EmbeddingStoreContentRetriever.builder()
                .embeddingStore(store)
                .embeddingModel(embeddingModel)
                .minScore(0.5)
                .maxResults(3)
                .build();
    }

}
~~~



---



## ==Tools （Function calling）工具== 

| 概念                             | 作用                                            | 技术机制                                      | 举例                              |
| -------------------------------- | ----------------------------------------------- | --------------------------------------------- | --------------------------------- |
| **Function Calling（函数调用）** | 大模型根据意图，**调用你定义的函数 / 工具方法** | OpenAI function calling / LangChain Tool 调用 | AI 自动调用 `searchWeather(city)` |

##  



# MCP server 开发





# 网络配置问题

### 修改 Windows 的 DNS 配置

这是最关键的一步 —— **当前使用的 `192.168.100.1` 是局域网 DNS，不能解析外部域名。你要改成公网可用的 DNS 服务器。**

#### 🛠 操作步骤如下：

1. 打开控制面板：

   > Win + R → 输入 `ncpa.cpl` → 回车

2. 找到你的联网网卡（如“以太网”或“WLAN”） → 右键 → 属性

3. 找到“Internet 协议版本 4（TCP/IPv4）” → 双击

4. 选择 **“使用下面的 DNS 服务器地址”**

   ```bash
   首选 DNS 服务器：223.5.5.5   （阿里公共 DNS）
   备用 DNS 服务器：8.8.8.8     （Google DNS）
   ```

5. 点击“确定”，关闭所有窗口。

------

### ✅ 第二步：清理 DNS 缓存（可选，但推荐）

打开命令提示符（CMD），运行：

```bash

ipconfig /flushdns
```

输出结果：

```nginx
Windows IP 配置

已成功刷新 DNS 解析缓存。
```

------

### ✅ 第三步：确认 DNS 是否生效

你可以在 CMD 中运行：

```bash
nslookup dashscope.aliyuncs.com
```

如果配置成功，会看到：

```bash复
服务器:  aliDNS 或 googleDNS
地址:  223.5.5.5

非权威应答:
名称:    dashscope.aliyuncs.com
地址:    xxx.xxx.xxx.xxx
```





# 权限控制问题 - ai会话的盗用？

水平越权”（Horizontal Privilege Escalation）是指用户在拥有合法权限的前提下，访问或操作与自己权限相同但不属于自己的数据或资源的一种权限滥用行为，属于访问控制不当的一种。



| **水平越权** | 普通用户访问 **其他用户的资源**（同一权限级别） |

| **垂直越权** | 普通用户访问 **管理员接口** 或执行超出自身权限的操作 |

### 防御措施

1. **身份校验**：后端接口根据用户身份 token 校验资源归属。
2. **资源访问控制**：接口必须验证“当前操作用户是否有权访问该资源”。
3. **使用权限注解或 AOP 控制资源访问**。
4. **不要信任前端传来的 ID、参数等敏感信息**



### 举个简单例子：

你和别人都在一个社交网站上，假设你是用户 A，对方是用户 B。

你访问你的个人信息页面：

```
https://example.com/user/profile?id=1001 
```

- 你试着手动修改 URL 为：

  ```
  https://example.com/user/profile?id=1002 
  ```

  

如果服务器**没有校验你是否是 ID=1002 的用户本人**，就把 B 的信息返回给你了 —— 这就是**水平越权**。

## 安全角度：用户不能被信任

后端接收到的所有参数（无论是请求体、请求参数、Header、Cookie）**都不能信任用户传来的值**，必须：

- 认证（Authentication）：验证用户身份（如 JWT、Session）
- 授权（Authorization）：验证当前身份是否能访问该资源（防止越权）



# ==响应式编程==

```css
聊天接口：后端接收id 利用 线程上下文
用户id 查询会话 先检查 是否用户
有这个会话  如可以 的话

调用ai接口 返回结果数据
写入数据库操作： 更新会话表 更新消息表


用户请求 ——> Controller
          ——> AI 服务生成流式响应（Flux<String>）
          ——> 一边推送给前端
          ——> 一边将数据写入 MQ（Kafka/RabbitMQ）
                            ↓
                    消费者异步消费消息
                            ↓
                  持久化到数据库（MongoDB/MySQL）
```

**Spring WebFlux**

## `.doOnNext(...)` 和 `.doOnComplete(...)` 都是对流的“副作用”操作

- `.doOnNext()` 不会改变 `Flux` 的数据流，它只是**在每个元素发出时执行你写的代码**。
- `.doOnComplete()` 是当流结束时触发的回调，也不会影响数据流传递。

所以**整个链的返回值还是那个流（Flux<String>）本身**，它会传递给 Spring WebFlux 的框架，由框架负责把它“写入 HTTP 响应”，**实现实时推送给前端**。



```java
@PostMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<String> chat(@RequestBody AiPromptDTO aiPromptDTO) {
    return aiChatService.chat(aiPromptDTO.getMsg())
            .doOnNext(token -> {
                // 异步写数据库（例如发送到消息队列或写入缓存）
                messageBuffer.append(token);
            })
            .doOnComplete(() -> {
                // 消息完整，落库
                messageService.saveMessage(aiPromptDTO.getUserId(), messageBuffer.toString());
            });
}
```
