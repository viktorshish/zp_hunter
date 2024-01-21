from environs import Env


env = Env()
env.read_env()

LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']

SB_KEY = env.str("SB_KEY")
