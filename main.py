import math
from TVC_Geometry import GeometrySolver
from TVC_Physics import Ts_to_Tg


# things to change
############################################
required_torque = 0.113  # Nm
required_speed = 30  # degrees/sec
required_angular_range = 20  # degrees/sec
required_angular_deflection = 10  # degrees
servo_torque = 1.3  # Nm
servo_speed = 300  # degrees/sec
h = ((1.28*0.0254)**2-(1.19*0.0254)**2)**(1/2)  # m
w = 1.19*0.0254  # m
l1 = 0.9*0.0254  # m
l2 = 1.19*0.0254  # m
l3 = (h**2+w**2)**(1/2)  # m
l4 = 2.41*0.0254  # m
offset_angle = math.acos(2.3/2.41)*180/math.pi # degrees (this is the angle of elevation from the servo rotation axis to the gimble rotation axis)
# print(l1/0.0254)
# print(l2/0.0254)
# print(l3/0.0254)
# print(l4/0.0254)
# print(h/0.0254)
# print(w/0.0254)
# # print(offset_angle)
############################################

# might need to change if really weird geometry and this throws an error
a_A = math.pi/2-offset_angle*math.pi/180

geo_solver = GeometrySolver()
geometry = geo_solver.Solve_Geometry(a_A,l1,l2,l3,l4)

b = geometry[0][1]
c = geometry[0][2]
phi = math.acos((b[0]-c[0])/l2)
a_D = geometry[1][3]

# plugging in 1 for Ts gives the torque transformation ratio R_T (where Tg = Ts * R_T)
R_T = Ts_to_Tg(l1,l2,l3,a_A,a_D,phi,1)
print(R_T)
# print(f"R_T = {R_T}")
# print(f"phi = {phi*180/math.pi}\u00B0")
# print(f"Angle Change Ratio (d_omega/d_theta) = {geo_solver.Angle_Change_Ratio(a_A,a_D,l1,l2,l3,l4)}")

print()
print()
print()

# this is based on torque ratio when a_A is what it is set to above
if servo_torque*R_T < required_torque:
    print("Required Torque Not Satisfied")
    print(f"Calculated Torque: {servo_torque*R_T}Nm")
else:
    print("Required Torque Satisfied")
    print(f"Calculated Torque: {servo_torque*R_T}Nm")

print(f"Required Torque: {required_torque}Nm")

a_min = a_A
while R_T > 0:
    a_min -= 0.05
    min_geometry = geo_solver.Solve_Geometry(a_min,l1,l2,l3,l4)
    R_T = Ts_to_Tg(l1,l2,l3,a_min,min_geometry[1][3],math.acos((min_geometry[0][1][0]-min_geometry[0][2][0])/l2),1)
a_min += 0.05
min_geometry = geo_solver.Solve_Geometry(a_min,l1,l2,l3,l4)

print(f"Torque at min: {servo_torque*Ts_to_Tg(l1,l2,l3,a_min,min_geometry[1][3],math.acos((min_geometry[0][1][0]-min_geometry[0][2][0])/l2),1)}Nm")

a_max = math.pi
flag = True
while flag:
    try:
        max_geometry = geo_solver.Solve_Geometry(a_max,l1,l2,l3,l4)
        flag = False
    except:
        a_max -= 0.05

print(f"Torque at max: {servo_torque*Ts_to_Tg(l1,l2,l3,a_max,max_geometry[1][3],math.acos((max_geometry[0][1][0]-max_geometry[0][2][0])/l2),1)}Nm")
print()
# print(f"a_min = {a_min}")
# print(f"a_max = {a_max}")
# print(a_max*180/math.pi+offset_angle)

angular_range = min_geometry[1][3]-max_geometry[1][3]
if angular_range < required_angular_range*math.pi/180:
    print("Required Angular Range Not Satisfied")
    print(f"Calculated Angular Range: {angular_range*180/math.pi}\u00B0")
else:
    print("Required Angular Range Satisfied")
    print(f"Calculated Angular Range: {angular_range*180/math.pi}\u00B0")
print()


omega_min = geo_solver.Find_Gimble_Angle(min_geometry[1][3],h,w)*180/math.pi + offset_angle
omega_max = geo_solver.Find_Gimble_Angle(max_geometry[1][3],h,w)*180/math.pi + offset_angle

# print(omega_max)
# print(omega_min)

if omega_max > required_angular_deflection and omega_min < -required_angular_deflection:
    print("Required Angular Deflection Satisfied")
    print(f"Calculated Angular Deflection: {omega_min}\u00B0, {omega_max}\u00B0")
else:
    print("Required Angular Deflection Not Satisfied")
    print(f"Calculated Angular Deflection: {omega_min}\u00B0, {omega_max}\u00B0")
print()


# this is based on the angle change ratio when a_A is what it is set to above
slew_rate = servo_speed*(math.pi/180)*geo_solver.Angle_Change_Ratio(a_A,a_D,l1,l2,l3,l4)
if slew_rate < required_speed*math.pi/180 :
    print("Required Slew Rate Not Satisfied")
    print(f"Calculate Slew Rate: {slew_rate*180/math.pi}\u00B0/s")
else:
    print("Required Slew Rate Satisfied")
    print(f"Calculate Slew Rate: {slew_rate*180/math.pi}\u00B0/s")
min_slew_rate = servo_speed*(math.pi/180)*geo_solver.Angle_Change_Ratio(a_min,min_geometry[1][3],l1,l2,l3,l4)
max_slew_rate = servo_speed*(math.pi/180)*geo_solver.Angle_Change_Ratio(a_max,max_geometry[1][3],l1,l2,l3,l4)
print(f"Required Slew Rate: {required_speed}")
print(f"Slew Rate at min: {min_slew_rate*180/math.pi}\u00B0/s")
print(f"Slew Rate at max: {max_slew_rate*180/math.pi}\u00B0/s")
print()


geo_solver.Show_Geometry("Neutral Angle",a_A,l1,l2,l3,l4,h,w,offset_angle)
geo_solver.Show_Geometry("Max Angle",a_max,l1,l2,l3,l4,h,w,offset_angle)
geo_solver.Show_Geometry("Min Angle",a_min,l1,l2,l3,l4,h,w,offset_angle)
