from get_words import random_word
from get_words import info
from plyer import notification
import time

def notify_vocab( timeout, word="animal", info="something in the wild"):

    notification.notify(
        title=word,
        message=info,
        app_icon="notify_vocab\\assets\\dictionary.ico",
        timeout=timeout
    )

def notifyVocab(timeout=5):
    notify_vocab(timeout,random_word,info)

notifyVocab()

