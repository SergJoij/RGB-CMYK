from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSpinBox, QLabel
from PyQt5.QtCore import QCoreApplication
import sys


def okrugl(c, znak):
    if int((c * (10 ** (znak + 1)) // 1) % 10) > 4:
        c = c + (10 ** -znak)
    c = (c * (10 ** znak) // 1) / (10 ** znak)
    return c


class Convert_colors_cmyk_to_rgb:
    def __init__(self, cyan, magenta, yellow, key):
        self.r = 0
        self.g = 0
        self.b = 0
        self.c = cyan
        self.m = magenta
        self.y = yellow
        self.k = key

    def convert_colors(self):
        rgb_scale = 255
        if (self.c, self.m, self.y, self.k) == (0, 0, 0, 1.0):
            self.r = self.g = self.b = 0
        else:
            # ПЕРЕВОД ИЗ cmyk [0,1] в rgb [0,255]
            min_cmy = self.k
            self.r = self.c * (1 - min_cmy) + min_cmy
            self.g = self.m * (1 - min_cmy) + min_cmy
            self.b = self.y * (1 - min_cmy) + min_cmy
            # извлечение к [0, 256]
            self.r = rgb_scale * (1 - self.r)
            self.g = rgb_scale * (1 - self.g)
            self.b = rgb_scale * (1 - self.b)

    def get_red(self):
        return int(okrugl(self.r, 0))

    def get_green(self):
        return int(okrugl(self.g, 0))

    def get_blue(self):
        return int(okrugl(self.b, 0))


class Convert_colors_rgb_to_cmyk:
    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue
        self.c = 0.0
        self.m = 0.0
        self.y = 0.0
        self.k = 0.0

    def convert_colors(self):
        rgb_scale = 255
        if (self.r, self.g, self.b) == (0, 0, 0):
            self.c = self.m = self.y = 0
            self.k = 1.0
        else:
            # ПЕРЕВОД ИЗ rgb [0,255] в cmy [0,1]
            self.c = 1 - self.r / rgb_scale
            self.m = 1 - self.g / rgb_scale
            self.y = 1 - self.b / rgb_scale
            # Из [0,255] к [0, 1]
            min_cmy = min(self.c, self.m, self.y)
            self.c = (self.c - min_cmy) / (1 - min_cmy)
            self.m = (self.m - min_cmy) / (1 - min_cmy)
            self.y = (self.y - min_cmy) / (1 - min_cmy)
            self.k = min_cmy

    def get_cyan(self):
        return self.c

    def get_magenta(self):
        return self.m

    def get_yellow(self):
        return self.y

    def get_key(self):
        return self.k


class Window(QMainWindow):
    def __init__(self, ra, ga, ba):
        super().__init__()
        self.r = ra
        self.g = ga
        self.b = ba
        self.title = "Converter"
        self.top = 150
        self.left = 150
        self.height = 550
        self.c = 0.0
        self.m = 0.0
        self.y = 0.0
        self.k = 0.0

        self.width = 360
        self.status_of_convert = True # RGB, кнопка "Изменить" переключает это значение
        # Становится True сразу после нажатия на кнопку "Изменить", а после превращается снова в false
        self.status_of_change = False

        quit_b = QPushButton('Выход', self)
        quit_b.clicked.connect(QCoreApplication.instance().quit)
        quit_b.resize(quit_b.sizeHint())
        quit_b.move(20, 20)

        self.box_red = QSpinBox(self)
        self.box_red.setMaximum(255)
        self.box_red.move(20, 70)
        self.box_red.valueChanged.connect(self.color_changed_red)
        self.box_red.show()

        self.box_green = QSpinBox(self)
        self.box_green.setMaximum(255)
        self.box_green.move(130, 70)
        self.box_green.valueChanged.connect(self.color_changed_green)
        self.box_green.show()

        self.box_blue = QSpinBox(self)
        self.box_blue.setMaximum(255)
        self.box_blue.move(240, 70)
        self.box_blue.valueChanged.connect(self.color_changed_blue)
        self.box_blue.show()

        self.box_cyan = QSpinBox(self)
        self.box_cyan.setMaximum(100)
        self.box_cyan.move(20, 70)
        self.box_cyan.valueChanged.connect(self.color_changed_cyan)
        self.box_cyan.hide()

        self.box_magenta = QSpinBox(self)
        self.box_magenta.setMaximum(100)
        self.box_magenta.move(130, 70)
        self.box_magenta.valueChanged.connect(self.color_changed_magenta)
        self.box_magenta.hide()

        self.box_yellow = QSpinBox(self)
        self.box_yellow.setMaximum(100)
        self.box_yellow.move(240, 70)
        self.box_yellow.valueChanged.connect(self.color_changed_yellow)
        self.box_yellow.hide()

        self.box_key = QSpinBox(self)  # width = 100
        self.box_key.setMaximum(100)
        self.box_key.move(130, 120)
        self.box_key.valueChanged.connect(self.color_changed_key)
        self.box_key.hide()

        self.label_cyan = QLabel(self)
        self.label_cyan.move(20, 370)
        self.label_cyan.setText("non")
        self.label_cyan.show()
        self.label_cyan.setFont(QFont("Arial", 10))

        self.label_magenta = QLabel(self)
        self.label_magenta.move(20, 410)
        self.label_magenta.setText("non")
        self.label_magenta.show()
        self.label_magenta.setFont(QFont("Arial", 10))

        self.label_yellow = QLabel(self)
        self.label_yellow.move(20, 450)
        self.label_yellow.setText("non")
        self.label_yellow.show()
        self.label_yellow.setFont(QFont("Arial", 10))

        self.label_key = QLabel(self)
        self.label_key.move(20, 490)
        self.label_key.setText("non")
        self.label_key.show()
        self.label_key.setFont(QFont("Arial", 10))

        self.label_red = QLabel(self)
        self.label_red.move(25, 45)
        self.label_red.setText("red")
        self.label_red.setFont(QFont("Arial", 10))
        self.label_red.show()
        self.label_green = QLabel(self)
        self.label_green.move(135, 45)
        self.label_green.setText("green")
        self.label_green.setFont(QFont("Arial", 10))
        self.label_green.show()
        self.label_blue = QLabel(self)
        self.label_blue.move(245, 45)
        self.label_blue.setText("blue")
        self.label_blue.setFont(QFont("Arial", 10))
        self.label_blue.show()

        self.change_b = QPushButton('Изменить', self)
        self.change_b.clicked.connect(self.change_converter)
        self.change_b.move(130, 20) #print(self.change_b.width())

        self.InitWindow()
        self.paintEvent(self.InitWindow())

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        if self.status_of_convert:  # Если RGB -> CMYK
            if not self.status_of_change: # Если только что не меняли режим...
                colors = Convert_colors_rgb_to_cmyk(self.r, self.g, self.b)
                colors.convert_colors()
                self.c = colors.get_cyan()
                self.m = colors.get_magenta()
                self.y = colors.get_yellow()
                self.k = colors.get_key()

                self.box_red.setValue(self.r)
                self.box_green.setValue(self.g)
                self.box_blue.setValue(self.b)
                self.box_cyan.setValue(int(okrugl(100 * self.c, 0)))
                self.box_magenta.setValue(int(okrugl(100 * self.m, 0)))
                self.box_yellow.setValue(int(okrugl(100 * self.y, 0)))
                self.box_key.setValue(int(okrugl(100 * self.k, 0)))

            self.label_cyan.setText("cyan \t" + str(int(okrugl(100 * self.c, 0))))
            self.label_magenta.setText("magenta \t" + str(int(okrugl(100 * self.m, 0))))
            self.label_yellow.setText("yellow \t" + str(int(okrugl(100 * self.y, 0))))
            self.label_key.setText("key \t" + str(int(okrugl(100 * self.k, 0))))
        else:  # Если CMYK -> RGB
            if not self.status_of_change: # Если только что не меняли режим...
                colors = Convert_colors_cmyk_to_rgb(self.c, self.m, self.y, self.k)
                colors.convert_colors()
                self.r = int(colors.get_red())
                self.b = int(colors.get_blue())
                self.g = int(colors.get_green())

                self.box_red.setValue(self.r)
                self.box_green.setValue(self.g)
                self.box_blue.setValue(self.b)
                self.box_cyan.setValue(int(okrugl(100 * self.c, 0)))
                self.box_magenta.setValue(int(okrugl(100 * self.m, 0)))
                self.box_yellow.setValue(int(okrugl(100 * self.y, 0)))
                self.box_key.setValue(int(okrugl(100 * self.k, 0)))

            self.label_red.setText("red   \t" + str(self.r))
            self.label_green.setText("green   \t" + str(self.g))
            self.label_blue.setText("blue   \t" + str(self.b))

        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor().fromCmykF(self.c, self.m, self.y, self.k))
        painter.setBrush(QColor().fromCmykF(self.c, self.m, self.y, self.k))
        painter.drawRect(80, 160, 100, 200)

        painter.setPen(QColor(self.r, self.g, self.b))
        painter.setBrush(QColor(self.r, self.g, self.b))
        painter.drawRect(180, 160, 100, 200)
        painter.end()


    def change_converter(self):
        if self.status_of_convert:  # Если сейчас RGB -> CMYK, то меняем
            # скрываем и открываем нужное
            self.box_cyan.show()
            self.box_magenta.show()
            self.box_yellow.show()
            self.box_key.show()

            self.box_red.hide()
            self.box_green.hide()
            self.box_blue.hide()

            self.label_red.move(20, 370)
            self.label_green.move(20, 410)
            self.label_blue.move(20, 450)

            self.label_cyan.move(25, 45)
            self.label_cyan.setText("cyan")
            self.label_magenta.move(135, 45)
            self.label_magenta.setText("magenta")
            self.label_yellow.move(245, 45)
            self.label_yellow.setText("yellow")
            self.label_key.move(135, 95)
            self.label_key.setText("key")
            # Меняем статус на smyk -> rgb
            self.status_of_convert = False
        else:  # Если сейчас CMYK -> RGB, то меняем
            self.box_cyan.hide()
            self.box_magenta.hide()
            self.box_yellow.hide()
            self.box_key.hide()

            self.box_red.show()
            self.box_green.show()
            self.box_blue.show()

            self.label_red.move(25, 45)
            self.label_red.setText("red")
            self.label_green.move(135, 45)
            self.label_green.setText("green")
            self.label_blue.move(245, 45)
            self.label_blue.setText("blue")

            self.label_cyan.move(20, 370)
            self.label_magenta.move(20, 410)
            self.label_yellow.move(20, 450)
            self.label_key.move(20, 490)
            # Изменяем размер окна (по умолчанию)
            self.status_of_convert = True
        self.status_of_change = True
        self.update()

    def color_changed_red(self):
        self.status_of_change = False
        self.r = self.box_red.value()
        self.update()

    def color_changed_green(self):
        self.status_of_change = False
        self.g = self.box_green.value()
        self.update()

    def color_changed_blue(self):
        self.status_of_change = False
        self.b = self.box_blue.value()
        self.update()

    def color_changed_cyan(self):
        self.status_of_change = False
        self.c = self.box_cyan.value() / 100
        self.update()

    def color_changed_magenta(self):
        self.status_of_change = False
        self.m = self.box_magenta.value() / 100
        self.update()

    def color_changed_yellow(self):
        self.status_of_change = False
        self.y = self.box_yellow.value() / 100
        self.update()

    def color_changed_key(self):
        self.status_of_change = False
        self.k = self.box_key.value() / 100
        self.update()


r = 99
g = 5
b = 207
app1 = QApplication(sys.argv)
window = Window(r, g, b)
window.show()
sys.exit(app1.exec())
