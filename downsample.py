import numpy as np

def decimate_once( x, y, kappa_ds_max ) :
    '''
    x, y = decimate_once( x, y, kappa_ds_max )

    Remove one point out of two where the curve x, y is too densely sampled.

    Parameters:
        x (array) : first coordinate of curve
        y (array) : second coordinate of curve
        kappa_ds_max (float) : curvature times step size, maximum acceptable value
    '''

    dx = np.diff(x)
    dy = np.diff(y)

    ds = np.sqrt( dx**2 + dy**2 )
    dx_ds = dx/ds
    dy_ds = dy/ds

    kappa_ds_2 = np.diff(dx_ds)**2 + np.diff(dy_ds)**2

    too_dense = np.array( [False] + list( kappa_ds_2 < kappa_ds_max**2 ) + [False] )
    wanted = sort( list( where( too_dense )[0][::2] ) + list( where( ~too_dense )[0] ) )

    return x[wanted], y[wanted]

def downsample( x, y, kappa_ds_max = 0.02 ) :
    '''
    x, y = downsample( x, y, kappa_ds_max = 0.02 )

    Remove one point out of two where the curve x, y is too densely sampled,
    and repeat on the new curve until conergence.

    Parameters:
        x (array) : first coordinate of curve
        y (array) : second coordinate of curve
        kappa_ds_max (float) : curvature times step size, maximum acceptable value
    '''

    while True :
        n = len(x)
        x, y = decimate_once( x, y, kappa_ds_max )
        if len(x) == n :
            break

    return x, y

if __name__ == "__main__" :

    from pylab import *

    t = linspace(0,2*pi, 500)

    x = cos(3*t)
    y = sin(t)

    plot( x, y, label = 'Original', color = 'grey' )

    for kappa_ds_max in [0.03, 0.1] :
        x_ds, y_ds = downsample( x, y, kappa_ds_max )
        plot( x_ds, y_ds, '.', label = r'$\kappa \, \mathrm{d}s=' + str(kappa_ds_max) + '$' )

    legend()
    axis('equal')
    axis('off')
    xticks([]); yticks([])


    fig_path_and_name = './' + __file__.split('/')[-1].split('.')[0] + '.pdf'
    savefig( fig_path_and_name , bbox_inches = 'tight' )
    print(fig_path_and_name)

    show()
