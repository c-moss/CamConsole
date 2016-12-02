class MotionCapture:
    def __init__(self, videoFile, imageFile=None, modDate=None):
        self.videoFile = videoFile
        self.imageFile = imageFile
        self.modDate = modDate

    @property
    def videoFile(self):
        return self.__videoFile

    @videoFile.setter
    def videoFile(self, f):
        self.__videoFile = f

    @property
    def imageFile(self):
        return self.__imageFile

    @imageFile.setter
    def imageFile(self, f):
        self.__imageFile = f

    @property
    def modDate(self):
        return self.__modDate

    @modDate.setter
    def modDate(self, d):
        self.__modDate = d
