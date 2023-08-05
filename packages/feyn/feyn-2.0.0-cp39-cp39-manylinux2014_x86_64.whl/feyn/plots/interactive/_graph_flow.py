import numpy as np
from feyn import Model
from typing import Iterable

from feyn.plots._graph_flow import plot_activation_flow


def interactive_activation_flow(model: Model, data: Iterable):
    """
    EXPERIMENTAL: For IPython kernels only.
    Interactively plot a model displaying the flow of activations.

    Requires installing ipywidgets, and enabling the extension in jupyter notebook or jupyter lab.
    Jupyter notebook: jupyter nbextension enable --py widgetsnbextension
    Jupyter lab: jupyter labextension install @jupyter-widgets/jupyterlab-manager

    Arguments:
        model {feyn.Model} -- A feyn.Model we want to describe given some data.
        data {Iterable} -- A Pandas DataFrame or dict of numpy arrays to compute on.

    Returns:
        SVG -- SVG of the model summary.
    """
    import ipywidgets as widgets

    features = model.features
    ranges = {}
    for i in model:
        if i.name in features:
            name = i.name
            if "cat" in i.spec:
                ranges[name] = data[name].unique()
            else:
                ranges[name] = (data[name].min(), data[name].max())

    def flow(**kwargs):
        for key in kwargs:
            kwargs[key] = np.array([kwargs[key]])
        return plot_activation_flow(model, data, kwargs)

    return widgets.interact(flow, **ranges)
