from tkinter import *
from bs4 import BeautifulSoup
import requests
# ticker source from:  https://www.nasdaq.com/market-activity/stocks/screener

root = Tk()
root.title('Nasdaq tickers')
root.geometry("350x400")
root.config(bg="gray")
# Update the listbox
def update(data):
    # Clear the listbox
    my_list.delete(0, END)

    # Add toppings to listbox
    for item in data:
        my_list.insert(END, item)

# Update entry box with listbox clicked
def fillout(e):
    # Delete whatever is in the entry box
    my_entry.delete(0, END)

    # Add clicked list item to entry box
    my_entry.insert(0, my_list.get(ANCHOR))


# Create function to check entry vs listbox
def check(e):
    # grab what was typed
    typed = my_entry.get()

    if typed == '':
        data = ticker
    else:
        data = []
        for item in ticker:
            if typed.lower() in item.lower():
                data.append(item)

    # update our listbox with selected items
    update(data)
def getinfo():

    # HTML From Website
    header = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    takein = my_entry.get()
    url = "https://www.marketwatch.com/investing/stock/" + takein
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.find(("h1", {"class", "company_name"})).text
    my_label1.config(text=name)

    price = soup.find("bg-quote", {"class": "value"}).text
    #print("company name is: " + name)
    my_label.config(text= "$" + price)
    #print(price)


# Create a label
#a = "Start Typing..."
my_label1 = Label(root, text="Stock name", font=("Helvetica", 14), fg="black", bg='gray')
my_label1.pack(pady=20)

my_label = Label(root, text="price", font=("Helvetica", 14), fg="black", bg='gray')
my_label.pack(pady=20)


# Create an entry box
my_entry = Entry(root, font=("Helvetica", 20))
my_entry.pack()

my_button = Button(root, text="Enter ticker", bg ="black", fg="white", command=getinfo)
my_button.pack(pady=10)

# Create a listbox
my_list = Listbox(root, width=50)
my_list.pack(pady=20)

ticker = []
with open(r"D:\PythonProjects\nasdaq_tickers.csv") as f:
    for row in f:
        ticker.append(row.split(",")[0])
    print(ticker)

# Add the toppings to our list
update(ticker)

# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>", fillout)

# Create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

root.mainloop()
