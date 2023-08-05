import Signal8
import time

env = Signal8.env('disaster_response')
env.reset(options={"instance_num": 0})
observation, _, terminations, truncations, _ = env.last()
entities = env.unwrapped.get_start_state()
time.sleep(5)
time.sleep(5)
env.step(1)
env.close()