from bs4 import BeautifulSoup as beauty
import cloudscraper
import random
import string
import json
scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
f = open('used_names.txt', 'r')
used_names = f.read().split(',')
run_amount = ''
c_amount = ''


def input_q():
    global run_amount
    global c_amount
    run_amount = input("How Many Names Do You Want To Generate?: ")
    c_amount = input("How Many Characters?: ")


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    return result_str


def generate_names():
    available_names = 0
    for i in range(int(run_amount)):
        currentName = get_random_string(int(c_amount))
        url = f"https://www.modd.io/api/user/getuserdetailbyname/{currentName}"
        info = scraper.get(url).text
        soup = beauty(info, "html.parser")
        soup = soup.find_all('script')
        if "success" not in info:
            if currentName not in used_names:
                available_names += 1
                file1 = open("used_names.txt", "a")
                file1.write(currentName + ",")
                file1.close()
                used_names.append(currentName)
                jsonString = json.dumps(info)
                jsonFile = open("available_names.json", "a")
                jsonFile.write(
                    f"Username: {currentName}" + "\n")
                jsonFile.close()
                print(f"The Username: {currentName} Is Available")
            else:
                print(currentName + " Is Already Used.")
        else:
            print(f"Username {currentName} Already Exists.")
    print(f"Generated {available_names} Names!")
    generateOnceMore()


def generateOnceMore():
    generate_again = input("Do You Want To Generate More?(yes/no): ").lower()
    if generate_again == "yes":
        input_q()
        generate_names()
    elif generate_again == "no":
        return
    else:
        print("Please Type Yes/No.")
        generateOnceMore()


input_q()
generate_names()