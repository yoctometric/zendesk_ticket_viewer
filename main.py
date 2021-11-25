# o-------------------------------------------o
# |   William Cunningham                      |
# |   Zendesk Internship challenge            |
# |   11 / 22 / 2021                          |
# o-------------------------------------------o

# used for handling get requests and auth
import requests
from requests.auth import AuthBase, HTTPBasicAuth


# global variables
page_size = 25

# default auth and subdomain to empty values. set by return of read_config
auth = AuthBase()
subdomain = ""


# reads authentication and account data from the config_path string. Default config.txt
# returns a requests AuthBase object and subdomain string
def read_config(config_path: str="config.txt"):
    subdomain = ""
    email = ""
    password = ""
    token = ""

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
            elif line.startswith("token:"):
                token = line.split(":")[1]

    # error checking
    if subdomain == "":
        raise Exception(f"Error: No subdomain found in {config_path}. Please specify by adding the line:\nsubdomain:your_subdomain")

    if email == "":
        raise Exception(f"Error: No subdomain found in {config_path}. Please specify by adding the line:\nemail:your_email")

    if password == "" and token == "":
        raise Exception(f"Error: No password or token found in {config_path}. Please specify by adding the line:\npassword:your_password\nor\ntoken:your_api_token")


    # make an auth object based on api_key or password. Pereference given to api token
    if token != "":
        return HTTPBasicAuth(f"{email}/token", token), subdomain
    else:
        return HTTPBasicAuth(email, password), subdomain


# returns a list of dictionaries of all the account's tickets and the number of pages of tickets
def get_all_tickets():
    print(f"Getting all tickets from {subdomain}")

    # get all of the tickets created since UNIX Epoch time
    resp = requests.get(f"https://{subdomain}.zendesk.com/api/v2/incremental/tickets/cursor.json?start_time={0}", auth=auth)
    code = resp.status_code

    # on a successful call, return the tickets array and page count
    if code == 200:
        tickets = resp.json()['tickets']
        page_count = ((len(tickets) - 1) // page_size)

        return tickets, page_count

    # otherwise, error
    raise Exception(f"Error: Request recieved error response code {code}")
    

# renders a page of tickets
def show_page(tickets: list, page: int, page_count: int):
    start = page * page_size

    # print header
    print(f"\n\n\nShowing page {page+1}/{page_count+1}")

    for i in range(start, len(tickets)):
        if i >= start + page_size:
            return # cancel after page_size tickets have been printed

        print(f"[id: {tickets[i]['id']}] | {tickets[i]['subject']}")


def show_ticket(tickets: list, id: int):
    # get the ticket from the tickets array by id. this is not limited to the current page intentionally
    ticket = None
    for t in tickets:
        if int(t['id']) == id:
            ticket = t
            break
    
    # if a ticket was found, display it and wait for any key to return
    if ticket:
        # assemble relevant fields into a string and display it
        # description, status, priority, subject, submitter

        # get the submitter's info
        resp = requests.get

        # hold user on ticket page until finished
        input("Enter to continue")
        return

    # otherwise, ticket id was out of bounds
    print(f"No ticket with id {id} was found. Please enter a vild id")

        



# parse the user input
def parse_command(command: str, page: int, page_count: int):
    command = command.lower()
    if command == 'q' or command == 'quit':
        exit()

    # if the command is an int, check for ticket id
    id = -1
    try:
        id = int(command)
    except ValueError:
        pass # int() returns a value error if the string was not parsable

    # if the id is valid, attempt to expand it
    if (id >= 0):
        show_ticket(tickets, id)
        return page
    
    # otherwise, this is a page operation. 
    if command == 'n' or command == 'next':
        page += 1
    
    elif command == 'p' or command == 'prev':
        page -= 1
    
    # if no command was recognized, explain so to the user
    else:
        print("No command recognized. Please enter a valid command")


    # clamp page 
    if page > page_count:
        page = page_count
    
    elif page < 0:
        page = 0

    return page        


if __name__ == "__main__":
    # read config
    try:
        auth, subdomain = read_config("config.txt")
    except Exception as e:
        print(e)
        exit()

    # get json data
    try:
        tickets, page_count = get_all_tickets()
    except Exception as e:
        print(e)
        exit()

    # show the first page
    page = 0
    show_page(tickets, page, page_count)

    # enter main loop
    while (True):
        command = input("q->quit, n->next page, p->prev page. Enter a ticket id to expand: ")
        page = parse_command(command, page, page_count)

        # show page
        show_page(tickets, page, page_count)

