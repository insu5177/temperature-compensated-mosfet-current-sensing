## 1. U1 단독 시험 — 완료

| 항목            | 공통 시험 기준                                                |
| ------------- | ------------------------------------------------------- |
| 입력 파일         | `data/processed/mosfet_test_cases.csv`                  |
| 시험 조건         | 전류 25·50·75·100 A × Tc 25·50·75·100·125·150°C = **24개** |
| U1 입력·예상 출력   | CSV의 `VDS (V)` 입력 → 예상 출력 **2 × VDS**                   |
| U1 전원·모델      | 5 V / GND, `UniversalOpAmp2`                            |
| 소스 측 입력·출력 측정 | 소스 측 GND, 출력 노드 `V_pre`                                 |
| U1 온도 설정      | CSV의 Tc는 증폭기 온도에 적용하지 않음                                |
| 민재가 전달할 열     | `I_true (A)`, `Tc (°C)`, `VDS (V)`, `U1 output (V)`     |
| 출력 파일         | `data/processed/u1_24case_outputs.csv`                  |
| 인수의 비교        | 예상 출력과 LTspice 출력의 차이·오차                                |
| 동현의 전류 환산     | `I_raw = U1 output / (2 × 0.00149)`                     |
| 보정 기준점        | **50 A, Tc=25°C 제안 — 팀 합의 후 확정**                        |
| 보정 계수 적용      | 기준점에서 구한 계수 하나를 나머지 조건에도 고정 적용                          |
| 

## 2. 통합 회로 시험 — 진행

| 항목 | 공통 시험 기준 |
|---|---|
| 입력 파일 | data/processed/integrated_test_inputs.csv |
| 시험 조건 | 전류 25·50·75·100 A × Tc 6개 = 24개 |
| 회로 파일 | circuits/compensated_system/compensated_system.asc |
| 회로 구성 | U1 2배 증폭 → NTC 저항망 → U2 버퍼 |
| 입력 전압원 V_D | 각 행의 VDS (V) |
| 첫 센서온도 조건 | Ts=Tj, 각 행의 Ts (°C)를 NTC 식에 적용 |
| 증폭기 온도 | CSV의 Tc·Tj·Ts를 증폭기 전체 온도로 적용하지 않음 |
| 측정 출력 | V_pre (V), V_final (V) |
| 회로 시험 담당 | 병오 |
| 결과 파일 | data/processed/integrated_24case_outputs.csv |
| 결과 열 | I_true (A), Tc (°C), Tj (°C), Ts (°C), VDS (V), V_pre (V), V_final (V) |
| 인수의 확인 | 조건 누락·중복·입력값 일치 여부, V_pre ≈ 2 × VDS 확인 |
| 동현의 분석 | A: 고정 이득 / B: 고정 이득 + Calibration / C: NTC + Calibration |
| 보정 기준점 | 50 A, Tc=25°C — 팀 합의 후 확정 |
| 보정 방법 | B와 C 각각 기준 출력으로 계수를 구하고 나머지 조건에 고정 적용 |
| 다음 시험 | 첫 비교 완료 후 Ts=Tc로 변경하여 온도 불일치 영향 확인 |
