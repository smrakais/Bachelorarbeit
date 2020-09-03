import numpy as np
import matplotlib.pyplot as plt


'''
alles sollen funktionen sein

ich über geben einer funktion den datensatz und die printed mir den graphen


bspl call_colormesh_int()
     call_rho_angle()
'''

##############
####Basics####
##############
# Set wavelength
wl=np.genfromtxt('775nm_grating3_wellenlängenbereich.txt',usecols=(0)) #only takes the first column (spalte)

# Set angle
theta=np.linspace(-23.578,23.578,256) #without sensor correction


#####################
####calculate rho####
#####################
def rho (mm_pos,mm_neg):
   return (mm_pos - mm_neg) / (mm_pos + mm_neg)
     

###########################
####Colormap: Intensity####
###########################
def colormap_intensity(PathData, start, stop):          # minValue of start = 0
                                                        # maxValue of stop = 257 (if you go higher it will ignore it)
                                                        # name of Data that is used
    data = np.load(PathData)
    mm = data['mm']                                     # select data --> look einlesen.py
    mm = mm[:,start:stop]                               # sensorfield  correction
    theta_new = np.linspace(-23.578,23.578,mm.shape[1]) # because of the greatness of the sensorfield
    
    plt.pcolormesh(theta_new,wl,mm,cmap='hot')          # make the axes correct x,y,matrix
    plt.gca().invert_yaxis()                            # inverts the y axis
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\lambda / \mathrm{nm}$')
    plt.title('Photolumineszenz')
    cbar = plt.colorbar()
    cbar.set_label('Intensity')
    
    #plt.show()
    plt.savefig('build/colormap__intensity_photolumineszenz_' + PathData + '.png')
    plt.clf()

#example
#call function to pass data, start and stop
colormap_intensity('read_data.npz',15,244)

##############################################
####colormap: relative change in intensity#### 
##############################################
def colormap_change_intensity(PathData, start, stop):
    
    data = np.load(PathData)
    mm = data['mm']
    mm_pos = data['mm_pos']
    mm_neg = data['mm_neg']  

    mm = mm[:,start:stop]
    mm_pos = mm_pos[:,start:stop]
    mm_neg = mm_neg[:,start:stop]  

    theta_new = np.linspace(-23.578,23.578,mm.shape[1])
    
    plt.pcolormesh(theta_new,wl,rho(mm_pos,mm_neg),cmap='bwr')
    plt.clim(-0.15,0.15)        #bar limit
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\lambda / \mathrm{nm}$')
    plt.title('relative Änderung der Intensität')
    plt.gca().invert_yaxis()
    cbar = plt.colorbar()
    cbar.set_label('relative Intensity')

    plt.savefig('build/colormap_rel_change_intensity_'  + PathData + '.png')
    plt.clf()

#example
#call function
colormap_change_intensity('read_data.npz',15,244)

####################################################################
####plot: rho at a specific wavelenght with respect to the angle####
####################################################################

def pot_rho_specific_wavelenght(PathData, wavelenght):

    minimized_array = abs(wl-wavelenght)                    #minimal array
    #print(minimized_array)

    minimum_value = np.amin(minimized_array)                #find minimum_value of array
    #print(minimum_value)

    index = np.where(minimized_array == minimum_value)      #index of the minimum
    #print(index[0][0])                                     #only index 
    index = index[0][0]
    print('You selected the wavelength:', wl[index],'nm.', 'The wavelength you wanted was: ', wavelenght,'nm.')


    #careful fails at boundries --> out of bounds
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

pot_rho_specific_wavelenght('read_data.npz',470,)