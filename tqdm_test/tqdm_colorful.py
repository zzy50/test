import time
import sys
from tqdm import trange
from IPython.display import clear_output
import random
from colorama import Fore
import logging 
import logging.handlers

log = logging.getLogger('sr_log')
log.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('./log.txt' , mode= "w")
log.addHandler(fileHandler)

# Cross-platform colored terminal text.
color_bars = [
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE]

def do_something():
    time.sleep(1)

def do_another_something():
    time.sleep(0.1)

bar_format="{l_bar}%s{bar}%s{r_bar}" % (color_bars[2], Fore.RESET)

for i in trange(10 , file=sys.stdout, unit_scale=True , leave= True , 
                desc='outer loop' , bar_format = bar_format):
    do_something()
    form = random.sample(color_bars , 1 )[0]
    bar_format="{l_bar}%s{bar}%s{r_bar}" % (form, Fore.RESET)
    for j in trange(10,file=sys.stdout, leave= False , bar_format = bar_format , 
                    unit_scale=True, desc='inner loop'):
        do_another_something()
        if (j % 50 == 0) & (j>0) :
            log.info("hp")