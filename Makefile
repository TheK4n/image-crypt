SCNAME = image-crypt
SCGNAME = image-crypt-gui
DESTDIR :=
PREFIX := /usr/local

.PHONY: all install uninstall

all: install

install:
	python setup.py install '--prefix=$(PREFIX)' '--root=$(DESTDIR)'
	install -Dm755 $(SCNAME) $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	install -Dm755 $(SCGNAME) $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)
	install -Dm644 LICENSE $(DESTDIR)$(PREFIX)/share/licenses/image-crypt/LICENSE

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/$(SCNAME)
	rm -f $(DESTDIR)$(PREFIX)/bin/$(SCGNAME)
	rm -rf $(DESTDIR)$(PREFIX)/share/licenses/image-crypt
