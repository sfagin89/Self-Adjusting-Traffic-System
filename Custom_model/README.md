# Training custom model with Tensorflow and Google Colab Pro

Smart Traffic custom model was trained with TensorFlow and TensorFlow object detection API on Google Colab Pro. The steps on how to train custom model is based on [techzizou's tutorial](https://medium.com/geekculture/training-a-model-for-custom-object-detection-using-tensorflow-1-x-on-google-colab-564d3e62e9ef) and the codes are from there (credits to techzizou). However, some codes have been slightly modified and it is best to follow [trainmodel.ipynb](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Custom_model/trainmodel.ipynb). The trainmodel.ipynb notebook contains detailed steps on how to run and train custom model. The detailed steps written below are the same as what is written on the notebook.

The custom model is created via TensorFlow. In order for the model to run efficiently on Raspberry Pi, the custom model needs to be converted to TensorFlow Lite model. Follow the steps [here](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi) (credits to EdjeElectronics for the guide) to convert TensorFlow to TensorFlow Lite object detection model. Note that there are some slight modification to the set up. Things to note are:
* Smart Traffic custom model was trained with ssd_mobilenet_v2_coco model and uses TensorFlow 1.15.
* bazel version for TensorFlow 1.15 is 0.24.1
* bazel 0.24.1 is compatible with Microsoft Visual Studio 2017 (including its build tools)
* If encounter ModuleNotFoundError: No module named 'cv2', make sure to
```
pip install opencv-python
```

Smart Traffic's custom TensorFlow Lite model is provided on [TFLite_model](https://github.com/sfagin89/Self-Adjusting-Traffic-System/tree/main/Custom_model/TFLite_model).

## Detailed steps on how to train custom model

**Colab Setup**
* Open Colab notebook on a browser
* Change Colab's runtime type to GPU:
> Runtime -> Change runtime type -> Hardware accelerator -> GPU

1. Download and prepare the following files:
    1. Images for data training in .jpg format. (For Smart Traffic, the total images used for training is 310 .jpg files). It is advised that there are 300+ images for better data training. Store all the images in *images* folder.
    2.  Label all the images with [Label Img](https://github.com/tzutalin/labelImg). Save the labeled images as .xml files and store them in *annotations* folder.
      * Refer to [Image dataset labeling](https://techzizou.com/dataset-labeling-annotation-tutorial-for-beginners/) for more information.

2. Install tensorflow 1.x
```python
!pip install tensorflow==1.15
```
```python
import tensorflow as tf
print(tf.__version__)
```
3. Import dependencies
```
import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd
```
4. Create a folder called 'customTF1' and the following directory on Google Drive:

```
/customTF1
├── data
└── training
```

5. Arrange files in the directory**
    1. Zip the *image folder* and *annotation folder* created on step 1 and put them to customTF1 folder.
    2. Download [generate_TF1record.py](https://github.com/techzizou/Train-Object-Detection-Model-TF-1.x/blob/main/generate_tfrecord.py) and put it to customTF1 folder. The current directory should look like:

```
/customTF1
├── annotations.zip
├── data
├── generate_tfrecord.py
├── images.zip
└── training
```
*Note: Credits to [techzizou](https://medium.com/geekculture/training-a-model-for-custom-object-detection-using-tensorflow-1-x-on-google-colab-564d3e62e9ef) for the generate_TFrecord.py file!*

6. Mount Google Drive to Google colab

```python
#mount drive
from google.colab import drive
drive.mount('/content/gdrive')
```

7. Clone the TensorFlow models git repository & Install TensorFlow Object Detection API
```python
# clone the tensorflow models on the colab cloud vm
!git clone --q https://github.com/tensorflow/models.git

#navigate to /models/research folder to compile protos
%cd models/research

# Compile protos.
!protoc object_detection/protos/*.proto --python_out=.

# Install TensorFlow Object Detection API.
!cp object_detection/packages/tf1/setup.py .  
!python -m pip install .
```

8. Test the model builder
```python
# testing the model builder
!python object_detection/builders/model_builder_tf1_test.py
```

9. Navigate to /gdrive/My Drive/customTF1/data/ and unzip the images.zip and annotations.zip files into the data folder
```python
%cd '/content/gdrive/My Drive/customTF1/data/'

# unzip the datasets and their contents so that they are now in /mydrive/customTF1/data/ folder
!unzip '/content/gdrive/My Drive/customTF1/images.zip' -d .
!unzip '/content/gdrive/My Drive/customTF1/annotations.zip' -d .
```

10. Create test_labels & train_labels
* Make sure you are in '/customTF1/data/' directory
* If the code below does not work, manually move 20% of .xml files from *annotation folder* to the *test_labels folder* and the rest of the .xml file to *train_labels* folder
```python
#creating two dir for training and testing
!mkdir test_labels train_labels

# lists the files inside 'annotations' in a random order (not really random, by their hash value instead)
# Moves the first 20% of the labels (62/310) to the testing dir: `test_labels`
!ls annotations/* | sort -R | head -62 | xargs -I{} mv {} test_labels/


# Moves the rest of the labels ( 248 labels ) to the training dir: `train_labels`
!ls annotations/* | xargs -I{} mv {} train_labels/
```
*Current directory should look like:*
```
/customTF1
├── annotations.zip
├── data
│   ├── annotations
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 35\ PM.xml
│   │   └── ......
│   ├── images
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 29\ PM.jpg
│   │   └── ......
│   ├── test_labels
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 35\ PM.xml
│   │   └── ......
│   └── train_labels
│       ├── Photo\ Nov\ 19,\ 1\ 55\ 29\ PM.xml
│       └── .......
├── generate_tfrecord.py
├── images.zip
└── training
```

11. Create the CSV files and the "label_map.pbtxt" file**
* Make sure you are in '/customTF1/data/' directory
* The script below generates **test_labels.csv**, **train_labels.csv**, and the **label_map.pbtxt** file using the classes mentioned in the XML files
```python
#adjusted from: https://github.com/datitran/raccoon_dataset
def xml_to_csv(path):
  classes_names = []
  xml_list = []

  for xml_file in glob.glob(path + '/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
      classes_names.append(member[0].text)
      value = (root.find('filename').text  ,       
               int(root.find('size')[0].text),
               int(root.find('size')[1].text),
               member[0].text,
               int(member[4][0].text),
               int(member[4][1].text),
               int(member[4][2].text),
               int(member[4][3].text))
      xml_list.append(value)
  column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
  xml_df = pd.DataFrame(xml_list, columns=column_name)
  classes_names = list(set(classes_names))
  classes_names.sort()
  return xml_df, classes_names

for label_path in ['train_labels', 'test_labels']:
  image_path = os.path.join(os.getcwd(), label_path)
  xml_df, classes = xml_to_csv(label_path)
  xml_df.to_csv(f'{label_path}.csv', index=None)
  print(f'Successfully converted {label_path} xml to csv.')

label_map_path = os.path.join("label_map.pbtxt")
pbtxt_content = ""

for i, class_name in enumerate(classes):
    pbtxt_content = (
        pbtxt_content
        + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)
    )
pbtxt_content = pbtxt_content.strip()
with open(label_map_path, "w") as f:
    f.write(pbtxt_content)
    print('Successfully created label_map.pbtxt ')
```

*Current directory should look like:*
```
/customTF1
├── annotations.zip
├── data
│   ├── annotations
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 35\ PM.xml
│   │   └── ......
│   ├── images
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 29\ PM.jpg
│   │   └── ......
│   ├── test_labels
│   │   ├── Photo\ Nov\ 19,\ 1\ 55\ 35\ PM.xml
│   │   └── ......
│   ├── train_labels
│   |   ├── Photo\ Nov\ 19,\ 1\ 55\ 29\ PM.xml
│   |   └── .......
│   ├── label_map.pbtxt
│   ├── test_labels.csv
│   └── train_labels.csv
├── generate_tfrecord.py
├── images.zip
└── training
```
12. Create **train.record** & **test.record** files
```python
%cd '/content/gdrive/My Drive/customTF1/data/'
```

```python
#Usage:  

#FOR train.record
!python '/content/gdrive/My Drive/customTF1/generate_tfrecord.py' train_labels.csv  label_map.pbtxt images/ train.record

#FOR test.record
!python '/content/gdrive/My Drive/customTF1/generate_tfrecord.py' test_labels.csv  label_map.pbtxt images/ test.record
```

13. Download pre-trained model checkpoint
* Make sure you are in '/customTF1/data/' directory
* Smart Traffic uses **ssd_mobilenet_v2_coco** model because the main system will run on raspberry pi. Check out the following [blog](https://serokell.io/blog/how-to-choose-ml-technique) to understand how to select a model suitable for different type of data and requirements.
* Download pre-trained model detection checkpoints for TensorFlow 1.x from [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md). For Smart Traffic, **ssd_mobilenet_v2_coco** was downloaded. Make sure to change the directory according to the model you selected.

```python
#Download the pre-trained model ssd_mobilenet_v2_coco_2018_03_29.tar.gz into the data folder & unzip it.

!wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
!tar -xzvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

14. Obtain the model pipeline config file, make changes, and put it inside the customTF1 data folder
* Edit the config file from '/content/models/research/object_detection/samples/configs/' in Colab and copy the edited config file to the '/content/gdrive/My Drive/customTF1/data/' folder
* Make the following changes to the config file:
    * **num_classes** to the number of your classes.
    * **test.record** path, **train.record** path & **label_map** path to the paths where these files are located
    * **fine_tune_checkpoint** to the path where the downloaded checkpoint from step 13 is.
    * **fine_tune_checkpoint_type** to 'detection'
    * **batch_size** to any multiple of 8 depending upon the capability of your GPU (Max batch size= available GPU memory bytes / 4 / (size of tensors + trainable parameters).
    * **num_steps** to the number of steps you want the detector to train.

```python
#copy the confif file to the data folder
!cp /content/models/research/object_detection/samples/configs/ssd_mobilenet_v2_coco.config  /content/gdrive/My Drive/customTF1/data/
```

15. Load Tensorboard
```python
#load tensorboard
%load_ext tensorboard
%tensorboard --logdir '/content/gdrive/MyDrive/customTF1/training'
```

16. Train the model
* For **ssd_mobilenet_v2_coco**, train until loss drops constantly below 2 or 1 for better result
* If loss explodes occur, adjust the learning_rate inside the config file. For more information on the topic, [read here](https://parthlathiya.medium.com/loss-explosion-while-training-a-custom-model-ad15fbc00d1)

```python
#change directory to object_detection
%cd '/content/models/research/object_detection'
```
```python
!python model_main.py --pipeline_config_path='/content/gdrive/My Drive/customTF1/data/ssd_mobilenet_v2_coco.config' --model_dir='/content/gdrive/My Drive/customTF1/training' --alsologtostderr
```

17. Export Inference graph
```python
#navigate to object_detection folder
%cd '/content/models/research/object_detection'
```
```python
!python export_inference_graph.py --input_type image_tensor --pipeline_config_path '/content/gdrive/MyDrive/customTF1/data/ssd_mobilenet_v2_coco.config' --trained_checkpoint_prefix '/content/gdrive/MyDrive/customTF1/training/model.ckpt-14082' --output_directory '/content/gdrive/MyDrive/customTF1/data/inference_graph'
```
