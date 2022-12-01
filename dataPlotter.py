import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
import numpy as np

plt.ion()  # enable interactive drawing

class dataPlotter:
    def __init__(self, plotList):
        
        self.handleDict = {}
        
        # Instantiate lists to hold the time and data histories
        self.xHistory = []  # position x
        self.yHistory = []  # position y
        self.zHistory = []  # position z
        
        self.phiHistory = []  # position phi
        self.thetaHistory = []  # position theta
        self.psiHistory = []  # position psi
        
        self.uHistory = []  # velocity u
        self.vHistory = []  # velocity v
        self.wHistory = []  # velocity w
        
        self.pHistory = []  # velocity p
        self.qHistory = []  # velocity q
        self.rHistory = []  # velocity r

        self.xRefHistory = []  # reference position x_r
        self.yRefHistory = []  # reference position y_r
        self.zRefHistory = []  # reference position z_r
        
        self.psiRefHistory =[] # reference position psi_r

        self.timeHistory = []  # time
        

        # self.Force_history = []  # control force
        
        # Crete figure and axes handles
        j = 0
        figNum = 0
        figList = []
        for i in range(len(plotList)):
            j = j+1
            if j%3 == 0:
                figNum = figNum + 1
                figList.append("fig"+str(figNum))
                j = 0
                
        if j != 0:
            figNum = figNum+1
            figList.append("fig"+str(figNum))
            
        self.num_cols = 1    # Number of subplot columns
        
        
        
        for i in figList:
            if i == "fig1":
                if len(plotList) >=3:
                    self.fig1, self.ax1 = plt.subplots(3, self.num_cols, sharex=True)
                else:
                    # print(j)
                    self.fig1, self.ax1 = plt.subplots(j, self.num_cols, sharex=True)
                    
            if i == "fig2":
                if len(plotList) >=6:
                    self.fig2, self.ax2 = plt.subplots(3, self.num_cols, sharex=True)
                else:
                    # print(j)
                    self.fig2, self.ax2 = plt.subplots(j, self.num_cols, sharex=True)
                    
            if i == "fig3":
                if len(plotList) >=9:
                    self.fig3, self.ax3 = plt.subplots(3, self.num_cols, sharex=True)
                else:
                    # print(j)
                    self.fig3, self.ax3 = plt.subplots(j, self.num_cols, sharex=True)
                        
            if i == "fig4":
                if len(plotList) >=12:
                    self.fig4, self.ax4 = plt.subplots(3, self.num_cols, sharex=True)
                else:
                    # print(j)
                    self.fig4, self.ax4 = plt.subplots(j, self.num_cols, sharex=True)
        

        # create a handle for every subplot.
        self.handle = []
        j = -1
        
        plotListTemp = plotList.copy()
        handleCount = 0
        for i in figList:
            
            if i == "fig1":
                ax = self.ax1
                # print("fig1")
                
            elif i == "fig2":
                ax = self.ax2
                # print("fig2")
                
            elif i == "fig3":
                ax = self.ax3
                
            elif i == "fig4":
                ax = self.ax4
                
            axCount = 0
            
            for i in plotListTemp:
                axCount = axCount+1
                # print(i)
                # print(axCount)
                # print(" ")
         
                if i == "x":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='x(m)', title='X Position Data'))
                    self.handleDict[handleCount] = [self.xHistory, self.xRefHistory]
                elif i == "y":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='y(m)', title='Y Position Data'))
                    self.handleDict[handleCount] = [self.yHistory, self.yRefHistory]
                elif i =="z":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='z(m)', title='Z Position Data'))
                    self.handleDict[handleCount] = [self.zHistory, self.zRefHistory]
 
                elif i =="phi":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='phi(deg)', title='Phi Position Data'))
                    self.handleDict[handleCount] = [self.phiHistory]
                elif i =="theta":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='theta(deg)', title='Theta Position Data'))
                    self.handleDict[handleCount] = [self.thetaHistory]
                elif i =="psi":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='psi(deg)', title='Psi Position Data'))
                    self.handleDict[handleCount] = [self.psiHistory, self.psiRefHistory]
                    
                elif i =="u":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='u(m/s)', title='U Velocity Data'))
                    self.handleDict[handleCount] = [self.uHistory]
                elif i =="v":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='v(m/s)', title='V Velocity Data'))
                    self.handleDict[handleCount] = [self.vHistory]
                elif i =="w":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='w(m/s)', title='W Velocity Data'))
                    self.handleDict[handleCount] = [self.wHistory]
                
                elif i =="p":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='p(deg/s)', title='P Velocity Data'))
                    self.handleDict[handleCount] = [self.pHistory]
                elif i =="q":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='q(deg/s)', title='Q Velocity Data'))
                    self.handleDict[handleCount] = [self.qHistory]
                elif i =="r":
                    self.handle.append(myPlot(ax[axCount-1], xlabel='t(s)', ylabel='r(deg/s)', title='R Velocity Data'))
                    self.handleDict[handleCount] = [self.rHistory]
                    
                handleCount = handleCount + 1
                if axCount %3 == 0:
                    plotListTemp = plotListTemp[3:]
                    break
                

    def storeHistory(self, t, reference, states, ctrl):
        self.xHistory.append(states[0])  # x base position
        self.yHistory.append(states[1])  # y base position
        self.zHistory.append(states[2])  # z base position

        self.phiHistory.append(np.rad2deg(states[3]))  
        self.thetaHistory.append(np.rad2deg(states[4]))  
        self.psiHistory.append(np.rad2deg(states[5]))
        
        self.uHistory.append(states[6])  
        self.vHistory.append(states[7])
        self.wHistory.append(states[8])
        
        self.pHistory.append(np.rad2deg(states[9]))  
        self.qHistory.append(np.rad2deg(states[10]))
        self.rHistory.append(np.rad2deg(states[11]))
        
        self.xRefHistory.append(reference[0])
        self.yRefHistory.append(reference[1])
        self.zRefHistory.append(reference[2])
        
        self.psiRefHistory.append(np.rad2deg(reference[3]))
        
        self.timeHistory.append(t)  # time
        
        # self.Force_history.append(ctrl)  # force on the base
        
        


    def update(self, t, reference, states, ctrl):
        '''
            Add to the time and data histories, and update the plots.
        '''
        # update the time history of all plot variables
        self.storeHistory(t, reference, states, ctrl)

        # update the plots with associated histories
        for i in range(len(self.handleDict)):
            self.handle[i].update(self.timeHistory, self.handleDict[i])
            
            
    def staticPlot(self, t, reference, states, ctrl):
        for i in range(len(self.handleDict)):
            self.handle[i].update(self.timeHistory, self.handleDict[i])
        
            


class myPlot:
    ''' 
        Create each individual subplot.
    '''
    def __init__(self, ax,
                 xlabel='',
                 ylabel='',
                 title='',
                 legend=None):
        ''' 
            ax - This is a handle to the  axes of the figure
            xlable - Label of the x-axis
            ylable - Label of the y-axis
            title - Plot title
            legend - A tuple of strings that identify the data. 
                     EX: ("data1","data2", ... , "dataN")
        '''
        
        
        
        # print(ax)
        # print(xlabel)
        # print(ylabel)
        # print(title)

        
        self.legend = legend
        self.ax = ax                  # Axes handle
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'b']
        # A list of colors. The first color in the list corresponds
        # to the first line object, etc.
        # 'b' - blue, 'g' - green, 'r' - red, 'c' - cyan, 'm' - magenta
        # 'y' - yellow, 'k' - black
        self.line_styles = ['-', '-', '--', '-.', ':']
        # A list of line styles.  The first line style in the list
        # corresponds to the first line object.
        # '-' solid, '--' dashed, '-.' dash_dot, ':' dotted

        self.line = []

        # Configure the axes
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)
        self.ax.set_title(title)
        self.ax.grid(True)

        # Keeps track of initialization
        self.init = True   

    def update(self, time, data):
        ''' 
            Adds data to the plot.  
            time is a list, 
            data is a list of lists, each list corresponding to a line on the plot
        '''
        if self.init == True:  # Initialize the plot the first time routine is called
            for i in range(len(data)):
                # Instantiate line object and add it to the axes
                self.line.append(Line2D(time,
                                        data[i],
                                        color=self.colors[np.mod(i, len(self.colors) - 1)],
                                        ls=self.line_styles[np.mod(i, len(self.line_styles) - 1)],
                                        label=self.legend if self.legend != None else None))
                self.ax.add_line(self.line[i])
            self.init = False
            # add legend if one is specified
            if self.legend != None:
                plt.legend(handles=self.line)
        else: # Add new data to the plot
            # Updates the x and y data of each line.
            for i in range(len(self.line)):
                self.line[i].set_xdata(time)
                self.line[i].set_ydata(data[i])

        # Adjusts the axis to fit all of the data
        self.ax.relim()
        self.ax.autoscale()
           

