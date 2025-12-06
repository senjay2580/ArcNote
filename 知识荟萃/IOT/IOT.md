

# IOT基本概念



<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250707161927173.png" alt="image-20250707161927173" style="zoom:50%;" />







产品：某一类设备集合
物模型：描述产品属性或者服务事件
设备：具体的某一款产品

产品：设备的集合，通常指一组具有相同功能的设备。物联网平台为每个产品颁发全局唯一的ProductK。
简单说就是某一类产品，比如，手表、大门通道门禁、紧急呼叫报警器、滞留报警器、跌倒报警器

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708165820377.png" alt="image-20250708165820377" style="zoom:50%;" />





<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708170508101.png" alt="image-20250708170508101" style="zoom:50%;" />

![image-20250708170503075](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708170503075.png)

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708174337145.png" alt="image-20250708174337145" style="zoom:50%;" />

<img src="https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708174606287.png" alt="image-20250708174606287" style="zoom: 80%;" />

| 消息队列系统 | Topic 使用方式                                               |
| ------------ | ------------------------------------------------------------ |
| **RabbitMQ** | 本质上通过“交换机（Exchange）”和“RoutingKey”模拟 Topic 模式，使用 `topic` 类型交换机。 |
| **Kafka**    | Topic 是核心概念，Producer 发消息到 Topic，Consumer 分组消费。 |
| **RocketMQ** | Producer 指定 Topic 发送消息，Consumer 订阅 Topic。          |
| **ActiveMQ** | 明确区分 Queue 和 Topic，Topic 用于广播消息给多个订阅者。    |

设备通过网络协议将传感器采集的数据，**推送给云端服务器或本地 IoT 平台**。

~~~
[传感器数据]
     ↓ 
[嵌入式设备/MCU（如 ESP32、树莓派）]   --- c程序运行在主控芯片上   
     ↓         ← 数据封装（JSON/二进制）+ 网络协议（MQTT/HTTP）
[网络（WiFi/4G/NB-IoT）]
     ↓
[IoT 平台服务器（阿里云、华为云、自建MQTT服务器等）]
     ↓
[数据库 / 应用服务处理 / 可视化平台]


~~~

程序烧录进芯片”或“固件烧录”，其实就是把你用 C/C++ 写的程序（**编译后的机器码**）写入芯片内部的**Flash 存储空间**里，让芯片上电后自动执行这个程序。

~~~
[C / C++ 源码]  →  [编译器]  →  [生成 .hex / .bin 文件]  →  [烧录工具]  →  [写入芯片 Flash]
~~~

**芯片平台**（也称为 MCU 平台、处理器平台），是指一种**基于特定芯片架构的软硬件开发环境**，包括芯片、工具链、开发板、外围驱动和软件库。

| 平台名称             | 所用芯片                | 架构             | 特点                     |
| -------------------- | ----------------------- | ---------------- | ------------------------ |
| **STM32**            | STM32F103, STM32F407... | ARM Cortex-M     | 工业级，低功耗，高性能   |
| **ESP32**            | ESP32, ESP8266          | Tensilica Xtensa | WiFi/蓝牙，物联网热门    |
| **51单片机**         | STC89C52                | MCS-51           | 古老经典，适合入门教学   |
| **Arduino**          | ATmega328P, SAMD21      | AVR / ARM        | 上手快，配件多           |
| **RISC-V 平台**      | GD32VF103, BL602        | RISC-V           | 开源新兴架构，性能较好   |
| **树莓派（看下方）** | Broadcom SoC            | ARM Cortex-A     | 实际是小型电脑，不是 MCU |



~~~js
// 通过软件模拟 硬件上传数据

// 引入阿里云提供的 mqtt 客户端库
const mqtt = require('aliyun-iot-mqtt');

// 设备身份信息（三元组）
const options = {
    productKey: "j0rk76chJkx", // 产品 Key
    deviceName: "cdr1",        // 设备名称
    deviceSecret: "9551b748504f25aaa803e61487a15676", // 设备密钥
    host: "iot-06z00frq8umvxk2.mqtt.iothub.aliyuncs.com" // 接入点域名
};

// 建立与阿里云物联网平台的 MQTT 连接
const client = mqtt.getAliyunIotMqttClient(options);

// 订阅云平台下发的指令（下行 Topic）
client.subscribe(`/${options.productKey}/${options.deviceName}/user/get`);
client.subscribe(`/sys/${options.productKey}/${options.deviceName}/thing/event/property/post`);

// 监听接收到的消息
client.on('message', function (topic, message) {
    console.log("📥 收到 Topic:", topic);
    console.log("📄 消息内容:", message.toString());
});

// 模拟电池电量取值范围（此值在 getPostData 中用到）
var batteryLevel = 100;

// 生成要上报的数据（JSON 格式）
function getPostData() {
    return JSON.stringify({
        params: {
            PowerConsumption: batteryLevel // 这里对应物模型
        }
    });
}

// 每隔 5 秒定时向阿里云平台上报设备属性数据
setInterval(function () {
    client.publish(
        `/sys/${options.productKey}/${options.deviceName}/thing/event/property/post`,
        getPostData()
    );
    console.log("📤 上报数据:", getPostData());
}, 5 * 1000);

~~~



**设备数据消费**

AMQP全称Advanced Message Queuing Protocol,是一种网络协议，用于在应用程序之间传递消息。它是一种开放标准的消息传
递协议，可以在**不同的系统之间**实现可靠、安全、高效的消息传递
AMQP**协议的实现包括多种消息队列软件**，例如**RabbitMQ、Apache ActiveMQ、Apache Qpid**等。这些软件提供了可靠、高效的消息传
递服务，广泛应用于分布式系统、云计算、物联网等领域。
![image-20250708201612163](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250708201612163.png)

 

在IOT官方文档中，已经提供了对应的接收数据的解决方案，如下链接：

https://help.aliyun.com/zh/iot/developer-reference/connect-a-client-to-iot-platform-by-using-the-sdk-for-java?spm=a2c4g.11186623.0.0.7d7234bdQCi7MQ

## application.yml文件中添加IOT配置

```yaml
zzyl:
  aliyun:
    accessKeyId: xxxxx
    accessKeySecret: yyyyy
    consumerGroupId: DEFAULT_GROUP
    regionId: cn-shanghai
    iotInstanceId: zzzz
    host: ddddddddd.amqp.iothub.aliyuncs.com

```

在zzyl-framework中添加读取文件配置类

```java
package com.itheima.properties;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 */

@Setter
@Getter
@NoArgsConstructor
@ToString
@Configuration
@ConfigurationProperties(prefix = "iot.aliyun")
public class AliIoTConfigProperties {

    /**
     * 访问Key
     */
    private String accessKeyId;
    /**
     * 访问秘钥
     */
    private String accessKeySecret;
    /**
     * 区域id
     */
    private String regionId;
    /**
     * 实例id
     */
    private String iotInstanceId;
    /**
     * 域名
     */
    private String host;

    /**
     * 消费组
     */
    private String consumerGroupId;

}
```



## 常见线程池配置类

在项目中添加配置类，如下

```java
package com.itheima.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

@Configuration
public class ThreadPoolConfig {

    /**
     * 核心线程池大小
     */
    private static final int CORE_POOL_SIZE = Runtime.getRuntime().availableProcessors();

    /**
     * 最大可创建的线程数
     */
    private static final int MAX_POOL_SIZE = Runtime.getRuntime().availableProcessors() * 2;

    /**
     * 队列最大长度
     */
    private static final int QUEUE_CAPACITY = 50000;

    /**
     * 线程池维护线程所允许的空闲时间
     */
    private static final int KEEP_ALIVE_SECONDS = 60;

    @Bean
    public ExecutorService executorService(){
        AtomicInteger c = new AtomicInteger(1);
        LinkedBlockingQueue<Runnable> queue = new LinkedBlockingQueue<Runnable>(QUEUE_CAPACITY);
        return new ThreadPoolExecutor(
                CORE_POOL_SIZE,
                MAX_POOL_SIZE,
                KEEP_ALIVE_SECONDS,
                TimeUnit.MILLISECONDS,
                queue,
                r -> new Thread(r, "itheima-pool-" + c.getAndIncrement()),
                new ThreadPoolExecutor.DiscardPolicy()
        );
    }
}
```

## AmqpClient

```java
package com.itheima.job;

import com.heima.properties.AliIoTConfigProperties;
import org.apache.commons.codec.binary.Base64;
import org.apache.qpid.jms.JmsConnection;
import org.apache.qpid.jms.JmsConnectionListener;
import org.apache.qpid.jms.message.JmsInboundMessageDispatch;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.jms.*;
import javax.naming.Context;
import javax.naming.InitialContext;
import java.net.InetAddress;
import java.net.URI;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.concurrent.ExecutorService;

@Component
public class AmqpClient implements ApplicationRunner {
    private final static Logger logger = LoggerFactory.getLogger(AmqpClient2.class);

    @Autowired
    private AliIoTConfigProperties aliIoTConfigProperties;

    //控制台服务端订阅中消费组状态页客户端ID一栏将显示clientId参数。
    
    //建议使用机器UUID、MAC地址、IP等唯一标识等作为clientId。便于您区分识别不同的客户端。
    private static String clientId;

    static {
        try {
            clientId = InetAddress.getLocalHost().getHostAddress();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    // 指定单个进程启动的连接数
    // 单个连接消费速率有限，请参考使用限制，最大64个连接
    // 连接数和消费速率及rebalance相关，建议每500QPS增加一个连接
    private static int connectionCount = 4;

    //业务处理异步线程池，线程池参数可以根据您的业务特点调整，或者您也可以用其他异步方式处理接收到的消息。
    @Autowired
    private ExecutorService executorService;

    public void start() throws Exception {
        List<Connection> connections = new ArrayList<>();

        //参数说明，请参见AMQP客户端接入说明文档。
        for (int i = 0; i < connectionCount; i++) {
            long timeStamp = System.currentTimeMillis();
            //签名方法：支持hmacmd5、hmacsha1和hmacsha256。
            String signMethod = "hmacsha1";

            //userName组装方法，请参见AMQP客户端接入说明文档。
            String userName = clientId + "-" + i + "|authMode=aksign"
                    + ",signMethod=" + signMethod
                    + ",timestamp=" + timeStamp
                    + ",authId=" + aliIoTConfigProperties.getAccessKeyId()
                    + ",iotInstanceId=" + aliIoTConfigProperties.getIotInstanceId()
                    + ",consumerGroupId=" + aliIoTConfigProperties.getConsumerGroupId()
                    + "|";
            //计算签名，password组装方法，请参见AMQP客户端接入说明文档。
            String signContent = "authId=" + aliIoTConfigProperties.getAccessKeyId() + "&timestamp=" + timeStamp;
            String password = doSign(signContent, aliIoTConfigProperties.getAccessKeySecret(), signMethod);
            String connectionUrl = "failover:(amqps://" + aliIoTConfigProperties.getHost() + ":5671?amqp.idleTimeout=80000)"
                    + "?failover.reconnectDelay=30";

            Hashtable<String, String> hashtable = new Hashtable<>();
            hashtable.put("connectionfactory.SBCF", connectionUrl);
            hashtable.put("queue.QUEUE", "default");
            hashtable.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.qpid.jms.jndi.JmsInitialContextFactory");
            Context context = new InitialContext(hashtable);
            ConnectionFactory cf = (ConnectionFactory) context.lookup("SBCF");
            Destination queue = (Destination) context.lookup("QUEUE");
            // 创建连接。
            Connection connection = cf.createConnection(userName, password);
            connections.add(connection);

            ((JmsConnection) connection).addConnectionListener(myJmsConnectionListener);
            // 创建会话。
            // Session.CLIENT_ACKNOWLEDGE: 收到消息后，需要手动调用message.acknowledge()。
            // Session.AUTO_ACKNOWLEDGE: SDK自动ACK（推荐）。
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            connection.start();
            // 创建Receiver连接。
            MessageConsumer consumer = session.createConsumer(queue);
            consumer.setMessageListener(messageListener);
        }

        logger.info("amqp  is started successfully, and will exit after server shutdown ");
    }

    private MessageListener messageListener = message -> {
        try {
            //异步处理收到的消息，确保onMessage函数里没有耗时逻辑
            executorService.submit(() -> processMessage(message));
        } catch (Exception e) {
            logger.error("submit task occurs exception ", e);
        }
    };

    /**
     * 在这里处理您收到消息后的具体业务逻辑。
     */
    private void processMessage(Message message) {
        try {
            byte[] body = message.getBody(byte[].class);
            String content = new String(body);
            String topic = message.getStringProperty("topic");
            String messageId = message.getStringProperty("messageId");
            logger.info("receive message"
                    + ",\n topic = " + topic
                    + ",\n messageId = " + messageId
                    + ",\n content = " + content);
            } catch (Exception e) {
            logger.error("processMessage occurs error ", e);
        }
    }

    private JmsConnectionListener myJmsConnectionListener = new JmsConnectionListener() {
        /**
         * 连接成功建立。
         */
        @Override
        public void onConnectionEstablished(URI remoteURI) {
            logger.info("onConnectionEstablished, remoteUri:{}", remoteURI);
        }

        /**
         * 尝试过最大重试次数之后，最终连接失败。
         */
        @Override
        public void onConnectionFailure(Throwable error) {
            logger.error("onConnectionFailure, {}", error.getMessage());
        }

        /**
         * 连接中断。
         */
        @Override
        public void onConnectionInterrupted(URI remoteURI) {
            logger.info("onConnectionInterrupted, remoteUri:{}", remoteURI);
        }

        /**
         * 连接中断后又自动重连上。
         */
        @Override
        public void onConnectionRestored(URI remoteURI) {
            logger.info("onConnectionRestored, remoteUri:{}", remoteURI);
        }

        @Override
        public void onInboundMessage(JmsInboundMessageDispatch envelope) {
        }

        @Override
        public void onSessionClosed(Session session, Throwable cause) {
        }

        @Override
        public void onConsumerClosed(MessageConsumer consumer, Throwable cause) {
        }

        @Override
        public void onProducerClosed(MessageProducer producer, Throwable cause) {
        }
    };

    /**
     * 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
     */
    private static String doSign(String toSignString, String secret, String signMethod) throws Exception {
        SecretKeySpec signingKey = new SecretKeySpec(secret.getBytes(), signMethod);
        Mac mac = Mac.getInstance(signMethod);
        mac.init(signingKey);
        byte[] rawHmac = mac.doFinal(toSignString.getBytes());
        return Base64.encodeBase64String(rawHmac);
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        start();
    }
}

```

##  设备消息订阅

在接收消息之前，我们需要让设备绑定消费组列表，这样才能通过消费组去接收消息

第一：找到  **消息转发**->**服务端订阅**->**消费者组列表**

目前有一个默认的消费组

![image-20231009185842242](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20231009185842242.png)

第二：创建订阅，让产品与消费组进行关联

![image-20231009190347810](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20231009190347810.png)

- 在**服务端订阅**页面的**订阅列表**页签下，单击**创建订阅**。

- 在**创建订阅**对话框，设置参数后单击**确认**。

  | 参数         | 说明                       |
  | ------------ | -------------------------- |
  | 产品         | 选择自己的产品（智能手表） |
  | 订阅类型     | 选择**AMQP**               |
  | 消费组       | 选择**默认消费组**         |
  | 推送消息类型 | 选择**设备上报消息**       |

## 接收设备端数据

### 思路分析

![image-20231009192825229](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20231009192825229.png)

### 功能实现

修改AmqpClient类中的processMessage，方法

```java
@Resource
private DeviceDataMapper deviceDataMapper;

@Resource
private DeviceMapper deviceMapper;

/**
 * 在这里处理您收到消息后的具体业务逻辑。
 */
private void processMessage(Message message) {
    try {
        byte[] body = message.getBody(byte[].class);
        String content = new String(body);
        String topic = message.getStringProperty("topic");
        String messageId = message.getStringProperty("messageId");
        logger.info("receive message"
                + ",\n topic = " + topic
                + ",\n messageId = " + messageId
                + ",\n content = " + content);
        Content c = JSONUtil.toBean(content, Content.class);
        
        //.........
     
    } catch (Exception e) {
        logger.error("processMessage occurs error ", e);
    }
}
```





