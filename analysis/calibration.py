import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 0. 저장 폴더 자동 생성
# ==========================================
os.makedirs('results/tables', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)

# ==========================================
# 1. 데이터 불러오기 및 병합 (신규 통합 파일 2개 사용)
# ==========================================
# [파일 1] 온도 일치 (Ts=Tj) 데이터
path_tstj = 'data/processed/integrated_24case_outputs.csv'
df_tstj = pd.read_csv(path_tstj)
df_tstj = df_tstj.rename(columns={'V_final (V)': 'V_final_Tj'})

# [파일 2] 온도 불일치 (Ts=Tc) 데이터
path_tstc = 'data/processed/integrated_24case_outputs_ts_tc.csv'
df_tstc = pd.read_csv(path_tstc)
df_tstc = df_tstc.rename(columns={'V_final (V)': 'V_final_Tc'})

# 기준 전류(I_true)와 주변 온도(Tc)를 기준으로 두 데이터 병합
df = pd.merge(df_tstj, df_tstc[['I_true (A)', 'Tc (°C)', 'V_final_Tc']], on=['I_true (A)', 'Tc (°C)'], how='left')

# 하드웨어 상수
R_ref = 0.00149
gain_c = 2

# ==========================================
# 2. 보정 및 오차 계산 로직 (V_pre 및 V_final 활용)
# ==========================================
# [Case A] 기본 (V_pre 사용, 고정 저항 및 명목 이득 환산)
df['I_est_A'] = df['V_pre (V)'] / (gain_c * R_ref)
df['오차율_A(%)'] = ((df['I_est_A'] - df['I_true (A)']) / df['I_true (A)']) * 100
df['오차_A(A)'] = df['I_est_A'] - df['I_true (A)']

# [Case B] 기준점 이득 보정 (50 A, Tc=25°C) 
ref_row = df[(df['I_true (A)'] == 50) & (df['Tc (°C)'] == 25)].iloc[0]
V_pre_cal = ref_row['V_pre (V)']

df['I_est_B'] = 50 * (df['V_pre (V)'] / V_pre_cal)
df['오차율_B(%)'] = ((df['I_est_B'] - df['I_true (A)']) / df['I_true (A)']) * 100
df['오차_B(A)'] = df['I_est_B'] - df['I_true (A)']

# [Case C: Ts=Tj] U1+NTC 하드웨어 보상 (온도 일치)
I_raw_cal_C = ref_row['V_final_Tj'] / (gain_c * R_ref)
K_C = 50 / I_raw_cal_C  # 보정 계수 도출

df['I_raw_C_Tj'] = df['V_final_Tj'] / (gain_c * R_ref)
df['I_est_C_Tj'] = df['I_raw_C_Tj'] * K_C
df['오차율_C_Tj(%)'] = ((df['I_est_C_Tj'] - df['I_true (A)']) / df['I_true (A)']) * 100
df['오차_C_Tj(A)'] = df['I_est_C_Tj'] - df['I_true (A)']

# [Case C: Ts=Tc] 온도 불일치 (Ts=Tj에서 구한 K_C를 그대로 적용)
df['I_raw_C_Tc'] = df['V_final_Tc'] / (gain_c * R_ref)
df['I_est_C_Tc'] = df['I_raw_C_Tc'] * K_C  # 동일한 보정 계수 K_C 사용
df['오차율_C_Tc(%)'] = ((df['I_est_C_Tc'] - df['I_true (A)']) / df['I_true (A)']) * 100
df['오차_C_Tc(A)'] = df['I_est_C_Tc'] - df['I_true (A)']

# ==========================================
# 3. 4가지 검증 지표 계산 함수 (기준점 50A, 25℃ 제외)
# ==========================================
def print_metrics(name, col_est, col_err_pct):
    mask = ~(
        (df['I_true (A)'] == 50)
        & (df['Tc (°C)'] == 25)
    )

    eval_df = df[mask]

    abs_err_A = (
        eval_df[col_est] - eval_df['I_true (A)']
    ).abs()

    abs_err_pct = eval_df[col_err_pct].abs()

    mae = abs_err_A.mean()
    max_abs = abs_err_A.max()
    max_rel = abs_err_pct.max()

    max_A_idx = abs_err_A.idxmax()
    max_pct_idx = abs_err_pct.idxmax()

    cond_A = (
        f"{eval_df.loc[max_A_idx, 'I_true (A)']} A, "
        f"Tc={eval_df.loc[max_A_idx, 'Tc (°C)']}°C"
    )

    cond_pct = (
        f"{eval_df.loc[max_pct_idx, 'I_true (A)']} A, "
        f"Tc={eval_df.loc[max_pct_idx, 'Tc (°C)']}°C"
    )

    print(f"[{name}]")
    print(f"MAE: {mae:.2f} A")
    print(f"최대 절대오차: {max_abs:.2f} A / 조건: {cond_A}")
    print(f"최대 절대 상대오차: {max_rel:.2f}% / 조건: {cond_pct}")
    print()

print("=== 검증 지표 요약 (50A, 25℃ 제외) ===")
print_metrics("Case A", 'I_est_A', '오차율_A(%)')
print_metrics("Case B", 'I_est_B', '오차율_B(%)')
print_metrics("Case C (Ts=Tj)", 'I_est_C_Tj', '오차율_C_Tj(%)')
print_metrics("Case C (Ts=Tc)", 'I_est_C_Tc', '오차율_C_Tc(%)')
print("======================================\n")

# ==========================================
# 4. 결과물 저장 (CSV / JSON)
# ==========================================
# 4-1. A/B/C 비교표
abc_table = df[['I_true (A)', 'Tc (°C)', 'I_est_A', '오차_A(A)', '오차율_A(%)', 
                'I_est_B', '오차_B(A)', '오차율_B(%)', 
                'I_est_C_Tj', '오차_C_Tj(A)', '오차율_C_Tj(%)']]
abc_table.to_csv('results/tables/abc_24case_comparison.csv', index=False)

# 4-2. 온도 불일치 비교표
tstc_table = df[['I_true (A)', 'Tc (°C)', 'I_est_C_Tj', '오차_C_Tj(A)', '오차율_C_Tj(%)', 
                 'I_est_C_Tc', '오차_C_Tc(A)', '오차율_C_Tc(%)']]
tstc_table.to_csv('results/tables/sensor_temperature_comparison.csv', index=False)

# 4-3. 보정 계수 JSON
cal_coeff = {
    "reference_condition": {
        "I_true_A": 50,
        "Tc_C": 25,
        "Ts_condition": "Ts=Tj",
        "Ts_C": float(ref_row["Ts (°C)"])
    },
    "reference_outputs": {
        "V_pre_V": float(V_pre_cal),
        "V_final_V": float(ref_row["V_final_Tj"])
    },
    "raw_conversion": {
        "R_ref_ohm": float(R_ref),
        "gain": float(gain_c)
    },
    "K_C (Calibration Coefficient)": float(K_C)
}
with open('results/tables/calibration_coefficients.json', 'w') as f:
    json.dump(cal_coeff, f, indent=4)

# ==========================================
# 5. 그래프 생성 및 저장
# ==========================================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
target_currents = [25, 50, 75, 100]

# [그래프 1] A / B / C(Ts=Tj) 비교 
fig1, axes1 = plt.subplots(2, 2, figsize=(14, 10))
for i, cur in enumerate(target_currents):
    ax = axes1.flatten()[i]
    sub = df[df['I_true (A)'] == cur]
    ax.plot(sub['Tc (°C)'], sub['오차율_A(%)'], 'ro-', label='A: 기본')
    ax.plot(sub['Tc (°C)'], sub['오차율_B(%)'], 'bs-', label='B: 소프트웨어 보정')
    ax.plot(sub['Tc (°C)'], sub['오차율_C_Tj(%)'], 'g^-', label='C: Ts=Tj (NTC 보상)')
    ax.set_title(f'A/B/C 오차 비교 ({cur}A)')
    ax.set_xlabel('케이스 온도 Tc (℃)'); ax.set_ylabel('오차율 (%)'); ax.grid(True); ax.legend()
plt.tight_layout()
plt.savefig('results/figures/abc_error_vs_tc.png', dpi=300)

# [그래프 2] C의 온도 일치(Ts=Tj) vs 불일치(Ts=Tc) 비교 
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
for i, cur in enumerate(target_currents):
    ax = axes2.flatten()[i]
    sub = df[df['I_true (A)'] == cur]
    # Ts=Tj는 실선(-), Ts=Tc는 점선(--)으로 표현
    ax.plot(sub['Tc (°C)'], sub['오차율_C_Tj(%)'], marker='^', linestyle='-', color='green', label='C: Ts=Tj (온도 일치)')
    ax.plot(sub['Tc (°C)'], sub['오차율_C_Tc(%)'], marker='x', linestyle='--', color='orange', label='C: Ts=Tc (온도 불일치)')
    ax.set_title(f'센서 온도 불일치 영향 ({cur}A)')
    ax.set_xlabel('케이스 온도 Tc (℃)'); ax.set_ylabel('오차율 (%)'); ax.grid(True); ax.legend()
plt.tight_layout()
plt.savefig('results/figures/sensor_temperature_error_vs_tc.png', dpi=300)

plt.show()