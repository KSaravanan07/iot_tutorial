#This should run with your default unzipping of aws sdk
#Make sure to replace caPath, certPath, awshost and keypath with your own certificates. Make sure you place this file inside the extracted aws-sdk folder
#Refer to the start.sh file to check your awshost form the command line arguments being passed there

import paho.mqtt.client as mqttClient
import time
import ast
import random
import ssl

def location_generator():
    corr={'x':random.randrange(0,250,1),
          'y':random.randrange(0,250,1)}
    return corr

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)


Connected = False  # global variable for the state of the connection
client_name="basicPubSub" #This is the client name by default allowed in the policy
curr=location_generator()


#AWS_PART
client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1, client_name)  # create new instance
client = mqttClient.Client(client_name)
client.on_connect = on_connect  # attach function to callback

awshost = "a2fo2kqe3qv56z-ats.iot.us-east-1.amazonaws.com" #replace
awsport = 8883

caPath = "./root-CA.crt" # Root certificate authority, comes from AWS (Replace)
certPath = "./iot_1.cert.pem" #Replace
keyPath = "./iot_1.private.key" #Replace

client.tls_set(caPath, 
    certfile=certPath, 
    keyfile=keyPath, 
    cert_reqs=ssl.CERT_REQUIRED, 
    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

client.connect(awshost, port = awsport)  # connect to broker
#AWS PART ENDS

client.loop_start()  # start the loop



while Connected != True:  # Wait for connection
    print("Connecting ...")
    time.sleep(0.1)


try:
    while True:
        client.publish("sdk/test/python", str(curr)) #This is the topic by default allowed in the policy
        print("Message published is : " + str(curr))
        time.sleep(2)
        curr=location_generator()

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
