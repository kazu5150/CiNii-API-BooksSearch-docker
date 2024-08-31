# CiNii Articles 検索ツール

このプロジェクトは、CiNii Articles APIを使用して学術論文を検索し、結果をExcelファイルとして保存するツールです。Docker環境を使用しているため、簡単にセットアップして実行することができます。

# CiNii サポートページ
https://support.nii.ac.jp/ja/cir/r_opensearch

## 機能

- CiNii Articles APIを使用して論文を検索
- 検索結果をExcelファイルとして保存
- Docker環境での簡単な実行

## 必要条件

- Docker
- Docker Compose

## セットアップ

1. このリポジトリをクローンします：

git clone https://github.com/yourusername/cinii-search-tool.git
cd cinii-search-tool

2. Dockerイメージをビルドします：

docker-compose build

## 使用方法

1. 以下のコマンドを使用して検索を実行します：

docker-compose run --rm app $(python -c "import urllib.parse; print(urllib.parse.quote('検索キーワード'))")

例えば、「人工知能」で検索する場合：

docker-compose run --rm app $(python -c "import urllib.parse; print(urllib.parse.quote('人工知能'))")

2. 検索結果は `output` ディレクトリに保存されます。ファイル名は `検索キーワード_results.xlsx` となります。

## Docker Composeの使い方

- イメージのビルド：
  docker-compose build

- アプリケーションの実行：
  docker-compose run --rm app $(python -c "import urllib.parse; print(urllib.parse.quote('検索キーワード'))")

- コンテナとネットワークの削除：
  docker-compose down

## 注意事項

- CiNii Articles APIの利用規約を遵守してください。
- 大量のリクエストを短時間に行うと、APIからのレスポンスが制限される可能性があります。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 貢献

バグ報告や機能リクエストは、GitHubのIssueを使用してください。プルリクエストも歓迎します。

