import numpy as np 


# This sample data file contains dic of parameters
# for Fibers and modulations to be used for analysis
# and comparation.
# Import this file on your main file.

tera =  pow(10,12)
giga = pow(10,9)
kilo = pow(10,3)
mili = pow(10,-3)
micro = pow(10,-6)



################################### Optical Fiber parameters ###################################
### Sumitomo

fiber_sumitomo = {
                'Aeff': 150*micro, #m^2
                'attenuation' : 0.15*mili, #dB/m
                'D' : 20.9, #ps/km.nm
                'slope' : 0.06, # ps/km.nm^2
                'PMD' : 0.02, #ps/sqrt(km)
                'n2' : 2.59992795*pow(10,-14),
                'linear_attenuator': 0, #dB
                }
### SMF28
fiber_SMF28 = {
              'Aeff': 80*micro, #m^2
              'attenuation' : 0.2*mili, #dB/m
              'D' : 16.75, #ps/km.nm
              'slope' : 0.075, # ps/km.nm^2
              'PMD' : 0.05, #ps/sqrt(km),
              'n2' : 2.59992795*pow(10,-14),
               'linear_attenuator': 0, #dB
              }




################################### Modulation DP-QPSK ###################################
#### Link parameters
link_qpsk = {
      'ideal_ber' : 1*mili,
      'optical_launch_power_per_channel' : np.arange(-6,10,0.5), #dbm
      'n_channels' : 20,
      'optical_link_length' : 8340000, #meters
      'channel_rate' : 100*giga, #bps
      'amplifier_noise_figure' : 9, #dB
      'amplifier_distance_spacing' : 60*kilo, #m
      'channel_spacing' : 100*giga, #Hz
      'central_frequency' :  193.41*tera, #Hz
      'R_bit_rate' : 56*giga, #baud/S
      'modulation_type' : 'DP-QPSK',
      'M' : 2, #QPSK bit per symbol
      'GEDFA' : 9, #dB
      'leff_a' : 321.7*kilo,
      'band_noise' : 12.5*giga #Hz
      }

#### Components parameters
components_qpsk = {
            'launch_booster_power_dB' : 16, #dBm
            'mux_attenuation' : 8, #dB
            'demux_attenuation' : 8, #dB
            'potencia_mw_lancamento_booster' : 39.8, #mW
            }





################################### Modulation DP-8QAM ###################################
### Link parameters
link_8qam = {
      'ideal_ber' : 1*mili,
      'optical_launch_power_per_channel' : np.arange(-10,11,1), #dbm
      'n_channels' : 20,
      'optical_link_length' : 8340000, #meters
      'channel_rate' : 100*giga, #bps
      'amplifier_noise_figure' : 9, #dB
      'amplifier_distance_spacing' : 60*kilo, #m
      'channel_spacing' : 100*giga, #Hz
      'central_frequency' :  193.41*tera, #Hz
      'R_bit_rate' : 56*giga, #baud/S
      'modulation_type' : 'DP-8QAM',
      'M' : 2, #QPSK bit per symbol
      'GEDFA' : 9, #dB
      'leff_a' : 321.7*kilo,
      'band_noise' : 12.5*giga #Hz
      }

### Components parameters
components_8qam = {
            'launch_booster_power_dB' : 16, #dBm
            'mux_attenuation' : 8, #dB
            'demux_attenuation' : 8, #dB
            'potencia_mw_lancamento_booster' : 39.8, #mW
            }






################################### Modulation DP-16QAM ###################################
#### Link parameters
link_16qam = {
      'ideal_ber' : 1*mili,
      'optical_launch_power_per_channel' : np.arange(-10,11,1), #dbm
      'n_channels' : 20,
      'optical_link_length' : 8340000, #meters
      'channel_rate' : 100*giga, #bps
      'amplifier_noise_figure' : 9, #dB
      'amplifier_distance_spacing' : 60*kilo, #m
      'channel_spacing' : 100*giga, #Hz
      'central_frequency' :  193.41*tera, #Hz
      'R_bit_rate' : 56*giga, #baud/S
      'modulation_type' : 'DP-16QAM',
      'M' : 2, #QPSK bit per symbol
      'GEDFA' : 9, #dB
      'leff_a' : 321.7*kilo,
      'band_noise' : 12.5*giga #Hz
      }

### Components parameters
components_16qam = {
            'launch_booster_power_dB' : 16, #dBm
            'mux_attenuation' : 8, #dB
            'demux_attenuation' : 8, #dB
            'potencia_mw_lancamento_booster' : 39.8, #mW
            }







