import numpy as np 
import glob
from natsort import natsorted


#importpath = r'E:\Kaiser\2020-06-30 110614A TMRLE 250nm\S110614A_T4K_A250nm_PpPol_Kpl_W775nm_raw'
importpath = 'S110614A_T4K_A250nm_PpPol_Kpl_W775nm_raw'
files = natsorted(glob.glob(importpath + '/*.txt'))     # natsorted macht 1,2,11 und nicht 1,11,2 wie sorted()

#print(importpath)
#print(glob.glob)
#print(files)

for file in files:  # Komma zu Punkt
    with open(file, 'r+') as f:
        source = f.read()
        replaced = source.replace(',','.')
        if replaced != source:
            f.seek(0)   # Go to position 0 in file
            f.write(replaced)
            f.truncate() # Delete characters trailing new content


#positive and negative B-Field
filesB_neg=files[0:26]
filesB_pos=files[26:]
#print(np.shape(files))
#print(filesB_neg)


# Initialise data array
data = np.zeros((len(files), 1024, 256))# 3d matrix len ist tiefe
dataB_pos = np.zeros((len(filesB_pos), 1024, 256))
dataB_neg = np.zeros((len(filesB_neg), 1024, 256))
#print(dataB_neg.shape)
#print(data.shape)


# Read files
# saves the files into the 3D matrices 
#3D Matrix
for idx, file in enumerate(files):
    data[idx] = np.genfromtxt(file) # when using [] you create a matrix, matrix has to be initialised before
    #print(data[idx])
    #print(idx)
    #print(file)
    #print(data.shape)
    #time.sleep(2)

#3D Matrix
for idx, file in enumerate(filesB_pos):
    dataB_pos[idx] = np.genfromtxt(file)
    #print(idx)
#print(dataB_pos.shape)  

#3D Matrix
for idx, file in enumerate(filesB_neg):
    dataB_neg[idx] = np.genfromtxt(file)     
#print(dataB_neg)     # gives back whole matrix
#print(dataB_neg)     # gives back whole matrix
#print(data[0])  # = print(data[0,0:1024,0:256]) #  gives back first matrix


#Mittelwert der Matrizen (old me)
#matrix = np.zeros(shape=(1024, 256))
#for index in range(0,data.shape[0]):
#    matrix += data[index]
#    print(index)
#
#mittelwert_matrix = matrix/(data.shape[0])
#np.savetxt("mittelwert_matrix.txt", mittelwert_matrix)
#print(mittelwert_matrix)


#Mittelwert der Matrizen (new me)
# creates the mean of the 3D Matrix so that you get a 'normal' 2D Matrix
mittelwert_matrix=np.mean(data,axis=0)  #one large matrix
mittelwert_matrix_pos=np.mean(dataB_pos,axis=0)
mittelwert_matrix_neg=np.mean(dataB_neg,axis=0)
#print(mittelwert_matrix_pos)


#Neuer Mittelwert Korrektur wegen Sensorgröße --> Mittelwerte sind Matrizen (liste in liste)
#**************************
mittelwert_matrix_new = mittelwert_matrix[:,15:244]
mittelwert_matrix_new_pos = mittelwert_matrix_pos[:,15:244]
mittelwert_matrix_new_neg = mittelwert_matrix_neg[:,15:244]
#print(mittelwert_matrix_new.shape)  # (1024,229)
#**************************

# the total sensor is getting saved
np.savez('read_data' ,mm = mittelwert_matrix, mm_pos = mittelwert_matrix_pos, mm_neg = mittelwert_matrix_neg )

#access:
#data = np.load('read_data.npz')
#print(data['mm'])