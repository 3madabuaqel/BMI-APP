import customtkinter as ctk 
from setting import *
import tkinter as tk
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass



class App(ctk.CTk):
    def __init__(self):
        
        #window setup 
        super().__init__(fg_color=GREEN)
        self.title('')
        self.iconbitmap("empty.ico")
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()
        
        # layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')
        
        # data
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()
        
        # tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)
        
        
        # widget
        ResultText(self, self.bmi_string)
        WeightInput(self, self.weight_float)
        HeighInput(self, self.height_int)
        UnitSwitcher(self)
        
        self.mainloop()
        
    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weigh_kg = self.weight_float.get()
        bmi_result = round(weigh_kg / height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)
        
    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND,DWMWA_ATTRIBUTE,byref(c_int(COLOR)),sizeof(c_int))
        except:
            pass

class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight='bold')
        
        super().__init__(master=parent, text='22.5', font=font, text_color=WHITE, textvariable=bmi_string)
        
        self.grid(column= 0,row=0,rowspan=2,sticky='news')

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float):
        
        super().__init__(master=parent, fg_color=WHITE)
        
        self.grid(column=0, row=2, sticky='nsew', padx=10,pady=15)
        
        self.weight_float = weight_float
        
        self.outputstring = ctk.StringVar()
        self.update_weight()
        
        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')
        
        # widgets
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        lable = ctk.CTkLabel(self, text='70kg', text_color=BLACK, font=font, textvariable=self.outputstring)
        lable.grid(row=0, column=2)
        
        # buttons
        minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)
        
        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)
        
        pluss_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        pluss_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)
        
        small_pluss_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_pluss_button.grid(row=0, column=3, padx=4, pady=4)
        
    def update_weight(self, info = None):
        if info:
            amount = 1 if info[1] == 'large' else 0.1
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        self.outputstring.set(f'{round(self.weight_float.get(), 1)}kg')

class HeighInput(ctk.CTkFrame):
    def __init__(self, parent, heighy_int):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
        #widgets
        slider = ctk.CTkSlider(
            master=self,
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=GREEN,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
            variable=heighy_int,
            from_ = 100, to =250
        )
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)
        
        self.output_string = ctk.StringVar()
        self.update_text(heighy_int.get())
        
        output_text = ctk.CTkLabel(self, text='1.80',textvariable=self.output_string , text_color=BLACK, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        output_text.pack(side='left', padx=20)
        
    def update_text(self, amount):
        text_string = str(int(amount))
        meter = text_string[0]
        cm = text_string[1:]
        self.output_string.set(f'{meter}.{cm}m')
        

class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent):
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold')
        
        super().__init__(master=parent, text="metric", font=font ,text_color=DARK_GREEN)
        
        self.place(relx=0.98,rely=0.01, anchor='ne')




if __name__ == '__main__':
    App()