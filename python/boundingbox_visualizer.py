import cv2, json, os, random
import numpy as np

ANNOTATIONS_PATH = r'\annotations\\'

IMAGES_PATH = r'\Train1-data\images\\'

BBOX_IMAGE_PATH = r'\bbox_images\\'

NUM_CLASSES = 0

"""
Reads a json file and returns the data from the file
    Args:
        filename: a string containg the filepath of the json
    Returns:
        the data from the json file
"""
def read_json(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data

"""
Takes coordinates from json files and creates bounding boxes associated with an image of the same name as the json
    Args:
    
    Returns:
        
"""
def create_bbox_images():
  #loop thru the filenames in the directory
    for filename in os.listdir(IMAGES_PATH):
        #get the image string as a json so we can retreive the coordinate values
        filename_txt = filename.replace('.jpg', '.json')
        #read the json file in
        json = read_json(ANNOTATIONS_PATH + filename_txt)
        #make a bbox list for this image
        bboxes = []
        #loop through all the objects which contain bounding box data and retreive pertinent data
        for obj in json['objects']:
            label_id = obj['label']
            xmin = obj['bbox']['xmin']
            ymin = obj['bbox']['ymin']
            xmax = obj['bbox']['xmax']
            ymax = obj['bbox']['ymax']
            #append the current bbox to the list
            bboxes.append([label_id, xmin, ymin, xmax, ymax])
        #plot the bounding box on the image
        plot_bboxes(filename, bboxes)


"""
Plots the bounding boxes on the image and saves the img
    Args:
        filename: the name of the file associated with the image (string)
        bboxvalues: a list of bboxes that contains lists of coordinates and class_ids associated with the image
    Returns:
        img: an img object containing the bounding box and the original img details
"""
def plot_bboxes(filename, bboxvalues):
    #read in the image from the filename
    img = cv2.imread(IMAGES_PATH + filename)
    #loop through each bbox in the list
    for bbox in bboxvalues:
        #set a random color
        color = (random.randint(0, 123), random.randint(0, 123), random.randint(0, 123))
        #get the class label for this bounding box
        class_label = bbox[0]
        #create a numpy array and convert the floats from json to ints
        bbox = np.array(bbox[1:]).astype(int)
        #convert this back to a python list 
        bbox = bbox.tolist()
        #create a label from the class_id
        label = f"{class_label}"
        #set the label margin
        lbl_margin = 3  # label margin
        #create a rectangle based on the bbox coords, the color and a thickness
        img = cv2.rectangle(img, (bbox[0], bbox[1]),
                            (bbox[2], bbox[3]),
                            color,
                            thickness=3)
        #get the text size for the 
        label_size = cv2.getTextSize(label,  # labelsize in pixels
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale=1, thickness=1)
        #get the label width and height
        lbl_w, lbl_h = label_size[0] 
        # create margins
        lbl_w += 2 * lbl_margin  
        lbl_h += 2 * lbl_margin
        # plot label background
        img = cv2.rectangle(img, (bbox[0], bbox[1]),  
                            (bbox[0] + lbl_w, bbox[1] - lbl_h),
                            color=color,
                            thickness=-1)
        #put the text on the label
        cv2.putText(img, label, (bbox[0] + lbl_margin, bbox[1] - lbl_margin),  # write label to the image
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0, color=(255, 255, 255),  #white text
                    thickness=1)
    #write the image out to a file path
    cv2.imwrite(BBOX_IMAGE_PATH + filename, img)
    return img


if __name__ == '__main__':
    create_bbox_images()
