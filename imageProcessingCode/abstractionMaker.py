from pyexpat.errors import XML_ERROR_UNKNOWN_ENCODING
#from cameraDriver import takeAPicture
import cv2.aruco  as aruco
import cv2 as cv
import numpy as np
import os
import math
import sys
sys.path.insert(1, './motorEmbeddedCode')
import piece



def modified_binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if  arr[mid-1] < x < arr[mid]:
            return mid
        
        if mid == 0:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return modified_binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return modified_binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1

# image, marker size, then for drawing
def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True, original=False):

    # filter the image to be gray, better for image detection
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # get the keys for the specific aruco marker resolution
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')

    # build a dictionary using those keys
    arucoDict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL) if original else aruco.Dictionary_get(key)
    
    # define detector parameters (EMPTY)
    arucoParam = aruco.DetectorParameters_create()

    arucoParam.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
    arucoParam.adaptiveThreshConstant = 10


    # detect the markers
    coords, ids, rejected = aruco.detectMarkers(imgGray, arucoDict)

    # draw them if draw is enabled
    if draw:
        aruco.drawDetectedMarkers(img, coords)

    # return the (x1, y1) and (x2, y2) coords and the corresponding ids
    # print(rejected)
    return [coords, ids]

def augmentAruco(bbox, id, img, imgAug, drawId=True, drawPoint=False):

    # get the 4 points of the drawn bbox
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    # get size of image 
    h,w,c = imgAug.shape
    
    # preprocess the data for warping
    pts1 = np.array([tl,tr,br,bl])
    pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])
    M, _ = cv.findHomography(pts2,pts1)

    # warps the dictionary key 
    imgOut = cv.warpPerspective(imgAug, M, (img.shape[1], img.shape[0]))

    cv.fillConvexPoly(img, pts1.astype(int), (0,0,0))

    imgOut = img + imgOut

    if drawId:
        cv.putText(imgOut, str(id), (int(tl[0]), int(tl[1])), cv.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)

    if drawPoint:

        midX = int((int(tl[0]) + int(br[0])) / 2)
        
        midY = int((int(tl[1]) + int(br[1])) / 2)

        cv.circle(imgOut, (midX, midY), radius=0, color=(0, 0, 255), thickness=6)

    return imgOut

def loadAugImages(path):

    # fetch list of all the files in path
    myList = os.listdir(path)
    myList.remove(".DS_Store")

    # get how many markers we have
    # numberOfMarkers = len(myList)

    # declare dictionary for the key/value pair of markers
    augDics = {}

    # get the keys ("key".png)
    # map each key number to an array of image.
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0])
        imgAug = cv.imread(f'{path}/{imgPath}')

        augDics[key] = imgAug
    
    return augDics

# need to edit this for the final one, y_inc/x_inc must be divide dy 12 on our actual board
def updateChesboard(chessboard, xBounds, yBounds, x, y, detectedPiece):

    # pieceIndex_x = modified_binary_search(xBounds, 0, len(xBounds)-1, x)
    # pieceIndex_y = modified_binary_search(yBounds, 0, len(yBounds)-1, y)

    pieceIndex_x = math.floor(x/xBounds[0])
    pieceIndex_y = math.floor(y/yBounds[0])


    chessboard[pieceIndex_x][pieceIndex_y] = detectedPiece
    
    return pieceIndex_x, pieceIndex_y

def getAbstraction():
    
    # set up a video stream to take pictures frmo
    # takeAPicture()
    img = cv.imread('chessboard.jpg')

    # loads up images using a value (aruco id) and key (image)
    augDics = loadAugImages("./imageProcessingCode/images")

    #inputs -- 
    blurKernel = (7,7)
    dilateKernel = (1,1)
    epsilon = 0.05

    # more advanced inputs -- make sure to test before changing these
    thresBlockSize = 31
    thresConstant = 0.001
    cannyUpper = 200
    cannyLower = 50

    # these are better for image processing -- gray and the gaussian blur needs to be tuned to the image
    frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(frame, blurKernel , 0)

    # then use adaptive thresholding (because there may be different illumation parts)
    # inputs: image, max_value, adaptive_method, threshold_type, block_size (of neighboring area), c (constant)
    # we use the mean of the neighborhood area 
    th1 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, thresBlockSize, thresConstant)

    # canny method to detect the edges of the picture
    edge = cv.Canny(th1, cannyUpper, cannyLower)

    # dialation, apparently it enhances the results IT DOES, the kernel area affects alot
    imgDil = cv.dilate(edge, np.ones(dilateKernel), iterations=1)

    cnts , _ = cv.findContours(imgDil , cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # getting countour with largest area 
    curMaxArea = 0
    maxContour = None
    for contour in cnts:
        # Trues are to signify if our contours are closed loop
        approx = cv.approxPolyDP(contour, epsilon * cv.arcLength(contour, True), True)
        curArea = cv.contourArea(approx)

        if(curArea > curMaxArea and len(approx) == 4):
            curMaxArea = curArea
            maxContour = [approx]

    if maxContour == None:
        #if chessboard not found, try again
        takeAPicture()
        return getAbstraction() 


    # WARPING part
    sanitizedPts = []
    for i in range(4):
        sanitizedPts.append(maxContour[0][i][0])


    # summing x,y terms to determine the tl
    minIndex = 0
    minSum = np.inf

    for i in range(len(sanitizedPts)):
        currentSum = sanitizedPts[i][0] + sanitizedPts[i][1]

        if currentSum < minSum:
            minSum = currentSum
            minIndex = i

    # counter - clockwise 
    tl = (sanitizedPts[minIndex][0], sanitizedPts[minIndex][1])
    bl = (sanitizedPts[(minIndex+1) % 4][0],  sanitizedPts[(minIndex+1) % 4][1])
    br = (sanitizedPts[(minIndex+2) % 4][0],  sanitizedPts[(minIndex+2) % 4][1])
    tr = (sanitizedPts[(minIndex+3) % 4][0],  sanitizedPts[(minIndex+3) % 4][1])


    squareSize = 1000
    src_pts = [tl, bl, tr, br]

    src_pts = np.float32(src_pts)
    dst_pts = np.float32([[0,0], [0, squareSize], [squareSize, 0], [squareSize, squareSize]])

    M = cv.getPerspectiveTransform(src_pts , dst_pts)

    warped = cv.warpPerspective(img, M, (squareSize , squareSize)) # The last parameter needs to be adjusted

    # flip the image horizontally to have the same origin
    # warped = cv.flip(warped, 1)
    (h, w) = warped.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    My = cv.getRotationMatrix2D((cX, cY), -90, 1.0)
    warped = cv.warpAffine(warped, My, (w, h))

    bundle = findArucoMarkers(warped, markerSize=4, totalMarkers=250, draw=True, original=True)

    coords = bundle[0]


    # need to update this for capture squares
    chessboard = None
    pieceArray = []
    x_row = 10
    y_col = 10


    
    if len(coords) != 0:
        # for visualization purposes ONLY

 
        for bbox, id in zip(bundle[0], bundle[1]):

            # guard in case it detects a random marker that doesnt exist
            val = augDics.get(int(id), "NOT-FOUND")

            # this is only for visualization purposes
            if val != "NOT-FOUND":
                warped = augmentAruco(bbox, id, warped, val, drawId=False, drawPoint=True)

            # img = augmentAruco(bbox, id, img, augDics[int(id)],drawId=False)

        # need to update this for capture squares
        chessboard = [["NA"]*x_row for i in range(y_col)]

        piecesDictionary = {69:"WR", 21:"BB", 5:"BK", 20:"BN", 4: "BR",
            68:"BP", 64:"BQ", 3:"WB", 1:"WK", 0:"WN", 80:"WP", 65:"WQ"}

        # setting bounds
        h,w,c = warped.shape

        # need to update this for capture squares also
        x_inc = w/x_row
        y_inc = h/y_col

        xBounds = []
        yBounds = []

        curX, curY = 0 , 0
        for i in range(x_row):
            curX+=x_inc
            curY+=y_inc
            xBounds.append(curX)
            yBounds.append(curY)

        for bbox, id in zip(bundle[0], bundle[1]):
                
            # find which piece we are dealing with 
            detectedPiece = piecesDictionary.get(int(id), "NOT-FOUND")

            if detectedPiece != "NOT-FOUND":
                #warped = augmentAruco(bbox, id, warped, val, drawId=False, drawPoint=True)

                tl = bbox[0][0][0], bbox[0][0][1]
                tr = bbox[0][1][0], bbox[0][1][1]
                br = bbox[0][2][0], bbox[0][2][1]
                bl = bbox[0][3][0], bbox[0][3][1]

                # midX = int((int(tl[0]) + int(br[0])) / 2)
                # midY = int((int(tl[1]) + int(br[1])) / 2)
                midX = int((int(tl[0]) + int(br[0])) / 2)
                midY = int((int(tl[1]) + int(br[1])) / 2)

                pieceIndex_x, pieceIndex_y = updateChesboard(chessboard, xBounds, yBounds, midX, midY, detectedPiece)
                #pieceArray.append()
                distX = midX*(508/1000)
                distY = midY*(508/1000)
                # print(warped.shape)
                # print(detectedPiece + " " + str(distY)  + "mm " + str(distX)+ "mm ")
                # print(str(pieceIndex_y) + " " + str(pieceIndex_x))
                currentPiece = piece.Piece(detectedPiece, pieceIndex_y, pieceIndex_x, distY, distX)
                pieceArray.append(currentPiece)


        # TO - DO ...add another for loop here that iterates through the coordinates and calls getAbstraction

    # ADD CHECK TO make sure t
    # here are 12 pieces


    if chessboard != None:
        transposed_array = list(zip(*chessboard))
    else:
        transposed_array = None

    #TODO: Comments these two out after debugging
    cv.imshow("Image", warped)
    cv.waitKey(0)
    # transposed_array = chessboard
    
    # if transposed_array != None:
    #     print("------ CHESSBOARD -----")
    #     for row in transposed_array:
    #         print(row)
    # else:
    #     print("No chessboard detected!")

    


    # rotating chessboard to make it the same as selenas code
    # rotatedChessboard = []
    # for row in chessboard:
    #     # res = row[::-1]
    #     rotatedChessboard.append(row)

    return transposed_array, pieceArray


if __name__ == "__main__":
  getAbstraction()

    

