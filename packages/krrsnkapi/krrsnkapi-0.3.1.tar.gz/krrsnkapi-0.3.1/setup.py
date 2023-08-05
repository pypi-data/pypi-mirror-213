from setuptools import setup

# ver = input("version: ")

setup(
  name = 'krrsnkapi',         # How you named your package folder (MyLib)
  packages = ['krrsnkapi'],   # Chose the same as "name"
  version = "0.3.1",      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Module for easy use of my api | info on GitHub: https://github.com/kararasenok-gd/krrsnkapi',   # Give a short description about your library
  author = 'kararasenok_gd',                   # Type in your name
  author_email = 'murzikkurzikpro@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/kararasenok-gd/krrsnkapi',   # Provide either the link to your github or to your website
  download_url = f'https://github.com/kararasenok-gd/krrsnkapi/archive/v0.3.tar.gz',    # I explain this later on
  keywords = ["api"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8'
  ],
)