
from json_file_error import JSONFileError
from main import *

#Constents
FIRST_WHEEL_MAX = 8
ABC_SIZE = 26
FIRST_WHEEL = 0
SECOND_WHEEL = 1
SECOND_WHEEL_MODULO_2 = 2
THIRD_WHEEL = 2
THIRD_WHEEL_MAX = 10
THIRD_WHEEL_MID = 5
THIRD_WHEEL_MIN = 0
THIRD_WHEEL_MODULO_10 = 10
THIRD_WHEEL_MODULO_3 = 3
EMPTY_STRING = ''

#Enigma Class
class Enigma:

    """
    Constructor

    Params:  
        dict hash_map: an encryption hash map 
        list wheels: values for the three wheels
        dict reflector_map: an encryption reflector map       
    """
    def __init__(self, hash_map: dict, wheels: list, reflector_map: dict):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map
   
    #==============================================================================================
    
    """
    Method Usage: Rotate the wheels based on given conditions
    
    Params: 
            int encrypted_char_count: number of already encrypted charecters
            list wheels: wheels to encrypt by 
    
    Returns:
            void
    """
     

    def rotate_wheels(self, encrypted_char_count, wheels):
        wheels[FIRST_WHEEL] += 1
        if wheels[FIRST_WHEEL] > FIRST_WHEEL_MAX: # If wheel_1 one is over 8, set it to 1
            wheels[FIRST_WHEEL] = 1

        if encrypted_char_count % SECOND_WHEEL_MODULO_2 == 0: 
            wheels[SECOND_WHEEL] *= 2 # If encrypted char count is even, multiply wheel_2 by 2
        else:
            wheels[SECOND_WHEEL] -= 1 # Else, decrease wheel_2 by 1

        if encrypted_char_count % THIRD_WHEEL_MODULO_10 == 0:  
            wheels[THIRD_WHEEL] = THIRD_WHEEL_MAX # If wheel_3 is divisible by 10, set it to 10
        elif encrypted_char_count % THIRD_WHEEL_MODULO_3 == 0:
            wheels[THIRD_WHEEL] = THIRD_WHEEL_MID # Elif wheel_3 is divisible by 3, set it to 5
        else:
            wheels[THIRD_WHEEL] = THIRD_WHEEL_MIN # Else, not divisible by 10 or 3, set it to 0

    #==============================================================================================
    
    """
    Method Usage: Reverse search hash_map dictionary, give a key and get value

    Params:
            str value: a value to find the key to

    Returns:
            str map_key: the correspending key for the value
    """


    def find_key_in_map(self, value: str):
        for map_key, map_value in self.hash_map.items():
            if map_value == value:
                return map_key
        raise JSONFileError() # If here, the given key was not found in hash_map, and the JSON file invalid

    #==============================================================================================

    """
    Method Usage: Encrypt a string message
    
    Parsms:
            str message: a message to encrypt
    Returns
            str encrypted_string: the enceypted message
    
    """


    def encrypt_message(self, message: str):
        encrypted_string = EMPTY_STRING # Initializing empty encrypyerd string
        encrypted_char_count = 0 
        wheels_copy = self.wheels.copy() # Using a wheels copy for easy wheels reset at end of function

        for char in message: # Iterate over the message charecters
            if not char.islower(): 
                encrypted_string += char # Non lower case letters are unchanged
                self.rotate_wheels(encrypted_char_count, wheels_copy) # Rotate the wheels for any charecter
                continue

            # The encryption algorithm
            i = self.hash_map[char] 
            calculation = ((2 * wheels_copy[FIRST_WHEEL]) - wheels_copy[SECOND_WHEEL] + wheels_copy[THIRD_WHEEL]) % ABC_SIZE
            if calculation == 0:
                i += 1
            else:
                i += calculation
            i %= ABC_SIZE
            

            c1 = self.find_key_in_map(i)
            c2 = self.reflector_map[c1]
            i = self.hash_map[c2]
            
            if calculation == 0:
                i -= 1
            else:
                i -= calculation
            i %= ABC_SIZE

            c3 = self.find_key_in_map(i)

            encrypted_string += c3
            encrypted_char_count += 1

            self.rotate_wheels(encrypted_char_count, wheels_copy)

        return encrypted_string


if __name__ == '__main__':
    main()