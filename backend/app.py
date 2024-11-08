from flask import Flask, jsonify, request,send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime,re
from transformers import pipeline
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer, TFAutoModelForTokenClassification
from transformers import TFAutoModelForTokenClassification
from fuzzywuzzy import process
from sqlalchemy import extract
from time import time
from werkzeug.utils import secure_filename
import os
import json

# import nltk
# nltk.download('stopwords')

# import nltk
# from nltk.corpus import stopwords


# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))

# intent_model = TFAutoModelForSequenceClassification.from_pretrained("C:/Users/jogee/Desktop/ChatBOT/backend/ChatBotExampleIntentModel")
# intent_tokenizer = AutoTokenizer.from_pretrained("C:/Users/jogee/Desktop/ChatBOT/backend/ChatBotExampleIntentModel")
# intent_classifier = pipeline("text-classification", model=intent_model, tokenizer=intent_tokenizer)
entity_model = TFAutoModelForTokenClassification.from_pretrained("C:/Users/jogee/Desktop/ChatBOT/backend/Old Models/ChatBotExampleEntityModel")
entity_tokenizer = AutoTokenizer.from_pretrained("C:/Users/jogee/Desktop/ChatBOT/backend/Old Models/ChatBotExampleEntityModel")
entity_classifier = pipeline("ner", model=entity_model, tokenizer=entity_tokenizer)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/Chatbot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class PurchasedComponents(db.Model):
    __tablename__ = 'PurchasedComponents'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    vendor_name = db.Column(db.String(100))
    component_purchased = db.Column(db.String(100))
    quantity_purchased = db.Column(db.Integer)
    purchased_price = db.Column(db.Float)
    purchased_date = db.Column(db.Date)
    stock_entry = db.Column(db.String(50))
    invoice_no = db.Column(db.String(50))
    updated_date=db.Column(db.DateTime,default=datetime.datetime.now)
    filename = db.Column(db.String(100), nullable=False)
    supplied_to = db.Column(db.String(100), nullable=False)

    def __init__(self, vendor_name, component_purchased, quantity_purchased, purchased_price, purchased_date, stock_entry, invoice_no,filename,supplied_to):
        self.vendor_name = vendor_name
        self.component_purchased = component_purchased
        self.quantity_purchased = quantity_purchased
        self.purchased_price = purchased_price
        self.purchased_date = purchased_date
        self.stock_entry = stock_entry
        self.invoice_no = invoice_no
        self.filename = filename
        self.supplied_to = supplied_to


class PurchasedComponentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'vendor_name', 'component_purchased', 'quantity_purchased', 'purchased_price', 'purchased_date', 'stock_entry', 'invoice_no','updated_date','supplied_to')

purchased_component_schema = PurchasedComponentsSchema()
purchased_components_schema = PurchasedComponentsSchema(many=True)

def preprocess(string):
    string=string.rstrip()
    string=string.lower()
    string=string.title()
    return string




with app.app_context():
    db.create_all()
    

def get_entities(text):
    response=entity_classifier(text)

    d={}
    for i in response:
        if i['entity'] not in d:
            d[i['entity']]=[i['word']]
        else:
            d[i['entity']].append(i['word'])

    entities = {
        'components': '',
        'years': '',
        'vendors': '',
        'invoices': ''
        }
    labels = {
        'B-component': 'components',
        'I-component': 'components',
        'B-year': 'years',
        'I-year': 'years',
        'B-vendors': 'vendors',
        'I-vendors': 'vendors',
        'B-invoice': 'invoices',
        'I-invoice': 'invoices'
    }


    for i in d:
        arr=d[i]
        s=''
        for j in arr:
            s+=j
        entities[labels[i]]+=s

    for i in entities:
        entities[i]=entities[i].split('Ġ')
        
    for i in entities:
        arr=[]
        for j in entities[i]:
            if j!='':
                arr.append(j)
        entities[i]=arr

    for i in entities:
        if i=='components':
            s=''
            for j in entities[i]:
                s+=j
            entities[i]=s.strip()
        elif i=='vendors':
            s=''
            for j in entities[i]:
                s+=j
            entities[i]=s.strip()
    print(entities)
    return entities



def no_match():
    return 'Sorry! I am unable to understand your context. Could you please provide a bit more detail or rephrase your question?'


def year_only(d):
    res=''
    data=[]
    for i in d['years']:
        data = PurchasedComponents.query.filter(extract('year', PurchasedComponents.purchased_date) == i).all()
        data=purchased_components_schema.dump(data)
        if not d['isvendors'] and not d['iscomponents'] and not d['isinvoices']:
            if len(data)>0:
                res+=f'Here is the list of components purchased in the year {i}\n'
            else:
                res+=f'No components are purchased in the year {i}\n'
        elif not d['isvendors'] and not d['iscomponents'] and d['isinvoices']:
            invoice=d['invoices'][0]
            r={}
            for j in data:
                if j['invoice_no']==invoice:
                    r['vendor_name']=j['vendor_name']
                    r['component_purchased']=j['component_purchased']
                    r['quantity_purchased']=j['quantity_purchased']
                    r['purchased_price']=j['purchased_price']
                    r['purchased_date']=j['purchased_date']
                    r['stock_entry']=j['stock_entry']
                    r['invoice_no']=j['invoice_no']
            if len(r)>0:
                res+=f'Here is the list of components purchased in the year {i} with invoice {invoice}.'
                data=[]
                data.append(r)
            else:
                res+=f'I Cannot identify the Invoice {invoice} in the year {i}. However I can provide you the invoices in the year {i}.'
                r=[]
                for j in data:
                    k={}
                    k['invoice_no']=j['invoice_no']
                    k['purchased_date']=j['purchased_date']
                    r.append(k)
                data=r
        elif not d['isvendors'] and d['iscomponents'] and not d['isinvoices']:
            res+=f'I Cannot identify the Component you have specified in the year {i}. However I can provide you the list of components purchased in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['component_purchased']=j['component_purchased']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
        elif not d['isvendors'] and d['iscomponents'] and d['isinvoices']:
            res+=f'I Cannot identify the Component and Invoice you have specified in the year {i}. However I can provide you the list of Components purchased and Invoices in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['component_purchased']=j['component_purchased']
                k['invoice_no']=j['invoice_no']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
        elif d['isvendors'] and not d['iscomponents'] and not d['isinvoices']:
            res+=f'I Cannot identify the Vendor you have specified in the year {i}. However I can provide you the list of components purchased in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['vendor_name']=j['vendor_name']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
        elif d['isvendors'] and not d['iscomponents'] and d['isinvoices']:
            res+=f'I Cannot identify the Vendor and Invoice you have specified in the year {i}. However I can provide you the list of Vendors and Invoices in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['vendor_name']=j['vendor_name']
                k['invoice_no']=j['invoice_no']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
        elif d['isvendors'] and d['iscomponents'] and not d['isinvoices']:
            res+=f'I Cannot identify the Vendor and Component you have specified in the year {i}. However I can provide you the list of Vendors and Components purchased in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['vendor_name']=j['vendor_name']
                k['component_purchased']=j['component_purchased']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
        elif d['isvendors'] and d['iscomponents'] and d['isinvoices']:
            res+=f'I Cannot identify the Vendor,Component and Invoice you have specified in the year {i}. However I can provide you the list of Vendors, Invoices and Components purchased in the year {i}.'
            r=[]
            for j in data:
                k={}
                k['vendor_name']=j['vendor_name']
                k['component_purchased']=j['component_purchased']
                k['invoice_no']=j['invoice_no']
                k['purchased_date']=j['purchased_date']
                r.append(k)
            data=r
    return {'response':res,'data':data}


def year_and_component(d):
    # print(d)
    flag=False
    res=''
    c_data=[]
    data = PurchasedComponents.query.filter(extract('year', PurchasedComponents.purchased_date) == d['years'][0]).all()
    data=purchased_components_schema.dump(data)
    for i in d['components']:
        for j in data:
            if j['component_purchased']==i:
                flag=True
                r={}
                r['vendor_name']=j['vendor_name']
                r['component_purchased']=j['component_purchased']
                r['quantity_purchased']=j['quantity_purchased']
                r['purchased_price']=j['purchased_price']
                r['purchased_date']=j['purchased_date']
                r['stock_entry']=j['stock_entry']
                r['invoice_no']=j['invoice_no']
                c_data.append(r)
    if flag:
        res+=f'Here are the matches I have found for the Component you have specified in the year {d['years'][0]} '
    else:
        res+=f'I cannot identify the component you have specified {d['components'][0]} in the year {d['years'][0]}. However I can provide the list of components purchased in the year {d['years'][0]}.'
        c_data=data
    return {'response':res,'data':c_data}



def year_and_vendor(d):
    flag=False
    res=''
    c_data=[]
    data = PurchasedComponents.query.filter(extract('year', PurchasedComponents.purchased_date) == d['years'][0]).all()
    data=purchased_components_schema.dump(data)
    for i in d['vendors']:
        for j in data:
            if j['vendor_name']==i:
                flag=True
                r={}
                r['vendor_name']=j['vendor_name']
                r['component_purchased']=j['component_purchased']
                r['quantity_purchased']=j['quantity_purchased']
                r['purchased_price']=j['purchased_price']
                r['purchased_date']=j['purchased_date']
                r['stock_entry']=j['stock_entry']
                r['invoice_no']=j['invoice_no']
                c_data.append(r)
    if flag:
        res+=f'Here are the matches I have found for the Vendor you have specified in the year {d['years'][0]} '
    else:
        res+=f'I cannot identify the vendor you have specified {d['vendors'][0]} in the year {d['years'][0]}. However I can provide the list of components purchased in the year {d['years'][0]}.'
        c_data=data
    return {'response':res,'data':c_data}





def component_only(d):
    # print(d)
    res=''
    c_data=[]
    if len(d['components'])>1:
        res+='I found multiple matches for the Component you have specified. '
        for i in range(len(d['components'])):
            data = PurchasedComponents.query.filter_by(component_purchased=d['components'][i]).all()
            data=purchased_components_schema.dump(data)
            if i==len(d['components'])-1:
                res+=f'and {d['components'][i]}.'
            else:
                res+=f'{d['components'][i]}, '
            for j in data:
                c_data.append(j)
        res+=' Here are the details.'
    else:
        res+=f'I found a match for the Component you have specified. Here are the details of {d['components'][0]}'
        data = PurchasedComponents.query.filter_by(component_purchased=d['components'][0]).all()
        data=purchased_components_schema.dump(data)
        for j in data:
            c_data.append(j)
    return {'response':res,'data':c_data}


def vendor_only(d):
    res=''
    c_data=[]
    if len(d['vendors'])>1:
        res+='I found multiple matches for the Vendor you have specified. '
        for i in range(len(d['vendors'])):
            data = PurchasedComponents.query.filter_by(vendor_name=d['vendors'][i]).all()
            data=purchased_components_schema.dump(data)
            if i==len(d['vendors'])-1:
                res+=f'and {d['vendors'][i]}.'
            else:
                res+=f'{d['vendors'][i]}, '
            for j in data:
                c_data.append(j)
        res+=' Here are the details.'
    else:
        res+=f'I found a match for the Vendor you have specified. Here are the details of {d['vendors'][0]}'
        data = PurchasedComponents.query.filter_by(vendor_name=d['vendors'][0]).all()
        data=purchased_components_schema.dump(data)
        for j in data:
            c_data.append(j)
    return {'response':res,'data':c_data}


def invoice_only(d):
    res=''
    c_data=[]
    if len(d['invoices'])>1:
        res+='I found multiple matches for the Invoice you have specified. '
        for i in range(len(d['invoices'])):
            data = PurchasedComponents.query.filter_by(invoice_no=d['invoices'][i]).all()
            data=purchased_components_schema.dump(data)
            if i==len(d['invoices'])-1:
                res+=f'and {d['invoices'][i]}.'
            else:
                res+=f'{d['invoices'][i]}, '
            for j in data:
                c_data.append(j)
        res+=' Here are the details.'
    else:
        data = PurchasedComponents.query.filter_by(invoice_no=d['invoices'][0]).all()
        data=purchased_components_schema.dump(data)
        if len(data)>0:
            res+=f'I found a match for the Invoice you have specified. Here are the details of {d['invoices'][0]}'
            for j in data:
                c_data.append(j)
        else:
            res+=f'I cannot find the Invoice you have specified {d['invoices'][0]}'
    return {'response':res,'data':c_data}



def display_all():
    res='I am unable to understand the query you have asked. However I can give you the list of all the components in the database sorted by Purchased Date.'
    data=PurchasedComponents.query.order_by(PurchasedComponents.purchased_date).all()
    data=purchased_components_schema.dump(data)
    r=[]
    for j in data:
        k={}
        k['component_purchased']=j['component_purchased']
        k['vendor_name']=j['vendor_name']
        k['purchased_date']=j['purchased_date']
        r.append(k)
    data=r
    return {'response':res,'data':data}



def reply(entities):
    res=''
    d={
    'vendors':[],
    'components':[],
    'invoices':entities['invoices'],
    'years':entities['years'],
    'isvendors':True if len(entities['vendors'])>0 else False,
    'iscomponents':True if len(entities['components'])>0 else False,
    'isinvoices':True if len(entities['invoices'])>0 else False,
    'isyears':True if len(entities['years'])>0 else False
    }

    with app.app_context():
        all_component_purchased = [component_purchased.component_purchased for component_purchased in PurchasedComponents.query.all()]
        if len(entities['components'])>0:
            matches = process.extractBests(entities['components'], all_component_purchased, score_cutoff=70)

            component_purchased_names = [match[0] for match in matches]
            
            d['components']=list(set(component_purchased_names))
        if len(entities['vendors'])>0:
            all_vendors = [vendor.vendor_name for vendor in PurchasedComponents.query.all()]
            
            matches = process.extractBests(entities['vendors'], all_vendors, score_cutoff=70)

            vendor_names = [match[0] for match in matches]
            
            d['vendors']=list(set(vendor_names))
    if len(d['years'])>0:
        res=year_only(d)
    # elif len(d['years'])>0 and len(d['components'])>0 and len(d['vendors'])==0 and len(d['invoices'])==0:
    #     res=year_and_component(d)
    # elif len(d['years'])>0 and len(d['components'])==0 and len(d['vendors'])>0 and len(d['invoices'])==0:
    #     res=year_and_vendor(d)
    elif len(d['years'])==0 and len(d['components'])>0 and len(d['vendors'])==0 and len(d['invoices'])==0:
        res=component_only(d)
    elif len(d['years'])==0 and len(d['components'])==0 and len(d['vendors'])>0 and len(d['invoices'])==0:
        res=vendor_only(d)
    elif len(d['years'])==0 and len(d['components'])==0 and len(d['vendors'])==0 and len(d['invoices'])>0:
        res=invoice_only(d)
    else:
        res=display_all()
    print(d)
    return res



@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Invalid input"}), 400
    start_time=time()
    res=reply(get_entities(user_input))
    response_time=abs(start_time-time())
    response_time = round(response_time, 2)
    return jsonify({"response": res,"response_time":response_time})



@app.route('/get/options', methods=['GET'])
def get_options_for_supplied_to():
    dept=['IT Department','CSE Department','AE Department','CS-AIML Department','CS-DS Department','CS-IoT Department','CS-CYS Department','CSBS Department','CE Department','ECE Department','EEE Department','EIE Department','ME Department']
    q=PurchasedComponents.query.all()
    supplied_to_list = list(set([item.supplied_to for item in q]))
    for i in supplied_to_list:
        if i not in dept:
            dept.append(i)
    return jsonify(dept)




@app.route('/purchasedcomponents/postall',methods=['POST'])
def postall_purchased_components():
    try:
        with app.app_context():
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                vendor=preprocess(request.form.get('vendor'))
                PurchasedDate=preprocess(request.form.get('PurchasedDate'))
                InvoiceNo=preprocess(request.form.get('InvoiceNo'))
                suppliedTo=request.form.get('suppliedTo')
                print(suppliedTo)
                components=request.form.get('components')
                components = json.loads(components) if components else []
                for i in components:
                    selectedComponentPurchased=preprocess(i['selectedComponentPurchased'])
                    QuantityPurchased=i['QuantityPurchased']
                    PurchasedPrice=i['PurchasedPrice']
                    StockEntry=i['StockEntry']
                    row=PurchasedComponents(vendor,selectedComponentPurchased,QuantityPurchased,PurchasedPrice,PurchasedDate,StockEntry,InvoiceNo,filename,suppliedTo)
                    db.session.add(row)
                    db.session.commit()
                return '201'
            else:
                return '400'
    except:
        return '400'
    
    
@app.route('/view/<int:id>', methods=['GET'])
def view_pdf(id):
    pdf_file = PurchasedComponents.query.get_or_404(id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='application/pdf')
    else:
        return jsonify({"error": "File not found"}), 400

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
