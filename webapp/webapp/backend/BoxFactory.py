import csv, json
from webapp.backend.Box import Box, Plane

class BoxFactory:
    def __init__(self, resource_path):
        self.resource_path = resource_path
        self._imported_boxes = []
        self.result_path = resource_path.replace("csv", "json")
        self._all_X = []
        self._all_Y = []
        self._all_Z = []

    @property 
    def get_boxes(self):
        return self._imported_boxes

    def get_bounding_box(self):
        start_pt = [min(self._all_X), min(self._all_Y), min(self._all_Z)]
        end_pt = [max(self._all_X), max(self._all_Y), max(self._all_Z)]
        return [start_pt, end_pt]

    def get_all_json_boxes(self):
        return [box.get_json_repr([180,180,180]) for box in self._imported_boxes]

    def add_to_all(self, x, y, z):
        self._all_X.append(x)
        self._all_Y.append(y)
        self._all_Z.append(z)

    def import_boxes_from_csv(self):
        with open(self.resource_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                self.add_to_all(row[1], row[2], row[3])
                self.add_to_all(row[4], row[5], row[6])
                plane_x = Plane(row[0], row[1], row[4])
                plane_y = Plane(row[0], row[2], row[5])
                plane_z = Plane(row[0], row[3], row[6])
                self._imported_boxes.append(Box(row[0], plane_x, plane_y, plane_z))

    def save_boxes_to_file(self, data):
        with open(self.result_path, 'w') as outfile:
             json.dump(data, outfile)
        
        print("------------------------------------")
        print("Result was saved in '{0}'".format(self.result_path))
        print("------------------------------------")