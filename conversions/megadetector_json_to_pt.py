"""Converts megadetector output JSON file to match Yolov8 pytortch txt format

A .yaml file with image directory and class information is needed to
train a Yolov8 model. The yaml file will need a format similar to 
the one described in the "EXAMPLE" section here:
https://roboflow.com/formats/yolov8-pytorch-txt

 Run as:
     python megadetector_json_to_csv.py output.json new_output.csv \
     /home/user/image_folder/
"""

import json
import csv
import os
import argparse
import random
import yaml
import shutil


def main():
    """Converts JSON data and writes to txt files

    Converts the JSON xywh bbox data to xyxy format and writes the
    data to txt files in the proper format [set, class, file, xmin, ymin,
    '', '', xmax, ymax, '', ''].
    """
    # pylint: disable=locally-disabled, too-many-locals
    # Get command line arguments when running program
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str,
                        help="filepath for the JSON input file")
    parser.add_argument("output_folder", type=str,
                        help="filepath for the txt output files")
    parser.add_argument("confidence", type=float,
                        help="confidence threshold for megadetector detections")
    args = parser.parse_args()

    # Opening JSON file and loading the data
    # into the variable
    with open(args.input_file, encoding="utf-8") as json_file:
        data = json.load(json_file)

    image_data = data['images']



    # For loop get to each image file name
    for img in image_data:
        
        # First check if file contains detections
        filename = img['file'][:-3] + 'txt'
        if 'failure' in img.keys():
            print(img['file'] + ' failed to access.\n')
        else:
            # Create a new text file for each image
            with open(args.output_folder + filename, 'w+') as text_file:
                for i in range(0, len(img['detections'])):
                    # Megadetector uses 3 categories 1-animal, 2-person,
                    # 3-vehicle, only the animal detections are needed
                    if img['detections'][i]['category'] == '1' and img['detections'][i]['conf'] >= args.confidence:
                        # Convert xmin, ymin, width, height json format to centerx, centery, width, height yolo format
                        xmin = img['detections'][i]['bbox'][0]
                        ymin = img['detections'][i]['bbox'][1]
                        width = img['detections'][i]['bbox'][2]
                        height = img['detections'][i]['bbox'][3]

                        center_x = xmin + (width / 2)
                        center_y = ymin + (height / 2)
                        
                        # Separate detections onto different lines
                        text_file.seek(0)
                        first_char = text_file.read(1)
                        if not first_char:
                            line = '0 ' + str(center_x) + ' ' + str(center_y) + ' ' + str(width) + ' ' + str(height)
                            text_file.write(line)
                        else:
                            line = '\n0 ' + str(center_x) + ' ' + str(center_y) + ' ' + str(width) + ' ' + str(height)
                            text_file.write(line)




if __name__ == "__main__":
    main()
