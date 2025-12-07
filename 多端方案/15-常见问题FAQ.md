# 15. 常见问题 FAQ 与 Bug 解决示例

## 15.1 环境配置问题

### 15.1.1 Flutter 环境问题

#### 问题 1：Flutter Doctor 检查失败
**现象**：运行 `flutter doctor` 出现多个错误

**根因分析**：
- Android SDK 路径配置错误
- Java 版本不匹配
- Android 许可证未接受

**解决步骤**：
```bash
# 1. 检查 Android SDK 路径
echo $ANDROID_HOME
# 如果为空，设置环境变量
export ANDROID_HOME=/path/to/android/sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# 2. 检查 Java 版本
java -version
# 确保使用 JDK 11 或更高版本

# 3. 接受 Android 许可证
flutter doctor --android-licenses

# 4. 重新检查
flutter doctor -v
```

**验收准则**：
- [ ] `flutter doctor` 显示所有项目为绿色勾号
- [ ] 能够成功创建和运行新的 Flutter 项目

**回滚方案**：
```bash
# 重置 Flutter 环境
flutter clean
flutter pub get
flutter doctor
```

#### 问题 2：依赖版本冲突
**现象**：`flutter pub get` 报版本冲突错误

**根因分析**：
- 不同包依赖同一个包的不同版本
- pubspec.yaml 中版本约束过于严格

**解决步骤**：
```yaml
# pubspec.yaml - 解决版本冲突
dependency_overrides:
  # 强制使用特定版本
  meta: ^1.9.1
  collection: ^1.17.2
  
# 或者放宽版本约束
dependencies:
  provider: ^6.0.0  # 改为 ^6.0.0 而不是 ^6.1.1
```

```bash
# 清理并重新获取依赖
flutter clean
flutter pub get
flutter pub deps  # 查看依赖树
```

### 15.1.2 网络连接问题

#### 问题 3：API 请求超时
**现象**：应用启动后无法连接到后端服务

**根因分析**：
- 网络配置错误
- 防火墙阻止连接
- 后端服务未启动

**解决步骤**：
```dart
// 1. 检查网络配置
class NetworkDiagnostic {
  static Future<void> diagnose() async {
    // 检查网络连接
    final connectivity = await Connectivity().checkConnectivity();
    print('网络状态: $connectivity');
    
    // 检查 DNS 解析
    try {
      final addresses = await InternetAddress.lookup('google.com');
      print('DNS 解析正常: ${addresses.first.address}');
    } catch (e) {
      print('DNS 解析失败: $e');
    }
    
    // 检查后端连接
    try {
      final response = await Dio().get(
        'http://your-server:8180/health',
        options: Options(
          connectTimeout: Duration(seconds: 5),
          receiveTimeout: Duration(seconds: 5),
        ),
      );
      print('后端连接正常: ${response.statusCode}');
    } catch (e) {
      print('后端连接失败: $e');
    }
  }
}
```

**验收准则**：
- [ ] 网络诊断显示所有连接正常
- [ ] 能够成功调用后端 API

## 15.2 WebSocket 连接问题

#### 问题 4：WebSocket 连接频繁断开
**现象**：WebSocket 连接建立后很快断开，无法保持稳定连接

**根因分析**：
- 网络不稳定
- 服务器端超时设置过短
- 客户端心跳机制失效

**解决步骤**：
```dart
// 1. 增强 WebSocket 连接稳定性
class RobustWebSocketService {
  WebSocketChannel? _channel;
  Timer? _heartbeatTimer;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  static const int maxReconnectAttempts = 5;
  
  Future<void> connect(String token) async {
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('ws://your-server:8090?token=$token'),
      );
      
      _channel!.stream.listen(
        _onMessage,
        onError: _onError,
        onDone: _onDone,
        cancelOnError: false,  // 重要：不要在错误时取消监听
      );
      
      _startHeartbeat();
      _reconnectAttempts = 0;
      
    } catch (e) {
      print('WebSocket 连接失败: $e');
      _scheduleReconnect();
    }
  }
  
  void _startHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(Duration(seconds: 30), (timer) {
      if (_channel != null) {
        try {
          _channel!.sink.add(jsonEncode({'type': 2}));
        } catch (e) {
          print('发送心跳失败: $e');
          _scheduleReconnect();
        }
      }
    });
  }
  
  void _onError(error) {
    print('WebSocket 错误: $error');
    _scheduleReconnect();
  }
  
  void _onDone() {
    print('WebSocket 连接关闭');
    _scheduleReconnect();
  }
  
  void _scheduleReconnect() {
    if (_reconnectAttempts >= maxReconnectAttempts) {
      print('达到最大重连次数，停止重连');
      return;
    }
    
    _heartbeatTimer?.cancel();
    _reconnectTimer?.cancel();
    
    final delay = Duration(seconds: math.pow(2, _reconnectAttempts).toInt());
    _reconnectTimer = Timer(delay, () {
      _reconnectAttempts++;
      print('尝试重连 ($_reconnectAttempts/$maxReconnectAttempts)');
      connect(_lastToken);
    });
  }
}
```

#### 问题 5：消息发送失败
**现象**：发送消息后没有收到确认，消息状态一直显示"发送中"

**根因分析**：
- WebSocket 连接已断开但未检测到
- 服务器处理消息失败
- 客户端消息格式错误

**解决步骤**：
```dart
// 1. 实现消息发送确认机制
class ReliableMessageSender {
  final Map<String, Completer<bool>> _pendingMessages = {};
  
  Future<bool> sendMessage(Map<String, dynamic> message) async {
    final messageId = message['id'] ?? DateTime.now().millisecondsSinceEpoch.toString();
    message['id'] = messageId;
    
    // 创建确认等待器
    final completer = Completer<bool>();
    _pendingMessages[messageId] = completer;
    
    try {
      // 发送消息
      _webSocketService.send(jsonEncode(message));
      
      // 等待确认或超时
      return await completer.future.timeout(
        Duration(seconds: 10),
        onTimeout: () {
          _pendingMessages.remove(messageId);
          return false;
        },
      );
    } catch (e) {
      _pendingMessages.remove(messageId);
      return false;
    }
  }
  
  void handleMessageAck(String messageId) {
    final completer = _pendingMessages.remove(messageId);
    completer?.complete(true);
  }
  
  void handleMessageError(String messageId, String error) {
    final completer = _pendingMessages.remove(messageId);
    completer?.complete(false);
  }
}
```

## 15.3 UI 渲染问题

#### 问题 6：列表滚动卡顿
**现象**：消息列表在滚动时出现明显卡顿，特别是包含图片的消息

**根因分析**：
- 图片未优化，内存占用过大
- ListView 未使用 itemExtent 或 prototypeItem
- 复杂 Widget 重建频繁

**解决步骤**：
```dart
// 1. 优化列表性能
class OptimizedMessageList extends StatelessWidget {
  final List<Message> messages;
  
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: messages.length,
      // 使用 prototypeItem 提高性能
      prototypeItem: MessageBubble(
        message: Message.prototype(),
        isCurrentUser: false,
      ),
      itemBuilder: (context, index) {
        return RepaintBoundary(  // 隔离重绘
          child: MessageBubble(
            key: ValueKey(messages[index].id),  // 稳定的 key
            message: messages[index],
            isCurrentUser: _isCurrentUser(messages[index]),
          ),
        );
      },
    );
  }
}

// 2. 优化图片加载
class OptimizedImageWidget extends StatelessWidget {
  final String imageUrl;
  final double? width;
  final double? height;
  
  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: imageUrl,
      width: width,
      height: height,
      memCacheWidth: width?.toInt(),  // 限制内存缓存尺寸
      memCacheHeight: height?.toInt(),
      placeholder: (context, url) => Container(
        width: width,
        height: height,
        color: Colors.grey[300],
        child: Icon(Icons.image),
      ),
      errorWidget: (context, url, error) => Container(
        width: width,
        height: height,
        color: Colors.grey[300],
        child: Icon(Icons.error),
      ),
    );
  }
}
```

#### 问题 7：键盘弹出时界面布局错乱
**现象**：输入消息时键盘弹出，界面元素重叠或被遮挡

**解决步骤**：
```dart
// 1. 正确处理键盘弹出
class ChatPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 重要：设置 resizeToAvoidBottomInset
      resizeToAvoidBottomInset: true,
      body: Column(
        children: [
          Expanded(
            child: MessageList(),
          ),
          // 使用 SafeArea 确保输入框不被遮挡
          SafeArea(
            child: MessageInput(),
          ),
        ],
      ),
    );
  }
}

// 2. 键盘弹出时自动滚动到底部
class MessageInput extends StatefulWidget {
  @override
  _MessageInputState createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  final _focusNode = FocusNode();
  final _scrollController = ScrollController();
  
  @override
  void initState() {
    super.initState();
    _focusNode.addListener(_onFocusChange);
  }
  
  void _onFocusChange() {
    if (_focusNode.hasFocus) {
      // 键盘弹出时滚动到底部
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }
}
```

## 15.4 数据存储问题

#### 问题 8：Hive 数据库损坏
**现象**：应用启动时崩溃，错误信息显示 Hive 数据库文件损坏

**解决步骤**：
```dart
// 1. 实现数据库恢复机制
class HiveRecoveryService {
  static Future<void> initializeWithRecovery() async {
    try {
      await Hive.initFlutter();
      await _openBoxes();
    } catch (e) {
      print('Hive 初始化失败，尝试恢复: $e');
      await _recoverDatabase();
    }
  }
  
  static Future<void> _openBoxes() async {
    await Hive.openBox<Message>('messages');
    await Hive.openBox<Contact>('contacts');
    await Hive.openBox<User>('users');
  }
  
  static Future<void> _recoverDatabase() async {
    try {
      // 1. 备份损坏的数据库
      await _backupCorruptedDatabase();
      
      // 2. 删除损坏的文件
      await _deleteCorruptedFiles();
      
      // 3. 重新初始化
      await Hive.initFlutter();
      await _openBoxes();
      
      // 4. 从服务器恢复数据
      await _restoreFromServer();
      
    } catch (e) {
      print('数据库恢复失败: $e');
      // 最后手段：完全重置
      await _resetDatabase();
    }
  }
  
  static Future<void> _backupCorruptedDatabase() async {
    final appDir = await getApplicationDocumentsDirectory();
    final backupDir = Directory('${appDir.path}/backup_${DateTime.now().millisecondsSinceEpoch}');
    await backupDir.create();
    
    // 复制损坏的文件到备份目录
    final hiveDir = Directory('${appDir.path}');
    await for (final file in hiveDir.list()) {
      if (file.path.endsWith('.hive') || file.path.endsWith('.lock')) {
        await File(file.path).copy('${backupDir.path}/${file.path.split('/').last}');
      }
    }
  }
  
  static Future<void> _deleteCorruptedFiles() async {
    final appDir = await getApplicationDocumentsDirectory();
    final hiveDir = Directory('${appDir.path}');
    
    await for (final file in hiveDir.list()) {
      if (file.path.endsWith('.hive') || file.path.endsWith('.lock')) {
        await File(file.path).delete();
      }
    }
  }
  
  static Future<void> _restoreFromServer() async {
    // 从服务器重新下载用户数据
    try {
      final userData = await ApiClient.getUserData();
      final messages = await ApiClient.getAllMessages();
      final contacts = await ApiClient.getContacts();
      
      // 保存到新的数据库
      await StorageService.saveUserData(userData);
      await StorageService.saveMessages(messages);
      await StorageService.saveContacts(contacts);
      
    } catch (e) {
      print('从服务器恢复数据失败: $e');
    }
  }
}
```

#### 问题 9：SharedPreferences 数据丢失
**现象**：用户登录状态丢失，需要重新登录

**解决步骤**：
```dart
// 1. 实现多重存储备份
class SecureStorageService {
  static Future<void> saveUserToken(String token) async {
    // 主存储：SharedPreferences
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_token', token);
    
    // 备份存储：FlutterSecureStorage
    const secureStorage = FlutterSecureStorage();
    await secureStorage.write(key: 'user_token_backup', value: token);
    
    // 第三备份：Hive
    final box = await Hive.openBox('auth_backup');
    await box.put('user_token', token);
  }
  
  static Future<String?> getUserToken() async {
    // 优先从主存储读取
    final prefs = await SharedPreferences.getInstance();
    String? token = prefs.getString('user_token');
    
    if (token != null) return token;
    
    // 从备份存储读取
    const secureStorage = FlutterSecureStorage();
    token = await secureStorage.read(key: 'user_token_backup');
    
    if (token != null) {
      // 恢复到主存储
      await prefs.setString('user_token', token);
      return token;
    }
    
    // 从第三备份读取
    try {
      final box = await Hive.openBox('auth_backup');
      token = box.get('user_token');
      
      if (token != null) {
        // 恢复到主存储
        await prefs.setString('user_token', token);
        await secureStorage.write(key: 'user_token_backup', value: token);
        return token;
      }
    } catch (e) {
      print('从 Hive 备份读取失败: $e');
    }
    
    return null;
  }
}
```

## 15.5 性能问题

#### 问题 10：内存泄漏
**现象**：应用长时间使用后内存占用持续增长，最终导致 OOM

**解决步骤**：
```dart
// 1. 实现内存监控
class MemoryLeakDetector {
  static Timer? _monitorTimer;
  static final List<int> _memoryHistory = [];
  
  static void startMonitoring() {
    _monitorTimer = Timer.periodic(Duration(seconds: 30), (timer) {
      _checkMemoryUsage();
    });
  }
  
  static void _checkMemoryUsage() {
    final currentMemory = ProcessInfo.currentRss;
    _memoryHistory.add(currentMemory);
    
    // 保留最近 20 次记录
    if (_memoryHistory.length > 20) {
      _memoryHistory.removeAt(0);
    }
    
    // 检查内存增长趋势
    if (_memoryHistory.length >= 10) {
      final recentAverage = _memoryHistory.skip(10).reduce((a, b) => a + b) / 10;
      final earlierAverage = _memoryHistory.take(10).reduce((a, b) => a + b) / 10;
      
      if (recentAverage > earlierAverage * 1.5) {
        print('⚠️ 检测到可能的内存泄漏');
        _analyzeMemoryLeaks();
      }
    }
  }
  
  static void _analyzeMemoryLeaks() {
    // 分析可能的内存泄漏源
    print('当前内存使用: ${ProcessInfo.currentRss / 1024 / 1024} MB');
    
    // 检查常见泄漏源
    _checkStreamSubscriptions();
    _checkTimers();
    _checkImageCache();
  }
  
  static void _checkImageCache() {
    final imageCache = PaintingBinding.instance.imageCache;
    print('图片缓存: ${imageCache.currentSize} / ${imageCache.maximumSize}');
    
    if (imageCache.currentSize > imageCache.maximumSize * 0.8) {
      print('清理图片缓存');
      imageCache.clear();
    }
  }
}

// 2. 正确管理资源
class ResourceManager {
  final List<StreamSubscription> _subscriptions = [];
  final List<Timer> _timers = [];
  
  void addSubscription(StreamSubscription subscription) {
    _subscriptions.add(subscription);
  }
  
  void addTimer(Timer timer) {
    _timers.add(timer);
  }
  
  void dispose() {
    for (final subscription in _subscriptions) {
      subscription.cancel();
    }
    _subscriptions.clear();
    
    for (final timer in _timers) {
      timer.cancel();
    }
    _timers.clear();
  }
}
```

## 15.6 平台特定问题

#### 问题 11：Android 后台被杀死
**现象**：应用切换到后台后被系统杀死，无法接收消息

**解决步骤**：
```dart
// 1. 实现后台保活策略
class BackgroundService {
  static Future<void> setupBackgroundTasks() async {
    // 请求忽略电池优化
    await Permission.ignoreBatteryOptimizations.request();
    
    // 设置前台服务
    await _setupForegroundService();
    
    // 注册后台任务
    await Workmanager().initialize(callbackDispatcher);
    await Workmanager().registerPeriodicTask(
      'background-sync',
      'backgroundSync',
      frequency: Duration(minutes: 15),
      constraints: Constraints(
        networkType: NetworkType.connected,
      ),
    );
  }
  
  static Future<void> _setupForegroundService() async {
    const channel = AndroidNotificationChannel(
      'background_service',
      'Background Service',
      description: 'Keep app running in background',
      importance: Importance.low,
    );
    
    await FlutterLocalNotificationsPlugin()
        .resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }
}

// 2. 后台任务回调
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    switch (task) {
      case 'backgroundSync':
        await _performBackgroundSync();
        break;
    }
    return Future.value(true);
  });
}

Future<void> _performBackgroundSync() async {
  try {
    // 同步未读消息
    final unreadMessages = await ApiClient.getUnreadMessages();
    
    // 显示通知
    for (final message in unreadMessages) {
      await _showMessageNotification(message);
    }
    
    // 更新本地数据
    await StorageService.saveMessages(unreadMessages);
    
  } catch (e) {
    print('后台同步失败: $e');
  }
}
```

#### 问题 12：iOS 推送权限被拒绝
**现象**：iOS 设备无法接收推送通知

**解决步骤**：
```dart
// 1. 优雅的权限请求流程
class IOSNotificationPermission {
  static Future<bool> requestPermission() async {
    // 检查当前权限状态
    final settings = await FirebaseMessaging.instance.getNotificationSettings();
    
    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      return true;
    }
    
    if (settings.authorizationStatus == AuthorizationStatus.denied) {
      // 权限被永久拒绝，引导用户到设置页面
      return await _showSettingsDialog();
    }
    
    // 请求权限
    final result = await FirebaseMessaging.instance.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );
    
    return result.authorizationStatus == AuthorizationStatus.authorized;
  }
  
  static Future<bool> _showSettingsDialog() async {
    return await showDialog<bool>(
      context: navigatorKey.currentContext!,
      builder: (context) => AlertDialog(
        title: Text('通知权限'),
        content: Text('需要通知权限来接收新消息，请在设置中开启通知权限。'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text('取消'),
          ),
          TextButton(
            onPressed: () async {
              Navigator.of(context).pop(true);
              await openAppSettings();
            },
            child: Text('去设置'),
          ),
        ],
      ),
    ) ?? false;
  }
}
```

## 15.7 调试技巧

#### 问题 13：难以复现的 Bug
**现象**：某些 Bug 只在特定条件下出现，难以调试

**解决步骤**：
```dart
// 1. 实现详细的日志系统
class DebugLogger {
  static final List<LogEntry> _logs = [];
  static const int maxLogs = 1000;
  
  static void log(String message, {String? tag, LogLevel level = LogLevel.info}) {
    final entry = LogEntry(
      message: message,
      tag: tag,
      level: level,
      timestamp: DateTime.now(),
      stackTrace: StackTrace.current,
    );
    
    _logs.add(entry);
    
    if (_logs.length > maxLogs) {
      _logs.removeAt(0);
    }
    
    // 输出到控制台
    print('[${level.name.toUpperCase()}] ${tag ?? 'APP'}: $message');
    
    // 严重错误立即上报
    if (level == LogLevel.error) {
      CrashReporter.recordError(message, entry.stackTrace);
    }
  }
  
  static List<LogEntry> getLogs({String? tag, LogLevel? level}) {
    return _logs.where((log) {
      if (tag != null && log.tag != tag) return false;
      if (level != null && log.level != level) return false;
      return true;
    }).toList();
  }
  
  static String exportLogs() {
    final buffer = StringBuffer();
    for (final log in _logs) {
      buffer.writeln('${log.timestamp} [${log.level.name}] ${log.tag}: ${log.message}');
    }
    return buffer.toString();
  }
}

// 2. 实现用户操作录制
class UserActionRecorder {
  static final List<UserAction> _actions = [];
  
  static void recordAction(String action, {Map<String, dynamic>? context}) {
    _actions.add(UserAction(
      action: action,
      context: context,
      timestamp: DateTime.now(),
    ));
    
    // 保持最近 100 个操作
    if (_actions.length > 100) {
      _actions.removeAt(0);
    }
  }
  
  static List<UserAction> getActionHistory() {
    return List.from(_actions);
  }
}
```

#### 问题 14：性能瓶颈定位
**现象**：应用某些操作响应缓慢，需要定位性能瓶颈

**解决步骤**：
```dart
// 1. 性能分析工具
class PerformanceProfiler {
  static final Map<String, Stopwatch> _timers = {};
  
  static void startProfile(String name) {
    _timers[name] = Stopwatch()..start();
  }
  
  static void endProfile(String name) {
    final timer = _timers[name];
    if (timer != null) {
      timer.stop();
      final duration = timer.elapsedMilliseconds;
      
      print('⏱️ $name: ${duration}ms');
      
      // 记录到性能监控
      PerformanceMonitor.recordMetric(name, duration.toDouble());
      
      _timers.remove(name);
    }
  }
  
  static T profileSync<T>(String name, T Function() operation) {
    startProfile(name);
    try {
      return operation();
    } finally {
      endProfile(name);
    }
  }
  
  static Future<T> profileAsync<T>(String name, Future<T> Function() operation) async {
    startProfile(name);
    try {
      return await operation();
    } finally {
      endProfile(name);
    }
  }
}

// 使用示例
class ChatService {
  static Future<List<Message>> loadMessages(String contactId) async {
    return await PerformanceProfiler.profileAsync(
      'load_messages_$contactId',
      () async {
        final messages = await ApiClient.getMessages(contactId);
        await StorageService.saveMessages(contactId, messages);
        return messages;
      },
    );
  }
}
```

---

**下一章节**：[16-迁移任务清单.md](./16-迁移任务清单.md) - 详细的任务分解和验收标准。
