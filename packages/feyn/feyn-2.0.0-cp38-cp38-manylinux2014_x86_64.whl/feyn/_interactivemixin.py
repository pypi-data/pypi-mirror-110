from typing import Iterable
import feyn


class InteractiveMixin:
    def interactive_flow(self, data: Iterable) -> "SVG":
        """EXPERIMENTAL: For IPython kernels only.

        Plots an interactive version of the flow of activations through the model, for the provided sample. Uses the provided data as background information for visualization.

        Requires installing ipywidgets, and enabling the extension in jupyter notebook or jupyter lab.
        Jupyter notebook: jupyter nbextension enable --py widgetsnbextension
        Jupyter lab: jupyter labextension install @jupyter-widgets/jupyterlab-manager

        Returns:
            SVG -- SVG of the model activation flow.
        """
        feyn.plots.interactive.interactive_activation_flow(self, data)
