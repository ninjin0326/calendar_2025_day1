#!/bin/bash
# 全課題の動作確認スクリプト
# 実行方法: サーバーを起動した状態で cd backend && sh ./scripts/test_all_features.sh

echo "=== バックエンド課題検証スクリプト ==="
echo ""

# カラー定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# テスト結果カウンタ
PASSED=0
FAILED=0

# テスト結果を記録する関数
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ $2${NC}"
        ((FAILED++))
    fi
}

echo "1. pytest による全課題の検証を実行"
echo "=================================="
pytest tests/test_all_tasks.py -v
check_result $? "pytest による課題検証"
echo ""

echo "2. 個別課題の詳細テスト"
echo "======================"

echo ""
echo "課題1: ジャンルフィルタ機能"
echo "--------------------------"
pytest tests/test_all_tasks.py::TestTask1GenreFilter -v --tb=short
check_result $? "ジャンルフィルタ機能テスト"

echo ""
echo "課題2: ユーザータイムスタンプ機能"
echo "--------------------------------"
pytest tests/test_all_tasks.py::TestTask2UserTimestamp -v --tb=short
check_result $? "ユーザータイムスタンプ機能テスト"

echo ""
echo "課題3: APIエラーメッセージ統一"
echo "-----------------------------"
pytest tests/test_all_tasks.py::TestTask3ErrorMessageUnification -v --tb=short
check_result $? "APIエラーメッセージ統一テスト"

echo ""
echo "課題4: イベント重複チェック機能"
echo "------------------------------"
pytest tests/test_all_tasks.py::TestTask4EventOverlapCheck -v --tb=short
check_result $? "イベント重複チェック機能テスト"

echo ""
echo "課題5: イベント継続時間計算機能"
echo "------------------------------"
pytest tests/test_all_tasks.py::TestTask5EventDurationCalculation -v --tb=short
check_result $? "イベント継続時間計算機能テスト"

echo ""
echo "課題6: APIヘルスチェック機能"
echo "---------------------------"
pytest tests/test_all_tasks.py::TestTask6HealthCheck -v --tb=short
check_result $? "APIヘルスチェック機能テスト"

echo ""
echo "=================================="
echo -e "テスト結果: ${GREEN}成功: $PASSED${NC} / ${RED}失敗: $FAILED${NC}"
echo "=================================="

# テストがすべて成功した場合は0、失敗がある場合は1を返す
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}すべての課題が正しく実装されています！${NC}"
    exit 0
else
    echo -e "${RED}いくつかの課題に問題があります。上記のエラーメッセージを確認してください。${NC}"
    exit 1
fi