## Project Summary:

As a student in Spanish 1 and Spanish 2, we were occassionally given oral exams - we would be given a sheet of potential questions a few days prior, and then we would be asked several of those questions. Studying orals by yourself was often challenging, as asking the questions to yourself doesn't really prepare you enough, which is why I have created this application.

Spanish Oral starts off by allowing you to enter several Spanish Questions, in this case, questions that you were given on an oral sheet. After you are done with that, you are transitioned to another screen you are asked randomly selected questions and tasked to answer them live. After you finish answering the question, a window will pop up with what you said in Spanish and the corresponding English translation. From there, you yourself can dictate whether you got the question right or wrong. When you have successfully answered all of the questions, you have the oppurtunity to restart all of the questions again. 

## How it Looks:

Question Inputting:

![enterin](https://github.com/GithubArnavSharma/SpanishOral/assets/77365987/9514c991-a750-444f-8743-aba7c6004cdb)

Question Recording:

![record](https://github.com/GithubArnavSharma/SpanishOral/assets/77365987/84325ea6-fbca-425d-9096-184d954e4e32)

Question Results:

![results](https://github.com/GithubArnavSharma/SpanishOral/assets/77365987/cec92cd2-d8f9-4ee6-9b5c-d8b637bd39e8)

## Try it Yourself:

1. Download the repository

2. Navigate to the repository and enter this command to download the requirements:
   
pip install -r requirements.txt

3. On command prompt, run spanish_oral.py. If you are using Python 3.8, this command may look like:

py -3.8 spanish_oral.py 

Note: You will need to download the Spanish voice package for Windows. Instructions are here: https://support.microsoft.com/en-us/windows/download-language-pack-for-speech-24d06ef3-ca09-ddcc-70a0-63606fd16394

You will also need to update the line "engine.setProperty('voice', voices[2].id)" depending on which index of the "voices" list holds the Spanish voice.
