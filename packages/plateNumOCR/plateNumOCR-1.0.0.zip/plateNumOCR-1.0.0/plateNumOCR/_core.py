import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import tools.infer.utility as utility
from tools.infer.predict_system import main


def demo(image_path):
    args = utility.parse_args(os.path.dirname(os.path.realpath(__file__)))
    args.image_dir = image_path
    main(args)
'''

def demo():
    args = utility.parse_args()
    #args.image_dir = 'D:/Studying_Data/project/plateNum_recognition/1.jpg'
    main(args)
'''

'''if __name__ == '__main__':
    #demo(sys.argv[1])
    demo(r'C:/Users/12138/Desktop/sample/1.jpg')'''