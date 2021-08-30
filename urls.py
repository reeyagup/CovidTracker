"""covid_visualizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

"""
from django.contrib import admin
from django.urls import path
from covid_visualizer import views


urlpatterns = [
    
    
    path('us_cases/', views.us_cases, name='us_cases'),
    path('avg_cases_and_deaths/', views.avg_cases_and_deaths, name='avg_cases_and_deaths'),
    path('top5_radar/', views.top5_radar, name='top5_radar'), 
    path('max_diff/', views.max_diff, name='max_diff'),
    path('positive_rates/', views.positive_rates, name='positive_rates')
    
]


# Each student will develop a data visualization 
# application using Django web framework. 
# Students will write twofiles to submit: a 
# URL file as the entry point (urls.py),  
# a file containing the view Python function 
# (views.py) that  takes  a  Web  request  and  
# returns  a  Web  response.  This  will  require  
# creating  a  data  model that  can  be  accessed 
# in the views.py to retrieve the data for creating 
# visualizations. The Python module views.py provides a 
# mapping between the URL path to Python functions for 
# different visualizations in views.py. When required, 
# create a form class to take user input in file forms.py. 


# The urls.py files should include 
# five different URLs corresponding to the 
# questions listed below:  
# 1)Data access to .csv file provided with the assignment on covid-19 data
# 2)Print out a Welcome message to the console.


# def main():
#     print("Welcome to the COVID Data Visualizer")
    
        

# if __name__ == "__main__":
#     main()