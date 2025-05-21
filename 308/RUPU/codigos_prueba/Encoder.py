from gpiozero import Button

class Encoder(object):
    def __init__(self, A, B):
        self.A = Button(A, pull_up=True)
        self.B = Button(B, pull_up=True)
        self.pos = 0
        self.state = (self.A.is_pressed << 1) | self.B.is_pressed
        
        self.A.when_pressed = self.__update
        self.A.when_released = self.__update
        self.B.when_pressed = self.__update
        self.B.when_released = self.__update

    def __update(self):
        state = (self.A.is_pressed << 1) | self.B.is_pressed
        delta = (self.state << 2) | state
        self.state = state

        if delta == 1 or delta == 7 or delta == 8 or delta == 14:
            self.pos += 1
        elif delta == 2 or delta == 4 or delta == 11 or delta == 13:
            self.pos -= 1
        elif delta == 3 or delta == 12:
            self.pos += 2
        elif delta == 6 or delta == 9:
            self.pos -= 2

    def read(self):
        return self.pos

    def write(self, num):
        self.pos = num
