from flask import Flask, render_template, request
from flask_dropzone import Dropzone

import uuid
import json
import os

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

app.config.update(
    UPLOADED_PATH= 'static/uploads',
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='text',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)

@app.route('/')
def index():
    return 'Hello, World!'

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
    if request.method == 'POST':
        form_dict = request.form
        as_dict = request.form.getlist('category')
        print(form_dict)
        print(as_dict)
    return render_template('analysis.html', options=options)



if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
