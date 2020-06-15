from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot('CoronaBot')

 # Training with Personal Ques & Ans
# import hyperlink
#
# url = hyperlink.parse(u'http://127.0.0.1:5000/')
#
# better_url = url.replace(scheme=u'https', port=443)
# org_url = better_url.click(u'.')
#
trainer = ListTrainer(chatbot)
#
trainer.train(["'Hi','Hey'", 'Hey Chatbot here B) what can I do for you'])
trainer.train(['How are you?', 'I am good what can I do for you' ])
trainer.train(['Bye', 'Bye, see you later' ])
trainer.train(['I want loan', 'Check Out link for Eligibility Screening: http://127.0.0.1:5000/'])
trainer.train(['"How you could help me?","What you can do?"|"What help you provide?","How you can be helpful?"|"What support is offered"', 'I help people to check eligibility for sanctioning loan'])
trainer.train(['"Bye","See you later","Goodbye","Nice chatting to you, bye", "Till next time"', 'Happy to Help!'])

#
# {"intents": [
#         {"tag": "greeting",
#          "patterns": [],
#          "responses": ["Hello, thanks for asking", "Good to see you again", "Hi there, how can I help?"],
#          "context": [""]
#         },
#         {"tag": "goodbye",
#          "patterns": ["Bye", "See you later", "Goodbye", "Nice chatting to you, bye", "Till next time"],
#          "responses": ["See you!", "Have a nice day", "Bye! Come back again soon."],
#          "context": [""]
#         },
#         {"tag": "thanks",
#          "patterns": ["Thanks", "Thank you", "That's helpful", "Awesome, thanks", "Thanks for helping me"],
#          "responses": ["Happy to help!", "Any time!", "My pleasure"],
#          "context": [""]
#         },
#         {"tag": "noanswer",
#          "patterns": [],
#          "responses": [""],
#          "context": [""]
#         },
#         {"tag": "options",
#          "patterns": [],
#          "responses": ["I can guide you through Adverse drug reaction list, Blood pressure tracking, Hospitals and Pharmacies", "Offering support for Adverse drug reaction, Blood pressure, Hospitals and Pharmacies"],
#          "context": [""]
#         },
#
# trainer.train(['"Hi there"|"How are you"| "Is anyone there?"|"Hey"|"Hola"| "Hello"|"Good day"', '"Hi there"|"How are you"| "Is anyone there?"|"Hey"|"Hola"| "Hello"|"Good day"'],
# ['"Thanks", "Thank you"|"Thats helpful"|"Awesome thanks"|"Thanks for helping me"', '"Sorry, cant understand you"|"Please give me more info"|"Not sure I understand"'])
# # trainer.train()
# trainer.train(['"How you could help me?"|"What you can do?"|"What help you provide?"|"How you can be helpful?"|"What support is offered"', 'Enter link to proceed: http://127.0.0.1:5000/'])
# trainer.train(['I want loan', 'Enter link to proceed: http://127.0.0.1:5000/'])
# trainer.train(['I want loan', 'Enter link to proceed: http://127.0.0.1:5000/'])
# trainer.train(['I want loan', 'Enter link to proceed: http://127.0.0.1:5000/'])


# trainer.train(['Hi', 'Heyy its ChatBot here. What can I do for you?'])
# trainer.train(['I want loan', 'Enter link to proceed: http://127.0.0.1:5000/'])



# Training with English Corpus Data
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
)
