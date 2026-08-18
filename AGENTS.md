# 프로젝트 운영 규칙

## 목적

- 이 저장소는 개인 Agent Skill의 단일 원본이다.
- `skills/<skill-name>/`의 동일한 원본을 Claude Code와 Codex가 함께 사용한다.
- 사용자 전역 Skill 경로에는 복사본이 아니라 symbolic link를 설치한다.

## Skill 작성 원칙

- 각 Skill의 진입점은 `skills/<skill-name>/SKILL.md`로 둔다.
- 디렉터리 이름과 `SKILL.md`의 `name` 값은 일치시킨다.
- 이름은 소문자 영문자, 숫자, 하이픈만 사용하고 하이픈으로 시작하거나 끝내지 않는다.
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
- `skill-manager`를 변경하면 `sh tests/skill-manager-test.sh`를 실행한다.
- 설치 검증은 실제 사용자 홈이 아닌 임시 `HOME`에서 수행한다.
- 기존 사용자 Skill을 대상으로 수동 테스트하지 않는다.
- 보조 문서는 한글로 작성한다.
