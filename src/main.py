#!/usr/bin/env sage

import sys
import time

from argparse import ArgumentParser
from sage.all import GF, is_prime, next_prime

from curve_generator import CurveGenerator
from trait_set       import TraitSet
from traits          import SecurityTrait, TechnicalTrait

class Main:
    def __init__(self):
        self.args = self.make_parser().parse_args()
        self.curve_traits = self.make_curve_traits()
        self.field_traits = self.make_field_traits()

    def run(self):
        start = time.time()

        F = self.make_base_field()

        curve = CurveGenerator(F, self.curve_traits).run()

        # Save generated curve to file
        with open(self.args.outfile, 'w') as outfile:
            outfile.write(str(curve) + '\n')
            outfile.write(str(curve.associated_ec()) + '\n')
            outfile.write("Elapsed time: " + str(time.time() - start))


    def make_base_field(self):
        if self.args.base_field != None:
            F = GF(self.args.base_field, 'F')
            self.field_traits.check(F)
            return F

        p = next_prime(2**self.args.num_bits)
        while not self.field_traits.check(GF(p, 'F'), nothrow = True):
            p = next_prime(p)

        return GF(p, 'F')

    def make_curve_traits(self):
        """ Security and technical requirements for the elliptic curve """
        traits = TraitSet()

        # Security requirements
        traits.add_trait(SecurityTrait.PrimeOrderSubgroup)
        traits.add_trait(SecurityTrait.NonTraceOne)
        traits.add_trait(SecurityTrait.EmbeddingResistance)

        # Technical requirements
        if self.args.overrun_protection:
            traits.add_trait(TechnicalTrait.OverrunProtection)

        return traits

    def make_field_traits(self):
        """ Security and technical requirements for the base field"""
        traits = TraitSet()

        # Technical requirements
        if self.args.point_compression:
            traits.add_trait(TechnicalTrait.PointCompression)

        return traits

    def make_parser(self):
        parser = ArgumentParser()

        parser = ArgumentParser(add_help = False)
        parser.add_argument('--num-proc',           type=int)
        parser.add_argument('--point-compression',  action='store_true')
        parser.add_argument('--overrun-protection', action='store_true')
        parser.add_argument('outfile', type=str,
                help='A path to a file where the generated curve will be stored')

        # Add subparser for base field options
        field_opts = parser.add_mutually_exclusive_group(required = True)

        field_opts.add_argument(
                '--base-field',
                type=str,
                help='Base field for the curve operations (i.e: GF(11)')

        field_opts.add_argument(
                '--num-bits',
                type=int,
                help='Select a random field with the given number of bits')

        return parser


if __name__ == "__main__":
    main = Main()
    main.run()
