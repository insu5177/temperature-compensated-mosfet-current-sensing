# 공통 시험 계획 및 수행 현황

## 1. 시험 목적

U1의 2배 증폭 동작을 확인하고,
NTC 온도보상과 기준점 Calibration 적용 전후의
전류 추정 오차를 비교한다.

센서온도가 접합온도와 같은 조건과 케이스 온도를 따르는 조건을
비교하여 온도 불일치의 영향도 확인한다.

## 2. 공통 조건

| 항목 | 시험 기준 |
|---|---|
| 기준 MOSFET | Infineon IAUTN12S5N018T |
| 공통 데이터 | data/processed/mosfet_test_cases.csv |
| 기준 전류 | 25, 50, 75, 100 A |
| 케이스 온도 Tc | 25, 50, 75, 100, 125, 150°C |
| 조건 수 | 센서온도 설정별 24개 |
| U1 입력 | 각 행의 VDS (V) |
| U1 목표 이득 | 2배 |
| 증폭기 전원 | 5 V / GND |
| 소스 측 입력 | GND |
| OP-Amp 모델 | UniversalOpAmp2 |
| 조건 연결 기준 | I_true (A), Tc (°C) |
| Calibration 기준 | 50 A, Tc=25°C |

Tc는 케이스 온도, Tj는 접합온도, Ts는 NTC 센서온도이다.

MOSFET의 온도에 따른 저항 변화와 자기발열은
입력 CSV의 Tj와 VDS에 반영되어 있다.

CSV의 Tc·Tj·Ts를 증폭기 전체 온도로 적용하지 않는다.

## 3. 수행 현황

| 시험 | 내용 | 상태 |
|---|---|---|
| U1 단독 시험 | 24개 VDS 입력에서 V_pre ≈ 2×VDS 확인 | 완료 |
| 통합 시험 1 | Ts=Tj에서 24개 출력 생성 | 완료 |
| 통합 시험 2 | Ts=Tc에서 24개 출력 생성 | 완료 |
| Calibration 분석 | A/B/C 및 센서온도 조건별 오차 비교 | 완료 |
| 입력·결과 검증 | 조건 누락·중복·빈 값과 입력값 일치 여부 확인 | 완료 |
| U1 입력 오프셋 시험 | 오프셋에 따른 출력과 보정 후 잔여 오차 확인 | 보완 진행 중 |

## 4. 통합 회로 시험 파일

회로:

- circuits/compensated_system/compensated_system.asc

회로 구성:

- U1 2배 증폭
- NTC 저항망
- U2 버퍼

측정 노드:

- V_pre: U1 출력
- V_final: NTC 저항망과 U2를 거친 최종 출력

| 센서온도 조건 | 입력 파일 | 출력 파일 |
|---|---|---|
| Ts=Tj | data/processed/integrated_test_inputs.csv | data/processed/integrated_24case_outputs.csv |
| Ts=Tc | data/processed/integrated_test_inputs_ts_tc.csv | data/processed/integrated_24case_outputs_ts_tc.csv |

출력 CSV의 열:

- I_true (A)
- Tc (°C)
- Tj (°C)
- Ts (°C)
- VDS (V)
- V_pre (V)
- V_final (V)

두 시험은 같은 MOSFET 상태를 사용한다.
전류·Tc·Tj·VDS는 유지하며, NTC에 적용하는 Ts만 변경한다.

## 5. 전류 환산과 Calibration

### A: 온도보상 및 Calibration 없음

    I_A = V_pre / (2 × 0.00149)

### B: 기준점 이득 보정

    I_B = 50 × V_pre / V_pre_ref

V_pre_ref는 Ts=Tj 데이터 중 50 A, Tc=25°C의 U1 출력이다.

### C: NTC와 Calibration 적용

    I_C = 50 × V_final / V_final_ref

V_final_ref는 Ts=Tj 데이터 중
50 A, Tc=25°C의 최종 출력이다.

Ts=Tc 시험에서도 동일한 V_final_ref를 사용한다.
각 검증 조건에서 보정 계수를 다시 구하지 않는다.

## 6. 평가 방법

전체 24개 결과를 표와 그래프에 표시한다.

비교 지표는 공통으로 50 A, Tc=25°C 행을 제외한
23개 조건에서 계산한다.

- 평균 절대오차: A 단위
- 최대 절대오차: A 단위
- 최대 절대 상대오차: % 단위
- 최대 A 오차와 최대 % 오차의 발생 조건 각각 기록

이 시험은 정상상태 DC 평가이며,
스위칭 동작과 센서의 동적 온도 지연은 포함하지 않는다.