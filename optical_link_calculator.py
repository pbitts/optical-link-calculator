from numpy.core.fromnumeric import reshape
from math import erfc, pow, exp, log, degrees, radians, asinh, sqrt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class OpticalLink:
  ''' This class receives link, componentes and fiber parameters
      to calculate characteristics of the Optical Link:
      [Power per channel (dBm), SNR (dB), BER, GWDM, GNLI0].
      It has a method that returns a table containing the 
      calculations.'''

  pi = np.pi
  c = 2.99792458*pow(10,8)
  hplank = 6.623*pow(10,-34) #m².kg/s


  def __init__(self, link: dict = {}, components: dict = {}, fiber: dict = {}):
    self.link = link
    self.components = components
    self.fiber = fiber

  def get_n_loops(self):
    optical_link_length = self.link['optical_link_length']
    amplifier_distance_spacing = self.link['amplifier_distance_spacing']
    return optical_link_length/amplifier_distance_spacing 

  def get_gama(self):
    omega0 = 2*OpticalLink.pi*self.link['central_frequency']
    return  (omega0*self.fiber['n2'])/(OpticalLink.c*self.fiber['Aeff'])

  def get_beta2(self):
    return abs((-self.fiber['D']*self.get_lambda()**2)/(2*OpticalLink.pi*OpticalLink.c)*pow(10,-6))

  def get_lambda(self):
    return OpticalLink.c/self.link['central_frequency']

  def get_linear_gama(self):
    return self.fiber['attenuation']/4.343

  def get_effective_length(self):
    linear_gama = self.get_linear_gama()
    return (1 - exp((-2)*(linear_gama)*self.link['amplifier_distance_spacing']))/(2*linear_gama)

  def get_channel_bandwidth(self):
    return self.link['R_bit_rate']/(2*log(self.link['M'],2))

  def get_gwdm(self):
    return self.convert_dbm_to_linear(self.link['optical_launch_power_per_channel'])/self.get_channel_bandwidth()

  def get_gase(self):
    nf_linear = self.convert_to_linear(self.link['amplifier_noise_figure'])
    glinear = self.get_linear_amplifier_gain()
    gedfa_linear = self.convert_to_linear(self.link['GEDFA'])
    vo = self.link['central_frequency']
    return (nf_linear*glinear - 1)*OpticalLink.hplank*vo

  def get_gnli0(self):
    gama_2 = self.get_gama()**2
    gwdm_3 = self.get_gwdm()**3
    leff_2 = self.get_effective_length()**2
    beta2 = self.get_beta2()
    leff_a = self.link['leff_a']
    bch = self.get_channel_bandwidth()
    nch = self.link['n_channels']
    deltaf = self.link['channel_spacing']
    a = gama_2*gwdm_3*leff_2
    b = OpticalLink.pi*beta2*leff_a
    c = (OpticalLink.pi**2)/2
    sup = bch/deltaf
    d = beta2*leff_a*(bch**2)*pow(nch**2,sup)
    step1 = (8/27)*(a/b)
    step2 = asinh((OpticalLink.c*d))
    return step1*step2
  
  def get_osnr(self):
    gwdm = self.get_gwdm()
    gase = self.get_gase()
    n_spans = self.get_n_loops() 
    gnli0 = self.get_gnli0()
    return gwdm/(gase*n_spans + gnli0*n_spans)

  def get_osnr_db(self):
    return self.convert_to_db(self.get_osnr())

  def get_snr(self):
    bn = self.link['band_noise']
    rs = self.get_channel_bandwidth()
    osnr = self.get_osnr()
    return (bn/rs)*osnr

  def get_snr_db(self):
    return self.convert_to_db(self.get_snr())

  def get_ber(self):
    modulation_type = self.link['modulation_type']
    snrs = self.get_snr()
    bers = []
    if modulation_type == 'DP-QPSK':
      for snr in snrs:
        res = (1/2)*erfc(sqrt(  snr/2)  ) 
        bers.append(res)
      return  np.array(bers)
    elif modulation_type == 'DP-8QAM':
      for snr in snrs:
        res = (2/3)*erfc(sqrt((3/14)*snr))
        bers.append(res)
      return  np.array(bers)
    elif modulation_type == 'DP-16QAM':
      for snr in snrs:
        res = (3/8)*erfc(sqrt(snr/10))
        bers.append(res)
      return  np.array(bers)
    
  def get_ber_db(self):
    return self.convert_to_db(self.get_ber())
    
  def convert_to_linear(self, db_value):
    return 10**(db_value/10)

  def convert_dbm_to_linear(self, db_value):
    return (10**((db_value - 30)/10))

  def convert_to_db(self, linear_value):
    return 10*np.log10(linear_value)

  def convert_to_dbm(self, linear_value):
    return 10*np.log10(linear_value)

  def get_dataframe(self):
    power_per_channel = pd.DataFrame(self.link['optical_launch_power_per_channel'], columns=['Power/Ch dBm']) 
    osnr_db = pd.DataFrame(self.get_osnr_db(), columns=['OSNR dB'])
    snr_db = pd.DataFrame(self.get_snr_db(), columns=['SNR dB'])
    ber = pd.DataFrame(self.get_ber(), columns=['BER'])
    gwdm = pd.DataFrame(self.get_gwdm(),columns=['GWDM'])
    gnli0 = pd.DataFrame(self.get_gnli0(),columns=['GNLI0'])
    table = pd.concat([power_per_channel,osnr_db,snr_db,ber,gwdm,gnli0], axis=1)
    pd.set_option('display.expand_frame_repr', False)
    return table

  def get_penalties(self):
    pass

  def get_assintotic_effective_length(self):
    return (1)/(0.09*self.get_linear_gama())

  def get_linear_attenuator(self):
    return self.fiber['linear_attenuator']/4.343

  def get_linear_amplifier_gain(self):
    return exp(self.get_linear_gama()*self.link['amplifier_distance_spacing'] + self.get_linear_attenuator())

  def __str__(self, table_only=True):
  
    print(pd.DataFrame(self.get_dataframe()))
    return ('\n\n\n======================='
          f'\nNúmero de Loops: {self.get_n_loops()} voltas'
          f'\nGama: {self.get_gama()} W-¹/m'
          f'\nLambda : {self.get_lambda()} m'
          f'\nBeta2 absolute : {abs(self.get_beta2())} s²/m'
          f'\nLinear gama: {self.get_linear_gama()}' 
          f'\nComprimento Efetivo Leff: {self.get_effective_length()} m '
          '\n======================'
          '\nTransponder'
          f'\nChannel Bandwidth : {self.get_channel_bandwidth()} Hz'
          f'\nGDWM : {self.get_gwdm()} W/Hz'
          '\n======================'
          '\nAmplificador'
          f'\nGASE : {self.get_gase()} W/Hz'
          f'\nGNLI(0) : {self.get_gnli0()} W/Hz'
          f'\nOSNR : {self.get_osnr()}'
          f'\nOSNR dB : {self.get_osnr_db()}'
          f'\nSNR : {self.get_snr()}'
          f'\nSNR dB: {self.get_snr_db()}'
          f'\nBER : {self.get_ber()} '
          f'\nBER dB: {self.get_ber_db()} ')



