import os
from dotenv import load_dotenv
load_dotenv()
print_text = os.getenv("PRINT")
def do():
    print(print_text)
do()