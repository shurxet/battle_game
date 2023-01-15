from typing import Tuple

from app.game_logic.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = None
    __motion_player = True
    __motion_enemy = True
    winner = None
    was_skill_player = False
    was_skill_enemy = False
    skill_activated = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        # TODO НАЧАЛО ИГРЫ -> None
        # TODO присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        self.player = player
        self.enemy = enemy
        # TODO а также выставляем True для свойства "началась ли игра"
        self.game_is_running = True
        return "БОЙ НАЧАЛСЯ!"

    def stop_game(self):
        return self._end_game()

    def _check_players_hp(self) -> str | bool:
        # TODO ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # TODO проверка здоровья игрока и врага и возвращение результата строкой:
        # TODO может быть три результата:
        # TODO Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # TODO если Здоровья игроков в порядке то ничего не происходит
        if self.player.hp == 0 and self.enemy.hp == 1:
            self.winner = "Ничья!"
            return self.winner
        elif self.player.hp > 0 and self.enemy.hp == 0:
            self.winner = self.player.name
            return f"{self.player.name} выиграл битву!"
        elif self.enemy.hp > 0 and self.player.hp == 0:
            self.winner = self.enemy.name
            return f"{self.enemy.name} выиграл битву!"
        else:
            return True

    def _stamina_regeneration(self):
        # TODO регенерация здоровья и стамины для игрока и врага за ход
        # TODO в этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # TODO главное чтобы оно не привысило максимальные значения (используйте if)
        if self.__motion_player:
            self.player.hp += self.STAMINA_PER_ROUND
            self.player.stamina += self.STAMINA_PER_ROUND
        else:
            self.player.stamina += (self.STAMINA_PER_ROUND * 2)
        if self.player.hp > self.player.unit_class.max_health:
            self.player.hp = self.player.unit_class.max_health
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina

        self.enemy.hp += self.STAMINA_PER_ROUND
        self.enemy.stamina += self.STAMINA_PER_ROUND
        if self.enemy.hp > self.enemy.unit_class.max_health:
            self.enemy.hp = self.enemy.unit_class.max_health
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self) -> tuple[str, str | bool] | tuple[str, str, str | bool] | tuple[str, str]:
        # TODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # TODO срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        # TODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # TODO если result -> возвращаем его
        # TODO если же результата пока нет и после завершения хода игра продолжается,
        # TODO тогда запускаем процесс регенирации стамины и здоровья для игроков (self._stamina_regeneration)
        # TODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага
        self.__motion_player = False
        result = self.player_hit()
        return result

    def _end_game(self):
        # TODO КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # TODO очищаем синглтон - self._instances = {}
        # TODO останавливаем игру (game_is_running)
        # TODO возвращаем результат
        self.player = None
        self.enemy = None
        self.__motion_player = True
        self.__motion_enemy = True
        self.winner = None
        self.was_skill_player = False
        self.was_skill_enemy = False
        self.skill_activated = False
        self._instances = {}
        self.game_is_running = False

    def player_hit(self) -> tuple[str, str | bool] | tuple[str, str, str | bool] | tuple[str, str]:
        # TODO КНОПКА УДАР ИГРОКА -> return result: str
        # TODO получаем результат от функции self.player.hit
        # TODO запускаем следующий ход
        # TODO возвращаем результат удара строкой
        result = {
            "player": "",
            "enemy": "",
            "winner": "",
            "status": ""
        }
        if self.winner is None:
            if self.skill_activated:
                player_result_skill = self.player.use_skill(self.enemy)
                result["player"] = player_result_skill
                self.skill_activated = False
            else:
                if self.__motion_player:
                    player_result = self.player.hit(self.enemy)
                    result["player"] = player_result
                else:
                    player_result = f"{self.player.name} пропустил ход!"
                    result["player"] = player_result
            enemy_result = self.enemy.hit(self.player)
            result["enemy"] = enemy_result
            self._check_players_hp()
            if self.winner is not None:
                if self.winner == self.player.name:
                    result["winner"] = self._check_players_hp()
                    return result["player"], result["winner"]
                elif self.winner == self.enemy.name:
                    result["winner"] = self._check_players_hp()
                    return result["player"], result["enemy"], result["winner"]
                else:
                    result["winner"] = self._check_players_hp()
                    return result["player"], result["enemy"], result["winner"]
            else:
                self._stamina_regeneration()
                self.__motion_player = True
                return result["player"], result["enemy"]
        else:
            result["status"] = "Бой завершён!"
            result["winner"] = self._check_players_hp()
            return result["status"], result["winner"]

    def player_use_skill(self):
        # TODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # TODO получаем результат от функции self.use_skill
        # TODO включаем следующий ход
        # TODO возвращаем результат удара строкой
        self.skill_activated = True
        self.__motion_player = False
        result = self.player_hit()
        return result
