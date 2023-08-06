import numpy as np
from scipy.optimize import newton

class Ellipse(): 
    """
    This class is for a simple elipse: a elipse with center in the center of coordinates x, y, parallel to x axis
    with both focus in x axis

    Parameters:
        a: int, float (1): 
            semi mayor axis 
        e: int, float (1):
            eccentricity 
        or 
        b: int, float (1):
            semi minor axis

    """
    a = 1
    
    def __init__(self, a, e = None, b = None): 
        
        if e != None:  
            self.a = a  #mayor semi axis
            self.e = e  #eccentricity
            self.b = self.a*(1-self.e**2)**(1/2)  #minor semi axis 
            self.c = (self.a**2 - self.b**2)**(1/2)  #focus distance 
            self.focus = [self.c, 0]  #focus
            self.vacant_focus = [-self.c, 0]  #vancat focus
            

        elif b != None: 
            self.a = a
            self.b = b
            self.e = (1 - self.b**2/self.a**2)**(1/2)  
            self.c = (self.a**2 - self.b**2)**(1/2)  
            self.focus = [self.c, 0]
            self.vacant_focus = [-self.c, 0]  

            

#---propiedades-----------------------------------------------------------------
    

#---comportamiento---------------------------------------------------------------
    #calculate points of the ellipse:
    def get_points(self):

        theta = np.linspace(0,2*np.pi,200)
        elipsex = self.a*np.cos(theta)
        elipsey = self.b*np.sin(theta)

        elipse_positions = np.zeros((200,2))
        elipse_positions[:,0] = elipsex
        elipse_positions[:,1] = elipsey

        return elipse_positions
    
    @staticmethod
    def get_focus(center1, center2, radio1, radio2):
        """Find the intersection between two circles. The center and the radio of the circles are given.                                                                                                                                                                        
                                                                                                                                                                                                                                                                                
        Parameters:                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                
           center1: list, tuple or array (2):                                                                                                                                                                                                                                   
              Center of the first point                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                
        Return:                                                                                                                                                                                                                                                                 
           point1: tuple (2):                                                                                                                                                                                                                                                   
              Point 1                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                
        """
        r1 = radio1
        r2 = radio2

        c1 = np.array(center1)
        c2 = np.array(center2)

        d = ((c2[0]-c1[0])**2 + (c2[1] - c1[1])**2)**(1/2)
        a = (r1**2 - r2**2 + d**2)/(2*d)

        dx = (c2[0] - c1[0])/d
        dy = (c2[1] - c1[1])/d

        px = c1[0] + a*dx
        py = c1[1] + a*dy

        h = (r1**2 - a**2)**(1/2)

        p1_x = px + h*dy
        p1_y = py - h*dx

        p2_x = px - h*dy
        p2_y = py + h*dx

        point1 = [p1_x, p1_y]
        point2 = [p2_x, p2_y]

        return point1, point2
    

def LambertProblem(r1, r2, theta, a = None, t = None):
    """
    LambertProblem solve the Lamnbert Equation given a value of semi mayor axis or a value of time

    Parameters:
        r1: int, float (1): 
            Distance point one to focus
        r2: int, float (1):
            Distance point two to focus
        theta: int, float (1):
            Angle between r1 and r2
        a: int, float (1):
            semi mayor axis from transfer elipse
        or 
        t: int, float (1):
            transfer time 


    Return:
    if you have the value of a and want to know the trasnfer time, the return is 
        t1, t2: tuple (2):
            two transfer times 

    if you have the value of time and want to know the semi mayor axis, the return is
        a: float(1): 
            semi mayor axis                            
    """
 
    if t != None:
        def funcion(a):
            c = np.sqrt(r1**2 + r2**2 - 2*r1*r2*np.cos(theta))
            s = (r1 + r2 + c)/2
                
            alpha = lambda a,s=s: 2*np.arcsin((s/(2*a))**(1/2))
            beta = lambda a,s=s,c=c: 2*np.arcsin(((s-c)/(2*a))**(1/2))

            f = t - a**(3/2)*(alpha(a) - beta(a) - (np.sin(alpha(a)) - np.sin(beta(a))))

            return f
        a = newton(funcion,1.2)
        return a
        
    if a != None: 
        c = np.sqrt(r1**2 + r2**2 - 2*r1*r2*np.cos(theta))
        s = (r1 + r2 + c)/2

        alpha1 = 2*np.arcsin((s/(2*a))**(1/2))
        alpha2 = 2*np.pi - alpha1
        beta1 = 2*np.arcsin(((s-c)/(2*a))**(1/2))
        beta2 = - beta1

        t1 = a**(3/2) * (alpha1 - beta1 - (np.sin(alpha1) - np.sin(beta1)))
        t2 = a**(3/2) * (alpha2 - beta2 - (np.sin(alpha2) - np.sin(beta2)))

        return t1, t2

    


    








