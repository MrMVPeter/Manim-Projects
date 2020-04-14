from manimlib.imports import *


POINTS = np.array([
    # Big Square UL-C
    [-6,1,0],
    [-2,1,0],
    [-2,-3,0],
    [-6,-3,0],
    # X square 4
    [-5,1,0],
    # 1
    [-2,-2,0],
    [-5,-2,0],
    # A\BX 7
    [-7,1,0],
    # 4
    # 6
    [-7,-2,0],
    # A\2Bx L 9
    # 0
    # 4
    # 6
    [-6,-2,0],
    # A\2Bx B 10
    # 7
    # 5
    # 2
    [-5,-3,0],
    # -C\A 11
    [2,1,0],
    [4,1,0],
    [4,-2,0],
    [2,-2,0]
])


# Quad Final
class QuadForm(Scene):
    def construct(self):
        self.add_sound('Gypsy')
        # Intro
        peter_big = TextMobject('Peter Gilliam',color='#900000').scale(4.5)
        peter = TextMobject('Peter Gilliam',color='#900000').scale(4).to_edge(UP)
        intro_text = TextMobject('We all know the quadratic equation,'
                                 ).scale(1.75).next_to(peter,DOWN)
        intro_text2 = TextMobject('but where does it come from?'
                                  ).scale(1.75).next_to(intro_text,DOWN)
        intro_text3 = TextMobject("Let's derive it and find out!"
                                  ).scale(1.75).next_to(intro_text2,DOWN)
        peter2 = TextMobject('Peter Gilliam',color='#666666')
        peter2.scale(0.5)
        peter2.to_edge(DL)
        self.play(Write(peter_big,run_time=5))
        self.play(ReplacementTransform(peter_big,peter))
        self.play(Write(intro_text))
        self.play(Write(intro_text2))
        self.wait(1)
        self.play(Write(intro_text3))
        self.wait(2)
        self.play(FadeOutAndShiftDown(intro_text),
                  FadeOutAndShiftDown(intro_text2),
                  FadeOutAndShiftDown(intro_text3))
        self.play(ReplacementTransform(peter,peter2))
        # 1 Top Caption

        captionup = TextMobject('Every',
                                ' Quadratic can be expressed as').to_edge(UP)
        captionup[0].set_color('#FFF200')
        self.play(Write(captionup))

        # 1 Main                0   1   2    3   4   5   6   7   8   9
        quad_form = TexMobject('a','x','^2','+','b','x','+','c','=','0').scale(3)
        for i in [1, 2, 5]:
            quad_form[i].set_color(RED)
        quad_form[0].set_color(GREEN)
        quad_form[4].set_color(BLUE)
        quad_form[7].set_color('#9966CB')
        self.play(Write(quad_form[:8], run_time=2))
        # 1 Bottom Caption

        captiond = TextMobject('Where ', 'a', ', ', 'b', ' and ', 'c', ' are constants'
                              ).to_edge(DOWN)
        captiond[1].set_color(GREEN)
        captiond[3].set_color(BLUE)
        captiond[5].set_color('#9966CB')
        self.play(Write(captiond))
        self.wait(1)
        # 1 Middle Caption

        captionmid = TextMobject("Let's Set it equal to Zero and Solve For ", 'x'
                                  ).next_to(quad_form, DOWN)
        captionmid[1].set_color(RED)
        # clearing first Scene
        self.play(Write(captionmid))
        self.play(Write(quad_form[8:]))
        self.wait(1)
        self.play(
            FadeOutAndShiftDown(captionup),
            FadeOutAndShiftDown(captionmid),
            FadeOutAndShiftDown(captiond))

        # 2 Top Caption
        caption2t = TextMobject("First, lets's separate the terms containing ",'x',
                                ' from those without').to_edge(UP)
        caption2t[1].set_color(RED)
        self.play(Write(caption2t))
        self.wait(1)
        # 2 Main                 0   1   2    3   4   5   6   7   8

        quad_form1 = TexMobject('a','x','^2','+','b','x','=','-','c').scale(3)
        for i in [1, 2, 5]:
            quad_form1[i].set_color(RED)
        quad_form1[0].set_color(GREEN)
        quad_form1[4].set_color(BLUE)
        quad_form1[8].set_color('#9966CB')
        changes0 = [
            (0, 1, 2, 3, 4, 5, 6, 7, 8),
            (0, 1, 2, 3, 4, 5, 7, 8, 6)
        ]
        self.play(
            *[
                ReplacementTransform(
                    quad_form[pre], quad_form1[pos]
                    )
                for pre,pos in zip(changes0[0], changes0[1])
            ],
            FadeOutAndShiftDown(quad_form[9]))
        self.wait(1)
        # 3 Caption Down
        caption3d = TextMobject("Next, We'll divide both sides by ",
                                'a').to_edge(DOWN)
        caption3d[1].set_color(GREEN)
        self.play(ReplacementTransform(caption2t, caption3d))
        self.wait(1)
        # 3 Main                 0    1   2    3   4        5    6

        quad_form2 = TexMobject('x','^2','+','{','b','\\over','a','}','x',
                                '=','-','{','c','\\over','a','}').scale(3)
        for i in [0, 1, 8]:
            quad_form2[i].set_color(RED)
        quad_form2[6].set_color(GREEN)
        quad_form2[14].set_color(GREEN)
        quad_form2[4].set_color(BLUE)
        quad_form2[12].set_color('#9966CB')
        changes1 = [
            (0,1,2,3,4,5,6,7,8),
            (6,0,1,2,4,8,9,10,12)
        ]
        self.play(
            *[
                ReplacementTransform(
                    quad_form1[pre2], quad_form2[pos2]
                )
                for pre2,pos2 in zip(changes1[0], changes1[1])
            ],
                ReplacementTransform(quad_form1[0].copy(), quad_form2[14]),
                Write(quad_form2[5]),
                Write(quad_form2[13])
        )
        self.wait(1)
        quad_form2_up = quad_form2.copy()
        quad_form2_up.scale(0.66).to_edge(UP,buff=0.1)
        caption_build1 = TextMobject("Let's Represent each term as an Area"
                                     ).to_edge(UP)
        self.play(Write(caption_build1),
                  FadeOut(caption3d))
        self.play(ShrinkToCenter(caption_build1),
                  ReplacementTransform(quad_form2,quad_form2_up))

        # Building Parts

        eql = TexMobject('=').scale(3).move_to(np.array([0, -1, 0]))
        c_a = c_rec()
        c_atitle = TexMobject('-{c \\over a}').move_to(np.array([3,-0.5,0]))
        xtitle = TexMobject('x^2', color=RED).move_to(np.array([-3.5, -0.5, 0]))
        xsquare = x_square()
        xbrace = Brace(xsquare,RIGHT)
        xbracetext = TexMobject('x',color=RED).next_to(xbrace,RIGHT)
        axside = ax_b()
        axtitle = TexMobject('{b \\over a}x', color=BLUE).move_to(np.array([-6, -0.5, 0]))
        ax_2br = left_rec()
        ax_2bltitle = TexMobject('{b \\over 2a}x', color=BLUE
                                 ).move_to(np.array([-5.5, -0.5, 0])).scale(0.75)

        ax_2bb = bot_rec()
        ax_2bbtitle = TexMobject('{b \\over 2a}x', color=BLUE
                                 ).move_to(np.array([-3.5, -2.5, 0])).scale(0.75)
        ax_2bbbrace = Brace(ax_2bb,RIGHT)
        ax_2bbbracetext = TexMobject('{b \\over 2a}',color=BLUE).next_to(ax_2bbbrace,RIGHT)
        smallsqr_L = small_square([-6,-2,0])
        smalltitle_L = TexMobject('{b^2 \\over 4a^2}', color=GREEN
                                ).move_to(np.array([-5.5, -2.5, 0])).scale(0.6)
        smallsqr_R = small_square([3,-2,0])
        smalltitle_R = TexMobject('{b^2 \\over 4a^2}', color=GREEN
                                  ).move_to(np.array([3.5, -2.5, 0])).scale(0.6)
        caption_build_title = TextMobject('Completing the Square',color='#FFF200'
                                          ).scale(1.5).to_edge(UP)
        caption_build2 = TextMobject('We need to rearrange the left side such that it becomes'
                                     ' a square').next_to(caption_build_title,DOWN)
        caption_build3 = TextMobject("Next, we're missing one corner on the left side"
                                     ).next_to(caption_build_title,DOWN,buff=0.1)
        caption_build4 = TextMobject('DONT forget to add to both sides!'
                                     ).next_to(caption_build3,DOWN)
        caption_build5 = TextMobject('Now we have a perfect square on the left side'
                                     ).move_to(caption_build3)
        caption_build6 = TexMobject('\\left( x + {b \\over 2a} \\right)^2'
                                    ).next_to(caption_build5,DOWN)
        caption_build7 = TextMobject('Now we can turn back to equations'
                                     ).move_to(caption_build5)

        # x squared box
        self.play(ShowCreation(xsquare),
                  ShowCreation(xbrace),
                  ShowCreation(xbracetext),
                  ReplacementTransform(quad_form2_up[0:2], xtitle),
                  FadeOut(quad_form2_up[2]))
        # temp side rec
        self.play(ShowCreation(axside),
                  ReplacementTransform(quad_form2_up[4:9], axtitle))
        # eql sign
        self.play(ReplacementTransform(quad_form2_up[9],eql))
        # c rec
        self.play(ReplacementTransform(quad_form2_up[10:].copy(),c_a),
                  ReplacementTransform(quad_form2_up[10:],c_atitle))
        self.play(Write(caption_build_title,run_time=2))
        # split recs
        self.play(Write(caption_build2))
        self.wait(1)
        self.play(ReplacementTransform(axside.copy(), ax_2br,run_time=2),
                  ReplacementTransform(axside, ax_2bb,run_time=2),
                  ReplacementTransform(axtitle.copy(), ax_2bltitle,run_time=2),
                  ReplacementTransform(axtitle, ax_2bbtitle,run_time=2),
                  ShowCreation(ax_2bbbrace,run_time=2),
                  ShowCreation(ax_2bbbracetext,run_time=2))
        self.wait(1)
        self.play(ReplacementTransform(caption_build2,caption_build3))
        self.wait(1)
        self.play(Write(caption_build4))
        self.wait(2)
        self.play(Write(smalltitle_L),
                  ShowCreation(smallsqr_L))
        self.wait(1)
        self.play(ReplacementTransform(smallsqr_L.copy(),smallsqr_R),
                  ReplacementTransform(smalltitle_L.copy(),smalltitle_R))
        self.play(ReplacementTransform(caption_build3,caption_build5),
                  ReplacementTransform(caption_build4,caption_build5),
                  Write(caption_build6))
        self.wait(2)
        self.play(ReplacementTransform(caption_build5, caption_build7))
        self.wait(1)
        self.play(FadeOutAndShiftDown(eql),
                  FadeOutAndShiftDown(c_a),
                  FadeOutAndShiftDown(c_atitle),
                  FadeOutAndShiftDown(xtitle),
                  FadeOutAndShiftDown(xsquare),
                  FadeOutAndShiftDown(xbrace),
                  FadeOutAndShiftDown(xbracetext),
                  FadeOutAndShiftDown(axside),
                  FadeOutAndShiftDown(axtitle),
                  FadeOutAndShiftDown(ax_2bbbrace),
                  FadeOutAndShiftDown(ax_2bbbracetext),
                  FadeOutAndShiftDown(ax_2bb),
                  FadeOutAndShiftDown(ax_2br),
                  FadeOutAndShiftDown(ax_2bltitle),
                  FadeOutAndShiftDown(ax_2bbtitle),
                  FadeOutAndShiftDown(smalltitle_R),
                  FadeOutAndShiftDown(smallsqr_R),
                  FadeOutAndShiftDown(smalltitle_L),
                  FadeOutAndShiftDown(smallsqr_L))


        quad_form5 = TexMobject('\\left(', 'x', '+', '{', 'b', '\\over', '2', 'a', '}', '\\right)',
                                '^2', '=', '-', '{', 'c', '\\over', 'a', '}', '+', '{', 'b', '^2',
                                '\\over', '4', 'a', '^2', '}').scale(2)
        quad_form5[1].set_color(RED)
        for i in [7, 16, 24, 25]:
            quad_form5[i].set_color(GREEN)
        for i in [4, 20, 21]:
            quad_form5[i].set_color(BLUE)
        quad_form5[14].set_color('#9966CB')

        self.play(ReplacementTransform(caption_build6,quad_form5[0:11]))
        self.play(FadeIn(quad_form5[11:]),
                  FadeOut(caption_build_title),
                  FadeOut(caption_build7))

        self.wait(1)
        quad_form5_copy = quad_form5.copy()
        mini_quad5 = quad_form5.copy().to_edge(DOWN).scale(0.75)
        pause_cap = TextMobject("PAUSE").scale(8)
        recap = TextMobject('Quick Review').scale(2).to_edge(UP)
        recap.set_color('#FFF200')
        recap_1 = TextMobject('By adding ').next_to(recap, DOWN)
        recap_1.shift([-2.1, 0, 0])
        recap_2 = TexMobject('{ b^2 \\over 4a^2').next_to(recap_1, RIGHT)
        recap_3 = TextMobject('to both sides,').next_to(recap_2, RIGHT)
        recap_4 = TextMobject('The left side can now factor into a perfect square,'
                              ).next_to(recap, DOWN, buff=1.2)
        recap_5 = TextMobject('Moving ', 'x', ' to only one term instead of two.'
                              ).next_to(recap_4, DOWN)
        recap_5[1].set_color(RED)
        recap_6 = TextMobject('Solving from here is a simple matter of Algebra'
                              ).next_to(recap_5, DOWN)
        self.play(GrowFromEdge(pause_cap, UP))
        self.wait(0.75)
        self.play(ShrinkToCenter(pause_cap))
        self.play(FadeOut(quad_form5, run_time=0),
                  ReplacementTransform(quad_form5_copy, mini_quad5))
        self.play(Write(recap))
        self.play(Write(recap_1))
        self.play(Write(recap_2))
        self.play(Write(recap_3))
        self.play(Write(recap_4))
        self.play(Write(recap_5))
        self.play(Write(recap_6))
        # 6 Set UP
        self.wait(2)
        self.play(FadeOut(recap),
                  FadeOut(recap_1),
                  FadeOut(recap_2),
                  FadeOut(recap_3),
                  FadeOut(recap_4),
                  FadeOut(recap_5),
                  FadeOut(recap_6))
        self.play(ReplacementTransform(mini_quad5, quad_form5))
        # 6 MAIN

        caption6t = TextMobject("Lets Find A common denominator on the right side"
                                ).to_edge(UP)
        self.play(Write(caption6t))
        self.wait(1)
        quad_form6 = TexMobject('\\left(', 'x', '+', '{', 'b', '\\over', '2', 'a', '}', '\\right)',
                                '^2', '=', '{', 'b', '^2', '-', '4', 'a', 'c', '\\over', '4',
                                'a', '^2', '}').scale(2)
        quad_form6[1].set_color(RED)
        for i in [7, 17, 21, 22]:
            quad_form6[i].set_color(GREEN)
        for i in [4, 13, 14]:
            quad_form6[i].set_color(BLUE)
        quad_form6[18].set_color('#9966CB')
        changes4 = [
            (12, 14, 16, 20, 21, 22, 23, 24, 25),
            (15, 18, 17, 13, 14, 19, 20, 21, 22),
            (15, 18),
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form5[i], quad_form6[z])
                for i, z in zip(changes4[0], changes4[1])],
            *[ReplacementTransform(
                quad_form5[i], quad_form6[i])
                for i in changes4[3]],
            ShrinkToCenter(quad_form5[18]),
            ReplacementTransform(quad_form5[15], quad_form6[16]))
        # 7 MAIN
        caption7t = TextMobject('Now we can take the square root of both sides'
                                ).to_edge(UP)
        self.play(ReplacementTransform(caption6t, caption7t))
        self.wait(2)
        quad_form7 = TexMobject('\\sqrt', '{', '\\left(', 'x', '+', '{', 'b', '\\over', '2', 'a', '}',
                                '\\right)', '^2', '}', '=', '\\sqrt', '{', 'b', '^2', '-', '4',
                                'a', 'c', '\\over', '4', 'a', '^2', '}', '}').scale(2)
        quad_form7[3].set_color(RED)
        for i in [9, 21, 25, 26]:
            quad_form7[i].set_color(GREEN)
        for i in [6, 17, 18]:
            quad_form7[i].set_color(BLUE)
        quad_form7[22].set_color('#9966CB')

        changes5 = [[], [], [0, 15]]
        for i in range(0, 11):
            changes5[0].append(i)
        for i in range(12, 23):
            changes5[1].append(i)

        self.play(
            *[ReplacementTransform(quad_form6[i], quad_form7[i + 2])
              for i in changes5[0]],
            *[ReplacementTransform(quad_form6[i], quad_form7[i + 4])
              for i in changes5[1]],
            ReplacementTransform(quad_form6[11], quad_form7[14]),
            *[GrowFromCenter(quad_form7[i])
              for i in changes5[2]])
        caption8t = TextMobject('Almost There! Now simplify').to_edge(UP)
        self.play(ReplacementTransform(caption7t, caption8t))
        self.wait(1)
        quad_form8 = TexMobject('x', '+', '{', 'b', '\\over', '2', 'a', '}', '=', '{', '\\pm', '\\sqrt',
                                '{', 'b', '^2', '-', '4', 'a', 'c', '}', '\\over', '\\sqrt', '{',
                                '4', 'a', '^2', '}', '}').scale(2)
        quad_form8[0].set_color(RED)
        for i in [6, 17, 24, 25]:
            quad_form8[i].set_color(GREEN)
        for i in [3, 13, 14]:
            quad_form8[i].set_color(BLUE)
        quad_form8[18].set_color('#9966CB')
        changes6 = [
            (0, 3, 4, 6, 7, 8, 9, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26),
            (21, 0, 1, 3, 4, 5, 6, 10, 8, 11, 13, 14, 15, 16, 17, 18, 20, 23, 24, 25),
            (2, 11)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form7[i], quad_form8[z])
                for i, z in zip(changes6[0], changes6[1])],
            ShrinkToCenter(quad_form7[2]),
            ShrinkToCenter(quad_form7[11]))
        self.wait(1)
        quad_form9 = TexMobject('x', '+', '{', 'b', '\\over', '2', 'a', '}', '=', '{', '\\pm', '\\sqrt',
                                '{', 'b', '^2', '-', '4', 'a', 'c', '}', '\\over', '2', 'a', '}'
                                ).scale(2)
        quad_form9[0].set_color(RED)
        for i in [6, 22]:
            quad_form9[i].set_color(GREEN)
        for i in [3, 13, 14]:
            quad_form9[i].set_color(BLUE)
        quad_form9[18].set_color('#9966CB')
        changes7 = [[23, 24], [21, 22], []]
        for i in range(0, 21):
            changes7[2].append(i)
        self.play(
            *[ReplacementTransform(
                quad_form8[i], quad_form9[z])
                for i, z in zip(changes7[0], changes7[1])],
            *[ReplacementTransform(
                quad_form8[i], quad_form9[i])
                for i in changes7[2]],
            ShrinkToCenter(quad_form8[25]),
            ShrinkToCenter(quad_form8[21]))
        caption9t = TextMobject('Now isolate ', 'x').to_edge(UP)
        self.play(ReplacementTransform(caption8t, caption9t))
        caption10 = TextMobject('Quadratic Formula').scale(3).to_edge(UP)
        caption10.set_color('#FFF200')
        self.wait(1)
        quad_form10 = TexMobject('x', '=', '{', '-', 'b', '\\pm', '\\sqrt', '{', 'b', '^2', '-',
                                 '4', 'a', 'c', '}', '\\over', '2', 'a', '}').scale(2)
        quad_form10[0].set_color(RED)
        for i in [12, 17]:
            quad_form10[i].set_color(GREEN)
        for i in [4, 8, 9]:
            quad_form10[i].set_color(BLUE)
        quad_form10[13].set_color('#9966CB')
        changes8 = [
            # Delete 4
            (0, 1, 3, 5, 6, 8, 10, 11, 13, 14, 15, 16, 17, 18, 20, 21, 22),
            (0, 3, 4, 16, 17, 1, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form9[i], quad_form10[z])
                for i, z in zip(changes8[0], changes8[1])],
            FadeOut(quad_form9[4]))
        self.play(ShrinkToCenter(caption9t),
                  FadeInFrom(caption10, DOWN, run_time=4))


def x_square():
    return Polygon(*POINTS[[4,1,5,6]],fill_color='#800000', fill_opacity=0.5)


def ax_b():
    return Polygon(*POINTS[[7,4,6,8]], fill_color='#0080FE', fill_opacity=0.5)


def small_square(UL):
    coords = np.array([
        [UL[0], UL[1], 0],
        [UL[0] + 1, UL[1], 0],
        [UL[0] + 1, UL[1] - 1, 0],
        [UL[0], UL[1] - 1, 0]
    ])
    return Polygon(*coords[[0,1,2,3]], fill_color='#388143', fill_opacity=0.5)


def bot_rec():
    return Polygon(*POINTS[[6,5,2,10]], fill_color='#0080FE', fill_opacity=0.5)


def left_rec():
    return Polygon(*POINTS[[0,4,6,9]], fill_color='#0080FE', fill_opacity=0.5)


def c_rec():
    return Polygon(*POINTS[[11,12,13,14]], fill_color='#B1560F', fill_opacity=0.5)

