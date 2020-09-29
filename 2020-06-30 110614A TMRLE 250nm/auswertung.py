import numpy as np
import matplotlib.pyplot as plt
'''
Das ist die Verbsserung.
Alles ist in Funktionen geliedert und kann viel besser und bequemer
aufgerufen werden.
Das Skript kann aber noch verbessert werden. :)
'''


'''
##########################
####Tipps für den Code####
##########################   
fig = plt.gca() #gca() makes it object orientated

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
####shift#### -----> noch nicht verwendet
def shift(area,index):                                  # careful can fail at boundries!
    lower = index - area
    upper = index + area + 1 
    return lower, upper

###########################
####Colormap: Intensity####
###########################
def colormap_intensity(PathData, start, stop):          # minValue of start = 0
                                                        # maxValue of stop = 257 (if you go higher it will ignore it)                                                        
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

    plt.xlim(-20, 20) #changed#
    plt.ylim(755, 730) #changed#
    #plt.show()
    plt.savefig('build/colormap__intensity_photolumineszenz_' + PathData + '.png') # colormaps as png because eps takes to long
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

    plt.xlim(-20, 20) #changed#
    plt.ylim(755,730) #changed#
    plt.savefig('build/colormap_rel_change_intensity_'  + PathData + '.png') # colormaps as png because eps takes to long
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
    #print(value_rho)
    mean_area_rho = np.mean(value_rho[lower:upper,:],axis=0) # axis=0 command for mean. otherwise --> only one value instead of a list.
    
    #plot
    plt.grid()
    plt.minorticks_on()

    theta_new = np.linspace(-23.578,23.578,mm.shape[1])

    plt.plot(theta_new,mean_area_rho,'r-')
    #plt.xlim(theta_new[0], theta_new[-1])
    plt.xlim(-20, 20) #changed#
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\rho$')
    plt.title('Messung bei einer Wellelänge von %i nm' % wavelenght)

    #save
    plt.savefig('build/rho_at_specific_wavelength_%i_nm_' % wavelenght + PathData + '.eps' )
    plt.clf()

#######################################################################################################
####plot: intensity with respect to theta for positive and negative B-field for specific wavelenght####
#######################################################################################################
def plot_intensity_pos_neg_b_field(PathData,wavelength, start, stop):

    data = np.load(PathData)

    mm = data['mm']
    mm_pos = data['mm_pos']
    mm_neg = data['mm_neg']  

    mm = mm[:,start:stop]
    mm_pos = mm_pos[:,start:stop]
    mm_neg = mm_neg[:,start:stop] 
      
    minimized_array = abs(wl-wavelength)                    # minimal array
    #print(minimized_array)

    minimum_value = np.amin(minimized_array)                # find minimum_value of array
    #print(minimum_value)

    index = np.where(minimized_array == minimum_value)      # index of the minimum
    #print(index[0][0])                                      # only index 
    index = index[0][0]
    print('You selected the wavelength:', wl[index],'nm.', 'The wavelength you wanted was: ', wavelength,'nm.')

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
    #plt.xlim(theta_new[0], theta_new[-1])
    plt.xlim(-20, 20) #changed#
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$I$')
    plt.legend(loc='best')

    plt.title('Intensität bei einer Wellenlänge von %i nm.' % wavelength)

    #save
    #plt.show()
    plt.savefig('build/positive_and_negative_intensity_at_specific_wavelength_%i_nm_' % wavelength + PathData + '.eps' )
    plt.clf()

#############################################################################################
####plot: different rho's at a specific wavelenght and temperature with respect to theta ####
#############################################################################################
#for labels
#names = ['4K','5K','10K','10K','15K','20K','25K','25K','35K','35K','45K','45K']
#names = ['4K','10K','20K','45K']

def plot_rho_diff_temp_const_wavelength(PathData,wavelength,start,stop,temps):
    max_values = []                                            #maximum values of rho 

    plt.grid()
    plt.minorticks_on()

    for enum, index in enumerate(PathData):# so bekommst du die zahl des durchlaufes noch raus wird in enum gespeichert.
        
        data = index

        mm = data['mm']
        mm_pos = data['mm_pos']
        mm_neg = data['mm_neg']

        #korrektur sensorgröße
        mm = mm[:,start:stop]                                    
        mm_pos = mm_pos[:,start:stop]
        mm_neg = mm_neg[:,start:stop]

        minimized_array = abs(wl-wavelength)                    # minimal array #TODO   
        minimum_value = np.amin(minimized_array)                # find minimum_value of array        
        index = np.where(minimized_array == minimum_value)      # index of the minimum                                   
        index = index[0][0]                                     # only index
        print('You selected the wavelength:' + str(wl[index])+ 'nm. The wavelength you wanted was: ' + str(wavelength) +'nm.')

        #shift
        shift = 20                                              # can fail at boundries                 
        lower = index - shift
        upper = index + shift + 1
    
        rho(mm_pos,mm_neg)
        value_rho = rho(mm_pos,mm_neg)
        mean_intensity_rho = np.mean(value_rho[lower:upper,:],axis=0)
        theta_new = np.linspace(-23.578,23.578,mm.shape[1])

        plt.plot(theta_new,mean_intensity_rho,label = temps[enum])
        
        #plt.xlim(theta[0], theta[-1])
        
        plt.xlim(-20, 20) #changed#
        plt.xlabel(r'$\theta / \mathrm{°}$')
        plt.ylabel(r'$\rho$')
        plt.legend(ncol=2)
        plt.title(' Messung bei einer Wellenlänge von %i nm.' % wavelength)
        
        #############################################################
        ####find max value of rho with respect to the angle theta####
        #############################################################
        #print(np.argmax(mean_intensity_rho)) #damit habe ich nur die stelle (index) rausgefunden bei der der maximale wert ist.
        #print(mean_intensity_rho[53])        
        max_values.append(max(mean_intensity_rho))    
        #print(theta_new[53]) # = -12.758
    

    plt.axvline(x=-12.758,color ='gold',linestyle = '--')
    plt.axvline(x=12.758,color ='gold',linestyle = '--')
    
    #plt.show()
    ###############################
    ####Teil des Speichernamens####
    ###############################
    save = ''
    for entry in temps:
        save+=entry
        

    plt.savefig('build/Temperaturabhaengigkeit_rho_at_%i_nm_' %wavelength + save + '.eps')
    plt.clf()
    return max_values


#######################################################
####maximum values of rho with respect to the angle####
#######################################################
def plot_max_values_of_rho(max_values,temps):
    plt.plot(temps,max_values,'r+',label = 'maximale rho')
    plt.show()
    plt.clf()

#example
colormap_intensity('read_data.npz',15,244)
colormap_change_intensity('read_data.npz',15,244)
plot_rho_specific_wavelenght('read_data.npz',740,15,244)
#plot_rho_specific_wavelenght('read_data.npz',750,15,244)
#plot_rho_specific_wavelenght('022818A 250nm 10K 2020-07-20.npz',739,13,245)
#plot_rho_specific_wavelenght('read_data.npz',831,15,244)
#plot_intensity_pos_neg_b_field('read_data.npz',740,14,255)
#
#alle Temperaturen
Temperaturabhängigkeit = [np.load('Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 5K 2020-07-20.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-20.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 15K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 20K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-31.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-31.npz')]
                         
temps = ['4K','5K','10K','10K','15K','20K','25K','25K','35K','35K','45K','45K']
#boundries from Lars
plot_max_values_of_rho(plot_rho_diff_temp_const_wavelength(Temperaturabhängigkeit,740,13,245,temps),temps) #die messung 25K_2 wegwerfen und die frühere von 45K


#4 Temperaturen
Temperaturabhängigkeit = [np.load('Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz'),  
                          np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-20.npz'),
                          np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-23.npz'),
                          np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-27.npz')] 
temps = ['4K','10K','25K','45K']
plot_rho_diff_temp_const_wavelength(Temperaturabhängigkeit,740,13,245,temps) #die messung 25K_2 wegwerfen und die frühere von 45K
