build:
	brew install pipx
	pipx install poetry
	poetry install

count:
	poetry run 	python count_pages.py
