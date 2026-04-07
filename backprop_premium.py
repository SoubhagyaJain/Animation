from manim import *


class BackpropPremiumScene1(MovingCameraScene):
    """Scene 1: Introduce a simple feedforward network with premium visual language."""

    def construct(self):
        # --- Art direction -------------------------------------------------
        self.camera.background_color = "#14171C"  # dark charcoal

        # Blues: activations/signals/forward flow
        blue_primary = "#7BC4FF"
        blue_mid = "#4D8DFF"
        blue_deep = "#2C5FD5"

        # Warm accent for later scenes (declared now for continuity)
        warm_brown = "#B9825A"

        # Typography
        title = Text(
            "Backpropagation",
            font_size=48,
            weight=MEDIUM,
            color=BLUE_A,
        ).to_edge(UP, buff=0.5)

        subtitle = Text(
            "How a network learns from error",
            font_size=24,
            color=GRAY_B,
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title, shift=0.2 * UP), FadeIn(subtitle, shift=0.2 * UP), run_time=1.6)

        # --- Network geometry (centered, readable) ------------------------
        layer_x = [-4.2, -0.3, 3.6]
        input_y = [1.8, 0.6, -0.6, -1.8]
        hidden_y = [1.2, 0.0, -1.2]
        output_y = [0.0]

        def make_nodes(x, ys):
            nodes = VGroup()
            for y in ys:
                core = Circle(radius=0.18, stroke_width=1.6, stroke_color=blue_primary, fill_color=blue_deep, fill_opacity=0.9)
                halo = Circle(radius=0.28, stroke_width=0, fill_color=blue_mid, fill_opacity=0.16)
                node = VGroup(halo, core).move_to([x, y, 0])
                nodes.add(node)
            return nodes

        input_nodes = make_nodes(layer_x[0], input_y)
        hidden_nodes = make_nodes(layer_x[1], hidden_y)
        output_nodes = make_nodes(layer_x[2], output_y)

        network_nodes = VGroup(input_nodes, hidden_nodes, output_nodes)

        input_label = Text("Input", font_size=22, color=GRAY_B).next_to(input_nodes, DOWN, buff=0.45)
        hidden_label = Text("Hidden", font_size=22, color=GRAY_B).next_to(hidden_nodes, DOWN, buff=0.45)
        output_label = Text("Output", font_size=22, color=GRAY_B).next_to(output_nodes, DOWN, buff=0.45)

        def connect_layers(left_layer, right_layer):
            edges = VGroup()
            for left_node in left_layer:
                for right_node in right_layer:
                    line = Line(
                        left_node.get_center(),
                        right_node.get_center(),
                        stroke_color=blue_mid,
                        stroke_width=1.4,
                        stroke_opacity=0.35,
                    )
                    edges.add(line)
            return edges

        edges_ih = connect_layers(input_nodes, hidden_nodes)
        edges_ho = connect_layers(hidden_nodes, output_nodes)
        network_edges = VGroup(edges_ih, edges_ho)

        # Subtle camera settle-in for cinematic calm
        self.play(self.camera.frame.animate.scale(0.96).move_to(ORIGIN), run_time=1.8)

        self.play(
            LaggedStart(
                *[FadeIn(node, scale=0.85) for node in network_nodes],
                lag_ratio=0.08,
            ),
            FadeIn(network_edges),
            FadeIn(input_label),
            FadeIn(hidden_label),
            FadeIn(output_label),
            run_time=2.6,
        )

        # --- Sample input signal ------------------------------------------
        sample_tag = Text("sample x", font_size=24, color=blue_primary)
        sample_tag.next_to(input_nodes, LEFT, buff=0.9)
        sample_dot = Dot(radius=0.08, color=blue_primary)
        sample_dot.move_to(sample_tag.get_right() + RIGHT * 0.22)

        self.play(FadeIn(sample_tag, shift=0.15 * RIGHT), FadeIn(sample_dot, scale=0.6), run_time=1.2)

        # Input node activation sequence
        input_pulses = []
        for n in input_nodes:
            input_pulses.append(Flash(n[0].get_center(), color=blue_primary, flash_radius=0.35, line_length=0.08, num_lines=10, run_time=0.5))
        self.play(
            AnimationGroup(*input_pulses, lag_ratio=0.12),
            run_time=1.6,
        )

        # Forward flow helper
        def flow_on_edge(edge, color, run_time=0.45):
            traveler = Dot(radius=0.05, color=color).move_to(edge.get_start())
            trace = TracedPath(traveler.get_center, stroke_color=color, stroke_width=2.0, dissipating_time=0.35)
            self.add(trace, traveler)
            self.play(
                edge.animate.set_stroke(color=color, opacity=0.9, width=2.4),
                traveler.animate.move_to(edge.get_end()),
                run_time=run_time,
                rate_func=smooth,
            )
            self.play(edge.animate.set_stroke(color=blue_mid, opacity=0.35, width=1.4), FadeOut(traveler), run_time=0.15)
            self.remove(trace)

        # Step 1: input -> hidden
        for edge in edges_ih:
            flow_on_edge(edge, blue_primary, run_time=0.24)

        # Hidden activation after incoming signals
        self.play(
            *[
                AnimationGroup(
                    n[0].animate.set_fill(blue_primary, opacity=0.30),
                    n[1].animate.set_fill(blue_mid, opacity=1.0),
                    run_time=0.35,
                )
                for n in hidden_nodes
            ],
            lag_ratio=0.12,
        )

        # Step 2: hidden -> output
        for edge in edges_ho:
            flow_on_edge(edge, blue_primary, run_time=0.35)

        # Output highlight
        self.play(
            output_nodes[0][0].animate.set_fill(blue_primary, opacity=0.35),
            output_nodes[0][1].animate.set_fill(blue_primary, opacity=1.0),
            Circumscribe(output_nodes[0], color=blue_primary, stroke_width=2.0, run_time=0.9),
            run_time=1.0,
        )

        pred_text = Text("prediction", font_size=24, color=blue_primary).next_to(output_nodes, RIGHT, buff=0.55)
        self.play(FadeIn(pred_text, shift=0.2 * RIGHT), run_time=0.9)

        # Hold for readability
        self.wait(1.3)

        # Keep warm accent visible in palette cue for continuity into scene 2+
        accent_sw = Dot(radius=0.06, color=warm_brown).next_to(subtitle, RIGHT, buff=0.35)
        self.play(FadeIn(accent_sw, scale=0.6), run_time=0.6)
        self.wait(0.4)
