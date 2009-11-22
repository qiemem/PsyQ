def main():
    for i in range(10):
        show("""
             one
             two
             three
             four
             five
             six
             seven
             eight
             nine
             ten
             """).now()
        yield for_user_input()
