#For socket API functions
import socket
import sys
import json
import os
HEADER_LENGTH = 10
#sock_stream is for TCP protocol
#AF_INET = adress family for IpV4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Ip address of local host
IP = "127.0.0.1"
#This port uses TCP
PORT = 42070

#Bind the socket to IP address and port
s.bind((IP, PORT))

#Await conenction from the client
#10 is max num of queued connections
s.listen(10)          
print(f"Server awaiting connnections")      

#conn is a new socket object to send/rec data
#Addr is address bound to the socket at other end
conn, addr = s.accept()
print("Connection from",addr,"has been established")




def recFn():
    #Receive bytes of data the length of the header
    message_header = conn.recv(HEADER_LENGTH)

    #If not return false
    if not len(message_header):
        return False

    #Decode the header
    #The message = the data we want
    message_length = int(message_header.decode('utf-8'))
    message = conn.recv(int(message_length))
    message = message.decode('utf-8')
    return message

def sendFn(data):
    number = len(data)
    header = f"{ (number+1) :<{HEADER_LENGTH}}".encode('utf-8')
    data = data.encode('utf-8')
    conn.send(header + data)
    

while True:

    rec_data = recFn()
    if not rec_data:
        break

    #Function to send shopping list to client
    def  refresh():
        with open('ShoppingList.json', 'rb') as s_file:
            s_list = json.load(s_file)
            #Encode-- Convert python dictionary to JSON string
            full_list = json.dumps(s_list)
            sendFn(full_list)
            print("Shopping list has been updated")
        #Using this statement the file is automatically closed

    #To write JSON to JSON file
    def write_json(data, filename): 
            with open(filename,'w') as f: 
                json.dump(data, f, indent=4) 
    
    #Await an instruction--add, delete, oor
    #Parse JSON string to get python dictionary
    #Decode JSON data
    data = json.loads(rec_data)
    pressed = data[0]
    #csv or json data
    json_data = data[1]
    
     #Send the whole JSON to the client
    if pressed == 'r':
        refresh()

	
    #Adding details
    elif pressed == 'q':
        print (json_data)
  
        with open('UserList.json', 'r') as user_file:
            user_list = json.load(user_file)
            user_list.append(json_data) 
        
        write_json(user_list,'UserList.json')
        print("Has been added to the user list")
     


    elif pressed == 'a': 
        print (json_data)
         #add
          
        with open('ShoppingList.json') as s_file: 
            s_list = json.load(s_file)
            #Append it to end of the JSON shopping list 
            s_list.append(json_data) 
        
        write_json(s_list,'ShoppingList.json')
        print("Has been added to the shopping list")
        #refresh()

    #delete
    elif pressed == 'd': 
        with open('ShoppingList.json', 'rb') as s_file:
            s_list = json.load(s_file)
            
            for i in range(len(s_list)):
                #i= number in list of the item
                if s_list[i]["id"] == int(float(json_data)):
                    s_list.pop(i)
                    break
        write_json(s_list,'ShoppingList.json')
        print(f" Id no: {json_data} has been removed from the shopping list")
        #refresh()
        

s.close()
sys.exit()
    
   
