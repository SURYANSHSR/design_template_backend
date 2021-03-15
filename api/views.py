from django.http import JsonResponse
import sqlite3
import pandas as pd
import json
import time
milliseconds = int(round(time.time() * 1000))

values = [milliseconds,"10.00R20","123" ];
con = sqlite3.connect('./tyredata.sqlite')
cursorObj = con.cursor()
cursorObj.execute("create table if not exists tes (pattern_name TEXT primary key not null, size TEXT, load_index TEXT);")
cursorObj.execute('insert into tes ("pattern_name","size","load_index") values (?,?,?)',values)
con.commit()
cursorObj.execute("SELECT * FROM 'tes' ;")

print(123)
rows = cursorObj.fetchall()
rs = pd.DataFrame(data=rows, columns=["pattern_name", "size", "load_index"])
# print(rs)
js = rs.to_json()
ps = json.loads(js)


def save_result(request):

    # table_data = json.loads(request.POST.get('MyData'))
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    print(data)

    return JsonResponse(data)
# to the the api


def check(request):
    data = {
        'hello': 'world',
    }
    print(data)

    return JsonResponse(ps)


def sqlquery(request):
    print(request.resolver_match.kwargs.get('url_param'))
    print(request.GET.get('q', ''))
    report_no = request.GET.get('q', '')
    con = sqlite3.connect('./pr.sqlite')
    cursorObj = con.cursor()
    cursorObj.execute(request.GET.get('q', ''))
    rows = cursorObj.fetchall()
    rs = pd.DataFrame(data=rows, columns=["sl_no", "report_no", "test_no", "test_description", "inspection_date", "region", "customer", "location", "site_type", "operation_type", "tyre_productcode", "otr_or_farm", "tyre_size", "tyre_make", "tyre_pattern", "tyre_pr", "category_code", "tt_tl", "compound", "site_or_project", "vehicle_make", "vehicle_model", "vehicle_no", "tyre_sl_no", "fitment_date", "fitment_position", "ip", "hardness", "fitment_hmr", "current_hmr", "previous_wheel_hmr", "till_date_hmr", "fitment_kms", "current_kms", "previous_wheel_kms", "till_date_kms", "otd", "rtd1", "rtd2", "avg_rtd", "percentage_wear", "wearrate_hmr", "projected_life_hmr", "wearrate_kms", "projected_life_kms", "remarks"
                                          ])
    print(rs)

    js = rs.to_json()
    ps = json.loads(js)

    data = {
        'hello': request.GET.get('q', ''),
    }
    print(data)

    return JsonResponse(ps)


def reportdetails(request):

    report_no = request.GET.get('q', '')
    con = sqlite3.connect('./pr.sqlite')
    cursorObj = con.cursor()
    print(report_no)
    query='SELECT * FROM "pr_performance_data" WHERE report_no = "'+report_no +'" '
    print(query)
    cursorObj.execute(query)
    #cursorObj.execute('SELECT * FROM "pr_pr" WHERE report_no = "RN/01/2020/01A" ')
    rows = cursorObj.fetchall()
    rs = pd.DataFrame(data=rows, columns=["sl_no", "report_no", "test_no", "test_description", "inspection_date", "region", "customer", "location", "site_type", "operation_type", "tyre_productcode", "otr_or_farm", "tyre_size", "tyre_make", "tyre_pattern", "tyre_pr", "category_code", "tt_tl", "compound", "site_or_project", "vehicle_make", "vehicle_model", "vehicle_no", "tyre_sl_no", "fitment_date", "fitment_position", "ip", "hardness", "fitment_hmr", "current_hmr", "previous_wheel_hmr", "till_date_hmr", "fitment_kms", "current_kms", "previous_wheel_kms", "till_date_kms", "otd", "rtd1", "rtd2", "avg_rtd", "percentage_wear", "wearrate_hmr", "projected_life_hmr", "wearrate_kms", "projected_life_kms","running_or_removed","removal_date", "remarks"
                                          ])
   

    js = rs.to_json()
    ps = json.loads(js)
    image_data=get_summary_data(rs)
    #performance_data=get_performance_data(rs)

    report_details = { 
        'raw_data': ps,
        'performance_data':"",
        'summary_data':"",
        'image_data':image_data
    }
   

    return JsonResponse(report_details)

def get_summary_data(rs):
    rs_plot = rs[['fitment_position','avg_rtd']]
    rs_plot['avg_rtd']=pd.to_numeric(rs_plot['avg_rtd'])
    rs_plot=rs_plot.groupby('fitment_position').mean()
    import matplotlib.pyplot as plt
    fig=rs_plot.plot.bar().get_figure()

    import base64
    import io 
    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    ENCODING = 'utf-8'

    base64_string = pic_hash.decode(ENCODING)
    #pic_hash = json.loads(pic_hash)
    raw_data = {'IMAGE_NAME': base64_string}

    # now: encoding the data to json
    # result: string
    from json import dumps
    report_image = dumps(raw_data, indent=2)
    


    return base64_string

def get_performance_data(rs):
    rs_pd = rs[['tyre_sl_no','fitment_position','otd','avg_rtd', 'till_date_hmr','projected_life_hmr','running_or_removed','remarks']]
    rs_pd['avg_rtd']=pd.to_numeric(rs_pd['avg_rtd'])
    js = rs_pd.to_json()
    ps = json.loads(js)
    return ps




def allreports(request):
    con = sqlite3.connect('./pr.sqlite')
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM 'pr_report_index' ;")
    rows = cursorObj.fetchall()
    rs = pd.DataFrame(data=rows, columns=["report_no", "test_no", "test_description", "inspection_date", "region", "customer", "location", "site_type", "operation_type", "product_code", "product_group", "tyre_size"
                                          ])
    print(rs)

    js = rs.to_json()
    ps = json.loads(js)

    data = {
        'hello': request.GET.get('q', ''),
    }
    print(data)

    return JsonResponse(ps)

