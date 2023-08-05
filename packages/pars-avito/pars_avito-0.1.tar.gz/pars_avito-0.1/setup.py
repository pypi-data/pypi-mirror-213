from setuptools import setup, find_packages


setup(name='pars_avito',
      version='0.1',
      author='soketpy',
      author_email='mb_vlad@vk.com',
      url = "https://github.com/Sudox00/pars_avito",
      download_url = "https://github.com/Sudox00/pars_avito/tarball/master",      
      description='Avito parser',
      keywords = ["pars_avito","soketpy"],
      install_requires = ["setuptools","requests", "bs4"],   
      setup_requires = ["wheel"],
      packages=find_packages()
)
