from __future__ import annotations
from typing import TYPE_CHECKING
from pygame_view import *
from grid import Grid, Intersection
if TYPE_CHECKING:
    from resolvers import Resolver

class View:

    def __init__(self, width: int, height: int, resolver: Resolver = None):
        self.actual_view = PygameView(width, height, resolver)

    def check_quit_request(self) -> bool:
        return self.actual_view.check_quit_request()

    def refresh(self):
        self.actual_view.refresh()
    
    def set_info_string(self, string: str):
        self.actual_view.set_info_string(string)

    def set_resolver(self, resolver: Resolver):
        self.actual_view.set_resolver(resolver)

    def shut_down(self):
        self.actual_view.shut_down()