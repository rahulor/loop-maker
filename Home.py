import streamlit as st
# configure page
#------------------------------------------------------------------------------------------------------
st.set_page_config(
     page_title="LoopMaker",
     page_icon=":knot:",
     layout="centered",
     initial_sidebar_state="expanded",
     menu_items={
        #'Get Help': 'https://www.extremelycoolapp.com/help',
        #'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "The loop-maker app creates random loops."
     })
#st.title("The LoopMaker app")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.2rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


st.subheader(":blue[LoopMaker] | science meets art") # LoopMaker: Creating Chaos and Beauty") # 
st.caption("**_the app that never creates the same loop twice.._**")
#------------------------------------------------------------------------------------------------------
# imorts 
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import butter, filtfilt
from streamlit_extras.switch_page_button import switch_page
#------------------------------------------------------------------------------------------------------
def initialize_parameters():
     if 'seedx' not in st.session_state:
          st.session_state.seedx = np.random.randint(0, 10000)
     if 'seedy' not in st.session_state:
          st.session_state.seedy = np.random.randint(10000, 20000)
     if 'seedz' not in st.session_state:
          st.session_state.seedz = np.random.randint(20000, 30000)
     if 'npoints' not in st.session_state:
          st.session_state.npoints = 100
     return
def update_seed(axis):
     match axis:
          case 'x':
               st.session_state.seedx += 1
          case 'y':
               st.session_state.seedy += 1
          case 'z':
               st.session_state.seedz += 1
     return

@st.cache_data
def brownian_bridge(seed, N):
    T = 1
    dt = T/N
    B = np.empty(N+1)
    rng= np.random.RandomState(seed)
    xi = np.sqrt(2*dt)*rng.randn(N+1) # D = 1
    xi[0] = 0
    W = np.cumsum(xi)
    for n in range(0, N+1):           
         t = n * dt
         B[n] = W[n] - (t/T)*W[N]                                                        
    return B

def pad_both_ends(arr_, pad):
     arr = np.roll(arr_, 30)
     return np.array(list(arr[-pad:]) + list(arr) + list(arr[0:pad]))

def get_smooth_bridge(B):
     #Setting standard filter requirements.
     w = 1.0/10 # The critical frequency 
     b, a = butter(5, w, 'low')
     pad = 50
     B_pad= pad_both_ends(B, pad)
     B_smooth = filtfilt(b, a, B_pad)[pad:-pad+1]
     return B_smooth     

def plot_brownian_bridge(x, y, z, title):
     fig = go.Figure(layout=go.Layout(height=350, width=300), layout_title_text=title)
     fig.add_trace(go.Scatter(x=None, y=x, mode='lines', name='x', line=dict(color='green')))
     fig.add_trace(go.Scatter(x=None, y=y, mode='lines', name='y', line=dict(color='blue')))
     fig.add_trace(go.Scatter(x=None, y=z, mode='lines', name='z', line=dict(color='orange')))
     fig.update_yaxes(range = [-2, 2])
     return fig

def create_the_sidebar():
     with st.sidebar:
          Bx = brownian_bridge(st.session_state.seedx, st.session_state.npoints)
          By = brownian_bridge(st.session_state.seedy, st.session_state.npoints)
          Bz = brownian_bridge(st.session_state.seedz, st.session_state.npoints)
          
          scalex = st.slider('scale x-coordinate', 0.0, 1.5, 1.0, step=0.01)
          scaley = st.slider('scale y-coordinate', 0.0, 1.5, 1.0, step=0.01)
          scalez = st.slider('scale z-coordinate', 0.0, 1.5, 1.0, step=0.01)
          
          Bx = Bx*scalex
          By = By*scaley
          Bz = Bz*scalez

          Bx_smooth = get_smooth_bridge(Bx)
          By_smooth = get_smooth_bridge(By)
          Bz_smooth = get_smooth_bridge(Bz)

          slot1 = st.empty() # for brownian bridge
          
          st.selectbox('number of points on the curve', 
          [100, 150, 200, 300, 400, 500, 600, 800, 1000, 2000, 3000], key='npoints')
          
          #slot2 = st.empty() # for smooth brownian bridge
          
          # fig1 = plot_brownian_bridge(Bx, By, Bz, "Brownian bridge")
          # slot1.plotly_chart(fig1)

          fig2 = plot_brownian_bridge(Bx_smooth, By_smooth, Bz_smooth, "")
          slot1.plotly_chart(fig2)
          return [Bx_smooth, By_smooth, Bz_smooth]
          
def create_the_main_page(xyz):
     xsmooth, ysmooth, zsmooth = xyz
     cubesize = 2
     fig = go.Figure(layout=go.Layout(
          height=500, width=350, uirevision=True, 
          scene=dict(
               aspectmode='cube', 
               aspectratio=dict(x=1, y=1, z=1),
               xaxis = dict(range=[-cubesize,cubesize], nticks=4,),
               yaxis = dict(range=[-cubesize,cubesize], nticks=4,),
               zaxis = dict(range=[-cubesize,cubesize], nticks=4,),
               )
          ))
     fig.add_trace(go.Scatter3d(x=xsmooth, y=ysmooth, z=zsmooth, # mode='markers', mode='lines',
                    marker=dict(
                         size=2,
                         color= zsmooth,  # set color to an array/list of desired values
                         colorscale='magma',# choose a colorscale
                         opacity=0.7),
                    line=dict(color='grey', width=2.0)
                    ))
     st.plotly_chart(fig)
     
def create_refresh_buttons():
     #st.write('🔄  Refresh coordinates')
     st.write('Refresh coordinates')
     col2, col3, col4 = st.columns([1,1,1], gap="small")
     st.write("""
          <style>
               [data-testid="column"] {
               width: calc(33.3333% - 1rem) !important;
               flex: 1 1 calc(33.3333% - 1rem) !important;
               min-width: calc(33.3333% - 1rem) !important;}
          </style>""", unsafe_allow_html=True)
     with col2:
          st.button('x', on_click=update_seed, args='x')
          #st.write('seed-x = ', st.session_state.seedx)
     with col3:
          st.button('y', on_click=update_seed, args='y')
          #st.write('seed-y = ', st.session_state.seedy)
     with col4:
          st.button('z', on_click=update_seed, args='z')
          #st.write('seed-z = ', st.session_state.seedz)
          
@st.cache_data
def convert_df(df):
     return df.to_csv(index=True).encode('utf-8')
def additional_info(xyz):
     with st.expander("datafile"):
          df = pd.DataFrame(np.vstack(xyz).T, columns=['x', 'y', 'z'])
          csv = convert_df(df)
          st.download_button("⬇️ Download (csv) ",csv, "file.csv", "text/csv", key='download-csv')
          st.dataframe(df)
          #st.write("Additional controls in the side bar (top-left arrow)")
          about = st.button("About")
          if about:
               switch_page("About")
     return

#     streamlit run curve.py --server.headless true &  
if __name__ == "__main__":
     initialize_parameters()
     xyz = create_the_sidebar()
     create_the_main_page(xyz)
     create_refresh_buttons()
     additional_info(xyz)
