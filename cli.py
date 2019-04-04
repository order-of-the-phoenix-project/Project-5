"""cli.py
    Usage:
        cli.py add <x> <y>
        cli.py subtract <x> <y>
        cli.py factorial <x>
        cli.py fibonacci <x>
        cli.py is-prime <x>
        cli.py slack-alert <string>
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
    if args['factorial']:
        num = int(args['<x>'])
        try:
            use = int(num)
            total = int(num)
            for i in range(1, int(num) - 1):
                use -= 1
                total = total * use
            print(int(num), total)
        #return str(total)
        except ValueError:
            print(num, "Input is not a positive integer")

       
    
if __name__ == "__main__":
    
    run()
