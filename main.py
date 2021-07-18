import json
import subprocess

import requests


def run(org, access_token):
    base_url = "https://api.github.com/orgs/" + org + "/repos?access_token=" + access_token
    response = requests.get(base_url)
    json_res = response.text
    repos = json.loads(json_res)
    repo_list = []
    for repo in repos:
        repo_list.append(repo['name'])

    return repo_list


if __name__ == '__main__':

    with open("./config.json", 'r') as f:
        config = json.load(f)

    organization = config['organization']
    access_token = config['github_access_token']
    write_to_directory = config.get('directory', '../')

    repo_name = run(organization, access_token)

    for name in repo_name:
        bashCommand = "cd " + write_to_directory + ";git clone git@github.com:" + organization + "/" + name + ".git;" \
                      + "git fetch --all"
        print(bashCommand)
        rc = subprocess.run(bashCommand, capture_output=True, shell=True)
        print(rc.stdout)
