import os, sys

f = os.path.realpath(__file__)
f = f[0:os.path.realpath(__file__).rfind("\\")+1] + "GameFiles"
sys.path.insert(1, f)

import GameLoop
