import json
from visitor import Visitor
from sourcetable import SourceTable
from copy import deepcopy

class DetectExplicitLeaks(Visitor):
    """
    Detects explicit leaks in slices for a given vulnerability.
    """
    def __init__(self):
        pass