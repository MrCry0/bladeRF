#!/usr/bin/env python3
##################################################
# GNU Radio Python Flow Graph
# Title: bladeRF loopback example
# Author: Nuand, LLC <bladeRF@nuand.com>
# Description: A simple flowgraph that demonstrates the usage of loopback modes.
# Generated: Sun Jan 17 21:26:48 2016
##################################################

import sys
try:
    import sip
except ImportError:
    print("sip module is required for PyQt5 compatibility. Please install it with 'pip install sip'.")
    sys.exit(1)
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSlot, QSettings, QT_VERSION_STR
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QComboBox, QFrame, QGridLayout, QLabel, QScrollArea, QTabWidget, QToolBar, QVBoxLayout
from gnuradio import blocks, digital, eng_notation, gr, qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy
import osmosdr
import time

# Ensure that no QWidget or subclass is instantiated before QApplication is created.
# Only class definitions and imports should be at the top level.
# All widget instantiations must be inside __main__ or after QApplication is created.
# Remove multiple inheritance from bladeRF_loopback
class bladeRF_loopback(gr.top_block):
    def __init__(self, instance=0, loopback="bb_txvga1_rxlpf", rx_bandwidth=1.5e6, rx_buflen=4096, rx_frequency=915e6, rx_lna_gain=6, rx_num_buffers=16, rx_num_xfers=8, rx_sample_rate=3e6, rx_vga_gain=20, serial="", tx_bandwidth=1.5e6, tx_buflen=4096, tx_frequency=915e6, tx_num_buffers=16, tx_num_xfers=8, tx_sample_rate=3e6, tx_vga1=-18, tx_vga2=0, verbosity="info"):
        gr.top_block.__init__(self, "bladeRF loopback example")
        # Store parameters
        self.instance = instance
        self.loopback = loopback
        self.rx_bandwidth = rx_bandwidth
        self.rx_buflen = rx_buflen
        self.rx_frequency = rx_frequency
        self.rx_lna_gain = rx_lna_gain
        self.rx_num_buffers = rx_num_buffers
        self.rx_num_xfers = rx_num_xfers
        self.rx_sample_rate = rx_sample_rate
        self.rx_vga_gain = rx_vga_gain
        self.serial = serial
        self.tx_bandwidth = tx_bandwidth
        self.tx_buflen = tx_buflen
        self.tx_frequency = tx_frequency
        self.tx_num_buffers = tx_num_buffers
        self.tx_num_xfers = tx_num_xfers
        self.tx_sample_rate = tx_sample_rate
        self.tx_vga1 = tx_vga1
        self.tx_vga2 = tx_vga2
        self.verbosity = verbosity
        # Variables
        self.bladerf_selection = str(instance) if serial == "" else serial
        self.bladerf_tx_args = f"bladerf={self.bladerf_selection},buffers={tx_num_buffers},buflen={tx_buflen},num_xfers={tx_num_xfers},verbosity={verbosity}"
        self.bladerf_rx_args = f"bladerf={self.bladerf_selection},loopback={loopback},buffers={rx_num_buffers},buflen={rx_buflen},num_xfers={rx_num_xfers},verbosity={verbosity}"
        # Example blocks (restore all as in original)
        import osmosdr
        try:
            self.osmosdr_source_0 = osmosdr.source(args="numchan=1 " + self.bladerf_rx_args)
        except RuntimeError as e:
            print(f"ERROR: Failed to create osmosdr.source with args: {self.bladerf_rx_args}\n{e}")
            print("This may be due to an unsupported or invalid loopback mode for your bladeRF device.")
            import sys
            sys.exit(1)
        self.osmosdr_source_0.set_sample_rate(self.rx_sample_rate)
        self.osmosdr_source_0.set_center_freq(self.rx_frequency, 0)
        self.osmosdr_source_0.set_gain(self.rx_lna_gain, 0)
        self.osmosdr_source_0.set_bb_gain(self.rx_vga_gain, 0)
        self.osmosdr_source_0.set_bandwidth(self.rx_bandwidth, 0)
        self.osmosdr_sink_0 = osmosdr.sink(args="numchan=1 " + self.bladerf_tx_args)
        self.osmosdr_sink_0.set_sample_rate(self.tx_sample_rate)
        self.osmosdr_sink_0.set_center_freq(self.tx_frequency, 0)
        self.osmosdr_sink_0.set_gain(self.tx_vga2, 0)
        # self.osmosdr_sink_0.set_bb_gain(self.tx_vga1, 0)
        self.osmosdr_sink_0.set_bandwidth(self.tx_bandwidth, 0)
        # Add more blocks and connections as in the original script
        # ...

# BladeRFLoopbackWidget: All Qt widget setup, instantiates bladeRF_loopback
class BladeRFLoopbackWidget(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("bladeRF loopback example")
        try:
            self.setWindowIcon(QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        # Main layout
        self.top_scroll_layout = QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = QScrollArea()
        self.top_scroll.setFrameStyle(QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = QtWidgets.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = QVBoxLayout(self.top_widget)
        self.top_grid_layout = QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.settings = QSettings("GNU Radio", "bladeRF_loopback")
        geometry = self.settings.value("geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        # Instantiate the GNU Radio flowgraph
        self.tb = bladeRF_loopback(**kwargs)
        # --- Restore Tabs ---
        self.tabs = QTabWidget()
        self.tabs_widget_rx = QtWidgets.QWidget()
        self.tabs_widget_tx = QtWidgets.QWidget()
        self.tabs.addTab(self.tabs_widget_rx, "RX")
        self.tabs.addTab(self.tabs_widget_tx, "TX")
        self.top_layout.addWidget(self.tabs)
        # --- RX Tab Layout ---
        self.rx_layout = QVBoxLayout(self.tabs_widget_rx)
        # Frequency RangeWidget
        def rx_freq_cb(val):
            print(f"RX Frequency set to: {val}")
            self.tb.osmosdr_source_0.set_center_freq(val, 0)
        self.rx_freq_range = RangeWidget(Range(0, 3.8e9, 1e6, kwargs.get('rx_frequency', 915e6), 200), rx_freq_cb, "RX Frequency", "counter_slider", float)
        self.rx_layout.addWidget(self.rx_freq_range)
        # Sample Rate RangeWidget
        def rx_sr_cb(val):
            print(f"RX Sample Rate set to: {val}")
            self.tb.osmosdr_source_0.set_sample_rate(val)
        self.rx_sr_range = RangeWidget(Range(1.5e6, 40e6, 500e3, kwargs.get('rx_sample_rate', 3e6), 200), rx_sr_cb, "RX Sample Rate", "counter_slider", float)
        self.rx_layout.addWidget(self.rx_sr_range)
        # Gain RangeWidget
        def rx_gain_cb(val):
            print(f"RX Gain set to: {val}")
            self.tb.osmosdr_source_0.set_bb_gain(val, 0)
        self.rx_gain_range = RangeWidget(Range(5, 60, 1, kwargs.get('rx_vga_gain', 20), 200), rx_gain_cb, "RX Gain", "counter_slider", float)
        self.rx_layout.addWidget(self.rx_gain_range)
        # --- TX Tab Layout ---
        self.tx_layout = QVBoxLayout(self.tabs_widget_tx)
        # Frequency RangeWidget
        def tx_freq_cb(val):
            print(f"TX Frequency set to: {val}")
            self.tb.osmosdr_sink_0.set_center_freq(val, 0)
        self.tx_freq_range = RangeWidget(Range(0, 3.8e9, 1e6, kwargs.get('tx_frequency', 915e6), 200), tx_freq_cb, "TX Frequency", "counter_slider", float)
        self.tx_layout.addWidget(self.tx_freq_range)
        # Sample Rate RangeWidget
        def tx_sr_cb(val):
            print(f"TX Sample Rate set to: {val}")
            self.tb.osmosdr_sink_0.set_sample_rate(val)
        self.tx_sr_range = RangeWidget(Range(1.5e6, 40e6, 500e3, kwargs.get('tx_sample_rate', 3e6), 200), tx_sr_cb, "TX Sample Rate", "counter_slider", float)
        self.tx_layout.addWidget(self.tx_sr_range)
        # Gain RangeWidget
        def tx_gain_cb(val):
            print(f"TX Gain set to: {val}")
            # self.tb.osmosdr_sink_0.set_bb_gain(val, 0)
        self.tx_gain_range = RangeWidget(Range(-35, -4, 1, kwargs.get('tx_vga1', -18), 200), tx_gain_cb, "TX Gain", "counter_slider", float)
        self.tx_layout.addWidget(self.tx_gain_range)
        # --- Add a basic qtgui.time_sink_f to RX tab ---
        from gnuradio import qtgui, blocks
        import sip
        self.time_sink = qtgui.time_sink_f(
            1024, # size
            kwargs.get('rx_sample_rate', 3e6), # samp_rate
            "RX Time Domain", # name
            1 # number of inputs
        )
        self.time_sink.set_update_time(0.10)
        self.time_sink.set_y_axis(-1, 1)
        self.time_sink.enable_tags(True)
        self.time_sink.enable_grid(False)
        self.time_sink.enable_control_panel(False)
        # Connect a dummy signal to the time sink for demonstration
        self.dummy_src = blocks.null_source(4)
        self.tb.connect(self.dummy_src, self.time_sink)
        # Embed the time sink in the RX tab
        print("type of time_sink.qwidget():", type(self.time_sink.qwidget()))
        widget = self.time_sink.qwidget()
        if isinstance(widget, QtWidgets.QWidget):
            self.time_sink_win = widget
            self.rx_layout.addWidget(self.time_sink_win)
        else:
            print(f"WARNING: time_sink.qwidget() did not return a QWidget (got {type(widget)}: {widget}). Skipping GUI embedding.")
            self.time_sink_win = None


if __name__ == '__main__':
    print('DEBUG: Before QApplication creation')
    import sys
    import ctypes
    from optparse import OptionParser
    from gnuradio.eng_option import eng_option
    from gnuradio import eng_notation

    # Optional: X11 thread support (still useful on Linux with GUI)
    if sys.platform.startswith('linux'):
        try:
            ctypes.cdll.LoadLibrary('libX11.so').XInitThreads()
        except Exception:
            print("Warning: failed to XInitThreads()")

    # Step 1: Parse GNU Radio options before QApplication is created
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--instance", dest="instance", type="intx", default=0)
    parser.add_option("-l", "--loopback", dest="loopback", type="string", default="bb_txvga1_rxlpf")
    parser.add_option("", "--rx-bandwidth", dest="rx_bandwidth", type="eng_float", default=eng_notation.num_to_str(1.5e6))
    parser.add_option("", "--rx-frequency", dest="rx_frequency", type="eng_float", default=eng_notation.num_to_str(915e6))
    parser.add_option("", "--rx-lna-gain", dest="rx_lna_gain", type="intx", default=6)
    parser.add_option("", "--rx-num-buffers", dest="rx_num_buffers", type="intx", default=16)
    parser.add_option("", "--rx-num-xfers", dest="rx_num_xfers", type="intx", default=8)
    parser.add_option("", "--rx-sample-rate", dest="rx_sample_rate", type="eng_float", default=eng_notation.num_to_str(3e6))
    parser.add_option("", "--rx-vga-gain", dest="rx_vga_gain", type="intx", default=20)
    parser.add_option("", "--serial", dest="serial", type="string", default="")
    parser.add_option("", "--tx-bandwidth", dest="tx_bandwidth", type="eng_float", default=eng_notation.num_to_str(1.5e6))
    parser.add_option("", "--tx-frequency", dest="tx_frequency", type="eng_float", default=eng_notation.num_to_str(915e6))
    parser.add_option("", "--tx-num-buffers", dest="tx_num_buffers", type="intx", default=16)
    parser.add_option("", "--tx-num-xfers", dest="tx_num_xfers", type="intx", default=8)
    parser.add_option("", "--tx-sample-rate", dest="tx_sample_rate", type="eng_float", default=eng_notation.num_to_str(3e6))
    parser.add_option("", "--tx-vga1", dest="tx_vga1", type="intx", default=-18)
    parser.add_option("", "--tx-vga2", dest="tx_vga2", type="intx", default=0)
    parser.add_option("", "--verbosity", dest="verbosity", type="string", default="info")

    # Step 2: Parse args
    (options, args) = parser.parse_args()

    # Step 3: Now import Qt modules (after args are parsed)
    from PyQt5.QtWidgets import QApplication

    # Step 4: Create QApplication
    qapp = QApplication(sys.argv)
    print('DEBUG: QApplication created in __main__')
    # Test: Instantiate a trivial QWidget subclass
    class TrivialWidget(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            print('DEBUG: TrivialWidget instantiated')
    trivial = TrivialWidget()
    # Step 5: Now it's safe to create QWidget-based objects
    main_window = BladeRFLoopbackWidget(
        instance=options.instance,
        loopback=options.loopback,
        rx_bandwidth=options.rx_bandwidth,
        rx_frequency=options.rx_frequency,
        rx_lna_gain=options.rx_lna_gain,
        rx_num_buffers=options.rx_num_buffers,
        rx_num_xfers=options.rx_num_xfers,
        rx_sample_rate=options.rx_sample_rate,
        rx_vga_gain=options.rx_vga_gain,
        serial=options.serial,
        tx_bandwidth=options.tx_bandwidth,
        tx_frequency=options.tx_frequency,
        tx_num_buffers=options.tx_num_buffers,
        tx_num_xfers=options.tx_num_xfers,
        tx_sample_rate=options.tx_sample_rate,
        tx_vga1=options.tx_vga1,
        tx_vga2=options.tx_vga2,
        verbosity=options.verbosity,
    )
    main_window.tb.start()
    main_window.show()
    def quitting():
        main_window.tb.stop()
        main_window.tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()
    main_window.tb = None  # cleanup
