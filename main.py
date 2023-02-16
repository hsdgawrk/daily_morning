#encoding:utf-8
from datetime import date, datetime
import math
from pickle import FALSE, TRUE
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os

weekday_dict = {0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"}
city_dict = {'济南':101120101,'大连':101070201}

today = datetime.now()
week_num = today.weekday()
week = weekday_dict[week_num]
special = ""

if week_num == 4:
    special = os.environ['FRI_SP']
elif week_num == 5 or week_num == 6:
    special = os.environ['WEEKEND_SP']

is_school = os.environ['IS_SCHOOL']

date_from = os.environ['DATE_FROM']
date_to = os.environ['DATE_TO']

home_city = os.environ['HOME_CITY']
school_city = os.environ['SCHOOL_CITY']
#need add comma before wearing tips
home_wearing_tips = ""
school_wearing_tips = ""

#birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id_2 = os.environ["USER_ID_2"]
template_id = os.environ["TEMPLATE_ID"]

weather_id = os.environ["WEATHER_ID"]

def get_weather(city):
  city_code = city_dict[city]
  url = "https://devapi.qweather.com/v7/weather/now?key=" + weather_id +"&location=" + str(city_code)
  res = requests.get(url).json()
  weather = res['now']
  return weather['text'], weather['feelsLike']

def get_count(date_str):
  delta = today - datetime.strptime(date_str, "%Y-%m-%d")
  return abs(delta.days)

#def get_birthday():
  #next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  #if next < datetime.now():
    #next = next.replace(year=next.year + 1)
  #return (next - today).days

def get_wearing_tips(city):
    city_code = city_dict[city]
    url = "https://devapi.qweather.com/v7/indices/1d?key=" + weather_id +"&location=" + str(city_code) + "&type=3,5"
    res = requests.get(url).json()
    tip = "，" + res['daily'][0]['text'] + "紫外线指数为：" + res['daily'][1]['level'] + res['daily'][1]['text'].strip('。')
    return tip

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

home_weather, home_temperature = get_weather(home_city)
school_weather, school_temperature = get_weather(school_city)

is_school_started = ""
if is_school == 'False':
    is_school_started = "目前看来还没有开学呢。"
    home_wearing_tips = get_wearing_tips(home_city)
else:
    is_school_started = "开始上学啦！努力做实验哦！加油！"
    school_wearing_tips = get_wearing_tips(school_city)

data = {"week":{"value":week},"special":{"value":special},"is_school_started":{"value":is_school_started},"home":{"value":home_city},"home_weather":{"value":home_weather}, \
"home_temp":{"value":home_temperature},"home_wearing_tips":{"value":home_wearing_tips},"school_wearing_tips":{"value":school_wearing_tips}, \
"school":{"value":school_city},"school_weather":{"value":school_weather},"school_temp":{"value":school_temperature},"date_from":{"value":get_count(date_from)}}

res = wm.send_template(user_id, template_id, data)
res = wm.send_template(user_id_2, template_id, data)
print(res)
