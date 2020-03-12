from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import copy
from kivy.config import Config

class mishbezet(Button):
    def __init__(self, whos_stone, row, col):
        Button.__init__(self)
        self.whos_stone = whos_stone
        self.row = row
        self.col = col


class Board(GridLayout):
    def __init__(self, touch = None):
        GridLayout.__init__(self)
        self.clear_widgets()
        self.cols = 3
        self.depth = 0
        for i in range(self.cols):
            for j in range(self.cols):
                if i < 2 and j in [0, 2]:
                    self.add_widget(Label())
                if i == 0 and j == 1:
                    self.add_widget(Label(text='Ugolki', font_size='50sp'))
                if i == 1 and j == 1:
                    button_rules = Button(text='Rules')
                    button_rules.bind(on_press=self.click_rules)
                    self.add_widget(button_rules)
                if i == 2 and j == 0:
                    button_easy = Button(text='Easy Difficulty')
                    button_easy.bind(on_press=self.game)
                    self.add_widget(button_easy)
                if i == 2 and j == 1:
                    button_medium = Button(text='Medium Difficulty')
                    button_medium.bind(on_press=self.game)
                    self.add_widget(button_medium)
                if i == 2 and j == 2:
                    button_hard = Button(text='Hard Difficulty')
                    button_hard.bind(on_press=self.game)
                    self.add_widget(button_hard)


    def click_rules(self, touch):
        self.clear_widgets()
        self.cols = 1
        self.add_widget(Label(text="Rules", font_size='50sp'))
        self.add_widget(Label(text="Both players start off with square arrangements of 16 game pieces in opposing corners of the gameboard."))
        self.add_widget(Label(text="Each player's goal is to move all their pieces from the starting corner to the occupied coner"))
        self.add_widget(Label(text="Players take turns moving one game piece."))
        self.add_widget(Label(text=" A piece may move only away from the starting location into a destination that is empty, provided either of the following conditions are met:"))
        self.add_widget(Label(text="the destination square is adjacent to the starting square"))
        self.add_widget(Label(text="the destination square can be reached by jumps over enemy game pieces."))
        self.add_widget(Label(text="The game ends when one of the player fills the other plaer's corner"))
        button_back = Button(text="Back to the main screen")
        button_back.bind(on_press=self.__init__)
        self.add_widget(button_back)


    def game(self, touch):
        self.clear_widgets()
        if touch.text == 'Easy Difficulty':
            self.depth = 1
        if touch.text == 'Medium Difficulty':
            self.depth = 2
        if touch.text == 'Hard Difficulty':
            self.depth = 3
        self.selected = None
        self.cols = 8
        self.board = []
        self.turn = 1
        for i in range(self.cols):
            line = []
            for j in range(self.cols):
                if i > 3 and j < 4:
                    cell = mishbezet(1, i, j)
                    cell.background_color = (0, 0, 255, 0.5)
                elif i < 4 and j > 3:
                    cell = (mishbezet(2, i, j))
                    cell.background_color = (255, 0, 0, 0.5)
                else:
                    cell = (mishbezet(0, i, j))
                    if i%2 == 0 and j%2 == 0 or i%2 == 1 and j%2 == 1:
                        cell.background_color = (255, 255, 255, 1)
                    else:
                        cell.background_color = (0, 0, 0, 1)
                cell.bind(on_press=self.click)
                self.add_widget(cell)
                line.append(cell)
            self.board.append(line)


    def click(self, touch):
        if touch.whos_stone == 1 or self.selected != None:
            if self.selected == None:
                touch.background_color = (0, 255, 0, 0.5)
                self.selected = touch
            elif self.selected == touch:
                touch.background_color = (0, 0, 255, 0.5)
                self.selected = None
            elif Board.valid_move(self.convert() , touch.row, touch.col, self.selected.row, self.selected.col):
                self.selected.whos_stone = 0
                if self.selected.row % 2 == 0 and self.selected.col % 2 == 0 or self.selected.row % 2 == 1 and self.selected.col % 2 == 1:
                    self.selected.background_color = (255, 255, 255, 1)
                else:
                    self.selected.background_color = (0, 0, 0, 1)
                self.selected = None
                touch.background_color = (0, 0, 255, 0.5)
                touch.whos_stone = 1

                enemy_move = Board.minimax(self.convert(), self.depth)
                self.board[enemy_move[1][0]][enemy_move[1][1]].whos_stone = 0
                if enemy_move[1][0] % 2 == 0 and enemy_move[1][1] % 2 == 0 or enemy_move[1][0] % 2 == 1 and enemy_move[1][1] % 2 == 1:
                    self.board[enemy_move[1][0]][enemy_move[1][1]].background_color = (255, 255, 255, 1)
                else:
                    self.board[enemy_move[1][0]][enemy_move[1][1]].background_color = (0, 0, 0, 1)
                self.board[enemy_move[2][0]][enemy_move[2][1]].background_color = (255, 0, 0, 0.5)
                self.board[enemy_move[2][0]][enemy_move[2][1]].whos_stone = 2
                end = Board.is_over(self.convert())
                if end != -1:
                    self.end_screen(end)

    def end_screen(self, end):
        self.clear_widgets()
        self.cols = 1
        if end == 1:
            self.add_widget(Label(text="Victory", font_size='50sp'))
        if end == 2:
            self.add_widget(Label(text="Defeat", font_size='50sp'))
        else:
            self.add_widget(Label(text="Draw", font_size='50sp'))
        button_back = Button(text="Play Again")
        button_back.bind(on_press=self.__init__)
        self.add_widget(button_back)

    def convert(self):
        board = []
        for i in range(8):
            line = []
            for j in range(8):
                line.append(self.board[i][j].whos_stone)
            board.append(line)
        return board

    @staticmethod
    def valid_move(board , touch_x, touch_y, x, y):
        if board[touch_x][touch_y] == 0:
            if x+1 == touch_x and y == touch_y or\
                x-1 == touch_x and y == touch_y or \
                x == touch_x and y+1 == touch_y or\
                x == touch_x and y-1 == touch_y:
                return True
            else:
                return Board.can_jump(board, touch_x, touch_y, x, y, [])


    @staticmethod
    def can_jump(board, touch_x, touch_y, x, y, temp):
        if x < 6 and board[x + 2][y] == 0 and [x + 2, y] not in temp and board[x + 1][y] != 0:
            if x + 2 == touch_x and y == touch_y:
                return True
            else:
                temp.append([x + 2, y])
                board[x][y] = 0
                board[x + 2][y] = 1
                if Board.can_jump(board, touch_x, touch_y,x + 2, y, temp):
                    return True
        if x > 1 and board[x - 2][y] == 0 and [x - 2, y] not in temp and board[x - 1][y] != 0:
            if x - 2 == touch_x and y == touch_y:
                return True
            else:
                temp.append([x - 2, y])
                board[x][y] = 0
                board[x - 2][y] = 1
                if Board.can_jump(board, touch_x, touch_y, x - 2, y, temp):
                    return True
        if y < 6 and board[x][y + 2] == 0 and [x, y + 2] not in temp and board[x][y + 1] != 0:
            if x == touch_x and y + 2 == touch_y:
                return True
            else:
                temp.append([x, y + 2])
                board[x][y] = 0
                board[x][y + 2] = 1
                if Board.can_jump(board, touch_x, touch_y, x, y + 2, temp):
                    return True
        if y > 1 and board[x][y - 2] == 0 and [x, y - 2] not in temp and board[x][y - 1] != 0:
            if x == touch_x and y - 2 == touch_y:
                return True
            else:
                temp.append([x, y - 2])
                board[x][y] = 0
                board[x][y - 2] = 1
                if Board.can_jump(board, touch_x, touch_y, x, y - 2, temp):
                    return True
        return False


    @staticmethod
    def is_over(board):
        counter_red = 0
        counter_blue = 0
        for i in range(8):
            for j in range(8):
                if i > 3 and j < 4:
                    if board[i][j] == 2:
                        counter_red +=1
                if i < 4 and j > 3:
                    if board[i][j] == 1:
                        counter_blue +=1
        if counter_red == 16:
            return 2
        elif counter_blue == 16:
            return 1
        elif counter_blue == counter_red == 16:
            return 0
        return -1


    @staticmethod
    def next_board(board, turn):
        board1 = copy.deepcopy(board)
        option = list()
        options = list()
        for i in range(8):
            for j in range(8):
                if board[i][j] == turn:
                    if i != 7 and board[i + 1][j] == 0:
                        board1[i + 1][j] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i + 1, j])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if i != 0 and board[i - 1][j] == 0:
                        board1[i - 1][j] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i - 1, j])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if j != 7 and board[i][j + 1] == 0:
                        board1[i][j + 1] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i, j + 1])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if j != 0 and board[i][j - 1] == 0:
                        board1[i][j - 1] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i, j - 1])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    options.extend(Board.check(board, i, j, [], turn))
        return options


    @staticmethod
    def check(board, i, j, temp, turn):
        options = []
        if i < 6 and board[i + 1][j] != 0 and board[i + 1][j] != 0 and board[i + 2][j] == 0 and [i + 2, j] not in temp:
            option = []
            board1 = copy.deepcopy(board)
            board1[i + 2][j] = turn
            board1[i][j] = 0
            temp.append([i, j])
            option.append(board1)
            option.append(temp[0])
            option.append([i + 2, j])
            options.append(option)
            op = Board.check(board1, i + 2, j, temp, turn)
            if len(op) != 0:
                options.extend(op)
        if i > 1 and board[i - 1][j] != 0 and board[i - 1][j] != 0 and board[i - 2][j] == 0 and [i - 2, j] not in temp:
            option = []
            board1 = copy.deepcopy(board)
            board1[i - 2][j] = turn
            board1[i][j] = 0
            temp.append([i, j])
            option.append(board1)
            option.append(temp[0])
            option.append([i - 2, j])
            options.append(option)
            op = Board.check(board1, i - 2, j, temp, turn)
            if len(op) != 0:
                options.extend(op)
        if j < 6 and board[i][j + 1] != 0 and board[i][j + 1] != 0 and board[i][j + 2] == 0 and [i, j + 2] not in temp:
            option = []
            board1 = copy.deepcopy(board)
            board1[i][j + 2] = turn
            board1[i][j] = 0
            temp.append([i, j])
            option.append(board1)
            option.append(temp[0])
            option.append([i, j + 2])
            options.append(option)
            op = Board.check(board1, i, j + 2, temp, turn)
            if len(op) != 0:
                options.extend(op)
        if j > 1 and board[i][j - 1] != 0 and board[i][j - 1] != 0 and board[i][j - 2] == 0 and [i, j - 2] not in temp:
            option = []
            board1 = copy.deepcopy(board)
            board1[i][j - 2] = turn
            board1[i][j] = 0
            temp.append([i, j])
            option.append(board1)
            option.append(temp[0])
            option.append([i, j - 2])
            options.append(option)
            op = Board.check(board1, i, j - 2, temp, turn)
            if len(op) != 0:
                options.extend(op)
        return options


    @staticmethod
    def points_board(board):
        sum = 0
        if Board.is_over(board) == 1:
            return -10000
        elif Board.is_over(board) == 2:
            return 10000
        elif Board.is_over(board) == 0:
            return 0
        counter1 = counter2 = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 1:
                    if i < 4 and j > 3:
                        counter1 += 1
                    else:
                        distance = i + (7 - j)
                        sum += (distance*100)
                if board[i][j] == 2:
                    if i > 3 and j < 4:
                        counter2 += 1
                    else:
                        distance = (7 - i) + j
                        sum -= (distance*10)
                distance = 0
        sum += (counter2 - counter1)*10
        return sum


    @staticmethod
    def minimax(game_state, depth):
        alpha = float('-inf')
        beta = float('inf')
        moves = Board.next_board(game_state, 2)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.min_play(clone, depth-1, alpha, beta)
            if score > best_score:
                best_move = move
                best_score = score
            if alpha < best_score:
                alpha = best_score
            if beta <= alpha:
                break
        return best_move


    @staticmethod
    def min_play(game_state, depth, alpha, beta):
        if depth == 0 or Board.is_over(game_state) != -1:
            for i in game_state:
                print i
            print Board.points_board(game_state)
            return Board.points_board(game_state)
        moves = Board.next_board(game_state, 1)
        best_score = float('inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.max_play(clone, depth-1, alpha, beta)
            if score < best_score:
                best_move = move
                best_score = score
            if beta > best_score:
                beta = best_score
            if beta <= alpha:
                break
        return best_score


    @staticmethod
    def max_play(game_state, depth, alpha, beta):
        if depth == 0 or Board.is_over(game_state) != -1:
            for i in game_state:
                print i
            print Board.points_board(game_state)
            return Board.points_board(game_state)
        moves = Board.next_board(game_state, 2)
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.min_play(clone,depth-1,alpha,beta)
            if score > best_score:
                best_move = move
                best_score = score
            if alpha < best_score:
                alpha = best_score
            if beta <= alpha:
                 break
        return best_score


class TestApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
        self.title = 'Ugolki'
        return Board()
TestApp().run()