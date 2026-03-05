# Exp.py - эксперимент
# Провести эксперимент: сгенерировать 100 пар ключей разного качества и измерить время их взлома

import time
import pandas as pd
from RSA import RSA
from Factor import Factorization


class Experiment:
    # samp - количество повторений, bit - размер ключа, c - близкие простые числа, st - сильные простые
    @staticmethod
    def run(samp=5, bit=64, c=False, st=False):

        result = []     #Список накопленных результатов

        #Повтор эксперимента некоторого кол-ва раз
        for _ in range(samp):
            # Генерация RSA с новыми параметрами (параметрами являются простые числа)
            rsa = RSA(bit=bit, c=c, st=st)

            start = time.perf_counter()         # Измерение времени факторизации методом Ферма
            Factorization.Fermat(rsa.n)         #Попытка разложения числа n
            elapsed = time.perf_counter() - start       #Вычисление времени

            #Фиксация значений, размер ключа, какие простые использовались, время факторизации
            result.append({"bit": bit, "c": c, "strong": st, "time": elapsed})

        df = pd.DataFrame(result)   # Формирование таблицы результатов
        return df