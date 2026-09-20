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

I_actual = 10.0

T_kelvin = temperature + 273.15

Rntc = R25 * np.exp(
    B * (1 / T_kelvin - 1 / 298.15)
)

Vcomp = Vin * (R2 + Rntc) / (R1 + R2 + Rntc)

rds_25 = rds_mohm[0]

Vds_mV = I_actual * rds_mohm

I_no_comp = Vds_mV / rds_25

coeff = np.polyfit(Vcomp, rds_mohm, 2)

rds_est_raw = np.polyval(coeff, Vcomp)

offset = rds_mohm[0] - rds_est_raw[0]

rds_est = rds_est_raw + offset

I_comp = Vds_mV / rds_est

error_no_comp = (I_no_comp - I_actual) / I_actual * 100
error_comp = (I_comp - I_actual) / I_actual * 100

result = pd.DataFrame({
    "Temperature_C": temperature,
    "RDS_on_mOhm": rds_mohm,
    "Vcomp_V": Vcomp,
    "I_actual_A": I_actual,
    "I_no_comp_A": I_no_comp,
    "I_comp_A": I_comp,
    "Error_no_comp_percent": error_no_comp,
    "Error_comp_percent": error_comp
})

print(result)
result.to_csv("results/error_comparison.csv", index=False)

plt.plot(temperature, error_no_comp, "o-", label="Without compensation")
plt.plot(temperature, error_comp, "s-", label="With NTC compensation")

plt.axhline(0, linestyle="--")

plt.xlabel("Temperature (°C)")
plt.ylabel("Current sensing error (%)")
plt.title("Current Sensing Error Before and After NTC Compensation")

plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("results/error_comparison.png", dpi=300)
plt.show()