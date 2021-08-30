import pandas as pd
from django.http import HttpResponse, request
from django.shortcuts import render
from pathlib import Path
import os
from .forms import get_month


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


FILENAME = '/Users/reeyagupta/Desktop/PerformantPython/Bonus/covid_visualizer/covid-data-10-16-20.csv'

#[os.path.join(BASE_DIR, 'covid_visualizer/covid-data-10-16-20.csv')]

def us_cases(request):

    data = pd.DataFrame(pd.read_csv(FILENAME, usecols=['location', 'date', 'new_cases_smoothed', 'total_cases']))
    US_data = data[(data.location == "United States")]

    US_data = US_data.dropna()

    label = US_data['date'].to_list()
    total_cases = US_data['total_cases'].to_list()
    new_cases_smoothed = US_data['new_cases_smoothed'].to_list()
    context = {'labels': label, "total_cases": total_cases, "new_cases": new_cases_smoothed }

    return render(request, 'us_cases.html', context)
  
def top5_radar(request):
    total_cases = pd.DataFrame(pd.read_csv(FILENAME, usecols= ['location', 'total_cases', 'total_cases_per_million', 'total_deaths_per_million',
                                                   'total_deaths']))

    total_cases = total_cases.drop_duplicates(subset=['location'], keep = "last")

    top_5 = total_cases.sort_values(by=['total_cases'], ascending=False)
    top_5 = top_5[(top_5.location != "World")]
    top_5 = top_5.head(5)
    
    labels = top_5['location'].tolist()

    total_cases = top_5['total_cases'].tolist()
    total_cases = [x / 10000 for x in total_cases]
    
    total_deaths = top_5['total_deaths'].tolist()
    total_deaths = [x / 1000 for x in total_deaths]
    
    total_cases_per_million = top_5['total_cases_per_million'].tolist()

    total_deaths_per_million = top_5['total_deaths_per_million'].tolist()
    total_deaths_per_million = [x * 100 for x in total_deaths_per_million]


    context = {
        'labels': labels, "cases": total_cases, "deaths": total_deaths, 'cases_per_million': total_cases_per_million, 'deaths_per_million': total_deaths_per_million

    }
    return render(request, "top5_radar.html", context)
    
def max_diff(request):
    data = pd.DataFrame(pd.read_csv(FILENAME, usecols= ['date', 'location', 'total_cases']))


    total_cases_before_may_31 = [(data.location != "World")]
    total_cases_before_may_31 = (data[data['date'].str.startswith('5/31/2020')])
    total_cases_before_may_31 = total_cases_before_may_31.sort_values(by=['total_cases'], ascending=False)
    total_cases_before_may_31 = total_cases_before_may_31[(total_cases_before_may_31.location != "World")]
    total_cases_before_may_31_top_5 = total_cases_before_may_31.head(5)


    #curr total cases
    total_cases_to_date = data[(data.location != "World")]
    total_cases_to_date = total_cases_to_date.drop_duplicates(subset=['location'], keep = "last")
    
    #LABELS
    top_5_labels = total_cases_before_may_31['location'].head(5)
    top_5_case_totals_before_may31 = total_cases_before_may_31['total_cases'].head(5) #total num of cases before may 31
    #print(top_5_case_totals_before_may31) #subtract from this the new amt with abs values
    


    top_5_case_totals_to_date = pd.DataFrame(columns = ['location', 'date', 'total_cases'])
    before_may_31 = pd.DataFrame(columns = ['location', 'date', 'total_cases'])

    for country in top_5_labels:
        top_5_case_totals_to_date = top_5_case_totals_to_date.append(total_cases_to_date[(total_cases_to_date.location == str(country))])
        before_may_31 = before_may_31.append(total_cases_before_may_31_top_5[(total_cases_before_may_31_top_5.location == str(country))])


    prev = {}
    old_cases = []
    new_cases = []

    for key, value in total_cases_before_may_31_top_5.iterrows():
        print("country", value['location'])
        print("before_may", value['total_cases'])
        
        prev[(str(value['location']))] = int(value['total_cases'])


    print("new vals")
    curr = {}
    #WORKS
    for key, value in top_5_case_totals_to_date.iterrows():

        print("country", value['location'])
        print("to_date", value['total_cases'])
        curr[(str(value['location']))] = int(value['total_cases'])
        new_cases.append(int(value['total_cases']) - prev[(str(value['location']))])
        

    index = 0
    max_diff = []
    for country in top_5_labels:
        max_diff.append(abs(new_cases[index] - prev[(str(value['location']))]))
        
        index = index + 1

    top_5_labels = top_5_labels.tolist()

    
    context = {
        'labels':top_5_labels, 'differences':max_diff
    }

    return render(request, 'max_diff.html', context)

class country:
    name = ""
    avg_new_cases = 0
    tmp = 0
    new_cases = 0

def avg_cases_and_deaths(request): 

    data = pd.DataFrame(pd.read_csv(FILENAME, usecols= ['location', 'date', 'new_cases_smoothed', 'new_deaths']))
    data = data.dropna(subset = ['new_cases_smoothed'])
    data = data[(data.location != "World")]
    data = data[(data.location != "International")]
    # data = data[(data.location == "United States")]
    #print(data)

    countries = pd.DataFrame(pd.read_csv(FILENAME, usecols=['location']))
    countries = countries[(countries.location != "World")]
    countries = countries[(countries.location != "International")]
    countries = countries.drop_duplicates()
    countries = countries['location']
    #print(countries)

    arr = ['12/', '1/', '2/', '3/', '4/', '5/', '6/', '7/', '8/', '9/', '10/']
   
    country_data = []
    for c in countries:
        new_country = country()
        new_country.name = str(c)
        max_avg = 0
        for num in arr:
            tmp = data[(data.location == str(c))]
            month = (tmp[tmp['date'].str.startswith(num)])
            
            if max_avg < month["new_cases_smoothed"].mean():
                max_avg = month["new_cases_smoothed"].mean() 
                new_country.avg_new_cases = max_avg
                new_country.new_cases = month["new_cases_smoothed"].sum()
                new_country.tmp = month["new_deaths"].sum()
                
        #print(str(c), " highest new cases avg for " , str(c),  " ", new_country.avg_new_cases , " new deaths for " , new_country.new_deaths)
        country_data.append(new_country)
    

    #to_list()
    country_data.sort(key=lambda x: x.avg_new_cases, reverse=True)

    country_list = []
    new_cases_list = []
    new_deaths_list = []
    index = 0
    for c in country_data:
        country_list.append(str(c.name))
        new_cases_list.append(int(c.new_cases)/10000)
        new_deaths_list.append(int(c.tmp))
        index = 1+index
        if index == 5:
            break
        
    context = {
        'labels': country_list,
        'new_cases': new_cases_list,
        'new_deaths': new_deaths_list
    }
        
    return render(request, 'avg_cases_and_tests.html', context)

class country_pos:
    name = ""
    pos_rate = 0.0
    total_cases = 0

def positive_rates(request):
    submitted = False
    if request.method == 'POST':
        form = get_month(request.POST)
        if form.is_valid():
            try:
                month_num = form['month_num'].value()

                month_str = str(month_num)+'/'

                new_cases = pd.DataFrame(pd.read_csv(FILENAME, usecols= ['location', 'date', 'new_cases','positive_rate']))

                new_cases = new_cases[(new_cases.location != "World")]
                new_cases = (new_cases[new_cases['date'].str.startswith(month_str)])
                #new_cases = new_cases.dropna

                countries = pd.DataFrame(pd.read_csv(FILENAME, usecols=['location']))
                countries = countries[(countries.location != "World")]
                countries = countries[(countries.location != "International")]
                countries = countries.drop_duplicates()
                countries = countries['location']
                
                country_arr = []

                for c in countries:
                    new_country = country_pos()
                    new_country.name = str(c)
                    tmp = new_cases[(new_cases.location == str(c))]
                    tmp = tmp.dropna()

                    month_data = (tmp[tmp['date'].str.startswith(month_str)])
                    month_data['positive_rate'].dropna()
                    #print(month_data)
                    sum = float(month_data["positive_rate"].sum()) #fix this
                    if sum == 0:
                        new_country.pos_rate = 0
                    else:
                        size = len(month_data["positive_rate"])
                        new_country.pos_rate = float(sum/size)
                    
                    new_country.total_cases = int(month_data["new_cases"].sum())
                    country_arr.append(new_country)

                country_arr.sort(key=lambda x: x.pos_rate, reverse=True)

                labels = []
                pos_rates = []
                index = 0
                for c in country_arr:
                    labels.append(str(c.name))
                    pos_rates.append(float(c.pos_rate))
                    index = 1+index
                    print(c.name)
                    if index == 5:
                        break
                
                pos_rates = [x * 100 for x in pos_rates]
                
                context = {
                    'form': form, 'labels' : labels, 'positive_rates' : pos_rates
                }
                return render(request, 'positive_rates.html', context)
            except:
                print("Error: Invalid input")
                return render(request, 'positive_rates.html', {'form': form})
    else:
        form = get_month()
        if submitted in request.GET:
            submitted = True
        return render(request, 'positive_rates.html', {'form': form})
            
            
    #top_5_case_totals_to_date = pd.DataFrame(columns = ['location', 'date', 'total_cases'])
    
    # total_cases_before_may_31 = data.set_index("location")

    # total_cases_before_may_31 = [(data.location != "World")]
    # total_cases_before_may_31 = (data[data['date'].str.startswith('5/31/2020')])

if __name__ == "__main__":    
    avg_cases_and_deaths()