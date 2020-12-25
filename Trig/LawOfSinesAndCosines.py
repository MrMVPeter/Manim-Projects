from manimlib.imports import *

# All colors to be used through out the program
color = {'a': '#FF0000',
         'b': '#00FF00',
         'c': '#3333FF',
         'h': '#FFF200'}
# Some Times used through out the program
wait_t = {'m': 1.5,
          'l': 2.5}


class Sines(Scene):
    def construct(self):
        self.peter_intro()
        self.intro_pyth()
        self.intro_laws()
        self.sines()

    def peter_intro(self):
        pete_logo = TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL)
        self.add(pete_logo)

    def intro_pyth(self):
        # List of texts
        intro_texts = []
        intro_texts.append(TextMobject('The Pythagorean Theorem', color=color['h']
                                       ).scale(1.5).to_edge(UP))
        intro_texts.append(TextMobject('The Pythagorean Theorem allows us to find any side length'
                                       ).next_to(intro_texts[0], DOWN))
        intro_texts.append(TextMobject('of a Right Triangle given the two others...'
                                       ).next_to(intro_texts[1], DOWN))
        intro_texts.append(TextMobject('But it ONLY works with right triangles.'
                                       ).next_to(intro_texts[2], DOWN))
        text1 = []
        text1.append(TextMobject('It breaks down with non-right triangles'))

        # Write texts
        for x in intro_texts:
            self.play(Write(x))

        # Right Triangle and equation
        r_tri = []
        r_tri.append(draw_triangle([[-1, 0.5, 0], [-1, -3, 0], [1, -3, 0]]))
        r_tri.append(Polygon([-1, -3, 0], [-0.8, -3, 0], [-0.8, -2.8, 0], [-1, -2.8, 0]))
        pyth = TexMobject('a^2', '+', 'b^2', '=', 'c^2').scale(2).to_edge(LEFT).shift([0, -1, 0])
        pyth[0].set_color(color['a'])
        pyth[2].set_color(color['b'])
        pyth[4].set_color(color['c'])

        # Write triangle and make equation
        for x in r_tri[0]:
            self.play(Write(x))
        self.play(Write(r_tri[1]))
        self.play(*[Write(x)
                    for x in [pyth[1], pyth[3]]])
        self.play(Transform(r_tri[0][0].copy(), pyth[0]))
        self.play(Transform(r_tri[0][1].copy(), pyth[2]))
        self.play(Transform(r_tri[0][2].copy(), pyth[4]))
        self.wait()

        # Final Act
        outro_text = TextMobject('What about other triangles?').to_edge(RIGHT).shift([0, -1, 0])
        self.play(Write(outro_text))
        self.wait(2)
        self.play(*[FadeOut(x)
                    for x in self.mobjects],
                  FadeIn(TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL)))

    def intro_laws(self):
        # introduce laws
        texts = []
        texts.append(TextMobject('Laws Of Sines And Cosines', color=color['h']
                                 ).scale(1.5).to_edge(UP))
        texts.append(TextMobject('These laws allow us to look at non-right triangles,'
                                 ).next_to(texts[0], DOWN))
        texts.append(TextMobject('Meaning EVERY triangle'
                                 ).next_to(texts[1], DOWN))
        texts.append(TextMobject('Lets get started!').next_to(texts[0], DOWN))
        for i in texts[0:3]:
            self.play(Write(i))

        # Initiate the triangle dance
        self.shifting_tris()

        # Lets get Started! + Cleanup
        self.play(FadeOutAndShift(texts[1], LEFT),
                  FadeOutAndShift(texts[2], RIGHT))
        self.play(Write(texts[3]))
        self.play(*[FadeOut(x)
                    for x in self.mobjects],
                  FadeIn(TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL)))

    def shifting_tris(self):

        # Build Triangle
        triangle = draw_triangle([[-1, 0.5, 0], [-1, -3, 0], [1, -3, 0]])
        for x in triangle:
            self.play(ShowCreation(x))

        # Create a list of triangles
        mover_tris = []
        mover_tris.append(draw_triangle([[0, 1.5, 0], [-2, -3, 0], [1, 0, 0]]))
        mover_tris.append(draw_triangle([[-0.5, 1, 0], [-2, -2, 0], [2, -1, 0]]))
        mover_tris.append(draw_triangle([[0.5, 1, 0], [-2, -1, 0], [2, -2, 0]]))
        mover_tris.append(draw_triangle([[0.5, 1, 0], [-1.5, -2, 0], [3, -1, 0]]))
        mover_tris.append(draw_triangle([[0.5, 1, 0], [-1.5, -2, 0], [-3, 1, 0]]))
        mover_tris.append(draw_triangle([[0, 0.5, 0], [-2, -3, 0], [2, -3, 0]]))

        # Triangle Dance
        for x in range(len(mover_tris)):
            self.play(*[Transform(i, z, run_time=2)
                        for i, z in zip(triangle, mover_tris[x])])

    def sines(self):
        # Triangle + Lables
        sine_tri = draw_triangle([[1, -2.5, 0], [5, 0, 0], [7, -2.5, 0]])
        lables = []
        lables.append(TextMobject('a', color=color['a']).move_to([6.5, -0.75, 0]))
        lables.append(TextMobject('b', color=color['b']).move_to([2.5, -0.75, 0]))
        lables.append(TextMobject('c', color=color['c']).move_to([4, -3, 0]))
        lables.append(Arc(0, 0.558599, arc_center=[1, -2.5, 0], color=color['a']))
        lables.append(TextMobject('A', color=color['a']).move_to([2.35, -2.1, 0]))
        lables.append(Arc(2.245537, 0.896055, arc_center=[7, -2.5, 0], color=color['b']))
        lables.append(TextMobject('B', color=color['b']).move_to([5.7, -2, 0]))
        perp = []
        perp.append(Line([5, 0, 0], [5, -2.5, 0]))
        perp.append(Polygon([5, -2.5, 0], [4.8, -2.5, 0], [4.8, -2.3, 0], [5, -2.3, 0]))
        perp.append(TextMobject('h').move_to([4.75, -1.35, 0]))
        c_lables = []
        c_lables.append(Arc(-0.896055, -1.686938, arc_center=[5, 0, 0], color=color['c'],
                            radius=0.8))
        c_lables.append(TexMobject('C', color=color['c']).move_to([4.9, -1.1, 0]))

        # Build Triangle
        for x in sine_tri:
            self.play(Write(x))
        for x in lables:
            self.play(Write(x))

        # Set of lists of texts
        texts = []
        texts.append(TextMobject('Law Of Sines', color=color['h']).scale(1.5).to_edge(UP))
        texts.append(TextMobject("$a^2+b^2=c^2$ can't help us here").next_to(texts[0], DOWN))
        texts.append(TextMobject("because we don't have a right triangle.").next_to(texts[1], DOWN))
        texts.append(TextMobject("But we can make some!").next_to(texts[2], DOWN))
        texts2 = []
        texts2.append(TextMobject("By drawing the height, We have some right triangles."
                                  ).next_to(texts[0], DOWN))
        texts2.append(TextMobject("That means trig functions are now available to us."
                                  ).next_to(texts[1], DOWN))
        texts2.append(TextMobject("Let's start by finding the height."
                                  ).next_to(texts[2], DOWN))
        texts3 = []
        texts3.append(TextMobject('The Sine of ', 'A', ' can be used to find h.'
                                  ).next_to(texts[0], DOWN))
        texts3.append(TextMobject('Also, the Sine of ', 'B', ' can be used as well.'
                                  ).next_to(texts3[0], DOWN))
        texts3.append(TextMobject('Now lets solve for h in both equations.'
                                  ).next_to(texts3[1], DOWN))
        texts4 = []
        texts4.append(TextMobject('Both equations are equal to h.').next_to(texts[0], DOWN))
        texts4.append(TextMobject('So they most also be equal to each other.').next_to(texts4[0], DOWN))
        texts4.append(TextMobject('Lastly, we can rearrange the equation.').next_to(texts4[1], DOWN))
        texts5 = []
        texts5.append(TextMobject('The Sine of the angle divided the corresponding side length'
                                  ).next_to(texts[0], DOWN))
        texts5.append(TextMobject('stays the same for any pair of angle and side.'
                                  ).next_to(texts5[0], DOWN))
        texts5.append(TextMobject('So we can add one more term.'
                                  ).next_to(texts5[1], DOWN))

        # Creating the varius equations at multiple states
        equations = []

        # initial equations
        equations.append(TexMobject('Sin\\left(', 'A', '\\right)', '=',
                                    '{', 'h', '\\over', 'b', '}').to_edge(LEFT))
        equations[0][1].set_color(color['a'])
        equations[0][7].set_color(color['b'])
        equations.append(TexMobject('Sin\\left(', 'B', '\\right)', '=',
                                    '{', 'h', '\\over', 'a', '}').next_to(equations[0], DOWN, 1))
        equations[1][1].set_color(color['b'])
        equations[1][7].set_color(color['a'])

        # Solved for h equations
        equations.append(TexMobject('h', '=', 'Sin\\left(', 'A', '\\right)', 'b').move_to(equations[0]))
        equations[2][3].set_color(color['a'])
        equations[2][5].set_color(color['b'])
        equations.append(TexMobject('h', '=', 'Sin\\left(', 'B', '\\right)', 'a').move_to(equations[1]))
        equations[3][3].set_color(color['b'])
        equations[3][5].set_color(color['a'])

        # Megered 1
        equations.append(TexMobject('Sin\\left(', 'A', '\\right)', 'b', '=',
                                    'Sin\\left(', 'B', '\\right)', 'a'
                                    ).next_to(equations[0], DOWN).align_to(equations[3], LEFT))
        equations[4][1].set_color(color['a'])
        equations[4][3].set_color(color['b'])
        equations[4][6].set_color(color['b'])
        equations[4][8].set_color(color['a'])
        equations.append(TexMobject('{', 'Sin\\left(', 'A', '\\right)', '\\over', 'a', '}', '=',
                                    '{', 'Sin\\left(', 'B', '\\right)', '\\over', 'b', '}'
                                    ).move_to(equations[4]))
        equations[5][2].set_color(color['a'])
        equations[5][5].set_color(color['a'])
        equations[5][10].set_color(color['b'])
        equations[5][13].set_color(color['b'])

        # Final Equaiton
        equations.append(TexMobject('{', 'Sin\\left(', 'A', '\\right)', '\\over', 'a', '}', '=',
                                    '{', 'Sin\\left(', 'B', '\\right)', '\\over', 'b', '}', '=',
                                    '{', 'Sin\\left(', 'C', '\\right)', '\\over', 'c', '}'
                                    ).move_to(equations[5]).shift([1, 0, 0]))
        equations[6][2].set_color(color['a'])
        equations[6][5].set_color(color['a'])
        equations[6][10].set_color(color['b'])
        equations[6][13].set_color(color['b'])
        equations[6][18].set_color(color['c'])
        equations[6][21].set_color(color['c'])

        # Set Up Scene
        for x in texts:
            self.play(Write(x))
        self.wait()
        for x in perp:
            self.play(Write(x))
        self.wait()

        # Texts 2 and 3
        for x in range(len(texts2)):
            self.play(ReplacementTransform(texts[x + 1], texts2[x]))
        self.wait(4)
        self.play(*[FadeOut(x)
                    for x in texts2])
        self.play(Write(texts3[0]))

        # First Equation for Sin(A)
        self.play(*[Write(equations[0][x])
                    for x in [0, 1, 2, 3, 4, 6, 8]])
        self.play(ReplacementTransform(perp[2].copy(), equations[0][5], run_time=2))
        self.play(ReplacementTransform(lables[1].copy(), equations[0][7], run_time=2))
        self.wait()
        self.play(Write(texts3[1]))

        # First Equation for Sin(B)
        self.play(*[Write(equations[1][x])
                    for x in [0, 1, 2, 3, 4, 6, 8]])
        self.play(ReplacementTransform(perp[2].copy(), equations[1][5], run_time=2))
        self.play(ReplacementTransform(lables[0].copy(), equations[1][7], run_time=2))
        self.play(Write(texts3[2]))

        # Transform Sin(A) for h
        self.play(*[ReplacementTransform(equations[0][x], equations[2][y])
                    for x, y in zip([0, 1, 2, 3, 5, 7],
                                    [2, 3, 4, 1, 0, 5])],
                  *[FadeOut(equations[0][x])
                    for x in [4, 6, 8]])

        # Transform Sin(B) for h
        self.play(*[ReplacementTransform(equations[1][x], equations[3][y])
                    for x, y in zip([0, 1, 2, 3, 5, 7],
                                    [2, 3, 4, 1, 0, 5])],
                  *[FadeOut(equations[1][x])
                    for x in [4, 6, 8]])
        self.wait(2)

        # Text3 to 4
        for x in range(2):
            if x % 2 == 0:
                dir = RIGHT
                ndir = LEFT
            else:
                dir = LEFT
                ndir = RIGHT
            self.play(FadeOutAndShift(texts3[x], dir),
                      FadeInFrom(texts4[x], ndir))
        self.play(FadeOutAndShift(texts3[2], RIGHT))
        self.wait()

        # Merge Equations
        self.play(*[ReplacementTransform(equations[2][x], equations[4][y])
                    for x, y in zip([2, 3, 4, 5],
                                    [0, 1, 2, 3])],
                  *[ReplacementTransform(equations[3][x], equations[4][y])
                    for x, y in zip([2, 3, 4, 5],
                                    [5, 6, 7, 8])],
                  *[FadeOut(equations[2][x])
                    for x in [0, 1]],
                  *[FadeOut(equations[3][x])
                    for x in [0, 1]],
                  Write(equations[4][4]))

        # Update Equation
        self.play(Write(texts4[2]))
        self.wait()
        self.play(*[ReplacementTransform(equations[4][x], equations[5][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8],
                                    [1, 2, 3, 13, 7, 9, 10, 11, 5])],
                  *[Write(equations[5][x])
                    for x in [4, 12]])

        # Explain Third Term
        for x in range(3):
            self.play(ReplacementTransform(texts4[x], texts5[x]))
        self.wait()

        # Final Equation Training
        self.play(*[ReplacementTransform(equations[5][x], equations[6][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])],
                  *[Write(x)
                    for x in equations[6][14:]])
        self.wait(2)

        # Final Tri
        self.play(*[FadeOut(x)
                    for x in perp],
                  *[Write(x, run_time=2)
                    for x in c_lables])
        final_title = TextMobject('Law Of Sines', color=color['h']).scale(4).to_edge(UP, 1)

        # Final Title
        self.play(*[FadeOut(x)
                    for x in texts5],
                  ReplacementTransform(texts[0], final_title))
        self.wait(3)

        # Clean-up
        self.play(*[FadeOut(x)
                    for x in [final_title, *equations[6], *sine_tri, *lables,
                              *c_lables]])


class Cosines(Scene):
    def construct(self):
        # Add Logo at bottom left corner
        self.add(TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL))
        self.problem()
        self.draw_tri()

    def problem(self):
        # Only Equation
        equation = (TexMobject('{Sin\\left(', 'A', '\\right)\\over', 'a}', '=',
                               '{Sin\\left(', 'B', '\\right)\\over', 'b}', '=',
                               '{Sin\\left(', 'C', '\\right)\\over', 'c}'
                               ).to_edge(UP))
        equation[1].set_color(color['a'])
        equation[3].set_color(color['a'])
        equation[6].set_color(color['b'])
        equation[8].set_color(color['b'])
        equation[11].set_color(color['c'])
        equation[13].set_color(color['c'])

        # Both Sets of Texts
        texts1 = []
        texts1.append(TextMobject('The Law of Sines is an GREAT tool for many triangles,'
                                  ).next_to(equation, DOWN, 2))
        texts1.append(TextMobject('But it only works if you have both an angle AND the side'
                                  ).next_to(texts1[0], DOWN))
        texts1.append(TextMobject('across from it...', 'we need another tool.'
                                  ).next_to(texts1[1], DOWN))
        texts2 = []
        texts2.append(TextMobject('We used the Sine function to derive the first equation.'
                                  ).move_to(texts1[0]))
        texts2.append(TextMobject("What if we go back and take a different approach?"
                                  ).move_to(texts1[1]))
        texts2.append(TextMobject("Let's give it a try!").move_to(texts1[2]))

        # LOS equation
        self.play(Write(equation, run_time=4))
        self.wait()

        # Text1
        for x in [texts1[0], texts1[1], texts1[2][0]]:
            self.play(Write(x, run_time=3))
        self.wait()
        self.play(Write(texts1[2][1]))
        self.wait()

        # Explain Strategy(Text2)
        for x in range(3):
            self.play(FadeOutAndShiftDown(texts1[x]),
                      Write(texts2[x]))
        self.wait()

        # CleanUP
        self.play(Succession(*[FadeOutAndShiftDown(x)
                               for x in [equation, *texts2]]))

    def draw_tri(self):

        # All Triangle Parts
        cosine_tri = draw_triangle([[1, -2.5, 0], [5, 0, 0], [7, -2.5, 0]])
        lables = []
        lables.append(TextMobject('a', color=color['a']).move_to([6.5, -0.75, 0]))
        lables.append(TextMobject('b', color=color['b']).move_to([2.5, -0.75, 0]))
        lables.append(TextMobject('c', color=color['c']).move_to([4, -3, 0]))
        lables.append(Arc(0, 0.558599, arc_center=[1, -2.5, 0], color=color['a']))
        lables.append(TextMobject('A', color=color['a']).move_to([2.35, -2.1, 0]))
        perp = []
        perp.append(Line([5, 0, 0], [5, -2.5, 0]))
        perp.append(Polygon([5, -2.5, 0], [4.8, -2.5, 0], [4.8, -2.3, 0], [5, -2.3, 0]))
        perp.append(TextMobject('h').move_to([4.75, -1.35, 0]))
        xtras = []
        xtras.append(TexMobject('X').scale(0.8).move_to([3.75, -2.25, 0]))
        xtras.append(TexMobject('C', '-X').scale(0.8).move_to([6, -2.25, 0]))
        xtras[1][0].set_color(color['c'])
        bc_lables = []
        bc_lables.append(Arc(-0.896055, -1.686938, arc_center=[5, 0, 0], color=color['c'],
                            radius=0.8))
        bc_lables.append(TexMobject('C', color=color['c']).move_to([4.9, -1.1, 0]))
        bc_lables.append(Arc(2.245537, 0.896055, arc_center=[7, -2.5, 0], color=color['b']))
        bc_lables.append(TextMobject('B', color=color['b']).move_to([5.7, -2, 0]))

        # All Texts Throughout the Scene
        texts1 = []
        texts1.append(TextMobject("Law of Cosines", color=color['h']).scale(1.5).to_edge(UP))
        texts1.append(TextMobject("Instead of using the Sine function to solve for h,"
                                  ).next_to(texts1[0], DOWN))
        texts1.append(TextMobject("let's try using ", "The Pythagorean Theorem", "."
                                  ).next_to(texts1[1], DOWN))
        texts1[2][1].set_color(color['h'])
        texts1.append(TextMobject("But we'll need two additional side lengths..."
                                  ).next_to(texts1[2], DOWN))

        texts2 = []
        texts2.append(TextMobject("Let's use what we know about ", "The Pythagorean Theorem", "."
                                  ).move_to(texts1[1]))
        texts2[0][1].set_color(color['h'])
        texts2.append(TextMobject("First we'll use the left triangle."
                                  ).move_to(texts1[2]))
        texts2.append(TextMobject("Afterwards, we can use the ride side triangle too."
                                  ).move_to(texts1[3]))

        texts3 = []
        texts3.append(TextMobject("Let's Solve the equations for $h^2$.").move_to(texts2[0]))
        texts3.append(TextMobject("Now both equations are equal to $h^2$,").move_to(texts2[0]))
        texts3.append(TextMobject("and thus equal to each other.").move_to(texts2[1]))
        texts3.append(TextMobject("And now we simplify").move_to(texts2[2]))

        texts4 = []
        texts4.append(TextMobject("We're almost done!").move_to(texts2[0]))
        texts4.append(TextMobject("We just need to get rid of that last X.").move_to(texts2[1]))
        texts4.append(TextMobject("Cosine can save the day.").move_to(texts2[2]))

        texts5 = []
        texts5.append(TextMobject("We can solve for X using the Cosine function."
                                  ).move_to(texts2[0]))
        texts5.append(TextMobject("Then we can get rid of the last X via ", "Substitution", '.'
                                  ).move_to(texts2[1]))
        texts5[1][1].set_color(color['h'])
        texts5.append(TextMobject("Afterwards, we rearrange and we're finished!"
                                  ).move_to(texts2[2]))

        texts6 = []
        texts6.append(TextMobject("If we start over but solve for a different side,"
                                  ).move_to(texts2[0]))
        texts6.append(TextMobject("we can derive two very similar equations."
                                  ).move_to(texts2[1]))

        # All Equations
        equations = []

        # First PYTH
        equations.append(TexMobject('h^2', '+', 'X^2', '=', 'b^2').to_edge(LEFT))  # 0
        equations[0][4].set_color(color['b'])
        equations.append(TexMobject('h^2', '+', '\\left(', 'c', '-X', '\\right)^2',
                                    '=', 'a^2').next_to(equations[0], DOWN, 1
                                                        ).align_to(equations[0], LEFT))  # 1
        equations[1][3].set_color(color['c'])
        equations[1][7].set_color(color['a'])

        # Pyth for h
        equations.append(TexMobject('h^2', '=', 'b^2', '-', 'X^2').move_to(equations[0]))  # 2
        equations[2][2].set_color(color['b'])
        equations.append(TexMobject('h^2', '=', 'a^2', '-', '\\left(', 'c', '-X',
                                    '\\right)^2').move_to(equations[1]))  # 3
        equations[3][2].set_color(color['a'])
        equations[3][5].set_color(color['c'])

        # Merge 4(1)
        equations.append(TexMobject('b^2', '-', 'X^2', '=', 'a^2', '-', '\\left(', 'c', '-X',
                                    '\\right)^2').next_to(equations[0], DOWN
                                                          ).align_to(equations[0], LEFT))  # 4
        equations[4][0].set_color(color['b'])
        equations[4][4].set_color(color['a'])
        equations[4][7].set_color(color['c'])

        # Merge 5(2)
        equations.append(TexMobject('b^2', '-', 'X^2', '=', 'a^2', '-', '\\left(', 'c^2',
                                    '-', '2', 'c', 'X', '+', 'X^2', '\\right)'  # 5
                                    ).move_to(equations[4]).align_to(equations[4], LEFT))
        equations[5][0].set_color(color['b'])
        equations[5][4].set_color(color['a'])
        equations[5][7].set_color(color['c'])
        equations[5][10].set_color(color['c'])

        # Merge 6(3)
        equations.append(TexMobject('b^2', '-', 'X^2', '=', 'a^2', '-', 'c^2',
                                    '+', '2', 'c', 'X', '-', 'X^2'  # 6
                                    ).move_to(equations[4]).align_to(equations[4], LEFT))
        equations[6][0].set_color(color['b'])
        equations[6][4].set_color(color['a'])
        equations[6][6].set_color(color['c'])
        equations[6][9].set_color(color['c'])

        # Merge 7(4)
        equations.append(TexMobject('b^2', '=', 'a^2', '-', 'c^2',
                                    '+', '2', 'c', 'X'  # 7
                                    ).move_to(equations[4]).align_to(equations[4], LEFT))
        equations[7][0].set_color(color['b'])
        equations[7][2].set_color(color['a'])
        equations[7][4].set_color(color['c'])
        equations[7][7].set_color(color['c'])

        # Merge 8(5)
        equations.append(TexMobject('a^2', '=', 'b^2', '+', 'c^2',
                                    '-', '2', 'c', 'X'  # 8
                                    ).move_to(equations[4]).align_to(equations[4], LEFT))
        equations[8][0].set_color(color['a'])
        equations[8][2].set_color(color['b'])
        equations[8][4].set_color(color['c'])
        equations[8][7].set_color(color['c'])

        # Cosine Equtions
        equations.append(TexMobject('Cos\\left(', 'A', '\\right)', '=',
                                    '{', 'X', '\\over', 'b', '}'
                                    ).next_to(equations[8], DOWN).scale(0.8))  # 9
        equations[9][1].set_color(color['a'])
        equations[9][7].set_color(color['b'])
        equations.append(TexMobject('Cos\\left(', 'A', '\\right)', 'b', '=', 'X'
                                    ).move_to(equations[9]).scale(0.8))  # 10
        equations[10][1].set_color(color['a'])
        equations[10][3].set_color(color['b'])

        # Substitute 1
        equations.append(TexMobject('a^2', '=', 'b^2', '+', 'c^2',  # 11
                                    '-', '2', 'c', '\\left(', 'Cos\\left(', 'A',
                                    '\\right)', 'b', '\\right)'
                                    ).move_to(equations[8]).align_to(equations[8], LEFT))
        equations[11][0].set_color(color['a'])
        equations[11][2].set_color(color['b'])
        equations[11][4].set_color(color['c'])
        equations[11][7].set_color(color['c'])
        equations[11][10].set_color(color['a'])
        equations[11][12].set_color(color['b'])

        # Substitute 2
        equations.append(TexMobject('a^2', '=', 'b^2', '+', 'c^2',  # 12
                                    '-', '2', 'b', 'c', '\\cdot', 'Cos\\left(', 'A', '\\right)'
                                    ).move_to(equations[8]).align_to(equations[8], LEFT))
        equations[12][0].set_color(color['a'])
        equations[12][2].set_color(color['b'])
        equations[12][4].set_color(color['c'])
        equations[12][7].set_color(color['b'])
        equations[12][8].set_color(color['c'])
        equations[12][11].set_color(color['a'])

        # Sister equations
        sister_equ = []
        sister_equ.append(TexMobject('c^2', '=', 'b^2', '+', 'a^2',  # 12
                                     '-', '2', 'a', 'b', '\\cdot', 'Cos\\left(', 'C', '\\right)'
                                     ).next_to(equations[12], UP).align_to(equations[8], LEFT))
        sister_equ[0][0].set_color(color['c'])
        sister_equ[0][2].set_color(color['b'])
        sister_equ[0][4].set_color(color['a'])
        sister_equ[0][7].set_color(color['a'])
        sister_equ[0][8].set_color(color['b'])
        sister_equ[0][11].set_color(color['c'])
        sister_equ.append(TexMobject('b^2', '=', 'a^2', '+', 'c^2',  # 12
                                     '-', '2', 'a', 'c', '\\cdot', 'Cos\\left(', 'B', '\\right)'
                                     ).next_to(equations[12], DOWN).align_to(equations[8], LEFT))
        sister_equ[1][0].set_color(color['b'])
        sister_equ[1][2].set_color(color['a'])
        sister_equ[1][4].set_color(color['c'])
        sister_equ[1][7].set_color(color['a'])
        sister_equ[1][8].set_color(color['c'])
        sister_equ[1][11].set_color(color['b'])

        # Draw Triangle
        for x in [*cosine_tri, *lables, *perp]:
            self.play(Write(x))

        # texts 1
        for x in texts1:
            self.play(Write(x))
            self.wait()

        self.highlight_line()

        # The extra side lengths
        for x in xtras:
            self.play(Write(x))

        # Replace Texts
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts1[x + 1]),
                      Write(texts2[x]))
        self.play(FadeOutAndShiftDown(texts1[3]))

        # Left Tri Equations
        self.highlight_tri('left')
        self.play(*[Write(equations[0][x])
                    for x in [1, 3]])
        self.play(ReplacementTransform(perp[2].copy(), equations[0][0]))
        self.play(ReplacementTransform(xtras[0].copy(), equations[0][2]))
        self.play(ReplacementTransform(lables[1].copy(), equations[0][4]))
        self.wait()

        self.play(Write(texts2[2]))

        # Right Tri Equations
        self.highlight_tri('right')
        self.play(*[Write(equations[1][x])
                    for x in [1, 6]])
        self.play(ReplacementTransform(perp[2].copy(), equations[1][0]))
        self.play(ReplacementTransform(xtras[1].copy(), equations[1][2:6]))
        self.play(ReplacementTransform(lables[0].copy(), equations[1][7]))
        self.wait()

        # Texts 3 (solve for h)
        self.play(*[FadeOutAndShiftDown(x)
                    for x in [*texts2]],
                  Write(texts3[0]))
        self.wait()
        self.play(*[ReplacementTransform(equations[0][x], equations[2][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4],
                                    [0, 3, 4, 1, 2])],
                  *[ReplacementTransform(equations[1][x], equations[3][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7],
                                    [0, 3, 4, 5, 6, 7, 1, 2])])
        self.wait()

        # Text 3 (merge)
        self.play(FadeOutAndShiftDown(texts3[0]),
                  *[Write(texts3[x], run_time=2)
                    for x in [1, 2]])
        self.wait(2)

        # Merge
        self.play(*[ReplacementTransform(equations[2][x], equations[4][y], run_time=wait_t['l'])
                    for x, y in zip([1, 2, 3, 4],
                                    [3, 0, 1, 2])],
                  *[ReplacementTransform(equations[3][x], equations[4][y], run_time=wait_t['l'])
                    for x, y in zip([2, 3, 4, 5, 6, 7],
                                    [4, 5, 6, 7, 8, 9])],
                  *[FadeOut(equations[2][x], run_time=wait_t['l'])
                    for x in [0]],
                  *[FadeOut(equations[3][x], run_time=wait_t['l'])
                    for x in [0, 1]])

        # Last of text 3
        self.play(Write(texts3[3]))
        self.wait()

        # Equation 4 to 5
        self.play(*[ReplacementTransform(equations[4][x], equations[5][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    [0, 1, 2, 3, 4, 5, 6, 7, 13, 14])],
                  *[Write(equations[5][x], run_time=wait_t['m'])
                    for x in [8, 9, 10, 11, 12]])
        self.wait()

        # Equation 5 to 6
        self.play(*[ReplacementTransform(equations[5][x], equations[6][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                    [0, 1, 2, 3, 4, 5, 7, 6, 11, 8, 9, 10, 11, 12])],
                  *[FadeOut(equations[5][x], run_time=wait_t['m'])
                    for x in [14]])
        self.wait()

        # Equation 6 to 7
        self.play(*[FadeOutAndShiftDown(equations[6][x], run_time=wait_t['m'])
                    for x in [1, 2, 11, 12]])
        self.play(*[ReplacementTransform(equations[6][x], equations[7][y], run_time=wait_t['m'])
                    for x, y in zip([0, 3, 4, 5, 6, 7, 8, 9, 10],
                                    [0, 1, 2, 3, 4, 5, 6, 7, 8])])
        self.wait()

        # Equation 7 to 8
        self.play(*[ReplacementTransform(equations[7][x], equations[8][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8],
                                    [2, 1, 0, 5, 4, 3, 6, 7, 8])])
        self.wait()

        # Text 4
        self.play(*[FadeOutAndShiftDown(texts3[x])
                    for x in [1, 2, 3]])
        for x in range(3):
            self.play(Write(texts4[x]))
        self.wait()

        # Text 5, First Line
        self.play(*[FadeOutAndShiftDown(texts4[x])
                    for x in [0, 1, 2]],
                  Write(texts5[0]))

        # First Cos Equation
        self.play(*[Write(equations[9][x])
                    for x in [0, 1, 2, 3, 6]])
        self.play(ReplacementTransform(xtras[0].copy(), equations[9][5], run_time=wait_t['m']))
        self.play(ReplacementTransform(lables[1].copy(), equations[9][7], run_time=wait_t['m']))
        self.wait()

        # Second Cos Equation
        self.play(*[ReplacementTransform(equations[9][x], equations[10][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 5, 7],
                                    [0, 1, 2, 4, 5, 3])],
                  *[FadeOut(equations[9][x], run_time=wait_t['m'])
                    for x in [6]])

        #  Text5 Second Line
        self.play(Write(texts5[1]))
        self.wait()

        # Final equation (Pre) 8 to 11 (And 10 to 11)
        self.play(*[ReplacementTransform(equations[8][x], equations[11][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7],
                                    [0, 1, 2, 3, 4, 5, 6, 7])],
                  *[ReplacementTransform(equations[10][x], equations[11][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3],
                                    [9, 10, 11, 12])],
                  *[FadeOut(equations[10][x], run_time=wait_t['m'])
                    for x in [4, 5]],
                  ReplacementTransform(equations[8][8].copy(), equations[11][8], run_time=wait_t['m']),
                  ReplacementTransform(equations[8][8], equations[11][13], run_time=wait_t['m']))
        self.wait()

        #  Text5 Third Line
        self.play(Write(texts5[2]))
        self.wait()

        # Final equation 11 to 12
        self.play(*[ReplacementTransform(equations[11][x], equations[12][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                    [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 7])],
                  FadeOut(equations[11][13]))
        self.wait(3)

        # Text 6
        self.play(*[FadeOutAndShiftDown(x)
                    for x in texts5],
                  Write(texts6[0]))
        self.play(Write(texts6[1]))
        self.wait()

        # Sister equations
        self.play(*[Write(x)
                    for x in sister_equ])
        self.wait(2)

        # Final Title
        final_title = TextMobject('Law Of Cosines', color=color['h']).scale(4).to_edge(UP, 1)
        self.play(*[FadeOut(x)
                    for x in [*texts6, *xtras, *perp]],
                  *[Write(x)
                    for x in bc_lables],
                  ReplacementTransform(texts1[0], final_title, run_time=wait_t['l']))

        self.wait(2)

        # Clean Up
        self.play(Succession(*[ShrinkToCenter(x)
                               for x in [final_title, *lables, *bc_lables,
                                         *cosine_tri, *sister_equ, *equations[12]]],
                             lag_ratio=0.1))

    def highlight_line(self):
        h_line1 = Line([1, -2.5, 0], [5, -2.5, 0], color=color['h'], stroke_width=8)
        h_line2 = Line([5, -2.5, 0], [7, -2.5, 0], color=color['h'], stroke_width=8)
        self.play(Write(h_line1, run_time=3))
        self.wait()
        self.play(ReplacementTransform(h_line1, h_line2))
        self.wait(2)
        self.play(FadeOut(h_line2))

    def highlight_tri(self, side):

        if side == 'left':
            left_tri = Polygon([1, -2.5, 0], [5, 0, 0], [5, -2.5, 0],
                               stroke_color=color['h'], stroke_width=8, run_time=3)
            self.play(ShowCreationThenFadeOut(left_tri))
        else:
            right_tri = Polygon([5, 0, 0], [5, -2.5, 0], [7, -2.5, 0],
                                stroke_color=color['h'], stroke_width=8, run_time=3)
            self.play(ShowCreationThenFadeOut(right_tri))


class Bonus(Scene):
    def construct(self):
        self.add(TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL))
        self.bonus_intro()
        self.right_triangle_case()

    def bonus_intro(self):
        bonus_title = TextMobject('BONUS', color=color['h']).scale(7)
        self.play(Write(bonus_title, run_time=4))
        self.wait()
        self.play(ShrinkToCenter(bonus_title))

    def right_triangle_case(self):
        # Two Set if Texts
        texts1 = []
        texts1.append(TextMobject('BONUS', color=color['h']).scale(1.5).to_edge(UP))
        texts1.append(TextMobject('What happens if we use ', 'The Law of Cosines'
                                  ).next_to(texts1[0], DOWN))
        texts1[1][1].set_color(color['h'])
        texts1.append(TextMobject('on a right triangle?'
                                  ).next_to(texts1[1], DOWN))

        texts2 = []
        texts2.append(TextMobject("We created ", "The Pythagoreon Theorem").move_to(texts1[1]))
        texts2[0][1].set_color(color['h'])
        texts2.append(TextMobject("Thanks For Watching", color='#6F2DA8'
                                  ).scale(1.5).next_to(texts2[0], DOWN))

        equations = []

        # Original LOC
        equations.append(TexMobject('c^2', '=', 'b^2', '+', 'a^2',  # 0
                                    '-', '2', 'a', 'b', '\\cdot', 'Cos\\left(', 'C', '\\right)'
                                    ).scale(1.5).to_edge(LEFT))
        equations[0][0].set_color(color['c'])
        equations[0][2].set_color(color['b'])
        equations[0][4].set_color(color['a'])
        equations[0][7].set_color(color['a'])
        equations[0][8].set_color(color['b'])
        equations[0][11].set_color(color['c'])

        # Plugged in 90
        equations.append(TexMobject('c^2', '=', 'b^2', '+', 'a^2',  # 1
                                    '-', '2', 'a', 'b', '\\cdot', 'Cos\\left(', '90^\\circ', '\\right)'
                                    ).scale(1.5).to_edge(LEFT))
        equations[1][0].set_color(color['c'])
        equations[1][2].set_color(color['b'])
        equations[1][4].set_color(color['a'])
        equations[1][7].set_color(color['a'])
        equations[1][8].set_color(color['b'])

        # Simplified Cosine
        equations.append(TexMobject('c^2', '=', 'b^2', '+', 'a^2',  # 2
                                    '-', '2', 'a', 'b', '\\cdot', '0'
                                    ).scale(1.5).to_edge(LEFT))
        equations[2][0].set_color(color['c'])
        equations[2][2].set_color(color['b'])
        equations[2][4].set_color(color['a'])
        equations[2][7].set_color(color['a'])
        equations[2][8].set_color(color['b'])

        # The Pyth Theorem
        equations.append(TexMobject('a^2', '+', 'b^2', '=', 'c^2'  # 3
                                    ).scale(3).to_edge(LEFT).shift([0, -0.75, 0]))
        equations[3][0].set_color(color['a'])
        equations[3][2].set_color(color['b'])
        equations[3][4].set_color(color['c'])

        # Right Triangle
        r_tri = []
        r_tri.append(draw_triangle([[4, 0.5, 0], [4, -3, 0], [6, -3, 0]]))
        r_tri.append(Polygon([4, -3, 0], [4.2, -3, 0], [4.2, -2.8, 0], [4, -2.8, 0]))

        # Text1 (What if?)
        for x in texts1:
            self.play(Write(x))

        # Draw Triangle
        self.play(*[Write(x)
                    for x in [*r_tri[0], r_tri[1]]])

        # Draw Equation
        self.play(Write(equations[0], run_time=3))
        self.wait()

        # Plugged equation 0-1
        self.play(*[ReplacementTransform(equations[0][x], equations[1][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])])
        self.wait()

        # Simplified Cos 1-2
        self.play(*[ReplacementTransform(equations[1][x], equations[2][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10])])
        self.wait()

        # Simplified Pyth 2
        self.play(*[FadeOutAndShiftDown(equations[2][x], run_time=wait_t['m'])
                    for x in [5, 6, 7, 8, 9, 10]])
        self.wait()

        # Final Pyth 3
        self.play(*[ReplacementTransform(equations[2][x], equations[3][y], run_time=wait_t['m'])
                    for x, y in zip([0, 1, 2, 3, 4],
                                    [4, 3, 2, 1, 0])])
        self.wait()

        # Text 0-1
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts1[x+1]),
                      Write(texts2[x]))
        self.wait(2)


class TL_TN(Scene):
    def construct(self):
        # Triangle and Lables
        sine_tri = draw_triangle([[-3, -2.5, 0], [1, 0, 0], [3, -2.5, 0]])
        lables = []
        lables.append(TextMobject('a', color=color['a']).move_to([2.5, -0.75, 0]))
        lables.append(TextMobject('b', color=color['b']).move_to([-1.5, -0.75, 0]))
        lables.append(TextMobject('c', color=color['c']).move_to([0, -3, 0]))
        lables.append(Arc(0, 0.558599, arc_center=[-3, -2.5, 0], color=color['a']))
        lables.append(TextMobject('A', color=color['a']).move_to([-1.65, -2.1, 0]))
        lables.append(Arc(2.245537, 0.896055, arc_center=[3, -2.5, 0], color=color['b']))
        lables.append(TextMobject('B', color=color['b']).move_to([1.7, -2, 0]))
        perp = []
        perp.append(Line([1, 0, 0], [1, -2.5, 0]))
        perp.append(Polygon([1, -2.5, 0], [0.8, -2.5, 0], [0.8, -2.3, 0], [1, -2.3, 0]))
        perp.append(TextMobject('h').move_to([0.75, -1.35, 0]))
        c_lables = []
        c_lables.append(Arc(-0.896055, -1.686938, arc_center=[1, 0, 0], color=color['c'],
                            radius=0.8))
        c_lables.append(TexMobject('C', color=color['c']).move_to([0.9, -1.1, 0]))
        self.add(*sine_tri,
                 *lables,
                 *c_lables)

        # Title for ThumbNail
        title = TextMobject("Law of Sines And Cosines", color=color['h']).scale(2).to_edge(UP)
        self.add(title)

        equations = []
        # Law Of Sines
        equations.append(TexMobject('{', 'Sin\\left(', 'A', '\\right)', '\\over', 'a', '}', '=',
                                    '{', 'Sin\\left(', 'B', '\\right)', '\\over', 'b', '}', '=',
                                    '{', 'Sin\\left(', 'C', '\\right)', '\\over', 'c', '}'
                                    ).scale(0.9).to_edge(UL).shift([0, -2, 0]))
        equations[0][2].set_color(color['a'])
        equations[0][5].set_color(color['a'])
        equations[0][10].set_color(color['b'])
        equations[0][13].set_color(color['b'])
        equations[0][18].set_color(color['c'])
        equations[0][21].set_color(color['c'])

        # Law Of Cosines
        equations.append(TexMobject('a^2', '=', 'b^2', '+', 'c^2',  # 12
                                    '-', '2', 'b', 'c', '\\cdot', 'Cos\\left(', 'A', '\\right)'
                                    ).scale(0.9).to_edge(UR).shift([0, -2.25, 0]))
        equations[1][0].set_color(color['a'])
        equations[1][2].set_color(color['b'])
        equations[1][4].set_color(color['c'])
        equations[1][7].set_color(color['b'])
        equations[1][8].set_color(color['c'])
        equations[1][11].set_color(color['a'])
        self.add(*equations)


def draw_triangle(tri_points):
    lines = []
    lines.append(Line(tri_points[1], tri_points[2], color=color['a']))
    lines.append(Line(tri_points[0], tri_points[1], color=color['b']))
    lines.append(Line(tri_points[2], tri_points[0], color=color['c']))
    return lines


def find_theta(point, right, left):
    start_theta = math.atan((right[1] - point[1]) / (right[0] - point[0]))
    end_theta = math.atan((left[1] - point[1]) / (left[0] - point[0]))
    return start_theta, end_theta
