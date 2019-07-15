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

# print('casual data:')
# print_dict(data_dict_casual)

# print('\nreddit data:')
# print_dict(data_dict_reddit)

#%%


def data_separator(label_list, dict_to_fill, input_list_1, input_list_2):
    '''
    Put the needed data in a seperate category dictionary 
    '''
    for label in label_list:
        dict_to_fill[label] = input_list_1[label] + input_list_2[label]

# split data up according to category
demographic_dict = {}
demographic_labels = ["How did you find this survey (e.g., \"personal contact\", \"forum X\", \"r/catlolz\", ...)?",
    "How old are you?", "What is your gender? ", "What is your highest degree?", "Which of the following best describes your role?",
    "What is your main programming language?", "How many years of professional coding experience do you have? "]
data_separator(demographic_labels, demographic_dict, data_dict_casual, data_dict_reddit)

activity_what_dict = {}
activity_what_labels = ["activity_what_[The visualizations are understandable.]", 
"activity_what_[The visualizations are useful.]", "activity_what_[I would use this part of the dashboard.]", 
"activity_what_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(activity_what_labels, activity_what_dict, data_dict_casual, data_dict_reddit)

activity_where_dict = {}
activity_where_labels = ["activity_where_[The visualizations are understandable.]", 
"activity_where_[The visualizations are useful.]", "activity_where_[I would use this part of the dashboard.]",
"activity_where_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(activity_where_labels, activity_where_dict, data_dict_casual, data_dict_reddit)

testing_written_dict = {}
testing_written_labels = ["testing_written_[The visualization is understandable.]", 
"testing_written_[The visualization is useful.]", "testing_written_[I would use this part of the dashboard.]",
"testing_written_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(testing_written_labels, testing_written_dict, data_dict_casual, data_dict_reddit)

testing_tdd_dict = {}
testing_tdd_labels = ["testing_tdd_[The visualization is understandable.]",
"testing_tdd_[The visualization is useful.]", "testing_tdd_[I would use this part of the dashboard.]",
"testing_tdd_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(testing_tdd_labels, testing_tdd_dict, data_dict_casual, data_dict_reddit)

global_stats_dict = {}
global_stats_labels = ["global_stats_[The table is understandable.]",
"global_stats_[The table is useful.]", "global_stats_[I would use this part of the dashboard.]",
"global_stats_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(global_stats_labels, global_stats_dict, data_dict_casual, data_dict_reddit)

privacy_dict = {}
privacy_labels = ["privacy_[The privacy settings are understandable.]", 
"privacy_[The privacy settings are useful.]", "privacy_[I would use this part of the dashboard.]",
"How much of your data would you be willing to share? (Optional)", "How much are you allowed to share? (Optional)",
"privacy_Do you have additional comments or ideas on this part of the dashboard? (Optional)"]
data_separator(privacy_labels, privacy_dict, data_dict_casual, data_dict_reddit)

closure_dict = {}
closure_labels = [" [I would use the dashboard I just saw.]",
"Are there any positive things that stood out? If yes, which were they? (Optional)",
"Are there any negative things that stood out? If yes, which were they? (Optional)",
"Imagine your ideal dashboard: What other statistics or metrics should this dashboard provide besides the ones already shown in this survey? (Optional)",
"Do you have any other comments or suggestions regarding this survey? (Optional)"]
data_separator(closure_labels, closure_dict, data_dict_casual, data_dict_reddit)

# print(activity_what_dict)   

#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

