from django.shortcuts import render, redirect, get_object_or_404
import json
from urllib.request import urlopen
from timezonefinder import TimezoneFinder
from datetime import datetime,time,timedelta,date
from django.conf import settings
import os

def remove_spaces(str):
  return (" ".join(str.split())).replace(' ','')


timezoness=os.path.join( settings.BASE_DIR, 'rahukal/static/assets/json/timezones.json' )
new_cities = os.path.join(settings.BASE_DIR, 'rahukal/static/assets/json/new_cities.json')

def index(request):
  days = {
    'Monday': 1,
    'Saturday': 2,
    'Friday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Tuesday':6,
    'Sunday': 7,
  }
  tf = TimezoneFinder()
  cities = [

    {'city': 'pune', 'longitude': 73.856255, 'latitude':18.516726,},
    {'city': 'Mumbai', 'longitude': 72.877426, 'latitude':19.076090,},
    {'city': 'Delhi', 'longitude': 77.216721, 'latitude':28.644800,},
    {'city': 'Patna', 'longitude': 85.1376, 'latitude':25.5941,},
    
  ]
  # u = staticfiles_storage.url('assets/json/cities.json')
  offset = 0
  hour = 0
  minute = 0
  rahukal_days = []
  datee= datetime.now()
  # datee= datee.replace(day=datee.day+a)
  datee= datee.strftime("%Y-%m-%d")

  for c in cities:
    with urlopen("https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={datee}".format(lat=c['latitude'], lng=c['longitude'],datee=datee)) as response:
      source = response.read()

    data = json.loads(source)
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    sunrise = datetime.strptime(sunrise, '%I:%M:%S %p')
    sunset = datetime.strptime(sunset, '%I:%M:%S %p')
    timezone = tf.timezone_at(lng=c['longitude'], lat=c['latitude'])
    with open(timezoness,encoding="utf8") as f:
      timezones = json.load(f)

    j = False
    for t in timezones:
      if (t['timezone'].lower() == timezone.lower() and j ==False):
        offset = t['offset']
        j = True
      elif(j):
        break;

    time_add = timedelta(hours=offset)
    sunrise = sunrise + time_add
    sunset = sunset + time_add
    sunrise = time(sunrise.hour, sunrise.minute)
    sunset = time(sunset.hour, sunset.minute)
    dates = date(1, 1, 1)
    dinman = datetime.combine(dates, sunset) - datetime.combine(dates, sunrise)
    diffrence = dinman / timedelta(hours=8)
    diffrence = float("{:.2f}".format(diffrence))
    dayOfTheWeek = (datetime.today()).strftime('%A')
    dinman_times_day = diffrence * timedelta(hours=int(days['{}'.format(dayOfTheWeek)]))
    sunrise_delta = timedelta(hours=sunrise.hour, minutes=sunrise.minute)
    rahukal_start = sunrise_delta + dinman_times_day

    sunset_delta = timedelta(hours=sunset.hour, minutes=sunset.minute)
    rahukal_finish = rahukal_start + timedelta(hours=diffrence)
    duration = rahukal_finish - rahukal_start

    rahukal_start = datetime.strptime(str(rahukal_start), '%H:%M:%S').strftime("%I:%M %p")
    rahukal_finish = datetime.strptime(str(rahukal_finish), '%H:%M:%S').strftime("%I:%M %p")
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")
    a = {'rahukal_start': rahukal_start, 'rahukal_finish': rahukal_finish, 'sunrise': sunrise, 'sunset': sunset, 'date': datee,'city':c['city'],'duration':duration}
    b = a.copy()
    rahukal_days.append(b)
  context = {'rahukal': rahukal_days}
  context['ali'] = 'ali'

  return render(request,'index.html',context)







def city(request):
  context = {}
  city_name = request.POST['city']
  country_name = city_name.split(", ")[1]
  city_name = city_name.split(", ")[0]
  day_name = request.POST['day']
  today_date = request.POST['today']
  context['city'] = city_name
  context['day_name'] = day_name
  context['today_date'] = today_date
  days = {
  'Monday': 1,
  'Saturday': 2,
  'Friday': 3,
  'Wednesday': 4,
  'Thursday': 5,
  'Tuesday':6,
  'Sunday': 7,
  }
  
  tf = TimezoneFinder()
  longitude = 0;
  latitude = 0;
  offset = 0
  hour = 0
  minute = 0
  rahukal_days = []



  try:
    with open(new_cities,encoding="utf8") as f:
      cities = json.load(f)


    i = False
    for city in cities:
      if (remove_spaces(city['name'].lower()) == remove_spaces(str(city_name).lower()) and i == False):
        longitude = float(city['lng'] )
        latitude = float(city['lat'])
        # city_name = city['name']
        i = True
      elif(i):
        break;
    
    if (not i):
      raise ValueError
      
    for a in range(4):
      datee = datetime.strptime(today_date, '%Y-%m-%d')
      datee= datee.replace(day=datee.day+a)
      dateeali = datee
      datee= datee.strftime("%Y-%m-%d")
      try:
        with urlopen("https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={datee}".format(lat=latitude, lng=longitude,datee=datee)) as response:
          source = response.read()

        data = json.loads(source)
        sunrise = data['results']['sunrise']
        sunset = data['results']['sunset']
        sunrise = datetime.strptime(sunrise, '%I:%M:%S %p')
        sunset = datetime.strptime(sunset, '%I:%M:%S %p')
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        with open(timezoness,encoding="utf8") as f:
          timezones = json.load(f)

        j = False
        for t in timezones:
          if (t['timezone'].lower() == timezone.lower() and j ==False):
            offset = t['offset']
            j = True
          elif(j):
            break;

        time_add = timedelta(hours=offset)
        sunrise = sunrise + time_add
        sunset = sunset + time_add
        sunrise = time(sunrise.hour, sunrise.minute)
        sunset = time(sunset.hour, sunset.minute)
        dates = date(1, 1, 1)
        dinman = datetime.combine(dates, sunset) - datetime.combine(dates, sunrise)
        diffrence = dinman / timedelta(hours=8)
        diffrence = float("{:.2f}".format(diffrence))
        dayOfTheWeek =  dateeali.strftime('%A')
        dinman_times_day = diffrence * timedelta(hours=int(days['{}'.format(dayOfTheWeek)]))
        sunrise_delta = timedelta(hours=sunrise.hour, minutes=sunrise.minute)
        rahukal_start = sunrise_delta + dinman_times_day

        sunset_delta = timedelta(hours=sunset.hour, minutes=sunset.minute)
        rahukal_finish = rahukal_start + timedelta(hours=diffrence)
        duration = rahukal_finish - rahukal_start
        rahukal_start = datetime.strptime(str(rahukal_start), '%H:%M:%S').strftime("%I:%M %p")
        rahukal_finish = datetime.strptime(str(rahukal_finish), '%H:%M:%S').strftime("%I:%M %p")
        sunrise = sunrise.strftime("%I:%M %p")
        sunset = sunset.strftime("%I:%M %p")
        # rahukal_days['day{}'.format(a + 1)] = {'rahukal_start': rahukal_start, 'rahukal_finish': rahukal_finish, 'sunrise': sunrise, 'sunset': sunset, 'date': datee}
        a = {'rahukal_start': rahukal_start, 'rahukal_finish': rahukal_finish, 'sunrise': sunrise, 'sunset': sunset, 'date': datee,'dayOfTheWeek':dayOfTheWeek,'country':country_name,'duration':duration}
        b = a.copy()
        rahukal_days.append(b)
      except Exception:
        print('oww sorry we couldn\'t find your Location')
  except Exception:
      print('oww sorry we couldn\'t find your Location')

  print(context)
  context['rahukal'] = rahukal_days
  return render(request,'city.html',context)


def index2(request):
  return render(request,'index2.html')
