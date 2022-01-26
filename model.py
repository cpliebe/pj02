"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730329298"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, point_1: Point) -> float:
        """Calculate the distance between two points."""
        real_distance: float = sqrt(((point_1.x - self.x)**2) + ((point_1.y - self.y)**2))
        return real_distance

    
class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        """Tick method."""
        self.location = self.location.add(self.direction)
        if self.sickness == constants.INFECTED:
            self.sickness += 1
        if self.sickness >= constants.RECOVERY_PERIOD:
            self.is_immune()

    def contract_disease(self) -> None:
        """Assign the INFECTED constant to the sickness attribute of the cell."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Determine whether a cell is vulnerable or not."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Determine whether a cell is infected or not."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def color(self) -> str:
        """Assign vulnerable cells gray and infected cells blue."""
        if self.is_immune():
            cell_color: str = "green"
        elif self.is_vulnerable():
            cell_color = "gray"
        else:
            cell_color = "blue"
        return cell_color

    def contact_with(self, other_cell: Cell) -> None:
        """Implements what happens when two cells come into contact."""
        if self.is_vulnerable() and other_cell.is_infected():
            self.contract_disease()
        if self.is_infected() and other_cell.is_vulnerable():
            other_cell.contract_disease()

    def immunize(self) -> None:
        """Immunizes a cell."""
        self.sickness = constants.IMMUNE
    
    def is_immune(self) -> bool:
        """Determine whether or not a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False
       

class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, beginning_infected: int, beginning_immune: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if beginning_infected >= cells:
            raise ValueError
        if beginning_infected <= 0:
            raise ValueError
        if beginning_immune > cells:
            raise ValueError
        if beginning_immune < 0:
            raise ValueError
        for _ in range(0, cells):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        i: int = 0 
        for _ in range(0, beginning_infected):
            self.population[i].sickness = constants.INFECTED
            i += 1
        if beginning_immune > 0: 
            for _ in range(beginning_infected + 1, beginning_infected + beginning_immune):
                self.population[i].sickness = constants.IMMUNE
                i += 1
        
    def check_contacts(self) -> None:
        """Check to see if cells have come into contact with one another."""
        i: int = 0
        cell: Cell = self.population[i]
        point = Point(cell.location.x, cell.location.y)
        a: int = 1
        cell_1: Cell = self.population[a]
        point_1 = Point(cell_1.location.x, cell_1.location.y)
        while a < len(self.population):
            if Point.distance(point, point_1) <= constants.CELL_RADIUS:
                Cell.contact_with(self.population[i], cell_1)
                i += 1
                a += 1
        # start with self.population[0], iterate through remaining
        # indices in the list, if their distance() is less than radius, then call 
        # Cell#contact_with for the two cells

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        return False
