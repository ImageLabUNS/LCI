from glob import glob as gl # This list paths
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go # https://plotly.com/python/
from PIL import Image

class ota_info():
    def __init__(self, folder_path):
        """
        Initialize.

        Args:
            folder_path (str): The path to the folder containing shapefiles.

        Attributes:
            path (str): The folder path.
            cats (list of str): List of OTA categories.

        Example:
            ota = ota_info("path/to/folder/")
        """

        self.path = folder_path
        self.cats =  ['cachorro','macho_adulto','hembra_adulta','macho_subadulto','juvenil','indeterminado']

    def ota2df_by_file(self,file_path,cls):
        """
        Convert a shapefile (.shp) to a DataFrame with columns 'x', 'y', and 'cls'.

        Args:
            file_path (str): The path to the .shp file.
            cls (str): The class.

        Returns:
            pandas.DataFrame: A DataFrame with 'x', 'y', and 'cls' columns.

        Example:
            df = ota.ota2df_by_file("path/to/shapefile.shp", "cachorro")
        """
        
        df_ = pd.DataFrame()
        try:
            data_df_ = gpd.read_file(file_path)
            
            df_['x'] = data_df_.geometry.x
            df_['y'] = data_df_.geometry.y
        except:
            df_['x'] = []
            df_['y'] = []
        df_['cls'] = cls
        return df_

    def ota2df(self):
        """
        Convert OTA shapefiles in the specified folder to a single DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing OTA data with 'x', 'y', and 'cls' columns.

        Example:
            ota_df = ota.ota2df()
        """
        try:
            sh_list = gl(self.path+'*.shp')
        except:
            from glob import glob as gl
            sh_list = gl(self.path+'/*.shp')

        #classes = ['cachorro','macho_adulto','hembra_adulta','macho_subadulto','juvenil','indeterminado']
        df = pd.DataFrame()
        for c in self.cats:
            
            try:
                file_name = [fl for fl in sh_list if c in fl][0]
                df = pd.concat([df,self.ota2df_by_file(file_name,c)],ignore_index = True)
            except:
                df = pd.concat([df,pd.DataFrame({'x':[],'y':[],'cls':[c]})])
                #pass
                #print('Error with file',file_name)

        return df

    def count(self):
        """
        Count the occurrences of OTA categories in the dataset.

        Returns:
            pandas.Series: A Series containing category counts.

        Example:
            category_counts = ota.count()
        """
        df = self.ota2df()
        return df.cls.value_counts()

    def plot(self):
        """
        Create an interactive plot showing the OTA data overlaid on an image.

        Example:
            ota.plot()
        """
        category_colors = {
                        'cachorro': 'rgba(255, 0, 0, 255)',        # Red
                        'macho_adulto': 'rgba(0, 255, 0, 255)',  # Green
                        'hembra_adulta': 'rgba(0, 0, 255, 255)',  # Blue
                        'macho_subadulto': 'rgba(255, 255, 0, 255)',  # Yellow
                        'juvenil': 'rgba(128, 0, 128, 255)',     # Purple
                        'indeterminado': 'rgba(0, 128, 128, 255)'  # Teal
                    }
        try:
            image_path = gl(self.path+'*[.png,.jpg]')[0]
        except:
            from glob import glob as gl
            image_path = gl(self.path+'*[.png,.jpg]')[0]
        image = Image.open(image_path)
        img_width, img_height = image.size


        # Create a Plotly figure
        fig = go.Figure()

        df = self.ota2df()

        for c in df.cls.unique():

            df_temp = df[df.cls == c].copy()
            fig.add_trace(go.Scatter(x = df_temp.x,
                                    y = img_height+df_temp.y,
                                    mode='markers',
                                    marker = dict(size=10,
                                                line_width = 2,
                                                color='rgba(255,0,0,0)',

                                                line_color = category_colors[c]),

                                    name = c,
                                    ))

        fig.update_layout(template="plotly_white",
                        xaxis = dict(range=[0,img_width]),
                        yaxis = dict(range=[0,img_height]),)

        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width,
                y=img_height,
                sizey=img_height,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=image)
        )
        self.figure = fig
        # Show the plot

        print('If the image is too large could crash plotly in colab. Do you want to Download the image?')
        multiple_choice = widgets.Dropdown(
            options=['Select one option','Save as HTML', 'Save as png', 'Try to show'],
            description='Select an option:',
        )

        # Function to handle the selection
        def handle_dropdown(change):
            selected_option = change.new
            if selected_option == 'Save as HTML':
                print('Saving... wait until another message shows')
                self.figure.write_html(self.path+'/interactive_image.html')
                print('The image was saved in the folder of the proyect as "interactive_image.html')
                print(f'You selected: {selected_option}')
            elif selected_option == 'Save as png':
                print('Saving... wait until another message shows')
                self.figure.write_image(self.path+'/image.png')
                print('The image was saved in the folder of the proyect as "image.png')
            elif selected_option == 'Try to show':
                print('Trying to show... wait until another message shows')
                self.figure.show()
                print("If the image doesn't show try to write ota_obj.figure.show(). Sometimes it works")
            else:
                print('You have to select one option')
                #return(fig.show())

        # Attach the function to the dropdown's change event
        multiple_choice.observe(handle_dropdown, names='value')

        # Display the dropdown widget
        display(multiple_choice)
        #fig.show()
        #return fig