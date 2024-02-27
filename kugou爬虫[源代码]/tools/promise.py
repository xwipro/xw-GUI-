from PyQt5.QtWidgets import QMessageBox


def promain(name):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("下载完成提醒")
    msg_box.setText(f"您下载的 {name} 已经下载完成! ")
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

