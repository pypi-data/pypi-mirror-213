import numpy as np
from Cython.Build import cythonize
from setuptools import setup

if __name__ == '__main__':
    import os, sys

    if sys.argv[1] == 'clear':
        os.remove(f'nsqdriver/compiler/ns_wave.c')
        os.remove(f'nsqdriver/compiler/py_wave_asm.c')
        os.remove(f'nsqdriver/compiler/ns_wave.py')
        os.remove(f'nsqdriver/compiler/py_wave_asm.py')
        sys.exit(0)
    else:
        setup(
            name='compiler',
            ext_modules=cythonize([r'nsqdriver/compiler/ns_wave.py', r'nsqdriver/compiler/py_wave_asm.py'],
                                  language_level=3),
            include_path=[np.get_include()]
        )
