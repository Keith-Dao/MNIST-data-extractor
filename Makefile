python := python
pip := pip

.PHONY: install clean
.DEFAULT_GOAL := default
default:
	@ echo "Please provide a command."

.env:
	$(python) -m venv .env

install: 
	$(pip) install --upgrade pip
	$(pip) install -r requirements.txt

clean:
	rm -rf .env
