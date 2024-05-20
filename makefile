PY=python3.8
SRC=pipe.py

TESTS=$(wildcard tests/*.txt)
DIFFS=$(patsubst tests/%.txt, tests/%.diff, $(TESTS))

run: $(SRC)
	@ $(PY) $(SRC)

test: clean $(DIFFS)

.PRECIOUS: tests/%.myout
tests/%.diff: tests/%.out tests/%.myout
	-@diff $^ > $@

tests/%.myout: tests/%.txt $(SRC)
	@echo $@ >> tests/err.myout
	-@$(PY) $(SRC) < $< > $@ 2>> tests/err.myout

clean:
	-$(RM) tests/*.myout
	-$(RM) tests/*.diff

view:
	@cd Visualizador && $(PY) visualizer.py
