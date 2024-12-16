import sys
import numpy as np
from view.src import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    np.set_printoptions(precision=3,suppress=True)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
