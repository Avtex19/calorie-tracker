import json

import requests
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from myapp.forms import CustomUserCreationForm, UserProfileUpdateForm
from myapp.models import Breakfast, Dinner, Lunch, UserProfile


# from myapp.forms import MealForm
# from myapp.models import Meal

@login_required(login_url='login')
def home(request):
    specified_food_data = {}
    food_data_json = {}
    food_data = {}
    global calories
    if request.method == 'POST':
        if 'submit-name' in request.POST:
            api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
            query = request.POST.get('name')
            response = requests.get(api_url + query,
                                    headers={'X-Api-Key': '1yPtcvsrXsk82coZkkXsyw==9QRr5sw42w1Vn3Wh'})
            foodN = response.json().get("items", [])  # in this query set get value what is a list
            if foodN:
                food_data = foodN[0]
                calories = food_data.get('calories')
                # create food_data items which we went to display
                specified_food_data = {
                    'Name': food_data.get('name'),
                    'Calories': food_data.get('calories'),
                    'Serving Size (g)': food_data.get('serving_size_g'),
                    'Protein (g)': food_data.get('protein_g'),
                    'Fat (g)': food_data.get('fat_total_g'),
                    'Sodium (g)': food_data.get('sodium_mg') / 1000,  # Convert mg to g
                    'Potassium (g)': food_data.get('potassium_mg') / 1000,  # Convert mg to g
                    'Cholesterol (mg)': food_data.get('cholesterol_mg'),
                    'Carbohydrates (g)': food_data.get('carbohydrates_total_g'),
                    'Fiber (g)': food_data.get('fiber_g'),
                    'Sugar (g)': food_data.get('sugar_g')
                }

                specified_food_data_for_charts = {
                    'Protein': food_data.get('protein_g'),
                    'Fat': food_data.get('fat_total_g'),
                    'Sodium': food_data.get('sodium_mg') / 1000,
                    'Potassium': food_data.get('potassium_mg') / 1000,
                    'Cholesterol': food_data.get('cholesterol_mg') / 1000,
                    'Carbohydrates': food_data.get('carbohydrates_total_g'),
                    'Fiber': food_data.get('fiber_g'),
                    'Sugar': food_data.get('sugar_g')
                }
                print(specified_food_data)

                # Serialize the food_data dictionary to JSON
                food_data_json = json.dumps(specified_food_data_for_charts)

        elif 'meal' in request.POST and 'foodName' in request.POST:
            meal = request.POST.get('meal')
            food_name = request.POST.get('foodName')

            # Determine which meal model to use based on the 'meal' parameter
            if meal == 'breakfast':
                meal_model = Breakfast
            elif meal == 'lunch':
                meal_model = Lunch
            elif meal == 'dinner':
                meal_model = Dinner
            else:
                return HttpResponseBadRequest("Invalid meal type.")

            # Check if the food is already in the selected meal
            if meal_model.objects.filter(user=request.user, name=food_name).exists():
                message = f'{food_name} is already in {meal}.'

            else:
                # Add the food to the selected meal
                food = meal_model(user=request.user, name=food_name, calories=calories)
                food.save()
                message = f'{food_name} added to {meal}.'

            response_data = {'message': message}
            return JsonResponse(response_data)

    return render(request, 'home.html', {'specified_food_data': specified_food_data, 'food_data': food_data,
                                         'food_data_json': food_data_json})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm  # Use your custom form

    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        print(user)
        print(UserProfile.objects.get_or_create(user=user))

        # Initialize the user's profile with data from the registration form
        user_profile.age = form.cleaned_data['age']
        user_profile.height = form.cleaned_data['height']
        user_profile.weight = form.cleaned_data['weight']

        user_profile.save()
        if user is not None:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.values():
            for error in errors:
                messages.error(self.request, error)
        return super(RegisterView, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def showDetails(request):
    # Retrieve the user's UserProfile or create it if it doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if the user_profile is created and associated with the user
    if created:
        user_profile.user = request.user
        user_profile.save()

    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
        else:
            print("ERROR")
    else:
        form = UserProfileUpdateForm(instance=user_profile)

    return render(request, "account_details.html", {'user_profile': user_profile,
                                                    "user_profile_form": form})


@login_required(login_url='login')
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})


def favourite_foods(request):
    favourite_lunch = Lunch.objects.filter(user=request.user)
    favourite_breakfast = Breakfast.objects.filter(user=request.user)
    favourite_dinner = Dinner.objects.filter(user=request.user)
    print(favourite_lunch)

    context = {'favourite_lunch': favourite_lunch, 'favourite_breakfast': favourite_breakfast,
               'favourite_dinner': favourite_dinner}
    return render(request, 'favourite_foods.html', context)


class lunchDelete(LoginRequiredMixin, DeleteView):
    model = Lunch
    context_object_name = 'lunch'
    success_url = reverse_lazy('favourite_foods')
    template_name = 'favourite_foods.html'


class breakfastDelete(LoginRequiredMixin, DeleteView):
    model = Breakfast
    context_object_name = 'breakfast'
    success_url = reverse_lazy('favourite_foods')
    template_name = 'favourite_foods.html'


class dinnerDelete(LoginRequiredMixin, DeleteView):
    model = Dinner
    context_object_name = 'dinner'
    success_url = reverse_lazy('favourite_foods')
    template_name = 'favourite_foods.html'


def showBmi(request):
    return render(request, 'bmi-tracker.html')
