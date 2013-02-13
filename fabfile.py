# -*- coding: utf-8 -*-
# Author Artem keeper Melanich

from fabric.api import *

# globals

hosts=[{
          'login'  : "user@server",
          'path'    : "/path/to/repo",
          'os'      : 'freebsd',
          'name'    : 'production'}, ]  # Used like a remote name
env.project_name='matrasi'
env.dev_branch='dev'
env.master_branch='master'
env.test_branch='test'
env.production_remotes=['production', ]
env.production_remote_branch='master'




# tasks

def test():
    """
    Коммит изменений в тестовую ветку и запуск теста
    """
    commit()
    merge_dev_to_test()
    local("python manage.py test")


def deploy(host=None, fake=False, update=True):
    """
    Push code to all remotes (servers), update virtualenvs, collect static,
    make migrations, restart wsgi daemon
    """
    if fake=='True': fake=True
    if not fake:
        deploy(host=host, fake=True, update=update)
        prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')  # тут можно прервать init
    if host is not None:
        local_run('git push -f %s %s'%(host['name'], env.production_remote_branch), fake=fake)
        if update: update_site(host, fake=fake)
    else:
        for host in hosts:
            deploy(host, fake=fake)

def commit():
    """
    Коммит изменений.
    """
    with settings(warn_only=True):
        local('git status')
        prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')  # тут можно прервать коммит,
            # если в него попали ненужные файлы или наоборот
        local('git add .')
        local('git commit')  # тут вылазит консольный редактор и можно ввести комментарий

def remote_init(fake=False):
    """
    Init remote repo and setup env
    """
    if fake=='True': fake=True
    if not fake:
        remote_init(fake=True)
        prompt('Press <Enter> to continue or <Ctrl+C> to cancel.')  # тут можно прервать init
    for host in hosts:
        # init remote repos
        remote_run('mkdir -p %s'%host['path'], cd=False, fake=fake, host=host)
        remote_run('git init', fake=fake, host=host)
        remote_run('git config receive.denyCurrentBranch ignore', fake=fake, host=host)
        # init remotes in our repo to push to
        try:
            local_run('git remote add %s ssh://%s%s'%(host['name'], host['login'], host['path']), fake=fake)
        except:
            local_run('git remote rm %s'%host['name'], fake=fake)
            local_run('git remote add %s ssh://%s%s'%(host['name'], host['login'], host['path']), fake=fake)
        deploy(host, fake=fake, update=False)
        remote_run('virtualenv --no-site-packages env', fake=fake, host=host)
        remote_run('cp Makefile.def.sample Makefile.def', fake=fake, host=host)
        update_site(host, fake=fake)


# Helpers. These are called by other functions rather than directly

def local_run(cmd, fake=False):
    if fake:
        print cmd
    else:
        local(cmd)

def update_site(host=None, fake=False):
    remote_run('git reset --hard', fake=fake, host=host)
    remote_run('make update', fake=fake, host=host)

def remote_run(cmd, cd=True, fake=False, host=None):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.
    
    Note:: Fabric (and paramiko) can't forward your SSH agent. 
    This helper uses your system's ssh to do so.
    """
    if host:
        if host['os']=="freebsd" and cmd.split(" ")[0]=='make':
            # Hack for FreeBSD make to use GMake
            cmdsp=cmd.split(" ")
            cmdsp[0]="gmake"
            cmd=" ".join(cmdsp)
        if cd:
            # cd to default dir first
            cmd="cd %s; %s"%(host['path'], cmd)
        if fake:
            print "[%s]: %s"%(host['login'], cmd)
            return

        try:
            # catch the port number to pass to ssh
            host, port=host['login'].split(':')
            local('ssh -p %s -A %s "%s"'%(port, host, cmd))
        except ValueError:
            local('ssh -A %s "%s"'%(host['login'], cmd))
    else:
        for host in hosts: remote_run(cmd=cmd, fake=fake, host=host)



def merge_dev_to_test(with_return=True):
    """
    Слияние изменений из разработки в тестовую ветку.
    """
    local('git checkout %s'%env.test_branch)  # переход в тестовую ветку
    local('git merge --no-ff %s'%env.dev_branch)  # слияние с веткой разработки

    if with_return:
        local('git checkout %s'%env.dev_branch)  # опциональное возвращение назад
