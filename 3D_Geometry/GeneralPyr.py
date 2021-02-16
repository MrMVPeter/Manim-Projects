from manimlib.imports import *

colors = {
    'h': '#FFF200',  # Highlight
    'sl': '#666666',  # Grey Used for Small logo
    'rh': '#FF5555',  # Red Height
    'ph': '#6F2DA8',  # Purple Height
    'a': '#00A86B',  # Green A
    'b': '#89CFEF',  # Blue
    'v': '#FFBF00'  # Orange-ish V
}

waits = {
    'ss': 0.33,
    's': 0.45,
    'm': 1.5,
    'ml': 1.5,
    'l': 2
}


class TableOC(Scene):
    def construct(self):
        next_scene = 0  # Scene Index
        time_scale = 1

        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        # Main Title
        title = VGroup(
            TextMobject("Solution Layout", color=colors["h"]).scale(2.5),
            Line([-4, 0, 0], [4, 0, 0])
        ).arrange(DOWN).to_edge(UP)

        # Chapters
        contents = VGroup(
            TextMobject("1) Area of General Polygon").scale(1.5),
            TextMobject("2) Cross-Section at any ", "height").scale(1.5),
            TextMobject("3) Integration for ", "Volume").scale(1.5)
        ).arrange(DOWN, buff=1).next_to(title, DOWN, buff=1)
        contents[1][1].set_color(colors["rh"])
        contents[2][1].set_color(colors["v"])

        # Write Everything
        for x in [title, *contents]:
            self.play(Write(x, run_time=time_scale))
            self.wait(time_scale * 0.5)

        # Move current title to stage center
        self.wait(time_scale)
        self.play(contents[next_scene].move_to, [0, 0, 0],
                  contents[next_scene].scale, 1.2,
                  *[FadeOut(contents[(next_scene + 1 + x) % 3])  # Complicated way to fade out all non-NEXT_SCENES
                    for x in range(2)])
        self.wait()
        self.play(*[FadeOut(x, run_time=time_scale * 1.5)
                    for x in [title, contents[next_scene]]])


class Introduction(Scene):
    def construct(self):
        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        header = VGroup(
            TextMobject("Volume Of General Pyramid"),
            Line([-5, 0, 0], [5, 0, 0])
        ).arrange(DOWN).to_edge(UP)
        header[0].set_color(colors["h"]).scale(1.75)

        text1 = VGroup(
            TextMobject("In this video, I will generalize my solution for"),
            TextMobject("The ", "Volume", " of a ", "Tetrahedron", "."),
            TextMobject("For greater detail, watch that video")
        ).arrange(DOWN).next_to(header, DOWN)
        text1[1][1].set_color(colors["v"])
        text1[1][3].set_color(colors["h"])

        text2 = VGroup(
            TextMobject("More specifically, I'll be finding the ", "Volume"),
            TextMobject("for an pyramid for with a regular polygonal base"),
            TextMobject('of "', 'n', '" number of sides.')
        ).arrange(DOWN).next_to(header, DOWN)
        text2[0][1].set_color(colors["v"])
        text2[2][1].set_color(colors["b"])

        # box to insert image/video
        box_insert = VGroup(
            Line([0, 0, 0], [7.2, 0, 0]),
            Line([0, 0, 0], [0, -4, 0])
        )
        TextMobject(str(self.camera.get_frame_width()))

        # Write out everything
        for x in [header, *text1, box_insert]:
            self.play(Write(x))
        self.wait(3.5)

        # Second Text
        for x in range(3):
            self.play(FadeOutAndShiftDown(text1[x]),
                      Write(text2[x]))
        self.wait(3.5)

        # Fade Everything out
        self.play(*[FadeOut(x, run_time=3)
                    for x in [header, *text2, box_insert]])


class GeneralPoly(Scene):
    def construct(self):
        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        poly = self.introduce()

        poly = self.disect_poly(poly)

        self.part_area(poly)

    def introduce(self):
        polies = []
        for x in range(3, 11):
            polies.append(self.make_poly(x, 3, [0, -0.5, 0], x))
        mover_poly = polies[0].copy()
        self.play(Write(mover_poly[0]))
        for z in polies[1:]:
            self.play(Transform(mover_poly[0], z[0], run_time=0.5))
        final_poly = self.make_poly(6, 3, [0, -0.5, 0])
        self.play(ReplacementTransform(mover_poly[0], final_poly[0]))
        self.wait()
        return final_poly[0]

    def disect_poly(self, start_poly=TextMobject("NONE")):
        n_sides = 6

        poly = self.poly_parts(n_sides, 3, [0, -0.5, 0])[:2]
        self.add(poly[0])
        self.remove(start_poly)
        self.play(Write(poly[1]))
        self.play(poly.scale, 0.75,
                  poly.shift, [3.5, 0, 0])

        # Take Apart Polygon
        parts1 = poly[1].copy()
        parts2 = poly[1].copy()
        for row in range(3):
            for col in range(2):
                parts1[2 * row + col].rotate(((-2 * PI * (2 * row + col)) / n_sides) + (PI / 2))
                parts1[2 * row + col].move_to([-4 + 1.75 * col, 2 - 2 * row, 0])
                parts1[2 * row + col].scale(0.75)
                self.play(ReplacementTransform(poly[1][(2 * row + col)], parts1[(2 * row + col)]))
        self.wait()

        # Combine Triangles
        self.play(*[ReplacementTransform(parts1[x], parts1[3])
                    for x in [0, 1, 2, 4, 5]])

        # Texs for equation
        texs = VGroup(
            TexMobject("\\left(").next_to(parts1, LEFT).scale(4),
            TexMobject("\\right)").next_to(parts1, RIGHT).scale(4),
            TexMobject("n\\cdot").next_to(parts1, LEFT, buff=2).scale(4),
            TexMobject("=").next_to(parts1, RIGHT, buff=1.5).scale(3)
        )
        self.play(Write(texs))
        self.wait(2)

        # Restore Copies to frame
        self.play(*[ReplacementTransform(parts1[3].copy(), parts2[x], run_time=3)
                    for x in range(6)])
        self.wait()

        # FadeOut The Equations
        self.play(*[FadeOut(x)
                    for x in [*texs, *parts2, parts1[3]]])

        self.play(poly[0].scale, 1 / 0.75,
                  poly[0].shift, [-3.5, 0, 0])
        return poly[0]

    def part_area(self, start_poly=TextMobject("NONE")):
        poly = self.make_poly(6, 3, [0, -0.5, 0])  # Basically the mover polygon

        # Replace Hex with identical Hex for use in this function
        self.add(poly[0])
        self.remove(start_poly)
        self.play(Write(poly[1:]))

        # Show Generalization by showing multiple Polygons
        polies = []
        for x in range(3, 9):
            polies.append(self.make_poly(x, 3, [0, -0.5, 0]))
        for z in polies:
            self.play(Transform(poly, z, run_time=0.5))
        self.play(Transform(poly, polies[3]))

        # Move polygon to the side
        self.play(poly.scale, 0.75,
                  poly.shift, [4, 0, 0])

        # Create setup equation
        equ_parts = VGroup(
            TextMobject("Area"),
            TexMobject("\\left(").scale(1.5),
            self.poly_parts(6, 3 * 0.75, [4, 0, 0])[1][5].scale(0.5).rotate(-PI / 2),
            TexMobject("\\right)").scale(1.5),
            TexMobject('=', '{1', '\\over', '2}', 'b', 'h')
        ).arrange(RIGHT, buff=0.1).scale(1.5).to_corner(UL)
        temp_part = self.poly_parts(6, 3, [0, -0.5, 0]  # Part to be placed in equation
                                    ).scale(0.75).shift([4., 0, 0])[1][5]
        self.play(*[Write(equ_parts[(3 + x) % 4])
                    for x in range(3)],
                  Write(temp_part))
        self.play(ReplacementTransform(temp_part, equ_parts[2]))
        self.play(Write(equ_parts[4]))
        self.wait()

        # Simplify Equation to one object (Because I don't hate myself)
        first_area = TexMobject('A', '=', '{', '1', '\\over', '2', '}', 'b', 'h').scale(2).to_corner(UL)
        first_area[0].set_color(color=colors['ph'])
        self.play(*[ReplacementTransform(equ_parts[x], first_area[0])
                    for x in range(4)],
                  ReplacementTransform(equ_parts[4], first_area[1:]))
        self.wait()

        # Substitute base
        area_1 = TexMobject('A', '=', '{', '1', '\\over', '2', '}', 'a', 'h').scale(2).to_corner(UL)
        area_1[0].set_color(color=colors['ph'])
        area_1[7].set_color(color=colors['a'])
        self.play(FadeOutAndShiftDown(first_area[7]),
                  ReplacementTransform(poly[3][0].copy(), area_1[7]),
                  *[ReplacementTransform(first_area[(8 + x) % 9], area_1[(8 + x) % 9])
                    for x in range(9)])
        self.wait()

        # Equation for height
        first_height = TexMobject('tan\\left(', '\\theta', '\\right)', '=', '{', '{a', '\\over', '2}', '\\over', 'h}'
                                  ).scale(2).to_edge(LEFT)
        first_height[1].set_color(color=colors['rh'])
        first_height[5].set_color(color=colors['a'])
        self.play(*[Write(first_height[x])
                    for x in range(10)])
        self.wait(1.5)
        height_1 = TexMobject('h', '=', '{a', '\\over', '2', '\\cdot', 'tan\\left(', '\\theta', '\\right)', '}'
                              ).scale(2).to_edge(LEFT)
        height_1[2].set_color(color=colors['a'])
        height_1[7].set_color(color=colors['rh'])
        self.play(*[ReplacementTransform(first_height[x], height_1[y])
                    for x, y in zip([0, 1, 2, 3, 5, 6, 7, 8, 9],
                                    [6, 7, 8, 1, 2, 5, 4, 3, 0])])
        self.wait()

        # Equation for theta
        first_theta = TexMobject('\\theta', '=', '2', '\\pi', '\\cdot', '{1', '\\over', 'n}', '\\cdot', '{1',
                                 '\\over', '2}').scale(2).to_corner(DL)
        first_theta[0].set_color(colors['rh'])
        first_theta[7].set_color(colors['b'])
        for i in [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]:
            self.play(*[Write(first_theta[z])
                        for z in i])
            self.wait(0.5)
        theta_1 = TexMobject('\\theta', '=', '{\\pi', '\\over', 'n}').scale(2).to_corner(DL)
        theta_1[0].set_color(colors['rh'])
        theta_1[4].set_color(colors['b'])
        self.play(*[ReplacementTransform(first_theta[x], theta_1[y])  # Combine Terms
                    for x, y in zip([0, 1, 3, 4, 6, 8, 10, 7],
                                    [0, 1, 2, 3, 3, 3, 3, 4])],
                  *[FadeOutAndShiftDown(first_theta[z])
                    for z in [2, 11]],
                  *[FadeOut(first_theta[z])
                    for z in [9, 5]])
        self.wait()

        # Substitute Theta
        height_2 = TexMobject('h', '=', '{a', '\\over', '2', '\\cdot', 'tan\\left(', '{\\pi', '\\over', 'n}',
                              '\\right)}').scale(2).to_edge(LEFT)
        height_2[2].set_color(colors['a'])
        height_2[9].set_color(colors['b'])
        self.play(*[ReplacementTransform(height_1[x], height_2[y])
                    for x, y in zip([*range(7), 8],
                                    [*range(7), 10])],
                  FadeOut(height_1[7]))
        self.play(*[ReplacementTransform(theta_1[x], height_2[y])
                    for x, y in zip([2, 3, 4], [7, 8, 9])],
                  *[FadeOutAndShiftDown(theta_1[x])
                    for x in [0, 1]])
        self.wait()

        # Substitute Height
        final_equ = TexMobject('A', '=', '{', '1', '\\over', '2', '}', 'a', '\\cdot', '{a', '\\over', '2', '\\cdot',
                               'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                               ).scale(1.5).to_corner(UL)
        final_equ[0].set_color(colors['ph'])
        final_equ[7].set_color(colors['a'])
        final_equ[9].set_color(colors['a'])
        final_equ[16].set_color(colors['b'])
        self.play(*[ReplacementTransform(area_1[x], final_equ[y])
                    for x, y in zip([*range(8)],
                                    [*range(8)])],
                  FadeOutAndShiftDown(area_1[8]),
                  Write(final_equ[8]))
        self.wait()
        self.play(*[ReplacementTransform(height_2[x], final_equ[y])
                    for x, y in zip([*range(2, 11)],
                                    [*range(9, 18)])],
                  *[FadeOut(height_2[z])
                    for z in [0, 1]])
        self.wait()

        # Simplify Final Equation
        final_equ_2 = TexMobject('A', '=', '{a^2', '\\over', '4', '\\cdot',
                                 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(1.5).to_corner(UL)
        final_equ_2[0].set_color(colors['ph'])
        final_equ_2[2].set_color(colors['a'])
        final_equ_2[9].set_color(colors['b'])
        self.play(*[ReplacementTransform(final_equ[x], final_equ_2[y])
                    for x, y in zip([0, 1, 7, 9, 4, 10, 3, 5, 11, 12, 8, 13, 14, 15, 16, 17],
                                    [0, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 7, 8, 9, 10])])
        self.wait()
        self.play(final_equ_2.scale, 1.5,
                  final_equ_2.move_to, [-3, 0, 0])
        ref_equ = final_equ_2.copy()
        self.wait()

        # Encapsulate in Triangle and make new equation
        geo_equ = VGroup(
            TexMobject('n', '\\cdot').scale(3.5),
            TexMobject('\\left(').scale(3.5),
            Triangle(fill_color="#700040", fill_opacity=0.5).scale(2),
            TexMobject('\\right)').scale(3.5),
            TexMobject('=').scale(3.5)
        ).arrange(RIGHT).to_edge(LEFT)
        self.play(ReplacementTransform(final_equ_2, geo_equ[2]))
        self.play(*[Write(geo_equ[(3 + x) % 5])
                    for x in range(4)])
        self.wait(2)

        # Turn Triangle back into equation
        geo_equ_2 = VGroup(
            TexMobject('n', '\\cdot').scale(2.5),
            TexMobject('\\left(').scale(2.5),
            ref_equ.copy()[2:].scale(0.75),
            TexMobject('\\right)').scale(2.5),
            TexMobject('=').scale(2.5)
        ).arrange(RIGHT).to_edge(LEFT)
        self.play(ReplacementTransform(geo_equ, geo_equ_2))
        self.wait(2)

        # ACTUAL FINAL EQUATION
        final_equ_3 = TexMobject('A', '=', '{n', 'a^2', '\\over', '4', '\\cdot',
                                 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(2.25).move_to([-3, 0, 0])
        final_equ_3[0].set_color(colors['v'])
        final_equ_3[2].set_color(colors['b'])
        final_equ_3[3].set_color(colors['a'])
        final_equ_3[10].set_color(colors['b'])
        self.play(*[ReplacementTransform(geo_equ_2[2][x], final_equ_3[y])
                    for x, y in zip([0, 1, 2, 3, 4, 5, 6, 7, 8],
                                    [3, 4, 5, 6, 7, 8, 9, 10, 11])],
                  ReplacementTransform(geo_equ_2[0][0], final_equ_3[2]),
                  *[FadeOut(geo_equ_2[x])
                    for x in [1, 3, 4]],
                  FadeOut(geo_equ_2[0][1]))
        self.play(Write(final_equ_3[:2]))
        surr_rect = SurroundingRectangle(final_equ_3)
        self.play(Write(surr_rect))
        self.wait()

        # Fade out all mobjects exept the first...my logo
        self.play(*[FadeOut(x)
                    for x in self.mobjects[1:]])

    def make_poly(self, sides, scale=1, center=[0, 0, 0], label="n"):
        final_output = VGroup()
        rotate_factor = (2 * PI) / sides

        # First Vect, lower-right
        # This is a complex but short way to draw out any regular polygon
        # I use complex multiplication to map out the points
        mover_vert = complex(scale, 0) * complex(math.cos(rotate_factor / 2), math.sin(rotate_factor / 2))
        all_verts = [mover_vert]  # List of complex nums
        for _ in range(sides - 1):
            mover_vert = mover_vert * complex(math.cos(rotate_factor), math.sin(rotate_factor))
            all_verts.append(mover_vert)
        final_points = []
        for i in all_verts:
            final_points.append([i.real, i.imag, 0])

        # Make polygon with points
        poly = Polygon(*final_points)
        n_label = TextMobject("{} sides".format(label)).scale(3).to_edge(UP, buff=0.05).shift([0, -center[1], 0])
        poly_group = VGroup(poly, n_label)
        final_output.add(poly_group)

        # Creating Annotations
        right_tri = [
            Line([0, 0, 0], [0 + scale * math.cos(rotate_factor / 2), 0, 0]),
            Line([0, 0, 0], final_points[0]),
            Line([0, 0, 0], final_points[sides - 1])
        ]
        line_group = VGroup(*right_tri)
        final_output.add(line_group)

        # Arc
        arc = Arc(0, rotate_factor / 2, arc_center=[0, 0, 0], radius=0.75, color=colors['rh'],
                  stroke_width=6)
        final_output.add(arc)

        # Create Labels
        labels_list = [
            TexMobject('a', color=colors['a']).scale(1.5).move_to(
                [(math.cos(rotate_factor / 2) * scale * 1.2) + center[0], center[0], 0]),
            TexMobject('\\theta', color=colors['rh']).scale(1).move_to(1.4 * arc.point_from_proportion(0.5))
        ]
        labels = VGroup(*labels_list)
        final_output.add(labels)

        final_output.shift(center)

        # [Polygon, Lines, Arc, Labels]
        return final_output

    def poly_parts(self, sides, scale=1, center=[0, 0, 0]):
        poly = self.make_poly(sides, scale, center)
        final_group = VGroup(poly[0])

        # Outer Vertices
        rotate_factor = (2 * PI) / sides
        mover_vert = complex(scale, 0) * complex(math.cos(rotate_factor / 2), math.sin(rotate_factor / 2))
        all_verts = [mover_vert]  # List of complex nums
        for _ in range(sides - 1):
            mover_vert = mover_vert * complex(math.cos(rotate_factor), math.sin(rotate_factor))
            all_verts.append(mover_vert)
        trianlge_points = []
        for i in all_verts:
            trianlge_points.append([i.real + center[0], i.imag + center[1], 0])

        # Triangles
        tris = VGroup()
        for i in range(sides):
            tris.add(Polygon(center, trianlge_points[i], trianlge_points[(i + 1) % (sides)],
                             fill_color="#700040", fill_opacity=1))
        final_group.add(tris)

        # Ghost object for bug fix
        final_group.add(
            TexMobject('a').scale(1.5).move_to(
                [(math.cos(rotate_factor / 2) * scale * 1.2) + center[0], center[0], 0]
            ))

        # [Frame, Triangles, GHOST]
        return final_group


class MakeFunction(Scene):
    def construct(self):
        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        header = VGroup(
            TextMobject("Cross-Section at any height"),
            Line([-5, 0, 0], [5, 0, 0])
        ).arrange(DOWN).to_edge(UP)
        header[0].set_color(colors["h"]).scale(1.75)
        self.play(Write(header))

        text_1 = VGroup(
            TextMobject("Similarly to my video on the ", "Tetrahedron", ","),
            TextMobject("we'll need to find the area of any cross-section"),
            TextMobject("when given the height of said cross-section.")
        ).arrange(DOWN).next_to(header, DOWN)
        text_1[0][1].set_color(colors['h'])

        for x in text_1:
            self.play(Write(x))
        self.wait(9)

        text_2 = VGroup(
            TextMobject("We need cross-sectional area with respect to ", "height", ","),
            TextMobject("However, our formula is with respect to edge length."),
            TextMobject("So we'll need to relate ", "a", " to ", "h", ".")
        ).arrange(DOWN).next_to(header, DOWN)
        text_2[2][1].set_color(colors['a'])
        text_2[2][3].set_color(colors['rh'])

        TEMP_A_to_H = TexMobject('A', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot',
                                 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(1.5).next_to(text_2, DOWN, 2)
        TEMP_A_to_H[0].set_color(colors['ph'])
        TEMP_A_to_H[2].set_color(colors['b'])
        TEMP_A_to_H[3].set_color(colors['a'])
        TEMP_A_to_H[11].set_color(colors['b'])

        PS_text = TextMobject("PS, \"", "H", "\" refers to the total height of the pyramid.", color=colors['h'])
        PS_text.move_to(text_2[1])
        PS_text[1].set_color(colors['ph'])

        # Second Text
        for x in range(3):
            self.play(FadeOutAndShiftDown(text_1[x]),
                      Write(text_2[x]))
        self.play(Write(TEMP_A_to_H))
        self.wait(2)
        self.play(Transform(text_2[1], PS_text))
        self.play(FadeOut(TEMP_A_to_H))

        # Box input for picture/video
        lines = VGroup(
            Line([0, 0, 0], [7.2, 0, 0]),
            Line([0, 0, 0], [0, -4, 0])
        )
        self.play(Write(lines))

        equ_set_1 = VGroup(  # The "CLUES" on the left side of the screen
            TextMobject("CLUES:", color=colors['h']).scale(1.5),
            TexMobject('A', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'),
            TexMobject('A', '\\left(', '0', '\\right)', '=', 'm', '\\cdot', '0', '+', 'b', '=', 'a'),
            TexMobject('A', '\\left(', 'H', '\\right)', '=', 'm', '\\cdot', 'H', '+', 'b', '=', '0')
        ).arrange(DOWN)
        equ_set_1[1][0].set_color(colors['ph'])
        equ_set_1[1][2].set_color(colors['rh'])
        equ_set_1[1][6].set_color(colors['rh'])
        equ_set_1[2][0].set_color(colors['ph'])
        equ_set_1[2][11].set_color(colors['a'])
        equ_set_1[3][0].set_color(colors['ph'])
        equ_set_1[3][2].set_color(colors['ph'])
        equ_set_1[3][7].set_color(colors['ph'])

        for x in equ_set_1[1:]:
            x.align_to(equ_set_1[0], LEFT)
        equ_set_1.to_edge(LEFT).shift([0, -1.5, 0])
        self.play(Write(equ_set_1))
        self.wait(2)

        equ_set_2 = VGroup(
            TextMobject("CLUES:", color=colors['h']).scale(1.5),
            TexMobject('A', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'),
            TexMobject('b', '=', 'a'),
            TexMobject('m', '=', '{-', 'b', '\\over', 'H}')
        ).arrange(DOWN)
        equ_set_2[1][0].set_color(colors['ph'])
        equ_set_2[1][2].set_color(colors['rh'])
        equ_set_2[1][6].set_color(colors['rh'])
        equ_set_2[2][2].set_color(colors['a'])
        equ_set_2[3][5].set_color(colors['ph'])

        for x in equ_set_2[1:]:
            x.align_to(equ_set_2[0], LEFT)
        equ_set_2.to_edge(LEFT).shift([0, -1.5, 0])

        # First set of "CLUE" equations to the second
        self.play(*[FadeOutAndShiftDown(x)  # Double Stacked For loop for fun
                    for y, z in zip([*range(5)], [*range(5)])
                    for x in [equ_set_1[2][y], equ_set_1[3][z]]],
                  *[FadeOutAndShiftDown(equ_set_1[2][x])
                    for x in range(5, 9)])
        self.wait()

        self.play(*[ReplacementTransform(equ_set_1[2][x], equ_set_2[2][y])
                    for x, y in zip([9, 10, 11],
                                    [0, 1, 2])],
                  *[ReplacementTransform(equ_set_1[3][x], equ_set_2[3][y])
                    for x, y in zip([5, 10, 11, 9, 8, 7],
                                    [0, 1, 2, 3, 4, 5])],
                  FadeOut(equ_set_1[3][6]),
                  ReplacementTransform(equ_set_1[:2], equ_set_2[:2])
                  )
        self.wait()

        # Equation used to relate a to h, to allow for substitution
        convert_equs = [
            TexMobject('A', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'b'
                       ).scale(1.5).move_to([3.55, -2, 0]),
            TexMobject('A', '\\left(', 'h', '\\right)', '=', 'm', 'h', '+', 'a'
                       ).scale(1.5).move_to([3.55, -2, 0]),
            TexMobject('A', '\\left(', 'h', '\\right)', '=', '{-', 'b', '\\over', 'H}', 'h', '+', 'a'
                       ).scale(1.5).move_to([3.55, -2, 0]),
            TexMobject('A', '\\left(', 'h', '\\right)', '=', '{-', 'a', '\\over', 'H}', 'h', '+', 'a'
                       ).scale(1.5).move_to([3.55, -2, 0])
        ]
        convert_equs[0][0].set_color(colors['ph'])
        convert_equs[0][2].set_color(colors['rh'])
        convert_equs[0][6].set_color(colors['rh'])
        convert_equs[1][0].set_color(colors['ph'])
        convert_equs[1][2].set_color(colors['rh'])
        convert_equs[1][6].set_color(colors['rh'])
        convert_equs[1][8].set_color(colors['a'])
        convert_equs[2][0].set_color(colors['ph'])
        convert_equs[2][2].set_color(colors['rh'])
        convert_equs[2][8].set_color(colors['ph'])
        convert_equs[2][9].set_color(colors['rh'])
        convert_equs[2][11].set_color(colors['a'])
        convert_equs[3][0].set_color(colors['ph'])
        convert_equs[3][2].set_color(colors['rh'])
        convert_equs[3][6].set_color(colors['a'])
        convert_equs[3][8].set_color(colors['ph'])
        convert_equs[3][9].set_color(colors['rh'])
        convert_equs[3][11].set_color(colors['a'])

        self.play(Write(convert_equs[0]))

        # Equation 0 - 1
        self.play(*[ReplacementTransform(convert_equs[0][x], convert_equs[1][y])
                    for x, y in zip([*range(8)],
                                    [*range(8)])],
                  *[ReplacementTransform(i, z)
                    for i, z in zip([convert_equs[0][8], equ_set_2[2][2].copy()],
                                    [equ_set_2[2][0], convert_equs[1][8]])])
        self.wait()

        # Equation 1 - 2
        self.play(*[ReplacementTransform(convert_equs[1][x], convert_equs[2][y])
                    for x, y in zip([*range(5), *range(6, 9)],
                                    [*range(5), *range(9, 12)])],
                  *[ReplacementTransform(i, z)
                    for i, z in zip([convert_equs[1][5], equ_set_2[3][2:].copy()],
                                    [equ_set_2[3][0], convert_equs[2][5:9]])])
        self.wait()

        # Equation 2 - 3
        self.play(*[ReplacementTransform(convert_equs[2][x], convert_equs[3][y])
                    for x, y in zip([*range(6), *range(7, 12)],
                                    [*range(6), *range(7, 12)])],
                  *[ReplacementTransform(i, z)
                    for i, z in zip([convert_equs[2][6], equ_set_2[2][2].copy()],
                                    [equ_set_2[2][0], convert_equs[3][6]])])
        self.wait()

        text_3 = VGroup(
            TextMobject("This function takes any height(", "h", "), And returns"),
            TextMobject("the egde length of the cross-sectional polygon at that height."),
            TextMobject("Next, We'll incorporate it into our area formula.")
        ).arrange(DOWN).next_to(header, DOWN)
        text_3[0][1].set_color(colors['rh'])

        for x in range(3):
            self.play(FadeOutAndShiftDown(text_2[x]),
                      Write(text_3[x]))
        self.wait()

        final_equ_1 = TexMobject('A', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot',
                                 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}').scale(1.5).next_to(header, DOWN)
        final_equ_1[0].set_color(colors['ph'])
        final_equ_1[2].set_color(colors['b'])
        final_equ_1[3].set_color(colors['a'])
        final_equ_1[11].set_color(colors['b'])

        self.play(FadeOutAndShiftDown(text_3),
                  Write(final_equ_1))
        self.wait()

        final_equ_2 = TexMobject('A', '=', '{n', '\\left(', '{-', 'a', '\\over', 'H}', 'h', '+', 'a', '\\right)', '^2',
                                 '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(1.5).next_to(header, DOWN)
        final_equ_2[0].set_color(colors['ph'])
        final_equ_2[2].set_color(colors['b'])
        final_equ_2[5].set_color(colors['a'])
        final_equ_2[7].set_color(colors['ph'])
        final_equ_2[8].set_color(colors['rh'])
        final_equ_2[10].set_color(colors['a'])
        final_equ_2[19].set_color(colors['b'])

        # Final Equation 1 - 2
        self.play(*[ReplacementTransform(final_equ_1[x], final_equ_2[y])
                    for x, y in zip([*range(3), *range(5, 13), 3, 4],
                                    [*range(3), *range(13, 21), 3, 12])],
                  ReplacementTransform(final_equ_1[3].copy(), final_equ_2[11]),
                  ReplacementTransform(convert_equs[3][5:12], final_equ_2[4:11]))
        self.play(FadeOut(convert_equs[3][:5]))
        self.wait()

        final_equ_3 = TexMobject('A', '=', '{n', '\\left(', '{a', '^2', 'h', '^2', '\\over', 'H', '^2}',
                                 '-', '{2', 'a', '^2', 'h', '\\over', 'H}', '+', 'a', '^2', '\\right)',
                                 '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(1.25).next_to(header, DOWN)
        final_equ_3[0].set_color(colors['ph'])
        final_equ_3[2].set_color(colors['b'])
        final_equ_3[4].set_color(colors['a'])
        final_equ_3[6].set_color(colors['rh'])
        final_equ_3[9].set_color(colors['ph'])
        final_equ_3[13].set_color(colors['a'])
        final_equ_3[15].set_color(colors['rh'])
        final_equ_3[17].set_color(colors['ph'])
        final_equ_3[19].set_color(colors['a'])
        final_equ_3[28].set_color(colors['b'])

        # Final Equation 2 - 3
        self.play(*[ReplacementTransform(final_equ_2[x], final_equ_3[y])
                    for x, y in zip([*range(4), *range(13, 21), 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                    [*range(4), *range(22, 30), 11, 4, 8, 9, 6, 18, 13, 21, 12])],
                  *[ReplacementTransform(final_equ_2[x].copy(), final_equ_3[y])
                    for x, y in zip([8, 10, 7, 6, 12, 12, 12, 12, 12],
                                    [15, 19, 17, 16, 5, 7, 10, 14, 20])])
        self.wait()

        final_equ_4 = TexMobject('A', '=', '{n', 'a', '^2', '\\left(', '{h', '^2', '\\over', 'H', '^2}',
                                 '-', '{2', 'h', '\\over', 'H}', '+', '1', '\\right)',
                                 '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                 ).scale(1.25).next_to(header, DOWN)
        final_equ_4[0].set_color(colors['ph'])
        final_equ_4[2].set_color(colors['b'])
        final_equ_4[3].set_color(colors['a'])
        final_equ_4[6].set_color(colors['rh'])
        final_equ_4[9].set_color(colors['ph'])
        final_equ_4[13].set_color(colors['rh'])
        final_equ_4[15].set_color(colors['ph'])
        final_equ_4[25].set_color(colors['b'])
        self.wait()

        # Final Equation 3 - 4
        self.play(*[ReplacementTransform(final_equ_3[x], final_equ_4[y])
                    for x, y in zip([*range(3), *range(22, 30), 4, 13, 19, 5, 14, 20,
                                     6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18],
                                    [*range(3), *range(19, 27), 3, 3, 3, 4, 4, 4,
                                     6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])],
                  *[ReplacementTransform(final_equ_3[x], final_equ_4[y])
                    for x, y in zip([3, 21],
                                    [5, 18])],
                  Write(final_equ_4[17]))
        self.wait()

        self.play(*[FadeOut(x)
                    for x in [equ_set_2, lines[0]]],
                  lines[1].shift, [0, 2, 0],
                  final_equ_4.move_to, [-3.55, 0, 0],
                  final_equ_4.scale, 0.8)

        self.wait(2)
        self.play(*[FadeOut(x, run_time=3)
                    for x in [final_equ_4, lines[1], header]])
        self.wait(2)

        # Fade out all mobjects except the first...my logo
        self.play(*[FadeOut(x, run_time=1.5)
                    for x in self.mobjects[1:]])


class Integration(Scene):
    def construct(self):
        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        header = VGroup(
            TextMobject("Integration For Volume"),
            Line([-5, 0, 0], [5, 0, 0])
        ).arrange(DOWN).to_edge(UP)
        header[0].set_color(colors["h"]).scale(1.75)
        self.play(Write(header))

        text_1 = VGroup(
            TextMobject("Having the cross-section at any ", "height", ","),
            TextMobject("we have the necessary information to find ", "volume", "."),
            TextMobject("We'll use integration to put together cross-sections.")
        ).arrange(DOWN).next_to(header, DOWN, 1.5)
        text_1[0][1].set_color(colors['rh'])
        text_1[1][1].set_color(colors['v'])
        for x in text_1:
            self.play(Write(x))
        self.play(FadeOut(text_1))
        self.wait(waits['m'])

        integral_1 = TexMobject('V', '=', '\\int_{0}^{H}', 'A', '\\left(', 'h', '\\right)', 'd', 'h'
                                ).scale(1.5).next_to(header, DOWN)
        integral_1[0].set_color(colors['v'])
        integral_1[3].set_color(colors['v'])
        integral_1[5].set_color(colors['rh'])
        integral_1[8].set_color(colors['rh'])
        self.play(Write(integral_1))

        lines = VGroup(
            Line([0, 0, 0], [7.2, 0, 0]),
            Line([0, 0, 0], [0, -4, 0])
        )
        self.play(Write(lines))

        init_equ_1 = TexMobject('A', '\\left(', 'h', '\\right)', '=', '{n', 'a', '^2', '\\left(', '{h', '^2', '\\over', 'H', '^2}',
                                '-', '{2', 'h', '\\over', 'H}', '+', '1', '\\right)',
                                '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over', 'n}', '\\right)}'
                                ).scale(1.15).move_to([3.55, -2, 0])
        init_equ_1[0].set_color(colors['v'])
        init_equ_1[2].set_color(colors['rh'])
        init_equ_1[5].set_color(colors['b'])
        init_equ_1[6].set_color(colors['a'])
        init_equ_1[9].set_color(colors['rh'])
        init_equ_1[12].set_color(colors['ph'])
        init_equ_1[16].set_color(colors['rh'])
        init_equ_1[18].set_color(colors['ph'])
        init_equ_1[28].set_color(colors['b'])
        self.play(Write(init_equ_1))
        self.wait(waits['s'])

        init_equ_2 = VGroup(
            TexMobject('V', '=', '\\int_{0}^{H}').scale(1.25),
            TexMobject('\\left(').scale(3),
            init_equ_1[5:].copy(),
            TexMobject('\\right)').scale(3),
            TexMobject('d', 'h').scale(1.25)
        ).arrange(RIGHT).next_to(header, DOWN)
        init_equ_2[0][0].set_color(colors['v'])
        init_equ_2[4][1].set_color(colors['rh'])

        # Integral & init_1 to init_2
        self.play(ReplacementTransform(integral_1[:3], init_equ_2[0]),
                  *[ReplacementTransform(integral_1[x].copy(), init_equ_2[y])
                    for x, y in zip([4, 6], [1, 3])],
                  ReplacementTransform(integral_1[7:], init_equ_2[4]),
                  ReplacementTransform(integral_1[3:7], init_equ_1[:4]))
        self.play(ReplacementTransform(init_equ_1[5:], init_equ_2[2], run_time=waits['m']),
                  FadeOut(init_equ_1[:5]))

        # Lower Line
        l_line = Line([-7.1, -1, 0], [7.1, -1, 0])
        self.play(ReplacementTransform(lines[0], l_line),
                  FadeOutAndShiftDown(lines[1]))

        # Move Equation
        self.play(init_equ_2.move_to, [0, 1, 0])

        # Step Sign FACTOR OUT CONSTANTS
        step_1 = VGroup(
            TextMobject("STEP:", color=colors['h']).scale(2),
            Line().scale(2.25),
            TextMobject("Factor Out Constants").scale(1.5),
        ).arrange(DOWN).next_to(l_line, DOWN)
        self.play(Write(step_1))
        self.wait(waits['m'])

        init_equ_3 = TexMobject('V', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over',
                                'n}', '\\right)}', '\\int_{0}^{H}', '\\left(', '{h', '^2', '\\over', 'H', '^2}',
                                '-', '{2', 'h', '\\over', 'H}', '+', '1', '\\right)', 'd', 'h'
                                ).scale(1.15).move_to([0, 1, 0])
        init_equ_3[0].set_color(colors['v'])
        init_equ_3[2].set_color(colors['b'])
        init_equ_3[3].set_color(colors['a'])
        init_equ_3[11].set_color(colors['b'])
        init_equ_3[15].set_color(colors['rh'])
        init_equ_3[18].set_color(colors['ph'])
        init_equ_3[22].set_color(colors['rh'])
        init_equ_3[24].set_color(colors['ph'])
        init_equ_3[29].set_color(colors['rh'])

        # init_equ 2 to 3
        self.play(*[ReplacementTransform(init_equ_2[0][x], init_equ_3[y], run_time=1.5)
                    for x, y in zip([0, 1, 2], [0, 1, 13])],
                  *[ReplacementTransform(init_equ_2[x], init_equ_3[y], run_time=1.5)
                    for x, y in zip([1, 3], [14, 27])],
                  *[ReplacementTransform(init_equ_2[2][x], init_equ_3[y], run_time=1.5)
                    for x, y in zip([0, 1, 2, 18, 19, 20, 21, 22, 23, 24,
                                     4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17],
                                    [2, 3, 4, 6, 7, 8, 9, 10, 11, 12,
                                     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 5])],
                  ReplacementTransform(init_equ_2[4], init_equ_3[-2:], run_time=1.5),
                  *[FadeOut(init_equ_2[2][x], run_time=1.5)
                    for x in [3, 16]])

        # Step Sign FIND ANTIDERIVATIVE
        step_2 = TextMobject("Find AntiDerivative").scale(1.5).move_to(step_1[2])
        self.play(FadeOutAndShiftDown(step_1[2]),
                  Write(step_2))
        self.wait(waits['m'])

        init_equ_4 = TexMobject('V', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over',
                                'n}', '\\right)}', '\\left(', '{h', '^3', '\\over', '3', 'H', '^2}',
                                '-', '{2', 'h', '^2', '\\over', '2', 'H}', '+', 'h', '\\right)', '\\biggr|_{0}^{H}'
                                ).scale(1.15).move_to([0, 1, 0])
        init_equ_4[0].set_color(colors['v'])
        init_equ_4[2].set_color(colors['b'])
        init_equ_4[3].set_color(colors['a'])
        init_equ_4[11].set_color(colors['b'])
        init_equ_4[14].set_color(colors['rh'])
        init_equ_4[18].set_color(colors['ph'])
        init_equ_4[22].set_color(colors['rh'])
        init_equ_4[26].set_color(colors['ph'])
        init_equ_4[28].set_color(colors['rh'])

        # 3 to 4
        self.play(*[ReplacementTransform(init_equ_3[x], init_equ_4[y], run_time=1.5)
                    for x, y in zip([*range(28)],
                                    [*range(13), 30, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 26, 27, 28, 29])],
                  *[ReplacementTransform(init_equ_3[x].copy(), init_equ_4[y], run_time=1.5)
                    for x, y in zip([16, 21, 21], [17, 23, 25])],
                  *[FadeOut(init_equ_3[x], run_time=1.5)
                    for x in [28, 29]])

        # Step Sign Evaluate across interval
        step_3 = TextMobject("Evaluate Across Interval").scale(1.5).move_to(step_2)
        self.play(FadeOutAndShiftDown(step_2),
                  Write(step_3))
        self.wait(waits['s'])

        init_equ_5 = TexMobject('V', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over',
                                'n}', '\\right)}', '\\left(', '{H', '^3', '\\over', '3', 'H', '^2}',
                                '-', '{2', 'H', '^2', '\\over', '2', 'H}', '+', 'H', '\\right)'
                                ).scale(1.15).move_to([0, 1, 0])
        init_equ_5[0].set_color(colors['v'])
        init_equ_5[2].set_color(colors['b'])
        init_equ_5[3].set_color(colors['a'])
        init_equ_5[11].set_color(colors['b'])
        init_equ_5[14].set_color(colors['ph'])
        init_equ_5[18].set_color(colors['ph'])
        init_equ_5[22].set_color(colors['ph'])
        init_equ_5[26].set_color(colors['ph'])
        init_equ_5[28].set_color(colors['ph'])

        # 4 to 5
        self.play(*[ReplacementTransform(init_equ_4[x], init_equ_5[x])
                    for x in range(30)],
                  FadeOut(init_equ_4[30]))

        # Step Sign Simplify
        step_4 = TextMobject("Simplify").scale(1.5).move_to(step_3)
        self.play(FadeOutAndShiftDown(step_3),
                  Write(step_4))
        self.wait(waits['s'])

        init_equ_6 = TexMobject('V', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over',
                                'n}', '\\right)}', '\\left(', '{H', '\\over', '3}',
                                '-', 'H', '+', 'H', '\\right)'
                                ).scale(1.15).move_to([0, 1, 0])
        init_equ_6[0].set_color(colors['v'])
        init_equ_6[2].set_color(colors['b'])
        init_equ_6[3].set_color(colors['a'])
        init_equ_6[11].set_color(colors['b'])
        init_equ_6[14].set_color(colors['ph'])
        init_equ_6[18].set_color(colors['ph'])
        init_equ_6[20].set_color(colors['ph'])

        # 5 to 6
        self.play(*[ReplacementTransform(init_equ_5[x], init_equ_6[y])
                    for x, y in zip([*range(14), 14, 16, 17, 20, 22, 27, 28, 29],
                                    [*range(22)])],
                  *[ReplacementTransform(init_equ_5[x], init_equ_6[y])
                    for x, y in zip([15, 18, 19, 21, 23, 24, 25, 26],
                                    [14, 14, 14, 18, 18, 18, 18, 18])])
        self.wait(waits['s'])

        init_equ_7 = TexMobject('V', '=', '{n', 'a', '^2', '\\over', '4', '\\cdot', 'tan\\left(', '{\\pi', '\\over',
                                'n}', '\\right)}', '\\cdot', '{H', '\\over', '3}'
                                ).scale(2)
        init_equ_7[0].set_color(colors['v'])
        init_equ_7[2].set_color(colors['b'])
        init_equ_7[3].set_color(colors['a'])
        init_equ_7[11].set_color(colors['b'])
        init_equ_7[14].set_color(colors['ph'])

        # Fade Out Lower Screen
        self.play(*[FadeOut(x)
                    for x in [l_line, step_1[0:2], step_4]])
        self.wait(waits['s'])

        # 6 to 7 FINAL TRANSFORM
        self.play(FadeOutAndShift(init_equ_6[17:19], RIGHT),
                  FadeOutAndShift(init_equ_6[19:21], LEFT),
                  *[FadeOut(init_equ_6[x])
                    for x in [13, 21]]
                  )
        self.play(*[ReplacementTransform(init_equ_6[x], init_equ_7[x])
                    for x in [*range(13), 14, 15, 16]],
                  Write(init_equ_7[13], run_time=2))

        # Move Equ DOWN
        self.play(init_equ_7.to_edge, DOWN,
                  init_equ_7.scale, 0.75)

        # Surringing Rect
        s_rect = SurroundingRectangle(init_equ_7[2:10])
        s_text = VGroup(TextMobject('This is equal to the area of our base polygon'),
                        TextMobject("So often, you'll find it writen out as")
                        ).arrange(DOWN).next_to(header, DOWN)
        self.play(*[Write(x)
                    for x in [s_rect, s_text]])
        self.wait(waits['m'])

        alt_form = TexMobject('V', '=', 'B', '\\cdot', '{H', '\\over', '3}'
                              ).scale(1.5).next_to(init_equ_7, UP, 0.75).align_to(init_equ_7[0], LEFT)
        alt_form[0].set_color(colors['v'])
        alt_form[2].set_color(colors['rh'])
        alt_form[4].set_color(colors['ph'])

        # Write out the simpler form of the equation
        self.play(Write(alt_form),
                  FadeOut(s_rect))
        self.wait()

        # Fade out the text and move the mobjects around for one last shot
        self.play(FadeOut(s_text))

        self.play(alt_form.next_to, header, DOWN, 1.35,
                  init_equ_7.to_edge, DOWN, 1.35)

        self.wait(2)

        # Fade Everything out
        self.play(*[FadeOut(x)
                    for x in [init_equ_7, alt_form, header]])


class BonusVisual(Scene):
    def construct(self):
        # Logo
        self.add(TextMobject('Peter Gilliam', color=colors['sl']).scale(0.5).to_edge(DL))

        # Title Header
        header = VGroup(
            TextMobject("Bonus Visualization!").scale(1.5),
            Line([-6, 0, 0], [6, 0, 0])
        ).arrange(DOWN).to_edge(UP)
        header[0].set_color(colors["h"]).scale(1.75)

        # Text Body to explain list
        text_1 = VGroup(
            TextMobject('The volume of any pyramid can be found using'),
            TextMobject('a three step procedure, described below.')
        ).arrange(DOWN).next_to(header, DOWN)

        # The procedure list
        proced_list = VGroup(
            TextMobject('1) ', 'Find Base ', 'Area').scale(1.25),
            TextMobject('2) ', 'Multiply by ', 'height').scale(1.25),
            TextMobject('3) ', 'Divide by 3').scale(1.25)
        ).arrange(DOWN)
        proced_list[0][2].set_color(colors['v'])
        proced_list[1][2].set_color(colors['rh'])
        for x in proced_list[1:]:
            x.align_to(proced_list[0], LEFT)
        proced_list.move_to([0, -2, 0]).align_to([-6.75, 0, 0], LEFT)

        # Line Frame for Video input
        lines = VGroup(
            Line([0, 0, 0], [7.2, 0, 0]),
            Line([0, 0, 0], [0, -4, 0])
        )

        #
        self.play(Write(header, run_time=1.5))
        self.wait(0.5)
        for x in text_1:
            self.play(Write(x))
        self.wait()
        for x in proced_list:
            self.play(Write(x))
        self.wait(10)
        self.play(Write(lines))
        self.wait(12)

