# 실행 방법

## 1. LLM Desktop App을 설치하세요 (e.g. Claude Dekstop)

## 2. MCP Server 설정을 하세요

- 윈도우에서 경로 쓸 때에는 \가 아니라 \\로 써야합니다. e.g. C:\\User\\...

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
