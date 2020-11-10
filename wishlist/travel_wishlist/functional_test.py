from selenium.webdriver.firefox.webdriver import WebDriver
from django .test import LiveServerTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .models import Places

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_title_shown_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn(self.selenium.title, 'Travel Wishlist')
    

class AddPlacesTests(LiveServerTestCase):

    fixtures = ['test_places']
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_new_place(self):

        self.selenium.get(self.live_server_url) # load the home page
        input_name = self.selenium.find_element_by_id('id_name')
        input_name.send_keys('Denver')
        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()


        # Expect new element to appear on page. 
        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', self.selenium.page_source)

        self.assertIn('Denver', self.selenium.page.source)

        self.assertIn('Tokyo', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)


        denver_db = Places.objects.get(pk=5)
        self.assertEqual('Denver', denver_db.name)
        self.assertFalse(denver_db.visited)


class EditPlacesTests(LiveServerTestCase):

    fixtures = ['test_places']
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_mark_place_as_visited(self):

        self.selenium.get(self.live_server_url)

        visited_button = self.selenium.find_element_by_id('visited-button-2')
        self.selenium.find_element_by_id('place-name-2')
        visited_button.click()


        wait = WebDriverWait(self.selenium, 3)
        wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))

        self.assertIn('Tokyo', self.selenium.page_source)

        self.assertNotIn('New York', self.selenium.page_source)

        self.selenium.get(self.live_server_url + '/visited')

        self.assertIn('New York', self.selenium.page_source)

        self.assertIn('San Francisco', self.selenium.page_source)
        self.assertIn('Moab', self.selenium.page_source)

        new_york = Places.objects.get(pk=2)
        self.assertTrue(new_york.visited)


class PageContentTests(LiveServerTestCase):

    fixtures = ['test_places']
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_get_home_page_list_of_places(self):
        self.selenium.get(self.live_server_url)

        self.assertIn('Tokyo', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)


        self.assertNotIn('San Francisco', self.selenium.page_source)
        self.assertNotIn('Moab', self.selenium.page_source)

    def test_get_list_of_visited_places(self):

        self.selenium.get(self.live_server_url + '/visited')

        self.asserNotIn('Tokyo', self.selenium.page_source)
        self.asserNotIn('New York', self.selenium.page_source)

        self.assertIn('San Francisco', self.selenium.page_source)
        self.assertIn('Moab', self.selenium.page_source)
