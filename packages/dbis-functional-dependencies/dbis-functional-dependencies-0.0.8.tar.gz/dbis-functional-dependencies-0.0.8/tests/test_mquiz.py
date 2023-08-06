from tests.fdstest import FunctionalDependencySetTest
from functional_dependencies.fdsbase import Notation, RelSchema, Set
from functional_dependencies.BCNF import FunctionalDependencySet
import functional_dependencies.fds as fd
import logging

class Test_MoodleQuiz(FunctionalDependencySetTest):
    '''
    test examples for dbis Moodle Quiz
    '''
    def setUp(self):
        debug=True
        profile=True
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        FunctionalDependencySetTest.setUp(self, debug=debug, profile=profile)
        
    def testQuiz(self):
        '''
        test Aufgabe 7.1
        '''

        fds=FunctionalDependencySet("ABCPQRXYZ")
        fds.add_dependency("A", "Z")
        fds.add_dependency("ABC","X")
        fds.add_dependency("PX","CR")
        fds.add_dependency("PZ","Q")
        fds.add_dependency("Y","AP")
        clos = fds.get_attr_closure("Y")
        print("attr closure of Y:",Set.stringify_set(clos,notation=Notation.short))


