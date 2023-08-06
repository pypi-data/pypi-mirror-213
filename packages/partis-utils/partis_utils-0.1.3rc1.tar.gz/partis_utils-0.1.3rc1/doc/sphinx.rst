
Sphinx Examples
===============

Figures
-------

.. seealso::

  * https://sphinx-subfigure.readthedocs.io/en/latest/

.. tab-set::

  .. tab-item:: HTML
    :sync: html

    .. subfigure:: AA|BC
      :layout-sm: A|B|C
      :gap: 8px
      :subcaptions: above
      :name: myfigure
      :class-grid: outline

      .. image:: img/A.png
          :alt: Image A
          :width: 25%

      .. image:: img/B.png
          :alt: Image B
          :width: 25%

      .. image:: img/C.png
          :alt: Image C
          :width: 25%

      Figure Caption

  .. tab-item:: RST
    :sync: rst

    .. code-block:: rst

      .. subfigure:: AA|BC
        :layout-sm: A|B|C
        :gap: 8px
        :subcaptions: above
        :name: myfigure
        :class-grid: outline

        .. image:: img/A.png
            :alt: Image A
            :width: 25%

        .. image:: img/B.png
            :alt: Image B
            :width: 25%

        .. image:: img/C.png
            :alt: Image C
            :width: 25%

        Figure Caption