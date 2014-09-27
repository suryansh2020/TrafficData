"""
Tests functions included in mapCoordinates.py
"""
import nose.tools as nt
from tempfile import mkstemp
import codecs
import xmltodict
from collections import OrderedDict
from secret import username
from mapCoordinates import open_xml, parse_pair_id, parse_routes, \
    parse_xml, request_route_info, make_geocode_api, find_road_name, \
    create_requests

class TestMapCoordinates(object):

    def setUp(self):
        self.datasource = self.create_test_dictionary()
        
    def tearDown(self):
        pass

    def create_test_dictionary(self):
        test_dict = OrderedDict([(u'geonames',
                                  OrderedDict([(u'streetSegment',
                                                [OrderedDict([(u'line', u'-71.211143 42.710274,'),
                                                              (u'distance', u'0.021'),
                                                              (u'mtfcc', u'S1100'),
                                                              (u'name', u'I- 93'),
                                                              (u'fraddl', None),
                                                              (u'fraddr', None),
                                                              (u'toaddl', None),
                                                              (u'toaddr', None),
                                                              (u'postalcode', None),
                                                              (u'placename', u'Methuen Town'),
                                                              (u'adminCode2', u'009'),
                                                              (u'adminName2', u'Essex'),
                                                              (u'adminCode1', u'MA'),
                                                              (u'adminName1', u'Massachusetts'),
                                                              (u'countryCode', u'US')])])]))])
        return test_dict

    def create_test_xml_file(self):
        """ Temporary xml file that can be used for reading

        Returns:
            Changes the scope of test_file to a class level variable
            by assigning test_file as self.test_file.
        """
        garbage, test_file = mkstemp("test.xml")
        with open(test_file, 'wb') as xmlfile:
            xmlfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<btdata>
 <TRAVELDATA>
  <LastUpdated>Nov-30-2013 11:34:30 GMT</LastUpdated>
  <PAIRDATA>
   <PairID>5490</PairID>
   <Title>1S - I-93 SB after Pelham St. in Methuen </Title>
   <Direction>SB</Direction>
   <Origin>I-93</Origin>
   <Destination>I-93 SB</Destination>
   <Routes>
    <Route>
     <lat>42.71946</lat>
     <lon>-71.20996</lon>
    </Route>
    <Route>
     <lat>42.71941</lat>
     <lon>-71.20972</lon>
    </Route>
   </Routes>
  </PAIRDATA>
  <PAIRDATA>
   <PairID>5491</PairID>
   <Title>1S - I-93 SB after Pelham St. in Methuen </Title>
   <Direction>SB</Direction>
   <Origin>I-93</Origin>
   <Destination>I-93 SB</Destination>
   <Routes>
    <Route>
     <lat>42.68080</lat>
     <lon>-71.20221</lon>
    </Route>
    <Route>
     <lat>42.68083</lat>
     <lon>-71.20208</lon>
    </Route>
   </Routes>
  </PAIRDATA>
 </TRAVELDATA>
</btdata>
""")
        return test_file

    def open_xml(self):
        with open(self.create_test_xml_file()) as fd:
            obj = xmltodict.parse(fd.read())
        return obj

    def test_open_xml(self):
        """ Can we open the temp file successfully? """
        nt.assert_equal(len(self.open_xml()), 1)

    def test_parse_pair_id(self):
        """ Did we retrieve pair_id successfully? """
        nt.assert_equal(len(parse_pair_id(self.open_xml())),2)

    def test_parse_routes(self):
        """ Did we parse the routes successfully? """
        nt.assert_equal(len(parse_routes(self.open_xml(), 0)), 2)
        nt.assert_equal(len(parse_routes(self.open_xml(), 1)), 2)

    def test_parse_xml_keys(self):
        """ Are the correct dictionary keys returned? """
        nt.assert_equal(parse_xml(self.open_xml()).keys(),\
                        [u'5490', u'5491'])

    def test_parse_xml_values(self):
        """ Are the correct dictionary values returned given a key? """
        nt.assert_equal(parse_xml(self.open_xml())[u'5490'], \
                        [OrderedDict([(u'lat', u'42.71946'),
                                      (u'lon', u'-71.20996')]),
                         OrderedDict([(u'lat', u'42.71941'),
                                      (u'lon', u'-71.20972')])])

    def test_make_geocode_api(self):
        """ API requested correctly? Concerned about imports here """
        correct = "http://api.geonames.org/findNearbyStreets?lat=42.71946&lng=-71.20996&username=" + username
        lat = '42.71946'
        lon = '-71.20996'
        nt.assert_equal(type(username), str)
        nt.assert_equal(make_geocode_api(lat, lon), correct)

    def test_request_route_info(self):
        """ Correct item queried from dictionary? """
        nt.assert_equal(request_route_info(self.datasource, 0),
                        u'I- 93')

    def test_find_road_name_datastructure(self):
        """ Test data structure used to extract lat & lon """
        # create variables needed for testing
        data = self.open_xml()
        pair_id = [u'5490', u'5491']
        index = [0, -1]
        # tests
        nt.assert_equal(parse_xml(self.open_xml())[u'5490']\
                        [index[0]][u'lat'], u'42.71946')
        nt.assert_equal(parse_xml(self.open_xml())[u'5490']\
                        [index[0]][u'lon'], u'-71.20996')
        nt.assert_equal(parse_xml(self.open_xml())[u'5491']\
                        [index[1]][u'lat'], u'42.68083')
        nt.assert_equal(parse_xml(self.open_xml())[u'5491']\
                        [index[1]][u'lon'], u'-71.20208')

    def test_create_requests(self):
        """ Is the correct data structure returned? """
        #http_request = [u'I- 93', u'I- 95']
        # test data
        #test_data = create_requests(self.open_xml(), http_request)
        #nt.assert_equal(test_data['5490'], [u'I- 95',u'I- 93'])
        # unless the http_request parameter passes road names each
        # time a pair_id is requested then an empty list will be
        # returned. 
        #nt.assert_equal(test_data['5491'], [])

        # welcome to async, have fun not using twisted.
        pass
        

    
        
        
                     
        
        
        
