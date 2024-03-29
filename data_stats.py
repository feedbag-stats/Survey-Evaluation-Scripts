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
import re

import plotly.plotly as py
import plotly.graph_objs as go

def show_bar_chart(input_data, xlabel, ylabel, title):
    y_pos = list( dict.fromkeys(input_data))
    performance = list(collections.Counter(input_data).values())
    plt.bar(y_pos, performance, align='center', alpha=0.5)

    plt.xticks(rotation='vertical')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

    xlocs, xlabs = plt.xticks()
    for i, v in enumerate(performance):
        plt.text(xlocs[i] - 0.25, v + 0.01, str(v))

    fig = plt.gcf()
    plt.show()
    fig.savefig('figures/bar-charts/' + title + '.png', bbox_inches='tight', dpi=300)

def show_grouped_bar_chart(labels, input_list, input_label_list, title):
    """
    Code taken and modified from: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    Last visited: 16.07.2019
    """
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects = []
    for inp,label in zip(input_list, input_label_list):
        rects.append(ax.bar(x - width/2, inp, width, label=label))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    for rect in rects:
        autolabel(rect, ax)

    fig.tight_layout()
    
    figToSafe = plt.gcf()
    plt.show()
    figToSafe.savefig('figures/grouped-bar-charts/' + title + '.png', bbox_inches='tight', dpi=300)

def autolabel(rects, ax):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    Code taken from: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    Last visited: 16.07.2019
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



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

#%%
def show_likert_scale_plot(input_list, title, number_of_inputs, axis_type):
    """
    Generate a likert scale plot for one or three inputs.
    Code taken and modified from: https://stackoverflow.com/questions/23142358/create-a-diverging-stacked-bar-chart-in-matplotlib
    Last visited: 16.07.2019
    """
    likert_colors = ['white', 'firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue', 'green']
    if number_of_inputs == 3:
        data = pd.DataFrame([input_list[0], input_list[1], input_list[2]],
                    columns=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "No Answer"],
                    index=["The visualizations are understandable.", 
                    "The visualizations are useful.", "I would use this part of the dashboard."])
    elif number_of_inputs == 1:
        data = pd.DataFrame([input_list[0]],
                    columns=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "No Answer"],
                    index=["I would use the dashboard I just saw."])
    else:
        return

    middles = np.sum(data[["Strongly Disagree", "Disagree"]], axis=1)+data["Neutral"]*.5
    longest = middles.max()
    
    complete_longest = np.sum(data, axis=1).max()
    data.insert(0, '', (middles - longest).abs())

    data.plot.barh(stacked=True, color=likert_colors, edgecolor='none', legend=False)
    z = plt.axvline(longest, linestyle='--', color='black', alpha=.5)
    z.set_zorder(-1)

    plt.xlim(0, complete_longest)
    plt.axis(axis_type)
    xvalues = range(0,complete_longest,20)
    xlabels = [str(x-longest) for x in xvalues]
    plt.xticks(xvalues, xlabels)
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig = plt.gcf()
    plt.show()
    fig.savefig('figures/likerts-charts/' + title + '.png', bbox_inches='tight', dpi=300)

#%%

### Demongraphic graphics

finding_survey_list = demographic_dict["How did you find this survey (e.g., \"personal contact\", \"forum X\", \"r/catlolz\", ...)?"]
try:
    finding_survey_list[finding_survey_list.index('personal contact (tim)')] = 'personal contact'
    finding_survey_list[finding_survey_list.index('friend sent it to me')] = 'personal contact'
except:
    pass

gender_list = demographic_dict["What is your gender? "]
age_list = demographic_dict["How old are you?"]
degree_list = demographic_dict["What is your highest degree?"]
try:
    degree_list[degree_list.index('high school diploma')] = 'high school'

except:
    pass

# fuse all different variations of writing bachelor and master together
try:
    pattern_bachelor = re.compile("(.*bachelor.*|.*bsc.*)")
    pattern_master = re.compile(".*master.*")
    for index, degree in enumerate(degree_list):
        if pattern_bachelor.match(degree):
            degree_list[index] = "bachelor"
        if pattern_master.match(degree):
            degree_list[index] = "master"
except:
    pass

role_list = demographic_dict["Which of the following best describes your role?"]
programming_lang_list = demographic_dict["What is your main programming language?"]
coding_exp_list = demographic_dict["How many years of professional coding experience do you have? "]

# fuse some similar expressions
try:
    coding_exp_list[coding_exp_list.index('0.5 years')] = '0.5'
    coding_exp_list[coding_exp_list.index('less than a year')] = '0.5'
    coding_exp_list[coding_exp_list.index('<1')] = '0.5'
    coding_exp_list[coding_exp_list.index('10+')] = '10'

except:
    pass

show_bar_chart(sorted(finding_survey_list), '', '', 'How did you find this survey?')
show_bar_chart(sorted(gender_list), '', '', 'Gender Distribution')
show_bar_chart(sorted(age_list), '', '', 'Age Distribution')
show_bar_chart(sorted(degree_list), '', '', 'Degrees')
show_bar_chart(sorted(role_list), '', '', 'Roles')
show_bar_chart(sorted(programming_lang_list), '', '', 'Main Programming Languages')
show_bar_chart(sorted(coding_exp_list, key=lambda x: float(x)), '', '', 'Years of Coding Experiences')

# female_degree_list = []
# male_degree_list = []
# for gender, degree in zip(gender_list, degree_list):
#     if gender == 'male':
#         male_degree_list.append(degree)
#     if gender == 'female':
#         female_degree_list.append(degree)
# female_degree_list.sort()
# male_degree_list.sort()
# male_performance = list(collections.Counter(male_degree_list).values())
# female_performance = list(collections.Counter(female_degree_list).values())

# degrees = list(dict.fromkeys(sorted(degree_list)))
# print(male_performance)
# print(female_performance)
# print(degrees)
# show_grouped_bar_chart(degrees, male_performance, female_performance, 'Male', 'Female')

#%%

### Likert Scale Questions

# activity what 
label_list = get_likert_scales_list(activity_what_dict, ["activity_what_[The visualizations are understandable.]", 
"activity_what_[The visualizations are useful.]", "activity_what_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "Activity Type", 3, "tight")

# activity where
label_list = get_likert_scales_list(activity_where_dict, ["activity_where_[The visualizations are understandable.]", 
"activity_where_[The visualizations are useful.]", "activity_where_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "Activity Location", 3, "tight")

# written tests
label_list = get_likert_scales_list(testing_written_dict, ["testing_written_[The visualization is understandable.]", 
"testing_written_[The visualization is useful.]", "testing_written_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "Written Tests", 3, "tight")

# TDD tests
label_list = get_likert_scales_list(testing_tdd_dict, ["testing_tdd_[The visualization is understandable.]",
"testing_tdd_[The visualization is useful.]", "testing_tdd_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "TDD cycles", 3, "tight")

# global stats
label_list = get_likert_scales_list(global_stats_dict, ["global_stats_[The table is understandable.]",
"global_stats_[The table is useful.]", "global_stats_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "Global Statistics", 3, "tight")

# privacy
label_list = get_likert_scales_list(privacy_dict, ["privacy_[The privacy settings are understandable.]", 
"privacy_[The privacy settings are useful.]", "privacy_[I would use this part of the dashboard.]"])
show_likert_scale_plot(label_list, "Privacy Settings", 3, "tight")

# closure
# input_data = sorted(closure_dict[" [I would use the dashboard I just saw.]"])
# show_bar_chart(input_data, '', '', 'I would use the dashboard I just saw.')
label_list = get_likert_scales_list(closure_dict, [" [I would use the dashboard I just saw.]"])
show_likert_scale_plot(label_list, "Closure", 1, "on")


#%%

### Combined Likert Results
# import operator
# def generate_grouped_bar_chart(categories_len, categories_list, input_list, label_list, title):
#     likert_scale_dict = {'strongly agree': [0] * categories_len, 'agree': [0] * categories_len, 'neutral': [0] * categories_len, 
#         'disagree': [0] * categories_len, 'strongly disagree': [0] * categories_len, 'no answer': [0] * categories_len}
    
#     zipped = zip(input_list, label_list)
#     for data, likert_scale in sorted(zipped, key=operator.itemgetter(1)):
#         index  = categories_list.index(data)
#         likert_scale_dict[likert_scale][index] += 1

#     performance = []
#     for value in likert_scale_dict.values():
#         performance.append(value)
    
#     show_grouped_bar_chart(categories_list, performance, 
#         ['strongly agree','agree', 'neutral', 'disagree', 'strongly disagree', 'no answer'], 
#         title)

# def generate_grouped_bar_chart_for_coding_exp(label_list, title):
#     year_list = list(dict.fromkeys(coding_exp_list))
#     year_len = len(year_list)
#     generate_grouped_bar_chart(year_len, year_list, coding_exp_list, label_list, title)

# # written tests
# generate_grouped_bar_chart_for_coding_exp(
#     testing_written_dict["testing_written_[The visualization is understandable.]"], 
#     'Year of Experience - written tests: The visualization is understandable')

# # activity types 
# generate_grouped_bar_chart_for_coding_exp(
#     activity_what_dict["activity_what_[The visualizations are understandable.]"], 
#     'Year of Experience - activity types: The visualization is understandable')

#%%
