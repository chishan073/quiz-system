開檔案三步驟
1.進到對的資料夾後輸入 
python3 -m venv venv

2.啟動環境  
source venv/scripts/activate => windows
source venv/bin/activate => Linux

3.安裝套件(資料夾裡面的套件會被一次裝好)  
pip install -r requirements.txt

收工兩步驟
1.儲存所有用到的套件(沒做下次會痛苦死)
pip freeze>requirements.txt

2.初次做版本控制
cd 路徑/my-project         # 進入專案資料夾
git init                   # 初始化 Git 倉庫
git add .                  # 加入所有檔案
git commit -m "first commit"   # 提交訊息
git branch -M main         # 設定主分支為 main（可選）
git remote add origin https://github.com/你的帳號/my-project.git
git push -u origin main    # 上傳到 GitHub
-----------------------------------------------------------------------
3.下次做版本控制(覆蓋掉type)
git add .
git commit -m "資料清理 及 題目重排列"
git push

4.下次做版本控制(branch type)

1. 建立新分支
git checkout -b feature/你的功能名稱

2. 在分支上做修改 & 提交
git add .
git commit -m "新增 UI 設計"

3. 推送分支到 GitHub
git push -u origin feature/你的功能名稱
4. 回到主分支
git checkout main

5. 合併分支（從 main 把新功能併進來）
git checkout main
git pull       # 先拉最新
git merge feature/ui-redesign

6. 合併後可以刪掉本地分支（可選）
git branch -d feature/ui-redesign
git push


FAQ:
Q1如果不知道在哪個資料夾怎麼辦?

Q2打開程式後顯示錯誤 有一堆套件要裝?
  因為上次做完沒有打 pip freeze>requirements.txt