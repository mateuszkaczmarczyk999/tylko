import csv, json
from webapp.backend.Box import Box, Plane

class BoxFactory:
    def __init__(self, resource_path):
        self.resource_path = resource_path
        self._imported_boxes = []
        self.result_path = resource_path.replace("csv", "json")
        self._all_coordinates = []

    @property 
    def get_boxes(self):
        return self._imported_boxes

    def get_bounding_box(self):
        end_pt = max(self._all_coordinates)
        return [end_pt, end_pt, end_pt]

    @property 
    def get_scalar(self):
        scalar = 1
        if(int(max(self._all_coordinates)) > 0):
            scalar = float(100/int(max(self._all_coordinates)))
        return scalar

    def get_all_json_boxes(self):
        return [box.get_json_repr([180,180,180]) for box in self._imported_boxes]

    def import_boxes_from_csv(self):
        with open(self.resource_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                self._all_coordinates.extend(row[1:])
                plane_x = Plane(row[0], row[1], row[4])
                plane_y = Plane(row[0], row[2], row[5])
                plane_z = Plane(row[0], row[3], row[6])
                self._imported_boxes.append(Box(row[0], plane_x, plane_y, plane_z, self))

    def save_boxes_to_file(self, data):
        with open(self.result_path, 'w') as outfile:
             json.dump(data, outfile)
        
        print("------------------------------------")
        print("Result was saved in '{0}'".format(self.result_path))
        print("------------------------------------")