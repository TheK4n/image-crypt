PREFIX = ~/.local/bin
SCNAME = image-crypt
SCGNAME = image-crypt-gui

all: install

install:
	mkdir -p $(PREFIX) || true
	python3 -m pip install -r requirements.txt || true
	chmod u+x $(SCNAME) $(SCGNAME) || true
	ln -s $(PWD)/$(SCNAME) $(PREFIX)/$(SCNAME) || true
	ln -s $(PWD)/$(SCGNAME) $(PREFIX)/$(SCGNAME) || true

uninstall:
	rm $(PREFIX)/$(SCNAME) || true
	rm $(PREFIX)/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md src/preview.png src/mainwindow.ui
