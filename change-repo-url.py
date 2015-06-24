import getpass
import requests

print "Please input your GitHub Credentials."
username = raw_input("Username: ")
password = getpass.getpass()

resp = requests.get('https://api.github.com/user', auth=(username, password))
print resp.status_code
print resp.json()