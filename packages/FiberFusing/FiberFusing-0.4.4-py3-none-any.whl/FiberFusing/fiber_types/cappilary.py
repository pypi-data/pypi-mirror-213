#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber

micro = 1e-6


class CapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       delta_n: float,
                       position: tuple = (0, 0)):

        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position
        self.delta_n = delta_n
        self.radius = radius
        self.brand = "Unknown"
        self.model = "Unknown"

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()

        self.add_next_structure_with_index(
            name='inner-clad',
            index=self.pure_silica_index + self.delta_n,
            radius=self.radius
        )


class FluorineCapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       delta_n: float = -15e-3,
                       position: tuple = (0, 0)):

        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position
        self.delta_n = delta_n
        self.radius = radius
        self.brand = "Unknown"
        self.model = "Unknown"

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()

        self.add_next_structure_with_index(
            name='inner-clad',
            index=self.pure_silica_index + self.delta_n,
            radius=self.radius
        )

# -
