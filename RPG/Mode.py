from GameInventory import Inventory
import random as ran
import DropChance as chance
import msvcrt
import time
import Map
import sys

class Easy:
    def __init__(self, character):
        self.enemy = Enemy()
        self.character = character
        self.start = Map.Map("Lobby")
        self.hallway = Map.Map("HallWay")
        self.registrar = Map.Map("Registrar")
        self.classroom = Map.Map("Classroom")
        self.feild = Map.Map("Feild")
        self.gymnasium = Map.Map("Gymnasium")
        self.admin = Map.Map("Admin Room")
        self.start.left = self.hallway
        self.hallway.right = self.registrar
        self.hallway.left = self.classroom
        self.start.right = self.feild
        self.feild.right = self.gymnasium
        self.gymnasium.right = self.admin
        self.location = self.start
        self.location_history = [self.start]
        self.inventory = Inventory()
        self.chance = chance.Chance()
        self.tool = self.inventory.equipedItem["Tool"]
        self.armor = self.inventory.equipedItem["Armor"]
        self.hashLcation = {
            
            "Lobby" : "Lobby",
            "HallWay" : self.goHallWay,
            "Registrar" : self.goRegistrar,
            "Classroom" : self.goClassroom,
            "Feild" : self.goFeild,
            "Gymnasium" : self.goGymnasium,
            "Admin Room" : self.goAdmin
            
        }
        self.hasCleared = []
        self.savedGame = None


    def mainGame(self, name):
        print(f"\nWelcome {name} to Easy Difficulty\n")
        while True:
            try:
                print(f"\nYou Are in {self.location.data}")
                print(f"Player Name: {name}\
                    \n1. Player Stats\
                    \n2. Inventory\
                    \n3. Map\
                    \n4. Pick Place\
                    \n5. Quit")
                choice = int(input("> "))
                if choice == 1:
                    print("\n")
                    for val, stat in self.character.items():
                        print(f"{val} : {stat}")
                    print("\n\n")
                    time.sleep(1)
                elif choice == 2:
                    while True:
                        print("\n-----Inventory-----" \
                        "\n1. Items" \
                        "\n2. Remove Item" \
                        "\n3. Check Capacity" \
                        "\n4. Back")
                        choice = int(input("> "))
                        if choice == 1:
                            self.inventory.printItems()
                        elif choice == 2:
                            if self.inventory.isEmpty():
                                print("\nItem Is Empty, Can't Delete Item\n")
                                break
                            print("\n-Input Correct Item To Remove-" \
                            "\nExample" \
                            "\n[Item Type]: Armor" \
                            "\n[Item Name]: Diamond Helmet")
                            itemType = input("[Item Type]: ")
                            itemName = input("[Item Name]: ")
                            print(self.inventory.removeItem([itemType, itemName]))
                        elif choice == 3:
                            print(f"is Capacity Max: {self.inventory.isMaxInv()}")
                        elif choice == 4:
                            break
                        else:
                            print(f"\n{choice} not Found\n")
                            time.sleep(1)
                        time.sleep(1)
                elif choice == 3:
                    print("\n")
                    Map.printMap(self.start)
                elif choice == 4:
                    while True:
                        print("\n----------" \
                        "\n1. Go Left" \
                        "\n2. Go Right" \
                        "\n3. Go Back" \
                        "\n4. Go Back To Menu")
                        choice = int(input("> "))
                        if choice == 1:
                            if self.location.left:
                                temporary_location = self.location.left
                                for i in self.hashLcation:
                                    if i == temporary_location.data:
                                        action = self.hashLcation.get(temporary_location.data)
                                if action:
                                    action()
                                else:
                                    print("\nFunction Error\n")
                                    time.sleep(1)
                            else:
                                print("\nLocation has no Right places\n")
                        elif choice == 2:
                            if self.location.right:
                                temporary_location = self.location.right
                                for i in self.hashLcation:
                                    if i == temporary_location.data:
                                        action = self.hashLcation.get(temporary_location.data)
                                if action:
                                    action()
                                else:
                                    print("\nFunction Error\n")
                            else:
                                print("\nLocation has no Left places\n")
                                time.sleep(1)
                        elif choice == 3:
                            if len(self.location_history) > 1:
                                self.location = self.location_history.pop()
                                self.location = self.location_history[-1]
                                print(f"You went back to {self.location.data}")
                                break
                            else:
                                print("\nYou are at the starting location. Cannot go back further.\n")
                            time.sleep(1)
                        elif choice == 4:
                            print("\nWelcome Back\n")
                            break
                        else:
                            print(f"\n{choice} not Found!\n")
                            time.sleep(1)
                        time.sleep(1)
                elif choice == 5:
                    break
                else:
                    print(f"{choice} not Found")
                    time.sleep(1)
            except ValueError:
                print("\n\nValue Error: Input Incorrect\n\n")
                time.sleep(3)
                continue
            except SyntaxError:
                print("Syntax Error: Incorrect Syntax")
            time.sleep(1)


    def helperSystem(self):
        if self.character["Health"] <= 0:
            print("\nYou die, connat respawn, just create a new one\n")
            time.sleep(2)
            sys.exit()


    def battleSystem(self, locationName):
        enemy_list = self.enemy.enemySpawn()
        print("\nEnemy Spawned\n")
        for i in enemy_list:
            print(i[0])
        while len(enemy_list) > 0 and self.character["Health"] >= 1:
            self.helperSystem()
            length = len(enemy_list)
            random = ran.randint(0, (length - 1))
            self.inventory.printEquipedArmor(); self.inventory.printEquipedTool()
            print(f"\nThere are {length} enemy\nYou must kill every single one of it\nItem You are using: {self.tool[0]}\n")
            try:
                print("5. Use Potion")
                print("6. Equip Armor")
                print("1. Basic Attack")
                if len(self.tool[2]) == 2:
                    print(f"2. {self.tool[2][0]}")
                    choice = int(input("> "))
                    if choice == 1:
                        enemy_list[random][1][0] -= self.tool[1]
                        print(f"\nYou damaged {enemy_list[random][0]} with {self.tool[1]}")
                        time.sleep(1)
                    elif choice == 2:
                        if self.character["Mana"] < self.tool[3]:
                            print("\nYou Can't use skill because your mana is Low\n")
                        else:
                            self.character["Mana"] = self.character["Mana"] - self.tool[3]
                            time.sleep(5)
                            for i in range(length):
                                enemy_list[i][1][0] -= self.tool[2][-1]
                    elif choice == 5:
                        self.usePotion()
                    elif choice == 6:
                        self.useArmor()
                    
                else:
                    choice = int(input("> "))
                    if choice == 1:
                        enemy_list[random][1][0] -= self.tool[1]
                        print(f"\nYou damaged {enemy_list[random][0]} with {self.tool[1]}")
                        time.sleep(1)
                        
                        if len(enemy_list) > 0:
                            if ran.choices([True, False]):
                                result = self.enemy.enemyAttack(enemy_list
                                [ran.randint(0, len(enemy_list) - 1)][1][1], 
                                self.character["Health"] ,
                                "Easy", self.armor)
                                if isinstance(result, int):
                                    self.character["Health"] = result
                                    print(f"\nYour health is now {self.character['Health']}\n")
                                else:
                                    print(result)
                        
                    elif choice == 5:
                        self.usePotion()
                    elif choice == 6:
                        self.useArmor()
                dead = [e for e in enemy_list if e[1][0] <= 0]
                for e in dead:
                    print(f"\nYou killed {e[0]}!\n")
                    item_drop = self.chance("Easy")
                    temporary_item = item_drop()
                    if temporary_item:
                        if temporary_item[1] is not None:
                            print(temporary_item)
                            self.inventory.addItem(temporary_item)
                enemy_list = [e for e in enemy_list if e[1][0] > 0]
                length = len(enemy_list)
                
            except ValueError:
                print("Value Error: Input Incorrect")
                time.sleep(3)
            except IndexError:
                print("\nIndex Out Of Bound\n")
            except SyntaxError:
                print("\nSyntax Error: Incorrect Syntax\n")
            if len(enemy_list) == 0:
                self.hasCleared.append(locationName)
                print("\nYou Cleared This Level\n")
            
            if len(self.hasCleared) == 6 and "Admin" in self.hasCleared:
                print("\nCONGRATULATION FOR BEATING THE RPG GAME!\n")
                time.sleep(3)
                print("\nWould You like to continue this game for fun?")
                print("For you to get your item for grinding.")
                print("You also have the ability to auto save your progress\n")
                yesNo = input("[Yes|No]: ")
                if yesNo.upper() == "YES":
                    self.savedGame = True
                    print("\n\n\n\n\n\n\n\n\n\n\n\n")
                    print("\nEnjoy!!\n")
                    self.hasCleared.clear();
                elif yesNo.upper() == "NO":
                    sys.exit()
            time.sleep(1)





    def goHallWay(self):
        print()
        self.location_history.append(self.location)
        self.location = self.hallway
        print("You are in the Hallway")
        if "Hallway" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Hallway")


    def goFeild(self):
        print()
        self.location_history.append(self.location)
        self.location = self.feild
        print("You are in the Feild")
        if "Feild" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Feild")


    def goRegistrar(self):
        print()
        self.location_history.append(self.location)
        self.location = self.registrar
        print("You are in the Registrar")
        if "Registrar" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Registrar")


    def goClassroom(self):
        print()
        self.location_history.append(self.location)
        self.location = self.classroom
        print("You are in the Classroom")
        if "Classroom" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Classroom")


    def goAdmin(self):
        print()
        self.location_history.append(self.location)
        self.location = self.admin
        print("You are in the Admin")
        if "Admin" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Admin")


    def goGymnasium(self):
        print()
        self.location_history.append(self.location)
        self.location = self.gymnasium
        print("You are in the Gymnasium")
        if "Gymnasium" in self.hasCleared:
            print("\nYou Cleared this level already.\n")
            return
        self.battleSystem("Gymnasium")



    def usePotion(self):
        try:
            
            if len(self.inventory.inventory["Potion"]) <= 0:
                print("\nThere is no Potion in the Inventory\n")
                return
            
            potions = {
            1 : "Health Potion",
            2 : "Damage Potion",
            3 : "Mana Potion",
            4 : "Critical Potion"
            }
            print("\n1. Health Potion\n2. Damage Potion\n3. Mana Potion\n4. Critical Potion");
            potion = int(input("> "))
            result = self.inventory.usePotion(potions.get(potion))
            
            if isinstance(result, str):
                print(result)
                return
            elif potions.get(potion) == "Health Potion":
                self.character["Health"] += result
                print(result)
                print(self.character["Health"])
            elif potions.get(potion) == "Damage Potion":
                self.tool[1] += result
                print(result)
                print(self.tool[1])
            elif potions.get(potion) == "Mana Potion":
                self.character["Mana"] += result
                print(result)
                print(self.character["Mana"])
            elif potions.get(potion) == "Critical Potion":
                self.tool[1] *= result
                print(result)
                print(self.tool[1])
        except ValueError:
            print('\nValue Error: Input Incorrect\n')
        except SyntaxError:
            print("Syntax Error: Incorrect Syntax")
        time.sleep(1)


    def useArmor(self):
        try:
            if self.inventory.isArmorEmpty():
                print("\nArmor is Empty\n")
                return
            self.inventory.printArmor()
            
            print("\n-Input Correct Item To Remove-" \
                                "\nExample" \
                                "\n[Item Name]: Diamond Helmet")
            itemName = input("[Item Name]: ")
            self.inventory.equipArmor(itemName)
        except ValueError:
            print("Value Error: Incorrect Input")
        except SyntaxError:
            print("Syntax Error: Incorrect Syntax")
        time.sleep(1)


class Enemy:
    def __init__(self):
        self.enemy = {
        "Enemy" : {
            "Slime" : [100, 20],
            "Goblin" : [150, 30],
            "Skeleton" : [200, 40],
            "Zombie" : [200, 50],
            "Vampire" : [300, 150],
            "Werewolf" : [300, 100],
            "Giant Zombie" : [500, 100],
            "Demon" : [650, 150],
            "Demonic Knight Boss" : [5000, 250],
            "Demon Vampire" : [1000, 150],
            "Possessed Werewolf" : [1000, 200],
            "Possessed Giant Zombie" : [1500, 250],
            "Devil Boss" : [10000, 500],
            "Demonic King Boss" : [15000, 1000],
            "Demon Lord Of The Last Boss" : [100000, 5000]
            },
        }


    def enemySpawn(self):
        number_of_enemies = ran.randint(5, 10)
        enemy_list = []
        for i in range(number_of_enemies):
            enemy = list(self.enemy["Enemy"].keys())
            random_enemy = ran.choice(enemy)
            enemy_stat = self.enemy["Enemy"].get(random_enemy)
            enemy_list.append([random_enemy, enemy_stat.copy()])
        return enemy_list


    def enemyAttack(self, enemy_health, char_health ,difficulty, armor):
        temporary_diff_var = {
            "Easy" : 5,
            "Medium" : 4,
            "Hard" : 3
        }
        print("\nPress 2 To Dodge Enemy Attack!!\n")
        time_num = temporary_diff_var.get(difficulty)
        start = time.time()
        while time.time() - start < time_num:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key == "2":
                    time.sleep(1)
                    return "\nyou Dodged!\n"
        else:
            armorStat = sum({k: sum(j) for k, j in armor.items() if isinstance(j, list)}.values())
            print("\nYou got hit!\n")
            time.sleep(1)
            if armorStat:
                damageLeft = armorStat - enemy_health
                if damageLeft < 0:
                    return max(char_health + damageLeft, 0)
                else:
                    return char_health
            return char_health - enemy_health