# import the require packages.
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject
from PyQt5 import QtCore
import sys
import time


class CaptureIpCameraFramesWorker(QThread):
    # Signal emitted when a new image or a new frame is ready.
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        # Declare and initialize instance variables.
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False

    def run(self) -> None:
        # Capture video from a network stream.
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        # Get default video FPS.
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        print(self.url)
        # If video capturing has been initialized already.q
        if cap.isOpened():
            # While the thread is active.
            while self.__thread_active:
                #
                if not self.__thread_pause:
                    # Grabs, decodes and returns the next video frame.
                    ret, frame = cap.read()
                    # Get the frame height, width and channels.
                    height, width, channels = frame.shape
                    # Calculate the number of bytes per line.
                    bytes_per_line = width * channels
                    # If frame is read correctly.
                    if ret:
                        # Convert image from BGR (cv2 default color format) to RGB (Qt default color format).
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # Convert the image to Qt format.
                        qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        # Scale the image.
                        # qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio)  # 720p
                        qt_rgb_image_scaled = qt_rgb_image.scaled(1920, 1080, Qt.KeepAspectRatio) # 1080p
                        # Emit this signal to notify that a new image or frame is available.
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                    else:
                        break
        # When everything done, release the video capture object.
        cap.release()
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0
        self.url_1 = "rtsp://admin:123456@10.252.73.31/stream0"
        self.url_2 = "rtsp://admin:123456@10.252.73.32/stream0"
        self.url_3 = "rtsp://admin:123456@10.252.11.34/stream0"
        self.url_4 = "rtsp://admin:123456@10.252.11.35/stream0"
        self.url_5 = "rtsp://admin:123456@10.252.11.36/stream0"
        self.url_6 = "rtsp://admin:123456@10.252.11.37/stream0"
        # self.url_7 = "rtsp://admin:123456@10.252.11.38/stream0"
        # self.url_8 = "rtsp://admin:123456@10.252.11.39/stream0"
        # self.url_9 = "rtsp://admin:123456@10.252.11.40/stream0"

        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}

        # Create an instance of a QLabel class to show camera 1.
        self.camera_1 = QLabel()
        self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_1.setScaledContents(True)
        self.camera_1.installEventFilter(self)
        self.camera_1.setObjectName("Camera_1")
        self.list_of_cameras_state["Camera_1"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 1 image.
        self.QScrollArea_1 = QScrollArea()
        self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_1.setWidgetResizable(True)
        self.QScrollArea_1.setWidget(self.camera_1)

        # Create an instance of a QLabel class to show camera 2.
        self.camera_2 = QLabel()
        self.camera_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_2.setScaledContents(True)
        self.camera_2.installEventFilter(self)
        self.camera_2.setObjectName("Camera_2")
        self.list_of_cameras_state["Camera_2"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 2 image.
        self.QScrollArea_2 = QScrollArea()
        self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_2.setWidgetResizable(True)
        self.QScrollArea_2.setWidget(self.camera_2)

        # Create an instance of a QLabel class to show camera 3.
        self.camera_3 = QLabel()
        self.camera_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_3.setScaledContents(True)
        self.camera_3.installEventFilter(self)
        self.camera_3.setObjectName("Camera_3")
        self.list_of_cameras_state["Camera_3"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 3 image.
        self.QScrollArea_3 = QScrollArea()
        self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_3.setWidgetResizable(True)
        self.QScrollArea_3.setWidget(self.camera_3)

        # Create an instance of a QLabel class to show camera 4.
        self.camera_4 = QLabel()
        self.camera_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_4.setScaledContents(True)
        self.camera_4.installEventFilter(self)
        self.camera_4.setObjectName("Camera_4")
        self.list_of_cameras_state["Camera_4"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 4 image.
        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.camera_4)

        # Create an instance of a QLabel class to show camera 5.
        self.camera_5 = QLabel()
        self.camera_5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_5.setScaledContents(True)
        self.camera_5.installEventFilter(self)
        self.camera_5.setObjectName("Camera_5")
        self.list_of_cameras_state["Camera_5"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 5 image.
        self.QScrollArea_5 = QScrollArea()
        self.QScrollArea_5.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_5.setWidgetResizable(True)
        self.QScrollArea_5.setWidget(self.camera_5)

        # Create an instance of a QLabel class to show camera 6.
        self.camera_6 = QLabel()
        self.camera_6.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_6.setScaledContents(True)
        # self.camera_6.installEventFilter(self)
        self.camera_6.setObjectName("Camera_6")
        self.list_of_cameras_state["Camera_6"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 6 image.
        self.QScrollArea_6 = QScrollArea()
        self.QScrollArea_6.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_6.setWidgetResizable(True)
        self.QScrollArea_6.setWidget(self.camera_6)

        # # Create an instance of a QLabel class to show camera 7.
        # self.camera_7 = QLabel()
        # self.camera_7.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.camera_7.setScaledContents(True)
        # # self.camera_7.installEventFilter(self)
        # self.camera_7.setObjectName("Camera_7")
        # self.list_of_cameras_state["Camera_7"] = "Normal"
        #
        # # Create an instance of a QScrollArea class to scroll camera 7 image.
        # self.QScrollArea_7 = QScrollArea()
        # self.QScrollArea_7.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_7.setWidgetResizable(True)
        # self.QScrollArea_7.setWidget(self.camera_6)
        #
        # # Create an instance of a QLabel class to show camera 8.
        # self.camera_8 = QLabel()
        # self.camera_8.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.camera_8.setScaledContents(True)
        # # self.camera_8.installEventFilter(self)
        # self.camera_8.setObjectName("Camera_8")
        # self.list_of_cameras_state["Camera_8"] = "Normal"
        #
        # # Create an instance of a QScrollArea class to scroll camera 8 image.
        # self.QScrollArea_8 = QScrollArea()
        # self.QScrollArea_8.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_8.setWidgetResizable(True)
        # self.QScrollArea_8.setWidget(self.camera_8)
        #
        # # Create an instance of a QLabel class to show camera 9.
        # self.camera_9 = QLabel()
        # self.camera_9.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.camera_9.setScaledContents(True)
        # # self.camera_9.installEventFilter(self)
        # self.camera_9.setObjectName("Camera_9")
        # self.list_of_cameras_state["Camera_9"] = "Normal"
        #
        # # Create an instance of a QScrollArea class to scroll camera 9 image.
        # self.QScrollArea_9 = QScrollArea()
        # self.QScrollArea_9.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_9.setWidgetResizable(True)
        # self.QScrollArea_9.setWidget(self.camera_9)

        # Set the UI elements for this Widget class.
        self.__SetupUI()

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1)
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_2)
        self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_3)
        self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.url_4)
        self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_5 = CaptureIpCameraFramesWorker(self.url_5)
        self.CaptureIpCameraFramesWorker_5.ImageUpdated.connect(lambda image: self.ShowCamera5(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_6 = CaptureIpCameraFramesWorker(self.url_6)
        self.CaptureIpCameraFramesWorker_6.ImageUpdated.connect(lambda image: self.ShowCamera6(image))

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_7 = CaptureIpCameraFramesWorker(self.url_7)
        # self.CaptureIpCameraFramesWorker_7.ImageUpdated.connect(lambda image: self.ShowCamera7(image))
        #
        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_8 = CaptureIpCameraFramesWorker(self.url_8)
        # self.CaptureIpCameraFramesWorker_8.ImageUpdated.connect(lambda image: self.ShowCamera8(image))
        #
        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_9 = CaptureIpCameraFramesWorker(self.url_9)
        # self.CaptureIpCameraFramesWorker_9.ImageUpdated.connect(lambda image: self.ShowCamera9(image))

        # Start the thread getIpCameraFrameWorker_1.
        self.CaptureIpCameraFramesWorker_1.start()

        # Start the thread getIpCameraFrameWorker_2.
        self.CaptureIpCameraFramesWorker_2.start()

        # Start the thread getIpCameraFrameWorker_3.
        self.CaptureIpCameraFramesWorker_3.start()

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_4.start()

        # Start the thread getIpCameraFrameWorker_5.
        self.CaptureIpCameraFramesWorker_5.start()

        # Start the thread getIpCameraFrameWorker_6.
        self.CaptureIpCameraFramesWorker_6.start()

        # # Start the thread getIpCameraFrameWorker_7.
        # self.CaptureIpCameraFramesWorker_7.start()

        # # Start the thread getIpCameraFrameWorker_8.
        # self.CaptureIpCameraFramesWorker_8.start()
        #
        # # Start the thread getIpCameraFrameWorker_9.
        # self.CaptureIpCameraFramesWorker_9.start()

    def __SetupUI(self) -> None:
        # Create an instance of a QGridLayout layout.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.QScrollArea_1, 0, 0)
        grid_layout.addWidget(self.QScrollArea_2, 0, 1)
        grid_layout.addWidget(self.QScrollArea_3, 0, 2)
        grid_layout.addWidget(self.QScrollArea_4, 1, 0)
        grid_layout.addWidget(self.QScrollArea_5, 1, 1)
        grid_layout.addWidget(self.QScrollArea_6, 1, 2)
        # grid_layout.addWidget(self.QScrollArea_7, 2, 0)
        # grid_layout.addWidget(self.QScrollArea_8, 2, 1)
        # grid_layout.addWidget(self.QScrollArea_9, 2, 2)

        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)

        # Set the central widget.
        self.setCentralWidget(self.widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'black';}")
        self.setWindowIcon(QIcon(QPixmap("camera_2.png")))
        # Set window title.
        self.setWindowTitle("UVINet rtsp viewer")

    @QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage) -> None:
        self.camera_1.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    @QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    @QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    @QtCore.pyqtSlot()
    def ShowCamera4(self, frame: QImage) -> None:
        self.camera_4.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    @QtCore.pyqtSlot()
    def ShowCamera5(self, frame: QImage) -> None:
        self.camera_5.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    @QtCore.pyqtSlot()
    def ShowCamera6(self, frame: QImage) -> None:
        self.camera_6.setPixmap(QPixmap.fromImage(frame))
        time.sleep(1)

    # @QtCore.pyqtSlot()
    # def ShowCamera7(self, frame: QImage) -> None:
    #     self.camera_7.setPixmap(QPixmap.fromImage(frame))

    # @QtCore.pyqtSlot()
    # def ShowCamera8(self, frame: QImage) -> None:
    #     self.camera_8.setPixmap(QPixmap.fromImage(frame))
    #
    # @QtCore.pyqtSlot()
    # def ShowCamera9(self, frame: QImage) -> None:
    #     self.camera_9.setPixmap(QPixmap.fromImage(frame))

    # # Override method for class MainWindow.
    # def eventFilter(self, source: QObject, event: QEvent) -> bool:
    #     """
    #     Method to capture the events for objects with an event filter installed.
    #     :param source: The object for whom an event took place.
    #     :param event: The event that took place.
    #     :return: True if event is handled.
    #     """
    #     #
    #     if event.type() == QtCore.QEvent.MouseButtonDblClick:
    #         if source.objectName() == 'Camera_1':
    #             #
    #             if self.list_of_cameras_state["Camera_1"] == "Normal":
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.QScrollArea_5.hide()
    #                 self.list_of_cameras_state["Camera_1"] = "Maximized"
    #             else:
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_4.show()
    #                 self.QScrollArea_5.show()
    #                 self.list_of_cameras_state["Camera_1"] = "Normal"
    #         elif source.objectName() == 'Camera_2':
    #             #
    #             if self.list_of_cameras_state["Camera_2"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.QScrollArea_5.hide()
    #                 self.list_of_cameras_state["Camera_2"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_4.show()
    #                 self.QScrollArea_5.show()
    #                 self.list_of_cameras_state["Camera_2"] = "Normal"
    #         elif source.objectName() == 'Camera_3':
    #             #
    #             if self.list_of_cameras_state["Camera_3"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.QScrollArea_5.hide()
    #                 self.list_of_cameras_state["Camera_3"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_4.show()
    #                 self.QScrollArea_5.show()
    #                 self.list_of_cameras_state["Camera_3"] = "Normal"
    #         elif source.objectName() == 'Camera_4':
    #             #
    #             if self.list_of_cameras_state["Camera_4"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_5.hide()
    #                 self.list_of_cameras_state["Camera_4"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_5.show()
    #                 self.list_of_cameras_state["Camera_4"] = "Normal"
    #         elif source.objectName() == 'Camera_5':
    #             #
    #             if self.list_of_cameras_state["Camera_5"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.list_of_cameras_state["Camera_5"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_4.show()
    #                 self.list_of_cameras_state["Camera_5"] = "Normal"
    #         else:
    #             return super(MainWindow, self).eventFilter(source, event)
    #         return True
    #     else:
    #         return super(MainWindow, self).eventFilter(source, event)

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        # If thread getIpCameraFrameWorker_1 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_1.isRunning():
            self.CaptureIpCameraFramesWorker_1.quit()
        # If thread getIpCameraFrameWorker_2 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_2.isRunning():
            self.CaptureIpCameraFramesWorker_2.quit()
        # If thread getIpCameraFrameWorker_3 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_3.isRunning():
            self.CaptureIpCameraFramesWorker_3.quit()
        # If thread getIpCameraFrameWorker_4 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_4.isRunning():
            self.CaptureIpCameraFramesWorker_4.quit()
        # If thread getIpCameraFrameWorker_5 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_5.isRunning():
            self.CaptureIpCameraFramesWorker_5.quit()
        # If thread getIpCameraFrameWorker_6 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_6.isRunning():
            self.CaptureIpCameraFramesWorker_6.quit()
        # # If thread getIpCameraFrameWorker_7 is running, then exit it.
        # if self.CaptureIpCameraFramesWorker_7.isRunning():
        #     self.CaptureIpCameraFramesWorker_7.quit()
        # # If thread getIpCameraFrameWorker_8 is running, then exit it.
        # if self.CaptureIpCameraFramesWorker_8.isRunning():
        #     self.CaptureIpCameraFramesWorker_8.quit()
        # # If thread getIpCameraFrameWorker_9 is running, then exit it.
        # if self.CaptureIpCameraFramesWorker_9.isRunning():
        #     self.CaptureIpCameraFramesWorker_9.quit()
        # Accept the event
        event.accept()


def main() -> None:
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    window = MainWindow()
    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
