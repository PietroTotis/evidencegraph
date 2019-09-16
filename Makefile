.PHONY: all virtualenv install-requirements download-spacy-data-de download-spacy-data-en test run-minimal-de run-minimal-en eval-minimal-de eval-minimal-en

VIRTUALENV_DIR=./env

virtualenv:
	if [ ! -e "${VIRTUALENV_DIR}/bin/pip" ]; then virtualenv --python=python3.6 ${VIRTUALENV_DIR}; fi

install-requirements: virtualenv
	${VIRTUALENV_DIR}/bin/pip install --upgrade pip
	${VIRTUALENV_DIR}/bin/pip install --upgrade wheel
	cat requirements.txt | xargs -n 1 -L 1 ${VIRTUALENV_DIR}/bin/pip install
	${VIRTUALENV_DIR}/bin/python setup.py develop

download-spacy-data-de:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python -m spacy download de_core_news_md
download-spacy-data-en:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python -m spacy download en_core_web_lg
download-spacy-data-it:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python -m spacy download it_core_news_sm

test:
	${VIRTUALENV_DIR}/bin/py.test -v --cov=src src

run-minimal-it:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -l it | tee "data/m112it-test-adu-simple-noop|equal.log"

run-minimal-en:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -l en | tee "data/m112en-test-adu-simple-noop|equal.log"

run-minimal-de:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -l de | tee "data/m112de-test-adu-simple-noop|equal.log"

run-complete-it:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -c -l it | tee "data/m112it-test-adu-simple-noop|equal.log"

run-complete-en:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -c -l en | tee "data/m112en-test-adu-simple-noop|equal.log"

run-complete-de:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/run.py -c -l de | tee "data/m112de-test-adu-simple-noop|equal.log"


eval-minimal-it:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/eval_minimal.py -l it | tee data/m112it-test-evaluation.log

eval-minimal-en:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/eval_minimal.py -l en | tee data/m112en-test-evaluation.log

eval-minimal-de:
	stdbuf -o 0 ${VIRTUALENV_DIR}/bin/python src/experiments/eval_minimal.py -l de | tee data/m112de-test-evaluation.log
