import sys
import Leap
from VirtualScreen import VirtualScreen



class SampleListener(Leap.Listener):

    def on_init(self, controller):
        self.Vscreen =  VirtualScreen()

    def on_frame(self, controller):
        frame = controller.frame()

        hand = frame.hands[0]

        finger = None

        for i in hand.fingers:
            if(i.type()==1):
                finger=i
                break

        if finger is not None :
            position = finger.tip_position.to_float_array()
            vitesse = finger.tip_velocity.to_float_array()
            direction = finger.direction.to_float_array()

            print self.Vscreen.getScreenZonePointedAt(position,direction)
        
            # print position
            # print vitesse
            # print direction    
        

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
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
