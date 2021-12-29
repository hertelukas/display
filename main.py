import json
from icalendar import Calendar
import requests
import datetime
import fontmap
import os
import socket
import locale

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
from entry import get_next_days
from weather import get_forecast

print("-----------")
print(datetime.datetime.now().strftime("%H:%M"))
print("-----------")

weatherDays = 4

locale.setlocale(locale.LC_ALL, '')

# Load icon font
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'display/font')
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

# Parse the entries for the next month
entries = get_next_days(cal, 31)

# Get weather data
forecast = get_forecast(jsonConfig['lat'], jsonConfig['lon'], weatherDays, jsonConfig['api'])

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
    draw.line((540, 0, 540, 480), fill=0)
    textLength = 10

    # Weather
    for i in range(weatherDays):
        if i != 0:
            draw.line((540, i * 105 + 50, 800, i * 105 + 50), fill=0)

        # Draw weather icon
        iconLength, iconHeight = owfont.getsize(fontmap.getChar(forecast[i].icon))
        draw.text((635, (i * 105 + 100 - iconHeight / 2)), fontmap.getChar(forecast[i].icon), font=owfont, fill=0)

        textLength, _ = font20.getsize(str(round(forecast[i].max)) + "°")
        draw.text((580 - (textLength / 2), i * 105 + 75), str(round(forecast[i].max)) + "°" , font=font20, fill=0)

        textLength, _ = font20.getsize(str(round(forecast[i].min)) + "°")
        draw.text((580 - (textLength / 2), i * 105 + 115), str(round(forecast[i].min)) + "°", font=font20, fill=0)

    # Calendar
    padding = 30
    currentHeight = 120
    draw.text((80, 65), "Kalender", font=font40, fill=0)

    for day in entries:
        if len(day.items) != 0:
            # Print title
            draw.text((80, currentHeight), day.date.strftime("%A"), font=font20, fill=0)
            draw.text((230, currentHeight), day.date.strftime("%d.%m"), font=font20, fill=0)
            currentHeight += padding
            # Print events
            for event in day.items:
                if currentHeight > 430:
                    break
                draw.text((80, currentHeight), event, font=font14, fill=0)
                currentHeight += padding - 10
            currentHeight += 10
        
        if currentHeight > 430:
            break


    # Info
    width, height = font14.getsize(datetime.datetime.now().strftime("Letztes update: %H:%M"))
    draw.text((730 - width, 470 - height), datetime.datetime.now().strftime("Letztes update: %H:%M"), font=font14, fill=0)

    # IP Adress
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip =  s.getsockname()[0]
    _, height = font14.getsize(ip)
    draw.text((80, 470 - height), ip)

    epd.display(epd.getbuffer(image))

    print("Finished drawing, going to sleep.")
    epd.sleep()

except KeyboardInterrupt:
    epd7in5_V2.epdconfig.module_exit()
    exit()
