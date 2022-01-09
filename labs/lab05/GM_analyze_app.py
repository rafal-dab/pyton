import numpy as np
from math import factorial
from bokeh.io import curdoc # żeby wykresy wysyłać do apki
from bokeh.layouts import layout
from bokeh.models import Legend, Slider
from bokeh.plotting import figure, show, column, row

def f_poisson(x, scal, mi):
    tmp = np.empty_like(x)
    for i in range(x.size):
        tmp[i] = scal * mi**int(x[i]) * np.exp(-mi) / factorial(int(x[i]))
    return tmp
    
def f_gauss(x, scal, mi, sigma):
    return scal / (sigma*np.sqrt(2*np.pi)) * np.exp(-0.5*((x-mi)/sigma)**2)

def chi2(O, E):
    return np.sum((O-E)**2/E)

fname = 'KIE_bieg_wlasny.txt'
# szerokość binów:
binw = 1
# flaga mówiąca, czy dane wejściowe są dyskretne (tylko liczby całkowite), czy rzeczywiste:
is_int_input = True
A = np.loadtxt(fname)

def generate_data():
    global binw, is_int_input, A, min_x, max_x, scal, mi, sigma, u_mi
    global bins, max_binw, max_x_plot, lbons, hist, litems
    global src_data, src_gauss, src_poisson, src_poisson_step, chi2_gauss, ndf_gauss, chi2_poisson, ndf_poisson
    min_x = np.min(A)
    max_x = np.max(A)
    scal = A.size * binw
    mi = np.mean(A)
    sigma = np.std(A)
    u_mi = np.sqrt(mi/A.size)
    #print(f"{A.size = }, {min_x = }, {max_x = }\n{mi = } +/- {u_mi}, {sigma = }")
    # krawędzie binów do np.histogram():
    bins = np.arange(min_x, max_x+1, binw)
    # W np.arange() są wartości < max_x+1 (bez max_x+1)
    # Do histogramu trzeba dodać jeszcze prawą krawędź ostatniego binu,
    # bo ostatni przedział w np.histogram() jest prawostronnie domknięty.
    # Nie trzeba dodawać, jeśli dane wejściowe lub szerokość binów nie są całkowite.
    if is_int_input:
        max_binw = max_x - min_x + 1
        if bins[-1] <= max_x:
            bins = np.append(bins, bins[-1] + binw)
    else:
        max_binw = max_x - min_x
        if bins[-1] < max_x:
            bins = np.append(bins, bins[-1] + binw)
    max_x_plot = bins[-1]

    lbins = bins.size #int((max_x-min_x) / binw)
    hist, histbins = np.histogram(A, bins)
    src_data = {'top': hist, 'bottom': np.zeros_like(hist), 'left': bins[:-1], 'right': bins[1:]}

    # Punkty x, dla których będzie obliczany test chi2 są środkami binów, jeżeli dane są ciągłe (is_int_input == False).
    # Jeżeli dane są całkowite, to punkty x są lewymi krawędziami binów (dla binw == 1)
    # lub środkami binów zaokrąglonymi w dół do liczb całkowitych (dla binw > 1)
    if is_int_input:
        if binw == 1:
            x_chi2 = bins[:-1]
        else:
            x_chi2 = np.floor(bins[:-1] + binw/2)
    else:
        x_chi2 = bins[:-1] + binw/2

    # Dopasowanie Gaussa rysujemy w każdym przypadku dla każdego punktu x
    x = np.linspace(min_x, max_x_plot, 200)
    y_gauss = f_gauss(x, scal, mi, sigma)
    src_gauss = {'x': x, 'y': y_gauss}
    chi2_gauss = chi2(hist, f_gauss(x_chi2, scal, mi, sigma))
    ndf_gauss = lbins - 3 - 1

    # Dopasowanie Poissona rysujemy schodkami dla dyskretnych wartości x_chi2
    # tylko jeżeli mamy dane całkowite
    if is_int_input:
        y_poisson = f_poisson(x_chi2, scal, mi)
        src_poisson = {'x': x_chi2, 'y': y_poisson}
        # żeby schodki dobrze się narysowały, trzeba dodać jeszcze raz ostatnią wartość do tablicy wartości y
        y_poisson = np.append(y_poisson, y_poisson[-1])
        src_poisson_step = {'x': bins, 'y': y_poisson}
        #print(y_poisson.size)
        chi2_poisson = chi2(hist, f_poisson(x_chi2, scal, mi))
        ndf_poisson = lbins - 2 - 1

def callback(attr, old, new):
    global binw
    binw = binw_slider.value
    generate_data()
    q_data.data_source.data = src_data
    l_gauss.data_source.data = src_gauss
    if is_int_input:
        l_poisson.data_source.data = src_poisson
        l_poisson_step.data_source.data = src_poisson_step
    
    litems=[ # lista wpisów w legendzie
        (f"Dane z pliku \"{fname}\"", [q_data]),
        (f"liczba wszystkich wyników: {A.size}, minimum: {min_x}, maksimum: {max_x}", []),
        (("średnia: %.1f ± %.1f; odchylenie std: %.1f" % (mi, u_mi, sigma)), []),
        (("Rozkład Gaussa: chi2 / NDF = %.1f / %d" % (chi2_gauss, ndf_gauss)), [l_gauss])
    ]
    if is_int_input:
        litems.append(
            (("Rozkład Poissona: chi2 / NDF = %.1f / %d" % (chi2_poisson, ndf_poisson)), [l_poisson_step])
        )
    legend.items = litems

generate_data()

binw_slider = Slider(start=1, end=max_binw, step=1, value=binw, title='Szerokość przedziałów', width=200)
binw_slider.on_change('value', callback)

fig = figure(x_range=(min_x, max_x_plot), \
            x_axis_label = 'CPM', \
            y_axis_label = 'Liczba wyników', \
            height = 600, \
            width = 800)
fig.toolbar.logo = None
fig.toolbar.autohide = True
fig.grid.grid_line_dash = (6, 5)

q_data = fig.quad(source = src_data, fill_color="skyblue", line_color="white")
l_gauss = fig.line(source = src_gauss, line_width=2, line_color="brown")
# Dopasowanie Poissona rysujemy schodkami dla dyskretnych wartości x_chi2
# tylko jeżeli mamy dane całkowite
if is_int_input:
    l_poisson = fig.circle(source = src_poisson, fill_color="gold", line_color="gold")
    l_poisson_step = fig.step(source = src_poisson_step, mode='after', line_width=2, line_color="gold")

litems=[ # lista wpisów w legendzie
    (f"Dane z pliku \"{fname}\"", [q_data]),
    (f"liczba wszystkich wyników: {A.size}, minimum: {min_x}, maksimum: {max_x}", []),
    (("średnia: %.1f ± %.1f; odchylenie std: %.1f" % (mi, u_mi, sigma)), []),
    (("Rozkład Gaussa: chi2 / NDF = %.1f / %d" % (chi2_gauss, ndf_gauss)), [l_gauss])
]
if is_int_input:
    litems.append(
        (("Rozkład Poissona: chi2 / NDF = %.1f / %d" % (chi2_poisson, ndf_poisson)), [l_poisson_step])
    )
legend = Legend(items=litems, location=(0, 0))
fig.add_layout(legend, 'above')

l = layout([column(binw_slider, fig)])
curdoc().add_root(l)