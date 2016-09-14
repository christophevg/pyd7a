COVERAGE=PYTHONPATH=. $(shell which coverage)

TESTFILES=$(shell grep -lr TestCase d7a | grep '\.py$$')

all: clean test coverage

test:
	@echo "*** running all tests"
	-@$(COVERAGE) run -m unittest2 $(TESTFILES)

test-%:
	@echo "*** performing tests for d7a-$(subst _,/,$(subst test-,,$@))"
	$(COVERAGE) run  -m unittest2 d7a/$(subst -,/,$(subst test-,,$@))/test/*.py

coverage:
	@echo "*** generating unittest coverage report (based on last test run)"
	@$(COVERAGE) report -m --omit '/System/*,*__init__.py,*/test/*,*site-packages*,*/support/*'

clean:
	@rm -f .coverage

.PHONY: all test clean test test-% coverage
