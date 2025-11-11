@echo off
chcp 65001 >nul
title CRT Buddy - 自动安装依赖
color 0B

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          CRT BUDDY - 自动安装脚本                        ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 此脚本将：
echo  1. 在C:\crt创建虚拟环境（避免路径长度问题）
echo  2. 安装所有必需的依赖
echo  3. 验证安装
echo.
echo ??  请确保以管理员权限运行！
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════
echo [1/6] 检查Python...
echo ════════════════════════════════════════════════════════════
python --version
if errorlevel 1 (
    color 0C
    echo.
    echo [? 错误] 找不到Python
    echo.
    echo 请先安装Python 3.11或3.13
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [?] Python已安装
timeout /t 2 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════
echo [2/6] 创建虚拟环境...
echo ════════════════════════════════════════════════════════════
echo 位置: C:\crt
echo.

if exist "C:\crt" (
    echo [!] 虚拟环境已存在，是否删除并重新创建？
    choice /C YN /M "删除并重新创建 (Y/N)"
    if errorlevel 2 goto skip_create
    if errorlevel 1 (
        echo 删除旧环境...
        rmdir /s /q "C:\crt"
    )
)

python -m venv C:\crt
if errorlevel 1 (
    color 0C
    echo.
    echo [? 错误] 虚拟环境创建失败
    pause
    exit /b 1
)
echo [?] 虚拟环境创建成功
timeout /t 2 /nobreak >nul

:skip_create
echo.
echo ════════════════════════════════════════════════════════════
echo [3/6] 激活虚拟环境...
echo ════════════════════════════════════════════════════════════
call C:\crt\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo [? 错误] 虚拟环境激活失败
    pause
    exit /b 1
)
echo [?] 虚拟环境已激活
timeout /t 2 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════
echo [4/6] 升级pip...
echo ════════════════════════════════════════════════════════════
python -m pip install --upgrade pip
echo [?] pip已升级
timeout /t 2 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════
echo [5/6] 安装依赖...
echo ════════════════════════════════════════════════════════════
echo.
echo 正在安装（这可能需要几分钟）...
echo  ? PyQt6 (GUI框架)
echo  ? Pillow (图像处理)
echo  ? NumPy (数值计算)
echo  ? OpenCV (图像滤镜)
echo  ? PyInstaller (打包工具)
echo.

pip install PyQt6==6.7.1 Pillow==11.0.0 numpy==2.2.1 opencv-python==4.10.0.84 pyinstaller==6.16.0

if errorlevel 1 (
    color 0C
    echo.
    echo [? 错误] 依赖安装失败
    echo.
    echo 可能的原因:
    echo  1. 网络问题
    echo  2. 权限不足
    echo  3. 磁盘空间不足
    echo.
    echo 尝试使用国内镜像:
    echo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt6
    echo.
    pause
    exit /b 1
)
echo [?] 所有依赖安装成功
timeout /t 2 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════
echo [6/6] 验证安装...
echo ════════════════════════════════════════════════════════════
echo.

set error_count=0

echo 检查 PyQt6...
python -c "import PyQt6.QtWidgets; print('[?] PyQt6 OK')" 2>nul
if errorlevel 1 (
    echo [?] PyQt6 失败
    set /a error_count+=1
)

echo 检查 Pillow...
python -c "import PIL; print('[?] Pillow OK')" 2>nul
if errorlevel 1 (
    echo [?] Pillow 失败
    set /a error_count+=1
)

echo 检查 NumPy...
python -c "import numpy; print('[?] NumPy OK')" 2>nul
if errorlevel 1 (
    echo [?] NumPy 失败
    set /a error_count+=1
)

echo 检查 OpenCV...
python -c "import cv2; print('[?] OpenCV OK')" 2>nul
if errorlevel 1 (
    echo [?] OpenCV 失败
    set /a error_count+=1
)

echo 检查 PyInstaller...
python -c "import PyInstaller; print('[?] PyInstaller OK')" 2>nul
if errorlevel 1 (
    echo [?] PyInstaller 失败
    set /a error_count+=1
)

echo.

if %error_count% gtr 0 (
    color 0C
    echo ════════════════════════════════════════════════════════════
    echo [?] 安装验证失败 (%error_count% 个错误)
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 请查看错误信息并重新运行此脚本
    echo.
    pause
    exit /b 1
)

color 0A
echo ════════════════════════════════════════════════════════════
echo [???] 安装完全成功！
echo ════════════════════════════════════════════════════════════
echo.
echo 虚拟环境位置: C:\crt
echo.
echo ┌──────────────────────────────────────────────────────────┐
echo │  ?? 下一步操作                                            │
echo └──────────────────────────────────────────────────────────┘
echo.
echo 方式1 - 运行程序:
echo   1. 激活环境: C:\crt\Scripts\activate
echo   2. 进入目录: cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy
echo   3. 运行程序: python CRT_Buddy.py
echo.
echo 方式2 - 打包EXE:
echo   1. 激活环境: C:\crt\Scripts\activate
echo   2. 进入目录: cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy
echo   3. 清理构建: Remove-Item -Recurse -Force build, dist
echo   4. 打包程序: python -m PyInstaller CRT_Buddy_complete.spec
echo   5. 测试运行: cd dist; .\CRT_Buddy.exe
echo.
echo ┌──────────────────────────────────────────────────────────┐
echo │  ?? 提示                                                  │
echo └──────────────────────────────────────────────────────────┘
echo.
echo  ? 每次使用前请激活虚拟环境
echo  ? 激活命令: C:\crt\Scripts\activate
echo  ? 退出命令: deactivate
echo.
echo 现在是否立即激活虚拟环境？
choice /C YN /M "激活虚拟环境 (Y/N)"

if errorlevel 2 goto end
if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════════════════════════
    echo 激活虚拟环境...
    echo ════════════════════════════════════════════════════════════
    echo.
    cmd /k "C:\crt\Scripts\activate.bat && cd /d C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy && echo 环境已激活！当前位置：项目根目录 && echo 运行程序: python CRT_Buddy.py && echo 打包程序: python -m PyInstaller CRT_Buddy_complete.spec"
)

:end
echo.
echo 感谢使用 CRT Buddy！
echo.
timeout /t 3 /nobreak >nul
exit
