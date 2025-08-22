from PyQt5.QtWidgets import QApplication
from gnuradio import qtgui, gr, blocks, window
import sys

class TopBlock(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.samp_rate = 1e6
        self.src = blocks.null_source(8)
        self.sink = qtgui.waterfall_sink_c(
            1024,
            window.WIN_BLACKMAN_hARRIS,
            0.0,
            self.samp_rate,
            "Waterfall",
            1
        )
        self.connect(self.src, self.sink)

app = QApplication(sys.argv)
tb = TopBlock()
tb.start()
tb.sink.qwidget().show()
app.exec_()
tb.stop()
tb.wait()

