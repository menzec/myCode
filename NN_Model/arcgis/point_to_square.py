# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 10:03:26
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$
import sys
import os
import arcpy
import pdb
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


def coordinate_list(input_features, attrs=None, downloadfile='download_file_.txt'):
    count = 0
    # ['id', 'SHAPE@XY']
    if attrs:
        class_attrs = list(attrs)
        class_attrs.append('SHAPE@XY')
    else:
        class_attrs = ['SHAPE@XY']
    # print(class_attrs)
    data = arcpy.da.SearchCursor(
        input_features, class_attrs)
    classinfo = {}
    for row in data:
        count += 1
        if attrs:
            classname = '_'.join(row[:len(attrs)])
        else:
            classname = 'ALL'
        if classname in classinfo.keys():
            classinfo[classname][0] += 1
            classinfo[classname][1].append(row[-1])
            if count % 5000 == 0:
                for classname in classinfo.keys():
                    with open('%s%s%s' % (downloadfile[:-4], str(classname), '.txt'), 'a') as fn:
                        # pdb.set_trace()
                        for i in range(len(classinfo[classname][1])):
                            coordinate = classinfo[classname][1].pop(0)
                            fn.write(
                                str(coordinate[0]) + ',' + str(coordinate[1]) + '\n')
        else:
            classinfo[classname] = [1, [row[-1]]]
    for classname in classinfo.keys():
        # pdb.set_trace()
        with open('%s%s%s' % (downloadfile[:-4], str(classname), downloadfile[-4:]), 'a') as fn:
            for i in range(len(classinfo[classname][1])):
                coordinate = classinfo[classname][1].pop(0)
                fn.write(str(coordinate[0]) + ',' + str(coordinate[1]) + '\n')
    print('Got %d point coordinate!' % (count))
    for classname in classinfo.keys():
        print('class {0:>5s}:{1}'.format(classname, classinfo[classname][0]))


def make_pdtfile(filedir, picsize=256):
    filenames = os.listdir(filedir)
    for file in filenames:
        if file[-4:] == '.txt':
            filename = filedir + '/' + file
            with open(filename, 'r') as fdata:
                coor_data = fdata.readlines()
            with open(filename[:-3] + 'pdt', 'w') as fpdt:
                fpdt.write(str(len(coor_data)) + '\n')
                fpdt.write(str(picsize) + ',' + str(picsize) + '\n')
                for coordinate in coor_data:
                    fpdt.write(coordinate)
    print('Build pdt file finished!')


def get_class_num(input_shp, info_file):
    count = 0
    # ['id', 'SHAPE@XY']
    class_num = {}
    data = arcpy.da.SearchCursor(input_shp, ['GRIDCODE', 'SHAPE@XY'])
    for row in data:
        count += 1
        if row[0] in class_num:
            class_num[row[0]] += 1
        else:
            class_num[row[0]] = 1
    with open(info_file, 'w') as fn:
        for keys, item in class_num.items():
            fn.write('类别：{:<4d}:{:<5d}\n'.format(int(keys), item))


def random_get_feature(input_shp):
    num = 0
    count = 0
    # Set local variables
    out_path = r"D:\NGCC\zheng\men"
    out_name = "randomchoose.shp"
    geometry_type = "POLYGON"
    template = input_shp
    has_m = "DISABLED"
    has_z = "DISABLED"
    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe(
        r"D:\NGCC\zheng\men\complete_within.shp").spatialReference
    # Execute CreateFeatureclass
    if os.path.exists('%s/%s' % (out_path, out_name)):
        os.remove('%s/%s' % (out_path, out_name))
    arcpy.CreateFeatureclass_management(
        out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference)
    print('create new feature!')
    data = arcpy.da.SearchCursor(input_shp)
    for row in data:
        num += 1
    interval = num // 500
    data = arcpy.da.SearchCursor(input_shp)
    new_shp = arcpy.InsertCursor('%s/%s' % (out_path, out_name))
    for row in data:
        count += 1
        if count % interval == 0:
            new_shp.insertRow(row)
    print("finished")


def main():
    print('main process')
    # get the number of every class
    # info_file = r'D:\data\tongji\shp\info_test.txt'
    # input_shp = r'D:\data\tongji\shp\Tongji_right.shp'
    # get_class_num(input_shp, info_file)

    # arcpy.env.workspace = r"D:\NGCC\airport\arcgis_script_workspace"
    # buffer_distence = 1600
    # single_point_shp = r"D:\NGCC\airport\medium_and_big_airport.shp"
    # four_point_square = "four_point_square.shp"
    # # point_to_sqr_point(single_point_shp, buffer_distence, four_point_square)
    # # get_coordinate(r"D:\NGCC\airport\arcgis_script_workspace\four_point_square.shp", '15-17',
    # #                r'D:\NGCC\airport\arcgis_script_workspace\download_file.txt')
    # class_attrs = ('pure_pixel', 'tm_interp')
    # coordinate_list(r"D:\data\AE176_CD_20170704\ShapeFile\AE176_CD_20170704.shp",
    #                 downloadfile=r'D:\data\AE176_CD_20170704\test\AE176_CD_20170704.txt')
    input_shp = r'D:\NGCC\zheng\men\complete_within.shp'
    random_get_feature(input_shp)

if __name__ == '__main__':
    main()
