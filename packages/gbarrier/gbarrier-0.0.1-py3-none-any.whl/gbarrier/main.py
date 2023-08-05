class GBarrier:
    def __init__(self, point_number, skud_sdk, *args, **kwargs):
        self.point_number = 1
        self.state = 'LOCKED'
        self.last_open_timestamp = None
        self.last_close_timestamp = None
        self.skud_sdk = skud_sdk
        self.point_number = point_number

    def set_state(self, state, *args, **kwargs):
        self.state = state

    def get_state(self, *args, **kwargs):
        return self.state

    def set_last_open_timestamp(self, timestamp, *args, **kwargs):
        self.last_open_timestamp = timestamp

    def get_last_open_timestamp(self, *args, **kwargs):
        return self.last_open_timestamp

    def set_last_close_timestamp(self, timestamp, *args, **kwargs):
        self.last_close_timestamp = timestamp

    def get_last_close_timestamp(self, *args, **kwargs):
        return self.last_close_timestamp

    def open_barrier(self):
        self.skud_sdk.open_gate(self.point_number)

    def close_barrier(self):
        self.skud_sdk.open_gate(self.point_number)
