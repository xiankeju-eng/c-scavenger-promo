#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C-Scavenger: A simple C disk cleaner utility
清理 C 盘垃圾文件和缓存
"""

import os
import shutil
import sys
from pathlib import Path
import subprocess
import ctypes

class CScavenger:
    """C Disk Cleaner Class"""
    
    def __init__(self):
        self.total_freed = 0
        self.files_deleted = 0
        
    def is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell.IsUserAnAdmin()
        except:
            return False
    
    def request_admin(self):
        """Request administrator privileges"""
        if not self.is_admin():
            print("⚠️  需要管理员权限来运行此程序")
            print("正在尝试以管理员身份重新运行...")
            ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    
    def clean_temp_files(self):
        """Clean temporary files"""
        print("\n🧹 开始清理临时文件...")
        
        temp_paths = [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%AppData%\Local\Temp"),
            os.path.expandvars(r"%SystemRoot%\Temp"),
            "C:\\Windows\\Temp",
        ]
        
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                self._delete_directory_contents(temp_path, "临时文件")
    
    def clean_recycle_bin(self):
        """Empty recycle bin"""
        print("\n🗑️  开始清空回收站...")
        try:
            # 使用 Windows API 清空回收站
            subprocess.run(
                'powershell.exe -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"',
                shell=True,
                capture_output=True
            )
            print("✅ 回收站已清空")
        except Exception as e:
            print(f"❌ 清空回收站失败: {e}")
    
    def clean_browser_cache(self):
        """Clean browser cache"""
        print("\n🌐 开始清理浏览器缓存...")
        
        # Chrome cache
        chrome_cache = os.path.expandvars(r"%AppData%\Local\Google\Chrome\User Data\Default\Cache")
        if os.path.exists(chrome_cache):
            self._delete_directory_contents(chrome_cache, "Chrome 缓存")
        
        # Edge cache
        edge_cache = os.path.expandvars(r"%AppData%\Local\Microsoft\Edge\User Data\Default\Cache")
        if os.path.exists(edge_cache):
            self._delete_directory_contents(edge_cache, "Edge 缓存")
        
        # Firefox cache
        firefox_cache = os.path.expandvars(r"%AppData%\Local\Mozilla\Firefox\Profiles")
        if os.path.exists(firefox_cache):
            self._delete_directory_contents(firefox_cache, "Firefox 缓存")
        
        # IE cache
        ie_cache = os.path.expandvars(r"%AppData%\Local\Microsoft\Windows\INetCache")
        if os.path.exists(ie_cache):
            self._delete_directory_contents(ie_cache, "IE 缓存")
    
    def clean_system_logs(self):
        """Clean system logs"""
        print("\n📋 开始清理系统日志...")
        
        log_paths = [
            "C:\\Windows\\Logs",
            os.path.expandvars(r"%AppData%\Local\Windows"),
        ]
        
        for log_path in log_paths:
            if os.path.exists(log_path):
                self._delete_old_logs(log_path)
        
        # Clear event logs
        try:
            subprocess.run(
                'powershell.exe -Command "Get-EventLog -LogName Application | Remove-EventLog -ErrorAction SilentlyContinue"',
                shell=True,
                capture_output=True
            )
            print("✅ 应用程序日志已清理")
        except:
            pass
    
    def clean_other_cache(self):
        """Clean other common cache locations"""
        print("\n💾 开始清理其他缓存...")
        
        other_paths = [
            os.path.expandvars(r"%AppData%\Local\CrashDumps"),
            os.path.expandvars(r"%AppData%\Local\Microsoft\Windows\WebCache"),
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Caches"),
            os.path.expandvars(r"%Windir%\Prefetch"),
            os.path.expandvars(r"%Windir%\SoftwareDistribution\Download"),
        ]
        
        for path in other_paths:
            if os.path.exists(path):
                self._delete_directory_contents(path, "缓存文件")
    
    def _delete_directory_contents(self, directory, category):
        """Safely delete directory contents"""
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        self.files_deleted += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        self.files_deleted += 1
                except Exception as e:
                    pass  # Skip files in use
            print(f"✅ {category} 清理完成")
        except Exception as e:
            print(f"⚠️  {category} 清理遇到问题: {e}")
    
    def _delete_old_logs(self, directory):
        """Delete old log files"""
        try:
            for filename in os.listdir(directory):
                if filename.endswith(('.log', '.bak', '.old')):
                    file_path = os.path.join(directory, filename)
                    try:
                        os.unlink(file_path)
                        self.files_deleted += 1
                    except:
                        pass
        except:
            pass
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("          🧹 C-Scavenger - C盘清理工具")
        print("="*50)
        print("1. 🧹 清理临时文件 (Temp)")
        print("2. 🗑️  清空回收站")
        print("3. 🌐 清理浏览器缓存")
        print("4. 📋 清理系统日志")
        print("5. 💾 清理其他缓存")
        print("6. 🚀 执行全面清理 (推荐)")
        print("0. 🚪 退出程序")
        print("="*50)
    
    def run_full_cleanup(self):
        """Run complete cleanup"""
        print("\n" + "="*50)
        print("开始执行全面清理...")
        print("="*50)
        self.clean_temp_files()
        self.clean_recycle_bin()
        self.clean_browser_cache()
        self.clean_system_logs()
        self.clean_other_cache()
        self.show_summary()
    
    def show_summary(self):
        """Show cleanup summary"""
        print("\n" + "="*50)
        print("✅ 清理完成！")
        print("="*50)
        print(f"已删除文件数: {self.files_deleted}")
        print("="*50)
    
    def main(self):
        """Main program loop"""
        self.request_admin()
        
        while True:
            self.show_menu()
            choice = input("\n请选择操作 (0-6): ").strip()
            
            if choice == '1':
                self.clean_temp_files()
            elif choice == '2':
                self.clean_recycle_bin()
            elif choice == '3':
                self.clean_browser_cache()
            elif choice == '4':
                self.clean_system_logs()
            elif choice == '5':
                self.clean_other_cache()
            elif choice == '6':
                self.run_full_cleanup()
            elif choice == '0':
                print("\n👋 感谢使用 C-Scavenger！")
                break
            else:
                print("❌ 无效选择，请重试")
            
            input("\n按 Enter 继续...")

if __name__ == "__main__":
    scavenger = CScavenger()
    scavenger.main()
