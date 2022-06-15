import sqlite3 # импортируем библиотеку СУБД sqlite
import dearpygui.dearpygui as dpg  # импортируем библиотеку DearPyGUI (графический интерфейс)

# ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ И ПОЛУЧЕНИЕ ДАННЫХ
conn = sqlite3.connect('bru.sqlite') # подключаемся к БД
cursor = conn.cursor() # создаем объект cursor, с помощью которого можно выполнять запросы
cursor.execute("SELECT * FROM sosna2 WHERE Id <= 15")
results1 = cursor.fetchall() # сохраняем результат запроса в массиве results1
#print(results1)
cursor.execute("SELECT * FROM sosna2")
results2 = cursor.fetchall() # сохраняем результат запроса в массиве results2
#print(results2[0][2]) # первая строка, второй столбец - AglPlan
cursor.execute("SELECT t1.Id, t1.AglPlan AS 'AglP', t1.AglFkt AS 'AglF', SUM(t2.AglPlan) AS 'AglPlanNit', SUM(t2.AglFkt) AS 'AglFktNit' FROM sosna2 AS t1, sosna2 AS t2 WHERE t1.Id>=t2.Id GROUP BY t1.Id")
results3 = cursor.fetchall() # сохраняем результат запроса в массиве results3
#print(results3)
# for result in results3:  # выводим на экран содержимое массива столбец AglPlan
#        print(result[3], result[4]) # 3 - AglPlanNit  4 - AglFktNit

# creating data for graphics
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] # весь месяц
x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]  # до текущей даты
x3 = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] # после текущей даты
y1 = []; y2 = []; y3 = []   # создаем пустые массивы y1, y2 и y3 (объем аглоруды НИТ)
for n in results3:
    y1.append(n[3]) # добавляем в массив y1 элементы массива results3 AglPlanNit
    #y2.append(n["AglFktNit"])  # добавляем в массив y2 элементы массива results3 AglFktNit
y2 = [2200,4300,5500,7500,8000,10000,12000,14000,16000,17000,19000,20000,23000,26000,27000]
# рассчитываем прогноз
y3 = []
for i in range(1, 32):
    y3.append(15*1800 + i*1800)

y4 = []; y5 = []   # создаем пустые массивы y4 и y5 (производительность)
for n in results2:
    y4.append(n[4]) # добавляем в массив y3 элементы массива results2  4 "PrstPlan"
    y5.append(n[5])  # добавляем в массив y4 элементы массива results2  5 "PrstFkt"

y6 = []; y7 = []   # создаем пустые массивы y6 и y7 (простои)
for n in results2:
    y6.append(n[6]) # добавляем в массив y6 элементы массива results2  6 "ProstPlan"
    y7.append(n[7])  # добавляем в массив y7 элементы массива results2  7 "ProstFkt"

y8 = []; y9 = []   # создаем пустые массивы y8 и y9 (Коэфф выхода)
for n in results2:
    y8.append(n[8]) # добавляем в массив y8 элементы массива results2 8  "KvPlan"
    y9.append(n[9])  # добавляем в массив y9 элементы массива results2 9  "KvFkt"

# ПРОИЗВОДИМ РАСЧЕТЫ :
# На текущую дату (15 дней):
SumPld = 0; SumFktd = 0
for n in results1: # считам сумму по Плану и по Факту (цикл for each - для каждого)
    SumPld = SumPld + n[2]; SumFktd = SumFktd + n[3] # "AglPlan" ,  "AglFkt"

# За Месяц:
SumPlm = 0; SumFktm = 0
for n in results2: # считам сумму по Плану и по Факту
    SumPlm = SumPlm + n[2]  # "AglPlan"

AglProgn = SumFktd/15*31 # Расчет прогноза на основе факта за 15 дней

Cena = 2000 # цена 1 тонны, руб.
PerZatr = 1335 # переменные затраты на 1 тонну,руб.
PostZanr = 30  # постоянные затраты в месяц млн.руб.
Post1 = 330000 # постоянная часть ФОТ семи руководителей, руб.
Koef1 =0.0092 # коэффициент формирования переменной части ФОТ руководителей
Post2 = 1421434 # постоянная часть ФОТ рабочих, руб. (67 рабочих)
Koef2 = 31.78 # коэффициент формирования переменной части ФОТ рабочих

PribPlan = SumPlm*(Cena-PerZatr)/1000000-PostZanr # Прибыль плановая на месяц, млн.руб.
PribProgn = AglProgn*(Cena-PerZatr)/1000000-PostZanr # Прибыль прогноз на месяц, млн.руб.
ZpRukPlan = int((Post1+Koef1*(PribPlan*1000000+6847588))/7)
ZpRukProgn = int((Post1+Koef1*(PribProgn*1000000+6847588))/7)
ZpRabPlan = int((Post2+Koef2*(SumPlm-35000))/67)
ZpRabProgn = int((Post2+Koef2*(AglProgn-35000))/67)

# ВЫВОДИМ РЕЗУЛЬТАТЫ НА ЭКРАН:
print("План пр-ва аглоруды на тек. дату, тн = ", SumPld)
print("Факт пр-ва аглоруды на тек. дату, тн = ", SumFktd)
print("Отставание на тек. дату, тн = ", SumPld - SumFktd)
print()
print("План пр-ва аглоруды на Месяц, тн = ", SumPlm)
print("Прогноз пр-ва аглоруды на Месяц, тн = ", AglProgn)
print("Отставание от месячного плана, тн = ", SumPlm - AglProgn)

# СТРОИМ ГРАФИКИ И ТАБЛИЦЫ  в DearPyGUI
dpg.create_context()  # создаем контекст

with dpg.window(label="Window1", pos=(0,0)): #  в Window1 график по Аглоруде
    with dpg.plot(label="Agloruda", height=300, width=300):
        dpg.add_plot_legend()  # выводим легенду (Plan, Fakt, Forecast)
        dpg.add_plot_axis(dpg.mvXAxis, label="day") # Ед. изм.по оси X
        dpg.add_plot_axis(dpg.mvYAxis, label="tn", tag="y1_axis") # Ед. изм.по оси Y
        dpg.add_line_series(x, y1, label="Plan", parent="y1_axis") # к родителю tag="y1_axis"
        dpg.add_line_series(x2, y2, label="Fakt", parent="y1_axis") # к родителю tag="y1_axis"
        dpg.add_line_series(x3, y3, label="Forecast", parent="y1_axis") # к родителю tag="y1_axis"
pass

with dpg.window(label="Window2", pos=(300,0)): #  в Window2 график по Производительности
    with dpg.plot(label="Proizvoditelnost", height=300, width=300):
        dpg.add_plot_legend(location=6) # в нижнем левом углу
        dpg.add_plot_axis(dpg.mvXAxis, label="day") # Ед. изм.по оси X
        dpg.add_plot_axis(dpg.mvYAxis, label="tn/hour", tag="y4_axis") # Ед. изм.по оси Y
        dpg.add_bar_series(x, y4, label="Plan", parent="y4_axis") # к родителю tag="y4_axis"
        dpg.add_bar_series(x, y5, label="Fakt", parent="y4_axis") # к родителю tag="y4_axis"
pass

with dpg.window(label="Window3", pos=(600,0)): #  в Window3 график по Простоям
    with dpg.plot(label="Prostoi", height=300, width=300):
        dpg.add_plot_legend(location=6)
        dpg.add_plot_axis(dpg.mvXAxis, label="day") # Ед. изм.по оси X
        dpg.add_plot_axis(dpg.mvYAxis, label="hour", tag="y6_axis") # Ед. изм.по оси Y
        dpg.add_bar_series(x, y6, label="Plan", parent="y6_axis") # к родителю tag="y6_axis"
        dpg.add_bar_series(x, y7, label="Fakt", parent="y6_axis") # к родителю tag="y6_axis"
pass

with dpg.window(label="Window4", pos=(900,0)):  #  в Window4 график по Коэффициенту выхода
    with dpg.plot(label="Kv", height=300, width=300):
        dpg.add_plot_legend(location=6)
        dpg.add_plot_axis(dpg.mvXAxis, label="day") # Ед. изм.по оси X
        dpg.add_plot_axis(dpg.mvYAxis, label="%", tag="y8_axis") # Ед. изм.по оси Y
        dpg.add_bar_series(x, y8, label="Plan", parent="y8_axis") # к родителю tag="y8_axis"
        dpg.add_bar_series(x, y9, label="Fakt", parent="y8_axis") # к родителю tag="y8_axis"
pass

with dpg.window(label="Window5", pos=(0,340), width=1240, height=400): # Таблица 1  и Таблица 2
    # Тфблица 1 (на текущую дату)
    dpg.add_text("Table1 (tek. data)")
    with dpg.table(label="Date", header_row=True, policy=dpg.mvTable_SizingFixedFit, resizable=True, no_host_extendX=True,
                   borders_innerV=True, borders_outerV=True, borders_outerH=True):
        dpg.add_table_column(label="POKAZATELI          ")
        dpg.add_table_column(label="Plan        ")
        dpg.add_table_column(label="Fakt        ")
        dpg.add_table_column(label="Otklonenie  ")
        with dpg.table_row():
            dpg.add_text("Agloruda, tonn")
            dpg.add_drag_int(default_value= SumPld, max_value=1)
            dpg.add_drag_int(default_value=SumFktd, max_value=1)
            dpg.add_drag_int(default_value=SumFktd-SumPld, max_value=1)
    dpg.add_text() # пустая строка (для пробела)
    # Тфблица 2 (Месяц)
    dpg.add_text("Table2 (mesiz)")
    with dpg.table(label="Mesiz", header_row=True, policy=dpg.mvTable_SizingFixedFit, resizable=True, no_host_extendX=True,
                   borders_innerV=True, borders_outerV=True, borders_outerH=True):
        dpg.add_table_column(label="POKAZATELI")
        dpg.add_table_column(label="Plan        ")
        dpg.add_table_column(label="Forecast    ")
        dpg.add_table_column(label="Otklonenie  ")
        with dpg.table_row():
            dpg.add_text("Agloruda, tonn")
            dpg.add_drag_int(default_value=SumPlm, max_value=1)
            dpg.add_drag_int(default_value=AglProgn, max_value=1)
            dpg.add_drag_int(default_value=AglProgn-SumPlm, max_value=1)
        with dpg.table_row():
            dpg.add_text("Pribyl, mln.rub")
            dpg.add_drag_int(default_value= PribPlan, max_value=1)
            dpg.add_drag_int(default_value=PribProgn, max_value=1)
            dpg.add_drag_int(default_value=PribProgn-PribPlan, max_value=1)
        with dpg.table_row():
            dpg.add_text("Zarplata Memegm, rub")
            dpg.add_drag_int(default_value= ZpRukPlan, max_value=1)
            dpg.add_drag_int(default_value=ZpRukProgn, max_value=1)
            dpg.add_drag_int(default_value=ZpRukProgn-ZpRukPlan, max_value=1)
        with dpg.table_row():
            dpg.add_text("Zarplata Raboch, rub")
            dpg.add_drag_int(default_value=ZpRabPlan, max_value=1)
            dpg.add_drag_int(default_value=ZpRabProgn, max_value=1)
            dpg.add_drag_int(default_value=ZpRabProgn-ZpRabPlan, max_value=1)
pass


dpg.create_viewport(title='Weis Consultig', x_pos=20, y_pos=20, width=1240, height=640)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()  # удаляем контекст