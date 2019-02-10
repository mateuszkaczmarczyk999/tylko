from webapp.backend.Group import AttachedGroup, ThicknessGroup, Group
from time import time

def timer(build_func):
    def func_wrapp(self, boxes):
        start = time()
        build_func(self, boxes)
        end = time()
        print("------------------------------------")
        print("Time for building groups:", end-start)
        print("------------------------------------")

    return func_wrapp

class GroupBuilder:
    def __init__(self):
        self.thickness_dict = {}
        self.boxes_to_check = {}
        self._sorted_attached_groups = []
        self._sorted_thickness_groups = []

    @property 
    def sorted_attached_groups(self):
        return self._sorted_attached_groups

    @property 
    def sorted_thickness_groups(self):
        return self._sorted_thickness_groups

    @property 
    def thickness_groups(self):
        return ThicknessGroup._all_groups

    @property 
    def attached_groups(self):
        return AttachedGroup._all_groups

    @timer
    def build_groups(self, all_boxes):
        self.binary_search_attached_planes(all_boxes)
        self.build_attached_groups()
        self.build_thickness_groups()
        self.sort_attached_groups()
        self.sort_thickness_groups()

    def sort_boxes_by_start_edge_of_plane(self, all_boxes):
        by_X = sorted(all_boxes, key=lambda b: b.planes[0].start_edge)
        by_Y = sorted(all_boxes, key=lambda b: b.planes[1].start_edge)
        by_Z = sorted(all_boxes, key=lambda b: b.planes[2].start_edge)
        return [by_X, by_Y, by_Z]

    def binary_search_attached_planes(self, all_boxes):
        boxes_grouped_by_plane = self.sort_boxes_by_start_edge_of_plane(all_boxes)
        for axis_idx, box_group in enumerate(boxes_grouped_by_plane):
            checked_targets = []
            for box in box_group:
                target = box.planes[axis_idx].end_edge
                if(target not in checked_targets):
                    first = self.binary_search(box_group, target, axis_idx, False, True)
                    last = self.binary_search(box_group, target, axis_idx, True, False)
                    if(box in self.boxes_to_check.keys()):
                        self.boxes_to_check[box].append({axis_idx: box_group[first:last+1]})
                    else:
                        self.boxes_to_check[box] = [{axis_idx: box_group[first:last+1]}]


    def binary_search(self, box_group, target, axis_idx, right=False, left=False): 
        start_id = 0
        end_id = len(box_group) - 1
        result = -1

        while(start_id <= end_id):
            mid_id = (start_id + end_id)//2
        
            if box_group[mid_id].planes[axis_idx].start_edge < target:
                start_id = mid_id + 1
            elif box_group[mid_id].planes[axis_idx].start_edge > target:
                end_id = mid_id - 1
            else:
                result = mid_id
                if(right):
                    start_id = mid_id + 1
                if(left):
                    end_id = mid_id - 1
        return result
                

    def build_attached_groups(self):
        for box, boxes_by_axis in self.boxes_to_check.items():
            box.find_neighbours(boxes_by_axis)
            if(len(box.get_neighbours) > 1):
                self.assign_to_group(box)

    def assign_to_group(self, box):
        attached_group = next((box.attached_group for box in box.get_neighbours if box.attached_group is not None), AttachedGroup())
        for neighbour in box.get_neighbours:
            if(not attached_group.contains(neighbour)):
                attached_group.add(neighbour)

    def build_thickness_groups(self):
        self.build_thickness_dict()
        for key, val in self.thickness_dict.items():
            thickness_group = ThicknessGroup(key)
            thickness_group.add(val)

    def build_thickness_dict(self):
        for group in AttachedGroup._all_groups:
            if(group.no_elements > 1):
                self._sorted_attached_groups.append(group)
                for box in group.get_boxes:
                    self.group_by_thickness(box)

    def group_by_thickness(self, box):
        if(box.thickness not in self.thickness_dict.keys()):
            self.thickness_dict[box.thickness] = []
        self.thickness_dict[box.thickness].append(box)

    def sort_attached_groups(self):
        self._sorted_attached_groups.sort(key=lambda g: g.group_volume)
        for idx, group in enumerate(self._sorted_attached_groups):
            group.group_id = idx

    def sort_thickness_groups(self):
        self._sorted_thickness_groups = sorted(ThicknessGroup._all_groups, key=lambda g: g.thickness)

    def get_json_file(self):
        return {'elements' : {box.id : box.get_dict() for g in self.sorted_attached_groups for box in g.get_boxes},
                'materials' : {g.thickness : g.get_dict() for g in self.sorted_thickness_groups},
                'groups' : {i : v.get_dict() for i,v in enumerate(self.sorted_attached_groups)}}