from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

# 在QApplication之前先实例化
uiLoader = QUiLoader()

class Stats:

    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load('main.ui')

    # 其它代码 ...

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec() # PySide6 是 exec 而不是 exec_