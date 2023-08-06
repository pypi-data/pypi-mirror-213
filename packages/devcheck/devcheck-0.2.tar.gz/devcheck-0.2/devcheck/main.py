# main.py
import os
import ast
import json
import logging
import httpx
import argparse
from glob import glob
from typing import Dict, List
from tqdm import tqdm
from colorama import Fore, Style
from datetime import datetime
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set API Endpoint
API_ENDPOINT = "http://api.devcheck.ai/prompt"

# Load API key from environment variable
API_KEY_TEST = os.getenv('API_KEY_TEST')



def authenticate():
    api_key = input("Please enter your API Key from devcheck.ai: ")
    set_key(".env", "API_KEY_TEST", api_key)
    print("API Key saved successfully.")

def print_colored_result(data: Dict) -> None:
    test_result = data["LLM_Test_Result"]
    print(f"{Fore.YELLOW}Status: {test_result['status']}")
    print(f"Time Completed: {datetime.fromisoformat(test_result['time_completed'].replace('Z', '+00:00'))}")
    for result in test_result["results"]:
        color = Fore.GREEN if result["status"] == "PASS" else Fore.RED
        print(f"{color}Test Name: {result['name']}\nStatus: {result['status']}\nScore: {result['score']}")
        if 'reason' in result:
            print(f"Reason: {result['reason']}")
    print(Style.RESET_ALL)


def send_to_api(data: str) -> None:
    try:
        response = httpx.post(API_ENDPOINT, json=data)
        if 300 > response.status_code >= 200:
            logging.info("Data sent to API successfully.")
            print_colored_result(response.json())
        else:
            logging.error("There may have been errors sending data to the API.")
            logging.error(response)
    except Exception as e:
        logging.error(f"Exception occurred: {e}")


def findpy(root_dir: str) -> List[str]:
    # Function to find all .py files in the root folder and subfolders, excluding venv directory
    files = []
    for root, dirs, _ in os.walk(root_dir):
        if "venv" in dirs:
            dirs.remove("venv")  # Exclude the venv directory from the search
        files.extend(glob(os.path.join(root, "*.py")))
    return files


def extract_decorated(file: str) -> List[str]:
    with open(file, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    decorated_functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "WatcherTest":
                    decorated_functions.append(node.name)
                    break

    return decorated_functions


def run_tests() -> None:
    # Iterate through the .py files and check for functions with @WatcherTest decorator
    root_folder = os.path.dirname(os.path.abspath(__file__))
    files = findpy(root_folder)

    functions_with_decorator = []
    for file in files:
        print(file)
        functions_with_decorator.extend(extract_decorated(file))

    for func in tqdm(functions_with_decorator, desc="Running tests", ncols=70):
        # calls the function from the function name
        result = globals()[func]()


def WatcherTest(dummy: Dict):
    def wrap(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            d = dict()
            d['key'] = API_KEY_TEST
            d['prompt'] = result
            d['inputs'] = dummy
            string = json.dumps(d)
            logging.info(string)
            send_to_api(string)
            return result

        return wrapper

    return wrap

def main():
    parser = argparse.ArgumentParser(prog='devcheck', description='Devcheck Command Line Interface')
    parser.add_argument('command', help='Command to run', choices=['run_tests', 'authenticate'])

    args = parser.parse_args()


    if args.command == 'run_tests':
        if not API_KEY_TEST:
            logging.error("API Key not found. Please authenticate using 'devcheck authenticate'")
            exit(1)
        run_tests()
    elif args.command == 'authenticate':
        authenticate()


if __name__ == "__main__":
    main()
