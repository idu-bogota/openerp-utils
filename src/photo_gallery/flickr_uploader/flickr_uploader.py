# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Instituto de Desarrollo Urbano (<http://www.idu.gov.co>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import flickrapi
from time import sleep
from PIL import Image
import os

import logging
_logger = logging.getLogger(__name__)

class flickr_uploader():

    def __init__(self, key, secret, login):
        self._api_key = key
        self._api_secret = secret
        self._api_login = login
        self.flickr = flickrapi.FlickrAPI(self._api_key, self._api_secret)
        self._token = self.get_token()  #Conectar con Flickr

    def get_token(self):
        (self.token, self.frob) = self.flickr.get_token_part_one(perms='write')
        if not self.token: raw_input("Press ENTER after you have authorized the app in flickr page...")
        self.flickr.get_token_part_two((self.token, self.frob))
        _logger.info("token: {0}".format(self.token))
        _logger.info("frob: {0}".format(self.frob))
        return self.token

    def upload(self, photo, title, tag):
        im_1 = Image.open(photo)
        width, height = im_1.size
        if (width > 500):
            relacion = float(width)/float(height)
            new_width = 500
            new_height = new_width/relacion
            im_2 = im_1.resize((int(new_width),int(new_height)), Image.ANTIALIAS)
            im_2.save(photo)
        self.flickr.upload(filename=photo, title=title, tags=tag)
        #upload(photo,title, tag)
        id_fs = ''
        attempts = 0
        while(id_fs == '' and attempts < 8):
            sleep(0.5)
            _logger.info("Flickr timeout. Retrying...")
            attempts += 1
            fotosubida = self.flickr.walk(
                tag_mode='any',
                tags=tag,
                user_id = self._api_login
            )
            for fs in fotosubida:
                id_fs = fs.get("id")
                _logger.info("Flicker ID: {0}".format(id_fs))

        photos = []
        for photo in self.flickr.walk(
                    tag_mode='any',
                    tags=tag,
                    user_id = self._api_login
        ):
            #Tamano mediano c : 800,800 en el lado mas largo
            photo_url = "http://farm{0}.static.flickr.com/{1}/{2}_{3}_b.jpg".format(
                photo.get("farm"),
                photo.get("server"),
                photo.get("id"),
                photo.get("secret"),
            )
            photo_title = photo.get("title")
            photo_id = photo.get("id")

            # Por si llega a encontrar mas de una photo con el mismo tag: 
            photos.append({'url':photo_url,'id':photo_id,'title':photo_title})

        url_photo = ''
        for p in photos:
            url_photo = p['url']

        _logger.info("Photo uploaded Flickr")
        os.remove(photo)
        return url_photo
