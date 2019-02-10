from webapp.backend.BoxFactory import BoxFactory
from webapp.backend.GroupBuilder import GroupBuilder
import sys

def main(path):
    factory = BoxFactory(path)
    factory.import_boxes_from_csv()
    all_boxes = factory.get_boxes

    group_builder = GroupBuilder()
    group_builder.build_groups(all_boxes)

    result = group_builder.get_json_file()
    factory.save_boxes_to_file(result)

if __name__ == "__main__":
   main(sys.argv[1])