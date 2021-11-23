# o-------------------------------------------o
# |   William Cunningham                      |
# |   Zendesk Internship challenge            |
# |   11 / 22 / 2021                          |
# o-------------------------------------------o

# used for handling get requests and auth
import requests
from requests.auth import HTTPBasicAuth


# global variables
page_size = 25


# reads authentication and account data from the config_path string. Default config.txt
# returns a requests AuthBase object and subdomain string
def read_config(config_path="config.txt"):
    subdomain = ""
    email = ""
    password = ""

    with open(config_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()

            # get each parameter from the file
            if line.startswith("subdomain:"):
                subdomain = line.split(":")[1]
            elif line.startswith("email:"):
                email = line.split(":")[1]       
            elif line.startswith("password:"):
                password = line.split(":")[1]

    # error checking
    if subdomain == "":
        raise Exception(f"Error: No subdomain found in {config_path}. Please specify by adding the line:\nsubdomain:your_subdomain")

    if email == "":
        raise Exception(f"Error: No subdomain found in {config_path}. Please specify by adding the line:\nemail:your_email")

    if password == "":
        raise Exception(f"Error: No password found in {config_path}. Please specify by adding the line:\npassword:your_password")

    # make an auth obhect
    auth = HTTPBasicAuth(email, password)
    
    return auth, subdomain


# returns a list of dictionaries of all the account's tickets and the number of pages of tickets
def get_all_tickets(auth, subdomain):
    print(f"Getting all tickets from {subdomain}")

    data = requests.get(f"https://{subdomain}.zendesk.com/api/v2/tickets.json", auth=auth)

    code = data.status_code

    # on a successful call, return the tickets list and number of pages
    if code == 200:
        tickets = data.json()['tickets']
        return tickets, (len(tickets) - 1) // page_size
    
    # otherwise, error
    raise Exception(f"Error: Request recieved error response code {code}")
    

# renders a page of tickets
def show_page(tickets, page, page_count):
    start = page * page_size

    # print header
    print(f"\n\n\nShowing page {page+1}/{page_size+1}")

    for i in range(start, len(tickets)):
        if i >= start + page_size:
            return # cancel after page_size tickets have been printed

        print(f"[{i+1}] id: {tickets[i]['id']} | {tickets[i]['subject']}")


# parse the user input
def parse_command(command):
    if command == 'q' or command == 'quit':
        exit()


if __name__ == "__main__":
    # read config
    try:
        auth, subdomain = read_config("config.txt")
    except Exception as e:
        print(e)
        exit()

    # get json data
    try:
        tickets, page_count = get_all_tickets(auth, subdomain)
    except Exception as e:
        print(e)
        exit()

    show_page(tickets, 0, page_count)
    # enter main loop

    while (True):
        command = input("(q/quit) to exit, (prev/p) for previous page, (next/n) for next page:")
        parse_command(command)
