"""This is the Bokeh charts interface. It gives you a high level API
to build complex plot is a simple way.

This is the Scatter class which lets you build your Scatter charts
just passing the arguments to the Chart class and calling the proper
functions.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2014, Continuum Analytics, Inc. All rights reserved.
#
# Powered by the Bokeh Development Team.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from bokeh.models import GlyphRenderer
from bokeh.charts._builder import create_and_build, XYBuilder
from bokeh.charts.utils import marker_types
from bokeh.charts import DEFAULT_PALETTE

from bokeh.charts.glyphs import ScatterGlyph

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------


def Scatter(*args, **kws):
    """ Create a scatter chart using :class:`ScatterBuilder <bokeh.charts.builder.scatter_builder.ScatterBuilder>`
    to render the geometry from values.

    Args:
        data (arrays or dict(array) or list(dict) or pd.DataFrame): table-like data

    In addition the the parameters specific to this chart,
    :ref:`userguide_charts_generic_arguments` are also accepted as keyword parameters.

    Returns:
        a new :class:`Chart <bokeh.charts.Chart>`

    Examples:

    .. bokeh-plot::
        :source-position: above

        from bokeh.sampledata.autompg import autompg as df
        from bokeh.charts import Scatter, output_file, show

        scatter = Scatter(df, x='mpg', y='hp', color='cyl', marker='origin',
                          title="mpg", xlabel="Miles Per Gallon", ylabel="Horsepower")

        output_file('scatter.html')
        show(scatter)

    """
    return create_and_build(ScatterBuilder, *args, **kws)


class ScatterBuilder(XYBuilder):
    """This is the Scatter class and it is in charge of plotting
    Scatter charts in an easy and intuitive way.

    Essentially, we provide a way to ingest the data, make the proper
    calculations and push the references into a source object.
    We additionally make calculations for the ranges. And finally add
    the needed glyphs (markers) taking the references from the source.

    """

    def _process_data(self):
        """Take the scatter.values data to calculate the chart properties
        accordingly. Then build a dict containing references to all the
        calculated points to be used by the marker glyph inside the
        ``_yield_renderers`` method.
        """
        self._attr = []

    def _yield_renderers(self):
        """Use the marker glyphs to display the points.

        Takes reference points from data loaded at the ColumnDataSource.
        """

        for group in self._data.groupby(**self.attributes):

            glyph = ScatterGlyph(group.data[self.x.selection], group.data[self.y.selection],
                                 line_color=group['color'], fill_color=group['color'],
                                 marker=group['marker'])

            renderer = glyph.renderers[0]
            self._legends.append((str(group.label), [renderer]))

            yield renderer
