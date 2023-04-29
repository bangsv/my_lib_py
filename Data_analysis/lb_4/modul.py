import math 
import dsmltf

def ex_1(__verHit):
    # Общее кол-во ударов
    __Data = 1000
    # Каждый __verHit удар гол
    p = (__Data / __verHit) / __Data

    u = __Data * p

    # Стандартное отклонение
    __gipotisa = math.sqrt(__Data * p * (1 - p))

    Smin = round(dsmltf.inv_f_norm(0.025,u,__gipotisa))
    Smax = round(u + ( u - Smin))

    print("Футболисту достаточно забить от",Smin,"до",Smax,
    "из",__Data,",чтобы подвертить гипотизу")
    

# __verHit - Частота предпологаемого действия
# __Data - Общее кол-во действий
# __TrueAction - Итоговое кол-во вып. дейсвтий
# __level_sign - Уровень значимости базовое 5%
def ex_2( __verHit , __Data, __TrueAction,__level_sign = 0.025):
    # Вероятность
    p = (__Data / __verHit) / __Data

    u = __Data * p
    
    # Стандартное отклонение
    __gipotisa = math.sqrt(__Data * p * (1 - p))
    Smin = round(dsmltf.inv_f_norm(__level_sign,u,__gipotisa))
    Smax = round(u + ( u - Smin))
    p_value = dsmltf.p_value(__TrueAction,u,__gipotisa)
    print("Гипотиза не верна" if p_value <  __level_sign else "Гипотиза верна")

# __verHit - Частота предпологаемого действия
# __Data - Общее кол-во действий
# __Alter - Альтернативная гипотиза 
# __level_sign - Уровень значимости базовое 5%
def ex_3( __verHit , __Data, __Alter,__level_sign = 0.025):
    # Вероятность
    p = (__Data / __verHit) / __Data
    print(p)
    u = __Data * p

    # Стандартное отклонение
    __gipotisa = math.sqrt(__Data * p * (1 - p))

    Smin = round(dsmltf.inv_f_norm(__level_sign, u, __gipotisa))
    Smax = round(u + ( u - Smin))


    pAlter = (__Data / __Alter) / __Data
    uAlter = __Data * pAlter

    __gipotisaAlter = math.sqrt(__Data * pAlter * (1 - pAlter))

    w =  round(1 - 
            (dsmltf.f_norm(Smax,uAlter,__gipotisaAlter) 
             - 
             dsmltf.f_norm(Smin,uAlter,__gipotisaAlter)),2)

    print(w)


""""
Предположим, что в фабрике производится 1000 товаров. 
Рабочие считают, что они допустят ошибку только в каждом 30-м товаре. 
Контролирующее управление качеством требует, чтобы рабочие допускали ошибки 
только в одном из 50 товаров.
В результате рабочие допустили ошибку в каждом 41 товаре
"""

def ex_4():
    n = int(input("Введите кол-во товар: ")) 
    dopusk_err = int(input("Введите допустимую частоту ошибок: "))
    predlog_err = int(input("Введите предпологаемую частоту ошибок: "))
    number_count = int(input("Введите кол-во ошибок: "))
    print("Интервал при 5%")
    ex_2(predlog_err,n,number_count)
    ex_3(predlog_err,n,dopusk_err)
    print("Интервал при 1%")
    ex_2(predlog_err,n,number_count, 0.005)
    ex_3(predlog_err,n,dopusk_err, 0.005)
    