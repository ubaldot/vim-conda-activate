import manim as mn  # type:ignore
import numpy as np  # type:ignore
from scipy import ndimage, fft
from scipy.io import wavfile
from scipy.interpolate import PchipInterpolator
import imageio.v3 as iio
import sys


sys.path.append("/users/ubaldot/.manim")
import myconfig as mycfg  # type:ignore


class Temperature(mn.Scene):
    def setup(self):
        pass
        # self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        MAKE_SMOOTH = True

        self.next_section("Scroll signal", skip_animations=False)

        # Generic signal
        N = 288
        signal = np.random.default_rng().uniform(10, 28, N)
        Ts = 0.1

        # Low pass filter data
        Tc = 1.8  # Tc = 1/Fc, OBS! Tc>Ts
        signal_filt = np.zeros(len(signal))
        signal_filt[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            signal_filt[ii + 1] = (1 - Ts / Tc) * signal_filt[ii] + Ts / Tc * s

        axis_config_others = {
            "y_range": [0, 32, 32 / 10],
            "x_length": 11.0,
            "y_length": 6.0,
        }
        x_span = 5
        x_range = [0.0, x_span, 1]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        # x_label = ax.get_x_axis_label(mn.MathTex(r"\textrm{time [s]}", font_size=28), edge=mn.DR)
        # y_label = ax.get_y_axis_label(mn.MathTex("^\circ C").scale(0.45), edge=mn.UL)
        x_label = mn.MathTex(r"\textrm{time [h]}", font_size=28).next_to(ax, mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\textrm{Temperature [}^\circ \textrm{C}]}", font_size=28)
            .rotate(90 * mn.DEGREES)
            .next_to(ax, mn.LEFT, buff=0.2)
        )

        # Convert the direction [Ts,0,0] to POINTS
        STEP_DIR = ax.c2p(Ts, 0) - ax.c2p(0, 0)

        grid = mycfg.get_grid(ax)
        self.add(mn.VGroup(ax, x_label, y_label, grid))

        # INIT
        current_time = 0
        P0 = ax.c2p(current_time, signal_filt[0])
        current_time += Ts
        P1 = ax.c2p(current_time, signal_filt[1])
        signal_displayed = mn.Line(P0, P1)
        value_tex = mn.MathTex(f"{np.round_(signal_filt[1],1)}^\circ C", font_size=28).move_to(
            signal_displayed.get_end(), mn.RIGHT
        )
        self.add(signal_displayed, value_tex)
        self.add(signal_displayed)
        self.wait(Ts)

        # ITERATIONS
        for ii, _ in enumerate(signal_filt[1:]):
            # for ii in range(0):
            # Scroll once the plot reaches the displayed max x.
            if current_time + Ts > x_range[1]:
                x_range[0] += Ts
                x_range[1] += Ts

            ax_new = mn.Axes(
                axis_config=mycfg.axis_config,
                **axis_config_others,
                x_range=x_range,
            )

            # Update Axes
            self.remove(ax)
            self.add(ax_new)
            ax = ax_new

            # Display signal_filt
            if current_time + Ts < x_span or np.isclose(current_time + Ts, x_span):
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))
            else:
                signal_displayed.shift(-STEP_DIR)
                signal_displayed.points = signal_displayed.points[4:]
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))

            if MAKE_SMOOTH:
                signal_displayed.make_smooth()

            # Update number
            value_tex_new = mn.MathTex(f"{np.round_(signal_filt[ii],1)}^\circ C", font_size=28).next_to(
                signal_displayed.get_end(), mn.RIGHT
            )
            value_tex.become(value_tex_new)

            current_time += Ts
            self.wait(Ts)
        self.wait(Ts)


class BirdChirp(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        MAKE_SMOOTH = True

        self.next_section("Scroll signal", skip_animations=False)

        # Bird chirp
        wav_fname = "./BirdAudio.wav"
        fs, data = wavfile.read(wav_fname)
        # Pick one sample every 4800 and normalize
        step = int(2400 * 2)  # OBS This depends on the FPS! Ts cannot be too small!
        Ts = step / fs  # Ts > 2/fps
        print(Ts)
        signal_filt = data[1::step, 0] / max(data[1::step, 0])
        print(len(signal_filt))

        axis_config_others = {
            "y_range": [-1, 1, 1 / 10],
            "x_length": 11.0,
            "y_length": 6.0,
        }
        x_span = 5
        x_range = [0.0, x_span, x_span / 10]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        # x_label = ax.get_x_axis_label(mn.MathTex(r"\textrm{time [s]}", font_size=28), edge=mn.DR)
        # y_label = ax.get_y_axis_label(mn.MathTex("^\circ C").scale(0.45), edge=mn.UL)
        x_label = mn.MathTex(r"\textrm{time [s]}", font_size=28).next_to(ax, mn.DOWN, buff=0.2)
        y_label = mn.MathTex(r"\textrm{Amplitude}", font_size=28).rotate(90 * mn.DEGREES).next_to(ax, mn.LEFT, buff=0.2)

        # Convert the direction [Ts,0,0] to POINTS
        STEP_DIR = ax.c2p(Ts, 0) - ax.c2p(0, 0)
        self.add(mn.VGroup(ax, x_label, y_label))

        # INIT
        current_time = 0.0
        P0 = ax.c2p(current_time, signal_filt[0])
        current_time += Ts
        P1 = ax.c2p(current_time, signal_filt[1])
        signal_displayed = mn.Line(P0, P1)
        self.add(signal_displayed)
        self.wait(Ts)

        # ITERATIONS
        for ii, _ in enumerate(signal_filt[1:]):
            # for ii in range(0):
            # Scroll once the plot reaches the displayed max x.
            if current_time + Ts > x_range[1]:
                x_range[0] += Ts
                x_range[1] += Ts

            ax_new = mn.Axes(
                axis_config=mycfg.axis_config,
                **axis_config_others,
                x_range=x_range,
            )

            # Update Axes
            self.remove(ax)
            self.add(ax_new)
            ax = ax_new

            # Display signal_filt
            if current_time + Ts < x_span or np.isclose(current_time + Ts, x_span):
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))
            else:
                signal_displayed.shift(-STEP_DIR)
                signal_displayed.points = signal_displayed.points[4:]
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))

            if MAKE_SMOOTH:
                signal_displayed.make_smooth()

            current_time += Ts
            self.wait(Ts)
        self.wait(Ts)


class ScrollSignalWithUpdater(mn.Scene):
    def construct(self):
        Ts = 0.1
        N = 200
        times = [t for t in np.linspace(0, N * Ts, N)]
        signal = np.random.default_rng().uniform(20, 28, N)
        Ts = 0.2
        Tc = 1.8  # Tc = 1/Fc, OBS! Tc>Ts

        # Low pass filter data
        data = np.zeros(len(signal))
        data[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            data[ii + 1] = (1 - Ts / Tc) * data[ii] + Ts / Tc * s

        # Bird chirp
        wav_fname = "/users/ubaldot/Downloads/BirdAudio.wav"
        fs, data = wavfile.read(wav_fname)
        # Pick one sample every 4800 and normalize
        step = 2400  # OBS This depends on the FPS! Ts cannot be too small!
        Ts = step / fs
        print(Ts)
        data = data[1::step, 0] / max(data[1::step, 0])
        N = len(data)
        times = [t for t in np.linspace(0, N * Ts, N)]

        time = mn.ValueTracker(0)
        trange = 5.05  # OBS! trange/Ts shall not be an integer!

        plot = mn.VMobject()
        ax = mn.VMobject()
        value = mn.VMobject()
        graph = mn.VGroup(ax, plot, value)

        def graph_updater(vgrp):
            startt = max(time.get_value() - trange, 0)
            ax, plot, value = vgrp

            # Moving window of size trange. The window move with the ValueTracker. OBS! trange/Ts shall not be an integer!
            tempts = [t for t in times if startt <= t <= time.get_value()]
            tempds = [d for i, d in enumerate(data) if startt <= times[i] <= time.get_value()]

            # New axis
            if time.get_value() > trange:
                tmin = tempts[0]
                tmax = tmin + trange
            else:
                tmin = 0.0
                tmax = trange

            ax_new = mn.Axes(
                x_range=[tmin, tmax, trange / 10],
                y_range=[-1, 1, 0.2],
                x_length=10,
                y_length=5,
                axis_config=mycfg.axis_config,
            ).add_coordinates()

            # New plot
            plot_new = ax_new.plot_line_graph(tempts, tempds, add_vertex_dots=False)

            # New value
            # value_new = mn.MathTex(f"{np.round_(tempds[-1],1)}^\circ C", font_size=28)

            ax.become(ax_new)
            plot.become(plot_new)
            # value.become(value_new)

        graph.add_updater(graph_updater, call_updater=True)

        x_label = mn.MathTex(r"\mathrm{time [s]}", font_size=28).next_to(graph[0], mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\mathrm{Volume}", font_size=28).rotate(90 * mn.DEGREES).next_to(graph[0], mn.LEFT, buff=0.2)
        )
        self.add(graph, x_label, y_label)
        self.play(time.animate.set_value(times[-1]), rate_func=mn.rate_functions.linear, run_time=times[-1])


class QuarterlyRevenue(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        mycfg.axis_config["font_size"] = 28
        y_range = [0, 100, 10]
        x_range = [0, 5, 1]
        ax = mn.Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=10,
            y_length=5,
            axis_config=mycfg.axis_config,
        ).add_coordinates()

        x_label = mn.MathTex(r"\textrm{Quarters}", font_size=36).next_to(ax, mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\textrm{Renevue [M€]}", font_size=36).rotate(90 * mn.DEGREES).next_to(ax, mn.LEFT, buff=0.3)
        )

        lines = mn.VGroup()
        for ii in range(*y_range):
            point = ax.c2p(x_range[1], ii)
            line = ax.get_horizontal_line(
                point, line_func=mn.DashedLine, line_config={"stroke_opacity": 0.4, "dash_length": 0.1}
            )
            lines.add(line)

        Q1 = mn.Rectangle(height=0.01, width=1.2, fill_opacity=0.5).move_to(ax.c2p(1, 0), aligned_edge=mn.DOWN)
        Q2 = Q1.copy().move_to(ax.c2p(2, 0), aligned_edge=mn.DOWN)
        Q3 = Q1.copy().move_to(ax.c2p(3, 0), aligned_edge=mn.DOWN)
        Q4 = Q1.copy().move_to(ax.c2p(4, 0), aligned_edge=mn.DOWN)

        self.add(ax, x_label, y_label, Q1, Q2, Q3, Q4, lines)

        Q1.generate_target()
        Q1.target.stretch_to_fit_height(3, about_edge=mn.DOWN)

        Q2.generate_target()
        Q2.target.stretch_to_fit_height(2.1, about_edge=mn.DOWN)

        Q3.generate_target()
        Q3.target.stretch_to_fit_height(4.2, about_edge=mn.DOWN)

        Q4.generate_target()
        Q4.target.stretch_to_fit_height(2.6, about_edge=mn.DOWN)
        self.play(mn.MoveToTarget(Q1), mn.MoveToTarget(Q2), mn.MoveToTarget(Q3), mn.MoveToTarget(Q4), run_time=3)
        self.wait()


class Discretization_Quantization(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        # Generic signal
        N = 50
        signal = np.random.default_rng().uniform(-2, 2, N)
        Ts = 0.1
        times = np.linspace(0.0, N * Ts, N)

        # Low pass filter data
        Tc = 0.2  # Tc = 1/Fc, OBS! Tc>Ts
        signal_filt = np.zeros(len(signal))
        signal_filt[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            signal_filt[ii + 1] = (1 - Ts / Tc) * signal_filt[ii] + Ts / Tc * s

        mycfg.axis_config["font_size"] = 32
        y_range = [-1.9, 2, 1]
        axis_config_others = {
            "y_range": y_range,
            "x_length": 12.0,
            "y_length": 5.5,
        }
        x_span = N * Ts
        x_range = [0.0, x_span, 0.5]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        x_label = ax.get_x_axis_label(mn.Text("time", font_size=28), edge=mn.DR)
        continuous_points = [ax.c2p(_x, _y) for _x, _y in zip(times, signal_filt)]
        # print(f"A = {continuous_points[:2]}")
        # A, B, C = ax.c2p(times, signal_filt)
        # continuous_points = zip(*ax.c2p(times, signal_filt))
        # continuous_signal = mn.VMobject().set_points_smoothly(list(zip(continuous_points[0], continuous_points[1])))
        continuous_signal = mn.VMobject().set_points_smoothly(continuous_points)

        self.next_section("Discretization", skip_animations=False)
        # Sampling perios
        Tss = 0.5
        sampling_times = times[0 :: int(Tss / Ts)]
        samples = signal_filt[0 :: int(Tss / Ts)]
        discrete_points = [ax.c2p(_x, _y, 0) for _x, _y in zip(sampling_times, samples)]
        Dots = mn.VGroup()
        for p in discrete_points:
            Dots.add(mn.VGroup(ax.get_vertical_line(p), mn.Dot(p, color=mn.TEAL)))

        label0 = mn.MathTex(rf"Sampling\quad(T_s = {Tss})").to_edge(mn.DOWN)
        self.play(mn.Write(mn.VGroup(ax, x_label)))
        self.wait()
        self.play(mn.Write(continuous_signal))
        self.wait()
        self.play(mn.Write(label0))
        self.wait()
        self.play(mn.Write(Dots))
        self.wait()
        self.play(mn.FadeOut(continuous_signal))
        self.wait()
        self.play(mn.FadeOut(label0, Dots))
        self.wait()
        self.play(mn.FadeIn(continuous_signal))
        self.wait(1)

        Delta = 0.2
        label1 = mn.MathTex(rf"Quantization\quad(\Delta = {Delta})").to_edge(mn.DOWN)

        quantization_lines = mn.VGroup()
        q_bins = np.arange(y_range[0], y_range[1], Delta)
        for y in q_bins:
            quantization_lines.add(ax.get_horizontal_line(ax.c2p(x_span, y)))

        brace = mn.BraceBetweenPoints(
            quantization_lines[16].get_end(), quantization_lines[17].get_end(), buff=0
        ).stretch_to_fit_width(0.1)
        delta_tex = mn.MathTex(r"\Delta", font_size=32).next_to(brace, mn.RIGHT, buff=0.05)

        self.play(mn.ReplacementTransform(label0, label1))
        self.play(mn.FadeIn(quantization_lines, brace, delta_tex))
        self.wait()

        self.next_section("Quantization", skip_animations=False)

        # Quantize values
        q_signal = np.empty_like(signal_filt)
        for ii, val in enumerate(signal_filt):
            closest_value = min(q_bins, key=lambda x: np.abs(x - val))
            q_signal[ii] = closest_value
        quantized_points = [ax.c2p(_x, _y) for _x, _y in zip(times, q_signal)]

        quantized_curve = mn.VMobject(color=mn.YELLOW)
        t_step = quantized_points[1][0] - quantized_points[0][0]
        for ii in range(len(quantized_points) - 1):
            x0, y0, _ = quantized_points[ii]
            x1, y1, _ = quantized_points[ii + 1]
            l0 = mn.Line((x0, y0, 0), (x0 + t_step / 2, y0, 0))
            l1 = mn.Line((x0 + t_step / 2, y0, 0), (x0 + t_step / 2, y1, 0))
            l2 = mn.Line((x0 + t_step / 2, y1, 0), (x0 + t_step, y1, 0))
            quantized_curve.append_vectorized_mobject(l0)
            quantized_curve.append_vectorized_mobject(l1)
            quantized_curve.append_vectorized_mobject(l2)

        self.add(quantized_curve)
        self.play(mn.FadeIn(quantized_curve))
        self.play(mn.FadeOut(continuous_signal, brace, delta_tex))
        self.wait()

        self.next_section("Sampling and quantization", skip_animations=False)

        q_Dots = mn.VGroup()
        quantized_samples = q_signal[0 :: int(Tss / Ts)]
        quantized_sampled_points = [ax.c2p(_x, _y, 0) for _x, _y in zip(sampling_times, quantized_samples)]
        for p in quantized_sampled_points:
            x0 = p[0]
            y0 = ax.c2p(0, y_range[0], 0)[1] - 0.1
            y1 = ax.c2p(0, y_range[1], 0)[1] + 0.1
            # TODO: remove DashedLines from q_Dots
            q_Dots.add(mn.VGroup(mn.DashedLine((x0, y0, 0), (x0, y1, 0), stroke_opacity=0.4), mn.Dot(p, color=mn.RED)))

        label2 = mn.MathTex(
            rf"Quantization\,(\Delta = {Delta})\quad and \quad Sampling\,(T_s = 0.5)", font_size=36
        ).to_edge(mn.DOWN)

        self.play(mn.ReplacementTransform(label1, label2))
        self.play(mn.FadeIn(q_Dots))
        self.wait()
        self.play(mn.FadeOut(quantized_curve))
        self.wait()
        self.play(mn.FadeOut(quantization_lines))
        self.wait()


class Quantization(mn.Scene):
    def construct(self):
        N = 10
        Ts = 0.5
        y_values = np.random.default_rng().uniform(-2, 2, N)
        x_values = np.linspace(np.ceil(-N * Ts), np.floor(N * Ts), N)
        points = [(x, y, 0) for x, y in zip(x_values, y_values)]

        zoh_curve = mn.VMobject(color=mn.TEAL)
        t_step = x_values[1] - x_values[0]
        for ii in range(len(points) - 1):
            x0, y0, z0 = points[ii]
            x1, y1, z0 = points[ii + 1]
            l0 = mn.Line((x0, y0, z0), (x0 + t_step / 2, y0, z0))
            l1 = mn.Line((x0 + t_step / 2, y0, z0), (x0 + t_step / 2, y1, z0))
            l2 = mn.Line((x0 + t_step / 2, y1, z0), (x0 + t_step, y1, z0))
            zoh_curve.append_vectorized_mobject(l0)
            zoh_curve.append_vectorized_mobject(l1)
            zoh_curve.append_vectorized_mobject(l2)

        self.add(zoh_curve)

        # Alternative
        steps = []
        for x, x_next, y in zip(x_values, x_values[1:], y_values):
            steps.append([x, y, 0])
            steps.append([x_next, y, 0])
        steps.append([x_values[-1], y_values[-1], 0])

        curve = mn.VMobject().set_points_as_corners(steps)
        curve2 = mn.VMobject().set_points_as_corners(points).set_color(mn.RED)
        self.add(curve, curve2, zoh_curve)


class StreamLine(mn.Scene):
    def setup(self):
        img = (
            mn.ImageMobject("Pianta")
            .stretch_to_fit_width(mn.config.frame_width)
            .stretch_to_fit_height(mn.config.frame_height)
        )
        self.add(img)
        # self.add(mycfg.imageBG)
        plane = mn.NumberPlane()
        self.add(plane)

    def construct(self):
        def func(x):
            x_eq = np.array((2, 2))
            xdot = np.array([[1, 2], [-2, 1]]) @ (x[0:2] - x_eq)
            return np.array((xdot[0], xdot[1], 0))

        stream_lines = mn.StreamLines(
            func,
            max_anchors_per_line=20,
            opacity=0.8,
            stroke_width=2,
            max_color_scheme_value=2,
            colors=["#FFFFFF", "#FFFFFF"],
            virtual_time=5,
        )
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=0.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)


class PixelImage(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        self.next_section("Empty grid", skip_animations=False)
        N_pixels = 30
        rows, cols = (
            N_pixels,
            N_pixels,
        )  # Number of rows and columns in the grid

        # Filled grid
        im = iio.imread("./assets/IO.jpeg")
        # im = iio.imread("Io2.jpeg")
        im_resized = ndimage.zoom(im, (N_pixels / im.shape[0], N_pixels / im.shape[1], 1), order=3)
        filled_grid_original = mn.VGroup(
            *[
                mn.Square(
                    # 0.2,
                    6 / N_pixels,
                    stroke_width=0.0,
                    fill_opacity=1,
                    fill_color=mn.rgb_to_color(
                        (
                            im_resized[x, y, 0] / 255,
                            im_resized[x, y, 1] / 255,
                            im_resized[x, y, 2] / 255,
                        )
                    ),
                )
                for x in range(cols)
                for y in range(rows)
            ]
        ).arrange_in_grid(rows, cols, buff=0.0)
        filled_grid = filled_grid_original.copy()

        empty_grid = (
            mn.VGroup(*[mn.Square(6 / N_pixels, stroke_width=0.4) for x in range(cols) for y in range(rows)])
            .move_to(filled_grid)
            .arrange_in_grid(rows, cols, buff=0.0)
        )

        self.play(mn.Create(filled_grid))
        self.wait()
        self.play(mn.FadeIn(empty_grid))
        self.wait()
        self.play(mn.FadeOut(filled_grid))
        self.wait()

        self.play(empty_grid.animate.to_edge(mn.LEFT))
        self.wait(0.5)

        self.next_section("Highlight cells", skip_animations=False)

        independent_seq_txt = mn.Text("Independent sequence", font_size=42).to_corner(mn.UR, buff=1)
        pixel_position_txt = (
            mn.Text("pixel position = ", font_size=32).next_to(independent_seq_txt, mn.DOWN, aligned_edge=mn.LEFT)
            # .shift(0.2 * mn.RIGHT)
        )
        self.play(mn.Write(independent_seq_txt), mn.Write(pixel_position_txt))
        self.wait()

        # coords = [(random.randint(0, N_pixels), random.randint(0, N_pixels) ) for _ in range(6)]
        coords = [(0, ii) for ii in range(8)]
        for coord in coords:
            ii, jj = coord

            # On the grid
            ij_val_grid_txt = mn.Text(f"({ii}, {jj})", font_size=24, slant=mn.ITALIC).next_to(
                empty_grid[cols * ii + jj], mn.UP, buff=0.1
            )

            # Nearby "pixel position = "
            ij_val_txt = mn.Text(
                f" ({ii},  {jj})",
                font_size=32,
                slant=mn.ITALIC,
            ).next_to(pixel_position_txt, mn.RIGHT)

            self.add(ij_val_txt)
            self.add(ij_val_grid_txt)
            empty_grid[cols * ii + jj].become(empty_grid[cols * ii + jj].set_stroke(width=3.0))
            self.wait(0.8)
            empty_grid[cols * ii + jj].become(empty_grid[cols * ii + jj].set_stroke(width=0.4))
            self.remove(ij_val_txt, ij_val_grid_txt)

        self.next_section("Transform in picture", skip_animations=False)

        dependent_seq_txt = mn.Text("Dependent sequence", font_size=42).next_to(
            pixel_position_txt, mn.DOWN, aligned_edge=mn.LEFT, buff=1.2
        )

        RGB_values_txt = mn.Text("RGB Values", font_size=28).next_to(dependent_seq_txt, mn.DOWN, aligned_edge=mn.LEFT)

        # filled_grid_original = filled_grid_original.align_to(filled_grid)
        self.play(
            mn.Transform(empty_grid, filled_grid_original.to_edge(mn.LEFT)),
            mn.Write(dependent_seq_txt),
            mn.Write(RGB_values_txt),
        )
        self.wait(0.5)

        # coords = [(random.randint(0, N_pixels), random.randint(0, N_pixels) ) for _ in range(10)]
        for coord in coords:
            ii, jj = coord

            pixel_zoomed = (
                filled_grid[cols * ii + jj]
                .copy()
                .scale(6)
                .set_stroke(width=3)
                .next_to(RGB_values_txt, mn.DOWN, buff=0.6, aligned_edge=mn.LEFT)
                # .stretch_to_fit_width(5, about_edge=mn.LEFT)
            )

            R, G, B = mn.color_to_int_rgb(pixel_zoomed.get_color())
            RGB_values = (
                mn.VGroup(
                    mn.VGroup(
                        mn.Text(f"{R}", color=mn.PURE_RED, font_size=32), mn.Text("R", color=mn.PURE_RED, font_size=32)
                    ).arrange(mn.UP),
                    mn.VGroup(
                        mn.Text(f"{G}", color=mn.PURE_GREEN, font_size=32),
                        mn.Text("G", color=mn.PURE_GREEN, font_size=32),
                    ).arrange(mn.UP),
                    mn.VGroup(
                        mn.Text(f"{B}", color=mn.PURE_BLUE, font_size=32),
                        mn.Text("B", color=mn.PURE_BLUE, font_size=32),
                    ).arrange(mn.UP),
                )
                .arrange(mn.RIGHT, buff=0.1)
                .next_to(pixel_zoomed, mn.RIGHT)
            )

            # Pixel position
            ij_val_txt = mn.Text(
                f"({ii}, {jj})",
                font_size=32,
            ).next_to(pixel_position_txt, mn.RIGHT)

            ij_val_grid_txt = mn.Text(f"({ii},  {jj})", font_size=24, slant=mn.ITALIC).next_to(
                empty_grid[cols * ii + jj], mn.UP, buff=0.1
            )

            empty_grid[cols * ii + jj].become(empty_grid[cols * ii + jj].set_stroke(width=3.0))
            self.add(RGB_values_txt, RGB_values, ij_val_grid_txt)
            self.add(pixel_zoomed, ij_val_txt, ij_val_grid_txt)
            self.wait()

            empty_grid[cols * ii + jj].become(empty_grid[cols * ii + jj].set_stroke(width=0.4))
            self.remove(
                RGB_values,
                RGB_values_txt,
                ij_val_txt,
                ij_val_grid_txt,
                pixel_zoomed,
            )

        self.add(
            RGB_values,
            RGB_values_txt,
            ij_val_txt,
            ij_val_grid_txt,
            pixel_zoomed,
        )
        self.play(mn.Circumscribe(mn.VGroup(pixel_position_txt, ij_val_txt)))
        self.wait()
        self.play(mn.Circumscribe(RGB_values))

        self.next_section("TESTS", skip_animations=True)

        ii = 10
        jj = 251
        kk = 99
        T = mn.Text(f"({ii}, {jj}, {kk})")

        # self.add(T)
        # self.wait()
        # self.play(mn.FadeOut(self.mobjects))
        # self.wait(0.2)


class ContinuousDiscrete(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        self.next_section("Temperature", skip_animations=False)
        # Temperature
        N = 48
        signal = np.random.default_rng().uniform(10, 28, N)
        Ts = 0.1
        times = np.linspace(0, N * Ts, N)

        # Low pass filter data
        Tc = 1.8  # Tc = 1/Fc, OBS! Tc>Ts
        signal_filt = np.zeros(len(signal))
        signal_filt[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            signal_filt[ii + 1] = (1 - Ts / Tc) * signal_filt[ii] + Ts / Tc * s

        # Axis
        mycfg.axis_config["include_numbers"] = False
        axis_config_others = {
            "y_range": [0, 32, 32 / 10],
            "x_length": 11.0,
            "y_length": 6.0,
        }
        x_span = 5
        x_range = [0.0, x_span, 1]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        ax.get_y_axis().add_numbers()

        # Signal
        temperature = ax.plot(lambda t: np.interp(t, times, signal_filt), x_range=[times[0], times[-1], Ts])
        # dot = mn.Dot(ax.i2gp(3, temperature))

        # Tracking stuff
        t0 = 0.0
        dn = mn.DecimalNumber(t0, font_size=32)

        x_label_tex = mn.MathTex(r"\textrm{time [h]}", font_size=28)
        x_label = ax.get_x_axis_label(x_label_tex, direction=mn.RIGHT, buff=0.3)
        y_label = ax.get_y_axis_label(
            mn.MathTex(r"\textrm{Temperature [}^\circ \textrm{C}]}", font_size=28), direction=mn.UL
        )

        triangle = mn.VMobject()
        line = mn.VMobject()

        def new_triangle(mob):
            next_mob = ax.get_T_label(x_val=dn.get_value(), graph=temperature)
            mob.become(next_mob)
            dn.next_to(mob, mn.DOWN)

        triangle.add_updater(new_triangle, call_updater=True)

        def new_line(mob):
            p0 = ax.c2p(t0, 0)
            p1 = ax.c2p(dn.get_value(), 0)
            next_mob = mn.Line(p0, p1, stroke_color=mn.RED, stroke_opacity=1.0, stroke_width=10)
            mob.become(next_mob)

        line.add_updater(new_line, call_updater=True)

        self.play(mn.Write(mn.VGroup(ax, x_label, y_label, temperature).scale(0.5).to_edge(mn.LEFT)))
        self.wait()
        self.play(mn.FadeIn(triangle, line, run_time=0.5), mn.ChangeDecimalToValue(dn, N * Ts, run_time=3))
        self.wait(2)

        # Quarterly Revenue
        self.next_section("Revenue", skip_animations=False)
        mycfg.axis_config["font_size"] = 28
        mycfg.axis_config["include_numbers"] = False
        y_range = [0, 100, 10]
        x_range = [0, 5, 1]
        axes = mn.Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=11,
            y_length=6,
            axis_config=mycfg.axis_config,
        )
        axes.get_y_axis().add_numbers()

        x_label_tex = mn.MathTex(r"\textrm{Quarters}", font_size=36).next_to(ax, mn.DOWN, buff=0.2)
        x_label = axes.get_x_axis_label(x_label_tex, direction=mn.DOWN, buff=0.3)

        y_label_tex = mn.MathTex(r"\textrm{Renevue [M€]}", font_size=36).next_to(ax, mn.LEFT, buff=0.3)
        y_label = axes.get_y_axis_label(y_label_tex, direction=mn.UL)

        nums = []
        for ii in range(1, 5):
            nums.append(axes.get_x_axis().get_number_mobject(ii, font_size=32))

        Q1 = mn.Rectangle(height=3, width=1.2, fill_opacity=0.5).move_to(axes.c2p(1, 0), aligned_edge=mn.DOWN)
        Q2 = mn.Rectangle(height=2.1, width=1.2, fill_opacity=0.5).move_to(axes.c2p(2, 0), aligned_edge=mn.DOWN)
        Q3 = mn.Rectangle(height=4.2, width=1.2, fill_opacity=0.5).move_to(axes.c2p(3, 0), aligned_edge=mn.DOWN)
        Q4 = mn.Rectangle(height=2.6, width=1.2, fill_opacity=0.5).move_to(axes.c2p(4, 0), aligned_edge=mn.DOWN)

        discrete_block = mn.VGroup(axes, x_label, y_label, Q1, Q2, Q3, Q4, *nums).scale(0.5).to_edge(mn.RIGHT)
        self.add(discrete_block)
        self.wait()

        triangle = mn.VMobject()
        self.add(triangle)
        for num in nums:
            # self.add(mn.Dot(color=mn.RED).next_to(num, mn.UP, buff=0.05))
            # self.play(mn.Indicate(num, scale_factor=2, color=mn.RED))
            triangle.become(mn.Triangle(radius=0.1, color=mn.WHITE, fill_opacity=1.0).next_to(num, mn.DOWN))
            num.become(num.scale(2, about_edge=mn.UP))
            self.add(mn.Dot(color=mn.RED).next_to(num, mn.UP, buff=0.05))
            # self.play( num.animate.scale(2, about_edge=mn.UP))
            self.wait()
        self.wait()


class Summary(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        # Labels
        time_text = mn.Text("Time", font_size=28).rotate(90 * mn.DEGREES).move_to((-6.5, 1.5, 0))
        frequency_text = mn.Text("Frequency", font_size=28).rotate(90 * mn.DEGREES).move_to((-6.5, -2, 0))
        continuous_text = mn.Text("Continuous", font_size=28).move_to((-3.5, 3.5, 0))
        discrete_text = mn.Text("Discrete", font_size=28).move_to((3.5, 3.5, 0))

        self.add(time_text, frequency_text, continuous_text, discrete_text)

        # Dashed Lines
        x0 = -0.9 * mn.config.frame_width / 2
        x1 = 0.9 * mn.config.frame_width / 2
        hline = mn.DashedLine((x0, -0.2, 0), (x1, -0.2, 0), stroke_opacity=0.4, dash_length=0.1)

        y0 = -0.9 * mn.config.frame_height / 2
        y1 = 0.9 * mn.config.frame_height / 2
        vline = mn.DashedLine((0, y0, 0), (0, y1, 0), stroke_opacity=0.4, dash_length=0.1)

        self.add(hline, vline)

        # Generic signal
        a0 = 2.1
        a1 = 3.3
        a2 = 0.5

        f0 = 2
        f1 = 3
        f2 = 3.5
        F = [f0, f1, f2]

        phi0 = 0
        phi1 = 1.2
        phi2 = 0.8

        ti = 0.0
        tf = 2.5
        fs = 8 * max(F)
        times = np.arange(ti, tf, 1 / fs)
        y = lambda a, f, phi: a * np.sin(2 * np.pi * f * times + phi)
        y0 = y(a0, f0, phi0)
        y1 = y(a1, f1, phi1)
        y2 = y(a2, f2, phi2)
        vals = y0 + y1 + y2

        # Axis config
        x_length = 4.5
        y_length = 2.5
        axis_config_others = {"y_range": [-8, 8, 12 / 4], "x_length": x_length, "y_length": y_length}
        x_range = [0.0, tf, 1]
        ax_ct = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others).next_to(
            time_text, mn.RIGHT
        )
        t_label = ax_ct.get_x_axis_label(mn.MathTex("t", font_size=28), mn.DR)

        y_ct = ax_ct.plot(lambda t: np.interp(t, times, vals), x_range=[times[0], times[-4], 1 / fs])
        self.add(ax_ct, y_ct, t_label)

        Ts = 0.15
        ax_dt = ax_ct.copy().shift(7 * mn.RIGHT)
        y_dt = ax_dt.plot(lambda t: np.interp(t, times, vals), x_range=[times[0], times[-4], 1 / fs])
        t_label = ax_dt.get_x_axis_label(mn.MathTex("t", font_size=28), mn.DR)
        # y_dt = y_ct.copy()
        samples = mn.VGroup(*[mn.Dot(ax_dt.i2gp(t, y_dt)) for t in np.linspace(0, tf - 0.2, int((tf - 0.2) / Ts))])
        vlines = mn.VGroup(*[ax_dt.get_vertical_line(p.get_center()) for p in samples])
        self.add(ax_dt, samples, t_label, vlines)

        # Frequency analysis
        # fft
        f_vals = fft.rfftn(vals / len(vals))
        f_vals_pow = [np.abs(x) ** 2 for x in f_vals]

        # Continuous frequency
        f_bins = fft.rfftfreq(len(vals), Ts)

        axis_config_others = {"y_range": [0.0, 2, np.around(3 / 4, 2)], "x_length": x_length, "y_length": y_length}
        x_range = [f_bins[0], f_bins[-1], 1]
        ax_cf = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others).next_to(
            ax_ct, mn.DOWN, buff=1
        )
        f_label = ax_cf.get_x_axis_label(mn.MathTex("f", font_size=28), mn.DR)

        interp = PchipInterpolator(f_bins, f_vals_pow)
        y_cf = ax_cf.plot(interp, x_range=[f_bins[0], f_bins[-1], 0.05])
        # print(y_cf.
        self.add(ax_cf, y_cf, f_label)

        # Discrete frequency

        ax_df = ax_cf.copy().shift(7 * mn.RIGHT)
        f_label = ax_df.get_x_axis_label(mn.MathTex("f", font_size=28), mn.DR)

        steps = []
        for x, x_next, y in zip(f_bins, f_bins[1:], f_vals_pow):
            steps.append([x, y, 0])
            steps.append([x_next, y, 0])
        steps.append([f_bins[-1], f_vals_pow[-1], 0])

        steps = [ax_df.c2p(x, y, 0) for x, y, _ in steps]
        print(max(f_vals_pow))

        y_df = mn.VMobject().set_points_as_corners(steps)
        # y_df = ax_df.plot(lambda f: np.interp(f, f_bins_d, f_vals_pow_d), x_range=[f_bins[0], f_bins[-1], Ts])
        # y_df = ax_df.plot_line_graph(f_bins_d, f_vals_pow_d)
        self.add(ax_df, y_df, f_label)


class Test(mn.ThreeDScene):
    def construct(self):
        y_range = [0, 100, 10]
        x_range = [0, 5, 1]
        axes = mn.Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=11,
            y_length=6,
        )
        axes.get_y_axis().add_numbers()

        xgrid = mycfg.get_xgrid(axes)
        block = mn.VGroup(axes, xgrid)
        self.add(block.rotate(-20 * mn.DEGREES, mn.UP))


# vim: set textwidth=120:
