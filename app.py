from flask import Flask, jsonify, request, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import plotly.express as px
import json
import plotly
from flask_cors import CORS

static_folder_path = 'C:\\Users\\Work\\Downloads\\Static'

app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/consumer_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ConsumerData(db.Model):
    __tablename__ = 'consumer_data'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    item = db.Column(db.String)
    all_consumer_units = db.Column(db.Integer)
    gen_z = db.Column(db.Integer)
    millennials = db.Column(db.Integer)
    gen_x = db.Column(db.Integer)
    baby_boomers = db.Column(db.Integer)
    silent_generation = db.Column(db.Integer)
    main_category = db.Column(db.String)
    subcategory = db.Column(db.String)

@app.route('/')
def index():
    image_url = url_for('static', filename='murder_mystery.png')
    return render_template_string(HTML_TEMPLATE, image_url=image_url)

@app.route('/get-dropdown-options', methods=['GET'])
def get_dropdown_options():
    column = request.args.get('column')
    main_category = request.args.get('main_category', '')
    subcategory = request.args.get('subcategory', '')
    query = db.session.query(getattr(ConsumerData, column)).distinct()
    if main_category:
        query = query.filter(ConsumerData.main_category == main_category)
    if subcategory and column == 'item':
        query = query.filter(ConsumerData.subcategory == subcategory)
    options = [option[0] for option in query.order_by(getattr(ConsumerData, column))]
    return jsonify(options)

@app.route('/get-chart-data', methods=['POST'])
def get_chart_data():
    data = request.json
    filter_conditions = []
    if 'years' in data and data['years']: 
        filter_conditions.append(ConsumerData.year.in_(data['years']))
    if 'mainCategory' in data and data['mainCategory']:
        main_category = data['mainCategory'][0] if isinstance(data['mainCategory'], list) else data['mainCategory']
        filter_conditions.append(ConsumerData.main_category == main_category)
    if 'subcategory' in data and data['subcategory']:
        subcategory = data['subcategory'][0] if isinstance(data['subcategory'], list) else data['subcategory']
        filter_conditions.append(ConsumerData.subcategory == subcategory)
    if 'item' in data and data['item']:
        item = data['item'][0] if isinstance(data['item'], list) else data['item']
        filter_conditions.append(ConsumerData.item == item)
    query = db.session.query(ConsumerData).filter(*filter_conditions)
    df = pd.read_sql(query.statement, db.engine)
    if df.empty:
        return jsonify({"error": "No data available for the selected filters."})
    if 'generations' in data and data['generations']:
        generation_columns = [gen for gen in data['generations'] if gen in df.columns and hasattr(ConsumerData, gen)]
        if generation_columns:
            df_melted = pd.melt(df, id_vars=['year'], value_vars=generation_columns, var_name='generation', value_name='value')
        else:
            return jsonify({"error": "Selected generations do not exist in the data."})
    else:
        df_melted = df
    try:
        chart_title = data.get('mainCategory')[0] if isinstance(data.get('mainCategory'), list) else data.get('mainCategory')
        subcategory_label = data.get('subcategory')[0] if isinstance(data.get('subcategory'), list) else data.get('subcategory')
        if data.get('chartType') == 'line':
            fig = px.line(df_melted, x='year', y='value', color='generation', title=chart_title, labels={'year': 'Year', 'value': subcategory_label})
        elif data.get('chartType') == 'scatter':
            fig = px.scatter(df_melted, x='year', y='value', color='generation', title=chart_title, labels={'year': 'Year', 'value': subcategory_label})
        elif data.get('chartType') == 'bar':
            fig = px.bar(df_melted, x='year', y='value', color='generation', barmode='group', title=chart_title, labels={'year': 'Year', 'value': subcategory_label})
        elif data.get('chartType') == 'pie':
            df_aggregated = df_melted.groupby('generation').sum().reset_index()
            fig = px.pie(df_aggregated, names='generation', values='value', title=chart_title)
        else:
            return jsonify({"error": "Unsupported chart type."})
    except Exception as e:
        return jsonify({"error": str(e)})
    chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(chart=chart)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: rgba(243,50,94,255);
            color: #333;
        }
        .filter-container {
            background-color: rgba(10,105,134,255);
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .filter-title {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
        }
        .form-check-label, .form-control, .custom-control-label {
            font-size: 14px;
            color: #fff;
        }
        .navbar, .footer {
            background-color: rgba(10,105,134,255);
            color: #fff;
        }
        .btn-primary {
            background-color: rgba(243,50,94,255);
            border-color: rgba(243,50,94,255);
        }
        .btn-primary:hover {
            background-color: rgba(243,50,94,200);
            border-color: rgba(243,50,94,200);
        }
        .custom-control-input:checked~.custom-control-label::before {
            color: #fff;
            background-color: rgba(243,50,94,255);
        }
        .banner-image {
            max-width: 85%;
            max-height: 225px;
            width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            margin-bottom: 20px;
        }
        .form-control {
            color: #333;
            background-color: #fff;
        }
        .form-control:focus {
            border-color: rgba(243,50,94,255);
            box-shadow: 0 0 0 0.2rem rgba(243,50,94,0.25);
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <img src="{{ image_url }}" alt="Banner" class="banner-image">
        <h2 class="mb-4 text-center">Consumer Data Visualization</h2>
        <div class="filter-container">
            <div class="filter-title">Filters</div>
            <div class="row">
                <div class="col-md-4">
                    <label>Generation:</label>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="generation" value="gen_z" id="gen_z" checked>
                        <label class="form-check-label" for="gen_z">Gen Z</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="generation" value="millennials" id="millennials" checked>
                        <label class="form-check-label" for="millennials">Millennials</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="generation" value="gen_x" id="gen_x" checked>
                        <label class="form-check-label" for="gen_x">Gen X</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="generation" value="baby_boomers" id="baby_boomers" checked>
                        <label class="form-check-label" for="baby_boomers">Baby Boomers</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="generation" value="silent_generation" id="silent_generation" checked>
                        <label class="form-check-label" for="silent_generation">Silent Generation</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <label>Year:</label>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="year" value="2019" id="year_2019" checked>
                        <label class="form-check-label" for="year_2019">2019</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="year" value="2020" id="year_2020" checked>
                        <label class="form-check-label" for="year_2020">2020</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="year" value="2021" id="year_2021" checked>
                        <label class="form-check-label" for="year_2021">2021</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" name="year" value="2022" id="year_2022" checked>
                        <label class="form-check-label" for="year_2022">2022</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <label>Chart Type:</label>
                    <div class="custom-control custom-radio">
                        <input type="radio" id="line" name="chartType" value="line" class="custom-control-input" checked>
                        <label class="custom-control-label" for="line">Line Chart</label>
                    </div>
                    <div class="custom-control custom-radio">
                        <input type="radio" id="bar" name="chartType" value="bar" class="custom-control-input">
                        <label class="custom-control-label" for="bar">Bar Chart</label>
                    </div>
                    <div class="custom-control custom-radio">
                        <input type="radio" id="pie" name="chartType" value="pie" class="custom-control-input">
                        <label class="custom-control-label" for="pie">Pie Chart</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <label>Main Category:</label>
                    <select id="main_category-dropdown" class="form-control" multiple></select>
                </div>
                <div class="col-md-4">
                    <label>Subcategory:</label>
                    <select id="subcategory-dropdown" class="form-control" multiple></select>
                </div>
                <div class="col-md-4">
                    <label>Metric:</label>
                    <select id="item-dropdown" class="form-control" multiple></select>
                </div>
            </div>
            <div class="text-center mt-3">
                <button type="button" id="load-chart" class="btn btn-primary">Load Chart</button>
            </div>
        </div>
        <div id="chart" class="mt-4"></div>
    </div>

    <footer class="footer bg-primary text-white mt-5">
        <div class="container">
            <p class="m-0 text-center">© 2024 Consumer Data Visualization, Inc.</p>
        </div>
    </footer>

    <script>
    $(document).ready(function() {
        function populateDropdown(column, additionalParams = {}) {
            let url = '/get-dropdown-options?column=' + column;
            for (const key in additionalParams) {
                url += '&' + key + '=' + encodeURIComponent(additionalParams[key]);
            }

            $.get(url, function(data) {
                let select = $('#' + column + '-dropdown');
                select.empty();
                data.forEach(function(option) {
                    select.append($('<option>', {value: option, text: option}));
                });
            });
        }

        populateDropdown('main_category', { year: $('input[name="year"]:checked').map(function() { return this.value; }).get() });
        populateDropdown('subcategory', { main_category: $('#main_category-dropdown').val() });
        populateDropdown('item', { subcategory: $('#subcategory-dropdown').val() });

        $('#load-chart').click(function() {
            let selectedGenerations = $('input[name="generation"]:checked').map(function() { return this.value; }).get();
            let selectedYears = $('input[name="year"]:checked').map(function() { return this.value; }).get();
            let selectedMainCategory = $('#main_category-dropdown').val();
            let selectedSubcategory = $('#subcategory-dropdown').val();
            let selectedItem = $('#item-dropdown').val();
            let selectedChartType = $('input[name="chartType"]:checked').val();

            $.ajax({
                url: '/get-chart-data',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    generations: selectedGenerations,
                    years: selectedYears,
                    mainCategory: selectedMainCategory,
                    subcategory: selectedSubcategory,
                    item: selectedItem,
                    chartType: selectedChartType
                }),
                success: function(response) {
                    var chartData = JSON.parse(response.chart);
                    var layout = {
                        xaxis: {
                            tickmode: 'array',
                            tickvals: chartData.x // Assuming this is an array of years
                        }
                        // Other layout settings
                    };
                    Plotly.newPlot('chart', chartData.data, layout);
                },
                error: function(error) {
                    console.error("Error loading chart:", error.responseText);
                }
            });
        });
    });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, host='192.168.50.231', port=5000)
