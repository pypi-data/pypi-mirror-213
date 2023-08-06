import os
from sys import maxsize, platform

def add_foma(original_function):
    def func_wrapper(*args, **kwargs):
        add_foma_to_path()
        return original_function(*args, **kwargs)
    
    return func_wrapper

def add_foma_to_path():
    bin_dir = os.path.join(
        os.path.dirname(__file__),
        'bin'
    )

    is_64 = maxsize > 2**32
    foma_path = ""
    if platform == "linux" or platform == "linux2":
        
        if is_64:
            foma_path = os.path.join(
                bin_dir,
                'linux64',
                'linux-x86_64'
            )
        else:
            foma_path = os.path.join(
                bin_dir,
                'linux32',
                'i386'
            )
    elif platform == "win32":
        foma_path = os.path.join(
            bin_dir,
            'windows',
            'win32'
        )

    if foma_path not in os.environ["PATH"]:  
        os.environ["PATH"] += os.pathsep + foma_path
