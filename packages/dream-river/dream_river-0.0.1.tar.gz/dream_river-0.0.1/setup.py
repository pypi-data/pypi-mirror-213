from setuptools import setup, find_packages

DESC ='This is a library that contain rice cultivated area detection tools and other geospatial tools for jupyter environment on https://sphere.gistda.or.th/ in part of Data Cube. Thus, you needs go to [sphere.gistda](https://sphere.gistda.or.th/) and [register the account](https://auth.sphere.gistda.or.th/auth/realms/sphere/protocol/openid-connect/registrations?client_id=frontend-iframe&redirect_uri=https%3A%2F%2Fsphere.gistda.or.th%2Fdashboard&state=b1580907-8f21-4a28-bd78-8cfa2ff9064b&response_mode=fragment&response_type=code&scope=openid&nonce=20300185-bc7b-4695-92c4-aa3159db0812&ui_locales=en) to access jupyter lab environment interactively from a browser.'

setup(
    name='dream_river',
    packages=['dream_river'],
    version='0.0.1',
    license='MIT',
    author_email='dreamusaha@gmail.com',
    description= 'This is a library that contain rice detection tools and other geospatial tools for jupyter environment on https://sphere.gistda.or.th/ in part of Data Cube',
    long_description= DESC,
    author='Pathakorn Usaha',
    url= 'https://github.com/Pathakorn40/rice-detection',
    download_url= 'https://pypi.org/project/dream_river/',
    keywords= ['geography','geospatiol','gis', 'rice detection'],
    install_requires= ['datacube','shapely','xarray','matplotlib','numpy','geopandas','dea_tools','sklearn',
                'pydotplus','subprocess','odc','flusstools','skimage','gdal','scipy','math','folium','json','odc.ui','os','odc.io'],
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

