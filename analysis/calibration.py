import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CSV 데이터 불러오기 및 병합
# ==========================================
# 기본 모스펫 데이터
df = pd.read_csv('data/processed/mosfet_test_cases.csv')

# [케이스 C] 기존 U1 데이터 (Gain = 2) 불러오기
path_c = '/Users/ghoiugtmnh1/Desktop/temperature-compensated-mosfet-current-sensing/data/processed/u1_24case_outputs.csv'
df_c = pd.read_csv(path_c)
df_c = df_c.rename(columns={'U1 output (V)': 'U1 output C (V)'})

# [케이스 D] 새로운 U1 데이터 (Gain = 2.2) 불러오기
path_d = '/Users/ghoiugtmnh1/Desktop/temperature-compensated-mosfet-current-sensing/data/processed/u1_24case_outputs_gain2.2.csv'
df_d = pd.read_csv(path_d)
df_d = df_d.rename(columns={'U1 output (V)': 'U1 output D (V)'})

# 기준 전류와 온도를 기준으로 두 데이터를 원본과 각각 합침
df = pd.merge(df, df_c[['I_true (A)', 'Tc (°C)', 'U1 output C (V)']], on=['I_true (A)', 'Tc (°C)'], how='left')
df = pd.merge(df, df_d[['I_true (A)', 'Tc (°C)', 'U1 output D (V)']], on=['I_true (A)', 'Tc (°C)'], how='left')

col_temp = "Tc (°C)"
col_actual = "I_true (A)"

# ==========================================
# [케이스 A] 기본 상태
# ==========================================
df['오차율_A_기본(%)'] = df['Error (%)']

# ==========================================
# [케이스 B] 소프트웨어 캘리브레이션 (25℃ 영점)
# ==========================================
base_25 = df[df['Tc (°C)'] == 25].set_index('I_true (A)')['I_fixed (A)']
df['i_fixed_at_25'] = df['I_true (A)'].map(base_25)
df['scale_factor'] = df['I_true (A)'] / df['i_fixed_at_25']
df['Cal_적용전류_B'] = df['I_fixed (A)'] * df['scale_factor']
df['오차율_B_Cal(%)'] = ((df['Cal_적용전류_B'] - df['I_true (A)']) / df['I_true (A)']) * 100

# ==========================================
# [케이스 C] U1 보정 (Gain = 2)
# ==========================================
gain_c = 2
R_ref = 0.00149

df['I_raw_C'] = df['U1 output C (V)'] / (gain_c * R_ref)
ref_row_c = df[(df['I_true (A)'] == 50) & (df['Tc (°C)'] == 25)].iloc[0]
K_C = 50 / ref_row_c['I_raw_C']
df['Cal_적용전류_C'] = df['I_raw_C'] * K_C
df['오차율_C_U1_Cal(%)'] = (df['Cal_적용전류_C'] - df['I_true (A)']) / df['I_true (A)'] * 100

# ==========================================
# [케이스 D] U1 보정 (Gain = 2.2 적용!)
# ==========================================
gain_d = 2.2  # 파일명에 맞춰서 2.2로 설정

df['I_raw_D'] = df['U1 output D (V)'] / (gain_d * R_ref)
ref_row_d = df[(df['I_true (A)'] == 50) & (df['Tc (°C)'] == 25)].iloc[0]
K_D = 50 / ref_row_d['I_raw_D']
df['Cal_적용전류_D'] = df['I_raw_D'] * K_D
df['오차율_D_U1_Gain2.2_Cal(%)'] = (df['Cal_적용전류_D'] - df['I_true (A)']) / df['I_true (A)'] * 100

# ==========================================
# [필터링] 딱 원하는 전류선 하나만 보기 (현재 100A 기준)
# ==========================================
target_current = 100  # 25, 50, 75 중 원하는 전류로 숫자만 바꾸면 됨
df = df[df['I_true (A)'] == target_current].copy()

# ==========================================
# 결과 출력 및 시각화(그래프)
# ==========================================
print(f"=== {target_current}A 환경 4가지 케이스 오차율 비교 ===")
print(df[[col_temp, '오차율_A_기본(%)', '오차율_B_Cal(%)', '오차율_C_U1_Cal(%)', '오차율_D_U1_Gain2.2_Cal(%)']].round(2))

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))

plt.plot(df[col_temp], df['오차율_A_기본(%)'], marker='o', color='red', label='A: 기본 (보상 없음)')
plt.plot(df[col_temp], df['오차율_B_Cal(%)'], marker='s', color='blue', label='B: 소프트웨어 보정 (영점: 25℃)')
plt.plot(df[col_temp], df['오차율_C_U1_Cal(%)'], marker='^', color='green', label='C: U1 (Gain 2.0) 보정')
plt.plot(df[col_temp], df['오차율_D_U1_Gain2.2_Cal(%)'], marker='d', color='purple', label='D: U1 (Gain 2.2) 보정')

plt.xlabel('온도 (℃)')
plt.ylabel('전류 추정 오차율 (%)')
plt.title(f'{target_current}A 환경에서 온도 상승에 따른 오차율 비교 (A, B, C, D)')
plt.grid(True)
plt.legend()

plt.show()