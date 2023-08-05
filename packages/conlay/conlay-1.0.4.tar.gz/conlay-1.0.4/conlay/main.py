

class Border:
    """ clear border unicode character set """
    
    vertical = u""
    horizontal = u""
    top_left = u""
    top_right = u""
    bottom_left = u""
    bottom_right = u""


class Bold(Border):
    """ bold border unicode character set """

    def __init__(self) -> None:
        self.vertical = u"\u2503"
        self.horizontal = u"\u2501"
        self.top_left = u"\u250F"
        self.top_right = u"\u2513"
        self.bottom_left = u"\u2517"
        self.bottom_right = u"\u251B"


class Thin(Border):
    """ thin border unicode character set """

    def __init__(self) -> None:
        self.vertical = u"\u2502"
        self.horizontal = u"\u2500"
        self.top_left = u"\u256D"
        self.top_right = u"\u256E"
        self.bottom_left = u"\u2570"
        self.bottom_right = u"\u256F"




class Color:
    """ color set """
    
    # clear color
    clear = "\x1b[0m"


    class Bg:
        """ background color set """

        # clear background color
        clear = "\x1b[49m"

        # function that returns a properly formatted ansi escape code for the background color
        def rgb(r:int, g:int, b:int) -> str:
            return "\x1b[48;2;{r};{g};{b}m".format(r=r, g=g, b=b)
        
        # default color set
        black = rgb(0, 0, 0)
        white = rgb(255, 255, 255)
        red = rgb(205, 49, 49)
        green = rgb(13, 188, 121)
        blue = rgb(36, 114, 200)
        yellow = rgb(229, 229, 16)
        purple = rgb(188, 63, 188)
        cyan = rgb(17, 168, 205)
    

    class Fg:
        """ foreground color set """

        # clear background color
        clear = "\x1b[49m"

        # function that returns a properly formatted ansi escape code for the foreground color
        def rgb(r:int, g:int, b:int) -> str:
            return "\x1b[38;2;{r};{g};{b}m".format(r=r, g=g, b=b)
        
        # default color set
        black = rgb(0, 0, 0)
        white = rgb(255, 255, 255)
        red = rgb(205, 49, 49)
        green = rgb(13, 188, 121)
        blue = rgb(36, 114, 200)
        yellow = rgb(229, 229, 16)
        purple = rgb(188, 63, 188)
        cyan = rgb(17, 168, 205)




class Console:
    """ ansi escape sequences for console """

    def reset() -> int:
        """ reset console and clear history """

        print("\x1bc", end="")
        return 1


    def clear() -> int:
        """ clear console and keep history"""

        print("\x1b[3J", end="")
        return 1
    

    def eraseLineToEnd() -> int:
        """ erase line from cursor to end """

        print("\x1b[0K", end="")
        return 1
    

    def eraseLinefromStart() -> int:
        """ erase line from start to cursor """

        print("\x1b[1K", end="")
        return 1
    

    def eraseLine() -> int:
        """ erase full line """

        print("\x1b[2K", end="")
        return 1




class Cursor:
    """ ansi escape sequences for cursor """

    def setPosition(x:int, y:int) -> int:
        """ set cursor to (x, y) coords """
        print("\x1b[{y};{x}H".format(y=y, x=x), end="")
        return 1


    def shiftHorizontal(sh: int) -> int:
        """ shift cursor position on x axis
            value > 0: shift to right
            value < 0: shift to left """

        if sh < 0:
            print("\x1b[{sh}D".format(sh=sh*-1), end="")
            return 1
        elif sh > 0:
            print("\x1b[{sh}C".format(sh=sh), end="")
            return 1
        return 0


    def shiftVertikal(sh:int) -> int:
        """ shift cursor position on y axis
            value > 0: shift down
            value < 0: shift up """

        if sh < 0:
            print("\x1b[{sh}A".format(sh=sh*-1), end="")
            return 1
        elif sh > 0:
            print("\x1b[{sh}B".format(sh=sh), end="")
            return 1
        return 0
    

    def hide() -> int:
        """ hide cursor """

        print("\x1b[?25l", end="")
        return 1
    
    
    def show() -> int:
        """ show cursor """

        print("\x1b[?25h", end="")
        return 1




class Conlay:
    """ main layout """

    # child list
    childs = []

    # reset console and set cursor to (0, 0) after class call
    Console.reset()
    Cursor.setPosition(1, 1)

    def __init__(self) -> None:
        # class attributes
        self.relative_x = int()
        self.relative_y = int()
        self.absolute_x = int()
        self.absolute_y = int()
        self.width = int()
        self.min_width = int()
        self.max_width = int()
        self.height = int()
        self.min_height = int()
        self.max_height = int()
        self.zindex = int()
        self.padding_x = int()
        self.padding_y = int()
        self.text = str()
        self.background = bool()
        self.background_color = Color.clear
        self.border_color = Color.clear
        self.text_color = Color.clear


    def __sort_childs_by_zindex__(self, reverse=False) -> list:
        """ sort child list by elements zindex attribute """
        
        return list(sorted(self.childs, key=lambda child: child.zindex, reverse=reverse))
    

    def __sort_childs_by_height__(self, reverse=False) -> list:
        """ sort child list by elements height attribute """

        return list(sorted(self.childs, key=lambda child: child.height, reverse=reverse))
    

    def __sort_childs_by_width__(self, reverse=False) -> list:
        """ sort child list by elements width attribute """

        return list(sorted(self.childs, key=lambda child: child.width, reverse=reverse))


    def __get_final_cursor_position__(self) -> int:
        """ calculate final cursor position """

        biggest_child = list(sorted(self.childs, key=lambda child: child.height + child.absolute_y, reverse=True))[0]
        return int(biggest_child.height + biggest_child.absolute_y) + 1


    def add(self, element:None) -> int: 
        """ add element to layout element """

        # set childs zindex to self zindex + 1
        element.zindex = self.zindex + 1
        
        # calculate childs absolute position based on self position, padding and childs relative position
        element.absolute_x = self.absolute_x + self.padding_x + element.relative_x
        element.absolute_y = self.absolute_y + self.padding_y + element.relative_y

        # calculate childs height, width based on min- and max- width/height
        if self.min_width != self.max_width and self.min_width < self.max_width and self.min_width >= 0:
            element.width = min(max(element.min_width, element.width), element.max_width)
            element.height = min(max(element.min_height, element.height), element.max_height)

        # append child to layouts child list
        self.childs.append(element)
        
        return 1
    

    def print(self) -> int:
        """ print layout """

        for element in self.__sort_childs_by_zindex__():
            # iterate through elements in child list sorted by zindex

            # try elements pre-printing function
            try:
                element.__preprint__()
            except AttributeError:
                pass
            

            # iterate through y axis
            for y in range(element.height):

                # set cursors position
                Cursor.setPosition(element.absolute_x, element.absolute_y + y)


                # iterate through x axis
                for x in range(element.width):

                    # print top left border
                    if x == 0 and y == 0:
                        print(element.background_color + element.border_color + element.border.top_left, end=Color.clear)
                    
                    # print bottom left border
                    elif x == 0 and y == element.height - 1:
                        print(element.background_color + element.border_color + element.border.bottom_left, end=Color.clear)
                    
                    # print top right border
                    elif x == element.width - 1 and y == 0:
                        print(element.background_color + element.border_color + element.border.top_right, end=Color.clear)

                    # print bottom right border
                    elif x == element.width - 1 and y == element.height - 1:
                        print(element.background_color + element.border_color + element.border.bottom_right, end=Color.clear)

                    # print vertical border
                    elif x == 0 or x == element.width - 1:
                        print(element.background_color + element.border_color + element.border.vertical, end=Color.clear)
                    
                    # print horizontal border
                    elif y == 0 or y == element.height - 1:
                        print(element.background_color + element.border_color + element.border.horizontal, end=Color.clear)
                    
                    # background behavior
                    else:
                        if element.background:
                            print(element.background_color + element.border_color + " ", end=Color.clear)
                        else:
                            Cursor.shiftHorizontal(1)


            # try elements past-printing function
            try:
                element.__pastprint__()
            except AttributeError:
                pass
        
        # set cursor position
        Cursor.setPosition(0, self.__get_final_cursor_position__())




class LayoutElement(Conlay):
    def __init__(self, x:int, y:int, w:int, h:int, border:Border) -> None:
        super().__init__()

        self.relative_x = x + 1
        self.relative_y = y + 1
        self.width = w
        self.height = h
        self.border = border




class Box(LayoutElement):
    def __init__(self, x:int, y:int, w:int, h:int, border:Border) -> None:
        super().__init__(x, y, w, h, border)

    
    def __preprint__(self) -> int:
        return 1
    

    def __pastprint__(self) -> int:
        return 1


class ThinBox(Box):
    def __init__(self, x:int, y:int, w:int, h:int) -> None:
        super().__init__(x, y, w, h, Thin())


class BoldBox(Box):
    def __init__(self, x:int, y:int, w:int, h:int) -> None:
        super().__init__(x, y, w, h, Bold())




class Label(LayoutElement):
    def __init__(self, x:int, y:int, text:str, border:Border) -> None:
        w = len(max(text.split("\n"), key=len))
        h = len(text.split("\n"))

        super().__init__(x, y, w, h, border)

        self.text = text


    def __preprint__(self) -> int:
        self.width = self.width + self.padding_x * 2 + 2
        self.height = self.height + self.padding_y * 2 + 2

        return 1


    def __pastprint__(self) -> int:
        Cursor.setPosition(self.absolute_x + 1 + self.padding_x, self.absolute_y + 1 + self.padding_y)
        print(self.text, end="")

        return 1


class ThinLabel(Label):
    def __init__(self, x:int, y:int, text:str) -> None:
        super().__init__(x, y, text, Thin())


class BoldLabel(Label):
    def __init__(self, x:int, y:int, text:str) -> None:
        super().__init__(x, y, text, Bold())