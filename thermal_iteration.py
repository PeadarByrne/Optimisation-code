import numpy as np


#Water in temperatures
T_h_in=60   #hot water input temperature
T_c_in=20   #cold water input temperature

#
#Guess mh
mh=0.45
mt=mh/nt

#made up values to test thermal
Re_i = 11e3     #example value of Reynolds number to test function
Re_o = 6e3      #example value of Reynolds number to test function
m_c = 0.45      #example value of cold water mass flow rate
m_h = 0.45      #example value of hot water mass flow rate

def Thermal():
    A_i = np.pi * d_i * Lt * nt #sum of inner surface areas of all tubes
    Nu_i = 0.023 * (Re_i**0.8) * (Pr**0.3) #inner Nusselt number
    Nu_o = c * (Re_o**0.6) * (Pr**0.3) #outer Nusselt number  #c is 0.2 for triangular tube pitch and0.15 for square tube pitch
    h_i = (Nu_i*kw)/d_i
    h_o = (Nu_o*kw)/d_o
    U = 1/((1/h_i) + ((d_i*np.log10(d_o/d_i)/(2*kt)))+(d_i/(d_o*h_o)))

    dT_target = 0.05    #cut off value for change in temperature estimate between iterations
    dT_c = 1    #initialise change in cold temperature output between interations
    dT_h = 1    #initialise change in hot temperature output between interations

    #Water out estimates
    T_h_out=55
    T_c_out=24
    while (dT_c>dT_target) or (dT_h>dT_target):

        T_c_out_old = T_c_out
        T_h_out_old = T_h_out   #keep the old values to see if values have converged enough
        '''
        #find new correction factor F, only for more than one tube pass
        R_corr = (T_c_in - T_c_out)/(T_h_out - T_h_in)
        P_corr = (T_h_out - T_h_in)/(T_c_in-T_h_in)
        F = something
        '''
        F = 1 #works for one tube pass, more gets complicated
        delta_T_lm = ((T_h_in-T_c_out)-(T_h_out-T_c_in))/(np.log((T_h_in-T_c_out)/(T_h_out-T_c_in)))
        T_c_out = ((F * U * A_i * delta_T_lm)+(T_c_in * m_c * Cp))/(m_c*Cp)     #finds new cold output temp
        T_h_out = (-(F * U * A_i * delta_T_lm)+(T_h_in * m_h * Cp))/(m_h*Cp)    #finds new hot output temp
        dT_c = abs(T_c_out-T_c_out_old)     #finds cahnge in estimated cold output temp
        dT_h = abs(T_h_out-T_h_out_old)     #finds cahnge in estimated hot output temp
    
    Q = U*A_i*F*delta_T_lm      #rate of heat transfer
    mc_c = m_c*Cp  
    mc_h = m_h*Cp
    mc_min = min(mc_h,mc_c)     #find the minimum value of mcp
    #find effectiveness using the minimum fluid
    if mc_min == mc_c :
        e=(T_c_out-T_c_in)/(T_h_in-T_c_in)
    else:
        e=(T_h_out-T_c_in)/(T_h_in-T_c_in)


    
    print('Cold output temperature = ',T_c_out)
    print('Hot output temperature = ',T_h_out)
    print('Rate of heat transfer = ',Q)
    print('Effectiveness = ',e)


Thermal()