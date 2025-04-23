import pdfplumber
import re

# 開啟 PDF 檔案
with pdfplumber.open("127691.pdf") as pdf:
    # 提取前六頁的內容（題目）
    questions = []
    for page_num in range(6):  # 假設前六頁是題目
        page = pdf.pages[page_num]
        questions.append(page.extract_text())

    # 提取第七頁的內容（答案）
    answers = pdf.pages[6].extract_text()  # 假設第七頁是答案


# 輸出提取的資料
print("題目資料:", questions)
print("答案資料:", answers)

all_questions_text = "\n".join(questions)  # 將六頁文字合併
question_items = re.split(r"\n(?=\d{1,2}\.)", all_questions_text)  # 根據題號斷開（如 1.、2.）

answer_dict = {}
answer_lines = answers.strip().splitlines()
for line in answer_lines:
    if re.search(r"^\d+", line):  # 找出包含題號的行
        parts = re.findall(r"(\d{1,2})\s*([A-D])", line)
        for q_num, ans in parts:
            answer_dict[int(q_num)] = ans

# 更新 qa_list 的生成邏輯
qa_list = []
for i, q in enumerate(question_items, 1):
    qa_list.append({
        "question_number": i,
        "question_text": q.strip(),
        "answer": answer_dict.get(i, "未提供")
    })

import json
# 儲存為 JSON 檔案

with open('questions_answers.json', 'w', encoding='utf-8') as f:
    json.dump(qa_list, f, ensure_ascii=False, indent=4)
print("題目和答案已成功提取並儲存為 JSON 檔案。")
