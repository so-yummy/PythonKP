#Graph - графическое представление
# Построить графики зависимости времени взлома от
# Размера ключа
# Близости чисел p и q
# Наличия/отсутствия требований к «сильным» простым числам

import matplotlib.pyplot as plt
import numpy as np

def PlotRes(df):    #График зависимости среднего времени факторизации от размера ключа.

    # Область построения
    plt.figure(figsize=(8, 5))

    # Группировка по параметрам
    for (c, strong), group in df.groupby(["c", "strong"]):
        grouped = group.groupby("bit")["time"].mean()   # Усреднение времени по размеру ключа

        label = f"простые={c}, сильные={strong}"           # Подписи

        #Построение линии
        plt.plot(grouped.index, grouped.values, marker="o", linewidth=2, label=label)   #Передача значний и обозначения в графике

    #Оформление графика (Подписи осей, заголовок, легенда, решетка, демонстрация)
    plt.xlabel("Размер ключа")
    plt.ylabel("Среднее время факторизации")
    plt.title("Зависимость времени взлома RSA от размера ключа")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def PlotWithTheory(df):   #Сравнение экспериментальных данных с теоретическим ростом сложности.
        plt.figure(figsize=(8, 5))

        grouped = df.groupby("bit")["time"].mean()  # Среднее время по каждому размеру ключа

        # Построение экспериментальной кривой
        plt.plot(grouped.index, grouped.values, marker="o", linewidth=2, label="Эксперимент")

        # Теоретическая оценка роста сложности
        bits = np.array(grouped.index)
        theory = 2 ** (bits / 8)      # Экспоненциальный рост
        theory = theory / max(theory) * max(grouped.values)     #Нормировка теоретической кривой

        plt.plot(bits, theory, linestyle="--", label="Теоретический рост")

        # Оформление графика
        plt.xlabel("Размер ключа")
        plt.ylabel("Время")
        plt.title("Эксперимент и теория")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def PlotExperiments(df):        # Отображение экспериментов

    plt.figure(figsize=(8, 5))

    #Маркеры значений
    markers = {True: "s", False: "o"}

    counter = 1  # Счетчик экспериментов

    # Группировка по типу простых чисел
    for (c, strong), group in df.groupby(["c", "strong"]):

        label = f"простые={c}, сильные={strong}"

        plt.scatter(group["bit"], group["time"], s=100, marker=markers[c], label=label)  # Отображение точек экспериментов

        # Нумерация точек
        for _, row in group.iterrows():
            plt.text(row["bit"], row["time"], str(counter), fontsize=9, ha='right', va='bottom')    #Параметры отображения
            counter += 1

    # Подписи осей, заголовок, легенда, решетка, демонстрация
    plt.xlabel("Размер ключа (бит)")
    plt.ylabel("Время факторизации (сек)")
    plt.title("Распределение времени взлома")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



