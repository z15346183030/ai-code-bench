# 🧪 AI Code Bench

一个轻量级的 AI 模型编程能力评估工具。通过标准化的编程题目测试不同大模型的代码生成能力，自动评分并生成对比报告。

## ✨ 特性

- **标准化题库** — 内置 Easy/Medium/Hard 三档编程题，每题配有测试用例
- **多模型对比** — 支持同时测试多个模型（OpenAI/Kimi/Claude 等 OpenAI 兼容接口）
- **自动评分** — 代码正确性（测试用例通过率）+ 代码质量（结构、规范）双维度评估
- **可视化报告** — 自动生成 Markdown 格式的对比报告，直观展示模型能力差异

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/yourname/ai-code-bench.git
cd ai-code-bench
pip install -r requirements.txt
```

### 配置

复制配置模板并填入 API Key：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "models": [
    {
      "name": "gpt-4o",
      "api_key": "sk-xxx",
      "base_url": "https://api.openai.com/v1"
    },
    {
      "name": "moonshot-v1-8k",
      "api_key": "sk-xxx",
      "base_url": "https://api.moonshot.cn/v1"
    }
  ]
}
```

### 运行

```bash
# 运行全部评估
python main.py

# 指定模型
python main.py --models gpt-4o,moonshot-v1-8k

# 只跑简单题
python main.py --difficulty easy

# 指定输出文件
python main.py --output my_report.md
```

## 📊 报告示例

评估完成后会在 `results/` 目录生成 Markdown 报告：

```
# AI Code Bench 评估报告
评估时间: 2026-06-27 15:30:00

## 总分排名
| 排名 | 模型 | 总分 | 正确性 | 代码质量 |
|------|------|------|--------|----------|
| 1    | gpt-4o | 92.5 | 100 | 85 |
| 2    | moonshot-v1-8k | 78.3 | 83.3 | 73.3 |

## 各题详情
...
```

## 🏗️ 项目结构

```
ai-code-bench/
├── main.py               # CLI 入口
├── config.example.json   # 配置模板
├── requirements.txt
├── bench/
│   ├── runner.py         # 评估流程编排
│   ├── evaluator.py      # 评分引擎
│   ├── models.py         # 模型调用封装
│   └── reporter.py       # 报告生成
├── challenges/
│   ├── base.py           # 题目基类
│   ├── easy/             # 简单题
│   ├── medium/           # 中等题
│   └── hard/             # 困难题
└── results/              # 评估结果
```

## 📐 设计思路

### 评估维度

1. **正确性 (60%)** — 提取模型生成的代码，注入测试用例运行，计算通过率
2. **代码质量 (40%)** — 评估代码结构、命名规范、注释质量、代码简洁度

### 题目设计原则

- 覆盖常见算法场景（数组、字符串、栈、链表、设计题）
- 每题提供函数签名 + 测试用例，模型只需填充实现
- 难度梯度清晰，能有效区分模型能力

## 🛠️ 扩展

### 添加新题目

在对应难度目录下创建新文件：

```python
from challenges.base import Challenge, TestCase

class MyChallenge(Challenge):
    name = "my_challenge"
    difficulty = "medium"
    description = "题目描述..."
    signature = "def my_func(nums: list[int]) -> int:"
    test_cases = [
        TestCase(input={"nums": [1, 2, 3]}, expected=6),
    ]
    solution = """
def my_func(nums: list[int]) -> int:
    return sum(nums)
"""
```

### 添加新模型

在 `config.json` 中添加即可，任何 OpenAI 兼容接口都支持。

## License

MIT
