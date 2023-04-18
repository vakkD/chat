# complete settings functions

# MULTIPLE CHOICE
# throughout the session, i will give you a series of multiple-choice questions. you will respond with the answer only, no description. do you understand?

# auto update

# make chat not continue last request when cancel output
import configparser
import io
from tqdm import tqdm
import subprocess
from termcolor import colored, cprint
from revChatGPT.V3 import Chatbot
import logging
import sys
import os
from itertools import cycle
import threading
import time

__version__ = "dev"

clear = lambda: os.system("cls")

message = ""

log_path = os.path.join(os.path.dirname(__file__), "log.log")
# Create a FileHandler that appends messages to the log file
file_handler = logging.FileHandler(log_path, mode="a")
logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, handlers=[file_handler]
)  # Set up logging with a custom format and the file handler

# region settings
default_settings = {"stream": True, "auto multi": False, "auto update": False}
if not os.path.exists("config.ini"):
    config = configparser.ConfigParser()
    config["settings"] = default_settings
    with open("config.ini", "w") as configfile:
        config.write(configfile)

config = configparser.ConfigParser()
config.read("config.ini")

settings = {}
for key, value in default_settings.items():
    settings[key] = config.getboolean("settings", key, fallback=value)
# endregion settings

logging.info("----- ----- ----- ----- -----")

dict = {
    "plagarism": {
        "description": "Attempts to make the text undetectable by reverse ai software",
        "functions": ["plag", "plagarism", "para", "paraphrase"],
    },
    "exit": {"description": "Exits the program", "functions": ["exit", "close"]},
    "topic expert": {
        "description": "Becomes an expert in any topic",
        "functions": ["topic", "expert"],
    },
    "multi line": {
        "description": "Allows input of multiple lines, when finished add a '*'",
        "functions": ["multiline", "multi", "long"],
    },
    "multiple choice": {
        "description": "Answers in the format of multiple choice, auto multi line, finish with --end",
        "functions": ["multiple", "choice"],
    },
    "view logs": {
        "description": "View the saved conversations",
        "functions": ["log", "logs", "openlog", "openlogs"],
    },
    "new session": {
        "description": "Clears the current session and starts new",
        "functions": ["session", "clear"],
    },
    "settings menu": {
        "description": "Open the settings menu",
        "functions": ["settings", "setting", "options"],
    },
    "stop output": {"description": "ctrl+c", "functions": []},
}


class Spinner:
    __default_spinner_symbols_list = [
        "|-----|",
        "|#----|",
        "|-#---|",
        "|--#--|",
        "|---#-|",
        "|----#|",
    ]

    def __init__(self, spinner_symbols_list: [str] = None):
        spinner_symbols_list = (
            spinner_symbols_list
            if spinner_symbols_list
            else Spinner.__default_spinner_symbols_list
        )
        self.__screen_lock = threading.Event()
        self.__spinner = cycle(spinner_symbols_list)
        self.__stop_event = False
        self.__thread = None

    def get_spin(self):
        return self.__spinner

    def start(self, spinner_message: str):
        self.__stop_event = False
        time.sleep(0.1)

        def run_spinner(message):
            while not self.__stop_event:
                print(
                    "\r{message} {spinner}".format(
                        message=message, spinner=next(self.__spinner)
                    ),
                    end="",
                )
                time.sleep(0.1)

            self.__screen_lock.set()

        self.__thread = threading.Thread(
            target=run_spinner, args=(spinner_message,), daemon=True
        )
        self.__thread.start()

    def stop(self):
        self.__stop_event = True
        if self.__screen_lock.is_set():
            self.__screen_lock.wait()
            self.__screen_lock.clear()
            print("\r", end="")

        print("\r", end="")


def get_input(function=None):
    cprint("input: ", "red", attrs=["bold"], end="")
    message = input()
    if not function == None:
        pass
    if message.startswith("--"):
        # passes a slice of the message string, starting from the 3rd character
        message = functions(message[2:])
        if not message == False:
            return message
        else:
            return False
    elif message.startswith("-"):
        cprint(
            "warning: functions have two dashes, --", "white", "on_red", attrs=["bold"]
        )
    elif not message:
        colored("message is empty", "white", "on_red", attrs=["bold"])
        return False
    logging.info(f"INPUT: {message}")
    return message


def settings_menu():
    while True:
        print("Settings Menu")
        print("-------------")
        for key, value in settings.items():
            print(f"{key.capitalize()}: {value}")
        print("-------------")
        setting = input(
            "Enter the name of the setting you want to modify, or 'exit' to return to the chat: "
        ).lower()
        if setting == "exit":
            clear()
            break
        elif setting not in settings:
            clear()
            print("Invalid setting name. Please try again.")
            continue
        else:
            print(f"Current value of {setting.capitalize()}: {settings[setting]}")
            toggle = input("Do you want to toggle this setting? (y/n) ").lower()
            if toggle == "y":
                settings[setting] = not settings[setting]
                print(f"{setting.capitalize()} set to {settings[setting]}")
                config = configparser.ConfigParser()
                config.read("config.ini")
                config.set("settings", setting, str(settings[setting]))
                with open("config.ini", "w") as configfile:
                    config.write(configfile)
            else:
                print("Setting not changed.")
        clear()


def functions(func):
    global message
    global chat
    func = func.lower()

    if func == "help":
        print("\nFunctions")
        for key, values in dict.items():
            print(f"{key.capitalize()}: ", end="")
            for i, value in enumerate(values["functions"]):
                if i == len(values["functions"]) - 1:
                    print(f"--{value}", end="")
                else:
                    print(f"--{value}", end=", ")
            print(f"\n\t{values['description']}\n")
        return False

    elif func == "exit":
        os._exit(0)

    elif func in dict["settings menu"]["functions"]:
        settings_menu()
        # print("in development")
        return False

    elif func in dict["view logs"]["functions"]:
        subprocess.Popen(["notepad.exe", log_path])
        return False

    elif func in dict["plagarism"]["functions"]:
        message = get_input()
        spinner.start("generating response")
        chat.ask(
            "I'm going to give you some information before asking you to write an article. Do you understand?"
        )
        chat.ask(
            """When it comes to writing content, two factors are crucial, "perplexity" and "burstiness." Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with great burstiness, for example, with some longer or complex sentences alongside shorter sentences. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness. Do you understand?"""
        )
        chat.ask(
            f'''using the concepts written previously, rewrite this article with a high degree of perplexity and burstiness:"{''.join(str(message))}"'''
        )
        spinner.stop()
        return "Rewrite this article changing 50% of nouns and verbs for similar ones and rewrite verb usages to add natural sounding variations in complexity but retain the same tense and overall meaning."

    elif func in dict["multiple choice"]["functions"]:
        print("in development")
        return False
        chat.ask(
            "throughout the session, i will give you a series of multiple-choice questions. you will respond with the answer only, no description. do you understand?"
        )
        message = get_input()
        while not message.startswith("--"):
            pass
        if message.replace("--", ""):
            return False

    elif func in dict["topic expert"]["functions"]:
        topic = get_input()
        message = f"""I want you to act as an expert in "{topic}". You have all the information about anything to do with "{topic}".\nI will ask you questions about different topics within "{topic}" and you will provide me with clear, concise, and accurate information.\nEnsure that you only respond back with answers that you are fully confident in.\nPlease limit your responses to the specific information requested and avoid providing unnecessary details."""
        return message

    elif func in dict["multi line"]["functions"]:
        message = " "
        while not message[-1] == "*":
            message += "\n" + str(get_input())
        return message[:-1]

    elif func in dict["new session"]["functions"]:
        logging.info("----- ----- ----- ----- -----")
        cprint("starting new session", "white", "on_red", attrs=["bold"])
        chat = Chatbot(api_key=os.getenv("OPENAI_API_KEY"))
        return False

    else:
        cprint(
            "Function does not exist, --help for info",
            "white",
            "on_red",
            attrs=["bold"],
        )
        return False


def clear_lines(lines_to_clear):
    for i in range(lines_to_clear):
        sys.stdout.write("\x1b[1A")  # Move the cursor one line up
        sys.stdout.write("\x1b[2K")  # Clear the line
    sys.stdout.flush()  # Flush the output buffer to ensure the changes are displayed


print("connecting")
chat = Chatbot(api_key=os.getenv("OPENAI_API_KEY"))
clear_lines(1)
spinner = Spinner()

while True:
    try:
        output = ""
        message = get_input()

        if message == False:
            continue
    except KeyboardInterrupt:
        cprint("\nuse --exit to close", "white", "on_red", attrs=["bold"])
        continue

    try:
        if settings["stream"] == True:
            cprint("output: ", "red", attrs=["bold"], end="")
            for data in chat.ask_stream(message):
                print(data, end="", flush=True)
                output += str(data)
        else:
            spinner.start("generating response")
            reponse = chat.ask(message)
            output += str(reponse)
            spinner.stop()
            cprint("output: ", "red", attrs=["bold"], end="")
            print(reponse)
        print("")
        logging.info(f"OUTPUT: {output}\n")
    except KeyboardInterrupt:
        cprint("\noutput interupted by user", "white", "on_red", attrs=["bold"])
        logging.info(f"OUTPUT: {output}\nOUTPUT INTERUPTED BY USER\n")
