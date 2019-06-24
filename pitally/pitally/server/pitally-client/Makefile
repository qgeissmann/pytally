all: dist/index.html

dist/index.html: $(shell find ./src -type f)
	yarn build || npm run build && npm run build

clean:
	rm -rf dist/



