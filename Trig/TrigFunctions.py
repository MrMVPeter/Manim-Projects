from manimlib.imports import *


class Functions(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 2 * PI,
        "x_axis_label": "$\\theta$",
        "x_axis_width": 6,
        "x_tick_frequency": PI/2,
        "y_min": -1.0,
        "y_max": 1.0,
        "y_axis_height": 4,
        "graph_origin": np.array([1, 0, 0]),
        "function_color": WHITE,
        "axes_color": BLUE
    }

    def construct(self):
        self.intro()

        small_sine = self.sine_intro([PI / 6, 2 * PI])

        # Draw Graph
        sin_graph, sin_line, sin_lab = self.sin_graph(PI / 6)
        self.play(*[ShowCreation(z)
                    for z in [sin_graph, sin_lab, sin_line]])

        # Draw Together
        self.animate_together([PI / 6, 2 * PI], small_sine, sin_graph, sin_line,
                              [-3, 0], 2)
        self.animate_together([2 * PI, PI / 6], small_sine, sin_graph, sin_line,
                              [-3, 0], 2)

        # Create Cos Graph
        small_cos = self.trig_func([-3,0], 2, PI / 6, 2)
        cos_graph, cos_line, cos_lab = self.cos_graph(PI/6)
        self.play(*[ReplacementTransform(i, z)
                    for i, z in zip([sin_graph, sin_line, sin_lab],
                                 [cos_graph, cos_lab, cos_line])],
                  ReplacementTransform(small_sine, small_cos))

        # Draw Together
        self.animate_together([PI / 6, 2 * PI], small_cos, cos_graph, cos_line,
                              [-3,0], 2, 2)
        self.animate_together([2 * PI, PI / 6], small_cos, cos_graph, cos_line,
                              [-3, 0], 2, 2)

        # Final Animation
        final_trig = self.trig_func([0, 0], 3, PI/6, 3)
        self.play(*[FadeOut(z)
                    for z in self.mobjects])
        self.play(ShowCreation(final_trig[0]),
                  ShowCreation(final_trig[1]))
        self.animate_trig(final_trig, [PI / 6, 13/6 * PI], [0, 0], 3,3,6,False)

        # clear screen
        self.play(*[ShrinkToCenter(z)
                    for z in self.mobjects],
                  ShowCreationThenFadeOut(TextMobject('Bonus', color='#FFF200').scale(6)))

        self.bonus()

    def intro(self):
        texts = []
        texts.append(TextMobject("Peter Gilliam", color='#800000').scale(4).to_edge(UP))
        texts.append(TextMobject("Basic Triginometry in ${ \\pi \\over e}$ minutes"
                                 ).scale(1.75).next_to(texts[0],DOWN, buff=1))
        texts.append(TextMobject("(69 Seconds)"
                                 ).scale(1.75).next_to(texts[1], DOWN, buff=1))
        texts.append(TextMobject("Let's Go!"
                                 ).scale(1.75).next_to(texts[2], DOWN, buff=1))
        for text in texts:
            self.play(Write(text))
        self.wait()
        self.play(*[FadeOutAndShift(z, LEFT)
                    for z in [texts[0], texts[2]]],
                  *[FadeOutAndShift(i, RIGHT)
                    for i in [texts[1], texts[3]]])

    def bonus(self):
        # A static drawing of the trig circle

        angle = PI/3
        sina = math.sin(angle) * 3
        cosa = math.cos(angle) * 3
        tana = math.tan(angle)
        axies = np.array([
            [-1, 0, 0],
            [cosa+(sina*tana)+1, 0, 0],
            [0, -1, 0],
            [0, sina+(cosa/tana)+1, 0]
        ])
        triangle_points = np.array([
            [0, 0, 0],
            [cosa, 0, 0],
            [cosa, sina, 0]
        ])
        tangent_points = np.array([
            [cosa, sina, 0],
            [3/math.cos(angle), 0, 0],
            [0, 3/math.sin(angle), 0]
        ])

        # Radius split
        trans_vect = complex(math.cos(angle), math.sin(angle))
        pre_vect = complex(3*((math.cos(angle))**2), 0)
        final_vect = pre_vect*trans_vect
        final_coor = [final_vect.real, final_vect.imag, 0]

        mobs = []
        # axies
        mobs.append(Line(*axies[[0, 1]]))
        mobs.append(Line(*axies[[2, 3]]))
        # circle
        mobs.append(Arc(0, PI/2, radius=3, color='#800000'))
        # triangle
        mobs.append(Line(*triangle_points[[0, 1]], color='#98FF98'))
        mobs.append(Line(*triangle_points[[1, 2]], color='#FFF200'))
        mobs.append(Line(*triangle_points[[0, 2]], color='#57A0D2'))
        # tangent
        mobs.append(Line(*tangent_points[[1, 2]], color='#95C8D8'))
        # angle
        mobs.append(Arc(0, angle, radius=0.35, stroke_width=5, color='#0018F9'))
        # cos**2
        mobs.append(Line([cosa,0,0], final_coor))


        # Braces
        cos_brace = Brace(Line([0,0,0],[cosa,0,0]), DOWN, buff=0.05)
        cos_tex = TexMobject('Cos').next_to(cos_brace,DOWN, buff=0).scale(0.5)
        cos_tri = VGroup(cos_brace, cos_tex)
        mobs.append(cos_tri)

        # sin
        sine_brace = Brace(Line([3*math.cos(angle), 0, 0],
                                [3*math.cos(angle),3*math.sin(angle),0]), RIGHT, buff=0.05)
        sine_tex = TexMobject('Sin').next_to(sine_brace, RIGHT, buff=0).scale(0.5)
        sin_tri = VGroup(sine_brace, sine_tex)
        mobs.append(sin_tri)

        # tan
        tan_brace = Brace(Line([cosa+(0.5*(sina*tana))-0.5*tana*3, 0.5*sina, 0],
                              [cosa+(0.5*(sina*tana))+0.5*tana*3, 0.5*sina, 0]), UP, buff=0)
        tan_tex = TexMobject('Tan').next_to(tan_brace, UP, buff=0).scale(0.5)
        tan_tri = VGroup(tan_brace, tan_tex).rotate(-(PI/2-angle)).shift([0.2,0,0])
        mobs.append(tan_tri)

        # Cot
        cot_brace = Brace(Line([(0.5 * cosa) - (0.5 * (3 / tana)), sina + 0.5 * (cosa / tana), 0],
                               [(0.5 * cosa) + (0.5 * (3 / tana)), sina + 0.5 * (cosa / tana), 0]),
                          UP, buff=0)
        cot_tex = TexMobject('Cot').next_to(cot_brace, UP, buff=0).scale(0.5)
        cot_group = VGroup(cot_brace, cot_tex).rotate(-(PI/2 - angle)).shift([0.2,0,0])
        mobs.append(cot_group)

        # cos^2
        cos_2_brace = Brace(Line([0,0,0], [3*(math.cos(angle)**2), 0, 0]),UP,buff=0)
        cos_2_tex = TexMobject('Cos^2').next_to(cos_2_brace,UP,buff=0).scale(0.5)
        cos_2_group = VGroup(cos_2_brace, cos_2_tex).rotate_about_origin(angle)
        mobs.append(cos_2_group)

        # sin^2
        sin_2_brace = Brace(Line([3*(math.cos(angle)**2), 0, 0],
                                 [3, 0, 0]), UP, buff=0)
        sin_2_tex = TexMobject('Sin^2').next_to(sin_2_brace,UP,buff=0).scale(0.5)
        sin_2_group = VGroup(sin_2_brace, sin_2_tex).rotate_about_origin(angle)
        mobs.append(sin_2_group)

        # Sec
        sec_brace = Brace(Line([0, 0, 0], [3/math.cos(angle), 0, 0]), DOWN, buff=0.6)
        sec_tex = TexMobject('Sec').next_to(sec_brace, DOWN, buff=0).scale(0.5)
        sec_group = VGroup(sec_brace, sec_tex)
        mobs.append(sec_group)

        # Csc
        csc_brace = Brace(Line([0, 0, 0], [0, 3/math.sin(angle), 0]), LEFT, buff=0.4)
        csc_tex = TexMobject('Csc').next_to(csc_brace, LEFT, buff=0).scale(0.5)
        csc_group = VGroup(csc_brace, csc_tex)
        mobs.append(csc_group)

        group = VGroup(*mobs)
        group.shift([-3,-2,0]).scale(1.25)

        for i in group:
            self.play(ShowCreation(i))
            self.wait(0.25)
        self.play(Write(TextMobject("Thanks For Watching!", color='#1134A6').scale(2).to_corner(UR)))


    def animate_together(self, thetas, mob, graph, graph_line, pos=[-4, 0], rad=2, mode=1):
        if mode == 1:
            func_col = '#FFF200'
        else:
            func_col = '#98FF98'
        mover = VGroup(mob[1], mob[2])
        theta_inters = np.linspace(thetas[0], thetas[1], 100)
        intervals = [[], []]
        for i in theta_inters:
            intervals[0].append(self.get_vertical_line_to_graph(i, graph,
                                                                color=func_col, stroke_width=8))
            intervals[1].append(VGroup(self.trig_triangle(pos, rad, i, mode),
                                       self.theta_group(i, rad, pos)))
        self.play(Succession(*[
            Transform(graph_line, z, rate_func=linear)
            for z in intervals[0]], run_time=3),
                  Succession(*[
                      Transform(mover, x, rate_func=linear)
                      for x in intervals[1]], run_time=3))

    def sin_graph(self, theta):
        self.setup_axes(animate=True)
        func_graph_sin = self.get_graph(sin_of_x, self.function_color)
        sin_lab = self.get_graph_label(func_graph_sin, label="Sin(x)").shift([-1, 1, 0])
        sine_line = self.get_vertical_line_to_graph(theta, func_graph_sin,
                                                    color='#FFF200', stroke_width=8)
        return func_graph_sin, sine_line, sin_lab

    def cos_graph(self, theta):
        self.setup_axes(animate=True)
        func_graph_cos = self.get_graph(cos_of_x, self.function_color)
        cos_lab = self.get_graph_label(func_graph_cos, label="Cos(x)")
        cos_line = self.get_vertical_line_to_graph(theta, func_graph_cos,
                                                   color='#98FF98', stroke_width=8)
        return func_graph_cos, cos_line, cos_lab

    def sine_intro(self, theta):
        # big sine
        sine_circle1 = self.trig_func([0, 0], 3, theta[0])
        self.play(ShowCreation(sine_circle1, run_time=5))

        # animated sine
        self.animate_trig(sine_circle1, theta, [0, 0], 3, 1)
        self.animate_trig(sine_circle1, [theta[1], theta[0]], [0, 0], 3, 1)

        # Smaller sine to the side
        sine_circle2 = self.trig_func([-3, 0], 2, theta[0])
        self.play(ReplacementTransform(sine_circle1, sine_circle2))
        return sine_circle2

    def trig_func(self, pos, rad=3, theta=(PI / 4), mode=1, thta = True):
        mobs = []
        bg = self.draw_background(pos, rad)
        tri = self.trig_triangle(pos, rad, theta, mode)
        theta_g = self.theta_group(theta, rad, pos)
        mobs.append(bg)
        mobs.append(tri)
        if thta:
            mobs.append(theta_g)
        initial = VGroup(*mobs)
        return initial

    def draw_background(self, pos, r):
        # Draws Lines
        vecs = [*[Line(np.array([pos[0], pos[1], 0]), np.array([x + pos[0], z + pos[1], 0]),
                       stroke_width=2)
                  for x, z in zip([-1.25 * r, 0, 1.25 * r, 0], [0, 1.25 * r, 0, -1.25 * r])]]
        cir = Circle(arc_center=[pos[0], pos[1], 0], radius=r, stroke_width=6)
        background = VGroup(*[vecs[x] for x in range(len(vecs))], cir)
        return background

    def trig_triangle(self, pos, r, a, mode):
        tri_points = np.array([
            [pos[0], pos[1], 0],
            [math.cos(a) * r + pos[0], pos[1], 0],
            [math.cos(a) * r + pos[0], math.sin(a) * r + pos[1], 0]
        ])
        Mobs = []
        tri = Polygon(*tri_points, stroke_width=3)
        Mobs.append(tri)
        if math.cos(a) > 0 and (mode == 1 or mode == 3):
            sin_brace = Brace(tri, RIGHT)
            sin_text = TexMobject('Sin\\left(x\\right)').next_to(sin_brace, RIGHT)
            Mobs.append(sin_brace)
            Mobs.append(sin_text)
        elif mode == 1 or mode == 3:
            sin_brace = Brace(tri, LEFT)
            sin_text = TexMobject('Sin\\left(x\\right)').next_to(sin_brace, LEFT)
            Mobs.append(sin_brace)
            Mobs.append(sin_text)
        if mode == 2 or mode == 3:
            cos_brace = Brace(tri, DOWN)
            cos_text = TexMobject('Cos\\left(x\\right)').next_to(cos_brace, DOWN)
            Mobs.append(cos_brace)
            Mobs.append(cos_text)
        if mode == 1 or mode == 3:
            sin_highlight = Line(*tri_points[[1, 2]], color='#FFF200', stroke_width=8)
            Mobs.append(sin_highlight)
        if mode == 2 or mode == 3:
            cos_highlight = Line(*tri_points[[0, 1]], color='#98FF98', stroke_width=8)
            Mobs.append(cos_highlight)

        tri_group = VGroup(*Mobs)

        return tri_group

    def theta_group(self, theta, r, pos):
        theta_arc = Arc(0, theta, arc_center=[pos[0], pos[1], 0],
                        radius=r * 0.2, color='#3BB143', stroke_width=6)
        theta_tex = TexMobject('\\theta', color='#3BB143'
                               ).move_to(np.array([r * 0.4 * math.cos(theta / 2) + pos[0],
                                                   r * 0.4 * math.sin(theta / 2) + pos[1], 0]))

        theta_group = VGroup(theta_arc, theta_tex)
        return theta_group

    def animate_trig(self, mob, theta_range, pos, rad, mode=2, time=4, thta=True):
        mover = VGroup(mob[1], mob[2])
        thetas = np.linspace(theta_range[0], theta_range[1], 100)
        intervals = []
        if thta:
            for theta_temp in thetas:
                intervals.append(VGroup(self.trig_triangle(pos, rad, theta_temp, mode),
                                        self.theta_group(theta_temp, rad, pos)))
        else:
            for theta_temp in thetas:
                intervals.append(VGroup(self.trig_triangle(pos, rad, theta_temp, mode)))
        self.play(Succession(*[
            Transform(mover, interval, rate_func=linear)
            for interval in intervals],
                             run_time=time))


def sin_of_x(x):
    return math.sin(x)


def cos_of_x(x):
    return math.cos(x)

