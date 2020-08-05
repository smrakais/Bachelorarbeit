import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##import data and create dataframe
#wine_data = 'wine.data' 
#wine_column_headers = ['Alcohol','Malic acid','Ash','Alcalinity of ash',  
#                       'Magnesium','Total phenols','Flavanoids',
#                       'Nonflavanoid phenols','Proanthocyanins','Color intensity', 
#                       'Hue','OD280/OD315 of diluted wines' ,'Proline']
#
##reads data
#wine_df = pd.read_csv(wine_data, names = wine_column_headers) #read_csv = "comma seperated value"
##print(wine_df)
#
##figure
#fig, ax1 = plt.subplots()   #objektorientiert du greifst auf klasse figure zu ax1 ist der erste plot
#fig.set_size_inches(13, 10)
#
##labels
#ax1.set_xlabel('Alcohol')   #set_xlabel da das die methode der klasse ist
#ax1.set_ylabel('Color Intensity')
#ax1.set_title('Relationship Between Color Intensity and Alcohol Content in Wines')
#
##c sequence
#c = wine_df['Color intensity']
#
##plot        x-achse             y-achse   
#plt.scatter( wine_df['Alcohol'], wine_df['Color intensity'] , c=c, #bei c=c bekommt jeder der werte in wine_df['Color intensity'] eine farbe zugeordnet. und cmap sagt dir welche
#            cmap = 'hot')# alpha =0.5, s = wine_df['Proline']*.5
#cbar = plt.colorbar()
#cbar.set_label('Color Intensity')
#
##save figure
#plt.savefig('test.png')
#
#show figure
#plt.show()


#************************************************************************************************************************
#a = np.array([[1,2,3,4,5,6,7,8,9,10],
              [4,7,4,3,7,4,5,3,3,33]])
#b=np.array([6,7,8,9,10])
#c=a+b
#print(a.shape[1])
#print(a[:,0:8])
#print(c/2)
#************************************************************************************************************************
#matrix1 = np.zeros(shape=(1024, 256))
#matrix2 = np.zeros(shape=(1024, 256))
#matrix3=matrix1+matrix2
#print(matrix3)
#************************************************************************************************************************
