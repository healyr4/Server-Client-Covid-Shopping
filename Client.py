from tkinter import *
import json
import socket

# pip install pillow
#from PIL import Image, ImageTk

MY_FONT= ("Helvetica", 14)
HEADER_LENGTH = 10

#Function to open file and increment ID counter
def getId(file_name):
        file = open(file_name).read()
        user_id = int(float(file))
        user_id = user_id + 1
        new_file = open(file_name, 'w')
        new_file.write(str(user_id))
        new_file.close()
        return user_id


#number is the length of the body after the header
#Include the length of the body of the message plus padding in the header
#It's encoded using UTF-8 and sent over the socket, along with the encoded header
def sendFn(data):
    number = len(data)
    header = f"{ (number+1) :<{HEADER_LENGTH}}".encode('utf-8')
    data = data.encode('utf-8')
    s.send(header + data)

def recFn():
    #Receive bytes of data the length of the header
    message_header = s.recv(HEADER_LENGTH)

    #If not return false
    if not len(message_header): 
        return False

    #Decode the header
    #The message = the data we want
    message_length = int(message_header.decode('utf-8'))
    message = s.recv(int(message_length))
    message = message.decode('utf-8')
    return message

#Add Item Function


#----------Start of GUI--------#
#Inherit from Tk class 
class Window(Tk):
    #initialise method
    #*args to pass keword arguments1`
    #**kwargs to pass any number of keyword arguments-- dictionaries
    def __init__(self, *args, **kwargs):
        #Initialising the inherited class
        Tk.__init__(self, *args, **kwargs)

        #define holder which will contain all frames I want
        holder = Frame(self)
        holder.pack(side="top", fill="both", expand=True)
        #grid for positioning things
        holder.grid_rowconfigure(0,weight=1)
        #Empty dictionary
        self.frames ={}

        
        for F in (DetailsPage,HomePage, ListView, AddItem, RemoveItem):
            frame = F(holder, self)
            self.frames[F]=frame
            #nsew, want widget to expand to fill whole cell
            frame.grid(row=0, column = 0, sticky="nsew")

        #Starting page
        self.show_frame(DetailsPage)

    #Bring forward frame of my choosing
    def show_frame(self, contr):
        frame = self.frames[contr]
        #Bring frame to front for user to see
        frame.tkraise()


#---------Details Page Frame------------------
class DetailsPage(Frame):

    def AddDetails(self):
        name = self.NameEntry.get()
        address = self.AddressEntry.get()
        number = self.PhoneEntry.get()


        #Delete text from these fields
        self.NameEntry.delete(0, END)
        self.AddressEntry.delete(0, END)
        self.PhoneEntry.delete(0, END)

        #increment the counter ID in the text file.
        user_id = getId('UserId.txt')
        
        #JSON object to add to JSON
        data = {"id": user_id,"Name": name, "Home Address": address, "Phone Number": number}
        #Encode Data and send the object with the "a" keyword
        list = ["q", data]
        json_data = json.dumps(list)
        sendFn(json_data)
        print("Sent to server")


    def __init__(self,parent, controller):
        Frame.__init__(self, parent)

        #Item text with entry field
        self.NameLabel = Label(self, text = "Name")
        self.NameLabel.pack()
        self.NameEntry = Entry(self)
        self.NameEntry.pack()

        #Address text with entry field
        self.AddressLabel = Label(self, text="Address")
        self.AddressLabel.pack()
        self.AddressEntry = Entry(self)
        self.AddressEntry.pack()

        #Phone Number text with entry field
        self.PhoneLabel = Label(self, text="Phone Number")
        self.PhoneLabel.pack()
        self.PhoneEntry = Entry(self)
        self.PhoneEntry.pack()
        
        #Add item button, calls the Add function.
        self.AddNameButton = Button(self, text = "Add Details", command=self.AddDetails)
        self.AddNameButton.pack()

        self.GoButton = Button(self, text = "Go to Shopping List", command=lambda: controller.show_frame(HomePage))
        self.GoButton.pack()



#---------Home Page Frame------------------
class HomePage(Frame):
    #Define initialisation
    #self = current object
    #parent = widget which is parent of self
    #controller = to switch between frames
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #label is the object. Label is method
        label = Label(self, text="Welcome To Your Shopping List", font=MY_FONT)
        label.pack(pady=10,padx=10)

        #load = Image.open("trolley.jpg")
        #render = ImageTk.PhotoImage(load)
        #img = Label(self, image=render)
        #img.image = render
        #img.place(x=0, y=0)

        #Add item
        AddItemButton = Button(self, text="Add item ", command=lambda: controller.show_frame(AddItem))
        AddItemButton.pack(side = TOP, expand = True)

        #Remove item
        RemoveItemButton = Button(self, text="Remove item", command=lambda: controller.show_frame(RemoveItem))
        RemoveItemButton.pack(side = TOP, expand = True)

        #Show Shopping list
        ListViewButton = Button (self, text="Open Shopping List", command=lambda: controller.show_frame(ListView))
        ListViewButton.pack(side = TOP, expand = True)

       

#---------Shopping List Frame------------------
class ListView(Frame):

    def RefreshList(self):

        #Leave data blank, no data to send only letter flag
        data = {}
        list = ["r", data]
        json_data = json.dumps(list)
        sendFn(json_data)

        received_list = recFn()
        my_list = json.loads(received_list)
        #Delete the list in the frame
        self.List.delete(0, END)
        for line in my_list:
            self.List.insert(0, line)
            self.List.pack()

    def __init__(self,parent, controller):
        Frame.__init__(self, parent)

        #Button to refresh list
        self.HomePageButton = Button(self, text="Back", command=lambda: controller.show_frame(HomePage))
        self.HomePageButton.pack(side = LEFT)

        #Button to return to main page
        self.EntryButton = Button(self, text="Refresh", command=self.RefreshList)
        self.EntryButton.pack(side=LEFT)

        #Listbox for items in shopping list
        self.List = Listbox(self, width = 60, bg="khaki")
        self.TopLabel = Label(self, text="My Shopping List", font=MY_FONT)
        #Positioning
        self.TopLabel.pack()
        self.List.pack()

    



##---------Adding Item Frame------------------
class AddItem(Frame):

    def AddFn(self):
        item = self.ItemEntry.get()
        quantity = self.QuantityEntry.get()

        #Delete text from these fields
        self.ItemEntry.delete(0, END)
        self.QuantityEntry.delete(0, END)
        

        #increment the counter ID in the text file.
        curr_id = getId('IdCounter.txt')

        #JSON object to add to JSON
        data = {"id": curr_id, "description": item, "quantity": quantity}
        #Encode Data and send the object with the "a" keyword
        list = ["a", data]
        json_data = json.dumps(list)
        sendFn(json_data)

    def __init__(self,parent, controller):
        Frame.__init__(self, parent)

        #BAck Button--> Go to Home Page
        self.HomePageButton = Button(self, text="Back", command=lambda: controller.show_frame(HomePage))
        self.HomePageButton.pack(side = LEFT)

        #Item text with entry field
        self.ItemLabel = Label(self, text = "Item Name")
        self.ItemLabel.pack()
        self.ItemEntry = Entry(self)
        self.ItemEntry.pack()

        #Quantity text with entry field
        self.QuantityLabel = Label(self, text="Quantity")
        self.QuantityLabel.pack()
        self.QuantityEntry = Entry(self)
        self.QuantityEntry.pack()
        
        #Add item button, calls the Add function.
        self.AddItemButton = Button(self, text = "ADD", command=self.AddFn)
        self.AddItemButton.pack()

  

class RemoveItem(Frame):

    def RemoveItem(self):
        #Get Id from entry field
        #Delete text from field
        #Encode it and send it in a list to the server with "d" keyword
        id = self.IdEntry.get()
        list = ["d", str(id)]
        json_data = json.dumps(list)
        sendFn(json_data)
        self.IdEntry.delete(0, END)

    #self = current object
    #parent = widget which is parent of self
    #controller = to switch between frames
    def __init__(self,parent, controller):
        Frame.__init__(self, parent)

        HomePageButton = Button(self, text="Back", command=lambda: controller.show_frame(HomePage))
        HomePageButton.pack(side = LEFT)

        self.DeleteButton = Button(self, text="Delete", command=self.RemoveItem)
        self.DeleteButton.pack(side=LEFT)
        self.IdEntry = Entry(self)
        self.IdEntry.pack()


        self.IdLabel = Label(self, text="Enter ID of item to be deleted")
        self.IdLabel.pack()

    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Ip address of local host
IP = "127.0.0.1"
#This port uses TCP
PORT = 42070
s.connect((IP, PORT))

#Create the instance
program = Window()

program['bg'] = 'SkyBlue1'
program.geometry('500x250')
program.resizable(False, False)
program.title ("CoVid-19 Shopping List")

program.mainloop()