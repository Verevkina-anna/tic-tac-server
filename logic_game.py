import sys
from logic_game_class import Game

def enter_coordinates(name, x_coordinate, y_coordinate):
    """Проверяем пришедшие координаты, и заводим их в моссив игрового поля"""
    if ((x_coordinate > 2 or x_coordinate < 0) or (y_coordinate >2 and y_coordinate < 0)):
        print("Error, the coordinate is already occupied")
        return
    elif (game_s.field_of_play[x_coordinate][y_coordinate] != 0):
        print("Error, the coordinate is already occupied")
        return
    elif (name != game_s.user_1 and name != game_s.user_2):
        print("Error, the user is not found")
        return
    else:
        if (name == game_s.user_1):
            game_s.field_of_play[x_coordinate][y_coordinate] = 1
            result_game()
        elif (name == game_s.user_2):
            game_s.field_of_play[x_coordinate][y_coordinate] = 2
            result_game()

def result_game():
    field = game_s.field_of_play
    flag = 0
    i = 0
    while (i <= 2):
        j = 0
        while (j <= 2):
            if (field[i][j] == 0):
                flag = 1
            j += 1
        i += 1
    if (flag == 0):
        game_s.victory(3)
    #Сравниваем по строкам-1

    if (field[0][0] == field[0][1] == field[0][2]):
       if(field[0][0]!=0):  game_s.victory(field[0][0])
    elif (field[1][0] == field[1][1] == field[1][2]):
        if (field[1][0] != 0):  game_s.victory(field[1][0])
    elif (field[2][0] == field[2][1] == field[2][2]):
        if(field[2][0]!=0): game_s.victory(field[2][0])
    #Сравниваем по столбцам
    elif (field[0][0] == field[1][0] == field[2][0]):
        if(field[0][0]!=0): game_s.victory(field[0][0])
    elif (field[0][1] == field[1][1] == field[2][1]):
        if(field[0][1]!=0): game_s.victory(field[0][1])
    elif (field[0][2] == field[1][2] == field[2][2]):
        if (field[0][2] != 0): game_s.victory(field[0][2])
    #Сравниваем диагонали
    elif (field[0][0] == field[1][1] == field[2][2]):
        if(field[0][0]!=0):game_s.victory(field[0][0])
    elif (field[2][0] == field[1][1] == field[0][2]):
        if(field[2][0]!=0): game_s.victory(field[2][0])

 

def process_command(command):
    """Выполняет действие, в зависимости от выбранной команды"""
    if (command == '-1'):
        print()
    # elif (command == '1'):
    #     start_game(input("Enter user number one: "), input("Enter user number two: "))
    elif (command == '2'):
        enter_coordinates(input("Enter user's name: "), int(input("Enter x: ")), int(input("Enter y: ")))
    elif (command == '3'):
        game_s.vivod()
    # elif():
    #     print(const.ERROR_MSG, file=sys.stderr)
    #     print()
    return


game_s = Game(input("Enter user number one: "), input("Enter user number two: "))

user_comand = '-2'
while user_comand != '-1':
    user_comand = input("Выберите действие: ")
    process_command(user_comand
