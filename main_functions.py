from enigma import Enigma, EMPTY_STRING, JSONFileError
import json

# ================================================================================================

"""
Usage: Exract an Enigma object variables and create an Enigma object

Params: 
      path to an in file

Returns:
      Enigma - an enigma mechine object
"""


def load_enigma_from_path(path: str): 
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except Exception:
        raise JSONFileError() # JSON file loading unseccessful

    return Enigma(data['hash_map'], data['wheels'], reflector_map = data['reflector_map'])

# ================================================================================================
"""
Usage: Parse an input file and feed it to the enigma machine

Params:
      str: in file path
      Enigma: an Enigma machinge instance

Returns:
      string: the encrypted text of the in file 
    """


def encrypt_file(in_file_path: str, enigma_encrypter: Enigma):

    try:
        encrypted_file_text = EMPTY_STRING
        with open(in_file_path, 'r') as in_file:
            line = in_file.readline() # use readline() because a \n symbolizes end of message in our main
            while line:
                encrypted_file_text += enigma_encrypter.encrypt_message(line) #encrypt each line and append to string
                line = in_file.readline() # read next line
            return encrypted_file_text 
        
    except Exception:
        print("The enigma script has encountered an error") # input file read failed
        exit(1)

# ================================================================================================
"""
Usage: Parse a CMD command in to a dictionary

Params:
  list commant: a command to parse

Returns:
  dict args_dict: a dictionary with file extentions as keys and and file paths as values
"""


def parse_command_to_dict(command: list):
    
    args_dict = {} # crate an empty dictionary

    # Parsing the command by flags associated
    skip_next = False  # Flag to skip the next iteration when needed
    for i in range(len(command)):
        if i == 0:
            continue

        if skip_next:
            skip_next = False 
            continue

        if command[i] == '-c':
            args_dict['json'] = command[i + 1] # a json file comes after -c flag
            skip_next = True # skip the json file argument
        elif command[i] == '-i': 
            args_dict['in'] = command[i + 1] # an input file comes after -i flag
            skip_next = True # skip the input file argument
        elif command[i] == '-o':
            args_dict['out'] = command[i + 1] # an output file comes after -o flag
            skip_next = True # skip the json file argument

    return args_dict

# ================================================================================================
"""
Usage: write a string to a file 

Params:
      string output_file_path: a path to the file we wish to write to
      string data: the data we want to write

Returns:
      void
"""


def write_to_file(output_file_path, data):
    try:
        with open(output_file_path, 'w') as out_file:
            out_file.write(data)

    except Exception:
        print("The enigma script has encountered an error") # Error opening\writing to the output file
        exit(1)


