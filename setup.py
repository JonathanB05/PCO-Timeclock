from setuptools import setup
import os
setup(name='PCO Timeclock',
      version='0.1',
      description='Get live times from PCO',
      url='http://github.com/stephentroutner/pcotimeclock',
      author='Stephen Troutner',
      author_email='',
      license='MIT',
      packages=['pcotimeclock'],
      install_requires=[
          'pypco',
          'python-dateutil',
          'keyboard',
          'schedule',
      ],
      zip_safe=False)
id=input("Authentication ID: ")#ask for the Authentication ID
secret=input("Secret: ")#ask for the secret
setup_auth=open(os.getcwd() + "\\pcotimeclock\\"+ "auth.py","w+")#create auth.py
setup_auth.write("id=\"" + id +"\"\n")#write the id to auth.py
setup_auth.write("secret=\"" + secret +"\"\n")#write the secret to auth.py
if not(os.path.exists(os.getcwd() + "\\pcotimeclock\\" + 'logs')):
    os.makedirs(os.getcwd() + "\\pcotimeclock\\" + 'logs')#create the log folder
