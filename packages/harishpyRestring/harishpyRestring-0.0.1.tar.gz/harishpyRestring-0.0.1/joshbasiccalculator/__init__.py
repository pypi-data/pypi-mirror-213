def String_replace(wholestring,currentword, replaceWord):
    txt = wholestring

    x = txt.replace(currentword,replaceWord)

    return x
print(String_replace("I like bananas","bananas", "apples"))