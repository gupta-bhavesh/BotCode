from utils import recieve
from predict import predict
from response import actions, model, tags, all_words

if __name__ == '__main__':
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = recieve()
        tag = predict(sentence, model, tags, all_words)
        a = actions[tag]()
        if a:
            break
