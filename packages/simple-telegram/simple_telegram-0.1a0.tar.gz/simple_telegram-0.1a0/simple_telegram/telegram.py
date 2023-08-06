#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Telegram Python API

@author: Alexis M.
@version: 0.1a
"""

import requests

class telegram():
    
    def __init__(self, token):
        self.token = token
        self.URL = f"https://api.telegram.org/bot{token}/"
    
    def sendMessage(self, message, chatid):
        """
        Send a message to the given chatid.

        Parameters
        ----------
        message : str
            Message to send.
        chatid : int
            Chat id.

        Returns
        -------
        None.

        """
            
        command_URL = self.URL+"sendMessage"
        
        payload = {
            "chat_id": chatid,
            "text": message,
            }
        
        res = requests.post(command_URL, json = payload)
        res = res.json()
        
        if not res['ok']:
            raise RuntimeError(f"Unable to send message\n\tError code: {res['error_code']}\n\tDescription: {res['description']}")
            
    def getUpdates(self):
        """
        Retrieve updates.

        Returns
        -------
        None.

        """
        
        command_URL = self.URL+"getUpdates"
        
        payload = {
            "allowed_updates": ["message"]
            }
        
        update = requests.post(command_URL, json = payload)
        self.last_update = update.json()
        
