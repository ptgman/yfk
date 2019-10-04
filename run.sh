#!/bin/bash

hiashi() {
    echo '**日足データを取得します**'

    while :
    do
        while :
        do
            echo '開始年月日を入力して下さい(YYYYMMDD)'
            read START
            PAT=$(echo $START | egrep '^[1-9][0-9][0-9][0-9](0|1)[0-9][0-3][0-9]$')
            if [ "$PAT" = "" ]; then
                echo '正しい日付を入力して下さい(YYYYMMDD)'
                continue
            else
                break
            fi
        done

        while :
        do
            echo '終了年月日を入力して下さい(YYYYMMDD)'
            read END
            PAT=$(echo $END | egrep '^[1-9][0-9][0-9][0-9](0|1)[0-9][0-3][0-9]$')
            if [ "$PAT" = "" ]; then
                echo '正しい日付を入力して下さい(YYYYMMDD)'
                continue
            else
                break
            fi
        done

        # 日付の大小チェック
        if [ $START -gt $END ]; then
            echo '開始日付が終了日付より大きくなっています'
            echo 'もう一度やり直して下さい'
            echo ''
            continue
        else
            break
        fi
    done

    echo "${START}〜${END}を取得します"
}

getsuashi() {
    echo '月足データを取得します'
    echo '取得したいデータの範囲を選んで下さい'
    echo '0) 全件'
    echo '1) YYYYMM〜YYYYMM'
    echo '2) ◯ヶ月前〜YYYYMM'
    echo '3) ◯年前〜YYYYMM'
    echo '4) OLDEST〜YYYYMM'
    echo '5) YYYYMM〜◯ヶ月後'
    echo '6) YYYYMMDD〜最新'

    read TERM

    echo "${TERM}を選択しました"
}

YFK_DIR=$(cd $(dirname $0); pwd)

# データ取得パラメータを収集

while :
do
    echo '0) 日足 1) 月足'
    read DATA_DIV
    if [ $DATA_DIV -ne '0' -a $DATA_DIV -ne '1' ]; then
        echo '入力データが間違ってます'
        continue
    else
        break
    fi
done

if [ $DATA_DIV -eq 0 ]; then
    hiashi
elif [ $DATA_DIV -eq 1 ]; then
    getsuashi
fi

echo '終了しました'
exit    # とりあえずPythonスクリプトは起動しないでおく

source $HOME/yfkenv/venv/bin/activate
# pip install --upgrade yfk/proj/dist/yfk-*.*.*-py3-none-any.whl

PY_SCRIPT=$YFK_DIR/run.py
python $PY_SCRIPT
deactivate
