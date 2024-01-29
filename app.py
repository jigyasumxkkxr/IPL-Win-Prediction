import streamlit as st
import pickle
import pandas as pd
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Chennai Super Kings',
         'Delhi Capitals',
         'Kings XI Punjab',
         'Rajasthan Royals']
city = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
        'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
        'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
        'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
        'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
        'Sharjah', 'Mohali', 'Bengaluru']
pipe = pickle.load(open("pipe.pkl", "rb"))
st.title("IPL-Win-Predictor")
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select Batting Team", (sorted(teams)))
with col2:
    bowling_team = st.selectbox("Select Bowling Team", sorted(teams))
selected_city = st.selectbox("Select Host Team", sorted(city))
target = st.number_input("Target")
col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input("Score")
with col4:
    overs = st.number_input("Overs Completed")
with col5:
    wickets = st.number_input("Wickets_Out")
if st.button("Predict Probability"):
    runs_left = target - score
    balls_left = 120 - overs * 6
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left
    input_df = pd.DataFrame({
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "city": selected_city,
        "runs_left": runs_left,
        "balls_left": balls_left,
        "wickets_left": wickets,
        "total_runs_x": target,
        "crr": crr,
        "rrr": rrr
    }, index=[0])
    if batting_team==bowling_team or score>=target or score<0 or overs>20 or overs<=0 or wickets>10 or wickets<0:
        if score==target:
            st.text(batting_team+" Wins")
        else:
            st.text("Give Correct Data")
    else:
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        wins = result[0][1]
        st.text(batting_team + "-" + str(round(wins * 100)) + "%")
        st.text(bowling_team + "-" + str(round(loss * 100)) + "%")
