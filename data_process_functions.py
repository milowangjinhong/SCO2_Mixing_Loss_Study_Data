import os
import numpy as np

# ===========================================================================================================================
# File saving and reading

def saving_XY(X,Y, file_name, x_name, y_name, note, format = '%-18.15f'):
    
    i = 1
    file_name_now = file_name
    while os.path.exists(file_name_now + '.txt'):
        file_name_now = file_name + '%i'%(i)
        i = i+1
    
    name = file_name_now + '.txt'
    with open(name, 'w') as outfile:

        outfile.write('# %s, %s, %s\n'%(x_name, y_name, note))

        outfile.write('# x array\n')
        np.savetxt(outfile, X.reshape(1,len(X)), fmt=format)
        
        outfile.write('# y arrays\n')
        np.savetxt(outfile, np.array([len(Y)]), fmt=format)
        for i in range(len(Y)):
            np.savetxt(outfile, Y[i].reshape(1,len(Y[i])), fmt=format)
    
    return name

def reading_XY(file_name):
    X = np.loadtxt(file_name,skiprows=2, max_rows=1)
    ny = int(np.loadtxt(file_name,skiprows=4, max_rows=1))
    
    Y = []
    for i in range(ny):
        Y.append(np.loadtxt(file_name,skiprows=5+i, max_rows=1))
        #print(Y[i])
        
    return X, Y

# saving 3D matrices in txt file
def saving_3D_array(x,y,z,Array, file_name, format = '%-18.15f'):
    
    i = 1
    file_name_now = file_name
    while os.path.exists(file_name_now + '.txt'):
        file_name_now = file_name + '%i'%(i)
        i = i+1

    name = file_name_now + '.txt'
    shape = Array.shape
    # x = X[0, :, 0]
    # y = Y[:, 0, 0]
    # z = Z[0, 0, :]
    
    with open(name, 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(shape))

        outfile.write('# x range\n')
        np.savetxt(outfile, x.reshape(1,len(x)), fmt=format)
        #outfile.write('\n')
        
        outfile.write('# y range\n')
        np.savetxt(outfile, y.reshape(1,len(y)), fmt=format)
        #outfile.write('\n')
        
        outfile.write('# z range\n')
        np.savetxt(outfile, z.reshape(1,len(z)), fmt=format)
        
        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for k in range(shape[2]):
            outfile.write('# z = %.2f \n'%(z[k]))

            # with 2 decimal places.  
            np.savetxt(outfile, Array[:,:,k], fmt=format)

    return name

# reading saved txt file into array
def reading_3D_array(file_name):
    
    x_range = np.loadtxt(file_name, skiprows=2, max_rows=1, ndmin=1)
    y_range = np.loadtxt(file_name, skiprows=4, max_rows=1, ndmin=1)
    z_range = np.loadtxt(file_name, skiprows=6, max_rows=1, ndmin=1)
    X, Y, Z = np.meshgrid(x_range, y_range, z_range)
    
    x = len(x_range)
    y = len(y_range)
    z = len(z_range)

    array = np.loadtxt(file_name, skiprows=8, ndmin=2)
    output = np.zeros((y,x,z))
    r1 = 0
    r2 = y
    for i in range(z):
        output[:,:,i] = array[r1:r2,:]
        r1 += y
        r2 += y
        
    return X, Y, Z, output

# only thing that matters is the last index Z
def XYZ_transfomration(X,Y,Z,res_list,out = 'XZY'):

    # original (4,3,5) with x-3, y-4, z-5
    # 'XZY' (5,3,4)
    # 'YZX' (5,4,3)
    # 'YXZ' (3,4,5)
    # 'ZXY' (3,5,4)
    # 'ZYX' (4,5,3)
    
    if out == 'XYZ':
        
        (X_new, Y_new, Z_new, res_list_new) = (X,Y,Z,res_list)
        
    else:
        
        x = X[0, :, 0]
        y = Y[:, 0, 0]
        z = Z[0, 0, :]

        if out == 'XZY':
            X_new,Y_new,Z_new = np.meshgrid(x,z,y)
        elif out == 'YZX':
            X_new,Y_new,Z_new = np.meshgrid(y,z,x)
        elif out == 'YXZ':
            X_new,Y_new,Z_new = np.meshgrid(y,x,z)
        elif out == 'ZXY':
            X_new,Y_new,Z_new = np.meshgrid(z,x,y)
        elif out == 'ZYX':
            X_new,Y_new,Z_new = np.meshgrid(z,y,x)
        else:
            raise TypeError('Incorrect out value')

        res_list_new = []
        
        for res in res_list:
            res_new = np.zeros(X_new.shape)

            if out == 'XZY':
                for i in range(len(y)): # iterating through new z axis
                    res_new[:,:,i] = np.transpose(res[i,:,:])
            elif out == 'YZX':
                for i in range(len(x)): # iterating through new z axis
                    res_new[:,:,i] = np.transpose(res[:,i,:])
            elif out == 'YXZ':
                for i in range(len(z)): # iterating through new z axis
                    res_new[:,:,i] = np.transpose(res[:,:,i])
            elif out == 'ZXY':
                for i in range(len(y)): # iterating through new z axis
                    res_new[:,:,i] = res[i,:,:]
            elif out == 'ZYX':
                for i in range(len(x)): # iterating through new z axis
                    res_new[:,:,i] = res[:,i,:]
            
            res_list_new.append(res_new)
    
    return X_new, Y_new, Z_new, res_list_new