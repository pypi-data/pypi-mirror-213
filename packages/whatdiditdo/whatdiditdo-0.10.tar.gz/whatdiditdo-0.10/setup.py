from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Observes what processes are doing (Windows only)'''

# Setting up
setup(
    name="whatdiditdo",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/whatdiditdo',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_df_to_string', 'a_pandas_ex_fast_string', 'a_pandas_ex_horizontal_explode', 'copytool', 'flatten_everything', 'gethandledf', 'getregdf', 'kthread_sleep', 'list_all_files_recursively', 'numpy', 'pandas', 'psutil', 'subprocesskiller', 'touchtouch'],
    keywords=['Monitoring', 'processes'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_df_to_string', 'a_pandas_ex_fast_string', 'a_pandas_ex_horizontal_explode', 'copytool', 'flatten_everything', 'gethandledf', 'getregdf', 'kthread_sleep', 'list_all_files_recursively', 'numpy', 'pandas', 'psutil', 'subprocesskiller', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*