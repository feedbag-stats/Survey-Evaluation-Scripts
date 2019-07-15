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
            data_dict[h].append(v.lower())
    
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
import collections
import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go

def show_bar_chart(input_data, xlabel, ylabel, title):

    y_pos = list( dict.fromkeys(input_data))
    performance = collections.Counter(input_data).values()

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, input_data, rotation='vertical')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

    plt.show()

def get_likert_scales_list(input_dict, label_list):
    all_likert_values_list = []
    for label in label_list:
        data = input_dict[label]
        y_pos = list(dict.fromkeys(data))
        performance = collections.Counter(data).values()
        individual_results_dict = {}
        for y, p in zip(y_pos, performance):
            individual_results_dict[y] = p
        
        if "strongly disagree" not in individual_results_dict.keys():
            individual_results_dict["strongly disagree"] = 0
        if "disagree" not in individual_results_dict.keys():
            individual_results_dict["disagree"] = 0
        if "neutral" not in individual_results_dict.keys():
            individual_results_dict["neutral"] = 0
        if "agree" not in individual_results_dict.keys():
            individual_results_dict["agree"] = 0
        if "strongly agree" not in individual_results_dict.keys():
            individual_results_dict["strongly agree"] = 0
        if "no answer" not in individual_results_dict.keys():
            individual_results_dict["no answer"] = 0

        individual_results_list = [individual_results_dict["strongly disagree"], individual_results_dict["disagree"], individual_results_dict["neutral"],
        individual_results_dict["agree"], individual_results_dict["strongly agree"], individual_results_dict["no answer"]]
        
        all_likert_values_list.append(individual_results_list)
    return all_likert_values_list

def likert_scale_plot(input_list, title):
    likert_colors = ['white', 'firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue']
    data = pd.DataFrame([input_list[0], input_list[1], input_list[2]],
                    columns=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "No Answer"],
                    index=["The visualizations are understandable.", 
                    "The visualizations are useful.", "I would use this part of the dashboard."])
    middles = data[["Strongly Disagree", "Disagree"]].sum(axis=1)+data["Neutral"]*.5
    longest = middles.max()
    
    complete_longest = data.sum(axis=1).max()
    data.insert(0, '', (middles - longest).abs())

    data.plot.barh(stacked=True, color=likert_colors, edgecolor='none', legend=False)
    z = plt.axvline(longest, linestyle='--', color='black', alpha=.5)
    z.set_zorder(-1)

    plt.xlim(0, complete_longest)
    xvalues = range(0,complete_longest,10)
    xlabels = [str(x-longest) for x in xvalues]
    plt.xticks(xvalues, xlabels)
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

### Demongraphic graphics

# how did you find this survey
input_data = sorted(demographic_dict["How did you find this survey (e.g., \"personal contact\", \"forum X\", \"r/catlolz\", ...)?"])
show_bar_chart(input_data, '', '', 'How did you find this survey?')

# age

# gender

# highest degree

# role

# programming language

# professional coding experience

#%%

# activity what 
input_data = get_likert_scales_list(activity_what_dict, ["activity_what_[The visualizations are understandable.]", 
"activity_what_[The visualizations are useful.]", "activity_what_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "Activity Type")

# activity where
input_data = get_likert_scales_list(activity_where_dict, ["activity_where_[The visualizations are understandable.]", 
"activity_where_[The visualizations are useful.]", "activity_where_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "Activity Location")

# written tests
input_data = get_likert_scales_list(testing_written_dict, ["testing_written_[The visualization is understandable.]", 
"testing_written_[The visualization is useful.]", "testing_written_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "Written Tests")

# TDD tests
input_data = get_likert_scales_list(testing_tdd_dict, ["testing_tdd_[The visualization is understandable.]",
"testing_tdd_[The visualization is useful.]", "testing_tdd_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "TDD cycles")

# global stats
input_data = get_likert_scales_list(global_stats_dict, ["global_stats_[The table is understandable.]",
"global_stats_[The table is useful.]", "global_stats_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "Global Statistics")

# privacy
input_data = get_likert_scales_list(privacy_dict, ["privacy_[The privacy settings are understandable.]", 
"privacy_[The privacy settings are useful.]", "privacy_[I would use this part of the dashboard.]"])
likert_scale_plot(input_data, "Privacy Settings")

# closure
input_data = sorted(closure_dict[" [I would use the dashboard I just saw.]"])
show_bar_chart(input_data, '', '', 'I would use the dashboard I just saw.')
#%%
