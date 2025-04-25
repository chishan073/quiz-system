import os
from openai import OpenAI
import json
import time
from dotenv import load_dotenv  # ⬅️ 讀取 .env 檔
from tqdm import tqdm  # ✅ 加入進度條

# ✅ 載入 .env 中的 API 金鑰
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ 請在 .env 檔中設定 OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 優先讀取補過解析的版本
if os.path.exists("questions_with_explanations.json"):
    with open("questions_with_explanations.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
        print("📁 已讀取已補上解析的題庫資料。")
else:
    with open("questions_answers.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
        print("📄 從原始題庫讀取資料。")

# 錯誤記錄檔初始化（每次重跑會清空）
with open("error_log.txt", "w", encoding="utf-8") as log_file:
    log_file.write("🚨 錯誤題目紀錄\n\n")

batch_size = 5
total_questions = len(questions)

for i in range(0, total_questions, batch_size):
    batch = questions[i:i + batch_size]
    any_updated = False

    print(f"\n🔄 處理第 {i+1} 到 {i+len(batch)} 題...")

    # 使用 tqdm 包裝批次中的題目，顯示進度條
    for item in tqdm(batch, desc="處理中", unit="題"):
        if "explanation" not in item or not item["explanation"].strip():
            prompt = f"""
            請針對以下選擇題提供詳細的解析，說明為什麼正確答案是 {item["answer"]}。

            題目：
            {item["question_text"]}

            選項：
            {json.dumps(item.get("options", {}), ensure_ascii=False, indent=2)}
            """
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一位醫學考題解析專家。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                explanation = response.choices[0].message.content.strip()
                item["explanation"] = explanation
                any_updated = True
                time.sleep(20)  # 每題間隔 20 秒
            except Exception as e:
                print(f"❌ 第 {item['question_number']} 題發生錯誤：{e}")
                item["explanation"] = "產生失敗"
                # 寫入錯誤 log
                with open("error_log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"第 {item['question_number']} 題錯誤：{str(e)}\n")

    
    # 儲存進度
    if any_updated:
        with open("questions_with_explanations.json", "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        print(f"💾 已儲存至第 {i+len(batch)} 題。")
        print(f"📊 已處理 {i+len(batch)}/{total_questions} 題")
        print("😴 等待 5 分鐘以避免觸發 API 限制...\n")
        print("✅ 批次完成，立即進入下一批（因為我們已經控制每題間隔）")

    else:
        print(f"⏭️ 這一批的題目都已有解析，無需儲存。")
        print("⚡ 快速跳過等待，因為這一批沒有新增解析。\n")

print("🎉 所有題目處理完成！")