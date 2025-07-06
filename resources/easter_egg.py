import logging

class helpful_functions:

    def __init__(self):
        logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s",
                            level = logging.INFO)

    def convert_hex_to_dec(self,input:str = None):
        if input == None:
            #Convert hex string to int
            input = "1A3F"
        logging.info(f"The value of hex string : {input} converted to integer is {int(input,16)}")
        return int(input,16)
    
    def one_liner_to_filter_numbers (self,odd_or_even:str=None, input = None):
        #One-liner to filter even numbers from a list
        input = [1,2,3,4,5,6,7,8]
        if odd_or_even == None:
            logging.info(f"The odd numbers of the input list are {list(filter(lambda x:x%2, input))}")
            logging.info (f"The even numbers of the input list are {[x for x in input if x%2==0]}")
            return None
        elif odd_or_even.lower() == "odd":
            return list(filter(lambda x:x%2, input))
        elif odd_or_even.lower() == "even":
            return list(filter(lambda x:x%2==0, input))
        else:
            logging.error (f"Invalid input")


if __name__ == "__main__":
    obj1 = helpful_functions()
    obj1.convert_hex_to_dec()
    logging.info (f"Return value : {obj1.one_liner_to_filter_numbers()}")