import random
import re


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()



def generate_otp() -> str:
    return str(random.randint(100000, 999999))
