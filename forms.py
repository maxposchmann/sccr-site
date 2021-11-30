from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length, InputRequired
from datetime import datetime

import pandas as pd
db = 'SelfConsistentCFBRanker/ncaafb.p'
d = pd.read_pickle(db)

teams = d['data']['teams']

class selectTeam(FlaskForm):
    myField = SelectField('Team', choices=teams,default =teams[0], validators=[DataRequired()])
