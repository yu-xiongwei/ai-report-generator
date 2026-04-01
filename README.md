# ai-report-generator

从数据清洗到 AI 分析的完整工程链路：自动清洗真实数据集，生成结构化质量分析报告。

## 技术栈

Python / 通义千问API / json

## 工程链路
```
telco_cleaner.py          →        telco_ai_analysis.py
处理7043行真实数据                  喂给大模型分析
发现3类脏数据问题                   输出结构化JSON报告
生成清洗报告                        质量分数70分，中风险
```

## 真实数据处理结果

使用 Kaggle Telco Customer Churn 数据集（7,043 行，21 列）：

| 指标 | 结果 |
|------|------|
| 原始行数 | 7,043 行 |
| 发现问题类型 | 3 类 |
| 数据可用率 | 100% |
| AI 质量评分 | 70 / 100 |
| 风险等级 | 中风险 |
| 可上线 | 否 |

## 核心功能

- system prompt 三层结构：角色定义 + 输出格式约束 + 评判标准（隐蔽空值扣15分、类型错误扣10分、字符串污染扣5分）
- `safe_json_parse()` 防御性解析，处理模型偶发的 ```json 包裹
- temperature=0 保证每次输出格式一致
- 支持字段名直接取值：`result['quality_score']`

## 输出示例
```json
{
  "quality_score": 70,
  "risk_level": "中风险",
  "issues_summary": ["TotalCharges字段类型错误", "含11行隐蔽空值"],
  "recommendations": ["转换字段类型", "清理空格伪装空值"],
  "is_production_ready": false
}
```

## 快速开始
```bash
pip install openai pandas
python telco_cleaner.py      # 第一步：清洗数据
python telco_ai_analysis.py  # 第二步：AI 分析
```
