from math import pi,sqrt 
import pandas as pd

file_location = ("https://raw.githubusercontent.com/TUDelft-CITG/"
                "learn-python/mike/book/06/Exercises/")


###================== NOTEBOOK 3=====================
def notebook_3_check_answer(question_number):

    if question_number == 0:
        try: 
            assert car_info[
                'top_speed'] in message and car_info[
                    'type'] in message, 'Incorrect answer.'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 1:
        try: 
            assert type(
                DegToRad) == type(
                lambda x:x) and abs(
                DegToRad(
                angle) - angle*pi/180) <= 1e-6, 'Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 2:
        try: 
            assert abs(
                Distance(
                1, 1, 3, 3) - 2 * sqrt(
                2)) <= 1e-6, '3.2.2 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')
    
    elif question_number == 3:
        try: 
            assert get_abbreviation(   
            ) == "AES", '3.4.1 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 4:
        try: 
            assert "B[3] = 8" in create_string_from_lists(
            ), '3.4.2 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 5:
        try: 
            assert factorial(
                5) == 120, '3.4.3 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')   

###==================NOTEBOOK 4=====================
def notebook_4_check_answer(question_number):

    if question_number == 0:
        try:
            assert get_display_temperature(
                [100]) == [
                    "-173.150  °C | -279.670  °F (ID=0)"
                    ], '4.1.1 - Incorrect answer' 
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 1:
        default_bands = ['B1', 'B2', 'B3', 'B4', 
                         'B5', 'B6', 'B7']
        d1 = prepare_template(default_bands, 'normal')
        d2 = prepare_template(default_bands, 'extended')
        d3 = prepare_template(default_bands, 'normal')
        try: 
            assert  d2['bands'] == ['B1', 'B2', 'B3', 'B4', 
                                   'B5', 'B6', 'B7', 'B8', 'B8A'] and \
                    d3['bands'] == ['B1', 'B2', 'B3', 'B4', 'B5', 
                        'B6', 'B7'], '4.1.2 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

###==================SOLUTIONS TEMPLATE=====================

###---------QUESTION 0 --------
# import time

# def get_display_temperature(temp_k):
#     #copying temporarily temp_k to temp_c
#     temp_c = temp_k.copy()
    
#     #converting kelvins to celsius
#     for i in range(len(temp_c)):
#         temp_c[i] = temp_c[i] - 273.15
        
#     #copying temporarily temp_k to temp_f
#     temp_f = temp_k.copy()
    
#     #converting kelvins to fahrenheit
#     for i in range(len(temp_f)):
#         temp_f[i] = (temp_f[i] - 273.15) * (9 / 5) + 32
    
#     #now, creating display messages from the converted temperatures
#     display_messages = []
#     for i in range(len(temp_k)):
#         msg = f"{temp_c[i]:<10.3f}°C | {temp_f[i]:<10.3f}°F (ID={i})"
#         display_messages.append(msg)
        
#     return display_messages
###------------END SOLUTION---------------------

###---------QUESTION 1 --------
# def prepare_template(default_bands, observation_mode):  
#     #creating metadata for the upcoming observations
#     template = {'time': time.ctime(time.time()),
#                'observation_mode': observation_mode,
#                'bands': default_bands.copy()}
    
#     #adding additional bands for the extended mode
#     if observation_mode == 'normal':
#         #no need to add bands
#         pass
#     elif observation_mode == 'extended':
#         template['bands'] += ['B8', 'B8A']
#     else:
#         #if the mode is unknonw - raise a RuntimeError
#         raise RuntimeError(f'Failed to identify observation mode: {observation_mode}')
        
#     return template
###------------END SOLUTION---------------------       
# 
###===========================================================

###==================NOTEBOOK 6=====================

def solution_6_2_1(series):
    series_types = "Types inside series:\n"
    for i in range(len(series)):
        item_type = type(series[i])
        series_types += str(item_type) + '\n'
    return series_types

def notebook_6_check_answer(question_number):

    if question_number == 0:
        my_list = ['begin', 2, 3/4, "end"]
        my_series = pd.Series(data=my_list)
        try: 
            assert list_types(
                my_series) == solution_6_2_1(
                my_series), '6.2.1 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 1:
        try: 
            assert count_nans(
                mineral_properties) == 12,'Incorrect'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 2:
        try: 
            assert count_minerals(
                mineral_properties, 4) == 7, 'Incorrect'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')
    
    elif question_number == 3:
        df_sol = pd.read_csv(file_location + 'tallest_mountains.csv')
        cols_sol = df_sol.columns
        max_height_sol = df_sol['Metres'].max() 
        indxmax_sol = df_sol['Metres'].idxmax() 
        tallest_mountain_sol = df_sol.loc[indxmax_sol,'Mountain']
        try: 
            assert df_sol.equals(
                mountains_8000) and cols_sol.equals(
                cols) and max_height_sol == max_height and \
        indxmax_sol == index_max and tallest_mountain_sol == tallest_mountain, \
    '6.5.1 - Incorrect answer, did you use idxmax for the 4th problem?'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 4:
        df_sol = pd.read_csv(file_location + 'tallest_mountains.csv')

        df7000_sol = pd.read_csv(
            file_location + 'mountains_above_7000m.csv', encoding_errors='ignore') # 1
        df_concat_sol = pd.concat([df7000_sol,df_sol]) # 2
        df_concat_norange_sol = df_concat_sol .drop('Range', axis=1) # 3
        df_reset_sol = df_concat_norange_sol.reset_index(drop=True) # 4
        missing_feet_series_sol = df_reset_sol["Feet"].isnull() # 5
        with_feet_series_sol = df_reset_sol["Feet"].mask(
            missing_feet_series_sol, df_reset_sol["Metres"]*3.28084) # 6
        df_reset_sol["Feet"] = with_feet_series_sol

        or_df7000_sol = pd.read_csv(
            file_location + 'mountains_above_7000m.csv', encoding_errors='ignore') # 1
        or_df_concat_sol = pd.concat([df_sol,or_df7000_sol]) # 2
        or_df_concat_norange_sol = or_df7000_sol.drop('Range', axis=1) # 3
        or_df_reset_sol = or_df_concat_norange_sol.reset_index(drop=True) # 4
        or_missing_feet_series_sol = or_df_reset_sol["Feet"].isnull() # 5
        or_with_feet_series_sol = or_df_reset_sol["Feet"].mask(
            or_missing_feet_series_sol, or_df_reset_sol["Metres"]*3.28084) # 6
        or_df_reset_sol["Feet"] = or_with_feet_series_sol
        try: 
            assert df_reset_sol.equals(df_reset) or \
                or_df_reset_sol.equals(df_reset), '6.5.2 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')

    elif question_number == 5:
        df_sol = pd.read_csv(file_location + 'tallest_mountains.csv')

        df7000_sol = pd.read_csv(
            file_location + 'mountains_above_7000m.csv', encoding_errors='ignore') # 1
        df7000_norange_sol = df7000_sol.drop('Range', axis=1) # 2
        df_concat_sol = pd.concat([df7000_norange_sol,df_sol]) # 3
        df_reset_sol = df_concat_sol.reset_index(drop=True) # 4
        missing_feet_series_sol = df_reset_sol["Feet"].isnull() # 5
        with_feet_series_sol = df_reset_sol["Feet"].mask(
            missing_feet_series_sol, df_reset_sol["Metres"]*3.28084) # 6
        df_reset_sol["Feet"] = with_feet_series_sol

        china_mountains_sol = df_reset_sol[
            "Location and Notes"].str.contains("China", case=True).sum()

        try: 
            assert china_mountains_sol == \
                  china_mountains, '6.5.3 - Incorrect answer'
            print('Correct answer :D')
        except AssertionError:
            print('Incorrect answer :(')     