from .motor import CalibratedMotor

class Forklift:
    def __init__(self, bot):
        self._bot = bot

        self._rotate_motor = CalibratedMotor(CalibratedMotor._bp.PORT_C, calpow=70)
        self._height_motor = CalibratedMotor(CalibratedMotor._bp.PORT_A, calpow=40)

    def __del__(self):
        self._height_motor.to_init_position()

    def stop_all(self):
        self._rotate_motor.stop()
        self._height_motor.stop()

    def calibrate(self):
        # TODO: standard calibration routine does not work well with this one
        # self._rotate_motor.calibrate()
        self._rotate_motor._pmin = self._rotate_motor._pinit = -128
        self._rotate_motor._pmax = 15603

        self._height_motor.calibrate()

    def to_carry_mode(self):
        # rotate backwards
        self._rotate_motor.change_position(self._rotate_motor._pmax)

        # move fork up
        self._height_motor.to_init_position()

    def to_pickup_mode(self):
        # rotate forward
        self._rotate_motor.to_init_position()

        # move fork down
        pos = self._height_motor.position_from_factor(-1.0)
        self._height_motor.change_position(pos)
