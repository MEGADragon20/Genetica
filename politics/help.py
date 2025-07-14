from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import numpy as np

def plot_colored_line(ax, data, x_attr, y_attr, cmap_name='coolwarm', linewidth=2, label=None):
    """
    Zeichnet eine Linie mit Farbverlauf auf eine bestehende Achse.

    Parameters:
    - ax: Die matplotlib-Achse, auf die geplottet wird
    - data: Liste von Objekten (z. B. deine Climate-Entries)
    - x_attr: Attributname für x-Werte (z. B. 'id')
    - y_attr: Attributname für y-Werte (z. B. 'tt')
    - cmap_name: Farbverlauf (default: 'coolwarm')
    - linewidth: Dicke der Linie
    - label: Legenden-Label (optional)
    """

    if not data or len(data) < 2:
        return  # Nichts zu zeichnen

    x = np.array([getattr(entry, x_attr) for entry in data])
    y = np.array([getattr(entry, y_attr) for entry in data])

    # Segmente für Farbverlauf
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = Normalize(vmin=y.min(), vmax=y.max())
    cmap = cm.get_cmap(cmap_name)

    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array((y[:-1] + y[1:]) / 2)
    lc.set_linewidth(linewidth)

    ax.add_collection(lc)
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min() - 1, y.max() + 1)

    if label:
        # Dummy für Legende hinzufügen
        ax.plot([], [], color=cmap(norm(y.mean())), label=label)

    return lc  # Optional: Rückgabe, falls du colorbar o.ä. machen willst
