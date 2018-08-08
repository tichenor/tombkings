from collections import deque


class TimeObject:

    time_travelers = deque()

    def __init__(self, action_pts=0):
        self.owner = None
        self.action_pts = action_pts

    def register(self):
        TimeObject.time_travelers.append(self)
        self.action_pts = 0

    def release(self):
        TimeObject.time_travelers.remove(self)

    def tick(self):
        if len(TimeObject.time_travelers) > 0:
            time_obj = TimeObject.time_travelers[0]
            TimeObject.time_travelers.rotate()
            time_obj.action_pts += time_obj.owner.fighter.speed
            while time_obj.action_pts > 0:
                time_obj.action_pts -= time_obj.owner.ai.take_turn()


