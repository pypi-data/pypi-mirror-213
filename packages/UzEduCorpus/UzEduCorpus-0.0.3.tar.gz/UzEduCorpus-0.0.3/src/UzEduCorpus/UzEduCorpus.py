import os

def load_1():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_1.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_2():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_2.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_3():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_3.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_4():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_4.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_5():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_5.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_6():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_6.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_7():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_7.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_8():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_8.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words

def load_9():
    words = list()
    dirname = os.path.dirname(__file__) + "/"
    with open(os.path.join(dirname + "grade_9.csv"), encoding='utf8') as file:
        for line in file:
            x = line.rstrip()
            words.append(x)
        words.remove(words[0])
    return words