#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber, get_silica_index
from FiberFusing.fiber_types.standard import SMF28, HP630, HI1060
from FiberFusing.fiber_types.graded_index import GradientCore, GradientFiber
from FiberFusing.fiber_types.cappilary import CapillaryTube, FluorineCapillaryTube
from FiberFusing.fiber_types.double_clad import *
from FiberFusing.fiber_types.castor import *

micro = 1e-6


class CustomFiber(GenericFiber):
    def __init__(self, wavelength: float, structure_dictionary: dict, position: tuple = (0, 0)):
        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position

        self.add_air()

        for name, structure in structure_dictionary.items():
            if structure.get('NA') is not None:
                self.add_next_structure_with_NA(
                    name=name,
                    na=structure.get('NA'),
                    radius=structure.get('radius')
                )

            if structure.get('index') is not None:
                self.add_next_structure_with_index(
                    name=name,
                    index=structure.get('index'),
                    radius=structure.get('radius')
                )
# -

