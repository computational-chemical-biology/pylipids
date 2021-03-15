from flask import Flask, flash, render_template, request, redirect, url_for, send_file
from flask_dropzone import Dropzone

from api.compute import compute

import uuid
import json
import os
import re
import sys

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config.update(
    UPLOADED_PATH= 'api/static/uploads',
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='text',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/graph')
def graph():
    df = pd.read_csv('Advertising.csv', index_col=0)
    df.sort_values(['Sales'], inplace=True)
    fig = go.Figure()
    for cname in df.columns[:-1]:
        fig.add_scatter(x=df[cname], y=df['Sales'], name=cname, mode="markers")

    fig.update_layout(width=1600, height=800)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html',
                           ids='invest',
                           graphJSON=graphJSON)


@app.route('/table')
def table():
    df = pd.read_csv('Advertising.csv', index_col=0)

    #meas = [dffinal.iloc[i].to_dict() for i in range(dffinal.shape[0])]
    meas = [list(map(str, df.iloc[i].values)) for i in range(df.shape[0])]
    #meas = {'data': meas}
    ddffinal = json.dumps(meas, cls=NpEncoder)
    return render_template('table.html',
                           dffinal=ddffinal)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        filename = f'{str(uuid.uuid4())}_{f.filename}'
        f.save(os.path.join(app.config['UPLOADED_PATH'], filename))
    return render_template('upload.html')

@app.route('/analysis', methods=['POST', 'GET'])
def analysis():
    options = os.listdir(app.config['UPLOADED_PATH'])
    error = None
    if request.method == 'POST':
        form_dict = dict(request.form)
        data_list = request.form.getlist('category')
        try:
            compute(form_dict, data_list, str(uuid.uuid4()))
            flash('Sua análise foi executada!')
            return redirect(url_for('results'))
        except BaseException as e:
            error = str(e)
            print(error)
            render_template('analysis.html', options=options, error=error)
    return render_template('analysis.html', options=options, error=error)


@app.route('/results')
def results():
    fls = os.listdir('api/static/results')
    meas = [x.split('###') for x in fls]
    for i in range(len(meas)):
        tmp = meas[i]
        url = '/static/results/%s' % '###'.join(tmp)
        #link = f'<a href="{url}" target="_blank">File</a>'
        link = url
        tmp = [re.sub('.tsv$|.pdf$|.gml$', '', x) for x in tmp]
        tmp.append(link)
        meas[i] = tmp
    ddffinal = json.dumps(meas, cls=NpEncoder)
    return render_template('results.html',
                           dffinal=ddffinal)


@app.route('/download')
def download():
    taskid = request.args.get('taskid')
    dr = os.path.join('api/static/results')
    fls = os.listdir(dr)
    fls = [x for x in fls if taskid in x][0]
    fls = 'static/results/%s' % fls
    return send_file(fls, as_attachment=True)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
