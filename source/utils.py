import datetime

def resolve_expression(expression_string):
    try:
        return eval(expression_string)
    except:
        return None

def log(text):
    now = datetime.datetime.now().ctime()
    print("[{}] {}".format(now, text))