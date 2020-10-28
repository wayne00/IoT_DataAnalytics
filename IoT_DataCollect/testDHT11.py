import Adafruit_DHT as dht
import time

def get_temp_hum():
	sensor = dht.DHT11
	pin = 2
	humidity, temperature = dht.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
		return round(temperature,2), round(humidity,2)
	else:
		return 0, 0


while True:
	print(get_temp_hum())
	time.sleep(3)
