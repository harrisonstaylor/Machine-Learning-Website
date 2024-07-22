import json, os

#path to the annotations from the dataset
ANNOTATIONS_PATH = r'\annotations\\'

#dictionary containing all the class ids and corresponding integers they were assigned
CLASS_ID_DICT = {}

#An integer keeping track of the number of classes in the dataset
NUM_CLASSES = 0

"""
Returns the integer associated with the class_id_str in the dictionary. If one does not exist 
    Args:
        class_id_str (string): A string containing the class_id associated with a bounding box
    Returns:
        an integer associated with the class_id_str in the global dictionary
"""
def add_or_get_dict_value(class_id_str):
    if class_id_str in CLASS_ID_DICT:
        return CLASS_ID_DICT[class_id_str]
    else:
        global NUM_CLASSES
        CLASS_ID_DICT[class_id_str] = NUM_CLASSES
        NUM_CLASSES += 1
        return CLASS_ID_DICT[class_id_str]


"""
Writes a text file with all values from the global class_id dictionary
    Args:
        
    Returns:
        
"""
def create_dict_file():
    f = open(r'annotations_with_yolo\annotations_dict.txt', 'x')
    f.write('{\n')
    for key, value in CLASS_ID_DICT.items():
        f.write(str(value)+':'+key+'\n')
    f.write('}')
    f.close()


"""
Writes a text file with all values of bounding boxes associated with images into a Yolov8 legible format
    Args:

    Returns:
"""
def create_text_file(filename, bboxs):
    f = open(r'\annotations_with_yolo\\'+filename, 'x')
    for bbox in bboxs:
        f.write(str(bbox[0])+' '+str(bbox[1])+' '+str(bbox[2])+' '+str(bbox[3])+' '+str(bbox[4])+'\n')
    f.close()
    return

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
Calculates the center values of a bounding box and the relative width and height of the bounding box according to Yolov8 format
    Args:
        xmin: the xmin value of the bounding box
        xmax: the xmax value of the bounding box
        ymin: the ymin value of the bounding box
        ymax: the ymax value of the bounding box
        img_width: the width of the image
        img_height: the height of the image
    Returns:
        rel_x_center: the relative center x coord of the bounding box 
        rel_y_center: the relative center y coord of the bounding box 
        rel_width: the relative width of the bounding box
        rel_height: the relative height of the bounding box
"""
def calc_center(xmin, xmax, ymin, ymax, img_width, img_height):
    #calc the bounding box width and height
    bbox_width = abs(xmax - xmin)
    bbox_height = abs(ymax - ymin)

    #divide and floor x_center and y_center
    x_center = (xmax + xmin) // 2
    y_center = (ymax + ymin) // 2

    #calculate the relative center of the bbox and round to 3 decimal places
    rel_x_center = round(x_center / img_width, 3)
    rel_y_center = round(y_center / img_height, 3)

    #calculate the relative width and height of the bbox and round to 3 decimal places
    rel_width = round(bbox_width / img_width, 3)
    rel_height = round(bbox_height / img_height, 3)

    return rel_x_center, rel_y_center, rel_width, rel_height

"""
Takes all json files from a directory and retrieves relevant values for center calculation
    Args:
    
    Returns:
"""
def convert_all_files():
    for filename in os.listdir(ANNOTATIONS_PATH):
        #get the string we will eventually write the text file to
        filename_txt = filename.replace('.json','.txt')
        #read the json in with the src filepath
        json = read_json(ANNOTATIONS_PATH+filename)
        #get the width of the image from the json
        width = json['width']
        #get the height of the image from the json
        height = json['height']
        #make a list for all bboxes in an image
        bboxes = []
        #loop through all the object tags of the json
        for obj in json['objects']:
            #get the class_id
            label_id = obj['label']
            #conver the id to an int for yolo
            class_id = add_or_get_dict_value(label_id)
            #get the x and y values from the json
            xmin = obj['bbox']['xmin']
            ymin = obj['bbox']['ymin']
            xmax = obj['bbox']['xmax']
            ymax = obj['bbox']['ymax']
            #create the center coords
            rel_x_center, rel_y_center, rel_width, rel_height = calc_center(xmin, xmax, ymin, ymax, width, height)
            #create a bbox list with the class id and all coordinate values
            bbox = [str(add_or_get_dict_value(class_id)), rel_x_center, rel_y_center, rel_width, rel_height]
            #append the bbox to the list of bboxes
            bboxes.append(bbox)
        #create the text file for this json file
        create_text_file(filename_txt, bboxes)
    #create the output dict file
    create_dict_file()


if __name__ == '__main__':
    convert_all_files()
