def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def run_until_num_entered(input_string):
    while True:
        entered_number = input(input_string)
        test_number = is_number(entered_number)
        if test_number == False:
            print("Please enter an integer")
        else:
            return int(entered_number)