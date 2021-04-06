import json
from urllib.request import urlopen
from timezonefinder import TimezoneFinder
from datetime import datetime,time,timedelta,date

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
city_name=''
offset = 0
hour = 0
minute = 0
c = input('enter city: ');
rahukal_days = {}

def remove_spaces(str):
  return (" ".join(str.split())).replace(' ','')


try:
  with open('new_cities.json',encoding="utf8") as f:
    cities = json.load(f)


  i = False
  for city in cities:
    if (remove_spaces(city['name'].lower()) == remove_spaces(str(c).lower()) and i == False):
      print(remove_spaces(city['name'].lower()))
      print(remove_spaces(str(c).lower()))
      longitude = float(city['lng'] )
      latitude = float(city['lat'])
      city_name = city['name']
      i = True
    elif(i):
      break;
  
  if (city_name == ''):
    raise ValueError
    
  for a in range(7):
    datee= datetime.now()
    datee= datee.replace(day=datee.day+a)
    datee= datee.strftime("%Y-%m-%d")
    try:
      with urlopen("https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={datee}".format(lat=latitude, lng=longitude,datee=datee)) as response:
        source = response.read()

      data = json.loads(source)
      sunrise = data['results']['sunrise']
      sunset = data['results']['sunset']
      print(sunrise, sunset)
      sunrise = datetime.strptime(sunrise, '%I:%M:%S %p')
      sunset = datetime.strptime(sunset, '%I:%M:%S %p')
      timezone = tf.timezone_at(lng=longitude, lat=latitude)
      with open('timezones.json',encoding="utf8") as f:
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
      rahukal_days['day{}'.format(a+1)]={'rahukal_start':rahukal_start,'rahukal_finish':rahukal_finish,'sunrise':sunrise,'sunset':sunset,'date':datee}
    except Exception:
      print('oww sorry we couldn\'t find your Location')

except Exception:
    print('oww sorry we couldn\'t find your Location')

print(rahukal_days)
