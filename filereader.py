from ulab import numpy as np
import math
dpi = 1016
pud_buff = 10

rad_max = 5.5
rad_min = 0.75


class Drawer():
    
    def Draw(self, filename):
        with open(filename) as f:
            raw = f.readline()
            print(raw)
            lines = raw.split(';')
            coord_list = []
            points = []
            # Last xs and last ys values, this will start at 0.75,0 and be changed later on. 
            lx = 0.75
            ly = 0
            
            with open('xy.txt', 'w') as xy:
                
                for line in lines:
                    command = line[:2] #check first two chars of string
                    print(command)
                    if command == "IN":     #initialize
                        print("Drawing initialized")
                    
                    elif command == "SP":
                        #announce selected pen, but not used for anything
                        pen = line[2:]
                        print("Pen Select: {}".format(pen))
                
                    elif command == 'PU':
                        # Parse Here
                        coord = line[2:].split(',')
                        if len(coord) > 1:
                            x = float(coord[0])/dpi
                            y = float(coord[1])/dpi
                            x,y = Drawer.adjust(x,y)

                            
                            for n in range(0,pud_buff):
                                string = str(x) + ',' + str(y) + ', 0'
#                                 print(string)
                                xy.write(f'{string} \n')
                                lx = x
                                ly = y
                        
                        elif len(coord) == 1:
                            print('empty coord in pu')
                            
                            
                            
                    if command == "PD":

                        coord = line[2:].split(',')
                        xs = coord[0:len(coord):2]
                        ys = coord[1:len(coord):2]
                        
                        for i in range(0,len(xs)):
                            
                            x = float(xs[i])/dpi
                            y = float(ys[i])/dpi
                            x,y = Drawer.adjust(x,y)
                            
                            
                            # This is a root-sum-square function that will determine the magnitude of the difference between
                            # x, x_n and y, y_n
                            magnitude = math.sqrt( (x-lx)**2 + (y-ly)**2 )
                            
                            if (magnitude > 0.5) & (magnitude < 1):
                                thresh = 10
                            elif (magnitude >= 1) & (magnitude < 1.5):
                                thresh = 15
                            elif (magnitude >= 1.5) & (magnitude < 2):
                                thresh = 20
                            elif magnitude > 2:
                                thresh = 25
                                
                            # If the magnitude is greater than a threshold value, we will interpolate
                            # 0.75 is a random threshold value I input based on the list of magnitudes
                            if magnitude > 0.5:
                                
                                # This creates 50 points between x and x_n, y and y_n
                                lin_x = np.linspace(lx, x, thresh)
                                lin_y = np.linspace(ly, y, thresh)
                                
                                # Now, for every point in that linspace (lin_x and lin_y), add the x,y pair to the list points 
                                for q in range(0,len(lin_x)):
                                    string = str(lin_x[q]) + ',' + str(lin_y[q]) + ', 1'
#                                     print(string, magnitude, 'interpolating')
                                    xy.write(f'{string} \n')
                                    lx = lin_x[q]
                                    ly = lin_y[q]

                            # If the magnitude of the difference between points is not greater than thresh, dont interpolate
                            else:
#                                 string = str(x) + ',' + str(y) + ', 1'
                                print(string, magnitude)
                                xy.write(f'{string} \n')

                    elif command == " ":
                        print("Blank Line")




    def adjust(x_target, y_target):
        
        rad_t = (x_target**2 + y_target**2)**(1/2)
        
        if x_target == y_target and x_target == 0: #moves off center allows adjustments to take place after
#             print('dead center')
            x_target += 0.01
            y_target += 0.01
            rad_t = (x_target**2 + y_target**2)**(1/2)
        
        if rad_t >= rad_max:
#             print('outer limit')
    #         adj_ratio = rad_t/rad_max
            adj_ratio = rad_max/rad_t
            
            x_target *= adj_ratio
            y_target *= adj_ratio
            
        if rad_t <= rad_min:
#             print('inner limit')
            adj_ratio = rad_min/rad_t
            x_target *= adj_ratio
            y_target *= adj_ratio
        

            
        return x_target, y_target
    
    
    
    
if __name__ == "__main__":
    fr = Drawer()
    filename = "single target point.hpgl"
    fr.Draw(filename)