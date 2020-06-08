class Game:
    def __init__(self,user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2
        self.field_of_play = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]

    def vivod(self):
        print(self.field_of_play)

    def victory(self,field):
        if (field == 1):
            print("Victory ", self.user_1)
            self.exit_game()
            return self.user_1
        elif (field == 2):
            print("Victory ", self.user_2)
            self.exit_game()
            return self.user_2
        elif (field == 3):
            print("No one won")
            self.exit_game()
            return "No one won"
    def exit_game(self):
        print("let's start again")
        self.field_of_play = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]
