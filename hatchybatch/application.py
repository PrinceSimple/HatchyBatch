import tkinter as tk
from tkinter import filedialog
from hatchybatch.views import Mainview, StatusBar
from hatchybatch.models import ImageData, Tracer
from threading import Thread


class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.xdog_sigma_high = tk.DoubleVar()
        self.xdog_sigma_low = tk.DoubleVar()
        self.xdog_sharp_p = tk.DoubleVar()
        self.xdog_phi = tk.DoubleVar()
        self.xdog_epsilon = tk.DoubleVar()

        self.edgemap_sigma = tk.DoubleVar()
        self.edgemap_thresh_low = tk.DoubleVar()
        self.edgemap_thresh_high = tk.DoubleVar()

        self.flowfield_sigma = tk.DoubleVar()
        self.flowfield_rho = tk.DoubleVar()
        self.flowfield_hatch_sigma = tk.DoubleVar()

        self.thresh_low_min = tk.DoubleVar()
        self.thresh_low_max = tk.DoubleVar()
        self.thresh_midlow_min = tk.DoubleVar()
        self.thresh_midlow_max = tk.DoubleVar()
        self.thresh_midhigh_min = tk.DoubleVar()
        self.thresh_midhigh_max = tk.DoubleVar()
        self.thresh_high_min = tk.DoubleVar()
        self.thresh_high_max = tk.DoubleVar()

        self.edge_probability = tk.DoubleVar()
        self.edge_length = tk.IntVar()
        self.low_length = tk.IntVar()
        self.midlow_length = tk.IntVar()
        self.midhigh_length = tk.IntVar()
        self.high_length = tk.IntVar()

        self.low_distance = tk.IntVar()
        self.midlow_distance = tk.IntVar()
        self.midhigh_distance = tk.IntVar()
        self.high_distance = tk.IntVar()

        self.low_crosshatch = tk.BooleanVar()
        self.midlow_crosshatch = tk.BooleanVar()
        self.midhigh_crosshatch = tk.BooleanVar()
        self.high_crosshatch = tk.BooleanVar()

        self.xdog_output = tk.BooleanVar()
        self.edges_output = tk.BooleanVar()
        self.hatch_output = tk.BooleanVar()

        self.status_text = tk.StringVar()

        self.main_view = Mainview(self.root, self)
        self.status_bar = StatusBar(self.root, self)

        self.main_view.pack(side='top', fill='both')
        self.status_bar.pack(side='bottom', fill='x')

        self.model = ImageData()
        ######### Initial Values #########
        self.xdog_sigma_high.set(1.8)
        self.xdog_sigma_low.set(1.0)
        self.xdog_sharp_p.set(20)
        self.xdog_phi.set(0.1)
        self.xdog_epsilon.set(20)

        self.edgemap_sigma.set(2.0)
        self.edgemap_thresh_low.set(0.1)
        self.edgemap_thresh_high.set(0.2)

        self.flowfield_sigma.set(1.5)
        self.flowfield_rho.set(5.5)
        self.flowfield_hatch_sigma.set(1.0)

        self.thresh_low_min.set(0.1)
        self.thresh_low_max.set(0.2)
        self.thresh_midlow_min.set(0.2)
        self.thresh_midlow_max.set(0.4)
        self.thresh_midhigh_min.set(0.4)
        self.thresh_midhigh_max.set(0.6)
        self.thresh_high_min.set(0.6)
        self.thresh_high_max.set(0.9)

        self.edge_probability.set(0.5)
        self.edge_length.set(5)
        self.low_length.set(20)
        self.midlow_length.set(20)
        self.midhigh_length.set(20)
        self.high_length.set(20)

        self.low_distance.set(4)
        self.midlow_distance.set(7)
        self.midhigh_distance.set(10)
        self.high_distance.set(20)

        self.low_crosshatch.set(False)
        self.midlow_crosshatch.set(False)
        self.midhigh_crosshatch.set(False)
        self.high_crosshatch.set(False)

        self.xdog_output.set(True)
        self.edges_output.set(True)
        self.hatch_output.set(True)
        self.status_text.set("Ready")

        self.run()

    def run(self):
        self.root.title("HatchyBatch")
        self.root.geometry('1250x780')
        self.root.iconbitmap('./hatchybatch/img/hatchybatch.ico')
        self.root.mainloop()

    def open_file(self):
        f = filedialog.askopenfilename(
            filetypes=[('Supported Images', '.png .jpg .jpeg .tif .bmp')])
        if f:
            self.model.load_image(f)
            self.run_threaded(self.calculate_all)

    def save_output(self):
        f = filedialog.asksaveasfilename(
            filetypes=[('HatchyBatch Output', '.svg')], defaultextension=".svg")
        if f:
            self.tracer.save_output(f)

    def show_image(self):
        self.main_view.control_frame.original.imshow(
            self.model.source, 'gray')
        self.main_view.control_frame.canvas.draw()

    def show_XDoG(self):
        self.model.generate_XDoG(
            self.xdog_sigma_high.get(),
            self.xdog_sigma_low.get(),
            self.xdog_sharp_p.get(),
            self.xdog_phi.get(),
            self.xdog_epsilon.get())
        self.show_thresholds()
        self.main_view.control_frame.xdog.imshow(
            self.model.xdog, 'gray')
        self.main_view.control_frame.canvas.draw()

    def show_DoG(self):
        self.model.generate_DoG(
            self.xdog_sigma_high.get(),
            self.xdog_sigma_low.get(),
            threshold=0.4)
        self.main_view.control_frame.xdog.imshow(
            self.model.dog, 'gray')
        self.main_view.control_frame.canvas.draw()

    def show_edgemap(self):
        self.model.generate_edge_map(
            self.edgemap_sigma.get(),
            self.edgemap_thresh_low.get(),
            self.edgemap_thresh_high.get())
        self.main_view.control_frame.edgemap.imshow(
            self.model.edgemap, 'gray')
        self.main_view.control_frame.canvas.draw()

    def show_flowfield(self):
        self.model.generate_flow_field(
            self.flowfield_sigma.get(), self.flowfield_rho.get(), self.flowfield_hatch_sigma.get())
        self.model.generate_lic()
        self.main_view.control_frame.flow_field.imshow(
            self.model.lic, 'gray')
        self.main_view.control_frame.canvas.draw()

    def show_thresholds(self):
        self.model.generate_thresholds(
            [self.thresh_low_min.get(),
             self.thresh_midlow_min.get(),
             self.thresh_midhigh_min.get(),
             self.thresh_high_min.get()],
            [self.thresh_low_max.get(),
             self.thresh_midlow_max.get(),
             self.thresh_midhigh_max.get(),
             self.thresh_high_max.get()])

        self.main_view.threshold_frame.thresh_low.imshow(
            self.model.thresholds[0], 'gray')
        self.main_view.threshold_frame.thresh_midlow.imshow(
            self.model.thresholds[1], 'gray')
        self.main_view.threshold_frame.thresh_midhigh.imshow(
            self.model.thresholds[2], 'gray')
        self.main_view.threshold_frame.thresh_high.imshow(
            self.model.thresholds[3], 'gray')
        self.main_view.threshold_frame.canvas.draw()

        self.main_view.xdog_threshold_frame.thresh_low.imshow(
            self.model.xdog_thresholds[0], 'gray')
        self.main_view.xdog_threshold_frame.thresh_midlow.imshow(
            self.model.xdog_thresholds[1], 'gray')
        self.main_view.xdog_threshold_frame.thresh_midhigh.imshow(
            self.model.xdog_thresholds[2], 'gray')
        self.main_view.xdog_threshold_frame.thresh_high.imshow(
            self.model.xdog_thresholds[3], 'gray')
        self.main_view.xdog_threshold_frame.canvas.draw()

    def calculate_all(self):
        try:
            self.show_image()
            self.show_XDoG()
            # self.show_DoG()
            self.show_edgemap()
            self.show_flowfield()
            # self.trace_image()
        except Exception as e:
            print(e)
            self.status_text.set("You have to open a bitmap image first...")

    def trace_image(self):
        self.tracer = Tracer(
            self.model.source.shape,
            self.model.edgemap,
            self.model.xdog_thresholds if self.xdog_output.get() else self.model.thresholds,
            self.model.flowfield_u,
            self.model.flowfield_v,
            self.model.flowfield_hatch_u,
            self.model.flowfield_hatch_v)
        if self.edges_output.get():
            self.tracer.generate_contours(
                self.edge_length.get(), self.edge_probability.get())
        if self.hatch_output.get():
            self.tracer.generate_hatchpaths(
                [self.low_length.get(), self.midlow_length.get(),
                 self.midhigh_length.get(), self.high_length.get()],
                [self.low_distance.get(), self.midlow_distance.get(),
                 self.midhigh_distance.get(), self.high_distance.get()],
                [self.low_crosshatch.get(), self.midlow_crosshatch.get(),
                 self.midhigh_crosshatch.get(), self.high_crosshatch.get()])
        self.status_text.set(f'{len(self.tracer._paths)} paths in output')

    def show_output(self):
        if hasattr(self, 'tracer'):
            self.tracer.show_preview()

    def disable_buttons(self):
        for button in self.main_view.buttons.winfo_children():
            try:
                if button.widgetName != 'frame':
                    button.configure(state='disabled')
            except Exception as e:
                print(e)

    def enable_buttons(self):
        for button in self.main_view.buttons.winfo_children():
            try:
                if button.widgetName != 'frame':
                    button.configure(state='normal')
            except Exception as e:
                print(e)

    def run_threaded(self, target):
        try:
            self.disable_buttons()
            thread = Thread(target=target)
            thread.start()
            self.check_thread(thread)
        except Exception as e:
            print(e)

    def check_thread(self, thread):
        if thread.is_alive():
            self.status_text.set('Calculating...Please be patient')
            self.root.after(200, self.check_thread, thread)
        else:
            if hasattr(self, 'tracer'):
                self.enable_buttons()
                self.status_text.set(
                    f'Done. - {len(self.tracer._paths)} paths in output')
            else:
                self.enable_buttons()
                self.status_text.set('You have to trace the image first...')

    def save_config(self):
        pass
        # for config in enumerate(self.__dict__):
        #   print(config.get())
