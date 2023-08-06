# Plotly ODF function for structure the ODF
import xarrayuvecs.uvecs as uvecs
import matplotlib.cm as cm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import xarray as xr

def ODF_template(res=400,xlabel='x',ylabel='y'):
    '''
    Create an circle with
    
    :param res: resolution of the image
    :type res: int
    :param xlabel: name of the x axis
    :type xlabel: string
    :param ylabel: name of the y axis
    :type ylabel: string
    '''

    fig=make_subplots(rows=1, cols=1)

    fig.add_shape(type="circle",
    xref='x', yref='y',
    x0=0, y0=0, x1=res, y1=res,
    line=dict(
        color="Black",
        width=5,
        )
    )
    fig.update_layout(height=600,width=700,paper_bgcolor="White")
    fig.update_layout(showlegend=False)
    #x axis
    fig.update_xaxes(visible=False)
    fig.add_trace(go.Scatter(
        x=np.array([res]),
        y=np.array([res/2]),
        mode="markers+text",
        text=xlabel,
        textposition="middle right"
    ))

    #y axis    
    fig.update_yaxes(visible=False)
    

    fig.add_trace(go.Scatter(
        x=np.array([res/2]),
        y=np.array([res]),
        mode="markers+text",
        text=ylabel,
        textposition="top center"
    ))

    fig.update_yaxes(scaleanchor = "x",scaleratio = 1)
    
    return fig

def add_orientation(proj_ori,fig=None,name=None,text=None,size=10,color='Black',symbol='circle',hovert=None):
    '''
    Add orientations on a pole figure

    :param proj_ori: projected point in the plane of projection dim=(n,2)
    :type proj_ori: np.array
    :param fig:
    :type fig: plotly.graph_objs._figure.Figure
    :param name: name of the point
    :type name: string
    :param text: text to print next to the point
    :type text: string
    :param size: marker size
    :type size: int
    :param color: marker color
    :type color: int
    '''
    if fig is None:
        res=400
        fig=ODF_template(res=res)
    else:
        res=float(fig.data[0].x)
    
    fig.add_trace(go.Scatter(
                    x=res/2+proj_ori[:,0]/(2**0.5)*res/2, 
                    y=res/2+proj_ori[:,1]/(2**0.5)*res/2,
                    mode="markers+text",
                    name=name,
                    text=text,
                    textposition="top center",
                    marker=dict(
                        color=color,
                        size=size,
                        symbol=symbol,
                    )
                ))
    
    if hovert is not None:
        if np.shape(hovert)[0]==1:
            hovert=np.array([np.array([np.mod(hovert[0][1],2*np.pi)*180./np.pi,np.mod(hovert[0][0],2*np.pi)*180./np.pi,hovert[0][2],hovert[0][3],hovert[0][4]])])
        else:
            hovert[:,0]=np.mod(hovert[...,0],2*np.pi)*180/np.pi
            hovert[:,1]=np.mod(hovert[...,1],2*np.pi)*180/np.pi
        fig.data[-1]['hovertemplate']='(phi,theta):(%{customdata[1]:.3f},%{customdata[0]:.3f}) <br> (x,y,z):(%{customdata[2]:.3f},%{customdata[3]:.3f},%{customdata[4]:.3f}) '
        fig.data[-1]['customdata']=hovert

    return fig

def ODF_background(color,fig=None,contourf=True,cline=10,xoz_plane=True,cmap='Greys',**kwargs):
    '''
    Print background image on Pole Figure

    :param ori: orientation in the plane dim=(n,2)
    :type ori: np.array 
    :param color: value associated with each orientation dim=(n)
    :type color: np.array
    :param fig:
    :type fig: plotly.graph_objs._figure.Figure
    :param contourf: use filled contour drawing 
    :type contourf: bool
    :param cline: number of line for filled contour plot
    :type cline: int
    :param cmap: build in plotly colormap https://plotly.com/python/builtin-colorscales/
    :type cmap: string
    '''

    z=np.float64(color)
    ss=color.shape

    if fig is None:
        res=ss[0]
        fig=ODF_template(res=res,xoz_plane=xoz_plane)
    else:
        res=int(fig.data[0].x)

    # Prepare the plot
    xx_pl=np.linspace(-2**0.5,2**0.5,res)
    yy_pl=np.linspace(-2**0.5,2**0.5,res)

    z_xx,z_yy=np.meshgrid(xx_pl,yy_pl)

    mask=(z_xx**2+z_yy**2)**0.5>2**0.5

    z_xx[mask]=None
    z_yy[mask]=None

    te=np.arctan2(z_yy,z_xx)
    pe=2.*np.arcsin((z_xx**2+z_yy**2)/4)**0.5

    xyz=xr.DataArray(np.dstack([te,pe]),dims=('y','x','uvecs')).uvecs.xyz()
    
    if xoz_plane:
        xyz_n=np.copy(xyz)
        xyz_n[...,1]=xyz[...,2]
        xyz_n[...,2]=xyz[...,1]
        xyz=xyz_n
        del xyz_n
        pe=np.arccos(xyz[...,2])
        te=np.arctan2(xyz[...,1],xyz[...,0])

    cd=np.dstack((np.mod(pe,2*np.pi)*180./np.pi, np.mod(te,2*np.pi)*180./np.pi,xyz))

    if contourf:
        fig.add_trace(go.Contour(
            z=color,
            ncontours=cline,
            name='ODF',
            customdata=cd,
            colorscale=cmap,
            hovertemplate='Value:%{z:.3f} <br> (phi,theta):(%{customdata[0]:.3f},%{customdata[1]:.3f}) <br> (x,y,z):(%{customdata[2]:.3f},%{customdata[3]:.3f},%{customdata[4]:.3f})',
        ))
    else:
        fig1=px.imshow(color,origin='lower',color_continuous_scale=cmap)
        fig1.data[0]['hovertemplate']='Value:%{z:.3f} <br> (phi,theta):(%{customdata[0]:.3f},%{customdata[1]:.3f}) <br> (x,y,z):(%{customdata[2]:.3f},%{customdata[3]:.3f},%{customdata[4]:.3f}) '
        fig1.data[0]['customdata']=cd
        fig.add_trace(fig1.data[0])
        fig['layout']['coloraxis']=fig1['layout']['coloraxis']
    return fig