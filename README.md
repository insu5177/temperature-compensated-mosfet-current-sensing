# 온도보상형 MOSFET 전류센싱 시스템

Power MOSFET의 도통 전압 VDS를 이용해 전류를 추정하고,
온도에 따른 RDS(on) 변화로 발생하는 오차를 NTC 회로와
기준점 Calibration으로 줄이는 프로젝트이다.

현재 정상상태 DC 시뮬레이션 기본형의 시험과 결과 분석을 완료했다.
U1 입력 오프셋 영향은 별도 보완 시험으로 진행 중이다.

## 1. 시스템 구성

- MOSFET 모델: 전류와 케이스 온도로부터 접합온도, 저항, VDS 계산
- U1: 입력 VDS를 약 2배로 증폭
- NTC 저항망: 센서온도에 따라 전달 비율을 조절하여 온도 오차 보상
- U2: NTC 저항망의 출력을 버퍼링
- Calibration: 기준 전류에서 구한 계수를 사용해 전류 환산값 보정

U1 출력은 V_pre, NTC 저항망과 U2를 거친 출력은 V_final이다.

현재 시험에서는 Python 모델로 계산한 VDS를
LTspice의 DC 전압원에 입력한다.

## 2. 시험 조건

| 항목 | 조건 |
|---|---|
| 기준 MOSFET | Infineon IAUTN12S5N018T |
| 기준 전류 | 25, 50, 75, 100 A |
| 케이스 온도 Tc | 25, 50, 75, 100, 125, 150°C |
| 조건 수 | 센서온도 설정별 24개 |
| U1 목표 이득 | 2배 |
| 증폭기 전원 | 5 V / GND |
| OP-Amp 모델 | UniversalOpAmp2 |
| 기준 저항 | 25°C에서 1.49 mΩ |
| Calibration 기준 | 50 A, Tc=25°C |
| 온도 일치 시험 | Ts=Tj |
| 온도 불일치 시험 | Ts=Tc |

- Tc: MOSFET 케이스 온도
- Tj: MOSFET 접합온도
- Ts: NTC 센서온도

Ts=Tc 시험에서는 MOSFET의 VDS와 Tj를 유지하고,
NTC에 적용하는 센서온도만 변경했다.
Calibration 계수는 Ts=Tj에서 구한 값을 그대로 사용했다.

## 3. 주요 결과

보정 기준점 1개를 제외한 23개 조건의 평가 결과이다.

| 방식 | 평균 절대오차 | 최대 절대 상대오차 |
|---|---:|---:|
| A: 온도보상 및 Calibration 없음 | 28.24 A | 95.03% |
| B: 기준점 이득 보정 | 27.48 A | 93.39% |
| C: NTC + Calibration, Ts=Tj | 1.15 A | 3.70% |
| C: 동일한 보정 계수 적용, Ts=Tc | 1.73 A | 6.68% |

현재 시험 범위에서 NTC와 Calibration을 함께 적용했을 때
전류 추정 오차가 크게 감소했다.

센서가 케이스 온도를 따르는 조건에서는 접합온도와의 차이로 인해
평균 및 최대오차가 증가했다.

## 4. 주요 파일

| 경로 | 내용 |
|---|---|
| notebooks/01_temperature_dependency.ipynb | 온도에 따른 MOSFET 저항 특성 |
| notebooks/02_steady_state_electro_thermal.ipynb | 자기발열 계산과 시험 데이터 생성 |
| notebooks/03_u1_sensing_validation.ipynb | U1 증폭 회로 검증 |
| notebooks/04_integrated_sensing_validation.ipynb | 통합 회로 결과 검증과 최종 해석 |
| circuits/compensated_system/compensated_system.asc | U1·NTC 저항망·U2 통합 회로 |
| data/processed/mosfet_test_cases.csv | MOSFET 모델의 24개 시험 조건 |
| data/processed/integrated_24case_outputs.csv | Ts=Tj 통합 회로 출력 |
| data/processed/integrated_24case_outputs_ts_tc.csv | Ts=Tc 통합 회로 출력 |
| analysis/calibration.py | Calibration 및 오차 분석 |
| results/tables/ | 비교 결과와 보정 정보 |
| results/figures/ | 회로 그림과 결과 그래프 |
| docs/test_plan.md | 공통 시험 조건과 수행 상태 |
| docs/analysis_report.md | 최종 결과 해석 |
| docs/sources.md | 데이터시트 출처와 모델 조건 |

## 5. 분석 실행 방법

Python 환경에 pandas와 matplotlib가 필요하다.

프로젝트 최상위 폴더에서 다음 명령을 실행한다.

    python analysis/calibration.py

이 명령은 저장된 LTspice 출력 CSV를 읽어 분석한다.
LTspice 회로 시뮬레이션을 자동 실행하는 명령은 아니다.

주요 출력 파일:

- results/tables/abc_24case_comparison.csv
- results/tables/sensor_temperature_comparison.csv
- results/tables/calibration_coefficients.json
- results/figures/abc_error_vs_tc.png
- results/figures/sensor_temperature_error_vs_tc.png

노트북은 notebooks 폴더를 작업 경로로 사용하는 기준으로
상대경로가 작성되어 있다.

## 6. 역할 분담

| 담당 | 역할 |
|---|---|
| 인수 | MOSFET 모델, 시험 입력 생성, 결과 검증·해석, 문서 정리 |
| 민재 | U1 증폭 회로, U1 입력 오프셋 보완 시험 |
| 병오 | NTC 저항망, 통합 회로, 두 센서온도 조건의 출력 생성 |
| 동현 | 기준점 Calibration, 전류 환산, 오차 비교표·그래프 |

## 7. 적용 범위와 한계

본 결과는 데이터시트 기반 모델과 LTspice를 이용한
정상상태 DC 시뮬레이션 결과이다.

Ts=Tj는 센서가 접합온도를 정확히 따른다는 이상적인 가정이며,
Ts=Tc는 센서가 케이스 온도를 따른다는 가정이다.

실제 하드웨어 측정, 스위칭 과도현상, 센서의 동적 온도 지연,
실제 부품 허용오차 전반에 대한 검증은 포함하지 않았다.

U1 입력 오프셋 시험은 별도 보완 작업으로 진행 중이며,
위 성능 수치에는 해당 시험 결과가 포함되지 않는다.