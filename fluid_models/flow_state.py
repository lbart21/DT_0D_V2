class FlowState():
    def __init__(self, model, state):
        self.fluid_model = model
        self.fluid_state = state
        self.vel_x = 0.0
        self.Ma = 0.0