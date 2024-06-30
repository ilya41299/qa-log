import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option(
    "-l",
    "--logs",
    dest="filepath",
    help="file or directory with log files",
    default="./logs",
)
(options, args) = parser.parse_args()

if os.path.isdir(options.filepath):
    files = os.listdir(options.filepath)
elif os.path.isfile(options.filepath):
    files = [options.filepath]
else:
    raise AssertionError(f"Path doesn't exist: {options.filepath}")
