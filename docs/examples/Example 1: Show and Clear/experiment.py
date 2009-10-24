def main():
    """
    Every instruction file must define a main() function,
    defined like this. You can use triple quotes after 
    the def line of your function to write a comment
    describing what it does. This has no effect on the 
    experiment.
    """
    show('I will be shown immediately.').now()
    show('I will be shown after two and a half seconds.').after(2500)
    show_message('I will be shown below the main text.').now()
    show_message('I will be shown after four and a half seconds.').after(4500)
    show('I will never be shown because Bryan forgot the to put .now() or .after(ms) after me.')
    show_bug('I will be shown \'unformatted\' at the bottom of the screen after three seconds.').after(3000)
    # To put a single line comment in the middle of your function
    # begin the line with a #, like this
    # Clear displayed text like so:
    clear().after(10000)
    clear_message().after(12000)
    clear_bug().after(14000)
    # You can use .now() and .after(ms) with both the show functions
    # and the clear functions.
    show_message('Press space to quit.').after(16000)
    show_event = show('I will never be shown because I am canceled before five seconds have passed.').after(5000)
    show_event.stop()
    yield for_space()

