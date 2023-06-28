import numpy as np
import collections

def getColorList():
    dict = collections.defaultdict(list)

    # red
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])
    color_list_red = []
    color_list_red.append(lower_red)
    color_list_red.append(upper_red)
    dict['red'] = color_list_red




    # blue
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])
    color_list_blue = []
    color_list_blue.append(lower_blue)
    color_list_blue.append(upper_blue)
    dict['blue'] = color_list_blue


    return dict

if __name__ == '__main__':
    color_dict = getColorList()
    print(color_dict)

    num = len(color_dict)
    print('num=', num)

    for d in color_dict:
        print('key=', d)
        print('value=', color_dict[d][1])