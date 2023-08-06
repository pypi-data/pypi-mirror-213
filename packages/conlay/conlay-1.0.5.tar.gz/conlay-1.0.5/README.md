# Conlay - Console Layout
[![PyPi version][shields-pypi_version]][url-pypi_version]
[![Github Issues][shields-issues]][url-issues]
[![Github License][shields-license]][url-license]

Create visually pleasing console layouts with this easy-to-use Python library. 




## Installing
Install using <a href="https://pip.pypa.io/en/stable/">pip</a>

```bash
pip install conlay
```

or install it from <a href="https://pypi.org/project/conlay/#files">PyPi</a>




## Example
```python
from conlay import *

layout = Conlay()

blank_box = BoldBox(0, 0, 30, 5)
layout.add(blank_box)

label = ThinLabel(0, 0, "this is a test")
blank_box.add(label)

layout.print()
``` 

Console output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃╭──────────────╮            ┃
┃│this is a test│            ┃
┃╰──────────────╯            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


>
```




## Conlay()
`Conlay()` is the core class within the library. It generates and prints out the layout.

```python
layout = Conlay()
```

There are some attributes that can be used to modify or update the positioning, scale, color and other things. Because each <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElement()</a> is a subclass of `Conlay()`, each <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElement()</a> has the same attributes.

| attribute        | description | expected type | default value |
| :--------        | :---------- | :------------ | :------------ |
| `relative_x`       | Relative x-position to the parent object | `int` | 0 |
| `relative_y`       | Relative y-position to the parent object | `int` | 0 |
| `absolute_x`       | Absolute x-position | `int` | 0 |
| `absolute_y`       | Absolute y-position | `int` | 0 |
| `width`            | Elements width | `int` | 0 |
| `min_width`        | Minimal width. May limit the specified with | `int` | 0 |
| `max_width`        | Maximal width. May limit the specified with | `int` | 0 |
| `height`           | Elements height | `int` | 0 |
| `min_height`       | Minimal height. May limit the specified with | `int` | 0 |
| `max_height`       | Maximal height. May limit the specified with | `int` | 0 |
| `zindex`           | Indicates whether an element is printed above or below other elements | `int` | 0 |
| `padding_x`        | Specifies the padding on the x axis, which affects the absolute position of the child elements | `int` | 0 |
| `padding_y`        | Specifies the padding on the y axis, which affects the absolute position of the child elements | `int` | 0 |
| `text`             | Specifies the text content | `str` | n/a |
| `background`       | Specifies whether the element should have a background or not | `bool` | False |
| `background_color` | Specifies the background color | <a href="https://github.com/Salliii/conlay#colorbg">`Color.Bg`</a> | Color.Bg.clear |
| `border_color`     | Specifies the border color | <a href="https://github.com/Salliii/conlay#colorfg">`Color.Fg`</a> | Color.Fg.clear |
| `text_color`       | Specifies the text color | <a href="https://github.com/Salliii/conlay#colorfg">`Color.Fg`</a> | Color.Fg.clear |


### Conlay.add()
You can use `add()` to add <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElements</a> to other <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElements</a>.

Syntax:

```python
parent.add(child)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `child`  | child element | <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElements()</a> or one of its subclasses such as <a href="https://github.com/Salliii/conlay#box">Box()</a>, <a href="https://github.com/Salliii/conlay#label">Label()</a>, etc. |

Example:

```python
# add a LayoutElement to the main layout 
layout = Conlay()
layout.add(ThinBox(...))

# add a LayoutElement to another LayoutElement
BoldBox(...).add(ThinLabel(...))
```


### Conlay.print()
You have to call `print()` to generate and print out the layout.

Syntax:

```python
layout.print()
```

Example:

```python
layout = Conlay()
...
layout.print()
```




## LayoutElement()
The `LayoutElement()` class serves as a superclass for all other layout elements such as <a href="https://github.com/Salliii/conlay#box">Box()</a>, <a href="https://github.com/Salliii/conlay#label">Label()</a>, etc.

Syntax:

```python
element = LayoutElement(x, y, w, h, border)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `w`      | Elements width | `int` |
| `h`      | Elements height | `int` |
| `border` | Borders character set | <a href="https://github.com/Salliii/conlay#border">Border()</a> or one of its subclasses such as <a href="https://github.com/Salliii/conlay#bold">Bold()</a> or <a href="https://github.com/Salliii/conlay#thin">Thin()</a> |

Example:

```python
from conlay import *

layout = Conlay()

element = LayoutElement(0, 0, 30, 5, Thin())
layout.add(element)

layout.print()
```

Console output:

```
╭────────────────────────────╮
│                            │
│                            │
│                            │
╰────────────────────────────╯


>
```




## Box()
The `Box()` class is a subclass of the <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElement()</a> class and is used to create a simple box.

Syntax:

```python
element = Box(x, y, w, h, border)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `w`      | Elements width | `int` |
| `h`      | Elements height | `int` |
| `border` | Borders character set | <a href="https://github.com/Salliii/conlay#border">Border()</a> or one of its subclasses such as <a href="https://github.com/Salliii/conlay#bold">Bold()</a> or <a href="https://github.com/Salliii/conlay#thin">Thin()</a> |

Example:

```python
from conlay import *

layout = Conlay()

box = Box(0, 0, 30, 5, Thin())
layout.add(box)

layout.print()
```

Console output:

```
╭────────────────────────────╮
│                            │
│                            │
│                            │
╰────────────────────────────╯


>
```




## ThinBox()
The `ThinBox()` class is a subclass of the <a href="https://github.com/Salliii/conlay#box">Box()</a> class and is used to create a simple box with a <a href="https://github.com/Salliii/conlay#thin">Thin()</a> Border.

Syntax:

```python
element = ThinBox(x, y, w, h)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `w`      | Elements width | `int` |
| `h`      | Elements height | `int` |

Example:

```python
from conlay import *

layout = Conlay()

thinbox = ThinBox(0, 0, 30, 5)
layout.add(thinbox)

layout.print()
```

Console output:

```
╭────────────────────────────╮
│                            │
│                            │
│                            │
╰────────────────────────────╯


>
```




## BoldBox()
The `BoldBox()` class is a subclass of the <a href="https://github.com/Salliii/conlay#box">Box()</a> class and is used to create a simple box with a <a href="https://github.com/Salliii/conlay#bold">Bold()</a> Border.

Syntax:

```python
element = BoldBox(x, y, w, h)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `w`      | Elements width | `int` |
| `h`      | Elements height | `int` |

Example:

```python
from conlay import *

layout = Conlay()

boldbox = BoldBox(0, 0, 30, 5)
layout.add(boldbox)

layout.print()
```

Console output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            ┃
┃                            ┃
┃                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


>
```




## Label()
The `Label()` class is a subclass of the <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElement()</a> class and is used to create a simple box.

Syntax:

```python
element = Label(x, y, text, border)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `text`   | Text content | `str` |
| `border` | Borders character set | <a href="https://github.com/Salliii/conlay#border">Border()</a> or one of its subclasses such as <a href="https://github.com/Salliii/conlay#bold">Bold()</a> or <a href="https://github.com/Salliii/conlay#thin">Thin()</a> |

```python
from conlay import *

layout = Conlay()

label = Label(0, 0, "this is a test", Thin())
layout.add(label)

layout.print()
```

Console output:

```
╭──────────────╮
│this is a test│
╰──────────────╯


>
```




## ThinLabel()
The `ThinLabel()` class is a subclass of the <a href="https://github.com/Salliii/conlay#label">Label()</a> class and is used to create a simple label with a <a href="https://github.com/Salliii/conlay#thin">Thin()</a> Border.

Syntax:

```python
element = ThinLabel(x, y, text)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `text`   | Text content | `str` |

```python
from conlay import *

layout = Conlay()

thinlabel = ThinLabel(0, 0, "this is a test")
layout.add(thinlabel)

layout.print()
```

Console output:

```
╭──────────────╮
│this is a test│
╰──────────────╯


>
```




## BoldLabel()
The `BoldLabel()` class is a subclass of the <a href="https://github.com/Salliii/conlay#label">Label()</a> class and is used to create a simple label with a <a href="https://github.com/Salliii/conlay#bold">Bold()</a> Border.

Syntax:

```python
element = BoldLabel(x, y, text)
```

| argument | description | expected type |
| :------- | :---------- | :------------ |
| `x`      | Relative x-position to its parent element | `int` |
| `y`      | Relative y-position to its parent element | `int` |
| `text`   | Text content | `str` |

```python
from conlay import *

layout = Conlay()

boldlabel = BoldLabel(0, 0, "this is a test")
layout.add(boldlabel)

layout.print()
```

Console output:

```
┏━━━━━━━━━━━━━━┓
┃this is a test┃
┗━━━━━━━━━━━━━━┛


>
```




## Cursor
The `Cursor` class provides a few functions for simple <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape</a> cursor actions.


### Cursor.setPosition()
Set the cursor to a specific position. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[<y>;<x>H`.

Syntax:

```python
Cursor.setPosition(x, y)
```

Example:

```python
Cursor.setPosition(10, 5)
```


### Cursor.shiftHorizontal()
Move the cursor along the X axis. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[<x>D` and `\x1b[<x>C`.

Syntax:

```python
Cursor.shiftHorizontal(x)
```

Example:

```python
# move the cursor 10 collumns to the right
Cursor.shiftHorizontal(10)

# move the cursor 5 collumns to the left
Cursor.shiftHorizontal(-5)
```


### Cursor.shiftVertical()
Move the cursor along the Y axis. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[<y>A` and `\x1b[<y>B`.

Syntax:

```python
Cursor.shiftVertical(y)
```

Example:

```python
# move the cursor 10 collumns down
Cursor.shiftVertical(10)

# move the cursor 5 collumns up
Cursor.shiftVertical(-5)
```


### Cursor.hide()
Hides the cursor. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[?25l`.

Syntax:

```python
Cursor.hide()
```


### Cursor.show()
Shows the cursor. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[?25h`.

Syntax:

```python
Cursor.show()
```




## Console
The `Console` class provides a few functions for simple <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape</a> console actions.


### Console.reset()
This Function resets the console. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1bc`.

Syntax:

```python
Console.reset()
```


### Console.clear()
This Function clears the console. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[3J`.

Syntax:

```python
Console.clear()
```


### Console.eraseLineToEnd()
Erase the line from the cursor position to the end. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[0K`.

Syntax:

```python
Console.eraseLineToEnd()
```


### Console.eraseLineFromStart()
Erase the line from start to the cursor position. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[1K`.

Syntax:

```python
Console.eraseLineFromStart()
```


### Console.eraseLine()
Erase the line. The <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797">Ansi Escape Sequence</a> used for this command is `\x1b[2K`.

Syntax:

```python
Console.eraseLine()
```




## Color
The `Color` class allows you to set the foreground and background color using the <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes">Ansi Escape Color Codes</a>.


### Color.Bg
The `Color.Bg` class provides a few predefined background <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes">Ansi Escape Color Codes</a>.

| Variable Name   | rgb values    | ansi escape sequence     |
| :------------   | :---------    | :-------------------     |
| Color.Bg.black  |   0,   0,   0 | `\x1b[49m`               |
| Color.Bg.black  |   0,   0,   0 | `\x1b[48;2;0;0;0m`       |
| Color.Bg.white  | 255, 255, 255 | `\x1b[48;2;255;255;255m` |
| Color.Bg.red    | 205,  49,  49 | `\x1b[48;2;205;49;49m`   |
| Color.Bg.green  |  13, 188, 121 | `\x1b[48;2;13;188;121m`  |
| Color.Bg.blue   |  36, 114, 200 | `\x1b[48;2;36;114;200m`  |
| Color.Bg.yellow | 229, 229,  16 | `\x1b[48;2;229;229;16m`  |
| Color.Bg.purple | 188,  63, 188 | `\x1b[48;2;188;63;188m`  |
| Color.Bg.cyan   |  17, 168, 205 | `\x1b[48;2;17;168;205m`  |


### Color.Bg.rgb()
This function takes three arguments `r, g, b` and returns a customized background <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes">Ansi Escape Color Code</a>

Syntax:

```python
Color.Bg.rgb(r, g, b)
```

Example:

```python
>>> Color.Bg.rgb(255, 0, 100)
'\x1b[48;2;255;0;100m'
```


### Color.Fg
The `Color.Fg` class provides a few predefined foreground <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes">Ansi Escape Color Codes</a>.

| Variable Name   | rgb values    | ansi escape sequence     |
| :------------   | :---------    | :-------------------     |
| Color.Bg.black  |   0,   0,   0 | `\x1b[39m`               |
| Color.Fg.black  |   0,   0,   0 | `\x1b[38;2;0;0;0m`       |
| Color.Fg.white  | 255, 255, 255 | `\x1b[38;2;255;255;255m` |
| Color.Fg.red    | 205,  49,  49 | `\x1b[38;2;205;49;49m`   |
| Color.Fg.green  |  13, 188, 121 | `\x1b[38;2;13;188;121m`  |
| Color.Fg.blue   |  36, 114, 200 | `\x1b[38;2;36;114;200m`  |
| Color.Fg.yellow | 229, 229,  16 | `\x1b[38;2;229;229;16m`  |
| Color.Fg.purple | 188,  63, 188 | `\x1b[38;2;188;63;188m`  |
| Color.Fg.cyan   |  17, 168, 205 | `\x1b[38;2;17;168;205m`  |


### Color.Fg.rgb()
This function takes three arguments `r, g, b` and returns a customized foreground <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes">Ansi Escape Color Code</a>

Syntax:

```python
Color.Fg.rgb(r, g, b)
```

Example:

```python
>>> Color.Fg.rgb(255, 0, 100)
'\x1b[38;2;255;0;100m'
```




## Border
The `Border()` class and its subclasses serve as a character set and define the required Unicode characters.

| class attributes | unicode characters |
| :--------------- | :----------------- |
| `vertical`       | n/a                |
| `horizontal`     | n/a                |
| `top_left`       | n/a                |
| `top_right`      | n/a                |
| `bottom_left`    | n/a                |
| `bottom_right`   | n/a                |




## Thin()
The `Thin()` class is a subclass of <a href="https://github.com/Salliii/conlay#border">Border()</a> and serves as a character set and defines the required thin Unicode characters.

| class attributes | unicode characters |
| :--------------- | :----------------- |
| `vertical`       | `\u2503`           |
| `horizontal`     | `\u2501`           |
| `top_left`       | `\u250F`           |
| `top_right`      | `\u2513`           |
| `bottom_left`    | `\u2517`           |
| `bottom_right`   | `\u251B`           |




## Bold()
The `Bold()` class is a subclass of <a href="https://github.com/Salliii/conlay#border">Border()</a> and serves as a character set and defines the required bold Unicode characters.

| class attributes | unicode characters |
| :--------------- | :----------------- |
| `vertical`       | `\u2502`           |
| `horizontal`     | `\u2500`           |
| `top_left`       | `\u256D`           |
| `top_right`      | `\u256E`           |
| `bottom_left`    | `\u2570`           |
| `bottom_right`   | `\u256F`           |




## Summary

- <a href="https://github.com/Salliii/conlay#conlay">Conlay()</a>
  - <a href="https://github.com/Salliii/conlay#conlayadd">_add()_</a>
  - <a href="https://github.com/Salliii/conlay#conlayprint">_print()_</a>

##### Elements
- <a href="https://github.com/Salliii/conlay#layoutelement">LayoutElement()</a>
- <a href="https://github.com/Salliii/conlay#box">Box()</a>
- <a href="https://github.com/Salliii/conlay#thinbox">ThinBox()</a>
- <a href="https://github.com/Salliii/conlay#boldbox">BoldBox()</a>
- <a href="https://github.com/Salliii/conlay#label">Label()</a>
- <a href="https://github.com/Salliii/conlay#thinlabel">ThinLabel()</a>
- <a href="https://github.com/Salliii/conlay#boldlabel">BoldLabel()</a>

##### Cursor & Console
- <a href="https://github.com/Salliii/conlay#cursor">Cursor</a>
  - <a href="https://github.com/Salliii/conlay#cursorsetposition">_setPosition()_</a>
  - <a href="https://github.com/Salliii/conlay#cursorshifthorizontal">_shiftHorizontal()_</a>
  - <a href="https://github.com/Salliii/conlay#cursorshiftvertical">_shiftVertical()_</a>
  - <a href="https://github.com/Salliii/conlay#cursorhide">_hide()_</a>
  - <a href="https://github.com/Salliii/conlay#cursorshow">_show()_</a>

- <a href="https://github.com/Salliii/conlay#console">Console</a>
  - <a href="https://github.com/Salliii/conlay#consolereset">_reset()_</a>
  - <a href="https://github.com/Salliii/conlay#consoleclear">_clear()_</a>
  - <a href="https://github.com/Salliii/conlay#consoleeraselinetoend">_eraseLineToEnd()_</a>
  - <a href="https://github.com/Salliii/conlay#consoleeraselinefromstart">_eraseLineFromStart()_</a>
  - <a href="https://github.com/Salliii/conlay#consoleeraseline">_eraseLine()_</a>

##### Coloring
- <a href="https://github.com/Salliii/conlay#color">Color</a>
  - <a href="https://github.com/Salliii/conlay#colorbg">Bg</a>
    - <a href="https://github.com/Salliii/conlay#colorbgrgb">_rgb()_</a>
  - <a href="https://github.com/Salliii/conlay#colorfg">Fg</a>
    - <a href="https://github.com/Salliii/conlay#colorfgrgb">_rgb()_</a>

##### Border & Border Types
- <a href="https://github.com/Salliii/conlay#border">Border</a>
- <a href="https://github.com/Salliii/conlay#bold">Bold</a>
- <a href="https://github.com/Salliii/conlay#thin">Thin</a>


## License

Licensed under the <a href="https://github.com/Salliii/conlay/blob/main/LICENSE">MIT License</a>.




<!-- shields -->
[shields-pypi_version]: https://img.shields.io/pypi/v/conlay?label=PyPi%20Version&style=for-the-badge
[shields-issues]: https://img.shields.io/github/issues/Salliii/conlay?style=for-the-badge
[shields-license]: https://img.shields.io/github/license/Salliii/conlay?style=for-the-badge

<!-- url -->
[url-pypi_version]: https://pypi.org/project/conlay/
[url-issues]: https://github.com/Salliii/conlay/issues
[url-license]: https://github.com/Salliii/conlay/blob/main/LICENSE