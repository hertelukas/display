import json
from icalendar import Calendar
import requests
import datetime
import fontmap
import os

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
from entry import DateEntry, Entry, TimeEntry, parse
from weather import get_forecast

weatherDays = 3

# Load icon font
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'epaper/pic')
# read config file
with open('config.dis', 'r') as file:
    config = file.read();

jsonConfig = json.loads(config)


# Download ical file
if jsonConfig['ical']:
    # TODO check status
    cal = Calendar.from_ical(requests.get(jsonConfig['ical']).content)
else:
    print("Failed to get calendar.")

today = datetime.date.today();

# Parse the entries for the next 7 days
entries = parse(cal, today, today + datetime.timedelta(days=7))

# Get weather data
forecast = get_forecast(jsonConfig['lat'], jsonConfig['lon'], 3, jsonConfig['api'])

# Drawing
try:
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    font14 = ImageFont.truetype(os.path.join(fontdir, 'font.ttf'), 14)
    font20 = ImageFont.truetype(os.path.join(fontdir, 'font.ttf'), 20)
    font40 = ImageFont.truetype(os.path.join(fontdir, 'font.ttf'), 40)
    owfont = ImageFont.truetype(os.path.join(fontdir, 'owfont.ttf'), 60)

    image = Image.new('1', (epd.width, epd.height), 255)
    icons = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)
    icons_draw = ImageDraw.Draw(icons)
    draw.line((0, 150, 480, 150), fill=0)
    draw.line((480, 0, 480, 480), fill=0)

    textLength = 10


    for i in range(weatherDays):
        draw.line((i * 160, 0, i * 160, 150), fill=0)
        iconLength, iconHeight = owfont.getsize(fontmap.getChar(forecast[i].icon))
        draw.text((80 + i * 160)- iconLength / 2, 20), fontmap.getChar(forecast[i].icon), font=owfont, fill=0)
        textLength, _ = font20.getsize(str(round(forecast[i].max)) + "°")
        draw.text(((80 + i * 160) - textLength / 2, 85), str(round(forecast[i].max)) + "°" , font=font20, fill=0)
        textLength, _ = font20.getsize(str(round(forecast[i].min)) + "°")
        draw.text(((80 + i * 160) - textLength / 2, 110), str(round(forecast[i].min)) + "°", font=font20, fill=0)

    # # Calendar
    # padding = 30
    # currentHeight = 80
    # draw.text((510, 20), "Calendar", font=font40, fill=0)

    # for day in calendarDays:
    #     draw.text((510, currentHeight), day.date.strftime("%A"), font=font20, fill=0)
    #     draw.text((650, currentHeight), day.date.strftime("%d.%m"), font=font20, fill=0)
    #     currentHeight += padding
    #     if len(day.items) != 0:
    #         for event in day.items:
    #             draw.text((520, currentHeight), event, font=font14, fill=0)
    #             currentHeight += padding - 10
    #         currentHeight += 10


    # Info
    width, height = font14.getsize(datetime.now().strftime("Last update: %H:%M"))
    draw.text((800 - width, 480 - height), datetime.now().strftime("Last update: %H:%M"), font=font14, fill=0)

    epd.display(epd.getbuffer(image))

    print("Finished drawing, going to sleep.")
    epd.sleep()

except KeyboardInterrupt:
    epd7in5_V2.epdconfig.module_exit()
    exit()
