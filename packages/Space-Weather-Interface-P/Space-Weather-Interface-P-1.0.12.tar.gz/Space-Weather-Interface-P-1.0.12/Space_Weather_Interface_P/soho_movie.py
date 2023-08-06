import cv2
import os
import shutil

# get the path to the images folder relative to the script's directory
folder_path = r"./images/soho/"

# get a list of all the files in the folder
files = os.listdir(folder_path)

# sort the files alphabetically to ensure the frames of the video are in order
files.sort()

# create a list to hold all the image frames
frames = []

# loop through all the files and add each image as a frame
for file in files:
    # make sure we're only processing image files
    if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
        # read in the image using OpenCV and add it to the frames list
        img = cv2.imread(os.path.join(folder_path, file))
        frames.append(img)

# get the dimensions of the first frame to use for the output video
height, width, channels = frames[0].shape

# create a VideoWriter object to write the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # use XVID codec for AVI format
out = cv2.VideoWriter('soho.avi', fourcc, 24.0, (width, height), isColor=True)

# write each frame to the output video
for frame in frames:
    out.write(frame)

# release the VideoWriter object and close all windows
out.release()
cv2.destroyAllWindows()

# Set the original output file path
original_path = 'soho.avi'

# Set the new output file path
new_path = './images/soho.avi'

# Move the file to the new location
shutil.move(original_path, new_path)

