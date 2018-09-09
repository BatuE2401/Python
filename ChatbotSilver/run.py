from Process import * #Imports the main code file

if __name__ == '__main__': #IfMain block to run the code
    p = Process()
    p.say("Hello, my name is Silver. I am a chatbot designed to help you when you struggle.") #Introduces herself
    while True:
        inp = input("You>> ") #Gets the input
        p.process(inp) #Processes the input
