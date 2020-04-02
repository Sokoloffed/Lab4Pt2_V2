class Item:
    schedule = []

    def __init__(self, course, group, professor, room, slot):
        self.course = course
        self.group = group
        self.professor = professor
        self.room = room
        self.slot = slot

    def __repr__(self):
        return "{}  |  {}  |  {}  |  {}  |  {}".format(str(self.course),
                                                       str(self.group),
                                                       str(self.professor),
                                                       str(self.room),
                                                       str(self.slot))
