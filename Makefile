.DEFAULT_GOAL := all
.PHONY: css pdf all

css:
	sass -s compressed --no-source-map css/cv.sass css/cv.css

all: css
