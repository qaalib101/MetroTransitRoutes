import requests
import os
from zipfile import ZipFile


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
transit_schedule_dir = BASE_DIR + '/transit_schedule'
r = requests.get('https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_metc/trans_transit_schedule_google_fd/csv_trans_transit_schedule_google_fd.zip')
zip_file_location = transit_schedule_dir + '/transit_schedule.zip'
open(zip_file_location, 'wb').write(r.content)
with ZipFile(zip_file_location, 'r') as zip:
    zip.extractall(transit_schedule_dir)