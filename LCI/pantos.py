import cv2
try:
    from google.colab.patches import cv2_imshow
except:
    pass
import pandas as pd
import numpy as np
from tqdm import tqdm


def erase_txt(image, blur = True):
    """
    Process an image by either blurring or covering text regions with black rectangles.

    This function takes an image.
    If text with a probability greater than 0.5 is detected, it applies blurring or covers
    the text with a black rectangle. If no such text is found, it returns the original image.

    Args:
        img (numpy.ndarray): The input image to be processed.
        blur (bool, optional): If True, blur the detected text regions; otherwise, cover
                               them with black rectangles. Default is True.

    Returns:
        numpy.ndarray: The processed image.

    Example:
        img = cv2.imread("image.jpg")
        processed_img = proc_img(img, blur=True)
    """
    try:
        from easyocr import Reader
    except:
        import LCI.utils as utl
        utl.install_package('easyocr')
        #!pip install easyocr
        from easyocr import Reader
    try:
        reader = Reader(['es','en'],gpu = True)
    except:
        reader = Reader(['es','en'],gpu = False)
    img = image.copy()
    res = reader.readtext(img)
    # For each results:
    for (bbox, text, prob) in res:
      # The next line display the text along with its associated probability.
      #print("[INFO] {:.4f}: {}".format(prob, text))
      if prob>0.5:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        
        if blur:
            img[tl[1]:bl[1], tl[0]:tr[0]] = cv2.blur(img[tl[1]:bl[1], tl[0]:tr[0]] ,(53,53))
        else:
            # A fix is needed because the zone that is blur is different from the black rectangle
            img = cv2.rectangle(img, tl, br, (0, 0, 0), -1)
    return img

class lci_db:
    def __init__(self,cred_path, name = 'lci'):
        try:
            import firebase_admin
        except: 
            import LCI.utils as utl
            utl.install_package('firebase-admin')
            # install_package('firebase-admin')
        
        from google.cloud import firestore
        import firebase_admin
        from firebase_admin import credentials
        import os
        import requests
        """
        Initializes the Firebase application with the provided credentials and returns a Firestore client.

        Args:
            cred_path (str): The path to the JSON credentials file for Firebase.
            name (str, optional): The name for the Firebase app. Default is 'lci'.

        Returns:
            firestore.Client: Initialized Firestore client.

        Example:
            lci = lci_db("path/to/credentials.json")
        """
        self.cred_path = cred_path
        # Set the environment variable for Google Application Credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path 

         # Initialize the Firebase application with the credentials
        cred = credentials.Certificate(cred_path) 
        try:
            firebase_admin.initialize_app(cred,name)
        except:
            t = '''
            The default Firebase app already exists. This means you called initialize_app() more 
            than once without providing an app name as the second argument. 
            In most cases you only need to call initialize_app() once. 
            But if you do want to initialize multiple apps, pass a second argument 'name = "another_app_name"'
            when initialize this object.
            '''
            print(t)
        self.db = firestore.Client()
    
    def collections(self):
        """
        Retrieves a list of collection names from the Firestore database.

        Returns:
            list of str: A list of collection names.

        Example:
            lci = lci_db("path/to/credentials.json")
            collection_names = lci.collections()
        """
        self.collections = [collection.id for collection in self.db.collections()]
        return self.collections

    def raw_query(self, collection_name):
        """
        Perform queries to Firestore and combine results without duplicates.

        Args:
            collection_name (str): The name of the Firestore collection to query.

        Returns:
            list: A list of combined results.

        Example:
            lci = lci_db("path/to/credentials.json")
            collection_name = "example_collection"
            query_results = lci.raw_query(collection_name)
        """
        query = self.db.collection(collection_name)
        results = query.stream()
        self.query_collection = list(results)
        return self.query_collection

    def filt_query(self,func):
        """
        Filters the data in the current query collection based on a given function.

        Args:
            func (callable): A function that defines the filter condition.

        Returns:
            list: A list of items that satisfy the filter condition.

        Example:
            lci = lci_db("path/to/credentials.json")
            # Define a filter function, e.g., lambda item: item['field'] == 'value'
            filtered_data = lci.filt_query(func)
        """
        self.filtered_data = list(filter(lambda item: func(item), self.query_collection))
        return self.filtered_data

    def download_jsons(self, file_list, dst_folder):
        """
        Download JSON files from a list of Firestore document references and save them to a destination folder.

        Args:
            file_list (list): A list of Firestore document references.
            dst_folder (str): The destination folder where JSON files will be saved.

        Returns:
            None

        Example:
            lci = lci_db("path/to/credentials.json")
            collection_list = lci.query_collection
            collection_name = collection_list[0]
            query_results = lci.raw_query(collection_name)
            dst_folder = "path/to/destination_folder"
            lci.download_json(query_results,dst_folder)
        """
        from datetime import date
        import requests
        from tqdm import tqdm

        today = str(date.today()).replace('-','_')
        dst_folder = dst_folder+'/query_'+today+'/jsons/'
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        print('Downloading jsons:')
        for f in tqdm(file_list):
            url = f.to_dict()['json_url']
            json_name = f.to_dict()['json_filename']
            response = requests.get(url)
            response.raise_for_status()
            save_path = dst_folder +  json_name
            with open(save_path, "wb") as archivo:
                archivo.write(response.content)

    def download_images(self, file_list, dst_folder):
        """
        Download images from a list of Firestore document references and save them to a destination folder.

        Args:
            file_list (list): A list of Firestore document references.
            dst_folder (str): The destination folder where images will be saved.

        Returns:
            None

        Example:
            lci = lci_db("path/to/credentials.json")
            collection_list = lci.query_collection
            collection_name = collection_list[0]
            query_results = lci.raw_query(collection_name)
            dst_folder = "path/to/destination_folder"
            lci.download_images(query_results,dst_folder)
            
        """
        from datetime import date
        import requests
        from  tqdm import tqdm
        import os

        today = str(date.today()).replace('-','_')
        dst_folder = dst_folder+'/query_'+today+'/images/'
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        print('Downloading images:')
        for f in tqdm(file_list):
            url = f.to_dict()['image_url']
            try:
                img_name = f.to_dict()['image_name']
            except:
                img_name = f.to_dict()['json_filename'][:-5]+'.jpg'
            response = requests.get(url)
            response.raise_for_status()
            save_path = dst_folder +  img_name
            with open(save_path, "wb") as archivo:
                archivo.write(response.content)

    
    def generate_csv(self, file_list):
        """
        Generate a Pandas DataFrame with specific columns from Firestore document data.

        Args:
            file_list (list): A list of Firestore document references.

        Returns:
            pandas.DataFrame: A DataFrame containing selected columns from the document data.

        Example:
            lci = lci_db("path/to/credentials.json")
            file_list = lci.query_collection
            dataframe = lci.generate_csv(file_list)
        """
        import pandas as pd

        col_names_1 = ['date','id','hash','data_origin','push_date','pull_date','last_download_date','annotator_name','code','anonymized_text','labels_in_json']
        col_names_2 = ['complete','incomplete','permanent','temporal','mixed','supernumerary','neoformation','uncertain_caries','retained','tartar','condylar_variations','atheroma',
                    'agenesis','radiolucency','dental_restoration','total_tooth_count','caries','bone_resorption','bone_loss','root_remains','labels_to_check']
        col_names_3 = ['image_filename','json_filename','diagnosis_filename','image_type','image_url','json_filename','json_url','diagnosis_text','comment','comments_Mariano']

        col_names = col_names_1+col_names_2+col_names_3
        df = pd.DataFrame()
        for f in file_list:
            data = f.to_dict()
            df_temp = pd.DataFrame()
            for c in col_names:
                df_temp[c] = [data[c]]
                if c in ['date','push_date','pull_date','last_download_date']:
                    try:
                        df_temp[c] = df_temp[c].dt.tz_localize(None)
                        df_temp[c] = pd.to_datetime(df_temp[c][0]).date()
                    except:
                        pass
                
            df = pd.concat([df,df_temp], ignore_index = True)
        return df

    def download_images_and_json(self,file_list,dst_folder):
        """
        Download images and JSON files from URLs and save them to the filesystem.
        Also save a csv and xlsx file with the info from each file.

        Args:
            file_list (list): A list of Firestore document references.
            dst_folder (str): The destination folder where images and JSON files will be saved.

        Returns:
            None

        Example:
            lci = lci_db("path/to/credentials.json")
            collection_list = lci.query_collection
            collection_name = collection_list[0]
            query_results = lci.raw_query(collection_name)
            dst_folder = "path/to/destination_folder"
            lci.download_images_and_json(query_results,dst_folder)
        """
        import pandas as pd
        from datetime import date
       
        today = str(date.today()).replace('-','_')
        self.download_images(file_list,dst_folder)
        self.download_jsons(file_list,dst_folder)
        df = self.generate_csv(file_list)
        df.to_csv(dst_folder+'/query_subset_results_'+today+'.csv')
        df.to_excel(dst_folder+'/query_subset_results_'+today+'.xlsx')
