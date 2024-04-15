import threading
import tkinter as tk
import tkinter.messagebox as messagebox
import re
import requests
from urllib.parse import urlparse

class SimpleBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Browser")
        self.create_widgets()
    
    def create_widgets(self):
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)
        
        self.go_button = tk.Button(self.root, text="Go", command=self.check_url)
        self.go_button.pack()
    
    def check_url(self):
        url = self.url_entry.get()
        if self.is_phishing(url):
            messagebox.showwarning("Warning", "This website might be phishing!")
        else:
            self.open_website(url)
    
    def is_phishing(self, url):
        # URLからドメインを抽出
        domain = urlparse(url).netloc
        
        # ドメインがIPアドレス形式の場合はフィッシングサイトと判定
        if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain):
            return True
        
        # ドメインが信頼できるリストに含まれているかをチェック（ここでは省略）
        # trusted_domains = ["example.com", "trustedwebsite.com", ...]
        
        # 一時的に常にフィッシングサイトと判定するようにしています
        return True
    
    def open_website(self, url):
        try:
            response = requests.get(url)
            # ここでウェブページを表示する処理を追加
            # 例えば、TkinterのWebViewを使うなど
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open website: {e}")
        
    def run(self):
        self.root.mainloop()

# バックグラウンドで実行する関数
def background_task():
    # ウェブブラウザのインスタンスを作成して実行
    browser = SimpleBrowser()
    browser.run()

# メインスレッド以外でバックグラウンドタスクを実行
background_thread = threading.Thread(target=background_task)
background_thread.daemon = True  # メインスレッドが終了したらバックグラウンドスレッドも終了する
background_thread.start()

# メインスレッドはここで終了するが、バックグラウンドスレッドは永続的に動作し続ける
