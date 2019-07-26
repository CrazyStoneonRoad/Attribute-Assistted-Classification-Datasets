#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# -----------------------------------------
#
# Authorized by Zhang Yuanlin from
# the Key Laboratory of Spectral Imaging Technology CAS,
# Xi'an Institute of Optics and Precision Mechanics,
# Chinese Academy of Sciences, Xi'an 710119, China.
#
# -----------------------------------------
# Convert the caption labels in dataset.json, 
# to attribute.json using selected attributes in Dict.txt.

import os,json,sys,re
print(sys.argv)

# read json
txtpth = './Dict.txt'
if len(sys.argv)>1:
    path = sys.argv[1]
else:
    path = './dataset.json'

root = json.load(open(path,'r'))

# list of attributes
with open('./Dict.txt','r') as f:
    lns = f.readlines()
Attr = [wd.strip() for wd in lns]

Labels = {}
for img in root['images']:
    # prepare a word list of an image
    List = [wd for sent in img['sentences'] for wd in sent['tokens']]
    List = list(set(List))
    # label of an image
    lbl = ['1' if atr in List else '0'   for atr in Attr]
    lbl = ''.join(lbl)
    assert len(lbl)==len(Attr)
    # update Lables
    Labels.update({img['filename']:lbl})

# Labels divided by class
# --------------------------
# for AID dataset
# 
# airport_1 in airport folder
# --------------------------
# KeyS = [re.sub(r'_.*$','',lbl) for lbl in Labels ]
# KeyS = list(set(KeyS))
# Lblsdbcls={Key:{} for Key in KeyS}
# for lbl in Labels:
    # Key = re.sub(r'_.*$','',lbl)
    # Lblsdbcls[Key].update( {lbl:Labels[lbl]} )


# Labels divided by class
# --------------------------
# for UCM dataset
# 
# caption dataset:
# 100 continuous images are of the same class
# the class names correspondingly ranged by their initials
# 
# classification dataset:
# categoryN.tif
# --------------------------
KeyS = ['agricultural','airplane','baseballdiamond','beach','buildings','chaparral','denseresidential','forest','freeway','golfcourse','harbor','intersection','mediumresidential','mobilehomepark','overpass','parkinglot','river','runway','sparseresidential','storagetanks','tenniscourt']
Lblsdbcls={Key:{} for Key in KeyS}
for lbl in Labels:
    clsid = int( (int(lbl[:-4])-1) /100)
    Key = KeyS[clsid]
    n = int( re.findall(r'^\d+(?=\.tif)',lbl)[0] )
    lbl__ = '{}{:0>2d}.tif'.format(Key,(n-1)%100)
    Lblsdbcls[Key].update( {lbl__:Labels[lbl]} )

# write
with open('./Attributes.json','w') as f:
    json.dump(Lblsdbcls,f)
