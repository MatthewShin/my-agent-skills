# 완료 작업

## 2026-09-03 tomato-commit-report 스킬 생성

- 하나 이상의 SHA, tag, branch를 commit 단위로 분석해 단일 `COMMIT-REPORT.html`에 커밋별 섹션으로 정리하는 Skill을 추가했다.
- 부모 대비 diff, root commit, merge commit의 첫 번째 부모 비교, 중복 revision 제거와 기존 산출물 보호 기준을 명시했다.
- 변경 요약, 파일별 통계, Before / After, 영향 분석, 핵심 hunk, 회귀 위험과 제한사항을 포함하는 오프라인 반응형 HTML 템플릿을 추가했다.
- Skill 이름·frontmatter·템플릿 placeholder·외부 리소스 부재와 `git diff --check`를 확인했다. 제공된 `quick_validate.py`는 로컬 `PyYAML` 부재로 실행하지 못했다.

## 2026-09-03 tomato-commit-report 스킬 이름 변경

- Skill의 디렉터리명과 frontmatter `name`을 `tomato-commit-report`로 변경했다.
- 이후 새 Skill 이름에 `tomato-` 접두사를 붙이도록 프로젝트 운영 규칙과 학습 기록을 갱신했다.

## 2026-08-21 문서 구조 변경 배포 준비

- 현재 변경 범위와 문서 검증 결과를 확인했다.
- 변경사항을 `docs: 프로젝트 문서 구조 정비` 커밋과 `v0.3.1` annotated tag 대상으로 확정했다.
- 커밋과 태그 생성 후 두 참조가 같은 변경사항을 가리키도록 검증하기로 했다.

## 2026-08-21 프로젝트 문서 구조 정비

- 루트의 `AGENTS.md`, `CLAUDE.md`, `README.md` 역할과 연결을 정비했다.
- `docs/` 필수 문서에 아키텍처, 설계, 규칙, 검증, 학습과 완료 이력을 기록했다.
- 기존 `tasks/todo.md`의 완료 기록과 `tasks/lessons.md`의 학습 기록을 지정 문서로 이관했다.
- `tasks/TODO.md`를 진행 중인 작업만 관리하는 목록으로 정리했다.
- 필수 파일과 문서 참조를 확인하고 `git diff --check`를 통과했다.

## 2026-08-21 이전 작업

### toamto-ux-tester 스킬 업데이트

- 초기 평가 보고서, 사용자 확인, 개선, 동일 보고서 업데이트 흐름을 반영했다.
- 보고서 파일명을 `REPORT-{yy-mm-dd}.html`로 정하고 평가 방법, 점수 시각화, 장단점, 개선 권고와 코드 수정 지점을 보완했다.
- frontmatter, 이름, 참조, 템플릿 구조와 필수 placeholder를 검증했다.

### UX Skill 이름 정비

- Skill 디렉터리와 frontmatter 이름을 각각 `toamto-ux-tester`, `tomato-style-setter`로 통일했다.
- 문서, 파일 경로와 symbolic link 대상에 이전 이름이 남지 않았음을 확인했다.

### tomato-review-quiz 스킬 생성

- 변경 복잡도에 따른 1~6문제 출제, 즉시 피드백, 오답 재출제와 Skip 처리 흐름을 작성했다.
- Skip 시 생성하는 `REVIEW.html` 템플릿을 추가하고 구조, 상대 참조와 필수 내용을 검증했다.

### 커밋 및 배포 이력

- UX Skill 변경을 `v0.2.0`, Review Quiz Skill 추가를 `v0.3.0` annotated tag로 관리했다.
- `main`, `v0.2.0`, `v0.3.0`의 원격 반영 상태를 검증했다.
