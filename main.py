import matplotlib.pyplot as plt
from IPython.display import display


from optical_link_calculator import OpticalLink
from sample_data import *


# Displaying table and plotting graphs

#####################################SUMITOMO

sumitomo_qpsk = OpticalLink(link_qpsk, components_qpsk, fiber_sumitomo)
sumitomo_8qam = OpticalLink(link_8qam, components_8qam, fiber_sumitomo)
sumitomo_16qam = OpticalLink(link_16qam, components_16qam, fiber_sumitomo)


table_sumitomo_qpsk = sumitomo_qpsk.get_dataframe()
table_sumitomo_8qam = sumitomo_8qam.get_dataframe()
table_sumitomo_16qam = sumitomo_16qam.get_dataframe()

print('-'*24 + 'Sumitomo QPSK')
display(table_sumitomo_qpsk)
print('-'*24 + 'Sumitomo 8QAM')
display(table_sumitomo_8qam)
print('-'*24 + 'Sumitomo 16QAM')
display(table_sumitomo_16qam)


power_per_channel_qpsk = sumitomo_qpsk.link['optical_launch_power_per_channel']
power_per_channel_8qam = sumitomo_8qam.link['optical_launch_power_per_channel']
power_per_channel_16qam = sumitomo_16qam.link['optical_launch_power_per_channel']


ber_qpsk = sumitomo_qpsk.get_ber()
ber_8qam = sumitomo_8qam.get_ber()
ber_16qam = sumitomo_16qam.get_ber()

plt.figure(figsize=(10, 10))
plt.plot(power_per_channel_qpsk, ber_qpsk)
plt.plot(power_per_channel_8qam, ber_8qam)
plt.plot(power_per_channel_16qam, ber_16qam)
plt.title('Fiber Sumitomo')
plt.xlabel('Launch Power/Channel dBm SUMITOMO')
plt.legend(['DP-QPSK','DP-8QAM','DP-16QAM'])
plt.ylabel('BER')
plt.yscale('log')
plt.show()


########################################SMF-28

smf28_qpsk = OpticalLink(link_qpsk, components_qpsk, fiber_SMF28)
smf28_8qam = OpticalLink(link_8qam, components_8qam, fiber_SMF28)
smf28_16qam = OpticalLink(link_16qam, components_16qam, fiber_SMF28)

table_smf28_qpsk = smf28_qpsk.get_dataframe()
table_smf28_8qam = smf28_8qam.get_dataframe()
table_smf28_16qam = smf28_16qam.get_dataframe()

print('-'*24 + 'SMF28 QPSK')
display(table_smf28_qpsk)
print('-'*24 + 'SMF28 8QAM')
display(table_smf28_8qam)
print('-'*24 + 'SMF28 16QAM')
display(table_smf28_16qam)


power_per_channel_qpsk = smf28_qpsk.link['optical_launch_power_per_channel']
power_per_channel_8qam = smf28_8qam.link['optical_launch_power_per_channel']
power_per_channel_16qam = smf28_16qam.link['optical_launch_power_per_channel']


ber_qpsk = smf28_qpsk.get_ber()
ber_8qam = smf28_8qam.get_ber()
ber_16qam = smf28_16qam.get_ber()

plt.figure(figsize=(10, 10))
plt.plot(power_per_channel_qpsk, ber_qpsk)
plt.plot(power_per_channel_8qam, ber_8qam)
plt.plot(power_per_channel_16qam, ber_16qam)
plt.title('Fiber SMF28')
plt.xlabel('Launch Power/Channel dBm')
plt.legend(['DP-QPSK','DP-8QAM','DP-16QAM'])
plt.ylabel('BER')
plt.yscale('log')
plt.show()
