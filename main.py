import random
import os
import time
from tkinter import *


class enemy():
    def __init__(self, name, dmg, hp, gold):
        self.name = name
        self.damage = dmg
        self.hitpoints = hp
        self.gold_drop = gold

    def attack(self):
        damage = 0
        for a in range(0, self.damage):
            damage += random.randint(1, 6)
        return damage


class weapon():
    def __init__(self, name, dmg, du):
        self.name = name
        self.damage = dmg
        self.durability = du

    def damaged(self):
        self.damage -= 1


class armor():
    def __init__(self, name, defe, du):
        self.name = name
        self.defence = defe
        self.durability = du

    def damaged(self):
        self.defence -= 1


dict_file_path = os.path.split(os.path.realpath(__file__))[0]
print(os.path.split(os.path.realpath(__file__)))
ENEMY_DATA_FILE = dict_file_path + os.sep + 'enemyData.txt'
ARMOR_DATA_FILE = dict_file_path + os.sep + 'armorData.txt'
print(ARMOR_DATA_FILE)
WEAPON_DATA_FILE = dict_file_path + os.sep + 'weaponData.txt'
SCOREBOARD_FILE = dict_file_path + os.sep + 'scoreboard.txt'

enemies = []
weapons = []
armors = []
chance_event_happen = [3, 2, 1, 4]
possible_events = ["nothing", "heal", "equipment", "enemy"]


def importEnemyData():
    try:
        with open(ENEMY_DATA_FILE, "r") as datas:
            data = [dt.strip().split(",") for dt in datas]
            for a in data:
                enemies.append(enemy(a[0], int(a[1]), int(a[2]), int(a[3])))

    except FileNotFoundError:
        fileNotFoundErrorText("enemyData")
    except PermissionError:
        permissionErrorText("enemyData")


def importWeaponData():
    try:
        with open(WEAPON_DATA_FILE, "r") as datas:
            data = [dt.strip().split(",") for dt in datas]
            for a in data:
                weapons.append(weapon(a[0], int(a[1]), int(a[2])))

    except FileNotFoundError:
        fileNotFoundErrorText("weaponData.txt")
    except PermissionError:
        permissionErrorText("weaponData.txt")


def importArmorData():
    try:
        with open(ARMOR_DATA_FILE, "r") as datas:
            data = [dt.strip().split(",") for dt in datas]
            for a in data:
                armors.append(armor(a[0], int(a[1]), int(a[2])))

    except FileNotFoundError:
        fileNotFoundErrorText("armorData")
    except PermissionError:
        permissionErrorText("armorData")


def permissionErrorText(fileName):
    print("ERROR")
    print("You do not have the permission to access the file.")
    print(f"{fileName}.txt might be a directory.", flush=True)
    time.sleep(0.2)
    quit()


def fileNotFoundErrorText(fileName):
    print("ERROR")
    print(f"The file {fileName}.txt is not found.")
    print(f"Please check if there is a file named {fileName}.txt", flush=True)
    time.sleep(0.2)
    quit()


def start_game():
    left_button.configure(text="return to surface", command=lambda: ask_if_quit())
    right_button.configure(text="heal", command=lambda: heal())
    generate_event()


def ask_if_quit():
    game_text_label.configure(text="please confirm that you want to\nquit this game")
    left_button.configure(text="Quit", command=lambda: quit())
    right_button.configure(text="cancel", command=lambda: not_quit())
    middle_button.configure(text="save score to scoreboard.", command=lambda: save_score())


def save_score():
    player_name = player_name_entry.get().strip()
    game_text_label.configure(
        text=f"please enter your user name in the text box\nnext to the name label\nyour current name is '{player_name}'")
    middle_button.configure(text="save", command=lambda: check_if_name_valid())


def check_if_name_valid():
    name = player_name_entry.get().strip()
    if not 0 < len(name) < 20 or len(name.split() > 1):
        game_text_label.configure(
            text="name need to be shorter than 20 characters,\ncan not be blank, and can't contain spaces")
    else:
        score = gold_amount_label.cget("text")
        try:
            file = open(SCOREBOARD_FILE, "r")
            datas = file.readlines()
            scores = []
            for data in datas:
                scores.append(data.strip().split())
            file.close()
            scores.append([name, score])
            scores = sorted(scores, key=lambda _: _[1], reverse=True)
            file = open(SCOREBOARD_FILE, "w")
            for a in scores:
                file.write(f"{a[0]} {a[1]}\n")
            file.close()
            game_text_label.configure(text="Score is saved")
            middle_button.configure(text="play again", command=lambda: reset_game())
        except FileNotFoundError:
            fileNotFoundErrorText("scoreboard")
        except PermissionError:
            permissionErrorText("scoreboard")


def not_quit():
    game_text_label.configure(text="So you are staying around HUH!")
    left_button.configure(text="quit", command=lambda: ask_if_quit())
    middle_button.configure(text="continue", command=lambda: generate_event())
    check_heal()


def check_heal():
    tmp = heal_amount_label.cget("text")
    if tmp == 0:
        right_button.configure(text="", command=lambda: None)
    else:
        right_button.configure(text="heal", command=heal())


def generate_event():
    global current_event
    possible_events = ["nothing", "heal", "equipment", "enemy"]
    current_event = random.choices(possible_events, weights=chance_event_happen)
    middle_button.configure(text="continue")
    if current_event[0] == "nothing":
        event_nothing()
    elif current_event[0] == "heal":
        event_heal()
    elif current_event[0] == "equipment":
        event_equipment()
    elif current_event[0] == "enemy":
        event_enemy()


def heal():
    potion_amount = heal_amount_label.cget("text")
    potion_amount -= 1
    heal_amount_label.configure(text=potion_amount)
    if potion_amount == 0:
        right_button.configure(command=lambda: None)
    player_health = health_stat_label.cget("text")
    heal_amount = random.randint(10, 25)
    game_text_label.configure(text=f"You heal yourself of {heal_amount} hitpoints")
    player_health += heal_amount
    if player_health > 100:
        health_stat_label.configure(text=100)
    else:
        health_stat_label.configure(text=player_health)


def event_enemy():
    global current_enemy
    current_enemy = random.choice(enemies)
    enemy_hp = 0
    for a in range(0, current_enemy.hitpoints):
        enemy_hp += random.randint(1, 6)
    current_enemy.hp = enemy_hp
    game_text_label.configure(text=f"You have enountered {current_enemy.name}.\nprepare for battle")
    middle_button.configure(command=lambda: event_combat())


def event_nothing():
    game_text_label.configure(text="You progress onward without concern")


def event_equipment():
    game_text_label.configure(text="found equipment")
    print(16)


def event_heal():
    game_text_label.configure(text="congradulations, you found a healing potion")
    potion_amount = heal_amount_label.cget("text")
    if potion_amount == 0:
        right_button.configure(text="heal", command=lambda: heal())
    potion_amount += 1
    heal_amount_label.configure(text=potion_amount)


def event_combat():
    enemy_damage = current_enemy.attack()
    player_hp = health_stat_label.cget("text")
    player_hp -= enemy_damage
    player_damage = get_player_damage()
    game_text_label.configure(
        text=f"You fight!\nYou deal {player_damage} damage to the enemy.\nThey deal {enemy_damage} damage to you.")
    if player_hp <= 0:
        game_over()
    else:
        health_stat_label.configure(text=player_hp)
    current_enemy.hitpoints -= player_damage
    if current_enemy.hitpoints <= 0:
        middle_button.configure(command=lambda: battle_victory())


def game_over():
    health_stat_label.configure(text=0)
    gold_amount_label.configure(text=0)
    game_text_label.configure(text="You died and lost all of\nyour gold. No one will ever\nknow of your achievements")
    middle_button.configure(text="Restart?", command=lambda: reset_game())
    left_button.configure(text="quit", command=lambda: quit())
    right_button.configure(text="", command=lambda: None)


def reset_game():
    weapon_stats_label.configure(text="None")
    armor_stats_label.configure(text="None")
    health_stat_label.configure(text=100)
    gold_amount_label.configure(text=0)
    heal_amount_label.configure(text=3)
    game_text_label.configure(text="click button below to continue")
    left_button.configure(text="return to surface", command=lambda: ask_if_quit())
    middle_button.configure(text="continue", command=lambda: generate_event())
    right_button.configure(text="heal", command=lambda: heal())


def battle_victory():
    enemy_gold_drop = 0
    for a in range(0, current_enemy.gold_drop):
        enemy_gold_drop += random.randint(1, 6)
    player_gold = gold_amount_label.cget("text")
    player_gold += enemy_gold_drop
    game_text_label.configure(text=f"You defeated the enemy and\nscavenged {enemy_gold_drop} gold pieces.")
    gold_amount_label.configure(text=player_gold)
    middle_button.configure(command=lambda: generate_event())


def get_player_damage():
    player_damage = random.randint(2, 7)
    return player_damage


importArmorData()
importEnemyData()
importWeaponData()

window = Tk()
window.geometry("480x320")
window.title("new and improved dungen game")
Font = ("Ariel", 15)

player_label = Label(window, text="Name: ", font=Font)
player_label.grid(row=0, column=0, sticky="w")

weapon_label = Label(window, text="Weapon:", font=Font)
weapon_label.grid(row=1, column=0, sticky="w")

armor_label = Label(window, text="Armor: ", font=Font)
armor_label.grid(row=2, column=0, sticky="w")

health_label = Label(window, text="Health: ", font=Font)
health_label.grid(row=0, column=2, sticky="w")

gold_label = Label(window, text="Gold: ", font=Font)
gold_label.grid(row=1, column=2, sticky="w")

heal_label = Label(window, text="Heal: ", font=Font)
heal_label.grid(row=2, column=2, sticky="w")

weapon_stats_label = Label(window, text="None", font=Font)
weapon_stats_label.grid(row=1, column=1, sticky="w")

armor_stats_label = Label(window, text="None", font=Font)
armor_stats_label.grid(row=2, column=1, sticky="w")

health_stat_label = Label(window, text=100, font=Font)
health_stat_label.grid(row=0, column=3, sticky="w")

gold_amount_label = Label(window, text=0, font=Font)
gold_amount_label.grid(row=1, column=3, sticky="w")

heal_amount_label = Label(window, text=3, font=Font)
heal_amount_label.grid(row=2, column=3, sticky="w")

game_text_label = Label(window, text="Click below to start your adventure", font=Font)
game_text_label.grid(row=3, column=0, columnspan=4, sticky="ew")

player_name_entry = Entry(window)
player_name_entry.grid(row=0, column=1, sticky="w")

left_button = Button(window, text="", command=lambda: None)
left_button.grid(row=4, column=0, sticky="ew")

right_button = Button(window, text="", command=lambda: None)
right_button.grid(row=4, column=3, sticky="ew")

middle_button = Button(window, text="start your quest", command=lambda: start_game())
middle_button.grid(row=4, column=1, columnspan=2, sticky="ew")

for col_num in range(window.grid_size()[0]):
    window.columnconfigure(col_num, minsize=120)

window.mainloop()


