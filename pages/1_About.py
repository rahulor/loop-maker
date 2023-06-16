
import streamlit as st

st.write("""
         # About
         """)
st.write("""
          The :blue[LoopMaker] app creates random loops. All you need to do is refresh the coordinates. It's fun!
          
          [For enthusiasts] You can tweak the scaling using our handy slider. 
          Add more points to your loop and make your life harder. The more points you add, the greater the risk of getting tied up
          in _knots_. How do you identify a _knot_? No, the real question is how to automate it once you've got the datafile? 
          If you've got the answer, we should talk!
          
          [For nerds] The app creates closed space curves. We employ _Brownian bridge_ to create closed space curves, and 
          each coordinate passes through a low pass filter to make the loop look smooth (differentiable) and aesthetically pleasing. 
          We also use various techniques like array rotation, padding, and slicing to avoid sharp bends that can distort the loop.
          The resulting loop is a random sample from the _space_ of all possible loops. However, not every sample is drawn through 
          this constrained approach, and we make no such claims. Good luck! 
               """)

st.write("""
Source code is available at 
[https://github.com/rahulor/loop-maker](https://github.com/rahulor/loop-maker).
""")
