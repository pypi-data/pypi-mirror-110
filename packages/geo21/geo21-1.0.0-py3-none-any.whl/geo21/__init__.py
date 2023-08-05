from logging import raiseExceptions
from shapely.geometry import Polygon,MultiPolygon,LineString,Point
import json
from shapely.ops import cascaded_union
import geopandas as gpd
from sklearn.neighbors import BallTree
import numpy as np 
import pandas as pd


# def get_nearest(src_points, candidates, k_neighbors=1):
#     # tree = BallTree(candidates, leaf_size=5, metric='haversine')
#     tree = BallTree(candidates, leaf_size=15, metric='minkowski')
#     distances, indices = tree.query(src_points, k=k_neighbors)
#     distances = distances.transpose()
#     indices = indices.transpose()
#     closest = indices[0]
#     closest_dist = distances[0]
#     return (closest, closest_dist)
# def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
#     left_geom_col = left_gdf.geometry.name
#     right_geom_col = right_gdf.geometry.name
#     right = right_gdf.copy().reset_index(drop=True)
#     left_radians = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
#     right_radians = np.array(right[right_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
#     closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)
#     closest_points = right.loc[closest]
#     closest_points = closest_points.reset_index(drop=True)
#     if return_dist:
#         earth_radius = 6371000  # meters
#         closest_points['distance'] = dist * earth_radius
#     return closest_points
class Geoprocessing:
    def Union(polylist):
        coordinate_list,final_coordinate_list_to_merge,feature_obj_dict,final_child_list,another_final_child_list = [],[],{},[],[]
        if type(polylist) == str:
            try:
                polylist = json.loads(polylist)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for index,file in enumerate(polylist):
                for data in file['features']:
                    area_data = data['properties']
                    if index < 1:
                        feature_obj_dict.update(area_data)
                    elif index>0:
                        for k,v in area_data.items():
                            for new_k,new_v in feature_obj_dict.items():
                                if k == new_k:
                                    feature_obj_dict[k] = (str(v)+" & "+str(new_v))
                        for k,v in area_data.items():
                            if k not in feature_obj_dict:
                                feature_obj_dict[k] = (v)
                                
                            # else:
                                
                for json_values in file['features']:
                    if json_values['geometry']['type'] == 'Polygon':
                        for coordinate in json_values['geometry']['coordinates']:
                            for inner_coordinate in coordinate:
                                if len(inner_coordinate) == 2:
                                    cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                    coordinate_data = (cord1,cord2)
                                    coordinate_list.append(coordinate_data)
                                if len(inner_coordinate) == 3:
                                    cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                    coordinate_data = (cord1,cord2,cord3)
                                    coordinate_list.append(coordinate_data)
                            copy_of_a_coordinate_list = coordinate_list.copy()
                            coordinate_list.clear()
                            convert_coordinate_into_polygon = Polygon(copy_of_a_coordinate_list)
                            final_coordinate_list_to_merge.append(convert_coordinate_into_polygon)
                    elif json_values['geometry']['type'] == 'MultiPolygon':
                        for coords in json_values['geometry']['coordinates']:
                            for coordinate in coords:
                                for inner_coordinate in coordinate:
                                    if len(inner_coordinate) == 2:
                                        cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                        coordinate_data = (cord1,cord2)
                                        coordinate_list.append(coordinate_data)
                                    if len(inner_coordinate) == 3:
                                        cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                        coordinate_data = (cord1,cord2,cord3)
                                        coordinate_list.append(coordinate_data)
                                copy_of_a_coordinate_list = coordinate_list.copy()
                                coordinate_list.clear()
                                convert_coordinate_into_polygon = Polygon(copy_of_a_coordinate_list)
                                final_coordinate_list_to_merge.append(convert_coordinate_into_polygon)
        except TypeError:
            raise TypeError("wrong data format")
        u = cascaded_union(final_coordinate_list_to_merge)
        if type(u) == Polygon:
            for data in u.exterior.coords:
                if len(data) == 3:
                    child_list = [data[0],data[1],data[2]]
                    final_child_list.append(child_list)
                if len(data) == 2:
                    child_list = [data[0],data[1]]
                    final_child_list.append(child_list)
        elif type(u) == MultiPolygon:
            for new_data in u:
                for data in new_data.exterior.coords:
                    if len(data) == 3:
                        child_list = [data[0],data[1],data[2]]
                        final_child_list.append(child_list)
                    elif len(data) == 2:
                        child_list = [data[0],data[1]]
                        final_child_list.append(child_list)
        another_final_child_list.append(final_child_list)
        final_obj = {
            "type": "FeatureCollection",
            "features": [
                        {
                    "type": "Feature",
                    "properties": feature_obj_dict,
                    "geometry": {
                    "type": "Polygon",
                    "coordinates": another_final_child_list
                    }
                 }
            ]
        }
        return final_obj
    def print():
        print("yes its works")
    def Intersection(polylist):
        coordinate_list,final_child_list,feature_obj_dict,new_list_to_store_polygon_data,another_new_list_to_store_polygon_data,new_list_for_intersection,another_final_child_list,final_child_list,file_list = [],[],{},[],[],[],[],[],[]
        if type(polylist) == str:
            try:
                polylist = json.loads(polylist)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for index,file in enumerate(polylist):
            # df = pd.read_json(file)
                for data in file['features']:
                    area_data = data['properties']
                    if index < 1:
                        feature_obj_dict.update(area_data)
                    elif index>0:
                        for k,v in area_data.items():
                            for new_k,new_v in feature_obj_dict.items():
                                if k == new_k:
                                    feature_obj_dict[k] = (str(v)+" & "+str(new_v))
                if index < 1:
                    print("this sis first condition")
                    for json_values in file['features']:
                        if json_values['geometry']['type'] == 'Polygon':
                            for coordinate in json_values['geometry']['coordinates']:
                                for inner_coordinate in coordinate:
                                    if len(inner_coordinate) == 2:
                                        cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                        coordinate_data = (cord1,cord2)
                                        coordinate_list.append(coordinate_data)
                                    if len(inner_coordinate) == 3:
                                        cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                        coordinate_data = (cord1,cord2,cord3)
                                        coordinate_list.append(coordinate_data)
                                copy_of_a_coordinate_list = coordinate_list.copy()
                                coordinate_list.clear()
                                convert_coordinate_into_polygon1 = Polygon(copy_of_a_coordinate_list)
                        elif json_values['geometry']['type'] == 'MultiPolygon':
                            for coord in json_values['geometry']['coordinates']:
                                for coordinate in coord:
                                    for inner_coordinate in coordinate:
                                        if len(inner_coordinate) == 2:
                                            cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                            coordinate_data = (cord1,cord2)
                                            coordinate_list.append(coordinate_data)
                                        if len(inner_coordinate) == 3:
                                            cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                            coordinate_data = (cord1,cord2,cord3)
                                            coordinate_list.append(coordinate_data)
                                    copy_of_a_coordinate_list = coordinate_list.copy()
                                    coordinate_list.clear()
                                    convert_coordinate_into_polygon1 = Polygon(copy_of_a_coordinate_list)
                elif index > 0:
                    for json_values in file['features']:
                        if json_values['geometry']['type'] == 'Polygon':
                            for coordinate in json_values['geometry']['coordinates']:
                                for inner_coordinate in coordinate:
                                    if len(inner_coordinate) == 2:
                                        cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                        coordinate_data = (cord1,cord2)
                                        coordinate_list.append(coordinate_data)
                                    if len(inner_coordinate) == 3:
                                        cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                        coordinate_data = (cord1,cord2,cord3)
                                        coordinate_list.append(coordinate_data)
                                copy_of_a_coordinate_list = coordinate_list.copy()
                                coordinate_list.clear()
                                convert_coordinate_into_polygon2 = Polygon(copy_of_a_coordinate_list)
                                another_new_list_to_store_polygon_data.append(convert_coordinate_into_polygon2)
                        elif json_values['geometry']['type'] == 'MultiPolygon':
                            for coord in json_values['geometry']['coordinates']:
                                for coordinate in coord:
                                    for inner_coordinate in coordinate:
                                        if len(inner_coordinate) == 2:
                                            cord1,cord2= inner_coordinate[0],inner_coordinate[1]
                                            coordinate_data = (cord1,cord2)
                                            coordinate_list.append(coordinate_data)
                                        if len(inner_coordinate) == 3:
                                            cord1,cord2,cord3= inner_coordinate[0],inner_coordinate[1],inner_coordinate[2]
                                            coordinate_data = (cord1,cord2,cord3)
                                            coordinate_list.append(coordinate_data)
                                    copy_of_a_coordinate_list = coordinate_list.copy()
                                    coordinate_list.clear()
                                    convert_coordinate_into_polygon2 = Polygon(copy_of_a_coordinate_list)
                                    another_new_list_to_store_polygon_data.append(convert_coordinate_into_polygon2)
        except TypeError:
            raise TypeError("wrong data format")
        for polygon_data in another_new_list_to_store_polygon_data:
        
            intersection_polygon_data = convert_coordinate_into_polygon1.intersection(polygon_data)
        
            new_list_for_intersection.append(intersection_polygon_data)
        
        u = cascaded_union(new_list_for_intersection)
        
        if type(u) == Polygon:
        
            for data in u.exterior.coords:
        
                if len(data) == 3:
        
                    child_list = [data[0],data[1],data[2]]
        
                    final_child_list.append(child_list)
        
                if len(data) == 2:
        
                    child_list = [data[0],data[1]]
        
                    final_child_list.append(child_list)
        
        elif type(u) == MultiPolygon:
            for new_data in u:
                for data in new_data.exterior.coords:
                    if len(data) == 3:
                        child_list = [data[0],data[1],data[2]]
        
                        final_child_list.append(child_list)
        
                    elif len(data) == 2:
        
                        child_list = [data[0],data[1]]
        
                        final_child_list.append(child_list)
        
        another_final_child_list.append(final_child_list)
        
        final_obj = {
        
            "type": "FeatureCollection",
        
            "features": [
        
                        {
        
                    "type": "Feature",
        
                    "properties": feature_obj_dict,
        
                    "geometry": {
        
                    "type": "Polygon",
        
                    "coordinates": another_final_child_list
        
                    }}]}
        
        return final_obj
    ######################### KNN VIEW ###########################
    # def KNN(s1,d1):
    #     if type(s1) == str:
    #         try:
    #             s1 = json.loads(s1)
    #         except json.decoder.JSONDecodeError:
    #             raise Exception("Expecting property name enclosed in double quotes")
    #     if type(d1) == str:
    #         try:
    #             d1 = json.loads(d1)
    #         except json.decoder.JSONDecodeError:
    #             raise Exception("Expecting property name enclosed in double quotes")
    #     final_dict_list,lat_list,long_list,lat_list2,long_list2,ds_pro,columns_list,destination_fature_list,feature_list,new_col_list = [],[],[],[],[],[],[],[],[],[]
    #     my_dict,new_dict,new_dict2 = {},{},{}
    #     for s in s1['features']:
    #         final_dict_list.append(s['properties'])
    #         lat_list.append(s['geometry']['coordinates'][0])
    #         long_list.append(s['geometry']['coordinates'][1])
    #     for d in d1['features']:
    #         ds_pro.append(d['properties'])
    #         lat_list2.append(d['geometry']['coordinates'][0])
    #         long_list2.append(d['geometry']['coordinates'][1])
    #     source_lat_long_df = pd.DataFrame(zip(lat_list,long_list),columns=['lat','long'])
    #     destination_lat_long_df = pd.DataFrame(zip(lat_list2,long_list2),columns=['lat','long'])
    #     source = gpd.GeoDataFrame(final_dict_list,geometry=gpd.points_from_xy(source_lat_long_df.lat, source_lat_long_df.long))
    #     destination = gpd.GeoDataFrame(geometry=gpd.points_from_xy(destination_lat_long_df.lat, destination_lat_long_df.long))
        
    #     new_des = gpd.GeoDataFrame(ds_pro,geometry=gpd.points_from_xy(destination_lat_long_df.lat, destination_lat_long_df.long))
    #     nearest_points = nearest_neighbor(source,destination,return_dist=True)
    #     nearest_points = nearest_points.rename(columns={"geometry": "closest_stop_geom"})
    #     source = source.join(nearest_points)
    #     source['link'] = source.apply(lambda row: LineString([row['geometry'], row['closest_stop_geom']]), axis=1)
    #     for col in source.columns[0:-4]:
    #         columns_list.append(col)
    #     #columns_list.append('distance')
    #     new_col_list.append("distance")
    #     for col in new_des.columns[0:-1]:
    #         destination_fature_list.append(col)
    #     b = 0
    #     while b < len(source['geometry']):
    #         n = [source['geometry'][b].x,source['geometry'][b].y] ###source POint
    #         l = [source['closest_stop_geom'][b].x,source['closest_stop_geom'][b].y] ### destination POint
    #         new_data = (source['closest_stop_geom'][b].x,source['closest_stop_geom'][b].y)
    #         for data in range(0,len(new_des['geometry'])):
    #             if new_data == (new_des['geometry'][data].x,new_des['geometry'][data].y):
    #                 for i in destination_fature_list:
    #                     new_dict[i] = new_des[i][data] 
    #                 new_dict["type"] = "destination" 
    #                 break
    #         for i in columns_list:
    #             my_dict[i] = source[i][b]
    #         for i in new_col_list:
    #             new_dict2[i] = source[i][b]
    #         my_dict["type"] = "source"
    #         copy_dict,copy_of_new_dict,copy_of_new_dict2 = my_dict.copy(),new_dict.copy(),new_dict2.copy()
    #         new_dict.clear()
    #         my_dict.clear()
    #         new_dict2.clear()
    #         my_obj = { "type": "Feature",
    #                 "geometry": {"type": "Point", "coordinates": n},
    #                 "properties": copy_dict
    #                 }
    #         my_obj_2 = { "type": "Feature",
    #                 "geometry": {"type": "Point", "coordinates": l},
    #                 "properties": copy_of_new_dict
    #                 }
    #         linestring_obj = { "type": "Feature",
    #                 "geometry": {"type": "LineString", "coordinates": [n,l]},
    #                 "properties": copy_of_new_dict2
    #                 }
    #         feature_list.append(my_obj)
    #         feature_list.append(my_obj_2)
    #         feature_list.append(linestring_obj)
    #         b+=1

    #     final_obj = { "type": "FeatureCollection",
    #             "features":feature_list
    #     }
            
    #     return final_obj
    ############### point withon polygon ##################
    def AvlPoint(point_data,polygon_data):
        point_array,polygon_list,feature_list,fl,nl,list_to_store_final_obj = [],[],[],[],[],[]
        if type(point_data) == str:
            try:
                point_data = json.loads(point_data)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        if type(polygon_data) == str:
            try:
                polygon_data = json.loads(polygon_data)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for point  in point_data['features']:
                feature_list.append(point['properties'])
                if len(point['geometry']['coordinates']) == 3:
                    x,y,z = point['geometry']['coordinates'][0] , point['geometry']['coordinates'][1], point['geometry']['coordinates'][2] 
                    final_data = (x,y,z)
                    point_array.append(final_data)
                elif len(point['geometry']['coordinates']) == 2:
                    x,y = point['geometry']['coordinates'][0] , point['geometry']['coordinates'][1]
                    final_data = (x,y)
                    point_array.append(final_data)
            for index1,poly_data in enumerate(polygon_data):
                for all_data in poly_data['features']:
                    if all_data['geometry']['type'] == 'Polygon':
                        for coords in all_data['geometry']['coordinates']:
                            for data in coords:
                                if len(data) == 3:
                                    a,b,c = data[0],data[1],data[2]
                                    da = (a,b,c)
                                    polygon_list.append(da)
                                elif len(data) == 2:
                                    a,b = data[0],data[1]
                                    da = (a,b)
                                    polygon_list.append(da)
                    elif all_data['geometry']['type'] == 'MultiPolygon':
                        for coords in all_data['geometry']['coordinates']:
                            for c in coords:
                                for data in c:
                                    if len(data) == 3:
                                        a,b,c = data[0],data[1],data[2]
                                        da = (a,b,c)
                                        polygon_list.append(da)
                                    elif len(data) == 2:
                                        a,b = data[0],data[1]
                                        da = (a,b)
                                        polygon_list.append(da)
                    copy_of_polygon_list = polygon_list.copy()
                    polygon_list.clear()
                    poly = Polygon(copy_of_polygon_list)
                    for index,data in enumerate(point_array):
                        pd = Point(data)
                        result = pd.within(poly)
                        if result == True:
                            point_obj = {
                                "type": "Feature",
                                "geometry": {
                                "type": "Point",
                                "coordinates":data
                                        },
                            "properties": feature_list[index]
                            }
                            fl.append(point_obj)
                    copy_of_fl = fl.copy()
                    fl.clear()
                    another_obj =  {
                                "polygon": index1,
                                "pointCollection": {
                                "type" : "FeatureCollection",
                                "features": copy_of_fl,
                                    }
                            }
                    list_to_store_final_obj.append(another_obj ) 
            return list_to_store_final_obj
        
        except TypeError:
            raise TypeError("wrong data format")
    ################ poly buffer ################# 
    def PolyBuffer(points,area):
        final_lat_long_list,final_list,feature_list = [],[],[]
        if type(points) == str:
            try:
                points = json.loads(points)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        if type(area) == str:
            try:
                area = float(area)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for point in points:
                if len(point) == 2:
                    p1 = Point((point[0],point[1]))
                    poly = Polygon(p1.buffer((area*0.00001)/1.0247,cap_style=1))
                elif len(point) == 3:
                    p1 = Point((point[0],point[1],point[2]))
                    poly = Polygon(p1.buffer((area*0.00001)/1.0247,cap_style=1))
                if type(poly) == Polygon:
                    for pnt in poly.exterior.coords:
                        if len(pnt) == 2:
                            reserve_list = [pnt[0],pnt[1]]
                        elif len(pnt) == 3:
                            reserve_list = [pnt[0],pnt[1],pnt[2]]
                        final_list.append(reserve_list)
                elif type(poly) == MultiPolygon:
                    for po in poly:
                        for pnt in po.exterior.coords:
                            if len(pnt) == 2:
                                reserve_list = [pnt[0],pnt[1]]
                            elif len(pnt) == 3:
                                reserve_list = [pnt[0],pnt[1],pnt[2]]
                            final_list.append(reserve_list)
                copy_of_final_list = final_list.copy()
                final_list.clear()
                my_obj = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [copy_of_final_list]
                        },
                        "properties": {
                        }
                    }

                feature_list.append(my_obj)

            final_obj = {
                "type": "FeatureCollection",
                "features": feature_list
                }
            return final_obj
        except TypeError:
            raise TypeError("wrong data format")
    #################### line buffer ###################
    def LineBuffer(points,area):
        final_lat_long_list,final_list,list_for_rearrange_data,final_list2,feature_list = [],[],[],[],[]
        if type(points) == str:
            try:
                points = json.loads(points)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        if type(area) == str:
            try:
                area = float(area)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for i in range(0,len(points)):
                for d in range(0,len(points[i])):
                    # print(points[i][d][0])
                    list_for_rearrange_data.append(points[i][d][0])
                    list_for_rearrange_data.append(points[i][d][1])
                copy_of_list = list_for_rearrange_data.copy()
                list_for_rearrange_data.clear()
                for latlong_data in range(0,len(copy_of_list),2):
                    p1 = Point((copy_of_list[latlong_data],copy_of_list[latlong_data+1]))
                    final_lat_long_list.append(p1)
                copy_of_final_lat = final_lat_long_list.copy()
                final_lat_long_list.clear()
                linestring = LineString(copy_of_final_lat)
                add_buffer = linestring.buffer((area*0.00001)/1.0247,cap_style=2)
                for line in add_buffer.exterior.coords:
                    nd = [line[0],line[1]]
                    final_list.append(nd)
                for line in linestring.coords:
                    nd = [line[0],line[1]]
                    final_list2.append(nd)
                copy_of_final_list = final_list.copy()
                copy_of_final_list2 = final_list2.copy()
                final_list.clear()
                final_list2.clear()
                geo_json_obj1 =  {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                        "type": "Polygon",
                        "coordinates":[copy_of_final_list]
                                }
                                }

                geo_json_obj2 = {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                        "type": "LineString",
                        "coordinates":copy_of_final_list2
                    }
                    }
                feature_list.append(geo_json_obj1)
                feature_list.append(geo_json_obj2)
            final_obj = {
                "type": "FeatureCollection",
                "features": feature_list
                }
            return final_obj
        except TypeError:
            raise TypeError("wrong data format")

    def Linestring(linestring,gap,quantity):
        line_string_list,feature_list = [],[]
        if type(linestring) == str:
            try:
                linestring = json.loads(linestring)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        if type(gap) == str:
            try:
                gap = float(gap)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        if type(quantity) == str:
            try:
                quantity = int(quantity)
            except json.decoder.JSONDecodeError:
                raise Exception("Expecting property name enclosed in double quotes")
        try:
            for feature in linestring['features']:
                linestring = LineString(feature['geometry']['coordinates'])
            add_buffer = linestring.buffer((gap*0.00001)/1.0247,cap_style=2,single_sided=True)
            for line in add_buffer.exterior.coords:
                line_string_list.append(line)
            my_obj = {
                    "type": "Feature",
                    "geometry": {
                    "type": "LineString",
                    "coordinates": [[line_string_list[2][0],line_string_list[2][1]],[line_string_list[3][0],line_string_list[3][1]]]}}
            feature_list.append(my_obj)
            a = 0
            while a < quantity:
                copy_of_line_string = line_string_list.copy()
                line_string_list.clear()
                new_linestring = LineString([[copy_of_line_string[2][0],copy_of_line_string[2][1]],[copy_of_line_string[3][0],copy_of_line_string[3][1]]])
                add_buffer2 = new_linestring.buffer((gap*0.00001)/1.0247,cap_style=2,single_sided=True)
                for line in add_buffer2.exterior.coords:
                    line_string_list.append(line)
                my_obj = {
                        "type": "Feature",
                        "geometry": {
                        "type": "LineString",
                        "coordinates": [[line_string_list[2][0],line_string_list[2][1]],[line_string_list[3][0],line_string_list[3][1]]]}
                        }
                feature_list.append(my_obj)     
                a+=1
            final_obj =  {
                    "type": "FeatureCollection",
                    "features":feature_list,
                    }
            return final_obj
        except TypeError:
            raise TypeError("wrong data format")

        