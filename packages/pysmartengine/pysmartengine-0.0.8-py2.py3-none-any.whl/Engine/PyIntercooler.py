

def TafterCool(Tin,etacool,Twater):
    return Tin-etacool*(Tin-Twater)

def pressuredrop(etazk,massflow,rho,Area,g=9.8):
    """
    11.5~15之间
    """
    return etazk*massflow**2/(2.*g*Area**2*rho)