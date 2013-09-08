# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import filters
import webapp2
from webapp2 import Route


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

routes = [
    #Route('/', handler='handlers.PageHandler:root', name='pages-root'),
    #Route('/test-string', handler='handlers.PageHandler:test_string', name='pages-test-string'),

    Route('/', handler='handlers.PageHandler:root', name='pages-root'),
    Route('/authenticate', handler='handlers.PageHandler:authenticate', name='pages-authenticate'),
    Route('/register', handler='handlers.PageHandler:register', name='pages-register'),
    Route('/adduser', handler='handlers.PageHandler:adduser', name='pages-adduser'),
    Route('/addbusiness', handler='handlers.PageHandler:addbusiness', name='pages-addbusiness'),
    Route('/feedme', handler='handlers.PageHandler:feedme', name='pages-feedme'),
    Route('/business', handler='handlers.PageHandler:business', name='pages-business'),
		Route('/populate', handler='handlers.PageHandler:populate', name='pages-populate'),
		Route('/locate', handler='handlers.PageHandler:locate', name='pages-locate'),
		Route('/contact', handler='handlers.PageHandler:contact', name='pages-contact'),
		Route('/orderML', handler='handlers.PageHandler:orderML', name='pages-orderML'),
		Route('/webhook', handler='handlers.PageHandler:webhook', name='pages-webhook')
    ]

config = {
    'webapp2_extras.jinja2': {
        'template_path': 'template_files',
        'filters': {
            'timesince': filters.timesince,
            'datetimeformat': filters.datetimeformat,
        },
    },
}


application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
