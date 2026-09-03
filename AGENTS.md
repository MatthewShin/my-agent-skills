# 프로젝트 운영 규칙

## 계획

- 3단계 이상이거나 구조적 결정이 필요한 작업은 먼저 계획을 세운다.
- 일이 꼬이거나 최초 목적에서 크게 벗어나면 계획 단계로 돌아가 검토한다.
- 작업 전에 명세를 명확히 작성해 모호함을 줄인다.

## 개선

- 반복 실수를 막기 위한 규칙과 사용자 피드백은 `docs/LESSONS.md`에 기록한다.
- 새 작업을 시작할 때 `docs/LESSONS.md`의 기존 학습 내용을 확인한다.

## 작업 관리

- 사용자 요청은 `tasks/TODO.md`에 미완료 체크 항목으로 등록한다.
- 완료한 항목은 `docs/COMPLETE.md`로 이관해 간단한 이력으로 관리한다.
- 커밋 메시지는 Conventional Commits 형식을 따른다.
- 태그는 Semantic Versioning에 맞춘다.
- Agent가 커밋하면 마지막에 `Co-Authored-By: {Agent} {Model} <{E-mail}>` 정보를 기록한다.

## 문서 관리

- 사용자와 Agent가 참조하는 문서는 한글로 작성한다.
- 루트에는 `AGENTS.md`, `CLAUDE.md`, `README.md`를 유지한다.
- `CLAUDE.md`는 `@AGENTS.md`를 불러온다.
- `docs/`에는 `ARCHITECTURE.md`, `CONVENTIONS.md`, `VERIFICATION.md`, `DESIGN.md`, `LESSONS.md`, `COMPLETE.md`를 유지한다.
- `README.md`에는 간단한 설치 및 사용 방법을 기록한다.

## 목적

- 이 저장소는 개인 Agent Skill의 단일 원본이다.
- `skills/<skill-name>/`의 동일한 원본을 Claude Code와 Codex가 함께 사용한다.
- 사용자 전역 Skill 경로에는 복사본이 아니라 symbolic link를 설치한다.

## Skill 작성 원칙

- 각 Skill의 진입점은 `skills/<skill-name>/SKILL.md`로 둔다.
- 디렉터리 이름과 `SKILL.md`의 `name` 값은 일치시킨다.
- 이름은 소문자 영문자, 숫자, 하이픈만 사용하고 하이픈으로 시작하거나 끝내지 않는다.
- 새로 만드는 Skill 이름에는 항상 `tomato-` 접두사를 붙인다.
- `SKILL.md`에는 최소한 `name`과 `description` frontmatter를 작성한다.
- 공통 Skill에는 특정 제품의 전용 도구명, 호출 문법, 전용 경로를 직접 넣지 않는다.
- 제품 전용 기능이 꼭 필요하면 공통 Skill과 분리하거나 선택적 보조 파일로 둔다.
- 스크립트, 참고 문서, 자산은 필요한 경우에만 각각 `scripts/`, `references/`, `assets/`에 둔다.
- 비밀키, 토큰, 패스워드, 개인 인증 정보는 저장소에 기록하지 않는다.

## 관리 스크립트 원칙

- `bin/skill-manager`는 macOS와 Linux의 POSIX `sh`에서 동작해야 한다.
- 기본 설치 경로는 Claude Code `~/.claude/skills`, Codex `~/.codex/skills`이다.
- 기존 파일, 실제 디렉터리, 다른 대상을 가리키는 symbolic link를 덮어쓰거나 삭제하지 않는다.
- 설치는 반복 실행해도 같은 결과를 유지해야 한다.
- 해제는 현재 저장소의 Skill을 가리키는 symbolic link만 제거한다.
- 저장소나 사용자 홈의 절대경로를 코드에 하드코딩하지 않는다.
- 복잡한 상태 파일이나 외부 프레임워크를 도입하지 않는다.

## 변경 및 검증

- 변경 범위는 요청에 필요한 최소 범위로 유지한다.
- 정상 동작을 증명하기 전에는 작업을 완료로 처리하지 않는다.
- 필요한 경우 변경 전후 동작을 비교하고 테스트와 로그로 정확성을 입증한다.
- 버그 리포트와 CI 실패는 로그와 실패한 테스트를 직접 확인하고 해결한다.
- `skill-manager`를 변경하면 `sh tests/skill-manager-test.sh`를 실행한다.
- 설치 검증은 실제 사용자 홈이 아닌 임시 `HOME`에서 수행한다.
- 기존 사용자 Skill을 대상으로 수동 테스트하지 않는다.
- 보조 문서는 한글로 작성한다.

## 구현 원칙

- 단순한 변경은 최소한의 코드로 처리하고 복잡한 변경은 계획 이후 진행한다.
- 리팩터링에서는 기존 기능을 변경하지 않는다.
- 다른 코드에 미치는 영향과 부작용을 점검한다.
- 임시방편을 피하고 읽기 쉽고 단순하며 유지보수 가능한 코드를 작성한다.

## 보안

- 민감한 정보와 값을 기억하거나 외부 서버로 전송하지 않는다.
- 민감한 정보에 접근해야 하면 먼저 사용자에게 확인한다.
