# ??? CRT Buddy - 你的桌面千禧年伙伴

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-ff00ff)
![Python](https://img.shields.io/badge/python-3.8+-00ffff)
![License](https://img.shields.io/badge/license-MIT-00ff00)

**Y2K风格桌面宠物 & Meme生成器**

? 让CRT显示器守护你的桌面，生成复古千禧年风格的Meme ?

</div>

---

## ?? 功能特性

### ?? 桌面宠物
- ? **可拖拽CRT显示器**窗口，放置在屏幕任意位置
- ? **透明背景**，始终置顶显示
- ? **动态扫描线效果**，模拟真实CRT显示器
- ? **心情系统**：闲置、开心、思考、处理中
- ? **霓虹闪烁动画**，纯正Y2K美学

### ?? Y2K特效库
支持多种千禧年风格图像滤镜：
- ??? **CRT效果** - 扫描线 + RGB色差
- ?? **VHS故障艺术** - 水平位移 + 色彩失真
- ?? **全息镭射** - 彩虹渐变 + 金属光泽
- ?? **镀铬效果** - 银色金属质感
- ?? **霓虹辉光** - 荧光增强 + 柔光
- ?? **像素化** - 复古游戏风格

### ?? Meme生成模式

#### 1. 文字模式
输入文字 → 自动生成Y2K风格标语
- 渐变文字
- 故障艺术文字
- 霓虹灯文字
- 镀铬金属文字
- 复古彩虹文字

#### 2. 图片模式
拖拽图片 → 应用Y2K滤镜 + 添加文字
- 自动应用随机特效
- 添加Y2K贴纸（??????）
- 支持文字叠加

#### 3. 随机模式
一键生成完全随机的Y2K Meme
- 随机选择经典Y2K文案
- 随机特效组合

---

## ?? 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python CRT_Buddy.py
```

---

## ?? 使用指南

### 基本操作
1. **拖拽移动**：鼠标左键拖拽CRT窗口
2. **关闭程序**：鼠标右键点击窗口
3. **文字输入**：在输入框输入想要的Meme文字
4. **图片上传**：
   - 方式1：点击 `?? UPLOAD IMAGE` 按钮
   - 方式2：直接拖拽图片到窗口

### 生成Meme
- **? GENERATE MEME** - 根据输入文字生成Y2K风格Meme
- **?? UPLOAD IMAGE** - 上传图片并应用特效
- **? RANDOM Y2K EFFECT** - 生成完全随机的Y2K Meme

### 输出位置
所有生成的Meme保存在 `output/` 文件夹中

---

## ?? 打包为EXE

使用PyInstaller打包为独立可执行文件：

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包（单文件模式）
pyinstaller --name="CRT_Buddy" ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            CRT_Buddy.py

# 或者使用提供的打包脚本
python build_exe.py
```

打包后的文件位于 `dist/CRT_Buddy.exe`

---

## ?? Y2K经典元素

### 视觉风格
- ?? **荧光色调板**：粉红、青色、黄色、绿色
- ? **金属渐变**：镀铬、全息、镭射效果
- ?? **CRT显示器**：扫描线、色差、辉光
- ?? **故障艺术**：像素位移、RGB分离

### 文化符号
- ?? 光盘时代（CD-ROM、DVD）
- ?? 早期互联网（Geocities、Netscape）
- ?? VHS录像带美学
- ?? 赛博朋克元素
- ? 星星、闪光、装饰元素

---

## ??? 技术栈

- **PyQt6** - 桌面GUI框架
- **Pillow** - 图像处理
- **NumPy** - 数值计算
- **OpenCV** - 高级图像滤镜
- **Pygame** - 音效系统（计划中）

---

## ?? 项目结构

```
CRT_Buddy/
├── CRT_Buddy.py              # 主程序入口
├── requirements.txt          # 依赖列表
├── build_exe.py             # 打包脚本
├── README.md                # 项目说明
├── core/                    # 核心模块
│   ├── __init__.py
│   └── pet_window.py        # 桌面宠物窗口
├── effects/                 # 特效模块
│   ├── __init__.py
│   ├── y2k_styles.py        # Y2K图像滤镜
│   └── text_effects.py      # 文字特效
├── generators/              # 生成器模块
│   ├── __init__.py
│   └── meme_engine.py       # Meme生成引擎
└── output/                  # 输出目录（自动创建）
```

---

## ?? 未来计划

### V2.0 功能
- [ ] 添加Y2K音效包（ICQ提示音、拨号音）
- [ ] GIF动图导出（闪烁文字、旋转元素）
- [ ] 更多预设Meme模板
- [ ] AI文案生成集成（OpenAI/Claude）
- [ ] 社交媒体一键分享
- [ ] 自定义贴纸库
- [ ] 保存收藏夹功能

### V3.0 功能
- [ ] 多语言支持
- [ ] 插件系统
- [ ] 在线模板商店
- [ ] 协作模式

---

## ?? 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
git clone https://github.com/yourusername/CRT_Buddy.git
cd CRT_Buddy
pip install -r requirements.txt
python CRT_Buddy.py
```

---

## ?? 许可证

MIT License - 自由使用、修改、分发

---

## ?? 致谢

灵感来源于：
- 千禧年早期的网页设计
- Geocities时代的个人网站
- Y2K美学复兴运动
- 桌面宠物文化（Bonzi Buddy等）

---

<div align="center">

**? Made with ?? for Y2K Lovers ?**

如果喜欢这个项目，请给个Star ?

[报告Bug](https://github.com/yourusername/CRT_Buddy/issues) ? 
[功能建议](https://github.com/yourusername/CRT_Buddy/issues) ? 
[加入讨论](https://github.com/yourusername/CRT_Buddy/discussions)

</div>
