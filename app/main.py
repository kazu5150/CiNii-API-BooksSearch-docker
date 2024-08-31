import sys
import io
import locale
import requests
import pandas as pd
import json
import urllib.parse


# 標準入出力のエンコーディングをUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# ロケールを'C.UTF-8'に設定し、文字化けを防ぐ
locale.setlocale(locale.LC_ALL, 'C.UTF-8')

# CiNii Articles APIのエンドポイントURL
CINII_API_URL = 'http://cir.nii.ac.jp/opensearch/articles'
# CINII_API_URL = 'https://cir.nii.ac.jp/openurl/query'


def search_cinii(keyword):
    """
    CiNii Articles APIを使用して、指定されたキーワードで論文を検索する

    :param keyword: 検索キーワード
    :return: API応答のJSONデータ

    dockerコマンド:
    docker-compose run --rm app
    $(python -c "import urllib.parse;
    print(urllib.parse.quote('検索キーワード'))")

    """

    params = {
        'q': keyword,
        'format': 'json',
        'sortorder': '0',
        'count': 100  # 取得件数（最大100）
    }

    # APIリクエストを送信
    response = requests.get(CINII_API_URL, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:500]}...")  # レスポンス内容の最初の500文字を表示
    print(f"Response Headers: {response.headers}")

    # HTTPエラーがあれば例外を発生させる
    response.raise_for_status()
    return response.json()


def main():
    # コマンドライン引数のチェック
    if len(sys.argv) < 2:
        print("使用方法: python main.py <検索キーワード>")
        sys.exit(1)

    # URLエンコードされたキーワードをデコード
    keyword = sys.argv[1]
    keyword = urllib.parse.unquote(keyword)
    print(f"受け取ったキーワード: {keyword}")

    try:
        # CiNii Articles APIで検索を実行
        results = search_cinii(keyword)

        # 検索結果をDataFrameに変換
        df = pd.json_normalize(results['items'])

        # 利用可能な列を表示
        print("利用可能な列:")
        print(df.columns)

        # 必要な列を選択
        available_columns = ['title']
        for col in ['dc:creator', 'prism:publicationDate', 'link.@id']:
            if col in df.columns:
                available_columns.append(col)

        df = df[available_columns]

        # 結果をExcelファイルとして保存
        output_file = f'/app/output/{keyword}_results.xlsx'
        df.to_excel(output_file, index=False)
        print(f"検索結果を {output_file} に保存しました。")
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラー: {e}")
    except Exception as e:
        print(f"予期せぬエラー: {e}")


if __name__ == "__main__":
    main()
