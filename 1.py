import sys
import time
from abc import ABC, abstractmethod
from peewee import *
import sqlite3
from threading import *
from threading import Thread
import asyncio

t_start = time.perf_counter()

print('I этап работы программы. Идет запуск, подождите 5 секунд...')
def one(num): # Многопоточность
    time.sleep(num)
    print(round(time.perf_counter() - t_start) + 1, '...')

for i in range(5):
    th = Thread(target=one, args=(i, ))
    th.start()

th.join() # Ждем завершения потоков
print()

try:
    connection = SqliteDatabase('Kr.sqlite')
    cursor = connection.cursor()
    print('База данных успешно создана и подключена к Sqlite')
    print()

    sql = "DROP TABLE IF EXISTS bank"
    cursor.execute(sql)

    array = ()
    arr = []
    answer = 0
    mnth = 0


    cursor.execute("""CREATE TABLE IF NOT EXISTS bank(
    Sum INT,
    Nomber INT,
    Result INT,
    Month INT);
    """)
    connection.commit()

    class Basic(ABC):
        @abstractmethod
        def first(self):
            print('Bank')

    class Advanced(Basic):
        def first(self):
            super().first()
            print('________Калькульятор вкладов________')

    a = Advanced()
    a.first()

    a = ['Срочный вклад (1)', 'Вклад с капитализацией процентов (2)']
    Proverka_arr = ['1', '2', '3']
    Proverka_arr_1 = ['1', '2']

    class IntFloatValueError(Exception): # Исключения
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return '"{}" не является верным вводом, принимаются только положительные значения ' \
                   'и значения с плавающей точкой'.format(self.value)
    Inf = 0
    array = ()
    def begin(s):
        global Inf
        alf = '0123456789.'
        t = s
        # Inf = 0
        count = 0
        for i in range(len(t)):
            if (t[i] in alf):
                count += 1
                if (count == len(t)):
                    Inf = 1
            else:
                print(IntFloatValueError(s))
                print('Попробуйте еще раз:')
                break
        return Inf

    while (Inf == 0):
        print('Введите сумму, которую хотите вложить (Int/Float): ')
        s = str(input())
        begin(s)
    Inf = 0
    array += (s,)

    if (int(s) < 15000):
        print('Введите номер варианта вклада, который вас интересует (1-2)')
        print("; ".join(a))
        var = input()
        if (var not in Proverka_arr_1):
            while (var not in Proverka_arr_1): # Прооверка на правильный ввод
                print('Попробуйте ещё раз (1-2): ', end = ' ')
                var = input()
    else:
        var = '3'
    array += (var,)


    class bank():
        def __init__(self, summa, percent, time):
            self.summa = summa
            if 1 <= int(percent) <= 100:
                self.percent = percent
            else:
                self.percent = 'Не определен'
                sys.exit()

            self.time = time

        def __private(self):
            print("Это приватный метод! Деньги не вернем.")

    if (var == '1'):
        class easy(bank):
            def display_wow(self):
                global answer
                global mnth
                print('Вклад размером: {}. Процент: {}%. Время {} месяц(-a/-ев)'.format(self.summa, self.percent, self.time))
                answer = int(self.summa)*(int(self.time)*0.05 + 1)
                mnth = self.time
                print('Итоговая сумма:', round(answer, 2))
        print('Выбран срочный вклад, введите срок')
        res_1 = easy(s, '5', str(input()))
        res_1.display_wow()


    if (var == '2'):
        class cap(bank):
            # def setSumma(self):
            #     self.summa = summa
            # def setTime(self):
            #     self.time = time
            def display_wow(self):
                global answer
                global mnth
                print('Вклад размером: {}. Процент: {}%. Время {} месяц(-a/-ев)'.format(self.summa, self.percent, self.time))
                answer = int(self.summa)*(int(self.percent)/100 + 1)**int(self.time)
                mnth = self.time
                print('Итоговая сумма:', round(answer, 2))
        print('Выбран вклад с капитализацией процентов, введите срок')
        res_1 = cap(s, '12', str(input()))
        res_1.display_wow()


    if (var == '3'):
        class bonus(bank):
            def display_wow(self):
                global answer
                global mnth
                print('Вклад размером: {}. Процент: {}%. Время: {} месяц(-a/-ев)'.format(self.summa, self.percent, self.time))
                answer = int(self.summa)*(int(self.time)*int(self.percent)/100 + 1)
                bonus = (answer - int(self.summa))*int(self.percent)/100
                mnth = self.time
                print('Итоговая сумма (+ бонус):', round(answer, 2) + int(bonus), 'Бонус: ', int(bonus))

        print('Бонусный вклад. Введите срок')
        res_1 = bonus(s, '7', str(input()))
        res_1.display_wow()

    array += (round(answer, 2),) + (mnth,)
    arr.append(array)

    cursor.executemany("INSERT INTO bank VALUES(?, ?, ?, ?);", arr)
    connection.commit()

    cursor.execute("SELECT * FROM bank")
    all_results = cursor.fetchone()

    print()
    pr = 0
    if (all_results[1] == 1):
        pr = '5'
    elif (all_results[1] == 2):
        pr = '12'
    else:
        pr = '7'

    print('Данные Sqlite таблицы сохранены. Номер вклада {}. Количество месяцев {}. Процент: {}%. Исходная сумма {}, Конечная сумма {}'.format(all_results[1], all_results[3], pr, all_results[0], all_results[2]))


    class BaseModel(Model):
        class Meta:
            database = connection


    class Bank(BaseModel):
        Nomber_of_contribution = AutoField(column_name='Nomber')
        Initial_Summa = TextField(column_name='Sum', null=True)
        Result_Summa = TextField(column_name='Result', null=True)
        Month_Time = TextField(column_name='Month', null=True)

        class Meta:
            table_name = 'bank'

    print()
    # print('Представлена информация из базы данных с помощью ORM:')
    # query = Bank.select().order_by(Bank.Nomber_of_contribution.desc())
    # art = query.dicts().execute()
    # for client in art:
    #     print('Client: ', *list(art))

    async def goodbye(): # Асинхронность
        k = 0
        for i in range(3):
            k += 1
            await asyncio.sleep(i)
            print(k, '...')
        print('Представлена информация из базы данных с помощью ORM:')

    async def main():
        print('Подождите окончания работы программы...')
        await goodbye()
        query = Bank.select().order_by(Bank.Nomber_of_contribution.desc())
        art = query.dicts().execute()
        for client in art:
            print('Client: ', *list(art))

    asyncio.run(main())
    cursor.close()

except sqlite3.Error as error:
    print()
    print("Ошибка при подключении к sqlite", error)
finally:
    if (connection):
        connection.commit()
        connection.close()
        print()
        print("Соединение с Sqlite закрыто")


print('Время окончания:', time.perf_counter() - t_start)
