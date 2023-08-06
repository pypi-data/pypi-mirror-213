# -*- coding: utf-8 -*-
"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
YouDao_API.py - The core part of the Author Number Creation get translate from YouDao.

This file is adapted from YouDao official documents.
Copyright (C) 2022 YouDao All Rights Reserved.

Author: Matt Belfast Brown
Creat Date: 2021-05-30
Version Date: 2023-06-10
Part Date: 2022-02-15
Version: 1.2.2
Part Version: 1.0.0

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021-2023 Matt Belfast Brown
Copyright (C) 2021-2023 MWAFU LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import time
import uuid
from hashlib import sha256

import requests


def encrypt(sign_str):
    hash_algorithm = sha256()
    hash_algorithm.update(sign_str.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(qurey):
    if qurey is None:
        return None
    size = len(qurey)
    return qurey if size <= 20 else qurey[0:10] + str(size) + qurey[size - 10:size]


def get_translate(qurey, app_id, app_key):
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = encrypt(app_id + truncate(qurey) + salt + curtime + app_key)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'appKey': app_id, 'q': qurey, 'curtime': curtime, 'salt': salt, 'sign': sign, 'signType': 'v3',
            'from': 'en', 'to': 'zh-CHS', }
    r = requests.post(api_url, data=data, headers=headers)
    result = r.json()
    return result


def get_result(query, app_id, app_key):
    r = get_translate(query, app_id, app_key)
    result = r['translation'][0]
    return result


api_url = 'https://openapi.youdao.com/api'
