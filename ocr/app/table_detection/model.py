import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os


class Model:
    confThreshold = 0.25  # Confidence threshold
    nmsThreshold = 0.25  # Non-maximum suppression threshold

    inpWidth = 416  # Width of network's input image
    inpHeight = 416  # Height of network's input image

    def __init__(self):
        # Give the configuration and weight files for the model and load the network using them.
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.modelConfiguration = os.path.join(dir_path, 'model_files', 'tablasFinaltest416320.cfg')
        self.modelWeights = os.path.join(dir_path, 'model_files', 'tablasFinaltrain_10000.weights')
        self.classesFile = os.path.join(dir_path, 'model_files', 'vocTablas.names')
        self.classes = None
        self.net = None

    # Load the model and classes.
    def build_model(self):
        # Load names of classes
        with open(self.classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.net = cv.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    def predict(self, image_path):
        """
            Create a 4D blob from a frame.

            Args:
                image_path: image path to predict
            Returns:
                A list of lists. Each list contains [left, top, right, bottom] of the predicted table
        """
        frame = cv.imread(image_path)
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames())

        # Remove the bounding boxes with low confidence
        boxes = self.postprocess(frame, outs)
        self.showImage(frame)
        return boxes

    # Get the names of the output layers
    def getOutputsNames(self):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()

        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # Draw the predicted bounding box
    def drawPred(self, frame, classId, conf, left, top, right, bottom):
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

        label = '%.2f' % conf

        # Get the label for the class name and its confidence
        if self.classes:
            assert (classId < len(self.classes))
            label = '%s:%s' % (self.classes[classId], label)

        # Display the label at the top of the bounding box
        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, left + width, top + height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            right = box[2]
            bottom = box[3]
            self.drawPred(frame, classIds[i], confidences[i], left, top, right, bottom)
        return boxes

    @staticmethod
    def showImage(image):
        if len(image.shape) == 3:
            img2 = image[:, :, ::-1]
            plt.imshow(img2)
            plt.show()
        else:
            img2 = image
            plt.imshow(img2, cmap='gray')
            plt.show()

