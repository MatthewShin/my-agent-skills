# 완료 작업

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
