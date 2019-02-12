from functools import reduce 

class Box:
    def __init__(self, id, x_plane, y_plane, z_plane, factory):
        self.id = int(id)
        self.planes = [x_plane, y_plane, z_plane]
        self.edges = [x_plane.range, y_plane.range, z_plane.range]
        self.attached_group = None
        self.thickness_group = None
        self._neighbours = set()
        self._neighbours.add(self)
        self._factory = factory

    @property 
    def get_neighbours(self):
        return self._neighbours

    @property 
    def get_centroid(self):
        x = sum(self.vector_X) / 2
        y = sum(self.vector_Y) / 2
        z = sum(self.vector_Z) / 2
        return [x, y, z]

    @property 
    def vector_X(self):
        return [self.planes[0].start_edge, self.planes[0].end_edge]

    @property 
    def vector_Y(self):
        return [self.planes[1].start_edge, self.planes[1].end_edge]

    @property 
    def vector_Z(self):
        return [self.planes[2].start_edge, self.planes[2].end_edge]

    @property 
    def thickness(self):
        return min(self.edges)

    @property 
    def area(self):
        result = 1
        for edge in self.edges:
            result *= edge
        return result//self.thickness

    def check_is_box_attach(self, other_box, axis_id):
        to_check = [i for i, p in enumerate(self.planes) if i != axis_id]
        return all(self.planes[i].is_intersect_with(other_box.planes[i]) for i in to_check)

    def find_neighbours(self, boxes_by_axis):
        for group in boxes_by_axis:
            for axis_id, boxes_to_check in group.items():
                for box in boxes_to_check:
                    if(self.check_is_box_attach(box, axis_id)):
                        self._neighbours.add(box)

    def get_json_repr(self, color):
        scalar = self._factory.get_scalar
        return {"id": self.id, "width": self.edges[0]*scalar, "height": self.edges[1]*scalar, "depth": self.edges[2]*scalar, "color": color, 
                "position": {"x": self.get_centroid[0]*scalar, "y": self.get_centroid[1]*scalar, "z": self.get_centroid[2]*scalar}}

    def get_dict(self):
        return {"y1": self.vector_Y[0], "x1": self.vector_X[0], "z1": self.vector_Z[0], "id": self.id, "y2": self.vector_Y[1], "x2": self.vector_X[1], "z2": self.vector_Z[1]}

    def __repr__(self):
        return str(self.id)


class Plane:
    def __init__(self, box_id, start, end):
        self.box_id = box_id
        self.start_edge = int(start)
        self.end_edge = int(end)

    @property 
    def range(self):
        return self.end_edge - self.start_edge

    def is_intersect_with(self, plane):
        return ((plane.end_edge > self.start_edge) and (plane.start_edge < self.end_edge))

    def is_on_the_edge(self, plane):
        return (plane.start_edge == self.end_edge) or (plane.end_edge == self.start_edge)