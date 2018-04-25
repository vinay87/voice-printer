# -*- coding: UTF-8 -*-

import cups
import os
import time
import random
import aiy.audio
import aiy.voicehat
import aiy.assistant.grpc
import datetime
from google_speech import Speech
import random
import glob

def say(text, lang="en"):
    speech = Speech(text)
    sox_effects = ("speed", "1", "vol", "0.7")
    speech.play(sox_effects)


def print_story():
    conn = cups.Connection()
    story_path = os.path.join(
            os.path.dirname(os.path.realpath(__file)),
            "data","stories","*.docx")
    random_story = random.choice(glob.glob(story_path))
    conn.printFile("ZJ-58", random_story)


def print_poem():
    conn = cups.Connection()
    story_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data","poems","*.docx")
    random_story = random.choice(glob.glob(story_path))
    conn.printFile("ZJ-58", random_story)


def print_quote():
    conn = cups.Connection()
    story_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data","quotes","*.docx")
    random_story = random.choice(glob.glob(story_path))
    conn.printFile("ZJ-58", random_story)

def print_gkn():
    conn = cups.Connection()
    story_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data","gkn","*.docx")
    random_story = random.choice(glob.glob(story_path))
    conn.printFile("ZJ-58", random_story)


def print_report():
    pass


def main():
    """main program"""
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status("starting")
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.BLINK)
    time.sleep(1)
    led.set_state(aiy.voicehat.LED.OFF)
    say("Hello, I am Zelda, your personal voice assistant.")
    say("Press the button and speak.")
    with aiy.audio.get_recorder():
        while True:
            try:
                status_ui.status("ready")
                button.wait_for_press()
                status_ui.status("listening")
                say("Listening...")
                text, audio = assistant.recognize()
                if text is not None:
                    if text == "goodbye":
                        status_ui.status("stopping")
                        say("Bye!")
                        break
                    elif "print" in text:
                        if "story" in text:
                            print_story()
                        elif "poem" in text:
                            print_poem()
                        elif "quote" in text:
                            print_quote()
                        elif "report" in text:
                            print_report()
                        else:
                            say("I'm sorry, I don't know what you want me to print.")
                    else:
                        say("Can you try again, I'm not sure what you want me to do.")
                else:
                    print_gkn()
            except KeyboardInterrupt:
                led.set_state(aiy.voicehat.LED.OFF)
                say("Farewell!")
                break

if __name__ == "__main__":
    main()
