SCNAME = image-crypt
SCGNAME = image-crypt-gui
DESTDIR :=
PREFIX := /usr/local

all: install

reqs:
	python3 -m pip install -r requirements.txt

install:
	chmod 755 $(SCNAME) $(SCGNAME)
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	ln -s $(PWD)/$(SCNAME) $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	ln -s $(PWD)/$(SCGNAME) $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

uninstall:
	rm $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	rm $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md src/preview.png src/mainwindow.ui
