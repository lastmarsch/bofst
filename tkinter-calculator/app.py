import json
from tkinter import END, LEFT, IntVar, Menu, Text, Tk, Canvas, Button, Toplevel
from tkinter.ttk import Combobox, Spinbox, Label

from calculator import calculate

help_text = "How to use:\n\n" +\
"1. Select Month (from 1 to 12).\n" +\
"2. Select Year (from 2000 to 2022).\n" +\
"3. Select Half of the month (\n\t1 - from 26th of the previous month to 15th of the selected month, \n\t2 - from 15th of the selected month to 25th of the selected month\n).\n" +\
"4. Click Calculate button.\n" +\
"5. The Result will be shown in the text area."

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def HighlightPattern(self, pattern, tag, start="1.0", end="end", regexp=True):
        '''Apply the given tag to all text that matches the given pattern'''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",end)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index,count.get()))
            self.tag_add(tag, "matchStart","matchEnd")

class App(Tk):

    WIDTH = 500
    HEIGHT = 470

    def __init__(self):
      super().__init__()
      self.load_data()
      self.render()   

    def help(self):
      try:
        self.win.focus_set()
        return
      except Exception:
        pass
         
      self.win = Toplevel(self.hm)
      self.win.title("Help") 
      self.win.resizable(0,0)
      t=Text(
        self.win, 
        highlightthickness=0,
        wrap="word", 
      )
      # print(help_text)
      t.insert(END, help_text.strip())
      t.config(state="disabled")
      t.pack()
        
    def render(self):
      self.title("Timesheet calculator")
      self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
      self.configure(bg = "#516BC6")
      self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

      # Menu
      self.mainmenu = Menu(self) 
      self.config(menu=self.mainmenu) 

      self.win = None
      self.hm = Menu(self.mainmenu, tearoff=0)
      self.mainmenu.add_cascade(label="Help",menu=self.hm)
      self.hm.add_command(label="How to use", command=self.help)

      self.create_canvas()
      
      self.create_title(
          118.0,
          30.0,
          "Timesheet calculator",
        )
        
      self.elements = {}
        
      self.create_label(
          60.0,
          80.0,
          "Month",
        )
      combobox = self.create_combobox(
          opts=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
          x=136.0, 
          y=79.0, 
          width=38.0,
          height=22.0
        )
      self.elements["month"] = combobox
        
      self.create_label(
          205.0,
          80.0,
          "Year",
        )
      spinbox = self.create_spinbox(
          from_=2000,
          to=2022,
          x=259.0,
          y=79.0,
          width=60.0,
          height=22.0
        )
      self.elements["year"] = spinbox
        
      self.create_label(
          345.0,
          80.0,
          "Half",
        )
      combobox = self.create_combobox(
          opts=["1", "2"],
          x=397.0,
          y=79.0,
          width=38.0,
          height=22.0
        )
      self.elements["half"] = combobox
        
      self.create_button(
          text="Calculate",
          callback=self.calculate,
          x=176.0,
          y=123.0,
          width=149.0,
          height=42.0
        )
        
      self.create_title(
          209.0,
          195.0,
          "Result",
        )
        
      self.resultarea = self.create_textarea(
          x=60.0,
          y=244.0,
          width=370.0,
          height=200.0
        )     
        
    def create_canvas(self):
      self.canvas = Canvas(
        self,
        bg = "#516BC6",
        height = App.HEIGHT,
        width = App.WIDTH,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
      )
      self.canvas.place(x = 0, y = 0)
      
    def create_title(self, x=0, y=0, text=''):
      self.canvas.create_text(
        x,
        y,
        anchor="nw",
        text=text,
        fill="#FFFFFF",
        font=("Montserrat", 24 * -1, 'bold')
      )
      
    def create_label(self, x=0, y=0, text=''):
      self.canvas.create_text(
        x,
        y,
        anchor="nw",
        text=text,
        fill="#FFFFFF",
        font=("Montserrat", 18 * -1)
      )
      
    def create_combobox(self, opts=[], x=0, y=0, width=0, height=0):
      combobox = Combobox(
        values=opts,
        state="readonly", 
      )
      combobox.current(0)
      combobox.place(
        x=x, 
        y=y, 
        width=width,
        height=height
      )    
      return combobox
      
    def create_spinbox(self, from_=0, to=0, x=0, y=0, width=0, height=0):
      spinbox = Spinbox(
        from_=from_,
        to=to,
        wrap=True,
        state="readonly", 
      )
      spinbox.set(to)
      spinbox.place(
        x=x, 
        y=y, 
        width=width,
        height=height
      )  
      return spinbox   
      
    def create_button(self, text='', callback=lambda x: x, x=0, y=0, width=0, height=0):
      button = Button(
        borderwidth=0,
        bg='#64BC97',
        activebackground='#64BC97',
        fg='white',
        activeforeground='white',
        font=("Montserrat", 18 * -1, 'bold'),
        text=text,
        highlightthickness=0,
        command=callback,
        state = "normal",
        relief="flat",    
      )
      button.place(
        x=x, 
        y=y, 
        width=width,
        height=height
      ) 
      
    def create_textarea(self, x=0, y=0, width=0, height=0):
      textarea = Text(
        bd=0,
        bg="#FFFFFF",
        fg="black",
        highlightthickness=0,
        state="disabled"
      )
      textarea.place(
        x=x, 
        y=y, 
        width=width,
        height=height
      )
      return textarea

    def calculate(self):
      month = int(self.elements["month"].get())
      year = int(self.elements["year"].get())
      half = int(self.elements["half"].get())
      
      # print(f"Month: {month}\tYear: {year}\tHalf: {half}")
      
      result = ""
      
      for department in self.departments:
        # print(department['name'])
        result += f"{department['name']}\n"
        
        for worker in department['workers']:
          name, time = worker.values()
          hours = calculate(time, month, year, half, part_time=self.part_time)
          
          # print(f"{name}:\t{round(hours, 1)} hours")
          result += f"{name}:\t{round(hours, 1)} hours\n"
          
        # print()
        result += "\n"
      
      self.resultarea.config(state="normal")
      self.resultarea.delete("1.0", END)
      self.resultarea.insert(END, result.strip())
      self.resultarea.config(state="disabled")
     
      
    def load_data(self): 
      # with open('data.json') as f:
      #   data = json.load(f)
        
      data = {
        "part_time": 8,
        "departments": [
          {
            "name": "Department Tr",
            "workers": [
              {
                "name": "Ш_Тр",
                "time": 0.25
              },
              {
                "name": "Щ_Тр",
                "time": 0.25
              },
              {
                "name": "Н_Тр",
                "time": 0.25
              },
              {
                "name": "К_Тр",
                "time": 0.2
              },
              {
                "name": "М_Тр",
                "time": 0.1
              }
            ]
          },
          {
            "name": "Department O",
            "workers": [
              {
                "name": "С_О",
                "time": 0.25
              },
              {
                "name": "Ш_1_О",
                "time": 0.25
              },
              {
                "name": "Ш_2_О",
                "time": 0.25
              }
            ]
          }
        ]
      }

      self.part_time = data['part_time']       # Get part_time constant
      self.departments = data['departments']   # Get departments info

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.mainloop()
