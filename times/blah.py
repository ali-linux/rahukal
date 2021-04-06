from django.shortcuts import render, redirect, get_object_or_404
import json
from urllib.request import urlopen
from timezonefinder import TimezoneFinder
from datetime import datetime,time,timedelta,date
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import os
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
  u=os.path.join( settings.BASE_DIR, 'rahukal/static/assets/json/timezones.json' )
  # u = staticfiles_storage.url('assets/json/cities.json')
  offset = 0
  hour = 0
  minute = 0
  rahukal_days = {}
  datee= datetime.now()
  # datee= datee.replace(day=datee.day+a)
  datee= datee.strftime("%Y-%m-%d")

  for c in cities:
    with urlopen("https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={datee}".format(lat=c['latitude'], lng=c['longitude'],datee=datee)) as response:
      source = response.read()

    data = json.loads(source)
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    print(sunrise, sunset)
    sunrise = datetime.strptime(sunrise, '%I:%M:%S %p')
    sunset = datetime.strptime(sunset, '%I:%M:%S %p')
    timezone = tf.timezone_at(lng=c['longitude'], lat=c['latitude'])
    with open(u,encoding="utf8") as f:
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

    rahukal_start = datetime.strptime(str(rahukal_start), '%H:%M:%S').strftime("%I:%M %p")
    rahukal_finish = datetime.strptime(str(rahukal_finish), '%H:%M:%S').strftime("%I:%M %p")
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")
    rahukal_days['{}'.format(c['city'])] = {'rahukal_start': rahukal_start, 'rahukal_finish': rahukal_finish, 'sunrise': sunrise, 'sunset': sunset, 'date': datee,'city':c['city']}
    
  context = {'rahukal':rahukal_days}
  return render(request,'index.html',context)
