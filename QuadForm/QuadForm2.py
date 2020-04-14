from manimlib.imports import *


#Quad Final
class QuadForm(Scene):
    def construct(self):
        # Intro
        peter = TextMobject('Peter Gilliam').scale(4).to_edge(UP)
        peter.set_color('#800000')
        intro_text = TextMobject('We all know the quadratic equation,'
                                 ).scale(1.75).next_to(peter,DOWN)
        intro_text2 = TextMobject('but where does it come from?'
                                  ).scale(1.75).next_to(intro_text,DOWN)
        intro_text3 = TextMobject("Let's solve for it and find out!"
                                  ).scale(1.75).next_to(intro_text2,DOWN)
        peter2 = TextMobject('Peter Gilliam')
        peter2.scale(0.5)
        peter2.to_edge(DL)
        peter2.set_color('#666666')
        self.add_sound('sorry_i_like_you',time_offset=1)
        self.add(peter)
        self.wait(2)
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
        # 3 Caption Top
        # Distributive Law of Multiplication
        caption3t = TextMobject("Foiling Tells us that squaring a binomial gives us"
                                ).to_edge(UP)
        capeq = TexMobject('\\left( n + m \\right) ^2 = n^2 + 2nm + m^2'
                           ).next_to(caption3t,DOWN)
        capeq2 = TexMobject('n^2','+','2','m','n','+','m^2','=',' \\left(','n','+m \\right) ^2'
                            ).move_to(capeq)
        for i in [0,4,9]:
            capeq2[i].set_color(RED)
        self.play(
            FadeOutAndShiftDown(caption3d),
            Write(caption3t),
            Write(capeq)
        )
        self.wait(2)
        self.play(ShrinkToCenter(capeq),
                  GrowFromCenter(capeq2))
        caption3d2 = TextMobject('That equation can be used to create a perfect square'
                                 ).to_edge(DOWN)
        self.wait(2)
        self.play(Write(caption3d2.scale(0.75)))

        # Completing the Square

        # Left Equations
        quad_formC = quad_form2.copy()
        quad_formC.scale(0.33)
        quad_formC.to_edge(LEFT)
        quad_formC.move_to(np.array([quad_formC.get_coord(0),-1,0]))
        Csquare = capeq2.copy()
        Csquare.to_edge(LEFT)
        Csquare.move_to(np.array([Csquare.get_coord(0),1,0]))
        caption3tE = TextMobject("We're interested in the left side of each ",
                                 'equation right now').to_edge(UP)
        caption3t2 = TextMobject('Our Equation is missing the last "m" term').to_edge(UP)
        caption3t3 = TextMobject("So we have to find the term and add it").to_edge(DOWN)

        self.play(ReplacementTransform(quad_form2, quad_formC),
                  ReplacementTransform(capeq2, Csquare),
                  FadeOutAndShiftDown(caption3d2))
        self.play(ReplacementTransform(caption3t, caption3tE))
        self.wait(1)
        self.play(FadeOutAndShiftDown(Csquare[7:]),
                  FadeOutAndShiftDown(quad_formC[9:]))
        self.wait(1)
        self.play(ReplacementTransform(caption3tE, caption3t2))
        self.wait(3)
        self.play(ReplacementTransform(caption3t2.copy(), caption3t3))
        # Right side Equations
        term1 = TexMobject('n^2','=','x^2').to_edge(RIGHT).shift([0,2,0])
        term1[0].set_color(RED)
        term1[2].set_color(RED)
        # Create mid right side equation, copy, than move origonal
        term2 = TexMobject('2','m','n','=','{','b','\\over','a','}','x')
        term2[2].set_color(RED)
        term2[9].set_color(RED)
        term2[5].set_color(BLUE)
        term2[7].set_color(GREEN)
        term2b = term2.copy()
        term2.to_edge(RIGHT)
        term2b.scale(2.5)

        term3 = TexMobject('n','=','x').move_to(term1)
        term3[2].set_color(RED)
        term3[0].set_color(RED)
        termM = TexMobject('m^2','=?').to_edge(RIGHT,1).shift([0,-2,0])
        # Building the right side equations
        self.play(Write(term1[1],run_time=2),
                  ReplacementTransform(quad_formC[0].copy(),term1[2],run_time=2),
                  ReplacementTransform(Csquare[0].copy(),term1[0]),run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(term1,term3))
        self.wait(1)
        self.play(Write(term2[3]),
            *[ReplacementTransform(Csquare[i].copy(),term2[z],run_time=2)
                for i,z in zip([2,3,4],[0,1,2])],
            *[ReplacementTransform(quad_formC[i].copy(), term2[i+1],run_time=2)
                for i in range(4,9)])


        self.wait(1)
        self.play(Write(termM[1]),
                  ReplacementTransform(Csquare[5].copy(),termM[0]))
        term_no_n = TexMobject('2','m','=','{','b','\\over ','a','}').scale(2.5)
        term_no_n[4].set_color(BLUE)
        term_no_n[6].set_color(GREEN)
        self.wait(1)
        self.play(ReplacementTransform(term2,term2b))
        self.wait(2)
        # self.play(ReplacementTransform(term2b,term_no_n))
        changes1b = [
            (0,1,3,5,6,7),
            (0,1,2,4,5,6)]
        self.play(
            *[ReplacementTransform(
                term2b[i], term_no_n[z])
                for i, z in zip(changes1b[0], changes1b[1])],
            FadeOutAndShiftDown(term2b[2]),
            FadeOutAndShiftDown(term2b[9]))
        self.wait(2)
        term4 = TexMobject('m','=','{','b','\\over','2','a','}').scale(2)
        term4[3].set_color(BLUE)
        term4[5].set_color(GREEN)
        term4b = term4.copy()
        term4b.scale(0.5).to_edge(RIGHT)
        term5 = TexMobject('m^2={','b','^2 \\over 4','a^2').move_to(termM)
        term5[1].set_color(BLUE)
        term5[3].set_color(GREEN)
        # self.play(ReplacementTransform(term_no_n, term4))
        changes1c = [
            (0,1,2,4,5,6),
            (5,0,1,3,4,6)]
        self.play(
            *[ReplacementTransform(
                term_no_n[i], term4[z])
                for i, z in zip(changes1c[0], changes1c[1])]
        )
        self.wait(2)
        self.play(ReplacementTransform(term4,term4b))
        self.wait(1)
        self.play(ReplacementTransform(termM, term5))
        self.wait(1)
        # 4 Main

        quad_form3 = TexMobject('x', '^2', '+', '{','b', '\\over', 'a','}', 'x',
                                '=', '-', '{','c', '\\over', 'a','}').scale(2)
        for i in [0, 1, 8]:
            quad_form3[i].set_color(RED)
        quad_form3[6].set_color(GREEN)
        quad_form3[14].set_color(GREEN)
        quad_form3[4].set_color(BLUE)
        quad_form3[12].set_color('#9966CB')
        termM2 = term5.copy().next_to(quad_form3,DOWN)
        caption4t = TextMobject('Dont Forget to add to BOTH sides!').to_edge(UP)
        self.play(FadeOutAndShiftDown(Csquare),
                  FadeOutAndShiftDown(term3),
                  FadeOutAndShiftDown(term4b),
                  FadeOutAndShift(caption3t2,UP),
                  ReplacementTransform(quad_formC,quad_form3),
                  ReplacementTransform(term5, termM2),
                  ReplacementTransform(caption3t3,caption4t))
        self.wait(1)
        quad_form4 = TexMobject('x','^2','+','{','b','\\over','a','}','x','+'
                                '{','b','^2','\\over','4','a','^2','}','=','-',
                                '{','c','\\over','a','}','+','{','b^2','\\over',
                                '4','a','^2').scale(2)
        for i in [0,1,8]:
            quad_form4[i].set_color(RED)
        for i in [6,14,15,22,29,30]:
            quad_form4[i].set_color(GREEN)
        for i in [4,10,11,26]:
            quad_form4[i].set_color(BLUE)
        quad_form4[20].set_color('#9966CB')
        changes2 = [
            (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),
            (0,1,2,3,4,5,6,7,8,17,18,19,20,21,22,23)
        ]
        self.play(
            *[
                ReplacementTransform(
                    quad_form3[i], quad_form4[z])
                for i, z in zip(changes2[0], changes2[1])],
            ReplacementTransform(termM2.copy(), quad_form4[24:]),
            ReplacementTransform(termM2.copy(), quad_form4[9:17]),
            ShrinkToCenter(termM2)
        )
        self.wait(1)
        # 5

        # Top Caption
        caption5t = TextMobject('The Left Side Can Now Be Re-Writen as a '+
                                'Perfect Square').to_edge(UP)
        # Perfect Square Tranform Example/Formula
        PSquare = TexMobject('n^2','+','2m','n','+','m^2','=',' \\left( ','n','+m \\right) ^2'
                             ).to_edge(DOWN)
        self.play(ReplacementTransform(caption4t, caption5t))
        self.play(Write(PSquare[0:7]))
        self.wait(1)
        self.play(ReplacementTransform(PSquare[0:6],PSquare[7:]))
        self.wait(1)
        # Main

        quad_form5 = TexMobject('\\left(','x','+','{','b','\\over','2','a','}','\\right)',
                                '^2','=','-','{','c','\\over','a','}','+','{','b','^2',
                                '\\over','4','a','^2','}').scale(2)
        quad_form5[1].set_color(RED)
        for i in [7,16,24,25]:
            quad_form5[i].set_color(GREEN)
        for i in [4,20,21]:
            quad_form5[i].set_color(BLUE)
        quad_form5[14].set_color('#9966CB')
        changes3 = [
            # Changes
            (0,1,2,3,4,5,6,7,13,17),
            (1,10,2,0,4,5,7,9,6,11),
            # Deletions
            (8,9,10,12,14,15,16),
            # Shifts
            (17,18,19,20,21,22,23,24,25,26,27,28,29,30),
            (11,12,13,14,15,16,17,18,19,20,22,23,24,25)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form4[i],quad_form5[z])
                for i,z in zip(changes3[0],changes3[1])],
            *[ShrinkToCenter(quad_form4[i])
                for i in changes3[2]],
            *[ReplacementTransform(quad_form4[i], quad_form5[z])
                for i,z in zip(changes3[3],changes3[4])],
            ReplacementTransform(quad_form4[11],quad_form5[21]),
            FadeOutAndShiftDown(PSquare))
        # Review Time!
        quad_form5_copy = quad_form5.copy()
        mini_quad5 = quad_form5.copy().to_edge(DOWN).scale(0.75)
        pause_cap = TextMobject("PAUSE").scale(8)
        recap = TextMobject('Quick Review').scale(2).to_edge(UP)
        recap.set_color('#FFF200')
        recap_1 = TextMobject('By adding ').next_to(recap,DOWN)
        recap_1.shift([-2.1,0,0])
        recap_2 = TexMobject('{ b^2 \\over 4a^2').next_to(recap_1,RIGHT)
        recap_3 = TextMobject('to both sides,').next_to(recap_2,RIGHT)
        recap_4 = TextMobject('The left side can now factor into a perfect square,'
                              ).next_to(recap,DOWN,buff=1.2)
        recap_5 = TextMobject('Moving ','x',' to only one term instead of two.'
                              ).next_to(recap_4,DOWN)
        recap_5[1].set_color(RED)
        recap_6 = TextMobject('Solving from here is a simple matter of Algebra'
                              ).next_to(recap_5,DOWN)
        self.play(GrowFromEdge(pause_cap,UP))
        self.wait(0.75)
        self.play(ShrinkToCenter(pause_cap))
        self.play(FadeOut(quad_form5, run_time=0),
                  FadeOut(caption5t),
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
        quad_form6 = TexMobject('\\left(','x','+','{','b','\\over','2','a','}','\\right)',
                                '^2','=','{','b','^2','-','4','a','c','\\over','4',
                                'a','^2','}').scale(2)
        quad_form6[1].set_color(RED)
        for i in [7,17,21,22]:
            quad_form6[i].set_color(GREEN)
        for i in [4,13,14]:
            quad_form6[i].set_color(BLUE)
        quad_form6[18].set_color('#9966CB')
        changes4 = [
            (12,14,16,20,21,22,23,24,25),
            (15,18,17,13,14,19,20,21,22),
            (15,18),
            (0,1,2,3,4,5,6,7,8,9,10,11)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form5[i], quad_form6[z])
                for i,z in zip(changes4[0],changes4[1])],
            *[ReplacementTransform(
                quad_form5[i], quad_form6[i])
                for i in changes4[3]],
            ShrinkToCenter(quad_form5[18]),
            ReplacementTransform(quad_form5[15],quad_form6[16]))
        # 7 MAIN
        caption7t = TextMobject('Now we can take the square root of both sides'
                                ).to_edge(UP)
        self.play(ReplacementTransform(caption6t,caption7t))
        self.wait(2)
        quad_form7 = TexMobject('\\sqrt','{','\\left(','x','+','{','b','\\over','2','a','}',
                                '\\right)','^2','}','=','\\sqrt','{','b','^2','-','4',
                                'a','c','\\over','4','a','^2','}','}').scale(2)
        quad_form7[3].set_color(RED)
        for i in [9,21,25,26]:
            quad_form7[i].set_color(GREEN)
        for i in [6,17,18]:
            quad_form7[i].set_color(BLUE)
        quad_form7[22].set_color('#9966CB')

        changes5 = [[],[],[0,15]]
        for i in range(0,11):
            changes5[0].append(i)
        for i in range(12,23):
            changes5[1].append(i)

        self.play(
            *[ReplacementTransform(quad_form6[i],quad_form7[i+2])
                for i in changes5[0]],
            *[ReplacementTransform(quad_form6[i],quad_form7[i+4])
                for i in changes5[1]],
            ReplacementTransform(quad_form6[11], quad_form7[14]),
            *[GrowFromCenter(quad_form7[i])
                for i in changes5[2]])
        caption8t = TextMobject('Almost There! Now simplify').to_edge(UP)
        self.play(ReplacementTransform(caption7t, caption8t))
        self.wait(1)
        quad_form8 = TexMobject('x','+','{','b','\\over','2','a','}','=','{','\\pm','\\sqrt',
                                '{','b','^2','-','4','a','c','}','\\over','\\sqrt','{',
                                '4','a','^2','}','}').scale(2)
        quad_form8[0].set_color(RED)
        for i in [6,17,24,25]:
            quad_form8[i].set_color(GREEN)
        for i in [3,13,14]:
            quad_form8[i].set_color(BLUE)
        quad_form8[18].set_color('#9966CB')
        changes6 =[
            (0,3,4,6,7,8,9,12,14,15,17,18,19,20,21,22,23,24,25,26),
            (21,0,1,3,4,5,6,10,8,11,13,14,15,16,17,18,20,23,24,25),
            (2,11)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form7[i], quad_form8[z])
                for i,z in zip(changes6[0],changes6[1])],
            ShrinkToCenter(quad_form7[2]),
            ShrinkToCenter(quad_form7[11]))
        self.wait(1)
        quad_form9 = TexMobject('x','+','{','b','\\over','2','a','}','=','{','\\pm','\\sqrt',
                                '{','b','^2','-','4','a','c','}','\\over','2','a','}'
                                ).scale(2)
        quad_form9[0].set_color(RED)
        for i in [6,22]:
            quad_form9[i].set_color(GREEN)
        for i in [3,13,14]:
            quad_form9[i].set_color(BLUE)
        quad_form9[18].set_color('#9966CB')
        changes7 = [[23,24],[21,22],[]]
        for i in range(0,21):
            changes7[2].append(i)
        self.play(
            *[ReplacementTransform(
                quad_form8[i],quad_form9[z])
                for i,z in zip(changes7[0],changes7[1])],
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
        quad_form10 = TexMobject('x','=','{','-','b','\\pm','\\sqrt','{','b','^2','-',
                                 '4','a','c','}','\\over','2','a','}').scale(2)
        quad_form10[0].set_color(RED)
        for i in [12,17]:
            quad_form10[i].set_color(GREEN)
        for i in [4,8,9]:
            quad_form10[i].set_color(BLUE)
        quad_form10[13].set_color('#9966CB')
        changes8 = [
            # Delete 4
            (0,1,3,5,6,8,10,11,13,14,15,16,17,18,20,21,22),
            (0,3,4,16,17,1,5,6,8,9,10,11,12,13,15,16,17)
        ]
        self.play(
            *[ReplacementTransform(
                quad_form9[i], quad_form10[z])
                for i, z in zip(changes8[0], changes8[1])],
            FadeOut(quad_form9[4]))
        self.play(ShrinkToCenter(caption9t),
                  FadeInFrom(caption10, DOWN, run_time=4))


