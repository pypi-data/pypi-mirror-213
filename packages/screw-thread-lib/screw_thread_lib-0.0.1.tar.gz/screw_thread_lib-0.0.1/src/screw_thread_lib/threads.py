from math import pi,sqrt

class Assembly:
    def __init__(self, thread_data, UTSs=None, UTSn=None):
        '''
        Define Assembly object
        
        Arguments:
        thread_data --- a dict incuding the following entries
            n     --- number of threads per inch
            dbsc  --- major diameter, external thread, basic value
            dmin  --- major diameter, external thread, minimum value
            d1bsc --- minor diameter, external thread, basic value
            d2bsc --- pitch diameter, external thread, basic value
            d2min --- pitch diameter, external thread, minimum value
            D1bsc --- minor diameter, internal thread, basic value
            D1max --- minor diameter, internal thread, maximum value
            D2bsc --- pitch diameter, internal thread, basic value
            D2max --- pitch diameter, internal thread, maximum value
        UTSs --- ultimate tensile strength of externally threaded part
        UTSn --- ultimate tensile strength of internally threaded part
        '''
        self.n     = thread_data['n']       
        self.dbsc  = thread_data['dbsc']    
        self.dmin  = thread_data.get('dmin',None)
        self.d1bsc = thread_data.get('d1bsc',None)   
        self.d2bsc = thread_data.get('d2bsc',None)   
        self.d2min = thread_data.get('d2min',None)   
        self.D1bsc = thread_data.get('D1bsc',None)   
        self.D1max = thread_data.get('D1max',None)   
        self.D2bsc = thread_data.get('D2bsc',None)   
        self.D2max = thread_data.get('D2max',None)   
        self.UTSs  = UTSs                   
        self.UTSn  = UTSn                   
        
    @classmethod
    def from_ASME_B11_UN_2A2B(cls, thread_designation, UTSs=None, UTSn=None):
        '''
        Define Assembly object based on thread data from ASME B1.1
        '''
        from screw_thread_lib.data import ASME_B11_UN_2A2B_dict
        thread_data = ASME_B11_UN_2A2B_dict[thread_designation]
        c = cls(thread_data, UTSs, UTSn)
        c.thread_designation  = thread_designation
        return c
        
    @property
    def p(self):
        return 1/self.n
    
    @property
    def H(self):
        return sqrt(3) / (2 * self.n)
    
    def Absc(self):
        '''
        Cross-sectional area based on dbsc
        '''
        return pi/4*self.dbsc**2
        
    def As_FEDSTD_1a(self):
        '''
        Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1a)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        As = pi * (self.d2bsc / 2 - 3 * self.H / 16) ** 2
        return As

    def As_FEDSTD_1b(self):
        '''
        Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1b)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        As = pi / 4 * (self.dbsc - (9 * sqrt(3)) / (16 * self.n)) ** 2
        return As
        
    def As_MH_2b(self, override_limit=False):
        '''
        Tensile stress area based on Machinery's Handbook, 31st Edition Eq. (2b) on Page 1668

        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        if (self.UTSs <= 180000) and (not override_limit):
            raise ValueError('As_MH_2b is only for steels of over 180,000 psi ultimate tensile strength')
        As = pi * ( (self.d2min / 2) - (3 * sqrt(3)) / (32 * self.n) ) ** 2
        return As
     
     
    def ASn_min_FEDSTD_2a(self, LE=1):
        '''
        Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (2a)
            (minimum material external and internal threads)
        
        Arguments:
        LE --- length of engagment (default = 1)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        ASn = pi * self.n * LE * self.dmin * ((1 / (2 * self.n)) + ((1 / sqrt(3)) * (self.dmin - self.D2max)))
        return ASn


    def ASn_FEDSTD_3(self, LE=1, override_limit=False):
        '''
        Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (3)
            (simplified: for d equal to or greater than 0.250 inch)
        
        Arguments:
        LE --- length of engagment (default = 1)
        override_limit --- option to ignore limit on diameter (default = False)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        if (self.d < 0.250) and (not override_limit):
            raise ValueError('ASn_FEDSTD_3 should not be used with d less than 0.250 inch')
        ASn = pi * self.D2bsc * (3 / 4) * LE
        return ASn     
     
     
    def ASs_min_FEDSTD_4a(self, LE=1):
        '''
        Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (4a)
            (minimum material external and internal threads)
        
        Arguments:
        LE --- length of engagment (default = 1)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        ASs = pi * self.n * LE * self.D1max * ((1 / (2 * self.n)) + ((1 / sqrt(3)) * (self.d2min - self.D1max)))
        return ASs

   
    def ASs_FEDSTD_5(self, LE=1):
        '''
        Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (5)
            (simplified)
        
        Arguments:
        LE --- length of engagment (default = 1)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        ASs = pi * self.d2bsc * (5 / 8) * LE
        return ASs 

        
    def ASs_max_FEDSTD_6b(self, LE=1):
        '''
        Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (6b)
            (basic size external and internal threads)
        
        Arguments:
        LE --- length of engagment (default = 1)
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        ASs = pi * self.D1bsc * 0.75 * LE
        return ASs


    def LEr_FEDSTD_13(self, As_eqn='1a'):
        '''
        Length of engagemnet required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (13)
            (based upon combined shear failure of external and internal threads)
        
        Arguments:
        As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
        
        Note: numbers with decmials replaced with equivalent mathematcal expressions.
        '''
        if As_eqn == '1a':
            As = self.As_FEDSTD_1a()
        elif As_eqn == '1b':
            As = self.As_FEDSTD_1b()
        else:
            raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')
        LEr = (4 * As) / (pi * self.d2bsc)
        return LEr


    def LEr_FEDSTD_14(self, As_eqn='1a', ASs_eqn='4a'):
        '''
        Length of engagemnet required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (14)
            (based upon shear of external thread)
        
        Arguments:
        As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
        ASs_eqn --- denotes which equation to use for As ('4a' or '4b', default = '4a')
        '''
        if As_eqn == '1a':
            As = self.As_FEDSTD_1a()
        elif As_eqn == '1b':
            As = self.As_FEDSTD_1b()
        else:
            raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')
            
        if ASs_eqn == '4a':
            ASs = self.ASs_min_FEDSTD_4a()
        elif ASs_eqn == '4b':
            raise NotImplementedError(f'ASs_FEDSTD_4b is not yet implemented')
        else:
            raise ValueError(f'Invalid value for ASs_eqn: {ASs_eqn} (need ''4a'' or ''4b'')')

        LEr = 2 * As / ASs
        return LEr
        
    def LEr_FEDSTD_15(self, As_eqn='1a'):
        '''
        Length of engagemnet required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (15)
            (based upon shear of external thread)
        
        Arguments:
        As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
        '''
        if As_eqn == '1a':
            As = self.As_FEDSTD_1a()
        elif As_eqn == '1b':
            As = self.As_FEDSTD_1b()
        else:
            raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')
            
        LEr = 2 * As / self.ASs_max_FEDSTD_6b()
        return LEr        
        
    def LEr_FEDSTD_16(self, As_eqn='1a', ASn_eqn='2a'):
        '''
        Length of engagemnet required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (15)
            (based upon shear of external thread)
        
        Arguments:
        As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
        ASn_eqn --- denotes which equation to use for ASn ('2a' or '2b', default = '2a')
        '''
        if As_eqn == '1a':
            As = self.As_FEDSTD_1a()
        elif As_eqn == '1b':
            As = self.As_FEDSTD_1b()
        else:
            raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')
        
        if ASn_eqn == '2a':
            ASn = self.ASn_min_FEDSTD_2a()
        elif ASn_eqn == '2b':
            raise NotImplementedError(f'ASn_FEDSTD_2a is not yet implemented')
        else:
            raise ValueError(f'Invalid value for As_eqn: {ASn_eqn} (need ''2a'' or ''2b'')')
               
        R2 = self.UTSn / self.UTSs
        LEr = (2 * As / ASn) / R2
        return LEr  
        

    def LEr_FEDSTD(self, As_eqn='1a', ASs_eqn='4a', ASn_eqn='2a', combined_failure_range=0.05):
        '''
        Length of engagemnet required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (13), (15), and (16)
        
        Arguments:
        As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
        ASn_eqn --- denotes which equation to use for ASn ('2a' or '2b', default = '2a')
        ASs_eqn --- denotes which equation to use for ASn ('4a' or '4b', default = '4a')
        combined_failure_range --- parameter that defines the limit of applicibility of the combined failure mode (default = 0.05)s
        '''
        R1 = self.ASs_max_FEDSTD_6b()/self.ASn_min_FEDSTD_2a() # @todo - code in options here see formulat (8)
        R2 = self.UTSn / self.UTSs
        if R1/R2 < (1-combined_failure_range):
            # External thread failure, Formula (15)
            LEr = self.LEr_FEDSTD_14(As_eqn, ASs_eqn)
        else:
            # Internal thread failure or combined failure, Formula (13) or (16)
            LEr_13 = self.LEr_FEDSTD_13(As_eqn)
            LEr_16 = self.LEr_FEDSTD_16(As_eqn, ASn_eqn)
            LEr = max(LEr_13,LEr_16)
    
        return LEr