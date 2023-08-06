from gym.envs.registration import register

register(
    id='panda_env-v0',
    entry_point='gym_panda_env.envs:PandaGymEnv',
)