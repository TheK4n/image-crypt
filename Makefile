all: install

install:
	python3 -m pip install -r requirements.txt
	chmod u+x image-crypt
	ln -s $(PWD)/image-crypt ~/bin/image-crypt

uninstall:
	rm ~/bin/image-crypt