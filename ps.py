import socket
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading

def port_scan(target):
    open_ports = {}  # オープンしているポートを格納する辞書
    total_ports = 99999

    progress['value'] = 0  # プログレスバーをリセット
    progress['maximum'] = total_ports

    result_text.delete(1.0, tk.END)  # テキストエリアをクリア
    log_text.delete(1.0, tk.END)  # ログエリアをクリア

    result_text.insert(tk.END, f"ホスト {target} のポートスキャンを開始します...\n\n")
    result_text.update()

    try:
        # ホストのすべてのポートをスキャン
        for port in range(1, total_ports + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # タイムアウトを1秒に設定

            # ポートに接続を試みる
            result = sock.connect_ex((target, port))
            if result == 0:
                result_text.insert(tk.END, f"ポート番号: {port:5} | ポート状態: OPEN\n")
                result_text.update()
                open_ports[port] = "OPEN"
                log_text.insert(tk.END, f"ホスト名: {target} | ポート番号: {port} | 状態: OPEN | ポートのアクセスされている数: 0 | ホスト名にアクセスされている数: 0\n")
            elif result == 111:
                log_text.insert(tk.END, f"ホスト名: {target} | ポート番号: {port} | 状態: 存在しない\n")
            else:
                log_text.insert(tk.END, f"ホスト名: {target} | ポート番号: {port} | 状態: 不明\n")

            sock.close()

            # プログレスバーを更新
            progress['value'] = port
            progress.update()

            # スキャン中の情報を更新
            scan_info_label.config(text=f"スキャン中のポート番号: {port} | スキャン中のポートの進行度: {port / total_ports:.2%} | 現在のホスト名: {target}")
            scan_info_label.update()

    except KeyboardInterrupt:
        result_text.insert(tk.END, "\nスキャンを中止しました\n")
        result_text.update()
    except socket.gaierror:
        result_text.insert(tk.END, "ホスト名の解決に失敗しました\n")
        result_text.update()
    except socket.error:
        result_text.insert(tk.END, "サーバへの接続に失敗しました\n")
        result_text.update()

    return open_ports

def start_scan():
    target = host_entry.get()
    threading.Thread(target=port_scan, args=(target,), daemon=True).start()

# ウィンドウを作成
root = tk.Tk()
root.title("ポートスキャナ")

# ホスト名入力フレーム
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

host_label = tk.Label(input_frame, text="スキャン対象のホスト名またはIPアドレス:")
host_label.grid(row=0, column=0)

host_entry = tk.Entry(input_frame, width=40)
host_entry.grid(row=0, column=1)

# スキャン開始ボタン
scan_button = tk.Button(root, text="スキャン開始", command=start_scan)
scan_button.pack()

# プログレスバー
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=5)

# スキャン情報ラベル
scan_info_label = tk.Label(root, text="", font=("Helvetica", 10))
scan_info_label.pack(pady=5)

# スキャン結果表示テキストエリア
result_text = scrolledtext.ScrolledText(root, width=100, height=25)
result_text.pack(padx=10, pady=5)

# スキャンログ表示テキストエリア
log_text = scrolledtext.ScrolledText(root, width=100, height=25)
log_text.pack(padx=10, pady=5)

# メインループ
root.mainloop()
