
# colorclip 1.0.6

![Colorclip](https://i.ibb.co/4pKgVFf/Screenshot-2023-06-13-18-33-16-81-e4424258c8b8649f6e67d283a50a2cbc.jpg)

Color pack library,python terminal console

### Installation
```
pip install colorclip
```
### Usage
Import all name from colorclip
```
from colorclip import *
```
### FirstRun
```
print(red('sample string'))
```
![main](https://i.ibb.co/HYr8Yjd/main.jpg) 
### Bold String
```
print(bold('bold string'))
````
![bold](https://i.ibb.co/9Y9xmvF/bold.jpg)
### Underline
```
print(underline("underline"))
```
### Background color
```
print(bg_red(lime('sample string')))
```
![bgcolor](https://i.ibb.co/x8dJNHP/bgcolor.jpg)
### Check available color
```
p_ac()
```
### Available color
| Text Color            | Background Color      |
|-----------------------|-----------------------|
| black                 | bg_black              |
| red                   | bg_red                |
| green                 | bg_green              |
| yellow                | bg_yellow             |
| blue                  | bg_blue               |
| magenta               | bg_magenta            |
| cyan                  | bg_cyan               |
| white                 | bg_white              |
| gray                  | bg_gray               |
| bright_red            | bg_bright_red         |
| bright_green          | bg_bright_green       |
| bright_yellow         | bg_bright_yellow      |
| bright_blue           | bg_bright_blue        |
| bright_magenta        | bg_bright_magenta     |
| bright_cyan           | bg_bright_cyan        |
| bright_white          | bg_bright_white       |
| orange                | bg_orange             |
| pink                  | bg_pink               |
| lime                  | bg_lime               |
| teal                  | bg_teal               |
| lavender              | bg_lavender           |

### Rainbow
```
rainbow ("string")
```
![rainbow](https://i.ibb.co/pKqvBdH/rainbow.jpg)
### Blink
```
blink("string")
```

Default 
- repeat=5
- delay=0.5

 Custom
```
blink("string", repeat=10, delay=0.2)
````
### Typewriter
```
typewriter("String")
```

Default
- Delay=0.1
### Wavy
```
wavy("string")
```

Default
- amplitude=1
- frequency=1
### Vaporwave
```
vaporwave("string")
```
![vapor](https://i.ibb.co/HBPRptT/vaporwave.jpg)
### Rainbow typewriter
```
cc_text("string")
```

Default
- delay=0.1
### Help
```
help()
```
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/onefinalhug) 

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)

![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)