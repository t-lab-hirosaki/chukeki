import sys
import os
import re

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
#filename = 'lora_profile'
ERR_MSG = {
    'INVALID_ARGS': "Invalid arguments\n",
    'FILE_NOT_FOUND': "No such file or directory\n",
}

def read(filename):
    check_args(filename)
    with open(filename, "r") as f:
        match_pattern = r'^\s*(#.*|)$'
        line = f.readline()
        data = {}
        while line:
            match = re.match(match_pattern, line)
            if not match:

                key, value = line.split("=")

                try:
                    data[key]=int(value.strip())
                except Exception as e:
                    data[key]=value.strip()


                #print(line, end="")
            line = f.readline()

    # print(data.keys())
    # print(data.values())
    # return EXIT_SUCCESS
    return data

def check_args(filename):
    if not os.path.isfile(filename):
        sys.stderr.write(filename + ": " + ERR_MSG['FILE_NOT_FOUND'])
        sys.exit(EXIT_FAILURE)

if __name__ == '__main__':
    read()
