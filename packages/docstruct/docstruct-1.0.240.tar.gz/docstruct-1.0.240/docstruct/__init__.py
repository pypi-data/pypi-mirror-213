from .bounding_box import BoundingBox
from .drawer import Drawer
from .point import Point
from .segment import Segment, Segment2D
from .text_block import (
    Character,
    Document,
    Page,
    Area,
    Line,
    Paragraph,
    TextBlock,
    Word,
    Table,
    TableColumn,
    TableCell,
)
from .vis_line import VisLine, VisLineOrientation
from .text_block_splitter import TextBlockSplitter
from .spatial_grid_indexing import SpatialGrid

from docstruct.version import VERSION


__version__ = VERSION
