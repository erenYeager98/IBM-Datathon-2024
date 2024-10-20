from flask import Flask, request, jsonify,render_template,redirect
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd

columns = [
    'age',
    'feeling_sad_or_tearful_No',
    'feeling_sad_or_tearful_Sometimes',
    'feeling_sad_or_tearful_Yes',
    'irritable_towards_baby_and_partner_No',
    'irritable_towards_baby_and_partner_Sometimes',
    'irritable_towards_baby_and_partner_Yes',
    'trouble_sleeping_at_night_No',
    'trouble_sleeping_at_night_Two or more days a week',
    'trouble_sleeping_at_night_Yes',
    'overeating_or_loss_of_appetite_No',
    'overeating_or_loss_of_appetite_Sometimes',
    'overeating_or_loss_of_appetite_Yes',
    'feeling_of_guilt_Maybe',
    'feeling_of_guilt_No',
    'feeling_of_guilt_Yes',
    'problems_of_bonding_with_baby_No',
    'problems_of_bonding_with_baby_Sometimes',
    'problems_of_bonding_with_baby_Yes',
    'suicide_attempt_No',
    'suicide_attempt_Not interested to say',
    'suicide_attempt_Yes'
]

app = Flask(__name__)
CORS(app)
model=load_model('postpartum.h5')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/ppd-test', methods=['GET'])
def ppd_test():
    return render_template('ppd-test.html')

@app.route('/ppd-test-result', methods=['POST'])
def ppd_test_result():
    data = request.form.to_dict()
    print(data)
    # Age group mapping
    age_group = {
        '25-30': 1,
        '30-35': 2,
        '35-40': 3,
        '40-45': 4,
        '45-50': 5
    }

    # Create a single row DataFrame with the one-hot encoded data
    df = pd.DataFrame([{
        'age': age_group[data['age']],  # Map age using age_group dictionary
        'feeling_sad_or_tearful_No': 1 if data['feelingSad'] == 'no' else 0,
        'feeling_sad_or_tearful_Sometimes': 1 if data['feelingSad'] == 'sometimes' else 0,
        'feeling_sad_or_tearful_Yes': 1 if data['feelingSad'] == 'yes' else 0,
        'irritable_towards_baby_and_partner_No': 1 if data['irritable'] == 'no' else 0,
        'irritable_towards_baby_and_partner_Sometimes': 1 if data['irritable'] == 'sometimes' else 0,
        'irritable_towards_baby_and_partner_Yes': 1 if data['irritable'] == 'yes' else 0,
        'trouble_sleeping_at_night_No': 1 if data['troubleSleeping'] == 'no' else 0,
        'trouble_sleeping_at_night_Two or more days a week': 1 if data['troubleSleeping'] == 'two_or_more_days_a_week' else 0,
        'trouble_sleeping_at_night_Yes': 1 if data['troubleSleeping'] == 'yes' else 0,
        'concentrationProblems_No': 1 if data['concentrationProblems'] == 'no' else 0,
        'concentrationProblems_Sometimes': 1 if data['concentrationProblems'] == 'sometimes' else 0,
        'concentrationProblems_Yes': 1 if data['concentrationProblems'] == 'yes' else 0,
        'overeating_or_loss_of_appetite_No': 1 if data['appetiteChanges'] == 'no' else 0,
        'overeating_or_loss_of_appetite_Sometimes': 1 if data['appetiteChanges'] == 'sometimes' else 0,
        'overeating_or_loss_of_appetite_Yes': 1 if data['appetiteChanges'] == 'yes' else 0,
        'feeling_of_guilt_Maybe': 1 if data['feelingAnxiety'] == 'maybe' else 0,
        'feeling_of_guilt_No': 1 if data['feelingAnxiety'] == 'no' else 0,
        'feeling_of_guilt_Yes': 1 if data['feelingAnxiety'] == 'yes' else 0,
        'problems_of_bonding_with_baby_No': 1 if data['bondingProblems'] == 'no' else 0,
        'problems_of_bonding_with_baby_Sometimes': 1 if data['bondingProblems'] == 'sometimes' else 0,
        'problems_of_bonding_with_baby_Yes': 1 if data['bondingProblems'] == 'yes' else 0,
        'suicide_attempt_No': 1 if data['suicidalThoughts'] == 'no' else 0,
        'suicide_attempt_Not interested to say': 1 if data['suicidalThoughts'] == 'not_interested_to_say' else 0,
        'suicide_attempt_Yes': 1 if data['suicidalThoughts'] == 'yes' else 0
    }])

    output = model.predict(df)
    print(output)
    print(output.shape)

    if output > 0.5:
        print('Positive')
        return render_template('positive.html')
    else:
        print('Negative')
        return render_template('negative.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chat-bot.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)



#data = request.form.to_dict()
    # print(data)
    # pd_data = pd.DataFrame([data])
    # age_group = {'25-30': 1,
    #              '30-35': 2,
    #              '35-40': 3,
    #              '40-45': 4,
    #              '45-50': 5}
    # pd_data['age'] = age_group[pd_data['age'][0]]
    # pd_data = pd.get_dummies(data=pd_data, columns=pd_data.columns[1:])
    # print(pd_data.head())
    # print(pd_data.columns)
    # print(pd_data.shape)
    # output = model.predict(pd_data)
    # print(output)