# o-------------------------------------------o
# |   William Cunningham                      |
# |   Zendesk Internship challenge            |
# |   11 / 24 / 2021                          |
# o-------------------------------------------o

# for testing the config file reading
import tempfile

# the unit test framework
import unittest

from requests.auth import AuthBase, HTTPBasicAuth

# and the file to test
import main

# used for testing syste output
import io
import sys


class TestConfigReading(unittest.TestCase):

    def setUp(self) -> None:
        # create a directory of valid and invalid config files
        self.test_dir = tempfile.TemporaryDirectory()

        # create test case config files

        # good case, token
        with open(f"{self.test_dir.name}\\tconf_0.txt", 'a') as f:
            f.writelines([
                "subdomain:a_domain\n",
                "email:an_email@email.edu\n",
                "token:some_old_token\n"
            ])

        # good case, password
        with open(f"{self.test_dir.name}\\tconf_1.txt", 'a') as f:
            f.writelines([
                "subdomain:a_domain\n",
                "email:an_email@email.edu\n",
                "password:a_password\n",
            ])

        # good case, both
        with open(f"{self.test_dir.name}\\tconf_2.txt", 'a') as f:
            f.writelines([
                "subdomain:a_domain\n",
                "email:an_email@email.edu\n",
                "password:a_password\n",
                "token:some_old_token\n"
            ])

        # bad case, no password or token
        with open(f"{self.test_dir.name}\\tconf_3.txt", 'a') as f:
            f.writelines([
                "subdomain:a_domain\n",
                "email:an_email@email.edu\n",
            ])

        # bad case, no email
        with open(f"{self.test_dir.name}\\tconf_4.txt", 'a') as f:
            f.writelines([
                "subdomain:a_domain\n",
                "token:some_old_token\n"
            ])

        # bad case, no subdomain
        with open(f"{self.test_dir.name}\\tconf_5.txt", 'a') as f:
            f.writelines([
                "token:some_old_token\n"
                "email:an_email@email.edu\n",
            ])


    def test_read_config(self):
        # good cases

        auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_0.txt")
        assert auth.username == "an_email@email.edu/token"
        assert auth.password == "some_old_token"
        assert sub == "a_domain"

        auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_1.txt")
        assert auth.username == "an_email@email.edu"
        assert auth.password == "a_password"
        assert sub == "a_domain"

        auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_2.txt")
        assert auth.username == "an_email@email.edu/token"
        assert auth.password == "some_old_token"
        assert sub == "a_domain"

        # bad cases
        try:
            auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_3.txt")
            assert False, "expected GeneralError"
        except main.GeneralError:
            pass

        try:
            auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_4.txt")
            assert False, "expected GeneralError"
        except main.GeneralError:
            pass

        try:
            auth, sub = main.read_config(f"{self.test_dir.name}\\tconf_5.txt")
            assert False, "expected GeneralError"
        except main.GeneralError:
            pass


    def tearDown(self):
        # close temp directory to delete temp files
        self.test_dir.cleanup()



class TestGetAllTickets(unittest.TestCase):
    def setUp(self) -> None:
        # set up dummy domain and auth
        main.subdomain = "test_subdomain"
        main.auth = HTTPBasicAuth('a', 'b')

    
    def test_get_all_tickets(self):
        try:
            main.get_all_tickets()
            assert False, "expected GeneralError"
        except main.GeneralError:
            pass



class TestShowPage(unittest.TestCase):
    
    def setUp(self) -> None:
        # redirect system output to a string variable
        self.output = io.StringIO()
        sys.stdout = self.output


    def test_show_page(self):
        # test that the header and dummy ticket output is good
        page_tickets = [{'id':1, 'subject':'a'}, {'id':2, 'subject':'b'}]
        trunctuated = main.show_page(page_tickets, 0, 1)
        assert self.output.getvalue() == '\n\n\n\n\nShowing page 1/2\n[id: 1] | a\n[id: 2] | b\n', f'{self.output.getvalue()}'
        assert trunctuated == False

        # test that page trunctuation activates at 26 pages
        page_tickets = [{'id':i, 'subject':'a'} for i in range(26)]
        trunctuated = main.show_page(page_tickets, 0, 1)
        assert trunctuated == True

    
    def tearDown(self) -> None:
        # reset system output to the default stream
        sys.stdout = sys.__stdout__

    

class TestShowTicket(unittest.TestCase):

    def setUp(self) -> None:
        self.tickets = [{'id':i} for i in range(100)]


    def test_show_ticket(self):
        # test 'good' input
        try:
            ret = main.show_ticket(tickets=self.tickets, id=50, immediate_breakout=True)
            assert False, "expected KeyError"
        except KeyError:
            pass

        # test bad input
        ret = main.show_ticket(tickets=self.tickets, id=-1, immediate_breakout=True)
        assert ret == False

        ret = main.show_ticket(tickets=self.tickets, id=1000, immediate_breakout=True)
        assert ret == False



class TestParseCommand(unittest.TestCase):

    def setUp(self) -> None:
        main.tickets = []


    def test_quit(self):
        try:
            main.parse_command('q', 0, 0)
            assert False, "expected SystemExit"
        except SystemExit:
            pass

        try:
            main.parse_command('quit', 0, 0)
            assert False, "expected SystemExit"
        except SystemExit:
            pass


    def test_paging(self):
        # next
        page = main.parse_command('n', 0, 0)
        assert page == 0, "page count was not clamped"

        page = main.parse_command('next', 0, 0)
        assert page == 0, "page count was not clamped"

        page = main.parse_command('next', 0, 1)
        assert page == 1, "page was not properly paged up"

        # prev
        page = main.parse_command('prev', 0, 1)
        assert page == 0, "page was not properly paged down"

        page = main.parse_command('p', 0, 0)
        assert page == 0, "page count was not clamped"

        page = main.parse_command('prev', 0, 0)
        assert page == 0, "page count was not clamped"


    def test_show_ticket_command(self):
        page = main.parse_command('42', 0, 0)
        assert page == 0



if __name__ == "__main__":
    unittest.main()