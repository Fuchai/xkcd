from flask import Flask, render_template, send_from_directory
from flask.ext.wtf import Form
from wtforms import SelectField, DecimalField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from pwgen import makePasswordList, doLetterSubs
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.debug=True
app.secret_key = 'luthercollege'


class PWSelections(Form):
    minLength = SelectField('Minimum Word Length',
                            choices=[('3','3'),('4','4'),('5','5')])
    maxLength = SelectField('Maximum Word Length',
                   choices=[('4','4'),('5','5'),('6','6'),('7','7'),('8','8')])
    maxPwLen = DecimalField('Max Length',validators=[DataRequired()])
    alternate = BooleanField('Easy Typing')
    lettersubs = BooleanField('Number Substitutions')
    adverbs = BooleanField('Adjective, noun, verb, adverb style')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PWSelections()
    if form.validate_on_submit():
        minLength = int(form.minLength.data)
        maxLength = int(form.maxLength.data)
        maxPwLen = form.maxPwLen.data
        alt = form.alternate.data
        pwlist = makePasswordList(minLength, maxLength, maxPwLen, alt)
        if form.lettersubs.data:
            doLetterSubs(pwlist)
        return render_template('pwlist.html', pwlist=pwlist)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()
