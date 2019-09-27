# ski_forecast.py 
'''
=====================
Author: Tingaev M.I.
==============================================================================
Task Description:

1.Описание ситуации
 
Вы помогаете организаторам школьных соревнований по лыжной гонке. Одна из задач организаторов - обеспечить всех одинаковой смазкой для лыж. Участников очень много, надо купить один вид на всех. Соревнования проходят в воскресенье, поставщик смазки может продать не позднее пятницы. Соревнования проходят в Челябинске в парке Гагарина.
 
2.Задание
 
Надо написать программу, которая получит прогноз погоды на ближайшее воскресение и подскажет нужный вид смазки.
 
3. Подсказка
 
Смазка выбирается следующим образом:
a) если температура воздуха -13 градусов Цельсия и холоднее рекомендуйте покупать смазку “Type C”.
b) Если от -13 до -5, то подойдет “Type B”.
c) Если теплее -5, то только “Type A”.

# Open Weather Map API Documentation: https://is.gd/oVdhiZ
# Latitude / Longitude checked at: https://www.latlong.net/
==============================================================================
'''
print(__doc__)


import pytz
import datetime
import requests



class Weather_Forecast:
    ''' Класс прогноза погоды
    Конструктор принимает текущую дату
    '''

    city = "chelyabinsk,ru"

    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q": city}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "6ef95dee6dmsh3718d08c7acdd83p143310jsnf0adc1e9fdc4"
        }
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.exceptions.HTTPError as e:
        # Вернулся код != 200
        print("Error: " + str(e))

    text = response.text
    json = response.json()


    def __init__(self, date):
        ''' 
        Метод инициализации класса
        '''
        self.date = date
	

    def get_the_temp(self):
        ''' 
        Метод класса, возвращает минимальную температуру на дату
        ближайшего воскресного дня на 12:00:00
        '''
        sunday_weather_data = dict()
        forecast_weather_data = self.json['list']

        for weather_data in forecast_weather_data:
            # Выводит словарь параметров на ближайшие 5 дней (на каждые 3 часа)
            # print(weather_data)      
            if weather_data['dt_txt'] == self.date:
                sunday_weather_data = weather_data
        
        main_parametres = sunday_weather_data['main']
        print('Основные параметры = ', main_parametres)
        temp = K_to_C(main_parametres['temp'])
        print('Средняя температура на воскресенье составит {0} °C'.format(to_fixed(temp, 2)))
        temp_min = K_to_C(main_parametres['temp_min'])
        print('Минимальная температура на воскресенье составит {0} °C'.format(to_fixed(temp_min, 2)))
        temp_max = K_to_C(main_parametres['temp_max'])
        print('Максимальная температура на воскресенье составит {0} °C'.format(to_fixed(temp_max, 2)))
        humidity = main_parametres['humidity']
        print('Влажность воздуха на воскресенье составит {0} %'.format(humidity))
        pressure = main_parametres['pressure']
        print('Давление воздуха в воскресенье составит {0} гПа'.format(pressure))

        return temp_min
    

    def greace_selection(self, temp):
        ''' 
        Метод класса, реализующий алгоритм выбора смазки
        в зависимости от прогноза погоды на ближайшее воскресенье
        '''
        print('К покупке рекомендуется смазка ', end='')
        return {
            temp < -13.0:           'Type C',
            -13.0 <= temp < -5.0:   'Type B',
            temp >= -5.0:           'Type A',
        }[True]


def utc_now():
    '''
    Функция возвращает текущее время в формате UTC для 
    time_zone = "Asia/Yekaterinburg"
    '''
    time_zone = "Asia/Yekaterinburg"

    return datetime.datetime.now(tz=pytz.timezone(time_zone))


def get_date():
    '''
    Функция возвращает текущую дату для time_zone
    в формате "%Y-%m-%d"
    '''
    now = utc_now()

    return now


def get_sunday():
    '''
    Функция возвращает дату ближайшего воскресенья
    в формате "%Y-%m-%d"
    '''
    sunday_weekday = 6
    date_utc = get_date()
    print('Дата в UTC: ', date_utc)
    days_to_plus = sunday_weekday - int(date_utc.weekday())
    print('Дней до воскресенья: ', days_to_plus)
    sunday_date = date_utc + datetime.timedelta(days = days_to_plus)
    print('Дата через 2 дня:', sunday_date)
    sunday_date = sunday_date.strftime("%Y-%m-%d") + ' 12:00:00'
    print("Дата на воскресенье в формате 'Y-m-d 12:00:00' : ", sunday_date)

    return sunday_date


def K_to_C(K):
    '''
    Функция переводит температуру из Кельвинов в градусы цельсия
    '''
    T0 = 273.15
    return (K - T0)

def to_fixed(numObj, digits=0):
    '''
    Функция производит форматирование типа float до нужного знака
    '''
    return f"{numObj:.{digits}f}"


def main():
    '''
    Создаем экземпляр класса Weather_Forecast
    и в него передаем текущую дату
    '''
    date = get_sunday()
    app = Weather_Forecast(date)
    temp = app.get_the_temp()
    result = app.greace_selection(temp)
    print(result)
    # print(app.__doc__)


if __name__ == "__main__":
    main()
