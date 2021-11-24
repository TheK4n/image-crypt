PREFIX = ~/bin
SCNAME = image-crypt
SCGNAME = image-crypt-gui

all: install

install:
	python3 -m pip install -r requirements.txt
	chmod u+x $(SCNAME) $(SCGNAME)
	ln -s $(PWD)/$(SCNAME) $(PREFIX)/$(SCNAME)
	ln -s $(PWD)/$(SCGNAME) $(PREFIX)/$(SCGNAME)

uninstall:
	rm $(PREFIX)/$(SCNAME)
	rm $(PREFIX)/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md requirements.txt
