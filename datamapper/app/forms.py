from flask.ext.wtf import Form
from wtforms.fields import (SubmitField, SelectField, DateField)
from wtf.validators import Required 


class DataSetForm(Form):
    """docstring for DataSetForm"""
    data_set = SelectField('Select Data Set:', choices=[], validators=[Required('This field is required.')])
    date_start = DateField('Start date range: ', validators=[Required('This field is required.')])
    date_end = DateField('End date range: ')
    submit = SubmitField('Submit')
