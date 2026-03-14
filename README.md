# ai-report-generator

调用大模型 API 自动生成数据质量分析报告，输出结构化 JSON，支持下游代码直接取字段。

## 技术栈

Python / 通义千问 API / Claude API / OpenAI 兼容接口 / json

## 功能

- system prompt 三层结构设计：角色定义 + 输出格式约束 + 评判标准
- 评判标准：缺失率 >5% 列入 issues，重复率 >1% 列入 issues，每项扣 10 分
- 实现 `safe_json_parse()` 防御性解析函数，处理模型偶发的 ```json 包裹
- temperature=0 保证每次输出格式一致，支持字段名直接取值

## 输出示例
```json
{
  "quality_score": 82,
  "issues": ["缺失率超过5%", "重复率超过1%"],
  "recommendations": ["处理缺失值，如填充或删除", "消除重复数据"],
  "is_production_ready": false
}
```

## 项目结构
```
ai_report/
├── ai_report.py          # 主程序，调用 API 生成报告
├── safe_json_parse.py    # 防御性 JSON 解析函数
├── prompt_engine.py      # 多场景 Prompt 模板管理类
├── data/
│   └── users_normal.csv
└── output/
    └── ai_report.txt
```

## 快速开始
```bash
pip install openai pandas
# 配置你的 API key
python ai_report.py
```

## 核心亮点

`safe_json_parse()` 处理三种模型输出格式：干净 JSON、带 ```json 包裹、带空格换行，生产环境不崩溃。
