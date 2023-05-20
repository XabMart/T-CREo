from better_profanity import profanity
import better_profanity

def badWordsProportion(text,lang):
    profanity.load_censor_words(lang)
    badWordsCounter = 0
    textLenght = len(text.split()) #Longitud del texto.
    for word in text.split():
      if profanity.contains_profanity(word): #Funci�n de librer�a que dice si una palabra es "malsonante"
         badWordsCounter+=1# Si la palabra no es adecuada, se suma 1
    result = 100 - (100*badWordsCounter/textLenght) #C�lculo del par�metro
    return result