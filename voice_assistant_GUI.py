
import os
from PIL import Image
import customtkinter as ctk
import threading
import voice_assistant


class App(ctk.CTk):
    def __init__(self, app_version, sidebar_width):
        super().__init__()
        self.app_version = app_version
        self.sidebar_width = sidebar_width
        self.file_loaded = False
        self.file_extension = None
        # Stworzenie obiektu asystenta głosowego zaimportowanego z modułu "voice_assistant.py"
        self.apostrophe = ''
        self.voice_assistant = voice_assistant.Voice_assistant(self.apostrophe)
        self.photo_status = None

    def open_file(self, relative_path, x_postition, y_position, sf): # sf - scalling factor of image
        path = os.getcwd()
        path = path + relative_path
        try:
            image_file = Image.open(path)
            self.file_loaded = True
        except:
            pass
        if self.file_loaded:
            if image_file.size[0] >= image_file.size[1]:
                image_width = sf*(self.w_width - self.sidebar_width)
                image_height = image_file.size[1]/image_file.size[0]*image_width
            else:
                image_height = sf*self.w_height
                image_width = image_file.size[0]/image_file.size[1]*image_height
            image = ctk.CTkImage(light_image=image_file, size=(image_width, image_height))
            self.label = ctk.CTkLabel(master=self.main_frame, image=image, text='')
            self.label.place(relx=x_postition, rely=y_position, anchor=ctk.CENTER)

    def constant_listening(self):
        if not self.voice_assistant.end:
            if self.photo_status == 1:
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                self.open_file(r'\images\Dominika_2.png', 0.5, 0.45, 0.85)
                self.update()
                self.photo_status = 2
            elif self.photo_status == 2:
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                self.open_file(r'\images\Dominika_1.png', 0.5, 0.45, 0.85)
                self.update()
                self.photo_status = 1
            main_path = os.getcwd()
            try:
                path1 = main_path + r'\images\listening.png'
                image_file1 = Image.open(path1)
                image1 = ctk.CTkImage(light_image=image_file1, size=(150, 150))
                self.label_img = ctk.CTkLabel(master=self.sidebar_frame, image=image1, text='')
                self.label_img.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
                self.update()
            except:
                pass
            command = self.voice_assistant.listen()
            try:
                self.label_img.destroy()
                path2 = main_path + r'\images\processing.png'
                image_file2 = Image.open(path2)
                image2 = ctk.CTkImage(light_image=image_file2, size=(150, 150))
                self.label_img = ctk.CTkLabel(master=self.sidebar_frame, image=image2, text='')
                self.label_img.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
                self.update()
            except:
                pass
            self.voice_assistant.execute_command(command)
            list_length = len(self.voice_assistant.file_list_to_load)
            # lista współrzędnych położeń - musi być zgodna z listą "file_list_to_load" i trzeba to sprawdzić "ręcznie"
            cord_list = [(0.2, 0.15), (0.5, 0.15), (0.8, 0.15), (0.2, 0.45), (0.5, 0.45), (0.8, 0.45), (0.2, 0.75), (0.5, 0.75), (0.8, 0.75)]
            if list_length > 0:
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                try:
                    for number, item in enumerate(self.voice_assistant.file_list_to_load):
                        self.open_file(item, cord_list[number][0], cord_list[number][1], 0.2)
                except:
                    pass
                self.update()
                self.after(4000)
            # self.constant_listening()
            self.after(200, self.constant_listening)
        else:
            self.exit()

    def constant_listening_threading(self): # Ta funkcja umożliwia działenie funkcji "constant_listening" w tle, tak by nie zamrozić głównego okna
        threading.Thread(target=self.constant_listening, daemon=True).start()

    def exit(self):
        self.voice_assistant.end = True
        self.destroy()

    def create_window(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title(f'Voice assistant by Krystian Mistewicz ver. {app_version}')
        self.after(0, lambda: self.state('zoomed'))
        self.iconbitmap('icon.ico')
        # print(self.winfo_screenheight())
        # print(self.winfo_height())
        self.w_height = self.winfo_screenheight()/2 # screen height
        self.w_width = self.winfo_screenwidth()/2 # screen width
        # print(w_height)
        # print(w_width)
        self.sidebar_frame = ctk.CTkFrame(self, width=self.sidebar_width, height=self.w_height)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame = ctk.CTkFrame(self, width=self.w_width-self.sidebar_width, height=self.w_height, fg_color='gray90')
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.description_frame1 = ctk.CTkFrame(self.sidebar_frame, height=100, width=250)
        self.description_frame1.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        description_text1 = 'Jestem Dominika - Twoja\nasystentka głosowa'
        self.label_description1 = ctk.CTkLabel(master=self.description_frame1, text=description_text1, font=('Arial', 20, 'bold'), justify='center')
        self.label_description1.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.description_frame2 = ctk.CTkFrame(self.sidebar_frame, height=280, width=250)
        self.description_frame2.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        description_text2 = 'Ta asystentka głosowa:\n - puści/zagra\n   piosenkę na YT,\n - poda aktualny czas,\n - odpowie na pytanie,\n - wyszuka frazę\n   w Google,\n - pokaże obraz, \n - zakończy program.'
        self.label_description2 = ctk.CTkLabel(master=self.description_frame2, text=description_text2, font=('Arial', 20, 'bold'), justify='left')
        self.label_description2.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        # self.button_exit = ctk.CTkButton(master=self.sidebar_frame, text="Wyjście\nz programu", command=lambda:self.exit())
        # self.button_exit.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
        # Załadowanie obrazu
        self.open_file(r'\images\Dominika_1.png', 0.5, 0.45, 0.85)
        self.photo_status = 1
        # Wywołanie powitania
        self.after(1000, self.voice_assistant.talk, 'Z tej strony Dominika. Co mogę dla Ciebie zrobić?')
        self.after(1100, self.constant_listening_threading)
        self.mainloop()


if __name__ == '__main__':
    app_version = 2.2
    sidebar_width = 300
    app = App(app_version, sidebar_width)
    app.create_window()
