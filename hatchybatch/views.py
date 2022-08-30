from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')


class PathlengthSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.edge_probability = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            label="edge path probability",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.edge_probability).pack()
        self.edge_length = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="edge path maxlength",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.edge_length).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.low_length = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="dark tone path maxlength",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.low_length).pack()
        self.midlow_length = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="dark mids path maxlength",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.midlow_length).pack()
        self.midhigh_length = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="light mids path maxlength",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.midhigh_length).pack()
        self.high_length = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="highlights path maxlength",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.high_length).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.output_options = OutputOptions(self, controller).pack(padx=20)


class PathdistanceSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.low_distance = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="dark tone path distance",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.low_distance
        ).pack()
        tk.Checkbutton(
            self, text="crosshatch dark", variable=controller.low_crosshatch
        ).pack()
        self.midlow_distance = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="dark mids path distance",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.midlow_distance
        ).pack()
        tk.Checkbutton(
            self, text="crosshatch dark mids", variable=controller.midlow_crosshatch
        ).pack()
        self.midhigh_distance = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="light mids path distance",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.midhigh_distance
        ).pack()
        tk.Checkbutton(
            self, text="crosshatch light mids", variable=controller.midhigh_crosshatch).pack()
        self.high_distance = tk.Scale(
            self,
            from_=1,
            to=50,
            resolution=1,
            length=200,
            label="highlights path distance",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.high_distance
        ).pack()
        tk.Checkbutton(
            self, text="crosshatch highlight", variable=controller.high_crosshatch
        ).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.output_options = OutputOptions(self, controller).pack()


class XDoGSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.sigma_high = tk.Scale(
            self,
            from_=0.01,
            to=10.0,
            length=200,
            label=u"\u03c3" + u"\u2081" + " - Sigma high",
            width=10,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=controller.xdog_sigma_high).pack()
        self.sigma_low = tk.Scale(
            self,
            from_=0.01,
            to=10.0,
            resolution=0.1,
            length=200,
            label=u"\u03c3" + u"\u2082" + " - Sigma low",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.xdog_sigma_low).pack()
        self.sharp_p = tk.Scale(
            self,
            from_=1,
            to=100,
            resolution=0.1,
            length=200,
            label="p - sharpen parameter",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.xdog_sharp_p).pack()
        self.phi = tk.Scale(
            self,
            from_=0.005,
            to=1.0,
            resolution=0.01,
            length=200,
            label=u"\u03c6" + " - Phi",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.xdog_phi).pack()
        self.epsilon = tk.Scale(
            self,
            from_=0.0,
            to=255.0,
            resolution=0.1,
            length=200,
            label=u"\u03b5" + " - Epsilon",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.xdog_epsilon).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        tk.Button(self,
                  text="Recalculate XDoG",
                  command=controller.show_XDoG,
                  padx=5, pady=5
                  ).pack(padx=10, pady=10)


class EdgeMapSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(
            fill='x', padx=10, pady=10)
        self.sigma_high = tk.Scale(
            self,
            from_=1.0,
            to=10.0,
            resolution=0.1,
            length=200,
            label=u"\u03c3" + " - Sigma",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.edgemap_sigma).pack()
        self.thresh_low = tk.Scale(
            self,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            length=200,
            label="low threshold",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.edgemap_thresh_low).pack()
        self.thresh_high = tk.Scale(
            self,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            length=200,
            label="high threshold",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.edgemap_thresh_high).pack()
        ttk.Separator(self, orient='horizontal').pack(
            fill='x', padx=10, pady=10)
        tk.Button(self,
                  text="Recalculate Edgemap",
                  command=controller.show_edgemap,
                  padx=5, pady=5).pack(padx=10, pady=10)


class FlowFieldSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.sigma = tk.Scale(
            self,
            from_=0.1,
            to=10.0,
            resolution=0.1,
            length=200,
            label=u"\u03c3" + " - Sigma",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.flowfield_sigma).pack()
        self.rho = tk.Scale(
            self,
            from_=0.1,
            to=20.0,
            resolution=0.1,
            length=200,
            label=u"\u03c1" + " - Rho",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.flowfield_rho).pack()
        self.hatch_sigma = tk.Scale(
            self,
            from_=0.1,
            to=10.0,
            resolution=0.1,
            length=200,
            label=u"Hatchfield smoothing \u03c3",
            width=10,
            orient=tk.HORIZONTAL,
            variable=controller.flowfield_hatch_sigma).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        tk.Button(self,
                  text="Recalculate Flowfield",
                  command=controller.show_flowfield,
                  padx=5, pady=5).pack(padx=10, pady=10)


class TresholdSliders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        self.thresh_low_min = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            label="dark tone min/max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_low_min).pack()
        self.thresh_low_max = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            #label="threshold low max min",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_low_max).pack()
        self.thresh_midlow_min = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            label="dark mids min/max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_midlow_min).pack()
        self.thresh_midlow_max = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            #  label="threshold middle low max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_midlow_max).pack()
        self.thresh_midhigh_min = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            label="light mids min/max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_midhigh_min).pack()
        self.thresh_midhigh_max = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            # label="threshold middle high max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_midhigh_max).pack()
        self.thresh_high_min = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            label="highlights min/max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_high_min).pack()
        self.thresh_high_max = tk.Scale(
            self,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            length=200,
            # label="threshold high max",
            width=5,
            orient=tk.HORIZONTAL,
            variable=controller.thresh_high_max).pack()
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        tk.Button(self,
                  text="Recalculate Thresholds",
                  command=controller.show_thresholds
                  ).pack(padx=2, pady=15)


class OutputOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.xdog_output = tk.Checkbutton(
            self, text="use XDoG\nmask", variable=controller.xdog_output).pack(side=tk.LEFT)
        self.edges_output = tk.Checkbutton(
            self, text="output\nedges", variable=controller.edges_output).pack(side=tk.LEFT)
        self.hatch_output = tk.Checkbutton(
            self, text="output\nhatch", variable=controller.hatch_output).pack(side=tk.LEFT)


class ControlFigure(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fig = Figure(figsize=(6.5, 6.5))
        self.original = self.fig.add_subplot(2, 2, 1, frame_on=False)
        self.original.set_title('Original')
        self.original.tick_params(axis='both', labelsize=8)
        self.xdog = self.fig.add_subplot(2, 2, 2, frame_on=False)
        self.xdog.set_title('XDoG')
        # self.xdog.axis('off')
        self.flow_field = self.fig.add_subplot(2, 2, 3, frame_on=False)
        self.flow_field.set_title('Flowfield')
        # self.flow_field.axis('off')
        self.edgemap = self.fig.add_subplot(2, 2, 4, frame_on=False)
        self.edgemap.set_title('Edge Map')
        # self.edgemap.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self, pack_toolbar=False)
        self.toolbar.pack(side=tk.BOTTOM)


class ThresholdFigure(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fig = Figure(figsize=(6.5, 6.5))
        self.thresh_low = self.fig.add_subplot(2, 2, 1, frame_on=False)
        self.thresh_low.set_title('dark tones')
        self.thresh_low.tick_params(axis='both', labelsize=8)
        self.thresh_midlow = self.fig.add_subplot(2, 2, 2, frame_on=False)
        self.thresh_midlow.set_title('dark mids')
        # self.thresh_midlow.axis('off')
        self.thresh_midhigh = self.fig.add_subplot(2, 2, 3, frame_on=False)
        self.thresh_midhigh.set_title('light mids')
        # self.thresh_midhigh.axis('off')
        self.thresh_high = self.fig.add_subplot(2, 2, 4, frame_on=False)
        self.thresh_high.set_title('highlights')
        # self.thresh_high.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self, pack_toolbar=False)
        self.toolbar.pack(side=tk.BOTTOM)


class XDoGThresholdFigure(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fig = Figure(figsize=(6.5, 6.5))
        self.thresh_low = self.fig.add_subplot(2, 2, 1, frame_on=False)
        self.thresh_low.set_title('dark tones masked')
        self.thresh_low.tick_params(axis='both', labelsize=8)
        self.thresh_midlow = self.fig.add_subplot(2, 2, 2, frame_on=False)
        self.thresh_midlow.set_title('dark mids masked')
        # self.thresh_midlow.axis('off')
        self.thresh_midhigh = self.fig.add_subplot(2, 2, 3, frame_on=False)
        self.thresh_midhigh.set_title('light mids masked')
        # self.thresh_midhigh.axis('off')
        self.thresh_high = self.fig.add_subplot(2, 2, 4, frame_on=False)
        self.thresh_high.set_title('highlights masked')
        # self.thresh_high.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self, pack_toolbar=False)
        self.toolbar.pack(side=tk.BOTTOM)


class OutputFigure(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fig = Figure(figsize=(7, 7))
        self.output = self.fig.add_subplot(frame_on=False)
        self.output.set_title('Output')
        # self.output.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self, pack_toolbar=False)
        self.toolbar.pack(side=tk.BOTTOM, padx=50)


class Buttons(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.recalculate_btn = tk.Button(
            self, text="Trace Image", command=lambda: controller.run_threaded(controller.trace_image)).grid(row=0, column=1, padx=5, pady=5, ipadx=37, ipady=5)
        self.recalculate_btn = tk.Button(
            self, text="Recalculate Everything", command=lambda: controller.run_threaded(controller.calc_threaded)).grid(row=1, column=1, padx=5, pady=5, ipadx=10, ipady=5)
        self.preview_btn = tk.Button(
            self, text="Preview in Browser", command=controller.show_output).grid(row=2, column=1, padx=5, pady=10, ipadx=20, ipady=5)
        self.open_file_btn = tk.Button(
            self, text="Open File...", command=controller.open_file).grid(row=3, column=0, padx=5, pady=5)
        self.save_output_btn = tk.Button(
            self, text="Save Output...", command=controller.save_output).grid(row=3, column=2, padx=5, pady=5)
        self.save_config_btn = tk.Button(
            self, text="Save config...", command=controller.save_config).grid(row=3, column=1, padx=5, pady=5)


class StatusBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.info = tk.Label(self, textvariable=controller.status_text)
        self.info.pack()


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.conf_tabs = ttk.Notebook(self)
        self.output_tabs = ttk.Notebook(self)
        self.xdog_sliders = XDoGSliders(self, controller)
        self.edgemap_sliders = EdgeMapSliders(self, controller)
        self.flowfield_sliders = FlowFieldSliders(self, controller)
        self.threshold_sliders = TresholdSliders(self, controller)
        self.path_length_sliders = PathlengthSliders(self, controller)
        self.path_distance_sliders = PathdistanceSliders(self, controller)

        self.conf_tabs.add(self.xdog_sliders, text="XDoG")
        self.conf_tabs.add(self.flowfield_sliders, text="Flow Field")
        self.conf_tabs.add(self.edgemap_sliders, text="Edge Map")
        self.conf_tabs.add(self.threshold_sliders, text="Threshold")
        self.output_tabs.add(self.path_length_sliders, text="Path length")
        self.output_tabs.add(self.path_distance_sliders,
                             text="Path Distance / Crosshatch")

        self.output_tabs.pack(side=tk.RIGHT, anchor=tk.NE,
                              ipady=22, ipadx=15, padx=5, pady=2)
        self.conf_tabs.pack(side=tk.RIGHT, anchor=tk.NE,
                            ipadx=15, padx=5, pady=2)


class Mainview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.menu_frame = MenuFrame(self, controller)
        self.buttons = Buttons(self, controller)
        self.plot_tabs = ttk.Notebook(self)
        self.control_frame = ControlFigure(self)
        self.threshold_frame = ThresholdFigure(self)
        self.xdog_threshold_frame = XDoGThresholdFigure(self)
        self.plot_tabs.add(self.control_frame, text="Control Images")
        self.plot_tabs.add(self.xdog_threshold_frame,
                           text="XDoG Masks")
        self.plot_tabs.add(self.threshold_frame, text="Threshold Masks")

        self.plot_tabs.grid(row=0, column=0, rowspan=2, sticky=tk.N)
        self.menu_frame.grid(row=0, column=1, rowspan=1, sticky=tk.N)
        self.buttons.grid(row=1, column=1, rowspan=1, sticky=tk.N)
