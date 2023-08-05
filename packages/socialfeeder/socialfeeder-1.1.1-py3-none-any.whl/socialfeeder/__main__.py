import argparse
import sys
from socialfeeder import feeder, __VERSION__
from socialfeeder.utilities.constants import FEEDER_FACEBOOK

def main():
    parser = argparse.ArgumentParser(prog='feeder')
    parser.add_argument('-v','--version', action='version', version='%(prog)s ' + __VERSION__)

    parser.add_argument('--social', help='Social network name', type=str, default=FEEDER_FACEBOOK)
    parser.add_argument('--config', help='Configuration file path (.xml)', type=str)
    parser.add_argument('--head',   help='Headless mode', action='store_false')

    args = parser.parse_args()
    feeder.run( social      = args.social,
                config      = args.config,
                headless    = args.head)

if __name__ == '__main__':
    main()