# **PYPI PYTHON TRANSLATOR**
This is a translation package that allows you to translate text from one language to another using the Google Translate service. The program provides a user-friendly interface that automatically translates itself into the selected language.

---

## **Getting Started**

To use this program, you need to install the following libraries:

- `googletrans==4.0.0-rc1`
- `fuzzywuzzy`

You can install them by running the following command:

```bash
pip install googletrans==4.0.0-rc1
pip install fuzzywuzzy
```
And ofc you need the download package library:
```bash
pip install pypi_python_translator
```

## **Services**

The program requires access to Google services for translation. You don't need to write the available Google services into the `services.txt` file. it writes them for just information, if you are interested about services you can use `writeservices()` function in your code.

## **Language Examples**

This file contains a list of languages that can be used with the translation application. Each language entry is in the format `"<language code> - <country>"`. You can refer to this file when using the `init()` function.

For example:
- `init("en")` for English
- `init("tr")` for Turkish

Make sure to use the appropriate language code when initializing the translation application.


## **Function Reference**

### `writeservices()`

Writes all Google services to the `services.txt` file for using the transcript.

### `TRnslte(text: str, languages: str) -> str`

This is a self-translate function. It translates the given `text` into the specified `languages`.

### `writeusage(num)`

This code will write the given example with the value of "num" as file "example_num.py".

### `init(langg: str) -> any`

This is the main function to start the translation application. It adjusts the interface based on the selected language and prompts the user for the desired exit language. After that, it performs the translations.

Please note that this program only runs with a valid `langg` value. If the value is not found in the `Language_Examples` file, the code will crash. Make sure to check the examples file for valid language codes.

## **Usage**

After setting up the necessary files and libraries, you can use the `init("language-code")` function to start the translation application. The program will guide you through the translation process, displaying the input and output languages, the translated text, and the translation accuracy.

Please make sure to enter valid languages and follow the instructions provided by the program.

# **Examples**
Example usages for this package. you can also write those examples by using code: 

```python
from translator import *
writeusage(example_number) #for ex -> writeusage(1) writes the first example.
```

---
---
## `Example Usage (1): Using init() function to start program.`
In this example we are going to use init() function to start main program in given `<language code>`, no need to much talk this is the easiest.
```python
from translator import *
init("<language code>") #For ex -> init("en") start code in english GUI.
```
`NOTE: This code will start program for "1" times, and won't repeat himself.`<br>

---
## `Example Usage (2): Using TRnslte() function`<br>
In this example we are using TRnslte() function to translate `your_message`<br>
```python
from translator import *

your_message = "Hello world"

translated_message = TRnslte(your_message,"<language code>")

print(translated_message)

```
This code will translate `your_message` to the given `<language code>` and prints.

---
## `Example Usage (3): Using this program for full file translating;`<br>
I have to warn you: in this example `with` function only supports utf-8 characters. if you want to use any other encoding you can change it by editing `encoding=""` part.

```python
from translator import *

filecontent = []
with open("<your_file>.txt", "r",encoding="utf-8") as file: #read the file for translation.
    #The .txt extension is not mandatory, it can be any extension. The important thing is that you specify the encoding of the file correctly.
    for line in file:
        line = line.strip()  # Remove spaces and empty lines  
        if line:  # If line has characters
            filecontent.append(line)

with open("<output_file>.txt","w",encoding="utf-8") as file: #output file writing, it has to be same encoding with reading file
    for line in filecontent: #Every line in our list;
        translated_line = TRnslte(line,"<language_code>") #translate line to the "your language code"
        file.write(translated_line + "\n") #write the translated line to the file.
```
# **LICENSE**
[SForces/PyPi_Python_Translator is licensed under the
GNU General Public License v2.0](https://github.com/SForces/PyPi_Python_Translator/blob/main/LICENSE)
---
---