#!/bin/bash

hiashi() {
    echo '**日足データを取得します**'

    while :
    do
        echo '取得データ年月日を入力して下さい(YYYYMMDD)'
        read START
        PAT=$(echo $START | egrep '^[1-9][0-9][0-9][0-9](0|1)[0-9][0-3][0-9]$')
        if [ "$PAT" = "" ]; then
            echo '正しい日付を入力して下さい(YYYYMMDD)'
            continue
        else
            break
        fi
    done

}

# 月足(0) 全件取得
mon_all() {
    echo "全期間を取得します"
}

# 月足(1) YYYYMM-YYYYMM
mon_yyyymm() {
    echo "YYYYMM~YYYYMM"
}

# 月足(2) ◯ヶ月前〜YYYYMM
mon_bm_yyyymm() {
    echo "** months ~ YYYYMM"
}

# 月足(3) ◯年前〜YYYYMM
mon_by_yyyymm() {
    echo "** years ~ YYYYMM"
}

#月足(4) 最古-YYYYMM
mon_min_yyyymm() {
    echo "Min ~ YYYYMM"
}

#月足(5) YYYYMM〜◯ヶ月後
mon_am_yyyymm() {
    echo "YYYYMM ~ ** months"
}

#月足(6) YYYYMM〜◯年後
mon_ay_yyyymm() {
    echo "YYYYMM ~ ** years"
}

#月足(7) YYYYMM〜最新
mon_max_yyyymm() {
    echo "YYYY ~ Max"
}

# 月足区分
getsuashi() {
    while :
    do
        echo '月足データを取得します'
        echo '取得したいデータの範囲を選んで下さい'
        echo '0) 全件'
        echo '1) YYYYMM〜YYYYMM'
        echo '2) ◯ヶ月前〜YYYYMM'
        echo '3) ◯年前〜YYYYMM'
        echo '4) OLDEST〜YYYYMM'
        echo '5) YYYYMM〜◯ヶ月後'
        echo '6) YYYYMM〜◯年後'
        echo '7) YYYYMMDD〜最新'

        read TERM

        PAT=$(echo $TERM | egrep '^[0-7]$')
        if [ "$PAT" = "" ]; then
            echo "入力内容が間違っています。"
            echo ""
            continue
        else
            break
        fi
    done

    case "$PAT" in
        "0" ) mon_all ;;
        "1" ) mon_yyyymm ;;
        "2" ) mon_bm_yyyymm ;;
        "3" ) mon_by_yyyymm ;;
        "4" ) mon_min_yyyymm ;;
        "5" ) mon_am_yyyymm ;;
        "6" ) mon_ay_yyyymm ;;
        "7" ) mon_max_yyyymm ;;
    esac
}

YFK_DIR=$(cd $(dirname $0); pwd)

# データ取得パラメータを収集

while :
do
    echo '0) 日足 1) 月足 q) プログラム終了'
    read DATA_DIV
    if [ "$DATA_DIV" != '0' -a "$DATA_DIV" != '1' -a "$DATA_DIV" != "q" -a "$DATA_DIV" != "Q" ]; then
        echo '入力データが間違ってます'
        continue
    else
        break
    fi
done

if [ "$DATA_DIV" = "0" ]; then
    PY_SCRIPT=$YFK_DIR/daily.py
    hiashi
elif [ "$DATA_DIV" = "1" ]; then
    PY_SCRIPT=$YFK_DIR/run.py
    getsuashi
elif [ "$DATA_DIV" = "q" -o "$DATA_DIV" = "Q" ]; then
    exit 0
else
    echo "** 異常終了 **"
    exit 1
fi

# echo '終了しました'
# exit    # とりあえずPythonスクリプトは起動しないでおく

source $HOME/yfkenv/venv/bin/activate
# pip install --upgrade yfk/proj/dist/yfk-*.*.*-py3-none-any.whl

if [ "$DATA_DIV" = "0" ]; then
    python $PY_SCRIPT $PAT
elif [ "$DATA_DIV" = "1" ]; then
    python $PY_SCRIPT
fi

deactivate
