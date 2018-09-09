import spacy #Module for Natural Language Processing
import sys #Module to interact strongly with the interpreter
import random #Module to pick random things
import re #Module to strip strings
import requests #Module I used for exception handling
import webbrowser #Module to open a new tab on your browser
from win32com.client import Dispatch #Module for Silver to speak
from collections import OrderedDict #Module that is used here to remove duplicates
from WikiSearch import * #Imports the file that has the class used for wikipedia searching

class Process:
    def __init__(self):
        #Defining all the variables
        self.greetings = [
        "hello", "hi", "Good Day",
        "hey", "what's up", "sup"
        ]

        self.exitphrases = [
        "bye", "goodbye",
        "see you", "see ya",
        "cya", "terminate"
        ]

        self.yesphrases = [
        "yes", "sure", "ok"
        ]

        self.nophrases = [
        "no", "nah", "nope"
        ]

        self.thanksphrases = [
        "thank", "thanks",
        "appreciate it",
        ]

        self.respondthanksphrases = [
        "You're welcome", "Yes, I know I am the best"
        ]

        self.q_words = [
        "what", "when", "who",
        'where', 'why', 'how'
        ]

        self.not_understood_phrases = [
        "I am not sure what that meant!",
        "Sorry I do not understand.",
        "I was unable to comprehend..."
        ]

        self.check_nothing_phrases = [
        "You have entered nothing!",
        "Is it me or have you not entered anything?",
        "I cannot understand something that is nothing!"
        ]

        self.speak = Dispatch("SAPI.SpVoice") #For the chatbot to speak

        self.wikisearch = WikiSearch()

    def break_down(self, s): #Splits the string into its words
        elements = re.split('\W+', s)
        if '' in elements:
            del elements[-1]
        return elements

    def remove_punctuation(self, s):
        words = self.break_down(s)
        sentence = ''
        for word in words:
            if words.index(word) != len(words) - 1:
                sentence += word + ' '
            else:
                sentence += word
        return sentence

    def parse(self, s): #Uses nlp to parses the string and append tokens to the tags array
        sentence = self.remove_punctuation(s)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(sentence)
        tags = []
        for token in doc:
            tags.append(token.pos_)
        return tags

    def isInt(self, s): #Checks if a string is a number, used to find dates in sentences
        try:
            s = int(s)
            return True
        except ValueError:
            return False

    def seperate_elements(self, s): #Seperates the elements by appending it to the different arrays according to their tags
        nouns = ['It', 'He', 'She', 'it', 'he', 'she']
        propns = []
        verbs = []
        tags = self.parse(s)
        elements = self.break_down(s)
        for i in range(len(elements)):
            if str.lower(elements[i]) not in self.q_words:
                if tags[i] is 'VERB':
                    verbs.append(elements[i])
                elif tags[i] is 'PROPN':
                    nouns.append(elements[i])
                    propns.append(elements[i])

        if propns == []: #If the were no proper nouns found it finds the nouns
            for i in range(len(elements)):
                if str.lower(elements[i]) not in self.q_words:
                    if tags[i] is 'NOUN':
                        propns.append(elements[i])
        return nouns, propns, verbs

    def check_words(self, s, words): #Check if the user has said any word in a certain words list
        for word in words:
            if word in str.lower(s):
                return True
        return False

    def find_ans(self, s): #Finds the answer to the question using the wikipedia library
        nouns, propns, verbs = self.seperate_elements(s)
        summary = self.wikisearch.get_summary(propns)
        sentences = summary.split('.')
        possible_ans = []
        new_possible_ans = []
        answers = []
        answer = ''

        for i in range(len(sentences)): #This loop finds the sentences that have the right nouns in it
            for j in range(len(nouns)):
                wordsSentence = re.split('\W+', sentences[i])
                if nouns[j] in wordsSentence:
                    possible_ans.append(sentences[i])

        for i in range(len(possible_ans)): #This loop finds the sentences according to the question word
            wordsSentence = re.split('\W+', possible_ans[i])
            for j in range(len(wordsSentence)):
                if 'when' in str.lower(s): #If the question word is 'when' the bot tries to find the sentence that has a date in it
                    if self.isInt(wordsSentence[j]):
                        new_possible_ans.append(possible_ans[i])
                if 'why' in str.lower(s): #If the question word is 'why' the bot tries to find the sentence that has conjuntions in it
                    if 'because' in wordsSentence[j] or 'reason' in wordsSentence[j] \
                        or 'purpose' in wordsSentence[j]:
                        new_possible_ans.append(possible_ans[i])
                else: #If none of them satisfies, it will continue with the original sentences
                    new_possible_ans.append(possible_ans[i])

        for i in range(len(new_possible_ans)): #This final loop finds the sentences that have the verbs got from the question
            for j in range(len(verbs)):
                wordsSentence = re.split('\W+', new_possible_ans[i])
                if verbs[j] in wordsSentence:
                    answers.append(new_possible_ans[i])

        answers = list(OrderedDict.fromkeys(answers)) #This function makes sure that the aren't any duplicates
        if len(answers) >= 1: #Only gives two of the sentences if it is too long
            answer = answers[0]
        return answer

    def say(self, s): #Function for the bot to speak
        print("Silver>>",s)
        self.speak.Speak(s)

    def process(self, s): #This function process the input and returns responds
        nouns, propns, verbs = self.seperate_elements(s)
        if self.check_words(s, self.greetings) is True: #If there is a greeting, respond with a random greeting phrase
            self.say(random.choice(self.greetings))

        if self.check_words(s, self.exitphrases) is True: #If there is a termination phrase, respond with a random exit phrase
            self.say(random.choice(self.exitphrases))
            sys.exit()

        if self.check_words(s, self.thanksphrases) is True: #If the user thanks Silver, it responds with a random response phrase
            self.say(random.choice(self.respondthanksphrases))

        if self.check_words(s, self.q_words) is True: #If there is a question word in the input, it triggers the find_ans function to return an answer
            article_name = self.wikisearch.create_article_name(propns)
            article_url = self.wikisearch.create_article_url(propns)
            try:
                answer = self.find_ans(s)
                if answer == '': #If the bot cannot find an answer, it responds apologetically
                    self.say("Sorry, I could not find what you were looking for...")
                else: #If tere is an answer found, it reponds with a formatted response
                    self.say("Here is what I found on Wikipedia, {}".format(answer))
                    self.say("Do you want to learn more?") #Checks if the user wants to learn more, if so uses the webbrowser module to open he wiki page in your browser
                    choice = input("You>> ")
                    for i in range(len(self.yesphrases)):#Checks if the user says yes
                        if self.yesphrases[i] in str.lower(choice):
                            self.say("Opening the Wikipedia Page for {}".format(article_name))
                            webbrowser.open_new(article_url)
            except wikipedia.exceptions.PageError: #Exception handling if there is no such page
                self.say("Must be a typo, I could not find the wiki page, can you check and say it again?")
            except requests.exceptions.ConnectionError: #Exception handling if the bot cannot reach the server
                self.say("Sorry, I cannot reach the Wikipedia server.")
            except wikipedia.exceptions.DisambiguationError: #Exception handling if there are many articles about what the user asks
                self.say("There are many {}s. Can you please be more specific?".format(article_name))
            except wikipedia.exceptions.WikipediaException:
                self.say("I am sorry, there has been an error. Please try again.")

        if s == "": #If the user says nothing the chatbot responds with a random phrase about it
            self.say(random.choice(self.check_nothing_phrases))
            
        #If the string is doesn't satisfy any of those conditions, the bot says that she doesn't understand
        elif self.check_words(s, self.greetings) is False and self.check_words(s, self.exitphrases) is False and \
             self.check_words(s, self.thanksphrases) is False and self.check_words(s, self.q_words) is False and s != "":
                self.say(random.choice(self.not_understood_phrases))
