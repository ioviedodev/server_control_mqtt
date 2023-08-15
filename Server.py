import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# Crear el documento JSON con un valor por defecto para "ControlTemperatura"
dataControl = {
    "TemperatureControl": "na", #na: no action
    "HumidityControl": "na"
}

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código: {rc}")
    client.subscribe(TOPICO_SUBSCRIPCION)

# Callback cuando se recibe un mensaje del broker
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temperature = data["Temperature"]
        humidity = data["Humidity"]
        # Obtener la hora actual
        current_time = datetime.now().time()
        print(f"--------->Data received {current_time} :")
        print(f" Checking Values........ \nTemperature: {temperature}°C, \nHumidity: {humidity}%")
        
        if temperature>=10:
            print(f"¡¡¡¡Temperature Threshold Reached!!!!!") 
            dataControl["TemperatureControl"]="ON"
            print(f"...Sending Turn on cooling system...")
        else:
             dataControl["TemperatureControl"]="OFF"
             print(f"...Sending Turn off cooling system...")    
        
        if humidity>=80:
            print(f"¡¡¡¡HumidityControl Threshold Reached!!!!!") 
            dataControl["HumidityControl"]="ON"
            print(f"...Sending Turn on valve water...")
        else:
            dataControl["HumidityControl"]="OFF"
            print(f"...Sending Turn off cooling system...")     
            
        json_data = json.dumps(dataControl)
        
        # Publicar el documento JSON en el tópico "Control"
        client.publish("Control01", json_data)
        
            
            
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON")
    
# Configuración
MQTT_SERVER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICO_SUBSCRIPCION = "Monitoring01"

# Crear cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Iniciar loop en segundo plano para procesar los callbacks
client.loop_start()

try:
    while True:
        # Publicar un número aleatorio entre 10.00 y 25.00 en el tópico "monitoring"
        # valor_aleatorio = round(random.uniform(10.00, 25.00), 2)
        # client.publish("monitoring", str(valor_aleatorio))
        time.sleep(5)  # Esperar 5 segundos

except KeyboardInterrupt:
    print("\nDesconectando...")
    client.loop_stop()  # Detener loop
    client.disconnect()  # Desconectar del broker

