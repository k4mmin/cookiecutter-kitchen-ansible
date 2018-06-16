#!/usr/bin/env python
import os
from jinja2 import Environment, FileSystemLoader
#https://gist.github.com/wrunk/1317933/d204be62e6001ea21e99ca0a90594200ade2511e

# Capture working directory
#WORKDIR = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.getcwd()+"/volumes/jenkins/jobs/kitchen"

def create_jenkins_config():
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(WORKDIR),trim_blocks=True)
    newfile = j2_env.get_template('config.xml.tpl').render(project_name='{{cookiecutter.role_name}}')
    with open(WORKDIR+"/config.xml", "wb") as fh:
        fh.write(newfile)

# if __name__ == '__main__':
