# main.py
import os
import sys
from glob import glob
from typing import Dict
import os
import httpx
import ast
import json

# Put Orestes IP here
API_ENDPOINT = "http://98.10.243.234:8080/prompt"
TEST_KEY = '3900DD-8D360E-3884AC-44A317-883B97-V3'


def convert_to_hero_ml(func):
    """
    Implement conversion logic here
    """
    return func


def send_to_api(data: str):
    response = httpx.post(API_ENDPOINT, json=data)
    if 300 > response.status_code >= 200:
        print("Data sent to API successfully.")
    else:
        print("There may have been errors sending data to the API")
        print(response)


def findpy(root_dir):
    # Function to find all .py files in the root folder and subfolders, excluding venv directory
    files = []
    for root, dirs, _ in os.walk(root_dir):
        if "venv" in dirs:
            dirs.remove("venv")  # Exclude the venv directory from the search
        files.extend(glob(os.path.join(root, "*.py")))
    return files


def extract_decorated(file):
    with open(file, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    decorated_functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if (
                        isinstance(decorator, ast.Call)
                        and isinstance(decorator.func, ast.Name)
                        and decorator.func.id == "WatcherTest"
                ):
                    # if len(decorator.args) == 1 and isinstance(decorator.args[0], ast.Name)
                    decorated_functions.append(node.name)
                    break

    return decorated_functions


def run_tests():
    # Iterate through the .py files and check for functions with @WatcherTest decorator
    root_folder = os.path.dirname(os.path.abspath(__file__))
    files = findpy(root_folder)

    functions_with_decorator = []
    for file in files:
        functions_with_decorator.extend(extract_decorated(file))

    for func in functions_with_decorator:
        # calls the function from the function name
        result = globals()[func]()


def WatcherTest(dummy: Dict):
    def wrap(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            d = dict()
            d['key'] = TEST_KEY
            d['prompt'] = result
            d['inputs'] = dummy
            string = json.dumps(d)
            print(string)
            send_to_api(string)
            return result

        return wrapper

    return wrap

if __name__ == "__main__":
    run_tests()

def main():
    files = [file for file in os.listdir(os.getcwd()) if file.endswith('.py')]
    if 'test' in sys.argv:
        print("Python files in the directory:")
        for file in files:
            print(file)
    elif files:
        print("Hello, World!")

if __name__ == "__main__":
    main()
