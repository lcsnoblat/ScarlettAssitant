import socket
import sys
import RPi.GPIO as GPIO
from thread import *
import datetime
import random
import requests
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

host = ''
port = 8220
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)
#Variable for the number of connections
numbOfConn = 0

#Name of list used for connections
addressList = []
clients = set()
##############################################################################
#small database of our bot
greetings = ['Ola', 'hello', 'oi', 'hey', 'hi']
questions = ['Tudo bem?', 'Como está?']
responses = ['Estou bem', 'Tudo tranquilo']
database={
    'Scarlet':'Olá, Como posso ajuda-lo?',
    'Qual seu nome?':'Scarlet',
    'Qual é o seu nome?':'Scarlet',
    'Olá Scarlet':'Olá, como posso lhe ajudar?',
    'Oque você pode fazer?':'Posso fazer muitas coisas'
}

print ("Listening for client . . .")
###############################################################################
#chatbot code here
def chatboat(data):
    if data in database:
        print(database[data])
        #os.system("flite -t '"+ database[data] +"'")
        sclient(database[data])
    elif data in questions:
        random_response = random.choice(responses)
        print(random_response)
        #os.system("flite -t '"+ random_response +"'")
        sclient(random_response)
    elif data in greetings:
        random_greeting = random.choice(greetings)
        print(random_greeting)
        sclient(random_greeting)
        #os.system("flite -t '"+ random_greeting +"'")
    elif 'ligue a luz' in data or 'acenda a luz' in data:
        sclient("light turn on")
        #os.system("flite -t 'light turn on'")
        GPIO.output(2,GPIO.HIGH)
        print("Light on")
    elif 'desligue a luz' in data or 'desligue a Luz' in data:
        sclient("light turn off")
        #os.system("flite -t 'light turn off'")
        GPIO.output(2,GPIO.LOW)
        print("Light Off")
    elif 'Horas' in data:
        now = datetime.datetime.now()
        time=str(now.hour)+str("hours")+str(now.minute)+str("minutes")
        print(time)
        #os.system("flite -t '"+ time+"'")
        sclient(time)
    elif 'Data'in data:
        now = datetime.datetime.now()
        date=str("%s/%s/%s" % (now.month,now.day,now.year))
        print(date)
        #os.system("flite -t '"+date+"'")
        sclient(date)
    else:
        conn.send("Não entendi... poderia repetir?")
        add_data = open("newdata.txt", 'a')
        add_data.write("\n")
        add_data.write(data)
        add_data.close()
###############################################################################
#Sending Reply to all clients
def sclient(mess):
    for c in clients:
        try:
            c.send(mess)
        except:
            c.close()
##############################################################################
#server code here
def clientthread(conn,addressList):
#infinite loop so that function do not terminate and thread do not end.
     while True:
        output = conn.recv(2048);
        if output.strip() == "disconnect":
            conn.close()
            sys.exit("Received disconnect message.  Shutting down.")
            conn.send("connection loss")
        elif output:
            print ("Message received from client:")
            data=str(output).lower()
            print (data)
            print("Reply from the server:")
            chatboat(data)

while True:
#Accepting incoming connections
    conn, address = server_socket.accept()
    print ("Connected to client at ", address)
    clients.add(conn)
#Creating new thread. Calling clientthread function for this function and passing conn as argument.
    start_new_thread(clientthread,(conn,addressList)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

conn.close()
sock.close()   
