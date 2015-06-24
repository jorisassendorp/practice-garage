""" Helper class for the params of the handler
"""
import datetime, cgi
import urllib
import logging

class ParamCollection():
    def __init__(self, request=None):
        self.params = {}
        if request:
            for k in request.arguments():
                self.params[urllib.unquote(k)] = urllib.unquote(request.get(k))

            # work around for PUT request that doesn't process the parameter correctly    
            if len(self.params) == 0 and request.method == 'PUT':
                pp = cgi.parse_qs(request.body, keep_blank_values=True)
                for p in pp:
                    value = pp[p][0]
                    if isinstance(value, str):
                        value = unicode(value, 'utf-8')
                    self.params[p] = value

    def removeEmpty(self):
        for k in self.params.keys():
            if self.params[k] == '':
                del self.params[k]

    def reset(self):
        self.params = {}

    def exists(self, param):
        if param in self.params:
            return True
        else:
            return False  
    
    def addValue(self, param, value):
        self.params[param] = value
      
    def getValue(self, param, default=None):
        if self.exists(param):
            v = self.params[param]
            if v == '':
                return default
            else:
                return v
        else:
            return default

    def hasValue(self, param):
        if self.exists(param):
            if self.getValue(param) is None:
                return False
            else:
                return True
        else:
            return False  

    # Get the values types out of the collection
    # ------------------------------------------  
    def getString(self, param, default=None):
        return self.getValue(param, default=None)
    
    def getDate(self, param, default=None):
        return ParamCollection.get_date(self.getValue(param), default)

    def getDateTime(self, param, default=None):
        return ParamCollection.get_datetime(self.getValue(param), default)

    def getDateTimeMicroSeconds(self, param, default=None):
        return ParamCollection.get_datetime_microseconds(self.getValue(param), default)

    def getTime(self, param, default=None):
        t = default
        v = self.getValue(param)
        if v is not None:
            try:
                if v in ['24:00', '24:00:00']:
                    t = datetime.time(hour=23, minute=59, second=59)
                elif len(v) == 8:
                    dt = datetime.datetime.strptime(v, '%H:%M:%S')
                    t = datetime.time(hour=dt.hour, minute=dt.minute, second=dt.second)
                else:
                    dt = datetime.datetime.strptime(v, '%H:%M')
                    t = datetime.time(hour=dt.hour, minute=dt.minute)

            except Exception, e:
                logging.warning("Time Error: %s - %s" % (v, e.message))
        
        return t   

    def getFloat(self, param, default=0.0):
        f = default
        v = self.getValue(param)
        if v is not None:
            try:
                f = float(v)
            except Exception, e:
                logging.warning("Number format Error: %s - %s" % (v, e.message))  

        return f

    def getInt(self, param, default=0):
        return ParamCollection.get_int(self.getValue(param), default)

    def getBool(self, param, default=False):
        return ParamCollection.get_bool(self.getValue(param), default)

    def getBinary(self, param):
        if self.exists(param):
            return self.params[param]
        else:
            return None
        
    @staticmethod
    def get_date(value, default=None):
        d = default
        v = value
        if v is not None:
            if isinstance(v, datetime.date) or isinstance(v, datetime.datetime):
                return v
            else:
                try:
                    if len(v) == 10:
                        dt = datetime.datetime.strptime(v,'%Y-%m-%d')
                    else:
                        # fix the date
                        i = v.find('.')
                        if i > 0: v = v[:i]
                        if v[-1] != 'Z': v += "Z"

                        dt = datetime.datetime.strptime(v,'%Y-%m-%dT%H:%M:%SZ')

                    d = datetime.date(dt.year, dt.month, dt.day)
                except Exception, e:
                    logging.warning("Date Error: %s - %s" % (v, e.message))

        return d

    @staticmethod
    def get_datetime(value, default=None):
        dt = default
        v = value
        if v is not None:
            if isinstance(v, datetime.date) or isinstance(v, datetime.datetime):
                return v

            if len(v) > 10 :
                # fix the date
                i = v.find('.')
                if i > 0: v = v[:i]
                if v[-1] != 'Z': v += "Z"

            try:
                dt = datetime.datetime.strptime(v,'%Y-%m-%dT%H:%M:%SZ')
            except Exception, e:
                logging.warning("DateTime Error: %s - %s" % (v, e.message))

        return dt

    @staticmethod
    def get_datetime_microseconds(value, default=None):
        """ Extension of get_datetime to support accuracy up to microseconds.
        This is first used by api/v1/locations/id/cont(r)acts?modified_after.
        """
        #TODO: Once this is verified to be working properly in all situations, we can merge this function with get_datetime

        dt = default
        v = value
        if v is not None:
            if isinstance(v, datetime.date) or isinstance(v, datetime.datetime):
                return v

            if len(v) > 10:
#                 # fix the date
#                 i = v.find('.')
#                 if i > 0: v = v[:i]
                if v[-1] != 'Z':
                    v += "Z"

            try:
                if len(v) > 20:
                    dt = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    dt = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except Exception, e:
                logging.warning("DateTime Error: %s - %s" % (v, e.message))

        return dt

    @staticmethod
    def get_int(value, default=0):
        i = default
        v = value
        if v is not None:
            try:
                i = int(v)
            except Exception, e:
                logging.warning("Integer Error: %s - %s" % (v, e.message))
        return i

    @staticmethod
    def get_bool(value, default=False):
        b = default
        v = value
        if v is not None:
            if v is not None and v in ['1', 'true', 'TRUE', 'True', True]:
                b = True

        return b

    @staticmethod
    def formatDate(date):
        if date:
            return date.strftime("%Y-%m-%d")
        return ''


    def removeParam(self, param):
        del self.params[param]

    def pprint(self, print_me=None):
        ''' Use this pretty printer to print dictionaries, its only available in development
            environments since it errors on production.
        '''
        import os
        if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
            from pprint import PrettyPrinter
            pp = PrettyPrinter(indent=4)
            if print_me is not None:
                logging.info('Printing given dictionary')
                pp.pprint(print_me)
            else:
                logging.info('Printing params')
                pp.pprint(self.params)