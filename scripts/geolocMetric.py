from geopy import Nominatim,distance
from countryinfo import CountryInfo
import country_converter as coco
import wbgapi as wb


class geographyMetric:
    def __init__(self):
        pass
    
    def get_info(self,coun):
        coun = self.get_standerd_name(coun)
        country = CountryInfo(coun.strip())
        return {
            'iso2':self.get_iso2(coun),
            'iso3':self.get_iso3(coun),
            'area':country.area(),
            'region':country.region(),
            'languages':country.languages(),
            'neighbours':self.get_neighbours(coun)
        }
    
    def get_gdp_pop(self,coun):
        coun = self.get_iso3(coun)
        data = wb.data.DataFrame(['SP.POP.TOTL', 'NY.GDP.PCAP.CD'],
                          [coun], range(2021, 2022)).to_dict()
        return data['NY.GDP.PCAP.CD'][coun],data['SP.POP.TOTL'][coun]

    def get_distance_loc(self,coun1, coun2):
        c1 = coco.convert(names=coun1, to='ISO2')
        c2 = coco.convert(names=coun2, to='ISO2')
        d = distance.distance
        g = Nominatim(user_agent="smy-application")
        _, wa = g.geocode(c1)
        _, pa = g.geocode(c2)
        return ((d(wa, pa)).kilometers)

    def get_neighbours(self, coun):
        borders = CountryInfo(coun).borders()
        iso3_codes = coco.convert(names=borders, to='ISO3')
        return iso3_codes

    def get_iso2(self, coun):
        return coco.convert(names=coun, to='ISO2')

    def get_iso3(self, coun):
        return coco.convert(names=coun, to='ISO3')
    
    def get_standerd_name(self, coun):
        return coco.convert(names=coun, to='name_short')
    
    
if __name__ == '__main__':
    gm=geographyMetric()
    couns=['Indonesia','Cambodia','Ireland']
    couns = gm.get_iso3(couns)
    print("country info {}:".format(couns[0]))
    print(gm.get_info(couns[0]))
    print("Distance between {}-{}: {}".format(couns[0],couns[1],gm.get_distance_loc(couns[0],couns[1])))
    print("gdp of {}: {}".format(couns[0],gm.get_gdp_pop(couns[0])[0]))
    print("population of {}: {}".format(couns[0],gm.get_gdp_pop(couns[0])[1]))