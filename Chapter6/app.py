from flask import Flask, session, render_template, request
import os
import swimclub

app = Flask(__name__)
app.secret_key = 'vinay_secret_key'

def populate_swimmers():
    if 'swimmers' not in session:
        files = os.listdir(swimclub.FOLDER)
        if '.DS_Store' in files:
            files.remove('.DS_Store')
        session['swimmers'] = {}
        for f in files:
            swimmer, *_, = swimclub.read_swim_data(f)
            if swimmer not in session['swimmers']:
                session['swimmers'][swimmer] = []
            session['swimmers'][swimmer].append(f)

@app.route('/')
def hello_world():
    return render_template('index.html', title='Home')


@app.route('/swimmers')
def display_swimmers():
    populate_swimmers()
    # return str(sorted(session['swimmers']))
    return render_template('select.html', title='Select Swimmer', url='/showfiles', select_id='swimmer_name', data=session['swimmers'])

@app.post('/showfiles')
def display_swimmer_files():
    populate_swimmers()
    swimmer = request.form['swimmer_name']
    # return str(session['swimmers'][swimmer])
    return render_template('select.html', title='Select Swimmer\'s Event', url='/showchart', select_id='swimmer_file_name', data=session['swimmers'][swimmer])

@app.post('/showchart')
def display_swimmer_bar_chart():
    populate_swimmers()
    filename = request.form['swimmer_file_name']
    chartHtmlPath = swimclub.produce_bar_chart(filename, location='templates/')
    return render_template(chartHtmlPath.removeprefix('templates/'))
    
if __name__ == '__main__':
    app.run(debug=True)