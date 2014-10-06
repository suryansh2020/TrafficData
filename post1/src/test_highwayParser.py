from tempfile import mkstemp
import codecs
import xmltodict
import nose.tools as nt

from highwayParser import parse_tags, parse_and_pop

class TestHighwayParser(object):
    """ Tests for highwayParser.py """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_test_xml(self):
        """ write contents for temporary xml file """
        garbage, test_file = mkstemp("test.xml")
        with codecs.open(test_file, 'wb', encoding='utf-8') as xmlfile:
            xmlfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<btdata>
 <TRAVELDATA>
  <LastUpdated>Nov-30-2013 11:34:30 GMT</LastUpdated>
  <PAIRDATA>
   <PairID>5490</PairID>
   <Title>1S - I-93 SB after Pelham St. in Methuen (u508) &lt;3D&gt; to I-93 SB before I-95 in Woburn (u495) &lt;1C&gt;</Title>
   <Direction>SB</Direction>
   <Origin>I-93 SB after Pelham St. in Methuen (u508) &lt;3D&gt;</Origin>
   <Destination>I-93 SB before I-95 in Woburn (u495) &lt;1C&gt;</Destination>
   <Routes>
    <Route>
     <lat>42.71946</lat>
     <lon>-71.20996</lon>
    </Route>
    <Route>
     <lat>42.71941</lat>
     <lon>-71.20972</lon>
    </Route>
    <Route>
     <lat>42.71876</lat>
     <lon>-71.20994</lon>
    </Route>
    <Route>
     <lat>42.71735</lat>
     <lon>-71.21037</lon>
    </Route>
   </Routes>
   <Stale/>
   <TravelTime>695.96389591268</TravelTime>
   <Speed>78.1</Speed>
   <FreeFlow>65</FreeFlow>
   <Status>Active</Status>
   <Highway/>
  </PAIRDATA>
  <PAIRDATA>
   <PairID>10525</PairID>
   <Title>0C to 95NB-MM015.3</Title>
   <Direction>NB</Direction>
   <Origin>I-93 NB after Columbia Rd. in Boston (u489) &lt;0C&gt;</Origin>
   <Destination>93 NB Viaduct before Ramp</Destination>
   <Routes>
    <Route>
     <lat>42.32514</lat>
     <lon>-71.05609</lon>
    </Route>
    <Route>
     <lat>42.32508</lat>
     <lon>-71.05622</lon>
    </Route>
    <Route>
     <lat>42.32736</lat>
     <lon>-71.05833</lon>
    </Route>
    <Route>
     <lat>42.32856</lat>
     <lon>-71.05945</lon>
    </Route>
    <Route>
     <lat>42.33007</lat>
     <lon>-71.06086</lon>
    </Route>
    <Route>
     <lat>42.33128</lat>
     <lon>-71.06196</lon>
    </Route>
    <Route>
     <lat>42.33158</lat>
     <lon>-71.06223</lon>
    </Route>
    <Route>
     <lat>42.33262</lat>
     <lon>-71.06306</lon>
    </Route>
    <Route>
     <lat>42.33328</lat>
     <lon>-71.06364</lon>
    </Route>
    <Route>
     <lat>42.33332</lat>
     <lon>-71.06356</lon>
    </Route>
   </Routes>
   <Stale/>
   <TravelTime>36</TravelTime>
   <Speed>70.0</Speed>
   <FreeFlow>55</FreeFlow>
   <Status>Active</Status>
   <Highway/>
  </PAIRDATA>
</TRAVELDATA>
</btdata>""")
            return test_file

    def read_test_xml(self):
        """ Read & parse test xml """
        with codecs.open(self.create_test_xml(), encoding='utf-8') as fd:
            obj = xmltodict.parse(fd.read())
            return obj
            

    def test_parse_tags(self):
        """ Make sure strings are parsed correctly/STOP THE PAIN """
        origin= u'I-93 SB after Pelham St. in Methuen (u508) <3D>'
        destination= u'I-93 SB before I-95 in Woburn (u495) <1C>'
        nt.assert_equals(parse_tags(self.read_test_xml(), 0),
                         (origin, destination))
        origin= u'I-93 NB after Columbia Rd. in Boston (u489) <0C>'
        destination = u'93 NB Viaduct before Ramp'
        nt.assert_equals(parse_tags(self.read_test_xml(), 1),
                         (origin, destination))

    def test_parse_and_pop(self):
        """ Pop it like it's hot?? How does that song go?"""
        origin= [u'I-93 SB after Pelham St. in Methuen (u508) <3D>',
                 u'93 NB Viaduct before Ramp']
        nt.assert_equals(parse_and_pop(origin[0]),u'I-93')
        nt.assert_equals(parse_and_pop(origin[1]),u'93')
        gremlins = [u'Rte. 3',u'Rt. 3',u'Rte. 495',
                    u'Hungry muffins',u'I-495']
        nt.assert_equals(parse_and_pop(gremlins[0]),u'Rte. 3')
        nt.assert_equals(parse_and_pop(gremlins[1]),u'Rt. 3')
        nt.assert_equals(parse_and_pop(gremlins[2]),u'Rte. 495')
        nt.assert_equals(parse_and_pop(gremlins[3]),u'Hungry')
        nt.assert_equals(parse_and_pop(gremlins[4]),u'I-495')
        monsters = [u'Rte 3']
        nt.assert_equals(parse_and_pop(monsters[0]),u'Rte 3')

        
