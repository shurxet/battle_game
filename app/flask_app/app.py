from flask import Flask, render_template, request

from app.game_logic.class_arena import Arena
from app.game_logic.class_equipment import equipment
from app.game_logic.classes_heroes import classes
from app.game_logic.unit import PlayerUnit, EnemyUnit


data_start = {
    "header_hero": "Выберите героя",  # для названия страниц
    "header_enemy": "Выберите противника",  # для названия страниц
    "classes": classes,  # для названия классов
    "weapons": equipment.get_weapons_names(),  # для названия оружия
    "armors": equipment.get_armors_names(),  # для названия брони
    "weapon": equipment,  # для получения объекта оружия по имени
    "armor": equipment  # для получения брони оружия по имени
}

arena = {
    "arena": Arena()
}

players_instances = {}

form_data = {}


app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():

    return render_template("hero_choosing.html", data_start=data_start, header=data_start["header_hero"])


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    form_data["name_player"] = request.values["name"]
    form_data["class_player"] = request.values["unit_class"]
    form_data["weapon_player"] = request.values["weapon"]
    form_data["armor_player"] = request.values["armor"]

    players_instances["player"] = PlayerUnit(form_data["name_player"], classes[form_data["class_player"]])

    weapon_player_obj = data_start["weapon"].get_weapon(form_data["weapon_player"])
    armor_player_obj = data_start["armor"].get_armor(form_data["armor_player"])

    players_instances["player"].equip_weapon(weapon_player_obj)
    players_instances["player"].equip_armor(armor_player_obj)

    return render_template("enemy_choosing.html", data_start=data_start, header=data_start["header_enemy"])


@app.route("/fight/", methods=['post', 'get'])
def start_fight():
    form_data["name_enemy"] = request.values["name"]
    form_data["class_enemy"] = request.values["unit_class"]
    form_data["weapon_enemy"] = request.values["weapon"]
    form_data["armor_enemy"] = request.values["armor"]

    players_instances["enemy"] = EnemyUnit(form_data["name_enemy"], classes[form_data["class_enemy"]])

    weapon_enemy_obj = data_start["weapon"].get_weapon(form_data["weapon_enemy"])
    armor_enemy_obj = data_start["armor"].get_armor(form_data["armor_enemy"])

    players_instances["enemy"].equip_weapon(weapon_enemy_obj),
    players_instances["enemy"].equip_armor(armor_enemy_obj)

    battle_result = arena["arena"].start_game(players_instances["player"], players_instances["enemy"])

    return render_template("fight.html", players_instances=players_instances, battle_result=battle_result)


@app.route("/fight/hit")
def hit():
    battle_result = arena["arena"].player_hit()

    return render_template("fight.html", players_instances=players_instances, battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
    battle_result = arena["arena"].player_use_skill()

    return render_template("fight.html", players_instances=players_instances, battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    battle_result = arena["arena"].next_turn()

    return render_template("fight.html", players_instances=players_instances, battle_result=battle_result)


@app.route("/fight/end-fight")
def end_fight():
    arena["arena"].stop_game()

    return render_template("index.html")
