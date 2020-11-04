import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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
#############
def shift(area,index):                                  # careful can fail at boundries!
    lower = index - area
    upper = index + area + 1 
    return lower, upper

########################
####rho_fit_function####
########################
def rho_fit_func(x, T_off, C_0):
    # % Function to fit Temp dependence of C/rho
    # % See Felix Dis, eq 8.14
    # % Brill function 4.1, 4.2
    S = 5/2
    g_Mn = 2.01
    mu_B = 9.2740100783e-24                             #% J/T
    k_B  = 1.380649e-23                                 #% J/K
    B = 0.5                                             #% T
    T_0 = 1                                             #%K
    kappa = S*mu_B*g_Mn*B/k_B
    Xi = kappa / (x+T_0+T_off)
    
    # coth = cosh / sinh
    Bril = (2*S+1)/(2*S)*(np.cosh((2*S+1)/(2*S)*Xi)/np.sinh((2*S+1)/(2*S)*Xi)) - 1/(2*S)*(np.cosh(1/(2*S)*Xi)/np.sinh(1/(2*S)*Xi))

    return C_0 * Bril

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
    cbar.set_label('Intensität / a.u.')

    plt.xlim(-20, 20) #changed#
    plt.ylim(750, 725) #changed#
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
    #plt.tight_layout()
    plt.pcolormesh(theta_new,wl,rho(mm_pos,mm_neg),cmap='bwr')
    plt.clim(-0.15,0.15)        #bar limit
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\lambda / \mathrm{nm}$')
    plt.title('relative Änderung der Intensität')
    plt.gca().invert_yaxis()
    cbar = plt.colorbar()
    cbar.set_label('relative Intensität')

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
    print(type(mm))
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
    
    ####C_0 calculation####
    #C_0 = (mean_area_rho - np.flip(mean_area_rho))/2
    #plt.plot(theta_new,C_0)
    #plt.ylabel(r'$c_o$')

    plt.plot(theta_new,mean_area_rho,'r-')
    ##plt.xlim(theta_new[0], theta_new[-1])
    plt.xlim(-20, 20) #changed#
    plt.xlabel(r'$\theta / \mathrm{°}$')
    plt.ylabel(r'$\rho$')
    plt.title('Messung bei einer Wellelänge von %i nm' % wavelenght)
    #plt.title('Messung bei einer Wellelänge von %i nm (korrigiert)' % wavelenght)

    #save
    plt.savefig('build/rho_at_specific_wavelength_%i_nm_' % wavelenght + PathData + '.pdf' )
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
    plt.ylabel('Intensität / a.u.')
    plt.legend(loc='best')

    plt.title('Intensität bei einer Wellenlänge von %i nm.' % wavelength)

    #save
    #plt.show()
    plt.savefig('build/positive_and_negative_intensity_at_specific_wavelength_%i_nm_' % wavelength + PathData + '.pdf' )
    plt.clf()

#############################################################################################
####plot: different rho's at a specific wavelenght and temperature with respect to theta ####
#############################################################################################
#for labels
#names = ['4K','5K','10K','10K','15K','20K','25K','25K','35K','35K','45K','45K']
#names = ['4K','10K','20K','45K']

def plot_rho_diff_temp_const_wavelength(PathData,wavelength,start,stop,temps):
    max_values = []                                            #maximum values of rho 
    max_values_c = []

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
        #plt.plot(theta_new,mean_intensity_rho,label = temps[enum])
        #plt.ylabel(r'$\rho$')


        ####C_0 calculation####
        C_0 = (mean_intensity_rho - np.flip(mean_intensity_rho))/2
        plt.plot(theta_new,C_0,label = temps[enum])
        plt.ylabel(r'$c_o$')

        
        #plt.xlim(theta[0], theta[-1])
        plt.xlim(-20, 20) #changed#
        plt.xlabel(r'$\theta / \mathrm{°}$')
        plt.legend(ncol=2)
        plt.title(' Messung bei einer Wellenlänge von %i nm.' % wavelength)
        
        ####find max value of rho with respect to the angle theta####        
        #print(np.argmax(mean_intensity_rho))       #   Index stelle wo max wert in array ist (rho)
       
        #print(np.argmax(C_0))                       #   Index stelle wo max wert in array ist (c_0)
        #print(C_0[np.argmax(C_0)])                  #   wert von c0 an der mx stelle

        ####PRINT####
        #Der printed jetzt die max werte von c_0 und die dazugehörigen winkel
        print('C_0 = ' + str(max(C_0)))                             #   wert von c0 an der mx stelle (alternative)
        print('WINKEL = ' + str(theta_new[np.argmax(C_0)]))

        #print(mean_intensity_rho[53])        
        max_values.append(max(mean_intensity_rho))
        max_values_c.append(max(C_0))               #ACHTUNG FEHLER NICHT IM CODE ABER DIE OSZILATIONEN AM ENDE ÜBERTRUMPFEN DAS EIG. MAXIMUM 
        #print(theta_new[48]) # = -13.5752
        #print(theta_new[49]) # = -13.7793
        #print(theta_new[52]) # =-12.9627

    plt.axvline(x=-13.5752,color ='gold',linestyle = '--')
    plt.axvline(x=13.5752,color ='gold',linestyle = '--')
    plt.axvline(x=-14,color ='gold',linestyle = '--')
    plt.axvline(x=14,color ='gold',linestyle = '--')

    #plt.show()
    ####Teil des Speichernamens####
    save = ''
    for entry in temps:
        save+=entry
        

    plt.savefig('build/Temperaturabhaengigkeit_rho_at_%i_nm_' %wavelength + save + '.pdf')
    plt.clf()
    #print(max_values)
    #print(np.argmax(C_0))
    return max_values_c
    #return max_values

#######################################################
####maximum values of rho with respect to the angle####
#######################################################
#temps bei aufruf bitte immer anpassen!
def plot_max_values_of_rho(max_values,temps_value):
    plt.plot(temps_value,max_values,'r+',label = 'Maximale Effektstärke')
    print(temps_value)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel(r'$T$ / K')
    #plt.ylabel(r'$\rho$')
    plt.ylabel(r'$c_0$')
    plt.title('Maximale Effektstärke bei unterschiedlichen Temperaturen.')

    ###########
    ####FIT####
    ###########    
    params, covariance_matrix = curve_fit(rho_fit_func,temps_value,max_values)
    errors = np.sqrt(np.diag(covariance_matrix))
    print('T_off =',params[0], '±', errors[0])
    print('C_0 =', params[1], '±', errors[1])    
    temps_value_new = np.linspace(temps_value[0],temps_value [-1],100)
    plt.plot(temps_value_new, rho_fit_func(temps_value_new, *params), "b-", label=r'Fit')
    plt.legend(ncol=2)    

    plt.savefig('build/Maximale_Rho_bei_Temperaturabhänigkeit.pdf')
    plt.clf()

################################################
####Intensity with respect to the wavelenght####
################################################
def max_value_intensity(PathData,temps):
    plt.grid()
    #plt.minorticks_on()
    for enum,index in enumerate(PathData) :
        #data = np.load(PathData)
        data = np.load(index)
        mm = data['mm']    
        mm = mm[:,179] #wegen 0 zähler
        #mm = mm[:,190] # 256/2 = 178 da ist theta = 0  hab da etwas verschoben weil der Graph bei0grad net ganz speigelsymm ist 
        plt.plot(np.linspace(688.745,860.588,1024),mm,label = temps[enum])
        plt.legend(ncol=2)   
        plt.xlim(725,750)
        plt.xlabel('$\lambda / \mathrm{nm}$')
        plt.ylabel('Intensität / a.u.')
        plt.title('Maximum der Photolumineszent bei '+'$\lambda = 737,7\mathrm{nm}$')
    plt.savefig('build/max_value_Pl.pdf')
    plt.clf()

#example
#colormap_intensity('read_data.npz',15,244)
colormap_intensity('022818A 250nm 4K 2020-07-14.npz',15,244)
#colormap_change_intensity('read_data.npz',15,244)
colormap_change_intensity('022818A 250nm 4K 2020-07-14.npz',15,244)
#plot_rho_specific_wavelenght('read_data.npz',740,15,244)
#plot_rho_specific_wavelenght('read_data.npz',750,15,244)
plot_rho_specific_wavelenght('022818A 250nm 4K 2020-07-14.npz',737,13,245) #test GaAS Linie
plot_rho_specific_wavelenght('022818A 250nm 4K 2020-07-14.npz',830,13,245) #test GaAS Linie

#plot_rho_specific_wavelenght('read_data.npz',831,15,244)
plot_intensity_pos_neg_b_field('022818A 250nm 4K 2020-07-14.npz',737,14,255)
#
#alle Temperaturen
Temperaturabhängigkeit = [np.load('Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 5K 2020-07-20.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-20.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 15K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 20K 2020-07-23.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-23.npz'),
                            #np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-31.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-27.npz'),
                            np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-31.npz')]
                         
temps = ['4K','5K','10K','10K','15K','20K','25K','35K','35K','45K','45K']
temps_value = [4,5,10,10,15,20,25,35,35,45,45]

#boundries from Lars
#temps bei aufruf bitte immer anpassen!
plot_max_values_of_rho(plot_rho_diff_temp_const_wavelength(Temperaturabhängigkeit,738,13,245,temps),temps_value) #die messung 25K_2 wegwerfen


#4 Temperaturen
Temperaturabhängigkeit = [np.load('Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz'),  
                          np.load('Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-20.npz'),
                          np.load('Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-23.npz'),
                          np.load('Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-27.npz')] 
temps = ['4K','10K','25K','45K']
plot_rho_diff_temp_const_wavelength(Temperaturabhängigkeit,738,13,245,temps) #die messung 25K_2 wegwerfen

#################################################################################################################### 
Temperaturabhängigkeit =   ['Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 5K 2020-07-20.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-20.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 10K 2020-07-23.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 15K 2020-07-23.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 20K 2020-07-23.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 25K 2020-07-23.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-27.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 35K 2020-07-31.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-27.npz',
                            'Temperaturabhaengigkeit/022818A 250nm 45K 2020-07-31.npz']
temps = ['4K','5K','10K','10K','15K','20K','25K','35K','35K','45K','45K']

#max_value_intensity('Temperaturabhaengigkeit/022818A 250nm 4K 2020-07-14.npz') geht net die funktionmuss modifiziert werden
max_value_intensity(Temperaturabhängigkeit,temps)
#################################################################################################################### 
