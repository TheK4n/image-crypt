SCNAME = image-crypt
SCGNAME = image-crypt-gui
DESTDIR :=
PREFIX := /usr/local

all: install

install:
	python setup.py install '--prefix=$(PREFIX)' '--root=$(DESTDIR)'
	install -Dm755 $(SCNAME) $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	install -Dm755 $(SCGNAME) $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	rm -f $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md src/preview.png src/mainwindow.ui
