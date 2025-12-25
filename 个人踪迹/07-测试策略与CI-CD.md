# 测试策略与 CI/CD

## 一、测试架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        测试金字塔                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌─────────┐                              │
│                        │  E2E    │  Playwright                  │
│                        │  Tests  │  (浏览器自动化)               │
│                       ┌┴─────────┴┐                             │
│                       │Integration│  @IntegrationTest           │
│                       │   Tests   │  (Testcontainers)           │
│                      ┌┴───────────┴┐                            │
│                      │  Unit Tests │  JUnit 5 + Mockito         │
│                      └─────────────┘                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 二、单元测试与集成测试

### 2.1 集成测试注解

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@ActiveProfiles("test")
@Import({TestContainerConfiguration.class, TestConfiguration.class})
@Retention(RetentionPolicy.RUNTIME)
@AutoConfigureMockMvc
public @interface IntegrationTest {
}
```

**设计亮点**:
- 自定义注解封装所有测试配置
- 使用随机端口避免冲突
- 激活 `test` Profile
- 自动配置 MockMvc

### 2.2 Testcontainers 配置

```java
@TestConfiguration(proxyBeanMethods = false)
public class TestContainerConfiguration {
    
    @Bean
    @ServiceConnection
    public PostgreSQLContainer<?> timescaledb() {
        return new PostgreSQLContainer<>(
            DockerImageName.parse("postgis/postgis:17-3.5-alpine")
                .asCompatibleSubstituteFor("postgres")
        )
        .withDatabaseName("reitti")
        .withUsername("test")
        .withPassword("test");
    }

    @Bean
    @ServiceConnection
    public RabbitMQContainer rabbitmq() {
        return new RabbitMQContainer("rabbitmq:3-management")
            .withExposedPorts(5672, 15672);
    }

    @Bean
    @ServiceConnection
    public RedisContainer redisContainer() {
        return new RedisContainer("redis:7-alpine");
    }
}
```

**关键特性**:
- `@ServiceConnection`: Spring Boot 3.1+ 自动配置连接
- PostGIS 镜像替代标准 PostgreSQL
- 容器自动启动和清理

### 2.3 测试工具类

```java
public class TestUtils {
    
    public static RawLocationPoint createLocationPoint(
            double lat, double lng, Instant timestamp) {
        return new RawLocationPoint(
            timestamp,
            new GeoPoint(lat, lng),
            10.0  // 默认精度
        );
    }
    
    public static List<RawLocationPoint> createTrajectory(
            double startLat, double startLng,
            double endLat, double endLng,
            Instant startTime, int pointCount, Duration interval) {
        List<RawLocationPoint> points = new ArrayList<>();
        
        for (int i = 0; i < pointCount; i++) {
            double progress = (double) i / (pointCount - 1);
            double lat = startLat + (endLat - startLat) * progress;
            double lng = startLng + (endLng - startLng) * progress;
            Instant time = startTime.plus(interval.multipliedBy(i));
            
            points.add(createLocationPoint(lat, lng, time));
        }
        
        return points;
    }
}
```

### 2.4 测试服务

```java
@Service
public class TestingService {
    
    private final RawLocationPointJdbcService rawLocationPointJdbcService;
    private final UserJdbcService userJdbcService;
    
    public User createTestUser(String username) {
        User user = new User(username, username, "password");
        return userJdbcService.save(user);
    }
    
    public void insertTestData(User user, List<RawLocationPoint> points) {
        rawLocationPointJdbcService.bulkInsert(user, points);
    }
    
    public void cleanupTestData(User user) {
        // 清理测试数据
        rawLocationPointJdbcService.deleteByUser(user);
        userJdbcService.delete(user);
    }
}
```

### 2.5 集成测试示例

```java
@IntegrationTest
class UnifiedLocationProcessingServiceTest {
    
    @Autowired
    private UnifiedLocationProcessingService processingService;
    
    @Autowired
    private TestingService testingService;
    
    private User testUser;
    
    @BeforeEach
    void setUp() {
        testUser = testingService.createTestUser("test-user");
    }
    
    @AfterEach
    void tearDown() {
        testingService.cleanupTestData(testUser);
    }
    
    @Test
    void shouldDetectVisitFromStationaryPoints() {
        // Given: 在同一位置停留30分钟的点
        List<RawLocationPoint> points = TestUtils.createStationaryPoints(
            52.5200, 13.4050,  // 柏林
            Instant.now().minus(1, ChronoUnit.HOURS),
            30,  // 30个点
            Duration.ofMinutes(1)
        );
        testingService.insertTestData(testUser, points);
        
        // When: 触发处理
        LocationProcessEvent event = new LocationProcessEvent(
            testUser.getUsername(),
            null,
            UUID.randomUUID().toString(),
            points.getFirst().getTimestamp(),
            points.getLast().getTimestamp()
        );
        processingService.processLocationEvent(event);
        
        // Then: 应该检测到一个访问
        List<ProcessedVisit> visits = processedVisitJdbcService
            .findByUser(testUser);
        assertThat(visits).hasSize(1);
        assertThat(visits.get(0).getDurationSeconds())
            .isGreaterThanOrEqualTo(29 * 60);
    }
    
    @Test
    void shouldDetectTripBetweenTwoVisits() {
        // Given: 两个地点之间的移动
        // ... 测试代码
    }
}
```

## 三、E2E 测试 (Playwright)

### 3.1 Playwright 配置

```javascript
// playwright.config.js
export default defineConfig({
    testDir: './tests',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: 0,
    workers: process.env.CI ? 1 : undefined,
    
    reporter: process.env.CI 
        ? [['html'], ["@midleman/github-actions-reporter"]] 
        : [["list"], ["html"]],
    
    use: {
        baseURL: 'http://localhost:8080',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ]
});
```

### 3.2 登录测试

```javascript
// tests/login.spec.js
import { expect, test } from '@playwright/test';

test.describe('Login Page Tests', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
        await page.waitForLoadState('networkidle');
        
        // 等待字体加载
        await page.waitForFunction(() => document.fonts.ready);
        
        // 处理初始设置
        if (await page.title() === 'Setup - Reitti') {
            await page.locator('#password').fill('admin');
            await page.keyboard.press('Enter');
        }
        await page.waitForLoadState('networkidle');
    });

    test('should load Login Page', async ({ page }) => {
        await expect(page).toHaveTitle('Reitti - Login');
        await expect(page.locator('#username')).toBeVisible();
        await expect(page.locator('#password')).toBeVisible();
    });

    test('should login successfully', async ({ page }) => {
        await page.locator('#username').fill('admin');
        await page.locator('#password').fill('admin');
        await page.locator('button:has-text("Login")').click();
        
        await page.waitForLoadState('networkidle');
        await expect(page.locator('.navbar .nav-link.active')).toBeVisible();
    });
});
```

### 3.3 日期选择器测试

```javascript
// tests/timeband.spec.js
test.describe('Date Picker Tests', () => {
    test('should select single date when startDate is given', async ({ page }) => {
        await page.goto('/?startDate=2018-12-30');
        
        await expect(page.locator('.date-day.range-start')).toBeVisible();
        await expect(page.locator('.date-day.range-start .day-number'))
            .toHaveText('30');
        await expect(page.locator('.date-day.range-start .month-year'))
            .toHaveText('Dec 2018');
    });

    test('should select date range', async ({ page }) => {
        await page.goto('/?startDate=2018-12-31&endDate=2019-01-01');
        
        await expect(page.locator('.date-day.range-start .day-number'))
            .toHaveText('31');
        await expect(page.locator('.date-day.range-end .day-number'))
            .toHaveText('1');
    });

    test('end date for month-selection should be last day of month', async ({ page }) => {
        await page.goto('/');
        
        // 滚轮切换到月视图
        await page.locator('#date-picker-container').hover();
        await page.mouse.wheel(0, 100);
        
        // 选择 2017年9月
        await page.getByText('2017Sep').click();
        
        await expect(page).toHaveURL(/startDate=2017-09-01&endDate=2017-09-30/);
    });

    test('should switch to auto-update mode', async ({ page }) => {
        await page.goto('/');
        
        await page.getByTitle('Enter Auto-Update Mode').click();
        await expect(page.locator('#auto-update-overlay')).toBeVisible();
        
        await page.locator('#auto-update-btn').click();
        await expect(page.locator('#auto-update-overlay')).not.toBeVisible();
    });
});
```

## 四、CI/CD 流水线

### 4.1 GitHub Actions 工作流

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 25
        uses: actions/setup-java@v4
        with:
          java-version: '25'
          distribution: 'temurin'
          cache: maven
      
      - name: Generate acknowledgments data
        run: ./scripts/generate-acknowledgments.sh
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build JAR without tests
        run: mvn compile package -DskipTests
      
      - name: Upload JAR artifact
        uses: actions/upload-artifact@v4
        with:
          name: jar-artifact
          path: staging/
          retention-days: 1

  unit-tests:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 25
        uses: actions/setup-java@v4
        with:
          java-version: '25'
          distribution: 'temurin'
          cache: maven
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Run unit tests
        run: mvn test
        env:
          DOCKER_HOST: unix:///var/run/docker.sock
          SPRING_PROFILES_ACTIVE: test,ci
      
      - name: Upload coverage reports
        uses: actions/upload-artifact@v4
        with:
          name: coverage-reports
          path: target/site/jacoco/

  e2e-tests:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      
      - name: Download JAR artifact
        uses: actions/download-artifact@v4
        with:
          name: jar-artifact
          path: staging/
      
      - name: Build docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          load: true
          tags: dedicatedcode/reitti:latest
      
      - name: Start docker-compose
        run: docker compose -f docker-compose.ci.yml up -d
        working-directory: e2e
      
      - name: Wait for app to be ready
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:8080; do sleep 2; done'
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
        working-directory: e2e
      
      - name: Run Playwright tests
        run: CI=1 npx playwright test --project=chromium --project=firefox --project=webkit
        working-directory: e2e
      
      - name: Upload test results on failure
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-test-results
          path: e2e/test-results/
```

### 4.2 E2E 测试 Docker Compose

```yaml
# e2e/docker-compose.ci.yml
services:
  reitti:
    image: dedicatedcode/reitti:latest
    ports:
      - 8080:8080
    depends_on:
      rabbitmq:
        condition: service_healthy
      postgis:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      POSTGIS_USER: reitti
      POSTGIS_PASSWORD: reitti
      POSTGIS_DB: reittidb
      POSTGIS_HOST: postgis
    volumes:
      - ./data.dump:/docker-entrypoint-initdb.d/data.dump
  
  postgis:
    image: postgis/postgis:17-3.5-alpine
    environment:
      POSTGRES_USER: reitti
      POSTGRES_PASSWORD: reitti
      POSTGRES_DB: reittidb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U reitti -d reittidb"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  rabbitmq:
    image: rabbitmq:3-management-alpine
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_port_connectivity"]
      interval: 30s
      timeout: 10s
      retries: 5
  
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 4.3 测试数据准备

```
e2e/data.dump  # 预置的测试数据
```

## 五、代码覆盖率

### 5.1 JaCoCo 配置

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.14</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### 5.2 覆盖率报告

```
target/site/jacoco/
├── index.html           # 覆盖率报告首页
├── jacoco.xml           # XML 格式报告
└── jacoco-sessions.html # 测试会话信息
```

## 六、学习要点

### 6.1 测试策略

1. **集成测试优先**: 项目约定优先使用 `@IntegrationTest`
2. **真实依赖**: 使用 Testcontainers 而非 Mock
3. **E2E 覆盖**: 关键用户流程使用 Playwright 测试
4. **多浏览器**: E2E 测试覆盖 Chrome、Firefox、Safari

### 6.2 CI/CD 最佳实践

1. **并行执行**: 构建、单元测试、E2E 测试并行
2. **缓存优化**: Maven、npm、Docker 层缓存
3. **失败保留**: 测试失败时保留截图和视频
4. **健康检查**: 等待服务就绪后再运行测试

### 6.3 Testcontainers 技巧

1. **@ServiceConnection**: 自动配置数据源
2. **镜像替换**: PostGIS 替代标准 PostgreSQL
3. **容器复用**: 减少测试启动时间
4. **健康检查**: 确保容器完全就绪

### 6.4 Playwright 技巧

1. **等待策略**: `networkidle` 确保页面完全加载
2. **字体等待**: 确保渲染一致性
3. **失败重试**: 配置重试策略
4. **多项目**: 同时测试多个浏览器
