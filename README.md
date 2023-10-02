# LCI
This is the LCI's python package. In here we will find differents modules from each proyect and a general one that is called utils. In this one you will find the functions, methods and classes that we use in a daily bases.

## Install
You can use PIP to install this package:

    pip install git+https://github.com/ImageLabUNS/LCI

## Documentation
The docs are in docs/_build/html. In a few days we will put the documentation online

## Examples of usage
Import the modules:

    import LCI.utils as utl
    import LCI.pantos as pts

### Use some functions from utils
drive_colab is a function that import all the packages needed for save/move/modify any file/folder in our google drive while using google colaboratory 

    utl.drive_colab()

For copy files, or move them, you can use 

    utl.copy_file(file_path, dest_path) 
    utl.move_file(file_path, dst_path)

### Using the database in pantos
If you need to make some querys in de DB you can use 

    db = pts.lci_db(cred_path, name='lci')

where cred_path is the json file with the credentials. The argument 'name' is an optative parameter. 
db is an object with it's methods

#### **Get the collections in the DB**
The DB consist in several collections. if you want to list them use

    db.collections()

#### **Make a raw query of a collection**
raw_query make a query where all json are listed

    raw_query(collection_name)

#### **Filter the query**
First we have to make some function/s that have a filter rules and with the item parameter. Here you have some examples:

    def filt_by_value(item):
        condition0 = item.to_dict()['tartar'] == True
        return condition0

    def filt_by_combination(item):
        condition1 = item.to_dict()['annotator_name'] != ''
        condition2 = (len(item.to_dict()['retained'])>0)# == True
        condition3 = item.to_dict()['tartar'] == True#item.to_dict()['annotator_name'] == 'user@gmail.com'
        boolean = condition1 & condition2 #& condition3
        return boolean

    def filt_by_key(item):
        condition4 = 'imageData' in item.to_dict().keys()
        return condition4

    def filt_by_date(item):
        if 'push_date' in item.to_dict().keys() and item.to_dict()['push_date']!='':
            push_date_str = item.to_dict()['push_date']
            # There are 4 different formats. With and without PM or AM, "%d/%m/Y% %H:%M:%S" and "%m/%d/%Y %H:%M:%S".
            # I cut at the first space to compare with a date easily
            push_date_cut = push_date_str[:push_date_str.find(' ')]
            try:
                push_date = datetime.strptime(push_date_cut, "%d/%m/%Y")
            except:
                push_date = datetime.strptime(push_date_cut, "%m/%d/%Y")

            compare_date = datetime.strptime('24/3/2023', "%d/%m/%Y") # Date to compare
            condition5 = compare_date < push_date

Then you can use any function as an argument. Here is an example using the first function:

    file_list = db.filt_query(filt_by_value)

#### **Download the json and the images**
For downloading the jsons files and the images files of a list of files filtered use:

    db.download_images(file_list, dst_folder)

where dst_folder is a folder where two other directories will be created: "jsons" and "images". Also in dst_folder will be created a csv and a xlsx file with the information in the jsons we download.


Test branches