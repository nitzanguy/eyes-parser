# in order to active the script you need to define the arguments with capital letters.
# than run the script

import pandas as pd
from glob import glob
import os
from add_semantic_labels import label_semantic_according_to_feature_maps as ls

# input file path - csv contains the fixation report \ fixation only
INPUT_FILE = r'C:\Users\guyni\Google Drive\SemanticFreeView\ver2018_adi\Analysis\180902\test.csv'
cur_file = pd.read_csv(INPUT_FILE)

# dir of the maps - the directory contains the feature maps
MAPS_DIR = r'C:\Users\guyni\PycharmProjects\LabProjects\AnalysisTools\semantic_wang_python\feature_maps'

# size of the images in the directory
IMAGE_SIZE = (150, 200)

# dir of the original images
IMAGES_DIR = r'C:\Users\guyni\PycharmProjects\LabProjects\AnalysisTools\semantic_wang_python\images'
wang_images_names = [os.path.basename(f) for f in glob(IMAGES_DIR + '\*')]

# which feature to add to fixation report
WANTED_FEATURES = ['face', 'emotion', 'gazed', 'motion', 'operability', 'smell', 'sound', 'taste', 'text', 'touch',
                   'touched', 'watchability']
LOW_LEVEL_FEATURES = ['color', 'complexity', 'convexity', 'eccentricity', 'intensity', 'orientation', 'size',
                      'solidity']
WANTED_FEATURES = WANTED_FEATURES + LOW_LEVEL_FEATURES

# the size of the screen as appeared in the experiment
PRESENTATION_SIZE = (600, 800)  # y than x, for the resizing of the images
resolution_divider_y = PRESENTATION_SIZE[0] * 1.0 / IMAGE_SIZE[0]
resolution_divider_x = PRESENTATION_SIZE[1] * 1.0 / IMAGE_SIZE[1]

# if value is chosen the script will add the raw score, if binary is chosen it will insert 1 or 0 according to limit - value/binary
BINARY_OR_VALUE = 'value'
MIN_VALUE_AS_1 = 64  # from wang experiment

# Eyelink info
# PARTICIPANT_COL_NAME = 'RECORDING_SESSION_LABEL'
# FIX_X_COL_NAME = 'CURRENT_FIX_X'
# FIX_Y_COL_NAME = 'CURRENT_FIX_Y'
# IMAGE_COL_NAME = 'image'

# SMI info
PARTICIPANT_COL_NAME = 'Participant'
FIX_X_COL_NAME = 'Fixation Position X [px]'
FIX_Y_COL_NAME = 'Fixation Position Y [px]'
IMAGE_COL_NAME = 'Stimulus'

# run the script
ls.add_semantic_labels(cur_file, INPUT_FILE, MAPS_DIR, WANTED_FEATURES, wang_images_names,
                       PARTICIPANT_COL_NAME, IMAGE_COL_NAME,
                       BINARY_OR_VALUE, MIN_VALUE_AS_1,
                       FIX_X_COL_NAME, FIX_Y_COL_NAME, resolution_divider_x, resolution_divider_y, IMAGE_SIZE)
