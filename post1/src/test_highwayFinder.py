from tempfile import mkstemp
import csv

import nose.tools as nt

from highwayFinder import use_correct_csv_column, read_description

class TestHighwayFinder(object):
    """ Tests for highwayFinder.py

    Please remove temporary files after running tests.
    $ rm /tmp/*.csv /tmp/*.xml
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_use_correct_csv_column(self):
        """ Are the correct columns being indexed? """
        nt.assert_equals(use_correct_csv_column(["pair_id",
                                                 "not_pairId",
                                                 "Description"]),
                         (0,2))

    def desc_example(self):
        """ Examples of descriptions used in pair_definitions.csv """
        return ["I-90 WB after on-ramps (Rte 9) TO I-90 WB before on-ramps (I-495)", "I-395 NB before I-90 (u1774) to I-290 SB before I-90",
                "395NB-MM011.0 (u1777) to 90WB-MM089.7",
                "Rte. 3 SB after Rte. 18 SB Ramps TO Rte. 3 SB before emergency area (Rte. 53)",
                "I-90 EB before on-ramps (I-395/I-290) TO I-90 EB after on-ramps (Rte. 122)",
                "I-95 SB before Rt. 28 in Wakefield (u497) <1E> to I-93 SB before Fallon Rd. in Stoneham"]

    def create_test_csv_file(self):
        """ write contents for temporary csv file """
        garbage, test_file = mkstemp("test.csv")
        with open(test_file, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(['pair_id','not_pair_id','Description'])
            writer.writerow(['12345','boo', self.desc_example()[0]])
            writer.writerow(['12346','boo', self.desc_example()[1]])
        return test_file
                            
                            
    def test_read_description(self):
        """ Is the correct data structure returned? """
        nt.assert_equals(read_description(("junk",
                                        self.create_test_csv_file(),
                                           "junk"))['12345'],
                                          self.desc_example()[0])
        nt.assert_equals(read_description(("junk",
                                        self.create_test_csv_file(),
                                           "junk"))['12346'],
                                          self.desc_example()[1])

    def test_regex_parse(self):
        """ oh boy, regex """

    

