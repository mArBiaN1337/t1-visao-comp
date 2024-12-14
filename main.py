import sys
from view.src import MainWindow
from PyQt5.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
