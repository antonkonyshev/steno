PYTHON=python
PYI=pyi-build
APPMODULE=steno/steno.py
SPECFILE=pyi/steno.spec
SOURCES=steno/defaults.py steno/dialogs.py steno/droptargets.py steno/events.py steno/ids.py steno/__init__.py steno/player_content.py steno/player_gui.py steno/player.py steno/player_settings.py steno/steno.py steno/translator.py steno/verificator.py steno/widgets.py
GITCONFIGS=.gitignore.default

.PHONY: clean start build gitconf install uninstall test all

all: test

clean:
	rm -rf build dist steno/*.pyc steno/test/*.pyc Steno.egg-info

start: $(SOURCES)
	$(PYTHON) $(APPMODULE)

build: $(SOURCES) $(SPECFILE)
	PYTHONPATH=. $(PYI) $(SPECFILE)

sdist: $(SOURCES) setup.py
	python setup.py sdist

gitconf: $(GITCONFIGS)
	$(shell for config in $(GITCONFIGS); do cp -n "$${config}" "$${config%.default}"; done)

install: $(SOURCES) setup.py
	$(PYTHON) setup.py install

test:
	PYTHONPATH=steno $(PYTHON) -m unittest discover -v -s steno
