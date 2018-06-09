# Cookiecutter Ansible Role

* Development branch: [![Build Status](https://travis-ci.org/ferrarimarco/cookiecutter-ansible-role.svg?branch=development)](https://travis-ci.org/ferrarimarco/cookiecutter-ansible-role)
* Master branch: [![Build Status](https://travis-ci.org/ferrarimarco/cookiecutter-ansible-role.svg?branch=master)](https://travis-ci.org/ferrarimarco/cookiecutter-ansible-role)

[Cookiecutter](https://github.com/audreyr/cookiecutter) recipe to easily create [ansible roles](http://docs.ansible.com/playbooks_roles.html#roles).
This is a fork of the excellent [iknite/cookiecutter-ansible-role](https://github.com/iknite/cookiecutter-ansible-role)
project that I used as a starting point.

## Features

1. Follows Ansible [best practices](http://docs.ansible.com/playbooks_best_practices.html)
1. Follows Ansible Galaxy [best practices](https://galaxy.ansible.com/intro#good)
1. Only Creates the necessary files and folders
1. Blazing fast creation, forget about file creation and focus in actions
1. Lint checks ([Ansible-lint](https://github.com/willthames/ansible-lint), [yamllint](https://github.com/adrienverge/yamllint))
1. Test infrastructure already implemented ([Test-kitchen](https://github.com/test-kitchen/test-kitchen), [kitchen-ansible](https://github.com/neillturner/kitchen-ansible), [kitchen-docker](https://github.com/test-kitchen/kitchen-docker), [InSpec](http://inspec.io/) + [kitchen-inspec](https://github.com/chef/kitchen-inspec)):
  1. Test your roles against multiple platforms using the power of Docker
  1. The life cycle of each platform is automatically managed by Test-kitchen
  1. Your roles can be verified with InSpec
1. Travis-CI integration ready, with support for parallel builds: ([.travis.yml]({{cookiecutter.role_name}}/.travis.yml), [badges in README.md for development and master branches]({{cookiecutter.role_name}}/README.md))
1. Parallel test execution ready ([{{cookiecutter.role_name}}/test/scripts/test-role.sh]({{cookiecutter.role_name}}/test/scripts/test-role.sh))

## Usage

1. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter): `pip install cookiecutter`
1. `cookiecutter https://github.com/ferrarimarco/cookiecutter-ansible-role`

It will ask you questions about the structure of your role like tasks names, handlers names, and default variables. You can jump to the next question by entering an empty string.

## Test the generated role

See [README.md of the generated role]({{cookiecutter.role_name}}/README.md).

## Example
```
    ROLE CONFIGURATION:
    ===================

    Should it have tasks?  [Y/n]
      Add task name i.e (Install packages) Add some task
      Add task name i.e (Install packages) another task
      Add task name i.e (Install packages)

    Should it have handlers? [Y/n]
      Add handler name i.e (Restart uwsgi) restart something
      Add handler name i.e (Restart uwsgi) alert someone
      Add handler name i.e (Restart uwsgi)

    It should contain default variables?:  [Y/n]
      Add variable i.e (operator: : drunken_master) var: name
      Add variable i.e (operator: : drunken_master)      

    Should it have meta info?  [Y/n]
     - Should it have dependencies?  [Y/n]
        Add dependency i.e ({role: aptsupercow, var: 'value'}) {role: cool, version: latest}
        Add dependency i.e ({role: aptsupercow, var: 'value'})

    Should it have templates?  [Y/n] n

    Should it have files?  [Y/n] y

```

## What is the rationale behind this fork?

While developing roles, I always wanted to test them in an ephemeral environment.

In my first role, I just ran a quick syntax check using the `--syntax-check` switch. Then I came across [this blog post](https://www.jeffgeerling.com/blog/testing-ansible-roles-travis-ci-github) by [Jeff Geerling](https://github.com/geerlingguy) and I was able to use his approach to use Travis CI to run my role against different platforms (via Docker), while also testing the its idempotence.

That methodology had a limitation: running tests on my local Docker environment was cumbersome and not practical as the process had too many "copy-and-paste-from-.travis.yml" steps. I managed to mitigate this issue to a certain extent by moving commands from `.travis.yml` to dedicated shell scripts (that you can now find in the `test/scripts` directory).

This partially solved the issue but the `.travis.yml` still contained the environment variables that described the platforms to run against (i.e. the Docker containers). So I still had some manual steps to tackle.

Then I stumbled upon [Test-Kitchen](https://github.com/test-kitchen/test-kitchen). It's a testing framework with a plug-in interface. You can use it with various combinations of drivers (Docker, Vagrant...), provisioners (Ansible, Chef, Puppet...) and verifiers (RSpec, Serverspec, InSpec...). This completely abstracts the test environment from the "test runtime" environment, in the sense that you can run the same set of tests against different platforms, no matter the environment you use to run such tests. But wait, couldn't you just use plain docker for that? Yes, but you have to manage the life cycle of the test environments by yourself.

## Examples of roles generated with this cookiecutter
- https://github.com/ferrarimarco/ansible-role-bash-aliases
- https://github.com/ferrarimarco/ansible-role-virtualbox
