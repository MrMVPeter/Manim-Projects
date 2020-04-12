'''
This is a Very basic Demonstration of the Quadratic equation.
It seved as a stepping stone to improve my knowledge of manim.
'''


from manimlib.imports import *


# Quad Legacy
class QuadformL(Scene):
    def construct(self):
        quad_form = TexMobject(
            'ax^2+bx+c=0'
        ).scale(3)
        quad_form1 = TexMobject(
            'ax^2+bx=-c'
        ).scale(3)
        quad_form2 = TexMobject(
            'x^2+{b \\over a}x={-c \\over a}'
        ).scale(3)
        quad_form3 = TexMobject(
            'x^2+{b \\over a}x+{b^2 \\over 4a^2}={-c \\over a}+{b^2 \\over 4a^2}'
        ).scale(2)
        quad_form4 = TexMobject(
            '\\left( x+{b \\over 2a}\\right)^2={-c \\over a}+{b^2 \\over 4a^2}'
        ).scale(2.5)
        quad_form5 = TexMobject(
            '\\left( x+{b \\over 2a}\\right)^2={b^2 - 4ac \\over 4a^2}'
        ).scale(2.5)
        quad_form6 = TexMobject(
            '\\sqrt{\\left( x+{b \\over 2a}\\right)^2}=\\sqrt{{b^2 - 4ac \\over 4a^2}}'
        ).scale(2)
        quad_form7 = TexMobject(
            'x+{b \\over 2a}={\\pm\\sqrt{b^2 - 4ac} \\over 2a}'
        ).scale(2.5)
        quad_form8 = TexMobject(
            'x={-b\\pm\\sqrt{b^2 - 4ac} \\over 2a}'
        ).scale(3)
        self.play(Write(quad_form))
        self.wait(1)
        self.play(ReplacementTransform(quad_form, quad_form1))
        self.wait(1)
        self.play(ReplacementTransform(quad_form1, quad_form2))
        self.wait(1)
        self.play(ReplacementTransform(quad_form2, quad_form3))
        self.wait(1)
        self.play(ReplacementTransform(quad_form3, quad_form4))
        self.wait(1)
        self.play(ReplacementTransform(quad_form4, quad_form5))
        self.wait(1)
        self.play(ReplacementTransform(quad_form5, quad_form6))
        self.wait(1)
        self.play(ReplacementTransform(quad_form6, quad_form7))
        self.wait(1)
        self.play(ReplacementTransform(quad_form7, quad_form8))
        self.wait(1)