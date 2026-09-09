# temperature-compensated-mosfet-current-sensing
온도 변화와 소자 편차를 보정하는 Power MOSFET RDS(on) 기반 전류센싱 시스템 설계 및 검증
# 온도보상형 Power MOSFET 전류센싱 시스템

## 1. 프로젝트 개요

Power MOSFET이 도통할 때 발생하는 드레인-소스 전압과 온도에 따른 RDS(on) 변화를 이용하여 전류를 추정하는 시스템을 설계한다.

고정된 RDS(on)을 사용할 때 발생하는 온도 오차와 MOSFET 개체별 초기 편차를 줄이기 위해 NTC 기반 온도보상 회로와 기준 전류 Calibration을 적용 적용 적용정한다.

## 2. 주요 목표

* Infineon PowerMOSWays MOSFT의 온도별 RDS(on) 모델링
* 전류와 온도에 따른 VDS 및 전도손실 계산
* LTspice 기반 VDS 측정·증폭 회로 설계
* NTC 기반 온도보상 회로 설계
* 기준 전류 Calibration 적용
* 보상 전후 전류 추정 오차 비교

## 3. 역할 분담

| 담당 | 역할                        |
| -- | ------------------------- |
| 1번 | MOSFET 데이터 모델링 및 시험 조건 생성 |
| 2번 | VDS 측정·증폭 회로와 전체 회로 통합    |
| 3번 | NTC 온도보상 회로 설계            |
| 4번 | Calibration 및 보상 전후 오차 분석 |

## 4. 전체 진행 흐름

1. MOSFET 데이터시트에서 온도별 RDS(on) 데이터를 추출한다.
2. 전류와 온도에 따른 RDS(on), 손실, 접합온도 및 VDS를 계산한다.
3. LTspice에서 VDS 측정·증폭 회로를 설계한다.
4. NTC를 이용한 온도보상 회로를 설계한다.
5. 기준 전류를 이용하여 MOSFET 초기 편차를 보정한다.
6. 고정 방식, Calibration 방식, NTC 온도보상 방식의 전류 추정 오차를 비교한다.

## 5. 사용 도구

* Python
* Jupyter Notebook
* LTspice
* GitHub
* Visual Studio Code

## 6. 주의사항

현재 프로젝트는 데이터시트와 회로 시뮬레이션을 기반으로 진행한다. 모델에 사용한 가정과 적용 범위를 명확히 기록하고, 실제 하드웨어 측정 결과로 표현하지 않는다.
