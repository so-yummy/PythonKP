# Реализовать атаку по времени на упрощенной теоретическая реализации и предложить методы защиты (теоретические сведения)
import time

class TimingAttack:

    #Уязвимая реализация модульного возведения в степень
    @staticmethod
    def VulnerPow(base, exp, mod):

        # Начальное значение результата
        result = 1

        # Перебор битов секретного ключа
        for bit in bin(exp)[2:]:
            result = (result * result) % mod        # Шаг возведения в квадрат

            # Если текущий бит равен 1, то осуществляется дополнительное умножение
            if bit == '1':
                result = (result * base) % mod
        return result

    #Измерение времени выполнения операции
    @staticmethod
    def MeasureTime(base, exp, mod):

        start = time.perf_counter()         # Фиксация начального момента времени
        TimingAttack.VulnerPow(base, exp, mod)      # Выполнение уязвимой операции
        return time.perf_counter() - start      # Возврат затраченного времени
