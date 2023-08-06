# InfixToPostfix

A python module converts infix expressions to postfix expressions and includes a visual interface.

## Table of Contents

- [Install](#install)
- [Usage](#usage)

## Install

```sh
pip install InfixToPostfix
```

## Usage

### No visual interface

```python
from InfixToPostfix.infix_to_postfix import InfixToPostfix

infix_to_postfix = InfixToPostfix()
expression = "a+b-(12.3*cde/(10%2^3))"
words, actions, states, result = infix_to_postfix.analyze(expression)
print(words, actions, states, result, sep="\n")
```

### With visual interface

```python
import sys

from PyQt6.QtWidgets import QApplication
from InfixToPostfix.ui import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
```

![visual_interface_1.png](https://github.com/RoiexLee/InfixToPostfix/blob/main/resource/visual_interface_1.png?raw=true)

![visual_interface_2.png](https://github.com/RoiexLee/InfixToPostfix/blob/main/resource/visual_interface_2.png?raw=true)