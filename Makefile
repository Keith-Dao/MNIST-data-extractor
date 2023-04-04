python := python
pip := pip
pip_flags := --require-virtualenv

.PHONY: install clean
.DEFAULT_GOAL := default
default:
	@ echo "Please provide a command."

.env:
	$(python) -m venv .env

install: 
	$(pip) $(pip_flags) install --upgrade pip
	$(pip) $(pip_flags) install -r requirements.txt

clean:
	rm -rf .env
