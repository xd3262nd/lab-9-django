from django.shortcuts import render, redirect, get_object_or_404
from .models import Places
from .forms import NewPlaceForm


def place_list(request):
    """ If this is a POST request, the user clicked the Add button
        in the form. Check if the new place is valid, if so, save a
        new Place to the database, and redirect to this same page.
        This creates a GET request to this same route.
        If not a POST route, or Place is not valid, display a page with
        a list of places and a form to add a new place.
    """
    if request.method == 'POST':
        form = NewPlaceForm(request.POST) # this is to create a form object based on what is being sent from the server
        place = form.save()  # Create a new Place from the form or creating a model object from the form
        if form.is_valid():  # Checks against DB Constraints, for example, are required fields present?
            place.save()  # Saves places to the database
            return redirect('place_list')  # redirects to GET view with name place_list - which is this same view or reload the homepage

    # If not a POST, or the form is not valid, render the page
    # with the form to add a new place, and list of places
    places = Places.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create the HTML

    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def about(request):
    author = 'Qian'
    about = 'A website to create a list of places to visit'

    return render(request, 'travel_wishlist/about.html', { 'author': author, 'about': about})

def places_visited(request):
    visited = Places.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Places, pk=place_pk)
        place.visited = True
        place.save()

    return redirect('place_list')


