import random
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QRadioButton


class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.screen_height = None
        self.screen_width = None
        self.main_board = None
        self.statusbar = None
        self.initUI()

    def initUI(self):
        self.main_board = Board(self, 30, 20)
        self.setCentralWidget(self.main_board)

        self.statusbar = self.statusBar()
        self.main_board.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.main_board.start()
        self.screen_width = 1000
        self.screen_height = 600

        py_choose_button1 = QRadioButton(self)
        py_choose_button1.resize(50, 50)
        py_choose_button1.move(950, 100)
        py_choose_button1.clicked.connect(self.clickMethod_1)

        py_choose_button2 = QRadioButton(self)
        py_choose_button2.resize(50, 50)
        py_choose_button2.move(950, 275)
        py_choose_button2.clicked.connect(self.clickMethod_2)

        py_choose_button3 = QRadioButton(self)
        py_choose_button3.resize(50, 50)
        py_choose_button3.move(950, 450)
        py_choose_button3.clicked.connect(self.clickMethod_3)

        self.resize(self.screen_width, self.screen_height)
        self.center()
        self.setWindowTitle('Jewelz block game')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def clickMethod_1(self):
        self.main_board.curPiece.set_figure(self.main_board.play_figures[2].piece_figure)
        self.main_board.cur_choose_index = 2
        self.update()

    def clickMethod_2(self):
        self.main_board.curPiece.set_figure(self.main_board.play_figures[1].piece_figure)
        self.main_board.cur_choose_index = 1
        self.update()

    def clickMethod_3(self):
        self.main_board.curPiece.set_figure(self.main_board.play_figures[0].piece_figure)
        self.main_board.cur_choose_index = 0
        self.update()

    @staticmethod
    def start_message():
        print("Game started")


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.play_figures = None
        self.choose_board_positions = None
        self.board = None
        self.choose_board = None
        self.num_lines_removed = None
        self.curY = None
        self.curX = None
        self.cur_choose_index = None
        self.choose_board_width = None
        self.choose_board_height = None
        self.board_height = None
        self.board_width = None
        self.curPiece = None
        self.can_place = None
        self.initBoard(width, height)

    def initBoard(self, width, height):

        self.curPiece = View_form()
        self.curPiece.set_figure(0)

        self.board_width = width
        self.board_height = height
        self.choose_board_height = height
        self.choose_board_width = 5

        self.cur_choose_index = -1
        self.can_place = False
        self.curX = -1
        self.curY = -1
        self.num_lines_removed = 0
        self.board = []
        self.choose_board = []
        self.choose_board_positions = [[self.choose_board_width // 2, self.choose_board_height // 5],
                                       [self.choose_board_width // 2, self.choose_board_height // 2],
                                       [self.choose_board_width // 2, self.choose_board_height * 4 // 5 + 1]]
        self.play_figures = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.clear_board()

    def figure_on_position_choose_board(self, x, y):
        return self.choose_board[(y * self.choose_board_width) + x]

    def figure_on_position_board(self, x, y):
        return self.board[(y * self.board_width) + x]

    def set_figure_at_board(self, x, y, figure):
        self.board[(y * self.board_width) + x] = figure

    def set_figure_at_choose_board(self, x, y, figure):
        self.choose_board[(y * self.choose_board_width) + x] = figure

    def square_width(self):
        return self.contentsRect().width() // (self.board_width + self.choose_board_width + 3)

    def square_height(self):
        return self.contentsRect().height() // self.board_height

    def start(self):

        self.num_lines_removed = 0
        self.clear_board()

        self.msg2Statusbar.emit(str(self.num_lines_removed))

        for i in range(3):
            self.set_play_figure(i)

    def set_play_figure(self, index):
        form = View_form()
        form.set_random_figure()
        self.play_figures.insert(index, form)
        return form

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - self.board_height * self.square_height()

        for i in range(self.board_height):
            for j in range(self.board_width):
                shape = self.figure_on_position_board(j, self.board_height - i - 1)
                self.draw_square(painter,
                                 rect.left() + j * self.square_width(),
                                 boardTop + i * self.square_height(), shape, self.square_width(), self.square_height(),
                                 0)

        for i in range(self.choose_board_height):
            for j in range(self.choose_board_width):
                shape = self.figure_on_position_choose_board(j, self.board_height - i - 1)
                self.draw_square(painter,
                                 rect.left() + self.board_width * self.square_width() + j * self.square_width(),
                                 boardTop + i * self.square_height(), shape, self.square_width(), self.square_height(),
                                 0)

        if self.curPiece.figure() != Figure.No_Figure and self.can_place:

            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.draw_square(painter, rect.left() + x * self.square_width(),
                                 boardTop + (self.board_height - y - 1) * self.square_height(),
                                 self.curPiece.figure(), self.square_width(), self.square_height(), 0)

        for j in range(3):
            if self.choose_board[j] != Figure.No_Figure:
                for i in range(4):
                    x = self.board_width + self.choose_board_positions[j][0] + self.play_figures[j].x(i)
                    y = self.choose_board_positions[j][1] - self.play_figures[j].y(i)
                    if self.cur_choose_index == j:
                        self.draw_square(painter, rect.left() + x * self.square_width(),
                                         boardTop + (self.board_height - y - 1) * self.square_height(),
                                         self.play_figures[j].piece_figure, self.square_width(), self.square_height(),
                                         1)
                    else:
                        self.draw_square(painter, rect.left() + x * self.square_width(),
                                         boardTop + (self.board_height - y - 1) * self.square_height(),
                                         self.play_figures[j].piece_figure, self.square_width(), self.square_height(),
                                         0)

    def mousePressEvent(self, event):
        self.can_place = True
        if event.button() == Qt.LeftButton:
            if event.pos().x() < self.board_width * self.square_width():
                self.mouse_place_click(event.pos().x(), event.pos().y())
                self.set_piece()
                self.update()
                self.can_place = False

    def check_place(self, check_x, check_y):
        for i in range(4):
            x = check_x + self.curPiece.x(i)
            y = check_y - self.curPiece.y(i)
            if self.figure_on_position_board(x, y) != Figure.No_Figure:
                self.can_place = False

    def set_piece(self):

        if self.can_place:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.set_figure_at_board(x, y, self.curPiece.figure())

            self.play_figures.pop(self.cur_choose_index)
            self.set_play_figure(self.cur_choose_index)
            self.curPiece.set_figure(self.play_figures[self.cur_choose_index].piece_figure)

            self.remove_full_lines()

    def clear_board(self):

        for i in range(self.board_height * self.board_width):
            self.board.append(Figure.No_Figure)

        for i in range(self.choose_board_height * self.choose_board_width):
            self.choose_board.append(Figure.Point_Figure2)

    def remove_full_lines(self):

        number_of_full_lines = 0
        rows_to_remove = []

        for i in range(self.board_height):
            n = 0
            for j in range(self.board_width):
                if not self.figure_on_position_board(j, i) == Figure.No_Figure:
                    n = n + 1

            if n == self.board_width:
                rows_to_remove.append(i)

        for m in rows_to_remove:
            for k in range(self.board_width):
                self.set_figure_at_board(k, m, Figure.No_Figure)

        number_of_full_lines = number_of_full_lines + len(rows_to_remove)

        if number_of_full_lines > 0:
            self.num_lines_removed = self.num_lines_removed + number_of_full_lines
            self.msg2Statusbar.emit(str(self.num_lines_removed))
            self.curPiece.set_figure(Figure.No_Figure)
            self.update()

    def mouse_place_click(self, x, y):
        c_x = x // self.square_width()
        c_y = (self.contentsRect().bottom() - y) // self.square_height()
        self.check_place(c_x, c_y)
        if self.can_place:
            self.curX = c_x
            self.curY = c_y

    @staticmethod
    def draw_square(painter, x, y, shape, s_w, s_h, index):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00,
                      0xCCC45, 0xFFFFFF]

        red_color = 0xFF0000
        color = QColor(colorTable[shape])

        if index == 1:
            painter.setPen(red_color)
            painter.drawLine(x, y + s_h - 3, x, y)
            painter.drawLine(x, y, x + s_w - 3, y)

            color.setAlpha(50)
            painter.fillRect(x + 1, y + 1, s_w - 2,
                             s_h - 2, color)

        else:
            painter.setPen(color.lighter())

            painter.drawLine(x, y + s_h - 2, x, y)
            painter.drawLine(x, y, x + s_w - 2, y)

            painter.fillRect(x + 1, y + 1, s_w - 2,
                             s_h - 2, color)

        # painter.setPen(color.darker())
        # painter.drawLine(x + 1, y + s_h - 1,
        #                  x + s_w - 1, y + s_h - 1)
        # painter.drawLine(x + s_w - 1,
        #                  y + s_h - 1, x + s_w - 1, y + 1)


class Figure(object):
    No_Figure = 0
    Z_Figure = 1
    S_Figure = 2
    Line_Figure = 3
    T_Figure = 4
    Square_Figure = 5
    L_Figure = 6
    Mirrored_Figure = 7
    Point_Figure1 = 8
    Point_Figure2 = 9


class View_form(object):
    coord_table = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 0)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0))
    )

    def __init__(self):

        self.coord = [[0, 0] for _ in range(4)]
        self.piece_figure = Figure.No_Figure

        self.set_figure(Figure.No_Figure)

    def figure(self):
        return self.piece_figure

    def set_figure(self, shape):

        table = View_form.coord_table[shape]

        for i in range(4):
            for j in range(2):
                self.coord[i][j] = table[i][j]

        self.piece_figure = shape

    def set_random_figure(self):
        self.set_figure(random.randint(1, 8))

    def x(self, index):
        return self.coord[index][0]

    def y(self, index):
        return self.coord[index][1]


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    Tetris.start_message()
    sys.exit(app.exec_())
