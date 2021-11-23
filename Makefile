all: install

install:
	python3 -m pip install -r requirements.txt
	chmod u+x image-crypt
	chmod u+x image-crypt-gui
	ln -s $(PWD)/image-crypt ~/bin/image-crypt
	ln -s $(PWD)/image-crypt-gui ~/bin/image-crypt-gui

uninstall:
	rm ~/bin/image-crypt