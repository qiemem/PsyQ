def main():
    """
    The programming language you have been using to write these
    experiments is called Python. Using Python greatly increases
    the flexibility and potentialcomplexity of the possible 
    experiments. You don't need to know Python to write experiments,
    particularly because the language has been somewhat augmented
    by this program. However, knowing a little does help.

    You may have noticed the def main() that begins every experiment
    script. The def keyword is how you define a new function in 
    Python. Thus,
    def main():
    defines a function called main. You will see a couple other
    function definitions in this example. The ':' after 'main()'
    indicates that a block of code will follow. This block of code
    must be indented. Thus, the contents of a function is all the
    indented code following it.

    Note:
    Unlike in a normal Python script, the main function here will
    not see anything defined outside of it. Thus, all function
    definitions, imports, variables, class definitions, etc. must
    go inside the main() function if you want to be actually
    able to use them at runtime.
    """
    def set_display(main_display, message_display):
        """
        The 'main_display' and 'message_display' are the function's
        arguments. This function simply takes two pieces of text and
        sets the main display to the first and the lower message
        display to the second. We can use it like:
        set_display("Welcome to the experiment!", "Press space to continue.")
        The 'return' at the end of this function is there purely for
        demonstrative reasons. This is how you can pass back a value
        after the function finishes. So,
        a_variable = set_display("One", "Two")
        would set a_variable to:
        "Main display is now 'One'."
        """
        show(main_display).now()
        show(message_display).now()
        return "Main display is now '"+main_display+"'."
    def ask_question():
        pick_question()
        set_display(question(), "Press submit to when you have answered.")
        yield for_user_input()


