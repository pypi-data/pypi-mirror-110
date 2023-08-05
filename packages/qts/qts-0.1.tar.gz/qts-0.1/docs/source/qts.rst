qts
+++

The top level package exposes the basic functionality of the qts library.

.. autodata:: qts.__version__

Selecting a wrapper
===================

A Qt wrapper must be chosen before leveraging the qts compatibility features.
qts is notified of the choice by a call to :func:`qts.set_wrapper`.

.. autofunction:: qts.set_wrapper


Supported wrappers
==================

The objects representing the supported wrappers are directly available.
Each is an instance of the :class:`qts.Wrapper` class.
The full list of supported wrappers is available as :attr:`qts._core.supported_wrappers`.

..
   TODO: we shouldn't need the `._core` but without it we don't get the proper
         docstring included here

.. autodata:: qts._core.pyqt_5_wrapper
.. autodata:: qts._core.pyqt_6_wrapper
.. autodata:: qts._core.pyside_5_wrapper
.. autodata:: qts._core.pyside_6_wrapper

.. autodata:: qts._core.supported_wrappers

.. autoclass:: qts.Wrapper


Available wrappers
==================

Not all supported wrappers will be available in every case.


.. autofunction:: qts.available_wrapper
.. autofunction:: qts.available_wrappers
.. autofunction:: qts.wrapper_by_name


Present configuration
=====================

You can directly query the present wrapper object multiple ways.
The wrapper object can be retrieved directly through :data:`qts.wrapper`.
In some cases it is more useful to simply check if a specific wrapper is selected.
The ``qts.is_*`` values are helpful for this.
In particular, mypy is able to understand booleans via the command line arguments ``--always-false`` and ``--always-true``.
The :ref:`cli` can be used to help generate the relevant options to pass to mypy.

..
   TODO: `qts.wrapper` should show the value `None` not the value when building the
         docs

.. autodata:: qts.wrapper
   :no-value:
.. autodata:: qts.is_pyqt_5_wrapper
.. autodata:: qts.is_pyqt_6_wrapper
.. autodata:: qts.is_pyside_5_wrapper
.. autodata:: qts.is_pyside_6_wrapper


Exceptions
==========

See :ref:`exceptions`.
