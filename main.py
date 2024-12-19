import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
root.geometry("400x400")
root.title("Tic Tac Toe")
main_font = tkFont.Font(family="Helvetica", size=20)
cell_font = tkFont.Font(family="Helvetica", size=40)


class Cell(tk.Frame):
    def __init__(self, parent, clickFunc, pos, default=""):
        tk.Frame.__init__(self, parent)
        self.state = -100
        self.clickFunc = clickFunc
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)
        onClick = lambda: clickFunc(pos[0], pos[1])
        self.button = tk.Button(self, text = "  ", font = cell_font, command = onClick)
        self.button.grid(sticky="NWSE")

        self.button.pack()

    def setState(self, state):
        self.state = state
        if self.state == -100:
            self.button["text"] = "  "
        elif self.state == 1:
            self.button["text"] = "x"
        elif self.state == 2:
            self.button["text"] = "o"

class Board(tk.Frame):

    def __init__(self, parent, winFunc):
        tk.Frame.__init__(self, parent)
        self.winFunc = winFunc
        self.warning = tk.Label(self, text = "", font = main_font)
        self.gridFrame = tk.Frame(self)
        self.grid = [[Cell(self.gridFrame, lambda x, y: self.handleMove(x, y), (w, h)) for w in range(3)] for h in range(3)]
        for h in range(3):
            for w in range(3):
                cell = self.grid[h][w]
                cell.grid(row = h, column = w)
        self.gridFrame.pack()
        self.turn = 0
        self.player = 1
        self.winner = ""

    def checkForWin(self):
        for row in range(3):
            total = sum(map(lambda x: x.state, self.grid[row]))
            if total == 3:
                return 1
            elif total == 6:
                return 2
        for col in range(3):
            total = sum(map(lambda row: row[col].state, self.grid))
            if total == 3:
                return 1
            elif total == 6:
                return 2
        total = sum([self.grid[i][i].state for i in range(3)])
        if total == 3:
            return 1
        elif total == 6:
            return 2
        total = sum([self.grid[2-i][i].state for i in range(3)])
        if total == 3:
            return 1
        elif total == 6:
            return 2
        return 0



    def handleMove(self, x, y):
        self.warning.pack_forget()
        if self.winner != "":
            return
        if self.grid[y][x].state != -100:
            self.warning["text"] = "Spot Already Taken"
            self.warning.pack()
            return
        self.grid[y][x].setState(self.player)
        self.turn += 1
        root.title(f"Tic Tac Toe - Game | Turn {self.turn}")
        if self.turn >= 5:
            check = self.checkForWin()
            if check == 1:
                self.winner = "Player 1"
            elif check == 2:
                self.winner = "Player 2"
        if self.turn == 9 and self.winner == "":
            self.winner = "Tie"
        if self.winner != "":
            if self.winner == "Tie":
                self.warning["text"] = self.winner
            else:
                self.warning["text"] = self.winner+" Wins"
            self.warning.pack()
            self.winFunc()
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1


    def reset(self):
        for h in range(3):
            for w in range(3):
                self.grid[h][w].setState(-100)
        self.turn = 0
        self.player = 1
        self.winner = ""
        self.warning.pack_forget()

class ChoiceMenu(tk.Frame):
    def __init__(self, parent, funcs):
        tk.Frame.__init__(self, parent)
        def wrap(func):
            def close():
                func()
                self.pack_forget()
            return close
        funcs = list(map(wrap, funcs))
        self.stats = tk.Button(self, text="Show\nStats", font=main_font)
        self.play  = tk.Button(self, text="Play\nAgain", font=main_font)
        self.quitb = tk.Button(self, text="Quit", height=2, font=main_font)

        self.stats.config(command=funcs[0])
        self.play.config(command=funcs[1])
        self.quitb.config(command=funcs[2])

        self.stats.grid(column=0, row=0)
        self.play.grid(column=1, row=0)
        self.quitb.grid(column=2, row=0)

class StatMenu(tk.Frame):
    def __init__(self, parent, closeFunc, stats=None):
        tk.Frame.__init__(self, parent)
        if stats is None:
            stats = [0, 0, 0, 0]
        self.stats = stats
        self.games = tk.Label(self, text=f"Games: {stats[0]}", font=main_font)
        self.p1wins = tk.Label(self, text=f"Player 1 Wins: {stats[1]}", font=main_font)
        self.p2wins = tk.Label(self, text=f"Player 2 Wins: {stats[2]}", font=main_font)
        self.ties = tk.Label(self, text=f"Ties: {stats[3]}", font=main_font)

        self.closeb = tk.Button(self, text="Close Stats", font=main_font)

        self.closeb.config(command=closeFunc)

        self.games.pack()
        self.p1wins.pack()
        self.p2wins.pack()
        self.ties.pack()
        self.closeb.pack()

    def updateStats(self, stats):
        self.stats = stats
        self.games["text"] = f"Games: {stats[0]}"
        self.p1wins["text"] = f"Player 1 Wins: {stats[1]}"
        self.p2wins["text"] = f"Player 2 Wins: {stats[2]}"
        self.ties["text"] = f"Ties: {stats[3]}"

class Game(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.game = Board(self, lambda: self.handleEndOfGame())
        self.choices = ChoiceMenu(self, [lambda: self.displayStats(), lambda: self.playAgain(), lambda: self.closeGame()])
        self.stats = StatMenu(self, lambda: self.closeStats())
        self.game.pack()
        self.games = 0
        self.player1WinCount = 0
        self.player2WinCount = 0
        self.tieCount = 0

    def closeStats(self):
        self.stats.pack_forget()
        self.displayMenu()

    def handleEndOfGame(self):
        self.games += 1
        if self.game.winner == "Player 1":
            self.player1WinCount += 1
        elif self.game.winner == "Player 2":
            self.player2WinCount += 1
        else:
            self.tieCount += 1
        self.after(1000, lambda: self.game.pack_forget())
        self.after(1000, lambda: self.displayMenu())

    def displayMenu(self):
        root.title(f"Tic Tac Toe - Menu")
        self.choices.pack()

    def playAgain(self):
        root.title(f"Tic Tac Toe - Game")
        self.game.pack()
        self.game.reset()

    def displayStats(self):
        root.title(f"Tic Tac Toe - Stats")
        self.stats.pack()
        self.stats.updateStats([self.games, self.player1WinCount, self.player2WinCount, self.tieCount])

    def closeGame(self):
        root.quit()

game = Game(root)
game.playAgain()
game.place(x=0, y=0, relwidth=1, relheight=1)

root.mainloop()