@echo off
chcp 65001 >nul
title CRT Buddy v2.0 - Quick Launch
color 0B

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          CRT BUDDY v2.0 - 快速启动                      ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ?? 新功能:
echo   ???  眼睛跟踪鼠标
echo   ???  真实CRT显示器外观
echo   ?? 智能心情表情
echo   ?? 多重动画效果
echo.
echo 正在启动...
echo.

cd /d "%~dp0"

REM 检查虚拟环境
if exist "C:\crt\Scripts\python.exe" (
    echo [?] 使用虚拟环境
    start "" "C:\crt\Scripts\python.exe" "main.py"
) else (
    echo [!] 虚拟环境未找到，使用系统Python
    start "" python "main.py"
)

timeout /t 2 /nobreak >nul

echo.
echo [?] CRT Buddy v2.0 已启动！
echo.
echo ?? 提示:
echo   - 移动鼠标，看吉祥物眼睛跟随
echo   - 等待几秒，看吉祥物眨眼
echo   - 右键点击窗口关闭程序
echo.
echo 享受你的Y2K桌面伙伴！
echo.
pause
