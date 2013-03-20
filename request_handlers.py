import os
import sys
import redis
import json
import logging

from tornado.web import RequestHandler, asynchronous
from tornado import httpclient, gen

redis_url  = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_pool = redis.from_url(redis_url)

log = logging.getLogger('tornado.general')

class MainHandler(RequestHandler):
    @asynchronous
    @gen.engine
    def post(self, game_name):
        """
        Get the json data and send it to apple to be verified
        """
        content = json.loads(self.request.body)
        
        header  = {'Content-Type' : 'application/json'}
        
        self.finish()
        
    def get(self, game_name):
        """
        Display Analytics for a specific game
        """
        self.write(json.dumps(redis_pool.zrange(game_name.lower(), 0, 20, desc=True, withscores=True)))
        
        
class StatusCheckHandler(RequestHandler):
    """
    Request Handler for new relic to ping and check that the site is up
    """
    def get(self):
        self.set_status(200)
        self.write('online')
        
    def head(self):
        self.set_status(200)