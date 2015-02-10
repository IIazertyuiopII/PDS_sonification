################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys
import Leap
import cPickle

class SampleFrameDataAccumulator(Leap.Listener):
    nFramesAccumulated = 0
    frameDataArray = []
    captureDuration = 0

    setEntries = []
    setResults = []
    Set = None
    currentSetSize = 0
    maxSetSize = 20

    sampleSize = 30
    filename = "TrainSet.pkl"

    mustBeKilled = False


    def to_file(self):
        self.Set = (self.setEntries,self.setResults)
        f = open(self.filename,"wb")
        cPickle.dump(self.Set, f, protocol=2)
        f.close()
        print "Successfully wrote Set data to file"
        self.mustBeKilled = True

    def from_file(self):
        f = open(self.filename,"rb")
        readData = cPickle.load(f)
        f.close()
        print readData

    def on_connect(self, controller):
        #self.from_file()
        pass

    def onSampleSizeReached(self,controller):
        controller.remove_listener(self)
        self.captureDuration = (controller.frame().timestamp - self.captureDuration)/1000
        print "--- Success"
        print "-"
        print "Wrote in "+self.filename+" %d frames, duration %f ms" % (self.sampleSize,self.captureDuration)
        n=int(input("Please enter the corresponding gesture number :"))
        self.setResults.append(n)
        self.setEntries.append(self.frameDataArray)
        self.currentSetSize=self.currentSetSize+1
        if(self.currentSetSize == self.maxSetSize):
            print "recording ends - reached %d samples" % (self.maxSetSize)
            self.to_file()
        else:
            raw_input("Press enter to record the next sample")
            self.nFramesAccumulated = 0
            self.frameDataArray = []
            controller.add_listener(self)

    def on_frame(self,controller):
        frame = controller.frame()
        if(self.nFramesAccumulated==0):
            print "starting sample recording"
            self.captureDuration=frame.timestamp

        if(self.nFramesAccumulated>self.sampleSize):
            self.onSampleSizeReached(controller)
            return
        
        frameData = []

        if len(frame.hands) == 0:
            print "Data capture aborted : no hand found"
            controller.remove_listener(self)
            return
        else:
            hand = frame.hands[0]

        # frameData.extend(hand.palm_position.to)
        # frameData.extend(hand.palm_normal)
        # frameData.extend(hand.direction)

        # Get fingers
        finger = None
        for i in hand.fingers:
            if(i.type()==1):
                finger=i
                break
        
        if finger is None:
            print "Data capture aborted : no finger found"
            controller.remove_listener(self)
            return

        frameData.extend(finger.direction.to_float_array())
        frameData.extend(finger.tip_position.to_float_array())

        self.frameDataArray.extend(frameData)
        self.nFramesAccumulated=self.nFramesAccumulated+1


def main():
    # Create a sample listener and controller
    listener = SampleFrameDataAccumulator()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    while(not listener.mustBeKilled):
        pass

if __name__ == "__main__":
    main()


