@echo off
chcp 65001 >nul
echo ========================================
echo   CRT BUDDY - 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ? 错误: 未检测到Python
    echo.
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ?? 首次运行，正在安装依赖包...
    echo 这可能需要几分钟时间...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ? 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo ? 环境检查完成
echo.
echo ?? 正在启动 CRT Buddy...
echo.

REM 启动程序
python CRT_Buddy.py

if errorlevel 1 (
    echo.
    echo ? 程序异常退出
    pause
)
