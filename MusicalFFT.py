from manimlib.imports import *


def make_wave(wave_data, shift_scale=1):
    """
    Creates a wave function which is the combination of multiple sine waves
    :param shift_scale: float from 0 to 1. 0 for centered around axis, 1 for bottom @ axis
    :param wave_data: a list of tuples, example: [(freq1, mag1, phase1), (freq2, mag2, phase2), (...), ...]
    :return: a function of a wave with all of the components given
    """

    def wave(input_num):
        return np.array([
            (math.sin((TAU * wave_part[0] * input_num) + wave_part[2]) * wave_part[1])  # Wave Centered at Zero
            for wave_part in wave_data
        ]).sum() + (shift_scale * (np.array([data[1] for data in wave_data]).sum()))  #

    return wave


def transform_wave(func, limits=(-20, 20), num_in=2000, scaler=1 / 10, low_filter=0.2):
    """
    Creates a function which is the Fourier Transform of the input function
    :param func: Input function to which the Fourier Transform will be applied
    :return: The fourier transform of 'fun
    """

    def freq_domain(f):
        num = num_in
        a = limits[0]
        b = limits[1]
        width = (b - a) / (num - 1)
        if f > low_filter:
            return abs(np.array([
                (func(a + (width * n)) * np.exp(-TAU * f * (a + (width * n)) * 1j) * width)
                for n in range(num)
            ]).sum() * scaler)
        else:
            return 0

    return freq_domain


def add_noise(func, noise_max):
    def resultant_func(num):
        return func(num) + (random.randrange(-100, 100) / (100 / noise_max))

    return resultant_func


class Introduction(Scene):
    CONFIG = {
        "bg_wave_freq": 0.5
    }

    def construct(self):
        self.setup_scene()
        spawner = VMobject().add_updater(self.random_wave_spawner)  # Spawns BG waves
        self.add(spawner)

        # Stroll the word "Hello!" across the screen
        hello_text = TextMobject("HELLO!", color=GREY).scale(4).move_to([-12, 0, 0])
        hello_text.add_updater(lambda obj, dt: obj.shift([dt * 6, 0, 0]))
        self.add(hello_text)
        self.wait(4)
        self.remove(hello_text)  # It should be well off the screen by now

        fourier_title = self.add_title()
        bulb = self.throwout_math()  # The mess of math symbols
        video_description = self.create_description().shift([0, -8, 0])
        self.add(video_description)
        self.wait(7)

        # Shift everything to see video description
        self.play(
            fourier_title.shift, [0, 8, 0],
            bulb.shift, [0, 8, 0],
            video_description.shift, [0, 8, 0]
        )
        self.wait(6)

        # Shift everything back
        self.play(
            fourier_title.shift, [0, -8, 0],
            bulb.shift, [0, -8, 0],
            video_description.shift, [0, -8, 0]
        )
        self.wait(2)

        self.play(
            *[FadeOut(x, run_time=2)
              for x in self.mobjects]
        )

    def throwout_math(self):
        selection = [
            *[
                "\\sum",
                "\\prod",
                "\\int",
                "\\sqrt[n]{abc}",
                "\\pi",
                "\\Gamma",
                "+",
                "-",
                "\\cdot",
                "\\div"
            ]
        ]
        bulb = SVGMobject("BULB").set_opacity(0.5)
        edges = {
            "left": bulb.get_left(),
            "top": bulb.get_top(),
            "right": bulb.get_right(),
            "bottom": bulb.get_bottom()
        }
        obstructing_symbols = []
        for _ in range(20):
            x = (random.random() * (edges['right'][0] - edges['left'][0])) + edges['left'][0]
            y = (random.random() * (edges['top'][1] - edges['bottom'][1])) + edges['bottom'][1]
            obstructing_symbols.append(
                TexMobject(selection[random.randrange(0, len(selection))]) \
                    .move_to([x, y, 0]).scale(3)
            )
        self.play(*[Write(x)
                    for x in obstructing_symbols])
        self.add(bulb)

        for index, mob in enumerate(obstructing_symbols):  # Remove all of the symbols
            if index % 2 == 0:
                shift_amt = 15  # 15 units to the right
            else:
                shift_amt = -15  # 15 units to the left
            self.play(mob.shift, [shift_amt, 0, 0], run_time=0.5)
            self.remove(mob)

        highlight_box = Square(stroke_color=YELLOW, stroke_width=8).scale(1.5)
        self.play(Write(highlight_box))
        self.play(
            highlight_box.scale, 0,
            bulb.set_fill, YELLOW
        )
        self.remove(highlight_box)
        self.wait(4)

        return bulb

    def random_wave_spawner(self, obj):
        if self.frame_count == round(60 / self.bg_wave_freq):
            x = (random.random() * 14.2) - 7.1  # random num from -7.1 to 7.1
            y = (random.random() * 8) - 4  # random num from -4 to 4
            self.make_wave([x, y, 0])
            self.frame_count = 0
        else:
            self.frame_count += 1

    def make_wave(self, wav_loc):
        wave_mob = Circle(
            arc_center=wav_loc,
            stroke_width=8,
            stroke_color=GREY,
            stroke_opacity=0.25,
            radius=0.04
        )
        wave_mob.time_born = self.clock.get_value()
        wave_mob.add_updater(self.update_wave)
        self.add(wave_mob)

    def update_wave(self, obj, dt):
        duration_alive = self.clock.get_value() - obj.time_born
        new_radius = 0.04 + (duration_alive * 4)
        if new_radius > 16.5:  # Remove Wave if its too big to be on screen
            self.remove(obj)
        else:
            updated_wave = Circle(
                arc_center=obj.get_center(),
                stroke_width=8,
                stroke_color=GREY,
                stroke_opacity=0.25,
                radius=new_radius
            )
            updated_wave.time_born = self.clock.get_value()
            obj.become(updated_wave)

    def setup_scene(self):
        self.clock = ValueTracker(0)
        self.add(self.clock)
        self.clock.add_updater(
            lambda obj, dt: obj.increment_value(dt)
        )
        self.frame_count = 0

    def add_title(self):
        title = TextMobject(
            "Fourier Transform", color=GREY
        ).scale(2).to_edge(UP)
        self.play(Write(title))
        return title

    def create_description(self):
        final_group = VGroup()
        line = Line([-7.1, 3.9, 0], [7.1, 3.9, 0])
        title = TextMobject(
            "Video Description",
            color=GREY
        ).scale(3).to_edge(UP)
        d_list = VGroup(
            *[TextMobject(x, color=GREY).scale(2) for x in [
                "Interactive Demonstration",
                "Link to Video Code",
                "Link to additional resources",
                "Music Citations"
            ]]
        ).arrange(DOWN).next_to(title, DOWN, 1)
        final_group.add(
            line,
            title,
            d_list
        )
        return final_group


class RoadMap(Scene):
    def construct(self):
        chapters = VGroup(  # Each mob gets a title and an amount of screen_time
            self.create_chapter_mob("What Is Sound?", 8),
            self.create_chapter_mob("Addition / Convolution", 5),
            self.create_chapter_mob("Fourier Transform", 5),
            self.create_chapter_mob("Intractable Experience", 4)
        )
        self.play(Write(chapters[0]))
        self.wait(chapters[0].screen_time)

        # Slide Chapters along
        for i in range(1, len(chapters)):
            chapters[i].move_to([15, 0, 0])  # Move next chapter_mob off screen
            self.add(chapters[i])  # Spawn chapter_mob
            self.play(
                chapters[i - 1].move_to, [-15, 0, 0],  # Move old Chapter_mob off screen
                chapters[i].move_to, [0, 0, 0]  # Move new chapter mod on screen
            )
            self.remove(chapters[i - 1])  # Remove old chapter
            self.wait(chapters[i].screen_time)

        # Clear Screen
        self.play(
            *[FadeOut(x, run_time=2)
              for x in self.mobjects]
        )

    def create_chapter_mob(self, chapter_name, screen_time):
        title = TextMobject(chapter_name).scale(1.5)
        box = Rectangle(width=14.2 * 2 / 3, height=8 * 2 / 3)
        chapter_mob = VGroup(
            title,
            box
        ).arrange(DOWN)
        chapter_mob.screen_time = screen_time  # How much time each move gets on the screen
        return chapter_mob


class WhatIsSound(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 2 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 13,
        "x_tick_frequency": PI / 2,
        "y_min": -1.0,
        "y_max": 1.0,
        "y_axis_height": 7,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.5, 0, 0]),
        "function_color": WHITE,
        "axes_color": GREY,
        "phase_correction_shift": 5,
    }

    def construct(self):
        # Clock
        self.setup_animation()

        # Show Waves, Frequencies, and Magnitudes
        particals = self.show_particle_sim()

        # Move Particles to Left
        self.play(particals.scale, 0.45,
                  particals.set_x, -3.55)
        self.wait()
        microphone_obj = SVGMobject("microphone.svg"
                                    ).rotate(PI).scale(0.5).next_to(particals, UP)
        self.play(Write(microphone_obj))

        # Split Screen
        divider_line = Line([0, -4, 0], [0, 4, 0], color="#888888")
        self.play(Write(divider_line))

        # Create Bar
        bar_sim_1 = self.show_bar_sim()

        # Play with frequency and magnitude
        self.tune_mags_and_freqs()

        # Get rid of the particle system
        bar_sim_1[2][3].set_value(0)  # Set Spawn == to false
        self.play(
            particals.shift, [-7.2, 0, 0],
            divider_line.shift, [-7.2, 0, 0],
            microphone_obj.shift, [-7.2, 0, 0],
            bar_sim_1[:2].move_to, [-6.5, 0, 0],
            self.sim_mag.set_value, 1
        )
        self.remove(particals, divider_line, microphone_obj)
        self.wait()

        # Demonstrate sine addition
        bar_sim_2, bar_sim_3 = self.sine_addition()

        # Sine Bars
        bar_sim_3[2][3].set_value(0)
        self.play(*[FadeOut(x[:2], run_time=2)
                    for x in [bar_sim_1, bar_sim_2, bar_sim_3]])
        self.wait()

        self.create_sine()  # Demonstrate sine addiction via sampling

        self.summarize_addition()

    def setup_animation(self):
        self.rate = ValueTracker(self.play_speed)
        self.add_clock()
        self.sim_freq = ValueTracker(5)
        self.sim_mag = ValueTracker(0)
        self.global_counter = 0

    def add_clock(self):
        self.clock = ValueTracker(0)
        self.add(self.clock)
        self.clock.add_updater(lambda obj, dt: obj.increment_value(dt * self.rate.get_value()))

    def show_particle_sim(self):
        partical_models = self.create_particles()
        self.play(Write(partical_models))
        self.wait()
        partical_models.add_updater(self.dynamic_move_particles)
        self.play(self.sim_mag.set_value, 0.6, run_time=2)
        self.wait(40)
        return partical_models

    def create_particles(self, dims=(12, 7), nums=(31, 25), freqs=[]):
        width = dims[0]
        height = dims[1]
        num_across = nums[0]
        num_up = nums[1]
        final = VGroup()  # Final Container
        final.freq_data = freqs  # Only used with the static_move_particles updater
        final.add(VGroup())  # The Container for the dots themselves
        for column in range(num_across):
            final[0].add(VGroup())  # The container for one individual column
            for row in range(num_up):
                final[0][column].add(Dot(color=BLUE).move_to([(-width / 2) + (width * column / (num_across - 1)),
                                                              (-height / 2) + (height * row / (num_up - 1)), 0]
                                                             ))

        # Reference Points
        final.add(VGroup())
        final[1].add(Dot().scale(0).move_to(final[0][0]))  # Left
        final[1].add(Dot().scale(0))  # Center
        final[1].add(Dot().scale(0).move_to(final[0][-1]))  # Right

        return final

    def static_move_particles(self, group):
        """
        Moves particles of a VGroup particle system aaccording to a static set
        of frequencies
        """
        freq_data = group.freq_data
        left = group[1][0].get_x()
        width = group[1][2].get_x() - left  # The Difference between the two reference points
        unit_width = width / (len(group[0]) - 1)
        unit_phase = (2 * math.pi) / (len(group[0]) - 1)  # Ensures that the dots are in different stages of oscillation
        for column in range(len(group[0])):
            root_position = left + (column * unit_width)
            scaler = width * self.sim_mag.get_value() * 0.1
            current_shift = 0
            for frequency in freq_data:
                current_shift += math.sin((self.clock.get_value() * frequency) - (column * unit_phase))
            group[0][column].set_x(root_position + (current_shift * scaler))

    def dynamic_move_particles(self, group):
        """
        An updater that moves the particles of a particle system VGroup.
        "dynamic" becasue it uses dynamic value trackers for freq and magnitude
        Allows me to change these parameters and seeing results without replacing this updater.
        """
        left = group[1][0].get_x()
        width = group[1][2].get_x() - left  # The Difference between the two reference points
        unit_width = width / (len(group[0]) - 1)
        unit_phase = (2 * math.pi) / (len(group[0]) - 1)  # Ensures that the dots are in different stages of oscillation
        for column in range(len(group[0])):
            group[0][column].set_x(left + (column * unit_width)  # Root position (Before sine oscillations)
                                   + math.sin(self.clock.get_value() * self.sim_freq.get_value()
                                              - (column * unit_phase))  # Unit Phase
                                   * (width * self.sim_mag.get_value() * 0.1))

    def show_bar_sim(self):
        def slider_func1(x):
            return math.sin((self.sim_freq.get_value() * x) + self.phase_correction_shift) * self.sim_mag.get_value()

        pressure_bar_1 = self.create_slider(4.5, 0.5, slider_func1).shift([1, 0, 0])
        pressure_bar_1[2][3].set_value(0)
        pressure_bar_1[1].set_color(RED)
        self.wait()
        self.play(Write(pressure_bar_1[:2]))
        self.wait()
        pressure_bar_1[2][3].set_value(1)
        self.wait(25)
        return pressure_bar_1

    def create_slider(self, height, width, func):
        final = VGroup()

        # Make Outline
        frame = VGroup()
        frame.add(Line([0, height / 2, 0], [0, -height / 2, 0], color=GREY))
        frame.add(Line([-width / 2, height / 2, 0], [width / 2, height / 2, 0], color=GREY))
        frame.add(Line([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0], color=GREY))
        frame.add(Line([-width / 4, 0, 0], [width / 4, 0, 0], color=GREY))
        final.add(frame)

        # Make Dot
        final.add(Dot().add_updater(lambda obj: obj.move_to([final[0][0].get_x(),  # X-Value
                                                             final[0][0].get_y()  # Y-Base (without-func)
                                                             + func(self.clock.get_value()) * (height / 2),  # (func)
                                                             0])))

        meta_data = VGroup()
        meta_data.add(Dot().scale(0))  # 0
        meta_data.add(ValueTracker(0))  # Left(0) or Right (1)          1
        meta_data.add(ValueTracker(2))  # Frames Between Dots Spawned   2
        meta_data.add(ValueTracker(0))  # Spawn or not?                 3

        final.add(meta_data)

        # Spawner Object
        final.add(Dot().scale(0).add_updater(lambda obj: self.spawn_dot(
            [final[1].get_x(), final[1].get_y(), 0],
            1,  # Direction
            final[2][2].get_value(),  # Rate
            final[2][3].get_value()  # Final boolean, spawn or not?
        )))
        self.add(final[3])

        return final  # [Outlines, Moving Dot, Meta-Data]

    def spawn_dot(self, location, direction, period, spawn):
        if spawn != 0:
            if self.global_counter == period:
                if direction == 0:
                    self.add(Dot().move_to([location[0], location[1], 0]).add_updater(self.move_dot_left))
                else:
                    self.add(Dot().move_to([location[0], location[1], 0]).add_updater(self.move_dot_right))
                self.global_counter = 0
            else:
                self.global_counter += 1

    def move_dot_left(self, obj):
        if obj.get_x() < -15:
            self.remove(obj)
        obj.shift([-0.06, 0, 0])

    def move_dot_right(self, obj):
        if obj.get_x() > 15:
            self.remove(obj)
        obj.shift([0.06, 0, 0])

    def tune_mags_and_freqs(self):
        """
        This is not a very elegant way of tuning the magnitude,
        but it does circumnavigate a bug within manim
        """
        change_log_mag = [  # (steps, change, run_time, end wait)
            (30, -self.sim_mag.get_value() + 0.1, 1, 2),
            (30, 0.5, 1, 1),
        ]
        for log in change_log_mag:
            for _ in range(log[0]):
                self.sim_mag.increment_value(log[1] / log[0])
                self.wait(log[2] / log[0])
            self.wait(log[3])

        # Same bug avoiding maneuver
        change_log_rate = [  # (steps, change, run_time, end wait)
            (10, 0.5, 0.5, 2.5),
            (10, -0.5, 1, 17)
        ]
        for log2 in change_log_rate:
            for _ in range(log2[0]):
                self.rate.increment_value(log2[1] / log2[0])
                self.wait(log2[2] / log2[0])
            self.wait(log2[3])

    def sine_addition(self):
        def slider_func2(x):
            return math.sin((self.sim_freq.get_value() * 2 * x) + self.phase_correction_shift + math.pi)

        def slider_func3(x):
            return (math.sin((self.sim_freq.get_value() * 2 * x) + self.phase_correction_shift + math.pi)
                    + math.sin((self.sim_freq.get_value() * x) + self.phase_correction_shift)) * 0.5

        sine_bar2 = self.create_slider(4.5, 0.5, slider_func2)
        sine_bar3 = self.create_slider(7.5, 0.5, slider_func3)
        sine_bar2[:2].move_to([-5.5, 0, 0])
        sine_bar3[:2].shift([-4.5, 0, 0])
        sine_bar2[1].set_color(BLUE)
        sine_bar3[1].set_color(PURPLE)
        self.play(Write(sine_bar2[:2]))
        self.wait(11)
        self.play(Write(sine_bar3[:2]))
        self.wait()
        self.play(self.rate.set_value, 0, run_time=1)
        for _ in range(2):
            self.play(self.clock.increment_value, 0.5, run_time=1)
            sine_bar3[2][3].set_value(1)
            self.wait(0.5)
            sine_bar3[2][3].set_value(0)
            self.wait()
        sine_bar3[2][3].set_value(1)

        # Resume Animation while keeping the updaters running
        for _ in range(20):
            self.rate.increment_value(0.025)
            self.wait(0.025)
        self.wait(6.5)

        return [sine_bar2, sine_bar3]

    def create_sine(self):
        axes1 = self.setup_axes(True, True)
        num_samples = 200

        sample_x_values = VGroup(
            *[
                Line(
                    self.coords_to_point(((2 * PI) / num_samples) * x, -5),
                    self.coords_to_point(((2 * PI) / num_samples) * x, 5),
                    stroke_width=2,
                    stroke_opacity=0.5,
                    color=GREY
                ) for x in range(0, num_samples)
            ]
        )
        mover_x_value = Line(
            self.coords_to_point(0, -5),
            self.coords_to_point(0, 5),
            stroke_width=3,
            stroke_opacity=0.7,
            color=WHITE
        )

        # First Sine Wave
        def sine1_func(x):
            return 0.2 * math.sin(x * 12)

        sine1_obj = self.get_graph(sine1_func, color=BLUE)
        sine1_sample = VGroup(
            *[Dot(  # Generate 200 Samples of sine1
                self.coords_to_point(((2 * PI) / num_samples) * x, sine1_func(((2 * PI) / num_samples) * x)),
                color=BLUE
            ).scale(0.5) for x in range(0, num_samples)]
        )

        # Second Sine Wave
        def sine2_func(x):
            return math.sin(2 * x) * 0.8

        sine2_obj = self.get_graph(sine2_func, color=RED)
        sine2_sample = VGroup(
            *[Dot(  # Generate 200 Samples of sine2
                self.coords_to_point(((2 * PI) / num_samples) * x, sine2_func(((2 * PI) / num_samples) * x)),
                color=RED
            ).scale(0.5) for x in range(0, num_samples)]
        )

        def sine3_func(x):
            return sine1_func(x) + sine2_func(x)

        sine3_obj = self.get_graph(sine3_func,
                                   color=PURPLE, stroke_width=10)
        sine3_sample = VGroup(
            *[Dot(  # Generate 200 Samples of sine3
                self.coords_to_point(((2 * PI) / num_samples) * x, sine3_func(((2 * PI) / num_samples) * x)),
                color=PURPLE
            ).scale(0.5) for x in range(0, num_samples)]
        )

        self.play(Write(sine1_obj, run_time=0.5))
        self.play(Write(sine2_obj, run_time=0.5))

        self.play(Write(sample_x_values, run_time=0.5))  # Vertical lines that represent x samples

        # Sample sine1
        self.play(FadeOut(sine1_obj),
                  Write(sine1_sample, run_time=1))

        # Sample sine2
        self.play(FadeOut(sine2_obj),
                  Write(sine2_sample, run_time=1))

        self.play(Write(mover_x_value, run_time=0.5))

        # Add Samples
        time_map = [(2 * (0.5 ** (0.5 * x))) for x in range(1, 201)]  # Arbitrary Function that depicts speed
        time_itter = 0
        for sam1, sam2, sam3 in zip(sine1_sample, sine2_sample, sine3_sample):
            self.play(mover_x_value.move_to, [sam1.get_x(), 0, 0], run_time=time_map[time_itter])
            self.play(
                ReplacementTransform(sam1, sam3, run_time=time_map[time_itter]),
                ReplacementTransform(sam2, sam3, run_time=time_map[time_itter])
            )
            time_itter += 1
        self.wait()

        # Fade Out Everything...well, the four things that are visible
        self.play(*[
            FadeOut(x, run_time=0.5)
            for x in [
                sample_x_values,
                mover_x_value,
                sine3_sample,
                axes1
            ]
        ])

    def summarize_addition(self):
        freq1 = 1
        freq2 = 2

        self.rate.set_value(2)  # Speed up scene speed, for visual effect only
        # Create the particle systems
        part1 = self.create_particles([3.55, 3], [15, 11], [freq1])
        part2 = self.create_particles([3.55, 3], [15, 11], [freq2])
        part2[0].set_color(RED)
        part3 = self.create_particles([3.55, 3], [15, 11], [freq1, freq2])
        part3[0].set_color(PURPLE)
        part1.move_to([-4.733, 1.25, 0])
        part2.move_to([0, 1.25, 0])
        part3.move_to([4.733, 1.25, 0])
        part1.add_updater(self.static_move_particles)
        part2.add_updater(self.static_move_particles)
        part3.add_updater(self.static_move_particles)

        # Create the bar representations
        bar1 = self.create_slider(2, 0.5, lambda x: math.sin(x * freq1))
        bar1[:2].move_to([-5.733, -2.2, 0])
        bar1[1].set_color(BLUE)
        bar2 = self.create_slider(2, 0.5, lambda x: math.sin(x * freq2))
        bar2[:2].move_to([-1, -2.2, 0])
        bar2[1].set_color(RED)
        bar3 = self.create_slider(3.5, 0.5,
                                  lambda x: 0.5 * (math.sin(x * freq1) + math.sin(x * freq2)))
        bar3[:2].move_to([3.733, -2.2, 0])
        bar3[1].set_color(PURPLE)

        # Create a small graph for each function
        graph1 = ParametricFunction(lambda t:
                                    np.array((
                                        t,
                                        math.sin(PI * t * freq1),
                                        0
                                    )),
                                    t_min=-1,
                                    t_max=1,
                                    color=BLUE).next_to(bar1[0], RIGHT)
        graph2 = ParametricFunction(lambda t:
                                    np.array((
                                        t,
                                        math.sin(PI * t * freq2),
                                        0
                                    )),
                                    t_min=-1,
                                    t_max=1,
                                    color=RED).next_to(bar2[0], RIGHT)
        graph3 = ParametricFunction(lambda t:
                                    np.array((
                                        t,
                                        math.sin(PI * t * freq1) + math.sin(PI * t * freq2),
                                        0
                                    )),
                                    t_min=-1,
                                    t_max=1,
                                    color=PURPLE).next_to(bar3[0], RIGHT)

        # The labels and table lines
        labels = VGroup(
            TextMobject("A").scale(2).move_to([-4.733, 3.5, 0]),
            TextMobject("B").scale(2).move_to([0, 3.5, 0]),
            TextMobject("A + B").scale(2).move_to([4.733, 3.5, 0]),
            Line([-2.366, 4, 0], [-2.366, -4, 0]),
            Line([2.366, 4, 0], [2.366, -4, 0])
        )
        labels.add(Line([-7.1, labels[0].get_bottom()[1] - 0.1, 0],
                        [7.1, labels[2].get_bottom()[1] - 0.1, 0]))

        self.sim_mag.set_value(0.5)  # Set a magnitude for the smaller particle systems
        self.play(Write(labels))  # Write the labels to the scene
        for particles in [part1, part2, part3]:  # Write each of the particles systems one by one
            self.play(Write(particles))
        self.wait()

        for bar in [bar1, bar2, bar3]:  # Write each of the bars
            self.play(Write(bar[:2]))

        for graph in [graph1, graph2, graph3]:  # Lastly, write each of the graphs
            self.play(Write(graph))

        self.wait(14)

        self.play(*[FadeOut(x, run_time=2)
                    for x in self.mobjects])
        self.rate.set_value(1)  # Set speed back to normal


class AddTwoGraphs(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 2 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 6.5,
        "x_tick_frequency": PI / 2,
        "y_min": -1.0,
        "y_max": 1.0,
        "y_axis_height": 2.533,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.8, 2.666, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        # Define my functions to add
        def waveA(x):
            return math.sin(2 * x)

        def waveB(x):
            return math.sin(4 * x)

        def waveC(x):
            return waveA(x) + waveB(x)

        # Upper Left
        self.setup_axes(animate=False)
        graph_left = self.get_graph(waveA, color=BLUE)
        f1 = TextMobject("Wave A", color=BLUE)
        f1.scale(0.8)
        label_coord1 = self.coords_to_point(PI * 0.75, 0)
        f1.next_to(label_coord1, UP)

        # Upper Right
        self.graph_origin = np.array((0.3, 2.666, 0))
        self.setup_axes(animate=False)
        graph_right = self.get_graph(waveB, color=RED)
        f2 = TextMobject("Wave B", color=RED)
        f2.scale(0.7)
        label_coord2 = self.coords_to_point(7 * PI / 8, 0)
        f2.next_to(label_coord2, UP, buff=1)

        # Lower
        self.graph_origin = np.array((-6.8, -1.333, 0))
        self.x_axis_width = 13
        self.y_min = -2
        self.y_max = 2
        self.y_axis_height = 5.066

        self.setup_axes(animate=False)
        graph_comp = VGroup(self.get_graph(waveA, color=BLUE, opactiy=0.1),
                            self.get_graph(waveB, color=RED, opactiy=0.1))
        graph_UL = self.get_graph(waveC, color=PURPLE)
        f3 = TexMobject("A + B", color=PURPLE)
        f3.scale(1)
        label_coord3 = self.coords_to_point(7 * PI / 8, 0)
        f3.next_to(label_coord3, UP, buff=1)

        graphs = VGroup(graph_left, graph_right, graph_UL)
        labels = VGroup(f1, f2, f3)

        self.wait(5)
        for x in range(2):
            self.play(
                Write(graphs[x]),
                Write(labels[x]),
                run_time=2,
            )
        self.play(ReplacementTransform(graphs[0].copy(), graph_comp[0]))
        self.play(ReplacementTransform(graphs[1].copy(), graph_comp[1]))
        self.play(ReplacementTransform(graph_comp, graphs[2], run_time=2))
        self.play(Write(f3))
        self.wait(3)
        self.play(*[FadeOut(x)
                    for x in self.mobjects])


class AddThreeGraphs(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 2 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 4.4666,
        "x_tick_frequency": PI / 2,
        "y_min": -1.0,
        "y_max": 1.0,
        "y_axis_height": 2.533,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.9, 2.666, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        # Define my functions to add
        def waveA(x):
            return math.sin(1 * x)

        def waveB(x):
            return math.sin(3 * x)

        def waveC(x):
            return math.sin(6 * x)

        def waveD(x):
            return waveA(x) + waveB(x) + waveC(x)

        # Upper Left
        self.setup_axes(animate=False)
        graph_left = self.get_graph(waveA, color=BLUE)
        f1 = TextMobject("Wave A", color=BLUE)
        f1.scale(0.8)
        label_coord1 = self.coords_to_point(PI * 0.75, 0)
        f1.next_to(label_coord1, UP)

        # Upper Middle
        self.graph_origin = np.array((-2.2333, 2.666, 0))
        self.setup_axes(animate=False)
        graph_up = self.get_graph(waveB, color=RED)
        f2 = TextMobject("Wave B", color=RED)
        f2.scale(0.7)
        label_coord2 = self.coords_to_point(7 * PI / 8, 0)
        f2.next_to(label_coord2, UP, buff=1)

        # Upper Right
        self.graph_origin = np.array((2.4333, 2.666, 0))
        self.setup_axes(animate=False)
        graph_right = self.get_graph(waveC, color=GREEN)
        f3 = TextMobject("Wave B", color=GREEN)
        f3.scale(0.7)
        label_coord3 = self.coords_to_point(7 * PI / 8, 0)
        f3.next_to(label_coord3, UP, buff=1)

        # Lower
        self.graph_origin = np.array((-6.9, -1.333, 0))
        self.x_axis_width = 14
        self.y_min = -3
        self.y_max = 3
        self.y_axis_height = 5.066

        self.setup_axes(animate=False)
        # Three Graphs
        graph_comp = VGroup(
            self.get_graph(waveA, color=BLUE),
            self.get_graph(waveB, color=RED),
            self.get_graph(waveC, color=GREEN
                           ))
        graph_down = self.get_graph(waveD, color=PURPLE)  # Sum Graph
        f4 = TexMobject("A + B + C", color=PURPLE)
        f4.scale(1)
        f4.next_to(self.coords_to_point(PI * (9 / 8), 0), UP, buff=1)

        self.wait(16)  # Wait before starting

        # Microphone
        microphone = SVGMobject("microphone").scale(0.5).move_to(self.coords_to_point(0, 3))

        # Sum wave Samples
        final_dots = VGroup(
            *[Dot(color=PURPLE).scale(1 / 2).move_to(
                self.coords_to_point(2 * PI * x / 100, waveD(2 * PI * x / 100))
            ) for x in range(101)]
        )
        moving_dot = Dot(color=PURPLE,
                         fill_opacity=0,
                         stroke_opacity=0
                         ).add_updater(lambda obj: obj.move_to(microphone))
        self.play(Write(microphone))
        self.add(moving_dot)
        for i in range(101):
            self.play(
                ReplacementTransform(
                    moving_dot.copy(), final_dots[i], run_time=0.05, rate_func=linear
                ),
                microphone.set_x, final_dots[i].get_x(), run_time=0.05, rate_func=linear
            )
        self.wait()

        # graphs = VGroup(graph_left, graph_up, graph_right, graph_down)
        mover_graph = graph_down.copy()
        labels = VGroup(f1, f2, f3, f4)
        self.play(
            FadeOut(final_dots),
            FadeOut(microphone),
            Write(mover_graph, run_time=2
                  ))
        self.play(Write(f4))
        self.wait(5)

        # Seperate Wave
        # Remaining Wave forms after each consecutive removal
        remaining_graphs = VGroup(self.get_graph(lambda x: waveA(x) + waveB(x), color=PURPLE),
                                  self.get_graph(waveA, color=PURPLE))

        # First Separation
        self.play(
            FadeOut(labels[3]),
            Transform(mover_graph, remaining_graphs[0]),
            ReplacementTransform(mover_graph.copy(), graph_right
                                 ))

        # Second Separation
        self.play(Transform(mover_graph, remaining_graphs[1]),
                  ReplacementTransform(mover_graph.copy(), graph_up))

        # Third Separation
        self.play(ReplacementTransform(mover_graph, graph_left))
        self.wait(3)

        # Move all the waves back to the bottom to recombine.
        self.play(
            ReplacementTransform(graph_left.copy(), graph_comp[0]),
            ReplacementTransform(graph_up.copy(), graph_comp[1]),
            ReplacementTransform(graph_right.copy(), graph_comp[2])
        )

        # Recombine all of the parts
        self.play(
            ReplacementTransform(graph_comp[0], graph_down),
            ReplacementTransform(graph_comp[1], graph_down),
            ReplacementTransform(graph_comp[2], graph_down)
        )

        self.wait(4)
        self.play(*[FadeOut(x)
                    for x in self.mobjects])


class AddNWaves(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 2 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 13,
        "x_tick_frequency": PI / 2,
        "y_min": -5.0,
        "y_max": 5.0,
        "y_axis_height": 7.6,
        "y_tick_frequency": 1,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.5, 0, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        num_waves = 7
        wave_components = []
        for _ in range(num_waves):
            freq = random.randrange(1, 1000) / 100
            mag = 1
            phase = random.randrange(0, 628) / 100
            wave_components.append(
                (freq, mag, phase)
            )
        self.setup_axes()

        mover_graph = self.get_graph(make_wave([wave_components[0]], 0),
                                     step_size=0.0005,
                                     color=BLUE)
        self.play(Write(mover_graph))
        self.wait(2)
        for i in range(1, len(wave_components)):
            component = self.get_graph(make_wave([wave_components[i]], 0),
                                       step_size=0.0005,
                                       color=RED)
            new_some = self.get_graph(make_wave(wave_components[:i + 1], 0),
                                      step_size=0.0005,
                                      color=BLUE)
            self.play(Write(component))
            self.play(
                Transform(
                    component, new_some
                ),
                Transform(
                    mover_graph, new_some
                )
            )
            self.remove(component)
            self.wait()
        self.wait(2)
        self.play(
            FadeOut(mover_graph, run_time=2)
        )
        self.wait()


class BuildSounds(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 5 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 13,
        "x_tick_frequency": PI / 2,
        "y_min": -3.0,
        "y_max": 3.0,
        "y_axis_height": 7,
        "y_tick_frequency": 1,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.5, 0, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        self.setup_axes(True)
        self.setup_freq_attributes()

        waveA = self.get_graph(
            lambda x: math.sin(self.waveA_freq.get_value() / 100 * x),
            color=RED,
            stroke_opacity=0.25,
        ).add_updater(self.update_wave_A)

        waveB = self.get_graph(
            lambda x: math.sin(self.waveB_freq.get_value() / 100 * x),
            color=BLUE,
            stroke_opacity=0.25
        ).add_updater(self.update_wave_B)

        waveC = self.get_graph(
            lambda x: math.sin(self.waveC_freq.get_value() / 100 * x),
            color=GREEN,
            stroke_opacity=0.25
        ).add_updater(self.update_wave_C)

        waveD = self.get_graph(
            lambda x: (
                    math.sin(self.waveA_freq.get_value() / 100 * x)
                    + math.sin(self.waveB_freq.get_value() / 100 * x)
                    + math.sin(self.waveC_freq.get_value() / 100 * x)
            ),
            color=PURPLE,
            stroke_width=6
        ).add_updater(self.update_wave_D)

        label_box = self.create_label_box()  # Show Exact Frequencies
        simplified_ratios_box = self.ratio_box()  # Show Simplified Freq Ratios

        self.play(
            Write(waveA),
            Write(waveB),
            Write(waveC)
        )
        self.wait()

        # Setup Dissonant Wave
        self.play(self.waveA_freq.set_value, 391.995)
        self.play(self.waveB_freq.set_value, 554.365)
        self.play(self.waveC_freq.set_value, 739.989)
        self.wait()

        self.play(Write(waveD))
        self.wait(2)

        label_box.add_updater(self.update_labels)
        self.play(Write(label_box))

        # Setup Dissonant wave 440, 466.1638, 493.883
        self.set_freqs_values(440, 466.1638, 493.883)
        self.wait(5)

        # Setup Dissonant wave 311, 392, 554
        self.set_freqs_values(311, 392, 554)
        self.wait(5)

        # Setup Dissonant wave 392, 415, 494
        self.set_freqs_values(392, 415, 494)
        self.wait(5)

        # Setup E-Major
        self.set_freqs_values(554.365, 698.456, 830.609)
        self.play(Write(simplified_ratios_box))  # Show the Simplified Ratio between frequencies
        self.wait(2)

        # Setup E-Minor
        self.set_freqs_values(554.365, 659.255, 830.609)
        self.set_ratios(simplified_ratios_box, 10, 12, 15)
        self.wait(2)

        # Setup C#-Major
        self.set_freqs_values(466.164, 587.330, 698.456)
        self.set_ratios(simplified_ratios_box, 4, 5, 6)
        self.wait(2)

        # Setup E-Augmented
        self.set_freqs_values(329.628, 415.305, 523.251)
        self.set_ratios(simplified_ratios_box, 16, 20, 25)
        self.wait(2)

    def update_wave_A(self, obj):
        obj.become(
            self.get_graph(
                lambda x: math.sin(self.waveA_freq.get_value() / 100 * x),
                color=RED,
                stroke_opacity=0.25
            )
        )

    def update_wave_B(self, obj):
        obj.become(
            self.get_graph(
                lambda x: math.sin(self.waveB_freq.get_value() / 100 * x),
                color=BLUE,
                stroke_opacity=0.25
            )
        )

    def update_wave_C(self, obj):
        obj.become(
            self.get_graph(
                lambda x: math.sin(self.waveC_freq.get_value() / 100 * x),
                color=GREEN,
                stroke_opacity=0.25
            )
        )

    def update_wave_D(self, obj):
        obj.become(
            self.get_graph(
                lambda x: (
                        math.sin(self.waveA_freq.get_value() / 100 * x)
                        + math.sin(self.waveB_freq.get_value() / 100 * x)
                        + math.sin(self.waveC_freq.get_value() / 100 * x)
                ),
                color=PURPLE,
                stroke_width=6
            )
        )

    def set_freqs_values(self, freqA, freqB, freqC):
        self.play(
            self.waveA_freq.set_value, freqA,
            self.waveB_freq.set_value, freqB,
            self.waveC_freq.set_value, freqC
        )

    def create_label_box(self):
        location = [4, 3, 0]
        final = VGroup()
        rect = Rectangle(
            width=5.75,
            height=1.5,
            fill_color=GREY,
            fill_opacity=0.5,
            stroke_opacity=0
        ).move_to(location)
        colums = VGroup(
            VGroup(
                TextMobject("Wave 1", color=RED),
                DecimalNumber(220, num_decimal_places=0, color=RED)
            ).arrange(DOWN),
            VGroup(
                TextMobject("Wave 2", color=BLUE),
                DecimalNumber(440, num_decimal_places=0, color=BLUE)
            ).arrange(DOWN),
            VGroup(
                TextMobject("Wave 3", color=GREEN),
                DecimalNumber(550, num_decimal_places=0, color=GREEN)
            ).arrange(DOWN)
        ).arrange(RIGHT).move_to(location)
        final.add(rect)
        final.add(colums)
        return final

    def update_labels(self, obj):
        decimal_a = obj[1][0][1]
        decimal_b = obj[1][1][1]
        decimal_c = obj[1][2][1]

        decimal_a.set_value(self.waveA_freq.get_value())
        decimal_b.set_value(self.waveB_freq.get_value())
        decimal_c.set_value(self.waveC_freq.get_value())

    def ratio_box(self):
        location = self.coords_to_point(2.5 * PI, -2)
        final = VGroup()
        rect = Rectangle(
            width=6.75,
            height=1.25,
            fill_color=GREY,
            fill_opacity=0.5,
            stroke_opacity=0
        ).move_to(location)
        ratio_text = VGroup(
            DecimalNumber(4, num_decimal_places=0, color=RED),
            TextMobject(" : "),
            DecimalNumber(5, num_decimal_places=0, color=BLUE),
            TextMobject(" : "),
            DecimalNumber(6, num_decimal_places=0, color=GREEN)
        ).scale(2).arrange(RIGHT, buff=0.5).move_to(location)
        final.add(rect)
        final.add(ratio_text)
        return final

    def set_ratios(self, label_obj, num1, num2, num3):
        # self.play(
        #     ReplacementTransform(
        #         label_obj[1][0],
        #         DecimalNumber(num1, num_decimal_places=0, color=RED
        #                       ).scale(2).move_to(label_obj[1][0].get_center()
        #                                          )
        #     ),
        #     ReplacementTransform(
        #         label_obj[1][2],
        #         DecimalNumber(num2, num_decimal_places=0, color=BLUE
        #                       ).scale(2).move_to(label_obj[1][2].get_center()
        #                                          )
        #     ),
        #     ReplacementTransform(
        #         label_obj[1][4],
        #         DecimalNumber(num3, num_decimal_places=0, color=GREEN
        #                       ).scale(2).move_to(label_obj[1][4].get_center()
        #                                          )
        #     )
        # )

        label_obj[1][0].become(DecimalNumber(num1, num_decimal_places=0, color=RED
                                             ).scale(2).move_to(label_obj[1][0].get_center()
                                                                ))

        label_obj[1][2].become(DecimalNumber(num2, num_decimal_places=0, color=BLUE
                                             ).scale(2).move_to(label_obj[1][2].get_center()
                                                                ))

        label_obj[1][4].become(DecimalNumber(num3, num_decimal_places=0, color=GREEN
                                             ).scale(2).move_to(label_obj[1][4].get_center()
                                                                ))

    def setup_freq_attributes(self):
        self.waveA_freq = ValueTracker(0)
        self.waveB_freq = ValueTracker(0)
        self.waveC_freq = ValueTracker(0)


class MusicalIntervals(Scene):
    def construct(self):
        # All the x inputs
        left_colum = VGroup(
            *[TextMobject(x)
              for x in [
                  "x",
                  *[str(x) for x in range(13)]
              ]
              ]
        )
        for i in left_colum[1:]:
            i.align_to(left_colum[0], LEFT)

        # Exact value
        middle_colum = VGroup(
            TexMobject("2^{x \\over 12}"),
            *[DecimalNumber(2 ** (x / 12), num_decimal_places=2)
              for x in range(13)]
        )
        middle_colum[0].next_to(left_colum[0], RIGHT, 0.5)
        for i in middle_colum[1:]:
            i.align_to(middle_colum[0], LEFT)

        # Approximate Fraction
        fraction_colum = VGroup(
            TextMobject("Fraction"),
            *[TexMobject(x).scale(0.9)
              for x in [
                  "=1",
                  "\\approx{16/15}",
                  "\\approx{9/8}",
                  "\\approx{6/5}",
                  "\\approx{5/4}",
                  "\\approx{4/3}",
                  "\\approx{7/5}",
                  "\\approx{3/2}",
                  "\\approx{8/5}",
                  "\\approx{5/3}",
                  "\\approx{7/4}",
                  "\\approx{15/8}",
                  "=2"
              ]]
        )
        fraction_colum[0].next_to(middle_colum[0], RIGHT, 0.5)
        for i in fraction_colum:
            i.align_to(fraction_colum[0], LEFT)

        # Interval Name
        name_colum = VGroup(
            *[TextMobject(x)
              for x in [
                  "Interval Name",
                  "Root",
                  "Minor Second (m2)",
                  "Major Second (M2)",
                  "Minor Third (m3)",
                  "Major Third (M2)",
                  "Perfect Fourth (P4)",
                  "Tritone (A4/D5)",
                  "Perfect Fifth (P5)",
                  "Minor Sixth (m6)",
                  "Major Sixth (M6)",
                  "Minor Seventh (m7)",
                  "Majro Seventh (M7)",
                  "Octave"
              ]]
        )
        name_colum[0].next_to(fraction_colum[0], RIGHT, 0.5)
        for i in name_colum:
            i.align_to(name_colum[0], LEFT)

        horizontal_lines = VGroup(
            *[Line(left_colum.get_left(), [name_colum.get_right()[0] + 0.5, 0, 0],
                   stroke_opacity=0.5)
              for _ in range(14)]
        ).arrange(DOWN, buff=8 / 15).align_to(left_colum, LEFT).shift([-0.2, 0, 0])

        vertical_lines = VGroup(
            *[Line([x.get_left()[0] - 0.2, horizontal_lines[0].get_y(), 0],
                   [x.get_left()[0] - 0.2, horizontal_lines[-1].get_y(), 0],
                   stroke_opacity=0.5)
              for x in [left_colum, middle_colum, fraction_colum, name_colum]],
            Line(horizontal_lines[0].get_right(), horizontal_lines[-1].get_right(),
                 stroke_opacity=0.5)
        )

        for x in range(14):
            left_colum[x].align_to(horizontal_lines[x], DOWN).shift([0, 0.1, 0])
            middle_colum[x].align_to(horizontal_lines[x], DOWN).shift([0, 0.1, 0])
            fraction_colum[x].align_to(horizontal_lines[x], DOWN).shift([0, 0.05, 0])
            name_colum[x].align_to(horizontal_lines[x], DOWN).shift([0, 0, 0])

        # Small Adjustments
        fraction_colum[1].shift([0, 0.1, 0])
        fraction_colum[-1].shift([0, 0.1, 0])
        name_colum[0].shift([0, 0.1, 0])
        name_colum[1].shift([0, 0.1, 0])
        name_colum[-1].shift([0, 0.1, 0])

        table_group = VGroup(
            left_colum,
            middle_colum,
            fraction_colum,
            horizontal_lines,
            vertical_lines,
            name_colum
        ).move_to([0, 0, 0])
        self.play(Write(table_group))
        self.play(table_group.shift, [-2, 0, 0])

        # Walk though each interval
        interval_groups = VGroup(
            *[
                VGroup(
                    self.interval_box(horizontal_lines, 0),
                    self.interval_box(horizontal_lines, x)
                ) for x in range(1, 13)
            ]
        )

        text_location = np.array([5, 0, 0])
        text_scaler = 1.75
        major_triad = VGroup(
            VGroup(
                TextMobject("Major").scale(text_scaler),
                TextMobject("Triad").scale(text_scaler),
                TextMobject("(4 : 5 : 6)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 4, 7]]
            )
        )
        minor_triad = VGroup(
            VGroup(
                TextMobject("Minor").scale(text_scaler),
                TextMobject("Triad").scale(text_scaler),
                TextMobject("(10 : 12 : 15)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 3, 7]]
            )
        )
        augmented_triad = VGroup(
            VGroup(
                TextMobject("Augmented").scale(text_scaler),
                TextMobject("Triad").scale(text_scaler),
                TextMobject("(16 : 20 : 25)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 4, 8]]
            )
        )
        diminished_triad = VGroup(
            VGroup(
                TextMobject("Diminished").scale(text_scaler),
                TextMobject("Triad").scale(text_scaler),
                TextMobject("(5 : 6 : 7)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 3, 6]]
            )
        )
        suspended_fourth = VGroup(
            VGroup(
                TextMobject("Suspended").scale(text_scaler),
                TextMobject("Fourth").scale(text_scaler),
                TextMobject("(6 : 8 : 9)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 5, 7]]
            )
        )
        suspended_second = VGroup(
            VGroup(
                TextMobject("Suspended").scale(text_scaler),
                TextMobject("Second").scale(text_scaler),
                TextMobject("(8 : 9 : 12)")
            ).arrange(DOWN).move_to(text_location),
            VGroup(
                *[self.interval_box(horizontal_lines, x)
                  for x in [0, 2, 7]]
            )
        )
        # Walk Through each interval
        mover_interval = interval_groups[0]
        self.play(Write(mover_interval))
        for interval in interval_groups[1:]:
            self.wait(1 / 16)
            self.play(
                Transform(
                    mover_interval,
                    interval,
                    run_time=1 / 16
                )
            )
        self.wait()
        self.play(FadeOut(mover_interval))

        all_chords = [
            major_triad, minor_triad,
            augmented_triad, diminished_triad,
            suspended_fourth, suspended_second
        ]
        current_chord = all_chords[0]

        # Walk Through one simple ratio
        ratio_simplification = VGroup(
            TextMobject("(1 : 5/4 : 3/2)").scale(1.25),
            TextMobject("Multiply by 4").scale(0.75),
            TextMobject("(4 : 5 : 6)").scale(1.25)
        ).arrange(DOWN).move_to(text_location)
        self.play(Write(current_chord[-1]))
        self.play(Write(ratio_simplification[0]))
        self.play(Write(ratio_simplification[1]))
        self.play(ReplacementTransform(
            ratio_simplification[0],
            ratio_simplification[2]
        ))
        self.play(FadeOut(ratio_simplification))

        self.play(Write(current_chord[:-1]))

        for num, chord in enumerate(all_chords[1:], 1):
            self.play(
                Transform(
                    current_chord[1],
                    chord[1]
                ),
                FadeOut(all_chords[num - 1][0]),
                Write(all_chords[num][0])
            )
            self.wait()

        self.wait(4)
        self.play(*[FadeOut(x, run_time=2) for x in self.mobjects])

    # Making Highlighting Boxes
    def interval_box(self, lines, interval):
        rect = Polygon(
            lines[interval].get_left(),
            lines[interval].get_right(),
            lines[interval + 1].get_right(),
            lines[interval + 1].get_left(),
            stroke_opacity=0,
            fill_opacity=0.5,
            fill_color=YELLOW
        )
        return rect


class IntroduceAlgorithm(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 6 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 6.5,
        "x_tick_frequency": PI / 2,
        "y_min": -3.0,
        "y_max": 3.0,
        "y_axis_height": 2.533,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([-6.8, 2, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def c_chord(self, x):
        a = math.sin((261.63 / 100) * x)
        b = math.sin((327.0375 / 100) * x)
        c = math.sin((392.445 / 100) * x)
        return a + b + c

    def dissonant_chord(self, x):
        a = math.sin((261.63 / 100) * x)
        b = math.sin((277.18 / 100) * x)
        c = math.sin((370 / 100) * x)
        return a + b + c

    def construct(self):
        # Upper Left
        self.setup_axes(animate=True)
        graph_left = self.get_graph(self.dissonant_chord, color=BLUE)
        f1 = TextMobject("Wave A", color=BLUE)
        f1.scale(0.8)
        label_coord1 = self.coords_to_point(PI * 0.75, 0)
        f1.next_to(label_coord1, UP)
        UL_box = Polygon([-6.95, 3.4, 0],
                         [-6.95, 0.6, 0],
                         [-0.25, 0.6, 0],
                         [-0.25, 3.4, 0])
        self.play(Write(UL_box),
                  Write(graph_left))

        # Upper Right
        self.graph_origin = np.array((0.3, 2, 0))
        self.setup_axes(animate=True)
        graph_right = self.get_graph(self.c_chord, color=RED)
        f2 = TextMobject("Wave B", color=RED)
        f2.scale(0.7)
        label_coord2 = self.coords_to_point(7 * PI / 8, 0)
        f2.next_to(label_coord2, UP, buff=1)
        UR_box = Polygon([0.15, 3.4, 0],
                         [0.15, 0.6, 0],
                         [6.85, 0.6, 0],
                         [6.85, 3.4, 0],
                         color=RED)
        self.play(Write(UR_box),
                  Write(graph_right))

        # Semi Opac regions to fade most the screen
        left_fade = Polygon([-7.1, 4, 0],
                            [0, 4, 0],
                            [0, 0, 0],
                            [-7.1, -4, 0],
                            color=BLACK,
                            fill=BLACK,
                            fill_opacity=0.75,
                            stroke_opacity=0)

        right_fade = Polygon([0, 4, 0],
                             [7.1, 4, 0],
                             [7.1, 0, 0],
                             [0, 0, 0],
                             color=BLACK,
                             fill=BLACK,
                             fill_opacity=0.75,
                             stroke_opacity=0)
        self.wait(8)
        self.play(FadeIn(right_fade))
        self.play(FadeOut(right_fade))
        self.play(FadeIn(left_fade))
        self.play(FadeOut(left_fade))
        self.wait(9)

        # Create Lower Algorithm
        self.graph_origin = np.array((-5, -2, 0))
        self.x_axis_width = 3
        self.y_axis_height = 2
        self.setup_axes(animate=True)
        left_input_graph = self.get_graph(self.dissonant_chord, color=BLUE)
        right_input_graph = self.get_graph(self.c_chord, color=RED)
        # equation
        f_x = VGroup(
            TexMobject("f(").scale(4).next_to(self.axes, LEFT),
            TexMobject(")=").scale(4).next_to(self.axes, RIGHT),
        )

        # Output
        output = VGroup(
            TexMobject("[Harmonious]", color=GREEN),
            TexMobject("/"),
            TexMobject("[Dissonant]", color=RED)
        ).arrange(RIGHT, buff=0.1).next_to(f_x, RIGHT, buff=0.1)
        self.play(Write(f_x),
                  Write(output))

        # Reference Highlight objects
        highlighting_boxes = VGroup(
            SurroundingRectangle(self.axes, color=YELLOW),
            SurroundingRectangle(output[0], color=YELLOW),
            SurroundingRectangle(output[2], color=YELLOW)
        )
        mover_highlight_box = highlighting_boxes[0].copy()
        self.play(Write(mover_highlight_box),
                  ReplacementTransform(graph_left.copy(), left_input_graph))
        self.wait()
        self.play(Transform(mover_highlight_box, highlighting_boxes[2].copy()))
        self.wait()
        self.play(ReplacementTransform(left_input_graph, graph_left),
                  ReplacementTransform(graph_right.copy(), right_input_graph))
        self.wait()
        self.play(Transform(mover_highlight_box, highlighting_boxes[1].copy()))
        self.wait()
        self.play(FadeOut(mover_highlight_box))
        self.wait()
        self.play(*[FadeOut(x, run_time=3)
                    for x in self.mobjects])


class CheckRatios(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 6 * PI,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 4.5,
        "x_tick_frequency": PI,
        "y_min": -1.0,
        "y_max": 1.0,
        "y_axis_height": 2.533,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array([2.5, 2.6335, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        # Define my functions to add
        # First Set of Waves
        # //////////////////////////////////////////////
        def waveA(x):
            return math.sin((261.63 / 100) * x)

        def waveB(x):
            return math.sin((327.0375 / 100) * x)

        def waveC(x):
            return math.sin((392.445 / 100) * x)

        def waveD(x):
            return waveA(x) + waveB(x) + waveC(x)

        # Second Set of Waves (The Dissonant Wave)
        # ////////////////////////////////////////////////
        def wave2A(x):
            return math.sin((222 / 100) * x)

        def wave2B(x):
            return math.sin((333 / 100) * x)

        def wave2C(x):
            return math.sin((400 / 100) * x)

        def wave2D(x):
            return wave2A(x) + wave2B(x) + wave2C(x)

        # Set up Upper Right(UR) graph
        self.setup_axes(animate=True)
        # Create the two graphs needed
        graph_UR = self.get_graph(waveA, color=BLUE)
        graph_UR_2 = self.get_graph(wave2A, color=BLUE)

        # Set up Middle Right(MR) graph
        self.graph_origin = np.array((2.5, 0, 0))
        self.setup_axes(animate=True)
        graph_MR = self.get_graph(waveB, color=RED)
        graph_MR_2 = self.get_graph(wave2B, color=RED)

        # Set up Lower Right(LR) graph
        self.graph_origin = np.array((2.5, -2.6335, 0))
        self.setup_axes(animate=True)
        graph_LR = self.get_graph(waveC, color=GREEN)
        graph_LR_2 = self.get_graph(wave2C, color=GREEN)

        # Lower
        self.graph_origin = np.array((-7, 2, 0))
        self.x_axis_width = 7
        self.y_min = -3
        self.y_max = 3
        self.y_axis_height = 4

        self.setup_axes(animate=True)
        graph_comp = VGroup(  # Recreates all of the graphs with the new axis
            self.get_graph(waveA, color=BLUE),
            self.get_graph(waveB, color=RED),
            self.get_graph(waveC, color=GREEN)
        )
        graph_comp_2 = VGroup(  # Recreates all of the graphs with the new axis
            self.get_graph(wave2A, color=BLUE),
            self.get_graph(wave2B, color=RED),
            self.get_graph(wave2C, color=GREEN)
        )
        graph_UL = self.get_graph(waveD, color=PURPLE)
        graph_UL_2 = self.get_graph(wave2D, color=PURPLE)

        graphs = VGroup(graph_UR, graph_MR, graph_LR, graph_UL)
        graphs_2 = VGroup(graph_UR_2, graph_MR_2, graph_LR_2, graph_UL_2)
        mover_graph = graphs[3].copy()
        self.wait()
        self.play(Write(mover_graph, run_time=2))

        # Separate Waves
        # /////////////////////////////////////////////////////////////////
        # Remaining Wave forms after each removal
        remaining_graphs = VGroup(
            self.get_graph(lambda x: waveA(x) + waveB(x), color=PURPLE),
            self.get_graph(waveA, color=BLUE)
        )
        remaining_graphs_2 = VGroup(
            self.get_graph(lambda x: wave2A(x) + wave2B(x), color=PURPLE),
            self.get_graph(wave2A, color=BLUE)
        )

        # First Separation
        c_label = TextMobject("392.45", " Hz").next_to(graph_LR, LEFT)
        self.play(
            Transform(mover_graph, remaining_graphs[0]),
            ReplacementTransform(mover_graph.copy(), graph_LR),
            Write(c_label)
        )

        # Second Separation
        b_label = TextMobject("327.04", " Hz").next_to(graph_MR, LEFT)
        self.play(
            Transform(mover_graph, remaining_graphs[1]),
            ReplacementTransform(mover_graph.copy(), graph_MR),
            Write(b_label)
        )

        # Third Separation
        a_label = TextMobject("261.63", " Hz").next_to(graph_UR, LEFT)
        self.play(
            ReplacementTransform(mover_graph, graph_UR),
            Write(a_label)
        )
        self.wait(2)

        # Move all the waves back to the bottom to recombine.
        self.play(
            ReplacementTransform(graph_UR.copy(), graph_comp[0]),
            ReplacementTransform(graph_MR.copy(), graph_comp[1]),
            ReplacementTransform(graph_LR.copy(), graph_comp[2])
        )

        # Recombine all of the parts
        self.play(
            ReplacementTransform(graph_comp[0], graphs[3]),
            ReplacementTransform(graph_comp[1], graphs[3]),
            ReplacementTransform(graph_comp[2], graphs[3])
        )

        # Write out the Ratios text on the lower left corner
        grey_BG_box = Polygon([-7, -1, 0],
                              [-7, -3, 0],
                              [0, -3, 0],
                              [0, -1, 0],
                              fill_color=GREY,
                              fill_opacity=0.5,
                              stroke_opacity=0)
        ratios1 = TextMobject("261.63", " : ", "327.04", " : ", "392.45").scale(1.25).move_to([-3.55, -1.5, 0])
        ratios2 = TextMobject("4", " : ", "5", " : ", "6").scale(1.25).move_to([-3.55, -2.5, 0])
        self.play(FadeIn(grey_BG_box))

        # Ratios without simplification
        self.play(
            Write(ratios1[1]),
            Write(ratios1[3]),
            Write(ratios2[1]),
            Write(ratios2[3])
        )
        self.play(
            ReplacementTransform(a_label[0].copy(), ratios1[0]),
            ReplacementTransform(b_label[0].copy(), ratios1[2]),
            ReplacementTransform(c_label[0].copy(), ratios1[4])
        )

        # Ratios after simplification
        self.play(
            ReplacementTransform(ratios1[0].copy(), ratios2[0]),
            ReplacementTransform(ratios1[2].copy(), ratios2[2]),
            ReplacementTransform(ratios1[4].copy(), ratios2[4])
        )
        self.wait()

        # Clear Graphs and Labels
        self.play(*[FadeOut(x)
                    for x in [
                        graph_UR, graph_MR, graph_LR, graph_UL,
                        a_label, b_label, c_label,
                        ratios1, ratios2
                    ]])

        # Start Second Sound analysis
        # //////////////////////////////////////////////////////////////////
        # Write UL graph
        mover_graph = graphs_2[3].copy()
        self.play(Write(mover_graph, run_time=2))
        # First Separation
        c_label_2 = TextMobject("400", " Hz").next_to(graph_LR_2, LEFT)
        self.play(
            Transform(mover_graph, remaining_graphs_2[0]),
            ReplacementTransform(mover_graph.copy(), graph_LR_2),
            Write(c_label_2)
        )

        # Second Separation
        b_label_2 = TextMobject("333", " Hz").next_to(graph_MR_2, LEFT)
        self.play(
            Transform(mover_graph, remaining_graphs_2[1]),
            ReplacementTransform(mover_graph.copy(), graph_MR_2),
            Write(b_label_2)
        )

        # Third Separation
        a_label_2 = TextMobject("222", " Hz").next_to(graph_UR_2, LEFT)
        self.play(
            ReplacementTransform(mover_graph, graph_UR_2),
            Write(a_label_2)
        )

        # Move all the waves back to the bottom to recombine.
        self.play(
            ReplacementTransform(graph_UR_2.copy(), graph_comp_2[0]),
            ReplacementTransform(graph_MR_2.copy(), graph_comp_2[1]),
            ReplacementTransform(graph_LR_2.copy(), graph_comp_2[2])
        )

        # Recombine all of the parts
        self.play(
            ReplacementTransform(graph_comp_2[0], graphs_2[3]),
            ReplacementTransform(graph_comp_2[1], graphs_2[3]),
            ReplacementTransform(graph_comp_2[2], graphs_2[3])
        )

        second_ratios1 = TextMobject("222", " : ", "333", " : ", "400").scale(1.25).move_to([-3.55, -1.5, 0])
        second_ratios2 = TextMobject("222", " : ", "333", " : ", "400").scale(1.25).move_to([-3.55, -2.5, 0])

        # Ratios without simplification
        self.play(
            Write(second_ratios1[1]),
            Write(second_ratios1[3]),
            Write(second_ratios2[1]),
            Write(second_ratios2[3])
        )
        self.play(
            ReplacementTransform(a_label_2[0].copy(), second_ratios1[0]),
            ReplacementTransform(b_label_2[0].copy(), second_ratios1[2]),
            ReplacementTransform(c_label_2[0].copy(), second_ratios1[4])
        )

        # Ratios after simplification
        self.play(
            ReplacementTransform(second_ratios1[0].copy(), second_ratios2[0]),
            ReplacementTransform(second_ratios1[2].copy(), second_ratios2[2]),
            ReplacementTransform(second_ratios1[4].copy(), second_ratios2[4])
        )
        self.wait(5)

        # End Scene
        # ////////////////////////////////////////////////////////////////
        self.wait(3)
        self.play(*[FadeOut(x)
                    for x in self.mobjects])


class PreRecs(Scene):
    def construct(self):
        # Fourier Transform Group
        fourier_transform = VGroup(
            TextMobject(
                "Fourier Transform: "
            ).scale(1.5),
            TexMobject(
                "F\\left(\\omega\\right)="
                "\\int_{-\\infty}^{\\infty}"
                "f\\left(x\\right)"
                "e^{-2{\\pi}{\\omega}xi}dx"
            )
        ).arrange(RIGHT).to_corner(UL)

        # Discrete Fourier Transform
        discrete_fourier_transform = VGroup(
            TextMobject(
                "Discrete Fourier Transform(DFT): "
            ),
            TexMobject(
                "F\\left(\\omega\\right)="
                "\\sum_{x=0}^{N-1}"
                "f\\left(x\\right)"
                "e^{{-2{\\pi}{\\omega}xi}\\over{N}}"
            )
        ).arrange(RIGHT).to_edge(LEFT)

        # Fast Fourier Transform
        fast_fourier_transform = VGroup(
            TextMobject(
                "Fast Fourier Transform(FFT): "
            ),
            VGroup(
                TextMobject("Divide and Conquer Implementation"),
                TextMobject("of the Discrete Fourier Transform")
            ).scale(0.75).arrange(DOWN)
        ).arrange(RIGHT).to_corner(DL)

        # Group of curved arrows that move from one transform to the next
        transitions = VGroup(
            CurvedArrow(np.array([-1, 2.5, 0]), np.array([-1, 0.5, 0])),
            CurvedArrow(np.array([-1, -0.5, 0]), np.array([-1, -2.5, 0]))
        )

        large_x = VGroup(
            Line(np.array([-7, 4, 0]), np.array([7, -4, 0]), color=RED, stroke_width=30),
            Line(np.array([-7, -4, 0]), np.array([7, 4, 0]), color=RED, stroke_width=30)
        )

        # Fourier Transform
        self.play(Write(fourier_transform))
        self.wait(2)

        # Discrete Fourier Transform
        self.play(ReplacementTransform(
            fourier_transform.copy(), discrete_fourier_transform
        ),
            Write(transitions[0])
        )
        self.wait(2)

        # Fast Fourier Transform
        self.play(ReplacementTransform(
            discrete_fourier_transform.copy(), fast_fourier_transform
        ),
            Write(transitions[1])
        )
        self.wait(2)
        self.play(Write(large_x))
        self.wait(4)
        self.play(*[FadeOut(x)
                    for x in self.mobjects])


class GeneralFourierExplanation(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 1,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 5,
        "x_tick_frequency": 1,
        "y_min": 0,
        "y_max": 2.0,
        "y_axis_height": 3,
        "y_axis_label": None,  # "$y$",
        "y_tick_frequency": 1,
        "y_bottom_tick": 0,
        "graph_origin": np.array([-6, -1, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        self.demonstrate_conversion()

        self.box_venn_diagram()

    def demonstrate_conversion(self):
        # Create Time Domain Graph
        time_axes = self.setup_axes()
        sine_func = make_wave([(2, 1, 0)])
        sine_obj = self.get_graph(sine_func)

        # Setup Trans Graph
        self.x_max = 3
        self.graph_origin = np.array([1, -1, 0])
        freq_axes = self.setup_axes()
        trans_func = transform_wave(sine_func, (-20, 20), 2000, 1 / 10, 0.1)
        trans_obj = self.get_graph(trans_func, step_size=0.005)

        title = TextMobject(
            "Fourier Transform", color=GREY
        ).scale(2).to_edge(UP)
        double_arrow = TexMobject(
            "\\rightleftharpoons", color=GREY
        ).scale(3)
        labels = VGroup(
            TextMobject("Time Domain", color=GREY).next_to(time_axes, DOWN),
            TextMobject("Freq Domain", color=GREY).next_to(freq_axes, DOWN)
        )
        self.wait(2)

        for graph in (sine_obj, trans_obj):
            self.play(Write(graph))

        self.play(*[Write(x) for x in (title, double_arrow, labels)])
        self.wait()
        frame = Rectangle(width=14.2 * 2 / 3, height=8 * 2 / 3).move_to([0, 8, 0])
        self.add(frame)
        self.wait(2)

        # I really wanted to use list comprehension here, but i couldn't because of manim & syntax
        # Instead, i condesned everything into a single object(VGroup)
        everything = VGroup(*self.mobjects)
        self.play(  # Slide everything down, revealing the frame
            everything.shift, [0, -8, 0]
        )
        self.wait(2)

        self.wait()
        self.play(  # Slide everything back
            everything.shift, [0, 8, 0]
        )
        self.wait(24)

        self.remove(*self.mobjects)  # FadeOut EVERYTHING
        self.wait(2)

    def box_venn_diagram(self):
        fourier_transform = VGroup(
            Rectangle(width=FRAME_WIDTH * (3 / 4), height=FRAME_HEIGHT * (3 / 4),
                      fill_opacity=0.25, fill_color=GREY),
            TextMobject("Fourier Transform").scale(1.25).move_to([0, FRAME_HEIGHT * (3 / 8) - 0.5, 0])
        )
        discrete_fourier = VGroup(
            Rectangle(width=FRAME_WIDTH * (5 / 8), height=FRAME_HEIGHT * (2 / 4),
                      fill_opacity=0.25, fill_color=GREY),
            TextMobject("Discrete Fourier Transform").scale(1.25).move_to([0, FRAME_HEIGHT * (2 / 8) - 0.5, 0])
        )
        fast_fourier = VGroup(
            Rectangle(width=FRAME_WIDTH * (2 / 4), height=FRAME_HEIGHT * (1 / 4),
                      fill_opacity=0.25, fill_color=GREY),
            TextMobject("Fast Fourier Transform").scale(1.25).move_to([0, FRAME_HEIGHT * (1 / 8) - 0.5, 0])
        )

        self.x_axis_width = 12
        self.y_axis_height = 3

        # Fourier Transform Graphs (ABOVE SCREEN)
        # Time Domain Graph
        self.graph_origin = np.array([-6, 0.5 + 8, 0])
        time_fourier_axes = self.setup_axes()
        time_domain_func = make_wave([(1, 0.5, 0), (2, 0.5, 0)])
        time_domain_obj = self.get_graph(time_domain_func, color=BLUE)
        self.add(time_domain_obj)
        # Freq Domain Graph
        self.graph_origin = np.array([-6, -3.5 + 8, 0])
        freq_fourier_axes = self.setup_axes()
        freq_domain_func = transform_wave(time_domain_func, (-40, 40), 2000, 1 / 10, 0.1)
        freq_domain_obj = self.get_graph(freq_domain_func, step_size=0.0025, color=BLUE)
        self.add(freq_domain_obj)

        # Discrete Fourier Transform Graph (RIGHT OF SCREEN)
        # Top graph
        self.graph_origin = np.array([-6 + 14.2, 0.5, 0])
        discrete_axes = self.setup_axes()
        time_discrete_dots = VGroup(
            *[Dot(color=GREEN).move_to(self.coords_to_point(
                x / (100 / 3), time_domain_func(x / (100 / 3))
            )) for x in [*range(101), 100 / 3, 200 / 3]]
        )
        self.add(time_discrete_dots)
        # Bottom Graph
        self.graph_origin = np.array([-6 + 14.2, -3.5, 0])
        discrete_axes = self.setup_axes()
        freq_discrete_dots = VGroup(
            *[Dot(color=GREEN).move_to(self.coords_to_point(
                x / (100 / 3), freq_domain_func(x / (100 / 3))
            )) for x in [*range(101), 100 / 3, 200 / 3]]
        )
        self.add(freq_discrete_dots)

        # Fast Fourier Transform Graph (BELOW SCREEN)
        self.y_axis_height = 6
        self.x_max = 20
        self.y_max = 400
        self.y_tick_frequency = 10
        self.graph_origin = np.array([-6, -3 - 8, 0])
        self.current_value = ValueTracker(5)
        fast_axes = self.setup_axes()

        time_axes_label = TextMobject("Time", color=GREY).rotate(PI / 2).move_to(
            self.coords_to_point(-1, 200)
        )

        def slow_func(x):
            return x ** 2

        def fast_func(x):
            return x * math.log2(x)

        slow_graph = self.get_graph(slow_func, color=GREEN)
        fast_graph = self.get_graph(fast_func, color=RED, x_min=0.01)

        updated_line = Line(  # A Line that Stretched from the x_axes to the top graph
            self.coords_to_point(self.current_value.get_value(), 0),
            self.coords_to_point(self.current_value.get_value(), self.current_value.get_value() ** 2)
        ).add_updater(
            lambda obj: obj.become(
                Line(
                    self.coords_to_point(self.current_value.get_value(), 0),
                    self.coords_to_point(self.current_value.get_value(), slow_func(self.current_value.get_value()))
                )
            )
        )

        # DFT Dot and label
        slow_func_dot = Dot(color=GREEN).scale(2.5).add_updater(
            lambda obj: obj.move_to(updated_line.get_top())
        )
        dft_label = TexMobject("O\\left(n^2\\right)", color=GREEN).move_to(
            self.coords_to_point(12, slow_func(14))
        )

        # FFT Dot and label
        fast_func_dot = Dot(color=RED).scale(2.5).add_updater(
            lambda obj: obj.move_to(
                self.coords_to_point(self.current_value.get_value(),
                                     fast_func(self.current_value.get_value()))
            )
        )
        fft_label = TexMobject("O\\left(nlog_2\\left(n\\right)\\right)", color=RED).move_to(
            self.coords_to_point(15, slow_func(10))
        )

        self.add(slow_graph, fast_graph, updated_line,
                 slow_func_dot, fast_func_dot,
                 dft_label, fft_label, time_axes_label)

        # Shift screen to Fourier Explanation
        self.play(Write(fourier_transform))
        everything = VGroup(*self.mobjects)
        self.play(
            everything.shift, [0, -8, 0]
        )
        self.wait(2)
        self.play(ReplacementTransform(
            time_domain_obj.copy(), freq_domain_obj
        ))
        self.wait(10)
        self.play(
            everything.shift, [0, 8, 0]
        )

        # Shift Screen to Discrete Fourier Transform Explanation
        self.play(Write(discrete_fourier))
        everything = VGroup(*self.mobjects)
        self.wait(2)
        self.play(
            everything.shift, [-14.2, 0, 0]
        )
        self.wait(5)
        self.play(ReplacementTransform(
            time_discrete_dots.copy(), freq_discrete_dots
        ))
        self.wait(2)
        self.play(
            everything.shift, [14.2, 0, 0]
        )
        self.wait(2)

        # Shift Screen to Fast Fourier Transform Explanation
        self.play(Write(fast_fourier))

        # Move the sample value up by 15 units
        self.wait(2)

        everything.add(fast_fourier)
        self.play(
            everything.shift, [0, 8, 0]
        )
        self.wait(7)
        self.play(
            self.current_value.increment_value, 15, run_time=4
        )

        for mob in [updated_line, fast_func_dot, slow_func_dot]:
            mob.clear_updaters()
            everything.add(mob)
        self.wait()

        # Shift to first Double graph screen
        self.play(
            everything.shift, [0, -16, 0],
            run_time=3
        )
        self.wait(4)

        self.play(*[FadeOut(x, run_time=2) for x in self.mobjects])  # Fade out everything


class SimpleExplanation(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 2,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 14,
        "x_tick_frequency": 0.4,
        "y_min": -0.25,
        "y_max": 2.0,
        "y_axis_height": 3.8,
        "y_axis_label": None,  # "$y$",
        "y_tick_frequency": 1,
        "y_bottom_tick": 0,
        "graph_origin": np.array([-7, 0.5222, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        #  /////////////////////////////////////////////////////
        #  Top Graph WAVE1
        #  /////////////////////////////////////////////////////

        self.setup_axes()
        time_label = TextMobject('time', color=GREY
                                 ).scale(1.2).move_to(self.coords_to_point(0.1, -0.145))

        wave1_func = make_wave([(2, 1, 0)])  # [(freq, mag, phase)]
        sine_wave_obj = VGroup()
        wave_graph_obj = self.get_graph(wave1_func, color=BLUE)
        sine_graph_label_bg = Rectangle(  # BackGround For Label
            fill_color=BLACK,
            fill_opacity=0.75,
            stroke_opacity=0
        ).scale(0.45).move_to(self.coords_to_point(0.625, 0.5))
        sine_graph_label = TextMobject("200Hz").scale(1.25).move_to(self.coords_to_point(0.625, 0.5))  # Label

        # Create samples of wave1 graph
        wave_sample_dots = VGroup()
        num_samples = 102
        sample_width = 2 / num_samples
        for i in range(num_samples):
            sample_x = sample_width * i
            wave_sample_dots.add(
                Dot(color=BLUE).move_to(self.coords_to_point(sample_x, wave1_func(sample_x))
                                        ).scale(0.5)
            )

        sine_wave_obj.add(
            wave_graph_obj,
            wave_sample_dots,
            sine_graph_label_bg,
            sine_graph_label
        )

        #  /////////////////////////////////////////////////////
        #  Top Graph Wave2
        #  /////////////////////////////////////////////////////
        wave2_func = make_wave([(2, 0.5, 0), (3, 0.5, 0)])  # [(freq, mag, phase)]
        wave2_group = VGroup()
        wave2_graph_obj = self.get_graph(wave2_func, color=BLUE)
        wave2_graph_label_bg = Rectangle(  # BackGround For Label
            fill_color=BLACK,
            fill_opacity=0.75,
            stroke_opacity=0
        ).scale(0.45).move_to(self.coords_to_point(0.625, 0.5))
        wave2_graph_label2 = TextMobject("200Hz+300Hz").scale(1.25).move_to(self.coords_to_point(0.625, 0.5))  # Label

        # Create samples of wave1 graph
        wave2_sample_dots = VGroup()
        num_samples_wave2 = 102
        wave2_sample_width = 2 / num_samples_wave2
        for i in range(num_samples):
            sample_x = wave2_sample_width * i
            wave2_sample_dots.add(
                Dot(color=BLUE).move_to(self.coords_to_point(sample_x, wave2_func(sample_x))
                                        ).scale(0.5)
            )

        wave2_group.add(
            wave2_graph_obj,
            wave2_sample_dots,
            wave2_graph_label_bg,
            wave2_graph_label2
        )

        #  /////////////////////////////////////////////////////
        #  Bottom Graph
        #  /////////////////////////////////////////////////////

        # New Axes Params
        self.graph_origin = np.array([-7, -3.4777, 0])
        self.x_min = 0
        self.x_max = 5
        self.y_min = -0.125
        self.y_max = 1
        self.y_tick_frequency = 0.5
        self.x_tick_frequency = 1
        self.setup_axes()

        # Draw Transform
        wave1_trans = transform_wave(wave1_func)
        transform_obj = VGroup()

        trans_graph_obj = self.get_graph(wave1_trans, GREEN)

        # Generate all of the x axis Labels
        x_axis_labels = VGroup()
        for i in range(1, 5):
            x_axis_labels.add(
                Rectangle(  # BackGround For Label
                    width=1.2,
                    height=0.44,
                    fill_color=BLACK,
                    fill_opacity=0.5,
                    stroke_opacity=0
                ).move_to(self.coords_to_point(i, -0.075)),

                TextMobject(
                    "{} Hz".format(i * 100)
                ).scale(0.75).move_to(self.coords_to_point(i, -0.075))
            )

        # Many Samples for DFT demonstration
        transform_sample_dots = VGroup()
        num_samples2 = 100
        sample_width2 = 5 / num_samples2
        for i in range(num_samples2):
            sample_x2 = sample_width2 * i
            transform_sample_dots.add(
                Dot(color=GREEN).move_to(self.coords_to_point(sample_x2, wave1_trans(sample_x2))
                                         ).scale(0.5)
            )
            if wave1_trans(sample_x2) > 0.9:
                for x, y in zip([sample_x2 + (sample_width2 / 2), sample_x2 - (sample_width2 / 2)],
                                [0.5, 0.5]):
                    transform_sample_dots.add(
                        Dot(color=GREEN).move_to(self.coords_to_point(x, y)).scale(0.5)
                    )

        transform_obj.add(trans_graph_obj, transform_sample_dots, x_axis_labels)

        #  ////////////////////////////////////////////////////////////
        #  Second Transform function
        #  ////////////////////////////////////////////////////////////
        # Draw Transform
        wave2_trans = transform_wave(wave2_func)
        transform_obj2 = VGroup()

        trans_graph_obj2 = self.get_graph(wave2_trans, color=GREEN)

        # Many Samples for DFT demonstration
        transform2_sample_dots = VGroup()
        num_samples2 = 100
        sample_width2 = 5 / num_samples2
        for i in range(num_samples2):
            sample_x2 = sample_width2 * i
            transform2_sample_dots.add(
                Dot(color=GREEN).move_to(self.coords_to_point(sample_x2, wave2_trans(sample_x2))
                                         ).scale(0.5)
            )
            if wave2_trans(sample_x2) > 0.45:
                for x, y in zip([sample_x2 + (sample_width2 / 2), sample_x2 - (sample_width2 / 2)],
                                [0.25, 0.25]):
                    transform2_sample_dots.add(
                        Dot(color=GREEN).move_to(self.coords_to_point(x, y)).scale(0.5)
                    )

        transform_obj2.add(trans_graph_obj2.copy(), transform2_sample_dots)

        #  /////////////////////////////////////////////////////
        #  Start Playing Animations
        #  /////////////////////////////////////////////////////
        self.add(time_label)

        # Top Graph Wave1
        self.play(
            Write(sine_wave_obj[0], run_time=5),
            *[Write(x)
              for x in [
                  sine_wave_obj[2],
                  sine_wave_obj[3],
                  transform_obj[2]
              ]])

        # Transform continuous first wave
        self.play(
            ReplacementTransform(sine_wave_obj[0].copy(), transform_obj[0], run_time=3),
            ReplacementTransform(transform_obj[2].copy(), transform_obj[2])  # Bug Fix, keeps the labels on top
        )
        self.wait(3)

        # Fade Out continuous function
        self.play(
            FadeOut(sine_wave_obj[0]),
            FadeOut(transform_obj[0])
        )

        # Add the data points for wave 1
        for sample in wave_sample_dots:
            self.add(sample)
            self.wait(1 / 20)
        self.wait(3)

        # Apply DFT
        self.play(ReplacementTransform(wave_sample_dots.copy(), transform_obj[1], run_time=3))
        self.wait(3)

        # Fade Out most of the parts
        self.play(*[FadeOut(x)
                    for x in [
                        sine_wave_obj[1],
                        sine_wave_obj[2],
                        sine_wave_obj[3],
                        transform_obj[1]
                    ]])
        self.wait()
        #  /////////////////////////////////////////////////////
        #  Wave2
        #  /////////////////////////////////////////////////////
        #  Continuous Wave Form
        self.play(
            Write(wave2_group[0], run_time=5),
            Write(wave2_group[2]),
            Write(wave2_group[3])
        )

        # Apply Fourier Transform
        self.play(ReplacementTransform(wave2_graph_obj.copy(), trans_graph_obj2, run_time=3))
        self.wait(3)

        # Fade Out continuous graph
        self.play(
            FadeOut(wave2_graph_obj),
            FadeOut(trans_graph_obj2)
        )
        self.wait()

        # Draw Out Samples
        for sample in wave2_sample_dots:
            self.add(sample)
            self.wait(1 / 20)
        self.wait(2)

        # Apply Discrete Fourier Transform
        self.play(ReplacementTransform(wave2_sample_dots.copy(), transform2_sample_dots, run_time=3))
        self.wait(3)

        #  /////////////////////////////////////////////////////
        #  OverLying Graph
        #  /////////////////////////////////////////////////////
        self.play(FadeIn(Rectangle(  # Dim the BackGround
            width=14.2, height=8,
            fill_color=BLACK, fill_opacity=0.75,
            stroke_opacity=0
        )))
        self.wait()

        self.x_min = 0
        self.x_max = 30
        # self.x_axis_label = "Input Size",  # "$\\theta$",
        self.x_axis_width = 14
        self.x_tick_frequency = 1
        self.y_min = 0
        self.y_max = 900
        self.y_axis_height = 7.8
        # self.y_axis_label = "Computation Time"  # "$y$",
        self.y_tick_frequency = 50
        self.y_bottom_tick = 0
        self.graph_origin = np.array([-7, -3.9, 0])
        self.function_color = WHITE
        self.axes_color = GREY

        self.setup_axes(True)

        o_n_squared = self.get_graph(lambda x: x * x, RED, stroke_width=8)
        o_n_squared_label = self.get_graph_label(
            o_n_squared, "O\\left(n^2\\right)", 15, UL
        )
        o_n_logn = self.get_graph(lambda x: x * math.log(x, 2), BLUE, 1, stroke_width=8)
        o_n_logn_label = self.get_graph_label(
            o_n_logn, "O\\left(nlog\\left(n\\right)\\right)", 20, UP
        )
        self.play(Write(o_n_squared, run_time=2),
                  Write(o_n_squared_label))
        self.wait(3)
        self.play(Write(o_n_logn, run_time=2),
                  Write(o_n_logn_label))


class CheckRatios2(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 8,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 10.1,
        "x_tick_frequency": 1,
        "y_min": -3.0,
        "y_max": 3.0,
        "y_axis_height": 3.8,
        "y_axis_label": None,  # "$y$",
        "graph_origin": np.array((-7, 2, 0)),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        # Waves with minimum set to y=0
        major_wave = make_wave([(2.6163, 1, 0), (3.270375, 1, 0), (3.92445, 1, 0)], 0)
        dissonant_wave = make_wave([(2.27, 1, 0), (3.31, 1, 0), (4.79, 1, 0)], 0)
        minor_wave = make_wave([(2.2, 1, 0), (2.62, 1, 0), (3.3, 1, 0)], 0)

        self.setup_axes(animate=False)  # Set up Upper Right(UR) graph

        major_wave_obj = self.get_graph(major_wave, color=PURPLE)  # Create the two graphs needed
        dissonant_wave_obj = self.get_graph(dissonant_wave, color=PURPLE)
        minor_wave_obj = self.get_graph(minor_wave, color=PURPLE)

        #  Lower Graph Params
        self.graph_origin = np.array((-16.35, -3.404, 0))
        self.x_axis_width = 14
        self.y_min = -0.15
        self.y_max = 1
        self.x_min = 2
        self.x_max = 5
        self.x_tick_frequency = 0.1
        self.x_leftmost_tick = self.x_min

        self.setup_axes(animate=False)
        transform_func = transform_wave(major_wave, (-100, 100), 2000, 0.01, 0.1)
        major_transform_obj = self.get_graph(transform_func, color=BLUE, step_size=0.001)  # Create Graph
        dissonant_trans_func = transform_wave(dissonant_wave, (-100, 100), 2000, 0.01, 0.1)
        dissonant_trans_obj = self.get_graph(dissonant_trans_func, color=BLUE, step_size=0.001)  # Create Graph
        minor_transform_func = transform_wave(minor_wave, (-100, 100), 2000, 0.01, 0.1)
        minor_transform_obj = self.get_graph(minor_transform_func, color=BLUE, step_size=0.001)
        # Create Axis Labels
        axis_labels = VGroup()
        for i in range(28):
            up = (i % 2) * 0.06
            axis_labels.add(
                Rectangle(  # BackGround For Label
                    width=1.2,
                    height=0.44,
                    fill_color=BLACK,
                    fill_opacity=0.5,
                    stroke_opacity=0
                ).move_to(self.coords_to_point(i, -0.075)),

                TextMobject(
                    "{}".format((i * 10) + 210)
                ).scale(0.4).move_to(self.coords_to_point((0.1 * i) + 2.1, -0.125 + up)
                                     ))

        grey_bg_box = Rectangle(width=3.8, height=1.5, fill_color=GREY, fill_opacity=0.5, stroke_opacity=0
                                ).move_to([5.1, 2, 0])
        ratios1 = TextMobject("261:327:392").move_to([5.1, 2.3, 0])
        simplified_ratios1 = TextMobject("4 : 5 : 6").move_to([5.1, 1.7, 0])
        ratios2 = TextMobject("227:331:479").move_to([5.1, 2.3, 0])
        simplified_ratios2 = TextMobject("227:331:479").move_to([5.1, 1.7, 0])
        ratios3 = TextMobject("220:264:330").move_to([5.1, 2.3, 0])
        simplified_ratios3 = TextMobject("10:12:15").move_to([5.1, 1.7, 0])

        # First Wave
        self.add(grey_bg_box)
        self.wait(4)
        self.play(
            Write(axis_labels),
            Write(major_wave_obj, run_time=2)
        )
        self.play(
            ReplacementTransform(major_wave_obj.copy(), major_transform_obj)
        )
        self.wait(7)
        self.play(
            Write(ratios1)
        )
        self.play(
            ReplacementTransform(ratios1.copy(), simplified_ratios1)
        )
        self.wait(2)

        # Dissonant Wave
        self.play(  # Transform Graphs into second example
            ReplacementTransform(major_wave_obj, dissonant_wave_obj),
            ReplacementTransform(major_transform_obj, dissonant_trans_obj)
        )

        self.play(  # Clear first ratios and write the second set of freqs
            FadeOutAndShiftDown(ratios1),
            FadeOutAndShiftDown(simplified_ratios1),
            Write(ratios2)
        )
        self.play(ReplacementTransform(ratios2.copy(), simplified_ratios2))

        # Minor Wave
        self.play(  # Transform Graphs into second example
            ReplacementTransform(dissonant_wave_obj, minor_wave_obj),
            ReplacementTransform(minor_transform_obj, dissonant_trans_obj)
        )

        self.play(  # Clear first ratios and write the second set of freqs
            FadeOutAndShiftDown(ratios2),
            FadeOutAndShiftDown(simplified_ratios2),
            Write(ratios3)
        )
        self.play(ReplacementTransform(ratios3.copy(), simplified_ratios3))

        self.wait(8)
        self.play(*[FadeOut(x) for x in self.mobjects])


class FourierVisual(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 2,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 10,
        "x_tick_frequency": 1,
        "y_min": -0.25,
        "y_max": 2.0,
        "y_axis_height": 2.8,
        "y_axis_label": None,  # "$y$",
        "y_tick_frequency": 1,
        "y_bottom_tick": 0,
        "graph_origin": np.array([-7, 1.4, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        self.setup_attributes()

        # Create Upper Left Graph
        self.setup_axes(False)
        self.create_sine_func()  # Stores func in self.sine_func
        sine_label = TextMobject("1 Hz").move_to(
            self.coords_to_point(1.25, 1.5)
        ).scale(1.25)
        compound_label = TextMobject("1 Hz + 2 Hz").move_to(
            self.coords_to_point(1.35, 1.5)
        ).scale(1.25)
        self.play(Write(sine_label))
        sine_obj1 = self.get_graph(self.sine_func, color=BLUE)
        compound_obj = self.get_graph(self.compound_func, color=BLUE)
        straight_arrow = self.create_straight_arrow()  # Simple straight arrow for demonstration

        # Create Transformed Graph
        self.setup_second_axes()
        self.transform_func1 = transform_wave(self.sine_func, (0, 16), 1000, 0.125, 1 / 16)
        self.transform_func2 = transform_wave(self.compound_func, (0, 16), 1000, 0.125, 1 / 8)
        transform_obj1 = self.get_graph(self.transform_func1, color=RED, step_size=0.001)
        transform_obj2 = self.get_graph(self.transform_func2, color=RED, step_size=0.001)

        # Create Parametric Graph
        self.setup_winding_axes()
        mover_wound_obj_sine = self.create_wound_obj(
            self.create_wound_sine(self.freq.get_value()),
            2
        )
        mover_wound_obj_comp = self.create_wound_obj(
            self.create_wound_compound(self.freq.get_value()),
            2
        )
        curved_arrow = self.create_wound_arrow()  # Curved Arrow for demonstration purposes

        self.create_scene_label()  # Does exactly as it says

        self.play(Write(sine_obj1))  # Write Sine Function
        self.play(Write(straight_arrow))

        curved_arrow.add_updater(self.update_curved_arrow)  # Curve arrow along sine graph
        self.play(
            ReplacementTransform(sine_obj1.copy(), mover_wound_obj_sine, run_time=3),  # Create Parametric Function Part
            ReplacementTransform(straight_arrow.copy(), curved_arrow, run_time=3)
        )
        mover_wound_obj_sine.add_updater(self.wound_sine_updater)  # Begin Updating Parametric Function
        self.wait()

        # Wind the function for demonstration before extending the signal
        self.play(self.freq.increment_value, 1 - (1 / 16), run_time=6)
        self.play(self.freq.increment_value, (1 / 16), run_time=2)
        self.play(self.freq.increment_value, (-2 / 16), run_time=2)
        self.play(self.freq.increment_value, (1 / 16), run_time=2)

        # Unwind the graph
        self.play(self.freq.set_value, 1 / 16, run_time=3)
        self.play(FadeOut(curved_arrow),
                  FadeOut(straight_arrow))
        self.wait(5)

        # Extend the length of the signal
        self.play(self.length.set_value, 16, run_time=7)

        # Show Center Of Mass
        sine_c_o_m = self.create_center_of_mass(self.sine_func)
        compound_c_o_m = self.create_center_of_mass(self.compound_func)
        self.play(Write(sine_c_o_m))
        sine_c_o_m.add_updater(lambda obj: obj.become(self.create_center_of_mass(self.sine_func)))

        # create transform
        sine_transform_mover = self.create_transform_mover(self.transform_func1)
        comp_transform_mover = self.create_transform_mover(self.transform_func2)
        self.play(Write(sine_transform_mover))
        sine_transform_mover.add_updater(lambda obj: obj.become(self.create_transform_mover(self.transform_func1)))

        # Draw Transform
        path = VMobject(color=RED)
        path.set_points_as_corners([sine_transform_mover[1].get_center(),  # The Dot Center
                                    sine_transform_mover[1].get_center()])

        def update_path(path_mob):  # Add the Dot's location to the path each frame
            previous_path = path_mob.copy()
            previous_path.add_points_as_corners([sine_transform_mover[1].get_center()])
            path_mob.become(previous_path)

        path.add_updater(update_path)
        self.add(path)
        self.play(self.freq.increment_value, 4 - (1 / 16), run_time=15, rate_func=smooth)  # Draw Out Path
        path.remove_updater(update_path)
        self.play(
            FadeOut(path, run_time=0.5),
            FadeIn(transform_obj1, run_time=0.5)
        )
        self.wait()

        self.play(self.freq.increment_value, -1, run_time=2)
        self.wait()
        self.play(self.freq.increment_value, -1, run_time=3)
        self.wait()
        self.play(self.freq.increment_value, -1 + (1 / 16), run_time=4)
        self.wait()
        self.play(self.freq.increment_value, -2 / 16, run_time=4)
        self.wait()
        self.play(self.freq.increment_value, 1 / 16, run_time=4)
        self.wait(5)

        # Remove Updaters before fading
        mover_wound_obj_sine.clear_updaters()
        sine_c_o_m.clear_updaters()
        sine_transform_mover.clear_updaters()
        self.wait(3)

        # Clean up all of the graphs
        self.play(
            *[FadeOut(x)
              for x in [
                  sine_obj1,
                  transform_obj1,
                  mover_wound_obj_sine,
                  sine_c_o_m,
                  sine_transform_mover,
                  sine_label
              ]]
        )
        self.wait(2)

        self.play(Write(compound_obj),
                  Write(compound_label))

        self.play(ReplacementTransform(
            compound_obj.copy(),
            mover_wound_obj_comp
        ))

        self.freq.set_value(1 / 16)
        self.length.set_value(2)

        # Begin updating the wound obj than Extend the function before winding it
        mover_wound_obj_comp.add_updater(lambda obj: obj.become(
            self.create_wound_obj(
                self.create_wound_compound(self.freq.get_value()),
                self.length.get_value()
            )
        ))

        self.play(self.freq.set_value, 1 / 8)
        self.play(self.length.set_value, 16, run_time=2)

        self.play(Write(compound_c_o_m),  # New Center of Mass
                  Write(comp_transform_mover))  # Transform Mover

        # Update Center of Mass
        compound_c_o_m.add_updater(lambda obj: obj.become(
            self.create_center_of_mass(self.compound_func)
        ))

        # Update transform mover
        comp_transform_mover.add_updater(lambda obj: obj.become(
            self.create_transform_mover(self.transform_func2)
        ))

        # Draw Transform
        path2 = VMobject(color=RED)
        path2.set_points_as_corners([comp_transform_mover[1].get_center(),  # The Dot Center
                                     comp_transform_mover[1].get_center()])

        def update_path2(path_mob):  # Add the Dot's location to the path each frame
            previous_path = path_mob.copy()
            previous_path.add_points_as_corners([comp_transform_mover[1].get_center()])
            path_mob.become(previous_path)

        path2.add_updater(update_path2)
        self.add(path2)
        self.play(self.freq.increment_value, 4 - (1 / 8), run_time=15, rate_func=smooth)  # Draw Out Path
        path2.remove_updater(update_path2)

        # Replace drawn-out path with graph object
        self.play(
            FadeOut(path2),
            Write(transform_obj2)
        )
        self.wait(8)

        self.play(self.freq.increment_value, -1, run_time=2)
        self.wait()
        self.play(self.freq.increment_value, -1 + (1 / 16), run_time=2)
        self.wait()
        self.play(self.freq.increment_value, -2 / 16, run_time=2)
        self.wait()
        self.play(self.freq.increment_value, 1 / 16, run_time=2)
        self.wait()
        self.play(self.freq.increment_value, -1 + (1 / 16), run_time=2)
        self.wait()
        self.play(self.freq.increment_value, -2 / 16, run_time=2)
        self.wait()
        self.play(self.freq.increment_value, 1 / 16, run_time=2)
        self.wait()

        # Clear Updaters
        mover_wound_obj_comp.clear_updaters()
        compound_c_o_m.clear_updaters()
        comp_transform_mover.clear_updaters()

        self.play(
            *[FadeOut(x)
              for x in self.mobjects]
        )

    def create_sine_func(self):
        simple_data = [
            (1, 1, PI),
        ]
        compound_data = [
            (1, 0.5, PI), (2, 0.5, PI)
        ]
        self.sine_func = make_wave(simple_data)
        self.compound_func = make_wave(compound_data)

    def create_straight_arrow(self):
        head_location = self.create_wound_sine(self.freq.get_value())
        arrow_group = VGroup()
        arrow_line = Line(
            self.coords_to_point(0, 1),
            self.coords_to_point(2, 1),
            color=GREEN
        )
        arrow_head = Triangle(
            stroke_opacity=0,
            fill_opacity=1,
            fill_color=GREEN
        ).rotate(-PI / 2
                 ).scale(0.25
                         ).move_to(self.coords_to_point(2, 1))
        arrow_group.add(
            arrow_line,
            arrow_head
        )
        return arrow_group

    def create_wound_arrow(self):
        arrow_location = self.create_wound_sine(self.freq.get_value())(self.length.get_value())
        wound_graph_origin = np.array([-5, -1.5, 0])
        curve_angle = -self.freq.get_value() * self.length.get_value() * 2 * PI
        curved_arrow_group = VGroup()
        arrow_arc = Arc(
            0,
            curve_angle,
            arc_center=wound_graph_origin,
            radius=1,
            color=GREEN
        )
        arrow_head = Triangle(
            stroke_opacity=0,
            fill_opacity=1,
            fill_color=GREEN
        ).rotate(-PI + curve_angle
                 ).scale(0.15
                         ).move_to([wound_graph_origin[0] + arrow_location[0],
                                    wound_graph_origin[1] + arrow_location[1],
                                    0])
        curved_arrow_group.add(
            arrow_arc,
            arrow_head
        )
        return curved_arrow_group

    def update_curved_arrow(self, obj):
        curved_arrow_group = self.create_wound_arrow()
        obj.become(curved_arrow_group)

    def create_wound_sine(self, freq):
        def func(x):
            return np.array((
                self.sine_func(x) * np.cos(-TAU * freq * x),
                self.sine_func(x) * np.sin(-TAU * freq * x),
                0
            ))

        return func

    def create_wound_compound(self, freq):
        def func(x):
            return np.array((
                self.compound_func(x) * np.cos(-TAU * freq * x),
                self.compound_func(x) * np.sin(-TAU * freq * x),
                0
            ))

        return func

    def create_wound_obj(self, func, length):
        return ParametricFunction(
            func,
            t_max=length,
            fill_opacity=0,
            color=BLUE
        ).shift(self.graph_origin)

    def wound_sine_updater(self, obj):
        replacement_obj = self.create_wound_obj(
            self.create_wound_sine(self.freq.get_value()),
            self.length.get_value()
        )
        obj.become(replacement_obj)

    def wound_comp_updater(self, obj):
        replacement_obj = self.create_wound_obj(
            self.create_wound_compound(self.freq.get_value()),
            self.length.get_value()
        )
        obj.become(replacement_obj)

    def setup_second_axes(self):
        self.x_min = 0
        self.x_max = 4
        self.x_axis_label = None  # "$\\theta$"
        self.x_axis_width = 9.5
        self.y_min = 0
        self.y_max = 1
        self.y_axis_height = 4
        self.y_axis_label = None  # "$y$"
        self.y_tick_frequency = 1
        self.y_bottom_tick = 0
        self.graph_origin = np.array([-2.75, -3.5, 0])
        self.setup_axes(True)

    def setup_winding_axes(self):
        # The Wound Graph
        # New Axes
        self.x_min = -1
        self.x_max = 1
        self.x_axis_width = 4
        self.x_tick_frequency = 0.5
        self.x_bottom_tick = -1
        self.y_min = -1
        self.y_max = 1
        self.y_axis_height = 4
        self.y_tick_frequency = 0.5
        self.y_bottom_tick = -1
        self.graph_origin = np.array([-5, -1.5, 0])
        self.setup_axes(True)

    def coords_to_transfrom_graph(self, coords):
        g_origin = (-2.75, -3.5, 0)
        g_limits = (4, 1)
        g_length = 9.5
        g_height = 4
        x = coords[0]
        y = coords[1]
        f_x = g_origin[0] + ((g_length / g_limits[0]) * x)
        f_y = g_origin[1] + ((g_height / g_limits[1]) * y)
        return [f_x, f_y, 0]

    def create_center_of_mass(self, tracked_func):
        c_o_m_group = VGroup()
        box_freq = 100  # amount of rectangles per unit length
        complex_loc = np.array([
            (tracked_func(x / box_freq) * np.exp(-TAU * (x / box_freq) * self.freq.get_value() * 1j) * (1 / box_freq))
            for x in range(round(self.length.get_value() * box_freq))
        ]).sum() / (self.length.get_value() / 2)
        real_location = [self.graph_origin[0] + complex_loc.real,
                         self.graph_origin[1] + complex_loc.imag,
                         0]
        c_o_m_group.add(Line(self.graph_origin, real_location, color="#BA0087"))
        c_o_m_group.add(Dot(color=RED).move_to(real_location))
        return c_o_m_group

    def create_transform_mover(self, func):
        final_group = VGroup()
        x = self.freq.get_value()
        y = func(x)
        axis_point = self.coords_to_transfrom_graph((x, 0))
        transform_value = self.coords_to_transfrom_graph((x, y))
        line = Line(axis_point, transform_value, color="#BA0087")
        dot = Dot(transform_value, color=RED)
        final_group.add(line)
        final_group.add(dot)
        return final_group

    def create_scene_label(self):
        self.play(
            Write(
                Rectangle(
                    width=3.8,
                    height=3,
                    fill_opacity=0.25, fill_color=GREY, stroke_opacity=0
                ).move_to([5, 2, 0])),
            Write(
                VGroup(
                    TextMobject("Fourier").scale(1.5),
                    TextMobject("Transform").scale(1.5)
                ).arrange(DOWN).move_to([5, 2, 0])
            )
        )

    def setup_attributes(self):
        # obj attributes
        self.freq = ValueTracker(1 / 16)
        self.length = ValueTracker(2)


class NoiseFilter(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 4,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 14,
        "x_tick_frequency": 0.4,
        "y_min": -0.25,
        "y_max": 2.0,
        "y_axis_height": 3.8,
        "y_axis_label": None,  # "$y$",
        "y_tick_frequency": 1,
        "y_bottom_tick": 0,
        "graph_origin": np.array([-7, 0.5222, 0]),
        "function_color": WHITE,
        "axes_color": GREY
    }

    def construct(self):
        self.introduce_denoising()

        self.make_static_wave()

        noise_amt = 0.5

        #  Top Graph WAVE1
        wave_root_func = make_wave([(2, 0.8, 0)])
        noisy_func = add_noise(wave_root_func, noise_amt)

        self.setup_axes()
        # Top Graph Wave2
        wave_root_func_2 = make_wave([(2.2, 0.3, 0), (2.75, 0.3, 0), (3.3, 0.3, 0)])
        noisy_func_2 = add_noise(wave_root_func_2, noise_amt)

        wave2 = self.get_graph(wave_root_func_2, color=BLUE)
        noisy_wave2 = self.get_graph(noisy_func_2, color=BLUE)

        # BG pitch wave3
        wave_root_func_3 = make_wave([(2.2, 0.3, 0), (2.75, 0.3, 0), (3.3, 0.3, 0)])
        wave_bg_pitch_func = make_wave([(2.2, 0.3, 0), (2.75, 0.3, 0), (3.3, 0.3, 0), (4.85, 0.4, PI)], 0.8)

        wave3 = self.get_graph(wave_root_func_3, color=BLUE)
        bg_pitch_wave = self.get_graph(wave_bg_pitch_func, color=BLUE)

        # New Axes Params
        self.graph_origin = np.array([-7, -3.4777, 0])
        self.x_min = 0
        self.x_max = 5
        self.y_min = -0.125 / 2
        self.y_max = 0.5
        self.y_tick_frequency = 0.5 / 2
        self.x_tick_frequency = 1
        self.setup_axes()

        # Each of the Fourier Transform Graphs
        trans2 = self.get_graph(transform_wave(wave_root_func_2, [-100, 100], 2000, 1 / 100, 0.1),
                                step_size=0.001,
                                color=GREEN
                                )
        noisy_trans2 = self.get_graph(transform_wave(noisy_func_2, [-100, 100], 2000, 1 / 100, 0.1),
                                      step_size=0.001,
                                      color=GREEN
                                      )
        trans3 = self.get_graph(transform_wave(wave_root_func_3, [-100, 100], 2000, 1 / 100, 0.1),
                                step_size=0.001,
                                color=GREEN
                                )
        bg_pitch_trans3 = self.get_graph(
            transform_wave(wave_bg_pitch_func, [-100, 100], 2000, 1 / 100, 0.1),
            step_size=0.001,
            color=GREEN
        )

        mover_graph = noisy_wave2.copy()  # Container to morph into each of the graphs
        self.play(Write(mover_graph))
        all_waves = [
            noisy_wave2, noisy_trans2,
            trans2, wave2,
            trans3
        ]
        wait_map = [
            10, 20, 5, 5, 5, 5
        ]
        for wait_index, wave in enumerate(all_waves):
            self.play(
                Transform(mover_graph, wave)
            )
            self.wait(wait_map[wait_index])

        self.play(ReplacementTransform(trans3.copy(), wave3))
        self.wait(20)

    def introduce_denoising(self):
        intro_group = VGroup(
            ParametricFunction(
                self.introduction_function,
                t_min=-5,
                t_max=5,
                color=WHITE,
                stroke_width=2
            ).scale(1.25).set_sheen(-3, LEFT),
            TextMobject("Fourier").scale(3).move_to([0, 2, 0]).set_sheen(-0.75, LEFT),
            TextMobject("Noise Filtering").scale(2).move_to([0, -2, 0]).set_sheen(-0.75, LEFT)
        )
        self.play(
            Write(intro_group[0], run_time=2),
            Write(intro_group[1:])
        )
        self.wait(20)
        self.play(*[FadeOut(x) for x in self.mobjects])

    def make_static_wave(self):
        wave_func = add_noise(make_wave([(2.2, 0.3, 0), (2.75, 0.3, 0), (3.3, 0.3, 0)]), 0.5)
        wave_para_func = lambda t: np.array((t, wave_func(t), 0))
        intro_group = ParametricFunction(
            wave_para_func,
            t_min=-50,
            t_max=50,
            color=WHITE,
            stroke_width=1
        ).scale(2).move_to([0, 0, 0])
        intro_group.move_to([-intro_group.get_left()[0] + 8, 0, 0])
        self.add(intro_group)
        self.play(intro_group.shift, [-intro_group.get_width() - 16, 0, 0], run_time=5)
        self.remove(intro_group)

    def introduction_function(self, t):
        return np.array((
            t,  # The X-Value...pretty simple
            math.sin(t * 4 * PI) *  # Sine component
            (t * t * 0.1) +  # The Weird funnel shape
            ((random.random() - 0.5) * (t * t * 0.1) * (0 if t > 0 else 1)),
            0
        ))


class NoiseFilterSummary(GraphScene):
    CONFIG = {
        "play_speed": 1,

        "x_min": 0,
        "x_max": 4,
        "x_axis_label": None,  # "$\\theta$",
        "x_axis_width": 14.2/3.5,
        "x_tick_frequency": 0.4,
        "y_min": -0.25,
        "y_max": 2.0,
        "y_axis_height": 8/3.5,
        "y_axis_label": None,  # "$y$",
        "y_tick_frequency": 1,
        "y_bottom_tick": 0,
        "graph_origin": np.array([-5.578571049, 1.1, 0]),
        "function_color": WHITE,
        "axes_color": GREY,
    }

    def construct(self):
        clean_func = make_wave([(2.2, 0.3, 0), (2.75, 0.3, 0), (3.3, 0.3, 0)])
        clean_trans_func = transform_wave(clean_func, [-100, 100], 2000, 1 / 100, 0.1)
        noisy_func = add_noise(clean_func, 0.5)
        noisy_trans_func = transform_wave(noisy_func, [-100, 100], 2000, 1 / 100, 0.1)

        #noisy_trans = self.get_graph(transform_wave(noisy_func, [-100, 100], 2000, 1 / 100, 0.1),
                                     # step_size=0.001,
                                     # color=GREEN
                                     # )

        # Simple Title
        title = VGroup(
            TextMobject("Noise Filtration").scale(1.5).set_x(-3.55),
            TextMobject("Summary").scale(1.5).set_x(3.55)
        )

        # Create 4 boxes that will frame each of graph of each step
        boxes = VGroup()
        for num in range(4):
            boxes.add(
                Rectangle(width=14.2 / 3, height=8 / 3).move_to([
                    -3.55 + (7.1 * (num % 2)),
                    2 - (4 * (1 if num > 1 else 0)),
                    0
                ])
            )

        # Create arrows that move from box to box
        arrow_points = [
            boxes[0].get_right(),
            boxes[1].get_left(),
            boxes[2].get_right(),
            boxes[3].get_left()
        ]
        arrows = VGroup()
        for num in range(3):
            arrows.add(
                Arrow(arrow_points[num], arrow_points[num + 1])
            )
        for word in title:
            self.play(Write(word))

        ########################################################
        #  GRAPH 1
        ########################################################
        self.play(Write(boxes[0]))
        self.setup_axes()
        graph1 = self.get_graph(noisy_func, color=BLUE, stroke_width=1)
        self.play(Write(graph1))
        self.play(Write(arrows[0]))

        ########################################################
        #  GRAPH 2
        ########################################################
        self.y_min = -0.25 / 3
        self.y_max = 2 / 3
        self.graph_origin = np.array((1.521428951, 1.1, 0))
        self.play(Write(boxes[1]))
        self.setup_axes()
        graph2 = self.get_graph(noisy_trans_func, step_size=0.001, color=GREEN, stroke_width=1)
        self.play(ReplacementTransform(graph1.copy(), graph2))
        self.play(Write(arrows[1]))

        ########################################################
        #  GRAPH 3
        ########################################################
        self.y_min = -0.25 / 3
        self.y_max = 2 / 3
        self.graph_origin = np.array((-5.578571049, -2.9, 0))
        self.play(Write(boxes[2]))
        self.setup_axes()
        graph3 = self.get_graph(clean_trans_func, step_size=0.001, color=GREEN, stroke_width=1)
        self.play(ReplacementTransform(graph2.copy(), graph3))
        self.play(Write(arrows[2]))

        ########################################################
        #  GRAPH 4
        ########################################################
        self.y_min = -0.25
        self.y_max = 2.0
        self.graph_origin = np.array((1.521428951, -2.9, 0))
        self.play(Write(boxes[3]))
        self.setup_axes()
        graph4 = self.get_graph(clean_func, step_size=0.001, color=BLUE, stroke_width=1)
        self.play(ReplacementTransform(graph3.copy(), graph4))

        self.wait(20)


class MoreApplications(Scene):
    def construct(self):
        header = VGroup(
            TextMobject("Applications").scale(2),
            Line(LEFT * 4, RIGHT * 4)
        ).arrange(DOWN).to_edge(UP)
        applications = VGroup(
            *[TextMobject(app_name)
              for app_name in [
                  "Audio Devices",
                  "Voice Recognition",
                  "Audio Compression",
                  "Telecommunications",
                  "Optics",
                  "Approximation Theory",
                  "Video Compression",
                  "Polynomial Multiplication"
              ]]
        ).arrange(DOWN).next_to(header, DOWN)
        self.play(Write(header))
        self.wait()
        self.play(Write(applications, run_time=2))
        self.wait(28)
        self.play(*[FadeOut(x) for x in self.mobjects])
