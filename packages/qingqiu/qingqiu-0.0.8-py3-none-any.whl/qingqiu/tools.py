# -*- coding: UTF-8 -*-

import base64
from datetime import datetime,timedelta
import hashlib
import inspect
import json
import os
try:
    import json_tools
except:
    pass

import urllib.parse

backup={'lastTime':None}

class tools:
    @staticmethod
    def md5(val: str) -> str:
        return hashlib.md5(str(val).encode('utf-8')).hexdigest()

    @staticmethod
    def time2Stamp(timeFormat=None, returnType='int', ms=False,days=0,hours=0,minutes=0,seconds=0,dayStart=False,dayEnd=False,lastTime=False):
        '''
        timeFormat='2013-10-10 23:40:00' 
        None:当前
        ret 'int' 'str'
        ms 是否毫秒级
        '''
        to=datetime.now()
        if lastTime:
            if backup['lastTime'] is not None:
                to=backup['lastTime']
        if timeFormat is not None and isinstance(timeFormat,str):
            to=datetime.strptime(timeFormat.strip(),"%Y-%m-%d %H:%M:%S")
        if dayStart:
            to=to.replace(hour=0,minute=0,second=0,microsecond=0)
        if dayEnd:
            to=to.replace(hour=23,minute=59,second=59,microsecond=0)
        to=to+timedelta(days=days,minutes=minutes,hours=hours,seconds=seconds)
        backup['lastTime']=to
        timeStamp=to.timestamp()
        if ms:
            timeStamp = timeStamp*1000
        timeStamp=int(to.timestamp())
        if returnType == 'str':
            return str(timeStamp)
        return timeStamp

    @staticmethod
    def timeFormat(ts:int=None):
        if ts is None:
            return str(datetime.now())
        else:
            return str(datetime.fromtimestamp(ts))

    @staticmethod
    def showJson(data):
        if isinstance(data,dict) or isinstance(data,list):
            return json.dumps(
                    data, ensure_ascii=False, indent=4)
        elif isinstance(data,str):
            try:
                return json.dumps(
                        json.loads(data), ensure_ascii=False, indent=4)
            except:
                return data
        else:
            return str(data)

    @staticmethod
    def desc(default=None,*l,**k):
        '''
        只用于备注，无逻辑
        '''
        return default

    @staticmethod
    def diff(a,b,printable=False,ig=None):
        '''
        a dict
        b dict
        printable bool 是否打印不一致的地方
        ig  str add/replace/...:keyname
        '''
        try:
            val= json_tools.diff(a,b)
            if printable:
                iggname=""
                iggval=""
                if ig is not None:
                    iggname=str(ig).split(':')[0]
                    iggval=str(ig).split(':')[1]
                for x in val:
                    if iggname!='' and iggname in x:
                        if str(x[iggname]).endswith(iggval):
                            continue
                    print(x)
            return val
        except :
            print('如果没安装json_tools，请使用pip install json_tools')
    


    @staticmethod
    def base64encode(val: str or bytes, return_str=True, encode='utf8') -> str or bytes:
        tmpVal = b'unknown'
        if isinstance(val, bytes):
            tmpVal = val
        else:
            tmpVal = str(val).encode(encoding=encode)
        tmpBytes = base64.b64encode(tmpVal)
        if return_str:
            return tmpBytes.decode(encoding=encode)
        else:
            return tmpBytes

    @staticmethod
    def base64decode(val: str, return_str=True, encode='utf8') -> str or bytes:
        tmpBytes=base64.b64decode(val.encode(encode))
        if return_str:
            return tmpBytes.decode(encoding=encode)
        else:
            return tmpBytes

    @staticmethod
    def urlEncode(val: str) -> str:
        return urllib.parse.quote(str(val))

    @staticmethod
    def urlDecode(val: str) -> str:
        return urllib.parse.unquote(str(val))

    @staticmethod
    def getfile():
        print(inspect.stack()[1][1])
        # inspect.stack()[1][1].f_code.co_filename
        return os.path.basename(inspect.stack()[1][1])
    