#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber

micro = 1e-6


class GradientCore(GenericFiber):
    # Fiber from https://www.nature.com/articles/s41598-018-27072-2
    def __init__(self, wavelength: float,
                       core_radius: float,
                       delta_n: float,
                       position: tuple = (0, 0)):

        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position
        self.delta_n = delta_n
        self.core_radius = core_radius
        self.brand = "Unknown"
        self.model = "Unknown"

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()
        self.add_silica_pure_cladding(radius=62.5e-6, name='outer-clad')

        index, delta_n = self.interpret_delta_n()

        self.add_next_structure_with_gradient(
            name='core',
            index=index,
            radius=self.core_radius,
            graded_index_factor=delta_n
        )

    def interpret_delta_n(self) -> tuple:
        """
        Interpret the inputed value of delta_n.

        :returns:   Tuple with the core refractive index and delta_n numerical value
        :rtype:     tuple
        """
        if isinstance(self.delta_n, str) and self.delta_n[-1] == '%':
            factor = float(self.delta_n.strip('%')) / 100
            delta_n = self.pure_silica_index * factor
            return delta_n + self.pure_silica_index, delta_n

        else:
            return self.delta_n + self.pure_silica_index, self.delta_n


GradientFiber = GradientCore
# -
