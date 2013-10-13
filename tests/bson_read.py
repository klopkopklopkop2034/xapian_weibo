# -*- coding: utf-8 -*-

import time
import csv
import json
import sys
import re
from datetime import datetime
from datetime import date
from bs_input import KeyValueBSONInput
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring

BSON_FILEPATH = "/opt/backup/mongodump/20130129/master_timeline/master_timeline_weibo.bson"

def load_bs(bs_filepath=BSON_FILEPATH):
    print 'bson file mode: 从备份的BSON文件中 %s 加载数据' % (bs_filepath)
    bs_input = KeyValueBSONInput(open(bs_filepath, 'rb'))
    return bs_input

def load_weibo_from_bs():
    bs_input = load_bs()
    count = 0
    #hit_count = 0
    #json_data = []
    f = open('jsonTOXML.xml', 'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>'+'\n'+'<statuses>')
    
    for _id, weibo in bs_input.reads():
        id = _id
        created_at = weibo['created_at']
        text = weibo['text']
        source = weibo['source']
        reposts_count = weibo['reposts_count']
        comments_count = weibo['comments_count']
        attitudes_count = weibo['attitudes_count']
        geo = weibo['geo']

        try:
            user = weibo['user']
            #print 'there is user'
        except KeyError:
            continue
        u_id = user['id']
        u_name = user['name']
        u_gender = user['gender']
        u_province = user['province']
        u_city = user['city']
        u_location = user['location']
        try:
            u_description = user['description']
        except KeyError:
            continue
        u_verified = user['verified']
        u_followers_count = user['followers_count']
        u_statuses_count = user['statuses_count']
        u_friends_count = user['friends_count']
        u_profile_image_url = user['profile_image_url']
        u_bi_followers_count = user['bi_followers_count']
        try:
            u_verified_type = user['verified_type']
        except KeyError:
            continue

        count = count + 1
        print count
        if count <= 100:
            xml_data = ElementTree()
            root = Element('status')
            xml_data._setroot(root)

            id_data = Element('id')
            id_data.text = str(id)
            root.append(id_data)

            created_at_data = Element('created_at')
            created_at_data.text = created_at
            root.append(created_at_data)

            text_data = Element('text')
            text_data.text = text
            root.append(text_data)

            source_data = Element('source')
            source_data.text = source
            root.append(source_data)

            reposts_count_data = Element('reposts_count')
            reposts_count_data.text = str(reposts_count)
            root.append(reposts_count_data)

            comments_count_data = Element('comments_count')
            comments_count_data.text = str(comments_count)
            root.append(comments_count_data)

            attitudes_count_data = Element('attitudes_count')
            attitudes_count_data.text = str(attitudes_count)
            root.append(attitudes_count_data)

            geo_data = Element('geo')
            geo_data.text = geo
            root.append(geo_data)

            user_data = Element('user')            
            root.append(user_data)
            SubElement(user_data, 'u_id').text = str(u_id)
            SubElement(user_data, 'u_name').text = u_name
            SubElement(user_data, 'u_gender').text = str(u_gender)
            SubElement(user_data, 'u_province').text = u_province
            SubElement(user_data, 'u_city').text = u_city
            SubElement(user_data, 'u_location').text = u_location
            SubElement(user_data, 'u_description').text = u_description
            SubElement(user_data, 'u_verified').text = str(u_verified)
            SubElement(user_data, 'u_followers_count').text = str(u_followers_count)
            SubElement(user_data, 'u_statuses_count').text = str(u_statuses_count)
            SubElement(user_data, 'u_friends_count').text = str(u_friends_count)
            SubElement(user_data, 'u_profile_image_url').text = str(u_profile_image_url)
            SubElement(user_data, 'u_bi_followers_count').text = str(u_bi_followers_count)
            SubElement(user_data, 'u_verified_type').text = str(u_verified_type)

            xml_data.write(f, 'utf-8')
            f.write('\n')
        else:
            break
    f.write('\n'+'</statuses>')
    f.close()


if __name__ == '__main__':
    load_weibo_from_bs()
        
