def main():
    """
    Notice that this directory has a file questions.txt. Questions
    and answers are stored in that file. That file also shows how
    to format your own questions.txt. Questions will be picked in
    a random order and no question will be picked twice.
    """
    # range(5) is a list of number 0 through 4. for i in range(5)
    # loops through the following code 5 times, first setting i 
    # to 0, then to 1, and so forth
    num_correct=0
    for i in range(5):
        pick_question()
        show(question()).now()
        show_message('Press space to answer.').now()
        bug = show_bug(answer()).after(1000)
        yield for_space()
        clear_message().now()
        bug.stop()
        clear_bug().now()
        yield for_user_input()
        if user_input()==answer():
            show('Correct!').now()
            num_correct += 1
        else:
            show('Wrong stupid face!').now()
        show_message('Press space to continue')
        yield for_space()
    # You have probably noticed that you can concatenate text using
    # +. To concatenate text with a number (or anything that's not
    # text), you must wrap it like str(num) first. For instance:
    show('You got '+str(num_correct)+' out of 5 right.').now()
    show_message('Press space to quit.').now()
    yield for_space()
