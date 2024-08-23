import sys
from enigma import EMPTY_STRING
from 
def main():

    path_dict = parse_command_to_dict(sys.argv)

    if path_dict['json'] == EMPTY_STRING or path_dict['in'] == EMPTY_STRING:
        print("The enigma script has encountered an error")
        exit(1)

    enigma_encrypter = load_enigma_from_path(path_dict['json'])
    encrypted_data = encrypt_file(path_dict['in'], enigma_encrypter)
    write_to_file(path_dict['out'], encrypted_data)