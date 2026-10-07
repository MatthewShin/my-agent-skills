# 개발 규칙

## Skill 작성

- Skill은 `skills/<skill-name>/SKILL.md`를 진입점으로 사용한다.
- 디렉터리 이름과 frontmatter의 `name`은 일치시킨다.
- 이름에는 소문자 영문자, 숫자, 하이픈만 사용한다.
- 새로 추가하는 Skill 이름에는 `tomato-` 접두사를 붙인다.
- frontmatter에는 최소한 `name`과 `description`을 작성한다.
- 스크립트, 참고 문서, 자산은 실제로 필요할 때만 추가한다.
- 공통 Skill에는 특정 제품에만 존재하는 도구명이나 호출 문법을 직접 포함하지 않는다.

## 구현

- 요청을 충족하는 최소 범위로 변경한다.
- 단순하고 읽기 쉬운 구현을 우선하며 임시방편을 남기지 않는다.
- 리팩터링에서는 기존 동작을 유지한다.
- `bin/skill-manager`는 macOS와 Linux의 POSIX `sh`에서 동작해야 한다.
- 절대경로, 비밀키, 토큰, 패스워드, 개인 인증 정보를 저장소에 기록하지 않는다.

## 작업 기록

- 새 요청은 `tasks/TODO.md`에 미완료 체크 항목으로 등록한다.
- 완료한 작업은 `docs/COMPLETE.md`로 이관한다.
- 반복 방지를 위한 교훈과 사용자 피드백은 `docs/LESSONS.md`에 기록한다.
- 사용자와 Agent가 함께 참조하는 보조 문서는 한글로 작성한다.

## Git

- 커밋 메시지는 Conventional Commits 형식을 따른다.
- 태그는 Semantic Versioning에 맞춘다.
- Agent가 커밋하면 마지막에 Agent와 모델의 `Co-Authored-By` trailer를 추가한다.
