from .title import Title
from .style import TextStyle, SubTextStyle
from .legend import Legend
from .tooltip import Tooltip
from .toolbox import Toolbox
from .datazoom import DatazoomInside, DatazoomSlider
from .grid import Grid, Grid3D
from .figsize import Figsize
from .brush import Brush
from .visualmap import VisualMap

__all__ = ["Title", "TextStyle", 'SubTextStyle', 'Legend', 'Grid', 'Grid3D', 'Figsize', 'Brush',
          'Tooltip', 'Toolbox', 'DatazoomInside', 'DatazoomSlider', 'VisualMap']


def get_all_supported_components():
    return sorted(__all__)