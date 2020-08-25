import numpy as np
import matplotlib.pyplot as plt
import glob
from  natsort import natsorted
import time


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
# saves the files into the 3d matrix 
for idx, file in enumerate(files):
    data[idx] = np.genfromtxt(file) # when using [] you create a matrix, matrix has to be initialised before
    #print(data[idx])
    #print(idx)
    #print(file)
    #print(data.shape)
    #time.sleep(2)

for idx, file in enumerate(filesB_pos):
    dataB_pos[idx] = np.genfromtxt(file)
    #print(idx)
#print(dataB_pos.shape)  

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
mittelwert_matrix=np.mean(data,axis=0)  #one large matrix
mittelwert_matrix_pos=np.mean(dataB_pos,axis=0)
mittelwert_matrix_neg=np.mean(dataB_neg,axis=0)
#print(mittelwert_matrix_pos)

#Neuer Mittelwert Korrektur wegen Sensorgröße
#**************************
mittelwert_matrix_new = mittelwert_matrix[:,15:244]
mittelwert_matrix_new_pos = mittelwert_matrix_pos[:,15:244]
mittelwert_matrix_new_neg = mittelwert_matrix_neg[:,15:244]
#print(mittelwert_matrix_new.shape)  # (1024,229)
#**************************

# Set wavelength
wl=np.genfromtxt('775nm_grating3_wellenlängenbereich.txt',usecols=(0)) #only takes the first column (spalte)
# Set angle
theta=np.linspace(-23.578,23.578,256)
theta_new=np.linspace(-23.578,23.578,mittelwert_matrix_new.shape[1]) # because of the greatness of the sensor field

#***************************************************************************************************************************
#Colormap plot
plt.pcolormesh(theta_new,wl,mittelwert_matrix_new,cmap='hot') # make the axes correct x,y,matrix
plt.gca().invert_yaxis()                            #inverts the y axis
plt.xlabel(r'$\theta / \mathrm{°}$')
plt.ylabel(r'$\lambda / \mathrm{nm}$')
plt.title('Photolumineszenz')
cbar = plt.colorbar()
cbar.set_label('Intensity')

#save figure and show figure
#plt.show()
plt.savefig('build/photolumineszenz.png')

#***************************************************************************************************************************
#Intensitätsunterschied rho berechnen 
plt.clf()                  # very useful to prevent plots to interact with each other. alternative: object oriented plotting.
rho= (mittelwert_matrix_new_pos - mittelwert_matrix_new_neg) / (mittelwert_matrix_new_pos + mittelwert_matrix_new_neg)
plt.pcolormesh(theta_new,wl,rho,cmap='bwr')
plt.clim(-0.15,0.15)        #bar limit
plt.xlabel(r'$\theta / \mathrm{°}$')
plt.ylabel(r'$\lambda / \mathrm{nm}$')
plt.title('relative Änderung der Intensität')
plt.gca().invert_yaxis()
cbar = plt.colorbar()
cbar.set_label('relative Intensity')
#print(np.max(rho))
#print(np.min(rho))

#save figure and show figure
#plt.show()
plt.savefig('build/rel_aenderung.png')

#***************************************************************************************************************************
# program to select a certain wavelength and to plot the relative intensity againt the angle

wavelenght = 740

minimized_array = abs(wl-wavelenght)            # minimal array
#print(minimized_array)

minimum_value = np.amin(minimized_array)          # find minimum_value of array
#print(minimum_value)

index = np.where(minimized_array == minimum_value)# index of the minimum
#print(index[0][0])                              # only index 
index = index[0][0]
print('You selected the wavelength:', wl[index],'nm.', 'The wavelength you wanted was: ', wavelenght,'nm.')


#careful fails at randwerte --> out of bounds
shift = 20
lower = index - shift
upper = index + shift + 1       #because of upper bound in mean_area_rho, see next line!

mean_area_rho = np.mean(rho[lower:upper,:],axis=0) #axis=0 is command for mean. otherwise it would give me only one value instead of a list.
#check
print(np.shape(rho[lower:upper,:]))
print(mean_area_rho)
print(rho[lower:upper,:])
print(np.shape(rho[lower:upper,:]))



#plot
plt.clf()
plt.grid()
plt.minorticks_on()

#plt.plot(theta_new,rho[index,:],'b-')       # without mean 
plt.plot(theta_new,mean_area_rho,'r-')      # with mean

plt.xlim(theta_new[0], theta_new[-1])
plt.xlabel(r'$\theta / \mathrm{°}$')
plt.ylabel(r'$\rho$')
plt.title('Messung bei einer Wellelänge von %i nm' % wavelenght)

#save
plt.savefig('build/rho_at_specific_wavelength_%i_nm.png' % wavelenght)
#***************************************************************************************************************************

#***************************************************************************************************************************
# progam to plot I against theta at a certain wavelength for positive an negative B field

#plot
plt.clf()
plt.grid()
plt.minorticks_on()

# Mittelwert der Intersität über den Bereich von vgl. lower upper.
#axis=0 is command for mean. otherwise it would give me only one value instead of a list.

#pos intensity
mean_intensity_pos = np.mean(mittelwert_matrix_new_pos[lower:upper,:],axis=0)
plt.plot(theta_new,mean_intensity_pos,'r-',label='pos. Magnetfeld')

#neg Intensity
mean_intensity_neg = np.mean(mittelwert_matrix_new_neg[lower:upper,:],axis=0)
plt.plot(theta_new,mean_intensity_neg,'b-',label='neg. Magnetfeld')

#format
plt.xlim(theta_new[0], theta_new[-1])
plt.xlabel(r'$\theta / \mathrm{°}$')
plt.ylabel(r'$I$')
plt.legend(loc='best')

plt.title('Intensität bei einer Wellenlämge von %i nm.' % wavelenght)

#save
plt.savefig('build/positive_and_negative_intensity_at_specific_wavelength_%i_nm.png' % wavelenght)
#***************************************************************************************************************************