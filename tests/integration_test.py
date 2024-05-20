import unittest
from cast.application.test import run
    
class Test(unittest.TestCase):


    def testName(self):
        # eng = create_postgres_engine(user='operator',
        #                    password='CastAIP',
        #                    host='localhost',
        #                    port=2284,
        #                    database='postgres')
        # run(kb_name= "recipeportal_local", application_name= "recipeportal", event='start_application')
        # run(kb_name= "recipeportal_local", application_name= "recipeportal", event='after_module')
        run(kb_name= "one_service_local", application_name= "One Service", event='after_snapshot')
        # run(kb_name= "recipeportal_local", application_name= "recipeportal", event='end_application')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
