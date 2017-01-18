END      = '\33[0m'
BOLD     = '\33[1m'
ITALIC   = '\33[3m'
URL      = '\33[4m'
BLINK    = '\33[5m'
BLINK2   = '\33[6m'
SELECTED = '\33[7m'

BLACK  = '\33[30m'
RED    = '\33[31m'
GREEN  = '\33[32m'
YELLOW = '\33[33m'
BLUE   = '\33[34m'
VIOLET = '\33[35m'
BEIGE  = '\33[36m'
WHITE  = '\33[37m'

BLACKBG  = '\33[40m'
REDBG    = '\33[41m'
GREENBG  = '\33[42m'
YELLOWBG = '\33[43m'
BLUEBG   = '\33[44m'
VIOLETBG = '\33[45m'
BEIGEBG  = '\33[46m'
WHITEBG  = '\33[47m'

GREY    = '\33[90m'
RED2    = '\33[91m'
GREEN2  = '\33[92m'
YELLOW2 = '\33[93m'
BLUE2   = '\33[94m'
VIOLET2 = '\33[95m'
BEIGE2  = '\33[96m'
WHITE2  = '\33[97m'

GREYBG    = '\33[100m'
REDBG2    = '\33[101m'
GREENBG2  = '\33[102m'

HEADING=VIOLET2
INFO=WHITE
WARNING=YELLOW
ERROR=RED

def print_heading(msg):
  print("{0}{1}{2}".format(HEADING, msg, END))

def print_warning(msg):
  print("{0}{1}{2}".format(WARNING, msg, END))

def print_info(msg):
  print("{0}{1}{2}".format(INFO, msg, END))

def print_error(msg):
  print("{0}{1}{2}".format(ERROR, msg, END))
