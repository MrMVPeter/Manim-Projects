from manimlib.imports import *


#     _    _         _                  _
#    / \  | |__  ___| |_ _ __ __ _  ___| |_
#   / _ \ | '_ \/ __| __| '__/ _` |/ __| __|
#  / ___ \| |_) \__ \ |_| | | (_| | (__| |_
# /_/   \_\_.__/|___/\__|_|  \__,_|\___|\__|
#  ____
# / ___|  ___ ___ _ __   ___  ___
# \___ \ / __/ _ \ '_ \ / _ \/ __|
#  ___) | (_|  __/ | | |  __/\__ \
# |____/ \___\___|_| |_|\___||___/
########################################################################################


class FourierCirclesScene(ZoomedScene):
    CONFIG = {
        "n_vectors": 10,
        "big_radius": 2,
        "final_scale": 1,
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "circle_config": {
            "stroke_width": 1,
        },
        "base_frequency": 1,
        "slow_factor": 0.5,
        "center_point": ORIGIN,
        "parametric_function_step_size": 0.001,
        "drawn_path_color": YELLOW,
        "drawn_path_stroke_width": 2,
        "interpolate_config": [0, 1],
        # Zoom config
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 4,
        "zoom_factor": 0.3,
        "zoomed_display_height": 3,
        "zoomed_display_width": 4,
        "image_frame_stroke_width": 1,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
        },
        "zoom_position": lambda mob: mob.move_to(ORIGIN),
        "zoom_camera_to_full_screen_config": {
            "run_time": 3,
            "func": there_and_back_with_pause,
            "velocity_factor": 1
        },
        "wait_before_start": None
    }

    def setup(self):
        ZoomedScene.setup(self)
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)

    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]

    def get_color_iterator(self):
        return it.cycle(self.colors)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            vectors.add(vector)
            last_vector = vector
        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT, **self.vector_config)
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coefficient = vector.coefficient
        freq = vector.freq
        phase = np.log(coefficient).imag

        vector.set_length(abs(coefficient))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])

    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()

        path = ParametricFunction(
            lambda t: center + reduce(op.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ]),
            t_min=0,
            t_max=1,
            color=color,
            step_size=self.parametric_function_step_size,
        )
        return path

    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config

        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path

    def get_y_component_wave(self,
                             vectors,
                             left_x=1,
                             color=PINK,
                             n_copies=2,
                             right_shift_rate=5):
        path = self.get_vector_sum_path(vectors)
        wave = ParametricFunction(
            lambda t: op.add(
                right_shift_rate * t * LEFT,
                path.function(t)[1] * UP
            ),
            t_min=path.t_min,
            t_max=path.t_max,
            color=color,
        )
        wave_copies = VGroup(*[
            wave.copy()
            for x in range(n_copies)
        ])
        wave_copies.arrange(RIGHT, buff=0)
        top_point = wave_copies.get_top()
        wave.creation = ShowCreation(
            wave,
            run_time=(1 / self.get_slow_factor()),
            rate_func=linear,
        )
        cycle_animation(wave.creation)
        wave.add_updater(lambda m: m.shift(
            (m.get_left()[0] - left_x) * LEFT
        ))

        def update_wave_copies(wcs):
            index = int(
                wave.creation.total_time * self.get_slow_factor()
            )
            wcs[:index].match_style(wave)
            wcs[index:].set_stroke(width=0)
            wcs.next_to(wave, RIGHT, buff=0)
            wcs.align_to(top_point, UP)

        wave_copies.add_updater(update_wave_copies)

        return VGroup(wave, wave_copies)

    def get_wave_y_line(self, vectors, wave):
        return DashedLine(
            vectors[-1].get_end(),
            wave[0].get_end(),
            stroke_width=1,
            dash_length=DEFAULT_DASH_LENGTH * 0.5,
        )

    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt * self.final_scale for freq in freqs
        ]

    def zoom_config(self):
        # This is not in the original version of the code.
        self.activate_zooming(animate=False)
        self.zoom_position(self.zoomed_display)
        self.zoomed_camera.frame.add_updater(lambda mob: mob.move_to(self.vectors[-1].get_end()))

    def scale_zoom_camera_to_full_screen_config(self):
        # This is not in the original version of the code.
        def fix_update(mob, dt, velocity_factor, dt_calculate):
            if dt == 0 and mob.counter == 0:
                rate = velocity_factor * dt_calculate
                mob.counter += 1
            else:
                rate = dt * velocity_factor
            if dt > 0:
                mob.counter = 0
            return rate

        fps = 1 / self.camera.frame_rate
        mob = self.zoomed_display
        mob.counter = 0
        velocity_factor = self.zoom_camera_to_full_screen_config["velocity_factor"]
        mob.start_time = 0
        run_time = self.zoom_camera_to_full_screen_config["run_time"]
        run_time *= 2
        mob_height = mob.get_height()
        mob_width = mob.get_width()
        mob_center = mob.get_center()
        ctx = self.zoomed_camera.cairo_line_width_multiple

        def update_camera(mob, dt):
            line = Line(
                mob_center,
                self.camera_frame.get_center()
            )
            mob.start_time += fix_update(mob, dt, velocity_factor, fps)
            if mob.start_time <= run_time:
                alpha = mob.start_time / run_time
                alpha_func = self.zoom_camera_to_full_screen_config["func"](alpha)
                coord = line.point_from_proportion(alpha_func)
                mob.set_height(
                    interpolate(
                        mob_height,
                        self.camera_frame.get_height(),
                        alpha_func
                    ),
                    stretch=True
                )
                mob.set_width(
                    interpolate(
                        mob_width,
                        self.camera_frame.get_width(),
                        alpha_func
                    ),
                    stretch=True
                )
                self.zoomed_camera.cairo_line_width_multiple = interpolate(
                    ctx,
                    self.camera.cairo_line_width_multiple,
                    alpha_func
                )
                mob.move_to(coord)
            return mob

        self.zoomed_display.add_updater(update_camera)


class AbstractFourierOfTexSymbol(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 50,
        "center_point": ORIGIN,
        "slow_factor": 0.05,
        "n_cycles": None,
        "run_time": 10,
        "tex": r"\rm M",
        "start_drawn": True,
        "path_custom_position": lambda mob: mob,
        "max_circle_stroke_width": 1,
        "tex_class": TexMobject,
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": WHITE
        },
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 1,
        "zoom_position": lambda mob: mob.scale(0.8).move_to(ORIGIN).to_edge(RIGHT)
    }

    def construct(self):
        # This is not in the original version of the code.
        self.add_vectors_circles_path()
        if self.wait_before_start != None:
            self.wait(self.wait_before_start)
        self.add_vector_clock()
        self.add(self.vector_clock)
        if self.include_zoom_camera:
            self.zoom_config()
        if self.scale_zoom_camera_to_full_screen:
            self.run_time -= self.scale_zoom_camera_to_full_screen_at
            self.wait(self.scale_zoom_camera_to_full_screen_at)
            self.scale_zoom_camera_to_full_screen_config()
        if self.n_cycles != None:
            if not self.scale_zoom_camera_to_full_screen:
                for n in range(self.n_cycles):
                    self.run_one_cycle()
            else:
                cycle = 1 / self.slow_factor
                total_time = cycle * self.n_cycles
                total_time -= self.scale_zoom_camera_to_full_screen_at
                self.wait(total_time)
        elif self.run_time != None:
            self.wait(self.run_time)

    def add_vectors_circles_path(self):
        path = self.get_path()
        self.path_custom_position(path)
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)
        if self.start_drawn:
            self.vector_clock.increment_value(1)
        self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_path(self):
        tex_mob = self.tex_class(self.tex, **self.tex_config)
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        return path


class AbstractFourierFromSVG(AbstractFourierOfTexSymbol):
    CONFIG = {
        "n_vectors": 101,
        "run_time": 10,
        "start_drawn": True,
        "file_name": None,
        "svg_config": {
            "fill_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        }
    }

    def get_shape(self):
        shape = SVGMobject(self.file_name, **self.svg_config)
        return shape

    def get_path(self):
        shape = self.get_shape()
        path = shape.family_members_with_points()[0]
        return path


class FourierOfPaths(AbstractFourierOfTexSymbol):
    CONFIG = {
        "n_vectors": None,
        "name_color": WHITE,
        "tex_class": TexMobject,
        "tex": None,
        "file_name": None,
        "tex_config": {
            "stroke_color": WHITE,
            "fill_opacity": 0,
            "stroke_width": 3,
        },
        "svg_config": {},
        "time_per_symbol": 5,
        "slow_factor": 1 / 5,
        "parametric_function_step_size": 0.0004,
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
    }

    def construct(self):
        self.add_vector_clock()
        if self.tex != None:
            name = self.tex_class(self.tex, **self.tex_config)
        elif self.file_name != None and self.tex == None:
            name = SVGMobject(self.file_name, **self.svg_config)
        max_width = FRAME_WIDTH - 2
        max_height = FRAME_HEIGHT - 2
        name.set_width(max_width)
        if name.get_height() > max_height:
            name.set_height(max_height)

        frame = self.camera.frame
        frame.save_state()

        vectors = VGroup(VectorizedPoint())
        circles = VGroup(VectorizedPoint())
        for path in name.family_members_with_points():
            for subpath in path.get_subpaths():
                sp_mob = VMobject()
                sp_mob.set_points(subpath)
                coefs = self.get_coefficients_of_path(sp_mob)
                new_vectors = self.get_rotating_vectors(
                    coefficients=coefs
                )
                new_circles = self.get_circles(new_vectors)
                self.set_decreasing_stroke_widths(new_circles)

                drawn_path = self.get_drawn_path(new_vectors)
                drawn_path.clear_updaters()
                drawn_path.set_style(**self.tex_config)
                drawn_path.set_style(**self.svg_config)

                static_vectors = VMobject().become(new_vectors)
                static_circles = VMobject().become(new_circles)

                self.play(
                    Transform(vectors, static_vectors, remover=True),
                    Transform(circles, static_circles, remover=True),
                    frame.set_height, 1.5 * name.get_height(),
                    frame.move_to, path,
                )

                self.add(new_vectors, new_circles)
                self.vector_clock.set_value(0)
                self.play(
                    ShowCreation(drawn_path),
                    rate_func=linear,
                    run_time=self.time_per_symbol
                )
                self.remove(new_vectors, new_circles)
                self.add(static_vectors, static_circles)

                vectors = static_vectors
                circles = static_circles
        self.play(
            FadeOut(vectors),
            FadeOut(circles),
            Restore(frame),
            run_time=2
        )
        self.wait(3)


########################################################################################
########################################################################################
########################################################################################

#  ____  _                 _        _____                _
# / ___|(_)_ __ ___  _ __ | | ___  |  ___|__  _   _ _ __(_) ___ _ __
# \___ \| | '_ ` _ \| '_ \| |/ _ \ | |_ / _ \| | | | '__| |/ _ \ '__|
#  ___) | | | | | | | |_) | |  __/ |  _| (_) | |_| | |  | |  __/ |
# |____/|_|_| |_| |_| .__/|_|\___| |_|  \___/ \__,_|_|  |_|\___|_|
#                   |_|
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Using TexMobject or TextMobject
class FourierOfTexSymbol(AbstractFourierOfTexSymbol):
    CONFIG = {
        # if start_draw = True the path start to draw
        "start_drawn": True,
        # Tex config
        "tex_class": TexMobject,
        "tex": r"\pi",
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_opacity": 0,
            "stroke_color": WHITE
        },
        # Draw config
        "drawn_path_color": YELLOW,
        "interpolate_config": [0.15, 1],
        "n_vectors": 200,
        "big_radius": 2,
        "drawn_path_stroke_width": 2,
        "center_point": ORIGIN,
        # Duration config
        "slow_factor": 0.1,
        "n_cycles": None,
        "run_time": 10,
        # colors of circles
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        # circles config
        "circle_config": {
            "stroke_width": 1,
        },
        # vector config
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "base_frequency": 1,
        # definition of subpaths
        "parametric_function_step_size": 0.001,
    }


# o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x o x
# SVG
class FourierFromSVG(AbstractFourierFromSVG):
    CONFIG = {
        # if start_draw = True the path start to draw
        "start_drawn": False,
        # SVG file name
        "file_name": None,
        "svg_config": {
            "fill_opacity": 0,
            "stroke_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        },
        # Draw config
        "drawn_path_color": '#FFF200',
        "interpolate_config": [0.2, 1],
        "n_vectors": 50,
        "big_radius": 2,
        "drawn_path_stroke_width": 2,
        "center_point": ORIGIN,
        # Duration config
        "slow_factor": 0.1,
        "n_cycles": None,
        "run_time": 10,
        # colors of circles
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        # circles config
        "circle_config": {
            "stroke_width": 1,
        },
        # vector config
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "base_frequency": 1,
        # definition of subpaths
        "parametric_function_step_size": 0.001,
    }


# file_name
class SVGDefault(FourierFromSVG):
    CONFIG = {
        "n_vectors": 150,
        "n_cycles": 2,
        # in assets/svg_images/c_clef.svg
        "file_name": "person"
    }


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# __        ___ _   _      
# \ \      / (_) |_| |__   
#  \ \ /\ / /| | __| '_ \  
#   \ V  V / | | |_| | | | 
#    \_/\_/  |_|\__|_| |_| 
#  _____                              _                                      
# |__  /___   ___  _ __ ___   ___  __| |   ___ __ _ _ __ ___   ___ _ __ __ _ 
#   / // _ \ / _ \| '_ ` _ \ / _ \/ _` |  / __/ _` | '_ ` _ \ / _ \ '__/ _` |
#  / /| (_) | (_) | | | | | |  __/ (_| | | (_| (_| | | | | | |  __/ | | (_| |
# /____\___/ \___/|_| |_| |_|\___|\__,_|  \___\__,_|_| |_| |_|\___|_|  \__,_|
# ---------------------------------------------------------------------------------------
# The following works in both Tex and SVG
# ---------------------------------------
#      ---------------------------
#          ----------------

# How activate it
class ZoomedActivate(FourierFromSVG):
    CONFIG = {
        "slow_factor": 0.05,
        "n_vectors": 50,
        "n_cycles": 1,
        "file_name": "c_clef",
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_corner(DR)
    }


# Zoomed camera: Moving camera
# Zoomed display: Static camera
# More info: https://github.com/Elteoremadebeethoven/AnimationsWithManim/blob/master/English/extra/faqs/faqs.md#zoomed-scene-example
class ZoomedConfig(FourierFromSVG):
    CONFIG = {
        "slow_factor": 0.05,
        "n_vectors": 150,
        "n_cycles": 1,
        "file_name": "ghost_s",
        "path_custom_position": lambda path: path.shift(LEFT * 2),
        "center_point": LEFT * 2,
        "circle_config": {
            "stroke_width": 0.5,
            "stroke_opacity": 0.2,
        },
        # Zoom config
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_edge(RIGHT).set_y(0),
        "zoom_factor": 0.2,
        "zoomed_display_height": 4,
        "zoomed_display_width": 5,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
            # What is cairo_line_width_multiple?
            # See here: https://stackoverflow.com/questions/60765530/manim-zoom-not-preserving-line-thickness
        },
    }


# Move Zoomed display to full screen
class ZoomedDisplayToFullScreen(FourierOfTexSymbol):
    CONFIG = {
        "slow_factor": 0.05,
        "n_vectors": 30,
        "run_time": 16,
        "tex": "\\tau",
        # Zoom config
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_corner(DR),
        # Zoomed display to Full screen config
        "scale_zoom_camera_to_full_screen": True,
        "scale_zoom_camera_to_full_screen_at": 4,  # Move the camera at 4 seconds
        "zoom_camera_to_full_screen_config": {
            "run_time": 3,
            "func": smooth,
            "velocity_factor": 1
        },
    }


# Move Zoomed display to full screen
class ZoomedDisplayToFullScreenSVG(FourierFromSVG):
    CONFIG = {
        "slow_factor": 0.1,
        "n_vectors": 50,
        "run_time": 16,
        "file_name": "person",
        "drawn_path_color": "#FFF200",
        # Zoom config
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_corner(DR),
        # Zoomed display to Full screen config
        "scale_zoom_camera_to_full_screen": True,
        "scale_zoom_camera_to_full_screen_at": 4,  # Move the camera at 4 seconds
        "zoom_camera_to_full_screen_config": {
            "run_time": 3,
            "func": smooth,
            "velocity_factor": 1
        },
    }


class ZoomedDisplayToFullScreenWithRestoreSVG(ZoomedDisplayToFullScreenSVG):
    CONFIG = {
        "run_time": 30,
        "svg_config": {
            "fill_opacity": 0,
            "stroke_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        },
        "zoom_factor": 0.1,
        "drawn_path_stroke_width": 4,
        "zoom_camera_to_full_screen_config": {
            "run_time": 12,
            "func": lambda t: there_and_back_with_pause(t, 1 / 10),
            # learn more: manimlib/utils/rate_functions.py
        },
    }


class ZoomedDisplayToFullScreenWithRestore(ZoomedDisplayToFullScreen):
    CONFIG = {
        "run_time": 20,
        "zoom_camera_to_full_screen_config": {
            "run_time": 12,
            "func": lambda t: there_and_back_with_pause(t, 1 / 10),
            # learn more: manimlib/utils/rate_functions.py
        },
    }


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

#  ____                                   _   _
# |  _ \ _ __ __ ___      __  _ __   __ _| |_| |__
# | | | | '__/ _` \ \ /\ / / | '_ \ / _` | __| '_ \
# | |_| | | | (_| |\ V  V /  | |_) | (_| | |_| | | |
# |____/|_|  \__,_| \_/\_/   | .__/ \__,_|\__|_| |_|
#                            |_|

# //////////////////////////////////////////////////////////////////////////////////////////

class FourierOfPathsTB(FourierOfPaths):
    CONFIG = {
        "n_vectors": 100,
        "tex_class": TextMobject,
        "tex": "Peter Gilliam",
        "tex_config": {
            "stroke_color": RED,
        },
        "time_per_symbol": 5,
        "slow_factor": 1 / 5,
    }


# Convert objects to paths
# Inkscape example: [ToolBar] Path > Object to path
class FourierOfPathsSVG(FourierOfPaths):
    CONFIG = {
        "n_vectors": 400,
        "file_name": "ukt",
        "svg_config": {
            "stroke_color": "#39FF14",
        },
        "time_per_symbol": 20,
        "slow_factor": 1 / 20,
    }


# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# The Coded the following mostly foe the purposes of my YouTube video on fourier series

class CustomAnimation(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 200,
        "slow_factor": 0.2,
        "fourier_symbol_config": {
            "stroke_width": 0,
            "fill_opacity": 0,
            "height": 4,
            "fill_color": RED
        },
        "circle_config": {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
        },
    }

    def construct(self):
        # Objects
        t_symbol = TextMobject("T", **self.fourier_symbol_config)
        c_clef_symbol = SVGMobject("c_clef", **self.fourier_symbol_config)
        c_clef_symbol.match_height(t_symbol)
        # set gradient
        for mob in [t_symbol, c_clef_symbol]:
            mob.set_sheen(0, UP)
            mob.set_color(color=[BLACK, GRAY, WHITE])
        group = VGroup(t_symbol, c_clef_symbol).arrange(RIGHT, buff=0.1)
        # set paths
        path1 = t_symbol.family_members_with_points()[0]
        path2 = c_clef_symbol.family_members_with_points()[0]
        # path 1 config
        coefs1 = self.get_coefficients_of_path(path1)
        vectors1 = self.get_rotating_vectors(coefficients=coefs1)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1)
        # path 2 config
        coefs2 = self.get_coefficients_of_path(path2)
        vectors2 = self.get_rotating_vectors(coefficients=coefs2)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2)
        # text definition
        text = TextMobject("Thanks for watch!")
        text.scale(1.5)
        text.next_to(group, DOWN)
        # all elements toget
        all_mobs = VGroup(group, text)
        # set mobs to remove
        vectors1_to_fade = vectors1.copy()
        circles1_to_fade = circles1.copy()
        vectors1_to_fade.clear_updaters()
        circles1_to_fade.clear_updaters()
        vectors2_to_fade = vectors2.copy()
        circles2_to_fade = circles2.copy()
        vectors2_to_fade.clear_updaters()
        circles2_to_fade.clear_updaters()

        self.play(
            *[
                GrowArrow(arrow)
                for vg in [vectors1_to_fade, vectors2_to_fade]
                for arrow in vg
            ],
            *[
                ShowCreation(circle)
                for cg in [circles1_to_fade, circles2_to_fade]
                for circle in cg
            ],
            run_time=2.5,
        )
        self.remove(
            *vectors1_to_fade,
            *circles1_to_fade,
            *vectors2_to_fade,
            *circles2_to_fade,
        )
        self.add(
            vectors1,
            circles1,
            drawn_path1.set_color(RED),
            vectors2,
            circles2,
            drawn_path2.set_color(BLUE),
        )
        self.add_vector_clock()

        # wait one cycle
        self.wait(1 / self.slow_factor)
        self.bring_to_back(t_symbol, c_clef_symbol)
        self.play(
            t_symbol.set_fill, None, 1,
            c_clef_symbol.set_fill, None, 1,
            run_time=3
        )
        self.wait()
        # move camera
        self.play(
            self.camera_frame.set_height, all_mobs.get_height() * 1.2,
            self.camera_frame.move_to, all_mobs.get_center()
        )
        self.wait(0.5)
        self.play(
            Write(text)
        )
        self.wait(10)


class Intro(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 250,
        "slow_factor": 0.2,
        "fourier_symbol_config": {
            "stroke_width": 0,
            "fill_opacity": 0,
            "height": 4,
            "fill_color": WHITE
        },
        "circle_config": {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
        },
    }

    def construct(self):
        # Objects
        fourier_objects = [
            TextMobject("P", **self.fourier_symbol_config),
            TextMobject("E", **self.fourier_symbol_config),
            TextMobject("T", **self.fourier_symbol_config),
            TextMobject("E", **self.fourier_symbol_config),
            TextMobject("R", **self.fourier_symbol_config),
            TextMobject("G", **self.fourier_symbol_config),
            TextMobject("I", **self.fourier_symbol_config),
            TextMobject("l", **self.fourier_symbol_config),
            TextMobject("l", **self.fourier_symbol_config),
            TextMobject("I", **self.fourier_symbol_config),
            TextMobject("A", **self.fourier_symbol_config),
            TextMobject("M", **self.fourier_symbol_config)
        ]
        for x in fourier_objects:
            x.set_sheen(0, DOWN)
            x.set_fill(color=['#AA0000', '#200000'])
        group_FN = VGroup(*fourier_objects[:5]).arrange(RIGHT, buff=0.13)
        group_LN = VGroup(*fourier_objects[5:]).arrange(RIGHT, buff=0.13)
        group = VGroup(group_FN, group_LN).arrange(RIGHT, buff=1.5).scale(0.32)
        # set paths
        paths = []
        coefs = []
        vectors = []
        circles = []
        drawn_paths = []

        # fill lists
        for x in fourier_objects:
            paths.append(x.family_members_with_points()[0])
        for x in paths:
            coefs.append(self.get_coefficients_of_path(x))
        for x in coefs:
            vectors.append(self.get_rotating_vectors(coefficients=x))
        for x in vectors:
            circles.append(self.get_circles(x))
            drawn_paths.append(self.get_drawn_path(x))

        # Vectors to fade
        vectors_to_fade = []
        circles_to_fade = []
        for x in vectors:
            vectors_to_fade.append(x.copy())
        for x in vectors_to_fade:
            x.clear_updaters()
        for x in circles:
            circles_to_fade.append(x.copy())
        for x in circles_to_fade:
            x.clear_updaters()

        all_mobs = VGroup(*fourier_objects)
        self.play(
            *[
                GrowArrow(arrow)
                for vg in vectors_to_fade
                for arrow in vg[1:]
            ],
            *[
                ShowCreation(circle)
                for cg in circles_to_fade
                for circle in cg[1:]
            ],
            run_time=2.5,
        )
        self.remove(
            *[arrow
              for vg in vectors_to_fade
              for arrow in vg[1:]],
            *[circle
              for cg in circles_to_fade
              for circle in cg[1:]],
        )
        self.add(
            *[vect
              for vects in vectors
              for vect in vects[1:]],
            *[circ
              for circs in circles
              for circ in circs[1:]],
            *[drawn_paths[x].set_color(RED)
              for x in range(len(fourier_objects))]
        )

        self.add_vector_clock()

        # wait one cycle
        self.wait(1 / self.slow_factor)

        self.bring_to_back(*fourier_objects)
        self.bring_to_back(*[*fourier_objects])

        # Could generalize this part, all parts must be stated
        self.play(fourier_objects[0].set_fill, None, 1,
                  fourier_objects[1].set_fill, None, 1,
                  fourier_objects[2].set_fill, None, 1,
                  fourier_objects[3].set_fill, None, 1,
                  fourier_objects[4].set_fill, None, 1,
                  fourier_objects[5].set_fill, None, 1,
                  fourier_objects[6].set_fill, None, 1,
                  fourier_objects[7].set_fill, None, 1,
                  fourier_objects[8].set_fill, None, 1,
                  fourier_objects[9].set_fill, None, 1,
                  fourier_objects[10].set_fill, None, 1,
                  fourier_objects[11].set_fill, None, 1,
                  )

        self.wait()
        final_dot = Dot(color=GREY).next_to(group, DOWN)
        final_line = Line([-6, 0, 0], [6, 0, 0]).align_to(final_dot, DOWN)
        final_text = TextMobject("Fourier Series", color='#666666'
                                 ).scale(0.75).next_to(final_line, DOWN)
        self.play(ShowCreation(final_dot))
        self.play(ReplacementTransform(final_dot, final_line))
        self.play(Write(final_text))
        self.wait(10)


# For Charlette
class uk(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 200,
        "slow_factor": 0.1,
        "fourier_symbol_config": {
            "stroke_width": 0,
            "fill_opacity": 0,
            "height": 4,
            "fill_color": WHITE
        },
        "circle_config": {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
        },
    }

    def construct(self):
        # Objects
        fourier_objects = [SVGMobject("ukt1", **self.fourier_symbol_config),
                           SVGMobject("ukt2", **self.fourier_symbol_config)]
        # set paths
        paths = []
        coefs = []
        vectors = []
        circles = []
        drawn_paths = []

        # fill lists
        for x in fourier_objects:
            paths.append(x.family_members_with_points()[0])
        for x in paths:
            coefs.append(self.get_coefficients_of_path(x))
        for x in coefs:
            vectors.append(self.get_rotating_vectors(coefficients=x))
        for x in vectors:
            circles.append(self.get_circles(x))
            drawn_paths.append(self.get_drawn_path(x))

        # Vectors to fade
        vectors_to_fade = []
        circles_to_fade = []
        for x in vectors:
            vectors_to_fade.append(x.copy())
        for x in vectors_to_fade:
            x.clear_updaters()
        for x in circles:
            circles_to_fade.append(x.copy())
        for x in circles_to_fade:
            x.clear_updaters()

        self.play(
            *[
                GrowArrow(arrow)
                for vg in vectors_to_fade
                for arrow in vg
            ],
            *[
                ShowCreation(circle)
                for cg in circles_to_fade
                for circle in cg
            ],
            run_time=2.5,
        )
        self.remove(
            *[arrow
              for vg in vectors_to_fade
              for arrow in vg],
            *[circle
              for cg in circles_to_fade
              for circle in cg],
        )
        self.add(
            *[vect
              for vects in vectors
              for vect in vects],
            *[circ
              for circs in circles
              for circ in circs],
            *[drawn_paths[x].set_color(RED)
              for x in range(len(fourier_objects))]
        )

        self.add_vector_clock()

        # wait one cycle
        self.wait(1 / self.slow_factor)
        self.wait()


class ProgressParts(FourierCirclesScene):
    p_a = 1
    CONFIG = {
        # Main Configurations
        "final_scale": 0.75,
        "wait_before_start": None,
        "start_completion": 0,
        "portion_animated": p_a,
        "start_drawn": False,
        "slow_factor": 1 / 5,
        "n_vectors": 2,
        "num_it": 2,

        # SVG configs
        "svg_config": {
            "fill_opacity": 0,
            "stroke_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        },

        # Others
        "file_name": "ukt1",
        "path_custom_position": lambda path: path.shift(LEFT),
        "center_point": LEFT,
        "circle_config": {
            "stroke_width": 0.5,
            "stroke_opacity": 0.2,
        },
        "run_time": None,
        "max_circle_stroke_width": 1,
        # Zoom config
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_corner(DR),
        "zoom_factor": 0.5,
        "zoomed_display_height": 3,
        "zoomed_display_width": 4,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 2,
            "default_frame_stroke_opacity": 0.25,
            "cairo_line_width_multiple": 0.05,
            # What is cairo_line_width_multiple?
            # See here: https://stackoverflow.com/questions/60765530/manim-zoom-not-preserving-line-thickness
        },

    }

    def construct(self):
        # Zoom SetUp
        ZoomedScene.setup(self)
        # ADD VECTORS TO CIRCLES
        path = self.get_path()
        self.path_custom_position(path)
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)

        # Starting the Circles
        if self.start_drawn:
            self.vector_clock.increment_value(1)
        self.vector_clock.increment_value(self.start_completion)
        self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

        # Text
        self.add(TextMobject("N:{}".format(self.n_vectors)).scale(1.5).to_edge(UP))
        # Wait Before Drawing
        if self.wait_before_start != None:
            self.wait(self.wait_before_start)
        # Initialize Clock
        self.add_vector_clock()
        self.add(self.vector_clock)
        # Zoom Camera
        if self.include_zoom_camera:
            self.zoom_config()
        if self.scale_zoom_camera_to_full_screen:
            self.run_time -= self.scale_zoom_camera_to_full_screen_at
            self.wait(self.scale_zoom_camera_to_full_screen_at)
            self.scale_zoom_camera_to_full_screen_config()
        self.run_amount(self.slow_factor, self.portion_animated)

        # Loop #########################
        iterable_parameters = self.it_parameters()  # Iterable Parts
        for i in range(len(iterable_parameters[0])):  # SF:Slow Factor, PA: Portion to animate, NV: Num of Vects

            # Update Configs
            self.n_vectors = iterable_parameters[2][i]
            # self.start_completion = (self.start_completion + self.portion_animated) % 1
            self.portion_animated = iterable_parameters[1][i]
            self.slow_factor = iterable_parameters[0][i]

            # Remove Prev Fourier
            self.vector_clock.clear_updaters()
            self.remove(*[x
                          for x in self.mobjects])

            # Update Clock
            self.slow_factor_tracker = ValueTracker(self.slow_factor)
            self.add_vector_clock()
            self.add(self.vector_clock)

            # GET VECTORS
            path = self.get_path()
            self.path_custom_position(path)
            coefs = self.get_coefficients_of_path(path)
            vectors = self.get_rotating_vectors(coefficients=coefs)
            circles = self.get_circles(vectors)
            self.set_decreasing_stroke_widths(circles)
            drawn_path = self.get_drawn_path(vectors)
            # Starting the Circles
            if self.start_drawn:
                self.vector_clock.increment_value(1)
            self.vector_clock.increment_value(self.start_completion)
            self.add(path)
            self.add(vectors)
            self.add(circles)
            self.add(drawn_path)

            self.vectors = vectors
            self.circles = circles
            self.path = path
            self.drawn_path = drawn_path

            # Title
            self.add(TextMobject("N:{}".format(self.n_vectors)).scale(1.5).to_edge(UP))
            # Zoom Camera
            if self.include_zoom_camera:
                self.zoom_config()
            if self.scale_zoom_camera_to_full_screen:
                self.run_time -= self.scale_zoom_camera_to_full_screen_at
                self.wait(self.scale_zoom_camera_to_full_screen_at)
                self.scale_zoom_camera_to_full_screen_config()
            self.run_amount(self.slow_factor, self.portion_animated)

    def add_vectors_circles_path(self):
        path = self.get_path()
        self.path_custom_position(path)
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)
        # Starting the Circles
        if self.start_drawn:
            self.vector_clock.increment_value(1)
        self.vector_clock.increment_value(self.start_completion)
        self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

    def run_amount(self, slow_factor, P_A):
        time = (1 / slow_factor) * P_A
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_shape(self):
        shape = SVGMobject(self.file_name, **self.svg_config)
        return shape

    def get_path(self):
        shape = self.get_shape()
        path = shape.family_members_with_points()[0]
        return path

    def it_parameters(self):
        cycle_freq = [
            0.1 for _ in range(248)
        ]
        portion_animate = [
            0.5, 0.5, 0.4, 0.3, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02,
            *[0.01 for _ in range(50)],
            *[0.005 for _ in range(187)],
            2
        ]
        num_vects = [  # doesnt include first (num1)
            n for n in range(3, 251)
        ]
        return [cycle_freq, portion_animate, num_vects]

# x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
# x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
# x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
