# Training custom model with Tensorflow and Google Colab Pro

Smart Traffic custom model was trained with TensorFlow and TensorFlow object detection API on Google Colab Pro. The steps on how to train custom model is based on [techzizou's tutorial](https://medium.com/geekculture/training-a-model-for-custom-object-detection-using-tensorflow-1-x-on-google-colab-564d3e62e9ef). However, some codes have been adjusted and it is best to follow [trainmodel.ipynb](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Custom_model/trainmodel.ipynb).

## Detailed steps on how to train custom model

1. Download and prepare the following files:
  i. Images for data training in .jpg format. (For Smart Traffic, the total images used for training is 310 .jpg files). It is advised that there are 300+ images for better data training. Store all the images in *images* folder.
  ii. Label all the images with [Label Img](https://github.com/tzutalin/labelImg). Save the labeled images as .xml files and store them in *annotations* folder.
  * Refer to [Image dataset labeling](https://techzizou.com/dataset-labeling-annotation-tutorial-for-beginners/) for more information.
  iii. Download TensorFlow object detection API model from here. Smart Traffic uses ssd_mobilenet_v2_coco_2018_03_29 model because it is suitable to be run on raspberry pi.

2. Create the folder and the following directory on Google Drive.

3. Zip the image and annotation folders and put them to customTF1 folder.

4. Download [generate_TF1record.py](https://github.com/techzizou/Train-Object-Detection-Model-TF-1.x/blob/main/generate_tfrecord.py) and put it to customTF1 folder. The current directory should look like:
![directory step 4]()
