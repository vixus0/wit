![Wit logo](https://raw.githubusercontent.com/vixus0/htp4/master/wit.png)
# Wit

_Proof of concept developed over 24 hours for Hack the Police 4_

Wit does two jobs:

- It provides an online service for submitting witness statements
- Using natural language processing (NLP) it attempts to find information that is common to many witness statements, helping police officer make connections

## Concept

Through discussions with police officers we determined that one of the biggest problems they had when responding to calls was collecting witness statements, especially in situations involving multiple potential witnesses or where time was critical.
Another problem was the paper-based bureaucracy involved with submitting case files.
Witness statements and accompanying information had to be carefully prepared using the format specified by the Crown Prosecution Service's Manual of Guidance (MG11 form).

We came up with the idea to have officers generate unique codes on the fly which they could hand out to witnesses.
Witnesses would then use the code to access an online service which would ensure they submitted the information and consent required for the MG11 form.
The form would ask them if they had more information about something they had mentioned.

![Screenshot of witness statement process 1](https://raw.githubusercontent.com/vixus0/htp4/master/screenshots/witness1.png)
![Screenshot of witness statement process 2](https://raw.githubusercontent.com/vixus0/htp4/master/screenshots/witness2.png)
![Screenshot of witness statement process 3](https://raw.githubusercontent.com/vixus0/htp4/master/screenshots/witness3.png)

On the police side of things, all the statements for a case would undergo NLP to extract potentially important information and draw links between names, places and times.
Potentially, we could automatically construct a timeline based on the information in multiple witness statements.

![Screenshot of police view 1](https://raw.githubusercontent.com/vixus0/htp4/master/screenshots/police1.png)
![Screenshot of police view 2](https://raw.githubusercontent.com/vixus0/htp4/master/screenshots/police2.png)

[View presentation slides](https://docs.google.com/presentation/d/18NUe7jNAlNt29VoPybCKdm2kr6ZAu2CeP5aYr8LLRlQ/edit?usp=sharing)

## Technology

- The backend applications `witness.py` and `police.py` are written in Python/[Flask](https://flask.pocoo.org)
- The NLP was performed using [spaCy](https://spacy.io)
- The graph on the police panel was drawn using [sigma.js](https://sigmajs.org)

## How to run

```
# Once you have virtualenv installed
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./witness.py &
./police.py &
```
