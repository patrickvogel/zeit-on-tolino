import os
import schedule
import time
from zeitOnTolino import ZeitOnTolino

scheduling = os.getenv("SCHEDULING", 'True').lower() in ['true', '1']

zot = ZeitOnTolino()

def sync():
    zot.syncTolinoCloudWithLatestZeitEditions()

schedule.every().wednesday.at("17:00").do(sync)
schedule.every().wednesday.at("18:00").do(sync)
schedule.every().wednesday.at("19:00").do(sync)
schedule.every().wednesday.at("20:00").do(sync)

# Initial sync
sync()

# Start scheduled syncs
if scheduling:
    while 1:
        schedule.run_pending()
        time.sleep(1)