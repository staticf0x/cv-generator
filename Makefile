.DEFAULT_GOAL := all
.PHONY: css pdf all

css:
	sass -s compressed --no-source-map css/cv.sass css/cv.css

pdf:
	python3 build.py

clean:
	rm -r _build

clean-all:
	rm -r _build
	rm -r output

all: css pdf
