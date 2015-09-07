PYTHON=PYTHONPATH=. python
COVERAGE=`which coverage`

MODULES=atp
TESTS=$(addprefix test-,${MODULES})

all: clean test

test: ${TESTS}

test-%: 
	@echo "*** performing tests for d7-$(subst test-,,$@)"
	@$(PYTHON) $(COVERAGE) run d7a/$(subst test-,,$@)/test/all.py;	\

clean:

.PHONY: all test clean test test-%
