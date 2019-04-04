"""cli.py
    Usage:
        cli.py add <x> <y>
        cli.py subtract <x> <y>
"""

# import docopt (remember to install)
from docopt import docopt
def run():
    # Make a dictionary from the arguments
    args = docopt(__doc__, version="0.1.0")
    if args['add']:
        x = float(args['<x>'])
        y = float(args['<y>'])
        print(x+y)
    if args['subtract']:
        x = float(args['<x>'])
        y = float(args['<y>'])
        print(x-y)        
    
if __name__ == "__main__":
    
    run()
