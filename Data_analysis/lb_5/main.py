import requests, fake_useragent
from bs4 import BeautifulSoup 
from matplotlib import pyplot as plt
from dsmltf import *
import math
from colorama import Fore, Back, Style

# Делаем запросы с разными User-Agent
user = fake_useragent.UserAgent().random 
# Заголовки
headers = {'User-Agent': user}

# Парсинг городов 1.5.1
def parsing(url):
    # Создаем сессию для запроса 
    request_session = requests.Session()
    # Делаем запрос
    request = request_session.get(url, headers=headers)
    # Проверяем статус запроса
    if request.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга
        soup = BeautifulSoup(request.content, 'lxml') # lxml - парсер
        # Ищем нужные данные
        class_temp = list(soup.find_all('td', class_='first_in_group'))[::2]
        # Возвращаем данные 
        return [data.text for data in class_temp]


def get_data(sity = 5039, year = 2022):
     # Список для хранения данных
    data_temp = []
    # Цикл для парсинга данных
    for i in range(1,5):
        # Ссылка на страницу
        url = f'https://www.gismeteo.ru/diary/{str(sity)}/{str(year)}/{str(i)}/'
        # Добавляем данные в список
        data_temp.append(parsing(url))
    
    # Удаляем пустые строки 
    for data in data_temp:
        for i in data:
            if i == '':
                data.remove(i)
            else:
                data[data.index(i)] = int(i)
    for data in data_temp:
        for i in data:
            data[data.index(i)] = int(i)
    
    data = []
    for x in data_temp:
        data.extend(x if isinstance(x, list) else [x])
    return data


def y_exp(t,A,b):
    return A * math.exp(b * t)

data = [0, -5, -1, -6, 3, 2, -2, -2, -3, 0, -7, -13, -13, 1, -1, -1, -1, -4, -8, -7, -3, -3, -4, -5, -8, -8, -5, -3, 0, -2, 0, -1, -1, -1, -3, -5, 0, 1, 1, 1, 2, 3, 0, 1, 1, 4, 1, 3, 3, 3, 4, 5, 3, 4, 4, -2, 0, 3, -1, 1, 1, 0, 0, -2, -1, -2, -2, -4, -10, -7, -3, -2, 1, -1, -4, -5, -2, 2, 3, 7, 8, 10, 11, 11, 12, 0, 3, 15, 8, 11,16, 20, 5, 5, 6, 10, 18, 18, 15, 16, 20, 12, 16, 14, 16, 16, 8, 11, 18, 8, 11, 15, 16, 15, 18, 20, 14, 16, 14, 13]

def ex_1(data,av_temp,range_av_temp):

    #print("Data: ", data)
    #print(av_temp)
    av_temp_shifted = list(map(lambda x: x + (abs(round(min(av_temp))) + 1) , av_temp)) 
    A,b = approx_exp(av_temp_shifted,range_av_temp)

    dev_list = [av_temp_shifted[t] - y_exp(t,A,b) for t in range_av_temp]
    dev_max = max([abs(y_exp(t,A,b) - av_temp_shifted[t]) for t in range(len(av_temp))])
    #print("Dev_max: ",dev_max)

    mu = mean(dev_list)
    sigma = standard_deviation(dev_list)
    print("Mean: ",mu, "\nSigma: ", sigma)
    
    p = p_value(dev_max, mu, sigma)
    print("P_val: ",p) # < 5

    plt.scatter(range_av_temp,av_temp_shifted, marker='x',  color = "red")
    plt.plot(range_av_temp,[y_exp(t,A,b) for t in range_av_temp], color = "green")
    plt.show()

    return p, sigma, mu

def y_poly(t,a):
    return sum(ai*t**i for i,ai in enumerate(a))

def ex_2(data,av_temp,range_av_temp):
    
    a4 = approx_poly(av_temp,range_av_temp,4)
    #print("A4: ", a4)
    
    dev_list = [av_temp[t] - y_poly(t,a4) for t in range_av_temp]
    dev_max = max(abs(y_poly(t,a4)- av_temp[t]) for t in range_av_temp)
    
    #print("Dev_max: ",dev_max)
    
    mu = mean(dev_list)
    sigma = standard_deviation(dev_list)
    print("Mean: ",mu, "\nSigma: ", sigma)

    p = p_value(dev_max, mu, sigma)
    print("P_val: ",p) # < 5

    plt.scatter(range_av_temp,av_temp, marker='x',  color = "red")
    plt.plot(range_av_temp,[y_poly(t,a4) for t in range_av_temp], color = "green")
    plt.plot(range(len(av_temp)), [y_poly(t,a4) for t in range_av_temp], color = "b")
    plt.show()

    return p, sigma, mu

def ex_3(p_val , p_sigma, p_mu , exp_p_val, exp_sigma, exp_mu ):
    if exp_p_val > p_val:
        print("P:W:", end = '')
        s_min = inv_f_norm(0.05 / 2, exp_mu, exp_sigma)
        s_max = 2 * exp_mu - s_min
        w = 1 - (f_norm(s_max, p_mu, p_sigma) - f_norm(s_min, p_mu, p_sigma))
    else: # Будет этот вариант выводить
        print("E:W: ", end = '')
        s_min = inv_f_norm(0.05 / 2, p_mu, p_sigma)
        s_max = 2 * p_mu - s_min
        w = 1 - (f_norm(s_max, exp_mu, exp_sigma) - f_norm(s_min, exp_mu, exp_sigma))
    print(w)

def ex_4(data,av_temp,range_av_temp):
    av_temp = [mean(data[7 *k :7 * k + 7]) for k in range(len(data) // 7 - 1)] + [mean(data[7 * (len(data) // 7) - 1 :]) ]
    av_short = av_temp[:-4]
    a7 = approx_poly(av_short,range_av_temp,7)
    #print("A7: ", a7)

    print(f"{Back.BLUE}Short: ", Style.RESET_ALL)
    dev_list_short = [av_short[t] - y_poly(t,a7) for t in range_av_temp[:-4]]
    dev_max_short = max(abs(y_poly(t,a7)- av_short[t]) for t in range_av_temp[:-4])
    #print("Dev_max: ", dev_max_short)

    mu_short = mean(dev_list_short)
    sigma_short = standard_deviation(dev_list_short)
    print("Mean: ",mu_short, "\nSigma: ", sigma_short)

    p_short = p_value(dev_max_short, mu_short, sigma_short)
    print("P: ",p_short) # < 5
    
    print(f"{Back.BLUE}Full selection: ", Style.RESET_ALL)
    dev_list = [av_temp[t] - y_poly(t,a7) for t in range_av_temp]
    dev_max = max(abs(y_poly(t,a7)- av_temp[t]) for t in range_av_temp)
    #print("Dev_max: ",dev_max)
    mu = mean(dev_list)
    sigma = standard_deviation(dev_list)
    print("Mean: ",mu, "\nSigma: ", sigma)
    p = p_value(dev_max, mu, sigma)
    print("P: ",p) # < 5

    if p < p_short:
        print("\nПредсказание на длинном хуже")
    else:
        print("\nПредсказание на кортком хуже")

# Лаба готова
def main():
    #data = get_data(5039,2022)
    av_temp = [mean(data[7 *k :7 * k + 7]) for k in range(len(data) // 7 - 1)] + [mean(data[7 * (len(data) // 7) - 1 :]) ]
    range_av_temp = range(len(av_temp))
    print(f"{Fore.RED}Ex_1_EXP:",Style.RESET_ALL)
    p_val_exp,exp_sigma_p, exp_mu_p  = ex_1(data, av_temp, range_av_temp)
    print(f"{Fore.RED}\nEx_2_Poly: ",Style.RESET_ALL)
    p_val, sigma_p, mu_p = ex_2(data, av_temp, range_av_temp)
    print(f"{Fore.RED}\nEx_3: ",Style.RESET_ALL)
    ex_3(p_val, sigma_p, mu_p, p_val_exp, exp_sigma_p, exp_mu_p)
    print(f"{Fore.RED}\nEx_4: ",Style.RESET_ALL)
    ex_4(data, av_temp, range_av_temp)

main()