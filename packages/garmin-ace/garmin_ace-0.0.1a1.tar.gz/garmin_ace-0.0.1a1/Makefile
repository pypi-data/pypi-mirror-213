.PHONY: clean test coverage

clean:
	rm -rf *~ __pycache__ htmlcov

test: clean
	python3 -m unittest discover

coverage: clean
	coverage run -m unittest discover
	coverage report
	coverage html
