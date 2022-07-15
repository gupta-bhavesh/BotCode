from predict import predict
import random
from utils import recieve, reply
from database import check_appointment, take_appointment
import torch
from model import NeuralNet

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).cuda()
model.load_state_dict(model_state)
model.eval()


def greeting():
    sentence = random.choice([
        "Hey :-)",
        "Hello, thanks for visiting. What can i do?",
        "Hi there, what can I do for you?",
        "Hi there, how can I help?"
    ])
    reply(sentence)


def help():
    sentence = "You can book appointment, get the timing, get updates on your appointment.\nFor eg: Can I get the appointment."
    reply(sentence)


def dont_understand():
    sentence = "I do not understand..."
    reply(sentence)


def no_match():
    dont_understand()
    return help()


def thanks():
    sentence = random.choice([
        "Happy to help!",
        "Any time!",
        "My pleasure"
    ])
    reply(sentence)


def goodbye():
    sentence = random.choice([
        "See you later, thanks for visiting",
        "Have a nice day",
        "Bye! Come back again soon."
    ])
    reply(sentence)
    return 1


def timing():
    sentence = random.choice([
        "Doctor is available 8am-8pm all days except Friday.",
        "Clinic is open 8am-8pm all days except Friday."
    ])
    reply(sentence)


def anything_else():
    sentence = random.choice([
        "Can I do something else for you?",
        "What else I can do for you?"
    ])
    reply(sentence)
    tag = predict(recieve(), model, tags, all_words)
    if tag == "reject":
        return goodbye()
    if tag == "accept":
        tag = predict(recieve(), model, tags, all_words)
        return actions[tag]()
    else:
        return actions[tag]()


def appointment_status():
    pno = "8955571184"
    prev_appointment = check_appointment(pno)
    if prev_appointment is None:
        sentence = "You dont have any appointment."
    else:
        sentence = "You have appointment booked at {} of time {}".format(
            prev_appointment[2], prev_appointment[3])
    reply(sentence)


def appointment():
    sentence = random.choice([
        "You can meet the doctor at 7pm. Is it okay for you?\nYes/No",
        "Doctor is available at 7pm tommorow. Is it okay for you?\nYes/No"
    ])
    reply(sentence)
    tag = predict(recieve(), model, tags, all_words)
    if tag == "accept":
        pno = "8955571184"
        reply(take_appointment(pno))
        return anything_else()

    if tag == "reject":
        return anything_else()
    else:
        return appointment()


def current_availability():
    ans = random.choice([
        "Yes, he is available right now. Should I book a seat for you?",
        "Yes, he is available. Should I book an appointment for you?"
    ])
    reply(ans)
    tag = predict(recieve(), model, tags, all_words)
    if tag == "accept":
        return appointment()
    if tag == "reject":
        return anything_else()
    else:
        return current_availability()


actions = {
    "greeting": greeting,
    "goodbye": goodbye,
    "thanks": thanks,
    "appointment": appointment,
    "timing": timing,
    "appointment_status": appointment_status,
    "current_availability": current_availability,
    "none": no_match,
    "help": help
}
