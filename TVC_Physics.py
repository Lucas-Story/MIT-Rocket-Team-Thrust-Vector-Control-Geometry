import math

# this function solves for the ratio between the input torque from the servo (Ts) and the output torque felt on the gimble joint (Tg)
# equation found using pen and paper physical analysis
def Ts_to_Tg(l1, l2, l3, a_A, a_D, phi, Ts):
    # note: this function will break if a_B is greater than 180 degrees
    gamma = (-math.sin(a_A)*math.sin(phi)*l2 - math.cos(a_A)*math.cos(phi)*l2)/(math.cos(a_A)*math.sin(phi)*l2-math.sin(a_A)*math.cos(phi)*l2)
    mu = -math.tan(a_D)*math.sin(a_A) - math.tan(a_D)*math.cos(a_A)*gamma + math.cos(a_A) - math.sin(a_A)*gamma
    return Ts*l3/l1*mu/(-math.cos(a_D) - math.tan(a_D)*math.sin(a_D))

