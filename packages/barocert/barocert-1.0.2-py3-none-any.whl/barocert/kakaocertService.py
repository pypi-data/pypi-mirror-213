# -*- coding: utf-8 -*-
# Module for KakaocertService API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# 
# Author : linkhub dev
# Written : 2023-03-08
# Updated : 2023-06-14
# Thanks for your interest.

import json
import zlib
import base64
import hmac
import json

from io import BytesIO
from hashlib import sha256
from time import time as stime
from json import JSONEncoder
from collections import namedtuple
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

try:
    import http.client as httpclient
except ImportError:
    import httplib as httpclient

import linkhub

from .base import BarocertException
from linkhub import LinkhubException

ServiceID = 'BAROCERT'
ServiceURL = 'barocert.linkhub.co.kr'
ServiceURL_Static = 'static-barocert.linkhub.co.kr'
APIVersion = '2.0'


def __with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KakaocertService(__with_metaclass(Singleton, object)):
    IsTest = False
    IPRestrictOnOff = True
    UseStaticIP = False
    UseLocalTimeYN = True

    def __init__(self, LinkID, SecretKey, timeOut=15):
        """ 생성자.
            args
                LinkID : 링크허브에서 발급받은 LinkID
                SecretKey : 링크허브에서 발급받은 SecretKey
        """
        self.__linkID = LinkID
        self.__secretKey = SecretKey
        self.__scopes = ["partner","401","402","403","404"]
        self.__tokenCache = {}
        self.__conn = None
        self.__connectedAt = stime()
        self.__timeOut = timeOut

    def _getConn(self):
        if stime() - self.__connectedAt >= self.__timeOut or self.__conn == None:
            if self.UseStaticIP :
                self.__conn = httpclient.HTTPSConnection(ServiceURL_Static)
            else :
                self.__conn = httpclient.HTTPSConnection(ServiceURL)

            self.__connectedAt = stime()
            return self.__conn
        else:
            return self.__conn

    def _getToken(self):

        try:
            token = self.__tokenCache[self.__linkID]
        except KeyError:
            token = None

        refreshToken = True

        if token != None:
            refreshToken = token.expiration[:-5] < linkhub.getTime(self.UseStaticIP, self.UseLocalTimeYN, False)

        if refreshToken:
            try:
                token = linkhub.generateToken(self.__linkID, self.__secretKey,
                                              ServiceID, "", self.__scopes, None if self.IPRestrictOnOff else "*",
                                              self.UseStaticIP, self.UseLocalTimeYN, False)

                try:
                    del self.__tokenCache[self.__linkID]
                except KeyError:
                    pass

                self.__tokenCache[self.__linkID] = token

            except LinkhubException as LE:
                raise BarocertException(LE.code, LE.message)

        return token

    def _httpget(self, url):

        conn = self._getConn()

        headers = {"x-pb-version": APIVersion}

        headers["Authorization"] = "Bearer " + self._getToken().session_token

        headers["Accept-Encoding"] = "gzip,deflate"

        conn.request('GET', url, '', headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise BarocertException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost(self, url, postData = None):

        xDate = linkhub.getTime(self.UseStaticIP, False, False)

        signTarget = ""
        signTarget += "POST\n"
        signTarget += url +"\n"
        if postData != None and postData != "":
            signTarget += Utils.b64_sha256(postData) + "\n"
        
        signTarget += xDate + "\n"

        signature = Utils.b64_hmac_sha256(self.__secretKey, signTarget)

        conn = self._getConn()

        headers = {"x-bc-date": xDate}
        headers["x-bc-version"] = APIVersion
        headers["Authorization"] = "Bearer " + self._getToken().session_token
        headers["Content-Type"] = "application/json; charset=utf8"
        headers["Accept-Encoding"] = "gzip,deflate"
        headers["x-bc-auth"] = signature
        headers["x-bc-encryptionmode"] = "GCM"

        conn.request('POST', url, postData, headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise BarocertException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _parse(self, jsonString):
        return Utils.json2obj(jsonString)

    def _stringtify(self, obj):
        return json.dumps(obj, cls=KakaocertEncoder)
    
    def _encrypt(self, plainText):
        return Utils.AES256GCM(plainText, self.__secretKey)

 # 본인인증 요청
    def requestIdentity(self, clientCode, identity):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if identity == None or identity == "":
            raise BarocertException(-99999999, "본인인증 요청정보가 입력되지 않았습니다.")    
        if identity.receiverHP == None or identity.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if identity.receiverName == None or identity.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if identity.receiverBirthday == None or identity.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        
        if identity.reqTitle == None or identity.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        
        if identity.expireIn == None or identity.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        
        if identity.token == None or identity.token == "":
            raise BarocertException(-99999999, "토큰 원문이 입력되지 않았습니다.")
        
        postData = self._stringtify(identity)

        return self._httppost('/KAKAO/Identity/' + clientCode, postData)

    # 본인인증 상태확인
    def getIdentityStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")
        

        return self._httpget('/KAKAO/Identity/' + clientCode + '/' + receiptId )
    
    # 본인인증 검증
    def verifyIdentity(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httppost('/KAKAO/Identity/' + clientCode + '/' + receiptId )

    # 전자서명 요청(단건)
    def requestSign(self, clientCode, sign):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if sign == None or sign == "":
            raise BarocertException(-99999999, "전자서명 요청정보가 입력되지 않았습니다.")
        if sign.receiverHP == None or sign.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if sign.receiverName == None or sign.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if sign.receiverBirthday == None or sign.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        
        if sign.reqTitle == None or sign.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        
        if sign.expireIn == None or sign.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        
        if sign.token == None or sign.token == "":
            raise BarocertException(-99999999, "토큰 원문이 입력되지 않았습니다.")
        
        if sign.tokenType == None or sign.tokenType == "":
            raise BarocertException(-99999999, "원문 유형이 입력되지 않았습니다.")
        
        postData = self._stringtify(sign)

        return self._httppost('/KAKAO/Sign/' + clientCode, postData)

    # 전자서명 상태확인(단건)
    def getSignStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httpget('/KAKAO/Sign/' + clientCode + '/' + receiptId)

    # 전자서명 검증(단건)
    def verifySign(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httppost('/KAKAO/Sign/' + clientCode + '/' + receiptId)
    
    # 전자서명 요청(복수)
    def requestMultiSign(self, clientCode, multiSign):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if multiSign == None or multiSign == "":
            raise BarocertException(-99999999, "전자서명 요청정보가 입력되지 않았습니다.")
        if multiSign.receiverHP == None or multiSign.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if multiSign.receiverName == None or multiSign.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if multiSign.receiverBirthday == None or multiSign.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        
        if multiSign.reqTitle == None or multiSign.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        
        if multiSign.expireIn == None or multiSign.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        
        if self._isNullorEmptyTitle(multiSign.tokens):
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        if self._isNullorEmptyToken(multiSign.tokens):
            raise BarocertException(-99999999, "토큰 원문이 입력되지 않았습니다.")
        
        if multiSign.tokenType == None or multiSign.tokenType == "":
            raise BarocertException(-99999999, "원문 유형이 입력되지 않았습니다.")

        postData = self._stringtify(multiSign)

        return self._httppost('/KAKAO/MultiSign/' + clientCode, postData)

    # 전자서명 상태확인(복수)	
    def getMultiSignStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httpget('/KAKAO/MultiSign/' + clientCode + '/' + receiptId)


    # 전자서명 검증(복수)
    def verifyMultiSign(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")
        
        return self._httppost('/KAKAO/MultiSign/' + clientCode + '/' + receiptId)

    # 출금동의 요청
    def requestCMS(self, clientCode, cms):
        
        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if cms == None or cms == "":
            raise BarocertException(-99999999, "자동이체 출금동의 요청정보가 입력되지 않았습니다.")
        if cms.receiverHP == None or cms.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if cms.receiverName == None or cms.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if cms.receiverBirthday == None or cms.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        
        if cms.reqTitle == None or cms.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        if cms.expireIn == None or cms.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        
        if cms.requestCorp == None or cms.requestCorp == "":
            raise BarocertException(-99999999, "청구기관명이 입력되지 않았습니다.")
        if cms.bankName == None or cms.bankName == "":
            raise BarocertException(-99999999, "은행명이 입력되지 않았습니다.")
        if cms.bankAccountNum == None or cms.bankAccountNum == "":
            raise BarocertException(-99999999, "계좌번호가 입력되지 않았습니다.")
        if cms.bankAccountName == None or cms.bankAccountName == "":
            raise BarocertException(-99999999, "예금주명이 입력되지 않았습니다.")
        if cms.bankAccountBirthday == None or cms.bankAccountBirthday == "":
            raise BarocertException(-99999999, "예금주 생년월일이 입력되지 않았습니다.")
        if cms.bankServiceType == None or cms.bankServiceType == "":
            raise BarocertException(-99999999, "출금 유형이 입력되지 않았습니다.")

        postData = self._stringtify(cms)

        return self._httppost('/KAKAO/CMS/' + clientCode, postData)

    # 출금동의 상태확인
    def getCMSStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httpget('/KAKAO/CMS/' + clientCode + '/' + receiptId)

    # 출금동의 검증
    def verifyCMS(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")
        
        return self._httppost('/KAKAO/CMS/' + clientCode + '/' + receiptId)
    
    def _isNullorEmptyTitle(self, multiSignTokens):
        if multiSignTokens == None or multiSignTokens == "":
            return True
        if len(multiSignTokens) == 0:
            return True
        for multiSignToken in multiSignTokens:
            if multiSignToken.reqTitle == None or multiSignToken.reqTitle == "":
                return True
        return False
    
    def _isNullorEmptyToken(self, multiSignTokens):
        if multiSignTokens == None or multiSignTokens == "":
            return True
        if len(multiSignTokens) == 0:
            return True
        for multiSignToken in multiSignTokens:
            if multiSignToken.token == None or multiSignToken.token == "":
                return True
        return False

class KakaoCMS(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class KakaoIdentity(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        
class KakaoSign(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class KakaoMultiSign(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class KakaoMultiSignTokens(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class KakaocertEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class JsonObject(object):
    def __init__(self, dic):
        try:
            d = dic.__dict__
        except AttributeError:
            d = dic._asdict()

        self.__dict__.update(d)

    def __getattr__(self, name):
        return None

class Utils:
    @staticmethod
    def b64_sha256(input):
        return base64.b64encode(sha256(input.encode('utf-8')).digest()).decode('utf-8')

    @staticmethod
    def b64_hmac_sha256(keyString, targetString):
        return base64.b64encode(hmac.new(base64.b64decode(keyString.encode('utf-8')), targetString.encode('utf-8'), sha256).digest()).decode('utf-8').rstrip('\n')

    @staticmethod
    def _json_object_hook(d):
        return JsonObject(namedtuple('JsonObject', d.keys())(*d.values()))

    @staticmethod
    def json2obj(data):
        if (type(data) is bytes): data = data.decode('utf-8')
        return json.loads(data, object_hook=Utils._json_object_hook)

    @staticmethod
    def isGzip(response, data):
        if (response.getheader('Content-Encoding') != None and
                'gzip' in response.getheader('Content-Encoding')):
            return True
        else:
            return False

    @staticmethod
    def gzipDecomp(data):
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)

    @staticmethod
    def AES256GCM(plainText, secretKey):
        iv = get_random_bytes(12)
        cipher = AES.new(base64.b64decode(secretKey), AES.MODE_GCM, iv)
        enc, tag = cipher.encrypt_and_digest(plainText.encode('utf-8'))
        return base64.b64encode(iv + enc + tag ).decode('utf-8')