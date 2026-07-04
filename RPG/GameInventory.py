
class Inventory:
    def __init__(self):
        self.inventory = {
            "Potion" : [],
            "Armor" : [ 
                [ [], [], [], [] ], #Iron
                [ [], [], [], [] ], #Gold
                [ [], [], [], [] ], #Diamond
                [ [], [], [], [] ] #Excalibur
                ], #i[0][0].append("Hello World")
            "Tools" : [],
            "Others" : []
        }
        self.equipedItem = {
            "Armor" : {
                "Helmet" : None,
                "Chestplate" : None,
                "Leggings" : None,
                "Boots" : None
            },
            "Tool" : ["Excalibur", 500, ["World Slash", 9999], 100]
        }
        self.armorMap = {
                    "Iron" : {
                        "Helmet" : self.inventory["Armor"][0][0],
                        "Chestplate" : self.inventory["Armor"][0][1],
                        "Leggings" : self.inventory["Armor"][0][2],
                        "Boots" : self.inventory["Armor"][0][3]
                        },
                    "Gold" : {
                        "Helmet" : self.inventory["Armor"][1][0],
                        "Chestplate" : self.inventory["Armor"][1][1],
                        "Leggings" : self.inventory["Armor"][1][2],
                        "Boots" : self.inventory["Armor"][1][3]
                        },
                    "Diamond" : {
                        "Helmet" : self.inventory["Armor"][2][0],
                        "Chestplate" : self.inventory["Armor"][2][1],
                        "Leggings" : self.inventory["Armor"][2][2],
                        "Boots" : self.inventory["Armor"][2][3]
                        },
                    "Excalibur" : {
                        "Helmet" : self.inventory["Armor"][3][0],
                        "Chestplate" : self.inventory["Armor"][3][1],
                        "Leggings" : self.inventory["Armor"][3][2],
                        "Boots" : self.inventory["Armor"][3][3]
                    }
                }


    def addItem(self, items):
        if self.isMaxInv():
            print("\nInventory Maximum Capacity\n")
            return
        for value, item in self.inventory.items():
            if value in items and not items[1].startswith(("Iron", "Gold", "Diamond", "Excalibur")):
                self.inventory[value].append(items[1])
            else:
                for x, y in self.armorMap.items():
                    if items[1].startswith(x):
                        armorType = items[1]
                        text = armorType.split()
                        for i, j in y.items():
                            if text[1] == i:
                                j.append(armorType)
                                self.itemSort()
                                return


    def removeItem(self, items):
        for value, item in self.inventory.items():
            if value in items and not items[1].startswith(("Iron", "Gold", "Diamond", "Excalibur")):
                self.inventory[value].remove(items[1])
                return f"\n{items[1]} successfully Removed\n"
            else:
                text = items[1].split()
                materialType = {"Iron": 0, "Gold": 1, "Diamond": 2, "Excalibur": 3}
                armorType = {"Helmet": 0, "Chestplate": 1, "Leggings": 2, "Boots": 3}
                armorList = self.inventory["Armor"][materialType.get(text[0])][armorType.get(text[1])]
                
                if items[1] in armorList:
                    armorList.remove(items[1])
                    print(f"\n{items[1]} successfully Removed\n")
                    return
        print(f"\n{items[1]} not Found\n")


    def usePotion(self, potion):
        if self.inventory["Potion"] == []:
            print("\nPotion Is Empty, Can't Use Potion\n")
            return
        for item in self.inventory["Potion"]:
            if item == potion:
                self.inventory["Potion"].remove(potion)
                print(f"\n{potion} successfully Used\n")
                for i, y in {
                    "Health Potion" : 50, 
                    "Mana Potion" : 100, 
                    "Damage Potion" : 150, 
                    "Critical Potion" : 2}.items():
                    if potion == i:
                        return y
        return f"\n{potion} not Found\n"

    def equipArmor(self, armor):
        if self.isArmorEmpty():
            print("\nArmor Is Empty, Can't Equip Armor\n")
            return
        for x, y in self.armorMap.items():
            if armor.startswith(x):
                text = armor.split()
                for i, j in y.items():
                    if text[1] == i and armor in j:
                        j.remove(armor)
                        for z, s in {
                            "Iron Helmet" : 25, 
                            "Iron Chestplate" : 75,
                            "Iron Leggings" : 50,
                            "Iron Boots" : 15,
                            "Gold Helmet" : 25,
                            "Gold Chestplate" : 75,
                            "Gold Leggings" : 45,
                            "Gold Boots" : 10,
                            "Diamond Helmet" : 50, 
                            "Diamond Chestplate" : 150, 
                            "Diamond Leggings" : 125, 
                            "Diamond Boots" : 25,
                            "Excalibur Helmet" : 200,
                            "Excalibur Chestplate" : 400,
                            "Excalibur Leggings" : 300,
                            "Excalibur Boots" : 100}.items():
                            if armor == z:
                                self.equipedItem["Armor"][text[1]] = [z, s]
                                return
        print("\nArmor not Found\n")


    def useTools(self, tools):
        if self.inventory["Tools"] == []:
            print("\nTools Is Empty, Can't Use Tools\n")
            return
        for item in self.inventory["Tools"]:
            if item == tools:
                self.inventory["Tools"].remove(tools)
                print(f"\n{tools} successfully Used\n")
                for i, y in {
                    "Iron Sword" : 100,
                    "Gold Sword" : 75,
                    "Diamond Sword" : 100,
                    "Excalibur Sword" : [500 ,["World Slash", 9999], 100],
                    "Atomic Sword" : [750 ,["Atomic Blast", 99999], 250]}.items():
                    if tools == i:
                        return y
        return f"\n{tools} not Found\n"


    def printEquipedArmor(self):
        print("\n_____Armor_____")
        for i, y in self.equipedItem["Armor"].items():
            print(f"{i}: {y}")


    def printEquipedTool(self):
        if self.equipedItem["Tool"] is None:
            print("\nYou dont have a tool")
        else:
            print("\n_____Tool_____")
            print(f"{self.equipedItem["Tool"][0]}: {self.equipedItem["Tool"][1]}")


    def printItems(self):
        for value, item in self.inventory.items():
            print(f"{value}:")
            for i in item:
                if isinstance(i, list):
                    for x in i:
                        print(f"    {x}")
                else:
                    print(f"    {i}")


    def isMaxInv(self):
        total = 0
        for key, item in self.inventory.items():
            if key == 'Armor':
                for i in item:
                    for y in i:
                        total += len(y)
            else:
                total += len(item)
        return total >= 50


    def isEmpty(self):
        total = 0
        for key, item in self.inventory.items():
            if key == 'Armor':
                for i in item:
                    for y in i:
                        total += len(y)
            else:
                total += len(item)
        return total == 0


    def itemSort(self):
        for x, y in self.inventory.items():
            if x == "Armor":
                continue
            else:
                self.mergeSort(y)


    def mergeSort(self, array):
        if len(array) <= 1:
            return array
        
        middleIndex = len(array) // 2
        leftHalf = array[:middleIndex]
        rightHalf = array[middleIndex:]
        
        self.mergeSort(leftHalf)
        self.mergeSort(rightHalf)
        i = j = k = 0
        
        while i < len(leftHalf) and j < len(rightHalf):
            if leftHalf[i] <= rightHalf[j]:
                array[k] = leftHalf[i]
                i += 1
            else:
                array[k] = rightHalf[j]
                j += 1
            k += 1
        
        while i < len(leftHalf):
            array[k] = leftHalf[i]
            i += 1
            k += 1
        
        while j < len(rightHalf):
            array[k] = rightHalf[j]
            j += 1
            k += 1


    def isArmorEmpty(self):
        total = 0
        for key, item in self.inventory.items():
            if key == 'Armor':
                for i in item:
                    for y in i:
                        total += len(y)
        return total == 0


    def printArmor(self):
        for value, item in self.inventory.items():
            print("Armor:")
            for i in item:
                if isinstance(i, list):
                    for x in i:
                        print(f"    {x}")