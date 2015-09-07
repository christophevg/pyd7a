PYTHON=PYTHONPATH=. python
COVERAGE=`which coverage`

MODULES=atp
TESTS=$(addprefix test-,${MODULES})

all: clean test coverage

test: ${TESTS}

test-%: 
	@echo "*** performing tests for d7-$(subst test-,,$@)"
	@$(PYTHON) $(COVERAGE) run d7a/$(subst test-,,$@)/test/all.py;	\

coverage:
	@echo "*** generating unittest coverage report (based on last test run)"
	@$(COVERAGE) report -m --omit '*__init__.py,*/test/*'

clean:

.PHONY: all test clean test test-%
