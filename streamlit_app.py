import streamlit as st
import pandas as pd
import json
import re

# 載入題目資料 (假設你將 JSON 檔案存放在同一資料夾下)
with open("questions_answers.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# 轉換為 DataFrame
df = pd.DataFrame(questions)

# 設定 Streamlit 網頁標題
st.title("題庫練習")

# 記錄使用者的選擇
user_answers = {}

# 顯示每題資訊並且讓使用者選擇答案
for index, row in df.iterrows():
    # 顯示題目
    st.subheader(f"題號 {row['question_number']}")
    st.write(row['question_text'])  # 顯示完整題目文字

    # 顯示「正課講義」與「複習課程」資訊（如果有）
    if "lectures" in row:
        st.write(f"正課講義：{row['lectures']}")
    if "review_courses" in row:
        st.write(f"複習課程：{row['review_courses']}")

    # 提取選項 (假設選項格式為 (A) ... (B) ... (C) ... (D) ...)
    options = row["options"]
    if options:
        # 顯示選項（由 options 字典動態產生）
        user_answer = st.radio(
         "請選擇答案：",
          options=[f"{key}: {val}" for key, val in options.items()],
           key=f"radio_{row['question_number']}_{index}"
)

        # 記錄使用者的選擇
        user_answers[row['question_number']] = user_answer.split(":")[0]  # 只記錄選項字母
    else:
        st.warning("⚠ 無法解析選項，請檢查題目格式！")

    # 顯示正確答案
    correct_answer = row['answer']
    st.write(f"正確答案：{correct_answer}")

    # 分隔線
    st.write("---")

# 顯示使用者總結 (可選)
if st.button("提交答案"):
    correct_count = sum(1 for k, v in user_answers.items() if v == df.loc[k-1, 'answer'])
    total_questions = len(user_answers)
    st.write(f"總共有 {correct_count}/{total_questions} 題答對！")
