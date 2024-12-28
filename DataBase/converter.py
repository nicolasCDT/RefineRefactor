__author__ = "nicolasCDT"
__description__ = "refine_table generator"

######################
# STATICS:
PATH = "item_proto.txt"
# Put the column's name (look first line)
VNUM_NAME = "ITEM_VNUM"
DEST_NAME = "REFINE"
REFINE_SET = "REFINESET"


class Converter:
    """Converter TXT -> SQl"""
    def __init__(self, proto_file: str):
        """Initialization of converter class
        :param proto_file: path of item_proto.txt
        """
        self.proto_file = proto_file
        self.vnum_index = -1
        self.dest_index = -1
        self.refine_set_index = -1
        self.first_line = list()
        self.content= list()
        self.refines = list()

    def read(self):
        """Read item_proto and save data"""
        with open(self.proto_file, "r+", encoding="utf-8") as file:
            lines = file.readlines()
            self.first_line = lines[0].split("\t")
            self.content = [x.split("\t") for x in lines[1:]]
        self.vnum_index = self.first_line.index(VNUM_NAME)
        self.dest_index = self.first_line.index(DEST_NAME)
        self.refine_set_index = self.first_line.index(REFINE_SET)
        for line in self.content:
            if line[self.dest_index] != '0':
                self.refines.append({
                    "vnum": line[self.vnum_index],
                    "refine": line[self.dest_index],
                    "refine_set": line[self.refine_set_index]
                })

    def write(self):
        """Write sql file"""
        with open("refine_table.sql", "w+", encoding="utf-8") as file:
            file.write("""CREATE TABLE `refine_table`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `src_vnum` int(11) NOT NULL DEFAULT 0,
  `dest_vnum_0` int(11) NOT NULL DEFAULT 0,
  `refine_set_0` int(11) NOT NULL DEFAULT 0,
  `dest_vnum_1` int(11) NOT NULL DEFAULT 0,
  `refine_set_1` int(11) NOT NULL DEFAULT 0,
  `dest_vnum_2` int(11) NOT NULL DEFAULT 0,
  `refine_set_2` int(11) NOT NULL DEFAULT 0,
  `dest_vnum_3` int(11) NOT NULL DEFAULT 0,
  `refine_set_3` int(11) NOT NULL DEFAULT 0,
  `dest_vnum_4` int(11) NOT NULL DEFAULT 0,
  `refine_set_4` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 0 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;
""")
            for index, item in enumerate(self.refines):
                file.write("INSERT INTO `refine_table`  VALUES (0, {}, {}, {}, 0, 0, 0, 0, 0, 0, 0, 0); \n".format(
                    item["vnum"],
                    item["refine"],
                    item["refine_set"]
                ))

    def run(self) -> None:
        """Enter function to start working"""
        self.read()
        self.write()


if __name__ == '__main__':
    Converter(PATH).run() # Main work
