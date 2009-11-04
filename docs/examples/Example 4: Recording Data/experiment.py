def main():
    """
    This example demonstrates how to record data and time user
    responses. Furthermore, this example demonstrates how one
    can use the standard python libraries to expand the possible
    styles of experiments.

    New functions:

    start_timer() - Sets the internal timer to 0 seconds.

    time() - Returns the number of seconds since start_timer()
    was called. The number will be accurate usually down to
    milliseconds or less, though it depends on your system.

    record(msg) - Adds msg to the data to be written to resulting
    data file. The file will be contained in the experiment
    folder and will be labelled with the date and time that the
    experiment ends.
    """
    # See the Example 5 for a discussion of how the following
    # line works.
    from random import randint
    # randint returns a random number in a given range.

    show('This experiment tests your response time. When the experiment begins, after a random amount of time, a message will appear telling you to press space. Do so as quickly as possible. You will do this five times.').now()
    show_message('Press space to continue.').now()
    yield for_space()
    for i in range(5):
        clear().now()
        clear_message().now()
        start_timer()
        # We get a random number between 0 and 3000.
        t = randint(0,3000)
        show('Press space now!').after(t)
        yield for_space()
        # time() is the amount of time that has passed since
        # start_timer() was called in seconds.
        # We first convert it to milliseconds.
        ms = time()*1000
        # We subtract the amount of time it took for the message
        # to show up and record it.
        record(ms - t)
        show('Get ready for the next one!').now()
        show_message('Press space when you\'re ready.').now()
    show('That\'s it. You\'re done!').now()
    show_message('Press space to quit.').now()
    yield for_space()
