#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber

micro = 1e-6


class SMF28(GenericFiber):
    brand = 'Corning'
    model = "SMF28"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()
        self.add_silica_pure_cladding(radius=62.5e-6, name='outer-clad')

        self.add_next_structure_with_NA(
            name='core',
            na=0.12,
            radius=8.2 / 2 * micro
        )


class HP630(GenericFiber):
    brand = 'Thorlab'
    model = "HP630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()
        self.add_silica_pure_cladding(radius=62.5e-6, name='outer-clad')

        self.add_next_structure_with_NA(
            name='core',
            na=0.13,
            radius=3.5 / 2 * micro
        )


class HI1060(GenericFiber):
    brand = 'Corning'
    model = "HI630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()
        self.add_silica_pure_cladding(radius=62.5e-6, name='outer-clad')

        self.add_next_structure_with_NA(
            name='core',
            na=0.14,
            radius=5.3 / 2 * micro
        )

# -
