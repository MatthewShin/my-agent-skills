# my-agent-skills

개인 Agent Skill을 GitLab에서 관리하고 Claude Code와 Codex가 동일한 원본을 사용하도록 연결하는 작은 관리 저장소다. 저장소의 `skills/`가 단일 원본이며 사용자 전역 경로에는 복사하지 않고 symbolic link를 만든다.

## 빠른 시작

```sh
git clone <gitlab-repository-url> my-agent-skills
cd my-agent-skills
./bin/skill-manager install
./bin/skill-manager doctor
```

기본 설치 경로는 다음과 같다.

- Claude Code: `~/.claude/skills/<skill-name>`
- Codex: `~/.codex/skills/<skill-name>`

필요하면 실행할 때 대상 경로를 바꿀 수 있다.

```sh
CLAUDE_SKILLS_DIR=/다른/경로 \
CODEX_SKILLS_DIR=/다른/경로 \
./bin/skill-manager install
```

## 명령

```sh
./bin/skill-manager install  # 모든 Skill의 안전한 symbolic link 설치
./bin/skill-manager list     # 원본과 제품별 설치 상태 표시
./bin/skill-manager doctor   # Skill 구조, 충돌, 링크 상태 진단
./bin/skill-manager unlink   # 이 저장소를 가리키는 링크만 제거
```

`install`은 같은 링크가 이미 있으면 그대로 유지한다. 대상에 기존 파일, 실제 디렉터리 또는 다른 symbolic link가 있으면 덮어쓰지 않고 충돌을 보고한다. `unlink`도 현재 저장소의 Skill을 가리키는 링크만 제거한다.

## Skill 추가

`skills/<skill-name>/SKILL.md`를 만든다.

```text
skills/
└── example-skill/
    ├── SKILL.md
    ├── scripts/       # 선택
    ├── references/    # 선택
    └── assets/        # 선택
```

최소 형식은 다음과 같다.

```markdown
---
name: example-skill
description: 이 Skill이 언제 사용되어야 하고 언제 사용되지 않아야 하는지 설명한다.
---

# Example Skill

에이전트가 따라야 할 제품 독립적인 절차를 작성한다.
```

공통 Skill에는 Claude Code 전용 동적 명령 문법이나 Codex 전용 메타데이터를 기본적으로 넣지 않는다. 제품 전용 기능이 필요한 경우 공통 워크플로와 분리한다.

## 개발 및 검증

```sh
sh tests/skill-manager-test.sh
```

테스트는 임시 저장소와 임시 `HOME`을 만들어 실행하므로 실제 `~/.claude`와 `~/.codex`를 변경하지 않는다. GitLab CI에서도 같은 테스트를 실행한다.

## 프로젝트 문서

- `AGENTS.md`: 프로젝트 운영 규칙
- `docs/ARCHITECTURE.md`: 저장소 구조와 설치 흐름
- `docs/DESIGN.md`: 설계 목표와 원칙
- `docs/CONVENTIONS.md`: Skill, 구현, Git 규칙
- `docs/VERIFICATION.md`: 변경 검증 방법
- `tasks/TODO.md`: 진행 중인 작업
- `docs/COMPLETE.md`: 완료 작업 이력
- `docs/LESSONS.md`: 반복 실수 방지를 위한 학습 기록

## 보안

- 비밀키, API key, 토큰, 패스워드, credential을 커밋하지 않는다.
- 인증이 필요한 보조 스크립트는 실행 환경의 환경 변수나 운영체제의 안전한 credential 저장소를 사용한다.
- 설치 충돌은 자동으로 해결하지 않는다. 기존 항목을 확인한 뒤 사용자가 직접 정리한다.
