def main():    start_timer()    show('The experiment is running').after(500)    show_message('Press space to continue').now()    yield for_space()    pick_question()    show(question()).now()    show_message('Press space to answer the question').now()    yield for_space()    clear_message().now()    show_bug(answer()).after(500)    yield for_user_input()    if user_input() == answer():        show('Right!').now()    else:        show('Wrong!').now()        show_message(user_input() + ' != ' + answer()).after(500)    show_message('Press space to quit').now()    yield for_space()    #t=time()    #record(t)    #show('I am now accepting input').now()    #show_bug('It took you '+str(t)+' seconds to press space').after(1000)    #yield for_user_input()    #record(user_input())    #record(time())    #show('You entered '+user_input()).now()    #yield for_space()