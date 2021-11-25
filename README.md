# Zendesk Ticket Viewer
### A command line ticket viewer created by William Cunningham for the Zendesk internship coding challenge
!["splash image"](splash.png)
## Installation
1. git clone or download the repository
2. in your terminal, navigate to main.py in the zendesk_ticket_veiwer directory
3. ensure you have python 3.9 installed
4. if the `requests` library is not installed for your python version, run `python -m pip install requests`
5. set up config.txt with your credentials
    * add your subdomain and email
    * either add your password or an api token. If both are added the program will just use the token
    * example config.txt file:
      `subdomain:zccwillcsquared
      
email:will********@gmail.com

token:******************************xduMNi`
7. run `python main.py`


## Unit testing
1. in your terminal, navigate to main.py in the zendesk_ticket_veiwer directory
2. run `python tests.py`
