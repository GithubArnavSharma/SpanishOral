import pyaudio
import wave
import speech_recognition as sr
import os
import pyttsx3
import cv2
import random
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from googletrans import Translator
from threading import *

translator = Translator()
def spanish_to_english(spanish_text):
    try:
        return translator.translate(spanish_text, dest='en').text
    except:
        return "Google Translate API Error: Try Again"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate',145)
def speak(spanish_text):
    engine.say(spanish_text)
    engine.runAndWait()


recording_text = ""
questions = []
do_record = True
def record_audio(filename):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    record_seconds = 20
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []

    global recording_text
    recording_text = "Recording..."
    
    for i in range(int(sample_rate / chunk * record_seconds)):
        if do_record:
            data = stream.read(chunk)
        else:
            break
        frames.append(data)

    recording_text = ""
    
    stream.stop_stream()
    stream.close()

    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()

def audio_to_spanish(filename):
    r = sr.Recognizer()                                                      
    audio = sr.AudioFile(filename)

    with audio as source:
        audio = r.record(source)
        try:
            result = r.recognize_google(audio, language="es-ES")
        except:
            result = "N/A: Please Speak Louder!"
        
    os.remove(filename)

    return result


app = Tk()

def exit_window():
    global rule_window
    rule_window.destroy()

current_question = ""
total_questions = []
def question_right():
    global questions_text
    right_before = int(questions_text.split(":")[1].split('/')[0])
    questions_text = f"Questions Completed: {right_before + 1} / {len(total_questions)}"
    questions.remove(current_question)
    exit_window()

def display_results(spanish_text, english_text):
    global rule_window
    rule_window = Toplevel(app)
    
    rule_window.title("Results")
    rule_window.geometry("750x150")

    instruct_lbl = Label(rule_window, text="Based on the Spanish and English translation of what you said, did you say it correctly?", font=("Arial", 11))
    instruct_lbl.pack()
    
    spanish = Label(rule_window, text=spanish_text, foreground="black", font=("Arial", 11))
    spanish.pack(pady=10, anchor="w", side=TOP)
    english = Label(rule_window, text=english_text, foreground="black", font=("Arial", 11))
    english.pack(pady=10, anchor="w", side=TOP)

    correct = Button(rule_window, text="Correct", command=question_right, font=("Arial", 11))
    correct.pack(padx=150, side=LEFT)

    wrong = Button(rule_window, text="Wrong", command=exit_window, font=("Arial", 11))
    wrong.pack(padx=150, side=RIGHT)
    

def spanish_question():

    if len(questions) == 0: return None

    filename = 'temp.wav'

    question = random.sample(questions, 1)[0]

    try:
        speak(question)
    except:
        return None

    global current_question
    current_question = question
    
    record_audio(filename)

    spanish_text = audio_to_spanish(filename)
    english_text = spanish_to_english(spanish_text)

    display_results(f"What you said in Spanish: {spanish_text}",
                    f"What it means in English: {english_text}")

    global do_record
    do_record = True

def thread_question():
    t1 = Thread(target=spanish_question)
    t1.start()

def record_off():
    if len(questions) == 0: return None
    
    global do_record
    do_record = False

def record_text():
    global text
    text = "Recording..."


q_instruct = Label(app, text="Write a question and click 'Add Question' to add the question!", font=("Arial", 11), foreground="black")
inputtxt = Text(app, height = 10, width = 40, font=("Arial", 11))

q_instruct.pack(pady=10)
inputtxt.pack(pady=5)

def printInput():
    lbl = Label(app, text = "", font=("Arial", 11))

    lbl.pack()
    inp = inputtxt.get(1.0, "end-1c")

    global questions
    questions.append(inp)
    lbl.config(text = f"{len(questions)}. {inp}")

def restart_questions():
    global questions, questions_text
    questions = total_questions.copy()
    questions_text = f"Questions Completed: 0 / {len(total_questions)}"
    

answer_q, stop_record, restart, vid, label_widget = None, None, None, None, None
def startCamera():
    global app
    
    app.destroy()

    global answer_q, stop_record, vid, label_widget, questions_text

    app = Tk()

    vid = cv2.VideoCapture(0)

    width, height = 800, 600
      
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    app.bind('<Escape>', lambda e: app.quit())

    instruct_txt = "Press 'Begin Question' when you're ready to be asked a question.\nWhen the 'Recording...' text comes up, begin answering it.\nWhen you are done"
    instruct_txt += " answering the question, click 'Finish Question'.\nWhen you have finished all of the questions, you may restart by clicking 'Restart'."
    instruct_lbl = Label(app, text=instruct_txt, font=("Arial", 11), foreground="black")

    instruct_lbl.pack()
    
    label_widget = Label(app)
    label_widget.pack(pady=10)

    answer_q = Button(app, text="Begin Question", command=thread_question, font=("Arial", 10))
    answer_q.pack(pady=5, side=LEFT, padx=25)

    stop_record = Button(app, text="Finished Question", command=record_off, font=("Arial", 10))
    stop_record.pack(pady=5, side=LEFT, padx=5)

    restart = Button(app, text="Restart", command=restart_questions, font=("Arial", 10))
    restart.pack(pady=5, side=RIGHT, padx=65)

    global total_questions
    total_questions = questions.copy()

    questions_text = f"Questions Completed: 0 / {len(total_questions)}"

    open_camera()

    app.mainloop()

    
addBtn = Button(app, text = "Add Question", command = printInput, font=("Arial", 10))
addBtn.pack(pady=5)

startBtn = Button(app, text = "Finish", command = startCamera, font=("Arial", 10))
startBtn.pack(pady=5)

#Credit:
#https://www.geeksforgeeks.org/how-to-show-webcam-in-tkinter-window-python/
def open_camera():
    _, frame = vid.read()
  
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    captured_image = Image.fromarray(opencv_image)

    global recording_text, questions_text
    font = ImageFont.truetype("arial.ttf", 25)
    
    ImageDraw.Draw(
        captured_image
    ).text(
        (0, 0), 
        recording_text,
        (0, 0, 0),
        font=font
    )

    ImageDraw.Draw(
        captured_image
    ).text(
        (320, 0),
        questions_text,
        (0, 0, 0),
        font=font
    )

  
    photo_image = ImageTk.PhotoImage(image=captured_image)
  
    label_widget.photo_image = photo_image
  
    label_widget.configure(image=photo_image)
    
    label_widget.after(10, open_camera)
