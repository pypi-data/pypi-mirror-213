from googletrans import LANGUAGES
def list_():
    supported_languages = []
    for languge_code, language_name in LANGUAGES.items():
        supported_languages.append(f"{languge_code} - {language_name}")
    return supported_languages
def writelist():
    supported_languages = list_()
    with open("Language_Examples.txt","w") as f:
        for language_names in supported_languages:
            f.write(language_names + "\n")