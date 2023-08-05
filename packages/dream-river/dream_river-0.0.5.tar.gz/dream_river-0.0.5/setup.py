from setuptools import setup, find_packages

DESC ='This is a library that contain rice cultivated area detection tools and other geospatial tools for jupyter environment on https://sphere.gistda.or.th/ in part of Data Cube. Thus, you needs go to sphere.gistda (https://sphere.gistda.or.th/) and register the account to access jupyter lab environment interactively from a browser.'

setup(
    name='dream_river',
    packages=['dream_river'],
    version='0.0.5',
    license='MIT',
    author_email='dreamusaha@gmail.com',
    description= 'This is a library contained rice detection tools and other geospatial tools for jupyter environment on sphere.gistda.or.th in part of Data Cube',
    long_description= DESC,
    author='Pathakorn Usaha',
    url= 'https://github.com/Pathakorn40/rice-detection',
    download_url= 'https://pypi.org/project/dream_river/',
    keywords= ['geography','geospatiol','gis', 'rice detection'],
    install_requires= ['datacube','shapely','xarray','matplotlib','numpy','geopandas','dea_tools','scikit-learn',
                'pydotplus','flusstools','scikit-image','GDAL','scipy','folium','odc.ui'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ],
    )

