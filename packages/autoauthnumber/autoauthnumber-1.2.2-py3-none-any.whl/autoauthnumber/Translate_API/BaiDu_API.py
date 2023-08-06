# -*- coding: utf-8 -*-
"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
BaiDu_API.py - The core part of the Author Number Creation get translate from BaiDu.

This file is adapted from BaiDu official documents.
Copyright (C) 2022 BaiDu All Rights Reserved.

Author: Matt Belfast Brown
Creat Date: 2021-05-30
Version Date: 2023-06-10
Part Date: 2022-02-15
Version: 1.2.0
Part Version: 1.0.0

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021-2023 Matt Belfast Brown
Copyright (C) 2021-2023 MWAFU LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import random
from hashlib import md5

import requests


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def get_translate(query, app_id, app_key):
    salt = random.randint(32768, 65536)
    sign = make_md5(app_id + query + str(salt) + app_key)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': app_id, 'q': query, 'salt': salt, 'sign': sign, 'from': 'en', 'to': 'zh'}
    r = requests.post(api_url, params=payload, headers=headers)
    result = r.json()
    return result


def get_result(query, app_id, app_key):
    r = get_translate(query, app_id, app_key)
    result = r['trans_result'][0]['dst']
    return result


api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
