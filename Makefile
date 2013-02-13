SHELL=/bin/bash

# Project settings

PROJECT_NAME=djangoprojectname
TEST_APP=djangoprojectname

# constants

PY=python
PIP=pip
MAKE=make

BIND_TO=0.0.0.0
BIND_PORT=8000

-include Makefile.def

# additional constants

MANAGE=$(PY) manage.py

# end of constants



# targets

run:
	@echo Starting $(PROJECT_NAME) ...
	$(MANAGE) runserver $(BIND_TO):$(BIND_PORT)

mailserver:
	python -m smtpd -n -c DebuggingServer localhost:1025

syncdb:
	@echo Syncing...
	$(MANAGE) syncdb --noinput
	$(MANAGE) migrate
#	$(MANAGE) loaddata base_initial_data.json 
	@echo Done
	
createsuperuser:
	$(MANAGE) createsuperuser
	
shell:
	@echo Starting shell...
	$(MANAGE) shell

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_APP)

clean:
	@echo Cleaning up...
	find ./ | grep '\.pyc$$' | xargs -I {} rm {}
	@echo Done

manage:
ifndef CMD
	@echo Please, spceify -e CMD=command argument to execute
else
	$(MANAGE) $(CMD)
endif


only_migrate:
ifndef APP_NAME
	$(MANAGE) migrate
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

migrate_fake:
	$(MANAGE) migrate --fake

migrate:
ifndef APP_NAME
	$(MANAGE) migrate
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

init_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting init migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --initial
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif


collectstatic:
	$(MANAGE) collectstatic --noinput

help:
	@cat readme.txt
	
update:
	$(PIP) install -r requirements.txt
	$(MAKE) syncdb
	$(MAKE) collectstatic
	touch $(PROJECT_NAME)/wsgi.py

fake_update:
	echo $(PIP) install -r requirements.txt
	echo $(MAKE) syncdb
	echo $(MAKE) collectstatic
	echo touch $(PROJECT_NAME)/wsgi.py