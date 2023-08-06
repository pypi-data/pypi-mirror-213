#########################Various Function##############################
import numpy as np
import colorsys
import plotly.express as px
import xarray as xr
import xarrayuvecs.uvecs as xu
import warnings
warnings.filterwarnings("ignore")

def lut(nx=512,semi=False,circle=True):
    '''
    Create a 2D colorwheel
    
    :param nx: number of pixel for the colorwheel
    :param circle: do you want create a black circle around
    :param semi: do you want a semi LUT
    :type nx: int
    :type circle: bool
    :type semi: bool
    :return: lut
    :rtype: array of size [nx,nx,3]
    :Exemple:
        >>> lut2d=lut()
        >>> plt.imshow(lut)
        >>> plt.show()
    '''
    
    
    x=np.linspace(-np.pi/2, np.pi/2, nx)
    y=np.linspace(-np.pi/2, np.pi/2, nx)
    xv, yv = np.meshgrid(x, y)
    rho,phi=cart2pol(xv, yv)
    
    if semi:
        phi=np.mod(phi,np.pi)
    
    h = (phi-np.min(phi))/(np.max(phi)-np.min(phi))
    v = rho/np.max(rho)

    luthsv = np.ones((nx, nx,3))
    luthsv[:,:,0]=h
    luthsv[:,:,2]=v
    # colorwheel rgb
    lutrgb = np.ones((nx, nx,3))
    for i in list(range(nx)):
        for j in list(range(nx)):
            lutrgb[i,j,0],lutrgb[i,j,1],lutrgb[i,j,2]=colorsys.hsv_to_rgb(luthsv[i,j,0],luthsv[i,j,1],luthsv[i,j,2])

        
    # build a circle color bar        
    if circle:
        for i in list(range(nx)):
            for j in list(range(nx)):
                if ((i-nx/2)**2+(j-nx/2)**2)**0.5>(nx/2):
                    lutrgb[i,j,0]=0 
                    lutrgb[i,j,1]=0
                    lutrgb[i,j,2]=0

    return lutrgb

def cart2pol(x, y):
    '''
    Convert cartesien coordinate x,y into polar coordinate rho, theta
    
    :param x: x cartesian coordinate
    :param y: y cartesian coordinate
    :type x: float
    :type y: float
    :return: rho (radius), theta (angle)
    :rtype: float
    :Exemple: >>> rho,theta=cart2pol(x,y)
    '''
    # transform cartesien to polar coordinate
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def plotly_lut(**kwargs):
    '''
    Plot LUT using plotly
    '''
    ll=lut(**kwargs)

    d=ll.shape[0]
    xx_pl=np.linspace(-2**0.5,2**0.5,d)
    yy_pl=np.linspace(-2**0.5,2**0.5,d)
    z_xx,z_yy=np.meshgrid(xx_pl,yy_pl)
    te=np.flipud(np.mod(np.arctan2(z_yy,z_xx),2*np.pi))
    pe=2.*np.arcsin((z_xx**2+z_yy**2)/4)**0.5
    
    xyz=xr.DataArray(np.dstack([te,pe]),dims=('y','x','uvecs')).uvecs.xyz()

    cd=np.dstack((pe*180./np.pi, te*180./np.pi,xyz))

    #data[np.isnan(theta),0]=np.nan

    fig=px.imshow(ll)
    fig.data[0]['hovertemplate']='(phi,theta):(%{customdata[0]:.3f},%{customdata[1]:.3f}) <br> (x,y,z):(%{customdata[2]:.3f},%{customdata[3]:.3f},%{customdata[4]:.3f}) '
    fig.data[0]['customdata']=cd

    fig=fig.update_xaxes(visible=False)
    fig=fig.update_yaxes(visible=False)

    return fig