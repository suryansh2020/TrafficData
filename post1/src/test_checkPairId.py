import nose.tools as nt
from tempfile import mkstemp
from checkPairId import parse_csv, parse_xml, check_ids,\
    check_input_type, datasources, use_correct_csv_column

class TestIdScript(object):
    """ Tests for functions in checkPairId.py """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_ids_for_true_value(self):
        """ Scenarios that will return True """
        # comparing one datasource
        nt.assert_true(check_ids(['12345'],['12345']))
        # comparing more than one datasource
        nt.assert_true(check_ids(['12345'],['12345'],['12345']))
        nt.assert_true(check_ids(['12345'],['12345'],['12345'],
                                 ['12345']))
        nt.assert_true(check_ids(['12345'],['12345'],['12345'],
                                 ['12345'], ['12345']))

    def test_check_ids_for_list_differences_error(self):
        """ Scenarios that will raise an error """
        nt.assert_raises(UserWarning, check_ids,['12345'],['1234'])

    def test_check_ids_for_bad_input_values(self):
        """ Correct error raised for bad input? """
        nt.assert_raises(TypeError, check_ids,['12345'],[12345])

    def test_check_input_type(self):
        """ Find correct input type check """
        nt.assert_equals(check_input_type(['12345']), True)

    def test_check_input_type_breaks(self):
        """ Room for improvement if necessary """
        demo = ['12345', 12345]
        nt.assert_equals(check_input_type(demo), True)

    def test_datasources_for_wrong_path_used(self):
        """ If the user starts at the wrong place in the directory..."""
        # changing the working directory to raise an error
        import os
        os.getcwd()
        os.chdir(os.path.abspath("") + "/MassDOThack/")
        # testing to see if the error is raised
        nt.assert_raises(UserWarning, datasources)

    def test_datasources_for_correct_values_returned(self):
        """ Unpack the tuple & make sure it matches the docstring """
        import os
        # creating the correct folder locations
        folder_location = os.path.abspath("")+ \
                      "/MassDOThack/Road_RTTM_Volume/"
        massdot_bluetoad_data = folder_location + \
                                "massdot_bluetoad_data/" + \
                                "massdot_bluetoad_data.csv"
        pair_definitions = folder_location + \
                           "pair_definitions.csv"
        pair_routes = folder_location + \
                      "pair_routes.xml"
        # unpack tuple
        ds1,ds2,ds3 = datasources()
        # test to see if they match
        nt.assert_equal(ds1,massdot_bluetoad_data)
        nt.assert_equal(ds2,pair_definitions)
        nt.assert_equal(ds3,pair_routes)

    def test_use_correct_csv_column(self):
        """ Does the list get indexed correctly? """
        nt.assert_equal(use_correct_csv_column(["pair_id"]),
                        0)
        nt.assert_equal(use_correct_csv_column(["not_pair_id",
                                                "pair_id"]),
                        1)

    def test_parse_csv_success(self):
        mkstemp("test.csv")
        

    
