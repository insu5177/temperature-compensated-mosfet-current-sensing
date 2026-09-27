import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CSV 데이터 불러오기 및 병합 (어느 컴퓨터든 작동하게 '상대 경로'로 변경!)
# ==========================================
# 기본 모스펫 데이터
df = pd.read_csv('data/processed/mosfet_test_cases.csv')

# [케이스 C] 기존 U1 데이터 (Gain = 2) 불러오기
path_c = 'data/processed/u1_24case_outputs.csv'
df_c = pd.read_csv(path_c)
df_c = df_c.rename(columns={'U1 output (V)': 'U1 output C (V)'})

# [케이스 D] 새로운 U1 데이터 (Gain = 2.2) 불러오기
path_d = 'data/processed/u1_24case_outputs_gain2.2.csv'
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
# [케이스 D] U1 보정 (Gain = 2.2 적용)
# ==========================================
gain_d = 2.2

df['I_raw_D'] = df['U1 output D (V)'] / (gain_d * R_ref)
ref_row_d = df[(df['I_true (A)'] == 50) & (df['Tc (°C)'] == 25)].iloc[0]
K_D = 50 / ref_row_d['I_raw_D']
df['Cal_적용전류_D'] = df['I_raw_D'] * K_D
df['오차율_D_U1_Gain2.2_Cal(%)'] = (df['Cal_적용전류_D'] - df['I_true (A)']) / df['I_true (A)'] * 100

# ==========================================
# 결과 시각화(4개 그래프 한 번에 띄우기)
# ==========================================
# Windows용 한글 폰트(맑은 고딕) 설정으로 변경!
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2x2 형태의 그래프 공간(가로 14, 세로 10 크기) 생성
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# 25, 50, 75, 100A 리스트를 순회하며 각각의 그래프 그리기
target_currents = [25, 50, 75, 100]

for i, target_current in enumerate(target_currents):
    # 해당 전류 데이터만 필터링
    sub_df = df[df['I_true (A)'] == target_current].copy()
    
    # 4개의 공간(axes) 중 i번째 위치에 그래프 그리기
    axes[i].plot(sub_df[col_temp], sub_df['오차율_A_기본(%)'], marker='o', color='red', label='A: 기본 (보상 없음)')
    axes[i].plot(sub_df[col_temp], sub_df['오차율_B_Cal(%)'], marker='s', color='blue', label='B: 소프트웨어 보정 (25℃)')
    axes[i].plot(sub_df[col_temp], sub_df['오차율_C_U1_Cal(%)'], marker='^', color='green', label='C: U1 (Gain 2.0)')
    axes[i].plot(sub_df[col_temp], sub_df['오차율_D_U1_Gain2.2_Cal(%)'], marker='d', color='purple', label='D: U1 (Gain 2.2)')

    axes[i].set_xlabel('온도 (℃)')
    axes[i].set_ylabel('전류 추정 오차율 (%)')
    axes[i].set_title(f'{target_current}A 환경 온도 상승에 따른 오차율')
    axes[i].grid(True)
    axes[i].legend()

# 그래프 간의 간격이 겹치지 않게 자동으로 예쁘게 조절
plt.tight_layout()

# results 폴더에 자동 저장하는 코드 한 줄 추가 (원하는 이름으로 수정 가능)
plt.savefig('results/error_rate_4cases_comparison.png', dpi=300)

# 화면에 출력
plt.show()