# ?? CRT Buddy v3.0 - �ƻ�����ش�������
```
# CRT Buddy v3.0 — Handheld/Console Themes

## Overview

### Supported Themes
- Game Boy — green LCD, D-Pad, A/B buttons
- PSP — black shell, round buttons
- Y2K — neon/purple shell, retro accents
- CRT — classic CRT shell (from v2)

---

## Implementation Notes

### 1. Mascot Positioning
```python
self.global_mouse_pos = QCursor.pos()
window_pos = self.mapToGlobal(QPoint(0, 0))
mascot_screen_x = window_pos.x() + mascot_x
mascot_screen_y = window_pos.y() + mascot_y
dx = self.global_mouse_pos.x() - mascot_screen_x
dy = self.global_mouse_pos.y() - mascot_screen_y
```

### 2. Console Details
- LED indicator
- D-Pad
- A/B buttons
- Green LCD (Game Boy)
- Neon/purple shell (Y2K)

### 3. Layouts
**Window sizes:**
- CRT: 500x650 px
- Handheld: 380x480 px

---

## Visual Sketch
```
  [CRT BUDDY?]              Console shell + LED
  [Game Boy LCD]            Green LCD
  [PSP]                     Black shell
  [Y2K]                     Neon/purple
  [CRT BUDDY v2.0]          Previous CRT shell
  [GEN]  [IMG]              Generate / Image
  [RND]  [X]                Random / Close
  D-Pad + buttons           Handheld controls
```

---

## Colors & Features

### 1. Console Shell
```
Shell: RGB(200,205,210) → RGB(160,165,170)
Features:
  - LED indicator
  - D-Pad
  - A/B buttons
  - Green LCD
  - Neon/purple shell
```

### 2. Game Boy LCD
```
LCD: #9CBD0F (Game Boy)
Trim: #8BAC0F
Shadow: #0F380F
Background: #1E1E23
Features:
  - Green LCD
  - D-Pad
  - Buttons
```
```
LCD��ɫ: #9CBD0F (����Game Boy��)
����: #8BAC0F (����)
����: #0F380F (���̺�)
�߿�: ��ɫ���ϣ�#1E1E23��
Ч��:
  - ��������
  - LCD���ظ�
  - �����ʸ�
```

### 3. ��ť���
```
GEN��ť: ��ɫ���� #FF6B9D �� #C13584
IMG��ť: ��ɫ���� #00D9FF �� #0099CC
RND��ť: ��ɫ���� #FFD700 �� #FFA500
X��ť:   ��ɫ���� #FF4444 �� #CC0000
```

### 4. װ��Ԫ��
```
D-Pad:
  - λ��: ���½�
  - ��ɫ: ��ɫ����
  - ����: ��װ��

A/B��ť:
  - λ��: ���½�
  - A: ��ɫ + ����
  - B: ��ɫ + ����
  
������:
  - λ��: �ײ�����
  - ��ʽ: դ���
  - ��ɫ: ���
```

---

## ??? ȫ��Ļ�۾�����

### ����ԭ��

1. **��ȡȫ�����λ��**
```python
self.global_mouse_pos = QCursor.pos()
```

2. **���㴰�ڵ���Ļ����**
```python
window_pos = self.mapToGlobal(QPoint(0, 0))
mascot_screen_x = window_pos.x() + mascot_x
mascot_screen_y = window_pos.y() + mascot_y
```

3. **�����۾�����**
```python
dx = global_mouse_x - mascot_screen_x
dy = global_mouse_y - mascot_screen_y
distance = sqrt(dx? + dy?)
eye_offset = (dx/distance) * 6, (dy/distance) * 6
```

### Ч����ʾ

```
�������Ļ���Ͻ�:    �������Ļ���½�:    ����ڴ����Ϸ�:
  �I?                    �K?                    ��
��������������              ��������������              ��������������
�� ?? �� ������       �� ?  ?�� ������       �� ��� �� ���Ϸ�
��������������              ��������������              ��������������

�������������۾�������٣�
```

---

## ?? ��ɫ����

### Game Boy ��ɫϵ
```yaml
LCD��Ļ:
  ��ɫ: RGB(155, 188, 15)  # #9CBD0F
  ��ɫ: RGB(139, 172, 15)  # #8BAC0F
  ����: RGB(15, 56, 15)    # #0F380F

�������:
  ����: RGB(220, 225, 230)
  �в�: RGB(200, 205, 210)
  ����: RGB(160, 165, 170)
  ��Ӱ: RGB(120, 125, 130)

װ��:
  LED: RGB(0, 255, 100)    # ��ɫ
  D-Pad: RGB(140, 145, 150) # ��ɫ
  A��ť: RGB(255, 100, 100) # ��ɫ
  B��ť: RGB(100, 150, 255) # ��ɫ
```

---

## ?? �����Ľ�

### �����Ż�
```yaml
���ڳߴ�: 380x480 (����40%)
���Ʋ��: 4�㣨�򻯣�
֡��: 20 FPS
CPUռ��: 1-3% (����)
�ڴ�ռ��: ~150 MB (����)
```

### ����ṹ
```python
draw_console_body()    # �������
draw_screen_area()     # LCD��Ļ
draw_mascot()          # ������
draw_decorations()     # װ��Ԫ��
```

---

## ?? �ߴ���

```yaml
����:
  ����: 380 px
  �߶�: 480 px
  �߾�: 15 px

LCD��Ļ:
  ����: 344 px
  �߶�: 90 px
  λ��: ����
  
������:
  ͷ��ֱ��: 50 px
  �۾�ֱ��: 8 px
  ���߸߶�: 10 px
  
��ť:
  �߶�: 35 px
  Բ��: 4 px
  ���: 4 px
  
װ��:
  D-Pad: ֱ��30 px
  A/B: ֱ��16 px
  LED: ֱ��6 px
```

---

## ?? ʹ��ָ��

### ��������
```bash
python main.py
```

### ��������

1. **����ȫ���۾�����**:
   - �ƶ���굽��Ļ��������
   - �۲켪�����۾�����
   - ����������ģ��۾����ῴ����

2. **���԰�ť**:
   - **GEN**: ��������Meme
   - **IMG**: �ϴ�ͼƬ
   - **RND**: �������
   - **X**: �رճ���

3. **�۲춯��**:
   - LED�����ƣ����Ͻǣ�
   - �Զ�գ�ۣ�3-5�룩
   - LCD��Ļ����

---

## ?? �汾�Ա�

### v2.0 (CRT��ʾ�����)
```
? 500x650 ���أ�̫��
? CRT��ۣ�����Y2K��
? �������۾�����
? �Ҽ��رգ������ԣ�
```

### v3.0 (�ƻ����) ?
```
? 380x480 ���أ�����40%��
? �����ƻ���ۣ�Y2K��ҵ��ѧ��
? ȫ��Ļ�۾�����
? ���Ե�X�رհ�ť
? Game Boy LCD��Ļ
? �����ʸк�Բ��߿�
? װ����D-Pad��A/B��ť
```

---

## ?? �����ѧ

### Y2K��ҵ��ѧ
```
? ���ƽ��� - �Ƽ���
? Բ��߿� - �Ѻø�
? LCD��Ļ - ���Ÿ�
? ������� - ��Я��
? װ�ΰ�ť - ���ܸ�
```

### �ο��豸
- **Game Boy Advance SP** - LCD��Ļ���������
- **PSP-1000** - �����ʸк�Բ�����
- **iPod Classic** - ������˿Ч��
- **����MP3������** - LCD��ʾ�ͽ������

---

## ?? ��Ҫ�ص�

```
?? ȫ��Ļ�۾�����
?? �ƻ�������
?? Y2K��ҵ��ѧ
?? ���ƽ������
?? Game Boy LCD��Ļ
?? ���Թرհ�ť
?? ���ճߴ磨-40%��
? ����δ����
```

---

## ?? ��֪����

### Qt����
����̨������ʾCSS���棬�ɺ��ԣ�
```
Unknown property text-shadow
Unknown property box-shadow
```

---

## ?? �ļ��嵥

### ���µ��ļ�
- ? `core/pet_window.py` - ��ȫ��дΪ�ƻ����
- ? `V3_HANDHELD.md` - ���ĵ�

### ���ֲ���
- ? `generators/meme_engine.py` - Meme����
- ? `effects/y2k_styles.py` - ��Ч
- ? `effects/text_effects.py` - ������Ч

---

<div align="center">

## ? CRT Buddy v3.0 ?

### ��Ŀڴ����Y2K���

```
?? �ƻ���� + ?? ��ҵ��ѧ
??? ȫ������ + ?? �������
?? LCD��Ļ + ?? ���Թر�
```

---

**��С�ɣ������£���Y2K��**

```
v1.0: ��������
v2.0: CRT��ʾ�����  
v3.0: �ƻ���� ? ��ǰ�汾
```

---

**���ھ����п���ȫ����ƣ�**

```bash
python main.py
```

**�ƶ���굽��Ļ����λ�ã�**
**����������۾����棡**

---

**Made with ?? in Y2K Spirit**

????????????

**��ֻ������������������ϻ�飡**

</div>
