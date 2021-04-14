#    Copyright (C) 2021 David J. Wooten
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod

from ipywidgets import widgets
import plotly.graph_objects as go
import numpy as np

class Demo(ABC):

    def _get_beta(self, E0, E1, E2, E3):
        minE = min(E1, E2)
        return (minE-E3)/(E0-minE)

    def _get_E3(self, E0, E1, E2, beta):
        minE = min(E1, E2)
        return minE - beta*(E0-minE)


    def _hill_inv(self, E, E0, Emax, h, C):
        E_ratio = (E-E0)/(Emax-E)
        d = np.float_power(E_ratio, 1./h)*C
        d[E_ratio<0] = np.nan
        return d

    def _hill_E(self, d, E0, Emax, h, C):
        dh = np.power(d,h)
        return E0 + (Emax-E0)*dh/(np.power(C,h)+dh)

    def _MuSyC_E(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        d1h1 = np.power(d1,h1)
        d2h2 = np.power(d2,h2)
        C1h1 = np.power(C1,h1)
        C2h2 = np.power(C2,h2)
        r1 = 100/C1h1
        r2 = 100/C2h2
        U=(r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        A1=(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12))/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        A2=(d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21))/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        return U*E0 + A1*E1 + A2*E2 + (1-(U+A1+A2))*E3

    def _bliss(self, d1, d2, E, E0, E1, E2, h1, h2, C1, C2):
        E1_alone = self._hill_E(d1, E0, E1, h1, C1)
        E2_alone = self._hill_E(d2, E0, E2, h2, C2)
        synergy = E1_alone*E2_alone - E
        synergy[(d1==0) | (d2==0)] = 0
        return synergy

    def _loewe(self, d1, d2, E, E0, E1, E2, h1, h2, C1, C2):
        with np.errstate(divide='ignore', invalid='ignore'):
            d1_alone = self._hill_inv(E, E0, E1, h1, C1)
            d2_alone = self._hill_inv(E, E0, E2, h2, C2)
            synergy = d1/d1_alone + d2/d2_alone
        synergy[(d1==0) | (d2==0)] = 1
        return synergy

    def get_plot(self, d1, d2, E, cmap='viridis', clim=None, center_on_zero=False):

        sorted_indices = np.lexsort((d1,d2))
        d1 = d1[sorted_indices]
        d2 = d2[sorted_indices]
        E = E[sorted_indices]

        n_d1 = len(np.unique(d1))
        n_d2 = len(np.unique(d2))
        d1 = d1.reshape(n_d2,n_d1)
        d2 = d2.reshape(n_d2,n_d1)
        E = E.reshape(n_d2,n_d1)

        if clim is None:
            if center_on_zero:
                cmin, cmax = -0.4,0.4
            else:
                cmin, cmax = 0,1
        else:
            cmin, cmax = clim

        data_to_plot = go.Surface(
            x=d1,
            y=d2,
            z=E,
            cmin=cmin,
            cmax=cmax,
            opacity=0.8,
            contours_z=dict(
                show=True,
                usecolormap=True,
                highlightcolor="limegreen",
                project_z=False
            ),
            colorscale=cmap,
            reversescale=False,
            colorbar=dict(
                lenmode='fraction',
                len=0.65,
                thickness=15
                ),
            connectgaps=False
            )


        return data_to_plot

    def get_fig_widget(self, d1, d2, E, title, zlim=(0,1.1), clim=None, cmap="viridis", width=800, height=600, center_on_zero=False, z_title=None):
        d1[d1==0] = min(d1[d1>0])/10
        d2[d2==0] = min(d2[d2>0])/10
        d1 = np.log10(d1)
        d2 = np.log10(d2)

        data = [self.get_plot(d1, d2, E, cmap=cmap, center_on_zero=center_on_zero, clim=clim),]

        if z_title is None:
            if center_on_zero:
                z_title = ""
            else:
                z_title="E"
        g = go.FigureWidget(data=data)

        g.update_layout(
            title=title,
            autosize=False,
            scene_camera_eye=dict(
                x=1.02, 
                y=2.15,
                z=1.48
            ),
            width = width,
            height = height,
            hovermode = False,
            margin=dict(
                l=10, 
                r=10, 
                b=10, 
                t=30
            ), 
            scene=dict(
                xaxis_title="Drug 1", 
                yaxis_title="Drug 2", 
                zaxis_title=z_title, 
                aspectmode="cube"
            ),
            font=dict(
                size=10
            )
        )
            
        g.update_layout(scene =
            dict(
                    zaxis = dict(range=zlim),
                    xaxis = dict(range=(min(d1),max(d1))),
                    yaxis = dict(range=(min(d2),max(d2))),
                )
        )

        return g

    def __init__(self, E0=1, E1=0.4, E2=0.5, E3=0.4, h1=2, h2=0.5, C1=1, C2=1, continuous=False, figsize=400):

        self._E0 = E0
        self._E1 = E1
        self._E2 = E2
        self._E3 = E3
        self._h1 = h1
        self._h2 = h2
        self._C1 = C1
        self._C2 = C2

        self._beta = self._get_beta(E0, E1, E2, E3)

        d1 = np.logspace(-3,3,30)
        d2 = np.logspace(-3,3,30)
        d1 = np.hstack([[0],d1])
        d2 = np.hstack([[0],d2])
        d1,d2 = np.meshgrid(d1, d2)
        d1 = d1.flatten()
        d2 = d2.flatten()
        self.d1 = d1
        self.d2 = d2


        self.paused = False
        self.continuous = continuous

        self.figsize = figsize

        self.E1_slider = None
        self.E2_slider = None
        self.h1_slider = None
        self.h2_slider = None
        self.C1_slider = None
        self.C2_slider = None
        
        self.alpha12_slider = None
        self.alpha21_slider = None
        self.gamma12_slider = None
        self.gamma21_slider = None
        self.beta_slider = None
        
        self.fig = None
        self.figs = []
        self.fig_widget_rows = []
        
        self.widgets = None

        self._setup_sliders()
        self._setup_figs()
        self._setup_widget()

    def _setup_sliders(self):

        continuous = self.continuous
        self.C1_slider = widgets.FloatSlider(
            value=np.log10(self._C1),
            min=-2.0,
            max=2.0,
            step=0.2,
            description='log(C1):',
            continuous_update=continuous)

        self.C2_slider = widgets.FloatSlider(
            value=np.log10(self._C2),
            min=-2.0,
            max=2.0,
            step=0.2,
            description='log(C2):',
            continuous_update=continuous)

        self.h1_slider = widgets.FloatSlider(
            value=np.log10(self._h1),
            min=-1.0,
            max=1.0,
            step=0.2,
            description='log(h1):',
            continuous_update=continuous)

        self.h2_slider = widgets.FloatSlider(
            value=np.log10(self._h2),
            min=-1.0,
            max=1.0,
            step=0.2,
            description='log(h2):',
            continuous_update=continuous)

        self.E1_slider = widgets.FloatSlider(
            value=self._E1,
            min=0,
            max=1,
            step=0.05,
            description='E1:',
            continuous_update=continuous)

        self.E2_slider = widgets.FloatSlider(
            value=self._E2,
            min=0,
            max=1,
            step=0.05,
            description='E2:',
            continuous_update=continuous)


        self.alpha12_slider = widgets.FloatSlider(
            value=0,
            min=-3.0,
            max=3.0,
            step=0.2,
            description='log(alp12):',
            continuous_update=continuous)

        self.alpha21_slider = widgets.FloatSlider(
            value=0,
            min=-3.0,
            max=3.0,
            step=0.2,
            description='log(alp21):',
            continuous_update=continuous)

        self.gamma12_slider = widgets.FloatSlider(
            value=0,
            min=-1.4,
            max=1.6,
            step=0.2,
            description='log(gam12):',
            continuous_update=continuous)

        self.gamma21_slider = widgets.FloatSlider(
            value=0,
            min=-1.4,
            max=1.6,
            step=0.2,
            description='log(gam21):',
            continuous_update=continuous)

        self.beta_slider = widgets.FloatSlider(
            value=self._beta,
            min=-1,
            max=1,
            step=0.05,
            description='beta:',
            continuous_update=continuous)

        sliders = [self.h1_slider, self.h2_slider,
            self.E1_slider, self.E2_slider, self.C1_slider, self.C2_slider,
            self.alpha12_slider, self.alpha21_slider,
            self.gamma12_slider, self.gamma21_slider, self.beta_slider]
        
        for s in sliders:
            s.observe(self.refresh, names="value")
        
    @abstractmethod
    def _setup_figs(self):
        pass
        

    def _setup_widget(self):

        for fig in self.figs:
            fig.layout.scene.on_change(self.cam_change, 'camera')

        E_container = widgets.HBox(
            children=[self.E1_slider, self.E2_slider]
        )
        C_container = widgets.HBox(
            children=[self.C1_slider, self.C2_slider]
        )
        h_container = widgets.HBox(
            children=[self.h1_slider, self.h2_slider]
        )
        alpha_container = widgets.HBox(
            children=[self.alpha21_slider, self.alpha12_slider]
        )
        gamma_container = widgets.HBox(
            children=[self.gamma21_slider, self.gamma12_slider]
        )
        beta_container = widgets.HBox(
            children=[self.beta_slider,]
        )



        label_single = widgets.Label(value="Single drug parameters")
        label_combo = widgets.Label(value="Synergy parameters")

        default_button = widgets.Button(description='Reset')
        musyc_button = widgets.Button(description='MuSyC Null')
        bliss_button = widgets.Button(description='Bliss Null')
        loewe_button = widgets.Button(description='Loewe Null')

        buttons = widgets.HBox([default_button, musyc_button, bliss_button, loewe_button])

        default_button.on_click(self.reset_to_default)
        musyc_button.on_click(self.reset_to_musyc)
        bliss_button.on_click(self.reset_to_bliss)
        loewe_button.on_click(self.reset_to_loewe)

        widget_list = [
            buttons,
            label_single,
            E_container,
            C_container,
            h_container,
            label_combo,
            beta_container,
            alpha_container,
            gamma_container]
        
        widget_list = self.fig_widget_rows + widget_list
        self.widgets = widgets.VBox(widget_list)

    def get_parameters(self):
        alpha12 = np.power(10., self.alpha12_slider.value)
        alpha21 = np.power(10., self.alpha21_slider.value)
        gamma12 = np.power(10., self.gamma12_slider.value)
        gamma21 = np.power(10., self.gamma21_slider.value)
        if alpha12==np.power(10., -3): alpha12=0
        if alpha21==np.power(10., -3): alpha21=0
        beta = self.beta_slider.value

        E1 = self.E1_slider.value
        E2 = self.E2_slider.value
        E0 = self._E0
        C1 = np.power(10., self.C1_slider.value)
        C2 = np.power(10., self.C2_slider.value)
        h1 = np.power(10., self.h1_slider.value)
        h2 = np.power(10., self.h2_slider.value)
        
        
        E3 = self._get_E3(E0, E1, E2, beta)

        return E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21

    def refresh(self, change):
        """
        Handler for changes in slider values
        Regenerates MuSyC model data, and plots it
        """

        if self.paused: return
        
        E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21 = self.get_parameters()

        d1 = np.power(10.,self.fig.data[0].x)
        d2 = np.power(10.,self.fig.data[0].y)
        

        d1[d1==np.min(d1)] = 0
        d2[d2==np.min(d2)] = 0
            
        self._update_figs(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)

    @abstractmethod
    def _update_figs(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        pass

    def run(self):
        return self.widgets

    def reset_to_default(self, b):
        self.paused=True
        self.E1_slider.value=self._E1
        self.E2_slider.value=self._E2
        self.h1_slider.value=np.log10(self._h1)
        self.h2_slider.value=np.log10(self._h2)
        self.C1_slider.value=np.log10(self._C1)
        self.C2_slider.value=np.log10(self._C2)
        self.alpha12_slider.value=0
        self.alpha21_slider.value=0
        self.beta_slider.value=self._beta
        self.gamma12_slider.value=0
        self.gamma21_slider.value=0
        self.paused=False
        self.refresh(0)

    def reset_to_bliss(self, b):
        self.paused=True
        E1 = self.E1_slider.value
        E2 = self.E2_slider.value
        self.alpha12_slider.value=0
        self.alpha21_slider.value=0
        self.gamma12_slider.value=0
        self.gamma21_slider.value=0

        E0=self._E0
        E3 = E1*E2
        self.beta_slider.value=self._get_beta(E0, E1, E2, E3)

        self.paused=False
        self.refresh(0)

    def reset_to_loewe(self, b):
        self.paused=True
        self.h1_slider.value=0
        self.h2_slider.value=0
        self.alpha12_slider.value=-3
        self.alpha21_slider.value=-3

        self.paused=False
        self.refresh(0)

    def reset_to_musyc(self, b):
        self.paused=True
        self.beta_slider.value=0
        self.alpha12_slider.value=0
        self.alpha21_slider.value=0
        self.gamma12_slider.value=0
        self.gamma21_slider.value=0

        self.paused=False
        self.refresh(0)

    def cam_change(self, layout, camera):
        if self.paused: return
        self.paused = True
        for other_fig in self.figs:
            other_fig.layout.scene.camera = camera
        self.paused = False

class MuSyC_Demo(Demo):
    def __init__(self, E0=1, E1=0.4, E2=0.5, E3=0.4, h1=2, h2=0.5, C1=1, C2=1, continuous=True, figsize=600):
        super().__init__(E0=E0, E1=E1, E2=E2, E3=E3, h1=h1, h2=h2, C1=C1, C2=C2, continuous=continuous, figsize=figsize)

    #override
    def _setup_figs(self):
        d1 = self.d1
        d2 = self.d2

        E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21 = self.get_parameters()
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)

        self.fig = self.get_fig_widget(d1, d2, E, "Dose Response", width=self.figsize, height=self.figsize, z_title="E (MuSyC)")
        self.figs.append(self.fig)
        self.fig_widget_rows.append(self.fig)

    def _update_figs(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        E = self._MuSyC_E(d1,d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        E[np.isnan(E)] = 0
        self.fig.data[0].z = E

class MuSyC_Bliss_Demo(Demo):
    def __init__(self, E0=1, E1=0.4, E2=0.5, E3=0.4, h1=2, h2=0.5, C1=1, C2=1, continuous=False, figsize=400):
        super().__init__(E0=E0, E1=E1, E2=E2, E3=E3, h1=h1, h2=h2, C1=C1, C2=C2, continuous=continuous, figsize=figsize)
        

    #override
    def _setup_figs(self):
        d1 = self.d1
        d2 = self.d2
        
        E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21 = self.get_parameters()
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        bs = self._bliss(d1, d2, E, E0, E1, E2, h1, h2, C1, C2)
        
        self.fig = self.get_fig_widget(d1, d2, E, "Dose Response", width=self.figsize, height=self.figsize, z_title="E (MuSyC)")
        self.figs.append(self.fig)

        bliss_fig = self.get_fig_widget(d1, d2, bs, "Bliss Excess", zlim=(-0.5,0.5),
                                clim=(-0.5,0.5), width=self.figsize,
                                height=self.figsize, center_on_zero=True,
                                cmap="PRGn", z_title="Bliss Excess")
        
        
        self.figs.append(bliss_fig)

        self.fig_widget_rows.append(widgets.HBox(
            [self.fig, bliss_fig]
        ))

    def _update_figs(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        E = self._MuSyC_E(d1,d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        bs = self._bliss(d1,d2, E, E0, E1, E2, h1, h2, C1, C2)
        E[np.isnan(E)] = 0
        self.fig.data[0].z = E
        self.figs[1].data[0].z = bs

class MuSyC_Loewe_Demo(Demo):
    def __init__(self, E0=1, E1=0.5, E2=0.5, E3=0.5, h1=2, h2=0.5, C1=1, C2=1, continuous=False, figsize=400):
        super().__init__(E0=E0, E1=E1, E2=E2, E3=E3, h1=h1, h2=h2, C1=C1, C2=C2, continuous=continuous, figsize=figsize)
        

    #override
    def _setup_figs(self):
        d1 = self.d1
        d2 = self.d2
        
        E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21 = self.get_parameters()
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        with np.errstate(divide='ignore', invalid='ignore'):
            ls = -np.log(self._loewe(d1, d2, E, E0, E1, E2, h1, h2, C1, C2))

        self.fig = self.get_fig_widget(d1, d2, E, "Dose Response", width=self.figsize, height=self.figsize, z_title="E (MuSyC)")
        self.figs.append(self.fig)

        loewe_fig = self.get_fig_widget(d1, d2, ls, "Loewe Synergy", zlim=(-3,3),
                                clim=(-3,3), width=self.figsize,
                                height=self.figsize, center_on_zero=True,
                                cmap="PRGn", z_title="-log(loewe)")
        
        
        self.figs.append(loewe_fig)

        self.fig_widget_rows.append(widgets.HBox(
            [self.fig, loewe_fig]
        ))

    def _update_figs(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        with np.errstate(divide='ignore', invalid='ignore'):
            ls = -np.log(self._loewe(d1, d2, E, E0, E1, E2, h1, h2, C1, C2))

        E[np.isnan(E)] = 0
        self.fig.data[0].z = E
        self.figs[1].data[0].z = ls

class All_Demo(Demo):

    #override
    def _setup_figs(self):
        d1 = self.d1
        d2 = self.d2
        
        E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21 = self.get_parameters()
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        bs = self._bliss(d1, d2, E, E0, E1, E2, h1, h2, C1, C2)
        

        with np.errstate(divide='ignore', invalid='ignore'):
            ls = -np.log(self._loewe(d1, d2, E, E0, E1, E2, h1, h2, C1, C2))

        self.fig = self.get_fig_widget(d1, d2, E, "Dose Response", width=self.figsize, height=self.figsize, z_title="E (MuSyC)")
        

        bliss_fig = self.get_fig_widget(d1, d2, bs, "Bliss Excess", zlim=(-0.5,0.5),
                        clim=(-0.5,0.5), width=self.figsize,
                        height=self.figsize, center_on_zero=True,
                        cmap="PRGn", z_title="Bliss Excess")
        


        loewe_fig = self.get_fig_widget(d1, d2, ls, "Loewe Synergy", zlim=(-3,3),
                                clim=(-3,3), width=self.figsize,
                                height=self.figsize, center_on_zero=True,
                                cmap="PRGn", z_title="-log(loewe)")
        
        
        self.figs.append(self.fig)
        self.figs.append(bliss_fig)
        self.figs.append(loewe_fig)

        self.fig_widget_rows.append(self.fig)
        self.fig_widget_rows.append(widgets.HBox(
            [bliss_fig, loewe_fig]
        ))

    def _update_figs(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        E = self._MuSyC_E(d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21)
        bs = self._bliss(d1, d2, E, E0, E1, E2, h1, h2, C1, C2)
        with np.errstate(divide='ignore', invalid='ignore'):
            ls = -np.log(self._loewe(d1, d2, E, E0, E1, E2, h1, h2, C1, C2))

        E[np.isnan(E)] = 0
        self.fig.data[0].z = E
        self.figs[1].data[0].z = bs
        self.figs[2].data[0].z = ls
        