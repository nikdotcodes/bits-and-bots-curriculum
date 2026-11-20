.PHONY: all pdf slides html html-slides check clean
all: pdf slides html
pdf:
	python3 scripts/build.py pdf
slides:
	python3 scripts/build.py slides
html:
	python3 scripts/build.py html
html-slides: html
check:
	python3 scripts/build.py check
clean:
	rm -rf build
