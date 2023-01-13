import cv2
import os


class Main:
    def __init__(self):
        image_path = 'M:/labelme/hooo'
        file_list = [_ for _ in os.listdir(image_path) if _.endswith(r"json")]
        print('總共有 : %s 個文件' %len(file_list))
        temp = 0
        for file_name in os.listdir(image_path):
            if file_name.split('.')[1] == 'png':
                image = cv2.imread(os.path.join(image_path, file_name))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)

                ret, thrash = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                data = ''
                write_flag = False
                for contour in contours:
                    approx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
                    point_list = [None, None, None, None]
                    for point in approx:
                        x, y = point[0][0], point[0][1]
                        if point_list[0] is None:
                            point_list[0] = x
                            point_list[1] = y
                            point_list[2] = x
                            point_list[3] = y
                        else:
                            if point_list[0] > x:
                                point_list[0] = x
                            if point_list[1] > y:
                                point_list[1] = y

                            if point_list[2] < x:
                                point_list[2] = x
                            if point_list[3] < y:
                                point_list[3] = y

                    size = (point_list[2] - point_list[0]) * (point_list[3] - point_list[1])
                    image_roi = thrash[point_list[1]:point_list[3], point_list[0]:point_list[2]]
                    scale = 0
                    for so_row in range(len(image_roi)):
                        for so_column in range(len(image_roi[0])):
                            if image_roi[so_row][so_column] == 255:
                                scale += 1
                            else:
                                scale -= 1
                    if size > 150:
                        write_flag = True
                        point_data = []
                        for point in approx:
                            x, y = point[0][0], point[0][1]
                            point_data.append([x, y])
                        if scale > 0:
                            label = 'True'
                            cv2.drawContours(image, [approx], 0, (0, 200, 0), 3)
                        else:
                            label = 'False'
                            cv2.drawContours(image, [approx], 0, (0, 0, 200), 3)
                        data += self.Formula(label, point_data)

                if write_flag:
                    with open(os.path.join(image_path, file_name.replace('png', 'json'))) as f:
                        self.Content = f.read()

                    start_index = self.Content.find('shapes') + 10
                    end_index = self.Content.find('imagePath') - 8

                    pre_content = self.Content[:start_index]
                    end_content = self.Content[end_index:]

                    with open(os.path.join(image_path, file_name.replace('png', 'json')), 'w') as fw:
                        fw.write(pre_content + data[:-2] + end_content)
                temp += 1
                print('\r' + '執行進度:[%s%s]%.2f%%' % (
                    '*' * int(temp * 20 / len(file_list)), ' ' * (20 - int(temp * 20 / len(file_list))),
                    float(temp / len(file_list) * 100)), end='')
                print('\t Processing', file_name, end='...OK\n')

    def Formula(self, label, points):
        form = '{\n' \
               ' "label": "' + label + '",\n' \
                                       ' "points": ['
        for pon in points:
            form += '\n\t[\n\t ' + str(pon[0]) + ',\n\t ' + str(pon[1]) + '\n\t],'
        form = form[:-1]
        form += '\n ],\n' \
                ' "group_id": null,\n' \
                ' "shape_type": "polygon",\n' \
                ' "flags": {}\n' \
                '},\n'

        return form


Main()
