# Create your models here.
from pickle import TRUE
from pyexpat import model
from django import forms
from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django import forms

class productionOrder(models.Model):
    sno=models.IntegerField(primary_key=TRUE)
    orderRefNo = models.CharField(max_length=122)
    orderVariant = models.CharField(max_length=122)
    orderStartDate = models.DateField(null=True)
    orderEndDate = models.DateField(null=True)
    orderQuantity = models.CharField(max_length=122)
    orderPriority = models.CharField(max_length=122)
    currentDate = models.DateField()

class machineDetails(models.Model):
    machine_name=models.CharField(max_length=122)
    line=models.CharField(max_length=122)  
    status=models.CharField(max_length=122)  
    MachineNo=models.CharField(max_length=122)
    Description=models.CharField(max_length=122,default=0)
    operation=models.CharField(max_length=122,default=0)
    currentDate = models.DateField()

class componentDetails(models.Model):
    component_name=models.CharField(max_length=122)
    DrawingNo=models.CharField(max_length=122)  
    qpp=models.CharField(max_length=122)  
    Level=models.CharField(max_length=122)
    description=models.CharField(max_length=122,default=0)
    modelName=models.CharField(max_length=122,default=0)
    currentDate = models.DateField()

class makelist(models.Model):
    component_name=models.CharField(max_length=122)
    machineName=models.CharField(max_length=122)  
    startTime=models.CharField(max_length=122)  
    EndTime=models.CharField(max_length=122)
    operationName=models.CharField(max_length=122,default=0)

#operation detail models
class operationsDetails(models.Model):
    operationName = models.CharField(max_length=300)
    inputComponentsName = models.CharField(max_length=300)
    outputComponentsName = models.CharField(max_length=300)
    operationMachineName = models.CharField(max_length=300)
    operationTime = models.CharField(max_length=300)

class HMIDetail(models.Model):
    operatorname=models.CharField(max_length=122)
    identity=models.CharField(max_length=122)
    machine=models.CharField(max_length=122)
    variant=models.CharField(max_length=122)
    partname=models.CharField(max_length=122)
    partno=models.CharField(max_length=122)
    timein=models.DateTimeField(null=True)
    timeout=models.DateTimeField(null=True)
    date=models.DateField()

class inhouseInventory(models.Model):
    sno=models.IntegerField(primary_key=True,default=0)
    productSno=models.CharField(max_length=122,default=0)
    level=models.CharField(max_length=122,default=0)
    qpp=models.CharField(max_length=122,default=0)
    drawingno=models.CharField(max_length=122,default=0)
    availableNos=models.CharField(max_length=122,default=0)
    timein=models.DateTimeField(null=True)
    date=models.DateField()

class InventoryIN(models.Model):
    sno=models.IntegerField(primary_key=True,default=0)
    productSno=models.CharField(max_length=122,default=0)
    level=models.CharField(max_length=122,default=0)
    qpp=models.CharField(max_length=122,default=0)
    drawingno=models.CharField(max_length=122,default=0)
    availableNos=models.CharField(max_length=122,default=0)
    timein=models.DateTimeField(null=True)
    date=models.DateField()