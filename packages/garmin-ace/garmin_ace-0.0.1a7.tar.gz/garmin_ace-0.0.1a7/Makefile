.PHONY: clean test coverage

clean:
	rm -rf *~ __pycache__ htmlcov dist/

test: clean
	python3 -m unittest discover tests/

coverage: clean
	coverage run -m unittest discover tests/
	coverage report
	coverage html

release: test
	python3 -m build
	twine upload dist/garmin_ace-*
