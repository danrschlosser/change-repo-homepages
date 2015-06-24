import getpass
import requests
from sys import argv, exit
import os.path
import json

# Validate Input
if len(argv) != 2:
	print "Usage: python {} <changes_file>".format(argv[0])
	exit(1)

changes_filename = argv[1]

if not os.path.isfile(changes_filename):
	print "No such file {}".fomrat(changes_filename)
	exit(1)

print "Please input your GitHub Credentials."

# Repeatedly ask for username / password combos until we get one that works.
status = -1
while status != 200:
	username = raw_input("Username: ")
	password = getpass.getpass()
	resp = requests.get('https://api.github.com/user', auth=(username, password))
	status = resp.status_code
	if status != 200:
		print "Invalid username / password combination, please try again."

# Loop over changes_file and perform changes
num_changed = 0
with open(changes_filename, 'r') as changes_file:
	for line_no_m1, line in enumerate(changes_file):

		# Skip blank lines or commented out lines
		line = line.strip()
		if not line or line[0] == '#':
			continue

		# Validate line
		tokens = line.split()
		if len(tokens) != 2:
			if len(tokens) == 1:
				error = "Missing token"
			else:
				error = "Too many tokens"
			print "Error on line {}: {}".format(line_no_m1 + 1, error)
			continue
		path, new_url = tokens

		# Get the original repo data
		gh_url = 'https://api.github.com/repos/{}'.format(path)
		resp = requests.get(gh_url, auth=(username, password))
		if resp.status_code != 200:
			print "Error GETing {}: {}".format(path, resp.json()['message'])
			print resp.json()
			exit(1)

		# Update the repo data
		repo_data = resp.json()
		old_url = repo_data.get('homepage')
		repo_data['homepage'] = new_url

		# Send the updates
		resp = requests.patch(gh_url,
				        	  auth=(username, password),
				        	  data=json.dumps(repo_data))
		if resp.status_code == 200:
			print "[{}]: {} -> {}".format(path, old_url, new_url)
			num_changed += 1
		else:
			print "Error PATCHing {}: {}".format(path, resp.json()['message'])
			print resp.json()
			exit(1)

print "Updated {} repos".format(num_changed)
