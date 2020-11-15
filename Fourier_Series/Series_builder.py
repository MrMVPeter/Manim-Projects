from manimlib.imports import *

colors = {
    "s": ORANGE,
    "f": GREEN,
    "theta": RED,
    "p": BLUE
}


class ECircle(Scene):
    # Animate one circle and play with the parameters
    CONFIG = {
        "init_config": {
            "scaler": 1,
            "frequency": 0,
            "phase": 0,
            "center": [0, 0, 0]
        },
        "actual_phase": 0,
        "time_factor": 0.5,
        "master_scale": 2
    }

    def construct(self):
        # Add all trackers
        self.add_values()

        # Draw Axis
        self.draw_axis()

        # Add lables
        self.equations()

        # Create and draw vector and circle
        vect = self.euler_vect()
        circ = self.euler_circ()
        self.play(ShowCreation(vect))
        self.play(ShowCreation(circ))

        # Now that the clock is added, I and activate my updaters
        vect.add_updater(self.update_vect)
        circ.add_updater(self.update_circ)
        self.wait(2)

        # Play with phase
        self.play(self.phase_trac.increment_value, 12,
                  run_time=4)
        self.wait(0.25)
        self.play(self.phase_trac.increment_value, -2,
                  run_time=0.5)
        self.wait(0.25)
        self.play(self.phase_trac.increment_value, -4,
                  run_time=0.5)
        self.wait(0.25)
        self.play(self.phase_trac.increment_value, -6,
                  run_time=0.5)
        self.wait()

        # Play with Scaler
        self.play(self.scaler_trac.increment_value, 2,
                  run_time=3)
        self.wait(0.25)
        self.play(self.scaler_trac.increment_value, -2.5,
                  run_time=1)
        self.wait(0.25)
        self.play(self.scaler_trac.increment_value, 0.5,
                  run_time=1)
        self.wait()

        # Play with Freq
        self.play(self.freq_trac.increment_value, 16,
                  run_time=3)
        self.wait()
        self.play(self.freq_trac.increment_value, -18,
                  run_time=2)
        self.wait()
        self.play(self.freq_trac.increment_value, 6,
                  run_time=3)
        self.wait(5)

        # Shrink before fading
        self.play(self.scaler_trac.increment_value, -1,
                  run_time=3)
        self.wait(3)

    def add_values(self):
        # Create an actual object for each parameter to be referenced and changed
        self.scaler_trac = ValueTracker(self.init_config["scaler"])
        self.freq_trac = ValueTracker(self.init_config["frequency"])
        self.phase_trac = ValueTracker(self.init_config["phase"])
        self.real_p = ValueTracker(self.actual_phase)
        for x in [self.scaler_trac, self.freq_trac, self.phase_trac, self.real_p]:
            self.add(x)

    def euler_vect(self):
        # Initial creation of the vector in the animation
        vector = Vector(RIGHT)
        vector.scaler = self.scaler_trac.get_value() * self.master_scale
        vector.phase = self.phase_trac.get_value()
        vector.scale(vector.scaler)
        vector.rotate(self.phase_trac.get_value(), ORIGIN)
        vector.shift(self.init_config["center"] - vector.get_start())
        return vector

    def euler_circ(self):
        # Initial creation of teh circle in the animation
        circ = Circle(radius=self.scaler_trac.get_value() * self.master_scale,
                      arc_center=self.init_config["center"])
        return circ

    def update_vect(self, vect, dt):
        # Update the vector
        scaler = self.scaler_trac.get_value() * self.master_scale

        vect.set_length(abs(scaler))
        vect.set_angle(self.real_p.get_value() + self.phase_trac.get_value())
        vect.shift(self.init_config["center"] - vect.get_start())
        self.real_p.increment_value(dt * self.freq_trac.get_value())

    def update_circ(self, circ):
        # Simple circle updater
        circ.scale(self.scaler_trac.get_value() * self.master_scale / (circ.get_width() / 2))

    def equations(self):
        # handles all the captions and equations found in the animation
        main_tex = TexMobject('s', 'e', '^{', '\\left(', 'f', '\\theta', '+', 'p', '\\right)', 'i}'
                              ).scale(2).to_corner(UL)
        main_tex[0].set_color(colors['s'])
        main_tex[4].set_color(colors['f'])
        main_tex[5].set_color(colors['theta'])
        main_tex[7].set_color(colors['p'])
        self.play(*[Write(x) for x in main_tex])

        scale_lbl = TexMobject("s", ": ")
        scale_lbl[0].set_color(colors['s'])
        freq_lbl = TexMobject("f", ": ")
        freq_lbl[0].set_color(colors['f'])
        phase_lbl = TexMobject("p", ": ")
        phase_lbl[0].set_color(colors['p'])
        lbls = VGroup(scale_lbl, freq_lbl, phase_lbl).arrange(DOWN).to_corner(UR).shift([-1, 0, 0])
        self.play(*[Write(x) for x in lbls])
        scale_dec = DecimalNumber(self.scaler_trac.get_value(), num_decimal_places=2
                                  ).next_to(scale_lbl, RIGHT
                                            ).add_updater(lambda m: m.set_value(self.scaler_trac.get_value()))
        freq_dec = DecimalNumber(self.freq_trac.get_value(), num_decimal_places=2
                                 ).next_to(freq_lbl, RIGHT
                                           ).add_updater(lambda m: m.set_value(self.freq_trac.get_value()))
        phase_dec = DecimalNumber(self.phase_trac.get_value(), num_decimal_places=2
                                  ).next_to(phase_lbl, RIGHT
                                            ).add_updater(lambda m: m.set_value(self.phase_trac.get_value()))
        self.play(*[Write(x) for x in [scale_dec, freq_dec, phase_dec]])

    def draw_axis(self):
        # pretty self explanitory, draws the axis
        axis_radius = 3
        dash_radius = 0.1
        a_color = "#888888"
        lines = [
            Line([-axis_radius, 0, 0], [axis_radius, 0, 0], stroke_color=a_color, stroke_opacity=0.5),
            Line([0, -axis_radius, 0], [0, axis_radius, 0], stroke_color=a_color, stroke_opacity=0.5)
        ]
        dashes = []
        for x in range(1, axis_radius + 1):
            dashes.append(Line([-x, -dash_radius, 0], [-x, dash_radius, 0], stroke_color=a_color, stroke_opacity=0.5))
            dashes.append(Line([x, -dash_radius, 0], [x, dash_radius, 0], stroke_color=a_color, stroke_opacity=0.5))
            dashes.append(Line([-dash_radius, -x, 0], [dash_radius, -x, 0], stroke_color=a_color, stroke_opacity=0.5))
            dashes.append(Line([-dash_radius, x, 0], [dash_radius, x, 0], stroke_color=a_color, stroke_opacity=0.5))
        for x in [lines, dashes]:
            self.play(*[ShowCreation(i)
                        for i in x],
                      run_time=2)


class Intro(Scene):
    def construct(self):
        text1 = []
        text1.append(TextMobject("Fourier Series", color="#FFF200").scale(1.5).to_edge(UP))
        text1.append(TextMobject("The Fourier Series is an").next_to(text1[0], DOWN, 2))
        text1.append(TextMobject("infinite sum of complex circle functions.").next_to(text1[1], DOWN))
        text1.append(TextMobject("Joseph Fourier found that any path in the").next_to(text1[2], DOWN))
        text1.append(TextMobject("complex plane could be built with these circles.").next_to(text1[3], DOWN))

        text2 = []
        text2.append(TextMobject("For an in-depth explanation on the underlying math,").move_to(text1[1]))
        text2.append(TextMobject("3Blue3Brown has an excellent video on the subject.").move_to(text1[2]))
        text2.append(TextMobject("I will provide a high-level explanation here.").move_to(text1[3]))
        text2.append(TextMobject("First, we'll take a look at any individual circle.").move_to(text1[4]))

        # Write first group of text
        for x in text1:
            self.play(Write(x))
            self.wait(0.3)

        self.wait(3)

        # Replace first group for second group of texts
        for x, y in zip(text1[1:], text2):
            self.play(FadeOutAndShiftDown(x),
                      Write(y))
            self.wait(0.3)
        self.wait(3)


class Series(Scene):
    def construct(self):
        self.wait()

        # gather all texts and texs throught the scene
        texts = self.textmobs()
        texs = self.texmobs()

        self.play(*[Write(x, run_time=2)
                    for x in texs[0][0]])

        # texts 0
        for x in texts[0]:
            self.play(Write(x))
            self.wait(0.25)
        self.wait()

        # texts 0-1
        self.play(*[ReplacementTransform(texs[0][0][x], texs[0][1][y], run_time=2)
                    for x, y in zip([0, 1, 2, 4, 5, 6, 7, 9],
                                    [0, 1, 2, 3, 4, 6, 7, 8])],
                  *[FadeOut(texs[0][0][x], run_time=2)
                    for x in [3, 8]],
                  ReplacementTransform(texs[0][0][9].copy(), texs[0][1][5], run_time=2))
        self.wait()

        # texts 1-2
        self.play(*[ReplacementTransform(texs[0][1][x], texs[0][2][y], run_time=2)
                    for x, y in zip([0, 1, 2, 3, 4, 5, 7, 8],
                                    [0, 1, 2, 7, 8, 4, 3, 9])],
                  *[FadeOut(texs[0][1][x], run_time=2)
                    for x in [6]],
                  *[ReplacementTransform(texs[0][1][x].copy(), texs[0][2][y], run_time=2)
                    for x, y in zip([1, 2],
                                    [5, 6])])
        self.wait()

        # texts 2-3
        self.play(*[ReplacementTransform(texs[0][2][x], texs[0][3][y], run_time=2)
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    [0, 0, 0, 0, 0, 1, 2, 3, 4, 5])])
        self.wait()

        self.play(*[FadeOutAndShiftDown(texts[0][x])
                    for x in range(3)])
        self.play(*[Write(texts[1][x])
                    for x in range(2)])
        self.wait()

        # Tex 2
        self.play(*[ReplacementTransform(texs[0][3][x], texs[1][0][y])
                    for x, y in zip([0, 1, 2, 3, 4, 5],
                                    [0, 2, 3, 4, 5, 6])],
                  ReplacementTransform(texs[0][3][0].copy(), texs[1][0][1]))
        self.wait()

        self.play(*[ReplacementTransform(texs[1][0][x].copy(), y)
                    for x, y in zip([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
                                    [texs[1][1][0], texs[1][2][0],
                                     texs[1][1][1], texs[1][2][1],
                                     texs[1][1][2], texs[1][2][2],
                                     texs[1][1][3], texs[1][2][3],
                                     texs[1][1][4], texs[1][2][4],
                                     texs[1][1][5], texs[1][2][5],
                                     texs[1][1][6], texs[1][2][6]])],
                  *[Write(texs[2][x])
                    for x in [0, 1]])
        self.wait()

        self.play(*[ReplacementTransform(texs[1][0][x].copy(), y)
                    for x, y in zip([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
                                    [texs[1][3][0], texs[1][4][0],
                                     texs[1][3][1], texs[1][4][1],
                                     texs[1][3][2], texs[1][4][2],
                                     texs[1][3][3], texs[1][4][3],
                                     texs[1][3][4], texs[1][4][4],
                                     texs[1][3][5], texs[1][4][5],
                                     texs[1][3][6], texs[1][4][6]])],
                  *[Write(texs[2][x])
                    for x in [2, 3]])
        self.wait()

        self.play(*[Write(texs[2][x])
                    for x in [4, 5, 6, 7]])
        self.wait()

        for x in texts[2]:
            self.play(Write(x))
            self.wait()

        for x in range(2):
            self.play(ReplacementTransform(texts[1][x], texts[3][x]))
            self.wait()

        self.play(*[FadeOut(x)
                    for x in texts[2]],
                  *[Write(x, run_time=3)
                    for x in texs[3][0]])
        self.wait()

        self.play(*[FadeOut(x)
                    for x in texts[3]],
                  Write(texts[4][0]))
        self.wait(4)

    def textmobs(self):
        texts = []

        texts.append([])
        texts[0].append(TextMobject("Upon rearranging, you might find that the").to_edge(UP))
        texts[0].append(TextMobject("phase", " and ", "size", " of each circle can be").next_to(texts[0][0], DOWN))
        texts[0][1][0].set_color(colors['p'])
        texts[0][1][2].set_color(colors['s'])
        texts[0].append(TextMobject("condensed into a single constant.").next_to(texts[0][1], DOWN))

        texts.append([])
        texts[1].append(TextMobject("As for the frequency,").move_to([0, 2.5, 0]))
        texts[1].append(TextMobject("We'll simply add a term for each integer frequency").next_to(texts[1][0], DOWN))

        texts.append([])
        texts[2].append(TextMobject("Now we simply need a list of constants").move_to([0, -1, 0]))
        texts[2].append(TextMobject("to form any path we want.").next_to(texts[2][0], DOWN))
        texts[2].append(TextMobject("Importantly, as we add more constants/circles").next_to(texts[2][1], DOWN))
        texts[2].append(TextMobject("Our path approaches that of our target.").next_to(texts[2][2], DOWN))

        texts.append([])
        texts[3].append(TextMobject("Given a target path in the form of a complex function,").move_to([0, 2.5, 0]))
        texts[3].append(TextMobject("each constant is computed using the following equation."
                                    ).next_to(texts[3][0], DOWN))

        texts.append([])
        texts[4].append(TextMobject("Finally, let's graph out our function!").move_to([0, 2, 0]))

        return texts

    def texmobs(self):
        texs = []

        texs.append([])
        texs[0].append(TexMobject('s', 'e', '^{', '\\left(', 'f', '\\theta', '+', 'p', '\\right)', 'i}').scale(2.5))
        texs[0][0][0].set_color(colors['s'])
        texs[0][0][4].set_color(colors['f'])
        texs[0][0][5].set_color(colors['theta'])
        texs[0][0][7].set_color(colors['p'])
        texs[0].append(TexMobject('s', 'e', '^{', 'f', '\\theta', 'i', '+', 'p', 'i}').scale(2.5))
        texs[0][1][0].set_color(colors['s'])
        texs[0][1][3].set_color(colors['f'])
        texs[0][1][4].set_color(colors['theta'])
        texs[0][1][7].set_color(colors['p'])
        texs[0].append(TexMobject('s', 'e', '^{', 'p', 'i}', 'e', '^{', 'f', '\\theta', 'i}').scale(2.5))
        texs[0][2][0].set_color(colors['s'])
        texs[0][2][3].set_color(colors['p'])
        texs[0][2][7].set_color(colors['f'])
        texs[0][2][8].set_color(colors['theta'])
        texs[0].append(TexMobject('c', 'e', '^{', 'f', '\\theta', 'i}').scale(2.5))
        texs[0][3][0].set_color(colors['s'])
        texs[0][3][3].set_color(colors['f'])
        texs[0][3][4].set_color(colors['theta'])

        texs.append([])

        # Second list for addition signs
        texs.append([])
        texs[1].append(TexMobject('c', '_0', 'e', '^{', '0', '\\theta', 'i}'))
        texs[1][0][0].set_color(colors['s'])
        texs[1][0][1].set_color(colors['s'])
        texs[1][0][5].set_color(colors['theta'])
        for x in [LEFT, RIGHT]:
            texs[2].append(TexMobject("+").next_to(texs[1][0], x))
        texs[1].append(TexMobject('c', '_{-1}', 'e', '^{', '1', '\\theta', 'i}').next_to(texs[2][0], LEFT))
        texs[1][1][0].set_color(colors['s'])
        texs[1][1][1].set_color(colors['s'])
        texs[1][1][5].set_color(colors['theta'])
        texs[1].append(TexMobject('c', '_{1}', 'e', '^{', '-1', '\\theta', 'i}').next_to(texs[2][1], RIGHT))
        texs[1][2][0].set_color(colors['s'])
        texs[1][2][1].set_color(colors['s'])
        texs[1][2][5].set_color(colors['theta'])
        texs[2].append(TexMobject("+").next_to(texs[1][1], LEFT))
        texs[2].append(TexMobject("+").next_to(texs[1][2], RIGHT))
        texs[1].append(TexMobject('c', '_{-2}', 'e', '^{', '2', '\\theta', 'i}').next_to(texs[2][2], LEFT))
        texs[1][3][0].set_color(colors['s'])
        texs[1][3][1].set_color(colors['s'])
        texs[1][3][5].set_color(colors['theta'])
        texs[1].append(TexMobject('c', '_{2}', 'e', '^{', '2', '\\theta', 'i}').next_to(texs[2][3], RIGHT))
        texs[1][4][0].set_color(colors['s'])
        texs[1][4][1].set_color(colors['s'])
        texs[1][4][5].set_color(colors['theta'])
        texs[2].append(TexMobject("+").next_to(texs[1][3], LEFT))
        texs[2].append(TexMobject("+").next_to(texs[1][4], RIGHT))
        texs[2].append(TextMobject("...").next_to(texs[2][4], LEFT))
        texs[2].append(TextMobject("...").next_to(texs[2][5], RIGHT))

        texs.append([])
        texs[3].append(TexMobject('c_n', '=', '{1 \\over 2\\pi} \\int_{0}^{2\\pi}',
                                  'f', '\\left(', '\\theta', '\\right)', 'e', '^{',
                                  '-n', '\\theta', 'i}', 'd', '\\theta').move_to([0, -2, 0]))
        texs[3][0][0].set_color(colors['s'])
        texs[3][0][3].set_color(colors['f'])
        texs[3][0][5].set_color(colors['theta'])
        texs[3][0][9].set_color(colors['s'])
        texs[3][0][10].set_color(colors['theta'])
        texs[3][0][13].set_color(colors['theta'])

        return texs
