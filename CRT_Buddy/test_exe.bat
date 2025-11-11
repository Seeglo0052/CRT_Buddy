@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════════════
echo   CRT BUDDY - EXE 测试脚本 v1.0.0
echo ═══════════════════════════════════════════════════════
echo.

cd /d "%~dp0dist"

if not exist "CRT_Buddy.exe" (
    echo [错误] 找不到 CRT_Buddy.exe
    echo 请确保在正确的目录运行此脚本
    pause
    exit /b 1
)

echo [信息] 找到 CRT_Buddy.exe
echo.

for %%A in (CRT_Buddy.exe) do (
    set size=%%~zA
    set /a sizeMB=!size! / 1048576
    echo 文件名: %%~nxA
    echo 大小: !sizeMB! MB (%%~zA 字节)
    echo 版本: 1.0.0 (完整PyQt6版本)
    echo.
)

echo [提示] 即将启动 CRT Buddy...
echo.
echo ? 操作说明：
echo  ? 左键拖拽窗口 - 移动到任意位置
echo  ? 右键点击窗口 - 关闭程序
echo  ? 输入文字 - 生成Y2K风格Meme
echo  ? 拖拽图片 - 添加Y2K特效
echo  ? 随机按钮 - 获得惊喜！
echo.
echo ?? 输出位置：
echo  ? 生成的文件保存在 "output" 文件夹
echo  ? 支持格式：PNG, JPG, GIF, BMP
echo.
echo ═══════════════════════════════════════════════════════
echo.

timeout /t 3 /nobreak >nul

echo [启动中] 正在启动 CRT Buddy...
start "" "CRT_Buddy.exe"

timeout /t 2 /nobreak >nul

echo.
echo [?] CRT Buddy 已启动！
echo.
echo ?? 提示：
echo  - 首次启动可能需要3-6秒
echo  - 窗口会出现在屏幕中央
echo  - 如果Windows提示安全警告，请选择"仍要运行"
echo.
echo ?? 开始你的Y2K创作之旅吧！
echo.
pause
