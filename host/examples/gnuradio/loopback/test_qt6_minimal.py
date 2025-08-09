import sys
from PyQt6.QtWidgets import QApplication, QWidget

print('DEBUG: Minimal PyQt6 test script start')
app = QApplication(sys.argv)
print('DEBUG: QApplication created')
window = QWidget()
window.setWindowTitle('Minimal PyQt6 Test')
window.show()
print('DEBUG: QWidget created and shown')
app.exec()
print('DEBUG: QApplication exec finished') 