from flask import Flask, render_template, request
import pandas as pd
import h2o 
from h2o.automl import H2OAutoML
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
h2o.init()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/EDA')
def EDA():
    return render_template('EDA.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/model1', methods=['GET','POST'])
def model1():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        page=[]
        for i in range(24):
            page.append(request.form['page'+str(i+1)])

        columns=['data','time',
         'BASKETLOADPAGE_total','CATEGORYDEPARTMENT_total','CATEGORYQUICKBROWSE_total','CATEGORYSTANDARD_total',
        'CHECKOUTBASKET_total','CHECKOUTPRODUCTUPSELLGROUP_total','DAILYSALESCLOSEOUTPAGE_total',
        'DAILYSALESEVENTPAGE_total',
        'DAILYSALESMAINPAGE_total',
        'DAILYSALESPRODUCTPAGE_total',
        'DAILYSALESSOLREVENTPAGE_total',
        'HOMEPAGE_total',
        'KEYWORDSEARCH_total',
        'PRODUCTKIT_total',
        'PRODUCTOPTIONSKU_total',
        'PRODUCTSIMPLESKU_total',
        'SAVETOBOARDMODALSCREEN_total',
        'STLLANDINGPAGE_total',
        'SUPERBROWSECATEGORY_total',
        'SUPERBROWSECATEGORY1ATTRIBUTES_total',
        'SUPERBROWSECATEGORY2ATTRIBUTES_total',
        'SUPERBROWSECATEGORY3ATTRIBUTES_total',
        'SUPERBROWSECATEGORY4+ATTRIBUTES_total',
        'SUPERBROWSEHOTDEALS_total']
        df = pd.DataFrame(columns=columns)
        input_list = []
        input_list.append(date)
        input_list.append(time)
        for i in range(24):
            input_list.append(page[i])
        df.loc[0]=input_list
        class_model = h2o.load_model('StackedEnsemble_AllModels_AutoML_20181214_163440')
        result = class_model.predict(h2o.H2OFrame(df))           
        return render_template('model1.html', data = result.as_data_frame().to_html())
    return render_template('model1.html')

@app.route('/model2',methods=['GET','POST'])
def model2():
    if request.method == 'POST':
        regression_input = []
        columns=['zipcode',              
        'quantity_ordered',    
        'weight',                
        'num_reviews',            
        'onsite_price',           
        'on_promotion',                    
        'num_returns',           
        'Friday',              
        'Monday',               
        'Saturday',            
        'Sunday',               
        'Thursday',             
        'Tuesday',              
        'Wednesday',            
        'afternoon',            
        'evening',              
        'morning',              
        'description_length',   
        'category_count',       
        'manu_count',           
        'category_rating',
        'manufacturer_rating']
        df = pd.DataFrame(columns=columns)
        regression_input.append(request.form['zipcode'])
        regression_input.append(request.form['quantity'])
        regression_input.append(request.form['weight'])
        regression_input.append(request.form['num-views'])
        regression_input.append(request.form['price'])
        regression_input.append(request.form['promotion'])
        regression_input.append(request.form['tax'])
        date = request.form['date']
        time = request.form['time']
        days = ['Friday',              
        'Monday',               
        'Saturday',            
        'Sunday',               
        'Thursday',             
        'Tuesday',              
        'Wednesday']
        for i in days:
            if date == i:
                regression_input.append('1')
            else:
                regression_input.append('0')
        for i in ['afternoon','evening','morning']:
            if time == i:
                regression_input.append('1')
            else:
                regression_input.append('0')
        
        regression_input.append(request.form['description'])
        regression_input.append(request.form['category'])
        regression_input.append(request.form['manufacturer'])
        regression_input.append(request.form['category-ratio'])
        regression_input.append(request.form['manufacturer-ratio'])
        df.loc[0] = regression_input

        data = pd.read_csv('regression_data.csv')
        features = data.drop(columns=['order_value']).values
        target = data.order_value.values
        X_train, X_test, y_train, y_test = train_test_split(features, target, train_size=0.07, test_size=0.93)
        clf = RandomForestRegressor(n_estimators= 1000, random_state= 42)
        clf.fit(X_train, y_train)
        reg_result = clf.predict(df)
        return render_template('model2.html',data=reg_result[0]) 
    return render_template('model2.html')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)