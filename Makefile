PYTHON=PYTHONPATH=. python
COVERAGE=$(shell which coverage)

PYTHONFILES=$(shell find d7a -name '*.py')

NOSE=/usr/lib/python2.7/dist-packages/nose/core.py

all: clean test coverage

test:
	@echo "*** running all tests"
	@$(PYTHON) $(COVERAGE) run --append $(NOSE) ${PYTHONFILES}
	
test-%: 
	@echo "*** performing tests for d7a-$(subst _,/,$(subst test-,,$@))"
	@$(PYTHON) $(COVERAGE) run --append $(NOSE) d7a/$(subst -,/,$(subst test-,,$@))/test/*.py

coverage:
	@echo "*** generating unittest coverage report (based on last test run)"
	@$(COVERAGE) report -m --omit '*__init__.py,*/test/*,*site-packages*,*/support/*'

clean:
	@rm -f .coverage

.PHONY: all test clean test test-% coverage
