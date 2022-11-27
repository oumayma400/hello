from robot.api import logger
from robot.output import librarylogger
import datetime

def log(text, msg, level):
    librarylogger.write(msg, level, False)
    with open('log.log', 'a') as f:
        print(f'{datetime.datetime.now()}   {level}    {text} {msg}', file=f)
