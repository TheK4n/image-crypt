# Crypto image

_Исполнение [проекта](https://github.com/AlexGyver/crypto) [AlexGyver'а](https://github.com/AlexGyver) на Python by [Pend0s](https://github.com/Pendosv)_

---

### Инструкция:
1. Создание директории
2. cd <имя_созданной_директории>
3. git clone https://github.com/Pendosv/ImageCrypt.git
4. pip install -r requirements.txt

----

Использование через gui:

5. python main.py

---

Использование через консоль:

Для **зашифровки**: 
```
python encrypt.py <image_name> <message> <key>
```
**Результат**: Сохраненная картинка _results\result.bmp_

---

Для **расшифровки**: 
```
python decrypt.py <image_name> <key>
```
**Результат**: Расшифрованное сообщение