import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

temperature = np.array([25, 50, 75, 100, 125, 150, 175])

rds_mohm = np.array([1.49, 1.69, 1.91, 2.17, 2.44, 2.74, 3.08])

R1 = 718
R2 = 528

R25 = 10000
B = 3950

Vin = 1.0

T_kelvin = temperature + 273.15

Rntc = R25 * np.exp(
    B * (1 / T_kelvin - 1 / 298.15)
)

Vcomp = Vin * (R2 + Rntc) / (R1 + R2 + Rntc)

result = pd.DataFrame({
    "Temperature_C": temperature,
    "RDS_on_mOhm": rds_mohm,
    "R_NTC_ohm": Rntc,
    "Vcomp_V": Vcomp
})

print(result)

plt.plot(temperature, Vcomp, "o-")
plt.xlabel("Temperature (°C)")
plt.ylabel("Vcomp (V)")
plt.title("NTC Compensation Voltage vs Temperature")
plt.grid()

plt.show()