from tkinter import messagebox

class MessageBox():
    def __init__(self):
        self.__whiteWin = "White has won the game!"
        self.__blackWin = "Black has won the game!"
        self.__question = "Would you like to restart the game?"
        self.__titleMessage = "Good Job"
        self.__restart = False

    def setWinner(self, isWhite):
        # check the winner
        if isWhite: self.__restart = messagebox.askyesno(self.__titleMessage, self.__whiteWin + "\n" + self.__question)
        else: self.__restart = messagebox.askyesno(self.__titleMessage, self.__blackWin + "\n" + self.__question)

    def getRestartResponse(self):
        return self.__restart