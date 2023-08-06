#skin temperature image functions for Drought Observatory platform
# input: year, month and day of the image to be retrieved from ERA5 CDS.
# output: return code - 0 OK
import cdsapi 
import rioxarray
import numpy as np
import xarray as xr
import requests
import os
import sqlalchemy as db
import logging

def get_n_save(year_in: int, month_in: int,basepath: str , days_in) -> int:
   
    c = cdsapi.Client()
    try:
        list_of_days = list(filter(lambda x: isinstance(x,str), days_in))
        myurl = 'https://droughtsdi.fi.ibimet.cnr.it/dgws3/api/upload/skin_temp'
        print(year_in)
        print(list_of_days)
        #Effettuo un ciclo per tutti i mesi dell'anno
    
        data = c.retrieve('reanalysis-era5-land',
            {
                'product_type': 'reanalysis',
                'variable': 'skin_temperature',   #per il dewpoint e' 2m_dewpoint_temperature
                'year': str(year_in),
                'format': 'netcdf',
                'month': str(month_in),
                'day': list_of_days,
                'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
                        ],
                    'area': [
                        70, -13, 20, 40,
                        ],  
            },
            basepath+'/skintemp_'+str(year_in)+'_'+str(month_in)+'.nc')    
        
        print('open nc file')
        nc_file = basepath+'/skintemp_'+str(year_in)+'_'+str(month_in)+'.nc'
        print('Loading dataset')
        ds = xr.open_dataset(nc_file).load()

        print('Calculate daily temperature and transform in Celsius')
        daily_data = ds.resample(time='d').mean()
        daily_data_celsius = daily_data.skt - 273.15

        print('Start cube elaboration')
        #always skip last retrieved day cause it could be incomplete
        for i in range((len(daily_data_celsius) - 1)):
            dout = daily_data_celsius[i,:,:]
            dout.rio.write_crs("EPSG:4326", inplace=True).rio.to_raster(nc_file+'_out_'+str((i+1))+'.tiff')
            #set file and form data for post call

            files_in = {
                'file': (nc_file+'_out_'+str((i+1))+'.tiff', open(nc_file+'_out_'+str((i+1))+'.tiff', 'rb'),'multipart/form-data'),
                'year': str(year_in),
                'month': str(month_in),
                'day': str((i+1))
            }
        
            #call rest api
            response = requests.post(myurl, files=files_in)
        
            print(response.content)
            dout.close()
            #delete tiff image
            print("remove "+nc_file+'_out_'+str((i+1))+'.tiff')
            os.remove(nc_file+'_out_'+str((i+1))+'.tiff')
        daily_data_celsius.close()
        daily_data.close()
            
        ds.close()
      
        #delete nc file
        print("remove "+nc_file)
        os.remove(nc_file)
        return 0
    except Exception as e:
        logging.error(e)
        return 1
    

def get_last_day(connect_str: str) -> int:
    retval = -1
    engine = db.create_engine(connect_str,future=True)
    connection = engine.connect()
    metadata = db.MetaData()
    try:
        sql = db.text("select max(dtime) from postgis.acquisizioni inner join postgis.skin_temperature using (id_acquisizione)")

        ResultProxy = connection.execute(sql).fetchall()
        
        for row in ResultProxy:
            retval = row     

        connection.close()
        return retval
    except:
        connection.close()
        return -1
    
def del_image(connect_str: str, dtime_from: str, dtime_to: str) -> int:
    retval = -1
    print(connect_str)
    engine = db.create_engine(connect_str,future=True)
    connection = engine.connect()
    metadata = db.MetaData()
    try:
     

        sql = db.text("delete from postgis.skin_temperature where id_acquisizione in (select id_acquisizione from postgis.acquisizioni inner join postgis.imgtypes using (id_imgtype) where imgtype = 'SKINTEMP' and dtime between '"+dtime_from+"'::timestamp and '"+dtime_to+"'::timestamp)")

        connection.execute(sql)
        
        connection.commit() 

        connection.close()
        return retval
    except Exception as es:
        logging.error(es)
        connection.rollback()
        connection.close()
        return -1

        