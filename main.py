import sys
from math import sin, cos, tan, pi
from random import randrange, choices

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


# https://mathworld.wolfram.com/CoinTossing.html

class helpme(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.setWindowTitle('Монетка кидать бесплатно')
        self.err_msg.setStyleSheet("color: red")
        self.setFixedSize(self.size())
        self.go.clicked.connect(self.reroll)
        self.coin_h, self.coin_r = None, None
        self.afta.valueChanged.connect(self.run)

    def run(self):
        # невозможно вычислить площадь монеты
        try:
            critical_angle = 1 / tan(self.coin_h / (self.coin_r * 2))
            edge_chance = (critical_angle - sin(critical_angle)) / \
                          (pi / 2 - (sin(critical_angle) + cos(critical_angle))) * 0.01
            tail_or_head_chance = (1 - edge_chance) / 2
            c = choices(population=[-1, 0, 1],
                        weights=[tail_or_head_chance, edge_chance, tail_or_head_chance],
                        k=int(self.amount.text()))  # орел ребро решка
            self.htc.setText(str(round(tail_or_head_chance, self.afta.value())))
            self.ec.setText(str(round(edge_chance, self.afta.value())))
            self.h.setText(str(self.coin_h))
            self.s.setText(str(round(self.coin_r * pi ** 2, self.afta.value())))
            self.h_s.setText(str(round(self.coin_r * pi * 2 * self.coin_h, self.afta.value())))
            self.heads.setText(str(c.count(-1)))
            self.tails.setText(str(c.count(1)))
            self.edges.setText(str(c.count(0)))
            self.err_msg.setText('')
        except ValueError:
            self.err_msg.setText('Введите корректное число!')
        except Exception:
            self.err_msg.setText('Неизвестная ошибка!')

    def reroll(self):
        self.coin_h, self.coin_r = randrange(1, 80), randrange(2, 160)
        while (2 * self.coin_r) <= self.coin_h:
            self.coin_r = randrange(2, 160)
        self.run()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = helpme()
    ex.show()
    sys.exit(app.exec_())
