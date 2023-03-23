import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget


class Board(QFrame):

    # BoardWidth = GameWindow.Width // Segment.SegmentSize
    # BoardHeight = GameWindow.Height // Segment.SegmentSize

    def __init__(self, parent):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        # self.start()

    def paintEvent(self, event):
        painter = QPainter(self)

        for x in range(int(self.width() / 2), self.width(), 30):
            painter.drawLine(x, 0, x, self.height())
        # for (int x=width / 2; x > 0; x -= 30){ // цикл от центра до леваого края
        # g.drawLine(x, 0, x, height); // вертикальная линия
        # }
        #
        # for (int y=height / 2; y < height; y += 30){ // цикл от центра до верхнего края
        # g.drawLine(0, y, width, y); // горизонтальная линия
        # }
        #
        # for (int y=height / 2; y > 0; y -= 30){ // цикл от центра до левого края
        # g.drawLine(0, y, width, y); // горизонтальная линия
        # }


class Figure(object):
    one_point = 0
    two_point_vertical = 1
    two_point_horizontal = 2
    three_point_horizontal = 3
    big_corner_left = 4
    small_corner_right = 4
    two_x_two_square = 5
    three_x_three_square = 6
    four_point_vertical = 7
    four_point_horizontal = 8
    arrow = 9
    l_figure = 10


class GameWindow(QMainWindow):
    Width = 1000
    Height = 800

    def __init__(self):
        super().__init__()
        self.board = None
        self.initUI()

    def initUI(self):
        self.board = Board(self)

        self.board.setGeometry(0, 0, GameWindow.Width, GameWindow.Height)

        self.resize(GameWindow.Width, GameWindow.Height)
        self.center()
        self.setWindowTitle('MyGame')

        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameWindow()
    sys.exit(app.exec_())
