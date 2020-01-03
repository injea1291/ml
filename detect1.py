import argparse
import time
import sys
from sys import platform
sys.path.append("C:\\Users\\kay\\PycharmProjects\\untitled1\\yolov3-master")
from models import *
from utils.datasets import *
from utils.utils import *

def detect(cfg,
           data,
           weights,
           images='data/samples',  # input folder
           img_size=416,
           conf_thres=0.5,
           nms_thres=0.5):
    # Initialize
    xyli, labli = [], []
    device = torch_utils.select_device()
    torch.backends.cudnn.benchmark = False  # set False for reproducible results

    # Initialize model
    if ONNX_EXPORT:
        s = (320, 192)  # (320, 192) or (416, 256) or (608, 352) onnx model image size (height, width)
        model = Darknet(cfg, s)
    else:
        model = Darknet(cfg, img_size)

    # Load weights
    if weights.endswith('.pt'):  # pytorch format
        model.load_state_dict(torch.load(weights, map_location=device)['model'])
    else:  # darknet format
        _ = load_darknet_weights(model, weights)

    # Fuse Conv2d + BatchNorm2d layers
    # model.fuse()

    # Eval mode
    model.to(device).eval()

    # Export mode
    if ONNX_EXPORT:
        img = torch.zeros((1, 3, s[0], s[1]))
        torch.onnx.export(model, img, 'weights/export.onnx', verbose=True)
        return

    # Half precision
    opt.half = opt.half and device.type != 'cpu'  # half precision only supported on cuda
    if opt.half:
        model.half()

    # Set Dataloader
    if opt.webcam:
        save_images = False
        dataloader = LoadWebcam(img_size=img_size, half=opt.half)
    else:
        dataloader = LoadImages(images, img_size=img_size, half=opt.half)

    # Get classes and colors
    classes = load_classes(parse_data_cfg(data)['names'])

    # Run inference
    for i, (path, img, im0, vid_cap) in enumerate(dataloader):
        t = time.time()
        # Get detections
        img = torch.from_numpy(img).unsqueeze(0).to(device)
        pred, _ = model(img)
        det = non_max_suppression(pred.float(), conf_thres, nms_thres)[0]

        if det is not None and len(det) > 0:
            # Rescale boxes from 416 to true image size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()


            for *xyxy, conf, cls_conf, cls in det:

                label = '%s %.2f' % (classes[int(cls)], conf)
                xyxy[0:4] = list(map(lambda a: int(a) * 4, xyxy[0:4]))
                xyli.append([label, xyxy[0], xyxy[1], xyxy[2], xyxy[3]])
            xyli.sort(key=lambda xyli: xyli[1])
            for iasd in xyli:
                labli.append(iasd[0])

        print('Done. (%.3fs)' % (time.time() - t))
    return labli

def asd():
    global opt
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='C:/Users/kay/PycharmProjects/untitled1/yolov3-master/cfg/yolov3-spparow.cfg', help='cfg file path')
    parser.add_argument('--data', type=str, default='C:/Users/kay/PycharmProjects/untitled1/yolov3-master/data/arow.data', help='coco.data file path')
    parser.add_argument('--weights', type=str, default='C:/Users/kay/PycharmProjects/untitled1/rune.pt', help='path to weights file')
    parser.add_argument('--images', type=str, default='C:\\Users\\kay\\PycharmProjects\\untitled1\\tmp',
                        help='path to images')
    parser.add_argument('--img-size', type=int, default=608, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
    parser.add_argument('--nms-thres', type=float, default=0.3, help='iou threshold for non-maximum suppression')
    parser.add_argument('--half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('--webcam', action='store_true', help='use webcam')
    opt = parser.parse_args()

    with torch.no_grad():
        labli1 = detect(opt.cfg,
               opt.data,
               opt.weights,
               images=opt.images,
               img_size=opt.img_size,
               conf_thres=opt.conf_thres,
               nms_thres=opt.nms_thres)

    return labli1