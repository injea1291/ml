# ml
Requirements dll file

CUDA DLL
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin

OPENCV DLL
opencv\build\x64\vc15\bin
  opencv_world430.dll
  opencv_world430d.dll
  
DARKNET DLL
https://github.com/AlexeyAB/darknet/tree/master/3rdparty/pthreads/bin

-show_imgs

darknet detector train data/lie.data cfg/yolov4-2cls.cfg weights/yolov4.conv.137

darknet detector train data/arrow.data cfg/yolov4-4cls.cfg weights/yolov4.conv.137

darknet detector train data/sum.data cfg/yolov4-6cls.cfg weights/yolov4.conv.137

darknet detector train data/sum.data cfg/yolov4-6cls.cfg backup/yolov4-6cls_last.weights

darknet detector train data/oldarrow.data cfg/yolov4-4cls.cfg weights/yolov4.conv.137

darknet.exe detector test data/arrow.data cfg/yolov44.cfg backup/yolov4-4cls_last.weights images/result/10.jpg

darknet.exe detector test data/arrow.data C:\Users\kay\PycharmProjects\teste/cfg/yolov44.cfg backup/yolov4-4cls_1000.weights C:\Users\kay\PycharmProjects\teste/images/arrow/10.png

git rm -cached [filename]
