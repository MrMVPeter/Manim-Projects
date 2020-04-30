from manimlib.imports import *
import math


class Intro(Scene):
    def construct(self):
        self.show_peter()
        self.show_problem()

    def show_peter(self):
        peter_big = TextMobject('Peter Gilliam', color='#900000').scale(4.5)
        peter = TextMobject('Peter Gilliam', color='#900000').scale(4).to_edge(UP)
        peter2 = small_logo()
        intro_caption_1 = TextMobject('I have a fun challenge for you'
                                      ).scale(1.2).next_to(peter, DOWN, buff=1)
        intro_caption_2 = TextMobject('What im really saying... ', 'Help me!'
                                      ).scale(1.15).next_to(intro_caption_1, DOWN, buff=0.5)
        intro_caption_2[1].set_color('#FFF200')
        self.play(Write(peter_big, run_time=5))
        self.play(ReplacementTransform(peter_big, peter))
        self.wait(1)
        self.play(Write(intro_caption_1, run_time=1))
        self.wait(1)
        self.play(Write(intro_caption_2[0], run_time=1))
        self.wait(1)
        self.play(Write(intro_caption_2[1], run_time=2))
        self.play(ReplacementTransform(peter, peter2),
                  FadeOutAndShiftDown(intro_caption_1),
                  FadeOutAndShiftDown(intro_caption_2))

    def show_problem(self):
        rad = 1
        n = 3
        caption1 = TextMobject("How about we start with a circle?").scale(1.5).to_edge(UP)
        caption2 = TextMobject("Next, we'll circumscribe a triangle (3 sided polygon)"
                               ).to_edge(UP)
        caption3 = TextMobject("Now we can form a new circle with new radius"
                               ).to_edge(UP)
        caption4 = TextMobject("Next up, we'll circumscribe a 4 sided polygon...", "Or square"
                               ).to_edge(UP)
        caption4[1].set_color('#FFF200')
        caption5 = TextMobject("So what happens as we continue this. ", "Let's take a look!"
                               ).to_edge(UP)
        caption5[1].set_color('#FFF200')
        caption6 = TextMobject("At each step, we'll use a polygon with an additional side"
                               ).to_edge(DOWN)
        circle1 = Circle()
        rad = change_radius(rad, n)
        poly1 = draw_poly(rad, n)
        circle2 = Circle(radius=rad)
        n += 1
        rad = change_radius(rad, n)
        poly2 = draw_poly(rad, n)
        circle3 = Circle(radius=rad)
        self.play(Write(caption1))
        self.play(Write(circle1, run_time=2))
        self.wait()
        self.play(ReplacementTransform(caption1, caption2, run_time=1))
        self.wait()
        self.play(Write(poly1, run_time=3))
        self.play(ReplacementTransform(caption2, caption3, run_time=1))
        self.wait(2)
        self.play(ReplacementTransform(circle1.copy(), circle2, run_time=1))
        self.wait()
        self.play(ReplacementTransform(caption3, caption4[0]))
        self.wait(2)
        self.play(Write(caption4[1], run_time=1))
        self.wait()
        self.play(Write(poly2, run_time=1))
        self.wait()
        self.play(ReplacementTransform(circle2.copy(), circle3, run_time=1))
        self.wait()
        self.play(ReplacementTransform(caption4, caption5[0], run_time=1))
        self.wait()
        self.play(Write(caption5[1], run_time=1))
        self.wait()
        self.play(Write(caption6, run_time=1))
        self.play(Succession(*[FadeOutAndShiftDown(z)
                               for z in [circle1, circle2, circle3, poly1,
                                         poly2, caption5, caption6]],
                             lag_ratio=0.2))
        self.wait()


class CirCir(Scene):
    CONFIG = {
        "initial_rad": 0.5,
        "initial_poly": 3,
        "line_thickness": 1.5,
        "initial_time": 2,
        "amount_polys": 40,
        "polygons": True
    }

    def construct(self):
        self.add(small_logo())
        time = self.initial_time
        rad = self.initial_rad
        n = self.initial_poly
        circles, polygons = draw_system(rad, n, self.amount_polys, self.line_thickness)
        i = 1
        for run in range(0, self.amount_polys):
            # Circles
            self.play(ShowCreation(circles[run], run_time=time))
            # Polygon
            if self.polygons == True:
                self.play(ShowCreation(polygons[run], run_time=time))
            # Timing
            n += 1
            if i % 3 == 0:
                time = time * 0.5
            i += 1

        self.questions(polygons, circles)

    def questions(self, polygons, circles):
        self.wait()
        caption1 = TextMobject("WOAH THERE!").to_corner(UL).set_color('#FFF200')
        caption2 = TextMobject("Let's get a better look"
                               ).scale(0.75).next_to(caption1, DOWN)
        caption3 = TextMobject("How Big are the Circles?"
                               ).shift([0, 0.75, 0])
        caption3b = TextMobject("What can we observe?").to_corner(UR).shift([0.25, 0, 0])
        caption4 = TextMobject("After circumscribing an infinite set of polygons"
                               ).scale(1.25).to_edge(UP)
        caption5 = TextMobject("The circle has a finite radius"
                               ).scale(1.25)
        caption6 = TextMobject("But how big is it?"
                               ).scale(1.25).to_edge(DOWN)
        final_circle = Circle(radius=2)
        self.play(Write(caption1))
        self.play(Write(caption2))
        self.wait(2)
        self.play(*[FadeOutAndShiftDown(z)
                    for z in polygons])
        self.wait()
        self.play(Succession(*[FadeOutAndShiftDown(z)
                               for z in circles[1:len(circles) - 1]], lag_ratio=0.1))
        self.play(ReplacementTransform(caption1.copy(), caption3))
        self.wait()
        self.play(ReplacementTransform(caption3.copy(), caption3b))
        self.wait(2)
        self.play(ReplacementTransform(circles[0], circles[len(circles) - 1]))
        self.play(ShrinkToCenter(circles[len(circles) - 1]),
                  ReplacementTransform(caption1, caption4),
                  FadeOutAndShiftDown(caption2),
                  FadeOutAndShiftDown(caption3),
                  FadeOutAndShiftDown(caption3b))
        self.play(ReplacementTransform(caption4.copy(), caption5))
        self.play(ReplacementTransform(caption5.copy(), caption6))
        self.wait(5)
        self.play(ReplacementTransform(caption5, final_circle))
        self.wait()
        self.play(*[FadeOutAndShiftDown(z)
                    for z in [final_circle, caption4, caption6]])


class Explain(Scene):
    def construct(self):
        self.add(small_logo())
        self.in_other_words()
        self.finite_circle()
        self.circles_look()

    def in_other_words(self):
        text1 = []
        text1.append(TextMobject("In Other Words"
                                 ).set_color('#FFF200').scale(1.5).to_edge(UP))
        text1.append(TextMobject("This process scales our circle by some number..."
                                 ).next_to(text1[0], DOWN))
        text1.append(TextMobject("But Exactly how much?").next_to(text1[1], DOWN))
        circle1 = Circle(radius=0.5).shift([-3, -0.5, 0])
        circle2 = Circle(radius=2).shift([3, -0.5, 0])
        vect = Arrow(np.array([-2, -0.5, 0]), np.array([0.5, -0.5, 0]))
        for i in text1:
            self.play(Write(i))
            self.wait()
        self.play(ShowCreation(circle1))
        self.play(ShowCreation(vect))
        self.play(ReplacementTransform(circle1.copy(), circle2))
        self.play(Succession(*[ShrinkToCenter(z)
                               for z in [text1[0], text1[1], text1[2], circle1, vect, circle2]],
                             lag_ratio=0.1))

    def finite_circle(self):
        r = 1.5
        text1 = []
        text1.append(TextMobject("After adding infinite polygons").scale(1.5).to_edge(UP))
        text1.append(TextMobject("The last circle DOES have a ", "finite", " radius"
                                 ).scale(1.45).next_to(text1[0], DOWN))
        text1.append(TextMobject("But how can we know that?"
                                 ).scale(1.5).next_to(text1[1], DOWN))
        text1.append(TextMobject("Let's take a look!").scale(1.5).next_to(text1[2], DOWN))
        text1.append(TextMobject("We'll start with a circle"
                                 ).scale(2).next_to(text1[3], DOWN, buff=1))
        text1[1][1].set_color('#FFF200')

        text2 = []
        text2.append(TextMobject("First, We'll circumscribe a triangle").to_edge(UP))
        text2.append(TextMobject("But watch what happens as we add sides"
                                 ).to_edge(UP))
        text2.append(TextMobject("The polygon hugs closer and closer to the circle,"
                                 ).to_edge(UP))
        text2.append(TextMobject("adding less and less radius").next_to(text2[2], DOWN))
        text2.append(TextMobject("Remember That!").scale(1.75).to_edge(DOWN))

        # Make List of polygons
        polys = []
        for i in range(3, 16):
            r2 = change_radius(r, i)
            polys.append(draw_poly(r2, i, 4))

        circle = Circle(radius=1.5)

        # introduce circle
        for i in text1:
            self.play(Write(i))
            self.wait()
        self.play(*[*[FadeOutAndShift(z, LEFT)
                      for z in text1[0:len(text1) - 1:2]],
                    *[FadeOutAndShift(z, RIGHT)
                      for z in text1[1:len(text1) - 1:2]]])
        self.play(ReplacementTransform(text1[-1], circle))
        self.play(Write(text2[0]))
        self.wait()
        self.play(ReplacementTransform(text2[0], text2[1]))
        self.wait(2)

        # Hug Initiated
        self.play(ShowCreation(polys[0]))
        self.wait()
        for i in range(0, len(polys) - 1):
            self.play(ReplacementTransform(polys[i], polys[i + 1]))
            self.wait(0.25)

        # What Happened
        self.play(ReplacementTransform(text2[1], text2[2]))
        self.wait()
        self.play(Write(text2[3]))
        self.play(Write(text2[4]))
        self.wait(2)

        # Hide all
        self.play(*[FadeOutAndShiftDown(z)
                    for z in [polys[-1], circle, text2[2], text2[3], text2[4]]])

    def circles_look(self):
        text1 = []
        text1.append(TextMobject("Let's bring back that infinite set of polygons"
                                 ).to_edge(UP))
        text1.append(TextMobject("And from here on out, we'll call it ", "Kyle"
                                 ).next_to(text1[0], DOWN))
        text1[1][1].set_color('#FFF200')
        text1.append(TextMobject("As the polygons hug tighter and tighter,"
                                 ).move_to(text1[0]))
        text1.append(TextMobject("they add less and less radius, limiting Kyle's growth"
                                 ).move_to(text1[1]))
        text1.append(TextMobject("But again, How big can Kyle get?"
                                 ).move_to(text1[0]).scale(1.5).set_color('#FFF200'))
        cirs, polys = draw_system(0.35, 3, 30, 1, -1)

        self.play(Write(text1[0]))
        self.play(Write(text1[1]))
        self.play(*[ShowCreation(z, run_time=2)
                    for z in cirs])
        self.play(*[ShowCreation(z, run_time=5)
                    for z in polys])
        self.play(ReplacementTransform(text1[0], text1[2]),
                  ReplacementTransform(text1[1], text1[3]))
        self.wait(5)
        self.play(ReplacementTransform(text1[2], text1[4]),
                  ReplacementTransform(text1[3], text1[4]))
        self.wait()
        self.play(*[FadeOut(z)
                    for z in polys])

        # Cool circle growth
        time = 1
        for i in range(0, len(cirs) - 1):
            self.play(ReplacementTransform(cirs[i], cirs[i + 1], run_time=time))
            time = time * 0.8
        self.wait()

        # Clear Screen
        self.play(*[FadeOutAndShiftDown(z)
                    for z in [cirs[-1], text1[-1]]])


class TransformCir(Scene):
    def construct(self):
        side = 3
        radius = 3
        temp = draw_poly(radius, side)
        self.play(ShowCreation(temp))
        for n in range(20):
            side += 1
            temp2 = draw_poly(radius, side)
            self.play(ReplacementTransform(temp, temp2))
            temp = temp2
            self.wait(0.5)


class Equation(Scene):
    def construct(self):
        self.add(small_logo())
        self.set_up()


    def set_up(self):
        groups = []
        groups.append(self.make_group(3))
        groups.append(self.make_group(4))
        groups.append(self.make_group(5))
        groups.append(self.make_group(6))
        groups.append(self.make_group(4))

        # Text 1
        text1 = []
        text1.append(TextMobject("First, we need to find the new radius after each added polygon"
                                 ).to_edge(UP, buff=0.21))
        text1.append(TextMobject("Importantly, we must do it in a way that works for"
                                 ).next_to(text1[0], DOWN, buff=0.21))
        text1.append(TextMobject("Any ", "Polygon").next_to(text1[1], DOWN, buff=0.21))
        text1[2][0].set_color('#FFF200')

        # Text 2
        text2 = []
        text2.append(TextMobject("We have an angle, adjacent leg, and hypotenuse"
                                 ).to_edge(UP))
        text2.append(TextMobject("So let's use Cos!").next_to(text2[0], DOWN))
        text2.append(TextMobject("Then solve for ", "$r_{n+1}$"
                                 ).next_to(text2[1], DOWN))

        # Text 3
        text3 = []
        text3.append(TextMobject("Now we're not done yet!").to_edge(UP))
        text3.append(TextMobject("We don't yet know the value of ", "$\\theta$"
                                 ).next_to(text3[0], DOWN))
        text3.append(TextMobject("However, we know it covers half a side length"
                                 ).next_to(text3[1], DOWN))
        text3[1][1].set_color('#3BB143')

        # Text 4
        text4 = []
        text4.append(TextMobject("Thus ", "$\\theta$", " is equal to the full circle (2",
                                 "$\\pi$", ")").to_edge(UP))
        text4.append(TextMobject("divided by the number of sides, then again by 2."
                                 ).next_to(text4[0], DOWN))
        text4.append(TextMobject("Afterwards, we can substitute!").next_to(text4[1], DOWN))
        text4[0][1].set_color('#3BB143')

        text5 = TextMobject("We now have our equation!").scale(2).to_edge(UP)

        equations = []
        equations.append(TexMobject('Cos', '\\left(', '\\theta', '\\right)', '=',
                                    '{', 'r_', '{n}', '\\over', 'r_',
                                    '{n+1}', '}').to_edge(LEFT))
        for i in [6, 9]:
            equations[0][i].set_color('#800000')
        for i in [7, 10]:
            equations[0][i].set_color('#1134A6')
        equations[0][2].set_color('#3BB143')

        equations.append(TexMobject('r_', '{n+1}', '=', '{', 'r_', '{n}', '\\over',
                                    'Cos', '\\left(', '\\theta', '\\right)', '}'
                                    ).to_edge(LEFT))
        for i in [0, 4]:
            equations[1][i].set_color('#800000')
        for i in [1, 5]:
            equations[1][i].set_color('#1134A6')
        equations[1][9].set_color('#3BB143')

        equations.append(TexMobject('\\theta', '=', '{', '2', '\\pi', '\\over', '2',
                                    'n', '}').to_edge(RIGHT))
        equations[2][0].set_color('#3BB143')
        equations[2][7].set_color('#1134A6')

        equations.append((TexMobject('\\theta', '=', '{', '\\pi', '\\over', 'n', '}'
                                     ).to_edge(RIGHT)))
        equations[3][0].set_color('#3BB143')
        equations[3][5].set_color('#1134A6')

        equations.append(TexMobject('r_', '{n+1}', '=', '{', 'r_', '{n}', '\\over',
                                    'Cos', '\\left(', '{', '\\pi', '\\over', 'n', '}',
                                    '\\right)', '}').to_edge(LEFT))
        for i in [0, 4]:
            equations[4][i].set_color('#800000')
        for i in [1, 5, 12]:
            equations[4][i].set_color('#1134A6')

        # Geometry Drawings
        for i in text1:
            self.play(Write(i))
        self.wait(2)
        for i in groups[0]:
            self.play(ShowCreation(i))
        self.wait()
        for i in range(4):
            self.play(*[ReplacementTransform(groups[i][z], groups[i + 1][z])
                        for z in range(len(groups[0]))])
            self.wait()
        for i in range(3):
            self.play(ShrinkToCenter(text1[i]),
                      GrowFromCenter(text2[i]))
        self.wait(1)

        # Equations Drawings
        self.play(ReplacementTransform(groups[4][6].copy(), equations[0][2], run_time=2),
                  ReplacementTransform(groups[4][7][0:2].copy(), equations[0][6:8], run_time=2),
                  ReplacementTransform(groups[4][8][0:2].copy(), equations[0][9:11], run_time=2),
                  *[Write(equations[0][z], run_time=2)
                    for z in [0, 1, 3, 4, 8]])
        self.wait()
        self.play(*[ReplacementTransform(equations[0][i], equations[1][z])
                    for i, z in zip([0, 1, 2, 3, 4, 6, 7, 8, 9, 10],
                                    [7, 8, 9, 10, 2, 4, 5, 6, 0, 1])])
        self.wait()

        # Right Equation
        self.play(*[FadeOutAndShiftDown(text2[z])
                    for z in range(3)],
                  *[FadeInFrom(text3[z], UP)
                    for z in range(3)])
        self.wait(6)
        self.play(*[FadeOutAndShiftDown(text3[z])
                    for z in range(3)],
                  *[FadeInFrom(text4[z], UP)
                    for z in range(3)])
        self.wait(6)
        self.play(ReplacementTransform(groups[-1][6].copy(), equations[2][0], run_time=2),
                  *[Write(equations[2][z], run_time=2)
                    for z in [1, 3, 4, 5, 6, 7]])
        self.wait()
        self.play(*[ReplacementTransform(equations[2][i], equations[3][z])
                    for i, z in zip([0, 1, 4, 5, 7], [0, 1, 3, 4, 5])],
                  *[FadeOutAndShiftDown(equations[2][z])
                    for z in [3, 6]])

        # Final Equation
        self.play(*[ReplacementTransform(equations[1][i], equations[4][z])
                    for i, z in zip([0, 1, 2, 4, 5, 6, 7, 8, 10],
                                    [0, 1, 2, 4, 5, 6, 7, 8, 14])],
                  ReplacementTransform(equations[3][3:6].copy(), equations[4][10:13],
                                       run_time=2),
                  FadeOutAndShiftDown(equations[1][9]))

        self.wait()
        self.play(*[FadeOutAndShiftDown(text4[z])
                    for z in range(len(text4))],
                  FadeIn(text5))
        self.wait()

        # Clear Screen
        self.play(*[FadeOutAndShiftDown(i)
                    for i in [text5, equations[4], equations[3], groups[-1]]])

    def make_group(self, n):

        # Random Stuff:
        # Remember, The group is rotated at the end, and is built accordingly
        square_points = np.array([[0, -2.5, 0], [0.2, -2.5, 0], [0.2, -2.3, 0], [0, -2.3, 0]])
        circle1 = Circle(radius=1.5).shift([0, -1, 0])
        r = 1.5 * (1 / math.cos(PI / n))
        poly = draw_poly(r, n, 3, -1)
        circle2 = Circle(radius=r).shift([0, -1, 0])
        line1 = self.radius([0, -2.5, 0])
        coords = complex(0, -r) * complex(math.cos(PI / n), math.sin(PI / n))
        line2 = self.radius([coords.real, coords.imag - 1, 0])
        right_square = Polygon(*square_points, color='#FFFFFF')

        # Labels!
        theta_arc = Arc(-2 * (PI / 4), (PI / n), arc_center=[0, -1, 0],
                        radius=0.5).set_color('#3BB143')
        theta = TexMobject("\\theta"
                           ).rotate(-1 * PI / 2).shift(1.25 * theta_arc.point_from_proportion(0.75))
        theta.set_color('#3BB143')
        lbl_small = TexMobject("r_", "{n}").rotate(-1 * PI / 2).next_to(line1, LEFT)
        lbl_small[0].set_color('#800000')
        lbl_small[1].set_color('#1134A6')
        lbl_big = TexMobject("r_", "{n+1}"
                             ).rotate(-1 * ((PI / 2) - (PI / n))).move_to(line2).shift([0.25, 0.25, 0])
        lbl_big[0].set_color('#800000')
        lbl_big[1].set_color('#1134A6')

        # Groups
        group = VGroup(circle1, poly, circle2, line1, line2, theta_arc, theta,
                       lbl_small, lbl_big, right_square)
        group.rotate(PI / 2)
        return group

    def radius(self, point):
        return Line([0, -1, 0], point)


class Final_build(Scene):
    def construct(self):
        self.add(small_logo())
        self.into_text()
        self.run_animation()
        self.wrap_it_up()

    def into_text(self):
        text1 = []
        text1.append(TextMobject('We now have an equation to help us out').to_edge(UP))
        text1.append(TextMobject('Each iteration, we plug in the previus radius '
                                 'alongside n (sides)').next_to(text1[0],DOWN))
        text1.append(TextMobject("let's iterate through the equations and watch"
                                 ).next_to(text1[1],DOWN))
        for i in text1:
            self.play(Write(i))
            self.wait()
        self.wait()
        for i in text1:
            self.play(FadeOut(i))


    def run_animation(self):
        # amt=100, rad = 0.48?
        amt = 100
        n = 3
        cirs, polys = draw_system(0.48, 3, amt, 2, 0, -3)
        rn = 1
        rn2 = change_radius(rn, n)
        rn2s = str(rn2)
        equation1 = TexMobject(rn2s[0:4], '={', '1.00', '\\over Cos \\left( {\\pi'
                                                        '\\over', str(n), '} \\right)}'
                               ).to_edge(RIGHT)
        equ_highlight = SurroundingRectangle(equation1, color='#FFF200')
        out_to_in = CurvedArrow(np.array([3.6,0.5,0]),np.array([5.2,0.9,0]),angle=(-PI/1.5))
        text0 = []
        text0.append(TextMobject('We can plug in our new radius and add 1 to n (3)'
                                 ).to_edge(UP))
        text0.append(TextMobject("That'll give us the radius of the next circle"
                                 ).next_to(text0[0],DOWN))
        text0.append(TextMobject('This process can be repeated indefinitely'
                                 ).next_to(text0[1],DOWN))
        time = 1

        self.play(*[Write(equation1[z])
                    for z in [1, 2, 3, 4, 5]])

        self.play(ShowCreation(cirs[0]))
        self.play(ShowCreation(polys[0]))
        self.wait()
        self.play(ShowCreationThenFadeOut(equ_highlight))
        self.play(ReplacementTransform(equation1[2:4].copy(), equation1[0]),
                  ShowCreation(cirs[1]))
        for i in text0:
            self.play(Write(i))
        self.wait(2)
        self.play(ShowCreation(out_to_in),
                  *[FadeOutAndShift(z,UP)
                    for z in text0])
        # Main Show
        for i in range(1, amt - 1):
            n += 1
            rn = rn2
            rns = str(rn)
            rn2 = change_radius(rn2, n)
            rn2s = str(rn2)
            equation2 = TexMobject(rn2s[0:4], '={', rns[0:4], '\\over Cos \\left( {\\pi'
                                                              '\\over', str(n), '} \\right)}'
                                   ).to_edge(RIGHT)
            self.play(ShowCreation(polys[i], run_time=time),
                      ReplacementTransform(equation1[3:6], equation2[3:6], run_time=time))
            self.play(ReplacementTransform(equation1[0], equation2[2], run_time=time),
                      ReplacementTransform(equation1[2], equation2[0], run_time=time),
                      ShowCreation(cirs[i + 1], run_time=time))

            equation1 = equation2
            time = time * 0.7

        # Fade Out
        time = 0.5
        for i in range(0, len(cirs)):
            self.play(FadeOutAndShift(cirs[i], UP, run_time=time),
                      FadeOutAndShift(polys[i], DOWN, run_time=time))
            time = time*0.8
        self.play(*[FadeOut(z)
                    for z in self.mobjects])


    def wrap_it_up(self):
        textf = []
        textf.append(TextMobject("Wrapping it Up", color='#FFF200').scale(2).to_edge(UP))
        textf.append(TextMobject("If we continue to iterate ", "10,000,000", " times,"
                                 ).scale(1.2).next_to(textf[0], DOWN))
        textf.append(TextMobject("the radius becomes 8.700032331930306"
                                 ).scale(1.2).next_to(textf[1], DOWN))
        textf.append(TextMobject("Going further from here only yields minuscule changes."
                                 ).scale(1.15).next_to(textf[2], DOWN))
        textf.append(TextMobject("It clearly converges to  ", "$\\approx 8.7$" ,
                                 " times the original radius."
                                 ).scale(1.2).next_to(textf[3], DOWN))
        textf.append(TextMobject("So there's our answer!"
                                 ).scale(1.2).next_to(textf[4], DOWN))
        textf.append(TextMobject("...Right?").scale(1.75).next_to(textf[5], DOWN, buff=1))

        textf2 = []
        textf2.append(TextMobject("Well, we have an approximate answer.").scale(1.2).next_to(textf[0], DOWN))
        textf2.append(TextMobject("A good one too...but not perfect.").scale(1.2).next_to(textf2[0], DOWN))
        textf2.append(TextMobject("I havn't found an exact solution yet, can you?").scale(1.2).next_to(textf2[1], DOWN))
        textf2.append(TextMobject("Please post any findings in the comments.").scale(1.2).next_to(textf2[2], DOWN))
        textf2.append(TextMobject("Thanks For Watching!", color='#1134A6'
                                  ).scale(2.5).next_to(textf2[3], DOWN, buff=1))

        for i in range(0, len(textf)):
            if i == 6:
                self.wait(1)
            self.play(Write(textf[i]))
            self.wait(0.5)
        self.wait(2)
        self.play(*[FadeOut(z, run_time=1)
                    for z in textf[1:]])
        for i in range(0, len(textf2)):
            if i == 4:
                self.wait()
            self.play(Write(textf2[i]))
            self.wait(0.5)
        self.wait(8)


class thumbnail(Scene):
    def construct(self):
        main_logo = TextMobject("Circumscribed Mania!", color='#A02020'
                                ).scale(2.5).to_edge(UP)
        cirs, polys = draw_system(0.35,3,50,3,-1)
        for i in range(len(cirs)):
            self.add(cirs[i])
            self.add(polys[i])
        self.add(main_logo)



def draw_system(init_rad, init_n, amt, thickness=1, y=0, x=0):
    rad = init_rad
    n = init_n
    circles = []
    polygons = []
    for run in range(amt):
        # Circles
        circle = Circle(radius=rad, stroke_width=thickness).shift([x, y, 0])
        circles.append(circle)
        rad = change_radius(rad, n)
        # Polygon
        polygon = draw_poly(rad, n, thickness, y, x)
        polygons.append(polygon)
        n += 1
    return circles, polygons


def draw_poly(r, n, thickness=1, y=0, x=0):
    point = complex(0, -r)
    on_poly = True
    poly_points = []
    theta = (PI / n)
    rotate_i = complex(math.cos(theta), math.sin(theta))
    for i in range(2 * n):
        point = point * rotate_i
        if on_poly:
            location = np.array([point.real + x, point.imag + y, 0])
            poly_points.append(location)
            on_poly = False
        else:
            on_poly = True

    final_poly = Polygon(*poly_points, stroke_width=thickness)
    return final_poly


def change_radius(radius, n):
    radius = (radius * (1 / (math.cos(PI / n))))
    return radius


def small_logo():
    return TextMobject('Peter Gilliam', color='#666666').scale(0.5).to_edge(DL)
