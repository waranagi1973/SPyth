import tkinter as tk
from tkinter import messagebox
import datetime

class FirewallManager:
    def __init__(self):
        self.firewall_active = False
        self.vpn_active = False
        self.activation_time = None
        self.user_rank = "レベル1プラスチック"
        self.ad_block_count = 0
        
        self.root = tk.Tk()
        self.root.title("Firewall Manager")
        self.root.geometry("1000x1000")  # ウィンドウのサイズを設定
        
        self.activation_label = tk.Label(self.root, text="ファイアウォールの稼働時間: N/A")
        self.activation_label.pack(pady=5)
        
        self.rank_label = tk.Label(self.root, text="ユーザーのランク: レベル1プラスチック")
        self.rank_label.pack(pady=5)
        
        self.ad_block_label = tk.Label(self.root, text="ブロックした広告数: 0")
        self.ad_block_label.pack(pady=5)
        
        self.vpn_label = tk.Label(self.root, text="VPN: オフ")
        self.vpn_label.pack(pady=5)
        
        self.build_button = tk.Button(self.root, text="BuildWall", command=self.build_wall)
        self.build_button.pack(pady=5)
        
        self.brake_button = tk.Button(self.root, text="BrakeWall", command=self.confirm_stop_firewall)
        self.brake_button.pack(pady=5)
        
        self.vpn_button = tk.Button(self.root, text="ToggleVPN", command=self.toggle_vpn)
        self.vpn_button.pack(pady=5)
        
        # タイマーを設定して、ウィンドウを定期的に更新
        self.root.after(1000, self.update_time)
        
    def build_wall(self):
        self.firewall_active = True
        self.activation_time = datetime.datetime.now()
        self.update_rank()
        self.update_labels()
        
    def brake_wall(self):
        if self.firewall_active:
            self.firewall_active = False
            self.activation_time = None
            self.update_rank()
            self.update_labels()
        else:
            tk.messagebox.showinfo("Firewall Disabled", "Firewall is already disabled.")
            
    def toggle_vpn(self):
        self.vpn_active = not self.vpn_active
        vpn_status = "オン" if self.vpn_active else "オフ"
        self.vpn_label.config(text=f"VPN: {vpn_status}")
        
    def confirm_stop_firewall(self):
        confirm = messagebox.askyesno("確認", "ファイアウォールを停止しますか？")
        if confirm:
            self.brake_wall()
        
    def update_labels(self):
        activation_text = f"ファイアウォールの稼働時間: {self.activation_time}" if self.activation_time else "ファイアウォールの稼働時間: N/A"
        self.activation_label.config(text=activation_text)
        
        rank_text = f"ユーザーのランク: {self.user_rank}"
        self.rank_label.config(text=rank_text)
        
        ad_block_text = f"ブロックした広告数: {self.ad_block_count}"
        self.ad_block_label.config(text=ad_block_text)
        
    def update_rank(self):
        if self.activation_time:
            duration = (datetime.datetime.now() - self.activation_time).days
            if duration >= 1825:
                self.user_rank = "レベル15核融合"
            elif duration >= 1095:
                self.user_rank = "レベル14 2H3H"
            elif duration >= 730:
                self.user_rank = "レベル13プラズマ"
            elif duration >= 365:
                self.user_rank = "レベル12プラチナ"
            elif duration >= 305:
                self.user_rank = "レベル11ダイアモンド"
            elif duration >= 243:
                self.user_rank = "レベル10鉛"
            elif duration >= 182:
                self.user_rank = "レベル9亜鉛合金"
            elif duration >= 152:
                self.user_rank = "レベル8亜鉛"
            elif duration >= 121:
                self.user_rank = "レベル7金"
            elif duration >= 91:
                self.user_rank = "レベル6青銅"
            elif duration >= 61:
                self.user_rank = "レベル5鉄"
            elif duration >= 31:
                self.user_rank = "レベル4ブロンズ"
            elif duration >= 15:
                self.user_rank = "レベル3石炭"
            elif duration >= 7:
                self.user_rank = "レベル2石"
            else:
                self.user_rank = "レベル1プラスチック"
        else:
            self.user_rank = "レベル1プラスチック"
    
    def update_time(self):
        if self.firewall_active:
            self.activation_label.config(text=f"ファイアウォールの稼働時間: {datetime.datetime.now() - self.activation_time}")
        self.root.after(1000, self.update_time)
            
    def run(self):
        self.root.mainloop()

# ファイアウォールのマネージャーを起動
firewall_manager = FirewallManager()
firewall_manager.run()
