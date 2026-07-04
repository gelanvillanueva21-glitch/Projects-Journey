import time
import sys

def description(speed=2.5):
    text = [
    "\n\n=== WELCOME TO THE RPG TEXT BASED GAME ===\n",
    "Welcome to this text-based RPG. You can choose from three difficulty\n",
    "levels: Easy, Medium, and Hard, each offering a unique gameplay\n",
    "experience.\n",
    "Bosses only appear in Medium and Hard modes. Hard mode features even\n",
    "more complex gameplay, including two distinct boss types: a Normal\n",
    "Boss that can spawn randomly in any level 2 room, and a massive World\n",
    "Boss that waits for you at the end of Level 5. Finally, every room features\n",
    "unique item drops awarded once you defeat all enemies or the area boss.\n"
    ]
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
    enemy = {
    "Easy" : {
        "Slime" : [100, 10],
        "Goblin" : [150, 20],
        "Skeleton" : [200, 30],
        "Zombie" : [200, 40],
    },
    "Medium" : {
        "Vampire" : [300, 50],
        "Werewolf" : [300, 75],
        "Giant Zombie" : [500, 100],
        "Demon" : [650, 150],
        "Demonic Knight Boss" : [5000, 250]
    },
    "Hard" : {
        "Demon Vampire" : [1000, 150],
        "Possessed Werewolf" : [1000, 200],
        "Possessed Giant Zombie" : [1500, 250],
        "Devil Boss" : [10000, 500],
        "Demonic King Boss" : [15000, 1000],
        "Demon Lord Of The Last Boss" : [100000, 5000]
    }
}
    for difficulty, enem in enemy.items():
        print(f"{difficulty} Enemies:")
        for name, stats in enem.items():
            print(f"    {name} - HP: {stats[0]}, Damage: {stats[1]}")
            time.sleep(0.5)
    print()