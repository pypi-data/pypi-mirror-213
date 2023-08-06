import math
import hashlib
import pytz
import requests
import os
from datetime import datetime
from tkinter import Tk, Label, Button


def out(value):
    print(value)


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

    def label(self, text="", x=0, y=0, width=100, height=30, bg="", fg=""):
        label = Label(self.root, text=text, bg=bg, fg=fg)
        label.place(x=x, y=y, width=width, height=height)
        self.elements.append(label)

    def button(self, text="", x=0, y=0, command=None):
        button = Button(self.root, text=text, command=command)
        button.place(x=x, y=y, width=100, height=30)
        self.elements.append(button)

    def run(self):
        self.root.mainloop()


