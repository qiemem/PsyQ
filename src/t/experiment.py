def main():
    import sys
    print('in main')
    foo='bar'
    for k in locals():
        print(k)
    yield for_space()
