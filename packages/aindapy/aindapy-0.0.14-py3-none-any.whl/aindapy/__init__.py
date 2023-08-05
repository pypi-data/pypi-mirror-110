from datetime import datetime
import requests
import json
import numpy as np
import os
import datetime
from PIL import Image
from . import settings
from . import log
from . import pbar


def main():
    """Entry point for the application script"""
    print("Call your main application code here")


def config(logLevel: int = 0):
    """Config the api endpoint. 
    Sample: 
        apiUrl='https://aindaanalytics.com/ainda/api/' """
    settings.init(logLevel=logLevel)


class Auth:
    def __init__(self, apiUrl: str = None, userName: str = None, passWord: str = None):
        if(apiUrl == None):
            log.error('You need to set a valid apiUrl', apiUrl)
        if(userName == None):
            log.error('You need to set a valid userName', userName)
        if(passWord == None):
            log.error('You need to set a valid dataSource', passWord)

        self.apiUrl = apiUrl
        self.userName = userName
        log.info("api call: {}login".format(self.apiUrl))
        response = requests.post(
            self.apiUrl + "login", data={'email': userName, 'password': passWord})
        if response.status_code == 200:
            log.debug('api call ok')
            data = response.json()
            self.token = data["token"]
            self.user = data
        else:
            log.error('Username or Password Invalid', response.text)


class DataSource:
    def __init__(self, auth: Auth, dataWareHouseName: str = None, dataSourceName: str = None, dataWareHouseId: int = None, dataSourceId: int = None):
        self.auth = auth

        if(dataWareHouseName != None):
            if(dataSourceName == None):
                log.error('You need to set a valid dataSourceName',
                          dataSourceName)
            self.dataWareHouseName = dataWareHouseName
            self.dataSourceName = dataSourceName
            # log.info("api call: {}datasource/get".format(self.auth.apiUrl))
            # response = requests.post(
            #     "{}datasource/get".format(self.auth.apiUrl),
            #     headers={'Authorization': 'Bearer {}'.format(
            #         self.auth.token)},
            #     data=payload
            # )

            # if response.status_code != 200:
            #     log.debug('Unable to upload data to api!', response)

            # asset = json.loads(response.text)
            # log.debug('api call ok', asset)
            log.info(
                'The datataware will be set as the default demo datasource because this function by name is not done yet')
            self.dataWareHouseId = 8
            self.dataSourceId = 37
        elif(dataWareHouseId != None):
            if(dataSourceId == None):
                log.error('You need to set a valid dataSourceId', dataSourceId)
            self.dataWareHouseId = dataWareHouseId
            self.dataSourceId = dataSourceId
        else:
            log.error('Problem setting data source')


class Tag:
    def __init__(self, auth: Auth = None, tagPath: str = None, tagId: int = None, tagTypeId: int = 1,):
        self.auth = auth
        if(tagPath != None):
            log.info("api call: {}tags/findOrRegister".format(self.auth.apiUrl))
            response = requests.post(
                "{}tags/findOrRegister".format(self.auth.apiUrl),
                headers={'Authorization': 'Bearer {}'.format(
                    self.auth.token)},
                json={
                    "type": tagTypeId,
                    "path": tagPath
                }
            )
            if response.status_code == 200:
                log.debug('api call ok', response.json())
            else:
                log.error('Error finding or registering tag', response.text)
            self.id = int(response.json()['id'])
        elif(tagId != None):
            self.id = tagId
        else:
            self.id = None

        self.typeId = tagTypeId


class Data:
    def __init__(self, auth: Auth, dataSource: DataSource = None, autoCommit: bool = False, bufferSize: int = 10000):
        if(dataSource == None):
            log.error('You need to set a valid dataSource', dataSource)

        self.auth = auth
        self.bufferSize = bufferSize
        self.dataSource = dataSource
        self.autoCommit = autoCommit
        self.dataBuffer = []
        self.dataBufferUniqueKeys = []

    def commit(self):
        """Sends all data stored in buffer by the function addToBuffer to the cloud in batches of 10000 records if exceeds this limit"""
        global data

        data = []
        totalSent = 0
        if(len(self.dataBuffer) > 0):
            pbar.printProgressBar(0, len(self.dataBuffer),
                                  prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
            for row in self.dataBuffer:
                data.append(row)
                totalSent = totalSent + 1
                if(len(data) >= self.bufferSize):
                    self.__commitToApi(data)
                    pbar.printProgressBar(totalSent, len(
                        self.dataBuffer), prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
                    data = []

            if(len(data) > 0):
                self.__commitToApi(data)
                pbar.printProgressBar(totalSent, len(self.dataBuffer),
                                      prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
        else:
            log.warning("Buffer is empty. No data to be commit to api")

        self.clearBuffer()

    def deleteDataKeys(self, datakeys: list):
        """Delete from our datawarehouse the data for the datakeys specify on the list. sample:
            deleteDataKeys(['project/graphic1', 'project/graphic2'])
        """

        if(not all(datakeys)):
            log.error(
                'List of datakeys can not contain items empty or null', datakeys)

        payload = {
            'data_warehouse_id': self.dataSource.dataWareHouseId,
            'datakeys': datakeys
        }

        log.info("api call: {}datasource/graphics/delete".format(self.auth.apiUrl))
        response = requests.delete(
            "{}datasource/graphics/delete".format(self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            json=payload
        )

        if response.status_code != 200:
            log.error('Unable to upload data to api!', response.text)

    def __checkIfDataKeyExistsInDataWareHouse(self, datakey: str):
        log.info(
            "api call: {}datasource/graphics/datakey/exists".format(self.auth.apiUrl))
        response = requests.post(
            "{}datasource/graphics/datakey/exists".format(
                self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            json={
                'data_warehouse_id': self.dataSource.dataWareHouseId,
                'datakey': datakey
            }
        )

        if response.status_code != 200:
            log.error('Unable to upload data to api!', response)
        else:
            data = response.json()
            return bool(data['datakey'])

    def getBuffer(self):
        """Return the list of data added to the buffer by the function addToBuffer"""
        return self.dataBuffer

    def clearBuffer(self):
        """Clear all data added to the buffer with function addToBuffer"""
        self.dataBuffer = []
        #self.dataBufferUniqueKeys = []

    def __getNextStepFor(self, datakey: str):
        total = 0
        for row in self.dataBuffer:
            if(row['datakey'] == datakey):
                total = total + 1

        total = total + 1
        return total

    def addToBuffer(self, dataKey: str = None, value: float = None, step: str = None):
        """Add Data to the buffer to be send to the cloud"""

        if(dataKey == '' or dataKey == None):
            log.error("Error adding to buffer. DataKey can not be null or empty")
            return

        if(value == '' or value == None):
            log.warning(
                "We will not add this to buffer. Value for {} is null/empty".format(dataKey))
            return

        if(dataKey not in self.dataBufferUniqueKeys):
            if(self.__checkIfDataKeyExistsInDataWareHouse(dataKey)):
                log.error(
                    "Datakey: ({}) already exists inside the datawarehouse. Please delete it first or choose another name".format(dataKey))
            self.dataBufferUniqueKeys.append(dataKey)

        if(step != None):
            self.dataBuffer.append({
                'datakey': dataKey,
                'value': value,
                'step': step
            })
        else:
            self.dataBuffer.append({
                'datakey': dataKey,
                'value': value,
                'step': self.__getNextStepFor(dataKey)
            })

        if(self.autoCommit):
            self.__commitToApi(self.dataBuffer)
            self.clearBuffer()

    def __commitToApi(self, data):
        log.info(
            "api call: {}datasource/graphics/register".format(self.auth.apiUrl))
        response = requests.post(
            "{}datasource/graphics/register".format(self.auth.apiUrl),
            headers={
                # 'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.auth.token),
                # 'Accept': 'application/json'
            },
            json={
                'data_warehouse_id': self.dataSource.dataWareHouseId,
                'data': data
            }
        )
        if response.status_code != 200:
            log.debug('Unable to upload data to api!', response.text)


class SensorTag:

    def __init__(self, auth: Auth = None, dataSource: DataSource = None, channel: int = 1, datatag: str = None, tag: str = None, tag_unit: str = '', tag_updaterate: int = 1000):
        self.auth = auth
        self.dataSource = dataSource
        log.info(
            "api call: {}datawarehouse/tags/findOrRegister".format(self.auth.apiUrl))
        response = requests.post(
            "{}datawarehouse/tags/findOrRegister".format(
                self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            json={
                "datawarehouse_id": dataSource.dataWareHouseId,
                "channel": channel,
                "datatag": datatag,
                "tag": tag,
                "tag_unit": tag_unit,
                "tag_updaterateinms": tag_updaterate
            }
        )
        if response.status_code == 200:
            log.debug('api call ok', response.json())

            data = response.json()
            self.id = data['id']
            self.channel = int(data['channel'])
            self.datatag = data['datatag']
            self.tag = data['tag']
            self.tag_unit = data['tag_unit']
            self.tag_updaterateinms = int(data['tag_updaterateinms'])
        else:
            log.error('Error finding or registering tag', response.text)


class DataTimeSeries:
    def __init__(self, auth: Auth, dataSource: DataSource = None, autoCommit: bool = False, bufferSize: int = 10000):
        if(dataSource == None):
            log.error('You need to set a valid dataSource', dataSource)

        self.auth = auth
        self.bufferSize = bufferSize
        self.dataSource = dataSource
        self.autoCommit = autoCommit
        self.dataBuffer = []
        self.dataBufferUniqueKeys = []

    def commit(self):
        """Sends all data stored in buffer by the function addToBuffer to the cloud in batches of 10000 records if exceeds this limit"""
        global data

        data = []
        totalSent = 0
        if(len(self.dataBuffer) > 0):
            pbar.printProgressBar(0, len(self.dataBuffer),
                                  prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
            for row in self.dataBuffer:
                data.append(row)
                totalSent = totalSent + 1
                if(len(data) >= self.bufferSize):
                    self.__commitToApi(data)
                    pbar.printProgressBar(totalSent, len(
                        self.dataBuffer), prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
                    data = []

            if(len(data) > 0):
                self.__commitToApi(data)
                pbar.printProgressBar(totalSent, len(self.dataBuffer),
                                      prefix='Progress:', suffix='Complete', length=50, printEnd='\r\n')
        else:
            log.warning("Buffer is empty. No data to be commit to api")
        self.clearBuffer()

    def getBuffer(self):
        """Return the list of data added to the buffer by the function addToBuffer"""
        return self.dataBuffer

    def clearBuffer(self):
        """Clear all data added to the buffer with function addToBuffer"""
        self.dataBuffer = []

    def addToBuffer(self, sensorTagId: int = None, sensorTag: SensorTag = None, timeStamp: datetime = None, value: float = None, value1: float = None, value2: float = None):
        """Add Data to the buffer to be send to the cloud"""

        if(sensorTagId == None and sensorTag == None):
            log.error(
                "Error adding to buffer. tag or tagId can not be null or empty")
            return
        if(value == '' or value == None):
            log.error("Error adding to buffer. value can not be null or empty")
            return

        if(timeStamp == None):
            timeStamp = datetime.datetime.now()

        if(sensorTagId != None):
            self.dataBuffer.append({
                'created_at': timeStamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                'tag_id': sensorTagId,
                'value1': value
            })
        else:
            self.dataBuffer.append({
                'created_at': timeStamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                'tag_id': sensorTag.id,
                'value1': value
            })

        if(self.autoCommit):
            self.__commitToApi(self.dataBuffer)
            self.clearBuffer()

    def __commitToApi(self, data):
        log.info(
            "api call: {}datawarehouse/rawdata/register".format(self.auth.apiUrl))
        response = requests.post(
            "{}datawarehouse/rawdata/register".format(self.auth.apiUrl),
            headers={
                # 'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.auth.token),
                # 'Accept': 'application/json'
            },
            json={
                'datawarehouse_id': self.dataSource.dataWareHouseId,
                'data': data
            }
        )
        if response.status_code != 200:
            log.debug('Unable to upload data to api!', response.text)


colorPalleteList = ['red', 'yellow', 'green', 'black', 'blue']


class AssetGraphicBarDataKeys:
    def __init__(self):
        self.data = []

    def add(self, columnName: str = None, displayName: str = None, isActive: bool = True, color: str = None):
        data = {}
        data['columnName'] = columnName
        data['isActive'] = isActive
        if(displayName == None):
            data['displayName'] = data['columnName']
        if(color == None):
            data['style'] = {
                "color": {
                    "value": np.random.choice(colorPalleteList)
                }
            }
        else:
            data['styles'] = {
                "color": {
                    "value": color
                }
            }
        self.data.append(data)

    def getKeys(self):
        return self.data


class Asset:

    def __init__(self, auth: Auth = None):
        if(auth == None):
            log.error('You need to set a valid auth', auth)

        self.auth = auth
        self.data = None

    def refreshAssetData(self):
        log.info(
            "api call: {}assets/get/{}".format(self.auth.apiUrl, self.data['_id']))
        response = requests.get(
            "{}assets/get/{}".format(self.auth.apiUrl, self.data['_id']),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)}
        )
        if response.status_code == 200:
            log.debug('api call ok', response.json())
            self.data = response.json()
        else:
            log.error('Error Loading asset', response.text)

    def loadAssetData(self, assetId: str = None):
        log.info("api call: {}assets/get/{}".format(self.auth.apiUrl, assetId))
        response = requests.get(
            "{}assets/get/{}".format(self.auth.apiUrl, assetId),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)}
        )
        if response.status_code == 200:
            log.debug('api call ok', response.json())
            self.data = response.json()
        else:
            log.error('Error Loading asset', response.text)

    def getData(self):
        return self.data

    def createGraphicBar(
        self,
        dataSource: DataSource = None,
        tag: Tag = None,
        name: str = None,
        dataKeys: list = None,
        axisXLabel: str = "",
        axisYLabel: str = ""
    ):
        payload = {
            'extension': 'graphicbar',
            'name': name,
            'tag_type': tag.typeId,
            'localPath': name
        }
        if(tag.id != None):
            payload['tag_root'] = tag.id

        fileContent = Image.new("RGB", (800, 1280), (255, 255, 255)).tobytes()
        files = [('file', (name, fileContent, 'image/png'))]

        log.info("api call: {}assets/uploadmultipart".format(self.auth.apiUrl))
        response = requests.post(
            "{}assets/uploadmultipart".format(self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            data=payload,
            files=files
        )

        if response.status_code != 200:
            log.debug('Unable to upload data to api!', response)
        else:
            log.debug('api call ok', response.json())

        asset = response.json()

        payload = {
            "id": asset['_id'],
            "settings": {
                "datawarehouse": {
                    "id": dataSource.dataWareHouseId,
                    "name": "Ainda Packaging Line"
                },
                "datasource": {
                    "id": dataSource.dataSourceId,
                    "name": "Graphics Data",
                    "length": 100000,
                    "from": "now-3M",
                    "to": "now"
                },
                "graphicData": {
                    "filter": {
                        "columnName": "datakey",
                        "values": dataKeys
                    },
                    "axisX": "step",
                    "axisY": "value"
                },
                "communication": {
                    "refreshRate": 0,
                    "refreshLabel": "off"
                },
                "styles": {
                    "axisX": {
                        "legend": axisXLabel
                    },
                    "axisY": {
                        "legend": axisYLabel
                    },
                    "graphicConfiguration": {
                        "groupMode": "stacked",
                        "layout": "vertical",
                        "reverse": False
                    },
                    "viewerConfiguration": {
                        "topMenu": True,
                        "bottomMenu": True,
                        "dateRange": True
                    }
                }
            }
        }

        log.info("api call: {}assets/update".format(self.auth.apiUrl))
        response = requests.put(
            "{}assets/update".format(self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            json=payload
        )
        if response.status_code != 200:
            log.debug('Unable to upload data to api!', response.text)
        else:
            log.debug('api call ok', response.json())
            self.loadAssetData(asset['_id'])

    def upload(self, path: str, tag: Tag, loadAssetAfterUpload: bool = False):
        """Upload file to the platform. TagId is the folder id where you want to send."""
        log.info("api call: {}assets/uploadmultipart".format(self.auth.apiUrl))
        fileName = os.path.basename(path)
        mimeType = os.popen("file --mime " + path +
                            " |awk {'print $2'} |sed -e 's/\;//'").read().strip('\n')
        files = [('file', (fileName, open(path, 'rb'), mimeType))]
        payload = {
            'localPath': fileName,
            'tag_type': tag.typeId
        }
        if(tag.id != None):
            payload['tag_root'] = tag.id

        log.info("api call: {}assets/uploadmultipart".format(self.auth.apiUrl))
        response = requests.post(
            "{}assets/uploadmultipart".format(self.auth.apiUrl),
            headers={'Authorization': 'Bearer {}'.format(
                self.auth.token)},
            data=payload,
            files=files
        )

        if response.status_code != 200:
            log.debug('Unable to upload data to api!', response.text)
        else:
            log.debug('api call ok', response.json())

        if(loadAssetAfterUpload):
            self.loadAssetData(response.json()['_id'])
