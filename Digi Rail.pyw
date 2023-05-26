from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

root=Tk()
root.title("Digi Rail")


r=IntVar()
r.set(1)
frame=LabelFrame(root,text="Welcome",padx=50,pady=50)#padding inside the frame
frame.pack(padx=40,pady=40)#padding outside of frame



def click(value):
	
	if value==1:
		top=Toplevel()
		top.title("Schedule Finder")

		t=IntVar()
		t.set(1)
		frame=LabelFrame(top,text="Train Data",padx=50,pady=50)#padding inside the frame
		frame.pack(padx=10,pady=10)#padding outside of frame

		def getdata(url):
			r = requests.get(url)
			return r.text

		station1=Entry(frame,width=35,borderwidth=5)
		station1.insert(0,"Please enter code of Station(From)")
		station1.grid(row=0,column=0,columnspan=2)
		station2=Entry(frame,width=35,borderwidth=5)
		station2.insert(0,"Please enter code of Station(To)")
		station2.grid(row=1,column=0,columnspan=2)
		sname1=Entry(frame,width=35,borderwidth=5)
		sname1.insert(0,"Please enter name of Station(From)")
		sname1.grid(row=2,column=0,columnspan=2)
		sname2=Entry(frame,width=35,borderwidth=5)
		sname2.insert(0,"Please enter name of Station(To)")
		sname2.grid(row=3,column=0,columnspan=2)
		date=Entry(frame,width=35,borderwidth=5)
		date.insert(0,"Please enter date")
		date.grid(row=4,column=0,columnspan=2)

		def find():
			mid=Toplevel()
			mid.title("Schedule")

			mid.geometry("500x500")

			# pass the url into getdata function
			url = "https://www.railyatri.in/booking/trains-between-stations?from_code="+station1.get()+"&from_name="+sname1.get()+"+JN+&journey_date="+date.get()+"&src=tbs&to_code="+station2.get()+"&to_name="+sname2.get()+"+JN+&user_id=-1636260722&user_token=61636260722&utm_source=train_ticket_dweb_search"

			htmldata = getdata(url)
			soup = BeautifulSoup(htmldata, 'html.parser')
			# find the Html tag
			# with find()
			# and convert into string
			data_str = ""
			for item in soup.find_all("div", class_="TravelTimeInfo"):
				data_str = data_str + item.get_text()
			result1 = data_str.split("\n")
			# print(result1)
			for item in soup.find_all("div", class_="namePart"):
				data_str = data_str + item.get_text()
			result2 = data_str.split("\n")
			# print(result2)

			# Display the result
			for element in result1:
				if element in result2:
					result2.remove(element)
			result1=list(filter(None,result1))
			

			my_tree=ttk.Treeview(mid)
			my_tree['columns']=("ele1","ele2")

			my_tree.column("#0",width=0)
			my_tree.column("ele1",width=300,anchor=W)
			my_tree.column("ele2",width=150,anchor=W)

			my_tree.heading("#0",text="",anchor=W)
			my_tree.heading("ele1",text="Train Names",anchor=W)
			my_tree.heading("ele2",text="Timings",anchor=W)

			l=[[] for i in range(len(result2))]
			k=0
			j=0
			for i in range(len(result2)-1):
				if result2[i] == '':
					j = j + 1
				else:
					l[j].append(result2[i])

			for i in range(len(result1)-1):
				if result1[i]=='                              ' or result1[i]==' ' or result1[i]=='            ':
					k = k + 1
				else:
					l[k].append(result1[i])
			# print(l)
			d=[]
			p=[]
			for d in range(len(l)-1):
				if len(l[d])==6:
					p.append(l[d])
			# print(p)
			c=0
			for r in p:
				my_tree.insert(parent='',index='end',iid=c,text="",values=(r[0],r[1]))
				c=c+1
				my_tree.insert(parent='',index='end',iid=c,text="",values=('',r[2]))
				my_tree.move(c,c-1,'end')
				c=c+1
				my_tree.insert(parent='',index='end',iid=c,text="",values=('',r[3]))
				my_tree.move(c,c-2,'end')
				c=c+1
				my_tree.insert(parent='',index='end',iid=c,text="",values=('',r[4]))
				my_tree.move(c,c-3,'end')
				c=c+1
				my_tree.insert(parent='',index='end',iid=c,text="",values=('',r[5]))
				my_tree.move(c,c-4,'end')
				c=c+1

			my_tree.pack(padx=40,pady=40)

			

		button=Button(top,text="Find",command=find)
		button.pack()



button=Button(frame,text="Train TimeTable",command=lambda:click(r.get()))
button.pack()



root.mainloop()