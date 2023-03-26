#!/usr/bin/env python
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import math
import cv2
import numpy as np
import os 
from EAR import eye_aspect_ratio
from MAR import mouth_aspect_ratio
from HeadPose import getHeadTiltAndCoords
from ImageAlignmentScript import imgAlig

EYE_AR_THRESH = 0.25
MOUTH_AR_THRESH = 0.7
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0
detected= 0
iouSum= 0

def calculate_iou(box1, box2):
    #calculated for each object in each image separately
    # determine the coordinates of the intersection rectangle
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    # calculate the area of intersection rectangle
    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    # calculate the area of both the prediction and ground-truth rectangles
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    # calculate the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection / float(box1_area + box2_area - intersection)
    return iou

def calculate_av_iou(detected, iouSum):
    return iouSum/detected
    

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    './dlib_shape_predictor/shape_predictor_68_face_landmarks.dat')

time.sleep(2.0)

# 400x225 to 1024x576
frame_width = 1024
frame_height = 576

# loop over the frames from the video stream
# 2D image points. If you change the image, you need to change vector
image_points = np.array([
    (359, 391),     # Nose tip 34
    (399, 561),     # Chin 9
    (337, 297),     # Left eye left corner 37
    (513, 301),     # Right eye right corne 46
    (345, 465),     # Left Mouth corner 49
    (453, 469)      # Right mouth corner 55
], dtype="double")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

annotatedImg = imgAlig()


images= os.listdir("./Annotations_Images")

for item in annotatedImg:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    path=item[0]
    annotations =item[1]
    
    for i in range(len(images)):
       if(images[i]==path):
            
            frame=cv2.imread('./Annotations_Images/%s' %(item[0]))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            size = gray.shape
            
            # detect faces in the grayscale frame
            rects = detector(gray, 0)

            # check to see if a face was detected, and if so, draw the total
            # number of faces on the frame
            if len(rects) > 0:
                text = "{} face(s) found".format(len(rects))
                cv2.putText(frame, text, (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                detected+=1

            # loop over the face detections
            for idx,rect in enumerate(rects):
                 
                # compute the bounding box of the face and draw it on the
                # frame
                
                bX= rect.left()
                bW= rect.right() - rect.left()
                bY= rect.top()
                bH= rect.bottom() - rect.top()           
                
                iouRectFormat=[rect.left(),rect.top(),rect.right(),rect.bottom()]
                
                iou=calculate_iou(annotations, iouRectFormat)
                iouSum += iou
                av_iou = calculate_av_iou(detected,iouSum)
                print(iou)
                
                aX,aY,aW,aH = annotations
                
                cv2.rectangle(frame, (aX, aY), (aW, aH), (0, 255, 0), 1)
                cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (255, 0, 0), 1)
                
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                    # if the eyes were closed for a sufficient number of times
                    # then show the warning
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        cv2.putText(frame, "Eyes Closed!", (500, 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # otherwise, the eye aspect ratio is not below the blink
                    # threshold, so reset the counter and alarm
                else:
                    COUNTER = 0

                mouth = shape[mStart:mEnd]

                mouthMAR = mouth_aspect_ratio(mouth)
                mar = mouthMAR
                # compute the convex hull for the mouth, then
                # visualize the mouth
                mouthHull = cv2.convexHull(mouth)

                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, "MAR: {:.2f}".format(mar), (650, 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Draw text if mouth is open
                if mar > MOUTH_AR_THRESH:
                    cv2.putText(frame, "Yawning!", (800, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


                # loop over the (x, y)-coordinates for the facial landmarks
                # and draw each of them
                for (i, (x, y)) in enumerate(shape):
                    if i == 33:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[0] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    elif i == 8:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[1] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    elif i == 36:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[2] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    elif i == 45:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[3] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    elif i == 48:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[4] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    elif i == 54:
                        # something to our key landmarks
                        # save to our new key point list
                        # i.e. keypoints = [(i,(x,y))]
                        image_points[5] = np.array([x, y], dtype='double')
                        # write on frame in Green
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                    else:
                        # everything to all other landmarks
                        # write on frame in Red
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                        cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
                    
            #Draw the determinant image points onto the person's face
            for p in image_points:
                cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

            (head_tilt_degree, start_point, end_point, 
                end_point_alt) = getHeadTiltAndCoords(size, image_points, frame_height)

            cv2.line(frame, start_point, end_point, (255, 0, 0), 2)
            cv2.line(frame, start_point, end_point_alt, (0, 0, 255), 2)

            if head_tilt_degree:
                cv2.putText(frame, 'Head Tilt Degree: ' + str(head_tilt_degree[0]), (170, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # extract the mouth coordinates, then use the
        # coordinates to compute the mouth aspect ratio
            # show the frameq
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(10000) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break


print('AverageIoU',av_iou)
# do a bit of cleanup
cv2.destroyAllWindows()

