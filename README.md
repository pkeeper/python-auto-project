python-auto-project
===================

Automatization helpers for Python\Django projects

ver: 0.1

This project is in early Alpha!
Use it with caution. Code review advised before use.
Questions, suggestions and pull requests are welcome!

Instalation:
------------
I know it's Ugly but thats how it is for now.
Just copy all files into your project.
Edit settings for a project in fabfile.py and Makefile.def.sample.
Install requirements.

Usage:
------
Init remote repos (shows commands before execution)
```
fab remote_init
```

Update remote repos with latest code
```
fab deploy
```

TODO:
-----
- [ ] initial deployment ability (done at 80%)
    - [ ] set up ssh key
    - [x] set up remote repo
    - [x] push to remote repo
    - [x] set up virtual env
    - [ ] set up remote settings
    - [x] init remote Django Project (install requirements, collect static, syncdb, touch wsgi.py)    
- [x] code redeploy (update)
- [ ] replace Makefile with fab script
- [ ] get settings out of the scripts
- [ ] integrate git-django-hooks
- [ ] make instalation with one command and set up as a PIP project
