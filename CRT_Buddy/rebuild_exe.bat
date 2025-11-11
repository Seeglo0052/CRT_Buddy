@echo off
chcp 65001 >nul
title CRT Buddy - 重新打包
color 0B

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          CRT BUDDY - 重新打包脚本                        ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/5] 检查虚拟环境...
if not exist "C:\crt\Scripts\activate.bat" (
    color 0C
    echo [?] 虚拟环境不存在
    echo.
    echo 请先运行: auto_install.bat
    echo.
    pause
    exit /b 1
)
echo [?] 虚拟环境已找到

echo.
echo [2/5] 激活虚拟环境...
call C:\crt\Scripts\activate.bat
echo [?] 虚拟环境已激活

echo.
echo [3/5] 清理旧的构建文件...
if exist "build" (
    rmdir /s /q "build"
    echo [?] 删除 build 文件夹
)
if exist "dist" (
    rmdir /s /q "dist"
    echo [?] 删除 dist 文件夹
)
if exist "*.spec" (
    del /q "CRT_Buddy.spec" 2>nul
    echo [?] 删除旧的 spec 文件
)

echo.
echo [4/5] 开始打包...
echo 这可能需要几分钟，请耐心等待...
echo.

python -m PyInstaller CRT_Buddy_complete.spec

if errorlevel 1 (
    color 0C
    echo.
    echo [?] 打包失败
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 验证EXE文件...
if exist "dist\CRT_Buddy.exe" (
    for %%A in (dist\CRT_Buddy.exe) do (
        set filesize=%%~zA
        set /a sizemb=%%~zA / 1048576
    )
    
    color 0A
    echo.
    echo ════════════════════════════════════════════════════════════
    echo [???] 打包成功！
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 文件位置: dist\CRT_Buddy.exe
    echo 文件大小: %sizemb% MB
    echo.
    echo 现在可以:
    echo  1. 测试EXE: cd dist; .\CRT_Buddy.exe
    echo  2. 压缩分发: 使用7-Zip压缩dist文件夹
    echo  3. 上传GitHub: 创建Release
    echo.
    
    choice /C YN /M "是否立即测试EXE"
    if errorlevel 2 goto end
    if errorlevel 1 (
        echo.
        echo 启动 CRT Buddy...
        start "" "dist\CRT_Buddy.exe"
        timeout /t 2 /nobreak >nul
        echo.
        echo [?] 程序已启动
        echo.
        echo 如果程序正常运行，打包就完全成功了！
        echo.
    )
) else (
    color 0C
    echo [?] 找不到 EXE 文件
)

:end
pause
