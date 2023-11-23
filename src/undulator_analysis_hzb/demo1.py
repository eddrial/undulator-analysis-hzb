"""
    Example NumPy style docstrings.
    
    This module demonstrates documentation as specified by the `NumPy
    Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
    are created with a section header followed by an underline of equal length.
    
    Example
    -------
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::
    
        $ python example_numpy.py
    
    
    Section breaks are created with two blank lines. Section breaks are also
    implicitly created anytime a new section starts. Section bodies *may* be
    indented:
    
    Notes
    -----
        This is an example of an indented section. It's like any other section,
        but the body is indented to help it stand out from surrounding text.
    
    If a section is indented, then a section break is created by
    resuming unindented text.
    
    Attributes
    ----------
    module_level_variable1 : int
        Module level variables may be documented in either the ``Attributes``
        section of the module docstring, or in an inline docstring immediately
        following the variable.
    
        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.
    
    
    .. _NumPy Documentation HOWTO:
       https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
    
"""
import matplotlib.pyplot as plt
import numpy as np

def add_one(number):
    return number + 1

def simply_plot():
    a = np.arange(19)
    b = np.arange(19) * a
    
    fig, ax = plt.subplots()
    fig.set_size_inches(8,4)
    ax.plot(a,b)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
    
    return fig