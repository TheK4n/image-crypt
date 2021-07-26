

<h1 align="center">ImageCrypt</h1>

<p align="center">
  <a href="https://github.com/Pendosv">
    <img src="https://img.shields.io/github/followers/Pendosv?label=Follow&style=social">
  </a>
  <a href="https://github.com/Pendosv/ImageCrypt">
    <img src="https://img.shields.io/github/stars/Pendosv/ImageCrypt?style=social">
  </a>
</p>

* [Project description](#chapter-0)
* [Installation](#chapter-1)
* [Usage](#chapter-2)


<a id="chapter-0"></a>
## Project description 

[Project](https://github.com/AlexGyver/crypto) [AlexGyver](https://github.com/AlexGyver) on Python by [Pend0s](https://github.com/Pendosv)

_Design by [Пашушка](https://github.com/PAPASKAS)_

Byte packing in decimal rgb:
```python
this_color = b * 65536 + g * 256 + r
this_char = ord(char)

new_color = (this_color & 0xF80000)       # 11111000 00000000 00000000
new_color |= (this_char & 0xE0) << 11     # 00000111 00000000 00000000
new_color |= (this_color & (0x3F << 10))  # 00000000 11111100 00000000
new_color |= (this_char & 0x18) << 5      # 00000000 00000011 00000000
new_color |= (this_color & (0x1F << 3))   # 00000000 00000000 11111000
new_color |= (this_char & 0x7)            # 00000000 00000000 00000111
```

Unpacking byte:
```python
new_color = b * 65536 + g * 256 + r

this_char = 0
this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
this_char |= (new_color & 0x300) >> 5     # 00000000 00000011 00000000 -> 00000000 00000000 00011000
this_char |= (new_color & 0x7)
```

Method for russian symbols:
```python
# Encryption
if this_char > 1000:
    this_char -= 890

# Decryption
if this_char > 130:
    this_char += 890
```

<a id="chapter-1"></a>
## Installation:

Clone repository, installing virtual environment and dependencies:

```bash
git clone https://github.com/Pendosv/{project_path}.git
cd {project_path}
virtualenv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

<a id="chapter-2"></a>
## Usage

### GUI:
```
python main.py
```
[![Example](https://i.ibb.co/pvGxP0f/crypto.png)]()



### Console:

For **encryption**: 
```
python encrypt.py <image_name> <message> <key>
```
**Result**: saved image _results\result.bmp_


For **decryption**: 
```
python decrypt.py <image_name> <key>
```
**Result**: decrypted text


<p align="center">
  Contact with me
</p>
<p align="center">
  <a href="https://T.me/Pend0s">
    <img src="https://raw.githubusercontent.com/Pendosv/Pendosv/master/img/telegram.png" width="40" height="40">
  </a>
    <a href="mailto:djvlad967891@gmail.com">
        <img src="https://raw.githubusercontent.com/Pendosv/Pendosv/master/img/mail.png" width="40" height="40">
      </a>
</p>

