import customtkinter as ctk
import os
import shutil
import ctypes
import subprocess
import psutil
import time
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TEMP_PATH = os.environ.get('TEMP', '/tmp')


class OptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚀 Comptimizer")
        self.geometry("500x450")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Boost Your Laptop Performance", font=("Arial", 18))
        self.label.pack(pady=20)

        self.log = ctk.CTkTextbox(self, height=250, width=460)
        self.log.pack(pady=10)

        self.button = ctk.CTkButton(self, text="🚀 Optimize Now", command=self.run_in_thread)
        self.button.pack(pady=20)

    def write_log(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def run_in_thread(self):
        threading.Thread(target=self.optimize, daemon=True).start()

    def optimize(self):
        self.write_log("🚀 Starting optimization...\n")

        # 1. Clear Temp Folder
        self.write_log("🧹 Clearing Temp Folder...")
        deleted = 0
        for root, dirs, files in os.walk(TEMP_PATH):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                    deleted += 1
                except:
                    pass
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except:
                    pass
        self.write_log(f"✅ Deleted {deleted} temp files.\n")

        # 2. Empty Recycle Bin
        self.write_log("🗑 Emptying Recycle Bin...")
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0007)
            self.write_log("✅ Recycle Bin emptied.\n")
        except:
            self.write_log("❌ Could not empty Recycle Bin.\n")

        # 3. Kill Background Apps (non-critical)
        self.write_log("🧠 Killing non-essential background apps...")
        safe_kill = ["YourPhone.exe", "OneDrive.exe", "Cortana.exe", "RuntimeBroker.exe"]
        killed = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] in safe_kill:
                try:
                    psutil.Process(proc.info['pid']).terminate()
                    killed += 1
                except:
                    pass
        self.write_log(f"✅ Stopped {killed} background processes.\n")

        # 4. Flush DNS Cache
        self.write_log("🌐 Flushing DNS Cache...")
        subprocess.run("ipconfig /flushdns", shell=True)
        self.write_log("✅ DNS Cache flushed.\n")

        # 5. Restart Explorer.exe
        self.write_log("🔄 Restarting Windows Explorer...")
        subprocess.run("taskkill /f /im explorer.exe", shell=True)
        time.sleep(1)
        subprocess.Popen("explorer.exe", shell=True)
        self.write_log("✅ Explorer restarted.\n")

        # 6. Set High Performance Power Plan
        self.write_log("⚡ Switching to High Performance mode...")
        subprocess.run("powercfg -setactive SCHEME_MIN", shell=True)
        self.write_log("✅ Power mode set to High Performance.\n")

        self.write_log("🎉 Optimization Complete!\n")


if __name__ == "__main__":
    app = OptimizerApp()
    app.mainloop()

    
