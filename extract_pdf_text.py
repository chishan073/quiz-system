import pdfplumber
import re
import json

# 清除每題雜訊文字（如說明、頁碼）
def clean_question_text(text):
    text = re.sub(r"\n－\d+－", "", text)  # 頁碼
    text = re.sub(r"說明：.*", "", text, flags=re.DOTALL)
    text = re.sub(r"\(含.*?\)", "", text)  # 括號補充
    text = re.sub(r"請檢查.*?考生自行負責。", "", text, flags=re.DOTALL)
    text = re.sub(r"本試題必須.*?試場。", "", text, flags=re.DOTALL)
    text = re.sub(r"本試題必須.*?試場。", "", text, flags=re.DOTALL)
    return text.strip()

# 自動修復文字中奇怪的符號或錯誤括號
def normalize_text(text):
    # 手動修復錯誤括號或亂碼選項（這根據出現頻率慢慢擴充）
    text = text.replace("版權(B所)", "(B)")
    text = text.replace("翻C", "(C)")
    text = text.replace("必(D究)", "(D)")

    # 通用亂碼清洗
    text = re.sub(r"[【】\[\]︱│｜—－印]", "", text)  # 加上印
    text = re.sub(r"\(\s*\)", "", text)             # 空括號
    text = re.sub(r"\)\s*", ") ", text)             # 括號後補空格
    text = re.sub(r"\(\s*", " (", text)             # 括號前補空格

    # 多餘符號與雜字處理（ex: "有，("、") "）
    text = re.sub(r"\s*有，\(", " ", text)
    text = re.sub(r"\)\s*", " ", text)

    # 多餘空格
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()





def extract_question_parts(q_body):
    original = q_body  # 備份原始題幹

    # 嘗試先不清洗直接分割
    parts = re.split(r"\s*\(([A-D])\)\s*", q_body)
    if len(parts) < 5:  # 如果分割出來不足 4 個選項，代表有問題，再清洗
        q_body = normalize_text(q_body)
        parts = re.split(r"\s*\(([A-D])\)\s*", q_body)

    question_text = parts[0].strip()
    options = {}

    for i in range(1, len(parts)-1, 2):
        key = parts[i]
        val = parts[i+1]
        options[key] = val.strip()

    return question_text, options


# 主流程：擷取題目＋答案
def extract_questions_and_answers(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        questions = []
        for page_num in range(6):  # 前6頁題目
            page = pdf.pages[page_num]
            text = page.extract_text()
            # 基本清洗
            text = re.sub(r"義守大學.*?\n", "", text, flags=re.DOTALL)
            text = re.sub(r"考試科目.*?\n", "", text, flags=re.DOTALL)
            text = re.sub(r"考試日期.*?\n", "", text, flags=re.DOTALL)
            text = re.sub(r"頁碼/總頁數.*?\n", "", text, flags=re.DOTALL)
            questions.append(text)

        answers_text = pdf.pages[6].extract_text()  # 第七頁答案

    # 分割題目段落
    all_questions_text = "\n".join(questions)
    question_items = re.split(r"\n(?=\d{1,2}\.)", all_questions_text)

    # 擷取答案
    answer_dict = {}
    for line in answers_text.splitlines():
        match = re.findall(r"(\d{1,2})\s*([A-D])", line)
        for q_num, ans in match:
            answer_dict[int(q_num)] = ans

    # 整合成 JSON 資料
    qa_list = []
    for i, q in enumerate(question_items, 1):
        q = q.strip()
        match = re.match(r"(\d{1,2})\.\s*", q)
        if match:
            real_question_num = int(match.group(1))
            q_body = q[match.end():].strip()
        else:
            real_question_num = i
            q_body = q

        question_text, options = extract_question_parts(q_body)

        current_question = {
            "question_number": real_question_num,
            "question_text": question_text,
            "options": options,
            "answer": answer_dict.get(real_question_num, "未提供")
        }
        qa_list.append(current_question)

    return qa_list

# 執行與儲存
qa_list = extract_questions_and_answers("127691.pdf")
with open('questions_answers.json', 'w', encoding='utf-8') as f:
    json.dump(qa_list, f, ensure_ascii=False, indent=4)

print("✅ 題目與答案成功儲存為 questions_answers.json")
