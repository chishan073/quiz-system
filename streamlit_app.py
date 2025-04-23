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

# 顯示每題資訊並且讓使用者選擇答案
for index, row in df.iterrows():
    # 顯示題目
    st.subheader(f"題號 {row['question_number']}")
    st.write(row['question_text'])  # 顯示完整題目文字

    # 提取選項 (假設選項格式為 (A) ... (B) ... (C) ... (D) ...)
    options = re.findall(r"\((A|B|C|D)\)\s*([^()]+)", row['question_text'])
    if options:
        # 顯示選項
        user_answer = st.radio(
            "請選擇答案：",
            options=[f"{opt[0]}: {opt[1]}" for opt in options],
            key=f"radio_{row['question_number']}"
        )
    else:
        st.warning("⚠ 無法解析選項，請檢查題目格式！")

    # 顯示正確答案
    st.write(f"正確答案：{row['answer']}")

    # 分隔線
    st.write("---")

