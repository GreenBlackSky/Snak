class Controller:
    def __init__(self):
        self.direction = (0, -1)
        self.desired_direction = self.direction
        
    def desire(self, direction):
        self.desired_direction = direction
        
    def decision(self):
        ndx, ndy = self.desired_direction
        cdx, cdy = self.direction
        if (ndx + cdx, ndy + cdy) != (0, 0):
            self.direction = (ndx, ndy)
        return self.direction
