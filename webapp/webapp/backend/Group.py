import json

class Group:
    def __init__(self):
        self.group_id = None
        self._boxes = []
        self.color = []
    
    @property    
    def get_boxes(self):
        return self._boxes

    @property    
    def get_boxes_id(self):
        return [box.id for box in self._boxes]

    @property    
    def elements_ids(self):
        return [box.id for box in self._boxes]

    @property 
    def no_elements(self):
        return len(self._boxes)

    def contains(self, box):
        return box in self._boxes

    def __repr__(self):
        return "Group: no_elements={0} group_id={1} elements_ids={2}".format(self.no_elements, self.group_id, self.elements_ids)


class AttachedGroup(Group):
    _all_groups = []

    def __init__(self):
        super().__init__()
        AttachedGroup._all_groups.append(self)
        self._all_X = []
        self._all_Y = []
        self._all_Z = []

    def add(self, box):
        box.attached_group = self
        self._boxes.append(box)
        self._all_X.extend(box.vector_X)
        self._all_Y.extend(box.vector_Y)
        self._all_Z.extend(box.vector_Z)

    def get_json(self):
        data = {}
        data["elements"] = 'wszystkie boxy'
        data["groups"] = '{"0": {"no_elements": 3, "group_id": 0, "elements_ids": ["0", "1", "2"], "group_volume": 200}'
        return json.dumps(data)

    @property 
    def group_volume(self):
        h = max(self._all_X) - min(self._all_X)
        w = max(self._all_Y) - min(self._all_Y)
        l = max(self._all_Z) - min(self._all_Z)
        return h*w*l

    def get_dict(self):
        return { "no_elements": self.no_elements, "group_id": self.group_id, "elements_ids": self.get_boxes_id, "group_volume": self.group_volume } 

    def __repr__(self):
        return "Group: no_elements={0} group_id={1} elements_ids={2} group_volume={3}".format(self.no_elements, self.group_id, self.elements_ids, self.group_volume)


class ThicknessGroup(Group):
    _all_groups = []

    def __init__(self, thickness):
        super().__init__()
        ThicknessGroup._all_groups.append(self)
        self.thickness = thickness

    def add(self, boxes):
        for box in boxes:
            box.thickness_group = self
        self._boxes.extend(boxes)

    @property 
    def total_area(self):
        return sum([box.area for box in self._boxes])

    def get_dict(self):
        return { "no_elements": self.no_elements, "total_area": self.total_area, "elements_ids": self.get_boxes_id, "thickness": self.thickness }        

    def __repr__(self):
        return "Group: no_elements={0} group_id={1} elements_ids={2} thickness={3} total_area={4}".format(self.no_elements, self.group_id, self.elements_ids, self.thickness, self.total_area)