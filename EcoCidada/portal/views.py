from django.shortcuts import render
from django.http import HttpResponse
import requests, json, csv
import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
from django.conf import settings
import mimetypes

def data_parser(response):

    print(json.loads(response))
    df = pd.DataFrame.from_dict(json.loads(response))
    table = []
    for row in df['features']:
        contrib_id = row['location']['id']
        device_id = row['display_field']['value']
        coordinate_x = row['geometry']['coordinates'][0]
        coordinate_y = row['geometry']['coordinates'][1]
        report_type = row['properties']['report_type']

        if(report_type < 28):
            input = row['properties']['input']
            if (report_type == 21):
                report_type = "oxigenio dissolvido"
            elif (report_type == 22):
                report_type = "amonia"
            elif (report_type == 23):
                report_type = "nitrato"
            elif (report_type == 24):
                report_type = "nitrito"
            elif (report_type == 25):
                report_type = "ortofosfato"
            elif (report_type == 26):
                report_type = "nivel Ph"
            else :
                report_type = "temperatura"
        else:
            input = "NULL"
            if (report_type == 28):
                report_type = "esgoto"
            elif (report_type == 29):
                report_type = "lixo"
            elif (report_type == 30):
                report_type = "erosao"
            else :
                report_type = "outros"

        updated_at = row['meta']['updated_at']
        new_row = [contrib_id, device_id, coordinate_x, coordinate_y, report_type, input, updated_at]
        table.append(new_row)
    n_dataframe = pd.DataFrame(table, columns=['contrib_id', 'device_id', 'longitude',
                               'latitude', 'report_type', 'input', 'data'])
    return n_dataframe.to_csv()


def home(request):
    return render(request, 'home.html')

def midias(request):
    return render(request, 'midias.html')

def send_file(request):
    gresponse = requests.get('http://35.237.4.221/api/projects/6/contributions/')
    path = default_storage.save('midias/data.csv', ContentFile(data_parser(gresponse.content)))
    filename     = "midias/data.csv" # Select your file here.
    download_name ="data.csv"
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    default_storage.delete(path)
    return response

def send_alfakit(request):
    filename     = "midias/alfakit/alfakit.pdf" # Select your file here.
    download_name ="alfakit.pdf"
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response

def send_collector(request):
    filename     = "midias/app/Eco-Cidades-Braslandia v1.3.sap" # Select your file here.
    download_name ="Eco-Cidades-Braslandia v1.sap"
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
