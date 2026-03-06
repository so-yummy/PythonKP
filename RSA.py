#RSA.py - генерация ключей

import random
from Func import Generator

#Создание параметров RSA
class RSA:
    def __init__(self, bit=64, c=False, st=False):

        # Генерация простых чисел p и q
        if st:
            self.p = Generator.GenStrongPr(bit // 2)    # Генерация сильных простых чисел
            self.q = Generator.GenStrongPr(bit // 2)
        else:
            self.p = Generator.GenPr(bit // 2)       # Генерация обычных простых чисел
            self.q = Generator.GenPr(bit // 2)

        # Приблежение q и p в целях демонстрации  уязвимости RSA
        if c:
            delt = random.randint(2, 100)      #Смещение случайное малое
            self.q = self.p + delt                   #Приближение значения  q к p
            while not Generator.MillerRabin(self.q):    #Проверка q на простоту, увеличение в случае если не является простым
                self.q += 1

        #Вычисление модуля RSA
        self.n = self.p * self.q

        # Вычисление функции Эйлера
        phi = (self.p - 1) * (self.q - 1)

        # Открытая экспонента
        self.e = 65537

        # Проверка взаимной простоты
        while math.gcd(self.e, phi) != 1:
            self.e += 2

        # Закрытая экспонента
        self.d = pow(self.e, -1, phi)
