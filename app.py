import os
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from optical_link_calculator import OpticalLink

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # --- Coletar parâmetros do formulário ---
    # Fiber parameters
    fiber_type =  request.form['fiber_type']
    fiber = {
        'Aeff': float(request.form['Aeff']),
        'attenuation': float(request.form['attenuation']),
        'D': float(request.form['D']),
        'slope': float(request.form['slope']),
        'PMD': float(request.form['PMD']),
        'n2': float(request.form['n2']),
        'linear_attenuator': float(request.form['linear_attenuator']),
    }

    # Link parameters
    power_start = float(request.form['power_start'])
    power_stop = float(request.form['power_stop'])
    power_step = float(request.form['power_step'])

    power_range = np.arange(power_start, power_stop + power_step, power_step)

    modulation_type = request.form['modulation_type']
    link = {
        'ideal_ber': float(request.form['ideal_ber']),
        'optical_launch_power_per_channel': power_range,
        'n_channels': int(request.form['n_channels']),
        'optical_link_length': float(request.form['optical_link_length']),
        'channel_rate': float(request.form['channel_rate']),
        'amplifier_noise_figure': float(request.form['amplifier_noise_figure']),
        'amplifier_distance_spacing': float(request.form['amplifier_distance_spacing']),
        'channel_spacing': float(request.form['channel_spacing']),
        'central_frequency': float(request.form['central_frequency']),
        'R_bit_rate': float(request.form['R_bit_rate']),
        'M': int(request.form['M']),
        'modulation_type': request.form['modulation_type'],
        'GEDFA': float(request.form['GEDFA']),
        'leff_a': float(request.form['leff_a']),
        'band_noise': float(request.form['band_noise'])
    }

    # Component parameters
    components = {
        'launch_booster_power_dB': float(request.form['launch_booster_power_dB']),
        'mux_attenuation': float(request.form['mux_attenuation']),
        'demux_attenuation': float(request.form['demux_attenuation']),
        'potencia_mw_lancamento_booster': float(request.form['potencia_mw_lancamento_booster'])
    }

    # --- Realizar simulação ---
    optical_link_simulation = OpticalLink(link=link, components=components, fiber=fiber)
    df = optical_link_simulation.get_dataframe()

    power_per_channel = optical_link_simulation.link['optical_launch_power_per_channel']
    ber = optical_link_simulation.get_ber()

       # --- Gerar gráfico ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(power_per_channel, ber, marker='o')
    ax.set_title(f'BER vs Launch Power - {fiber_type}')
    ax.set_xlabel('Launch Power per Channel (dBm)')
    ax.set_ylabel('Bit Error Rate (BER)')
    ax.set_yscale('log')
    ax.grid(True)
    plot_path = os.path.join('static', 'ber_plot.png')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()

    # --- Exibir resultado ---
    return render_template('result.html', table=df.to_html(classes='table table-striped', index=False), plot_url=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
