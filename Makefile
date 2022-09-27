SCNAME = image-crypt
SCGNAME = image-crypt-gui
DESTDIR :=
PREFIX := /usr/local

all: install

reqs:
	python3 -m pip install -r requirements.txt

install:
	install -Dm755 $(SCNAME) $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	install -Dm755 $(SCGNAME) $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

uninstall:
	rm $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	rm $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md src/preview.png src/mainwindow.ui
