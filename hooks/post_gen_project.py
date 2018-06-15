#!/usr/bin/env python
from git import Repo,remote
import git
import os
import shutil
from github import Github

#clone repository
Repo.clone_from('{{cookiecutter.ansible_url}}', '{{cookiecutter.role_name}}', branch='master')

#copy all files from repository to working directory (cannot clone into not empty directory)
path = os.getcwd()+"/{{cookiecutter.role_name}}/"
moveto = os.getcwd()+"/"
files = os.listdir(path)
files.sort()
for f in files:
    src = path+f
    dst = moveto+f
    shutil.move(src,dst)
os.rmdir('{{cookiecutter.role_name}}')
shutil.rmtree(os.getcwd()+'/.git')

#create new repo if credentials are defined
try:
    os.environ['gittoken']
except (NameError,KeyError), e:
    pass
else:
    print("Variable is defined.")
    #create a repo using name/pass or token
    #g = Github(os.environ['gituser'], os.environ['gitpass'])
    g = Github(os.environ['gittoken'])
    u = g.get_user()
    u.create_repo('{{cookiecutter.repo_name}}')

    # create working directory repo
    git.Repo.init(os.getcwd())

    # get working diretory repo
    repo = git.Repo(os.getcwd())
    # add files, remote, commit and push
    repo.git.add('.')
    repo.index.commit("wei commit")
    remote = repo.create_remote('origin', url='https://'+os.environ['gituser']+':'+os.environ['gitpass']+'@github.com/'+'{{cookiecutter.github_user}}'+'/'+'{{cookiecutter.repo_name}}'+'.git')
    remote.push(refspec='{}:{}'.format('master', 'origin'))
