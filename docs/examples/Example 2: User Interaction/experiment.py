def main():
    """
    This script demonstrates how to interact with the user.
    User interaction is done with by typing yield and then
    whatever you want to wait for from the user.
    """
    show('Example 2: User Interaction').now()
    show_message('Press space to continue.').now()
    yield for_space()   
    # Nothing past this point will be executed until the 
    # user presses space.
    show('Enter some text:').now()
    show_message('Press submit to continue.').now()
    yield for_user_input()
    # Nothing past this will happen until the user presses
    # submit.
    show('You entered ' + user_input()).now()
    show_message('Press space to quit.').now()
    yield for_space()

