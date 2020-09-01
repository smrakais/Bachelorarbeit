import numpy as np
import matplotlib.pyplot as plt
#import glob
#from  natsort import natsorted
#import time


#load data
data = np.load('read_data.npz')

#selecting the specific values
mm = data['mm']
mm_pos = data['mm_pos']
mm_neg = data['mm_neg']


#daten der Temperaturabhängigkeit in array laden
Temperaturabhängigkeit = [np.load('read_data_4K.npz'),np.load('read_data_5K.npz'),
                          np.load('read_data_10K.npz'),np.load('read_data_10K_2.npz'),
                          np.load('read_data_15K.npz'),np.load('read_data_20K.npz'),
                          np.load('read_data_25K.npz'),np.load('read_data_25K_2.npz'),
                          np.load('read_data_35K.npz'),np.load('read_data_35K_2.npz'),
                          np.load('read_data_45K.npz'),np.load('read_data_45K_2.npz')] 


#korrektur sensorgröße
mm = mm[:,15:244]
mm_pos = mm_pos[:,15:244]
mm_neg = mm_neg[:,15:244]


# Set wavelength
wl=np.genfromtxt('775nm_grating3_wellenlängenbereich.txt',usecols=(0)) #only takes the first column (spalte)
# Set angle
theta=np.linspace(-23.578,23.578,256)
theta_new=np.linspace(-23.578,23.578,mm.shape[1]) # because of the greatness of the sensor field

#***************************************************************************************************************************
#Colormap plot
plt.pcolormesh(theta_new,wl,mm,cmap='hot') # make the axes correct x,y,matrix
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
rho = (mm_pos - mm_neg) / (mm_pos + mm_neg)
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
#print(np.shape(rho[lower:upper,:]))
#print(mean_area_rho)
#print(rho[lower:upper,:])
#print(np.shape(rho[lower:upper,:]))


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
mean_intensity_pos = np.mean(mm_pos[lower:upper,:],axis=0)
plt.plot(theta_new,mean_intensity_pos,'r-',label='pos. Magnetfeld')

#neg Intensity
mean_intensity_neg = np.mean(mm_neg[lower:upper,:],axis=0)
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

#***************************************************************************************************************************
#program to plot the intensity against the angle at a certain wavelength

#plot
plt.clf()
plt.grid()
plt.minorticks_on()

#for labels
names = ['4K','5K','10K','10K','15K','20K','25K','25K','35K','35K','45K','45K']

for enum, index in enumerate(Temperaturabhängigkeit):# so bekommst du die zahl des durchlaufes noch raus
    #load data
    
    data = index

    #get value ohne sensorkorrektur
    mm = data['mm']
    mm_pos = data['mm_pos']
    mm_neg = data['mm_neg']

    #korrektur sensorgröße
    mm = mm[:,13:245]           #neuer bereich von lars vorgegeben
    mm_pos = mm_pos[:,13:245]
    mm_neg = mm_neg[:,13:245]

    #plot
    rho = (mm_pos - mm_neg) / (mm_pos + mm_neg)
    mean_intensity_rho = np.mean(rho[lower:upper,:],axis=0)
    theta_new=np.linspace(-23.578,23.578,mm.shape[1])
    plt.plot(theta_new,mean_intensity_rho,label = names[enum])

    #format
    plt.xlim(theta[0], theta[-1])
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\rho$')
    plt.legend(ncol=2)
    #plt.legend(loc='best',ncol=2)
    plt.title(' Messung bei einer Wellenlämge von %i nm.' % wavelenght)

plt.savefig('build/Temperaturabhaenigkeit.png')
##***************************************************************************************************************************