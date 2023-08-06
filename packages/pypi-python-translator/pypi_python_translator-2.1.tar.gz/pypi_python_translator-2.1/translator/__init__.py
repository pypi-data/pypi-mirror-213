import os
import sys
from translator.services import google_services
from translator.messages import *
from translator.languageExamples import *
try:
    from googletrans import Translator
    from fuzzywuzzy import fuzz
except ModuleNotFoundError:
    raise ModuleNotFoundError("To use this program, you need to download those libraries;\npip install googletrans==4.0.0-rc1\npip install fuzzywuzzy")
def writeservices() -> None:
    """
    Services
    ~~~~~~~~
    Write all google services for using transcript
    """
    with open("services.txt","w") as f:
        for service in google_services:
            f.write(service + "\n")
def TRnslte(text:str,languages:str) -> str:
    """
    What is that ?
    ~~~
    This is self translate.

    Program translates his own gui and messages
    """
    while True:
        try:
            translator = Translator()
            ceviri = translator.translate(text,dest=languages)
            break
        except TypeError:
            continue
        except ValueError:
            print(f"The output language should be one of the languages in the 'Language_Examples.txt' file, not {languages}!")
            input()
            sys.exit()
    return ceviri.text
def init(langg:str) -> any:
    """
    TRANSLATOR MAIN FUNCTION
    ~~~
    This is the function you will use to start this translation application.
    
    The interface translates itself, and then prompts the user for the desired exit language. 
    
    After that, translations are performed. 
    
    Please note that this program runs only in a true langg value, if value isn't in the 'Language_Examples' file, code will crash.

    So don't forget to look at examples file.
    """
    os.system("cls")
    writelist()
    #default messages
    print("The program adjusting his interface for the language you choose, this may take a few seconds, please be patient.")
    welcome_title0 = TRnslte(f"{welcome0}",langg)
    welcome_title1 = TRnslte(f"{welcome1}",langg)
    translatingg = TRnslte(translating,langg)
    inputlanguage = TRnslte(inputlanguages,langg)
    OutputLanguage = TRnslte(OutputLanguages,langg)
    texthere = TRnslte(textheres,langg)
    original = TRnslte(originalTexts,langg)
    os.system("cls")
    output_lang = input(f"{welcome_title0}\n{welcome_title1} ")
    os.system("cls")
    msg = input(f"{texthere}\n").lower()
    translator = Translator()
    print(translatingg)
    while True:
        try:
            msg_language = translator.detect(msg)
            msg_language = msg_language.lang
            ceviri = translator.translate(msg, dest=output_lang)
            text_org = translator.translate(ceviri.text, dest=msg_language)
            accuracy = fuzz.ratio(msg, text_org.text)
            Accury = TRnslte(f"Çeviri Doğruluğu: %{accuracy}",langg)
            os.system("cls")
            E1 = TRnslte("Çeviri doğruluğu nedir ?",langg)
            E2 = TRnslte(f"Program tries to achieve the same result by reverse engineering the output message of the message you entered, the more similar the result, its going to the higher % value, its accuracy can be misleading.",langg)
            print(f"{inputlanguage} {msg_language}\n\n{OutputLanguage} {output_lang}: {ceviri.text}\n\n{original} {text_org.text}\n{Accury}")
            print(f"\n{E1}\n{E2}")
            input()
            break
        except TypeError:
            continue
        except ValueError:
            errmsg = TRnslte(f"The output language should be one of the languages in the 'Language_Examples.txt' file, not {output_lang}!",langg)
            print(errmsg)
            input()
            sys.exit()