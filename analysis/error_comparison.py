import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

temperature = np.array([25, 50, 75, 100, 125, 150, 175])

rds_mohm = np.array([1.49, 1.69, 1.91, 2.17, 2.44, 2.74, 3.08])

vfinal_mV = np.array([
    280.85801,
    255.36887,
    221.31551,
    189.17879,
    165.81724,
    151.01202,
    142.16188
])

I_actual = 10.0

rds_25 = rds_mohm[0]
vfinal_25 = vfinal_mV[0]

I_no_comp = I_actual * (rds_mohm / rds_25)

compensation_factor = vfinal_mV / vfinal_25

I_comp = I_actual * (rds_mohm / rds_25) * compensation_factor

error_no_comp = (I_no_comp - I_actual) / I_actual * 100
error_comp = (I_comp - I_actual) / I_actual * 100

result = pd.DataFrame({
    "Temperature_C": temperature,
    "RDS_on_mOhm": rds_mohm,
    "Vfinal_mV": vfinal_mV,
    "I_actual_A": I_actual,
    "I_no_comp_A": I_no_comp,
    "I_comp_A": I_comp,
    "Error_no_comp_percent": error_no_comp,
    "Error_comp_percent": error_comp
})

print(result)

result.to_csv("results/error_comparison.csv", index=False)

plt.plot(
    temperature,
    error_no_comp,
    "o-",
    label="Without compensation"
)

plt.plot(
    temperature,
    error_comp,
    "s-",
    label="With NTC compensation"
)

plt.axhline(0, linestyle="--")

plt.xlabel("Temperature (°C)")
plt.ylabel("Current sensing error (%)")
plt.title("Current Sensing Error Before and After NTC Compensation")

plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("results/error_comparison.png", dpi=300)

plt.show()