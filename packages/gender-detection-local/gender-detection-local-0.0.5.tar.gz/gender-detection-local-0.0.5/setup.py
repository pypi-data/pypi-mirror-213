import setuptools

setuptools.setup(
     name='gender-detection-local',  
     version='0.0.5',
     author="Circles",
     author_email="info@circles.zone",
     description="PyPI Package for gender detection",
     long_description="This is a package for running gender detection and predicting gender",
     long_description_content_type="text/markdown",
     url="https://github.com/circles-zone/gender-detection-local-python-package",
     packages=setuptools.find_packages(),
     package_data={"CirclesGenderDetectionPython": ["gender_detection"]},
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
    
 )
