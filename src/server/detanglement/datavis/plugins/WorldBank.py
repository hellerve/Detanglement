import wbpy

class WorldBank(object):
    def __init__(self):
        self.api = wbpy.IndicatorAPI()
        self.requiresFilter = True
        self.overview = self.api.get_countries()
        self.indicators = self.api.get_indicators()
        self.country_list = self._get_countries()

    def _get_countries(self):
        clist = {}
        for i in self.overview:
            clist[self.overview[i]['name']] = [self.overview[i]['name'], i]
        return clist

    def getLocations(self):
        return self.country_list

    def getIndicators(self):
        return [self.indicators[i]['name'] for i in self.indicators]

    def getDataForLocation(self, location, filt, date=(1990, 2012)):
        filters = None
        if type(filt) is list:
            for i in filt:
                for j in self.indicators:
                    if self.indicators[j]['name'] == i:
                        filters = j
                        break
        elif type(filt) is str:
            for j in self.indicators:
                if self.indicators[j]['name'] == filt:
                    filters = j
                    break
        else: raise ValueError("'filt' must be of type list or str")
        if type(location) is list:
            try:
                x = self.api.get_dataset(filters,
                        [self.country_list[i][1] for i in location],
                        date=":".join(str(i) for i in date)).as_dict()
            except ValueError as e:
                return None
        elif type(location) is str:
            try:
                x = self.api.get_dataset(filters,
                        [self.country_list[location][1]],
                        date=":".join(str(i) for i in date)).as_dict()
            except ValueError as e:
                return None
        else: raise ValueError("'location' must be of type list or str")
        return x
