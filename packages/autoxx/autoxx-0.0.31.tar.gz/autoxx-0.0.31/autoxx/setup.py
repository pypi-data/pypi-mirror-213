import openai,os
from autoxx.config.config import Config, GlobalConfig

def setup_config(
        debug:bool = False,
) -> Config:
    globalCFG = GlobalConfig()

    CFG = globalCFG.get()
    openai.api_key = CFG.openai_api_key
    return CFG
