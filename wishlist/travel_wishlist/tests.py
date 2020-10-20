from django.test import TestCase
from django.urls import reverse

from .models import Places

class TestHomePage(TestCase):

    def test_load_home_page_shows_empty_list_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')


class TestWishList(TestCase):

    fixtures = ['test_places']

    def test_view_wishlist_contains_not_visited_places(self):

        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

# Test for no places visited
class TestNoPlacesVisited(TestCase):

    def test_no_places_visited_displays_message(self):

        response = self.client.get(reverse('places_visited'))
        self.assertFalse(response.context['visited'])
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet.')

# Test visited places and showing the visited places only
class TestVisitedList(TestCase):

    fixtures = ['test_places']

    def test_view_visited_contains_only_visited(self):

        response =self.client.get(reverse('places_visited'))

        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestAddNewPlace(TestCase):

    def test_add_new_place_to_wish_list(self):

        response = self.client.post(reverse('place_list'), {'name': 'Tokyo', 'visited':False}, follow=True)

        # checking if using the right template
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        places_response = response.context['places']

        # should get one item
        self.assertEqual(len(places_response), 1)
        tokyo_response = places_response[0]

        # use get() to get the data with the expected values
        # Check what is expected in the database
        tokyo_in_db = Places.objects.get(name='Tokyo', visited=False)

        # Test if it render the same data
        self.assertEqual(tokyo_response, tokyo_in_db)


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):

        # Change place_pk 2 to Visited
        response = self.client.post(reverse('place_was_visited', args=(2,) ), follow=True)

        # checking if using the right template
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # New York should not be in the response
        self.assertNotContains(response, "New York")

        response = Places.objects.get(pk=2)
        # Expecting the visited is True
        self.assertTrue(response.visited)

    def test_visit_with_no_existent_place(self):

        response = self.client.post(reverse('place_was_visited', args=(200,) ), follow=True)
        self.assertEqual(response.status_code, 404)