import argparse
import logging
import os
import sys

import agentes.othello
parser = argparse.ArgumentParser(description='Agentes - IA.')
parser.add_argument('--log', action='store_true', help='Ninguna...')

from agentes.sub.othello import othello
othello.main()
