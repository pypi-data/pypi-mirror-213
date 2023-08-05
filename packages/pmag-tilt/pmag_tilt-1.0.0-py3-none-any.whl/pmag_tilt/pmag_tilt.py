'''
This code package contains functions to perform the analysis needed for continental marginal tilt and as supplementary material to 
Mirzaei et al. (2023). However, it can also be used for the following applications: converting unit vectors from XYZ to polar
coordinates and vice versa, finding the angle between vectors (directions), APWP interpolation, and wherever the goal is to find
the amount of tilt (or folding) by comparing paleomagnetic directions.
These computational goals are achieved via modules, which are sets of functions of this code package. 
If one wants to export and share some parts of the package, it can be easily done to consider different modules.


The software is provided "AS IS", without warranty of any kind, express or
Implied, including but not limited to the warranties of merchantability,
Fitness for a particular purpose and non-infringement. In no event shall the
Authors or copyright holders be liable for any claim, damages, or other
Liability, whether in an action of contract, tort or otherwise, arising from,
Out of or in connection with the software or the use or other dealings in the
Software.

by MMS_Summer2023
'''
import numpy as np
from numpy import deg2rad, rad2deg, cos, sin, arccos, arcsin, arctan2
from pmagpy import pmag
from scipy.spatial import geometric_slerp as slerp
import matplotlib.pyplot as plt


def sph2xyz(latlon):
    lat= deg2rad(latlon[0])
    lon= deg2rad(latlon[1])
    x = cos(lat)*cos(lon)
    y = cos(lat)*sin(lon)
    z = sin(lat)
    return np.asarray([x,y,z])

def xyz2sph(xyz):
    lenght = np.sqrt(xyz[0]**2+xyz[1]**2+xyz[2]**2)
    lat = arcsin(xyz[2]/lenght)
    lon = arctan2(xyz[1], xyz[0])
    return np.asarray([rad2deg(lat), rad2deg(lon) if rad2deg(lon)>=0 else 360+rad2deg(lon)])

def angle(v1,v2):
    """
    takes two vectors in lat/lon format and returns the angle between in radians
    """
    if len(v1) == 2:
        v1 = sph2xyz(v1)
        v2 = sph2xyz(v2)
    
    return arccos(np.dot(v1,v2))

"""""""""
The module to find the Tilting Axis from directions of a certain pmag poles to concide with the reference direction set.
This is designed for North American APWP dispute in mid Jurassic. 
Module ftilt.py 
"""""""""

def ftilt(file='', apwpRef = 'apwp_interpolated.txt', output= False):
    """
    This is the main function for ftilt module. It takes pole coordinates and age to calculate the tilting axis 
    with reference apwp sequence. The input text should have the following header format:
    "plat    plong  slat    slong   age (has to be rounded to the nearest 0.5 Myrs)"
    *site coordinates should be set for the region of comparison, and this might not necessary match the 
    actual site location of the correponding pmag pole.
    This looks for the reference apwp sequesnce (like the output of apwp function)
    in the working directory to find tilting axis from this reference apwp. In the function arguments name of apwp could be changed.
    positive sign of tilting means clockwise tilting looking toward the azimuth of tilting axis.
    """
    input = np.loadtxt(file, skiprows=1)
    if input.ndim <= 1:
        input = np.asarray([input])
    
    apwp = np.loadtxt(apwpRef, skiprows=1)
    if apwp.ndim <= 1:
        apwp = np.asarray([apwp])
    
    #creating the to-be-compared directions from poles at the target site coordinates:
    decs, incs = ([]), ([]) # to-be-compared directions
    rdecs, rincs = ([]), ([]) #reference directions 
    for i in range(len(input)): 
        dec, inc = pmag.vgp_di(input[i,0],input[i,1],input[i,2],input[i,3])
        decs = np.append(decs,dec)                                      
        incs = np.append(incs, inc)   
        inx = find_closest(apwp[:,2],input[i,4])
        if (apwp[inx,2] == input[i,4]):
            rdec, rinc = pmag.vgp_di(apwp[inx,0],apwp[inx,1],input[i,2],input[i,3])
        else:
            rdec, rinc = None, None
        rdecs = np.append(rdecs, rdec)                                      
        rincs = np.append(rincs, rinc)

    data =np.column_stack((incs, decs, rincs, rdecs, input[:,4])) #creating data table 

    #lints, cents, ages = ([]), ([]), ([]) #creating line of intersecions and centers of pair directions and ages vector
    taxs, tilts, ages = ([]), ([]), ([])
    for i in range(len(data)):
        if data[i,2] != None:
            lint = np.cross(sph2xyz(data[i,:2]).astype(np.float64), sph2xyz(data[i,2:4].astype(np.float64)))
            #lints = np.append(lints, lint)
            cent = sph2xyz([(data[i,0]+data[i,2])/2,(data[i,1]+data[i,3])/2])
            #cents = np.append(cents, cent)
            ages = np.append(ages, data[i,4])
            
            pint = np.cross(lint, cent)
            #finding tilting axis
            if lint[2] < 0: # checks if the z value is up or down and set the sense of the tilting accordingly 
                tax = ((xyz2sph(pint)[1])+90)%360
            else:
                tax = ((xyz2sph(pint)[1])-90)%360
            
            taxs = np.append(taxs, tax) #appending the trends of the tiltiing axis
            
            #findindg the amount of rotation via auxilary Lines 1 & 2
            taxv = sph2xyz([0, tax])
            aux1 = np.cross(taxv.astype(np.float64), sph2xyz(data[i,:2]))
            aux2 = np.cross(taxv.astype(np.float64), sph2xyz(data[i,2:4]))
            tilt = xyz2sph(aux1)[0] - xyz2sph(aux2)[0]
            tilts = np.append(tilts, tilt)
        else: 
            continue

    
    #generating output array
    out = np.column_stack((taxs, tilts, ages))

    if output == True:
        np.savetxt(f'tilting_axis_{file}',out,fmt=['%.4f','%.4f','%.4f'],header='azi of tiltiling axis\tamount of tilting\tage', comments='', delimiter='\t')
       
    return out


def apwp(file='', ageint = 0.5, output = False, plot = False, sphere = False):
    """
    This function takes a apwp text file with below header structure:
    "plat    plong   age" (poles should be in the decending order)
    and interpolates in 3d with the defined age spacing (in Myrs)  and also plots them if wanted.    
    """
    input = np.loadtxt(file,skiprows=1)
    segs = len(input[:,:2])-1
    poles = input[:,:2] #take poles coordinated (latlon)
    ages = input[:,2:] #take poles ages (Ma)
    old_age = input[:,2:][-1] #considering that the input file is in such a way that youngest age is the first entry 
    young_age = input[:,2:][0]
    interval = ages[1] - ages[0]
    agespacing = ageint * (1/interval)
    apwp = np.zeros(3)
    for i in range(len(poles)):
        polexyz = sph2xyz(poles[i])
        apwp = np.vstack((apwp,polexyz))
    
    apwp = np.delete(apwp,0,0)
    #generating 0.5 My APWP spacing:
    results=np.zeros(3)
    for i in range(segs):
        start = apwp[i]
        end = apwp[i+1]
        t_vals = np.arange(0,1,agespacing)
        result = slerp(start, end, t_vals)
        results = np.vstack((results,result))
        
    results = np.delete(results,0,0)
    #plotting and interpolation in 3d/spherical 
    if plot == True:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
        if sphere == True:
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x, y, z, color='y' ,alpha=0.2)
    
        ax.plot(results[:,0], results[:,1], results[:,2], c='k')
        plt.show()
    #generating results in lat long format:
    resultssph = np.zeros(2)
    for i in range(len(results)):
        latlon = xyz2sph(results[i])
        resultssph = np.vstack((resultssph,latlon))
    
    resultssph = np.delete(resultssph,0,0)
    #adding age time line to the file
    resultswtage = np.insert(resultssph,2,np.arange(young_age,old_age,ageint),axis=1)
    resultswtage = np.vstack((resultswtage,[poles[-1][0],poles[-1][1],float(old_age)]))
 
    if output == True:
        np.savetxt(f'{file}_interpolated.txt',resultswtage,fmt=['%.4f','%.4f','%.2f'],header='lat\tlon\tage', comments='', delimiter='\t')
       
    return resultswtage

def find_closest(arr, val):
    idx = np.abs(arr - val).argmin()
    return idx

def make_dir(file='swath_ML_inter.txt', coor='section_coor_int.txt', output=False):
    '''
    this function is for modification of the input files of the ftilt function.
    '''
    input = np.loadtxt(file, skiprows=1)
    coor = np.loadtxt(coor, skiprows=1)
    for j in range(len(coor)):
        results = np.zeros(5)
        for i in range(len(input)):
            result = np.asarray([input[i,0], input[i,1], coor[j,0], coor[j,1], input[i,2]])
            results = np.vstack((results, result))
        results = np.delete(results,0,0)
        if output == True:
            np.savetxt(f'swath_ML_{coor[j,2]}km.txt',results,fmt=['%.4f','%.4f','%.4f','%.4f','%.2f'],header='Plat\tPlon\tSlat\tSlong\tage', comments='', delimiter='\t')

    return   results
