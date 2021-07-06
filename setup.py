from setuptools import setup

def get_dependencies():
    with open("requirements.txt") as f:
        dependencies = f.read()
        return dependencies.split("\n")

setup(name='highlight_butler-Boot-Error',
      version='0.1',
      description='Highlight Butler collects highlights from services and create notes in your note-taking systems',
      url='http://github.com/Boot-Error/highlight_butler',
      author='Boot-Error',
      author_email='booterror99@gmail.com',
      license='MIT',
      packages=['highlight_butler'],
      zip_safe=False,
      install_requires=get_dependencies(),
      entry_points={
          'console_scripts': ['highlight_butler=highlight_butler.app.cli:main']})