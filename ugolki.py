from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import copy
from kivy.config import Config

class mishbezet(Button):
    #פעולה זהו מאתילת את המחלקה
    def __init__(self, whos_stone, row, col):
        Button.__init__(self)
        self.whos_stone = whos_stone #משתנה זה שומר למי שייח המשבצת
        self.row = row #משתנה זה שומר את השורה בא נימצאת המשבצת
        self.col = col #משתנה זה שומר את העמודה בא נימצאת המשבצת


class Board(GridLayout):
    #פעולה זהו מאתחלת את הלוח
    def __init__(self, touch=None):
        GridLayout.__init__(self)
        self.clear_widgets()
        self.cols = 3 #משתנה זה שומר כמה עמודות ושורות היו על המסך שעלים ניתן להוסיף כפתורים
        self.depth = 0#משתנה זה סופר כמה צעדים קדימה המחשב מחשב במהלך המחשחק
        for i in range(self.cols):#לולאה זהו יוצרת את מסך התחלה
            for j in range(self.cols):
                if i < 2 and j in [0, 2]:
                    self.add_widget(Label())
                if i == 0 and j == 1:
                    self.add_widget(Label(text='Ugolki', font_size='50sp'))#מוסיף כותרת למסך הפתיחה
                if i == 1 and j == 1:
                    button_rules = Button(text='Rules')
                    button_rules.bind(on_press=self.click_rules)
                    self.add_widget(button_rules)#מוסיף כפתור שמוביל למסך החוקים
                if i == 2 and j == 0:
                    button_easy = Button(text='Easy Difficulty')
                    button_easy.bind(on_press=self.game)
                    self.add_widget(button_easy)#מוסיף כפתור שמשנה את רמת הקושי של המשחק
                if i == 2 and j == 1:
                    button_medium = Button(text='Medium Difficulty')
                    button_medium.bind(on_press=self.game)
                    self.add_widget(button_medium)#מוסיף כפתור שמשנה את רמת הקושי של המשחק
                if i == 2 and j == 2:
                    button_hard = Button(text='Hard Difficulty')
                    button_hard.bind(on_press=self.game)
                    self.add_widget(button_hard)#מוסיף כפתור שמשנה את רמת הקושי של המשחק

    #פעולה זהו יוצרת את מסך החוקים
    def click_rules(self, touch):
        self.clear_widgets()
        self.cols = 1#משנה את מספר העמודים במסך הליהם ניתן להוסיף כפורים או תווית
        self.add_widget(Label(text="Rules", font_size='50sp'))
        self.add_widget(Label(text="Both players start off with square arrangements of 16 game pieces in opposing corners of the gameboard."))
        self.add_widget(Label(text="Each player's goal is to move all their pieces from the starting corner to the occupied coner"))
        self.add_widget(Label(text="Players take turns moving one game piece."))
        self.add_widget(Label(text=" A piece may move only when the following conditions are met:"))
        self.add_widget(Label(text="the destination square is adjacent to the starting square"))
        self.add_widget(Label(text="the destination square can be reached by jumps  other game pieces belonging to either player."))
        self.add_widget(Label(text="The game ends when one of the player fills the other plaer's corner"))
        button_back = Button(text="Back to the main screen")
        button_back.bind(on_press=self.__init__)
        self.add_widget(button_back)

    #פעולה זהו מריצה את המשחק
    def game(self, touch):
        self.clear_widgets()
        if touch.text == 'Easy Difficulty':#בודק איזה רמת קושי בחר השחקן
            self.depth = 1
        if touch.text == 'Medium Difficulty':#בודק איזה רמת קושי בחר השחקן
            self.depth = 2
        if touch.text == 'Hard Difficulty':#בודק איזה רמת קושי בחר השחקן
            self.depth = 3
        self.selected = None#בודק האם חייל של השחקן נלחץ
        self.cols = 8#משנה את גמספר העמודים ושורות אליהם ניתן להוסיף כפתורים
        self.board = []#מאתחל את המערך הגרפי
        self.turn = 1#שומר אצל מי התור לשחק
        for i in range(self.cols):#לולאה זהו מסדרת את המצב התחלתי של המשחק
            line = []
            for j in range(self.cols):
                if i > 3 and j < 4:#תנאי זה מסדר את החיילים של השחקן
                    cell = mishbezet(1, i, j)
                    cell.background_color = (0, 0, 255, 0.5)
                elif i < 4 and j > 3:#תנאי זה מסדר את החיילים של המחשב
                    cell = (mishbezet(2, i, j))
                    cell.background_color = (255, 0, 0, 0.5)
                else:
                    cell = (mishbezet(0, i, j))
                    if i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1:#תנאי זה צובע את הלוח בשחור ולבן
                        cell.background_color = (255, 255, 255, 1)
                    else:
                        cell.background_color = (0, 0, 0, 1)
                cell.bind(on_press=self.click)
                self.add_widget(cell)
                line.append(cell)
            self.board.append(line)

    #פעולה זהו מופעלת כאשר כפתור נלחץ על הלוח
    def click(self, touch):
        if touch.whos_stone == 1 or self.selected != None:#תנאי זה בודק האם כפתור של השחקן נלחץ או האם זהו לא הפעם הראשונה
            if self.selected == None:#תנאי זה בודק האם זהו הפעם הראשונה שכפתור נלחץ
                touch.background_color = (0, 255, 0, 0.5)#משנה את צבע הכפתור לסימון
                self.selected = touch#מסמן את הכפתור הנלחץ
            elif self.selected == touch:#תנאי זה בודק האם השחקן רוצה לבטטל את בחירת החייל
                touch.background_color = (0, 0, 255, 0.5)#משנה את צבע הכפתור לברירת מחדל
                self.selected = None#מבטל את הכפתור הנלחץ
            elif Board.valid_move(self.convert(), touch.row, touch.col, self.selected.row, self.selected.col):#תנאי זה בודק האם הלחיצה השנייה חוקית וניתן להזיז את החייל ללחיצה
                self.selected.whos_stone = 0#משנה את הערך של הכפתור ממנו בא החייל
                if self.selected.row % 2 == 0 and self.selected.col % 2 == 0 or self.selected.row % 2 == 1 and self.selected.col % 2 == 1:#תנאי זה בודק האם המשבצת ממנה זז החייל צריכה להיות שחור או לבנה
                    self.selected.background_color = (255, 255, 255, 1)
                else:
                    self.selected.background_color = (0, 0, 0, 1)
                self.selected = None#מאפס את התור
                touch.background_color = (0, 0, 255, 0.5)#צובע את הכפותר אליו זז החייל בצבע בנכון
                touch.whos_stone = 1#משנה את הסימון של הכפתור אליו זז החייל

                enemy_move = Board.minimax(self.convert(), self.depth)#מריץ את ה-A.L
                self.board[enemy_move[1][0]][enemy_move[1][1]].whos_stone = 0#משנה את הערך של המקום ממנו זז החייל של המחשב
                if enemy_move[1][0] % 2 == 0 and enemy_move[1][1] % 2 == 0 or enemy_move[1][0] % 2 == 1 and enemy_move[1][1] % 2 == 1:#תנאי זה בודק איזה צבע השבצת שממנה זז החייל
                    self.board[enemy_move[1][0]][enemy_move[1][1]].background_color = (255, 255, 255, 1)
                else:
                    self.board[enemy_move[1][0]][enemy_move[1][1]].background_color = (0, 0, 0, 1)
                self.board[enemy_move[2][0]][enemy_move[2][1]].background_color = (255, 0, 0, 0.5)#צובע את המשבצת עליה החייל של המחשב מגיע
                self.board[enemy_move[2][0]][enemy_move[2][1]].whos_stone = 2#משנה את הערך של המשבצת אליה החייל של המחשב מגיע
                end = Board.is_over(self.convert())#מקבל את הערך האם המשחק נגמר
                if end != -1:#תנאי זה בודק האם המשחק נגמר
                    self.end_screen(end)#שולח למסך הסיום


    #פעולה זהו יוצרת את מסך הסיום
    def end_screen(self, end):
        self.clear_widgets()
        self.cols = 1#משנה את מספר העמדות במסך
        if end == 1:#תנאי זה בודק האם בשחקן ניצח
            self.add_widget(Label(text="Victory", font_size='50sp'))
        if end == 2:#תנאי זה בודק האם המחשב ניצח
            self.add_widget(Label(text="Defeat", font_size='50sp'))
        if end == 0:#תנאי זה בודק האם יש שווין
            self.add_widget(Label(text="Draw", font_size='50sp'))
        button_back = Button(text="Play Again")
        button_back.bind(on_press=self.__init__)#יוצר כפתור המחזיר למסך הפתיחה
        self.add_widget(button_back)

    #פעולה זהו ממירה את המערך הגרפי למערך מספרי
    def convert(self):
        board = []#מאתחלת את המערך המספרי
        for i in range(8):
            line = []
            for j in range(8):
                line.append(self.board[i][j].whos_stone)
            board.append(line)
        return board

    #פעולה זהו בודקת האם המסלך שהתקבל משחקן חוקי
    @staticmethod
    def valid_move(board, touch_x, touch_y, x, y):
        if board[touch_x][touch_y] == 0:#תנאי זה בודק האם הכפתור שנלחץ ריק
            if x+1 == touch_x and y == touch_y or\
                x-1 == touch_x and y == touch_y or \
                x == touch_x and y+1 == touch_y or\
                x == touch_x and y-1 == touch_y:#תנאי זה בודק שהכפתור שנלחץ חוקי לתזוזה
                return True
            else:
                return Board.can_jump(board, touch_x, touch_y, x, y, [])

    #פעולה זהו בודק האם המהלך שהתבצע חוקי לפי חוקי הקפיצה
    @staticmethod
    def can_jump(board, touch_x, touch_y, x, y, temp):
        if x < 6 and board[x + 2][y] == 0 and [x + 2, y] not in temp and board[x + 1][y] != 0:#תנאי זה בודק האם שהקפיצה לא תצא מתחום הלוח, שהיא חוקי וגם שלא נבדקה
            if x + 2 == touch_x and y == touch_y:#תנאי זה בודק האם הכפתור שנלחץ הוא תנוע חוקית
                return True
            else:
                temp.append([x + 2, y])#שומר את המיקומים שנבדק
                board[x][y] = 0
                board[x + 2][y] = 1
                if Board.can_jump(board, touch_x, touch_y,x + 2, y, temp):#בודק האת המשך הקפיצה
                    return True
        if x > 1 and board[x - 2][y] == 0 and [x - 2, y] not in temp and board[x - 1][y] != 0:#תנאי זה בודק האם שהקפיצה לא תצא מתחום הלוח, שהיא חוקי וגם שלא נבדקה
            if x - 2 == touch_x and y == touch_y:#תנאי זה בודק האם הכפתור שנלחץ הוא תנוע חוקית
                return True
            else:
                temp.append([x - 2, y])#שומר את המיקומים שנבדק
                board[x][y] = 0
                board[x - 2][y] = 1
                if Board.can_jump(board, touch_x, touch_y, x - 2, y, temp):#בודק האת המשך הקפיצה
                    return True
        if y < 6 and board[x][y + 2] == 0 and [x, y + 2] not in temp and board[x][y + 1] != 0:#תנאי זה בודק האם שהקפיצה לא תצא מתחום הלוח, שהיא חוקי וגם שלא נבדקה
            if x == touch_x and y + 2 == touch_y:#תנאי זה בודק האם הכפתור שנלחץ הוא תנוע חוקית
                return True
            else:
                temp.append([x, y + 2])#שומר את המיקומים שנבדק
                board[x][y] = 0
                board[x][y + 2] = 1
                if Board.can_jump(board, touch_x, touch_y, x, y + 2, temp):#בודק האת המשך הקפיצה
                    return True
        if y > 1 and board[x][y - 2] == 0 and [x, y - 2] not in temp and board[x][y - 1] != 0:#תנאי זה בודק האם שהקפיצה לא תצא מתחום הלוח, שהיא חוקי וגם שלא נבדקה
            if x == touch_x and y - 2 == touch_y:#תנאי זה בודק האם הכפתור שנלחץ הוא תנוע חוקית
                return True
            else:
                temp.append([x, y - 2])#שומר את המיקומים שנבדק
                board[x][y] = 0
                board[x][y - 2] = 1
                if Board.can_jump(board, touch_x, touch_y, x, y - 2, temp):#בודק האת המשך הקפיצה
                    return True
        return False

    #פעולה זהו בודק האם המשחק נגמר
    @staticmethod
    def is_over(board):
        counter_red = 0#מאתחל את הסופר של החיילים של המחשב
        counter_blue = 0#מאחל את הסופר של החיילים של השחקן
        for i in range(8):
            for j in range(8):
                if i > 3 and j < 4:#תנאי זה בודק האם בפינה התחלה של השחקן יש חיילים של המחשב
                    if board[i][j] == 2:
                        counter_red += 1
                if i < 4 and j > 3:#תנאי זה בודק האם באזור התחלה של המחשב יש חיילים של השחקן
                    if board[i][j] == 1:
                        counter_blue += 1
        if counter_blue == counter_red == 16:#תנאי זה בודק האם יש שווין
            return 0
        elif counter_blue == 16:#תנאי זה בודק האם השחקן ניצח
            return 1
        elif counter_red == 16:  # תנאי זה בודק האם המחשב ניצח
            return 2
        return -1

    #פעולה זהו מחזירה מערך עם כול האפשריות שאחד השחקנים יכול לבצע
    @staticmethod
    def next_board(board, turn):
        board1 = copy.deepcopy(board)
        option = list()#מאתחל מערך שתישמור אפשרות
        options = list()#מאתחל את המערך ששומר את האפשריות
        for i in range(8):
            for j in range(8):
                if board[i][j] == turn:#תנאי זה האם החייל שייך למי שבודרים
                    if i != 7 and board[i + 1][j] == 0:#תנאי זה בודק האם הוא יכול לבצע תנועה הפשוטה
                        board1[i + 1][j] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i + 1, j])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if i != 0 and board[i - 1][j] == 0:#תנאי זה בודק האם הוא יכול לבצע תנועה הפשוטה
                        board1[i - 1][j] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i - 1, j])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if j != 7 and board[i][j + 1] == 0:#תנאי זה בודק האם הוא יכול לבצע תנועה הפשוטה
                        board1[i][j + 1] = turn
                        board1[i][j] = 0
                        option.append(board1)
                        option.append([i, j])
                        option.append([i, j + 1])
                        options.append(option)
                        option = []
                        board1 = copy.deepcopy(board)
                    if j != 0 and board[i][j - 1] == 0:#תנאי זה בודק האם הוא יכול לבצע תנועה הפשוטה
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

    #פעולה זהו בודקת האם יש אפשרות לאחד השחקנים לבצע קפיצה
    @staticmethod
    def check(board, i, j, temp, turn):
        options = []
        if i < 6 and board[i + 1][j] != 0 and board[i + 1][j] != 0 and board[i + 2][j] == 0 and [i + 2, j] not in temp:#תנאי זה בודק האם יש אפשרות לבצע קפיצה למקום שלא נבדק
            option = []
            board1 = copy.deepcopy(board)
            board1[i + 2][j] = turn
            board1[i][j] = 0
            temp.append([i, j])#שומר את המיקומים שנבדק
            option.append(board1)
            option.append(temp[0])
            option.append([i + 2, j])
            options.append(option)
            op = Board.check(board1, i + 2, j, temp, turn)
            if len(op) != 0:#תנאי זה בודק שלא מחזירים מערך בלי אפשרות
                options.extend(op)
        if i > 1 and board[i - 1][j] != 0 and board[i - 1][j] != 0 and board[i - 2][j] == 0 and [i - 2, j] not in temp:#תנאי זה בודק האם יש אפשרות לבצע קפיצה למקום שלא נבדק
            option = []
            board1 = copy.deepcopy(board)
            board1[i - 2][j] = turn
            board1[i][j] = 0
            temp.append([i, j])#שומר את המיקומים שנבדק
            option.append(board1)
            option.append(temp[0])
            option.append([i - 2, j])
            options.append(option)
            op = Board.check(board1, i - 2, j, temp, turn)
            if len(op) != 0:#תנאי זה בודק שלא מחזירים מערך בלי אפשרות
                options.extend(op)
        if j < 6 and board[i][j + 1] != 0 and board[i][j + 1] != 0 and board[i][j + 2] == 0 and [i, j + 2] not in temp:#תנאי זה בודק האם יש אפשרות לבצע קפיצה למקום שלא נבדק
            option = []
            board1 = copy.deepcopy(board)
            board1[i][j + 2] = turn
            board1[i][j] = 0
            temp.append([i, j])#שומר את המיקומים שנבדק
            option.append(board1)
            option.append(temp[0])
            option.append([i, j + 2])
            options.append(option)
            op = Board.check(board1, i, j + 2, temp, turn)
            if len(op) != 0:#תנאי זה בודק שלא מחזירים מערך בלי אפשרות
                options.extend(op)
        if j > 1 and board[i][j - 1] != 0 and board[i][j - 1] != 0 and board[i][j - 2] == 0 and [i, j - 2] not in temp:#תנאי זה בודק האם יש אפשרות לבצע קפיצה למקום שלא נבדק
            option = []
            board1 = copy.deepcopy(board)
            board1[i][j - 2] = turn
            board1[i][j] = 0
            temp.append([i, j])#שומר את המיקומים שנבדקו
            option.append(board1)
            option.append(temp[0])
            option.append([i, j - 2])
            options.append(option)
            op = Board.check(board1, i, j - 2, temp, turn)
            if len(op) != 0:#תנאי זה בודק שלא מחזירים מערך בלי אפשרות
                options.extend(op)
        return options

    #פעולה זהו נותנת ניקוד ללוח מספרי
    @staticmethod
    def points_board(board):
        sum = 0
        if Board.is_over(board) == 1:#תנאי זה בודק האם יש ניצחון לשחקן
            return -10000000000000000
        elif Board.is_over(board) == 2:#תנאי זה בודק האם יש ניצחון למחשב
            return 10000000000000000
        elif Board.is_over(board) == 0:#תנאי זה בודק האם יש תיקו
            return 0
        counter1 = counter2 = 0#מאתחל את הסופרים של חיילים בפינות של האויב
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 1:#תנאי זה בודק האם התא שייח לשחקן
                    if i < 4 and j > 3:#תנאי זה בודק האם החייל של השחקן נמצא בפינה של האויב
                        counter1 += 1
                    distance = i + (7 - j)
                    sum += distance * 5
                if board[i][j] == 2:#תנאי זה בודק האם התא שייח למחשב
                    if i > 3 and j < 4:#תנאי זה בודק האם החייל נמצא בפינה של השחקן
                        counter2 += 1
                    distance = (7 - i) + j
                    sum -= distance * 5
        if counter2 > 13:#בודק מקרה קצה
            if board[3][0] == 2 or board[2][0] == 2 or board[7][4] == 2 or board[7][5] == 2:
                sum -= 500
        sum += (counter2 - counter1) * 10000
        return sum

    #פעולה זהו מתחילה את החישוב של המחשב למהלך הבא שלו
    @staticmethod
    def minimax(game_state, depth):
        alpha = -10000000000000000
        beta = 10000000000000000
        moves = Board.next_board(game_state, 2)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.min_play(clone, depth-1, alpha, beta)
            if score > best_score:#תנאי זה מוצא את הניקוד הגבוה היותר מבין כול המהלכים האפשריים
                best_move = move
                best_score = score
            if alpha < best_score:#בודק האם נמצא ניקוד יותר גובה ולכן יותר טוב למחשב
                alpha = best_score
            if beta <= alpha:#תנאי זה בודק האם יש להמשיך לרדת ולבדוק ניקודים אחרים
                break
        return best_move


    @staticmethod
    def min_play(game_state, depth, alpha, beta):
        if depth == 0 or Board.is_over(game_state) != -1:
            return Board.points_board(game_state)
        moves = Board.next_board(game_state, 1)
        best_score = float('inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.max_play(clone, depth-1, alpha, beta)
            if score < best_score:#תנאי זה מוצא את הניקוד הגבוה היותר מבין כול המהלכים האפשריים
                best_move = move
                best_score = score
            if beta > best_score:#בודק האם נמצא ניקוד יותר גובה ולכן יותר טוב לשחקן
                beta = best_score
            if beta <= alpha:#תנאי זה בודק האם יש להמשיך לרדת ולבדוק ניקודים אחרים
                break
        return best_score


    @staticmethod
    def max_play(game_state, depth, alpha, beta):
        if depth == 0 or Board.is_over(game_state) != -1:
            return Board.points_board(game_state)
        moves = Board.next_board(game_state, 2)
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(move[0])
            score = Board.min_play(clone, depth-1, alpha, beta)
            if score > best_score:#תנאי זה מוצא את הניקוד הגבוה היותר מבין כול המהלכים האפשריים
                best_move = move
                best_score = score
            if alpha < best_score:#בודק האם נמצא ניקוד יותר גובה ולכן יותר טוב למחשב
                alpha = best_score
            if beta <= alpha:#תנאי זה בודק האם יש להמשיך לרדת ולבדוק ניקודים אחרים
                 break
        return best_score


class TestApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
        self.title = 'Ugolki'
        return Board()
TestApp().run()