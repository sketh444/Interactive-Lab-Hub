# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***

<img width="478" alt="Screen Shot 2021-11-02 at 8 26 42 PM" src="https://user-images.githubusercontent.com/73661058/139969662-fdffef1f-2050-4b16-8e99-7ae6a6672b6b.png">
- object detection: could be used in detecting if someone has a full equipment set ready before starting some DIY projects/cooking/any project that require a set of objects ready.

<img width="566" alt="Screen Shot 2021-11-02 at 8 21 57 PM" src="https://user-images.githubusercontent.com/73661058/139969610-a367d8ea-dd01-468e-bc39-4d2b6c46fa41.png">
- Face recognition: could be used in detecting whether someone is wearing a mask or not when entering an indoor space during pandemic.

<img width="591" alt="Screen Shot 2021-11-02 at 8 24 31 PM" src="https://user-images.githubusercontent.com/73661058/139969621-a1c16e11-f278-40e8-b9d6-3f38b5972630.png">
- flow detection: could be used in studying the workflow of physicians during treatments/surgery and improving the environment/interior accordingly.

<img width="525" alt="Screen Shot 2021-11-02 at 8 19 49 PM" src="https://user-images.githubusercontent.com/73661058/139969645-8e722210-4092-4097-8adb-cd0fae17209b.png">
- contour detection: could be used in detecting shapes of organs and automating the annotation on top of a medical image. Or it could be used in detecting a logo and shape of a car and tell the maker and model of a car.

#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

<img width="583" alt="Screen Shot 2021-11-02 at 8 37 47 PM" src="https://user-images.githubusercontent.com/73661058/139970258-0fcbfabe-b42b-48ce-9ce3-c81a703f9a2d.png">

<img width="608" alt="Screen Shot 2021-11-02 at 8 37 16 PM" src="https://user-images.githubusercontent.com/73661058/139970262-da5ff4f5-ce9a-4565-9372-9adffbd4155f.png">


**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***

It could be used as detecting a hand sign to signal the level of pain during a dentist visit. haha Usually they tell me to raise my left arm since I cannot speak while they're working on my mouth but it can only have binary extreme senario- YES pain and NO pain. Usually it's somewhere in between. Using the relative finger positions used in this system, we could detect four different levels of pain expressed by connecting one of the fingers to the thumb.

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)


#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```

<img width="929" alt="Screen Shot 2021-11-02 at 1 23 36 AM" src="https://user-images.githubusercontent.com/42717070/139794388-c37554e2-cd57-44a9-8feb-3058617f7ac9.png">
<img width="1085" alt="Screen Shot 2021-11-02 at 1 33 08 AM" src="https://user-images.githubusercontent.com/42717070/139794390-2eba20e7-2dc5-4042-af84-efcea5c1a8bf.png">
I was not sure if the detection from teachable model was performing well from the given code, as it was detecting my cup, phone, and hand all as 'mask'. However, it did perform very well when I trained my own images. I trained four classes: me holding a blue piece of paper, red piece of paer, empty background, and me holding nothing(face).

(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***


*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

For this lab we will be creating an interactive Morpheus (from the Matrix) device that dispenses red or blue pills (Candy) based on the users choice. We will specifically be re-creating the scene below and using exact audio from the scene in our device. 

https://user-images.githubusercontent.com/73661058/139364599-9e9ed69a-d9c1-4b22-b7e4-0f0195026e1e.mov

Our device will be made up of a 3D printed Morpheus and cardboard box behind him to store the Pi, camera, motors, and pill dispensors. 
The way the interaction will work is when the device is turned on Morpheus will start speaking "This is your last chance, after this there is no turning back. You take the blue pill the story ends and you wake up in your bed and belive whatever you want to belive. You take the red pill you stay in wonderland and I show you how deep the rabit hole goes". This will promt the user to choose either a red or blue pill from Morpheus's hands. As the user picks up the pill from Morpheus's hands a camera in the back the box behind Morpheus will detect whether the pill selected is blue or red using a model we trained using trainable machines. Based on the users selection a candy pill will be despensed through a slide at the bottom of the device. 

Device design: 

Front- 

<img width="548" alt="Screen Shot 2021-10-28 at 11 11 44 PM" src="https://user-images.githubusercontent.com/73661058/139367522-cb5e20a9-a646-44f4-a2f1-1fe3dc160553.png">

Back/inside-

<img width="503" alt="Screen Shot 2021-10-28 at 10 54 17 PM" src="https://user-images.githubusercontent.com/73661058/139366050-552c59a1-0333-4ab1-a440-c647f09ece42.png">

Other experimentation and ideation: 

<img width="463" alt="Screen Shot 2021-10-28 at 11 15 58 PM" src="https://user-images.githubusercontent.com/73661058/139369663-5a6a0543-1146-4472-a3a8-3a94be87e219.png">

<img width="358" alt="Screen Shot 2021-10-28 at 11 15 51 PM" src="https://user-images.githubusercontent.com/73661058/139369888-7d28ded7-385b-4cfe-833e-529e33938e1e.png">

<img width="580" alt="Screen Shot 2021-10-28 at 11 15 38 PM" src="https://user-images.githubusercontent.com/73661058/139369962-c65a8d46-16ed-4412-85cc-0f68cc254c6b.png">

<img width="637" alt="Screen Shot 2021-10-28 at 11 14 42 PM" src="https://user-images.githubusercontent.com/73661058/139370000-4af3b001-422a-4539-ad11-1621b2718cc8.png">

<img width="871" alt="Screen Shot 2021-10-28 at 11 15 22 PM" src="https://user-images.githubusercontent.com/73661058/139369981-0ad65d32-f152-47de-966a-f07a1d36f2d2.png">


### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
1. How bad would they be impacted by a miss classification?
1. How could change your interactive system to address this?
1. Are there optimizations you can try to do on your sense-making algorithm.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
Are device can be used for a fun and interactive way to eat red and blue candy. 
* What is a good environment for X?
A good environment would be in a Matrix enthusiasts home, perhaps on their desk or coffee table. Ideally when the interaction takes place the backround will be clear so Morpheus camera can clearly see the red or blue pill.  
* What is a bad environment for X?
A Bad environment would be somewhere crowded where the device can not clearly pick up on the detection of the red or blue pill which is essental for the interaction to work correctly. Another bad environmemt would be in ther presents on a non Matrix enthusiasts or Matrix hater. 
* When will X break?
The device will break any of its parts stoped working, the camera, the Pi, or the motors. The device would also break if it was phsyically destroyed, Morpheus was smashed or disasembled from his box set up. Anther way the device could break is if the red and blue pills where taken from Morpheus hands, the user would not know what to do or how to interact with the device. Lastly the device would break if the candy it dispenses runs out. 
* When it breaks how will X break?
* What are other properties/behaviors of X?
The device reenacts a classic sense from the Matrix through audio and user interaction. The device has computer vision and detect red and blue pills. The device can make dispensing decsions based on the sight of red or blue pills. The device dispenses red and blue candy. The devive allows for appreciation of the Matrix. 
* How does X feel?
The devices like a plastic 3D model and cardboard. It also feels like delious candy in the users mouth. 

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
