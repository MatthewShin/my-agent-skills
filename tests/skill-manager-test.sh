#!/bin/sh

set -eu

fail() {
  printf '실패: %s\n' "$1" >&2
  exit 1
}

assert_link_target() {
  link_path=$1
  expected=$2
  [ -L "$link_path" ] || fail "symbolic link가 아닙니다: $link_path"
  actual=$(readlink "$link_path")
  [ "$actual" = "$expected" ] || fail "링크 대상이 다릅니다: $link_path"
}

TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/skill-manager-test.XXXXXX")
TEST_ROOT=$(CDPATH= cd -- "$TEST_ROOT" 2>/dev/null && pwd -P)
trap 'rm -rf "$TEST_ROOT"' EXIT HUP INT TERM

TEST_REPO=$TEST_ROOT/'agent skills repo'
TEST_HOME=$TEST_ROOT/home
mkdir -p "$TEST_REPO/bin" "$TEST_REPO/skills/sample-skill" "$TEST_HOME"
cp "$(dirname "$0")/../bin/skill-manager" "$TEST_REPO/bin/skill-manager"

printf '%s\n' \
  '---' \
  'name: sample-skill' \
  'description: 테스트용 portable Skill이다.' \
  '---' \
  '' \
  '# Sample Skill' \
  > "$TEST_REPO/skills/sample-skill/SKILL.md"

HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" install
assert_link_target "$TEST_HOME/.claude/skills/sample-skill" "$TEST_REPO/skills/sample-skill"
assert_link_target "$TEST_HOME/.codex/skills/sample-skill" "$TEST_REPO/skills/sample-skill"

HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" install
HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" doctor
HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" list | grep 'sample-skill' >/dev/null

mkdir -p "$TEST_REPO/skills/conflict-skill"
printf '%s\n' \
  '---' \
  'name: conflict-skill' \
  'description: 충돌 보존을 확인하는 Skill이다.' \
  '---' \
  > "$TEST_REPO/skills/conflict-skill/SKILL.md"
printf '%s\n' '기존 사용자 파일' > "$TEST_HOME/.claude/skills/conflict-skill"

if HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" install; then
  fail '기존 파일 충돌에서 install이 성공했습니다.'
fi
[ "$(sed -n '1p' "$TEST_HOME/.claude/skills/conflict-skill")" = '기존 사용자 파일' ] || fail '기존 파일이 변경되었습니다.'
assert_link_target "$TEST_HOME/.codex/skills/conflict-skill" "$TEST_REPO/skills/conflict-skill"

mkdir -p "$TEST_ROOT/foreign-skill"
ln -s "$TEST_ROOT/foreign-skill" "$TEST_HOME/.claude/skills/foreign-skill"

HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" unlink
[ ! -e "$TEST_HOME/.claude/skills/sample-skill" ] || fail 'Claude 링크가 제거되지 않았습니다.'
[ ! -e "$TEST_HOME/.codex/skills/sample-skill" ] || fail 'Codex 링크가 제거되지 않았습니다.'
[ -f "$TEST_HOME/.claude/skills/conflict-skill" ] || fail '기존 충돌 파일이 제거되었습니다.'
[ -L "$TEST_HOME/.claude/skills/foreign-skill" ] || fail '외부 링크가 제거되었습니다.'

mkdir -p "$TEST_REPO/skills/missing-entry"
if HOME=$TEST_HOME "$TEST_REPO/bin/skill-manager" doctor 2>"$TEST_ROOT/doctor-error.log"; then
  fail 'SKILL.md가 없는 디렉터리에서 doctor가 성공했습니다.'
fi
grep 'SKILL.md가 없습니다' "$TEST_ROOT/doctor-error.log" >/dev/null || fail '누락된 SKILL.md 진단이 없습니다.'

printf '%s\n' '모든 skill-manager 테스트를 통과했습니다.'
