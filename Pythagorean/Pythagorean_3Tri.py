from manimlib.imports import *

abc_colors =[
    '#800000',
    '#1134A6',
    '#3BB143']

POINTS_final = np.array([
    [-2.5,-1,0],
    [2.5,-1,0],
    [2.5,-3,0],
    [-2.5,-3,0],
    #  0
    # 3
    [-1.5,-1,0]
    #  4
    # 1
    # 2
    #  3
    # 4
    # 2
])
POINTS_base = np.array([
    [-0.5,2.5,0],
    [-0.5,0.5,0],
    [0.5,0.5,0]])

POINTS_line = np.array([
    [-2.5,-1,0],
    [2.5,-1,0],

    [2.5,-3,0],
    [-2.5,-3,0],

    [-1.5,-0.95,0],
    [-1.5,-1.06,0]])

POINTS_right = np.array([
    [-0.5,0.5,0],
    [-0.5,0.75,0],
    [-0.25,0.75,0],
    [-0.25,0.5,0],

    [-2.5,-1,0],
    [-2.3,-1,0],
    [-2.3,-1.2,0],
    [-2.5,-1.2,0],

    [-1.5,-1,0],
    [-1.34,-1.08,0],
    [-1.42,-1.24,0],
    [-1.58,-1.16,0],

    [2.5,-1,0],
    [2.5,-1.2,0],
    [2.3,-1.2,0],
    [2.3,-1,0]
])

class Pythagorean(Scene):
    def construct(self):
        # Intro
        self.add_sound('I_feel_serene')
        peter_big = TextMobject('Peter Gilliam', color='#900000').scale(4.5)
        peter = TextMobject('Peter Gilliam', color='#900000').scale(4).to_edge(UP)
        peter2 = TextMobject('Peter Gilliam',color='#666666').scale(0.5).to_edge(DL)
        intro_caption_1 = TextMobject('The Pythagorean Theorem',' tell us how to find any'
                                      ).scale(1.2).next_to(peter,DOWN,buff=1)
        intro_caption_2 = TextMobject('side length of a right triangle given the two other sides'
                                      ).scale(1.15).next_to(intro_caption_1,DOWN,buff=0.5)
        intro_equation = TexMobject('a^2','+','b^2','=','c^2').scale(4).to_edge(DOWN)
        intro_equation[0].set_color(abc_colors[0])
        intro_equation[2].set_color(abc_colors[1])
        intro_equation[4].set_color(abc_colors[2])

        self.play(Write(peter_big, run_time=5))
        self.play(ReplacementTransform(peter_big, peter))
        self.play(Write(intro_caption_1,run_time=2))
        self.play(Write(intro_caption_2,run_time=2))
        self.play(Write(intro_equation,run_time=3))
        self.wait(2)
        self.play(ReplacementTransform(peter, peter2),
                  FadeOutAndShiftDown(intro_caption_1),
                  FadeOutAndShiftDown(intro_caption_2),
                  FadeOut(intro_equation))

        # Base Triangle

        caption_base = TextMobject('Here is a right triangle with side lengths ',
                                   'a',', ','b',' and ','c').to_edge(UP)
        caption_base[1].set_color(abc_colors[0])
        caption_base[3].set_color(abc_colors[1])
        caption_base[5].set_color(abc_colors[2])
        tri_base = Polygon(*POINTS_base[[0,1,2]])
        base_a = TexMobject('a',color=abc_colors[0]).next_to(tri_base,DOWN)
        base_b = TexMobject('b', color=abc_colors[1]).next_to(tri_base, LEFT)
        base_c = TexMobject('c', color=abc_colors[2]).move_to([0.4,1.5,0])
        right_angle_base = Polygon(*POINTS_right[[0,1,2,3]])
        tri_base_G = VGroup(tri_base,base_a,base_b,base_c,right_angle_base)

        intro_tri = tri_base_G.copy().scale(2).shift([0,-1.5,0])

        # First Triangle

        tri_1 = Polygon(*POINTS_final[[0, 3, 4]],color=abc_colors[0],fill_opacity=0.5,
                        stroke_width=0)
        tri_1_a = TexMobject('aa',color=abc_colors[0]).next_to(tri_1,UP)
        tri_1_b = TexMobject('a','b').next_to(tri_1, LEFT)
        tri_1_b[0].set_color(abc_colors[0])
        tri_1_b[1].set_color(abc_colors[1])
        tri_1_c = TexMobject('a','c').move_to([-1.6,-2,0])
        tri_1_c[0].set_color(abc_colors[0])
        tri_1_c[1].set_color(abc_colors[2])
        right_angle_1 = Polygon(*POINTS_right[[4, 5, 6, 7]],stroke_width=2,color='#000000',
                                stroke_opacity=0.75)
        tri_1_G = VGroup(tri_1,tri_1_a,tri_1_b,tri_1_c,right_angle_1)

        # Second Triangle

        tri_2 = Polygon(*POINTS_final[[3, 4, 2]],color=abc_colors[2],fill_opacity=0.5,
                        stroke_width=0)
        tri_2_a = TexMobject('a','c').move_to([-2.5,-2,0])
        tri_2_a[0].set_color(abc_colors[0])
        tri_2_a[1].set_color(abc_colors[2])
        tri_2_b = TexMobject('b', 'c').move_to([1.4, -2, 0])
        tri_2_b[0].set_color(abc_colors[1])
        tri_2_b[1].set_color(abc_colors[2])
        tri_2_c = TexMobject('cc',color=abc_colors[2]).next_to(tri_2,DOWN)
        right_angle_2 = Polygon(*POINTS_right[[8, 9, 10, 11]], stroke_width=2, color='#000000',
                                stroke_opacity=0.75)
        tri_2_G = VGroup(tri_2,tri_2_a,tri_2_b,tri_2_c,right_angle_2)

        # Third Triangle

        tri_3 = Polygon(*POINTS_final[[4, 1, 2]],color=abc_colors[1],fill_opacity=0.5,
                        stroke_width=0)
        tri_3_a = TexMobject('a','b').move_to([3,-2,0])
        tri_3_a[0].set_color(abc_colors[0])
        tri_3_a[1].set_color(abc_colors[1])
        tri_3_b = TexMobject('b', 'b',color=abc_colors[1]).next_to(tri_3,UP)
        tri_3_c = TexMobject('b','c').move_to([0,-2,0])
        tri_3_c[0].set_color(abc_colors[1])
        tri_3_c[1].set_color(abc_colors[2])
        right_angle_3 = Polygon(*POINTS_right[[12,13,14,15]], stroke_width=2, color='#000000',
                                stroke_opacity=0.75)
        tri_3_g = VGroup(tri_3,tri_3_a,tri_3_b,tri_3_c,right_angle_3)

        # Takes apart the rectangle

        pre_1_g = tri_1_G.copy().shift([-3, 0, 0])
        pre_3_g = tri_3_g.copy().shift([3, 0, 0])

        self.play(Write(caption_base),
                  Write(intro_tri, run_time=8))
        self.play(ReplacementTransform(intro_tri,tri_base_G))

        # Explaining The Left side

        caption_copying_a = TextMobject("First, let's copy the triangle and scale it by ",
                                      'a').to_edge(UP)
        caption_copying_a[1].set_color(abc_colors[0])
        caption_copying_a2 = TextMobject("In other words, we'll multiply each side by ",
                                      'a').to_edge(UP)
        caption_copying_a2[1].set_color(abc_colors[0])
        self.play(ReplacementTransform(caption_base, caption_copying_a))
        self.wait(3)
        self.play(ReplacementTransform(caption_copying_a,caption_copying_a2))
        self.wait(3)
        self.play(ReplacementTransform(tri_base.copy(),pre_1_g))
        self.wait(1)

        # Explaining The right side

        caption_copying_b = TextMobject("Next, we'll make another copy, but this time",
                                        " we'll scale it by ",'b').to_edge(UP)
        caption_copying_b[2].set_color(abc_colors[1])
        self.play(ReplacementTransform(caption_copying_a2,caption_copying_b))
        self.wait(3)
        self.play(ReplacementTransform(tri_base.copy(), pre_3_g))
        self.wait(1)

        # Explaining Middle

        caption_copying_c = TextMobject("Let's make one more copy, but we'll scale by ",
                                        'c').to_edge(UP)
        caption_copying_c[1].set_color(abc_colors[2])
        self.play(ReplacementTransform(caption_copying_b,caption_copying_c))
        self.wait(2)
        self.play(ReplacementTransform(tri_base.copy(),tri_2_G))
        self.wait(1)

        # Connecting Left two triangles

        l_m_connection = TextMobject('Our left two triangles each share a common side length'
                                     ).to_edge(UP)
        l_m_connection_2 = TextMobject("So let's stick them together!"
                                       ).to_edge(UP)
        ac1 = SurroundingRectangle(pre_1_g[3],color='#FFF200')
        ac2 = SurroundingRectangle(tri_2_G[1],color='#FFF200')
        self.play(ReplacementTransform(caption_copying_c,l_m_connection))
        self.wait(3)
        self.play(ReplacementTransform(l_m_connection,l_m_connection_2))
        self.wait(1)
        self.play(ShowCreationThenFadeOut(ac1),
                  ShowCreationThenFadeOut(ac2))
        self.play(ReplacementTransform(pre_1_g,tri_1_G),
                  FadeOut(tri_2_a))
        self.wait(1)

        # Connecting Right two triangles

        m_r_connection = TextMobject("We can do a similar thing with the right two triangles"
                                     ).to_edge(UP)
        self.play(ReplacementTransform(l_m_connection_2,m_r_connection))
        self.wait(1)
        bc1 = SurroundingRectangle(tri_2_G[2], color='#FFF200')
        bc2 = SurroundingRectangle(pre_3_g[3], color='#FFF200')
        self.play(ShowCreationThenFadeOut(bc1),
                  ShowCreationThenFadeOut(bc2))
        self.play(ReplacementTransform(pre_3_g,tri_3_g),
                  FadeOut(tri_2_b))

        # Relabeling
        tri_1_new = TexMobject('a^2', color=abc_colors[0]).move_to(tri_1_a)
        tri_2_new = TexMobject('c^2', color=abc_colors[2]).move_to(tri_2_c)
        tri_3_new = TexMobject('b^2', color=abc_colors[1]).move_to(tri_3_b)

        self.play(ReplacementTransform(tri_1_a, tri_1_new),
                  ReplacementTransform(tri_2_c, tri_2_new),
                  ReplacementTransform(tri_3_b, tri_3_new))

        # Lines
        caption_line = TextMobject('Important thing to notice, we made a rectangle!!'
                                   ).to_edge(UP)
        caption_line2 = TextMobject('thus, the top and bottom sides must have equal'
                                    ' length').to_edge(UP)
        top_line = Line(*POINTS_line[[0, 1]],color='#404040',stroke_width=5)
        top_dash = Line(*POINTS_line[[4,5]],color='#404040',stroke_width=5)
        top_group = VGroup(top_line, tri_1_a, tri_3_b, top_dash)
        bot_line = Line(*POINTS_line[[2, 3]],color='#404040',stroke_width=5)
        bot_group = VGroup(bot_line, tri_2_c)

        self.play(Write(top_group))
        self.play(Write(bot_group))

        self.play(ReplacementTransform(m_r_connection,caption_line))
        self.wait(3)
        self.play(ReplacementTransform(caption_line,caption_line2))
        self.wait(1)

        big_top = top_group.copy().move_to(np.array([0,2,0])).scale(1.5)
        big_bot = bot_group.copy().move_to(np.array([0,0.5,0])).scale(1.5)
        big_bot_temp = big_bot.copy().shift([0,0.6,0])
        big_bot_final = big_bot.copy()

        self.play(FadeOutAndShift(tri_base_G,UP),
                  ReplacementTransform(top_group.copy(), big_top))
        self.play(ReplacementTransform(bot_group.copy(), big_bot))

        caption_line3 = TextMobject('Thus, we know that'
                                    ).to_edge(UP)

        self.wait(1)
        self.play(ReplacementTransform(big_bot, big_bot_temp))
        self.wait(1)
        self.play(ReplacementTransform(big_bot_temp, big_bot_final))

        # Final Equation
        final_equation = intro_equation.copy()
        final_equation.shift([0,3.5,0])

        self.play(ReplacementTransform(caption_line2,caption_line3))
        self.play(ReplacementTransform(big_top[1],final_equation[0],run_time=2),
                  ReplacementTransform(big_top[2],final_equation[2],run_time=2),
                  ReplacementTransform(big_bot_final[1],final_equation[4],run_time=2),
                  FadeOutAndShiftDown(big_top[0]),
                  FadeOutAndShiftDown(big_bot_final[0]),
                  FadeOutAndShiftDown(big_top[3]),
                  Write(final_equation[1]),
                  Write(final_equation[3]))

        # Final Shot
        final_title = TextMobject('Pythagorean Theorem',color='#FFF200'
                                  ).scale(2.9).to_edge(UP)
        self.play(FadeOutAndShift(caption_line3,UP),
                  FadeIn(final_title,run_time=3))

        # Bonus Question
        big_bonus = TextMobject('BONUS',color='#FFF200').scale(8)
        self.play(GrowFromCenter(big_bonus))
        self.play(ShrinkToCenter(big_bonus))

        bonus_question_title = TextMobject('Bonus Question',color='#FFF200'
                                           ).scale(3).to_edge(UP)
        b_q1 = TextMobject('I tell you that the below figure is a rectangle.'
                           ).next_to(bonus_question_title,DOWN)
        b_q2 = TextMobject("However, it must be shown to complete my proof."
                           ).next_to(b_q1,DOWN)
        b_q3 = TextMobject('Question: Prove that the shape below is a rectangle.'
                           ).next_to(b_q2,DOWN)
        b_q4 = TextMobject('Hint: All three triangles are similar'
                           ).next_to(b_q2,DOWN)

        self.play(ReplacementTransform(final_title,bonus_question_title),
                  FadeOut(final_equation))
        self.play(Write(b_q1,run_time=2))
        self.play(Write(b_q2,run_time=2))
        self.play(Write(b_q3,run_time=2))
        self.wait(5)
        self.play(ReplacementTransform(b_q3,b_q4))
        self.wait(12)
