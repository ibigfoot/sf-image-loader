# Load File to Salesforce

This is a short script that shows how to create a File in Salesforce and attach it to a record, in this case to load a binary file like an image.

Salesforce Files require you to create a couple of objects, the ContentVersion which is the image itself and then the ContentDocumentLink, which describes the relationship between the File and the object you want to relate it to. 

##Trigger warning
This is my first attempt at learning python ;) 
I would definitely beware of this code!