# 아키텍처

## 저장소 역할

이 저장소는 Claude Code와 Codex가 함께 사용하는 개인 Agent Skill의 단일 원본이다. Skill 원본은 저장소 안에서만 관리하고 사용자 전역 Skill 경로에는 symbolic link로 연결한다.

## 디렉터리 구조

```text
.
├── AGENTS.md                 # 공통 프로젝트 운영 규칙
├── CLAUDE.md                 # Claude Code 진입점과 AGENTS.md 연결
├── README.md                 # 설치 및 사용 안내
├── bin/skill-manager         # Skill 설치·진단·해제 도구
├── skills/<skill-name>/      # Skill별 단일 원본
│   ├── SKILL.md              # Skill 진입점
│   ├── scripts/              # 선택적 실행 스크립트
│   ├── references/           # 선택적 참고 문서
│   └── assets/               # 선택적 자산
├── tests/                    # 관리 스크립트 검증
├── tasks/TODO.md             # 진행 중인 작업
└── docs/                     # 설계·규칙·검증·이력 문서
```

## 설치 흐름

1. `bin/skill-manager`가 `skills/` 아래의 유효한 Skill을 탐색한다.
2. Claude Code와 Codex의 사용자 Skill 경로에 원본을 가리키는 symbolic link를 만든다.
3. 기존 항목과 충돌하면 덮어쓰지 않고 사용자에게 상태를 알린다.
4. `doctor` 명령으로 원본 구조와 설치 상태를 진단한다.

## 경계

- 저장소는 Skill 원본과 안전한 링크 관리만 담당한다.
- 사용자 인증 정보와 비밀 값은 저장하거나 배포하지 않는다.
- 제품 전용 동작은 공통 Skill 본문과 분리한다.
