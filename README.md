# Crypto image
* [Описание проекта](#chapter-0)
* [Инструкция](#chapter-1)


<a id="chapter-0"></a>
## Описание проекта 

Исполнение [проекта](https://github.com/AlexGyver/crypto) [AlexGyver'а](https://github.com/AlexGyver) на Python by [Pend0s](https://github.com/Pendosv)  
Исходный ЯП: Processing

_Design by [Пашушка](https://github.com/PAPASKAS)_

Программа упаковывает байт символа в десятичное представление rgb:
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

Распаковка производится следующим методом:
```python
new_color = b * 65536 + g * 256 + r

this_char = 0
this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
this_char |= (new_color & 0x300) >> 5     # 00000000 00000011 00000000 -> 00000000 00000000 00011000
this_char |= (new_color & 0x7)
```

Костыль для русских букв:
```python
# Для зашифровки
if this_char > 1000:
    this_char -= 890

# Для расшифровки
if this_char > 130:
    this_char += 890
```

<a id="chapter-1"></a>
## Инструкция:

Создание виртуального окружения и установка зависимостей:

```

git clone https://github.com/Pendosv/ImageCrypt.git
cd ImageCrypt
virtualenv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```


### Использование через GUI:
```
python main.py
```
[![Пример](https://i.ibb.co/pvGxP0f/crypto.png)]()



### Использование через консоль:

Для **зашифровки**: 
```
python encrypt.py <image_name> <message> <key>
```
**Результат**: Сохраненная картинка _results\result.bmp_


Для **расшифровки**: 
```
python decrypt.py <image_name> <key>
```
**Результат**: Расшифрованное сообщение