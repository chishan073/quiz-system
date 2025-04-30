import time
import os
from xmindparser import xmind_to_dict
from notion_client import Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ========== 配置 ==========
XMIIND_FILE_PATH = "化學.xmind"
NOTION_TOKEN = "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"
PAGE_ID = "1e4c3dc3eb2c80c2934fe451e5cf83fb"

notion = Client(auth=NOTION_TOKEN)

def push_to_notion(topics, block_id, indent=0):
    try:
        # 先列出目前 block_id 底下的所有 toggle 區塊標題
        existing_children = notion.blocks.children.list(block_id)["results"]
        existing_titles = set()
        for block in existing_children:
            if block["type"] == "toggle":
                texts = block["toggle"]["rich_text"]
                if texts:
                    existing_titles.add(texts[0]["text"]["content"])
    except Exception as e:
        print(f"⚠️ 無法讀取已存在區塊：{e}")
        existing_titles = set()

    for topic in topics:
        title = topic['title']
        if title in existing_titles:
            print(f"✅ 已存在：{title}")
            continue

        toggle_block = {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": title}}],
                "children": []
            }
        }

        try:
            result = notion.blocks.children.append(block_id, children=[toggle_block])
            time.sleep(0.3)  # 可視情況再拉長點
            new_block_id = result['results'][0]['id']
        except Exception as e:
            print(f"❌ 加入 {title} 失敗：{e}")
            continue

        if 'topics' in topic:
            push_to_notion(topic['topics'], new_block_id, indent + 1)

        

def sync_xmind(file_path):
    print(f"🔄 偵測到 {file_path} 修改，開始同步...")
    data = xmind_to_dict(file_path)
    topics = data[0]["topic"].get("topics", [])
    push_to_notion(topics, PAGE_ID)
    print("✅ 同步完成！")

# ========== 檔案監控 ==========
class XMindHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".xmind"):
            sync_xmind(event.src_path)

if __name__ == "__main__":
    if not os.path.exists(XMIIND_FILE_PATH):
        print(f"❌ 找不到檔案：{XMIIND_FILE_PATH}")
        exit(1)

    print("🚀 開始監控 XMind 檔案：", XMIIND_FILE_PATH)
    sync_xmind(XMIIND_FILE_PATH)  # 啟動時同步一次
    
    event_handler = XMindHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(XMIIND_FILE_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
