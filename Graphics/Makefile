INTERPRETER=python
PACMAN=pip

.ONESHELL:

activate=. .venv/bin/activate

define install_task =
if [ -d '.venv' ]
then
    echo "Using existing .venv as virtual environment"
else
    python3 -m venv .venv
fi
. .venv/bin/activate
pip install -r dev-requirements.txt
endef

install: ; $(value install_task)

run:
	$(activate) ; $(INTERPRETER) src/main.py