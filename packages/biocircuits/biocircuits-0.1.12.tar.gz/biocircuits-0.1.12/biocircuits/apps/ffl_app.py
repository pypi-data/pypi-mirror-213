import biocircuits.apps
import bokeh.plotting

app = biocircuits.apps.ffl_app()

app(bokeh.plotting.curdoc())