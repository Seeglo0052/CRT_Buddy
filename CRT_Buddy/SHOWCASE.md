# ?? CRT Buddy - ����չʾ

## ?? Ч��Ԥ��

### ������ﴰ��
```
����������������������������������������������������������������������
��  ? CRT BUDDY ?                 ��
# CRT Buddy Showcase 展示

精选功能与效果展示，帮助你快速理解 CRT Buddy 的视觉风格与输出结果。

---

## UI Overview 界面概览

典型主界面（示意）：

```
┌───────────────────────────────────────────────┐
│ CRT BUDDY — READY TO GENERATE Y2K VIBES       │
│                                               │
│  [ Type your message or drag an image here ]  │
│                                               │
│  [ GENERATE MEME ]  [ UPLOAD IMAGE ]  [ RANDOM]
│                                               │
│  Drag me anywhere · Right-click for menu      │
└───────────────────────────────────────────────┘
```

---

## Text Styles 文字样式示例

- Gradient 渐变文字：高光 + 3D 阴影
- Glitch 故障风格：RGB 分离 + 抖动
- Neon 霓虹：发光轮廓 + 内阴影
- Chrome 镀铬：金属高光反射，适合 LOGO/标题
- Retro 复古：像素化边缘 + 旧网感

可在 `effects/text_effects.py` 中查看实现细节。

---

## Image Effects 图片效果示例

- CRT：扫描线 + 轻微 RGB 偏移，显像管质感
- VHS：抖动/拖影/噪点，录像带风味
- Holographic/Chrome/Neon：全息/镀铬/霓虹高光
- Pixelate：强像素化（8/16-bit 风格）

实现见 `effects/y2k_styles.py` 与 `generators/meme_engine.py`。

---

## Example Prompts 文案灵感

- WELCOME TO MY WEBSITE
- UNDER CONSTRUCTION
- BEST VIEWED IN NETSCAPE
- POWERED BY GEOCITIES
- CYBER DREAMS 2000

---

## Export 输出

- 输出目录：`output/`
- 文件命名：`y2k_text_*.png` / `y2k_image_*.png` / `y2k_random_*.png`

---

如需提交截图或案例，欢迎在仓库 Discussions/Issues 中补充分享。

---

## ?? ��ɫ����

```markdown
# CRT Buddy — Showcase

Curated features and outputs to quickly grasp the visual style and results of CRT Buddy.

---

## UI Overview

Example main window (illustrative):

```
┌────────────────────────────────────────────────────────┐
│ CRT BUDDY — READY TO GENERATE Y2K VIBES               │
│                                                        │
│  [ Type your message or drag an image here ]           │
│                                                        │
│  [ GENERATE MEME ]  [ UPLOAD IMAGE ]  [ RANDOM ]       │
│                                                        │
│  Drag me anywhere · Right-click for menu               │
└────────────────────────────────────────────────────────┘
```

---

## Text Styles (examples)

- Gradient: glossy highlight + subtle 3D shadow
- Glitch: RGB channel split + jitter
- Neon: glow ring + inner shadow
- Chrome: metallic reflection; great for logos/headlines
- Retro: pixelated edge with old-web vibes

---

## Effects on Images

- CRT scanlines + RGB shift
- VHS jitter/ghosting/static noise
- Pixelate (8/16-bit)
- Holographic, chrome, neon overlays

---

## Sample Prompts

- WELCOME TO MY WEBSITE
- UNDER CONSTRUCTION
- BEST VIEWED IN NETSCAPE
- POWERED BY GEOCITIES

---

## Outputs

- Text → `output/y2k_text_*.png`
- Image → `output/y2k_image_*.png`
- Random → `output/y2k_random_*.png`
```

### �Ƽ��ⲿ���壨��ѡ��
```
Y2K������壺
1. Visitor (���ط��)
2. Orbitron (�Ƽ���)
3. Audiowide (���Ӹ�)
4. Press Start 2P (��Ϸ���)
5. VT323 (�ն˷��)

������վ:
- Google Fonts
- DaFont
- 1001 Fonts
```

---

## ?? ��������

### ͼ����
```yaml
���ͼ��ߴ�: 800x800 px
����ͼ��Ĭ��: 800x400 px
�����ʽ: PNG (����)
ɫ�ʿռ�: RGB
λ���: 8-bit per channel

��Ч����:
  ɨ���߼��: 3-4 px
  ɫ��ƫ��: 3 px
  ��������: 5-30 px
  ���ؿ��С: 6-12 px
  �Թ�뾶: 15 px
  �߿����: 10 px
```

### ����ָ��
```yaml
��������: <1��
ͼ����Ч: 1-3��
ͼ�񱣴�: <1��

�ڴ�ռ��: ~100-200 MB
CPUռ��: �еȣ�����ʱ��

֧��ͼƬ��С: ���4000x4000
�Ƽ�ͼƬ��С: 500-2000 px
```

---

## ?? ʹ�ó���

### ����ʹ��
```
? �罻ý��ͷ��
? ����Ȧ/Instagram����
? ���������
? ���Ӻؿ�
? �����ֽ
```

### ����ʹ��
```
? Y2K������
? ������վԪ��
? Vaporwave����
? ����ר������
? �����
```

### ��ҵʹ��
```
? Ʒ��Y2KӪ��
? ��������
? �罻ý������
? ��װ��Ʋο�
? �������
```

---

## ?? �������

### ����Y2KԪ�����
```
���1: CRTЧ�� + "UNDER CONSTRUCTION"
�� �����ĸ�����վԪ��

���2: �޺�Թ� + �ɶ���Ƭ
�� 90���ҹ���Χ

���3: VHS���� + ��ͥ��Ƭ
�� ���ɼ�ͥ¼���

���4: ȫϢЧ�� + Logo
�� CD����/��ֽ���

���5: �Ƹ����� + �Ƽ��ʻ�
�� ������˱���
```

### Memeģ�崴��
```
ģ��1: Drake��ʽ
- ��ͼ: ��ͨ��Ƭ���ܾ����ƣ�
- ��ͼ: Y2K��Ч��Ƭ���������ƣ�

ģ��2: �Աȸ�ʽ
- ���: "2023"���ִ���Լ��
- �ұ�: "2000"��Y2K��Ч��

ģ��3: ˼ά��չ
- С��: ��ͨ���
- ������: Y2K��ѧ

ģ��4: ʱ����
- չʾ��ͬY2K��Ч���ݱ�
```

---

## ?? δ������Ԥ��

### V2.0 �ƻ�
```
? ����Ч:
   - ˮ����Ч��
   - ��������
   - �����꣨Matrix���
   - �������񱳾�

?? �¹���:
   - GIF��������
   - ��������ģʽ
   - �Զ���ɫ��
   - ģ�屣��

?? ��Ч:
   - ICQ "Uh oh!"
   - Windows������
   - ������
   - ������Ч
```

### V3.0 Ը��
```
?? AI����:
   - AI����Y2K�İ�
   - AIͼ����ǿ
   - ����Ƽ�ϵͳ

?? ���߹���:
   - �ƶ�ģ���
   - ��������
   - ����Э��

?? רҵ����:
   - ͼ��ϵͳ
   - �����Զ���ѡ��
   - ��Ƶ����
```

---

## ?? ���ʵ��

### ������Ч���ļ���

1?? **ѡ����ʵ�ԴͼƬ**
```
? �߷ֱ��ʣ�500px���ϣ�
? ����������
? �Աȶ�����
? ����ѹ����ͼƬ
? ̫����̫��
```

2?? **�������ԭ��**
```
? ���������3-5�����ʣ�
? ȫ��д���г����
? ʹ��Y2K������
? ̫���ľ���
? ���ӵĴʻ�
```

3?? **��Чѡ��**
```
��Ƭ���� �� �Ƽ���Ч
������Ƭ �� �޺�Թ�/CRT
�羰��Ƭ �� ȫϢ/VHS
�������� �� �Ƹ�/����
Logo��� �� �Ƹ�/����
```

4?? **��ɫ����**
```
��ɫ + ��ɫ = ����Y2K
��ɫ + ��ɫ = �Ա�ǿ��
��ɫ + ��ɫ = ������
��ɫ + ��ɫ = �Ƽ���
```

---

<div align="center">

## ?? ��ʼ�������Y2K������

**CRT Buddy ��ÿ���˶��ܳ�ΪY2K������**

[����](https://github.com/yourusername/CRT_Buddy) ? 
[�̳�](USAGE.md) ? 
[����](https://github.com/yourusername/CRT_Buddy/issues)

</div>
