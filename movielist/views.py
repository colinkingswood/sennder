import requests
from datetime import datetime
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60), name='dispatch')
class MoviesView(TemplateView):
    template_name = 'movies.html'

    def get_context_data(self, **kwargs):
        print("Get context data")
        people_url =  "https://ghibliapi.herokuapp.com/people"
        response = requests.get(people_url)
        # todo check response code, handle errors properly,
        # (though no details were given in the spec how to handle problems with endpoints,
        # this is something I would ask for more details on)
        films_to_people = {}
        for person in response.json():
            for film_url in person['films']:
                film_id = film_url.split('/')[-1]
                if not film_id in films_to_people:
                    films_to_people[film_id] = set([])  # add an empty set
                films_to_people[film_id].add(person["name"])

        film_url = "https://ghibliapi.herokuapp.com/films"
        response = requests.get(film_url)
        # todo check response code, handle errors properly
        film_list = response.json()
        for film in film_list:
            film_id = film["id"]
            try:
                person_list = list(films_to_people[film_id])
                film["people"] = person_list
            except KeyError:
                # not found in the other enpoint,
                film["people"] = ["Unknown"]

        context = super(MoviesView, self).get_context_data(**kwargs)
        context.update({'movie_list': film_list})
        context.update({"last_refresh": datetime.now()})
        return context



