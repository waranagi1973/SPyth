import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import time
import winsound

def scan_file(file_path):
    # ファイルのスキャンロジックを実装
    try:
        with open(file_path, 'r', encoding='cp932') as file:
            total_lines = sum(1 for line in file)
            lines_scanned = 0
            file_progress_bar['maximum'] = total_lines

            with open(file_path, 'r', encoding='cp932') as file:
                for line in file:
                    # 0.1秒待機してスキャンを続行
                    time.sleep(0.1)
                    lines_scanned += 1
                    file_progress_bar['value'] = (lines_scanned / total_lines) * 100
                    file_progress_bar.update()

                    # スキャン中の進捗状況と残り時間を表示
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    progress_percentage = (file_progress_bar['value'] / 100) * (overall_progress_bar['value'] / 100)
                    estimated_remaining_time = (elapsed_time / progress_percentage) - elapsed_time
                    status_label.config(text=f"{int(progress_percentage * 100)}% 完了 | スキャン中: {os.path.dirname(file_path)} / {os.path.basename(file_path)} | 残り時間: {int(estimated_remaining_time)}秒")

            # 1ファイルのスキャンが完了したら、全体のスキャンプログレスバーを進める
            overall_progress_bar['value'] += (1 / total_files) * 100
            overall_progress_bar.update()

            # スキャン結果を表示
            if "virus" in file_path.lower():
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, f"ファイル名: {file_path} | スキャン結果: ウイルス\n")
                result_text.see(tk.END)
                result_text.config(state=tk.DISABLED)
            else:
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, f"ファイル名: {file_path} | スキャン結果: 正常\n")
                result_text.see(tk.END)
                result_text.config(state=tk.DISABLED)
        
        return False  # 仮の返り値

    except Exception as e:
        # ファイルの読み取り時にエラーが発生した場合の処理
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"ファイルの読み取り中にエラーが発生しました: {e}\n")
        result_text.see(tk.END)
        result_text.config(state=tk.DISABLED)
        return False

def scan_all_drives():
    # 全ドライブの全ファイルをスキャンする

    # 例外としてスキップするディレクトリのリスト
    skip_dirs = ["C:/Windows", "C:/Program Files"]

    drives = ["{}:/".format(chr(i)) for i in range(ord('A'), ord('Z') + 1) if os.path.exists("{}:/".format(chr(i)))]
    global total_files
    total_files = 0
    scanned_files = 0
    infected_files = 0
    errors = 0

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            # 例外ディレクトリを削除してスキャンします
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in skip_dirs]

            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    total_files += 1
                    is_infected = scan_file(file_path)
                    if is_infected:
                        infected_files += 1
                        result_text.config(state=tk.NORMAL)
                        result_text.insert(tk.END, f"ウイルスが検出されました！ | ファイル名: {file_name}\n")
                        result_text.see(tk.END)
                        result_text.config(state=tk.DISABLED)
                    scanned_files += 1
                except PermissionError as pe:
                    result_text.config(state=tk.NORMAL)
                    result_text.insert(tk.END, f"PermissionError: {pe}\n")
                    result_text.see(tk.END)
                    result_text.config(state=tk.DISABLED)
                    errors += 1

    # スキャン終了を通知する音を鳴らす
    winsound.Beep(440, 3000)  # 3秒間なるように修正
    
    # スキャン終了メッセージを表示
    result_text.config(state=tk.NORMAL)
    result_text.insert(tk.END, "スキャンが終了しました。 | ")
    result_text.insert(tk.END, f"スキャン結果 ウイルスの数: {infected_files} | 安全なファイルの数: {total_files - infected_files - errors} | エラーが発生した数: {errors}\n")
    result_text.see(tk.END)
    result_text.config(state=tk.DISABLED)

    # スキャンが完了したファイル数などを表示
    status_label.config(text=f"スキャンが完了したファイル数: {scanned_files} | スキャンが完了していないファイル数: {total_files - scanned_files} | スキャンするファイルの総数: {total_files}")

# メインウィンドウを作成
root = tk.Tk()
root.title("セキュリティソフト")
root.geometry("1500x1250")

# スキャンボタンを作成
scan_button = tk.Button(root, text="全ドライブスキャン", command=scan_all_drives)
scan_button.pack(pady=20)

# プログレスバーを作成
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=800, mode='determinate')
progress_bar.pack(pady=10)

# スキャンファイルのプログレスバーを作成
file_progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')  # 横幅を400に変更
file_progress_bar.pack(pady=10)

# 全体のスキャンプログレスバーを作成
overall_progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=800, mode='determinate')
overall_progress_bar.pack(pady=10)

# ステータスラベルを作成
status_label = tk.Label(root, text="")
status_label.pack()

# 結果/ログテキストを表示するラベルを作成
result_label = tk.Label(root, text="結果/ログ")
result_label.pack()

# スキャン結果表示用のテキストエリアを作成
result_text = tk.Text(root, height=30, width=400)
result_text.insert(tk.END, "ここにスキャン結果が表示されます。\n")
result_text.config(state=tk.DISABLED)
result_text.pack(pady=10)

# ウィンドウをループで実行
start_time = time.time()
root.mainloop()
