# -*- coding:utf-8 -*-
'''
@author: wulin
'''

class Comment(object):
    
    def setContentId(self, contentId):
        self.contentId = contentId
        
    def setContent(self, content):
        self.content = content
        
    def setPublicTime(self, publicTime):
        self.publicTime = publicTime
        
    def setUId(self, uid):
        self.uid = uid
    
    def setSourceInfo(self, sourceInfo):
        self.sourceInfo = sourceInfo
        
    def setReplies(self, replies):
        self.replise = replies
        
    def setLikes(self, likes):
        self.likes = likes
        
    def setMainContentId(self, mainContentId):
        self.mainContentId = mainContentId
        
    def setAtNickNameUids(self, atNickNameUids):
        self.atNickNameUids = atNickNameUids
        
    def setHot(self, hot):
        self.hot = hot
    
    def __str__(self):
        return ''

class User(object):
    
    def setUId(self, uid):
        self.uid = uid
        
    def setUName(self, uname):
        self.uname = uname
        
    def setGender(self, gender):
        self.gender = gender
        
    def setIcon(self, icon):
        self.icon = icon
        
    def setProfileUrl(self, profileUrl):
        self.profileUrl = profileUrl
        
    def setLocation(self, location):
        self.location = location
        
    def setSubAccount(self, subAccount):
        self.subAccount = subAccount
        
    def setQiYiVipInfo(self, qiyiVipInfo):
        self.qiyiVipInfo = qiyiVipInfo
        
    def setPPSVipInfo(self, ppsVipInfo):
        self.ppsVipInfo = ppsVipInfo
        
    def setVerifyInfo(self, verifyInfo):
        self.verifyInfo = verifyInfo
        
    
    
    
    
    
    
    
    
    
    
    

    
    