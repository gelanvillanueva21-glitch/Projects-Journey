import random as ran

class Chance:
    def __init__(self):
        self.difficulty_loot_type = {
            "Easy" : self.easyLoot,
            "Medium" : self.mediumLoot,
            "Hard" : self.hardLoot
        }

    def __call__(self, difficulty):
        temporary_func = self.difficulty_loot_type.get(difficulty)
        return temporary_func

    def easyLoot(self):
        def potion():
            temporary_list = ["Potion"]
            potions = ["Health Potion", "Damage Potion", "Mana Potion", "Critical Potion", None, None]
            choice = ran.choice(potions)
            temporary_list.append(choice)
            return temporary_list

        def armor():
            temporary_list = ["Armor"]
            def iron():
                ironList = ["Iron Helmet", "Iron Chestplate", "Iron Leggings", "Iron Boots"]
                armorChoice = ran.choice(ironList)
                return armorChoice

            def gold():
                goldList = ["Gold Helmet", "Gold Chestplate", "Gold Leggings", "Gold Boots"]
                armorChoice = ran.choice(goldList)
                return armorChoice

            def diamond():
                diamondList = ["Diamond Helmet", "Diamond Chestplate", "Diamond Leggings", "Diamond Boots"]
                armorChoice = ran.choice(diamondList)
                return armorChoice

            def excalibur():
                excaliburList = ["Excalibur Helmet", "Excalibur Chestplate", "Excalibur Leggings", "Excalibur Boots"]
                armorChoice = ran.choice(excaliburList)
                return armorChoice

            armorType = {
                4 : iron,
                5 : gold,
                20 : diamond,
                250 : excalibur,
            }
            choice = ran.choice(list(armorType.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                temp_var = armorType.get(choice)
                temporary_list.append(temp_var())
                return temporary_list

        def tool():
            temporary_list = ["Tools"]
            toolList = {
                4 : "Iron Sword",
                5 : "Gold Sword",
                20 : "Diamond Sword",
                250 : "Excalibur Sword",
                500 : "Atomic Sword"
            }
            choice = ran.choice(list(toolList.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                temporary_list.append(toolList.get(choice))
                return temporary_list

        def others():
            pass

        loot = [potion, armor, tool]
        random_choice = ran.choice(loot)
        return random_choice()


    def mediumLoot(self):
        def potion():
            potions = ["Health Potion", "Damage Potion", "Mana Potion", "Critical Potion", None, None]
            choice = ran.choice(potions)
            return choice

        def armor():
            def iron():
                ironList = ["Iron Helmet", "Iron Chestplate", "Iron Leggings", "Iron Boots"]
                armorChoice = ran.choice(ironList)
                return armorChoice

            def gold():
                goldList = ["Gold Helmet", "Gold Chestplate", "Gold Leggings", "Gold Boots"]
                armorChoice = ran.choice(goldList)
                return armorChoice

            def diamond():
                diamondList = ["Diamond Helmet", "Diamond Chestplate", "Diamond Leggings", "Diamond Boots"]
                armorChoice = ran.choice(diamondList)
                return armorChoice

            def excalibur():
                excaliburList = ["Excalibur Helmet", "Excalibur Chestplate", "Excalibur Leggings", "Excalibur Boots"]
                armorChoice = ran.choice(excaliburList)
                return armorChoice

            armorType = {
                4 : iron,
                5 : gold,
                20 : diamond,
                400 : excalibur,
            }
            choice = ran.choice(list(armorType.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                return armorType.get(choice)

        def tool():
            toolList = {
                4 : "Iron Sword",
                5 : "Gold Sword",
                20 : "Diamond Sword",
                400 : "Excalibur Sword",
                7000 : "Atomic Sword"
            }
            choice = ran.choice(list(toolList.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                return toolList.get(choice)

        def others():
            pass

        loot = [potion, armor, tool, others]
        random_choice = ran.choice(loot)
        return random_choice()


    def hardLoot(self):
        def potion():
            potions = ["Health Potion", "Damage Potion", "Mana Potion", "Critical Potion", None, None, None, None]
            choice = ran.choice(potions)
            return choice

        def armor():
            def iron():
                ironList = ["Iron Helmet", "Iron Chestplate", "Iron Leggings", "Iron Boots"]
                armorChoice = ran.choice(ironList)
                return armorChoice

            def gold():
                goldList = ["Gold Helmet", "Gold Chestplate", "Gold Leggings", "Gold Boots"]
                armorChoice = ran.choice(goldList)
                return armorChoice

            def diamond():
                diamondList = ["Diamond Helmet", "Diamond Chestplate", "Diamond Leggings", "Diamond Boots"]
                armorChoice = ran.choice(diamondList)
                return armorChoice

            def excalibur():
                excaliburList = ["Excalibur Helmet", "Excalibur Chestplate", "Excalibur Leggings", "Excalibur Boots"]
                armorChoice = ran.choice(excaliburList)
                return armorChoice

            armorType = {
                4 : iron,
                5 : gold,
                20 : diamond,
                500 : excalibur,
            }
            choice = ran.choice(list(armorType.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                return armorType.get(choice)

        def tool():
            toolList = {
                4 : "Iron Sword",
                5 : "Gold Sword",
                20 : "Diamond Sword",
                500 : "Excalibur Sword",
                1000 : "Atomic Sword"
            }
            choice = ran.choice(list(toolList.keys()))
            random_number = ran.randint(1, choice)
            if random_number == choice:
                return toolList.get(choice)

        def others():
            pass

        loot = [potion, armor, tool, others]
        random_choice = ran.choice(loot)
        return random_choice()