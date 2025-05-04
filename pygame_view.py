from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import Rect
from pygame.math import Vector2
from grid import Grid, Intersection
if TYPE_CHECKING:
    from resolvers import Resolver

class PygameView:

    def __init__(self, width: int, height: int, resolver: Resolver = None):
        self.width       = width
        self.height      = height
        self.screen      = pygame.display.set_mode((width, height))
        self.clock       = pygame.time.Clock()
        self.font        = pygame.font.SysFont('Arial', 10)
        self.resolver    = resolver
        self.info_string = ""

    def check_quit_request(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def refresh(self):
        self.screen.fill("white")
        gridi: Grid = self.resolver.game_grid

        x_scale_candidate = (self.width - 10) / (gridi.x_max - gridi.x_min)
        y_scale_candidate = (self.height - 10) / (gridi.y_max - gridi.y_min)
        scale = min(x_scale_candidate, y_scale_candidate)
        x_offset = (self.width - ((gridi.x_max - gridi.x_min) * scale) - 10) / 2
        y_offset = (self.height - ((gridi.y_max - gridi.y_min) * scale) - 10) / 2

        if hasattr(gridi, "focus"):
            pygame.draw.rect(surface=self.screen,
                            color="blue",
                            rect=Rect(((gridi.focus.x-gridi.x_min)*scale)+2+x_offset, 
                                    ((gridi.focus.y-gridi.y_min)*scale)+2+y_offset, 
                                    7, 7))

        for x in range(gridi.x_min, gridi.x_max+1):
            for y in range(gridi.y_min, gridi.y_max+1):
                if gridi.is_filled(Intersection(x, y)):
                    pygame.draw.circle(surface=self.screen, 
                                        center=Vector2(((x-gridi.x_min)*scale)+5+x_offset, 
                                                ((y-gridi.y_min)*scale)+5+y_offset),
                                        color="black",
                                        radius=2)

        seggies = gridi.get_segments()
        for segment in seggies:
            pygame.draw.line(surface=self.screen,
                            color="black",
                            start_pos=Vector2(((segment.intersection.x-gridi.x_min)*scale)+5+x_offset, 
                                                ((segment.intersection.y-gridi.y_min)*scale)+5+y_offset),
                            end_pos=Vector2(((segment.intersection.x+segment.x_heading-gridi.x_min)*scale)+5+x_offset, 
                                                ((segment.intersection.y+segment.y_heading-gridi.y_min)*scale)+5+y_offset))

        #punctuator = "!"
        #if self.resolver.is_still_going():
        #    punctuator = "..."
        #if hasattr(self.resolver, "current_path"):
        #    text = self.font.render(f'Line: {gridi.line_count}:{self.resolver.current_path}/{self.resolver.total_paths}({self.resolver.future_paths}){punctuator}', True, "black")
        #else:
        #    text = self.font.render(f'Line: {gridi.line_count}{punctuator}', True, "black")
        self.screen.blit(self.font.render(self.info_string, True, "black"), (1, 1))

        pygame.display.flip()

        return

    def set_info_string(self, string: str):
        self.info_string = string

    def set_resolver(self, resolver: Resolver):
        self.resolver = resolver
        return
    
    def shut_down(self):
        pygame.quit()
