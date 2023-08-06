import os, sys

# app.py is in this directory, so make sure that's available:
mypath = os.getcwd()
if mypath not in sys.path:
    sys.path.append(mypath)

from app import app as application
