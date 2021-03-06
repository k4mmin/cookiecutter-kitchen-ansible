#!/usr/bin/env python
from git import Repo,remote
import git
import os
import shutil
from github import Github
import os
from jinja2 import Environment, FileSystemLoader
#https://gist.github.com/wrunk/1317933/d204be62e6001ea21e99ca0a90594200ade2511e
import errno

def copydir(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def create_jenkins_config():
    # Capture working directory and generates a new working directory
    # os.path.dirname(os.getcwd())+"/jenkins/jobs/kitchen" dont work with cookiecutter
    WORKDIR = os.getcwd()
    TEMPLATEDIR = WORKDIR.rsplit('/', 2)[0]+"/jenkins/jobs/kitchen"
    NEWDIR = TEMPLATEDIR.rsplit('/', 1)[0]+"/{{cookiecutter.role_name}}"
    copydir(TEMPLATEDIR,NEWDIR)
    # Create the jinja2 environment and parse configuration file
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(NEWDIR),trim_blocks=True)
    newfile = j2_env.get_template('config.xml.tpl').render(project_name='{{cookiecutter.role_name}}')
    with open(NEWDIR+"/config.xml", "wb") as fh:
        fh.write(newfile)

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

create_jenkins_config()
