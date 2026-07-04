import GameDescription
import Mode
import time
import sys

class GamePlay:
    def __init__(self):
        self.warrior = {
            "Character": "Warrior",
            "Health" : 500,
            "Mana" : 1000,
        }


    def Main(self):
        name = input("Enter Your Nickname: ")
        print(f"\n\nWelcome {name} to a RPG\n\n")
        while True:
            try:
                print("" \
                "\n_____Game Menu_____" \
                "\n1. Play Game" \
                "\n2. Help" \
                "\n3. Exit")
                choice = int(input("> "))
                
                if choice == 1:
                    while True:
                        try:
                            print("\n\n_____Difficulty_____" \
                                "\n1. Easy" \
                                "\n2. Medium" \
                                "\n3. Hard" \
                                "\n4. Exit")
                            dfclt = int(input("> "))
                            if dfclt == 1:
                                easy = Mode.Easy(self.warrior)
                                easy.mainGame(name)
                            elif dfclt == 2:
                                pass
                            elif dfclt == 3:
                                pass
                            elif dfclt == 4:
                                return
                            else:
                                print(f"\n\n{dfclt} not Found!\n\n")
                        except ValueError:
                            print("\n\nValue Error: input Incorrect\n\n")
                            time.sleep(3)
                            continue
                        time.sleep(1)
                elif choice == 2:
                    GameDescription.description()
                elif choice == 3:
                    sys.exit()
                else:
                    print(f"\n\n{choice} not found!\n\n")
                    time.sleep(1)
            except ValueError:
                print("\n\nValue Error: Input Incorrect\n\n")
                time.sleep(3)
                continue
        time.sleep(1)


    def store(self):
        pass

game = GamePlay()
game.Main()