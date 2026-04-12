## 调研报告：WebApp 全方位自动化测试方案

### 一、你已经有的 Skill（可直接使用）

你的 Claude Code 环境已安装了这些相关 Skill：

| Skill                                | 说明                                                         | 适合场景                                   |
| ------------------------------------ | ------------------------------------------------------------ | ------------------------------------------ |
| **`webapp-testing`**                 | [AutumnsGrove/ClaudeSkills](https://github.com/AutumnsGrove/ClaudeSkills) 的 E2E 测试模块，基于 Playwright | 浏览器自动化、表单测试、视觉回归、API Mock |
| **`e2e-testing-patterns`**           | Playwright + Cypress E2E 测试模式库                          | 测试架构设计、最佳实践                     |
| **`verification-before-completion`** | 完成前自动验证                                               | 防止交付时遗漏                             |
| **`test-fixing`**                    | 自动修复失败测试                                             | 批量跑完测试后修                           |

### 二、高价值 GitHub 项目（推荐）

#### A. AI + Playwright 测试报告（最贴合你的需求）

| 项目                                                         | Stars | 说明                                                         |
| ------------------------------------------------------------ | ----- | ------------------------------------------------------------ |
| [**playwright-ai-reporter**](https://github.com/deepakkamboj/playwright-ai-reporter) | -     | **企业级**：AI 分析失败原因 + 自动生成 Bug 报告 + auto-healing PR + HTML 仪表盘。支持 Claude/GPT/Gemini |
| [**autospec-ai/playwright**](https://github.com/autospec-ai/playwright) | -     | GitHub Action，每次 commit 自动 diff 分析 → 生成 Playwright 测试 → 提 PR。支持 Claude |
| [**ai-web-testing-agent**](https://github.com/AkshayG999/ai-web-testing-agent) | -     | AI 自主扫描网站 → 自动生成 E2E 测试 → 执行 → 输出报告        |

#### B. AI Agent 全自动测试

| 项目                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [**WebProber**](https://arxiv.org/html/2509.05197v1) (学术论文) | AI Agent 给一个 URL → 自动模拟用户操作 → 发现 Bug → 生成可读报告。120 个网站案例发现 29 个传统工具遗漏的问题 |
| [**claude-code-test-runner**](https://github.com/firstloophq/claude-code-test-runner) | 用自然语言写测试步骤 → Claude Code 自动执行浏览器操作 → 输出结果 |
| [**browser-use**](https://github.com/browser-use/browser-use) | 让 AI Agent 像人一样操作浏览器（Claude Code 可直接调用）     |
| [**webqa-agent**](https://github.com/MigoXLab/webqa-agent)   | 自主 Web QA Agent，支持 Generate 模式（生成测试）和 Run 模式（执行测试） |

#### C. Claude Code 浏览器 Skill

| 项目                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [**lackeyjb/playwright-skill**](https://github.com/lackeyjb/playwright-skill) | Claude Code Skill：让 Claude 写 Playwright 代码 → 执行 → 返回结果+截图 |
| [**smartlabsAT/claude-playwright**](https://github.com/smartlabsAT/claude-playwright) | MCP Server，26+ 浏览器自动化工具，Claude Code 直接调用       |

### 三、社区讨论亮点

| 来源                                                         | 要点                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [LinuxDo: AI 自动化测试方案](https://linux.do/t/topic/1462003) | Claude Code 跑自动化测试的实战经验，提到 Token 消耗和测试质量问题 |
| [Medium: Playwright AI Agents 实测一周](https://scrolltest.medium.com/playwright-ai-agents-wrote-my-test-suite-for-a-week-heres-the-honest-report-card-1186850e2b01) | 在真实 SaaS 项目上用 AI Agent 写了一周测试，Planner 拿 A，Generator 拿 B- |
| [Medium: AI Agent 跑浏览器测试过夜](https://medium.com/@tboryss/what-happens-when-an-ai-agent-iterates-on-browser-tests-overnight-06fba52ce3e0) | 给 AI Agent 一个测试问题，2 小时跑了 24 次实验迭代           |

### 四、推荐方案

结合你的项目（SmartLock CRM，Umi Max + .NET 9），我建议分两步走：

**第一步：用已有 Skill 快速启动**



```
/webapp-testing  →  对 Admin 前端做 E2E 浏览器测试
```

你已经装了这个 Skill，可以直接用。

**第二步：引入 `playwright-ai-reporter` 产出专业报告**

- 安装后，每次测试自动生成 HTML 仪表盘 + AI 分析失败原因 + 修复建议
- 支持 Claude API 做智能分析

**第三步（可选）：引入 `autospec-ai` 做 CI/CD 级自动测试**

- 每次 git push 自动 diff 分析 → 生成新测试 → PR 提交