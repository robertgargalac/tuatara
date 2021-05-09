import numpy as np
import cv2
import imutils
#from skimage.filters import threshold_local


class PageDetector:
    def process(self, image, scale_factor=500):
        ratio = image.shape[0] / scale_factor

        resized_image = imutils.resize(image, height=scale_factor)
        self.h_res_image, self.w_res_image, _ = resized_image.shape

        document_contour = self.__find_document(resized_image)
        camera_adjustments = self.check_document_position(document_contour)

        if True in camera_adjustments.values():
            return None, camera_adjustments

        rescaled_contour = document_contour.reshape(1, 4, 2)[0] * ratio
        warped = self.four_point_transform(image, rescaled_contour)
        warped_or = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        # Optional, use only if the document is noisy
        # t = threshold_local(warped_or, 11, offset=10, method="gaussian")
        # warped = (warped_or > t).astype("uint8") * 255
        return warped, camera_adjustments

    def __find_document(self, image):
        contours = self.__get_contours(image)
        approximated_shapes = []

        for c in contours:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            approximated_shapes.append(approx)

        document_contour = max(approximated_shapes, key=cv2.contourArea)
        return document_contour

    def check_document_position(self, doc_contour, margin_threshold=15):
        adjustments = {'right': False, 'left': False, 'top': False, 'bottom': False}
        max_x, max_y, min_x, min_y = self.get_extreme_coordinates(doc_contour)

        if min_x < margin_threshold:
            adjustments['right'] = True
        if self.w_res_image - margin_threshold < max_x:
            adjustments['left'] = True
        if min_y < margin_threshold:
            adjustments['top'] = True
        if self.h_res_image - margin_threshold < max_y:
            adjustments['bottom'] = True

        return adjustments

    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # set of destination points to obtain a "birds eye view",
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    @staticmethod
    def __get_contours(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours

    @staticmethod
    def get_extreme_coordinates(contour):
        coord_matrix = np.array([line for item in contour for line in item])
        max_x, max_y = coord_matrix.max(axis=0)
        min_x, min_y = coord_matrix.min(axis=0)
        return max_x, max_y, min_x, min_y

    @staticmethod
    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # the top-left point will have the smallest sum, whereas
        rect[2] = pts[np.argmax(s)]  # the bottom-right point will have the largest sum

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right point will have the smallest difference
        rect[3] = pts[np.argmax(diff)]  # bottom-left will have the largest difference
        return rect

