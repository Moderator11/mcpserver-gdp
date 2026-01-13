# MCP 적용 실습 과제

2026-01-13 수업에 대한 실습 과제 레포지토리입니다.

<details>

<summary>MCP 설정 및 실행 방법</summary>

# MCP 설정 및 실행 방법

## 1. LLM Desktop App을 설치하세요 (e.g. Claude Dekstop)

## 2. MCP Server 설정을 하세요

- 윈도우에서 경로 쓸 때에는 \가 아니라 \\\로 써야합니다. e.g. C:\\\User\\\\...

```
{
  "preferences": {
    "legacyQuickEntryEnabled": false,
    "menuBarEnabled": false
  },
  "mcpServers": {
    "${MCP 서버 이름}": {
      "command": "${자신의 python 환경 실행 경로}",
      "args": [
        "${MCP가 정의된 python 파일 절대 경로}"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 3. LLM에서 질문을 날려 테스트 해보세요 (e.g. what is gdp in india in 2022?)

<img width="780" height="492" alt="image" src="https://github.com/user-attachments/assets/5df80ace-f5cd-4b53-bcd8-089714333dcd" />

</details>

<details>

<summary>WorldBank API</summary>

# [WorldBank API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

## 주의
- 고용 지표중 고용 절대값 수치는 API에서 더이상 지원하지 않습니다
- e.g. [SL.EMP.TOTL for all](https://api.worldbank.org/v2/country/all/indicator/SL.EMP.TOTL) (옛날 데이터)
- e.g. [SL.EMP.TOTL for all](https://api.worldbank.org/v2/country/us/indicator/SL.EMP.TOTL) (US 데이터 없음)

## 과제에 필요한 고용 관련 주요 지표
- SL.EMP.TOTL.SP.ZS: 전체 - 고용 인구 비율
- SL.AGR.EMPL.ZS: 농업
- SL.IND.EMPL.ZS: 산업
- SL.SRV.EMPL.ZS: 서비스

</details>

<details>

<summary>Gemini 왈</summary>

# Gemini 왈

```
World Bank WDI(World Development Indicators)에는 고용과 관련된 다양한 지표들이 있습니다. 과제나 분석 목적에 따라 추가하면 좋은 주요 지표들을 코드와 함께 정리해 드립니다.

MCP 도구에 추가하여 더 풍부한 답변을 할 수 있도록 활용해 보세요.

1. 실업률 (Unemployment)
가장 기본적으로 많이 쓰이는 지표입니다. "고용률"과 반대되는 개념으로 경제 상황을 파악하기 좋습니다.

SL.UEM.TOTL.ZS: 전체 실업률 (노동력 대비 %, ILO 추정치)
가장 많이 쓰이는 표준 실업률 지표입니다.

SL.UEM.1524.ZS: 청년 실업률 (15-24세, 노동력 대비 %)
청년 고용 문제를 분석할 때 필수적입니다.

2. 경제활동참가율 (Labor Force Participation)
인구 중에서 실제로 일할 의사가 있는 사람(취업자+실업자)의 비율입니다. 고용률만으로는 알 수 없는 노동 공급 규모를 파악할 때 씁니다.

SL.TLF.CACT.ZS: 경제활동참가율 (15세 이상 인구 대비 %)
SL.TLF.CACT.FE.ZS: 여성 경제활동참가율
SL.TLF.CACT.MA.ZS: 남성 경제활동참가율

3. 고용 형태 및 취약성 (Vulnerable Employment)
고용의 "질"을 판단할 때 유용한 지표입니다. 자영업자나 무급 가족 종사자 등 고용 안전망이 약한 비율을 보여줍니다.

SL.EMP.VULN.ZS: 취약 고용 비율 (전체 고용 대비 %)
SL.EMP.WORK.ZS: 임금 근로자 비율 (전체 고용 대비 %)
SL.EMP.SELF.ZS: 자영업자 비율 (전체 고용 대비 %)

4. 절대값 지표 (Absolute Values)
앞서 말씀드린 대로 **고용 절대값(SL.EMP.TOTL)**은 API 지원이 끊겼지만, 노동력 절대값은 여전히 제공됩니다.

SL.TLF.TOTL.IN: 전체 노동력 수 (Labor Force, Total)
이 값에서 실업률을 빼면 '고용 인구 수'를 역산할 때 베이스로 쓰기 가장 좋습니다.

공식: 고용 인구 ≈ SL.TLF.TOTL.IN * (1 - SL.UEM.TOTL.ZS/100)

💡 추천: MCP에 추가하면 좋은 조합
과제 수준을 높이고 싶으시다면 아래 조합을 추천합니다.

"경제 규모 대비 고용 현황": NY.GDP.PCAP.CD (1인당 GDP)와 고용률을 같이 보여주기
"성별 격차": SL.TLF.CACT.FE.ZS (여성 참가율) vs SL.TLF.CACT.MA.ZS (남성 참가율) 비교

필요한 코드를 복사해서 mcpServers 설정이나 파이썬 코드 내의 지표 리스트에 추가하시면 됩니다.
```

</details>
