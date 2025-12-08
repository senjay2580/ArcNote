# ==WEB-SPIDER==

# Request & BeautifulSoup(静态网页 简单结构数据)

<span style="color:#CC0000;">**<span style="font-size:1.5em;">结合Pandas 导入导出数据</span>**</span>



![image-20250417221626357](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250417221626357.png)





## 一、`requests` 库核心 API

### 1. **发送 HTTP 请求**

- **GET 请求**

  ```py
  response = requests.get(
      url,                 # 目标 URL
      params=None,         # 字典类型，附加 URL 参数（自动编码）
      headers=None,        # 字典类型，设置请求头（如 User-Agent）
      cookies=None,        # 字典类型，设置 Cookie
      timeout=10,          # 超时时间（秒）
      allow_redirects=True # 是否允许重定向
  )
  // 一般json格式 和py中字典格式一样！！
  params = {
      'page': 1,                  # 数字 → 自动转为字符串 '1'
      'q': 'python爬虫',          # 字符串（自动编码）
      'tags': ['web', 'scraping'] # 列表 → 转为 'tags=web&tags=scraping'
  }
  ```



![image-20250417221637096](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250417221637096.png)

- **POST 请求**

  

  ```py
  response = requests.post(
      url,
      data=None,    # 字典或字符串，发送表单数据（Content-Type: application/x-www-form-urlencoded）
      json=None,    # 字典，发送 JSON 数据（Content-Type: application/json）
      files=None    # 字典，上传文件（如 {'file': open('test.jpg', 'rb')}）
  )
  ```

------

### 2. **处理响应**

- **基本属性**

  ```py
  response.status_code   # 状态码（200 表示成功）
  response.text    # 响应内容（自动解码文本）
  reponse.json() 
  response.content       # 响应内容（二进制原始数据，适合下载图片/文件）
  response.headers       # 响应头（字典格式）
  response.cookies       # 服务器返回的 Cookie（RequestsCookieJar 对象）
  ```

- **JSON 解析**

  ```py
  data = response.json()  # 自动解析 JSON 数据，返回字典或列表
  ```

- **编码处理**

  ```py
  response.encoding = 'utf-8'  # 手动设置编码格式（解决乱码问题）
  ```

------

### 3. **会话管理（保持登录状态）**

```py
session = requests.Session()  # 创建会话对象
session.get(url)              # 使用会话发送请求（自动保持 Cookie）
session.post(url, data={...})
```

------

### 4. **代理设置**

```py
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080'
}
response = requests.get(url, proxies=proxies)
```

------

### 5. **异常处理**

```py
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # 如果状态码不是 200，抛出 HTTPError
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```



## 编解码问题

响应头中 content-type 如果没有的话默认就是 isoXXX

**所以在py中接收的时候可以指定解码格式** 

1. **服务器声明编码错误**

- **现象**：响应头中 `Content-Type: text/html; charset=ISO-8859-1`，但实际是 UTF-8。

- **解决**：覆盖默认编码：

  

  ```py
  response.encoding = 'utf-8'  # 忽略服务器声明2. **动态编码（无响应头声明）**
  ```

- **现象**：响应头未指定 `charset`，但页面内用 `<meta>` 标签声明（如 `<meta charset="gb2312">`）。

- **解决**：使用 `apparent_encoding` 自动推测：

  

  ```py
  response.encoding = response.apparent_encoding  # 基于内容分析
  ```







------

## 二、`Beautiful Soup` 核心 API

**<span style="font-size:1.2em; color:#FF0000;">(核心还是playwright!!!语法类似)</span>**

### 1. **解析 HTML**

```py
from bs4 import BeautifulSoup
// 创建 BeautifulSoup实例
soup = BeautifulSoup(
    html_content,      # HTML 文本（通常用 response.text 传入）
    'html.parser'      # 解析器（可选 'lxml' 或 'html5lib'，需安装）
)
```



soup是 处理过的html 内容和html一样 但是可以通过BeautifulSoup的API 进行识别和处理 

**而没有处理过的html 不行**



------

### 2. **查找元素**

- **按标签名查找**

  ```py
  soup.find('div')           # 返回第一个匹配的 <div> 标签
  soup.find('a',id/class_='') # 细粒化
  soup.find_all('a')[]        # 返回所有 <a> 标签（列表） 【】 随机存取访问
  ```

- **按属性查找**

  

  ```py
  soup.find(id='header')     # 查找 id="header" 的标签
  soup.find(class_='title')  # 查找 class="title" 的标签（注意下划线）cause 和py关键字冲突
  soup.find(attrs={'data-id': '123'})  # 按自定义属性查找
  ```

- **CSS 选择器**

  

  ```py
  soup.select('div.item')        # 所有 class="item" 的 <div> 标签
  soup.select('#main > ul li')   # 层级选择器
  ```

------

![image-20250417223445886](https://cdn.jsdelivr.net/gh/kasahuki/os_test@main/img/image-20250417223445886.png)







### 3. **提取数据**

- **文本内容**

  

  ```py
  tag.text          # 获取标签内所有文本（包含子标签文本）
  tag.get_text()    # 同上
  tag.string        # 仅获取标签的直接文本（无子标签）
  ```

- **属性值**

  

  ```py
  tag['href']       # 获取 href 属性值
  tag.get('href')   # 安全获取属性值（属性不存在返回 None）
  
  # 选择同时具有 href 和 class 的 <a> 标签
  links = soup.select('a[href][class]')
  for link in links:
      print(link)
  
  # 选择 href="https://example.com" 且 class="external" 的 <a>
  specific_link = soup.select('a[href="https://example.com"][class="external"]')
  print(specific_link)
  ```

- **遍历节点**

  

  ```py
  tag.parent        # 父节点
  tag.children      # 子节点（生成器）
  tag.next_sibling  # 下一个同级节点
  ```

------

### 4. **高级操作**

- **过滤结果**

  

  ```py
  soup.find_all('a', limit=5)         # 限制返回数量
  soup.find_all('div', class_='item') # 按多个条件过滤
  ```

- **==正则表达式==匹配**

  

  ```py
  import re
  soup.find_all(text=re.compile('Python'))  # 查找包含 "Python" 的文本
  ```

------

## 三、完整爬虫示例



```py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

def scrape_page(base_url, page, headers):
    """爬取单个页面，返回链接列表"""
    # 构造分页URL（根据实际网站的分页规则调整）
    url = f"{base_url}?page={page}"  # 示例：假设分页参数是 ?page=N
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        soup = BeautifulSoup(response.text, 'html.parser')
        
        page_links = []
        for a in soup.select('a[href]'):
            href = a.get('href')
            absolute_url = urljoin(base_url, href)  # 处理相对路径
            if absolute_url.startswith('http'):
                page_links.append({
                    "page": page,
                    "url": absolute_url,
                    "text": a.text.strip()  # 链接文本
                })
        print(f"第 {page} 页提取到 {len(page_links)} 个链接")
        return page_links
    except requests.exceptions.RequestException as e:
        print(f"第 {page} 页请求失败: {e}")
        return []

def main():
    base_url = 'https://example.com'  # 替换为你的目标网站
    headers = {'User-Agent': 'Mozilla/5.0'}
    max_pages = 5  # 最大爬取页数（根据实际调整或设置为自动检测）
    all_links = []

    # 分页循环爬取
    for page in range(1, max_pages + 1):
        page_links = scrape_page(base_url, page, headers)
        if not page_links:  # 如果当前页无数据，提前终止
            print(f"第 {page} 页无数据，停止爬取")
            break
        all_links.extend(page_links)
        time.sleep(1)  # 避免频繁请求，添加延时

    # 使用Pandas导出数据
    if all_links:
        df = pd.DataFrame(all_links)
        df.to_csv('links.csv', index=False)  # 导出为CSV
        print(f"总共提取到 {len(df)} 个链接，已保存到 links.csv")
    else:
        print("未提取到任何链接")

if __name__ == "__main__":
    main()
```



---





# ==PlayWright==(自动化测试 动态网页)

# 快速上手



`Playwright` 是微软开发的 `Web应用` 的 `自动化测试框架` 。

它和另外一个 web自动化框架 `Selenium` 有 什么区别呢？



区别一：

Selenium 只提供了 Web 自动化功能， 如果你要做自动化测试，需要结合其它自动化测试框架

而 Playwright 是面向自动化测试的，除了Web自动化功能，它也包含了自动化测试的功能框架；



区别二：

两者的自动化原理有些差别，如下图所示，详见视频讲解

![image](https://www.byhy.net/cdn2/imgs/api/tut_20231105181519_81.png)

## 安装

Playwright 也支持多种语言开发，比如 JavaScript/TypeScript， Python， Java， C#

本教程 使用的是 Python语言

### 安装 playwright 客户端库

执行 `pip install playwright`



### 安装 浏览器

playwright 这个项目默认使用自己编译好的几种浏览器，比如 `chromium， firefox， webkit`

这些浏览器是通过各自的开源项目编译出来的。

和我们下载安装的 `Chrome，Firefox，Safri` 这些品牌浏览器（stock browser）的区别，[请看这里](https://stackoverflow.com/q/62184117/2602410)



playwright 每个版本都绑定 自编译浏览器的某个版本， 可以通过 [官方Release Note](https://playwright.dev/python/docs/release-notes) 看到对应关系



安装很简单，执行 `playwright install` 即可，

会出现如下浏览器下载界面



如果你只需要自动化一种浏览器，可以在参数中指定，比如 `playwright install chromium`



当然 playwright 也可以自动化 已经安装好的品牌浏览器，比如Chrome, Edge, Firefox等，后文会有讲解

品牌浏览器往往会自动更新，如果使用Selenium自动化，就需要不断下载新的驱动。

playwright使用自编译浏览器不会自动更新，从而避免驱动和浏览器不匹配的问题。

当然，如果你只是想测试和品牌浏览器的兼容性，就无需上述下载了。

## 简单示例

对照下面这段代码，观看视频讲解

```python
from playwright.sync_api import sync_playwright

input('1....')
# 启动 playwright driver 进程
p = sync_playwright().start()

input('2....')
# 启动浏览器，返回 Browser 类型对象
browser = p.chromium.launch(headless=False)

# 创建新页面，返回 Page 类型对象
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
print(page.title()) # 打印网页标题栏

# 输入通讯，点击查询。这是定位与操作，是自动化重点，后文详细讲解
page.locator('#kw').fill('通讯')  # 输入通讯
page.locator('#go').click()      # 点击查询

# 打印所有搜索内容
lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())

input('3....')
# 关闭浏览器
browser.close()
input('4....')
# 关闭 playwright driver 进程
p.stop()
```



可以这样换一种浏览器，

```python
# 启动firefox浏览器
browser = p.firefox.launch(headless=False)

# 启动webkit浏览器
browser = p.webkit.launch(headless=False)
```



可以通过参数 `executable_path` 指定使用安装的其它浏览器

```python
# 加上 executable_path参数
browser = p.chromium.launch(headless=False,
  executable_path='c:\Program Files\Google\Chrome\Application\chrome.exe')
```



可以使用 `with as` 会话管理，我们的代码简化，不需要调用 `start()` 和 `stop()`

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
    print(page.title())
    page.locator('#kw').fill('通讯\n')
    page.locator('#go').click()
    # 打印所有搜索内容
    lcs = page.locator(".result-item").all()
    for lc in lcs:
        print(lc.inner_text())
    browser.close()
```

## 界面等待

上面的代码，大家发现不能打印出股票搜索的结果，

原因是：点击查询后，立即就去检查搜索结果了，这时，界面上还没有呈现结果，所以返回的是空结果

需要等待一段时间，比如2秒。



但是目前，我们不能在Playwright中使用 time.sleep 进行等待。

因为Playwright底层使用的是异步的python库进行各种事件处理，time.sleep 会破坏异步框架的处理逻辑。

可以使用 Page 对象的 `wait_for_timeout` 方法达到等待效果，单位是 `毫秒`

```
page.wait_for_timeout(1000)
```

## 自动化代码助手

Playwright 内置了 `代码助手` 的功能，可以帮我们产生 自动化代码

输入如下命令，即可启动代码助手

```
playwright codegen
```



注意这个只能作为助手，它主要是记录人对页面的输入。

并不能取代人自己写代码，特别是那些 `获取页面上信息` 的代码

比如，这个打印标题栏，就没法自动化生成

```
print(page.title())
```



还有这些，获取所有搜索内容 的代码

```
# 打印所有搜索内容
lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())
```

## 跟踪功能

Playwright 有个特色功能： 跟踪（tracing）

启用跟踪功能后， 可以在执行自动化后，通过记录的跟踪数据文件， 回看自动化过程中的每个细节。



下面的的代码进行了自动化搜索股票，并打开跟踪功能，保存 跟踪数据文件 为 `trace.zip`。

```
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)

# 创建 BrowserContext对象
context = browser.new_context()
# 启动跟踪功能
context.tracing.start(snapshots=True, sources=True, screenshots=True)

page = context.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")

# 搜索名称中包含 通讯 的股票
page.locator('#kw').fill('通讯') 
page.locator('#go').click()

page.wait_for_timeout(1000) # 等待1秒

lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())

# 搜索名称中包含 软件 的股票
page.locator('#kw').fill('软件')  
page.locator('#go').click()    

page.wait_for_timeout(1000) # 等待1秒

lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())

# 结束跟踪
context.tracing.stop(path="trace.zip")

browser.close()
p.stop()
```



执行完以后，我们发现，当前工作目录下面多了 trace.zip 这个跟踪数据文件。

怎么查看这个跟踪文件呢？有2种方法：

- 直接访问 [trace.playwright.dev](https://trace.playwright.dev/) 这个网站，上传 跟踪文件
- 执行命令 `playwright show-trace trace.zip`



---

# ==CSS选择器 定位方法==

[CSS 选择器参考手册](http://www.w3school.com.cn/cssref/css_selectors.asp)

## 定位元素的重要性

前面这段代码

```
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")

# 输入通讯，点击查询
page.locator('#kw').fill('通讯')
page.locator('#go').click() 

page.wait_for_timeout(1000)

# 打印所有搜索内容
lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())
```

其中， `输入通讯，点击查询` 对应两行代码，分别进行了web界面元素的 `定位` 和 `操作`



web界面自动化，要对界面进行 `操作` ，首先需要 `定位` 界面元素。

就是 先告诉浏览器，你要操作 `哪个` 界面元素， 让它找到你要操作的界面元素。

我们必须要让浏览器 **先定位找到元素，然后，才能操作元素**。



相对来说，定位元素比后续的操作更难一些，

因为常见的操作并不是很多，而且就是一些固定的调用，比较容易理解。

比如

- 点击元素， `click()` 方法
- 元素内输入文本， `fill()` 方法
- 获取元素内部文本， `inner_text()` 方法



怎么找元素呢？就是告诉浏览器，你要操作的这个 web 元素的 `特征` 。

就是告诉浏览器，这个元素它有什么与众不同的地方，可以让浏览器一下子找到它。

元素的特征怎么查看？

可以使用浏览器的 `开发者工具栏` 帮我们查看、选择 web 元素。



请大家用浏览器访问 [这个网址](https://www.byhy.net/cdn2/files/selenium/stock1.html) ，

按F12后，点击 `Elements` 标签，即可查看页面对应的HTML 元素，

对照视频讲解，了解一下 `html元素/下级元素/上级元素/名称/属性/id属性/class属性` 的概念



HTML网页元素特征定位，最典型的就是 `CSS Selector` 定位方法

## CSS Selector 定位原理

HTML中经常要 为 某些元素 指定 **显示效果**，比如 前景文字颜色是红色， 背景颜色是黑色， 字体是微软雅黑等。

那么CSS必须告诉浏览器：要 **选择哪些元素** ， 来使用这样的显示风格。

比如 ，[点击这里，打开下图对应网页](https://www.byhy.net/cdn2/files/selenium/sample1.html)，为什么 `狮子/老虎/山羊` 会显示为红色呢？

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_62668791-c36b6c00-b9bf-11e9-8196-8df5c8ffd890.png)

因为蓝色框里面用css 样式，指定了class 值为animal的元素，要显示为红色。

其中 蓝色框里面的 .animal 就是 CSS Selector ，或者说 CSS 选择器。

CSS Selector 语法就是用来选择元素的。

既然 CSS Selector 语法 天生就是浏览器用来选择元素的， Playwright 自然就可以使用它用在自动化中，去选择要操作的元素了。



只要 CSS Selector 的语法是正确的， Playwright 就可以选择到该元素。

CSS Selector 非常强大，学习 Playwright Web自动化一定要学习 CSS Selector

## Locator 对象

Playwright 中，根据 CSS Selector 选择元素，就是使用 [Locator](https://playwright.dev/python/docs/api/class-locator) 类型的对象

比如，前文中， Page 对象的 locator方法就会创建一个 `Locator` 类型对象，参数就可以是 CSS Selector 表达式

```python
page.locator('#kw').fill('通讯')
page.locator('#go').click() 
```

Page对象的 locator 定位到的如果是唯一的 html元素，就可以调用 Locator 对象的 方法，比如 `fill` , `click` , `inner_text` 等等对元素进行操作了。

具体使用方法见下文

## 根据 tag名、id、class 选择元素



CSS Selector 可以根据 `tag名` 、 `id 属性` 和 `class属性` 来 选择元素，

根据 tag名 选择元素的 CSS Selector 语法非常简单，直接写上tag名即可，

比如 要选择 所有的tag名为div的元素，就可以是这样

```python
locators = page.locator('div').all()
```

然后可以这样，打印所有的tag名为div的元素的内部可见文本

```python
for one in locators:
    print(one.inner_text())
```



要获取 所有的tag名为div的元素的内部可见文本，也可以直接调用 `all_inner_texts`

```python
texts = page.locator('div').all_inner_texts()
```



注意，如果 locator调用 `匹配的结果是多个元素` ， 调用 `针对单个元素的方法` ，比如 `inner_text` ，会有错误抛出：

```python
page.locator('div').inner_text()
```



------



根据id属性 选择元素的语法是在id号前面加上一个井号： `#id值`

比如 ，有下面这样的元素：

```python
<input  type="text" id='searchtext' />
```

就可以使用 `#searchtext` 这样的 CSS Selector 来选择它。

比如，我们想在 `id 为 searchtext` 的输入框中输入文本 `你好` ，完整的Python代码如下

```python
lct = page.locator('#searchtext')
lct.fill('你好')
```



------



根据class属性 选择元素的语法是在 class 值 前面加上一个点： `.class值`

要选择 class 属性值为 animal的元素 动物，可以这样写

```python
page.locator('.animal')
```



一个 学生张三 可以定义有 `多个` 类型： `中国人` 和 `学生` 。

`中国人` 和 `学生` 都是 张三 的 类型。

元素也可以有 `多个class类型` ，多个class类型的值之间用 `空格` 隔开，比如

```python
<span class="chinese student">张三</span>
```

注意，这里 span元素 有两个class属性，分别 是 chinese 和 student， 而不是一个 名为 `chinese student` 的属性。

我们要用代码选择这个元素，可以指定任意一个class 属性值，都可以匹配到这个元素，如下

```python
page.locator('.chinese')
```

或者

```python
page.locator('.student')
```

而不能这样写

```python
page.locator('.chinese student')
```

如果要表示同时具有两个class 属性，可以这样写

```python
page.locator('.chinese.student')
```

## 验证 CSS Selector

那么我们怎么验证 CSS Selector 的语法是否正确选择了我们要选择的元素呢？

当然可以像下面这样，写出Python代码，运行看看，能否操作成功

```python
page.locator('#searchtext').fill('输入的文本')
```

如果成功，说明选择元素的语法是正确的。



但是这样做的问题就是：太麻烦了。

当我们进行自动化开发的时候，有大量选择元素的语句，都要这样一个个的验证，就非常耗时间。



由于 CSS Selector 是浏览器直接支持的，可以在浏览器 **开发者工具栏** 中验证。

比如我们使用Chrome浏览器打开 https://www.byhy.net/cdn2/files/selenium/sample1.html

按F12 打开 开发者工具栏， 点击 Elements 标签后， 同时按 Ctrl 键 和 F 键， 就会出现下图箭头处的 搜索框

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_38160687-1fe71db4-34f4-11e8-81e7-b65b5edd5e69.png)

我们可以在里面输入任何 CSS Selector 表达式 ，如果能选择到元素， 右边的的红色方框里面就会显示出类似 `2 of 3` 这样的内容。

```python
of 后面` 的数字表示这样的表达式 `总共选择到几个元素
of 前面` 的数字表示当前黄色高亮显示的是 `其中第几个元素
```

上图中的 `2 of 3` 就是指当前的 选择语法， 在当前网页上共选择到 3 个元素， 目前高亮显示的是第2个。

如果我们输入 `.plant` 就会发现，可以选择到3个元素

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_38160817-d286d148-34f5-11e8-8488-db5bf83bc7f3.png)

## 匹配多个元素

前面已经说， 如果一个 locator表达式匹配多个元素，要获取所有的元素对应的 locator 对象，使用 `all方法`

```python
locators = page.locator('.plant').all()
```



有时，我们只需要得到某种表达式对应的元素数量 ，可以使用 `count方法`，如下

```python
count = page.locator('.plant').count()
```

返回结果就是匹配的元素数量。 可以根据返回结果是否为0 判断元素是否存在



有时，我们只需要得到某种表达式对应的第一个，或者最后一个元素。

可以使用 `first` 和 `last` 属性 ， 如下

```python
lct = page.locator('.plant')
print(lct.first.inner_text(), lct.last.inner_text())
```

也可以，通过 `nth` 方法，获取指定次序的元素，参数0表达第一个， 1 表示第2个，

比如

```python
lct = page.locator('.plant')
print(lct.nth(1).inner_text())
```

## 元素内部定位

前面都是通过 `Page` 对象调用的 locator 方法， 定位的范围是整个网页。

如果我们想在某个元素内部定位，可以通过 `Locator` 对象 调用 locator 方法。

比如

```python
lct = page.locator('#bottom')

# 在 #bottom 对应元素的范围内 寻找标签名为 span 的元素。
eles = lct.locator('span').all()
for e in eles:
    print(e.inner_text())
```

## 选择 子元素 和 后代元素

HTML中， 元素 内部可以 **包含其他元素**， 比如 下面的 HTML片段

```python
<div id='container'>

    <div id='layer1'>
        <div id='inner11'>
            <span>内层11</span>
        </div>
        <div id='inner12'>
            <span>内层12</span>
        </div>
    </div>

    <div id='layer2'>
        <div id='inner21'>
            <span>内层21</span>
        </div>
    </div>

</div>
```

下面的一段话有些绕口， 请 大家细心 阅读：

id 为 `container` 的div元素 包含了 id 为 `layer1` 和 `layer2` 的两个div元素。

这种包含是直接包含， 中间没有其他的层次的元素了。 所以 id 为 `layer1` 和 `layer2` 的两个div元素 是 id 为 `container` 的div元素 的 **直接子元素**

而 id 为 `layer1` 的div元素 又包含了 id 为 `inner11` 和 `inner12` 的两个div元素。 中间没有其他层次的元素，所以这种包含关系也是 **直接子元素** 关系

id 为 `layer2` 的div元素 又包含了 id 为 `inner21` 这个div元素。 这种包含关系也是 **直接子元素** 关系



而对于 id 为 `container` 的div元素来说， id 为 `inner11` 、`inner12` 、`inner22` 的元素 和 两个 `span类型的元素` 都不是 它的直接子元素， 因为中间隔了 几层。

虽然不是直接子元素， 但是 它们还是在 `container` 的内部， 可以称之为它 的 **后代元素**

后代元素也包括了直接子元素， 比如 id 为 `layer1` 和 `layer2` 的两个div元素 也可以说 是 id 为 `container` 的div元素 的 **直接子元素，同时也是后代子元素**



如果 `元素2` 是 `元素1` 的 直接子元素， CSS Selector 选择子元素的语法是这样的

```python
元素1 > 元素2
```

中间用一个大于号 （我们可以理解为箭头号）

注意，最终选择的元素是 **元素2**， 并且要求这个 **元素2** 是 **元素1** 的直接子元素



也支持更多层级的选择， 比如

```python
元素1 > 元素2 > 元素3 > 元素4
```

就是选择 `元素1` 里面的子元素 `元素2` 里面的子元素 `元素3` 里面的子元素 `元素4` ， 最终选择的元素是 **元素4**





如果 `元素2` 是 `元素1` 的 后代元素， CSS Selector 选择后代元素的语法是这样的

```python
元素1   元素2
```

中间是一个或者多个空格隔开

最终选择的元素是 **元素2** ， 并且要求这个 **元素2** 是 **元素1** 的后代元素。


也支持更多层级的选择， 比如

```python
元素1   元素2   元素3  元素4
```

最终选择的元素是 **元素4**



## 根据属性选择



[点击这里，边看视频讲解，边学习以下内容](https://www.bilibili.com/video/BV1Z4411o7TA?p=14)



id、class 都是web元素的 `属性` ，因为它们是很常用的属性，所以css选择器专门提供了根据 id、class 选择的语法。

那么其他的属性呢？

比如

```python
<a href="http://www.miitbeian.gov.cn">苏ICP备88885574号</a>
```

里面根据 href选择，可以用css 选择器吗？

当然可以！

css 选择器支持通过任何属性来选择元素，语法是用一个方括号 `[]` 。

比如要选择上面的a元素，就可以使用 `[href="http://www.miitbeian.gov.cn"]` 。

这个表达式的意思是，选择 属性href值为 `http://www.miitbeian.gov.cn` 的元素。

完整代码如下

```python
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False, slow_mo=50)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/sample1.html")

# 根据属性选择元素
element = page.locator('[href="http://www.miitbeian.gov.cn"]')
# 打印出元素文本
print(element.inner_text())
```



当然，前面可以加上标签名的限制，比如 `a[href="http://www.miitbeian.gov.cn"]` 表示 选择所有 标签名为 `a` ，且 属性 href值为 `http://www.miitbeian.gov.cn` 的元素。

属性值用单引号，双引号都可以。



根据属性选择，还可以不指定属性值，比如 `[href]` ， 表示选择 所有 具有 属性名 为href 的元素，不管它们的值是什么。



CSS 还可以选择 属性值 `包含` 某个字符串 的元素

比如， 要选择a节点，里面的href属性包含了 miitbeian 字符串，就可以这样写

```python
a[href*="miitbeian"]
```



还可以 选择 属性值 以某个字符串 `开头` 的元素

比如， 要选择a节点，里面的href属性以 http 开头 ，就可以这样写

```python
a[href^="http"]
```



还可以 选择 属性值 以某个字符串 `结尾` 的元素

比如， 要选择a节点，里面的href属性以 gov.cn 结尾 ，就可以这样写

```python
a[href$="gov.cn"]
```



如果一个元素具有多个属性

```python
<div class="misc" ctype="gun">沙漠之鹰</div>
```

CSS 选择器 可以指定 选择的元素要 同时具有多个属性的限制，像这样 `div[class=misc][ctype=gun]`

## 选择语法联合使用



[点击这里，边看视频讲解，边学习以下内容](https://www.bilibili.com/video/BV1Z4411o7TA?p=16)



CSS selector的另一个强大之处在于： 选择语法 可以 `联合使用`

比如， 我们要选择 如下网页中 html 中的元素 `版权1` 对应的 `span`

```python
<div id='bottom'>
    <div class='footer1'>
        <span class='copyright' name='cp1'>版权1</span>
        <span class='copyright' name='cp2'>版权2</span>
        <span class='copyright1' name='cp1'>版权3</span>
    </div>
    <div class='footer2'>
        <span class='copyright' name='cp1'>版权4</span>
    </div>        
</div>         
```

CSS selector 表达式 可以这样写：

```python
.footer1 > .copyright[name=cp1]
```

## 组选择



如果我们要 同时选择所有class 为 plant `和` class 为 animal 的元素。怎么办？

这种情况，css选择器可以 使用 `逗号` ，称之为 组选择 ，像这样

```python
.plant , .animal
```



再比如，我们要同时选择所有tag名为div的元素 `和` id为BYHY的元素，就可以像这样写

```python
div,#BYHY
```

对应的Playwright代码如下

```python
elements = wd.find_elements(By.CSS_SELECTOR, 'div,#BYHY')
for element in elements:
    print(element.text)
```



我们再看一个例子

打开这个网址 [请点击打开这个网址](https://www.byhy.net/cdn2/files/selenium/sample1a.html)

我们要选择所有 唐诗里面的作者和诗名， 也就是选择所有 id 为 t1 里面的 `span 和 p 元素`

我们是不是应该这样写呢？

```python
#t1 > span,p
```

不行哦，这样写的意思是 选择所有 `id 为 t1 里面的 span` 和 `所有的 p 元素`

只能这样写

```python
#t1 > span , #t1 > p
```



另外注意：组选择结果列表中，选中元素排序， 不是 组表达式的次序， 而是符合这些表达式的元素，在HTML文档中的出现的次序。

## 按次序选择子节点

[请点击打开这个网址](https://www.byhy.net/cdn2/files/selenium/sample1b.html)

对应的html如下，关键信息如下

```python
    <body>  
       <div id='t1'>
           <h3> 唐诗 </h3>
           <span>李白</span>
           <p>静夜思</p>
           <span>杜甫</span>
           <p>春夜喜雨</p>              
       </div>      

       <div id='t2'>
           <h3> 宋词 </h3>
           <span>苏轼</span>
           <p>赤壁怀古</p>
           <p>明月几时有</p>
           <p>江城子·乙卯正月二十日夜记梦</p>
           <p>蝶恋花·春景</p>
           <span>辛弃疾</span>
           <p>京口北固亭怀古</p>
           <p>青玉案·元夕</p>
           <p>西江月·夜行黄沙道中</p>
       </div>             

    </body>
```

### 父元素的第n个子节点

我们可以指定选择的元素 `是父元素的第几个子节点`

使用 `nth-child`

比如，

我们要选择 唐诗 和宋词 的第一个 作者，

也就是说 选择的是 第2个子元素，并且是span类型

所以这样可以这样写 `span:nth-child(2)` ，



如果你不加节点类型限制，直接这样写 `:nth-child(2)`

就是选择所有位置为第2个的所有元素，不管是什么类型



学员对nth-child的含义很容易产生误解，[请点击这里，观看白月黑羽给实战班学员答疑讲解 nth-child](https://www.bilibili.com/video/BV1Z4411o7TA?p=34)

### 父元素的倒数第n个子节点

也可以反过来， 选择的是父元素的 `倒数第几个子节点` ，使用 `nth-last-child`

比如：

```python
p:nth-last-child(1)
```

就是选择第倒数第1个子元素，并且是p元素

### 父元素的第几个某类型的子节点

我们可以指定选择的元素 是父元素的第几个 `某类型的` 子节点

使用 `nth-of-type`

比如，

我们要选择 唐诗 和宋词 的第一个 作者，

可以像上面那样思考：选择的是 第2个子元素，并且是span类型

所以这样可以这样写 `span:nth-child(2)` ，



还可以这样思考，选择的是 `第1个span类型` 的子元素

所以也可以这样写 `span:nth-of-type(1)`

### 父元素的倒数第几个某类型的子节点

当然也可以反过来， 选择父元素的 `倒数第几个某类型` 的子节点

使用 `nth-last-of-type`

像这样

```python
p:nth-last-of-type(2)
```

### 奇数节点和偶数节点

如果要选择的是父元素的 `偶数节点`，使用 `nth-child(even)`

比如

```python
p:nth-child(even)
```

如果要选择的是父元素的 `奇数节点`，使用 `nth-child(odd)`

```python
p:nth-child(odd)
```



如果要选择的是父元素的 `某类型偶数节点`，使用 `nth-of-type(even)`

如果要选择的是父元素的 `某类型奇数节点`，使用 `nth-of-type(odd)`

## 兄弟节点选择



[点击这里，边看视频讲解，边学习以下内容](https://www.bilibili.com/video/BV1Z4411o7TA?p=19)

### 相邻兄弟节点选择

上面的例子里面，我们要选择 唐诗 和宋词 的第一个 作者

还有一种思考方法，就是选择 h3 `后面紧跟着的兄弟节点` span。

这就是一种 相邻兄弟 关系，可以这样写 `h3 + span`

表示元素 紧跟关系的 是 `加号`

### 后续所有兄弟节点选择

如果要选择是 选择 h3 `后面所有的兄弟节点` span，可以这样写 `h3 ~ span`

---



# ==Xpath/Role/视觉 定位方法==

## Xpath 定位

XPath (XML Path Language) 是由国际标准化组织W3C指定的，用来在 XML 和 HTML 文档中选择节点的语言。



xpath的语法，在我的Selenium教程中已经有详细的讲解，大家可以[点击这里学习](https://www.byhy.net/auto/selenium/xpath_1/)。

Playwright 的 Locator 参数也可以使用 Xpath语法，比如

原来这样根据CSS selector 选择的

```python
element = page.locator('[href="http://www.miitbeian.gov.cn"]')
```

改为 Xpath 可以这样写

```python
element = page.locator('//*[@href="http://www.miitbeian.gov.cn"]')
```



## Playwright更推荐的定位

CSS 选择器定位/xpath定位，都是根据 `HTML网页元素特征` 的定位，属于开发者角度的定位。

Playwright 优先不推荐这样，它推荐从用户角度视觉呈现的定位。

因为它觉得用户角度相对比较固定，不容易变， 而 html页面写法容易变化。



但有时，有的元素，没有通过用户视觉定位的特征。

开发者角度的这种HTML网页元素特征定位 还是有其优势的，必须要学习的。



下面学习 通过用户视觉定位的方法

## 根据文本内容定位

有时我们想获取页面包含某些文字的元素， 这用 css selector 不好选择，可以使用 Page/Locator 对象的 [get_by_text](https://playwright.dev/python/docs/api/class-locator#locator-get-by-text) 方法

比如，[点击打开这个网页](https://www.byhy.net/cdn2/files/selenium/stock1.html)，

如果要获取 所有 文本内容包含 `11` 的元素，就可以这样

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")

# 根据文本内容选择所有元素
elements = page.get_by_text('11').all()

# 打印出元素文本
for ele in elements:
    print(ele.inner_text())
```

运行发现，打印结果为

```python
600111
600113
600115
```



如果，你希望包含的内容是以 `11` 结尾的，就可以使用正则表达式对象 作为参数，如下

```python
import re
elements = page.get_by_text(re.compile("11$")).all()
```



正则表达式 `11$` 表示以 `11` 结尾，通过正则表达式，我们可以进行各种复杂的基于文本模式的定位。

关于详细的 Python 正则表达式 的用法，[点击这里学习](https://www.byhy.net/py/lang/extra/regex/)。

## 根据 元素 role 定位

### ARIA Role

Playwright 支持根据 元素 `角色 role）` 定位。

这是个很让人迷糊的定位方式。

什么叫 元素的 `角色` ？



web应用现在有一种标准 称之为： `ARIA （Accessible Rich Internet Applications）`。

ARIA 根据web界面元素的用途，为这些元素定义了一套 [角色（ Role ）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles) 信息，添加到页面中，

从而 让 残疾人士，或者 普通人在 某种环境下（比如夜里，太空中），不方便使用常规方法操作应用，使用[辅助技术工具](https://www.w3.org/TR/wai-aria-1.2/#dfn-assistive-technology)，来操作web应用的。



ARIA 为web元素增加了一些 Role相关的属性定义，方便 `辅助技术工具` 识别和操作。

比如：当我们完成系统注册时，弹出提示信息，html通常会这样

```python
<div class="alert-message">
  您已成功注册，很快您将收到一封确认电子邮件
</div>
```

但是，这样写的内容不方便辅助技术识别出这是一个重要的信息，需要读给用户听。

这时，可以加上 ARIA role 属性设置，如下

```python
<div class="alert-message" role="alert">
  您已成功注册，很快您将收到一封确认电子邮件
</div>
```

因为 `role="alert"` 是 ARIA规范里面的属性， 辅助系统（比如读屏系统）会特别注意，就会侦测到，并且实时读出来。

所以，直接可以根据如下代码 定位该元素

```python
# 根据 role 定位
lc = page.get_by_role('alert')

# 打印元素文本
print(lc.inner_text())
```



html元素中，有些 特定语义元素（semantic elements）被ARIA规范认定为自身就包含 ARIA role 信息，并不需要我们明显的加上 ARIA role 属性设置，

比如

```python
<progress value="75" max="100">75 %</progress>
```

就等于隐含了如下信息

```python
<progress value="75" max="100"
  role="progressbar"
  aria-valuenow="75"
  aria-valuemax="100">75 %</div>
```

所以，直接可以根据如下代码 定位该元素

```python
# 根据 role 定位
lc = page.get_by_role('progressbar')

# 打印元素属性 value 的值
print(lc.get_attribute('value'))
```



再比如 `search` 类型的输入框，默认就有 `searchbox` role，

```python
<input type="search">
```

所以，直接可以根据如下代码 定位该元素

```python
lc = page.get_by_role('searchbox')
print(lc.fill('白月黑羽'))
```

### ARIA Attribute

ARIA规范除了可以给元素添加 `ARIA role` ，还可以添加其它 [ARIA属性（ARIA attributes）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes) ，比如

```python
<div role="heading" aria-level="1">白月黑羽标题1</div>
<div role="heading" aria-level="2">白月黑羽标题2</div>
```

`aria-level` 就是一个 ARIA 属性，表示 role 为 `heading` 时的 `等级` 信息

上面的定义，其实和下面的 html 元素 h1/h2 等价

```python
<h1>白月黑羽标题1</h1>
<h2>白月黑羽标题2</h2>
```

`h1` 隐含了 `role="heading" aria-level="1"` 属性

`h2` 隐含了 `role="heading" aria-level="2"` 属性



Playwright 对常见的 ARIA 属性 ，[有额外的参数](https://playwright.dev/python/docs/api/class-page#page-get-by-role)对应，

比如 `aria-checked/aria-disabled/aria-expanded/aria-level` 等等



上例中，h2 元素，隐含了 `role="heading" aria-level="2"`， 所以可以用下面代码定位

```python
lc = page.get_by_role('heading',level=2)
print(lc.inner_text())
```

### Accessible Name

只根据 `ARIA role` 和 `ARIA属性` 往往并不能唯一定位元素。

role定位最常见的组合是 `ARIA role` 和 [Accessible Name](https://developer.mozilla.org/en-US/docs/Glossary/Accessible_name)

因为，`Accessible Name` 就像元素的 `名字` 一样，往往可以唯一定位。

html 元素标准属性 `name` 是浏览器内部的，用户看不到，比如



```python
<a name='link2byhy' href="https://www.byhy.net">白月黑羽教程</a>
```



`Accessible Name` 不一样，它是元素界面可见的文本名，

比如上面的元素，暗含的 `Accessible Name` 值就是 `白月黑羽教程` ， 当然也暗含了 `ARIA role` 值为 `link`

所以，可以这样定位

```python
lc = page.get_by_role('link',name='白月黑羽教程')
print(lc.click())
```

上面的写法， 只要 Accessible Name 包含 参数name 的字符串内容即可，而且大小写不分， 并不需要完全一致。

所以，这样也可以定位到

```python
lc = page.get_by_role('link',name='白月黑羽')
```

如果你需要 Accessible Name 和 参数name 的内容完全一致，可以指定 `exact=True` ，如下

```python
lc = page.get_by_role('link',name='白月黑羽', exact=True)
```



name值还可以通过[正则表达式](https://www.byhy.net/py/lang/extra/regex/)，进行较复杂的匹配规则，比如

```python
lc = page.get_by_role('link',name=re.compile("^白月.*羽"))
```



那么除了html 元素 a 以外， 哪些元素是自带 Accessible Name 属性的呢？

他们的 Accessible Name 值 又是怎么确定的呢？

[w3c有个计算规则文档](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/#name_calculation)，很复杂，不容易看懂。



我们这里说一些常见的：

<a> <td> <button> Accessible Name 值 就是其内部的文本内容。



`<textarea> <input>` 这些输入框，它们的 Accessible Name 值 是和他们关联的 的文本。

比如：

```python
<label>
  <input type="checkbox" /> Subscribe
</label>
```

这个 checkbox 的 Accessible Name 却是 `Subscribe` ，应该这样定位

```python
page.get_by_role("checkbox", name="Subscribe")
```



另外，一些元素 比如 `<img>` ，它的 Accessible Name 是其html 属性 `alt` 的值

比如

```python
<img src="grape.jpg" alt="banana"/>
```

它的 Accessible Name 值为 `banana` ，role 为 `img`

### 使用 codegen 助手

Playwright 认为， 这种根据role定位是 用户 或者辅助技术 直观感知页面的方式， 应该是最优先使用的。

但是，哪些HTML元素有哪些隐含的 ARIA role 和 ARIA Attribute，对应的 Accessible Name又是什么？

规则比较复杂，新手不太容易掌握。

我们可以使用 Playwright 的代码助手 `codegen` ，

代码助手产生代码时， 能使用 role定位的，会优先使用 role 定位。

输入如下命令：

```python
playwright codegen
```

## 其它用户视觉定位

下面的这4种定位，也属于根据用户视觉上的内容定位。

可以通过代码助手产生，其实也完全可以用 css selector 定位替代，了解即可。

### 根据 元素 placeholder 定位

`input` 元素，通常都有 `placeholder` 属性，

可以使用 Page/Locator 对象的 [get_by_placeholder](https://playwright.dev/python/docs/api/class-locator#locator-get-by-placeholder) 方法，根据 `placeholder` 属性值定位。



比如

```python
<input type="text" placeholder="captcha" />
```

就可以这样定位

```python
page.get_by_placeholder('captcha',exact=True).fill('白月黑羽')
```

参数 `exact` 值为 `True` ，表示完全匹配，且区分大小写。如果值为False，就只需包含参数字符串即可，且不区分大小写。

作用类似 get_by_role 里面的 `exact` 参数

### 根据 元素关联的 label 定位

`input` 元素，通常都有关联的 label

可以使用 Page/Locator 对象的 [get_by_label](https://playwright.dev/python/docs/api/class-locator#locator-get-by-label) 方法，根据 元素关联的 label 定位。



比如

```python
  <input aria-label="Username">
  <label for="password-input">Password:</label>
  <input id="password-input">
```

就可以这样定位

```python
page.get_by_label("Username").fill("john")
page.get_by_label("Password").fill("secret")
```



`get_by_label` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

### 根据 元素的 alt text 定位

有些元素，比如 `img` 元素，通常都有 `alt` 属性

可以使用 Page/Locator 对象的 [get_by_alt_text](https://playwright.dev/python/docs/api/class-locator#locator-get-by-alt-text) 方法，根据 元素的 `alt` 属性值 定位



比如

```python
<img 
  src="https://doc.qt.io/qtforpython/_images/windows-pushbutton.png" 
  alt="qt-button">
```

就可以这样定位

```python
href = page.get_by_alt_text("qt-button").get_attribute('src')
print(href)
```



`get_by_alt_text` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

### 根据 元素 title 定位

有些元素，比如 `span`, `a` 等等，可能有 `title` 属性，当鼠标悬浮在该元素上时，可以显示title属性内在一个提示框里面

可以使用 Page/Locator 对象的 [get_by_title](https://playwright.dev/python/docs/api/class-locator#locator-get-by-title) 方法，根据 元素的 `title` 属性值 定位



比如

```python
  <a href="https://www.byhy.net" title="byhy首页">白月黑羽教程</a>
```

就可以这样定位

```python
page.get_by_title("byhy首页").click()
```



`get_by_title` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

## 缺省等待时间

Playwright 中，当我们定位元素（比如 通过locator/get_by_text 等方法）后，对元素进行操作（比如 click, fill），

如果当时根据定位条件，找不到这个元素， Playwright并不会立即抛出错误， 而是缺省等待元素时间为30秒，在30秒内如果元素出现了，就立即操作成功返回。

比如，[点击打开这个网页](https://www.byhy.net/cdn2/files/selenium/stock1.html)。

这个网页，我们输入股票名称关键字，点击搜索后， 搜索结果并不是立即返回的，而是有 一定的延时。

前面我们讲 Selenium时，发现如果在定位 id为1的元素不sleep或者设置缺省等待时间， 会报错。

但是，如下代码并没有sleep之类的等待，也没有设置缺省等待时间，为什么在 打印 id为1的元素文本时，不会报错呢？

```python
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
page.locator('#kw').fill('通讯\n')
page.locator('#go').click()
element = page.locator("[id='1']")

print(element.inner_text())
```



因为Playwright不需要我们额外设置，本来元素操作时，如果根据定位规则找不到元素，就会等待最多 30秒。



如果我们修改下面的代码

```python
print(element.inner_text())
```

改为

```python
print(element.inner_text(timeout=10 ))
```

表示等待元素出现时长修改为10毫秒，再运行，就会有错误了。



如果，我们想修改 `缺省` 等待时间， 可以使用 `BrowserContext` 对象， 如下

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False, slow_mo=50)
context = browser.new_context()
context.set_default_timeout(10) #修改缺省等待时间为10毫秒
page = context.new_page() # 通过context 创建Page对象
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
page.locator('#kw').fill('通讯\n')
page.locator('#go').click()

element = page.locator("[id='1']")
print(element.inner_text())
```

可以发现缺省等待时间修改为10毫秒，后续操作等待时间无需单独指定，都是10毫秒了。

---



# ==界面操作==

## 元素通用操作

### 获取文本内容

前面我们学过 通过 Locator对象的 [inner_text()](https://playwright.dev/python/docs/api/class-locator#locator-inner-text) 方法 可以获取元素的内部文本，

如果Locator选择到的元素是多个，可以使用 [all_inner_texts](https://playwright.dev/python/docs/api/class-locator#locator-all-inner-texts) 获取所有匹配的文本，放到列表中返回。



上面者两个方法返回的都是元素内部的 `可见` 文本。

html元素内部还可以包括不可见的文本，比如

```python
<p id="source">
  <span id='text'>看一下<br>这个内容<br>如何变化</span>
  <span style="display:none">隐藏内容</span>
</p>
```

要获取p元素内部所有内容，包括隐藏内容，可以用 Locator对象的 [text_content()](https://playwright.dev/python/docs/api/class-locator#locator-text-content) 或者 [all_text_contents()](https://playwright.dev/python/docs/api/class-locator#locator-all-text-contents) 方法 获取 `单个` 或者 `多个` 匹配对象文本

如下所示

```python
lc = page.locator("#source")
print('innerText:',   lc.inner_text())
print('--------------')
print('textContent:', lc.text_content())
```

大家可以对比一下区别

### 获取元素属性

获取元素的属性值，可以使用 Locator对象的 [get_attribute](https://playwright.dev/python/docs/api/class-locator#locator-get-attribute) 方法

### 获取元素内部Html

获取元素内部的整个html文本， 可以使用 Locator对象的 [inner_html](https://playwright.dev/python/docs/api/class-locator#locator-inner-html) 方法

### 点击

前面讲过的Locator对象的 [click](https://playwright.dev/python/docs/api/class-locator#locator-click) 方法，是 `单击` 元素



如果要 `双击` ，可以使用 [dblclick](https://playwright.dev/python/docs/api/class-locator#locator-dblclick) 方法

### 悬停

让光标悬停在某个元素上方，可以使用 Locator对象的 [hover](https://playwright.dev/python/docs/api/class-locator#locator-hover) 方法

### 等待元素可见

前面讲过，Playwright通过Locator对元素进行操作时，如果元素当前还没有出现，缺省就会等待30秒。

但是，有时我们的代码并不是要操作这个元素，而是要等待这个元素出现后，进行别的操作。

这时，可以使用 Locator对象的 [wait_for](https://playwright.dev/python/docs/api/class-locator#locator-wait-for) 方法

比如

```python
page.locator("#source").wait_for()
```

该方法有个参数 `state` ，缺省值为 `'visible'` ， 就是等待元素可见。

如果值为 `'hidden'` 就是等待该元素消失。



等待时长为全局设定的时长， 缺省为 30秒，如果要修改，可以使用参数 `timeout`。

超出时长，元素还没有出现在界面上，会抛出错误。

### 判断元素是否可见

有时，我们的自动化代码需要根据当前界面中，`是否存在某些内容` ，来决定下一步操作。

这时，可以使用 Locator对象的 [is_visible](https://playwright.dev/python/docs/api/class-locator#locator-is-visible) 方法

比如

```python
page.locator("#source").is_visible()
```



该方法不会等待元素出现，而是立即返回 True 或 False 。

## 输入框操作

### 文本框输入

单行文本框 `input` 或者 多行文本框 `textarea` 都可以使用 Locator对象的 [fill](https://playwright.dev/python/docs/api/class-locator#locator-fill) 方法进行输入

### 文本框清空

要清空 单行文本框 `input` 或者 多行文本框 `textarea` 的内容，都可以使用 Locator对象的 [clear](https://playwright.dev/python/docs/api/class-locator#locator-clear) 方法

### 获取输入框里面的文字

如果要获取输入框 `<input>` ， `<textarea>` 对应的用户输入文本内容，不能用 `inner_text()` 方法。

而是应该用 [input_value](https://playwright.dev/python/docs/api/class-locator#locator-input-value) 方法

### 文件输入框

html中 有文件类型的输入框，用于指定本地文件， 通常用于上传文件

```python
<input type="file" multiple="multiple">
```

要设置选中的文件，可以使用 Locator 对象的 [set_input_files](https://playwright.dev/python/docs/api/class-locator#locator-set-input-files) 方法。

比如

```python
# 先定位
lc = page.locator('input[type=file]')

# 单选一个文件
lc.set_input_files('d:/1.png')

# 或者 多选 文件
lc.set_input_files(['d:/1.png', 'd:/2.jpg'])
```

### radio单选/checkbox多选

[请点击打开这个网址](https://www.byhy.net/cdn2/files/selenium/test2.html)

并且按F12，观察HTML的内容



常见的选择框包括： radio框、checkbox框、select框

`radio` 是常见的 点选 元素

比如, 下面的 html：

```python
<div id="s_radio">
  <input type="radio" name="teacher" value="小江老师">小江老师<br>
  <input type="radio" name="teacher" value="小雷老师">小雷老师<br>
  <input type="radio" name="teacher" value="小凯老师" checked="checked">小凯老师
</div>
```

如果要点选 radio框， 可以使用 Locator对象的 [check](https://playwright.dev/python/docs/api/class-locator#locator-check) 方法

如果要取消选择 radio框， 可以使用 Locator对象的 [uncheck](https://playwright.dev/python/docs/api/class-locator#locator-uncheck) 方法

如果我们要判断 radio框 是否选中，可以使用 Locator对象的 [is_checked](https://playwright.dev/python/docs/api/class-locator#locator-is-checked) 方法



假设，我们对上面html中的 radio 输入框

- 先打印当前选中的老师名字
- 再选择 小雷老师

对应的代码如下

```python
# 获取当前选中的元素
lcs = page.locator('#s_radio input[name="teacher"]:checked').all()
teachers = [lc.get_attribute('value')  for lc in lcs ]
print('当前选中的是:', ' '.join(teachers))

# 确保点选 小雷老师
page.locator("#s_radio input[value='小雷老师']").check()
```



`checkbox` 是常见的 勾选 元素

比如, 下面的html：

```python
<div id="s_checkbox">
  <input type="checkbox" name="teacher" value="小江老师" checked="checked">小江老师<br>
  <input type="checkbox" name="teacher" value="小雷老师">小雷老师<br>
  <input type="checkbox" name="teacher" value="小凯老师" checked="checked">小凯老师
</div>
```

和 radio input 一样，

如果要点选 checkbox框， 可以使用 Locator对象的 [check](https://playwright.dev/python/docs/api/class-locator#locator-check) 方法

如果要取消选择 checkbox框， 可以使用 Locator对象的 [uncheck](https://playwright.dev/python/docs/api/class-locator#locator-uncheck) 方法

如果我们要判断 checkbox 框 是否选中，可以使用 Locator对象的 [is_checked](https://playwright.dev/python/docs/api/class-locator#locator-is-checked) 方法

比如, 我们要在前面面的html中

- 先打印当前选中的老师名字
- 再选择 小雷老师

对应的代码如下

```python
# 获取当前选中的元素
lcs = page.locator('#s_checkbox input[name="teacher"]:checked').all()
teachers = [lc.get_attribute('value')  for lc in lcs ]
print('当前选中的是:', ' '.join(teachers))

# 点选 小雷老师
page.locator("#s_checkbox input[value='小雷老师']").click()
```

### select元素操作

radio框及checkbox框都是input元素，只是里面的type不同而已。

select框 则是一个新的select标签，大家可以对照浏览器网页内容查看一下



要选择选项，可以使用 `select` 元素对应的 Locator对象的 [select_option](https://playwright.dev/python/docs/api/class-locator#locator-select-option) 方法

#### select单选框

对于 select单选框：

不管原来选的是什么，直接用Select方法选择即可。

例如，选择示例里面的小江老师，示例代码如下

```python
page.locator('#ss_single').select_option('小江老师')
```

这里 select_option 参数是 选项 `option` 元素 的 `value 或者 选项文本` ， 要完全匹配。



也可以使用关键字参数 `index` , `value` , `label` 指定分别根据 索引，value属性， 选项文本 进行匹配

比如

```python
# 根据 索引 选择， 从0 开始， 但是为0的时候，好像有bug
page.locator('#ss_single').select_option(index=1)

# 根据 value属性 选择
page.locator('#ss_single').select_option(value='小江老师')

# 根据 选项文本 选择
page.locator('#ss_single').select_option(label='小江老师')

# 清空所有选择
page.locator('#ss_single').select_option([])
```

#### select多选框

对于select多选框，要选中某几个选项，同样可以使用上面的方法，参数为包含多个值的列表即可

比如

```python
# 根据 value属性 或者 选项文本 多选
page.locator('#ss_multi').select_option(['小江老师', '小雷老师'])

# 根据 value属性 多选
page.locator('#ss_multi').select_option(value=['小江老师', '小雷老师'])

# 根据 选项文本 多选
page.locator('#ss_multi').select_option(label=['小江老师', '小雷老师'])

# 清空所有选择
page.locator('#ss_multi').select_option([])
```

注意，原来已经选中的选项，没有出现在 参数里面的，自动被清除选择。

#### 获取select选中选项

同样可以通过css selector 表达式 `:checked` 伪选择 获取所有选中的 select选项

比如：

```python
page.locator('#ss_multi').select_option(['小江老师','小雷老师'])

lcs = page.locator('#ss_multi option:checked').all_inner_texts()
print(lcs)
```

## 网页操作

### 打开网址/刷新/前进/后退

要 `打开网址/刷新/前进/后退` ， 可以分别调用 Page 对象的 `goto/reload/go_back/go_forward` 方法

### 获取网页Html

要 `获取整个网页对应的HTML` ， 可以调用 Page 对象的 `content` 方法

### title

要 `获取整个网页的标题栏文本` ， 可以调用 Page 对象的 `title` 方法

### set-viewport-size

要 `设置页面大小` ， 可以调用 Page 对象的 `set_viewport_size` 方法

比如

```python
page.set_viewport_size({"width": 640, "height": 480})
```

设置宽度/高度的单位是 像素 。

---



# ==frame/tab 切换，一些技巧==



## frame切换

[请大家点击这里，打开这个链接](https://www.byhy.net/cdn2/files/selenium/sample2.html)

如果我们要 选择 下图方框中 所有的 蔬菜，使用css选择，怎么写表达式？

当然，要先查看到它们的html元素特征

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_44899250-d4cde200-ad33-11e8-9abf-e1f24be6fbe3.png)

大家可能会照旧写出如下代码：

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.byhy.net/cdn2/files/selenium/sample2.html")

lcs = page.locator('.plant').all()
for lc in lcs:
    print(lc.inner_text(timeout=1000))
```

运行一下，你就会发现，运行结果打印内容为空白，说明没有选择到 class 属性值为 plant 的元素。

为什么呢？

因为仔细看，你可以发现， 这些元素是在一个叫 `iframe` 的 元素中的。

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_44899479-76edca00-ad34-11e8-9a56-cb4be10fceb5.png)

这个 iframe 元素非常的特殊， 在html语法中， `frame` 元素 或者 `iframe` 元素的内部 会包含一个 **被嵌入的** 另一份html文档。

在我们使用 Playwright 打开一个网页时， 操作范围 缺省是当前的 html ， 并不包含被嵌入的html文档里面的内容。

如果我们要 定位/操作 被嵌入的 html 文档 中的元素， 就必须 `切换操作范围` 到 被嵌入的文档中。

怎么切换呢？

使用 Page 或者 Locator 对象的 `frame_locator` 方法定位到你要操作的frame。

这个 方法会产生一个 `FrameLocator` 对象，后续的定位，就使用这个对象，在其内部进行定位。

像这样

```python
# 产生一个  FrameLocator 对象
frame = page.frame_locator("iframe[src='sample1.html']")

# 再 在其内部进行定位
lcs = frame.locator('.plant').all()
for lc in lcs:
    print(lc.inner_text(timeout=1000))
```

其中， `frame_locator` 方法的参数是 css 或者 xpath selector



## 窗口切换

在网页上操作的时候，我们经常遇到，点击一个链接 或者 按钮，就会打开一个 `新窗口` 。

[请大家点击这里，打开这个链接](https://www.byhy.net/cdn2/files/selenium/sample3.html)

在打开的网页中，点击 链接 `访问bing网站` ， 就会弹出一个新窗口，访问bing网址。

如果我们用 Playwright 写自动化程序 **在新窗口里面 打开一个新网址**， 并且去自动化操作新窗口里面的元素，会有什么问题呢？

我们可以运行如下代码验证一下

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.byhy.net/cdn2/files/selenium/sample3.html")

# 点击链接，打开新窗口
page.locator("a").click()

# 打印网页窗口标题
print(page.title())
```



运行完程序后，最后一行 打印当前窗口的标题栏 文本， 输出内容是

```python
白月黑羽测试网页3
```

问题就在于，即使新窗口打开了， 这时候，我们的 page 变量对应的 还是老窗口，自动化操作也还是在老窗口进行，



如果我们要到新的窗口里面操作，该怎么做呢？

这时，需要使用 BrowserContext 对象。如下

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()

browser = pw.chromium.launch(headless=False)

# 创建 BrowserContext 对象
context = browser.new_context()

# 通过context 创建page
page = context.new_page() 

page.goto("https://www.byhy.net/cdn2/files/selenium/sample3.html")

# 点击链接，打开新窗口
page.locator("a").click()

# 等待2秒， 不能用 time.sleep
page.wait_for_timeout(2000)

# pages属性是 所有窗口对应Page对象的列表
newPage = context.pages[1]

# 打印新网页窗口标题
print(newPage.title())

# 打印老网页窗口标题
print(page.title())
```

`BrowserContext` 对象有个 `pages` 属性，这是一个列表，里面依次为所有窗口对应Page对象。

我们就可以通过不同的page对象操作对应的不同窗口了。



如果自动化打开了很多链接窗口，不知道目标窗口的次序号，这时可以根据标题栏定位到要操作的page

那么我们就可以通过 类似下面的代码，

```python
for pg in  context.pages:
    # 得到该窗口的标题栏字符串，判断是不是我们要操作的那个窗口
    if '必应' in pg.title():
        break

print(pg.title())   
```

### 设置当前tab

如果当前界面有很多窗口，要把某个窗口作为当前活动窗口显示出来，可以调用该窗口对应的Page对象的 [bring_to_front](https://playwright.dev/python/docs/api/class-page#page-bring-to-front) 方法。

### 关闭网页窗口

前面我们学过Browser对象有close 方法，那是关闭整个浏览器。

如果只是要关闭某个网页窗口，可以调用该窗口对应的Page对象的 [close](https://playwright.dev/python/docs/api/class-page#page-close) 方法。

## 冻结界面

有些网站上面的元素， 我们鼠标放在上面，会动态弹出一些内容。

比如，百度首页的导航栏，有个 **更多** 选项

如果我们把鼠标放在上边，就会弹出 一个更多产品内容的图标页 。

如果我们要用 Playwright 自动化 点击 其中一个产品，比如 `音乐` ，就需要 F12 查看这个元素的特征。

但是 当我们的鼠标 从 `音乐` 移开， 这个 栏目就整个消失了， 就没法 查看 其对应的 HTML。

怎么办？

可以如下图所示：

![image](https://www.byhy.net/cdn2/imgs/gh/36257654_44762324-3e55c100-ab79-11e8-89af-4a744d775c45.png)



在 开发者工具栏 console 里面执行如下js代码

```python
setTimeout(function(){debugger}, 5000)
```



这句代码什么意思呢？

表示在 5000毫秒后，执行 debugger 命令

执行该命令会 浏览器会进入debug状态。 debug状态有个特性， 界面被冻住， 不管我们怎么点击界面都不会触发事件。



所以，我们可以在输入上面代码并回车 执行后， 立即 鼠标放在界面 右上角 更多产品处。

这时候，就会弹出 下面的 图标。

然后，我们仔细等待 5秒 到了以后， 界面就会因为执行了 debugger 命令而被冻住。

然后，我们就可以点击 开发者工具栏的 查看箭头， 再去 点击 `音乐` 图标 ，查看其属性了。

## 截屏

要 `整个网页` 截屏，使用 Page 对象的 [screenshot](https://playwright.dev/python/docs/api/class-page#page-screenshot) 方法。

比如

```python
# 截屏当前页面可见内容，保存到当前工作目录下的ss1.png文件中
page.screenshot(path='ss1.png')

# 截屏 完整页面，页面内容长度超过窗口高度时，包括不可见部分。
page.screenshot(path='ss1.png', full_page=True)
```



也可以只对 `某个元素的显示内容` 进行截屏，使用 Locator 对象的 [screenshot](https://playwright.dev/python/docs/api/class-locator#locator-screenshot) 方法。

比如

```python
page.locator('input[type=file]').screenshot(path='ss2.png')
```

## 拖拽

要实现拖拽功能，可以使用Page对象的 [drag_and_drop](https://playwright.dev/python/docs/api/class-page#page-drag-and-drop) 方法。

比如，对下面这段 html

```python
<span id="t1">t1</span>
<span id="t2">t2</span>


<form >
  <div id="captcha">
  </div>
  <input type="text" placeholder="captcha" />
  <button type="submit">Submit</button>
</form>
```

要选中 `span#t1` 文本内容，并且拖拽到 输入框 `[placeholder="captcha"]` 里面去，可以使用如下代码：

```python
# 选中  `span#t1`  文本内容
page.locator('#t1').select_text()

# 拖拽到 输入框  `[placeholder="captcha"]` 里面去
page.drag_and_drop('#t1', '[placeholder="captcha"]')
```

drag_and_drop 方法的：

第1个参数是被拖动元素的 css selector 或者 xpath selector ， 如果可以匹配页面多个元素，取第一个匹配到的元素

第1个参数是拖动目标元素的 css selector 或者 xpath selector， 如果可以匹配页面多个元素，取第一个匹配到的元素



如果被拖动元素的Locator对象已经产生，可以直接调用其 [drag_to](https://playwright.dev/python/docs/api/class-locator#locator-drag-to) 方法 进行拖动

上例中，代码也可以这样写

```python
# 选中  `span#t1`  文本内容
lc = page.locator('#t1')

lc.select_text()

# 拖拽到 输入框  `[placeholder="captcha"]` 里面去
lc.drag_to(page.locator('[placeholder="captcha"]'))
```

注意， drag_to 的参数是 目标元素的 Locator 对象 ， 而不是 selector 表达式字符串

## 弹出对话框

有的时候，我们经常会在操作界面的时候，出现一些弹出的对话框。

[请点击打开这个网址](https://www.byhy.net/cdn2/files/selenium/test4.html)

分别点击界面的3个按钮，你可以发现：

弹出的对话框有三种类型，分别是 `alert（警告信息）` 、 `confirm（确认信息）` 和 `prompt（提示输入）`

### Alert

Alert 弹出框，目的就是显示通知信息，只需用户看完信息后，点击 OK（确定） 就可以了。

那么，自动化的时候，代码怎么模拟用户点击 OK 按钮呢？

可以这样

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/test4.html")

# 处理 弹出对话框 的 回调函数
def handleDlg(dialog):
    # 等待1秒
    page.wait_for_timeout(1000)
    # 点击确定
    dialog.accept()
    # 打印 弹出框 提示信息
    print(dialog.message) 

# 设置弹出对话框事件回调函数
page.on("dialog", handleDlg )

# 点击 alert 按钮
page.locator('#b1').click()
```

处理函数中被回调时，会传入 [Dialog](https://playwright.dev/python/docs/api/class-dialog) 对象

这个对象的

`accept` 方法作用等同于点击确定按钮

`dismiss` 方法作用等同于点击取消按钮

`message` 属性就是对话框界面的提示信息字符串



注意：

- 注册的处理函数中一定要调用 `accept` 或者 `dismiss` 方法，让对话框消失。

否则当对话框弹出时，后续任何代码都不会执行，并且会有超时错误。

比如

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/test4.html")

# 处理 弹出对话框 的 回调函数
def handleDlg(dialog):
    print('不调用accept')

page.on("dialog", handleDlg )

#点击 alert 按钮
page.locator('#b1').click()

print('后续代码')
```

会发现，点击alert 按钮之后的后续代码不会执行

- Playwright 在界面有弹出框时，发现如果没有任何注册的处理函数，会自动点击取消

比如

```python
# 注释掉 事件回调函数
# page.on("dialog", handleDlg )

#点击 alert 按钮
page.locator('#b1').click()
print('点击1次')

page.wait_for_timeout(1000)

#点击 alert 按钮
page.locator('#b1').click()
print('点击2次')
```

会发现，对话框自动取消

### Confirm

Confirm弹出框，主要是让用户确认是否要进行某个操作。

比如：当管理员在网站上选择删除某个账号时，就可能会弹出 Confirm弹出框， 要求确认是否确定要删除。

Confirm弹出框 有两个选择供用户选择，分别是 `OK` 和 `Cancel` ， 分别代表 `确定` 和 `取消` 操作。

那么，自动化的时候，代码怎么模拟用户点击 `确定` 或者 `取消` 按钮呢？

前面说过，处理函数中被回调时，会传入 [Dialog](https://playwright.dev/python/docs/api/class-dialog) 对象

这个对象的

`accept` 方法作用等同于点击确定按钮

`dismiss` 方法作用等同于点击取消按钮



比如，前面的代码改为

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()

browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/test4.html")

def handleDlg(dialog):    
    page.wait_for_timeout(1000)
    dialog.dismiss() # 点击取消

page.on("dialog", handleDlg)

# 点击 confirm 按钮
page.locator('#b2').click()


input('....')
```

会发现打印出来的是 `取消操作`

### Prompt

出现 Prompt 弹出框 是需要用户输入一些信息，提交上去。

比如：当管理员在网站上选择给某个账号延期时，就可能会弹出 Prompt 弹出框， 要求输入延期多长时间。

怎么办呢？

[Dialog](https://playwright.dev/python/docs/api/class-dialog) 对象，这个对象的 `accept` 方法可以输入参数字符串，作为要输入的信息



比如，前面的代码改为

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/test4.html")


def handleDlg(dialog):    
    page.wait_for_timeout(1000)
    dialog.accept('你好啊') # 输入信息，并确定

page.on("dialog", handleDlg)

# 点击 confirm 按钮
page.locator('#b3').click()

input('....')
```

# ==js代码嵌入、异步爬虫==







# Pandas 使用








# ==Brower-use 使用==

