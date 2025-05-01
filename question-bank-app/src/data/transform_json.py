import json

# 第一份 JSON 檔案路徑
input_file_path = "/home/jason_tmu_bioeng/cs-adventure/題庫系統開發/question-bank-app/src/data/questions.json"

# 輸出檔案路徑
output_file_path = "/home/jason_tmu_bioeng/cs-adventure/題庫系統開發/question-bank-app/src/data/questions_transformed.json"

# 讀取第一份 JSON
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 轉換每個題目
for exercise in data["exercises"]:
    # 將 question 從字串轉換為陣列（按句號或換行符分割）
    if isinstance(exercise["question"], str):
        exercise["question"] = exercise["question"].split(". ")
    
    # 確保每個題目都有 section 和 image 欄位
    exercise.setdefault("section", "")
    exercise.setdefault("image", "")

# 將轉換後的資料寫入新的 JSON 檔案
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"轉換完成！輸出檔案位於：{output_file_path}")