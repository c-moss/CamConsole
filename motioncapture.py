class MotionCapture:
    def __init__(self, cameraId, fileName, frame, fileType, timestamp, eventTimestamp):
        self.cameraId = cameraId
        self.fileName = fileName
        self.frame = frame
        self.fileType = fileType
        self.timestamp = timestamp
        self.eventTimestamp = eventTimestamp

    @property
    def cameraId(self):
        return self.__cameraId

    @cameraId.setter
    def cameraId(self, f):
        self.__cameraId = f

    @property
    def fileName(self):
        return self.__fileName

    @fileName.setter
    def fileName(self, f):
        self.__fileName = f

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, f):
        self.__frame = f

    @property
    def fileType(self):
        return self.__fileType

    @fileType.setter
    def fileType(self, f):
        self.__fileType = f

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, f):
        self.__timestamp = f

    @property
    def eventTimestamp(self):
        return self.__eventTimestamp

    @eventTimestamp.setter
    def eventTimestamp(self, f):
        self.__eventTimestamp = f
