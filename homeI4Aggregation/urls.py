from unicodedata import name
from django.contrib import admin
from django.urls import path
from homeI4Aggregation import views
from django.views.generic import TemplateView

urlpatterns = [
    path('home',views.index, name='productionSchedualar'),
    path('operations_chart',views.operationsChart, name='operations_chart'),
    path('machine_loading',views.machineLoading, name='machine_loading'),
    path('place_order',views.placeOrder, name='place_order'),
    path('generate_schedule',views.generateSchedule, name='generate_schedule'),
    path('update/<int:sno>',views.update, name='update'),
    path('delete/<int:sno>',views.delete, name='delete'),
    path('deleteMachine/<int:id>',views.deleteMachine, name='deleteMach'),
    path('<int:sno>',views.updatedView,name='updated_view'),
    path('machine_details',views.mcDetails,name='mc_details'),
    path('machine_details_input',views.mcDetailsInput,name='mc_details_input'),
    path('comp_details',views.compDetails,name='comp_details'),
    path('operation_details',views.operationDetails,name='oper_details'),
    path('contact',views.contact,name='contact'),
    path('daq',views.daq,name="daq"),
    path('daqpanelbharat',views.daqpanelbharat,name="daqpanelbharat"),
    path('addidaq',views.addidaq,name="addidaq"),
    path('daqpanelopen',views.addidaqpanel,name="daqpanelopen"),
    path('daqpanelexe',views.daqpanel,name='daqpanelexe'),
    path('daqengine',views.daqEngine,name='daqengine'),
    path('daqniopc',views.daqniopc,name='daqniopc'),
    path('daqmtlinki',views.daqmtlinki,name='daqmtlinki'),
    path('process',views.process,name='process'),
    path('rfid',views.rfid,name='rfid'),
    path('ssLV',views.ssLV,name='ssLV'),
    path('ssSch',views.ssSch,name='ssSch'),
    path('machineUtilization',views.machineUtilization,name='machineUtilization'),
    path('shopfloor',views.shopFloor,name='shopfloor'),
    path('hmi',views.hmi_get_data,name='hmi'),
    path('inv',views.inv_get_data,name='inv'),
    path('inventoryInput',views.inventory,name = 'inventoryInput'),
    path('make',views.make,name='make'),
    path('machineHealth',views.machineHealth,name='machineHealth'),
    path('deepLearn',views.machineHealth,name='deepLearn'),
    path('buy',views.buy,name='buy'),
    path('operation_details',views.operationDetails,name='oper_details'),
]