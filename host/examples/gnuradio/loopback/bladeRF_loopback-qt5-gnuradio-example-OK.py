#!/usr/bin/env python3
##################################################
# GNU Radio Python Flow Graph
# Title: bladeRF loopback example
# Author: Nuand, LLC <bladeRF@nuand.com>
# Description: A simple flowgraph that demonstrates the usage of loopback modes.
# Generated: Sun Jan 17 21:26:48 2016
##################################################

import sys
print('DEBUG: after import sys')
try:
    import sip
    print('DEBUG: after import sip')
except ImportError:
    print("sip module is required for PyQt5 compatibility. Please install it with 'pip install sip'.")
    sys.exit(1)
from PyQt5 import QtCore, QtWidgets
print('DEBUG: after import PyQt5.QtCore, QtWidgets')
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSlot, QSettings, QT_VERSION_STR
print('DEBUG: after import PyQt5.QtCore symbols')
from PyQt5.QtGui import QIcon
print('DEBUG: after import PyQt5.QtGui.QIcon')
from PyQt5.QtWidgets import QBoxLayout, QComboBox, QFrame, QGridLayout, QLabel, QScrollArea, QTabWidget, QToolBar, QVBoxLayout
print('DEBUG: after import PyQt5.QtWidgets symbols')
from gnuradio import blocks, digital, eng_notation, gr, qtgui
print('DEBUG: after import gnuradio symbols')
from gnuradio.eng_option import eng_option
print('DEBUG: after import gnuradio.eng_option')
from gnuradio.filter import firdes
print('DEBUG: after import gnuradio.filter.firdes')
from gnuradio.qtgui import Range, RangeWidget
print('DEBUG: after import gnuradio.qtgui.Range, RangeWidget')
from optparse import OptionParser
print('DEBUG: after import optparse.OptionParser')
import numpy
print('DEBUG: after import numpy')
import osmosdr
print('DEBUG: after import osmosdr')
import time
print('DEBUG: after import time')

print('DEBUG: Script start')

# Ensure that no QWidget or subclass is instantiated before QApplication is created.
# Only class definitions and imports should be at the top level.
# All widget instantiations must be inside __main__ or after QApplication is created.
# Remove multiple inheritance from bladeRF_loopback
class bladeRF_loopback(gr.top_block):
    def __init__(self, **kwargs):
        print('DEBUG: bladeRF_loopback.__init__ called')
        gr.top_block.__init__(self, "bladeRF loopback example")
        # Minimal GNU Radio flowgraph: signal source -> null sink
        from gnuradio import analog, blocks
        self.src = analog.sig_source_f(32000, analog.GR_SIN_WAVE, 350, 0.1, 0)
        self.snk = blocks.null_sink(gr.sizeof_float)
        self.connect(self.src, self.snk)

# BladeRFLoopbackWidget: All Qt widget setup, instantiates bladeRF_loopback
class BladeRFLoopbackWidget(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("bladeRF loopback example (Minimal)")
        try:
            self.setWindowIcon(QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        layout = QVBoxLayout()
        label = QLabel("Minimal GNU Radio + PyQt6 Example Running!")
        layout.addWidget(label)
        # Add a simple RangeWidget (not connected to flowgraph)
        def dummy_callback(val):
            print(f"RangeWidget value changed: {val}")
        range_widget = RangeWidget(Range(0, 10, 1, 5, 100), dummy_callback, "Test Range", "counter_slider", int)
        layout.addWidget(range_widget)
        self.setLayout(layout)
        self.tb = bladeRF_loopback(**kwargs)

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
