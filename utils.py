import sys
import time
import msvcrt
BOT_NAME = "Sam"


class TimeoutExpired(Exception):
    pass


def input_with_timeout(timeout, timer=time.monotonic):
    prompt = "You: "
    print(prompt, end="")
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche())
            if result[-1] == '\r':
                return ''.join(result[:-1])
        time.sleep(0.04)
    raise TimeoutExpired


def reply(msg):
    print(f"{BOT_NAME}: {msg}")


def recieve():
    try:
        sentence = input_with_timeout(10)
    except TimeoutExpired:
        print('Sorry, times up')
        return "bye"
    else:
        return sentence
