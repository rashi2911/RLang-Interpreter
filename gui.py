import RLang

while True:
    text = input('RLang > ')
    result, error = RLang.result(text)

    if error:
        print(error.convert_to_string())
    elif result:
        print(result)


