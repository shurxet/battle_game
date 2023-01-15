from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina >= self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            self.user._is_skill_used = True
            return self.skill_effect()

        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Яростный удар"
    stamina = 5
    damage = 10

    def skill_effect(self):
        # TODO логика использования скилла -> return str
        # TODO в классе нам доступны экземпляры user и target - можно использовать любые их методы
        # TODO именно здесь происходит уменшение стамины у игрока применяющего умение и
        # TODO уменьшение здоровья цели.
        # TODO результат применения возвращаем строкой
        target_health = self.target.hp - self.damage
        user_stamina = self.user.stamina - self.stamina
        if target_health < 0:
            target_health = 0
        if user_stamina < 0:
            user_stamina = 0
        self.target.hp = round(target_health, 1)
        self.user.stamina = round(user_stamina, 1)
        return f"{self.user.name} используя умение {self.name} наносит Вам {self.damage} урона."


class HardShot(Skill):
    name = "Жесткий выстрел"
    stamina = 8
    damage = 15

    def skill_effect(self):
        target_health = self.target.hp - self.damage
        user_stamina = self.user.stamina - self.stamina
        if target_health < 0:
            target_health = 0
        if user_stamina < 0:
            user_stamina = 0
        self.target.hp = round(target_health, 1)
        self.user.stamina = round(user_stamina, 1)
        return f"{self.user.name} используя умение {self.name} наносит противнику {self.damage} урона."
