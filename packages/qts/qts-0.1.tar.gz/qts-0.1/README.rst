qts - use the Qt you've got
+++++++++++++++++++++++++++

Resources
=========

=================================  =================================  =============================

`Documentation <documentation_>`_  `Read the Docs <documentation_>`_  |documentation badge|
`Issues <issues_>`_                `GitHub <issues_>`_                |issues badge|

`Repository <repository_>`_        `GitHub <repository_>`_            |repository badge|
`Tests <tests_>`_                  `GitHub Actions <tests_>`_         |tests badge|

`Distribution <distribution_>`_    `PyPI <distribution_>`_            | |version badge|
                                                                      | |python versions badge|
                                                                      | |python interpreters badge|

=================================  =================================  =============================


Introduction
============

.. note::

   qts is presently an exploratory project.
   It does have test coverage and is significantly documented.
   It only covers a few Qt modules.

qts is a Qt5/6 and PyQt/PySide compatibility layer for your libraries and applications.
It is designed to work with mypy and includes a CLI utility to notify mypy of the needed conditions.
To keep the scope reasonable, qts will focus on the variances that all code using Qt will need such as imports and signals.
Nuanced detailed differences will not be abstracted away.
Helper functions and similar may be provided on a case by case basis.

.. code-block:: python

    import qts
    import qts.util


    def main():
        qts.set_wrapper(qts.available_wrappers()[0])

        from qts import QtWidgets

        application = QtWidgets.QApplication([])
        widget = QtWidgets.QLabel("this is qts")
        widget.show()
        qts.util.exec(application)

    main()


.. _documentation: https://qts.readthedocs.io
.. |documentation badge| image:: https://img.shields.io/badge/docs-read%20now-blue.svg?color=royalblue&logo=Read-the-Docs&logoColor=whitesmoke
   :target: `documentation`_
   :alt: Documentation

.. _distribution: https://pypi.org/project/qts
.. |version badge| image:: https://img.shields.io/pypi/v/qts.svg?color=indianred&logo=PyPI&logoColor=whitesmoke
   :target: `distribution`_
   :alt: Latest distribution version

.. |python versions badge| image:: https://img.shields.io/pypi/pyversions/qts.svg?color=indianred&logo=PyPI&logoColor=whitesmoke
   :alt: Supported Python versions
   :target: `distribution`_

.. |python interpreters badge| image:: https://img.shields.io/pypi/implementation/qts.svg?color=indianred&logo=PyPI&logoColor=whitesmoke
   :alt: Supported Python interpreters
   :target: `distribution`_

.. _issues: https://github.com/python-qt-tools/qts/issues
.. |issues badge| image:: https://img.shields.io/github/issues/python-qt-tools/qts?color=royalblue&logo=GitHub&logoColor=whitesmoke
   :target: `issues`_
   :alt: Issues

.. _repository: https://github.com/python-qt-tools/qts
.. |repository badge| image:: https://img.shields.io/github/last-commit/python-qt-tools/qts.svg?color=seagreen&logo=GitHub&logoColor=whitesmoke
   :target: `repository`_
   :alt: Repository

.. _tests: https://github.com/python-qt-tools/qts/actions?query=branch%3Amain
.. |tests badge| image:: https://img.shields.io/github/workflow/status/python-qt-tools/qts/CI/main?color=seagreen&logo=GitHub-Actions&logoColor=whitesmoke
   :target: `tests`_
   :alt: Tests
