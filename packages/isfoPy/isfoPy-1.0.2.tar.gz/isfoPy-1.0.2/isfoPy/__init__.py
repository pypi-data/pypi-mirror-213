import math
import hashlib
import pytz
import requests
import os
from datetime import datetime
from tkinter import *
import re
import shutil
import random
import string
from pytube import YouTube


def out(*args):
    result = ""
    for value in args:
        result += str(value) + " "
    print(result.strip())


def sub1(value):
    return value - 1


def add1(value):
    return value + 1


def add(value, number):
    return value + number


def sub(value, number):
    return value - number


def mul(value, number):
    return value * number


def div(value, number):
    return value / number


def sq(value):
    return value * value


def sqRoot(value):
    return math.sqrt(value)


def quot(value, number):
    return value % number


def power(value, exponent):
    return value ** exponent


def factorial(value):
    return math.factorial(value)


def logarithm(value, base=math.e):
    return math.log(value, base)


def sin(value):
    return math.sin(value)


def cos(value):
    return math.cos(value)


def tan(value):
    return math.tan(value)


def ceil(value):
    return math.ceil(value)


def floor(value):
    return math.floor(value)


def hashValue(value):
    hashed_value = hashlib.sha256(value.encode()).hexdigest()
    return hashed_value


def getCurrentTime(timezone_code=None, time_format='24'):
    if timezone_code:
        try:
            timezone = pytz.timezone(timezone_code)
            current_time = datetime.now(timezone)
            if time_format == '12':
                formatted_time = current_time.strftime('%Y-%m-%d %I:%M:%S %p')
            else:
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_time
        except pytz.UnknownTimeZoneError:
            return "Unknown timezone code."
    else:
        current_time = datetime.now()
        if time_format == '12':
            formatted_time = current_time.strftime('%Y-%m-%d %I:%M:%S %p')
        else:
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time


def getCurrentDate():
    current_date = datetime.date.today()
    return current_date


def downloadFile(url, output):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            output_path = os.path.join(output, filename)
            with open(output_path, 'wb') as file:
                file.write(response.content)
            return f"Downloaded file saved as: {output_path}"
        else:
            return "Failed to download the file."
    except requests.RequestException:
        return "An error occurred during the download process."


def validateEmail(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


def validateURL(url):
    pattern = r'^(http|https)://[\w\.-]+\.\w+$'
    if re.match(pattern, url):
        return True
    else:
        return False


def validatePhoneNumber(phone_number):
    pattern = r'^\d{10}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False


def validateUsername(username):
    pattern = r'^[a-zA-Z0-9_-]{3,16}$'
    if re.match(pattern, username):
        return True
    else:
        return False


def createDirectory(directory_path):
    try:
        os.mkdir(directory_path)
        return f"Directory created: {directory_path}"
    except FileExistsError:
        return f"Directory already exists: {directory_path}"
    except Exception as e:
        return f"Failed to create directory: {str(e)}"


def deleteFile(file_path):
    try:
        os.remove(file_path)
        return f"File deleted: {file_path}"
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Failed to delete file: {str(e)}"


def renameFile(file_path, new_name):
    try:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_name)
        os.rename(file_path, new_file_path)
        return f"File renamed to: {new_file_path}"
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Failed to rename file: {str(e)}"


def copyFile(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        return f"File copied to: {destination_path}"
    except FileNotFoundError:
        return f"File not found: {source_path}"
    except Exception as e:
        return f"Failed to copy file: {str(e)}"


def moveFile(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        return f"File moved to: {destination_path}"
    except FileNotFoundError:
        return f"File not found: {source_path}"
    except Exception as e:
        return f"Failed to move file: {str(e)}"


def reverseString(string):
    return string[::-1]


def countOccurrences(string, substring):
    return string.count(substring)


def removeWhitespace(string):
    return "".join(string.split())


def capitalize(string):
    return " ".join(word.capitalize() for word in string.split())


def generateRandomInt(min_val, max_val):
    return random.randint(min_val, max_val)


def generateRandomPassword(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


class GUIApplication:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.elements = []

    def label(self, text="", x=0, y=0, width=100, height=30, bg="", fg="", font="", anchor="", justify="", relief="", borderwidth=0, padx=0, pady=0, wraplength=0, image=None, compound=None):
        label = Label(self.root, text=text, bg=bg, fg=fg, font=font, width=width, height=height, anchor=anchor, justify=justify, relief=relief, borderwidth=borderwidth, padx=padx, pady=pady, wraplength=wraplength, image=image, compound=compound)
        label.place(x=x, y=y)
        self.elements.append(label)

    def button(self, text="", x=0, y=0, command=None, bg="", fg="", font="", width=100, height=30, relief="", borderwidth=0, padx=0, pady=0, image=None, compound=None):
        button = Button(self.root, text=text, command=command, bg=bg, fg=fg, font=font, width=width, height=height, relief=relief, borderwidth=borderwidth, padx=padx, pady=pady, image=image, compound=compound)
        button.place(x=x, y=y)
        self.elements.append(button)

    def entry(self, x=0, y=0, width=100, textvariable=None, show="", font="", relief="", borderwidth=0, padx=0, pady=0):
        entry = Entry(self.root, width=width, textvariable=textvariable, show=show, font=font, relief=relief, borderwidth=borderwidth, padx=padx, pady=pady)
        entry.place(x=x, y=y)
        self.elements.append(entry)

    def text(self, x=0, y=0, width=100, height=10, font="", relief="", borderwidth=0, padx=0, pady=0):
        text = Text(self.root, width=width, height=height, font=font, relief=relief, borderwidth=borderwidth, padx=padx, pady=pady)
        text.place(x=x, y=y)
        self.elements.append(text)

    def checkbutton(self, text="", x=0, y=0, variable=None, onvalue=1, offvalue=0, bg="", fg="", font="", width=100, height=30, padx=0, pady=0):
        checkbutton = Checkbutton(self.root, text=text, variable=variable, onvalue=onvalue, offvalue=offvalue, bg=bg, fg=fg, font=font, width=width, height=height, padx=padx, pady=pady)
        checkbutton.place(x=x, y=y)
        self.elements.append(checkbutton)

    def radiobutton(self, text="", x=0, y=0, variable=None, value=None, bg="", fg="", font="", width=100, height=30, padx=0, pady=0):
        radiobutton = Radiobutton(self.root, text=text, variable=variable, value=value, bg=bg, fg=fg, font=font, width=width, height=height, padx=padx, pady=pady)
        radiobutton.place(x=x, y=y)
        self.elements.append(radiobutton)

    def scale(self, x=0, y=0, from_=0, to=100, variable=None, resolution=1, orient="horizontal", length=200, width=10, sliderlength=20, showvalue=True, bg="", fg="", font=""):
        scale = Scale(self.root, from_=from_, to=to, variable=variable, resolution=resolution, orient=orient, length=length, width=width, sliderlength=sliderlength, showvalue=showvalue, bg=bg, fg=fg, font=font)
        scale.place(x=x, y=y)
        self.elements.append(scale)

    def listbox(self, x=0, y=0, width=100, height=10, font="", selectmode="browse", bg="", fg=""):
        listbox = Listbox(self.root, width=width, height=height, font=font, selectmode=selectmode, bg=bg, fg=fg)
        listbox.place(x=x, y=y)
        self.elements.append(listbox)

    def spinbox(self, x=0, y=0, from_=0, to=100, increment=1, textvariable=None, width=10, font=""):
        spinbox = Spinbox(self.root, from_=from_, to=to, increment=increment, textvariable=textvariable, width=width, font=font)
        spinbox.place(x=x, y=y)
        self.elements.append(spinbox)

    def scrollbar(self, x=0, y=0, orient="vertical"):
        scrollbar = Scrollbar(self.root, orient=orient)
        scrollbar.place(x=x, y=y)
        self.elements.append(scrollbar)

    def canvas(self, x=0, y=0, width=100, height=100, bg="", bd=0, relief="", highlightthickness=0):
        canvas = Canvas(self.root, width=width, height=height, bg=bg, bd=bd, relief=relief, highlightthickness=highlightthickness)
        canvas.place(x=x, y=y)
        self.elements.append(canvas)

    def menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        return menu

    def frame(self, x=0, y=0, width=100, height=100, bg="", bd=0, relief="", highlightthickness=0):
        frame = Frame(self.root, width=width, height=height, bg=bg, bd=bd, relief=relief, highlightthickness=highlightthickness)
        frame.place(x=x, y=y)
        self.elements.append(frame)

    def run(self):
        self.root.mainloop()


def downloadYT(link="", resolution="144p-2440p/mp3", output="output directory", type=".mp4"):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output, exist_ok=True)

        # Set the resolution and file extension based on user input
        res_map = {
            "144p": "144p",
            "240p": "240p",
            "360p": "360p",
            "480p": "480p",
            "720p": "720p",
            "1080p": "1080p",
            "1440p": "1440p",
            "2440p": "2440p",
            "mp3": "mp3"
        }
        resolution = resolution.lower()
        if resolution not in res_map:
            print("Invalid resolution. Please choose from: ", ", ".join(res_map.keys()))
            return
        if resolution == "mp3":
            type = ".mp3"
        else:
            type = ".mp4"

        # Download the YouTube video
        yt = YouTube(link)
        stream = yt.streams.get_by_resolution(res_map[resolution])
        if stream is None:
            print("Resolution not available for this video.")
            return
        filename = f"{yt.title}{type}"
        filepath = os.path.join(output, filename)
        stream.download(output_path=output, filename=filename)

        print("Download complete. Video saved as:", filepath)
    except Exception as e:
        print("Error:", e)