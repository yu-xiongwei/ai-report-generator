import json
import pandas as pd
from openai import OpenAI

def safe_json_parse(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:-1]
        text = "\n".join(lines)
    return json.loads(text.strip())

#--1.读取并统计CSV数据
df = pd.read_csv("data/users_normal.csv")

summary = {
    "总行数": len(df),
    "列名": list(df.columns),
    "缺失值统计": df.isnull().sum().to_dict(),
}

summary_text = json.dumps(summary, ensure_ascii=False, indent=2)
print("📊 数据摘要已生成，准备发送给大模型...\n")

#--2. 调用通义千问 API
client = OpenAI(
    api_key="sk-4becd4ec98e6435293b76cb8ed7fbcaf",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-turbo",
    temperature=0,
    messages=[
        {
            "role":"system",
             "content": '你是数据质量分析师。只输出合法 JSON,不输出任何其他文字。格式严格如下：{"quality_score": <0-100的整数>, "issues": [<问题描述字符串列表>], "recommendations": [<改进建议字符串列表>], "is_production_ready": <true或false>}'
        },
            {
                "role": "user",
                "content": f"请分析以下数据摘要 :\n{summary_text}"
            }
    ]
)

# ── 3. 解析 JSON 输出
report = response.choices[0].message.content
print("模型原始输出：")
print(report)
print()

result = safe_json_parse(report)
print("质量分数：", result["quality_score"])
print("发现问题：",result["issues"])
print("建议改进建议：",result["recommendations"])
print("可上线：",result["is_production_ready"])

# ── 4. 写入文件
with open("output/ai_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\n✅ 分析报告已生成：output/ai_report.txt")