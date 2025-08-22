from gnuradio import gr, analog, blocks
import time

class MinimalFlowgraph(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Minimal GNU Radio Test")
        src = analog.sig_source_f(32000, analog.GR_SIN_WAVE, 350, 0.1, 0)
        snk = blocks.null_sink(gr.sizeof_float)
        self.connect(src, snk)

if __name__ == '__main__':
    tb = MinimalFlowgraph()
    tb.start()
    print("Minimal GNU Radio flowgraph started. Running for 2 seconds...")
    time.sleep(2)
    tb.stop()
    tb.wait()
    print("Minimal GNU Radio flowgraph stopped.") 