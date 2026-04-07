from manim import *


class BackpropPremiumScene(MovingCameraScene):
    """Premium end-to-end backpropagation explainer (Scenes 1-9)."""

    def construct(self):
        # ------------------------------------------------------------------
        # Visual system
        # ------------------------------------------------------------------
        self.camera.background_color = "#14171C"  # dark charcoal

        blue_a = "#7BC4FF"  # activations
        blue_b = "#4D8DFF"  # signal travel
        blue_c = "#2C5FD5"  # node core
        brown = "#B9825A"  # loss/error/gradients
        fg_soft = GRAY_B

        # ------------------------------------------------------------------
        # Base layout: centered network
        # ------------------------------------------------------------------
        x_in, x_h, x_out = -4.2, -0.5, 3.4
        input_y = [1.8, 0.6, -0.6, -1.8]
        hidden_y = [1.2, 0.0, -1.2]
        output_y = [0.0]

        def build_nodes(x, ys):
            nodes = VGroup()
            for y in ys:
                halo = Circle(radius=0.29, stroke_width=0, fill_color=blue_b, fill_opacity=0.14)
                core = Circle(radius=0.18, stroke_color=blue_a, stroke_width=1.6, fill_color=blue_c, fill_opacity=0.95)
                nodes.add(VGroup(halo, core).move_to([x, y, 0]))
            return nodes

        in_nodes = build_nodes(x_in, input_y)
        h_nodes = build_nodes(x_h, hidden_y)
        out_nodes = build_nodes(x_out, output_y)

        def fully_connect(left, right):
            edges = VGroup()
            for l in left:
                for r in right:
                    edges.add(
                        Line(
                            l.get_center(),
                            r.get_center(),
                            stroke_color=blue_b,
                            stroke_width=1.4,
                            stroke_opacity=0.34,
                        )
                    )
            return edges

        e_in_h = fully_connect(in_nodes, h_nodes)
        e_h_out = fully_connect(h_nodes, out_nodes)
        net = VGroup(e_in_h, e_h_out, in_nodes, h_nodes, out_nodes)

        title = Text("Backpropagation", font_size=46, color=BLUE_A).to_edge(UP, buff=0.45)
        subtitle = Text("A visual intuition for learning", font_size=24, color=fg_soft).next_to(title, DOWN, buff=0.12)

        label_in = Text("Input", font_size=20, color=fg_soft).next_to(in_nodes, DOWN, buff=0.45)
        label_h = Text("Hidden", font_size=20, color=fg_soft).next_to(h_nodes, DOWN, buff=0.45)
        label_out = Text("Output", font_size=20, color=fg_soft).next_to(out_nodes, DOWN, buff=0.45)

        self.play(FadeIn(title, shift=0.2 * UP), FadeIn(subtitle, shift=0.2 * UP), run_time=1.4)
        self.play(self.camera.frame.animate.scale(0.95), run_time=1.4)
        self.play(
            FadeIn(VGroup(in_nodes, h_nodes, out_nodes), lag_ratio=0.08, scale=0.92),
            FadeIn(VGroup(e_in_h, e_h_out)),
            FadeIn(VGroup(label_in, label_h, label_out)),
            run_time=2.1,
        )

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------
        def flow(edge, color, rt=0.3):
            dot = Dot(radius=0.05, color=color).move_to(edge.get_start())
            trail = TracedPath(dot.get_center, stroke_color=color, stroke_width=2.2, dissipating_time=0.35)
            self.add(trail, dot)
            self.play(
                edge.animate.set_stroke(color=color, opacity=0.92, width=2.5),
                dot.animate.move_to(edge.get_end()),
                run_time=rt,
                rate_func=smooth,
            )
            self.play(edge.animate.set_stroke(color=blue_b, opacity=0.34, width=1.4), FadeOut(dot), run_time=0.12)
            self.remove(trail)

        def pulse_nodes(nodes, fill_color, rt=0.35):
            self.play(
                *[
                    AnimationGroup(
                        n[0].animate.set_fill(fill_color, opacity=0.26),
                        n[1].animate.set_fill(fill_color, opacity=0.98),
                        run_time=rt,
                    )
                    for n in nodes
                ],
                lag_ratio=0.12,
            )

        # ------------------------------------------------------------------
        # Scene 1: forward signal enters network
        # ------------------------------------------------------------------
        x_text = Text("sample x", font_size=24, color=blue_a).next_to(in_nodes, LEFT, buff=0.85)
        self.play(FadeIn(x_text, shift=0.2 * RIGHT), run_time=0.8)

        self.play(AnimationGroup(*[Flash(n[0].get_center(), color=blue_a, flash_radius=0.34, num_lines=10, run_time=0.5) for n in in_nodes], lag_ratio=0.1), run_time=1.2)
        for edge in e_in_h:
            flow(edge, blue_a, rt=0.2)
        pulse_nodes(h_nodes, blue_b)
        for edge in e_h_out:
            flow(edge, blue_a, rt=0.3)
        pulse_nodes(out_nodes, blue_a)

        # ------------------------------------------------------------------
        # Scene 2: prediction vs truth
        # ------------------------------------------------------------------
        pred = MathTex(r"\hat{y}=0.82", color=blue_a, font_size=42).next_to(out_nodes, RIGHT, buff=0.55)
        truth = MathTex(r"y=1.00", color=WHITE, font_size=42).next_to(pred, DOWN, buff=0.25).align_to(pred, LEFT)
        mismatch = Brace(VGroup(pred, truth), RIGHT, color=brown)
        mismatch_txt = Text("mismatch", font_size=20, color=brown).next_to(mismatch, RIGHT, buff=0.15)

        self.play(FadeIn(pred, shift=0.15 * RIGHT), run_time=0.9)
        self.play(FadeIn(truth, shift=0.1 * RIGHT), run_time=0.8)
        self.play(GrowFromCenter(mismatch), FadeIn(mismatch_txt), run_time=0.8)

        # ------------------------------------------------------------------
        # Scene 3: loss appears
        # ------------------------------------------------------------------
        loss_eq = MathTex(r"L=(\hat{y}-y)^2", color=brown, font_size=48).to_edge(RIGHT, buff=1.0).shift(UP * 1.9)
        loss_dot = Dot(radius=0.11, color=brown).move_to(mismatch.get_center())
        loss_glow = Circle(radius=0.42, stroke_width=0, fill_color=brown, fill_opacity=0.22).move_to(loss_dot)

        self.play(FadeIn(loss_glow), FadeIn(loss_dot), run_time=0.55)
        self.play(TransformFromCopy(VGroup(pred, truth), loss_eq), run_time=1.2)
        self.play(loss_glow.animate.scale(1.3).set_opacity(0.16), run_time=0.7)
        self.wait(0.7)

        # ------------------------------------------------------------------
        # Scene 4: begin backprop (brown reverse flow)
        # ------------------------------------------------------------------
        back_label = Text("error flows backward", font_size=22, color=brown).next_to(loss_eq, DOWN, buff=0.2).align_to(loss_eq, LEFT)
        self.play(FadeIn(back_label, shift=0.1 * DOWN), run_time=0.6)

        dL_da = MathTex(r"\frac{\partial L}{\partial a^{(2)}}", color=brown, font_size=36).next_to(out_nodes, UP, buff=0.4)
        self.play(Write(dL_da), run_time=0.7)

        for edge in reversed(e_h_out):
            rev = edge.copy().reverse_points()
            flow(rev, brown, rt=0.27)
        pulse_nodes(h_nodes, brown)

        dL_da1 = MathTex(r"\frac{\partial L}{\partial a^{(1)}}", color=brown, font_size=34).next_to(h_nodes, UP, buff=0.45)
        self.play(TransformFromCopy(dL_da, dL_da1), run_time=0.7)
        for edge in reversed(e_in_h):
            rev = edge.copy().reverse_points()
            flow(rev, brown, rt=0.2)

        # ------------------------------------------------------------------
        # Scene 5: chain rule visualization
        # ------------------------------------------------------------------
        chain = MathTex(
            r"\frac{\partial L}{\partial w}",
            r"=",
            r"\frac{\partial L}{\partial a}",
            r"\cdot",
            r"\frac{\partial a}{\partial z}",
            r"\cdot",
            r"\frac{\partial z}{\partial w}",
            color=WHITE,
            font_size=40,
        ).to_edge(DOWN, buff=0.55)
        chain[0].set_color(brown)
        chain[2].set_color(brown)
        chain[4].set_color(brown)
        chain[6].set_color(brown)

        self.play(Write(chain[0:2]), run_time=0.65)
        self.play(Write(chain[2]), run_time=0.55)
        self.play(Write(chain[3:5]), run_time=0.55)
        self.play(Write(chain[5:7]), run_time=0.55)

        scale_boxes = VGroup(
            SurroundingRectangle(chain[2], color=brown, buff=0.08, stroke_width=1.4),
            SurroundingRectangle(chain[4], color=brown, buff=0.08, stroke_width=1.4),
            SurroundingRectangle(chain[6], color=brown, buff=0.08, stroke_width=1.4),
        )
        self.play(LaggedStart(*[Create(b) for b in scale_boxes], lag_ratio=0.2), run_time=1.0)
        self.play(scale_boxes.animate.set_stroke(opacity=0.35), run_time=0.5)

        # ------------------------------------------------------------------
        # Scene 6: individual weights and gradients
        # ------------------------------------------------------------------
        tracked_edges = [e_h_out[0], e_h_out[1], e_h_out[2]]
        grad_labels = VGroup(
            MathTex(r"\frac{\partial L}{\partial w_1}", color=brown, font_size=30),
            MathTex(r"\frac{\partial L}{\partial w_2}", color=brown, font_size=30),
            MathTex(r"\frac{\partial L}{\partial w_3}", color=brown, font_size=30),
        )
        for i, (edge, g) in enumerate(zip(tracked_edges, grad_labels)):
            g.next_to(edge, RIGHT if i == 1 else UP, buff=0.15)
            self.play(edge.animate.set_stroke(color=brown, width=3.2, opacity=0.95), FadeIn(g), run_time=0.6)
            self.play(edge.animate.set_stroke(color=blue_b, width=1.4, opacity=0.34), run_time=0.35)

        # ------------------------------------------------------------------
        # Scene 7: gradient descent update
        # ------------------------------------------------------------------
        update_eq = MathTex(r"w \leftarrow w-\eta\frac{\partial L}{\partial w}", color=WHITE, font_size=46).move_to([0, 2.5, 0])
        update_eq[4:].set_color(brown)
        self.play(TransformMatchingTex(chain.copy(), update_eq), run_time=1.1)

        old_w = MathTex(r"w_1=0.80", r"\quad", r"w_2=-0.45", r"\quad", r"w_3=0.30", font_size=30, color=blue_a).next_to(update_eq, DOWN, buff=0.22)
        new_w = MathTex(r"w_1=0.86", r"\quad", r"w_2=-0.32", r"\quad", r"w_3=0.41", font_size=30, color=blue_a).move_to(old_w)
        self.play(FadeIn(old_w, shift=0.1 * DOWN), run_time=0.7)
        self.play(Transform(old_w, new_w), run_time=1.0)

        self.play(
            tracked_edges[0].animate.set_stroke(width=2.0, opacity=0.50),
            tracked_edges[1].animate.set_stroke(width=2.0, opacity=0.50),
            tracked_edges[2].animate.set_stroke(width=2.0, opacity=0.50),
            run_time=0.6,
        )

        # ------------------------------------------------------------------
        # Scene 8: forward pass again, improved prediction + reduced loss
        # ------------------------------------------------------------------
        self.play(FadeOut(VGroup(back_label, dL_da, dL_da1, mismatch, mismatch_txt, loss_glow, loss_dot, *grad_labels)), run_time=0.8)

        for edge in e_in_h:
            flow(edge, blue_a, rt=0.14)
        for edge in e_h_out:
            flow(edge, blue_a, rt=0.2)

        new_pred = MathTex(r"\hat{y}=0.95", color=blue_a, font_size=42).move_to(pred)
        smaller_loss = MathTex(r"L=(0.95-1.00)^2", color=brown, font_size=38).move_to(loss_eq)
        self.play(Transform(pred, new_pred), run_time=0.8)
        self.play(Transform(loss_eq, smaller_loss), run_time=0.8)

        improve_arrow = Arrow(pred.get_bottom(), truth.get_top(), buff=0.08, color=blue_a, stroke_width=2.2)
        improve_txt = Text("closer to truth", font_size=20, color=blue_a).next_to(improve_arrow, RIGHT, buff=0.1)
        self.play(GrowArrow(improve_arrow), FadeIn(improve_txt), run_time=0.8)

        calm_error = Circle(radius=0.22, stroke_color=brown, stroke_width=1.4, fill_color=brown, fill_opacity=0.08).next_to(loss_eq, LEFT, buff=0.22)
        self.play(Create(calm_error), run_time=0.6)

        # ------------------------------------------------------------------
        # Scene 9: final summary frame
        # ------------------------------------------------------------------
        summary = VGroup(
            Text("Forward pass", font_size=26, color=blue_a),
            Text("→ Prediction", font_size=26, color=blue_a),
            Text("Loss", font_size=26, color=brown),
            Text("→ Error", font_size=26, color=brown),
            Text("Backward pass", font_size=26, color=brown),
            Text("→ Gradients", font_size=26, color=brown),
            Text("Weight update", font_size=26, color=blue_a),
            Text("→ Better prediction", font_size=26, color=blue_a),
        ).arrange_in_grid(rows=4, cols=2, buff=(0.55, 0.45), col_alignments="ll")
        summary_box = SurroundingRectangle(summary, color=GRAY_C, buff=0.35, stroke_width=1.1)
        summary_group = VGroup(summary_box, summary).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)

        self.play(self.camera.frame.animate.scale(1.03).shift(LEFT * 1.0), run_time=1.1)
        self.play(FadeIn(summary_group, shift=0.18 * UP), run_time=1.1)
        self.play(Indicate(summary[1], color=blue_a), Indicate(summary[5], color=brown), Indicate(summary[7], color=blue_a), run_time=1.3)

        final_note = Text("Blue: computation   •   Brown: correction", font_size=20, color=fg_soft).next_to(summary_group, DOWN, buff=0.25)
        self.play(FadeIn(final_note), run_time=0.7)
        self.wait(1.8)
