################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys
import OSC
import math
sys.path.append("C:\Users\IAZERTYUIOPI\Documents\maths\cours_pure_data\LeapMotion\LeapSDK\lib")
sys.path.append("C:\Users\IAZERTYUIOPI\Documents\maths\cours_pure_data\LeapMotion\LeapSDK\lib\\x86")

import Leap, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def sendMSG(self,route_1,content,route_2=None):

        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/"+route_1)
        if(route_2 is not None):
            oscmsg.append("/"+route_2)
        oscmsg.append(content)
        self.client.send(oscmsg)

    def on_init(self, controller):

        print "############################Initalized############################"
        self.client = OSC.OSCClient()
        self.client.connect(('127.0.0.1', 5005))  


    def on_connect(self, controller):

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "############################Disconnected############################"

    def on_exit(self, controller):
        print "############################Exited############################"

    def on_frame(self, controller):
        frame = controller.frame()

        # print  "Gestes reconnus : %d" % (len(frame.gestures()))                

        # Get hands

        if len(frame.hands) == 0:
            self.sendMSG("positionMain",-1)
        else:
            hand = frame.hands[0]

            handType = "Left hand" if hand.is_left else "Right hand"

            distance = math.sqrt(hand.palm_position[1]*hand.palm_position[1] + hand.palm_position[2]*hand.palm_position[2] + hand.palm_position[3]*hand.palm_position[3])
            # print(distance)
            self.sendMSG("positionMain",distance)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
            #     direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            #     arm.direction,
            #     arm.wrist_position,
            #     arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type()],
                #     finger.id,
                #     finger.length,
                #     finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #     self.bone_names[bone.type],
                    #     bone.prev_joint,
                    #     bone.next_joint,
                    #     bone.direction)

        # Get tools
        # for tool in frame.tools:

            # print "  Tool id: %d, position: %s, direction: %s" % (
            #     tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                if circle.state is Leap.Gesture.STATE_START:
                    print "starting circle"
                if circle.state is Leap.Gesture.STATE_UPDATE:
                    print "updating circle"
                if circle.state is Leap.Gesture.STATE_STOP:
                    print "stopping circle"
                    self.sendMSG("events","bang","circle")

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                # print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                #         gesture.id, self.state_names[gesture.state],
                #         circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                if swipe.state is Leap.Gesture.STATE_START:
                    print "starting swipe"
                if swipe.state is Leap.Gesture.STATE_UPDATE:
                    print "updating swipe"
                if swipe.state is Leap.Gesture.STATE_STOP:
                    print "stopping swipe"
                    self.sendMSG("events","bang","swipe")

                # print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                #         gesture.id, self.state_names[gesture.state],
                #         swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                if keytap.state is Leap.Gesture.STATE_STOP:
                    print "keytap occurred"
                # print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                #         gesture.id, self.state_names[gesture.state],
                #         keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                if screentap.state is Leap.Gesture.STATE_STOP:
                    print "screentap occurred"
                # print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                #         gesture.id, self.state_names[gesture.state],
                #         screentap.position, screentap.direction )

        # if not (frame.hands.is_empty or frame.gestures().is_empty):
        #     print "------------------------------------------------------------\n"

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def controllerSetup(c):
    c.config.set("Gesture.Swipe.MinLength", 15.0)
    c.config.set("Gesture.Swipe.MinVelocity", 500)
    c.config.save()

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controllerSetup(controller)
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()


