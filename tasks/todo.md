# toamto-ux-tester 스킬 업데이트

- [x] 기존 스킬과 요청 명세의 차이를 정리한다.
- [x] 초기 평가 보고서 → 사용자 확인 → 개선 → 동일 보고서 업데이트 흐름을 반영한다.
- [x] 보고서 파일명을 `REPORT-{yy-mm-dd}.html`로 변경하고 보고서 구성을 보완한다.
- [x] 스킬 구조, placeholder, 참조 경로와 명명 규칙을 검증한다.

## 리뷰

- 기존 스킬은 10개 평가 기준과 severity 분류를 이미 충족했다. 초기 보고서 이후 사용자 승인을 기다리는 중단점과 날짜형 파일명 규칙이 빠져 있어 이를 보완했다.
- 보고서 템플릿에 평가 방법, 점수 시각화, 장점·단점·개선 권고, 코드 수준 수정 포인트를 명시적으로 추가했다.
- 공식 `quick_validate.py`는 로컬 `PyYAML` 부재로 실행할 수 없었다. 같은 frontmatter·이름·description·TODO 조건을 Ruby 기본 YAML 파서로 검증했고, 템플릿 태그 균형·ID 참조·필수 placeholder와 `git diff --check`를 확인했다.

# toamto-ux-tester 이름 변경

- [x] 스킬 디렉터리를 `toamto-ux-tester`로 변경한다.
- [x] frontmatter와 저장소 내 기존 이름 참조를 새 이름으로 변경한다.
- [x] 디렉터리명과 Skill 이름 일치 및 기존 이름 제거를 검증한다.

## 리뷰

- Skill 디렉터리를 `skills/toamto-ux-tester/`로 변경하고 frontmatter의 `name`도 동일하게 맞췄다.
- 저장소의 문서, 파일 경로와 symbolic link 대상에서 이전 이름이 남아 있지 않음을 확인했다.
- Ruby YAML 파서로 새 이름의 형식과 디렉터리 일치를 확인하고 `git diff --check`를 통과했다.

# tomato-style-setter 이름 변경

- [x] 스킬 디렉터리를 `tomato-style-setter`로 변경한다.
- [x] frontmatter와 저장소 내 기존 이름 참조를 새 이름으로 변경한다.
- [x] 디렉터리명과 Skill 이름 일치 및 기존 이름 제거를 검증한다.

## 리뷰

- Skill 디렉터리와 `SKILL.md`의 `name`을 `tomato-style-setter`로 통일했다.
- 저장소의 문서, 파일 경로와 symbolic link 대상에서 이전 이름이 남아 있지 않음을 확인했다.
- Ruby YAML 파서로 이름 형식과 디렉터리 일치를 확인하고, 세 개의 상대 참조 및 `git diff --check`를 검증했다.

# 변경사항 커밋 및 태그

- [x] 현재 변경 범위와 검증 상태를 최종 확인한다.
- [x] 전체 변경사항을 커밋한다.
- [x] 다음 마이너 버전 태그 `v0.2.0`을 생성하고 커밋·태그를 검증한다.

## 리뷰

- 두 Skill의 이름·참조와 HTML 템플릿 구조를 검증하고 저장소의 현재 변경사항 전체를 커밋 대상으로 확정했다.
- 변경 유형과 기존 `v0.1.0` 태그 규칙을 기준으로 커밋 메시지는 `feat: UX 스킬 이름 및 보고서 흐름 정비`, 태그는 annotated `v0.2.0`으로 정했다.
