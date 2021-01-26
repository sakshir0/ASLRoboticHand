################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
import math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import csv
from numpy import *
import datetime

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print ("Frame id: {}, timestamp: {}, hands: {}, fingers: {}, tools: {}, gestures: {}" .format (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures())))

        # Get hands
        for hand in frame.hands:
            input = []
            input.append(frame.id)
            ts = frame.timestamp // 1000
            dt = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            input.append(dt)

            handType = "Left hand" if hand.is_left else "Right hand"

            print ("  {}, id {}, position: {}" .format (
                handType, hand.id, hand.palm_position))

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print ("  pitch: {} degrees, roll: {} degrees, yaw: {} degrees" .format (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG))

            # Get arm bone
            arm = hand.arm
            print ("  Arm direction: {}, wrist position: {}, elbow position: {}" .format (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position))

            
            # Finger tip locations
            thumb_tip = hand.fingers[0].bone(3).next_joint
            index_tip = hand.fingers[1].bone(3).next_joint
            middle_tip = hand.fingers[2].bone(3).next_joint
            ring_tip = hand.fingers[3].bone(3).next_joint
            pinky_tip = hand.fingers[4].bone(3).next_joint
            '''
            # Thumb tip to palm position
            palm_thumb = thumb_tip-hand.palm_position
            for i in range(0,3):
                input.append(palm_thumb[i])
            '''
            # Get fingers
            for finger in hand.fingers:

                print ("    {} finger, id: {}, length: {}mm, width: {}mm" .format (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width))

                #difference in top of finger to bottom
                diff = finger.bone(4).next_joint - finger.bone(0).prev_joint
                # for i in range(0,3):
                input.append(linalg.norm([diff[0], diff[1], diff[2]]))
                #   input.append(diff[i])


                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print ("      Bone: {}, start: {}, end: {}, direction: {}" .format (
                        self.bone_names[bone.type],
                        bone.prev_joint,
                        bone.next_joint,
                        bone.direction))
                    

                    '''
                    # Ignores the metacarpal thumb bone
                    if self.finger_names[finger.type] != 'Thumb' or b != 0:
                        diff = bone.next_joint-bone.prev_joint
                        for i in range(0,3):
                            input.append(diff[i])

                    # Calculate fingertip distances to thumb
                    if self.bone_names[bone.type] == 'Distal' and self.finger_names != 'Thumb':
                        diff = thumb_tip-bone.next_joint
                        for i in range(0,3):
                            input.append(diff[i])
                    

                    # Calculate promximal end to thumb tip (m,n,t)
                    if self.bone_names[bone.type] == 'Proximal' and self.finger_names != 'Thumb':
                        diff = thumb_tip-bone.next_joint
                        for i in range(0,3):
                            input.append(diff[i])
                    '''
            
            '''
            #Get direction of thumb
            # print(hand.fingers[0].bone(3).direction)
            dx = hand.fingers[0].bone(3).direction[0]
            dz = hand.fingers[0].bone(3).direction[2]
            input.append(math.atan(dx/dz))
            '''

            #IDEA 2: distance from tip to palm
            dist0 = thumb_tip - hand.palm_position
            dist1 = index_tip - hand.palm_position
            dist2 = middle_tip - hand.palm_position
            dist3 = ring_tip - hand.palm_position
            dist4 = pinky_tip - hand.palm_position

            input.append(linalg.norm([dist0[0], dist0[1], dist0[2]]))
            input.append(linalg.norm([dist1[0], dist1[1], dist1[2]]))
            input.append(linalg.norm([dist2[0], dist2[1], dist2[2]]))
            input.append(linalg.norm([dist3[0], dist3[1], dist3[2]]))
            input.append(linalg.norm([dist4[0], dist4[1], dist4[2]]))

            #IDEA 1: finger bend angle
            for i in range(0,5):
                prox = hand.fingers[i].bone(1).direction
                dist = hand.fingers[i].bone(3).direction
                dprod = prox[0]*dist[0] + prox[1]*dist[1] + prox[2]*dist[2]
                angle = math.acos(dprod)
                input.append(angle)

            #IDEA 3: knuckle slope (m,n,t)
            for i in range(0,5):
                boneT = hand.fingers[i].bone(2).direction
                dy = boneT[1]
                dz = boneT[2]
                angle = math.atan(dy/dz)
                input.append(angle)

            # Wrist
            input.append(normal.roll * Leap.RAD_TO_DEG)

            # Calculate consecutive fingertip distances
            if self.bone_names[bone.type] == 'Distal':
                diff0 = index_tip-thumb_tip
                diff1 = middle_tip-index_tip
                diff2 = ring_tip-middle_tip
                diff3 = pinky_tip-ring_tip
                for i in range(0,3):
                    input.append(diff0[i])
                    input.append(diff1[i])
                    input.append(diff2[i])
                    input.append(diff3[i])

            with open('data/fuckyou2/train_back.csv', mode = 'ab') as csv_file:
                wr = csv.writer(csv_file, dialect='excel')
                wr.writerow(input)
                csv_file.close()

        # Get tools
        for tool in frame.tools:

            print ("  Tool id: {}, position: {}, direction: {}" .format (
                tool.id, tool.tip_position, tool.direction))

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

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

                print ("  Circle id: {}, {}, progress: {}, radius: {}, angle: {} degrees, {}" .format (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness))

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print ("  Swipe id: {}, state: {}, position: {}, direction: {}, speed: {}" .format (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed))

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print ("  Key Tap id: {}, {}, position: {}, direction: {}" .format (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction ))

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print ("  Screen Tap id: {}, {}, position: {}, direction: {}" .format (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction ))

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ("")

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
