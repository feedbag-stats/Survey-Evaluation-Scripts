#%%
import markdown
from IPython.core.display import display, HTML
def md(str):
    display(HTML(markdown.markdown(str + "<br />")))

#%%
import csv

def get_data_dict_from_csv(csv_file):

    survey_file = open(csv_file, mode='r', encoding='UTF-8')
    reader = csv.reader(survey_file)
    headers = next(reader, None)

    data_dict = {}
    for h in headers:
        data_dict[h] = []

    for row in reader:
        for h, v in zip(headers, row): 
            data_dict[h].append(v)
    
    return data_dict

def print_dict(dict_to_print):
    for key, value in dict_to_print.items():
        print(key, ":", value)
        
data_dict_casual = get_data_dict_from_csv('data/Dashboard_Survey_v3.csv')
data_dict_reddit = get_data_dict_from_csv('data/Dashboard_Survey_v3_Reddit_Version.csv')

print('casual data:')
print_dict(data_dict_casual)

print('\nreddit data:')
print_dict(data_dict_reddit)
    

#%%
