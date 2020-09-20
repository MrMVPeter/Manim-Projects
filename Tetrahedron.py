from manimlib.imports import *

colors = {
    'h': '#FFF200',
    'sl': '#666666',
    'rh': '#FF5555',
    'ph': '#6F2DA8',
    'a': '#00A86B',
    'b': '#89CFEF',
    'v': '#FFBF00'
}

waits = {
    'ss': 0.33,
    's': 0.45,
    'm': 1.5,
    'ml': 1.5,
    'l': 2
}


class Table(Scene):
    def construct(self):
        # choose the chapter to send to the top (1-7)
        chapter_select = 1

        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        # Set up Texts
        tables_final = []
        tables_final.append(TextMobject('TABLE OF CONTENTS'))
        tables_final.append(TextMobject('1) ', 'What is a Tetrahedron?'))
        tables_final.append(TextMobject('2) ', 'Solution Layout'))
        tables_final.append(TextMobject('3) ', 'Height of Tetrahedron'))
        tables_final.append(TextMobject('4) ', 'Cross-Sectional Base'))
        tables_final.append(TextMobject('5) ', 'Cross-Sectional Height'))
        tables_final.append(TextMobject('6) ', 'Cross-Sectional Area'))
        tables_final.append(TextMobject('7) ', 'Integration'))

        # Set Upper-left and left borders
        upper_left = (-4, 2)
        left_edges = [[-6.25, 0, 0], [1.25, 0, 0]]

        # Create Writable titles
        for y in range(4):
            for x in range(2):
                tables_final[(2 * y + x)].move_to([upper_left[0] + (8 * x), upper_left[1] - (1.5 * y), 0]
                                                  ).align_to((left_edges[x]), LEFT)
        tables_final[0].scale(1.3).shift([0.7, 0, 0]).set_color(colors['h'])

        # Write titles
        self.play(*[Write(x, run_time=2)
                    for x in tables_final])
        self.wait(4)

        # Transition Phase
        final_title = tables_final[chapter_select][1].copy().move_to([0, 3.5, 0]).set_color(colors['h']
                                                                                            ).to_edge(UP)

        # Fade All but selected
        not_final = []
        for x in tables_final:
            if x != tables_final[chapter_select]:
                not_final.append(x)
        self.play(*[FadeOut(x)
                    for x in not_final])
        self.wait()

        # Transform
        self.play(Transform(tables_final[chapter_select][1], final_title),
                  FadeOut(tables_final[chapter_select][0]))
        self.wait()


class WhatIsTetrahedron(Scene):
    def construct(self):
        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('What is a Tetrahedron?', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # Texts Describing the tetrahedron
        texts1 = []
        texts1.append(TextMobject('The ', 'Tetrahedron', ' is a polyhedron').next_to(title, DOWN, 0.5))
        texts1.append(TextMobject('built from 4 equilateral triangles.').next_to(texts1[0], DOWN))
        texts1.append(TextMobject('It can also be described as a triangular pyramid.').next_to(texts1[1], DOWN))
        texts1[0][1].set_color(colors['h'])

        texts2 = []
        texts2.append(TextMobject('The ', 'Tetrahedron', ' is 1 of 5 platonic solids,').next_to(title, DOWN, 0.5))
        texts2.append(TextMobject('meaning all faces, edges, and vertices are congruent.').next_to(texts1[0], DOWN))
        texts2.append(TextMobject('ONLY', ' five 3D solids meet those requirements.').next_to(texts1[1], DOWN))
        texts2[0][1].set_color(colors['h'])
        texts2[2][0].set_color(colors['h'])

        bullets = []
        bullets.append(TextMobject('$\\bullet$ 4 Faces'))
        bullets.append(TextMobject('$\\bullet$ 6 Edges'))
        bullets.append(TextMobject('$\\bullet$ 4 Vertices'))
        vbullets = VGroup(*bullets).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift([0, -1.25, 0])

        self.wait()
        lines = [Line([0, 0, 0], [0, -4, 0]),
                 Line([0, 0, 0], [7.1, 0, 0])]

        for x in texts1:
            self.play(Write(x, run_time=waits['m']))
            self.wait(waits['ss'])
        self.wait(6)

        for x in lines:
            self.play(Write(x, run_time=waits['m']))
            self.wait(waits['ss'])
        self.wait(3)

        for x in bullets:
            self.play(Write(x, run_time=waits['m']))
            self.wait(waits['m'])
        self.wait()

        # Text 2
        for x, y in zip(texts1, texts2):
            self.play(FadeOut(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
            self.wait(waits['ss'])
        self.wait(4)

        # Fade Out
        self.play(*[FadeOut(x, run_time=2)
                    for x in [*texts2, title, vbullets, *lines]])
        self.wait(5)


class SolutionLayout(Scene):
    def construct(self):
        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Solution Layout', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # text0
        texts0 = []
        texts0.append(TextMobject("Throughout this video, we'll be looking at the ", "tetrahedron", "."
                                  ).next_to(title, DOWN, 0.5))
        texts0.append(TextMobject("Given the edge length the the ", "tetrahedron", "(", 'a', '),'
                                  ).next_to(texts0[0], DOWN))
        texts0.append(TextMobject("Our goal is to solve for the volume."
                                  ).next_to(texts0[1], DOWN))
        texts0[0][1].set_color(colors['h'])
        texts0[1][1].set_color(colors['h'])
        texts0[1][3].set_color(colors['a'])

        # texts describing solution layout
        texts1 = []
        texts1.append(TextMobject('Finding the volume directly is very difficult.').next_to(title, DOWN, 0.5))
        texts1.append(TextMobject('BUT...we can approximate a ', 'tetrahedron', ' using prisms,'
                                  ).next_to(texts1[0], DOWN))
        texts1.append(TextMobject('of which we DO know the volume.').next_to(texts1[1], DOWN))
        texts1[1][1].set_color(colors['h'])

        # texts describing solution layout
        texts2 = []
        texts2.append(TextMobject('By using integration, we can add up the volume of all').next_to(title, DOWN, 0.5))
        texts2.append(TextMobject('prisms(slices) as the number of prisms(slices) approach $\\infty$.'
                                  ).next_to(texts2[0], DOWN))
        texts2.append(TextMobject('First, we must find the volume of any one prism.').next_to(texts2[1], DOWN))

        # texts describing solution layout
        texts3 = []
        texts3.append(TextMobject('We know the volume of any prism is equal to the').next_to(title, DOWN, 0.5))
        texts3.append(TextMobject('base area multiplied by the height of the prism.'
                                  ).next_to(texts3[0], DOWN))

        # Hight of slice
        texts4 = []
        texts4.append(TextMobject('The height of the slice is equal to the difference').next_to(title, DOWN, 0.5))
        texts4.append(TextMobject('between the height of top and bottom of the slice,'
                                  ).next_to(texts4[0], DOWN))
        texts4.append(TextMobject('or d', 'h', '(change in height)').next_to(texts4[1], DOWN))
        texts4[2][1].set_color(colors['rh'])

        # Area of slice
        texts5 = []
        texts5.append(TextMobject('The Base Area of the triangular prism varies').next_to(title, DOWN, 0.5))
        texts5.append(TextMobject('based off the height of the prism.'
                                  ).next_to(texts5[0], DOWN))
        texts5.append(TextMobject("Thus, we'll write Area as a function of (", 'h', ').').next_to(texts5[1], DOWN))
        texts5[2][1].set_color(colors['rh'])

        # Integration
        texts6 = []
        texts6.append(TextMobject('Armed with the volume of any prism(slice)').next_to(title, DOWN, 0.5))
        texts6.append(TextMobject('at a given height and d', 'h', ','
                                  ).next_to(texts6[0], DOWN))
        texts6.append(TextMobject('We can use an integral to add all the slices up.').next_to(texts6[1], DOWN))
        texts6[1][1].set_color(colors['rh'])

        # Integration
        texts7 = []
        texts7.append(TextMobject('From here, its a matter of simplifying the integral.').next_to(texts1[0], DOWN, 0.5))

        # equations
        equations = []
        equations.append(TexMobject('V', '(Prism)', '=', 'A', '(', 'Base', ')', '\\cdot', 'H').move_to([3.55, -2, 0]))
        equations[0][0].set_color(colors['v'])
        equations[0][3].set_color(colors['a'])
        equations[0][8].set_color(colors['ph'])
        equations.append(TexMobject('V', '(Prism)', '=', 'A', '(', 'Base', ')', '\\cdot', 'd', 'h'
                                    ).move_to([3.55, -2, 0]))
        equations[1][0].set_color(colors['v'])
        equations[1][3].set_color(colors['a'])
        equations[1][9].set_color(colors['rh'])
        equations.append(TexMobject('V', '(Prism)', '=', 'A', '(', 'h', ')', '\\cdot', 'd', 'h'
                                    ).move_to([3.55, -2, 0]))
        equations[2][0].set_color(colors['v'])
        equations[2][3].set_color(colors['a'])
        equations[2][5].set_color(colors['rh'])
        equations[2][9].set_color(colors['rh'])
        equations.append(TexMobject('V', '=', '\\int_b^t', 'A', '(', 'h', ')', '\\cdot', 'd', 'h'
                                    ).move_to([3.55, -2, 0]))
        equations[3][0].set_color(colors['v'])
        equations[3][3].set_color(colors['a'])
        equations[3][5].set_color(colors['rh'])
        equations[3][9].set_color(colors['rh'])

        # Bullet point
        bullet = []
        bullet.append(TextMobject('$\\bullet$ as we add more prisms,'))
        bullet.append(TextMobject('the total volume approaches'))
        bullet.append(TextMobject('that of a ', 'tetrahedron'))
        bulletg = VGroup(*bullet).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift([0, -1.25, 0])

        # Frame for 3D animation
        lines = [Line([0, 0, 0], [0, -4, 0]),
                 Line([0, 0, 0], [7.1, 0, 0])]
        left_box = Line([0, 0, 0], [-7.1, 0, 0])

        # Layout Texts (Pre-Animation)
        self.wait()
        for x in texts0:
            self.play(Write(x), run_time=waits['m'])
        self.wait(3)

        self.play(*[ReplacementTransform(x, y)
                    for x, y in zip(texts0, texts1)])
        self.wait(6)
        self.add(*lines)
        self.wait(10)

        # (Post Animation)
        for x in bulletg:
            self.play(Write(x))
        self.wait(2)

        # text 1-2
        for x, y in zip(texts1, texts2):
            self.play(ShrinkToCenter(x, run_time=waits['m']),
                      GrowFromCenter(y, run_time=waits['m']))
        self.wait(4)

        # text 2-3
        for x, y in zip(texts2[0:2], texts3[0:2]):
            self.play(FadeOutAndShiftDown(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
        self.play(*[FadeOutAndShiftDown(x)
                    for x in [texts2[2], bulletg]])
        self.wait(3)

        # Equation
        self.play(Write(equations[0], run_time=2.5))
        self.wait()

        # text 3-4
        for x, y in zip(texts3[0:2], texts4[0:2]):
            self.play(FadeOutAndShiftDown(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
        self.play(Write(texts4[2]))

        self.wait(2)
        self.play(Write(left_box))

        # Equilateral Triangle
        eq_tri, label = self.con_eq_tri()
        eq_tri.move_to([-3.55, -2, 0]).scale(1.5)
        self.play(ShowCreation(eq_tri, run_time=3))
        self.wait()

        # equation 1-2
        self.play(ReplacementTransform(equations[0][0:8], equations[1][0:8]),
                  FadeOutAndShiftDown(equations[0][8:]),
                  ReplacementTransform(label.copy(), equations[1][8:], run_time=2))

        # Fade Group and introduce animation(External render)
        self.play(FadeOut(eq_tri))
        self.wait(4)

        # text 4-5
        for x, y in zip(texts4, texts5):
            self.play(FadeOutAndShiftDown(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
        self.wait(4)

        # equation 2-3
        self.play(ReplacementTransform(equations[1][0:5], equations[2][0:5]),
                  ReplacementTransform(equations[1][6:], equations[2][6:]),
                  FadeOutAndShiftDown(equations[1][5]),
                  ReplacementTransform(texts5[2][1].copy(), equations[2][5], run_time=2))

        # text 5-6
        for x, y in zip(texts5, texts6):
            self.play(FadeOutAndShift(x, RIGHT, run_time=waits['m']),
                      FadeInFrom(y, LEFT, run_time=waits['m']))
        self.wait(4)

        # equation 3-4(Final)
        self.play(*[ReplacementTransform(equations[2][x], equations[3][x])
                    for x in range(10)])
        self.wait(2)

        # text 6-7
        self.play(*[ShrinkToCenter(x, run_time=waits['m'])
                    for x in texts6],
                  GrowFromCenter(texts7[0]))

        self.play(*[FadeOut(x, run_time=2)
                    for x in self.mobjects])

    def con_eq_tri(self):
        # equalateral Triangle
        trans_vect = complex(np.cos(np.pi * 2 / 3), np.sin(np.pi * 2 / 3))
        vect1 = complex(0, 1)
        vect2 = vect1 * trans_vect
        vect3 = vect2 * trans_vect
        points = []
        for x in [vect1, vect2, vect3]:
            points.append([x.real, x.imag, 0])
        poly = Polygon(points[0], points[1], points[2])

        # Inner Rects
        rect1p = [[0.5660254, 0.0196152, 0],
                  [0.5660254, -0.49, 0],
                  [-0.5660254, -0.49, 0],
                  [-0.5660254, 0.0196152, 0]]
        rect2p = [[0.2660254, 0.539230484, 0],
                  [0.2660254, 0.0196152, 0],
                  [-0.2660254, 0.0196152, 0],
                  [-0.2660254, 0.539230484, 0]]
        rect1 = Polygon(*rect1p, stroke_color=colors['h'])
        rect2 = Polygon(*rect2p, stroke_color=colors['h'])

        # Lines
        lines = []
        l_points = [[[1, -0.5, 0], [1, 0.0163152, 0]],
                    [[1.2, -0.5, 0], [1.2, 0.539230484, 0]]]
        for x in l_points:
            lines.append(Line(x[0], x[1]))
            lines.append(Line([x[0][0] - 0.05, x[0][1], 0], [x[0][0] + 0.05, x[0][1], 0]))
            lines.append(Line([x[1][0] - 0.05, x[1][1], 0], [x[1][0] + 0.05, x[1][1], 0]))

        # label
        label = TextMobject('d', 'h').move_to([0.8, 0.3, 0]).scale(0.7)
        label[1].set_color(colors['rh'])

        group = VGroup(poly, rect1, rect2, *lines, label)
        return group, label


class HeightOfT(Scene):
    def construct(self):
        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Height of Tetrahedron', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # Various sets of explanatory text
        text1 = []
        text1.append(TextMobject("If we're planning on integrating from bottom to top,"
                                 ).next_to(title, DOWN, 0.5))
        text1.append(TextMobject("we must first find out where the top is."
                                 ).next_to(text1[0], DOWN))
        text1.append(TextMobject("That is, we must find the height of the ", 'tetrahedron', '.'
                                 ).next_to(text1[1], DOWN))
        text1[2][1].set_color(colors['h'])

        text2 = []
        text2.append(TextMobject("Let's try using ", 'The Pythagorean Theorem', '.'
                                 ).next_to(title, DOWN, 0.5))
        text2.append(TextMobject("We can make a right triangle with edge length for a hypotenuse,"
                                 ).next_to(text2[0], DOWN))
        text2.append(TextMobject("and height of the ", "tetrahedron", " for one of the legs."
                                 ).next_to(text2[1], DOWN))
        text2[0][1].set_color(colors['h'])
        text2[2][1].set_color(colors['h'])

        text3 = []
        text3.append(TextMobject("We can solve for height IF we can find the other two lengths."
                                 ).next_to(title, DOWN, 0.5))
        text3.append(TextMobject("Let's start by finding the lower leg."
                                 ).next_to(text3[0], DOWN))
        text3.append(TextMobject("We'll use a Top-Down projection."
                                 ).next_to(text3[1], DOWN))

        text3 = []
        text3.append(TextMobject("We can solve for height IF we can find the other two lengths."
                                 ).next_to(title, DOWN, 0.5))
        text3.append(TextMobject("Let's start by finding the lower leg."
                                 ).next_to(text3[0], DOWN))
        text3.append(TextMobject("We'll use a Top-Down projection."
                                 ).next_to(text3[1], DOWN))

        text4 = []
        text4.append(TextMobject("Using this triangle, we can solve for ", "x", '.'
                                 ).next_to(title, DOWN, 0.5))
        text4.append(TextMobject("We'll employ ", "The Law Of Sines", " to find that"
                                 ).next_to(text4[0], DOWN))
        text4.append(TexMobject("{", "x", "\\over", "Sin\\left(", "30^\\circ", "\\right)", "}", "=",
                                "{", "a", "\\over", "Sin\\left(", "120^\\circ", "\\right)", "}"
                                ).next_to(text4[1], DOWN))
        text4[1][1].set_color(colors['h'])
        text4[2][1].set_color(colors['rh'])
        text4[2][4].set_color(colors['rh'])
        text4[2][9].set_color(colors['a'])
        text4[2][12].set_color(colors['a'])

        text5 = []
        text5.append(TextMobject("With this equation at hand,"
                                 ).next_to(title, DOWN, 0.5))
        text5.append(TextMobject("we can solve for ", "x", " , then simplify."
                                 ).next_to(text5[0], DOWN))
        text5.append(TexMobject("x", "=", "{", "a", "\\over", "\\sqrt", "3", "}"
                                ).next_to(text5[1], DOWN))
        text5[1][1].set_color(colors['rh'])
        text5[2][0].set_color(colors['rh'])
        text5[2][3].set_color(colors['a'])

        text6 = []
        text6.append(TextMobject("Going back to the first triangle,").next_to(title, DOWN, 0.5))
        text6.append(TextMobject("we'll use ", "The Pythagorean Theorem", " to solve for height."
                                 ).next_to(text6[0], DOWN))
        text6[1][1].set_color(colors['h'])

        text7 = []
        text7.append(TextMobject("Finally, armed with this equation,").next_to(title, DOWN, 0.5))
        text7.append(TextMobject("we can solve for ", "h", " and simplify."
                                 ).next_to(text7[0], DOWN))
        text7[1][1].set_color(colors['rh'])

        text8 = []
        text8.append(TextMobject('The Height of a ', 'tetrahedron', ' is equal to'
                                 ).next_to(title, DOWN, 0.4))
        text8.append(TexMobject("h", "=", "{", "a", "\\sqrt", "6", "\\over", "3", "}"
                                ).next_to(text8[0], DOWN))
        text8.append(TextMobject("Where ", "a", " is equal to the edge length."
                                 ).next_to(text8[1], DOWN))
        text8[1][0].set_color(colors['rh'])
        text8[1][3].set_color(colors['a'])
        text8[2][1].set_color(colors['a'])

        text9 = []
        text9.append(TextMobject('Now with the top and bottom and the ', 'tetrahedron', ','
                                 ).move_to(text8[0]))
        text9.append(TextMobject('we can plug them into the integral.').move_to(text8[2]))
        text9[0][1].set_color([colors['h']])

        # Animation Lines
        lines = []
        lines.append(Line([0, 0, 0], [7.1, 0, 0]))
        lines.append(Line([0, 0, 0], [0, -4, 0]))
        lines.append(Line([0, 0, 0], [-7.1, 0, 0]))

        # Animation length labels
        length_label = []
        length_label.append(TextMobject('a', color=colors['a']).scale(1.25).move_to([-3.55, -1, 0]))
        length_label.append(TextMobject('x', color=colors['rh']).scale(1.25).move_to([-2.15, -2.25, 0]))

        # Lower Leg solution
        # First projection
        main_tri, line_group, LOS_tri, labels = self.tet_proj()
        proj1 = VGroup(main_tri, line_group, LOS_tri, *labels[0], *labels[1])
        proj1.scale(2).move_to([-3.55, -2, 0])

        # Second Projection
        main_tri2, line_group2, LOS_tri2, labels2 = self.tet_proj()
        proj2 = VGroup(LOS_tri2, *labels2[0], *labels2[1])
        proj2.scale(3).move_to([-3.55, -2, 0])

        # Height Right Triangle
        right_triangle = self.height_triangle().scale(1.25).move_to([-3.55, -1.75, 0])
        right_labels = []
        right_labels.append(TexMobject('h', color=colors['rh']).move_to([-4.7, -1.7, 0]))
        right_labels.append(TexMobject('a', color=colors['a']).move_to([-3.25, -1.7, 0]))
        right_labels.append(TexMobject("{", "a", "\\over", "\\sqrt", "3", "}").scale(0.75).move_to([-3.5, -3.5, 0]))
        right_labels[2][1].set_color(colors['a'])

        # equations used throughout the animation
        equations = []
        equations.append(TexMobject("{", "x", "\\over", "Sin\\left(", "30^\\circ", "\\right)", "}", "=",
                                    "{", "a", "\\over", "Sin\\left(", "120^\\circ", "\\right)", "}"
                                    ).scale(1.2).move_to([3.55, -2, 0]))  # 0
        equations[0][1].set_color(colors['rh'])
        equations[0][4].set_color(colors['rh'])
        equations[0][9].set_color(colors['a'])
        equations[0][12].set_color(colors['a'])
        equations.append(TexMobject("x", "=", "{", "Sin\\left(", "30^\\circ", "\\right)", "a", "\\over",
                                    "Sin\\left(", "120^\\circ", "\\right)", "}"
                                    ).scale(1.2).move_to([3.55, -2, 0]))  # 1
        equations[1][0].set_color(colors['rh'])
        equations[1][4].set_color(colors['rh'])
        equations[1][6].set_color(colors['a'])
        equations[1][9].set_color(colors['a'])
        equations.append(TexMobject("x", "=", "{", "{", "a", "\\over", "2", "}", "\\over",
                                    "{", "\\sqrt", "3", "\\over", "2", "}", "}"
                                    ).scale(1.2).move_to([3.55, -2, 0]))  # 2
        equations[2][0].set_color(colors['rh'])
        equations[2][4].set_color(colors['a'])
        equations.append(TexMobject("x", "=", "{", "a", "\\over", "\\sqrt", "3", "}"
                                    ).scale(1.2).move_to([3.55, -2, 0]))  # 3
        equations[3][0].set_color(colors['rh'])
        equations[3][3].set_color(colors['a'])
        equations.append(TexMobject("h^2", "+", "\\left(", "{", "a", "\\over", "\\sqrt", "3", "}",
                                    "\\right)", "^2", "=", "a^2"
                                    ).next_to(text6[1], DOWN, 0.01))  # 4
        equations[4][0].set_color(colors['rh'])
        equations[4][4].set_color(colors['a'])
        equations[4][12].set_color(colors['a'])
        equations.append(TexMobject("h^2", "+", "{", "a^2", "\\over", "3", "}",
                                    "=", "a^2"
                                    ).next_to(text6[1], DOWN, 0.01))  # 5
        equations[5][0].set_color(colors['rh'])
        equations[5][3].set_color(colors['a'])
        equations[5][8].set_color(colors['a'])
        equations.append(TexMobject("h^2", "=", "a^2", "-", "{", "a^2", "\\over", "3", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 6
        equations[6][0].set_color(colors['rh'])
        equations[6][2].set_color(colors['a'])
        equations[6][5].set_color(colors['a'])
        equations.append(TexMobject("h^2", "=", "{", "3", "a^2", "-", "a^2", "\\over", "3", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 7
        equations[7][0].set_color(colors['rh'])
        equations[7][4].set_color(colors['a'])
        equations[7][6].set_color(colors['a'])
        equations.append(TexMobject("h^2", "=", "{", "2", "a^2", "\\over", "3", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 8
        equations[8][0].set_color(colors['rh'])
        equations[8][4].set_color(colors['a'])
        equations.append(TexMobject("h", "=", "\\sqrt", "{", "{", "2", "a^2", "\\over", "3", "}", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 9
        equations[9][0].set_color(colors['rh'])
        equations[9][6].set_color(colors['a'])
        equations.append(TexMobject("h", "=", "{", "\\sqrt", "2", "a", "\\over", "\\sqrt", "3", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 10
        equations[10][0].set_color(colors['rh'])
        equations[10][5].set_color(colors['a'])
        equations.append(TexMobject("h", "=", "{", "\\sqrt", "6", "a", "\\over", "3", "}"
                                    ).next_to(text6[1], DOWN, 0.01))  # 11
        equations[11][0].set_color(colors['rh'])
        equations[11][5].set_color(colors['a'])
        equations.append(TexMobject('V', '=', '\\int', '_{', 'b', '}', '^{', 't', '}', 'A',
                                    '(', 'h', ')', '\\cdot', 'd', 'h'
                                    ).move_to([[3.55, -2, 0]]))
        equations[12][0].set_color(colors['v'])
        equations[12][9].set_color(colors['a'])
        equations[12][11].set_color(colors['rh'])
        equations[12][15].set_color(colors['rh'])
        equations.append(TexMobject('V', '=', '\\int', '_{', '0', '}', '^{', '{', 'a', '\\sqrt', '6', '\\over', '3',
                                    '}', '}', 'A', '(', 'h', ')', '\\cdot', 'd', 'h'
                                    ).move_to([3.55, -2, 0]))
        equations[13][0].set_color(colors['v'])
        equations[13][15].set_color(colors['a'])
        equations[13][17].set_color(colors['rh'])
        equations[13][21].set_color(colors['rh'])

        # text1
        self.wait()
        for x in text1:
            self.play(Write(x, run_time=waits['m']))
        self.wait(3)

        # text2
        for x, y in zip(text1, text2):
            self.play(FadeOut(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))

        # Right side box
        for x in range(2):
            self.play(ShowCreation(lines[x]))
        self.wait(6)

        # text3
        for x, y in zip(text2, text3):
            self.play(FadeOutAndShift(x, RIGHT, run_time=waits['m']),
                      FadeInFrom(y, LEFT, run_time=waits['m']))

        # Left side Box
        self.play(Write(lines[2]))
        self.wait(6)

        # Show base triangle creation
        self.play(ShowCreation(proj1, run_time=4, rate_func=linear))
        self.wait(3)
        self.play(*[FadeOut(x)
                    for x in [*main_tri, *line_group, *main_tri]])
        self.play(*[ReplacementTransform(x, y)
                    for x, y in zip([LOS_tri, *labels[0], *labels[1]],
                                    [LOS_tri2, *labels2[0], *labels2[1]])])
        self.play(*[Write(x)
                    for x in length_label])
        self.wait(2)

        # text4
        for x in range(3):
            if x % 2 == 0:
                self.play(FadeOutAndShift(text3[x], RIGHT),
                          FadeInFrom(text4[x], LEFT))
            else:
                self.play(FadeOutAndShift(text3[x], LEFT),
                          FadeInFrom(text4[x], RIGHT))
        self.wait(4)

        # Right-Side equation
        self.play(*[Write(equations[0][x], run_time=1.5)
                    for x in [2, 3, 5, 7, 10, 11, 13]],
                  *[ReplacementTransform(length_label[x].copy(), equations[0][y], run_time=2)
                    for x, y in zip([0, 1], [9, 1])],
                  *[ReplacementTransform(labels2[1][x].copy(), equations[0][y], run_time=2)
                    for x, y in zip([0, 2], [12, 4])])
        self.wait(2)

        # Text 5
        for x in range(2):
            self.play(FadeOutAndShift(text4[x], UP),
                      FadeInFrom(text5[x], DOWN))
        self.play(FadeOutAndShift(text4[2], UP))
        self.wait(3)

        # Equations 0-1
        self.play(*[ReplacementTransform(equations[0][x], equations[1][y])
                    for x, y in zip([1, 3, 4, 5, 7, 9, 10, 11, 12, 13],
                                    [0, 3, 4, 5, 1, 6, 7, 8, 9, 10])],
                  FadeOut(equations[0][2]))
        self.wait(2)

        # Equations 1-2
        self.play(*[ReplacementTransform(equations[1][x], equations[2][y])
                    for x, y in zip([0, 1, 6, 3, 5, 7, 8, 9, 10, 10],
                                    [0, 1, 4, 5, 6, 8, 10, 11, 12, 13])],
                  FadeIn(equations[2][12]),
                  FadeOut(equations[1][4]))
        self.wait(2)

        # Equations 2-3
        self.play(*[ReplacementTransform(equations[2][x], equations[3][y])
                    for x, y in zip([0, 1, 4, 8, 10, 11],
                                    [0, 1, 3, 4, 5, 6])],
                  *[FadeOutAndShift(equations[2][x], DOWN)
                    for x in [5, 6, 12, 13]])
        self.wait(2)

        # equation 3-text5
        self.play(ReplacementTransform(equations[3], text5[2]))

        # text 5-6
        for x in range(2):
            self.play(ReplacementTransform(text5[x], text6[x]))
        self.wait(2)

        # Height Pyth Triangle(and Fade Bas Tri)
        self.play(*[FadeOut(x)
                    for x in [LOS_tri2, *labels2[0], *labels2[1], *length_label]])
        self.play(ShowCreation(right_triangle))
        self.wait(2)

        # Draw Two Labels
        for x in [right_labels[0], right_labels[1]]:
            self.play(Write(x))

        # Move Third label from text to triangle
        self.play(*[ReplacementTransform(text5[2][x], right_labels[2][y])
                    for x, y in zip([3, 4, 5, 6], [1, 2, 3, 4])],
                  *[FadeOut(text5[2][z])
                    for z in [0, 1]])
        self.wait(2)

        # equation 4 (From Labels)
        self.play(*[ReplacementTransform(x, equations[4][y], run_time=2)
                    for x, y in zip([right_labels[0], right_labels[1], right_labels[2][1],
                                     right_labels[2][2], right_labels[2][3], right_labels[2][4]],
                                    [0, 12, 4, 5, 6, 7])],
                  *[FadeIn(equations[4][z], run_time=2)
                    for z in [1, 2, 9, 10, 11]])
        self.wait(2)

        # text 6-7
        for x in range(2):
            self.play(ReplacementTransform(text6[x], text7[x]))
        self.wait(2)

        # equation 4-5
        self.play(*[ReplacementTransform(equations[4][x], equations[5][y])
                    for x, y in zip([0, 1, 4, 5, 7, 11, 12, 13], [0, 1, 3, 4, 5, 7, 8])],
                  *[FadeOut(equations[4][z])
                    for z in [2, 6, 9, 10]])
        self.wait(2)

        # equation 5-6
        self.play(*[ReplacementTransform(equations[5][x], equations[6][y])
                    for x, y in zip([0, 1, 3, 4, 5, 7, 8],
                                    [0, 3, 2, 6, 7, 1, 5])])
        self.wait(2)

        # equation 6-7
        self.play(*[ReplacementTransform(equations[6][x], equations[7][y])
                    for x, y in zip([0, 1, 2, 3, 5, 6, 7],
                                    [0, 1, 4, 5, 6, 7, 8])],
                  ReplacementTransform(equations[6][2].copy(), equations[7][3]))
        self.wait(2)

        # equation 7-8
        self.play(*[ReplacementTransform(equations[7][x], equations[8][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8],
                                    [0, 1, 3, 4, 4, 4, 5, 6])])
        self.wait(2)

        # equation 8-9
        self.play(*[ReplacementTransform(equations[8][x], equations[9][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6],
                                    [0, 1, 5, 6, 7, 8])],
                  FadeIn(equations[9][2]))
        self.wait(2)

        # equation 9-10
        self.play(*[ReplacementTransform(equations[9][x], equations[10][y])
                    for x, y in zip([0, 1, 2, 5, 6, 7, 8],
                                    [0, 1, 3, 4, 5, 6, 8])],
                  ReplacementTransform(equations[9][2].copy(), equations[10][7]))
        self.wait(2)

        # equation 10-11
        self.play(*[ReplacementTransform(equations[10][x], equations[11][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8],
                                    [0, 1, 3, 4, 5, 6, 3, 7])],
                  ReplacementTransform(equations[10][7].copy(), equations[11][4]))
        self.wait(2)

        # text 7-8
        self.play(ShrinkToCenter(text7[0]),
                  GrowFromCenter(text8[0]))
        self.play(ReplacementTransform(equations[11], text8[1]),
                  ShrinkToCenter(text7[1]))
        self.play(GrowFromCenter(text8[2]))
        self.wait(2)

        # text 8-9
        self.play(FadeOut(text8[0]),
                  Write(text9[0]))
        self.play(FadeOut(text8[2]),
                  Write(text9[1]))
        self.wait(2)

        # Write equation 12
        self.play(*[Write(x, run_time=1.5)
                    for x in equations[12]])
        self.wait(2)

        # Plug in equation from text8-equation13
        self.play(*[ReplacementTransform(equations[12][x], equations[13][y])
                    for x, y in zip([0, 1, 2, 4, 9, 10, 11, 12, 13, 14, 15],
                                    [0, 1, 2, 4, 15, 16, 17, 18, 19, 20, 21])],
                  *[ReplacementTransform(text8[1][x].copy(), equations[13][y])
                    for x, y in zip([3, 4, 5, 6, 7],
                                    [8, 9, 10, 11, 12])],
                  FadeOut(equations[12][7]))
        self.wait(2)

        # Fade Out Everything
        self.play(*[FadeOut(x, run_time=2)
                    for x in self.mobjects])

    def tet_proj(self):
        center_p = [0, 0, 0]
        color = '#9999FF'
        # main Triangle
        bottom_p = [0, -1, 0]
        trans_vect = complex(np.cos((2 * PI) / 3), np.sin((2 * PI) / 3))
        bottom_vect = complex(bottom_p[0], bottom_p[1])
        left_vect = bottom_vect * trans_vect
        right_vect = left_vect * trans_vect
        right_p = [left_vect.real, left_vect.imag, 0]
        left_p = [right_vect.real, right_vect.imag, 0]
        tri_points = [right_p, left_p, bottom_p]
        main_tri = Polygon(*tri_points, stroke_color=color)

        # mid lines
        lines = []
        for x in tri_points:
            lines.append(Line(center_p, x, stroke_color=color, stroke_width=2))
        line_group = VGroup(*lines)

        # LOS triangle
        LOS_tri = Polygon(center_p, right_p, left_p, stroke_color=color, stroke_width=2)
        angles = []
        angles.append(Arc(PI / 6, 2 * PI / 3, radius=0.12))
        angles.append(Arc(PI, PI / 6, radius=0.2, arc_center=right_p))
        angles.append(Arc(0, -PI / 6, radius=0.2, arc_center=left_p))
        labels = []
        labels.append(TexMobject('120^\\circ', color=colors['a']).scale(0.33).move_to([0.15, 0.2, 0]))
        labels.append(TexMobject('30^\\circ', color=colors['rh']).scale(0.33).move_to(right_p).shift([-0.35, -0.09, 0]))
        labels.append(TexMobject('30^\\circ', color=colors['rh']).scale(0.33).move_to(left_p).shift([0.4, -0.09, 0]))
        return main_tri, line_group, LOS_tri, [angles, labels]

    def height_triangle(self):
        points = [[0, 1, 0], [0, -1, 0], [1.4, -1, 0]]
        right_box_points = [[0, -1, 0], [0.1, -1, 0], [0.1, -0.9, 0], [0, -0.9, 0]]
        main_tri = Polygon(*points)
        right_box = Polygon(*right_box_points)
        MainGroup = VGroup(main_tri, right_box)
        return MainGroup


class CrossBase(GraphScene):
    # configs for the graph to be used
    CONFIG = {
        "x_min": 0,
        "x_max": 0.83,
        "x_axis_width": 6.39,
        "x_tick_frequency": 0.2,
        "x_axis_label": "$h$",
        "y_min": 0,
        "y_max": 1.1,
        "y_axis_height": 3.6,
        "y_tick_frequency": 0.5,
        "y_axis_label": None,
        "axes_color": BLUE,
        "graph_origin": np.array([0.355, -3.8, 0]),
        "function_color": WHITE
    }

    def construct(self):
        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Cross-Sectional Base', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # Pull all texts and equations from methods
        texts = self.all_texts(title)
        equations = self.equations()

        # Lines
        lines = [Line([0, 0, 0], [0, -4, 0]),
                 Line([0, 0, 0], [7.1, 0, 0])]
        left_box = Line([0, 0, 0], [-7.1, 0, 0])

        # highlight boxes
        h_boxes = [SurroundingRectangle(texts[7][1], color=colors['h']),
                   SurroundingRectangle(texts[7][2], color=colors['h']),
                   SurroundingRectangle(texts[7][3], color=colors['h'])]

        # Draw right box
        for x in lines:
            self.play(Write(x))

        # Draw Equation
        self.play(*[Write(x, run_times=1.5)
                    for x in equations[0]])
        self.wait()

        # Text 0
        for x in texts[0]:
            self.play(Write(x))
        self.wait()

        # Fade out all of equation1 execpt (h)
        self.play(*[FadeOut(equations[0][x])
                    for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21]])

        # Equation 0-1 (Scale and focus (h))
        self.play(*[ReplacementTransform(equations[0][x], equations[1][y])
                    for x, y in zip([15, 16, 17, 18], [0, 1, 2, 3])])

        # text 0-1
        for x in range(3):
            self.play(ReplacementTransform(texts[0][x], texts[1][x], run_time=waits['m']))
        self.wait()

        # Left Box
        for x in left_box:
            self.play(ShowCreation(x))

        # Fade Out equation
        self.play(FadeOut(equations[1]))

        # Cross-Section triangle
        mover_tris = []
        start_tri = self.tris(2).move_to([-3.55, -1.8, 0])
        end_tri = self.tris(0.001).move_to([-3.55, -1.8, 0])
        for x in np.linspace(2, 0.001, 10):
            mover_tris.append(self.tris(x).move_to([-3.55, -1.8, 0]))
        self.play(ShowCreation(start_tri))
        self.wait()
        self.play(Succession(*[Transform(start_tri, x, rate_func=linear)
                               for x in mover_tris],
                             Transform(start_tri, end_tri), run_time=2.083))
        self.wait(0.4167)
        self.play(Succession(*[Transform(start_tri, x, rate_func=linear)
                               for x in mover_tris[::-1]], run_time=2.083))

        # Lengths and texs
        lengths, texs = self.labels(2)
        lengths.move_to([-3.55, -1.8, 0])
        texs[0].move_to([-3, -3, 0])
        texs[1].move_to([-4, -2, 0])
        for x in [*lengths, *texs]:
            self.play(Write(x))
        self.wait()

        # Text 1-2
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[1][x], run_time=waits['m']),
                      Write(texts[2][x], run_time=waits['m']))
        self.play(FadeOutAndShiftDown(texts[1][2]))
        self.play(*[Write(x, run_time=1.5)
                    for x in texts[2][2]])
        self.wait(2.5)

        # Text 2-3
        for x in range(2):
            self.play(FadeOutAndShift(texts[2][x], RIGHT, run_time=waits['m']),
                      FadeInFrom(texts[3][x], LEFT, run_time=waits['m']))
        self.wait(2.25)

        # Text 3-4
        for x in range(2):
            self.play(FadeOutAndShift(texts[3][x], RIGHT, run_time=waits['m']),
                      FadeInFrom(texts[4][x], LEFT, run_time=waits['m']))
        self.wait(2)

        # Fade Out all of text 2 equation execpt B(h), and merge to text4
        self.play(*[FadeOut(texts[2][2][x])
                    for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18]])
        self.play(ReplacementTransform(texts[2][2][10:14], texts[4][1][1:]))
        self.wait(0.5)

        # text 4-5
        for x in range(2):
            self.play(ShrinkToCenter(texts[4][x], run_time=waits['m']),
                      GrowFromCenter(texts[5][x], run_time=waits['m']))
        self.play(GrowFromCenter(texts[5][2], run_time=waits['m']))
        self.wait(3.5)

        # text 5-6
        for x in range(3):
            self.play(FadeOutAndShiftDown(texts[5][x], run_time=waits['m']),
                      Write(texts[6][x], run_time=waits['m']))
        self.wait(2)

        # Function graph
        graph = self.b_function_graph()
        self.play(ShowCreation(graph, run_time=2))

        # Fade Triangle
        self.play(*[FadeOut(x)
                    for x in [*lengths, *texs, start_tri]])

        # Write bullet points(text7, title and bull_1)
        for x in texts[7][:2]:
            self.play(Write(x, run_time=waits['m']))

        # Fade Graph...ISH(Manim bug doesn't allow to fade graph, so this is a work around)
        b_box = Polygon([0.2, -0.2, 0], [0.2, -4, 0], [7.1, -4, 0], [7.1, -0.2, 0], color='#000000'
                        ).set_fill(color='#000000', opacity=1)
        self.play(FadeIn(b_box))

        # Explain second bullet point + second bullet point
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[6][x + 1]),
                      Write(texts[6][x + 3]))
        self.wait(2)
        self.play(Write(texts[7][2]))
        self.wait()

        # Explain third bullet point + third bullet point
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[6][x + 3]),
                      Write(texts[6][x + 5]))
        self.wait()
        self.play(Write(texts[7][3]))
        self.wait()

        # Fade Top Text
        for i in [texts[6][0], texts[6][5], texts[6][6]]:
            self.play(*[FadeOut(x, run_time=waits['m'])
                        for x in i])
        self.wait()

        # Use first clue
        self.play(ShowCreation(h_boxes[0]))
        self.wait()
        for x in [texts[8][0], texts[8][1]]:
            self.play(Write(x))
        self.wait()
        for x, y in zip([texts[8][0], texts[8][1]], [texts[8][2], texts[8][3]]):
            self.play(FadeOutAndShiftDown(x),
                      Write(y))
        self.wait()
        self.play(ReplacementTransform(texts[8][2].copy(), texts[8][4]))
        self.wait()
        self.play(ReplacementTransform(texts[8][3].copy(), texts[9][0]))
        self.wait(2)

        self.play(*[FadeOut(x)
                    for x in [texts[8][2], texts[8][4]]])

        # Use second clue
        self.play(FadeOut(h_boxes[0]),
                  ShowCreation(h_boxes[1]))
        self.wait()
        self.play(ReplacementTransform(texts[8][3], texts[10][0]))
        self.wait(2)
        self.play(*[ReplacementTransform(texts[10][0][x], texts[10][1][y])
                    for x, y in zip([0, 1, 3, 4, 5, 7, 8],
                                    [2, 3, 5, 6, 7, 10, 11])],
                  *[FadeOutAndShiftDown(texts[10][0][x])
                    for x in [2, 6]],
                  *[ReplacementTransform(texts[7][2][3].copy(), texts[10][1][x])
                    for x in [4, 9]],
                  FadeIn(texts[10][1][8]))
        self.wait()
        self.play(ReplacementTransform(texts[7][2][5].copy(), texts[10][1][0]),
                  FadeIn(texts[10][1][1]))
        self.wait()
        self.play(*[ReplacementTransform(texts[10][1][x], texts[10][2][y])
                    for x, y in zip([0, 1, 7, 8, 9, 10, 11],
                                    [0, 1, 2, 3, 4, 5, 6])],
                  *[FadeOutAndShiftDown(texts[10][1][x])
                    for x in [2, 3, 4, 5, 6]])
        self.wait()
        self.play(*[ReplacementTransform(texts[10][2][x], texts[10][3][y])
                    for x, y in zip([0, 1, 6],
                                    [0, 1, 2])],
                  *[FadeOutAndShiftDown(texts[10][2][x])
                    for x in [2, 3, 4, 5]])
        self.wait()
        self.play(*[ReplacementTransform(texts[10][3][x], texts[10][4][y])
                    for x, y in zip([0, 1, 2], [2, 1, 0])])
        self.wait()
        self.play(ReplacementTransform(texts[10][4], texts[9][1]))
        self.wait()

        # Use third clue
        self.play(FadeOut(h_boxes[1]),
                  ShowCreation(h_boxes[2]))
        self.wait()
        self.play(*[ReplacementTransform(texts[9][0][x].copy(), equations[3][x])
                    for x in range(9)])
        self.wait()
        self.play(*[ReplacementTransform(equations[3][x], equations[4][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8],
                                    [0, 1, 3, 9, 10, 11, 12, 13, 14])],
                  *[ReplacementTransform(texts[7][3][2].copy(), equations[4][3:8])],
                  FadeOut(equations[3][2]))
        self.wait()
        self.play(*[ReplacementTransform(equations[4][x], equations[5][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14],
                                    [0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 20, 21])],
                  ReplacementTransform(equations[4][2:9].copy(), equations[5][13:20]),
                  FadeIn(equations[5][12]),
                  FadeOutAndShiftDown(equations[4][12]))
        self.wait()
        self.play(*[ReplacementTransform(equations[5][x], equations[6][x + 2])
                    for x in range(22)],
                  *[ReplacementTransform(texts[7][3][4].copy(), equations[6][x])
                    for x in range(2)])
        self.wait()
        self.play(*[ReplacementTransform(equations[6][x], equations[7][y])
                    for x, y in zip([0, 1, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23],
                                    [0, 1, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12])],
                  *[FadeOutAndShiftDown(equations[6][x])
                    for x in [2, 3, 5, 6, 7, 8, 9, 11]])
        self.wait()
        self.play(*[ReplacementTransform(equations[7][x], equations[8][y])
                    for x, y in zip([1, 2, 3, 5, 6, 7, 8, 9, 11, 12],
                                    [2, 3, 4, 6, 7, 8, 9, 10, 0, 1])],
                  FadeOutAndShiftDown(equations[7][0]))
        self.wait()
        self.play(*[ReplacementTransform(equations[8][x], equations[9][y])
                    for x, y in zip([0, 1, 2, 3, 6, 7, 8, 9, 10],
                                    [1, 2, 12, 13, 5, 6, 7, 8, 9])],
                  FadeOutAndShiftDown(equations[8][4]),
                  FadeIn(equations[9][3]))
        self.wait()
        self.play(*[ReplacementTransform(equations[9][x], equations[10][y])
                    for x, y in zip([1, 2, 3, 5, 6, 7, 9, 12, 13],
                                    [1, 3, 4, 5, 6, 7, 2, 9, 10])],
                  FadeOutAndShiftDown(equations[9][8]))
        self.wait()
        self.play(*[ReplacementTransform(equations[10][x], equations[11][x])
                    for x in [0, 1, 2, 4, 5, 6, 7, 9, 10]],
                  ReplacementTransform(equations[10][3], texts[9][1][0]),
                  ReplacementTransform(texts[9][1][2].copy(), equations[11][3]))
        self.wait()
        self.play(*[FadeOutAndShiftDown(equations[11][x])
                    for x in [3, 5]])
        self.wait()
        self.play(*[ReplacementTransform(equations[11][x], equations[12][y])
                    for x, y in zip([1, 2, 4, 6, 7, 9, 10],
                                    [1, 2, 5, 3, 6, 8, 9])],
                  ReplacementTransform(equations[11][7].copy(), equations[12][4]))
        self.wait()
        self.play(*[ReplacementTransform(equations[12][x], equations[13][y])
                    for x, y in zip([1, 2, 3, 4, 5, 6, 8, 9],
                                    [1, 5, 2, 3, 4, 5, 7, 8])])
        self.wait()
        self.play(*[ReplacementTransform(equations[13][x], texts[9][2][y])
                    for x, y in zip([1, 2, 3, 4, 5, 7, 8],
                                    [3, 4, 5, 6, 7, 1, 0])])
        self.wait()

        # Putting it all together
        self.play(FadeOut(h_boxes[2]))
        self.play(Write(texts[11][0]))
        self.wait()
        self.play(*[ReplacementTransform(texts[9][0][x].copy(), texts[11][1][x])
                    for x in range(9)])
        self.wait()
        self.play(*[ReplacementTransform(texts[11][1][x], texts[11][2][x])
                    for x in range(8)],
                  ReplacementTransform(texts[11][1][8], texts[9][1][0]),
                  ReplacementTransform(texts[9][1][2].copy(), texts[11][2][8]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][2][x], texts[11][3][y])
                    for x, y in zip([0, 1, 2, 3, 4, 6, 7, 8],
                                    [0, 1, 2, 3, 4, 13, 14, 15])],
                  ReplacementTransform(texts[11][2][5], texts[9][2][0]),
                  *[ReplacementTransform(texts[9][2][x].copy(), texts[11][3][y])
                    for x, y in zip([3, 4, 5, 6, 7],
                                    [6, 7, 8, 9, 10])],
                  FadeIn(texts[11][3][12]))
        self.wait()

        # Finishing up
        self.play(FadeOut(texts[11][0]),
                  Write(texts[12][0]))
        self.wait(2)

        # CleanUp All
        self.play(*[FadeOut(x, run_time=3)
                    for x in [*lines, left_box, title, texts[12][0], texts[11][3],
                              *texts[9], *texts[7], small_l]])

    # A way of organizing all the texts into a single method
    def all_texts(self, title):
        # The all-incompassing container (tg = text group)
        tg = []

        # Add a group of texts inside the larger list
        tg.append([])
        # [group]
        tg[0].append(TextMobject("We can't simplify the integral yet.").next_to(title, DOWN, 0.5))
        tg[0].append(TextMobject("We must first figure out the function").next_to(tg[0][0], DOWN))
        tg[0].append(TexMobject('A', '(', 'h', ')').next_to(tg[0][1], DOWN))
        tg[0][2][0].set_color(colors['a'])
        tg[0][2][2].set_color(colors['rh'])

        # 1
        tg.append([])
        tg[1].append(TextMobject("This function describes the area of a cross-sectional"
                                 ).next_to(title, DOWN, 0.5))
        tg[1].append(TextMobject("triangle given the height of the cross-section."
                                 ).next_to(tg[1][0], DOWN))
        tg[1].append(TextMobject("Let's take a closer look at the triangle."
                                 ).next_to(tg[1][1], DOWN))

        # 2
        tg.append([])
        tg[2].append(TextMobject("Each cross-section has a height and base"
                                 ).next_to(title, DOWN, 0.5))
        tg[2].append(TextMobject("that we can use to find the area."
                                 ).next_to(tg[2][0], DOWN))
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                                'B', '\\left(', 'h', '\\right)', '\\cdot', 'H', '\\left(',
                                'h', '\\right)'
                                ).next_to(tg[2][1], DOWN))
        tg[2][2][0].set_color(colors['a'])
        tg[2][2][2].set_color(colors['rh'])
        tg[2][2][10].set_color(colors['b'])
        tg[2][2][12].set_color(colors['rh'])
        tg[2][2][15].set_color(colors['ph'])
        tg[2][2][17].set_color(colors['rh'])

        # 3
        tg.append([])
        tg[3].append(TextMobject("Now we're a little closer, but not done yet.").next_to(title, DOWN, 0.5))
        tg[3].append(TextMobject("We've broken down ", 'A', '(', 'h', ') ', "into two smaller functions"
                                 ).next_to(tg[3][0], DOWN))
        tg[3][1][1].set_color(colors['a'])
        tg[3][1][3].set_color(colors['rh'])

        # 4
        tg.append([])
        tg[4].append(TextMobject("But we still have to solve the smaller functions.").next_to(title, DOWN, 0.5))
        tg[4].append(TextMobject("Let's start with ", '$B$', '$($', '$h$', '$)$').next_to(tg[4][0], DOWN))
        tg[4][1][1].set_color(colors['b'])
        tg[4][1][3].set_color(colors['rh'])

        # 5
        tg.append([])
        tg[5].append(TextMobject('B', '(', 'h', ') ', "takes the height of a cross-section").next_to(title, DOWN, 0.5))
        tg[5].append(TextMobject("as an input, and outputs the base of the cross-sectional triangle."
                                 ).next_to(tg[5][0], DOWN))
        tg[5].append(TextMobject("With that in mind, we can start investigating."
                                 ).next_to(tg[5][1], DOWN))
        tg[5][0][0].set_color(colors['b'])
        tg[5][0][2].set_color(colors['rh'])

        # 6
        tg.append([])
        tg[6].append(TextMobject("Upon investigation, we can find a few hints to aide us.", color=colors['h']
                                 ).next_to(title, DOWN, 0.5))
        tg[6].append(TextMobject("First, the function appears to be linear."
                                 ).next_to(tg[6][0], DOWN))
        tg[6].append(TextMobject("Im presenting it as a given, but feel free to figure out why!"
                                 ).next_to(tg[6][1], DOWN))
        tg[6].append(TextMobject("Second, at the lowest cross-section(", "B", "(0)),"
                                 ).next_to(tg[6][0], DOWN))
        tg[6].append(TextMobject("The base of the triangle is equal to any edge of the ", "tetrahedron", "."
                                 ).next_to(tg[6][1], DOWN))
        tg[6][4][1].set_color(colors['h'])
        tg[6].append(TextMobject("Lastly, at the highest cross-section(The top of the ", "tetrahedron", "),"
                                 ).next_to(tg[6][0], DOWN))
        tg[6][5][1].set_color(colors['h'])
        tg[6].append(TextMobject("the cross-section is a point and thus has no edge length."
                                 ).next_to(tg[6][1], DOWN))

        # 7
        tg.append([])
        tg[7].append(TextMobject("CLUES:"))
        tg[7].append(TextMobject("$\\bullet$ ", "B", "(", "h", ") is linear."
                                 ))
        tg[7].append(TextMobject("$\\bullet$ ", "B", "(", "$0$", ")=", " $a$"
                                 ))
        tg[7].append(TextMobject("$\\bullet$ ", "B", "$\\left({a\\sqrt6\\over3}\\right)$", "$=$", "$0$"
                                 ))
        # arrange 7 as group
        VGroup(*tg[7]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift([0, -1.75, 0])

        # 8
        tg.append([])
        tg[8].append(TextMobject("Every linear function can be expressed as").next_to(title, DOWN, 0.5))
        tg[8].append(TexMobject('y', '=', 'm', 'x', '+', 'b').next_to(tg[8][0], DOWN))
        tg[8].append(TextMobject("We'll change symbles to better match our situation"
                                 ).next_to(title, DOWN, 0.5))
        tg[8].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b').next_to(tg[8][0], DOWN))
        tg[8].append(TextMobject("Now it's a matter of finding the Slope(m) and y-intercept(b)"
                                 ).next_to(tg[8][3], DOWN))
        tg[8][3][0].set_color(colors['b'])
        tg[8][3][2].set_color(colors['rh'])
        tg[8][3][6].set_color(colors['rh'])

        # 9 BR list
        tg.append([])
        tg[9].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                ).scale(1.4).move_to([3.55, 0, 0]).align_to(tg[7][0], UP))
        tg[9].append(TexMobject('b', '=', 'a').scale(1.4).next_to(tg[9][0], DOWN))
        tg[9].append(TexMobject('m', '=', '{', '-', '\\sqrt', '6',
                                '\\over', '2', '}').scale(1.4).next_to(tg[9][1], DOWN))
        tg[9][0][0].set_color(colors['b'])
        tg[9][0][2].set_color(colors['rh'])
        tg[9][0][6].set_color(colors['rh'])
        tg[9][1][2].set_color(colors['a'])

        # 10 (Should have been placed under equations, but it works)
        tg.append([])
        tg[10].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(2).move_to(tg[8][3]))
        tg[10].append(TexMobject('a', '=', 'B', '\\left(', '0', '\\right)', '=', 'm', '\\cdot', '0', '+', 'b'
                                 ).scale(2).move_to(tg[10][0]))
        tg[10].append(TexMobject('a', '=', 'm', '\\cdot', '0', '+', 'b'
                                 ).scale(2).move_to(tg[10][0]))
        tg[10].append(TexMobject('a', '=', 'b'
                                 ).scale(2).move_to(tg[10][0]))
        tg[10].append(TexMobject('b', '=', 'a'
                                 ).scale(2).move_to(tg[10][0]))
        tg[10][0][0].set_color(colors['b'])
        tg[10][0][2].set_color(colors['rh'])
        tg[10][0][6].set_color(colors['rh'])
        tg[10][1][0].set_color(colors['a'])
        tg[10][1][2].set_color(colors['b'])
        tg[10][2][0].set_color(colors['a'])
        tg[10][3][0].set_color(colors['a'])
        tg[10][4][2].set_color(colors['a'])

        # 11
        tg.append([])
        tg[11].append(TextMobject("Lastly, we'll put it all together.").next_to(title, DOWN, 0.5))
        tg[11].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(1.5).next_to(tg[11][0], DOWN))
        tg[11].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'a'
                                 ).scale(1.5).next_to(tg[11][0], DOWN))
        tg[11].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', '{', '-', '\\sqrt', '6', '\\over', '2', '}',
                                 '\\cdot', 'h', '+', 'a').scale(1.5).next_to(tg[11][0], DOWN))
        tg[11][1][0].set_color(colors['b'])
        tg[11][1][2].set_color(colors['rh'])
        tg[11][1][6].set_color(colors['rh'])
        tg[11][2][0].set_color(colors['b'])
        tg[11][2][2].set_color(colors['rh'])
        tg[11][2][6].set_color(colors['rh'])
        tg[11][2][8].set_color(colors['a'])
        tg[11][3][0].set_color(colors['b'])
        tg[11][3][2].set_color(colors['rh'])
        tg[11][3][13].set_color(colors['rh'])
        tg[11][3][15].set_color(colors['a'])

        # 12
        tg.append([])
        tg[12].append(TextMobject("And our function is complete!").next_to(title, DOWN, 0.5))

        return tg

    def equations(self):
        # eq = equation group
        eq = []

        # 0 integrall Full
        eq.append(TexMobject('V', '=', '\\int', '_{', '0', '}', '^{', "{", "a", "\\sqrt", "6", "\\over", "3", "}", '}',
                             'A', '(', 'h', ')', '\\cdot', 'd', 'h'
                             ).move_to([3.55, -2, 0]))
        eq[0][0].set_color(colors['v'])
        eq[0][15].set_color(colors['a'])
        eq[0][17].set_color(colors['rh'])
        eq[0][21].set_color(colors['rh'])

        # 1 integrall highlight
        eq.append(TexMobject('A', '(', 'h', ')').scale(2).move_to([3.55, -2, 0]))
        eq[1][0].set_color(colors['a'])
        eq[1][2].set_color(colors['rh'])

        # 2 area of cross section
        eq.append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                             'B', '\\left(', 'h', '\\right)', '\\cdot', 'H', '\\left(',
                             'h', '\\right)').move_to([3.55, -2, 0]))

        # 3 for third clue
        eq.append(TexMobject('B', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b').scale(2).move_to([0, 1.6, 0]))
        eq[3][0].set_color(colors['b'])
        eq[3][2].set_color(colors['rh'])
        eq[3][6].set_color(colors['rh'])

        # 4
        eq.append(TexMobject('B', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=', 'm', 'h',
                             '+', 'b'
                             ).scale(1.5).move_to(eq[3]))
        eq[4][0].set_color(colors['b'])
        eq[4][3].set_color(colors['a'])
        eq[4][12].set_color(colors['rh'])

        # 5
        eq.append(TexMobject('B', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=', 'm',
                             '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                             ).scale(1.5).move_to(eq[3]))
        eq[5][0].set_color(colors['b'])
        eq[5][3].set_color(colors['a'])
        eq[5][14].set_color(colors['a'])

        # 6
        eq.append(TexMobject('0', '=', 'B', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=',
                             'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                             ).scale(1.5).move_to(eq[3]))
        eq[6][2].set_color(colors['b'])
        eq[6][5].set_color(colors['a'])
        eq[6][16].set_color(colors['a'])

        # 7
        eq.append(TexMobject('0', '=', 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                             ).scale(1.5).move_to(eq[3]))
        eq[7][5].set_color(colors['a'])

        # 8
        eq.append(TexMobject('-', 'b', '=', 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}'
                             ).scale(1.5).move_to(eq[3]))
        eq[8][6].set_color(colors['a'])

        # 9
        eq.append(TexMobject('{', '-', 'b', '\\over', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '}', '=', 'm'
                             ).scale(1.5).move_to(eq[3]))
        eq[9][5].set_color(colors['a'])

        # 10
        eq.append(TexMobject('{', '-', '3', 'b', '\\over', 'a', '\\sqrt', '6', '}', '=', 'm'
                             ).scale(1.5).move_to(eq[3]))
        eq[10][5].set_color(colors['a'])

        # 11
        eq.append(TexMobject('{', '-', '3', 'a', '\\over', 'a', '\\sqrt', '6', '}', '=', 'm'
                             ).scale(1.5).move_to(eq[3]))
        eq[11][3].set_color(colors['a'])
        eq[11][5].set_color(colors['a'])

        # 12
        eq.append(TexMobject('{', '-', '3', '\\sqrt', '6', '\\over', '6', '}', '=', 'm'
                             ).scale(1.5).move_to(eq[3]))

        # 13
        eq.append(TexMobject('{', '-', '\\sqrt', '6', '\\over', '2', '}', '=', 'm'
                             ).scale(1.5).move_to(eq[3]))
        return eq

    def tris(self, rad):
        # The triangle
        top = [0, rad, 0]
        trans_vect = complex(np.cos((2 / 3) * PI), np.sin((2 / 3) * PI))
        top_vect = complex(top[0], top[1])
        left_vect = top_vect * trans_vect
        right_vect = left_vect * trans_vect
        left = [left_vect.real, left_vect.imag, 0]
        right = [right_vect.real, right_vect.imag, 0]
        points = [top, left, right]
        poly = Polygon(*points, stroke_color=colors['h'])
        return poly

    def labels(self, rad):
        # The triangle
        top = [0, rad, 0]
        trans_vect = complex(np.cos((2 / 3) * PI), np.sin((2 / 3) * PI))
        top_vect = complex(top[0], top[1])
        left_vect = top_vect * trans_vect
        right_vect = left_vect * trans_vect
        left = [left_vect.real, left_vect.imag, 0]
        right = [right_vect.real, right_vect.imag, 0]

        # lines
        bottom = [0, -1, 0]
        height = Line(top, bottom, stroke_color=colors['h'])
        base = Line(left, right, stroke_color=colors['h'])
        lines = [height, base]
        lines_g = VGroup(*lines)

        # letters
        base_tex = TexMobject('B', '(', 'h', ')').scale(0.75).shift([1, -2, 0])
        base_tex[0].set_color(colors['b'])
        base_tex[2].set_color(colors['rh'])
        height_tex = TexMobject('H', '(', 'h', ')').scale(0.75).shift([1, 0, 0])
        height_tex[0].set_color(colors['ph'])
        height_tex[2].set_color(colors['rh'])
        letters = [base_tex, height_tex]

        return lines_g, letters

    def b_function_graph(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(self.b_func, self.function_color)
        func_lab = self.get_graph_label(func_graph, label="B(h)").shift([-3, 2, 0])
        func_group = VGroup(func_graph, func_lab)
        return func_group

    def b_func(self, x):
        return 1 - (6 ** 0.5) / 2 * x


class CrossHeight(Scene):
    def construct(self):
        lines = [
            Line([0, 0, 0], [0, -4, 0]),
            Line([0, 0, 0], [7.1, 0, 0]),
            Line([0, 0, 0], [-7.1, 0, 0])
        ]

        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Cross-Sectional Height', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # gather all texts/equations from methods
        texts = self.texts(title)

        # Create highlight boxes for the bullet points
        h_boxes = []
        for x in texts[2][1:]:
            h_boxes.append(SurroundingRectangle(x, color=colors['h']))

        # texts0 a
        for x in texts[0][0:2]:
            self.play(Write(x, run_time=waits['m']))

        self.play(*[Write(texts[0][2][x], run_time=2)
                    for x in range(19)])
        self.wait(1.5)

        # texts0 b
        for x, y in zip([0, 1], [3, 4]):
            self.play(FadeOutAndShiftDown(texts[0][x], run_time=waits['m']),
                      Write(texts[0][y], run_time=waits['m']))
            self.wait()

        # Fade Out must the equation, and merge the rest
        self.play(*[FadeOut(texts[0][2][x])
                    for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])
        self.wait()
        self.play(*[ReplacementTransform(texts[0][2][x], texts[0][4][y])
                    for x, y in zip([15, 16, 17, 18],
                                    [1, 2, 3, 4])])
        self.wait()

        # Draw box lines
        self.play(*[ShowCreation(x)
                    for x in [lines[0], lines[2]]])

        # Draw Triangle for H(h)
        tri = self.tris(2).move_to([-3.55, -1.8, 0])
        l_line, l_letters = self.labels(2)

        l_line.move_to([-3.55, -1.8, 0])
        l_letters[0].move_to([-3, -3, 0])
        l_letters[1].move_to([-4, -2, 0])

        for x in [tri, l_line, *l_letters]:
            self.play(Write(x))
        self.wait()

        # text 1
        self.play(*[FadeOut(x, run_time=waits['m'])
                    for x in texts[0][3:]])
        for x in texts[1]:
            self.play(Write(x))
            self.wait(waits['s'])
        self.wait()

        # Replace triangle with checklist(bullets)
        self.play(*[FadeOut(x)
                    for x in [tri, l_line, *l_letters]],
                  Write(texts[2][0]))
        self.wait()

        # text 3 and text[2][1](first bullet point)
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[1][x]),
                      FadeInFrom(texts[3][x], UP))
            self.wait(waits['s'])
        self.play(Write(texts[2][1]))
        self.wait()

        # text 4
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[3][x], run_time=waits['m']),
                      Write(texts[4][x], run_time=waits['m']))
        self.play(Write(texts[4][2]))
        self.wait()

        # Right Box
        self.play(ShowCreation(lines[1]))
        self.wait()

        # Draw Triangle for H(h)
        tri2 = self.tris(2).move_to([3.55, -2, 0])
        l_line2, l_letters2 = self.labels(2)
        l_line2.move_to([3.55, -2, 0])
        h_tex = TexMobject('H', color=colors['ph']).move_to([3.9, -2.2, 0])
        a_tex = TexMobject('a', color=colors['a']).move_to([2.4, -2, 0])
        angle_tex = TexMobject('60').move_to([2.6, -3.1, 0])
        angle_arc = Arc(0, PI/3, arc_center=[1.819492, -3.5, 0], radius=0.5)

        self.play(*[ShowCreation(x, run_time=waits['m'])
                    for x in [tri2, l_line2, h_tex, a_tex, angle_arc, angle_tex]])
        self.wait()

        # right box label and fade text[4]
        self.play(Write(texts[5][0]))
        self.play(*[FadeOut(x)
                    for x in texts[4]])
        self.wait()

        # set up first equation for second bullet
        self.play(*[FadeIn(texts[5][1][x], run_time=waits['m'])
                    for x in [0, 2, 3, 6]],
                  *[ReplacementTransform(x.copy(), texts[5][1][y], run_time=waits['m'])
                    for x, y in zip([a_tex, h_tex, angle_tex],
                                    [7, 5, 1])])
        self.wait()

        # second equation
        self.play(ReplacementTransform(texts[5][1][0:3], texts[5][2][0:6]),
                  *[ReplacementTransform(texts[5][1][x], texts[5][2][y])
                    for x, y in zip([3, 5, 6, 7],
                                    [6, 8, 9, 10])])
        self.wait()

        # third equation
        self.play(*[ReplacementTransform(texts[5][2][x], texts[5][3][y])
                    for x, y in zip([1, 2, 3, 4, 6, 8, 10],
                                    [2, 3, 4, 5, 7, 8, 1])],
                  FadeOut(texts[5][2][9]))
        self.wait()

        # finally write second bullet point
        self.play(Write(texts[2][2][0:5]))
        self.play(ReplacementTransform(texts[5][3][:7], texts[2][2][5:]),
                  FadeOut(texts[5][3][7:]))
        self.wait()

        # Fade Out Heigt triangle
        self.play(*[FadeOut(x)
                    for x in [l_line2, h_tex, a_tex, angle_tex, angle_arc, texts[5][0], tri2]])
        self.wait()

        # Write Text 6
        for x in texts[6]:
            self.play(Write(x, run_time=waits['m']))
        self.wait()

        # Write third bullet
        self.play(Write(texts[2][3]))
        self.wait(2.5)

        # text 6-7
        for x in range(2):
            self.play(FadeOutAndShiftDown(texts[6][x], run_time=waits['m']),
                      Write(texts[7][x], run_time=waits['m']))
        self.play(FadeOutAndShiftDown(texts[6][2], run_time=waits['m']))
        self.wait(2)

        # first clue
        self.play(*[FadeOut(x)
                    for x in texts[7]])
        self.play(ShowCreation(h_boxes[0]))
        self.wait()
        self.play(ReplacementTransform(texts[2][1][1:].copy(), texts[8][0]))
        self.wait()
        self.play(Write(texts[8][1]))
        self.wait(1.5)
        self.play(ReplacementTransform(texts[8][1], texts[9][0]))
        self.wait()

        # second clue
        self.play(*[FadeOut(x)
                    for x in [texts[8][0], h_boxes[0]]])
        self.play(ShowCreation(h_boxes[1]))
        self.wait()
        self.play(ReplacementTransform(texts[9][0].copy(), texts[10][0]))
        self.wait()
        self.play(*[ReplacementTransform(texts[10][0][x], texts[10][1][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8],
                                    [0, 1, 3, 4, 5, 6, 7, 8])],
                  ReplacementTransform(texts[2][2][3].copy(), texts[10][1][2], run_time=waits['ml']),
                  FadeOut(texts[10][0][2]))
        self.wait()
        self.play(*[ReplacementTransform(texts[10][1][x], texts[10][2][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 7, 8],
                                    [0, 1, 2, 3, 4, 5, 8, 9])],
                  ReplacementTransform(texts[10][1][2].copy(), texts[10][2][7]),
                  FadeIn(texts[10][2][6]),
                  FadeOut(texts[10][1][6]))
        self.wait()
        self.play(ReplacementTransform(texts[10][2], texts[10][3][8:]),
                  ReplacementTransform(texts[2][2][5].copy(), texts[10][3][:7]),
                  FadeIn(texts[10][3][7]))
        self.wait()
        self.play(FadeOutAndShiftDown(texts[10][3][8:12]))
        self.wait()
        self.play(*[ReplacementTransform(texts[10][3][x], texts[10][4][y])
                    for x, y in zip([*range(0, 8), *range(12, 18)],
                                    [*range(0, 8), *range(7, 13)])])
        self.wait()
        self.play(FadeOutAndShiftDown(texts[10][4][8:11]))
        self.play(FadeOut(texts[10][4][11]))
        self.wait()
        self.play(*[ReplacementTransform(texts[10][4][x], texts[10][5][y])
                    for x, y in zip([*range(0, 8), 12],
                                    [*range(0, 8), 8])])
        self.wait()
        self.play(*[ReplacementTransform(texts[10][5][x], texts[9][1][y])
                    for x, y in zip([*range(0, 7), 7, 8],
                                    [*range(2, 9), 1, 0])])
        self.wait()

        # use third clue
        self.play(FadeOut(h_boxes[1]))
        self.play(ShowCreation(h_boxes[2]))
        self.wait()
        self.play(Write(texts[11][0]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][0][x], texts[11][1][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8],
                                    [0, 1, 9, 10, 11, 12, 13, 14])],
                  ReplacementTransform(texts[11][0][2], texts[11][1][2:9]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][1][x], texts[11][2][y])
                    for x, y in zip([*range(0, 12), 13, 14],
                                    [*range(0, 12), 20, 21])],
                  ReplacementTransform(texts[11][1][2:9].copy(), texts[11][2][13:20]),
                  FadeOut(texts[11][1][12]),
                  FadeIn(texts[11][2][12]))
        self.wait()
        self.play(ReplacementTransform(texts[11][2], texts[11][3][2:]),
                  ReplacementTransform(texts[2][3][4].copy(), texts[11][3][0]),
                  FadeIn(texts[11][3][1]))
        self.wait()
        self.play(FadeOutAndShiftDown(texts[11][3][2:12]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][3][x], texts[11][4][y])
                    for x, y in zip([0, 1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                                    [0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])])
        self.wait()
        self.play(*[ReplacementTransform(texts[11][4][x], texts[11][5][y])
                    for x, y in zip([1, 2, 3, 5, 6, 7, 8, 9, 11, 12],
                                    [2, 3, 4, 6, 7, 8, 9, 10, 0, 1])],
                  FadeOut(texts[11][4][0]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][5][x], texts[11][6][y])
                    for x, y in zip([0, 1, 2, 3, 4, 6, 7, 8, 9, 10],
                                    [1, 2, 12, 13, 3, 5, 6, 7, 8, 9])])
        self.wait()
        self.play(*[ReplacementTransform(texts[11][6][x], texts[11][7][y])
                    for x, y in zip([1, 2, 3, 5, 6, 7, 9, 12, 13],
                                    [1, 3, 4, 5, 6, 7, 2, 9, 10])],
                  FadeOut(texts[11][6][8]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][7][x], texts[11][8][y])
                    for x, y in zip([1, 2, 3, 4, 5, 6, 7, 9, 10],
                                    [1, 2, 3, 6, 8, 4, 7, 10, 11])],
                  ReplacementTransform(texts[11][7][7].copy(), texts[11][8][5]))
        self.wait()
        self.play(*[ReplacementTransform(texts[11][8][x], texts[11][9][y])
                    for x, y in zip([1, 3, 4, 5, 6, 8, 10, 11],
                                    [1, 2, 3, 4, 5, 7, 9, 10])],
                  *[ReplacementTransform(texts[11][8][x], texts[11][9][6])
                    for x in [2, 7]])
        self.wait()
        self.play(*[ReplacementTransform(texts[11][9][x], texts[9][2][y])
                    for x, y in zip([*range(1, 8), 9, 10],
                                    [*range(3, 10), 1, 0])])
        self.wait()

        # About to combine equations texts
        self.play(FadeOut(h_boxes[2]))
        for x in texts[12]:
            self.play(Write(x))
            self.wait(waits['s'])
        self.play(*[FadeOut(x)
                    for x in texts[12]])
        self.wait()

        # Putting it all together
        self.play(ReplacementTransform(texts[9][0].copy(), texts[13][0]))
        self.wait()
        self.play(*[ReplacementTransform(texts[13][0][x], texts[13][1][y], run_time=waits['m'])
                    for x, y in zip([*range(0, 8)],
                                    [*range(0, 8)])],
                  *[ReplacementTransform(texts[9][1][x].copy(), texts[13][1][y], run_time=waits['ml'])
                    for x, y in zip([3, 4, 5, 6, 7],
                                    [9, 10, 11, 12, 13])],
                  ReplacementTransform(texts[13][0][8], texts[9][1][0], run_time=waits['m']))
        self.wait()
        self.play(*[ReplacementTransform(texts[13][1][x], texts[13][2][y], run_time=waits['m'])
                    for x, y in zip([*range(0, 5),  6,  7,  9, 10, 11, 12, 13],
                                    [*range(0, 5), 14, 15, 17, 18, 19, 20, 21])],
                  *[ReplacementTransform(texts[9][2][x].copy(), texts[13][2][y], run_time=waits['ml'])
                    for x, y in zip([3, 4, 5, 6, 7, 8, 9],
                                    [6, 7, 8, 9, 10, 11, 12])],
                  ReplacementTransform(texts[13][1][5], texts[9][2][0], run_time=waits['m']))
        self.wait()
        self.play(*[ReplacementTransform(texts[13][2][x], texts[13][3][y], run_time=waits['m'])
                    for x, y in zip([*range(0, 7),  8,  9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21],
                                    [*range(0, 7), 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 28, 29])],
                  *[ReplacementTransform(texts[9][1][x].copy(), texts[13][3][y], run_time=waits['ml'])
                    for x, y in zip([3, 4, 5, 6, 7],
                                    [9, 10, 11, 12, 13])],
                  *[FadeIn(texts[13][3][x], run_time=waits['m'])
                    for x in [7, 15]],
                  ReplacementTransform(texts[13][2][7], texts[9][1][0], run_time=waits['m']))
        self.wait()
        self.play(*[ReplacementTransform(texts[13][3][x], texts[13][4][y])
                    for x, y in zip([*range(0, 7), 9, 10, 11, 13, 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 28, 29],
                                    [*range(0, 7), 7,  8,  9, 13, 10, 11, 12, 13, 14, 16, 17, 19, 20, 21, 22, 23])],
                  *[FadeOut(texts[13][3][x])
                    for x in [7, 12, 15]])
        self.wait()
        self.play(*[ReplacementTransform(texts[13][4][x], texts[13][5][y])
                    for x, y in zip([*range(0, 10), *range(12, 24), 10, 11],
                                    [*range(0, 10), *range(10, 22), 8, 9])])
        self.wait()
        self.play(*[ReplacementTransform(texts[13][5][x], texts[13][6][y])
                    for x, y in zip([*range(0, 8), 8, 9, *range(10, 22)],
                                    [*range(0, 8), 9, 10, *range(11, 23)])],
                  ReplacementTransform(texts[13][5][9].copy(), texts[13][6][8]))
        self.wait()
        self.play(*[FadeOutAndShiftDown(texts[13][6][x])
                    for x in [7, 13]])
        self.wait()
        self.play(*[ReplacementTransform(texts[13][6][x], texts[13][7][y])
                    for x, y in zip([*range(0, 7), *range(8, 13), *range(15, 23)],
                                    [*range(0, 7), *range(7, 12), *range(13, 21)])])
        self.wait()

        # Final equation and text
        self.play(ReplacementTransform(texts[13][7], texts[14][1]))
        self.play(Write(texts[14][0]))
        self.wait(3)

        # cleanup
        self.play(*[FadeOut(x, run_time=2)
                    for x in self.mobjects])

    def texts(self, title):
        # main package
        tg = []

        # 0 first group
        tg.append([])
        tg[0].append(TextMobject("Let's take another look our function ", "$A$", "$($", "$h$", "$)$"
                                 ).next_to(title, DOWN, 0.5))
        tg[0][0][1].set_color(colors['a'])
        tg[0][0][3].set_color(colors['rh'])
        tg[0].append(TextMobject("We broke it down into the following equation."
                                 ).next_to(tg[0][0], DOWN))
        tg[0].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                                'B', '\\left(', 'h', '\\right)', '\\cdot', 'H', '\\left(',
                                'h', '\\right)'
                                ).next_to(tg[0][1], DOWN))
        tg[0][2][0].set_color(colors['a'])
        tg[0][2][2].set_color(colors['rh'])
        tg[0][2][10].set_color(colors['b'])
        tg[0][2][12].set_color(colors['rh'])
        tg[0][2][15].set_color(colors['ph'])
        tg[0][2][17].set_color(colors['rh'])
        tg[0].append(TextMobject("Additionally, we solved the function ", "$B$", "$($", "$h$", "$)$"
                                 ).next_to(title, DOWN, 0.5))
        tg[0][3][1].set_color(colors['b'])
        tg[0][3][3].set_color(colors['rh'])
        tg[0].append(TextMobject("Lastly, we just need to solve for ", "$H$", "$($", "$h$", "$)$"
                                 ).next_to(tg[0][0], DOWN))
        tg[0][4][1].set_color(colors['ph'])
        tg[0][4][3].set_color(colors['rh'])

        # text group 1
        tg.append([])
        tg[1].append(TextMobject("The solution for ", "H", "$($", "$h$", "$)$", " is very similar to that of ",
                                 "$B$", "$($", "$h$", "$)$,").next_to(title, DOWN, 0.5))
        tg[1][0][1].set_color(colors['ph'])
        tg[1][0][3].set_color(colors['rh'])
        tg[1][0][6].set_color(colors['b'])
        tg[1][0][8].set_color(colors['rh'])
        tg[1].append(TextMobject("So let's begin investigating and gathering clues!").next_to(tg[1][0], DOWN))

        # 2
        tg.append([])
        tg[2].append(TextMobject("CLUES:"))
        tg[2].append(TextMobject("$\\bullet$ ", "H", "(", "h", ") is linear."
                                 ))
        tg[2].append(TextMobject("$\\bullet$ ", "B", "(", "$0$", ") =", " ${a\\sqrt3\\over2}$"
                                 ))
        tg[2].append(TextMobject("$\\bullet$ ", "B", "$\\left({a\\sqrt6\\over3}\\right)$", " $=$ ", "$0$"
                                 ))
        # arrange 7 as group
        VGroup(*tg[2]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift([0, -1.75, 0])

        # 3 explain first bullet point
        tg.append([])
        tg[3].append(TextMobject("First, similarly to ", "$B$", "$($", "$h$", "$)$,").next_to(title, DOWN, 0.5))
        tg[3][0][1].set_color(colors['b'])
        tg[3][0][3].set_color(colors['rh'])
        tg[3].append(TextMobject("$H$", "$($", "$h$", "$)$ ", "is a linear function.").next_to(tg[3][0], DOWN))
        tg[3][1][0].set_color(colors['ph'])
        tg[3][1][2].set_color(colors['rh'])

        # 4 explain second bullet point
        tg.append([])
        tg[4].append(TextMobject("Secondly, at ", "$H$", "$($", "$0$", "$)$,").next_to(title, DOWN, 0.5))
        tg[4][0][1].set_color(colors['ph'])
        tg[4].append(TextMobject("the function outputs the height of the base triangle.").next_to(tg[4][0], DOWN))
        tg[4].append(TextMobject("So let's find said height!").next_to(tg[4][1], DOWN))

        # 5 equations for second bullet point
        tg.append([])
        tg[5].append(TextMobject("H", "$($", "$0$", "$):$").move_to([0.75, -0.35, 0]))
        tg[5][0][0].set_color(colors['ph'])
        tg[5].append(TexMobject('Sin\\left(', '60', '\\right)', '=', '{', 'H', '\\over', 'a', '}'
                                ).scale(1.5).move_to([0, 1.6, 0]))
        tg[5][1][5].set_color(colors['ph'])
        tg[5][1][7].set_color(colors['a'])
        tg[5].append(TexMobject('{', '\\sqrt', '3', '\\over', '2', '}', '=', '{', 'H', '\\over', 'a', '}'
                                ).scale(1.5).move_to(tg[5][1]))
        tg[5][2][8].set_color(colors['ph'])
        tg[5][2][10].set_color(colors['a'])
        tg[5].append(TexMobject('{', 'a', '\\sqrt', '3', '\\over', '2', '}', '=', 'H').scale(1.5).move_to(tg[5][1]))
        tg[5][3][1].set_color(colors['a'])
        tg[5][3][8].set_color(colors['ph'])

        # 6 explain last bullet point
        tg.append([])
        tg[6].append(TextMobject("Lastly, just like ", "$B$", "(", "h", "),").next_to(title, DOWN, 0.5))
        tg[6][0][1].set_color(colors['b'])
        tg[6].append(TextMobject("At the top of the ", "tetrahedron", "$\\left({a\\sqrt6\\over3}\\right)$,"
                                 ).next_to(tg[6][0], DOWN))
        tg[6][1][1].set_color(colors['h'])
        tg[6].append(TextMobject("Our function ", "$H$ ", "will output 0."
                                 ).next_to(tg[6][1], DOWN))
        tg[6][2][1].set_color(colors['ph'])

        # 7 initiate using the clues
        tg.append([])
        tg[7].append(TextMobject("Now that we've gathered these clues,").next_to(title, DOWN, 0.5))
        tg[7].append(TextMobject("We can start putting them together!").next_to(tg[7][0], DOWN))

        # 8 use first bullet
        tg.append([])
        tg[8].append(TextMobject("H", "(", "h", ")", " is linear.").next_to(title, DOWN, 0.5))
        tg[8].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                ).scale(1.5).next_to(tg[8][0], DOWN))
        tg[8][1][0].set_color(colors['ph'])
        tg[8][1][2].set_color(colors['rh'])
        tg[8][1][6].set_color(colors['rh'])

        # 9 BR list
        tg.append([])
        tg[9].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                ).scale(1.3).move_to([3.55, 0, 0]).align_to(tg[2][0], UP))
        tg[9][0][0].set_color(colors['ph'])
        tg[9][0][2].set_color(colors['rh'])
        tg[9][0][6].set_color(colors['rh'])
        tg[9].append(TexMobject('b', '=', '{', 'a', '\\sqrt', '3', '\\over', '2', '}'
                                ).scale(1.1).next_to(tg[9][0], DOWN, 0.2))
        tg[9][1][3].set_color(colors['a'])
        tg[9].append(TexMobject('m', '=', '{', '-', 'b', '\\sqrt', '6', '\\over', '2', 'a', '}'
                                ).scale(1.1).next_to(tg[9][1], DOWN, 0.2))
        tg[9][2][9].set_color(colors['a'])

        # 10 use second bullet point
        tg.append([])
        tg[10].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(1.5).next_to(tg[8][0], DOWN))
        tg[10][0][0].set_color(colors['ph'])
        tg[10][0][2].set_color(colors['rh'])
        tg[10][0][6].set_color(colors['rh'])
        tg[10].append(TexMobject('H', '\\left(', '0', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[10][1][0].set_color(colors['ph'])
        tg[10][1][6].set_color(colors['rh'])
        tg[10].append(TexMobject('H', '\\left(', '0', '\\right)', '=', 'm', '\\cdot', '0', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[10][2][0].set_color(colors['ph'])
        tg[10].append(TexMobject('{', 'a', '\\sqrt', '3', '\\over', '2', '}', '=', 'H', '\\left(', '0', '\\right)',
                                 '=', 'm', '\\cdot', '0', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[10][3][1].set_color(colors['a'])
        tg[10][3][8].set_color(colors['ph'])
        tg[10].append(TexMobject('{', 'a', '\\sqrt', '3', '\\over', '2', '}', '=', 'm', '\\cdot', '0', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[10][4][1].set_color(colors['a'])
        tg[10].append(TexMobject('{', 'a', '\\sqrt', '3', '\\over', '2', '}', '=', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[10][5][1].set_color(colors['a'])

        # 11 use third bullet point
        tg.append([])
        tg[11].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][0][0].set_color(colors['ph'])
        tg[11][0][2].set_color(colors['rh'])
        tg[11][0][6].set_color(colors['rh'])
        tg[11].append(TexMobject('H', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=',
                                 'm', 'h', '+', 'b').scale(1.5).move_to(tg[10][0]))
        tg[11][1][0].set_color(colors['ph'])
        tg[11][1][3].set_color(colors['a'])
        tg[11].append(TexMobject('H', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=',
                                 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][2][0].set_color(colors['ph'])
        tg[11][2][3].set_color(colors['a'])
        tg[11][2][14].set_color(colors['a'])
        tg[11].append(TexMobject('0', '=', 'H', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '=',
                                 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][3][2].set_color(colors['ph'])
        tg[11][3][5].set_color(colors['a'])
        tg[11][3][16].set_color(colors['a'])
        tg[11].append(TexMobject('0', '=', 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][4][5].set_color(colors['a'])
        tg[11].append(TexMobject('-', 'b', '=', 'm', '\\cdot', '{', 'a', '\\sqrt', '6', '\\over', '3', '}'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][5][6].set_color(colors['a'])
        tg[11].append(TexMobject('{', '-', 'b', '\\over', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '}', '=', 'm'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][6][5].set_color(colors['a'])
        tg[11].append(TexMobject('{', '-', '3', 'b', '\\over', 'a', '\\sqrt', '6', '}', '=', 'm'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][7][5].set_color(colors['a'])
        tg[11].append(TexMobject('{', '-', '3', 'b', '\\sqrt', '6', '\\over', '6', 'a', '}', '=', 'm'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][8][8].set_color(colors['a'])
        tg[11].append(TexMobject('{', '-', 'b', '\\sqrt', '6', '\\over', '2', 'a', '}', '=', 'm'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[11][9][7].set_color(colors['a'])

        # 12
        tg.append([])
        tg[12].append(TextMobject("Like last time,").next_to(title, DOWN, 0.5))
        tg[12].append(TextMobject("We can combine our equations using ", "Substitution").next_to(tg[12][0], DOWN))
        tg[12][1][1].set_color(colors['h'])

        # 13 combination of all equations
        tg.append([])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                                 ).scale(1.5).move_to(tg[10][0]))
        tg[13][0][0].set_color(colors['ph'])
        tg[13][0][2].set_color(colors['rh'])
        tg[13][0][6].set_color(colors['rh'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', '{', 'a', '\\sqrt', '3', '\\over',
                                 '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][1][0].set_color(colors['ph'])
        tg[13][1][2].set_color(colors['rh'])
        tg[13][1][6].set_color(colors['rh'])
        tg[13][1][9].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', 'b', '\\sqrt', '6', '\\over', '2', 'a',
                                 '}', 'h', '+', '{', 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][2][0].set_color(colors['ph'])
        tg[13][2][2].set_color(colors['rh'])
        tg[13][2][12].set_color(colors['a'])
        tg[13][2][14].set_color(colors['rh'])
        tg[13][2][17].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', '\\left(', '{', 'a', '\\sqrt', '3',
                                 '\\over', '2', '}', '\\right)', '\\sqrt', '6', '\\over', '2', 'a','}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][3][0].set_color(colors['ph'])
        tg[13][3][2].set_color(colors['rh'])
        tg[13][3][9].set_color(colors['a'])
        tg[13][3][20].set_color(colors['a'])
        tg[13][3][22].set_color(colors['rh'])
        tg[13][3][25].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', 'a', '\\sqrt', '3',
                                 '\\sqrt', '6', '\\over', '4', 'a', '}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][4][0].set_color(colors['ph'])
        tg[13][4][2].set_color(colors['rh'])
        tg[13][4][7].set_color(colors['a'])
        tg[13][4][14].set_color(colors['a'])
        tg[13][4][16].set_color(colors['rh'])
        tg[13][4][19].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', 'a', '\\sqrt', '{18}',
                                 '\\over', '4', 'a', '}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][5][0].set_color(colors['ph'])
        tg[13][5][2].set_color(colors['rh'])
        tg[13][5][7].set_color(colors['a'])
        tg[13][5][12].set_color(colors['a'])
        tg[13][5][14].set_color(colors['rh'])
        tg[13][5][17].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', 'a', '3', '\\sqrt', '2',
                                 '\\over', '4', 'a', '}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][6][0].set_color(colors['ph'])
        tg[13][6][2].set_color(colors['rh'])
        tg[13][6][7].set_color(colors['a'])
        tg[13][6][13].set_color(colors['a'])
        tg[13][6][15].set_color(colors['rh'])
        tg[13][6][18].set_color(colors['a'])
        tg[13].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', '3', '\\sqrt', '2',
                                 '\\over', '4', '}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).move_to(tg[13][0]))
        tg[13][7][0].set_color(colors['ph'])
        tg[13][7][2].set_color(colors['rh'])
        tg[13][7][13].set_color(colors['rh'])
        tg[13][7][16].set_color(colors['a'])

        # 14 Last equation and text
        tg.append([])
        tg[14].append(TextMobject("And our second function is now complete!").next_to(title, DOWN, 0.5))
        tg[14].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', '3', '\\sqrt', '2',
                                 '\\over', '4', '}', 'h', '+', '{',
                                 'a', '\\sqrt', '3', '\\over', '2', '}'
                                 ).scale(1.5).next_to(tg[14][0], DOWN))
        tg[14][1][0].set_color(colors['ph'])
        tg[14][1][2].set_color(colors['rh'])
        tg[14][1][13].set_color(colors['rh'])
        tg[14][1][16].set_color(colors['a'])

        return tg

    def tris(self, rad):
        # The triangle
        top = [0, rad, 0]
        trans_vect = complex(np.cos((2 / 3) * PI), np.sin((2 / 3) * PI))
        top_vect = complex(top[0], top[1])
        left_vect = top_vect * trans_vect
        right_vect = left_vect * trans_vect
        left = [left_vect.real, left_vect.imag, 0]
        right = [right_vect.real, right_vect.imag, 0]
        points = [top, left, right]
        poly = Polygon(*points, stroke_color=colors['h'])
        return poly

    def labels(self, rad):
        # The triangle
        top = [0, rad, 0]
        trans_vect = complex(np.cos((2 / 3) * PI), np.sin((2 / 3) * PI))
        top_vect = complex(top[0], top[1])
        left_vect = top_vect * trans_vect
        right_vect = left_vect * trans_vect
        left = [left_vect.real, left_vect.imag, 0]
        right = [right_vect.real, right_vect.imag, 0]

        # lines
        bottom = [0, -1, 0]
        height = Line(top, bottom, stroke_color=colors['h'])
        base = Line(left, right, stroke_color=colors['h'])
        lines = [height, base]
        lines_g = VGroup(*lines)

        # letters
        base_tex = TexMobject('B', '(', 'h', ')').scale(0.75).shift([1, -2, 0])
        base_tex[0].set_color(colors['b'])
        base_tex[2].set_color(colors['rh'])
        height_tex = TexMobject('H', '(', 'h', ')').scale(0.75).shift([1, 0, 0])
        height_tex[0].set_color(colors['ph'])
        height_tex[2].set_color(colors['rh'])
        letters = [base_tex, height_tex]
        return lines_g, letters


class CrossArea(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 0.83,  # 0.8164965809 if you want exact height
        "x_axis_width": 6,  # 6.39 legacy
        "x_tick_frequency": 0.11664,
        "x_axis_label": None,
        "y_min": 0,
        "y_max": 0.5,  # 0.4330127019
        "y_axis_height": 3.6,
        "y_tick_frequency": 0.1,
        "y_axis_label": None,
        "axes_color": BLUE,
        "graph_origin": np.array([-6.745, -3.8, 0]),
        "function_color": WHITE
    }
    def construct(self):

        lines = [
            Line([0, 0, 0], [0, -4, 0]),
            Line([0, 0, 0], [7.1, 0, 0]),
            Line([0, 0, 0], [-7.1, 0, 0])
        ]

        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Cross-Sectional Area', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # Gather all texts...and equations
        texts = self.mobs(title)

        # text0
        for x in texts[0]:
            self.play(Write(x, run_time=waits['m']))
            self.wait(waits['ss'])
        self.wait()

        # draw boxes
        self.play(*[Write(x)
                    for x in lines])

        # Show growing and shrinking trinagle from A(h)
        tri = self.solid_tri(2, [-3.55, -2.3, 0])
        mover_tris = []
        for x in np.linspace(2, 0, 25):
            mover_tris.append(self.solid_tri(x, [-3.55, -2.3, 0]))
        self.play(ShowCreation(tri))
        self.play(Succession(*[Transform(tri, x, rate_func=linear)
                               for x in mover_tris], run_time=2.083))
        self.wait(0.4167)
        self.play(Succession(*[Transform(tri, x, rate_func=linear)
                               for x in mover_tris[::-1]], run_time=2.083))
        self.wait()

        # text 1 a
        for x in range(0, 2):
            self.play(FadeOutAndShiftDown(texts[0][x], run_time=waits['m']),
                      Write(texts[1][x], run_time=waits['m']))
            self.wait(waits['ss'])
        self.play(FadeOutAndShiftDown(texts[0][2], run_time=waits['m']),
                  *[Write(x, run_time=waits['m'])
                    for x in texts[1][2]])
        self.wait(2)

        # text 2 b
        self.play(*[ReplacementTransform(texts[1][2][x], texts[1][3][y])
                    for x, y in zip([0, 1, 3, 4, 5, 7, 8, 9],
                                    [0, 4, 6, 7, 8, 10, 14, 15])])
        self.wait()
        self.play(*[Write(texts[1][3][x])
                    for x in [1, 2, 3, 11, 12, 13, 16, 17, 18]])

        # text 2 c
        self.play(*[FadeOut(texts[1][x])
                    for x in [0, 1]],
                  *[Write(texts[1][x])
                    for x in [4, 5]])
        self.wait(2)

        # Start final equation
        self.play(*[FadeOut(texts[1][x])
                    for x in [4, 5]],
                  ReplacementTransform(texts[1][3], texts[2][0]))
        self.play(*[Write(x, run_time=1.5)
                    for x in [*texts[3][0], *texts[3][1]]])
        self.wait(2)

        # First substitution
        self.play(*[ReplacementTransform(texts[2][0][x], texts[2][1][y])
                    for x, y in zip([*range(0, 10), *range(13, 19), 11],
                                    [*range(0, 10), *range(21, 27), 10])],
                  *[FadeOut(x)
                    for x in [texts[2][0][10], texts[2][0][12], texts[3][1][0], texts[3][1][1],
                              texts[3][1][2], texts[3][1][3], texts[3][1][4]]],
                  *[ReplacementTransform(texts[3][1][x], texts[2][1][y])
                    for x, y in zip([*range(5, 16)], [*range(11, 21)])])
        self.wait(1.25)

        # Second substitution
        self.play(*[ReplacementTransform(texts[2][1][x], texts[2][2][y])
                    for x, y in zip([*range(0, 22), 24, 26],
                                    [*range(0, 22), 22, 40])],
                  *[FadeOut(x)
                    for x in [texts[2][1][22], texts[2][1][23], texts[2][1][25], texts[3][0][0:5]]],
                  *[ReplacementTransform(texts[3][0][x], texts[2][2][y])
                    for x, y in zip([*range(5, 21)],
                                    [*range(23, 39)])])
        self.wait(2)

        # stuff equation into corner
        self.play(ReplacementTransform(texts[2][2], texts[3][2]))
        self.wait()

        # Start simplification
        self.play(Write(texts[4][0]))
        self.play(FadeOut(texts[4][0]))

        # First Main equation
        self.play(*[ReplacementTransform(texts[3][2][x], texts[2][3][y])
                    for x, y in zip([*range(0, 10)],
                                    [*range(0, 10)])],
                  *[ReplacementTransform(texts[3][2][x].copy(), texts[2][3][y])
                    for x, y in zip([10, 40],
                                    [10, 48])])
        self.play(*[ReplacementTransform(texts[3][2][x].copy(), texts[2][3][y])
                    for x, y in zip([*range(11, 19), *range(23, 32)],
                                    [*range(11, 20), *range(11, 20)])])
        self.play(*[ReplacementTransform(texts[3][2][x].copy(), texts[2][3][y])
                    for x, y in zip([*range(11, 19), *range(32, 40)],
                                    [*range(20, 29), *range(20, 29)])])
        self.play(*[ReplacementTransform(texts[3][2][x].copy(), texts[2][3][y])
                    for x, y in zip([*range(19, 21), *range(23, 32)],
                                    [*range(29, 39), *range(29, 39)])])
        self.play(*[ReplacementTransform(texts[3][2][x].copy(), texts[2][3][y])
                    for x, y in zip([*range(19, 21), *range(32, 40)],
                                    [*range(39, 48), *range(39, 48)])])
        self.wait()

        # FadeOut lower right
        self.play(*[FadeOut(texts[3][2][x])
                    for x in range(10, 41)])
        self.wait()

        # second Main Equation [4]
        self.play(*[ReplacementTransform(texts[2][3][x], texts[2][4][y])
                    for x, y in zip([*range(0, 5), *range(12, 16), *range(18, 26), *range(28, 36), *range(38, 46),
                                     8, 16, 26, 36, 46],
                                    [*range(0, 5), *range(6, 10), *range(12, 20), *range(22, 30), *range(32, 40),
                                     10, 10, 20, 30, 40])],
                  *[FadeOut(texts[2][3][x])
                    for x in [6, 7, 10, 48]],
                  *[ReplacementTransform(texts[2][3][8].copy(), texts[2][4][x])
                    for x in [20, 30, 40]])
        self.wait(2)

        # third main Equation [5]
        self.play(*[ReplacementTransform(texts[2][4][x], texts[2][5][y])
                    for x, y in zip([*range(0, 16), *range(16, 42)],
                                    [*range(0, 16), *range(17, 43)])],
                  *[ReplacementTransform(texts[2][5][x].copy(), texts[2][5][y])
                    for x, y in zip([8, 18],
                                    [6, 16])])
        self.wait(2)

        # fourth main equation [6]
        self.play(*[ReplacementTransform(texts[2][5][x], texts[2][6][y])
                    for x, y in zip([*range(0, 15), *range(14, 24), *range(25, 34), *range(34, 43)],
                                    [*range(0, 15), *range(14, 24), *range(15, 24), *range(24, 33)])])
        self.wait(2)

        # final main equation [7]
        self.play(*[ReplacementTransform(texts[2][6][x], texts[2][7][y])
                    for x, y in zip([*range(0, 33)],
                                    [*range(0, 33)])],
                  *[ReplacementTransform(texts[2][6][x].copy(), texts[2][7][y])
                    for x, y in zip([6, 16],
                                    [10, 21])])
        self.wait(2)

        self.play(FadeOut(tri))

        # Create Graph
        a_graph = self.a_function_graph()
        a_label = TexMobject('A', '(', 'h', ')', '=').move_to([-3.55, -2, 0])
        a_label[0].set_color(colors['a'])
        a_label[2].set_color(colors['rh'])
        h_label = TexMobject('h', color=colors['rh']).move_to([-0.4, -3.7, 0])
        a_group = VGroup(a_graph, a_label, h_label)

        # Func Lines
        v_lines = self.get_vertical_lines_to_graph(a_graph, 0, 0.81649, 30, stroke_color=colors['h'])
        v_line_start = v_lines[0]

        a_in = ValueTracker(0)
        a_out = ValueTracker(self.a_func(a_in.get_value()))
        a_tex = DecimalNumber(a_out.get_value(), num_decimal_places=4
                              ).add_updater(lambda x: x.set_value(self.a_func(a_in.get_value())))
        a_tex.set_color(colors['h']).next_to(a_label, RIGHT, 0.2)

        # Initialize group
        self.play(*[ShowCreation(x)
                    for x in [v_line_start, a_tex, a_group]])

        # Set func to top
        self.play(Succession(*[Transform(v_line_start, x, rate_func=linear)
                               for x in v_lines]),
                  a_in.set_value, 0.81649,
                  run_time=2.08333)
        self.wait(0.4166666)

        # Return func bottom
        self.play(Succession(*[Transform(v_line_start, x, rate_func=linear)
                               for x in v_lines[::-1]]),
                  a_in.set_value, 0,
                  run_time=2.08333,
                  rate_func=linear)

        # Fade everything
        self.wait(2)
        self.play(*[FadeOut(x, run_time=2)
                    for x in self.mobjects])


    def mobs(self, title):
        tg = []

        # 0
        tg.append([])
        tg[0].append(TextMobject("Let's start with a little bit of review").next_to(title, DOWN, 0.5))
        tg[0].append(TextMobject("$A$", "$($", "$h$", "$)$", " outputs the area of a cross-sectional triangle"
                                 ).next_to(tg[0][0], DOWN))
        tg[0][1][0].set_color(colors['a'])
        tg[0][1][2].set_color(colors['rh'])
        tg[0].append(TextMobject("when given the height of the cross-section."
                                 ).next_to(tg[0][1], DOWN))

        # 1
        tg.append([])
        tg[1].append(TextMobject("We solved for the base and the height of any cross-section."
                                 ).next_to(title, DOWN, 0.5))
        tg[1].append(TextMobject("Next, we'll use the Triangle Area Formula to solve for ", "$A$", "$($", "$h$", "$)$"
                                 ).next_to(tg[1][0], DOWN))
        tg[1][1][1].set_color(colors['a'])
        tg[1][1][3].set_color(colors['rh'])
        tg[1].append(TexMobject('A', '=', '{', '1', '\\over', '2', '}', 'B', '\\cdot', 'H').next_to(tg[1][1], DOWN))
        tg[1][2][0].set_color(colors['a'])
        tg[1][2][7].set_color(colors['b'])
        tg[1][2][9].set_color(colors['ph'])
        tg[1].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                                'B', '\\left(', 'h', '\\right)', '\\cdot', 'H', '\\left(',
                                'h', '\\right)'
                                ).next_to(tg[1][1], DOWN))
        tg[1][3][0].set_color(colors['a'])
        tg[1][3][2].set_color(colors['rh'])
        tg[1][3][10].set_color(colors['b'])
        tg[1][3][12].set_color(colors['rh'])
        tg[1][3][15].set_color(colors['ph'])
        tg[1][3][17].set_color(colors['rh'])
        tg[1].append(TextMobject("Let's use ", "Substitution"
                                 ).next_to(title, DOWN, 0.5))
        tg[1][4][1].set_color(colors['h'])
        tg[1].append(TextMobject("to incorporate our functions into the formula."
                                 ).next_to(tg[1][4], DOWN))

        # 2 Main Equations
        tg.append([])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                                'B', '\\left(', 'h', '\\right)', '\\cdot', 'H', '\\left(',
                                'h', '\\right)'
                                ).move_to([0, 1.7, 0]))
        tg[2][0][0].set_color(colors['a'])
        tg[2][0][2].set_color(colors['rh'])
        tg[2][0][10].set_color(colors['b'])
        tg[2][0][12].set_color(colors['rh'])
        tg[2][0][15].set_color(colors['ph'])
        tg[2][0][17].set_color(colors['rh'])
        tg.append([])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}',
                                '\\left(', '{', '-', '\\sqrt', '6', '\\over', '2', '}',
                                'h', '+', 'a', '\\right)', '\\cdot', 'H', '\\left(',
                                'h', '\\right)').move_to(tg[2][0]))
        tg[2][1][0].set_color(colors['a'])
        tg[2][1][2].set_color(colors['rh'])
        tg[2][1][18].set_color(colors['rh'])
        tg[2][1][20].set_color(colors['a'])
        tg[2][1][23].set_color(colors['ph'])
        tg[2][1][25].set_color(colors['rh'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}', '\\left(',
                                '{', '-', '\\sqrt', '6', '\\over', '2', '}', 'h', '+', 'a', '\\right)',
                                '\\left(', '{', '-', '3', '\\sqrt', '2', '\\over', '4', '}', 'h', '+', '{', 'a',
                                '\\sqrt', '3', '\\over', '2', '}', '\\right)').move_to(tg[2][0]))
        tg[2][2][0].set_color(colors['a'])
        tg[2][2][2].set_color(colors['rh'])
        tg[2][2][18].set_color(colors['rh'])
        tg[2][2][20].set_color(colors['a'])
        tg[2][2][23].set_color(colors['ph'])
        tg[2][2][31].set_color(colors['rh'])
        tg[2][2][34].set_color(colors['a'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}', '\\left(', '{', '3',
                                '\\sqrt', '{12}', '\\over', '8', '}', 'h', '^2', '-', '{', 'a', '\\sqrt', '{18}',
                                '\\over', '4', '}', 'h', '-', '{', '3', 'a', '\\sqrt', '2', '\\over', '4', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '2', '}', '\\right)').move_to(tg[2][0]))
        tg[2][3][0].set_color(colors['a'])
        tg[2][3][2].set_color(colors['rh'])
        tg[2][3][18].set_color(colors['rh'])
        tg[2][3][19].set_color(colors['rh'])
        tg[2][3][22].set_color(colors['a'])
        tg[2][3][28].set_color(colors['rh'])
        tg[2][3][32].set_color(colors['a'])
        tg[2][3][38].set_color(colors['rh'])
        tg[2][3][41].set_color(colors['a'])
        tg[2][3][42].set_color(colors['a'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '3',
                                '\\sqrt', '{12}', '\\over', '16', '}', 'h', '^2', '-', '{', 'a', '\\sqrt', '{18}',
                                '\\over', '8', '}', 'h', '-', '{', '3', 'a', '\\sqrt', '2', '\\over', '8', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}').move_to(tg[2][0]))
        tg[2][4][0].set_color(colors['a'])
        tg[2][4][2].set_color(colors['rh'])
        tg[2][4][12].set_color(colors['rh'])
        tg[2][4][13].set_color(colors['rh'])
        tg[2][4][16].set_color(colors['a'])
        tg[2][4][22].set_color(colors['rh'])
        tg[2][4][26].set_color(colors['a'])
        tg[2][4][32].set_color(colors['rh'])
        tg[2][4][35].set_color(colors['a'])
        tg[2][4][36].set_color(colors['a'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '6',
                                '\\sqrt', '{3}', '\\over', '16', '}', 'h', '^2', '-', '{', '3', 'a', '\\sqrt', '{2}',
                                '\\over', '8', '}', 'h', '-', '{', '3', 'a', '\\sqrt', '2', '\\over', '8', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}').move_to(tg[2][0]))
        tg[2][5][0].set_color(colors['a'])
        tg[2][5][2].set_color(colors['rh'])
        tg[2][5][12].set_color(colors['rh'])
        tg[2][5][13].set_color(colors['rh'])
        tg[2][5][17].set_color(colors['a'])
        tg[2][5][23].set_color(colors['rh'])
        tg[2][5][27].set_color(colors['a'])
        tg[2][5][33].set_color(colors['rh'])
        tg[2][5][36].set_color(colors['a'])
        tg[2][5][37].set_color(colors['a'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '6', '\\sqrt', '{3}', '\\over', '16', '}',
                                'h', '^2', '-', '{', '6', 'a', '\\sqrt', '{2}', '\\over', '8', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}').move_to(tg[2][0]))
        tg[2][6][0].set_color(colors['a'])
        tg[2][6][2].set_color(colors['rh'])
        tg[2][6][12].set_color(colors['rh'])
        tg[2][6][13].set_color(colors['rh'])
        tg[2][6][17].set_color(colors['a'])
        tg[2][6][23].set_color(colors['rh'])
        tg[2][6][26].set_color(colors['a'])
        tg[2][6][27].set_color(colors['a'])
        tg[2].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '3', '\\sqrt', '{3}', '\\over', '8', '}',
                                'h', '^2', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '4', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}').move_to(tg[2][0]))
        tg[2][7][0].set_color(colors['a'])
        tg[2][7][2].set_color(colors['rh'])
        tg[2][7][12].set_color(colors['rh'])
        tg[2][7][13].set_color(colors['rh'])
        tg[2][7][17].set_color(colors['a'])
        tg[2][7][23].set_color(colors['rh'])
        tg[2][7][26].set_color(colors['a'])
        tg[2][7][27].set_color(colors['a'])

        # 3 smaller functions
        tg.append([])
        tg[3].append(TexMobject('H', '\\left(', 'h', '\\right)', '=', '{', '-', '3', '\\sqrt', '2',
                                '\\over', '4', '}', 'h', '+', '{', 'a', '\\sqrt', '3', '\\over', '2', '}'
                                ).move_to([3.55, -1.2, 0]))
        tg[3][0][0].set_color(colors['ph'])
        tg[3][0][2].set_color(colors['rh'])
        tg[3][0][13].set_color(colors['rh'])
        tg[3][0][16].set_color(colors['a'])
        tg[3].append(TexMobject('B', '\\left(', 'h', '\\right)', '=', '{', '-', '\\sqrt', '6', '\\over', '2', '}',
                                'h', '+', 'a').move_to([3.55, -2.8, 0]))
        tg[3][1][0].set_color(colors['b'])
        tg[3][1][2].set_color(colors['rh'])
        tg[3][1][12].set_color(colors['rh'])
        tg[3][1][14].set_color(colors['a'])
        tg[3].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '1', '\\over', '2', '}', '\\left(',
                                '{', '-', '\\sqrt', '6', '\\over', '2', '}', 'h', '+', 'a', '\\right)',
                                '\\left(', '{', '-', '3', '\\sqrt', '2', '\\over', '4', '}', 'h', '+', '{', 'a',
                                '\\sqrt', '3', '\\over', '2', '}', '\\right)').scale(0.65).move_to([3.55, -2, 0]))
        tg[3][2][0].set_color(colors['a'])
        tg[3][2][2].set_color(colors['rh'])
        tg[3][2][18].set_color(colors['rh'])
        tg[3][2][20].set_color(colors['a'])
        tg[3][2][23].set_color(colors['ph'])
        tg[3][2][31].set_color(colors['rh'])
        tg[3][2][34].set_color(colors['a'])

        # 4
        tg.append([])
        tg[4].append(TextMobject("Now we simplify!").move_to([0, 1.7, 0]))
        return tg

    def solid_tri(self, r, loc=[0, 0, 0]):
        t_vect = complex(np.cos(2*PI/3), np.sin(2*PI/3))
        vects = []
        vects.append(complex(0, r))
        vects.append(vects[0] * t_vect)
        vects.append(vects[1] * t_vect)
        points = []
        for x in vects:
            points.append([x.real + loc[0], x.imag + loc[1], 0])
        return Polygon(*points, color=colors['h'], fill_color=colors['h'], fill_opacity=1)

    def a_function_graph(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(self.a_func, self.function_color)
        return func_graph

    def a_func(self, x):
        a = (3 * (3 ** 0.5)) / 8
        b = (-3 * (2 ** 0.5)) / 4
        c = (3 ** 0.5) / 4
        return (a * (x ** 2)) + (b * x) + c


class Integration(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 0.83,  # 0.8164965809 if you want exact height
        "x_axis_width": 6,  # 6.39 legacy
        "x_tick_frequency": 0.11664,
        "x_axis_label": None,
        "y_min": 0,
        "y_max": 0.5,  # 0.4330127019
        "y_axis_height": 3.6,
        "y_tick_frequency": 0.1,
        "y_axis_label": None,
        "axes_color": BLUE,
        "graph_origin": np.array([-6.745, -3.8, 0]),
        "function_color": WHITE
    }
    def construct(self):
        lines = [
            Line([0, 0, 0], [0, -4, 0]),
            Line([0, 0, 0], [7.1, 0, 0]),
            Line([0, 0, 0], [-7.1, 0, 0])
        ]

        # logo plus title
        small_l = TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL)
        title = TextMobject('Integration', color=colors['h']).to_edge(UP)
        self.add(small_l, title)

        # Gather all texts...and equations
        texts = self.mobs(title)

        # text 0
        for x in range(0, 6, 2):
            self.play(Write(texts[0][x]))
            self.play(Write(texts[0][x + 1]))
            self.wait(2)

        # text 1, and lines
        for x in texts[0]:
            self.play(FadeOutAndShiftDown(x, run_time=0.2))
        for x in [*texts[1], *lines]:
            self.play(Write(x, run_time=waits['m']))

        # text 3 highlight boxes
        h_boxes = [
            SurroundingRectangle(texts[1][1][1:6]),
            SurroundingRectangle(texts[1][2][1:3])
        ]
        self.play(ShowCreation(h_boxes[0]))

        # Dh Triangle
        i = 35
        tri, slices, labels, ah_lines = self.dh_trianlge(2.8, [-3.55, -1.8, 0], i)

        self.play(*[ShowCreation(x)
                    for x in [tri, ah_lines[0][0], *ah_lines[1]]])

        # A(h) function
        self.play(Transform(ah_lines[0][0], ah_lines[0][1], rate_func=there_and_back, run_time=4))

        # setting up dh portion
        self.play(*[ShowCreation(x)
                    for x in [slices[0], labels[0]]],
                  *[FadeOut(x)
                    for x in [ah_lines[0][0], *ah_lines[1]]],
                  FadeOut(h_boxes[0]),
                  ShowCreation(h_boxes[1]))
        self.wait()

        # Increasing recs
        self.play(Succession(*[Transform(slices[0], slices[x], rate_func=linear)
                               for x in range(1, i)], run_time=4),
                  Succession(*[Transform(labels[0], labels[x], rate_func=linear)
                               for x in range(1, i)], run_time=4))
        self.wait()

        # text 1-2
        self.play(FadeOut(h_boxes[1]))
        for x, y in zip([*texts[1]], [*texts[2]]):
            self.play(FadeOutAndShiftDown(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
        self.wait()

        # Descreasing recs
        self.play(Succession(*[Transform(slices[0], slices[x], rate_func=linear)
                               for x in range(1, i)[::-1]], run_time=1),
                  Succession(*[Transform(labels[0], labels[x], rate_func=linear)
                               for x in range(1, i)[::-1]], run_time=1))
        self.wait(2)

        # text 2-3
        for x, y in zip([*texts[2]], [*texts[3]]):
            self.play(FadeOutAndShiftDown(x, run_time=waits['m']),
                      Write(y, run_time=waits['m']))
        self.wait(2)

        # Fade Out triangle
        self.play(*[FadeOut(x)
                    for x in [tri, slices[0], labels[0]]])

        # Create Graph, Func, recs, braces and labels
        func = self.a_function_graph()
        self.play(ShowCreation(func))
        r_recs = self.get_riemann_rectangles(func, 0, 0.8164965809, 0.8164965809 / 2, "left",
                                             0, BLACK, 0.6)
        ah_brace = Brace(r_recs[0], RIGHT).shift([-3, 0, 0])
        ah_brace_label = TexMobject('A', '(', 'h', ')').next_to(ah_brace, RIGHT, 0.1)
        dh_brace = Brace(r_recs[0], UP)
        dh_brace_label = TexMobject('d', 'h').next_to(dh_brace, UP, 0.4)

        # Show recs
        self.play(ShowCreation(r_recs))
        self.play(*[ShowCreation(x)
                    for x in [ah_brace, ah_brace_label, dh_brace, dh_brace_label]])
        self.wait(6)

        # Area under curve
        area = self.get_riemann_rectangles(func, 0, 0.8164965809, 0.8164965809 / 512, "left",
                                             0, BLACK, 0.6)
        self.play(ReplacementTransform(r_recs, area),
                  *[FadeOut(x)
                    for x in [ah_brace, ah_brace_label, dh_brace, dh_brace_label]])
        self.wait(17)

        # text 3-4
        for x, y in zip([*texts[3]], [*texts[4]]):
            self.play(FadeOut(x, run_time=waits['m']))
            self.play(Write(y, run_time=waits['m']))

        # Write integral
        self.play(*[Write(x)
                    for x in texts[5][0]])
        self.wait()

        # Move integral
        self.play(Transform(texts[5][0], texts[5][0].copy().scale(1.25).move_to([0, 1.7, 0])),
                  *[FadeOutAndShiftDown(x)
                    for x in texts[4]])
        self.wait()

        # A(h) equation
        self.play(*[Write(x)
                    for x in texts[5][1]])
        self.wait()

        # substitution animations
        a_highlights = [SurroundingRectangle(texts[5][0][15:19]),
                        SurroundingRectangle(texts[5][1][0:4])]
        self.play(*[Write(x)
                    for x in a_highlights])

        self.play(*[ReplacementTransform(texts[5][0][x], texts[5][2][y])
                    for x, y in zip([*range(0, 15), *range(20, 22)],
                                    [*range(0, 15), *range(45, 47)])],
                  *[ReplacementTransform(texts[5][0][x], texts[5][1][y])
                    for x, y in zip([*range(15, 19)],
                                    [*range(0, 4)])],
                  *[ReplacementTransform(texts[5][1][x].copy(), texts[5][2][y])
                    for x, y in zip([*range(5, 33)],
                                    [*range(16, 44)])],
                  *[FadeIn(texts[5][2][x])
                    for x in [15, 44]],
                  *[FadeOut(x)
                    for x in [*a_highlights, texts[5][0][19]]]
                  )
        self.wait()

        # Fade Out bottom
        self.play(*[FadeOut(x)
                    for x in texts[5][1]])
        self.wait()

        # Introduce steps
        self.play(*[Write(texts[8][x])
                    for x in range(2)])

        # anti-derivative across interval
        self.play(*[ReplacementTransform(texts[5][2][x], texts[5][3][y])
                    for x, y in zip([0, 1, 15, 44, *range(2, 15), *range(18, 35), *range(35, 44)],
                                    [0, 1, 2, 32, *range(33, 46), *range(4, 21), *range(22, 31)])],
                  *[FadeOut(texts[5][2][x])
                    for x in [17, 45, 46]],
                  *[FadeIn(texts[5][3][x])
                    for x in [21, 31]])
        self.wait()

        # step 2
        self.play(ReplacementTransform(texts[8][1], texts[8][2]))

        # Final equation...left side
        self.play(*[ReplacementTransform(texts[5][3][x], y)
                    for x, y in zip([*range(0, 33)],
                                    [texts[6][0][0], texts[6][0][1],
                                     texts[6][1][0],
                                     *[texts[6][2][i] for i in range(0, 6)],
                                     *[texts[6][3][i] for i in [0, 9]],
                                     *[texts[6][4][i] for i in range(0, 9)],
                                     *[texts[6][5][i] for i in [0, 9]],
                                     *[texts[6][6][i] for i in range(0, 9)],
                                     texts[6][7][0],
                                     texts[6][8][0]
                                     ])],
                  *[ReplacementTransform(texts[5][3][x].copy(), y)
                    for x, y in zip([9, 20, 31],
                                    [texts[6][3][8], texts[6][5][8], texts[6][7][8]])],
                  *[ReplacementTransform(texts[5][3][38:45].copy(), x)
                    for x in [*[texts[6][3][i] for i in range(1, 8)],
                              *[texts[6][5][i] for i in range(1, 8)],
                              *[texts[6][7][i] for i in range(1, 8)]]],
                  FadeOut(texts[5][3][33:]))
        self.wait(0.5)

        # Final equation...whole equation, just need to simplify
        self.play(*[Write(x)
                    for x in [texts[6][9][0],
                              texts[6][10][0],
                              *[texts[6][11][i] for i in [*range(0, 7)]],
                              *[texts[6][12][i] for i in [*range(0, 10)]],
                              *[texts[6][13][i] for i in [*range(0, 10)]],
                              texts[6][14][0]]])
        self.wait()

        # step 3
        self.play(ReplacementTransform(texts[8][2], texts[8][3]))

        # Simplify the terms multiplied by zero
        self.play(*[FadeOutAndShiftDown(x)
                    for x in [texts[6][9][0],
                              texts[6][10][0],
                              *[texts[6][11][i] for i in [*range(0, 7)]],
                              *[texts[6][12][i] for i in [*range(0, 10)]],
                              *[texts[6][13][i] for i in [*range(0, 10)]],
                              texts[6][14][0]]])
        self.wait()

        # Move equation to center stage
        self.play(*[ReplacementTransform(x, texts[7][0][y])
                    for x, y in zip([*[texts[6][0][i] for i in range(0, 2)],
                                     *[texts[6][2][i] for i in range(0, 6)],
                                     *[texts[6][3][i] for i in range(0, 10)],
                                     *[texts[6][4][i] for i in range(0, 9)],
                                     *[texts[6][5][i] for i in range(0, 10)],
                                     *[texts[6][6][i] for i in range(0, 9)],
                                     *[texts[6][7][i] for i in range(0, 9)]],
                                     [*range(0, 55)])],
                  *[FadeOutAndShiftDown(texts[6][x][0])
                    for x in [1, 8]])
        self.wait()

        # simplify exponents
        self.play(*[ReplacementTransform(texts[7][0][x], texts[7][1][y])
                    for x, y in zip([*range(0, 10), 10, 11, 12, 13, 14, 15, 16, 17, *range(18, 29), 29, 31, 32,
                                     33, 34, 35, 36, 37, *range(38, 55)],
                                    [*range(0, 10), 11, 13, 14, 15, 16, 17, 18, 12, *range(19, 30), 31, 30, 33,
                                     34, 35, 36, 32, 37, *range(38, 55)])],
                  *[FadeOut(texts[7][0][x])
                    for x in [30]],
                  ReplacementTransform(texts[7][0][17].copy(), texts[7][1][10]))
        self.wait()

        # combine products
        self.play(*[ReplacementTransform(texts[7][1][x], texts[7][2][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 19, 21,
                                     22, 23, 24, 25, 26, 30, 31, 32, 33, 34, 37, 39, 40, 41, 42,
                                     43, 44, 48, 49, 50, 51, 52],
                                    [0, 1, 2, 4, 5, 8, 9, 10, 3, 6, 7, 4, 5, 8, 9, 11, 13,
                                     16, 14, 15, 18, 19, 13, 16, 17, 18, 19, 21, 25, 26, 23, 25,
                                     27, 28, 25, 23, 24, 27, 28])],
                  *[FadeOut(texts[7][1][x])
                    for x in [8, 18, 28, 36, 46, 54]])
        self.wait()

        # Lower terms factors
        self.play(*[ReplacementTransform(texts[7][2][x], texts[7][3][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 18, 19, 21,
                                     23, 24, 25, 25, 26, 27, 28, 29],
                                    [0, 1, 8, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 20,
                                     23, 24, 24, 25, 26, 27, 28, 28])],
                  ReplacementTransform(texts[7][2][24].copy(), texts[7][3][22]))
        self.wait()

        # Common denominator
        self.play(*[ReplacementTransform(texts[7][3][x], texts[7][4][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22,
                                     23, 24, 25, 26, 27, 28],
                                    [0, 1, 3, 4, 5, 6, 19, 20, 7, 8, 9, 10, 11, 12, 19, 20, 13, 14,
                                     15, 16, 17, 18, 19, 20])])
        self.wait()

        # Factored equation
        self.play(*[ReplacementTransform(texts[7][4][x], texts[7][5][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7,  8, 9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                                    [0, 1, 3, 4, 5, 6, 9, 10, 3, 4,  5,  6, 11, 12,  3,  4,  6,  5, 14, 15])],
                  *[FadeIn(texts[7][5][x])
                    for x in [7, 8, 13]])
        self.wait()

        # simplified parenthesis
        self.play(*[ReplacementTransform(texts[7][5][x], texts[7][6][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                    [0, 1, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 9, 10, 11])])
        self.wait()

        # Final Equation!
        self.play(*[ReplacementTransform(texts[7][6][x], texts[7][7][y])
                    for x, y in zip([0, 1, 3, 4, 5, 6, 10, 11],
                                    [0, 1, 3, 4, 5, 6, 7, 8])],
                  *[FadeOutAndShiftDown(texts[7][6][x])
                    for x in [7, 8, 9]],
                  FadeOut(title))
        self.wait()

        # Fade Out bottom left
        self.play(*[FadeOut(texts[8][x])
                    for x in [0, 3]])
        self.wait(10)


    def mobs(self, title):
        tg = []

        # 0
        tg.append([])
        tg[0].append(TextMobject('With our function ', 'A', '(', 'h', ')', ' at hand,').next_to(title, DOWN, 0.5))
        tg[0].append(TextMobject('we can integrate the function for volume.').next_to(tg[0][0], DOWN))
        tg[0].append(TextMobject("But first, let's explore exactly").next_to(tg[0][1], DOWN, 0.75))
        tg[0].append(TextMobject("what it means to integrate ", 'A', '(', 'h', ').').next_to(tg[0][2], DOWN))
        tg[0].append(TextMobject("Let's start by defining a process").next_to(tg[0][3], DOWN, 0.75))
        tg[0].append(TextMobject('that approximates a ', 'tetrahedron', ' to increasing precision.'
                                 ).next_to(tg[0][4], DOWN))
        tg[0][0][1].set_color(colors['a'])
        tg[0][0][3].set_color(colors['rh'])
        tg[0][3][1].set_color(colors['a'])
        tg[0][3][3].set_color(colors['rh'])
        tg[0][5][1].set_color(colors['h'])

        # 1
        tg.append([])
        tg[1].append(TextMobject("We're going to approximate our ", "tetrahedron").next_to(title, DOWN, 0.5))
        tg[1].append(TextMobject('using triangular prisms with ', 'Base Area ', 'A', '(', 'h', ')'
                                 ).next_to(tg[1][0], DOWN))
        tg[1].append(TextMobject('and ', 'height d', 'h').next_to(tg[1][1], DOWN))
        tg[1][0][1].set_color(colors['h'])
        tg[1][1][2].set_color(colors['a'])
        tg[1][1][4].set_color(colors['rh'])
        tg[1][2][2].set_color(colors['rh'])

        # 2
        tg.append([])
        tg[2].append(TextMobject("Importantly, as d", "h", " shrinks,").next_to(title, DOWN, 0.5))
        tg[2].append(TextMobject("the prisms grow in number and precision, and the sum"
                                 ).next_to(tg[2][0], DOWN))
        tg[2].append(TextMobject("of their volumes approach the volume of our ", "tetrahedron", "."
                                 ).next_to(tg[2][1], DOWN))
        tg[2][0][1].set_color(colors['rh'])
        tg[2][2][1].set_color(colors['h'])


        # 3
        tg.append([])
        tg[3].append(TextMobject("Additionally, we can represent each prism another way.").next_to(title, DOWN, 0.5))
        tg[3].append(TextMobject("We'll put our prisms on the graph ", "A", "(", "h", ")."
                                 ).next_to(tg[3][0], DOWN))
        tg[3].append(TextMobject("then we'll let d", "h", ' shink, adding the prisms along the way.'
                                 ).next_to(tg[3][1], DOWN))
        tg[3][1][1].set_color(colors['a'])
        tg[3][1][3].set_color(colors['rh'])
        tg[3][2][1].set_color(colors['rh'])

        # 4
        tg.append([])
        tg[4].append(TextMobject("The total volume approaches that of the area under our graph."
                                 ).next_to(title, DOWN, 0.5))
        tg[4].append(TextMobject("In fact, we're describing the work of an integral!"
                                 ).next_to(tg[4][0], DOWN))
        tg[4].append(TextMobject("We can solve the integral for an exact value."
                                 ).next_to(tg[4][1], DOWN))

        # 5
        tg.append([])
        tg[5].append(TexMobject('V', '=', '\\int', '_{', '0', '}', '^{', '{', 'a', '\\sqrt', '6', '\\over', '3',
                                '}', '}', 'A', '(', 'h', ')', '\\cdot', 'd', 'h'
                                ).move_to([3.55, -2, 0]))
        tg[5][0][0].set_color(colors['v'])
        tg[5][0][15].set_color(colors['a'])
        tg[5][0][17].set_color(colors['rh'])
        tg[5][0][21].set_color(colors['rh'])

        tg[5].append(TexMobject('A', '\\left(', 'h', '\\right)', '=', '{', '3', '\\sqrt', '{3}', '\\over', '8', '}',
                                'h', '^2', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '4', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}'
                                ).scale(0.75).move_to([3.55, -2, 0]))
        tg[5][1][0].set_color(colors['a'])
        tg[5][1][2].set_color(colors['rh'])
        tg[5][1][12].set_color(colors['rh'])
        tg[5][1][13].set_color(colors['rh'])
        tg[5][1][17].set_color(colors['a'])
        tg[5][1][23].set_color(colors['rh'])
        tg[5][1][26].set_color(colors['a'])
        tg[5][1][27].set_color(colors['a'])

        tg[5].append(TexMobject('V', '=', '\\int', '_{', '0', '}', '^{', '{', 'a', '\\sqrt', '6', '\\over', '3',
                                '}', '}', '\\left(', '{', '3', '\\sqrt', '{3}', '\\over', '8', '}',
                                'h', '^2', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '4', '}', 'h',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}', '\\right)', 'd', 'h'
                                ).move_to([0, 1.7, 0]))
        tg[5][2][0].set_color(colors['v'])
        tg[5][2][23].set_color(colors['rh'])
        tg[5][2][24].set_color(colors['rh'])
        tg[5][2][28].set_color(colors['a'])
        tg[5][2][34].set_color(colors['rh'])
        tg[5][2][37].set_color(colors['a'])
        tg[5][2][38].set_color(colors['a'])
        tg[5][2][46].set_color(colors['rh'])

        tg[5].append(TexMobject('V', '=', '\\left(', '{', '\\sqrt', '{3}', '\\over', '8', '}',
                                'h', '^3', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '8', '}', 'h', '^2',
                                '+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}', 'h', '\\right)', '\\Biggr|',
                                '_{', '0', '}', '^{', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '}'
                                ).move_to([0, 1.7, 0]))
        tg[5][3][0].set_color(colors['v'])
        tg[5][3][9].set_color(colors['rh'])
        tg[5][3][10].set_color(colors['rh'])
        tg[5][3][14].set_color(colors['a'])
        tg[5][3][20].set_color(colors['rh'])
        tg[5][3][21].set_color(colors['rh'])
        tg[5][3][24].set_color(colors['a'])
        tg[5][3][25].set_color(colors['a'])
        tg[5][3][31].set_color(colors['rh'])

        tg.append([])
        tg[6].append(TexMobject('V', '='))
        tg[6][0][0].set_color(colors['v'])
        tg[6].append(TexMobject('\\left(').scale(3))
        tg[6].append(TexMobject('{', '\\sqrt', '{3}', '\\over', '8', '}'))
        tg[6].append(TexMobject('\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '^3'))
        tg[6][3][2].set_color(colors['a'])
        tg[6].append(TexMobject('-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '8', '}'))
        tg[6][4][3].set_color(colors['a'])
        tg[6].append(TexMobject('\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '^2'))
        tg[6][5][2].set_color(colors['a'])
        tg[6].append(TexMobject('+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}'))
        tg[6][6][2:4].set_color(colors['a'])
        tg[6].append(TexMobject('\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)'))
        tg[6][7][2].set_color(colors['a'])
        tg[6].append(TexMobject('\\right)').scale(3))
        tg[6].append(TexMobject('-'))
        tg[6].append(TexMobject('\\left(').scale(3))
        tg[6].append(TexMobject('{', '\\sqrt', '{3}', '\\over', '8', '}', '\\left(0\\right)'))
        tg[6].append(TexMobject('-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '8', '}', '\\left(0\\right)'))
        tg[6][12][3].set_color(colors['a'])
        tg[6].append(TexMobject('+', '{', 'a', '^2', '\\sqrt', '3', '\\over', '4', '}', '\\left(0\\right)'))
        tg[6][13][2:4].set_color(colors['a'])
        tg[6].append(TexMobject('\\right)').scale(3))
        tg[6].append(VGroup(*tg[6]).arrange_submobjects(direction=RIGHT, buff=0.1).scale(0.7).shift([0, 1.7, 0]))

        tg.append([])
        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{3}', '\\over', '8', '}', '\\left(', '{', 'a', '\\sqrt', '6',
                                '\\over', '3', '}', '\\right)', '^3', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over',
                                '8',
                                '}', '\\left(', '{', 'a', '\\sqrt', '6', '\\over', '3', '}', '\\right)', '^2', '+', '{',
                                'a', '^2', '\\sqrt', '3', '\\over', '4', '}', '\\left(', '{', 'a', '\\sqrt', '6',
                                '\\over', '3', '}', '\\right)').move_to([0, 1.7, 0]))
        tg[7][0][0].set_color(colors['v'])
        tg[7][0][10].set_color(colors['a'])
        tg[7][0][21].set_color(colors['a'])
        tg[7][0][29].set_color(colors['a'])
        tg[7][0][39:41].set_color(colors['a'])
        tg[7][0][48].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{3}', '\\over', '8', '}', '\\left(', '{', '2', 'a', '^3',
                                '\\sqrt', '6',
                                '\\over', '9', '}', '\\right)', '-', '{', '3', 'a', '\\sqrt', '{2}', '\\over', '8',
                                '}', '\\left(', '{', '2', 'a', '^2', '\\over', '3', '}', '\\right)', '+', '{',
                                'a', '^2', '\\sqrt', '3', '\\over', '4', '}', '\\left(', '{', 'a', '\\sqrt', '6',
                                '\\over', '3', '}', '\\right)').move_to([0, 1.7, 0]))
        tg[7][1][0].set_color(colors['v'])
        tg[7][1][11:13].set_color(colors['a'])
        tg[7][1][22].set_color(colors['a'])
        tg[7][1][31:33].set_color(colors['a'])
        tg[7][1][39:41].set_color(colors['a'])
        tg[7][1][48].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '2', '\\sqrt', '{18}', 'a', '^3', '\\over', '72', '}', '-', '{', '6',
                                '\\sqrt', '{2}', 'a', '^3', '\\over', '24', '}', '+', '{', '\\sqrt', '{18}', 'a', '^3',
                                '\\over', '12', '}').move_to([0, 1.7, 0]))
        tg[7][2][0].set_color(colors['v'])
        tg[7][2][6:8].set_color(colors['a'])
        tg[7][2][16:18].set_color(colors['a'])
        tg[7][2][25:27].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{2}', 'a', '^3', '\\over', '12', '}', '-', '{', '3',
                                '\\sqrt', '{2}', 'a', '^3', '\\over', '12', '}', '+', '{', '3', '\\sqrt', '{2}', 'a',
                                '^3', '\\over', '12', '}').move_to([0, 1.7, 0]))
        tg[7][3][0].set_color(colors['v'])
        tg[7][3][5:7].set_color(colors['a'])
        tg[7][3][15:17].set_color(colors['a'])
        tg[7][3][25:27].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{2}', 'a', '^3', '-', '3',
                                '\\sqrt', '{2}', 'a', '^3', '+', '3', '\\sqrt', '{2}', 'a', '^3',
                                '\\over', '12', '}').move_to([0, 1.7, 0]))
        tg[7][4][0].set_color(colors['v'])
        tg[7][4][5:7].set_color(colors['a'])
        tg[7][4][11:13].set_color(colors['a'])
        tg[7][4][17:19].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{2}', 'a', '^3', '\\left(', '1', '-', '3', '+', '3',
                                '\\right)', '\\over', '12', '}').move_to([0, 1.7, 0]))
        tg[7][5][0].set_color(colors['v'])
        tg[7][5][5:7].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{2}', 'a', '^3', '\\left(', '1', '\\right)', '\\over', '12',
                                '}').move_to([0, 1.7, 0]))
        tg[7][6][0].set_color(colors['v'])
        tg[7][6][5:7].set_color(colors['a'])

        tg[7].append(TexMobject('V', '=', '{', '\\sqrt', '{2}', 'a', '^3', '\\over', '12',
                                '}').scale(2.5).to_edge(UP))
        tg[7][7][0].set_color(colors['v'])
        tg[7][7][5:7].set_color(colors['a'])

        # Texts regarding solving the integral
        tg.append([])
        tg[8].append(TextMobject("Step:").scale(1.5).move_to([3.55, -1.5, 0]))
        tg[8].append(TextMobject("Find the Anti-Derivative").next_to(tg[8][0], DOWN))
        tg[8].append(TextMobject("Solve across the interval").next_to(tg[8][0], DOWN))
        tg[8].append(TextMobject("Now Simplify!").next_to(tg[8][0], DOWN))

        return tg

    def dh_trianlge(self, c=1, location=[0, 0, 0], i=5):
        # lines
        line1 = Line([0.57735, 0, 0], [-0.57735, 0, 0], stroke_color=colors['h'])
        line2 = Line([0, 1, 0], [0, 1, 0], stroke_color=colors['h'])
        VGroup(line1, line2).scale(c).move_to(location)
        label_tri_1 = RegularPolygon(3, start_angle=0, stroke_color=colors['a'], stroke_width=8
                                     ).scale(0.20).next_to(line1, LEFT).add_updater(lambda v: v.next_to(line1, LEFT))
        line_label = TexMobject('A', '(', 'h', ')'
                                ).next_to(label_tri_1, LEFT).add_updater(lambda v: v.next_to(label_tri_1, LEFT))
        line_label[0].set_color(colors['a'])
        line_label[2].set_color(colors['rh'])

        # triangle
        tri = Polygon([0, 1, 0], [0.57735, 0, 0], [-0.57735, 0, 0], stroke_width=7
                      ).scale(c).move_to(location)
        fh = lambda x: -0.57735*x + 0.57735
        slices = []
        slice_labels = []
        for n in range(2, 2 + i):
            recs = []
            h = 0
            dx = 1 / n
            for i in range(0, n):
                recs.append(Polygon([-1 * fh(h), dx * i, 0],
                                    [fh(h), dx * i, 0],
                                    [fh(h), dx * (i + 1), 0],
                                    [-1 * fh(h), dx * (i + 1), 0],
                                    stroke_width=3,
                                    stroke_color=colors['h']))
                h += dx
            slices.append(VGroup(*recs).scale(c).move_to(location))
            brace = Brace(recs[0], LEFT)
            brace_label = TexMobject('d', 'h').next_to(brace, LEFT, 0.1)
            brace_label[1].set_color(colors['rh'])
            slice_labels.append(VGroup(brace, brace_label))

        return tri, slices, slice_labels, [[line1, line2], [label_tri_1, line_label]]

    def a_function_graph(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(self.a_func, self.function_color)
        return func_graph

    def a_func(self, x):
        a = (3 * (3 ** 0.5)) / 8
        b = (-3 * (2 ** 0.5)) / 4
        c = (3 ** 0.5) / 4
        return (a * (x ** 2)) + (b * x) + c


class IntegrationBRoll(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 0.83,  # 0.8164965809 if you want exact height
        "x_axis_width": 13,  # 6.39 legacy
        "x_tick_frequency": 0.11664,
        "x_axis_label": None,
        "y_min": 0,
        "y_max": 0.5,  # 0.4330127019
        "y_axis_height": 7,
        "y_tick_frequency": 0.1,
        "y_axis_label": None,
        "axes_color": BLUE,
        "graph_origin": np.array([-6.5, -3.5, 0]),
        "function_color": WHITE
    }

    def construct(self):
        self.wait()
        i = 10

        # Create Graph
        a_func = self.a_function_graph()
        self.play(ShowCreation(a_func))

        # Create list of riemann_rectangle_groups
        rec_groups = self.get_riemann_rectangles_list(a_func, i, 0.81649/2, fill_opacity=0.75)

        # Write tex...20 was an abritrary number to anylize volumes past what i animated
        equ1 = TexMobject('V', '\\approx').scale(2).move_to([3, 2, 0])
        equ1[0].set_color(colors['v'])
        volumes = self.progressing_volume(i + 20, equ1)

        self.play(*[Write(x)
                    for x in [equ1, volumes[0]]])

        # Shrinking rectangles
        self.play(ShowCreation(rec_groups[0], run_time=1.5))
        time = 1.5
        for x in range(1, i):
            self.transform_between_riemann_rects(rec_groups[0], rec_groups[x],
                                                 added_anims=[Transform(volumes[0], volumes[x])],
                                                 run_time=time)
            time = time * 0.8
        for x in range(i, i + 20):
            self.play(Transform(volumes[0], volumes[x], run_time=time))
            time = time * 0.8
        self.wait(3)

    def a_function_graph(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(self.a_func, self.function_color)
        return func_graph

    def a_func(self, x):
        a = (3 * (3 ** 0.5)) / 8
        b = (-3 * (2 ** 0.5)) / 4
        c = (3 ** 0.5) / 4
        return (a * (x ** 2)) + (b * x) + c

    def progressing_volume(self, i, neighbor):
        vols = []
        h = 0.8164965809
        for i in range(i):
            x = 0
            n = i + 2
            dx = h / n
            sum = 0
            for zz in range(n):
                sum += (self.a_func(x)*dx)
                x += dx
            vols.append(DecimalNumber(sum, num_decimal_places=4
                                      ).scale(2).next_to(neighbor, RIGHT, 0.4))
        return vols




