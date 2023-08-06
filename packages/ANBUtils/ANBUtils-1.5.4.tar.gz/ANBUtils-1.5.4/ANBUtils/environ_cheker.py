import os
import warnings

def environment_checker():
    for k in ['MONGODB_URL', 'MONGODB_PUB_URI', 'DINGTALK_WEBHOOK']:
        if k not in os.environ:
            warnings.warn('\nPlease set %s in environment variable' %k)