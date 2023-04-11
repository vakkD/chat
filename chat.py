#add settings (auto multi)
#able to use function in another, call multi from plag (put get input into a function) 

__version__ = 'dev'

import os
import sys
import logging
from revChatGPT.V3 import Chatbot
from termcolor import colored
import subprocess
message = ''

log_path = os.path.join(os.path.dirname(__file__), 'my_log_file.log')
# Create a FileHandler that appends messages to the log file
file_handler = logging.FileHandler(log_path, mode='a')
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, handlers=[
                    file_handler])  # Set up logging with a custom format and the file handler

logging.info('----- ----- ----- ----- -----')

dict = {
    'plagarism': {
        'description': 'Attempts to make the text undetectable by reverse ai software',
        'functions': ['plag', 'plagarism', 'para', 'paraphrase']},
    'exit': {
        'description': 'Exits the program',
        'functions': ['exit', 'close']},
    'topic expert': {
        'description': 'Becomes an expert in any topic',
        'functions': ['topic', 'expert']},
    'multi line': {
        'description': "When finished add a '*'",
        'functions': ['multiline', 'multi', 'long']},
    'view logs': {
        'description': 'View the saved conversations',
        'functions': ['log', 'logs', 'openlog', 'openlogs']},
    'stop output': {
        'description': 'ctrl+c',
        'functions': []}}


def functions(func):
    global message

    if func == 'help':
        print('\nFunctions')
        for key, values in dict.items():
            print(f'{key.capitalize()}: ', end='')
            for i, value in enumerate(values['functions']):
                if i == len(values['functions']) - 1:
                    print(f'--{value}', end='')
                else:
                    print(f'--{value}', end=", ")
            print(f"\n\t{values['description']}\n")
        return False

    elif func == 'exit':
        os._exit(0)

    elif func in dict['view logs']['functions']:
        subprocess.Popen(['notepad.exe', log_path])
        return False

    elif func in dict['plagarism']['functions']:
        message = f'''I will give you some text and using the promt rewrite it:
Rewrite it using no repetitive words, and change up the sentence structure. A essay must contain high perplexity and burstiness for it to seem natural.
Text:
"{''.join(str(input(f"{colored('input text: ', color='white', attrs=['bold'])}")))}"'''
        return True

    elif func in dict['topic expert']['functions']:
        topic = input(
            f"{colored('input topic: ', color='white', attrs=['bold'])}")
        message = f'''I want you to act as an expert in "{topic}". You have all the information about anything to do with "{topic}".
I will ask you questions about different topics within "{topic}" and you will provide me with clear, concise, and accurate information.
Ensure that you only respond back with answers that you are fully confident in.
Please limit your responses to the specific information requested and avoid providing unnecessary details.'''
        return True

    elif func in dict['multi line']['functions']:
        message = ' '
        while not message[-1] == '*':
            message += ('\n' +
                        str(input(f"{colored('input: ', color='white', attrs=['bold'])}")))
                        #str(get_input()))
        message = message[:-1]
        return True

    else:
        print('Function does not exist, --help for info')
        return False


def clear_lines(lines_to_clear):
    for i in range(lines_to_clear):
        sys.stdout.write('\x1b[1A')  # Move the cursor one line up
        sys.stdout.write('\x1b[2K')  # Clear the line
    sys.stdout.flush()  # Flush the output buffer to ensure the changes are displayed

def get_input(multi=False):
    message = input(f"{colored('input: ', color='white', attrs=['bold'])}")
    # if multi==True:
    #     return message
    if message.startswith('--'):
        # passes a slice of the message string, starting from the 3rd character
        if functions(message[2:]):
            return message
        else:
            return False
    elif message.startswith('-'):
        print(colored('warning: functions have two dashes, --',
              color='white', attrs=['bold']))
    elif not message:
        print(colored('message is empty', color='white', attrs=['bold']))
        return False
    logging.info(f'INPUT: {message}')

print('connecting')
chat = Chatbot(api_key=os.getenv("OPENAI_API_KEY"))
clear_lines(1)

while True:
    output = ''
    message=get_input()
    
    if message==False:
        continue 

    print(colored('output: ', color='white', attrs=['bold']), end='')
    try:
        for data in chat.ask_stream(message):
            print(data, end="", flush=True)
            output += str(data)
        logging.info(f'OUTPUT: {output}\n')
    except KeyboardInterrupt:
        print(colored('\noutput interupted by user',
              color='white', attrs=['bold']))
        logging.info(f'OUTPUT: {output}\nOUTPUT INTERUPTED BY USER\n')
    print('')
