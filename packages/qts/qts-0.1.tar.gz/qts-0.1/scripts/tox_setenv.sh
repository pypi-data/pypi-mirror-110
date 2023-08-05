#!/bin/bash

echo "    pyqt-5: QTS_MYPY_ARGUMENTS="$(venv/bin/qts mypy args --wrapper pyqt5)
echo "    pyqt-6: QTS_MYPY_ARGUMENTS="$(venv/bin/qts mypy args --wrapper pyqt6)
echo "    pyside-5: QTS_MYPY_ARGUMENTS="$(venv/bin/qts mypy args --wrapper pyside2)
echo "    pyside-6: QTS_MYPY_ARGUMENTS="$(venv/bin/qts mypy args --wrapper pyside6)
