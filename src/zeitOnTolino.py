from bs4 import BeautifulSoup
import epub_meta
import logging
import os
import requests
from tolinoPython.tolinocloud import TolinoCloud
import urllib.parse

class ZeitOnTolino:

    logging.basicConfig(
        format='[%(asctime)s][%(levelname)-8s] %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    _encZeitUser = urllib.parse.quote(os.environ['ZEIT_USER'])
    _encZeitPassword = urllib.parse.quote(os.environ['ZEIT_PASSWORD'])

    _tolinoUser = os.environ['TOLINO_USER']
    _tolinoPassword = os.environ['TOLINO_PASSWORD']
    _tolinoPartner = int(os.environ['TOLINO_PARTNER'])

    _ePubsDir = '/var/epubs'
    if not os.path.exists(_ePubsDir):
        os.makedirs(_ePubsDir)

    def _readSecuredZeitWebsite(self, url):
        requestUrl = 'https://meine.zeit.de/anmelden'
        payload='email='+self._encZeitUser+'&pass='+self._encZeitPassword+'&return_url='+urllib.parse.quote(url)
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
        }
        response = requests.request('POST', requestUrl, headers=headers, data=payload)
        assert(response.status_code == 200), "Request failed ("+str(response.status_code)+")."
        return response.text

    def _getLatestEditionsDates(self):
        latestEditionsDates = []
        latestEditionsHtml = self._readSecuredZeitWebsite('https://epaper.zeit.de/abo/diezeit/')
        latestEditionsSoup = BeautifulSoup(latestEditionsHtml, features='html.parser')

        for editionLink in latestEditionsSoup.select('div.epaper-cover a'):
            editionDate = editionLink['href'][-10:]
            latestEditionsDates.append(editionDate)

        return latestEditionsDates

    def _getEPubDownloadUrlOfEdition(self, editionDate):
        editionUrl = 'https://epaper.zeit.de/abo/diezeit/'+editionDate
        editionHtml = self._readSecuredZeitWebsite(editionUrl)
        editionSoup = BeautifulSoup(editionHtml, features='html.parser')

        ePubLink = editionSoup.find("a", {"href" : lambda L: L and L.endswith('epub')})
        assert(ePubLink is not None), "Could not find ePub download link."
        ePubDownloadLink = 'https://'+self._encZeitUser+':'+self._encZeitPassword+'@'+ePubLink['href'][8:]
        
        return ePubDownloadLink

    def _downloadEditionEPub(self, url):   
        fileName = ZeitOnTolino._ePubsDir+'/'+url.rsplit('/', 1)[1]
        download = requests.get(url, allow_redirects=True)
        assert(download.status_code == 200), "Request failed ("+str(download.status_code)+")."
        newEPubFile = open(fileName, 'wb')
        newEPubFile.write(download.content)   
        newEPubFile.close()  

    def _syncLocalEPubsWithLatestZeitEditions(self):
        logging.info('Syncing local ePubs with latest ZEIT editions ...')    

        ePubFileNames = os.listdir(ZeitOnTolino._ePubsDir)
        logging.info('- Local ePubs: '+str(len(ePubFileNames))+' files found')
        
        logging.info('- Fetching latest ZEIT editions ... ')
        try:
            latestEditionsDates = self._getLatestEditionsDates()
            logging.info('  ... done.')
            for latestEditionDate in latestEditionsDates:
                logging.info('- Checking ZEIT edition '+latestEditionDate+' ... ')
                try:
                    ePubDownloadUrl = self._getEPubDownloadUrlOfEdition(latestEditionDate)
                    ePubFileName = ePubDownloadUrl.rsplit('/', 1)[1]
                    if ePubFileName not in ePubFileNames:
                        logging.info('  ... downloading '+ePubFileName+' ... ')
                        self._downloadEditionEPub(ePubDownloadUrl)
                        logging.info('  ... done.')
                    else:
                        logging.info('  ... already exists in local ePubs.')  
                except AssertionError as error:
                    logging.error('  ... an error occurred: ' + str(error))

            logging.info('... done.')  
        except:
            logging.error('  ... an error occurred: ' + str(error))

    def _getEditionsTitlesInTolinoCloud(self):
        editionsTitlesInTolinoCloud = []
        c = TolinoCloud(self._tolinoPartner)
        c.login(self._tolinoUser, self._tolinoPassword)
        c.register()
        inv = c.inventory()
        c.unregister()
        c.logout()

        for i in inv:
            if i['title'][:8] == 'DIE ZEIT':
                editionsTitlesInTolinoCloud.append(i['title'])

        return editionsTitlesInTolinoCloud

    def _uploadEditionToTolinoCloud(self, fileName):
        c = TolinoCloud(self._tolinoPartner)
        c.login(self._tolinoUser, self._tolinoPassword)
        c.register()
        document_id = c.upload(ZeitOnTolino._ePubsDir+'/'+fileName)
        c.unregister()
        c.logout()

    def _syncTolinoCloudWithLocalEpubs(self):
        logging.info('Syncing Tolino Cloud with local ZEIT ePubs ...')    

        ePubFileNames = os.listdir(ZeitOnTolino._ePubsDir)
        logging.info('- Local ePubs: '+str(len(ePubFileNames))+' files found')
        
        editionsTitlesInTolinoCloud = self._getEditionsTitlesInTolinoCloud()
        logging.info('- Tolino Cloud: '+str(len(editionsTitlesInTolinoCloud))+' files found')

        for ePubFileName in ePubFileNames:
            ePubMeta = epub_meta.get_epub_metadata(ZeitOnTolino._ePubsDir+'/'+ePubFileName)
            logging.info('- Checking "'+ePubMeta['title']+'" ... ')
            if ePubMeta['title'] not in editionsTitlesInTolinoCloud:
                logging.info('  ... uploading ...')
                self._uploadEditionToTolinoCloud(ePubFileName)
                logging.info('  ... done.')
            else:
                logging.info('  ... already synced.')    

        logging.info('... done.')  

    def syncTolinoCloudWithLatestZeitEditions(self):
        logging.info('+++ SYNC TOLINO CLOUD WITH LATEST ZEIT EDITIONS +++')
        
        self._syncLocalEPubsWithLatestZeitEditions()    
        self._syncTolinoCloudWithLocalEpubs()

        logging.info('+++ DONE +++')    

