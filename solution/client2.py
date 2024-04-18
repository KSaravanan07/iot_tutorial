import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import ast

all_clients=[]
for i in range(1,6):
    all_clients.append('client'+str(i))
contact=[]

def location_generator():
    corr={"x":random.randrange(0,250,1),
          "y":random.randrange(0,250,1)}
    return corr

def distance(curr,to):
    return math.sqrt((to['x']-curr['x'])**2+(to['y']-curr['y'])**2)



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)


def on_message(client, userdata, message):
    #Task-5 Write code here
    print("Message Received is : " + str(message.payload))
    print("Message Received on Topic " + str(message.topic))
    temp = message.payload.decode("utf-8")
    resp = ast.literal_eval(temp)
    print(" distance from " + str(message.topic).split('/')[0] + " is " + str(distance(curr,resp)))
    neighbor_name = str(message.topic).split('/')[1] 
    if distance(curr,resp) < 20 and neighbor_name not in contact:
        contact.append(neighbor_name)



curr=location_generator()
#Task-1 Write code here

Connected = False
client_name = sys.argv[1]
broker_address = "127.0.0.1"
port = 1883 


#Task-2 Write code here
 # create new instance MQTT client 
client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1, client_name)

client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback


client.connect(broker_address, port=port)  # connect to broker
client.loop_start()  # start the loop

#Task-3 Write code here
self_id = int(client_name[6:])
print(" current client ID " + str(self_id))

for i in range(1,6):
    if i != self_id:
        client.subscribe("location/client" + str(i))
        print("client subscribed for location/client" + str(i))

end_time=time.time()+15

try:
    while time.time() < end_time:
        # Task-4 Write code here
        client.publish("location/"+client_name,str(curr))
        time.sleep(0.25)
        curr=location_generator()

except KeyboardInterrupt:
     print("exiting")
     client.disconnect()
     client.loop_stop()



print(contact)
