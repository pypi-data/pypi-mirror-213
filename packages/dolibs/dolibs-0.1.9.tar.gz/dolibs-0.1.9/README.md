# This project contains a package of utilities for downloading and, managing ERA5 data and storing them into local database of Drought Observatory platform (https://drought.climateservices.it/en/)

# package dolibs - **Drought Observatory Library**
## skintemp module: functions for retrieving and manipulating skin temperature data from ERA5 Copernicus

## supplied functions for skin temperature module:
### `get_n_save(year_in: int, month_in: int,basepath: str , days_in)` 
### retrieve data from Copernicus hub for given year, month and the list of days. the basepath contains workspace directory used for temporary data storage and manipulation
### 
### **Example:**
### `from dolibs import skintemp as sk`
### `def test_skintemp():`
###    `assert sk.get_n_save(1990,1,'/tmp/pytmp',['01'])` 


### `del_image(connect_str: str, dtime_from: str, dtime_to: str)` 
### delete old images from Drought Observatory database with given connect string and dates defining interval
### 
### **Example:**
### `from dolibs import skintemp as sk`
### `def test_del_skintemp():`
###    `assert sk.del_image('connection string to db','2023-01-01','2023-02-01')` 