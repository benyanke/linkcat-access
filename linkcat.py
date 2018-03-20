#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# Handles interaction with linkcat (South Central Wisconsin Library System online tool)
class linkcat:

  logged_in = False
  username = None
  password = None

  debug = True

  checked_out_books = None
  all_books = None

  # Session handler
  session = None

  # Urls
  ROOT_URL        = "https://www.linkcat.info"
  LOGIN_URL       = "/cgi-bin/koha/opac-user.pl"
  LOOUT_URL       = "/cgi-bin/koha/opac-main.pl?logout.x=1"
  USER_INFO_URL   = "/cgi-bin/koha/opac-userupdate.pl"
  CHECKED_OUT_URL = "/cgi-bin/koha/opac-user.pl"

  # Login
  def __init__(self, u, pw):
    self.username = u
    self.password = pw

    # Setup sessions handler for requests without logging in again
    self.session = requests.Session()
    self.try_login()


  # Logs in and populates the object with the session cookie
  def try_login(self):

    # Attempt login
    r = self.session.post(self.ROOT_URL + self.LOGIN_URL, verify=False, data={'userid': self.username, 'password': self.password, 'koha_login_context': 'opac', 'Submit':'Log In'})

    # Get login cookie
    cookies = self.session.cookies.get_dict();
    if 'CGISESSID' in cookies:
      self.cookie = cookies['CGISESSID']
      if self.debug:
        print("Login suceess")
      self.logged_in = True
      return True

    else:
      if self.debug:
        print("Login failure")
      return False

  # returns checked out books
  def logout():
     self.session.get(self.ROOT_URL + self.LOGOUT_URL, verify=False)


  # returns checked out books
  def get_checked_out_books(self):
     if not self.logged_in:
       print("Not logged in!")
       return False

     page = self.session.get(self.ROOT_URL + self.CHECKED_OUT_URL, verify=False)
     soup = BeautifulSoup(page.content, 'lxml')

     table = soup.find('table', attrs={'id':'checkoutst'})
     table_head = table.find('thead')
     table_body = table.find('tbody')

     books = []

     # Loop through rows
     for row in table_body.find_all('tr'):

       row_data = {}

       row_data['title'] = row.find_all('td')[1].a.get_text().lstrip().rstrip()

       # Cleanup title
       if row_data['title'].endswith(":") or row_data['title'].endswith("/"):
         row_data['title'] = row_data['title'][:-2]

       row_data['author'] = row.find_all('td')[1].span.get_text().lstrip().rstrip()
       row_data['call_no'] = row.find_all('td')[2].get_text().lstrip().rstrip()
       row_data['due'] = row.find_all('td')[3].get_text().lstrip().rstrip()


       # This renewal count data is not fully tested, due to lack of data, but it seems to work
       raw_renewal_data = row.find_all('td')[4].span.get_text().lstrip().rstrip()
       row_data['renewals_total'] = int(raw_renewal_data.split(" of ")[1].split(" renewals remaining")[0].lstrip().rstrip())
       row_data['renewals_available'] = int(raw_renewal_data.split(" of ")[0][1:].lstrip().rstrip())
       row_data['renewals_used'] = row_data['renewals_total'] - row_data['renewals_available'];

       del row_data['renewals_total'];

       books.append(row_data)

     return books


# Run commands
lc = linkcat("LIB-CARD-NO", "PASSWORD")

co_books = lc.get_checked_out_books()
print(co_books)
