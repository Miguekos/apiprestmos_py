from app import app
from mongo import mongo
import time
import json
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
import requests
from pytz import timezone

try:
    print(mongo.db)
except:
    print("{}".format("Error al conectar al MONGO"))

now_new = datetime.now()

timestamp = datetime.timestamp(now_new)

print("timestamp =", timestamp)

lima = timezone('America/Lima')
li_time = datetime.now(lima)
print(li_time)
time_hora_new = li_time.strftime('%H:%M:%S')
date_time = li_time.strftime('%d/%m/%Y')

# print("{} {}".format(date_time, time_hora_new))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)