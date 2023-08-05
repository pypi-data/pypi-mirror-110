from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
] #You can changed this information to be more relevant or you can also left as it is
 
setup(
  name='implement_pypi_example', #this is the name of your package. make sure to check
      #the availability of the name on pypi.org, as package name must be unique.
      #To avoid confusion, name it with the same name of the folder that contains codes.
  version='0.0.0', #the version of your package, remember that you can not
      #upload a version more than once, so the version name must be
      #changed before upload, even if it just a minor change.
  description='Example on how to upload package on pypi', #introduction to your pypi package
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  # can be left as it is
  url='',  #if your package have a website, provide it here
  author='Nguyen Nguyen Nguyen', #your name, for credit if package becomes famous
  author_email='example@example.com', #contact email
  license='MIT', #if you use default licence, just leave it as it is. If you use
      #other licence, provide the name here
  classifiers=classifiers, #shall not change
  keywords='example', #the keyword about your package 
  packages=find_packages(), #shall not change
  install_requires=['numpy'] #if your package require other external existing
  #package, provide it here. Note that standard package like random or math is not required,
  #and thus, should not be put here. If your requires none, replace that line it to:
  #install_requires=[]
)
