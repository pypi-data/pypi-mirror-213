from googletrans import LANGUAGES
def list_():
    desteklenen_diller = []
    for dil_kodu, dil_adı in LANGUAGES.items():
        desteklenen_diller.append(f"{dil_kodu} - {dil_adı}")
    return desteklenen_diller
def writelist():
    desteklenen_diller = list_()
    with open("Language_Examples.txt","w") as f:
        for dil in desteklenen_diller:
            f.write(dil + "\n")