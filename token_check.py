def check(token):
    with open('tokens_base') as base:
        for line in base:
            if token in line:
                return True
