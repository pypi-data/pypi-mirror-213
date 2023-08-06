'''
This is an object to take care of unit vector
'''
from xarrayuvecs.uniform_dist import unidist
import xarrayuvecs.lut2d as lut2d
import xarrayuvecs.odfplot as odfplot

import multiprocessing
import random
import datetime
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.tri as tri
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.neighbors import KernelDensity
import scipy

@xr.register_dataarray_accessor("uvecs")

class uvecs(object):
    '''
    This is a classe to work on unit vector in xarray environnement that respect the -1 symmetry (i.e. u is equivalent to -u)
    
    .. note:: xarray does not support heritage from xr.DataArray may be the day it support it, we could move to it
    '''
    
    def __init__(self, xarray_obj):
        '''
        Constructor for uvec. The univ vector u should be pass as azimuth and colatitude in radian
        Colatitude : angle between u-vector and z vector [0 pi/2]
        Azimuth : angle between the projection of u-vector in xOy plan and x-vector [0 2pi]
        
        :param xarray_obj: dimention should be (n,m,2), xarray_obj[n,m,0]=azimuth , xarray_obj[n,m,1]=colatitude
        :type xarray_obj: xr.DataArray
        '''
        self._obj = xarray_obj 
    pass
    

#-----------------------------vector representation-------------------------------------        
    def azi_col(self):
        '''
        :return: the azimuth out[n,m,0] and colatitude out[n,m,0], dim (n,m,2)
        :rtype: np.array
        '''
        return self
        
    def bunge_euler(self):
        '''
        This is from the Euler angle, Bunge convention

        1. rotate around z-axis of phi1
        2. rotate around x'-axis of phi

        :return: phi1 and phi, out[n,m,0]=phi1, out[n,m,1]=phi
        :rtype: np.array
        '''
        BE=np.moveaxis(np.array([np.mod(self._obj[...,0]+np.pi/2.,2*np.pi),self._obj[...,1]]),0,-1)
        
        dd=list(self._obj.coords.dims[0:-1])
        dd.append('vbe')
        
        da=xr.DataArray(BE,dims=dd)
        for nn in dd[0:-1]:
            da.coords[nn]=self._obj[nn]
        return da


    def xyz(self):
        '''
        Return vectors in cartesian coordinate
        
        :return: out[n,m,0]=x, out[n,m,1]=u , out[n,m,2]=z
        :rtype: np.array
        '''
        XYZ=np.moveaxis(np.array([np.cos(self._obj[...,0])*np.sin(self._obj[...,1]),np.sin(self._obj[...,0])*np.sin(self._obj[...,1]),np.cos(self._obj[...,1])]),0,-1)
        
        dd=list(self._obj.coords.dims[0:-1])
        dd.append('vc')
        
        da=xr.DataArray(XYZ,dims=dd)
        for nn in dd[0:-1]:
            da.coords[nn]=self._obj[nn]
        
        return da
    
#-----------------------------------colormap function-------------------------------------
    def calc_colormap(self,**kwargs):
        '''
        Compute the colormap value

        :param nlut: size of the lut (default:512)
        :type nlut: int
        
        .. note:: ``**kwargs`` for xarray_uvecs.lut2d.lut
        '''
        rlut=lut2d.lut(circle=False,**kwargs)
        nlut=np.shape(rlut)[0]
        
        XX=np.int32((nlut-1)/2*np.multiply(np.sin(self._obj[...,1]),-np.sin(self._obj[...,0]))+(nlut-1)/2)
        YY=np.int32((nlut-1)/2*np.multiply(np.sin(self._obj[...,1]),np.cos(self._obj[...,0]))+(nlut-1)/2)
                
        id=XX<0
        XX[id]=0
        YY[id]=0
        
        
        img=rlut[XX,YY]
        if len(XX.shape)==2:
            idx,idy=np.where(id==True)
            img[idx,idy,:]=np.array([255,255,255])
        elif len(XX.shape)==3:
            idx,idy,idz=np.where(id==True)
            img[idx,idy,idz,:]=np.array([255,255,255])
        
        ll=list(self._obj.coords.dims)
        ll.remove('uvecs')
        ll.append('img')
        
        da=xr.DataArray(img,dims=ll)
        da['x']=self._obj['x']
        da['y']=self._obj['y']
        da=da.clip(0,1)

        return da
#--------------------------------------------------------------------------------------------
    def OT2nd(self,xoz_plane=False):
        '''
        Compute the second order orientation tensor
        
        :return eigvalue: eigen value w[i]
        :rtype eigvalue: np.array
        :return: eigvector eigen vector v[:,i]
        :rtype: eigvector np.array
        
        .. note:: eigen value w[i] is associate to eigen vector v[:,i] 
        '''
        u_xyz=self.xyz()
        if xoz_plane:
            ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
            uy=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
            uz=-1.*np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
        else:
            ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
            uy=np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
            uz=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
        
        
        a11 = np.float32(np.nanmean(np.longdouble(np.multiply(ux,ux))))
        a22 = np.float32(np.nanmean(np.longdouble(np.multiply(uy,uy))))
        a33 = np.float32(np.nanmean(np.longdouble(np.multiply(uz,uz))))
        a12 = np.float32(np.nanmean(np.longdouble(np.multiply(ux,uy))))
        a13 = np.float32(np.nanmean(np.longdouble(np.multiply(ux,uz))))
        a23 = np.float32(np.nanmean(np.longdouble(np.multiply(uy,uz))))
        
        Tensor=np.array([[a11, a12, a13],[a12, a22, a23],[a13, a23, a33]])
        eigvalue,eigvector=np.linalg.eig(Tensor)
        
        idx = eigvalue.argsort()[::-1]
           
        return eigvalue[idx],eigvector[:,idx]
#--------------------------------------------------------------------------------------------
    def misorientation_profile(self,xx,yy,degre=True,method="nearest",**kwargs):
        '''
        Extract value for xx,yy

        :param xx: x coordinate
        :type xx: np.array()
        :param yy: y coordinate
        :type yy: np.array()
        :param degre: Do you want the angle in degree (default:True)
        :type degre: bool

        .. note:: ``**kwargs`` for xr.sel
        '''
        ori=self._obj.sel(x=xx,y=yy, method=method,**kwargs)
        # trasform it in numpy array in cartesien coordinate
        vxyz=np.array(ori.uvecs.xyz())[0]
        # compute the misorientation to origin
        mis2o=np.arccos(np.round(np.dot(vxyz,vxyz[0]),10))
    
        mis2o[np.where(mis2o>np.pi/2)]=np.pi-mis2o[np.where(mis2o>np.pi/2)]
        # compute misorientation from previous
        vxyzm=np.zeros(np.shape(vxyz))
        vxyzm[:,:]=np.nan
        vxyzm[1::,:]=vxyz[0:-1,:]
        mis2p=np.arccos(np.round(np.diag(np.dot(vxyz,np.transpose(vxyzm))),10))
        mis2p[np.where(mis2p>np.pi/2)]=np.pi-mis2p[np.where(mis2p>np.pi/2)]
        #compute distance
        d=((xx-xx[0])**2+(yy-yy[0])**2)**0.5
        
        if degre:
            coeff=180/np.pi
        else:
            coeff=1.
        
        ds=xr.Dataset(
        {
            'mis2i': (['d'],mis2o*coeff),
            'mis2p': (['d'],mis2p*coeff),
        },
        coords={'d':d})
        return ds
    
    
#--------------------------------------------------------------------------------------------
    def mis_angle(self,random=False):
        '''
        Compute the misorientation with the neighbouring grain

        :param random: suffle the image and compute the angle
        :type random: bool

        '''
        phi1=np.array(self.bunge_euler())[:,:,0]
        phi=np.array(self.bunge_euler())[:,:,1]

        if random:
            np.random.shuffle(phi1)
            np.random.shuffle(phi)
            phi1=phi1.flatten()
            phi=phi.flatten()
            phi1 = phi1[~np.isnan(phi1)]
            phi = phi[~np.isnan(phi)]
            dd=np.int(np.sqrt(len(phi1)))
            phi1=phi1[0:dd**2].reshape([dd,dd])
            phi=phi[0:dd**2].reshape([dd,dd])

        mat=np.zeros([3,3])
        mat[0,1]=1
        phi_a=scipy.signal.convolve2d(phi,mat,mode='same',boundary='symm')
        phi1_a=scipy.signal.convolve2d(phi1,mat,mode='same',boundary='symm')

        mat=np.zeros([3,3])
        mat[1,0]=1
        phi_b=scipy.signal.convolve2d(phi,mat,mode='same',boundary='symm')
        phi1_b=scipy.signal.convolve2d(phi1,mat,mode='same',boundary='symm')


        mat=np.zeros([3,3])
        mat[1,2]=1
        phi_c=scipy.signal.convolve2d(phi,mat,mode='same',boundary='symm')
        phi1_c=scipy.signal.convolve2d(phi1,mat,mode='same',boundary='symm')


        mat=np.zeros([3,3])
        mat[2,1]=1
        phi_d=scipy.signal.convolve2d(phi,mat,mode='same',boundary='symm')
        phi1_d=scipy.signal.convolve2d(phi1,mat,mode='same',boundary='symm')

        phi1_s=[phi1_a,phi1_b,phi1_c,phi1_d]
        phi_s=[phi_a,phi_b,phi_c,phi_d]
        if random:
            tot=np.zeros([dd,dd,4])
        else:
            tot=np.zeros([len(self._obj.y),len(self._obj.x),4])
        
        for i in range(4):
            nphi1=phi1_s[i]
            nphi=phi_s[i]
            res=np.arccos(np.round(np.sin(phi1)*np.sin(nphi1)*np.sin(phi)*np.sin(nphi)+np.cos(phi1)*np.cos(nphi1)*np.sin(phi)*np.sin(nphi)+np.cos(phi)*np.cos(nphi),5))
            #put everything between 0  and pi/2 because c=-c
            id=np.where(res>np.pi/2)
            res[id]=np.pi-res[id] 

            res[0,:] = np.nan  # delete first row 
            res[-1,:] = np.nan
            res[:,0] = np.nan
            res[:,-1] = np.nan
            tot[:,:,i]=res
            

        if random:
            tot=tot.flatten()
            tot=tot[~np.isnan(tot)]
        else:
            tot=xr.DataArray(tot,dims=[self._obj.coords.dims[0],self._obj.coords.dims[1],'misAngle'])

        return tot
#-------------------------------------------------------------------------------------------
    def calcODF(self,nbr=0,bw=0.2):
        '''
        Compute ODF

        :param nbr: number of point selected for the Kernel Density Estimation KDE (default : 10000)
        :type nbr: int
        :param bw: bandwidth for the KDE (default : 0.2)
        :type bw: float
        '''
        #compute phi theta under the nice form for kde fit
        u_xyz=self.xyz()
        ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
        uy=np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
        uz=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])

        if nbr!=0:
            if nbr>len(ux):
                nbr=len(ux)
                
            rng = np.random.default_rng()
            numbers = rng.choice(len(ux), size=nbr, replace=False)
            
            ux=ux[numbers]
            uy=uy[numbers]
            uz=uz[numbers]

        phi=np.arccos(uz)-np.pi/2.
        theta=np.arctan2(uy,ux)-np.pi

        kde = KernelDensity(bandwidth=bw, metric='haversine',kernel='gaussian', algorithm='ball_tree')
        kde.fit(np.transpose(np.array([phi,theta])))

        return kde
#--------------------------------------------------------------------------------------------
    def plotODF(self,nbr=10000,bw=0.2,projz=1,plot_cm=True,plotOT=True,angle=np.array([30.,60.]),cline=10,ax=None,xoz_plane=False,cmap=cm.viridis,**kwargs):
        '''
        Plot the Orienation Density Function

        :param nbr: number of point selected for the Kernel Density Estimation KDE (default : 10000)
        :type nbr: int
        :param bw: bandwidth for the KDE (default : 0.2)
        :type bw: float
        :param projz: plan of projection (0 or 1) (default : 1)
        :type projz: int
        :param plotOT: plot eigenvectore of second order orientation tensor
        :type plotOT: bool
        :param angle: plot circle for given angle (default : np.array([30.,60.]))
        :type angle: np.array
        :param cline: number or line for the contourf
        :type cline: int
        :param ax: matplotlib axes to plot inside. if none create a new figure
        :type ax: matplotlib.axes._subplots.AxesSubplot
        :param xoz_plane: plot the pole figure in xOz plane if True. In xOy plane overwise.
        :type xoz_plane: bool

        .. note:: ``**kwargs`` for plt.tricontourf
        '''
        
        #compute phi theta under the nice form for kde fit
        u_xyz=self.xyz()
        
        if xoz_plane:
            ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
            uy=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
            uz=-1.*np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
        else:
            ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
            uy=np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
            uz=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
        
        ux=ux[~np.isnan(ux)]
        uy=uy[~np.isnan(uy)]
        uz=uz[~np.isnan(uz)]
        
        
        if nbr!=0:
            if nbr>len(ux):
                nbr=len(ux)
                
            rng = np.random.default_rng()
            numbers = rng.choice(len(ux), size=nbr, replace=False)
            
            ux=ux[numbers]
            uy=uy[numbers]
            uz=uz[numbers]
                        
        
        phi=np.arccos(uz)-np.pi/2.
        theta=np.arctan2(uy,ux)-np.pi
        
        
        #compite the kde
        kde = KernelDensity(bandwidth=bw, metric='haversine',kernel='gaussian', algorithm='ball_tree')
        kde.fit(np.transpose(np.array([phi,theta])))
        
        # Prepare the plot
        val=unidist
        dim=int(np.size(val)/3)
        vs=val.reshape([dim,3])
        id=np.where(vs[:,2]>0)
        vs_u=vs[id[0],:]
        
        # add point on the disc for contourf
        tot=10000
        omega = np.linspace(0, 2*np.pi, tot)
        zcir = np.zeros(tot)
        xcir = np.cos(omega)
        ycir = np.sin(omega)
        
        vs_x=np.concatenate([vs[:,0],xcir])
        vs_y=np.concatenate([vs[:,1],ycir])
        vs_z=np.concatenate([vs[:,2],zcir])
        
        id=np.where(vs_z<0)
        vs_x[id]=-vs_x[id]
        vs_y[id]=-vs_y[id]
        vs_z[id]=-vs_z[id]
        
        phi_e=np.arccos(vs_z)
        theta_e=np.arctan2(vs_y,vs_x)
        
        weights=kde.score_samples(np.transpose(np.array([phi_e-np.pi/2.,theta_e-np.pi])))
        
        # Choose the type of projection
        if projz==0:
            LpL=1./(1.+vs_z)
            xx=LpL*vs_x
            yy=LpL*vs_y
            rci=np.multiply(1./(1.+np.sin((90-angle)*np.pi/180.)),np.cos((90-angle)*np.pi/180.))
            rco=1.
        else:
            xx = np.multiply(2*np.sin(phi_e/2),np.cos(theta_e))
            yy = np.multiply(2*np.sin(phi_e/2),np.sin(theta_e))
            rci=2.*np.sin(angle/2.*np.pi/180.)
            rco=2.**0.5
        
        if ax is None:
            ax = plt.gca()    
        
        # plot contourf
        triang = tri.Triangulation(xx, yy)
        ax.tricontour(xx, yy, np.exp(weights)/np.mean(np.exp(weights)), cline, linewidths=0.5, colors='k',**kwargs)
        sp=ax.tricontourf(xx, yy, np.exp(weights)/np.mean(np.exp(weights)), cline,cmap=cmap, **kwargs)
        
        if plot_cm:
            fig=plt.gcf()
            fig.colorbar(sp,orientation='horizontal',aspect=4,shrink=0.5)
        # Compute the outer circle
        omega = np.linspace(0, 2*np.pi, 1000)
        x_circle = rco*np.cos(omega)
        y_circle = rco*np.sin(omega)
        ax.plot(x_circle, y_circle,'k', linewidth=3)
        # compute a 3 circle
        if np.size(angle)>1:
            for i in list(range(len(rci))):
                x_circle = rci[i]*np.cos(omega)
                y_circle = rci[i]*np.cos(i*np.pi/180.)*np.sin(omega)
                
                ax.plot(x_circle, y_circle,'k', linewidth=1.5)
                ax.text(x_circle[200], y_circle[300]+0.04,'$\phi$='+str(angle[i])+'°')
            # plot Theta line
            ax.plot([0,0],[-1*rco,1*rco],'k', linewidth=1.5)
            ax.text(rco-0.2, 0+0.06,'$\Theta$=0°')
            ax.text(-rco+0.1, 0-0.06,'$\Theta$=180°')
            ax.plot([-rco,rco],[0,0],'k', linewidth=1.5)
            ax.text(-0.25, rco-0.25,'$\Theta$=90°')
            ax.text(0.01, -rco+0.15,'$\Theta$=270°')
            ax.plot([-0.7071*rco,0.7071*rco],[-0.7071*rco,0.7071*rco],'k', linewidth=1.5)
            ax.plot([-0.7071*rco,0.7071*rco],[0.7071*rco,-0.7071*rco],'k', linewidth=1.5)
          
            
        # draw a cross for x and y direction
        ax.plot([1*rco, 0],[0, 1*rco],'+k',markersize=12)
        # write axis
        ax.text(1.05*rco, 0, r'$X$')
        if xoz_plane:
            ax.text(0, 1.05*rco, r'$Z$')
        else:
            ax.text(0, 1.05*rco, r'$Y$')

        ax.axis('equal')
        ax.axis('off')
                   
        
        if plotOT:
            eigvalue,eigvector=self.OT2nd(xoz_plane=xoz_plane)
                            
            for i in list(range(3)): # Loop on the 3 eigenvalue
                if (eigvector[2,i]<0):
                    v=-eigvector[:,i]
                    hemi_sud=True
                else:
                    v=eigvector[:,i]
                    hemi_sud=False
                    
                    
                if projz==0:    
                    LpLv=1./(1.+v[2])
                    xxv=LpLv*v[0]
                    yyv=LpLv*v[1]
                else:
                    phiee=np.arccos(v[2])
                    thetaee=np.arctan2(v[1],v[0])
                    xxv = np.multiply(2*np.sin(phiee/2),np.cos(thetaee))
                    yyv = np.multiply(2*np.sin(phiee/2),np.sin(thetaee))
                    

                if hemi_sud:
                    ax.plot(xxv,yyv,'sk',markersize=8)
                else:
                    ax.plot(xxv,yyv,'sk',markersize=8)


                ax.text(xxv+0.04, yyv+0.04,str(round(eigvalue[i],2)))

        return ax,sp
    
#-------------------------------------------------------------------------------------------
    def plotly_ODF(self,nbr=10000,bw=0.2,plot_cm=True,plotOT=True,cf=True,cline=10,xoz_plane=False,res=400,add_dot=None,cmap='viridis'):
            '''
            Plot the Orienation Density Function

            :param nbr: number of point selected for the Kernel Density Estimation KDE (default : 10000)
            :type nbr: int
            :param bw: bandwidth for the KDE (default : 0.2)
            :type bw: float
            :param plotOT: plot eigenvectore of second order orientation tensor
            :type plotOT: bool
            :param cf: use contour filled plot
            :type cf: bool
            :param cline: number or line for the contour filled plot
            :type cline: int
            :param xoz_plane: plot the pole figure in xOz plane if True. In xOy plane overwise.
            :type xoz_plane: bool
            :param res: resolution of the image
            :type res: int
            :param add_dot: Number of orientation to print with dot on the image
            :type add_dot: int
            :param cmap: build in plotly colormap https://plotly.com/python/builtin-colorscales/
            :type cmap: string


            .. note:: ``**kwargs`` for plt.tricontourf
            '''
            if xoz_plane:
                namey = 'z'
            else:
                namey = 'y'
            fig=odfplot.ODF_template(res=res,xlabel='x',ylabel=namey)
            
            if plot_cm:
                #compute phi theta under the nice form for kde fit
                u_xyz=self.xyz()
                
                if xoz_plane:
                    ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
                    uy=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
                    uz=-1.*np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
                    

                else:
                    ux=np.concatenate([np.array(u_xyz[...,0]).flatten(),-np.array(u_xyz[...,0]).flatten()])
                    uy=np.concatenate([np.array(u_xyz[...,1]).flatten(),-np.array(u_xyz[...,1]).flatten()])
                    uz=np.concatenate([np.array(u_xyz[...,2]).flatten(),-np.array(u_xyz[...,2]).flatten()])
                    namey = 'y'
                
                ux=ux[~np.isnan(ux)]
                uy=uy[~np.isnan(uy)]
                uz=uz[~np.isnan(uz)]
                
                
                if nbr!=0:
                    if nbr>len(ux):
                        nbr=len(ux)
                        
                    rng = np.random.default_rng()
                    numbers = rng.choice(len(ux), size=nbr, replace=False)
                    
                    ux=ux[numbers]
                    uy=uy[numbers]
                    uz=uz[numbers]
                                
                
                phi=np.arccos(uz)-np.pi/2.
                theta=np.arctan2(uy,ux)-np.pi
                
                
                #compite the kde
                kde = KernelDensity(bandwidth=bw, metric='haversine',kernel='gaussian', algorithm='ball_tree')
                kde.fit(np.transpose(np.array([phi,theta])))
                
                # Prepare the plot
                xx_pl=np.linspace(-2**0.5,2**0.5,res)
                yy_pl=np.linspace(-2**0.5,2**0.5,res)

                z_xx,z_yy=np.meshgrid(xx_pl,yy_pl)

                mask=(z_xx**2+z_yy**2)**0.5>2**0.5

                z_xx[mask]=None
                z_yy[mask]=None

                te=np.arctan2(z_yy,z_xx)
                pe=2.*np.arcsin((z_xx**2+z_yy**2)/4)**0.5
                
                pef=pe.flatten()
                tef=te.flatten()

                idd=np.where(~np.isnan(pef))

                pef=pef[~np.isnan(pef)]
                tef=tef[~np.isnan(tef)]

                def parrallel_score_samples(kde, samples, thread_count=int(0.875 * multiprocessing.cpu_count())):
                    with multiprocessing.Pool(thread_count) as p:
                        return np.concatenate(p.map(kde.score_samples, np.array_split(samples, thread_count)))

                w_plt=parrallel_score_samples(kde,np.transpose(np.array([pef-np.pi/2.,tef-np.pi])))
                w0=np.zeros(res**2)
                w0[:]=np.nan
                w0[idd]=w_plt
                w0=w0.reshape([res,res])
                w0=np.exp(w0)/np.nanmean(np.exp(w0))

                # plot contourf
                fig=odfplot.ODF_background(w0,contourf=cf,cline=cline,fig=fig,xoz_plane=xoz_plane,cmap=cmap)

            if add_dot is not None:
                proj_dot=self.vector2plane(xoz_plane=xoz_plane)
                xyz=self.xyz()
                ss=proj_dot.shape
                proj_dot=proj_dot.reshape([ss[0]*ss[1],2])
                pt=np.dstack([np.array(self._obj),xyz]).reshape([ss[0]*ss[1],5])
                id_dot=np.unique(np.random.randint(0,ss[0]*ss[1],size=add_dot))   
                proj_dot=proj_dot[id_dot,:]
                pt=pt[id_dot,:]
                if xoz_plane:
                    id=np.where(pt[:,3]<0)
                    pt[id,2:]=-pt[id,2:]
                    pt[id,0]=np.mod(pt[id,0]+np.pi,2*np.pi)
                    pt[id,1]=np.pi-pt[id,1]
                fig=odfplot.add_orientation(proj_dot,fig,name='ori',size=2,color='Red',hovert=pt)

            if plotOT:
                eigvalue,eigvector=self.OT2nd(xoz_plane=xoz_plane)
                            
                for i in list(range(3)): # Loop on the 3 eigenvalue
                    if (eigvector[2,i]<0):
                        v=-eigvector[:,i]
                    else:
                        v=eigvector[:,i]
                        
                    phiee=np.arccos(v[2])
                    thetaee=np.arctan2(v[1],v[0])

                    if xoz_plane:
                        ip=1
                        vp=np.array([eigvector[0,i],eigvector[2,i],eigvector[1,i]])
                        
                    else:
                        ip=2
                        vp=eigvector[:,i]

                    phit=np.mod(np.arccos(vp[2]),2*np.pi)
                    thetat=np.mod(np.arctan2(vp[1],vp[0]),2*np.pi)

                    if eigvector[ip,i]<0:
                        sym='square'
                    else:
                        sym='circle'
            

                    xxv = np.multiply(2*np.sin(phiee/2),np.cos(thetaee))
                    yyv = np.multiply(2*np.sin(phiee/2),np.sin(thetaee))
                        
                    dt=np.concatenate([np.array([phit,thetat]),vp])
                    fig=odfplot.add_orientation(np.array([[xxv,yyv]]),fig,name='e'+str(i+1),text=str(round(eigvalue[i],2)),hovert=[dt],symbol=sym)

            return fig



#-------------------------------------------------------------------------------------------            
    def calc_schmid(self,axis):
        '''
        Compute the schimd sc=abs(cos(a)sin(a)) where a is the angle between c and axis

        :param axis: axis from which you want to compute the schimd factor in cartesien coordinate (X,Y,Z)
        :type axis: np.array
        '''

        ori=self.xyz()
        angle=np.arccos(np.sum(ori*axis,axis=-1))
        schmid=np.abs(np.cos(angle)*np.sin(angle))

        return schmid
    
#--------------------------------------------------------------------------------------------
    def inner_angle(self, other):
        '''
        Compute the inner angle between to uvecs DataArray

        :param other: DataArray of same dimention than self and compatible with uvec
        :param other: xr.DataArray
        :return:
        :rtype: xr.DataArray
        '''
        o1=self.xyz()
        o2=other.uvecs.xyz()
        angle=np.array(np.arccos(np.sum(o1*o2,axis=-1)))
        id=np.where(angle>np.pi/2)
        angle[id]=np.pi-angle[id]
        
        return xr.DataArray(angle,dims=self._obj.coords.dims[0:2])
#-------------------------------------------------------------------------------------------
    def quiver(self,density=1,color_code=0,**kwargs):
        '''
        Plot quiver map

        :param length: give a length map for the quiver
        :type length: xr.DataArray
        :param density: density of quiver plotted between 0 and 1
        :type density: float

        .. note:: ``**kwargs`` for xr.plot.quiver
        '''
        
        u_xyz=self.xyz()
        
        ds1=xr.Dataset()
        ds1.coords['x']=u_xyz.x
        ds1.coords['y']=u_xyz.y
        ds1['u']=u_xyz[...,0]
        ds1['v']=u_xyz[...,1]
        if type(color_code)!=int:
            ds1['eigen_value']=color_code
            
        ds2=xr.Dataset()
        ds2.coords['x']=u_xyz.x
        ds2.coords['y']=u_xyz.y
        ds2['u']=-u_xyz[...,0]
        ds2['v']=-u_xyz[...,1]
        if type(color_code)!=int:
            ds2['eigen_value']=color_code
            
        ss=ds1.u.shape
            
        if density!=1:
            val=np.zeros(100)
            val[0:int(density*100)]=1
            l = np.array([random.choice(val) for i in range(ss[0]*ss[1])]).reshape(ss)
            ds1['mask']=xr.DataArray(l,dims=ds1.u.coords.dims)
            ds2['mask']=xr.DataArray(l,dims=ds2.u.coords.dims)
            ds1=ds1.where(ds1.mask==1)
            ds2=ds2.where(ds2.mask==1)
            
        if type(color_code)!=int:
            ds1.plot.quiver(x='x',y='y',u='u',v='v',hue='eigen_value',**kwargs)
            ds2.plot.quiver(x='x',y='y',u='u',v='v',hue='eigen_value',**kwargs)
        else:
            ds1.plot.quiver(x='x',y='y',u='u',v='v',**kwargs)
            ds2.plot.quiver(x='x',y='y',u='u',v='v',**kwargs)

#-------------------------------------------------------------------------------------------
    def vector2plane(self,xoz_plane=False):
        '''
        Project a 3D vector uvecs to the plane of the pole figure
        :param xa_uvecs: uvecs vector object
        :type xa_uvecs: uvecs
        :param xoz_plane: project in xoz plane
        :type xoz_plane: bool
        '''
        xyz_vec=self.xyz()
        if xoz_plane:
            xyz_vec2=np.copy(xyz_vec)
            xyz_vec2[...,1]=xyz_vec[...,2]
            xyz_vec2[...,2]=xyz_vec[...,1]
            xyz_vec=xyz_vec2
            del xyz_vec2
        
        id0,id1=np.where(xyz_vec[...,2]<0)
        xyz_vec[id0,id1,:]=-xyz_vec[id0,id1,:]
            
        phiee=np.arccos(xyz_vec[...,2])
        thetaee=np.arctan2(xyz_vec[...,1],xyz_vec[...,0])
        xxv = np.multiply(2*np.sin(phiee/2),np.cos(thetaee))
        yyv = np.multiply(2*np.sin(phiee/2),np.sin(thetaee))

        proj_xy=np.dstack([xxv,yyv])

        return proj_xy

#-----------------------------------------------------------------
    def plotly_colormap(self,add_hover=False,**kwargs):
        '''
        Plot colormap in plotly
        '''

        da=self.calc_colormap(**kwargs)
        
        fig=px.imshow(da,origin='lower')
        if add_hover:
            cd=np.dstack([np.array(self._obj),self.xyz()])
            fig.data[0]['hovertemplate']='<b>Orientation</b> <br> (phi,theta):(%{customdata[1]:.3f},%{customdata[0]:.3f}) <br> (x,y,z):(%{customdata[2]:.3f},%{customdata[3]:.3f},%{customdata[4]:.3f}) '
            fig.data[0]['customdata']=cd
        
        return fig
