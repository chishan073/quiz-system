import pdfplumber
import re
import json

pdf_path = "127691.pdf"
output_path = "parsed_questions.json"

questions = []

with pdfplumber.open(pdf_path) as pdf:
    current_question = {}
    options = []
    for page in pdf.pages:
        lines = page.extract_text().split("\n")
        for line in lines:
            # 題號開頭的題目，例如 "15 Unit 2 ..."
            match = re.match(r"^(\d{1,3})\s+(Unit \d+ [^\s]+)\s+(.*)", line)
            if match:
                if current_question:
                    # 如果題目有選項，將選項加入
                    current_question["options"] = options
                    questions.append(current_question)
                
                # 新一題開始
                current_question = {
                    "question": match.group(3).strip(),
                    "chapter": match.group(2),
                    "number": int(match.group(1)),
                    "options": [],  # 用來存選項
                    "correct_answer": "",  # 若有正確答案資訊可以加入
                    "lectures": "",
                    "review_courses": ""
                }
                options = []  # 清空選項列表

            elif "正課講義：" in line:
                current_question["lectures"] = line.split("正課講義：", 1)[-1].strip()
            elif "複習課程：" in line:
                current_question["review_courses"] = line.split("複習課程：", 1)[-1].strip()
            elif re.match(r"^\([A-D]\)", line):  # 假設選項以 (A) 開頭
                options.append(line.strip())

    # 確保最後一題也能加入
    if current_question:
        current_question["options"] = options
        questions.append(current_question)

# 儲存成 JSON 檔案
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✔ 題目已儲存至 {output_path}")
