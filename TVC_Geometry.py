import math
import matplotlib.pyplot as plt

class GeometrySolver:

    def __init__(self):
        pass

    # this function is essentially a 4 bar linkage solver given an angle and 3 sides
    # a1 is the angle between l1 and l4 which have a vertex at (0,0)
    # C is the intersection of l2 and l3
    def Find_C(self,a_A,l1,l2,l3,l4):
        # need to use epsilon to avoid rounding errors causing sqrt(-#)
        # and to avoid rounding errors causing comparisons to be false when should be true
        epsilon = 0.001

        e = l4
        f = math.cos(a_A)*l1
        g = math.sin(a_A)*l1

        a = (2*f-2*e)**2/(4*g**2)+1
        b = 2*(2*f-2*e)*(f**2+l3**2-e**2-l2**2+g**2)/(4*g**2)+2*e
        c = (f**2+l3**2-e**2-l2**2+g**2)**2/(4*g**2)+e**2-l3**2

        descriminant = b**2 - 4*a*c
        # checking if descriminant is a small negative
        # if so, it was likely a rounding error and was supposed to be 0
        if descriminant < 0 and abs(descriminant) < epsilon:
            descriminant = 0

        plus_root = (-b + math.sqrt(descriminant))/(2*a)
        minus_root = (-b - math.sqrt(descriminant))/(2*a)

        descriminant_plus = 4*g**2-4*(g**2-l2**2+(plus_root+f)**2)
        descriminant_minus = 4*g**2-4*(g**2-l2**2+(minus_root+f)**2)

        if descriminant_plus < 0 and abs(descriminant_plus) < epsilon:
            descriminant_plus = 0
        if descriminant_minus < 0 and abs(descriminant_minus) < epsilon:
            descriminant_minus = 0

        circ_D_y = math.sqrt(l3**2-(plus_root+l4)**2)
        circ_B_y1 = (2*g+math.sqrt(descriminant_plus))/2
        circ_B_y2 = (2*g-math.sqrt(descriminant_plus))/2
        y_plus_root = [circ_D_y,-circ_D_y,circ_B_y1,circ_B_y2]

        circ_D_y = math.sqrt(l3**2-(minus_root+l4)**2)
        circ_B_y1 = (2*g+math.sqrt(descriminant_minus))/2
        circ_B_y2 = (2*g-math.sqrt(descriminant_minus))/2
        y_minus_root = [circ_D_y,-circ_D_y,circ_B_y1,circ_B_y2]

        possible_pos = []

        if(abs(y_plus_root[0] - y_plus_root[2]) < epsilon):
            possible_pos.append((plus_root,y_plus_root[0]))
        elif(abs(y_plus_root[0] - y_plus_root[3]) < epsilon):
            possible_pos.append((plus_root, y_plus_root[0]))
        else:
            possible_pos.append((plus_root,y_plus_root[1]))

        # used y_minus_root[1] instead of y_minus_root[0]
        # to prevent missing the negative overlap point if a1 is very close to 0
        if(abs(y_minus_root[1] - y_minus_root[2]) < epsilon):
            possible_pos.append((minus_root,y_minus_root[1]))
        elif(abs(y_minus_root[1] - y_minus_root[3]) < epsilon):
            possible_pos.append((minus_root, y_minus_root[1]))
        else:
            possible_pos.append((minus_root,y_minus_root[0]))

        # returns the possible position with the greatest y value
        # this is the relavent location for our use case
        if possible_pos[0][1] > possible_pos[1][1]:
            return possible_pos[0]
        return possible_pos[1]


    def Solve_Geometry(self,a_A,l1,l2,l3,l4):
        b = [-math.cos(a_A)*l1, math.sin(a_A)*l1]
        c = self.Find_C(a_A, l1, l2, l3, l4)

        a_B = math.acos((-b[0]*(c[0]-b[0]) + -b[1]*(c[1]-b[1]))/(l1*l2))
        a_C = math.acos((((-l4-c[0])*(b[0]-c[0]) + -c[1]*(b[1]-c[1]))/(l3*l2)))
        a_D = math.acos(((c[0]+l4)*l4)/(l4*l3))

        return [[[0,0],b,c,[-l4,0]],[a_A,a_B,a_C,a_D]]


    def Angle_Change_Ratio(self,a_A,a_D,l1,l2,l3,l4):
        delta_A = 0.001
        geometry_change = self.Solve_Geometry(a_A+delta_A,l1,l2,l3,l4)
        delta_D = geometry_change[1][3]-a_D
        angle_ratio = -delta_D/delta_A

        return angle_ratio

    def Find_Gimble_Angle(self,a_D,h,w):
        return -(math.pi/2 - (math.pi-(a_D+math.atan(w/h))))


    def Show_Geometry(self,name,a_A,l1,l2,l3,l4,h,w,offset_angle):

        geometry = self.Solve_Geometry(a_A,l1,l2,l3,l4)
        b = geometry[0][1]
        c = geometry[0][2]

        a_B = geometry[1][1]
        a_C = geometry[1][2]
        a_D = geometry[1][3]

        # print(f"a_A = {a_A*180/math.pi}\u00B0")
        # print(f"a_B = {a_B*180/math.pi}\u00B0")
        # print(f"a_C = {a_C*180/math.pi}\u00B0")
        # print(f"a_D = {a_D*180/math.pi}\u00B0")

        # test that all internal angles in the quadrilateral add to 360 degrees
        # print((a_D+a_A+a_B+a_C)*180/math.pi)

        rot_angle = -offset_angle*math.pi/180  # changes to radians

        x = [0,b[0]]
        y = [0,b[1]]
        # rotates points to match the orientation of the physical system
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]
        plt.plot(x,y)
        x = [b[0], c[0]]
        y = [b[1], c[1]]
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]
        plt.plot(x,y)
        x = [c[0], -l4]
        y = [c[1], 0]
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]
        # plt.plot(x,y)  # plots the non-physical line from point C to point D
        x = [-l4, 0]
        y = [0, 0]
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]
        #plt.plot(x,y)  # plots the non-physical line from servo rotation axis to gimble rotation axis
        plt.plot([0,x[0]],[0,0])
        plt.plot([x[0],x[0]],[0,y[0]])
        x = [-l4, -l4-math.cos(math.pi-(a_D+math.atan(w/h)))*h]
        y = [0, math.sin(math.pi-(a_D+math.atan(w/h)))*h]
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]
        plt.plot(x,y)
        g = math.pi-(a_D+math.atan(w/h))
        x = [-l4-math.cos(g)*h, c[0]]
        y = [math.sin(g)*h, c[1]]
        x = [math.cos(rot_angle)*x[0]-math.sin(rot_angle)*y[0], math.cos(rot_angle)*x[1]-math.sin(rot_angle)*y[1]]
        y = [math.sin(rot_angle)*x[0]+math.cos(rot_angle)*y[0], math.sin(rot_angle)*x[1]+math.cos(rot_angle)*y[1]]

        # print h
        # print(((math.sin(math.pi-(a_D+math.atan(w/h)))*h)**2 + (math.cos(math.pi-(a_D+math.atan(w/h)))*h)**2)**(1/2))
        # print l3
        # print(((-l4-c[0])**2+(c[1])**2)**(1/2))

        plt.plot(x,y)
        plt.axis("equal")
        plt.title(label=name)
        plt.show()
