from dataclasses import dataclass
from typing import List
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        unknown = marshmallow.EXCLUDE


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    armors: List[Armor]
    weapons: List[Weapon]


class Equipment:
    def __init__(self):
        self.equipment: EquipmentData = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        for x in self.equipment.weapons:
            if weapon_name in x.name:
                return x

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        for x in self.equipment.armors:
            if armor_name in x.name:
                return x

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        weapon = self.equipment.weapons
        return weapon

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        armor = self.equipment.armors
        return armor

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        with open("app/data/equipment.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)

        except marshmallow.exceptions.ValidationError:
            raise ValueError


equipment = Equipment()
