import tkinter as tk
import cv2
import os
import subprocess
import datetime
from PIL import Image, ImageTk
import Utilities


class App:
    # Creating the main window
    def __init__(self):
        self.main_window = tk.Tk()
        # Create the window's geometry
        self.main_window.geometry("1200x520+350+100")
        
        # Create login button on main window
        self.login_button_main_window = Utilities.get_button(self.main_window, "Login", "green", self.login)
        # Placing the button on the main window
        self.login_button_main_window.place(x=750, y=300)
        
        # Create Register button on main window
        self.register_new_user_button_main_window = Utilities.get_button(self.main_window, "Register", "gray",
                                                                         self.register_new_user, fg="black")
        # Placing the button on the main window 
        self.register_new_user_button_main_window.place(x=750, y=400)
        
        # Creating webcam label
        self.webcam_label = Utilities.get_img_label(self.main_window)
        # Placing the webcam label on the main window
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        # 
        self.add_webcam(self.webcam_label)
        
        # Create a database directory to store saved images
        self.db_dir = "./db"
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
            
        # Create a path file to log all users
        self.log_path = "./log.txt"
        
    # Specifying the add webcam function
    def add_webcam(self, label):
        if "cap" not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            
        self._label = label
        
        self.process_webcam()
     
    # Specifying the webcam function to establish parameters   
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        
        self.most_recent_capture_pil = Image.fromarray(img_)
        
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)
        
    # Specifying the login funciton
    def login(self):
        unknown_img_path = "./.tmp.jpg"
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        
        output = str(subprocess.check_output(["face_recognition", self.db_dir, unknown_img_path]))
        name = output.split(",")[1][:-3]
        
        # Create pop up message for error or successful login
        if name in ["unkown_person", "no_persons_found"]:
            Utilities.msg_box("Error, please register new account or try again")
        else:
            Utilities.msg_box("Welcome!", "Welcome, {}.".format(name))
            with open(self.log_path, "a") as f:
                # Initialise the log pathway to ensure all users log in name and times are stored
                f.write("{}, {}\n".format(name, datetime.datetime.now()))
                f.close()
        
        os.remove(unknown_img_path)
    
    # Creating the register new user window
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        # Create the window's geometry
        self.register_new_user_window.geometry("1200x520+370+120")
        
        # Create register new user button on the register new user window
        self.accept_button_register_new_user_window = Utilities.get_button(self.register_new_user_window, "Register", "green", self.accept_register_new_user)
        # Placing the button on the register new user window
        self.accept_button_register_new_user_window.place(x=750, y=300)
        
        # Create try again button on the register new user window
        self.try_again_button_register_new_user_window = Utilities.get_button(self.register_new_user_window, "Try Again", "red", self.try_again_new_user)
        # Placing the button on the register new user window
        self.try_again_button_register_new_user_window.place(x=750, y=400)
        
        # Creating webcam label to capture new user
        self.capture_label = Utilities.get_img_label(self.register_new_user_window)
        # Placing the webcam label on the register new user window
        self.capture_label.place(x=10, y=0, width=700, height=500)
        
        # Add a single image
        self.add_img_to_label(self.capture_label)
        
        # Create username input
        self.entry_text_register_new_user = Utilities.get_entry_text(self.register_new_user_window)
        # Placing the username input
        self.entry_text_register_new_user.place(x=750, y=150)
        # Create label for the username input
        self.text_label_register_new_user = Utilities.get_text_label(self.register_new_user_window, "Create your username")
        # Place the label for the input
        self.text_label_register_new_user.place(x=750, y=70)
        
    # Specifying the try again function so the button returns to main window
    def try_again_new_user(self):
        self.register_new_user_window.destroy()
        
    # Specifying the single image function
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()


    # Start function to run app
    def start(self):
        self.main_window.mainloop()
        
    # Specifying the register new user function
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        
        # Save captured images onto database
        cv2.imwrite(os.path.join(self.db_dir, "{}.jpg".format(name)), self.register_new_user_capture)
        
        # Create account created successfully message
        Utilities.msg_box("Welcome", "You have created your account")
        self.register_new_user_window.destroy()
    
    
if __name__ == "__main__":
    app = App()
    app.start()