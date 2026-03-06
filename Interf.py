# Interf.py - расширенный интерфейс RSA

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from Func import Generator
from Exp import Experiment
import Graph
from RSA import RSA
from TimingAttack import TimingAttack      

# Интерфейс
class Gui:

    # Инициализация интерфейса
    def __init__(self, root):
        self.root = root                #Ссылка на окно
        self.root.title("RSA")          #Заголовок окна
        self.root.geometry("520x550")   #Размер
        self.res = None                 #Хранение результатов

        self.rsa = None                 #Параметры RSA
        self.params = None              

        # Параметры эксперимента
        ttk.Label(root, text="Размер ключа:").pack(pady=5)    #Подпись
        self.bitsentry = ttk.Entry(root)    # Поле ввода
        self.bitsentry.pack()

        ttk.Label(root, text="Количество экспериментов:").pack(pady=5) #Подпись
        self.sampentry = ttk.Entry(root)    # Поле ввода
        self.sampentry.pack()

        # Переменная выбора типа простых
        self.prtype = tk.StringVar(value="normal")

        ttk.Label(root, text="Тип простых чисел:").pack(pady=5)

        # Фрейм для размещения в одну строку
        radfr = ttk.Frame(root)
        radfr.pack(pady=5)

        #кнопки выбора
        ttk.Radiobutton(radfr, text="Обычные", variable=self.prtype, value="normal").pack(side="left", padx=10)
        ttk.Radiobutton(radfr, text="Близкие", variable=self.prtype, value="close").pack(side="left", padx=10)
        ttk.Radiobutton(radfr, text="Сильные", variable=self.prtype, value="strong").pack(side="left", padx=10)

        ttk.Button(root, text="Запустить эксперимент", command=self.RunExper).pack(pady=10)     #Запуск эксперимента

        # Фрейм для размещения 2 кнопок в одной строке
        btnfr = ttk.Frame(root)
        btnfr.pack(pady=15)

        # Кнопка генерации
        ttk.Button(btnfr, text="Сгенерировать", command=self.GenWindow).pack(side="left", padx=10)

        #Кнопка графиков
        ttk.Button(btnfr, text="Графики", command=self.GraphWindow).pack(side="left", padx=10)

        # Поле вывода результатов
        self.output = tk.Text(root, height=15)
        self.output.pack(pady=10, fill="both", expand=True)

    # Эксперимент, создание потока для отдельного окна
    def RunExper(self):
        thread = threading.Thread(target=self.ExperThread)
        thread.start()

    #Выполнение эксперимента в отдельном потоке
    def ExperThread(self):
        try:
            # Проверка на генерацию
            if self.rsa is None:
                messagebox.showwarning("Сначала сгенерируйте ключ")
                return

            rsa = self.rsa
            # Получение значений
            bit = int(self.bitsentry.get())     #Размер ключа
            samp = int(self.sampentry.get())    #Количество экспериментов

            #Получение значений переключателя
            ptype = self.prtype.get()  # Получение выбранного типа простых

            close = (ptype == "close")  # Выбор близких простых
            strong = (ptype == "strong")  # Выбор сильных простых

            self.output.delete("1.0", tk.END)   #Очистка поля вывода

            #Вывод данных
            #rsa = RSA(bit, c=close, st=strong)
            #self.rsa = rsa

            self.output.insert(tk.END, "Параметры RSA:\n")

            self.output.insert(tk.END, f"\np = {rsa.p}")
            self.output.insert(tk.END, f"\nq = {rsa.q}")
            self.output.insert(tk.END, f"\nn = {rsa.n}")
            self.output.insert(tk.END, f"\ne = {rsa.e}")
            self.output.insert(tk.END, f"\nd = {rsa.d}\n")

            self.output.insert(tk.END, "Выполняется эксперимент...\n")  #Сообщение

            df = Experiment.run(samp=samp, bit=bit, c=close, st=strong) #Запуск эксперимента
            self.res = df   #Сохранение результата

            #Вычисление среднего по времени
            avg = df["time"].mean()
            self.output.insert(tk.END,f"\nСреднее время факторизации: {avg:.6f} сек\n\n")   #Вывод времени
            self.output.insert(tk.END, str(df))         #Вывод таблицы

        #Ошибки
        except Exception as e: messagebox.showerror("Ошибка", str(e))

    # Генерация
    def GenWindow(self):

        #Создание окна поверх основного
        genwin = tk.Toplevel(self.root)
        genwin.title("Генерация простых чисел")
        genwin.geometry("400x300")
        genwin.grab_set()  # Модальное окно

        ttk.Label(genwin, text="Размер числа в битах:").pack(pady=5)
        bitent = ttk.Entry(genwin)      #Поле ввода
        bitent.pack()

        typeprine = tk.StringVar(value="normal")    #Переменная типа простого числа

        #Кнопки выбора
        ttk.Radiobutton(genwin, text="Простое число по Миллеру-Рабину", variable=typeprine, value="normal").pack(pady=5)
        ttk.Radiobutton(genwin, text="Сильное простое", variable=typeprine, value="strong").pack(pady=5)

        #Вывод результат
        output = tk.Text(genwin, height=8)
        output.pack(pady=10, fill="both", expand=True)

        # Функция генерации числа
        def Generate():

            try:
                bit = int(bitent.get())

                #Выбор метода генерации
                if typeprine.get() == "normal":
                    pr = Generator.GenPr(bit)
                    title = "Обычное простое число"
                else:
                    pr = Generator.GenStrongPr(bit)
                    title = "Сильное простое число"

                #Вывод результата
                output.delete("1.0", tk.END)    #Очистка окна ввода
                #rsa = RSA(bit=bit, c=(type == "close"), st=(type == "strong"))

                # Генерация RSA
                rsa = RSA(bit)

                # Сохранение ключа
                self.rsa = rsa
                self.params = {"n": rsa.n, "e": rsa.e, "d": rsa.d}

                output.insert(tk.END, f"p = {rsa.p}\nq = {rsa.q}\nn = {rsa.n}")

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        #Фрейм для кнопок
        btnfr = ttk.Frame(genwin)
        btnfr.pack(pady=5)

        ttk.Button(btnfr, text="ОК", command=Generate).pack(side="left", padx=10)       #Запуск генерации
        ttk.Button(btnfr, text="Отмена", command=genwin.destroy).pack(side="left", padx=10)     #Закрытие окна

    # Графики
    def GraphWindow(self, rsa=None):

        #Предупреждение если эксперимент не был выполнен
        if self.res is None:
            messagebox.showwarning("Сначала выполните эксперимент")
            return

        # Предупреждение если нет ключа
        if self.rsa is None:
            messagebox.showwarning("Сначала выполните сгенерируйте ключ RSA")
            return

        graphwin = tk.Toplevel(self.root)
        graphwin.title("Графики")
        graphwin.geometry("300x220")

        ttk.Label(graphwin, text="Выбор графика").pack(pady=10)

        #Вызов графика по среднему времени
        ttk.Button(graphwin, text="Среднее время", command=lambda: Graph.PlotRes(self.res)).pack(pady=5)

        #Вызов графика по всем экспериментам
        ttk.Button(graphwin, text="Все эксперименты", command=lambda: Graph.PlotExperiments(self.res)).pack(pady=5)

        #ИЗМЕНЕНО: кнопка графика для атаки по времени
        ttk.Button(
            graphwin,
            text="Атака по времени",
            command=lambda: Graph.PlotTimingAttack({"n": self.rsa.n, "e": self.rsa.e, "d": self.rsa.d})).pack(pady=5)

        #Не рабочий
        #ttk.Button(graphwin, text="Сравнение с теорией", command=lambda: Graph.PlotWithTheory(self.result)).pack(pady=5)

# Запуск
if __name__ == "__main__":
    root = tk.Tk()  #Создание основного окна
    app = Gui(root)     #Создание объекта интерфейса
    root.mainloop()     #Запуск обработки событий
