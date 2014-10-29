# Copyright 2014 Open Connectome Project (http://openconnecto.me)
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

from celery import Celery
from django.conf import settings

import h5annasync

celery = Celery('tasks', broker='amqp://guest@localhost//')

@celery.task()
def async ( ):
  """ Write the h5py files back to database. """

  h5annasync.h5Async()
  #logger.warning ("Fetching url {}".format(url))
  #tc = tilecache.TileCache ( token, channels )
  #tc.loadData(url)
