PREFIX = ~/.local/bin
SCNAME = image-crypt
SCGNAME = image-crypt-gui

all: install

install:
	mkdir -p $(PREFIX) || true
	python3 -m pip install -r requirements.txt
	chmod u+x $(SCNAME) $(SCGNAME)
	ln -s $(PWD)/$(SCNAME) $(PREFIX)/$(SCNAME)
	ln -s $(PWD)/$(SCGNAME) $(PREFIX)/$(SCGNAME)

uninstall:
	rm $(PREFIX)/$(SCNAME) || true
	rm $(PREFIX)/$(SCGNAME)

clean:
	rm -rf images .github .git .gitignore LICENSE README.md src/preview.png src/mainwindow.ui
