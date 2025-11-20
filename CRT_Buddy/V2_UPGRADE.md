# CRT Buddy v2.0 — Upgrade Notes

## Overview

### 1. New Shell Colors & Themes

CRT monitor-style shell:
- Top shell and full CRT frame
- Real-time eye/mouth motion with easing
- Multiple shell colorways (blue/teal/purple)
- Auto blink cadence (every 3–5s)
- Subtle shell flicker

Mascot motion:
- Mouse-relative position with soft follow
- Easing-based interpolation
- Damped movement for smoothness

### 2. Authentic CRT Frame Details

Front frame additions:
- Beige/colored shell options with vents
- Branding badge "CRT BUDDY"
- Side vents
- Colored bezel
- Curved screen effect with reflection
- Scanline glow

Bottom details:
- Power LED indicator (on-state color)
- "POWER" label

### 3. Visual Enhancements

Screen effects:
- Subtle vignette
- Static noise grain
- Animated scanline sweeps
- Flicker for realism
- Phosphor trail effect

Buttons:
- Hover states
- Press states
- Clear iconography
- Solid accent colors

### 4. Status System

State-driven messages:

| state       | face | when         |
|-------------|------|--------------|
| idle        | -_-  | standing by  |
| happy       | ^_^  | success      |
| processing  | @_@  | in progress  |

---

## Implementation Notes

### Eye tracking
- Track mouse position relative to window
- Compute relative vector to eye center
- Apply easing for motion
- Dampen for smooth stop

### Blink cadence
- Blink every 3–5 seconds
- Close duration ~150ms
- Randomized jitter

### Screen effects
- Scanline sweep moves slowly
- Power LED toggles with state
- Subtle flicker noise
- Timed flashing

---

## Size/Layout

Window enlarged to:
- Width: 500px (from 400px)
- Height: 650px (from 500px)
- More space for CRT shell

---

## Colors

Primary (blue theme):
- Shell gradient: #64C8FF → #3264C8
- Bezel: darker blue
- Eye glow: #00FF00
- Idle glow: soft white
- Accent glow: #FF00FF

CRT theme:
- Beige shell: #B4B4A0 → #8C8C78
- Bezel/dark trim: #282823 → #141412
- Curved glass reflection lines

Buttons:
- Generate: #00FFFF
- Image:    #FFFF00
- Random:   #FF00FF

---

## Algorithm (eye follow)
```python
dx = mouse_x - mascot_x
dy = mouse_y - mascot_y
distance = math.hypot(dx, dy)

# ��һ��������
eye_offset_x = (dx / distance) * 8
eye_offset_y = (dy / distance) * 8
```

### ����ϵͳ
- **����ʱ��**: 50ms��20 FPS��
- **ɨ����**: ÿ֡�ƶ�3����
- **գ��**: 60-100֡����һ��
- **LED����**: sin����������

### ��Ⱦ���
1. CRT��ǣ���ײ㣩
2. ��Ļ����
3. �������ɫ
4. ɨ����Ч��
5. ��ԴLED����㣩

---

## ?? ʹ������

### ����Ч��
1. ��������
2. ����������ڴ��ڶ���
3. �۾���ʼ�������
4. �Զ���ʼգ��
5. ���ֶ���Ч������

### ��������
- **�ƶ����** �� �������۾�����
- **��������** �� �����￴����
- **�������** �� �������ɴ���״̬��@_@��
- **���ɳɹ�** �� �����￪�ģ�^_^��

---

## ?? ��������

```yaml
���ڴ�С: 500x650 ����
֡��: 20 FPS
�ڴ�ռ��: ~180 MB
CPUռ��: �ͣ�2-5%��

����Ԫ��:
  - ɨ�����ƶ�
  - �۾�����
  - �Զ�գ��
  - LED����
  - ������˸
  - ��̬���
```

---

## ?? �Ӿ���ɫ

### ����CRT��ѧ
- ? �׻�ɫ������ǣ�90������䣩
- ? ���β�����Ļ
- ? ӫ����ɨ����
- ? ��̬���
- ? ��Ļ����

### Y2K���
- ? ӫ��ɫ�ʣ��̡��ۡ��ࡢ�ƣ�
- ? ��������壨Courier New��
- ? ���䰴ť
- ? ����Ч��
- ? ������˷�Χ

---

## ?? �ԱȾɰ汾

### v1.0���ɰ棩
```
- �򵥵�͸������
- ֻ�������ֱ���
- ����ɨ����
- �޼������ɫ
- ���� 400x500
```

### v2.0���°棩?
```
+ ������CRT��ʾ�����
+ �ɰ��ļ������ɫ
+ �۾��������
+ �Զ�գ�۶���
+ �������ϵͳ
+ ��ԴLEDָʾ��
+ ��ǿ���Ӿ�Ч��
+ ����Ĵ��ڣ�500x650��
+ ����ʵ��CRT�ʸ�
```

---

## ?? �����嵥

| ���� | �ٶ� | Ч�� |
|------|------|------|
| **ɨ����** | 3px/֡ | ���ϵ���ѭ�� |
| **�۾�����** | ʵʱ | �������λ�� |
| **�Զ�գ��** | 3-5�� | ����150ms |
| **LED����** | sin�� | ���ȱ仯 |
| **������˸** | sin�� | ӫ�����˸ |
| **��̬���** | ��� | 30����/֡ |

---

## ?? ��֪����

### Qt��ʽ����
```
Unknown property text-shadow
Unknown property box-shadow
```
- **ԭ��**: Qt��֧��CSS����Ӱ����
- **Ӱ��**: �ޣ�������̨����
- **���**: ���Ժ��ԣ���Ӱ�칦��

---

## ?? ��һ�����ܵĸĽ�

### ���ද��
- [ ] ������������΢ҡ��
- [ ] �����ͣʱ��Ӧ
- [ ] ���ʱ��Ծ����
- [ ] �������������ҿ���

### �������
- [ ] ���� (o_o)
- [ ] ���� (?_??)
- [ ] ���� (>_<)
- [ ] ˯�� (-.-)zzz

### ��������
- [ ] ���Ե��������
- [ ] ��קʱ�����ﷴӦ
- [ ] ������ʾ
- [ ] ����Ч��

---

<div align="center">

## ? CRT Buddy v2.0 - ȫ��������?

### ��Ҫ��ɫ

```
?? �۾��������ļ�����
??? ��ʵ��CRT��ʾ�����  
?? ��������ϵͳ
?? ��ǿ���Ӿ�Ч��
?? ������ԴLED
?? ��˸������
```

---

**���ھ����п���Ч���ɣ�**

```bash
python main.py
```

**�ƶ������꣬����������۾������㣡**

---

**Made with ?? in Y2K Spirit**

??????????

</div>
