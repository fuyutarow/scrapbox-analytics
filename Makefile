build:
	brew install pyenv pipx
	pipx install poetry
	poetry install

count:
	poetry run 	python count.py
