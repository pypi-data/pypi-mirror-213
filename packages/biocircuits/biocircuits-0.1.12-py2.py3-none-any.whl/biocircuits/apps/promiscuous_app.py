import biocircuits.apps
import bokeh.plotting

app = biocircuits.apps.promiscuous_222_app()

app(bokeh.plotting.curdoc())