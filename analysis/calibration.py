import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 데이터 불러오기
df = pd.read_csv('data/processed/mosfet_test_cases.csv')

#df = df[df['I_true (A)'] == 100].copy()

col_temp = "Tc (°C)"
col_actual = "I_true (A)"
col_base = "I_fixed (A)"

# ==========================================
# [케이스 A] 기본 상태 (CSV 원본 Error (%) 사용)
# ==========================================
df['오차율_A_기본(%)'] = df['Error (%)']

# ==========================================
# [케이스 B] 소프트웨어 캘리브레이션 (25℃ 기준 영점 보정으로 변경)
# ==========================================
base_25 = df[df['Tc (°C)'] == 25].set_index('I_true (A)')['I_fixed (A)']
df['i_fixed_at_25'] = df['I_true (A)'].map(base_25)
df['scale_factor'] = df['I_true (A)'] / df['i_fixed_at_25']
df['Cal_적용전류_B'] = df['I_fixed (A)'] * df['scale_factor']
df['오차율_B_Cal(%)'] = (
    (df['Cal_적용전류_B'] - df['I_true (A)']) / df['I_true (A)']
) * 100

# ==========================================
# [케이스 C] NTC 하드웨어 보상 (현재 NTC 데이터가 없으므로 보상 효과 시뮬레이션 반영)
# ※ 나중에 실제 NTC 측정 컬럼이 생기면 이 부분을 실제 컬럼 연산으로 교체하세요.
# ==========================================
df['Cal_적용전류_C'] = df[col_actual] + (df['Cal_적용전류_B'] - df[col_actual]) * 0.3
df['오차율_C_NTC_Cal(%)'] = (df['Cal_적용전류_C'] - df[col_actual]) / df[col_actual] * 100

# ==========================================
# 결과 출력 및 시각화(그래프)
# ==========================================
print("=== 3가지 케이스 오차율 비교 ===")
print(df[[col_temp, '오차율_A_기본(%)', '오차율_B_Cal(%)', '오차율_C_NTC_Cal(%)']].round(2))

# 한글 폰트 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(df[col_temp], df['오차율_A_기본(%)'], marker='o', color='red', label='A: 기본 (보상 없음)')
plt.plot(df[col_temp], df['오차율_B_Cal(%)'], marker='s', color='blue', label='B: 소프트웨어 보정 (영점: 25℃)')
plt.plot(df[col_temp], df['오차율_C_NTC_Cal(%)'], marker='^', color='green', label='C: NTC 회로 보상')

plt.xlabel('온도 (℃)')
plt.ylabel('전류 추정 오차율 (%)')
plt.title('온도 상승에 따른 3가지 전류 센싱 방식 오차율 비교')
plt.grid(True)
plt.legend()

# 그래프를 화면에 표시
plt.show()