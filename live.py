# Import the required libraries.
# ---------------------------------------------------------------------------------------------------------------------#
import requests
import time
import os
import datetime
import calendar
import sys
import pandas as pd

# ---------------------------------------------------------------------------------------------------------------------#
# LiveChat class to handle authentication and methods to access the API
# ---------------------------------------------------------------------------------------------------------------------#
class LiveChat:
    # to get and hold authentication information
    def __init__(self, livechat_username, livechat_token):
        self.livechat_url = 'https://api.livechatinc.com/'
        self.livechat_username = livechat_username
        self.livechat_token = livechat_token

    # function to access the Chats API and return the response, the default page will always be first
    # also used to paginate as well
    def chat_pull(self, date_from, page=1):
        headers = {'Accept': 'application/json', 'X-API-Version':'2'}
        livechat_endpoint = 'chats'
        url = self.livechat_url + livechat_endpoint + '?' + 'date_from=' + date_from +'&page=' + str(page)
        response = requests.get(url, auth=(self.livechat_username, self.livechat_token), headers=headers)
        return response
    
    # function to get the group data, to match names with the data in the chat pull
    def group_pull(self):
        headers = {'Accept': 'application/json', 'X-API-Version':'2'}
        livechat_endpoint = 'groups'
        url = self.livechat_url + livechat_endpoint + '?'
        response = requests.get(url, auth=(self.livechat_username, self.livechat_token), headers=headers)
        return response
    
    # function to allow the user to specify a number of days ago to pull data from
    def delta_start_time(self, daysago=1):
        return (datetime.date.today() - datetime.timedelta(days=daysago)).strftime('%Y-%m-%d')
    
    # helper function to use with pandas apply, to get visitor e-mail into a separate column
    def get_visitor_email(self, data):
            if 'email' in data:
                return data['email']
            else:
                return ''
    
    # helper function to use with pandas apply, to unpack tags from their list into a comma seperated string
    def unpack_tags(self, data):
        if data == '':
            return ''
        else:
            return ', '.join(data)
    
    # helper function to use with pandas apply, to count the number of total interactions between a rep and customer
    def get_num_interactions(self, data):
        if data == '':
            return 0
        else:
            return len(data)
    
    # helper function to use with pandas apply, to get the agent e-mail into a separate column
    def get_agent_email(self, data):
        if type(data) == list:
            if 'email' in data[0]:
                return data[0]['email']
            else:
                return ''
    
    # helper funtion to use with pandas apply, to unpack groups from a list into a comma separated string
    def unpack_groups(self,data):
        if type(data) == list:
            return ', '.join(str(group) for group in data)
        else: 
            return data
    
    # helper function to use with pandas apply, to get the duration the customer was in a queue
    def get_duration(self,data):
        if data == '':
            return 0
        else:
            return data['duration']

# ---------------------------------------------------------------------------------------------------------------------#
