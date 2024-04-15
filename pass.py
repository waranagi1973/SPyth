import tkinter as tk
from tkinter import messagebox
import re

def is_password_strong(password):
    """
    パスワードの強度をチェックする関数
    強度は以下の基準に基づいて評価されます:
    - 長さが8文字以上であること
    - 小文字、大文字、数字、特殊文字がそれぞれ1文字以上含まれること
    """
    if len(password) < 8:
        return False
    
    if not re.search(r"[a-z]", password):
        return False
    
    if not re.search(r"[A-Z]", password):
        return False
    
    if not re.search(r"[0-9]", password):
        return False
    
    if not re.search(r"[!@#$%^&*()-_+=]", password):
        return False
    
    return True

def is_id_strong(id_str):
    """
    IDの強度をチェックする関数
    強度は以下の基準に基づいて評価されます:
    - 長さが6文字以上であること
    - 英数字のみで構成されていること
    """
    if len(id_str) < 6:
        return False
    
    if not re.match(r"^[a-zA-Z0-9]+$", id_str):
        return False
    
    return True

def check_password_and_id():
    password = entry_password.get()
    id_str = entry_id.get()
    password_result = is_password_strong(password)
    id_result = is_id_strong(id_str)
    
    message = ""
    if password_result and id_result:
        message = "パスワードとIDの強度は十分です！\n\nパスワード: " + password + "\nID: " + id_str
    elif password_result:
        message = "パスワードの強度は十分ですが、IDの強度が不十分です。"
    elif id_result:
        message = "IDの強度は十分ですが、パスワードの強度が不十分です。"
    else:
        message = "パスワードとIDの強度がともに不十分です。"
    
    messagebox.showinfo("強度チェック結果", message)

# ウィンドウの作成
window = tk.Tk()
window.title("パスワードとIDの強度チェック")

# ラベルとエントリーの作成（パスワード）
label_password = tk.Label(window, text="パスワード:")
label_password.grid(row=0, column=0, padx=10, pady=10)
entry_password = tk.Entry(window, show="*")
entry_password.grid(row=0, column=1, padx=10, pady=10)

# ラベルとエントリーの作成（ID）
label_id = tk.Label(window, text="ID:")
label_id.grid(row=1, column=0, padx=10, pady=10)
entry_id = tk.Entry(window)
entry_id.grid(row=1, column=1, padx=10, pady=10)

# ボタンの作成
button_check = tk.Button(window, text="チェック", command=check_password_and_id)
button_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# ウィンドウの表示
window.mainloop()
