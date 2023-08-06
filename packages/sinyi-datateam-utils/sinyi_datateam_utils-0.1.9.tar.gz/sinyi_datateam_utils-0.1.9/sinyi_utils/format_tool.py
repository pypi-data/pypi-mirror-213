import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import requests


def roc_era_to_ad(roc_era):
    roc_era = roc_era.replace('-',"").replace(" ","").replace('_',"")
    if roc_era: 
        if len(roc_era) == 6 or len(roc_era) == 7 :
            year = roc_era[:-4]
            year = str(int(year)+1911)
            return year+roc_era[-4:]
        else:
            return None

class AESCrypto:
    def __init__(self, secrect_key, secrect_iv):
        self.key = secrect_key.encode("utf8")
        self.iv =  secrect_iv.encode("utf8")
    def decrypt(self, text:str)-> str:
        # decrypt text
        if text:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

            decryptByts = base64.b64decode(text)
            msg = cipher.decrypt(decryptByts)
            paddingLen = msg[len(msg)-1]
        else:
            return None
        
        return msg[0:-paddingLen].decode('utf8')

    def encrypt(self,text:str):
        cipher = AES.new(self.key, AES.MODE_CBC,self.iv)
        
        text = pad(text.encode('utf-8'), AES.block_size)

        msg = cipher.encrypt(text)
        msg = base64.b64encode(msg)

        return msg.decode('utf8')

class Road8:
    def __init__(self, api_key, host):
        self.road8_api_key = api_key
        self.url =  host

    def normalize(self, address = None):
        address = address.replace('\u3000','')
        normalize_url = self.url + '/Api/Normalization'
        params = {'key': self.road8_api_key, 
                'zip': 'zip33', 
                'update': 0,
                'exist': 1,
                'locate':1,
                'addr' : address}
        error_json={
             'source_address': address,
             'standard_address': '',
             'update_address': '',
             'exists_address': '',
             'addrno': 0,
             'location': {'match_type': '無法定位',
                          'crs': 'EPSG:3826',
                          'x': 0,
                          'y': 0,
                          'lat': 0,
                          'lng': 0,
                          'level': 0 }
             }
        success = True
        retry = 0
        
        while success:
            assert retry < 10, 'Retry Road8 over 10 times, please contact service provider'
            try:
                response = requests.get(normalize_url, params=params, timeout=10)   
            except:
                print('starting retry, response is timeout')
                retry += 1
            else:  
                if response.status_code == 200 :
                    
                    if 'Message' in response.json() :
                        js = response.json()
                        
                        if js['Message']== 'key 不存在或已達限額.':
                            print('Error, response: ',response.json(), ', address: ',address )
                            retry += 1
                        else:
                            print('Error, response: ',response.json(), ', address is null or other condition')
                            return error_json
                    else:
                        success = False
                        return response.json() 
                else:
                    print(f'{address} can not be normalized, status code', response.status_code)
                    return error_json
            
            
                
                
                
                