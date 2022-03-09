import threading

exitFlag = 0

class myThread (threading.Thread):

    def __init__(self, threadID, function, file, sheet):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.function = function
      self.sheet = sheet
      self.file = file
    
    def run(self):
        self.function(self.file,self.sheet)