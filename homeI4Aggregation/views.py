from msilib.schema import Class
import operator
import re
import shutil
from tracemalloc import start
from django.shortcuts import render,HttpResponse,redirect
from datetime import date, datetime
from matplotlib.pyplot import cla

from pyparsing import line
from homeI4Aggregation.models import InventoryIN, machineDetails, makelist, productionOrder,componentDetails,HMIDetail,inhouseInventory,operationsDetails
from django.contrib import messages
from src._inputs._lib import main
from src._inputs._lib.main_inputs import forPreInventory
from django.views.decorators.csrf import csrf_protect
import os,subprocess
import sys
import requests
import json
from src._inputs._lib.main import Schedule
import pandas as pd
#id pass: industry4.0 , iforgotit1234

orderVariant = ""

somelist =  []
a = 0
# Create your views here.
@csrf_protect
def index (request):
    return render(request, "index.html")

def operationsChart (request):
    return render(request, "operations_chart.html")

def machineLoading (request):
    return render(request, "machine_loading.html")
    
def placeOrder (request):
    if request.method =="POST":
        OR_no=request.POST.get('OR_no')
        variant=request.POST.get('variant')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date') 
        quantity=request.POST.get('quantity') 
        priority=request.POST.get('priority') 
        order=productionOrder(orderRefNo=OR_no,orderVariant=variant,orderStartDate=start_date,orderEndDate=end_date,orderQuantity=quantity,orderPriority=priority,currentDate=datetime.today())
        order.save()
        messages.success(request, 'your Order has been sent!')
        generateNewVariantOperationData(request,variant=variant)
        global orderVariant
        orderVariant = variant
    orders = productionOrder.objects.all()
    return render(request, "place_order.html",{'orders':orders})

def generateSchedule (request):
    todaysOrder = productionOrder.objects.filter(currentDate = datetime.today()).order_by("sno")
    main.call_this(request,todaysOrder)
    return render(request, "machine_loading.html")
    
# @app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(request,sno):
    if request.method=='POST':
        OR_no=request.POST.get('OR_no')
        variant=request.POST.get('variant')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date') 
        quantity=request.POST.get('quantity') 
        priority=request.POST.get('priority')
        order = productionOrder.objects.get(sno=sno)
        order.orderRefNo = OR_no
        order.orderVariant = variant
        order.orderStartDate = start_date
        order.orderEndDate =end_date
        order.ordeQuantity =quantity
        order.orderPriority =priority
        order.save()
            # db.session.add(todo)
            # db.session.commit()
        return redirect("/place_order")
        
    order = productionOrder.objects.get(sno=sno)
    return render(request, "update.html",{'order':order})

def delete(request,sno):
    order = productionOrder.objects.get(sno=sno)
    order.delete()
    return redirect("/place_order")

def deleteMachine(request,id):
    mach = machineDetails.objects.get(id=id)
    mach.delete()
    return redirect("/machine_details")

def updatedView(request,sno):
    order = productionOrder.objects.get(sno=sno)
    return render(request,"update.html",{'order':order})

def mcDetails(request):
    machDetail = machineDetails.objects.all()
    return render(request,"mc_details.html",{"machDetail":machDetail})

def mcDetailsInput(request):
    if request.method == "POST":
        MachineName = request.POST.get("machine_name")
        line = request.POST.get("shopName")
        status = "READY"
        machineno = request.POST.get("MachineNo")
        operationName = request.POST.get("description")
        machineDBData = machineDetails(machine_name = MachineName,line = line,status=status,MachineNo =machineno,Description=operationName,operation = operationName,currentDate=datetime.today())
        machineDBData.save()
        messages.success(request, 'your message has been sent!')
    machDetail = machineDetails.objects.all()
    return render(request,"mc_details.html",{"machDetail":machDetail})

def contact(request):
    return render(request,"contact.html")

def daqpanel(request):
    subprocess.Popen(os.getcwd() + "\\static\\execuables\\daqPanel\\daqPanel.exe") 
    return render(request,"daq.html")

def daq(request):
    return render(request,"daq.html")

def addidaq(request):
    return render(request,"additionalDaq.html")

def addidaqpanel(request):
    subprocess.Popen(os.getcwd() + "\\static\\execuables\\addiDaqPanel\\MCF-i4 Dashboard.exe") 
    return render(request,"additionalDaq.html")

def daqpanelbharat(request):
    subprocess.Popen(os.getcwd() + "\\static\\execuables\\IndustryMonitoring\\IndustryMonitoring.exe") 
    return render(request,"additionalDaq.html")

def daqEngine(request):
    return render(request,"daq_engines.html")

def process(request):
    return render(request,"process.html")

def rfid(request):
    return render(request,"rfid.html")

def machineUtilization(request):
    return render(request,"machine_utilization.html")

def ssLV(request):
    return render(request,"ssLabViewCode.html")

def ssSch(request):
    return render(request,"ssSchedularCode.html")

def shopFloor(request):
    return render(request,"shop_floor.html")

def daqniopc(request):
    subprocess.Popen(os.getcwd() + "\\static\\execuables\\daqEngine_NIOPC\\daqEngine_NIOPC.exe")
    return render(request,"daq_engines.html")

def daqmtlinki(request):
    subprocess.Popen(os.getcwd() + "\\static\\execuables\\daqEngine_MTLINKi\\daqEngine_MTLINKi.exe")
    return render(request,"daq_engines.html")

apiURL = "http://172.26.98.238:8000/hmiPartInfo/"

def hmi_get_data(request):
    readFromAPI = requests.get(apiURL).json()
    getHMIData = getHMIdataFromAPI(readFromAPI)
    return render(request,"hmi.html",{'hmiAllData':getHMIData})

def getHMIdataFromAPI(readFromAPI):
    getAPIData = []
    r1 = readFromAPI["data"][0]
    for i in range(0,len(r1)):
        d1 = {"id":r1[i]["id"],
        "operatorName":r1[i]["operatorName"],
        "operatorIDNo":r1[i]["operatorIDNo"],
        "machineName":r1[i]["machineName"],
        "variantName":r1[i]["variantName"],
        "partName":r1[i]["partName"],
        "partNumber":r1[i]["partNumber"],
        "timeIN":r1[i]["timeIN"],
        "timeOUT":r1[i]["timeOUT"]}
        getAPIData.append(d1)
    return getAPIData

def deleteHMIAPIdata(request,id):
    return redirect("/hmi")

apiInvURL = "http://172.26.98.238:8100/inhouseInventoryInfo/"

def inv_get_data(request):
    readFromInvAPI = requests.get(apiInvURL).json()
    getINVData = getINVdataFromAPI(readFromInvAPI)
    return render(request,"inHouseInv.html",{'invAllData':getINVData})

def getINVdataFromAPI(readFromInvAPI):
    getInvAPIData = []
    r12 = readFromInvAPI["data"][0]
    for i in range(0,len(r12)):
        d12 = {"id":r12[i]["id"],
        "ProductSNo":r12[i]["ProductSNo"],
        "Level":r12[i]["Level"],
        "DrawingNo":r12[i]["DrawingNo"],
        "Description":r12[i]["Description"],
        "qpc":r12[i]["qpc"],
        "length":r12[i]["length"],
        "width":r12[i]["width"],
        "thick":r12[i]["thick"],
        "InnerDia":r12[i]["InnerDia"],
        "OuterDia":r12[i]["OuterDia"],
        "quantityAvailable":r12[i]["quantityAvailable"]}
        getInvAPIData.append(d12)
    return getInvAPIData

def deleteINVAPIdata(request,id):
    return redirect("/inv")

def make(request):
    for names in Schedule:
        operationName = names['Operation']
        MachineName = names['Machine']
        componentName = names['Input']
        startTime = names['Start Time']
        endTime = names['End Time']
        makelistBData = makelist(component_name = componentName,machineName = MachineName,startTime = startTime,EndTime = endTime,operationName = operationName)
        makelistBData.save()
    df = makelist.objects.all()
    return render(request,"make.html",{"df":df})

def machineHealth(request):
    return render(request,"machineHealth.html")

def buy(request):
    readFromInvAPI = requests.get(apiInvURL).json()
    getINVData = getINVdataFromAPI(readFromInvAPI)
    return render(request,"buy.html",{'invAllData':getINVData})

def inventory(request):
    if request.method == "POST":
        productSno=request.POST.get('productSno')
        level=request.POST.get('level')
        qpp=request.POST.get('qpp')
        drawingno=request.POST.get('drawingno')
        availableNos=request.POST.get('availableNos')
        timein=request.POST.get('timein')
        inhouseInv=InventoryIN(productSno=productSno,level=level,qpp=qpp,drawingno=drawingno,availableNos=availableNos,timein=timein,date=datetime.today())
        inhouseInv.save()
        doc ={"ProductSNo":productSno,"Level":level,"DrawingNo":drawingno,"Description":drawingno,"qpc":qpp,"length":drawingno,"width":drawingno,"thick":drawingno,"InnerDia":drawingno,"OuterDia":drawingno,"quantityAvailable":availableNos}
        # mycol.insert_one(doc)
        jsonConvert = json.dumps(doc)
        createToAPI = requests.post(apiInvURL,data=jsonConvert)
        messages.success(request, 'your message has been sent!')
    inhouseInvs=InventoryIN.objects.all()
    # print(inhouseInvs)
    # addToMainInventory(request)
    getInventoryDetails(request)
    return render(request,"inHouseInventory.html",{'inhouseInvs':inhouseInvs})

def hmi(request):
    if request.method == "POST":
        operatorname=request.POST.get('operatorname')
        identity=request.POST.get('identity')
        machine=request.POST.get('machine')
        variant=request.POST.get('variant')
        partname=request.POST.get('partname')
        partno=request.POST.get('partno')
        timein=request.POST.get('timein')
        timeout=request.POST.get('timeout')
        detail=HMIDetail(operatorname=operatorname,identity=identity,timein=timein,timeout=timeout,machine=machine,variant=variant,partname=partname,partno=partno,date=datetime.today())
        detail.save()
        doc ={"ProductSNo":operatorname,"operatorIDNo":identity,"machineName":machine,"variantName":variant,"partName":partname,"partNumber":partno,"timeIN":timein,"timeOUT":timeout}
        jsonConvert = json.dumps(doc)
        createToAPI = requests.post(apiURL,data=jsonConvert)
        messages.success(request, 'your message has been sent!')
    hmiAllDatas = HMIDetail.objects.all()
    return render(request,"hmi/hmi.html",{'hmiAllData':hmiAllDatas})

def readOperationJsonSaveToDB(request):
    jsonfileOperat = './static/json/operation.json'
    json_data_file = open(jsonfileOperat)
    json_load_file = json.load(json_data_file)

    with open(jsonfileOperat,'r') as opera:
        parsed_json_file = json.load(opera)
    
    for names in parsed_json_file.keys():
        operationName = parsed_json_file[names]['name']
        inputComponentsName = parsed_json_file[names]['inputs']
        outputComponentsName = parsed_json_file[names]['outputs']
        operationMachineName = parsed_json_file[names]['machine']
        operationTime = parsed_json_file[names]['time']
        operationDBData = operationsDetails(operationName = operationName, inputComponentsName = inputComponentsName,outputComponentsName = outputComponentsName,operationMachineName= operationMachineName,operationTime= operationTime)
        operationDBData.save()

def readAllDB(request):
    readMachineJsonSaveToDB(request)
    operDetail = machineDetails.objects.all()
    print(operDetail)

def operationDetails(request):
    operDetail = operationsDetails.objects.all()
    return render(request,"operation_details.html",{'operDetail':operDetail})

def readMachineJsonSaveToDB(request):
    jsonfileMachine = './static/json/machine.json'
    json_data_file = open(jsonfileMachine)
    json_load_file = json.load(json_data_file)

    with open(jsonfileMachine,'r') as Machine:
        parsed_json_file = json.load(Machine)
        # print(parsed_json_file)
    
    for names in parsed_json_file:
        operationName = names['operation']
        MachineName = names['name']
        line = names['line']
        machineno = names['machine_no']
        status = names['status']
        machineDBData = machineDetails(machine_name = MachineName,line = line,status=status,MachineNo =machineno,Description=operationName,operation = operationName,currentDate=datetime.today())
        machineDBData.save()
        
def getInventoryDetails(request):
    inv = inhouseInventory.objects.all()

def readInventoryData(request):
    global orderVariant
    print(orderVariant)
    if orderVariant =="":
        # file_name = "operation_data.xlsx"
        input_folder = os.path.join(os.getcwd(),"src\\_inputs\\data\\")
        file_path = input_folder+"operation_data.xlsx"
    else:
        input_folder = os.path.join(os.getcwd(),"src\\_inputs\\data\\")
        file_path = input_folder+"operation_data"+"_"+orderVariant+".xlsx"
    swl_op = pd.read_excel(file_path,sheet_name = 'swl_operation_components',header = None,skiprows = [0],engine="openpyxl")
    ewl_op = pd.read_excel(file_path,sheet_name = 'ewl_operation_components',header = None,skiprows = [0],engine="openpyxl")
    rf_op = pd.read_excel(file_path,sheet_name = 'rf_operation_components',header = None,skiprows = [0],engine="openpyxl")
    uf_op = pd.read_excel(file_path,sheet_name = 'uf_operation_components',header = None,skiprows = [0],engine="openpyxl")
    sh_op = pd.read_excel(file_path,sheet_name = 'sh_operation_components',header = None,skiprows = [0],engine="openpyxl")
    operation_list = [swl_op,ewl_op,rf_op,uf_op,sh_op]
    components = {}
    i = 0

    for items in operation_list:
        for index,row in items.iterrows():
            i = i + 1
            # if row not in components:
            components = {"sno":i,"operation":row[0],"component_name":row[1],"drawing_no":row[2],"qpc":row[3],"types":row[4],"ac":row[5],"inventory":row[6]}
            somelist.append(components)
    return render(request,"componentsDetails.html",{"components":somelist})

def updateComponentsDetails(request,listindex):
    getDataFromComponentsUpdate = somelist[listindex - 1]
    return render(request,"updateComponentsDetails.html",{"updateComponent":getDataFromComponentsUpdate})

def updateToNewFile(request,sno):
    new_component_name = request.POST.get('component_name')
    new_drawing_no = request.POST.get('drawing_no')
    new_qpc = request.POST.get('qpc')
    new_inventory = request.POST.get('inventory')
    assembly_code = request.POST.get('assembly_code')
    types = request.POST.get('type')
    new_component = {"component_name":new_component_name,"drawing_no":new_drawing_no,"qpc":new_qpc,"types":types,"ac":assembly_code,"inventory":new_inventory}
    somelist[sno - 1].update(new_component)
    writeToExcelComponentDetails(request)
    return render(request,"componentsDetails.html",{"components":somelist})

def writeToExcelComponentDetails(request):
    global orderVariant
    cwd = os.path.join(os.getcwd(),"src/_inputs/data/")
    if orderVariant == "":
        newFileName = "operation_data_new.xlsx"
    else:
        newFileName = "operation_data_"+orderVariant+"_new.xlsx"
    column = ('sno','Operation','Item Description','Drg.No.', 'QPC', 'I or O','Assembly Code','Inventory')
    df = pd.DataFrame(data=somelist)
    df.to_excel(os.path.join(cwd,newFileName),sheet_name="Inventory",header=column,index=None,engine="openpyxl")
    # return render(request,"componentsDetails.html",{"components":somelist})

def generateNewVariantOperationData(request,variant):
    variantName  = variant
    cwd = os.path.join(os.getcwd(),"src/_inputs/data/")
    newFileName = "operation_data_"+variantName
    newFileDirectory = cwd+""+newFileName+".xlsx"
    oldFileDirectory = cwd+"operation_data.xlsx"
    if os.path.isfile(newFileDirectory) == False:
        shutil.copy(oldFileDirectory,newFileDirectory)