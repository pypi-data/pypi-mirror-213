from inspect import signature
import logging
import numpy as np
import os
import pandas as pd
import pylab as plt
import sys

try:
    from .interface import Interface
except:
    Interface = object

class DAT(Interface):
    """Read and write dat files
    
    The DAT class contains functions for reading dat files to
    a pandas dataframe object where various calculations can be
    performed on it and then writing it back out again.
    """
    
    '''
    Constructor
    '''
    def __init__(self, datfile=None):
        ###start a log file
        self.logger = logging.getLogger('readwrite.DAT')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s',"[%Y-%m-%d %H:%M:%S]")
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        if len(self.logger.handlers) == 0:
            self.logger.addHandler(streamhandler)
            self.logger.debug('Starting a new readwrite.DAT job')        
        self.type = 'dat'

        

        self.hashdata = pd.DataFrame.from_dict( {'Q': [], 'I': [], 'E': []}, orient='columns').set_index('Q')
        self.header=''
        self.footer=''

        #The units dictionary allows on the fly output in different unit schemes
        self.units={}
        self.add_unit('linear', lambda x: x, r'Q ($\AA^{-1}$)')
        self.add_unit('^2', lambda x: np.power(x,2), r'Q ($\AA^{-1}$)$^{2}$')
        self.add_unit('^3', lambda x: np.power(x,3), r'Q ($\AA^{-1}$)$^{3}$')
        self.add_unit('^4', lambda x: np.power(x,4), r'Q ($\AA^{-1}$)$^{4}$')
        self.add_unit('ln', lambda x: np.log(x), r'ln[I(q)]')
        self.add_unit('q*I(q)', lambda x,y: x*y, r'Q x I(q)')
        self.add_unit('q^2*I(q)', lambda x,y: np.power(x,2)*y, r'Q$^{2}$ x I(q)')
        self.add_unit('q^3*I(q)', lambda x,y: np.power(x,3)*y, r'Q$^{3}$ x I(q)')
        self.add_unit('q^4*I(q)', lambda x,y: np.power(x,4)*y, r'Q$^{4}$ x I(q)')

        if self.set_datfile(datfile):
            self.parse_file()

    def add_unit(self, name, func, unit):
        '''Add a new unit for outputting data columns 

        Units are saved in a dictionary with a descriptive name linking to a
        lambda function that can be applied directly to data arrays to change
        the units and a formatted text string indicating the units for plotting
        i.e. add_unit(name='X^2', func=lambda x: x**2, unit=r'Q ($\AA^{-1}$)^{2}')
        '''
        self.logger.debug('The add_unit method was called')

        if name in self.units.keys():
            self.logger.error(f'Units {name} already exists in the units definitions')
            return False
        if not callable(func):
            self.logger.error('the func argument must be a callable function, see function help')
            return False
        self.units[name] = (func,unit)
        self.logger.debug(f'Unit {name} added to output unit options')
        return True

    def set_datfile(self, datfile):
        '''Set the datfile'''
        self.logger.debug('The set_datfile method was called')
        if datfile == None:
            self.logger.info('No dat file provided, instantiating with empty data array')
            self.datfile = None
            return False
        elif os.path.isfile(datfile) and str(datfile)[-4:] == '.dat':
            self.datfile = str(datfile)
            self.logger.info(f'{datfile} lookks like a valid datfile')
            return True
        else:
            self.datfile = None
            self.logger.error(f'{datfile} either does not exist or is not of type ".dat"')
            return False
            
    def parse_file(self):
        '''Parse the dat file to a Pandas dataframe'''
        self.logger.debug('The parse_file method was called')
        self.logger.info(f'Reading and parsing dat file: {self.datfile}')

        with open(self.datfile, 'r') as f:
            datdata = f.readlines()
        '''
        We're going to check through the data for header and footer
        records, we start by assuming there is no data hence the
        start of the data is the end of the file (i.e. no data) and
        the end of the data is the start of the file.
        '''
        data_start = len(datdata)-1
        data_end = 0
        
        #Check for header
        for i,l in enumerate(datdata):
            try:
                [float(x) for x in l.split()]
                data_start=i
                break
            except:
                pass
        if data_start>0:
            self.header=''.join(datdata[:data_start])
            
        #Check for footer
        for i,l in reversed(list(enumerate(datdata))):
            try:
                [float(x) for x in l.split()]
                data_end=i
                break
            except:
                pass
        if data_end>0:
            self.footer=''.join(datdata[data_end+1:])

        #Parse the data
        if data_end > data_start:
            self.hashdata = pd.read_table(self.datfile,
                                          skiprows=data_start,
                                          engine='python',
                                          skipfooter=len(datdata)-data_end,
                                          names=['Q','I','E'],
                                          index_col=0
            )
        self.logger.info(f'Parsed dat file with {self.hashdata.index.size} points.')
                
            
    def return_ie_data(self, q):
        '''Given a valid Q value will return I and E as a tuple'''
        self.logger.debug('the returnIEData method was called')
        if q in self.hashdata.index:
            self.logger.debug(f'Q value {q} was found in the dat file')
            return tuple(self.hashdata.xs(q))
        else:
            self.logger.debug(f'Q value {q} was not found in the dat file')
            return False

    def return_data_column(self, column='I', qmin=None, qmax=None, unit=None):
        '''Given column "Q", "I" or "E" will return data as a numpy array
        
        The optional argument unit refers to the entries in the units dictionary
        that stores lambda functions that allows the specified data column to be
        output with altered units i.e choosing column='I' and unit='^2' will output
        an array containing I^2 rather than I. The exception is for units that
        refer to more than one data column i.e. 'q^2*I(q)' that might be used for
        making a Kratky plot for example. In this case the requested unit function 
        will be tested for number of arguments and if it is 2 then Q will be presumed
        as the x term (the first argument in the lambda) and I the y term (the second
        argument in the lambda) regardless of what was specified in the column term

        '''
        self.logger.debug('The return_data_column method was called')        
        #Check that qmin and qmax are of the right type
        if qmin is not None and not isinstance(qmin, (float, int)):
            self.logger.error('qmin variable in ReturnDataColumn method should be a float, int or None')
            qmin=None
        if qmax is not None and not isinstance(qmax, (float, int)):
            self.logger.error('qmax variable in ReturnDataColumn method should be a float, int or None')
            qmax=None
            
        #If qmin is bigger than qmax just switch them
        if isinstance(qmin, (float,int)) and isinstance(qmax, (float,int)):
            if qmin > qmax:
                self.logger.error('qmin was larger than qmax in ReturnDataColumn method, will reverse')
                qmin,qmax = sorted((qmin,qmax))

        if unit:
            if unit in self.units.keys():
                if len(signature(self.units[unit][0]).parameters) > 2:
                    self.logger.error('Unit functions should not contain more than 2 arguments')
                    return False
                elif len(signature(self.units[unit][0]).parameters) == 2:
                    self.logger.info('The requested unit function has 2 arguments, will assume these refer to Q,I')
                    return self.units[unit][0](self.hashdata.loc[qmin:qmax].index.values,self.hashdata.loc[qmin:qmax]['I'].values)
                elif str(column).upper() in ['I', 'E']:
                    return self.units[unit][0](self.hashdata.loc[qmin:qmax][column].values)
                elif str(column).upper() == 'Q':
                    return self.units[unit][0](self.hashdata.loc[qmin:qmax].index.values)
                else:
                    self.logger.error('ReturnDataColumn function requires you specify either Q, I or E')
                    return False
            else:
                self.logger.error(f'Unit {unit} is not in the units definition')
                return False
        else:
            if str(column).upper() in ['I', 'E']:
                return self.hashdata.loc[qmin:qmax][column].values
            elif str(column).upper() == 'Q':
                return self.hashdata.loc[qmin:qmax].index.values
            else:
                self.logger.error('ReturnDataColumn function requires you specify either Q, I or E')
                return False
        
    def return_file(self):
        self.logger.debug('The return_file method was called')        
        self.logger.info('Writing out a formatted DAT file')
        string_list = [self.header]
        string_list.append("%-15s %-13s %-13s\n" % ("Q(A-1)","I(au)","Error"))
        for q in self.return_data_column('Q'):
            if q > 0:
                i,e = self.return_ie_data(q)
                string_list.append('{:<15.7E} {:<13.6E} {:<13.6E}\n'.format(q,i,e))
        string_list.append(self.footer)
        return ''.join(string_list)


    def input_dataframe(self, input_dataframe):
        self.logger.debug('The input_dataframe method was called')        
        self.logger.info('Reading in DAT data as a dictionary')
        if isinstance(input_dataframe, pandas.core.frame.DataFrame):
            self.hashdata = input_dataframe

    def return_dataframe(self):
        self.logger.debug('The return_dataframe method was called')        
        self.logger.info('Returning DAT data as a dataframe')
        return self.hashdata

    def plot(self,
             log_y=True,
             log_x=False,
             linewidth=2,
             height=8,
             width=15,
             fontsize=16,
             title=None,
             x_unit = 'linear',
             y_unit = 'linear',
             qrange_min=None,
             qrange_max=None,
             yrange_min=None,
             yrange_max=None,
             filename=None,
             label='',
             show=True
             ):
        self.logger.debug('The plot method was called')        
        '''Use pyplt to graph the dat data'''
        if x_unit not in self.units.keys():
            self.logger.error('x_unit is not recognised, will use linear')
            x_unit = 'linear'
        x_label = self.units[x_unit][1]
        if y_unit not in self.units.keys():
            self.logger.error('y_unit is not recognised, will use linear')
            y_unit = 'linear'
        y_label = self.units[y_unit][1]
        
        if not show:
            plt.ioff()
        plt.rc('xtick',labelsize=fontsize-2)
        plt.rc('ytick',labelsize=fontsize-2)
        fig, ax = plt.subplots()
        fig.set_figwidth(width)
        fig.set_figheight(height)
        if log_y:
            plt.yscale('log')
        if log_x:
            plt.xscale('log')
        if title:
            ax.set_title(f'{title}', fontsize=fontsize)
        plt.rc('lines', linewidth=linewidth)
        ax.set_ylabel(y_label, fontsize=fontsize)
        ax.set_xlabel(x_label, fontsize=fontsize)
        q=self.return_data_column(column='Q', qmin=qrange_min, qmax=qrange_max, unit=x_unit).tolist()
        i=self.return_data_column(column='I', qmin=qrange_min, qmax=qrange_max, unit=y_unit).tolist()
        plt.plot(q,i)
        y_bottom,y_top = plt.ylim()
        self.logger.debug(f'autoscale limits are {y_top}x{y_bottom}')
        if yrange_min == None:
            yrange_min=y_bottom
        if yrange_max == None:
            yrange_max=y_top
        plt.ylim(bottom=yrange_min,top=yrange_max)
        self.logger.debug(f'New Y scale limits are: {yrange_min}x{yrange_max}')

        plt.title(f'{label}')
        if filename:
            plt.savefig(f'{filename}')
        if not show:
            plt.close(fig)
        else:
            plt.show()


if __name__ == '__main__':
    test_file = '/Users/nathan/Documents/PYTHON/test_data/bsa_dimer.dat'
    job=DAT(test_file)
    import code; code.interact(local=locals())
                    
