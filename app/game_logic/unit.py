from __future__ import annotations

import random
from abc import ABC, abstractmethod

from app.game_logic.class_equipment import Weapon, Armor, Equipment
from app.game_logic.classes_heroes import UnitClass

from typing import Optional, Callable


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return self.hp  # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return self.stamina  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit, damage_random: float) -> round(float, 1):
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        self.stamina = round(self.stamina - self.weapon.stamina_per_hit, 1)
        health = 0
        stamina = 0
        # если игрок пробил броню соперника
        if damage_random > target.armor.defence:
            # то из здоровья соперника вычитается урон
            health += target.hp - damage_random
            # если выносливости не хватает для брони
            if target.stamina < target.armor.stamina_per_turn:
                # то выносливость остаётся прежней
                stamina += target.stamina
            # если хватает выносливости для брони
            else:
                # то вычитаем выносливость
                stamina += target.stamina - target.armor.stamina_per_turn
            target.get_damage(health, stamina)
            damage = round(damage_random, 1)
            return damage
        # если не пробил
        else:
            # то здоровье остаётся прежним
            health += target.hp
            # если выносливости не хватает для брони
            if target.stamina < target.armor.stamina_per_turn:
                # то выносливость остаётся прежней
                stamina += target.stamina
            # если выносливости хватает
            else:
                # то вычитается выносливасть которую соперник использовал для брони
                stamina += target.stamina - target.armor.stamina_per_turn
            target.get_damage(health, stamina)

    def get_damage(self, damage: float, stamina: float):
        # TODO получение урона целью
        #  присваиваем новое значение для аттрибута self.hp
        if damage < 0:
            self.hp = 0
        else:
            self.hp = round(damage, 1)
        if stamina < 0:
            self.stamina = 0
        else:
            self.stamina = round(stamina, 1)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Умение использавано"
        else:
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        # TODO результат функции должен возвращать следующие строки:
        damage_random = random.uniform(self.weapon.min_damage, self.weapon.max_damage)
        if self.stamina >= self.weapon.stamina_per_hit:
            if damage_random > target.armor.defence:
                damage = self._count_damage(target, damage_random)
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            self._count_damage(target, damage_random)
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):
     def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        if not self._is_skill_used:
            skill = bool(random.randint(0, 1))
            if skill:
                return self.use_skill(target=target)
        damage_random = random.uniform(self.weapon.min_damage, self.weapon.max_damage)
        if self.stamina >= self.weapon.stamina_per_hit:
            if damage_random > target.armor.defence:
                damage = self._count_damage(target, damage_random)
                # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
            self._count_damage(target, damage_random)
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
