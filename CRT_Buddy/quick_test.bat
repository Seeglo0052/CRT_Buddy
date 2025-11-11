@echo off
chcp 65001 >nul
title CRT Buddy - 快速测试
color 0B

cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║          CRT BUDDY - 快速测试脚本 v1.0                   ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0dist"

if not exist "CRT_Buddy.exe" (
    color 0C
    echo [? 错误] 找不到 CRT_Buddy.exe
    echo.
    echo 请确保在项目根目录运行此脚本
    echo 预期位置: dist\CRT_Buddy.exe
    echo.
    pause
    exit /b 1
)

echo [? 成功] 找到 CRT_Buddy.exe
echo.

REM 获取文件信息
for %%A in (CRT_Buddy.exe) do (
    set filesize=%%~zA
    set /a sizemb=%%~zA / 1048576
)

echo ┌───────────────────────────────────────────────────────────┐
echo │  ?? 文件信息                                               │
echo └───────────────────────────────────────────────────────────┘
echo.
echo   文件名: CRT_Buddy.exe
echo   大小: %sizemb% MB
echo   版本: 1.0.0
echo   状态: 独立可执行文件
echo.

echo ┌───────────────────────────────────────────────────────────┐
echo │  ?? 测试选项                                               │
echo └───────────────────────────────────────────────────────────┘
echo.
echo   [1] 启动 CRT Buddy
echo   [2] 查看使用说明
echo   [3] 打开output文件夹
echo   [4] 退出
echo.
set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto start_app
if "%choice%"=="2" goto show_help
if "%choice%"=="3" goto open_output
if "%choice%"=="4" goto exit

:start_app
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo [启动中] 正在启动 CRT Buddy...
echo.
echo ?? 使用提示:
echo   ? 左键拖拽窗口 - 移动到任意位置
echo   ? 右键点击窗口 - 关闭程序
echo   ? 输入文字 + GENERATE - 生成文字Meme
echo   ? 拖拽图片到窗口 - 添加Y2K特效
echo   ? RANDOM按钮 - 随机生成惊喜
echo.
echo ?? 输出位置: output\ 文件夹
echo.
echo ═══════════════════════════════════════════════════════════
echo.

timeout /t 2 /nobreak >nul

start "" "CRT_Buddy.exe"

timeout /t 2 /nobreak >nul

echo.
echo [? 完成] CRT Buddy 已启动！
echo.
echo ?? 提示:
echo   - 首次启动可能需要3-6秒
echo   - 如果Windows提示安全警告:
echo     点击"更多信息" → "仍要运行"
echo.
pause
goto menu

:show_help
echo.
echo ┌───────────────────────────────────────────────────────────┐
echo │  ?? 使用说明                                               │
echo └───────────────────────────────────────────────────────────┘
echo.
if exist "使用说明.txt" (
    type "使用说明.txt"
) else (
    echo ? CRT Buddy - Y2K桌面宠物 Meme生成器
    echo.
    echo 【快速开始】
    echo   1. 双击运行 CRT_Buddy.exe
    echo   2. 窗口会显示在屏幕上
    echo   3. 开始创作！
    echo.
    echo 【三种使用方式】
    echo   方式1 - 文字Meme:
    echo     输入文字 → 点击 GENERATE MEME
    echo.
    echo   方式2 - 图片处理:
    echo     拖拽图片到窗口 → 自动添加Y2K特效
    echo.
    echo   方式3 - 随机生成:
    echo     点击 RANDOM Y2K EFFECT → 获得惊喜
    echo.
    echo 【输出位置】
    echo   生成的文件保存在: output\ 文件夹
    echo.
    echo 【Y2K特效】
    echo   ??? CRT效果 ?? VHS故障 ?? 全息镭射
    echo   ?? 镀铬金属 ?? 霓虹辉光 ?? 像素化
echo.
)
echo.
pause
goto menu

:open_output
cd ..
if not exist "output" (
    mkdir output
    echo.
    echo [?? 信息] output文件夹已创建
    echo.
    echo ?? 提示: 生成Meme后文件会保存在这里
) else (
    echo.
    echo [? 成功] 打开output文件夹
)
start "" "output"
timeout /t 2 /nobreak >nul
goto menu

:menu
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║          CRT BUDDY - 测试菜单                             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0dist"
echo   [1] 启动 CRT Buddy
echo   [2] 查看使用说明
echo   [3] 打开output文件夹
echo   [4] 退出
echo.
set /p choice="请选择 (1-4): "
if "%choice%"=="1" goto start_app
if "%choice%"=="2" goto show_help
if "%choice%"=="3" goto open_output
if "%choice%"=="4" goto exit

:exit
echo.
echo 感谢使用 CRT Buddy！
echo.
echo ? 享受Y2K之旅！?
echo.
timeout /t 2 /nobreak >nul
exit
