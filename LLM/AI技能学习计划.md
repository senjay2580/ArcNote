# AI 工程师技能学习与项目实践计划

> 目标：2026届秋招，双非大三，Java后端背景，主攻 AI 应用工程方向
> 时间窗口：2026年3月 → 2026年9月（6个月）
> 核心原则：**项目驱动，边学边做，不囤课**

---

## 技能地图总览

```
LLM API 使用          ████████████  必会，基础中的基础
RAG 系统              ████████████  已有，需要深化+评估
Agent / Function Call ████████████  已有，需要强化设计能力
Prompt Engineering    ██████████    系统化补强
向量数据库            ████████      已用pgvector，补横向对比
模型微调（LoRA）      ██████        补一次完整实验
训练数据生成          ████          补基础概念+实践
LLM 评估体系          ████          重点补，项目缺失项
LangChain/LlamaIndex  ██████        了解主流框架
AI 部署与工程化       ████████      已有Docker基础，补推理服务
```

---

## 第一阶段：3月-4月（深化已有，补关键缺口）

### Week 1-2：LLM API 与 Prompt Engineering 系统化

**学什么：**
- OpenAI / Claude API 完整特性：streaming、function calling、vision、batch API
- System Prompt 设计原则：角色设定、Few-shot、CoT、输出格式控制
- Token 成本管理：tiktoken 计算、prompt 压缩技巧
- 结构化输出：JSON mode、Pydantic 模型校验

**怎么学：**
- 直接看官方文档：[OpenAI API Docs](https://platform.openai.com/docs) + [Anthropic Docs](https://docs.anthropic.com)
- 不看视频课，直接跑代码

**项目实践：**
- 在 MutiExpert 里给每个场景写一个专门优化的 System Prompt
- 实现 Prompt 版本管理（把 prompt 存数据库，支持 A/B 对比）
- 记录每次 Prompt 修改前后的效果差异

---

### Week 3-4：RAG 深化 + 评估体系

**学什么：**

**RAG 进阶技术：**
- Hybrid Search：向量检索 + BM25 关键词检索融合（RRF 算法）
- Reranker：用 Cross-Encoder 对初检结果二次排序
- Query 改写：HyDE（假设文档生成）、多查询扩展
- Chunk 策略：固定大小 vs 语义分块 vs 父子块
- Late Chunking（2024年新方法，了解原理）

**RAG 评估（最重要）：**
- Recall@K：top-K 检索里有多少包含正确答案
- Answer Relevance：生成答案和问题的相关性（用 LLM 打分）
- Faithfulness：答案是否基于检索内容，有没有幻觉
- 框架：RAGAS（Python库，直接用）

**资源：**
- [RAGAS GitHub](https://github.com/explodinggradients/ragas) — 直接看文档跑示例
- [Advanced RAG 技术综述](https://arxiv.org/abs/2312.10997) — 扫一遍了解全貌

**项目实践：**
- 在 MutiExpert 里加 Hybrid Search（pgvector 已有向量，补一个 tsvector 全文检索）
- 接入 RAGAS，对现有 RAG 做一次完整评估，记录基线数据
- 实现 Reranker（用 Cohere Rerank API 或本地 bge-reranker）
- 目标：对比优化前后 Recall@5 的数字变化

---

### Week 5-6：Agent 架构深化

**学什么：**

**Agent 核心模式：**
- ReAct（Reasoning + Acting）：思考→动作→观察循环
- Plan and Execute：先规划全部步骤，再依次执行
- Reflection：Agent 自我审查输出并迭代改进
- Multi-Agent：Orchestrator + Specialist 分工架构

**工具设计原则：**
- Tool 的描述怎么写才能让 LLM 准确选择
- 错误处理：工具失败时 Agent 如何恢复
- 状态管理：多轮对话中 Agent 的记忆设计

**框架了解（不深学，知道能干什么）：**
- LangGraph：状态机式 Agent，适合复杂流程
- Anthropic Claude Agents SDK：和你项目最相关
- AutoGen：多 Agent 对话框架

**资源：**
- [LangGraph 官方教程](https://langchain-ai.github.io/langgraph/tutorials/)
- 吴恩达 AI Agents 课（DeepLearning.AI，免费，5小时内看完）

**项目实践：**
- 把 MutiExpert 现有的 intent/router 重构为更清晰的 ReAct 循环
- 加 Agent 执行日志：记录每一步的 thinking / tool_call / result
- 实现一个 Reflection 机制：Agent 对自己的回答打分，低于阈值重试

---

### Week 7-8：向量数据库横向对比 + 工程优化

**学什么：**

**主流向量数据库对比：**
| 数据库 | 特点 | 适合场景 |
|--------|------|--------|
| pgvector（你在用） | PostgreSQL 扩展，事务支持好 | 数据量<千万，已有PG |
| Milvus | 专用向量库，高性能 | 亿级向量，高并发 |
| Qdrant | Rust编写，支持 payload 过滤 | 需要复杂过滤条件 |
| Chroma | 轻量，本地开发友好 | 原型验证 |
| Weaviate | 内置 BM25+向量混合 | 快速搭建 RAG |

**索引算法了解：**
- HNSW（分层可导航小世界图）：大多数向量库默认，了解核心思路
- IVF_FLAT：倒排索引+精确搜索，适合中等规模
- 不需要深学，能解释为什么向量搜索比暴力搜索快就够

**Embedding 模型选择：**
- OpenAI text-embedding-3-small/large
- BGE 系列（BAAI，中文效果好，可本地部署）
- text2vec-large-chinese（中文场景）
- 如何用 MTEB 排行榜选模型

**项目实践：**
- 在 MutiExpert 里把 embedding 模型抽象成可配置项（现在是硬编码的话）
- 对比 OpenAI embedding vs BGE embedding 在你场景下的检索效果
- 写一篇技术笔记：为什么选 pgvector，什么时候该换 Milvus

---

## 第二阶段：5月-6月（补微调实验，强化工程化）

### Week 9-12：模型微调实践

**学什么：**

**微调基础概念：**
- Full Fine-tuning vs LoRA vs QLoRA 的区别和适用场景
- LoRA 原理：低秩矩阵分解，为什么参数少但效果好
- 指令微调（Instruction Tuning）：数据格式 alpaca / sharegpt
- RLHF 了解即可，不需要实现

**训练数据生成：**
- 用 LLM 生成合成数据（Self-Instruct 方法）
- 数据清洗：去重、质量过滤
- 数据格式：构建 (instruction, input, output) 三元组

**实践工具：**
- LLaMA-Factory：最易用的微调框架，支持几十种模型
- Unsloth：QLoRA 加速，消费级显卡可用
- 基座模型选择：Qwen2.5-7B（中文最强开源，阿里），Llama3.1-8B

**资源：**
- [LLaMA-Factory GitHub](https://github.com/hiyouga/LLaMA-Factory) — 跟着 README 跑通
- [QLoRA 论文](https://arxiv.org/abs/2305.14314) — 看摘要和实验部分

**项目实践：**
- 用 MutiExpert 里的知识库文档生成微调数据集（文档→问答对，用 GPT-4o 生成）
- 用 LLaMA-Factory 对 Qwen2.5-7B 做 QLoRA 微调（垂直领域问答）
- 对比微调前后在你场景里的回答质量，记录数据
- 把实验过程写成 `experiments/finetune/README.md`，这是简历上的硬证明

---

### Week 13-16：AI 工程化与部署

**学什么：**

**推理服务化：**
- vLLM：高性能 LLM 推理引擎，支持 OpenAI 兼容接口
- Ollama：本地模型一键部署，开发调试用
- 如何把自己微调的模型部署成 API 服务

**工程化最佳实践：**
- 异步并发：asyncio + httpx，LLM 调用不阻塞（你项目已有，继续深化）
- 流式输出（Streaming）：SSE 实现原理和前端接入（你项目已有）
- 限流与重试：LLM API 的 rate limit 处理
- 观测性：LLM 调用链路追踪（LangSmith / 自建日志）
- Prompt 版本管理：不把 Prompt 硬编码，支持热更新

**成本控制：**
- Prompt Caching（Claude/OpenAI 都支持，可省 90% token 费用）
- 路由策略：简单问题用小模型，复杂问题用大模型
- Batch API：非实时场景批量处理，价格降 50%

**项目实践：**
- 在 MutiExpert 加 LLM 调用日志：记录每次调用的 token 数、耗时、费用
- 实现模型路由：意图识别用小模型（gpt-4o-mini），生成回答用大模型
- 用 Ollama 在本地跑一个开源模型，接入 MutiExpert 作为第三个模型选项
- 加 Prompt Caching 支持，统计节省了多少 token

---

## 第三阶段：7月-8月（整合输出，面试准备）

### 项目最终形态 Checklist

- [ ] RAG 有评估指标数据（Recall@K、Faithfulness 数字）
- [ ] Hybrid Search 上线（向量 + 全文）
- [ ] 微调实验目录完整（数据、训练、对比结果）
- [ ] LLM 调用日志可查（token 消耗、延迟）
- [ ] 公网可访问（不需要本地跑）
- [ ] README 有 Demo 截图 / 视频链接
- [ ] 代码有基本注释，核心模块有文档

### 面试深挖题准备（必须能流畅回答）

| 问题 | 答案要点 |
|------|--------|
| 你的 RAG 效果怎么样，怎么评估的？ | 说出 RAGAS、Recall@5 数字、优化前后对比 |
| 为什么选 pgvector 不选 Milvus？ | 数据量、事务需求、运维成本三个维度 |
| Function Calling 怎么设计的，踩过什么坑？ | 工具描述怎么写、模型选错工具怎么处理 |
| RAG 和微调分别什么时候用？ | 实时数据用RAG，风格/格式偏好用微调 |
| LLM 幻觉怎么缓解的？ | RAG接地 + Faithfulness 评估 + 置信度阈值 |
| 你项目最难的技术点是什么？ | 结合实际踩过的坑来答，不要背答案 |

---

## 学习资源精选（不囤课原则）

| 资源 | 类型 | 用途 |
|------|------|------|
| [DeepLearning.AI 短课](https://www.deeplearning.ai/short-courses/) | 免费视频 | RAG、Agent、微调各有1门1-2小时短课 |
| [RAGAS 文档](https://docs.ragas.io/) | 文档 | RAG 评估实践必查 |
| [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 开源库 | 微调实践直接用 |
| [Hugging Face 课程](https://huggingface.co/learn) | 免费 | NLP基础、微调基础 |
| [Simon Willison's Blog](https://simonwillison.net/) | 博客 | 最新 LLM 工程实践动态 |

---

## 里程碑检查点

| 时间 | 目标 | 验收标准 |
|------|------|--------|
| 4月底 | RAG 有评估数据 | 能说出 Recall@5 的具体数字 |
| 5月底 | Hybrid Search 上线 | 项目里跑通，有对比数据 |
| 6月底 | 微调实验完成 | experiments/ 目录有完整记录 |
| 7月底 | 项目公网部署 | 面试官能访问 Demo |
| 8月 | 开始投简历 | 简历上能写出3个有数据支撑的成果 |

---

*制定日期：2026-03-21*

---

## 补充模块：Agent 工程化三件套（对应高级 Agent 岗 JD）

> 以下内容针对要求「Agent 观测体系 + 自动化评测 + 记忆方案」的岗位，在第二阶段（5-6月）穿插完成。

### 补充1：Agent 全链路观测

**要做什么：**
- 每次 Agent 执行写结构化日志：step / input / tool_called / output / latency_ms / tokens / success
- 实现执行轨迹可视化（哪步失败，失败原因是什么）
- 接入 LangSmith 或自建 `agent_traces` 数据库表

**面试怎么说：**
> "我在项目里实现了 Agent 全链路追踪，每次执行都记录意图识别→工具选择→执行结果的完整链路，平均响应时间 XXms，工具调用成功率 XX%"

### 补充2：自动化评测 + 回测

**要做什么：**
- 建 golden dataset：100条领域问答，人工标注标准答案
- 写评测脚本：跑完 golden set，输出 Recall@5 / Faithfulness / Answer Relevance 三个指标
- 每次改 Prompt 或检索策略后跑一次，记录分数变化
- 维护一个 `experiments/eval_history.csv`：日期 / 改动内容 / 各项指标

**面试怎么说：**
> "我建立了自动化评测机制，有 100 条 golden dataset，每次迭代后跑回测对比，Recall@5 从 62% 提升到 81%"

### 补充3：长期记忆方案

**三种记忆类型实现：**
```
短期记忆（已有）：对话窗口 history list
长期记忆（需加）：用户重要信息向量化存储，检索相关记忆注入 context
结构化记忆（需加）：用户偏好/实体信息存 PostgreSQL，精确查询
```

**实现步骤：**
1. 加 `user_memories` 表：user_id / content / embedding / created_at
2. 每轮对话结束后，用 LLM 提取关键信息存入
3. 下次对话开始时，检索 top-3 相关记忆注入 System Prompt

### 补充4：Prompt 注入防御

**基本防御措施：**
- 用户输入和系统指令严格分离（不要把用户输入直接拼进 System Prompt）
- 输入过滤：检测 "ignore previous instructions" 类攻击模式
- 输出校验：敏感操作（删除/写入）要二次确认，不能只靠 LLM 判断
- 权限边界：工具调用只能访问用户有权限的资源

**面试怎么说：**
> "我在 Agent 工具调用层加了权限校验，用户输入和系统指令严格分离，防止 Prompt 注入攻击"

### 补充5：Claude Code 使用经验（这个 JD 的独特加分项）

这个岗位明确要求 Claude Code 重度玩家，你现在就在用，直接在简历和面试里说：
- 用 Claude Code 开发 MutiExpert 的完整后端（FastAPI + RAG + Agent）
- 掌握 CLAUDE.md 项目规则文件的编写，让 AI 写出符合项目约定的生产级代码
- 理解上下文工程（Context Engineering）：如何给 AI 提供恰好合适的信息
- 有 Agent 工作流实践：多步骤任务分解、验收标准定义、两次失败即换思路

---

*最后更新：2026-03-21*

---

## 补充模块：Boss直聘高频要求（3个JD汇总）

> 以下是从实际招聘JD中提炼的高频技能缺口，穿插在第一、二阶段完成。

### 缺口1：Pydantic 结构化输出 + 校验重试（高频，必须补）

**为什么重要：** 3个JD都提到。生产环境中LLM输出不稳定，必须有校验和自动重试机制。

**要掌握的：**
- OpenAI Structured Output / JSON mode + Pydantic 模型接收
- `instructor` 库：自动重试直到输出符合 Pydantic Schema
- 设计健壮的 Schema：必填字段、枚举约束、嵌套模型
- 重试策略：最多N次，每次把校验错误信息反馈给模型

**代码示例（要能手写）：**
```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

client = instructor.from_openai(OpenAI())

class ExtractedInfo(BaseModel):
    name: str
    intent: str
    confidence: float

result = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=ExtractedInfo,
    messages=[{"role": "user", "content": "..."}],
    max_retries=3,  # 校验失败自动重试
)
```

**项目实践：**
- 把 MutiExpert 的意图识别结果改为 Pydantic 结构化输出
- 加校验重试：识别失败时把错误信息反馈给模型重新识别
- 统计重试率，作为系统健康指标之一

---

### 缺口2：LangGraph 实际项目经验

**为什么重要：** JD要求"精通LangChain/LangGraph，有实际构建Agent的项目经验"。

**学习策略：** 不需要把 MutiExpert 重写成 LangGraph，而是用 LangGraph 做一个独立的小项目，证明你会用。

**LangGraph 核心概念：**
- State Graph：把 Agent 执行流程建模为状态机
- Node：每个处理步骤（意图识别 / 工具调用 / 反思）
- Edge：条件跳转（成功→下一步，失败→重试）
- Checkpoint：状态持久化，支持断点恢复

**实践任务（2周，做一个独立demo）：**
用 LangGraph 实现一个「多步骤研究 Agent」：
1. 接收用户问题
2. 分解为子问题
3. 对每个子问题搜索 + 检索知识库
4. 汇总生成报告
5. 反思检查，不满意就重来

**资源：**
- [LangGraph 官方教程](https://langchain-ai.github.io/langgraph/tutorials/introduction/) — 从 quickstart 开始
- 完成后把 demo 放 GitHub，README 说明架构

---

### 缺口3：LLM 调用工程优化四件套

**JD 原话：** "掌握LLM API调用中的缓存、去重、批处理、流式处理等实用优化技术"

| 优化技术 | 做什么 | 实现方式 |
|---------|--------|--------|
| **精确缓存** | 相同 prompt 直接返回缓存结果 | Redis / 内存字典，key=hash(prompt) |
| **语义去重** | 语义相似的 prompt 复用结果 | 向量相似度 > 0.95 时走缓存 |
| **Prompt Caching** | Claude/OpenAI 原生前缀缓存 | 固定 System Prompt 加 cache_control |
| **Batch API** | 非实时任务批量处理，降价50% | OpenAI Batch API，异步任务用 |
| **流式输出** | 逐token返回，降低首字延迟 | SSE，你项目已有 |

**项目实践：**
- 加 Redis 缓存层：相同问题命中缓存，记录缓存命中率
- 用 Claude Prompt Caching：把长 System Prompt 标记为可缓存，统计节省 token 数
- 对批量文档处理任务改用 OpenAI Batch API

---

### 缺口4：CoT 系统性运用

**三种 CoT 模式要会设计：**

**Zero-shot CoT：**
```
在回答前，先一步步思考，然后给出答案。
```

**Few-shot CoT（最有效）：**
```
问题：[示例问题]
思考：首先...，其次...，因此...
答案：[示例答案]

问题：[真实问题]
思考：
```

**Self-Consistency：**
同一问题生成3-5个推理路径，投票选最一致的答案（复杂逻辑判断用）

**什么时候用 CoT：**
- 多步推理、数学计算、逻辑判断 → 用 CoT
- 简单分类、信息提取 → 不用，浪费 token
- 意图识别 → Few-shot CoT 效果最好

**项目实践：**
- 把 MutiExpert 的意图识别 prompt 改为 Few-shot CoT 版本
- 对比改前改后的意图识别准确率

---

*补充日期：2026-03-21（来源：Boss直聘3个Agent工程师JD汇总）*
