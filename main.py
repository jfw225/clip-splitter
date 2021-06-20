from core.controller import Controller

PATH = "test.mp4"


def main():
    c = Controller(PATH)

    while True:
        c.get_input()
        for _ in c:
            pass


if __name__ == '__main__':
    main()
