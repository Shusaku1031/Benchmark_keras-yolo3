import sys,os
import argparse
import tensorflow as tf
import keras.backend as K
from timeit import default_timer as timer
from yolo import YOLO, detect_video
from PIL import Image

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        if img == "q":
            break
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            result_list = []
            for i in range(101):
                start = timer()
                r_image = yolo.detect_image(image)
                end = timer()
                calc_time = end - start
                print(i,end-start)
                if i != 0:
                    result = '{},{}'.format(str(i),str(calc_time))
                    result_list.append(result)
                #print(r_image["info"])
                if i == 0:
                    r_image["image"].show()
            with open(os.path.join('/home','shusaku','image_result.txt'),'w') as f:
                for rl in result_list:
                    f.write(rl+'\n')

    yolo.close_session()

FLAGS = None

if __name__ == '__main__':


    """print("Configuration...")
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.66
    sess = tf.Session(config=config)
    K.set_session(sess)"""

    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    parser.add_argument(
        "--frame_path", nargs='?', type=str, default="",
        help = "Frame save path"
    )

    parser.add_argument(
        '--round_num', type=int,
        help='Number of detection round '
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        print(FLAGS.round_num)
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output, FLAGS.frame_path, FLAGS.round_num)
        print('END')
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
