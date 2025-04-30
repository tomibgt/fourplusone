from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import Rect
from pygame.math import Vector2
from grid import Intersection
if TYPE_CHECKING:
    from resolvers import Resolver

class View:

    def __init__(self, width: int, height: int, resolver: Resolver = None):
        self.width    = width
        self.height   = height
        self.screen   = pygame.display.set_mode((width, height))
        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont('Arial', 10)
        self.resolver = resolver

    def refresh(self):
        self.screen.fill("white")

        x_scale_candidate = (self.width - 10) / (self.resolver.game_grid.x_max - self.resolver.game_grid.x_min)
        y_scale_candidate = (self.height - 10) / (self.resolver.game_grid.y_max - self.resolver.game_grid.y_min)
        scale = min(x_scale_candidate, y_scale_candidate)
        x_offset = (self.width - ((self.resolver.game_grid.x_max - self.resolver.game_grid.x_min) * scale) - 10) / 2
        y_offset = (self.height - ((self.resolver.game_grid.y_max - self.resolver.game_grid.y_min) * scale) - 10) / 2

        if hasattr(self.resolver.game_grid, "focus"):
            pygame.draw.rect(surface=self.screen,
                            color="blue",
                            rect=Rect(((self.resolver.game_grid.focus[0]-self.resolver.game_grid.x_min)*scale)+2+x_offset, 
                                    ((self.resolver.game_grid.focus[1]-self.resolver.game_grid.y_min)*scale)+2+y_offset, 
                                    7, 7))

        print(f"{self.resolver.game_grid.intersections}")
        for x in range(self.resolver.game_grid.x_min, self.resolver.game_grid.x_max+1):
            for y in range(self.resolver.game_grid.y_min, self.resolver.game_grid.y_max+1):
                if self.resolver.game_grid.is_filled(Intersection(x, y)):
                    pygame.draw.circle(surface=self.screen, 
                                        center=Vector2(((x-self.resolver.game_grid.x_min)*scale)+5+x_offset, 
                                                ((y-self.resolver.game_grid.y_min)*scale)+5+y_offset),
                                        color="black",
                                        radius=2)

        seggies = self.resolver.game_grid.get_segments()
        for segment in seggies:
            pygame.draw.line(surface=self.screen,
                            color="black",
                            start_pos=Vector2(((segment.intersection.x-self.resolver.game_grid.x_min)*scale)+5+x_offset, 
                                                ((segment.intersection.y-self.resolver.game_grid.y_min)*scale)+5+y_offset),
                            end_pos=Vector2(((segment.intersection.x+segment.intersection.x_heading-self.resolver.game_grid.x_min)*scale)+5+x_offset, 
                                                ((segment.intersection.y+segment.y_heading-self.resolver.game_grid.y_min)*scale)+5+y_offset))

        punctuator = "!"
        if self.resolver.is_still_going():
            punctuator = "..."
        if hasattr(self.resolver, "current_path"):
            text = self.font.render(f'Line: {self.resolver.game_grid.line_count}:{self.resolver.current_path}/{self.resolver.total_paths}({self.resolver.future_paths}){punctuator}', True, "black")
        else:
            text = self.font.render(f'Line: {self.resolver.game_grid.line_count}{punctuator}', True, "black")
        self.screen.blit(text, (1, 1))

        #self.clock.tick(60)
        pygame.display.flip()

        return

    def set_resolver(self, resolver: Resolver):
        self.resolver = resolver
        return
