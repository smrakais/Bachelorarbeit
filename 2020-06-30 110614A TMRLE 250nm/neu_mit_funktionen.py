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

#############     
####shift#### -----> noch nicht eingesetzt
#############
def shift(area,index):                                  # careful can fail at boundries!
    lower = index - area
    upper = index + area + 1 
    return lower, upper

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

##############################################
####colormap: relative change in intensity#### 
##############################################
def colormap_change_intensity(PathData, start, stop):
    
    data = np.load(PathData)                #TODO extra load funktion + cut--> def load_and_cut():
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

####################################################################
####plot: rho at a specific wavelenght with respect to the angle####
####################################################################

def plot_rho_specific_wavelenght(PathData, wavelenght, start, stop):

    data = np.load(PathData)

    mm = data['mm']
    mm_pos = data['mm_pos']
    mm_neg = data['mm_neg']  

    mm = mm[:,start:stop]
    mm_pos = mm_pos[:,start:stop]
    mm_neg = mm_neg[:,start:stop]  

    minimized_array = abs(wl-wavelenght)                    # minimal array
    minimum_value = np.amin(minimized_array)                # find minimum_value of array
    
    index = np.where(minimized_array == minimum_value)      # index of the minimum
    #print(index[0][0])                                     # only index 
    index = index[0][0]
    print('You selected the wavelength:', wl[index],'nm.', 'The wavelength you wanted was: ', wavelenght,'nm.')

    shift = 20                                              # careful fails at boundries --> out of bounds #TODO extra funktion
    lower = index - shift
    upper = index + shift + 1                               # because of upper bound in mean_area_rho, see next line!

    value_rho = rho(mm_pos,mm_neg)
    mean_area_rho = np.mean(value_rho[lower:upper,:],axis=0) # axis=0 command for mean. otherwise --> only one value instead of a list.

    #plot
    plt.grid()
    plt.minorticks_on()

    theta_new = np.linspace(-23.578,23.578,mm.shape[1])

    plt.plot(theta_new,mean_area_rho,'r-')
    plt.xlim(theta_new[0], theta_new[-1])
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\rho$')
    plt.title('Messung bei einer Wellelänge von %i nm' % wavelenght)

    #save
    plt.savefig('build/rho_at_specific_wavelength_%i_nm_' % wavelenght + PathData + '.png' )
    plt.clf()

#######################################################################################################
####plot: intensity with respect to theta for positive and negative B-field for specific wavelenght####
#######################################################################################################

def plot_intensity_pos_neg_b_field(PathData,wavelenght, start, stop):

    data = np.load(PathData)

    mm = data['mm']
    mm_pos = data['mm_pos']
    mm_neg = data['mm_neg']  

    mm = mm[:,start:stop]
    mm_pos = mm_pos[:,start:stop]
    mm_neg = mm_neg[:,start:stop] 
      
    minimized_array = abs(wl-wavelenght)                    # minimal array
    #print(minimized_array)

    minimum_value = np.amin(minimized_array)                # find minimum_value of array
    #print(minimum_value)

    index = np.where(minimized_array == minimum_value)      # index of the minimum
    print(index[0][0])                                      # only index 
    index = index[0][0]
    print('You selected the wavelength:', wl[index],'nm.', 'The wavelength you wanted was: ', wavelenght,'nm.')

    #shift
    shift = 20                          # can fail at boundries                 
    lower = index - shift
    upper = index + shift + 1

    #plot
    plt.grid()
    plt.minorticks_on()

    #pos intensity
    theta_new = np.linspace(-23.578,23.578,mm.shape[1])
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
    #plt.show()
    plt.savefig('build/positive_and_negative_intensity_at_specific_wavelength_%i_nm_' % wavelenght + PathData + '.png' )



#example
colormap_intensity('read_data.npz',15,244)
colormap_change_intensity('read_data.npz',15,244)
plot_rho_specific_wavelenght('read_data.npz',740,15,244)
plot_rho_specific_wavelenght('read_data.npz',750,15,244)
plot_rho_specific_wavelenght('read_data.npz',831,15,244)
plot_intensity_pos_neg_b_field('read_data.npz',740,14,255)