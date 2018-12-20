# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 10:03:26
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$
import sys
import os
import arcpy
from arcpy import env


def point_to_sqr_point(single_point_shp, buffer_distence, four_point_square):
    distance = str(buffer_distence) + " Meter"
    circle_buffer = arcpy.CreateScratchName(
        "temp", data_type="Shapefile", workspace=arcpy.env.workspace)
    square_buffer = arcpy.CreateScratchName(
        "temp112", data_type="Shapefile", workspace=arcpy.env.workspace)
    arcpy.Buffer_analysis(single_point_shp, circle_buffer,
                          distance, "FULL", "ROUND", "NONE")
    print('circle buffer is finished！')
    arcpy.FeatureEnvelopeToPolygon_management(circle_buffer, square_buffer)
    print('square buffer is finished!')
    arcpy.FeatureVerticesToPoints_management(
        square_buffer, four_point_square, "ALL")
    print("square smashed")


def get_coordinate(input_features, image_degree='15-17', downloadfile='download_file.txt'):
    cur_list = []
    for row in arcpy.da.SearchCursor(input_features, ['id', 'Shape']):
        last_id = row[0]
        break
    i = 1
    err = 0
    with open('%s%03d%s' % (os.path.splitext(downloadfile)[0], i / 200 + 1, os.path.splitext(downloadfile)[1]), 'w') as fn:
        with open(r'D:\NGCC\airport\arcgis_script_workspace\err_id.txt', 'w') as fn_err:
            for row in arcpy.da.SearchCursor(input_features, ['id', 'Shape']):
                cur_id = row[0]
                if cur_id != last_id:
                    x_corr = []
                    y_corr = []
                    for corr in cur_list:
                        x_corr.append(corr[1][0])
                        y_corr.append(corr[1][1])
                    if len(x_corr) != 5:
                        fn_err.write('%s,%d\n' % (last_id, len(x_corr)))
                        err += 0
                    if not i % 200:
                        fn.close()
                        fn = open('%s%03d%s' % (os.path.splitext(downloadfile)[
                                  0], i // 200 + 1, os.path.splitext(downloadfile)[1]), 'w')
                    fn.write('%d|%s,%s|%s,%s|%s\n' % (last_id, min(x_corr), min(
                        y_corr), max(x_corr), max(y_corr), image_degree))
                    # print('%s|%f,%f|%s,%s|%s' % (last_id, min(x_corr), min(
                    #     y_corr), max(x_corr), max(y_corr), image_degree))
                    i += 1
                    del cur_list[:len(x_corr)]
                    del x_corr, y_corr
                    last_id = cur_id
                # print(cur_id, row)
                cur_list.append(row)
            if err == 0:
                fn_err.write('err_num:0')
            print('err:%d,correct_point:%d' % (err, i))


def coordinate_list(input_features, downloadfile='download_file.txt'):
    i = 0
    with open('%s%03d%s' % (os.path.splitext(downloadfile)[0], i / 200 + 1, os.path.splitext(downloadfile)[1]), 'w') as fn:
        for row in arcpy.da.SearchCursor(input_features, ['id', 'Shape']):
            i += 1
            fn.write(str(row[1][0]) + ',' + str(row[1][1])+'\n')
        fn.close()
    print(i)


def main():
    print('main process')
    arcpy.env.workspace = r"D:\NGCC\airport\arcgis_script_workspace"
    buffer_distence = 1600
    single_point_shp = r"D:\NGCC\airport\medium_and_big_airport.shp"
    four_point_square = "four_point_square.shp"
    # point_to_sqr_point(single_point_shp, buffer_distence, four_point_square)
    # get_coordinate(r"D:\NGCC\airport\arcgis_script_workspace\four_point_square.shp", '15-17',
    #                r'D:\NGCC\airport\arcgis_script_workspace\download_file.txt')
    coordinate_list(r"D:\NGCC\airport\medium_and_big_airport.shp",
                    r'D:\NGCC\airport\img\download_file0916.txt')


if __name__ == '__main__':
    main()
