Change GitHub Repo Homepages
============================
A script to bulk-edit the homepage URLs of GitHub repos.

Usage
-----

1. Edit `changes.txt` and populate it with newline-separated changes.  On each line, put the repository `owner/repo_name` and the new homepage URL to set.
2. Enter these commands:

```bash
virtualenv --no-site-packages                # Create the virtualenv
source bin/activate                          # Enter the virtualenv
pip install -r requriements.txt              # Install required packages
python change-repo-homepages.py changes.txt  # Run the script
```

