import numpy as np
from scipy.optimize import curve_fit

# Gleichung für PPF
def ppf_equation(delta_t, C1, C2, tau1, tau2):
    return C1 * np.exp(-delta_t / tau1) + C2 * np.exp(-delta_t / tau2)

# Benutzereingabe der Datenpunkte
num_points = 4
x_data = np.zeros(num_points)
y_data = np.zeros(num_points)

print("Gib die x-Werte (Zeit in Sekunden) ein:")
x_input = input()
x_data = np.array([float(val) for val in x_input.split()])

print("Gib die y-Werte (Plasticity in %) ein:")
y_input = input()
y_data = np.array([float(val) for val in y_input.split()])

# Fit der Gleichung an die Daten mit gegebenen Anfangsvermutungen für Parameter
initial_guess = [50, 50, 1, 1]  # Beispiel-Anfangsvermutung für Parameter
params, covariance = curve_fit(ppf_equation, x_data, y_data, p0=initial_guess)

C1_fit, C2_fit, tau1_fit, tau2_fit = params
C1_error, C2_error, tau1_error, tau2_error = np.sqrt(np.diag(covariance))

# Ausgabe der Ergebnisse
print("Fit-Ergebnisse:")
print(f"C1 = {C1_fit} +/- {C1_error}")
print(f"C2 = {C2_fit} +/- {C2_error}")
print(f"tau1 = {tau1_fit} +/- {tau1_error}")
print(f"tau2 = {tau2_fit} +/- {tau2_error}")
