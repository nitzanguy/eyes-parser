import pandas as pd
from scipy import misc
from glob import glob
import os
import time


def add_semantic_labels(cur_file, input_file, maps_dir, wanted_features, wang_images_names,
                        participant_col_name, image_name_col,
                        binary_or_value, min_value_as_1,
                        fix_x_col_name, fix_y_col_name, resolution_divider_x, resolution_divider_y, image_size):
    """

    :param cur_file: the dataframe with the fixation locations
    :param input_file: the path of the input file. used for the output file
    :param maps_dir: the directory with the features directories
    :param wanted_features: the features of interest - each one have a unique directory in maps_dir
    :param wang_images_names: the names of the images as appeared in the image col
    :param participant_col_name: the name of the col with the participant name
    :param image_name_col: the name of the col with the image\stimulus name
    :param binary_or_value: value for a raw score and binary for 1\0 according to 'min_value_as_1'
    :param min_value_as_1: the min score for insert 1 in the binary mode (64 in wang paper)
    :param fix_x_col_name: the name of the col contains x position
    :param fix_y_col_name: the name of the col contains y position
    :param resolution_divider_x: presented x \ feature map x
    :param resolution_divider_y: presented y \ feature map y
    :param image_size: the size of the presented image
    :return:
    """
    # create a list for each features (updating the dataframe does not work with pandas)
    dict_features = {}
    for feature in wanted_features:
        dict_features[feature] = []

    # due to the long time reading images, first read the image of the certain feature and than go over the lines
    for feature in wanted_features:
        print "start reading the images of ", feature, time.asctime()
        dict_images = {}
        feature_images = glob(r'%s\%s\*.jpg' % (maps_dir, feature))
        for cur_image_path in feature_images:
            cur_image = misc.imread(cur_image_path)  # maybe need to be first for all images
            image_number = os.path.basename(cur_image_path)[:os.path.basename(cur_image_path).find('.')]  # only number
            dict_images[image_number] = cur_image

        print "Start going over the fixation for - ", feature, time.asctime()
        for line in cur_file.iterrows():
            if line[1][participant_col_name] == '\n':
                pass
            else:
                # which image to process
                cur_image_name = line[1][image_name_col][:line[1][image_name_col].find('.')]
                if cur_image_name + '.jpg' in wang_images_names:  # take only wang images
                    fix_x = int(int(float(line[1][fix_x_col_name])) / resolution_divider_x)
                    fix_y = int(int(float(line[1][fix_y_col_name])) / resolution_divider_y)
                    # check if fixation and right coordinates
                    if fix_x < 0 or fix_x >= image_size[1] or \
                            fix_y < 0 or fix_y >= image_size[0]:
                        # print line[1]['Participant'], line[1]['Event Start Trial Time [ms]'], \
                        #    line[1]['Fixation Position X [px]'], line[1]['Fixation Position Y [px]']
                        dict_features[feature].append(-1)
                    else:
                        # check if the fixation inside the areas of the current feature
                        if binary_or_value == 'value':
                            dict_features[feature].append(dict_images[cur_image_name][fix_y, fix_x])
                        else:
                            if dict_images[cur_image_name][fix_y, fix_x] >= min_value_as_1:
                                dict_features[feature].append(1)
                            else:
                                dict_features[feature].append(0)
                else:
                    dict_features[feature].append(-1)

    # updating the dataframe
    for feature in wanted_features:
        cur_file[feature] = dict_features[feature]

    print "Saving the output file"
    cur_file.to_csv(input_file + "_with_features.csv")
    tmp_data = file(input_file + "_with_features.csv").read().replace('\r', '')
    file(input_file + "_with_features.csv", 'w').write(tmp_data)
