from dataclasses import dataclass

from app.game_logic.classes_skills import Skill, HardShot, FuryPunch


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorHero = UnitClass(
    name="Воин",
    max_health=80.5,
    max_stamina=70.5,
    attack=0,
    stamina=0,
    armor=0,
    skill=HardShot()
)  # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

ThiefHero = UnitClass(
    name="Вор",
    max_health=70.3,
    max_stamina=60.3,
    attack=0,
    stamina=0,
    armor=0,
    skill=FuryPunch()
)  # TODO действуем так же как и с войном


classes = {
    ThiefHero.name: ThiefHero,
    WarriorHero.name: WarriorHero
}
