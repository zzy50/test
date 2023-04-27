from dataclasses import dataclass, make_dataclass

@dataclass
class InfoCountedObject:
    pass
total_list = [[3,5,8,21,132],
              [4,5,9,11,52]]

tracked_object = InfoCountedObject()
for id_list in total_list:
    tracked_object
