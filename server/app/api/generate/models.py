import math
import random

from   app.api.generate.schema import GetPass

class PassGenerate:

    @staticmethod
    async def generate(length: int, low_str: bool, hight_str: bool, symbol: bool, number: bool) -> GetPass:
        """ Метод для генерации пароля """

        alpha    = 'abcdefghijklmnopqrstuvwxyz'
        symbols  = '!@#$%^&*~'
        numbers  = '0123456789'

        pre_set  = []
        power    = 0
        password = {"Ваш пароль": "", "Уровень сложности пароля": ""}

        # собираем все пре-сеты условий в массив
        if low_str  :
            pre_set.append(alpha)
            power += 26
        if hight_str:
            pre_set.append(alpha.upper())
            power += 26
        if symbol   :
            pre_set.append(symbols)
            power += 9
        if number   :
            pre_set.append(numbers)
            power += 10

        # проверка на выборку параметров
        if not pre_set:

            return GetPass(generate_pass={'Пароль не сгенерирован': 'Не выбран ни один параметр'})

        # генерация
        for char in range(length):
            rand_set                 = random.choice(pre_set)
            password["Ваш пароль"]   += random.choice(rand_set)

        # сложность пароля как произведение его длины на логарифм по основанию 2 от мощности
        entropy = length * math.log2(power)

        if entropy < 36   : password["Уровень сложности пароля"] = "Слабый"
        elif entropy < 60 : password["Уровень сложности пароля"] = "Средний"
        elif entropy < 128: password["Уровень сложности пароля"] = "Сильный"
        else              : password["Уровень сложности пароля"] = "Очень сильный"

        return GetPass(generate_pass=password)
