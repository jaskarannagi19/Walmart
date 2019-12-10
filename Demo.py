from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package to extract useful information from html page
import tkinter as tk # tkinter is a library for developing GUI
from tkinter import Scrollbar # import canvas and BOTH for drawing but where not used in project can be removed
import requests #requests to actually call the url

class GUI(tk.Frame): #main GUI class which takes in Tkinker frame as object for initialization
   def __init__(self, frame):# init constructor of class when class is called this function runs and set everything
       tk.Frame.__init__(self, frame) #calling constructor of tk.Frame and telling it what frame to use
       self.root = frame #setting frame in class so that we can access it anywhere using self.root
       self.initialize_user_interface() #let's call this function to actually create GUI

   def initialize_user_interface(self):
       self.root.geometry("400x400") #set the size of frame
       self.root.title("Price Scraper") #set title of the frame

       walmart_frame = tk.LabelFrame(self.root, text="Walmart Link", pady=0) #declare label frame so that it looks like a box with borders and text Walnart Link
       self.entry1=tk.Text(walmart_frame, height=10, width=30) #define input place where use will be pasting the link. # NOTE:  we want this input to be inside walmart_frame thus we are injecting it, we can also infect self.root if we want this to be in mai tkinter frame
       self.entry1.pack() #pack the entry we created this needs to be done for every fields,buttons we want to show in frame
       self.button=tk.Button(walmart_frame,text="Submit", command=self.readUrl) #make a button and tell it that on clicking call readUrl function
       self.button.pack() #pack the button
       self.label=tk.Listbox(walmart_frame) #create an empty label where we will be display our extracted price.
       self.label.pack() #pack this label
       walmart_frame.pack() #finally pack this label frame as well. # NOTE: pack this frame at last since we where building elements inside it.



       homedepot_frame = tk.LabelFrame(self.root, text="Homedepot Link", pady=0) #create another label frame for homedepot
       self.entry2=tk.Text(homedepot_frame, height=10, width=30) # input field
       self.entry2.pack() #pack field
       self.button1=tk.Button(homedepot_frame,text="Submit", command=self.homedepotUrl) # button to call function which does scrapping call homedepotUrl
       self.button1.pack() #pack this button
       self.label1=tk.Label(homedepot_frame,text="") #emtpy label to declare price.
       self.label1.pack() #pack
       homedepot_frame.pack() #finally pack frame


   def homedepotUrl(self): #on button click of Homedepot frame this function is called
       url1 = self.entry2.get("1.0",END) # let's get the value of entry. ## NOTE: we initialed that entry2 in self becase we want to access it here. Variables in self can be access anywhere in python class. But don't consider them as global variable its more of constructor thing study about "self" in detail separately
       #url="https://www.homedepot.com/p/DEWALT-20-Volt-MAX-XR-Lithium-Ion-Brushless-Cordless-Combo-Kit-6-Tool-2-5Ah-Batteries-Charger-Bag-Free-Impact-Wrench-DCK694P2W894B/309377460"  #this is nothing but test url so that I dont have to keep on copy paste url while development

       content1 = requests.get(url1,headers={'User-agent': 'Mozilla/5.0'}) #using requests to navigate to the url pasted by user and store its response in content1
       soup1 = BeautifulSoup(content1.text, 'html.parser') #since this is not an API but an HTML page thus we parse it using BeautifulSoup(BS) with html parser

       mydivs1 = soup1.findAll("div",{"class":"price__wrapper"}) #now using BS we will find all divs in html with class price_wrapper

       price1 = "" # declare an empty string

       ## this will be different for each website or even within website because each html is structurally different

       for span in mydivs1[0].findAll("span"): #for each element we find in mydivs[0] since mydivs is a resultset we cannot iterate over it. We can only itereate results which are at index 0
           str=span.text.replace(" ","") #for this span text we will replace whitespace with "" that means no whitespace because price extract has unnecessary whitespace and we dont want that
           str = str.replace("\n","") #we will also replace new line character with "" because prices are in different span and each span has a new line at the end
           price_len= len(str) #find the length of the string price we get is like this 64900 notice this doesnt have dot of cents
           start_len = price_len - 2 #let subtract the 2 from the length because each price will be different and we want a dot before last 2 digits
           final = str[:start_len] + '.' + str[start_len:] #string are not mutable(google about it) so we will create new string with character upto length minus last 2 plus a dot and then last 2 chars
           price1 = final # stupid assignment
           break #break the loop after 1st since we get 6 spans with sames classes and 1 operations gets us the price


       self.label1.insert(price1) #get the label1 get create above empty label and set it text
       pass #end of function
       #print("Final price is {}".format(price))



   def readUrl(self):
       urls = self.entry1.get("1.0","end-1c")
       urls = urls.split('\n')

       for url in urls:
           price=[]
           content = requests.get(url)
           soup = BeautifulSoup(content.text, 'html.parser')
           mydivs = soup.findAll("span", {"class": "price-group"})
           name = soup.select('h1.prod-ProductTitle')[0].text.strip() + " "
           for span in mydivs[0].findAll("span"):
       	       name+=span.text
           price.append(name)
           self.label.insert(0,price)

       
if __name__ == '__main__':

   root = tk.Tk() #call tinker for initial frame
   run = GUI(root) #send this frame as object to our class
   root.mainloop() #mainloop so that tkinker runs and display stuff
