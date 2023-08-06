from plotly import graph_objects as go
from plotly.offline import plot
import os

from fsa_logger.config.log_config import logger


def plot_figure(fig: go.Figure, filename=None, inline=False, get_html=False, auto_open=True,
                include_plotlyjs='directory'):
    """
    Utility para mostrar una figura plotly
    :param fig: Figura a mostrar
    :param filename: nombre del archivo para guardar la figura
    :param inline: llama a fig.show() y no genera nada más --> cuadernos jypyter
    :param get_html: llama a fig.to_html() y no genera nada más --> devolver cadena de texto para un servidor web
    :param auto_open: Guarda el archivo localmente y lo abre automáticamente (si el nombre es largo se genera un fichero temporal que es el que se abre)
    :param include_plotlyjs: directiva para incluir la librería plotly.js (True | False | 'cdn' | 'directory' | path - default='directory')
    :return:
    """
    # para jupyter
    if inline:
        fig.show()
    elif get_html:
        return fig.to_html(include_plotlyjs='cdn')
    else:
        # guardar fichero
        logger.info(f'Generating chart {filename}...')

        if filename is not None:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if len(filename) < 150:
                plot(fig, filename=filename, auto_open=auto_open, include_plotlyjs=include_plotlyjs)
            else:
                plot(fig, filename=filename, auto_open=False, include_plotlyjs=include_plotlyjs)
                if auto_open:
                    plot(fig, include_plotlyjs=include_plotlyjs)
        # abrir en ventana
        elif auto_open:
            plot(fig, include_plotlyjs=include_plotlyjs)
