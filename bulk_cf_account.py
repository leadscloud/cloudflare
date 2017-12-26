#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import random
import string
import time

TIMEOUT = 30
DOMAINS = ['sparkeducationgroup.in', 'asbl-cab.org', 'callcentercollege.in', 'sjmhospital.in', 'morningwalkerindia.co.in', 'progresshighschool.co.in', 'taw.org.in', 'hotelturmot.com', 'garant-moebel-group.asia', 'southdelhidentist.co.in', 'wiremach.in', 'geoplanet.co.in', 'aitc.org.in', 'habitatcorporate.in', 'visionaviationacademy.in']
SAVE_FILE = 'cf_accounts_by_lanthy_at_20171207.txt'
HTTP_PROXY="http://192.168.10.220:1080"

def create_cf_account(email, password):
    create_url = 'https://www.cloudflare.com/api/v4/user/create'

    headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest",
        # "x-newrelic-id:": "XAUOVFRRGwcJVlRQBAA=",
        "referer": "https://www.cloudflare.com/a/sign-up",
        # ":scheme": "https",
        # ":path": "/api/v4/user/create",
        # ":method": "POST",
        # ":authority": "www.cloudflare.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    }
    s = requests.session()
    # s.proxies = {
    #     'http': 'http://127.0.0.1:8118'
    # }
    # print("requests")
    # r = s.get('http://www.google.com', timeout=TIMEOUT, proxies={'http': HTTP_PROXY})
    # print(r.headers)
    r = s.get('https://www.cloudflare.com/a/sign-up', timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    # print(r.text)

    security_token = re.search('security_token":"(.+?)"', r.text).group(1)

    params = {
      "email": email,
      "first_name": "",
      "last_name": "",
      "telephone": "",
      "country": "",
      "zipcode": "",
      "two_factor_authentication_enabled": False,
      "created_on": None,
      "modified_on": None,
      "betas": [],
      "ui_preferences": {},
      "enterprise_zone_quota": {
        "maximum": 0,
        "current": 0,
        "available": 0
      },
      "email_confirm": email,
      "password": password,
      "password_confirm": password,
      "security_token": security_token,
      "referral_code": ""
    }

    '''
    {"result":{"id":"e6ecf1375bc9f2cbda47d337032","email":"hatu2@gmail.com","username":"125b9319c8c5e99bfbe4e8142c0","first_name":null,"last_name":null,"telephone":null,"country":null,"zipcode":null,"two_factor_authentication_enabled":false,"two_factor_authentication_locked":false,"created_on":"2016-04-13T04:23:36.810824Z","modified_on":"2016-04-13T04:23:36.810824Z","organizations":null,"has_pro_zones":false,"has_business_zones":false,"has_enterprise_zones":false},"success":true,"errors":[],"messages":[]}
    '''
    r = s.post(create_url, headers=headers, data=json.dumps(params), timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    result = r.json()
    try:
        api_key = get_api_key(s)
    except Exception as e:
        api_key = None

    try:
        name_servers = get_name_servers_by_api(email, api_key)["result"]["name_servers"]
    except:
        name_servers = ["", ""]
    result['api_key'] = api_key
    result['name_servers'] = name_servers

    return result


def get_api_key(s):
    r = s.get('https://www.cloudflare.com/a/account/my-account', timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    atok = re.search('"atok":"(.+?)"', r.text).group(1)
    # print(atok)
    # to get api key
    api_headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest",
        # "x-newrelic-id:": "XAUOVFRRGwcJVlRQBAA=",
        "referer": "https://www.cloudflare.com/a/account/my-account",
        # ":scheme": "https",
        # ":path": "/api/v4/user/api_key",
        # ":method": "GET",
        # ":authority": "www.cloudflare.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "x-atok": atok
    }
    api = s.get('https://www.cloudflare.com/api/v4/user/api_key', headers=api_headers, timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    # try:
    #     names_servers = get_name_servers(s, atok)
    # except Exception as e:
    #     names_servers = ["", ""]
    if api.json()["success"] is True:
        return api.json()["result"]["api_key"]
    return False

def get_name_servers(s, atok):
    headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest",
        "x-newrelic-id:": "XAUOVFRRGwcJVlRQBAA=",
        "referer": "https://www.cloudflare.com/a/setup/sbmchina.com/scan",
        ":scheme": "https",
        ":path": "/api/v4/zones",
        ":method": "POST",
        ":authority": "www.cloudflare.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "x-atok": atok
    }
    params = {
        "name": "example.com",
        "jump_start": False,
        "status": "initializing",
        "type": "full",
        "paused": False,
        "meta": {},
        "betas": [],
        "owner": {},
        "development_mode": False,
        # "created_on": "2016-04-13T06:34:45.156Z",
        # "modified_on": None
    }
    r = s.post('https://www.cloudflare.com/api/v4/zones', headers=headers, data=json.dumps(params), timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    return r.json()["result"]["name_servers"]


def get_name_servers_by_api(email, api_key):
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "name": '{}'.format(random.choice(DOMAINS)),
        "jump_start": False
    }
    r = requests.post('https://api.cloudflare.com/client/v4/zones', headers=headers, data=json.dumps(params), timeout=TIMEOUT, proxies={'https': HTTP_PROXY})
    # print(r.text)
    return r.json()

def generate_email(length):
    import names
    def get_random_domain(domains):
        return random.choice(domains)

    def get_random_name(length):
        first_name = names.get_first_name().lower()
        last_name = names.get_last_name().lower()
        full_name = "_".join(names.get_full_name().split(" ")).lower()
        return random.choice([first_name, last_name, full_name]) + ''.join(str(random.randint(1, 10)) for i in range(length))

    domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com", "lanthy.com"]
    return get_random_name(length) + '@' + get_random_domain(domains)


def generate_password(length):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

	
def login(email, password):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "referer": "https://www.cloudflare.com/a/login",
        ":scheme": "https",
        ":path": "/a/login",
        ":method": "POST",
        ":authority": "www.cloudflare.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    }
    login_url = 'https://www.cloudflare.com/a/login'
    s = requests.session()
    r = s.get(login_url, proxies={'https': HTTP_PROXY})
    security_token = re.search('security_token":"(.+?)"', r.text).group(1)

    params = {
      "email": email,
      "password": password,
      "security_token": security_token,
    }
    r = s.post(login_url, headers=headers, data=params, allow_redirects=False, proxies={'http': HTTP_PROXY})
    if 'location' in r.headers:
        api_key = get_api_key(s)
        name_servers = get_name_servers_by_api(email, api_key)

        owner_id = name_servers["result"]["owner"]["id"]
        name_servers = "\t".join(name_servers["result"]["name_servers"])
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(email, password, name_servers, api_key, owner_id))


while True:
    email = generate_email(4)
    password = generate_password(8)
    try:
        result = create_cf_account(email, password)
        if result["success"] is True:
            item_msg = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(
                email,
                password,
                "\t".join(result["name_servers"]),
                result["api_key"],
                result["result"]["id"],
                result["result"]["username"],
                result["result"]["created_on"])
            print(item_msg)
            with open(SAVE_FILE, 'a') as myFile:
                myFile.write(item_msg + '\n')
        elif result["errors"][0]["code"] == 1111:
            print(result)
            # time.sleep(10)
            time.sleep(60 * 15)
    except Exception as e:
        print("Error: {0}".format(e))
    time.sleep(30)