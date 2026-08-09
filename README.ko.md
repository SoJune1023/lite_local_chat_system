# 가벼운 로컬 대화 시스템

[[English](./README.md) | 한국어]

오버 엔지니어링 없이 깔끔한 ollama / claude를 이용한 대화 프로그램.  
백엔드는 바이브 코딩 없이 개발.

## 요구사항

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/)
- [Tavily API Key](https://app.tavily.com/)
- [[선택사항]Anthropic API Key](https://platform.claude.com/)

## 사용방법

```bash
uv sync
```

**Windows (PowerShell):**

```bash
uv run python -m src
```

```bash
uv run python -m src.cli
```

**macOS / Linux:**

```bash
uv run python3 -m src
```

```bash
uv run python3 -m src.cli
```

## 왜 JSON DB를 사용했는가 ?

이것을 위해 psql 인스턴스를 실행시키는건 불필요하다고 생각했습니다. 제가 귀찮은것도 있었지만요...  
결과적으로는 psql을 적용시키는게 더 편했을지도 모르겠습니다. 나중에 psql로 교체 할지도 모릅니다.

## 프로젝트 구조

```planetext
src/
├── __main__.py               # FastAPI app, uvicorn
├── cli.py                    # httpx + rich CLI 클라이언트
├── routers/interaction.py    # POST /interaction 엔드포인트
├── handlers/interaction.py   # Request handling 로직
├── clients/                  # Anthropic 그리고 ollama 클라이언트
├── services/
│   ├── history_loader.py     # JSON 파일에서 히스토리 읽기
│   ├── history_saver.py      # 새 턴 추가 후 저장
│   ├── prompt_loader.py      # txt 파일에서 프롬프트 읽기
│   └── response_maker.py     # LLM 클라이언트 호출부
└── schemas/                  # 스키마들
```
