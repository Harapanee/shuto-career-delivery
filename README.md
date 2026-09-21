# shuto-career-delivery

@shuto.career のリール配信用。制作は別リポジトリ。

## Threads 自動投稿(2026-09-22 追加)

`threads_schedule.json` の items を 7:00 / 12:30 / 21:00 JST に `threads_publish.yml` が出す。
記録は `threads_state.json`。スクリプトは `publish/threads_client.py` / `publish/threads_publish.py`。
Secrets: `THREADS_ACCESS_TOKEN`(長期60日・要更新)/ `THREADS_USER_ID`。
item の形: `{"key","publish_at","text","image_url"(任意),"reply_text"(任意=自己リプ)}`。画像は `docs/media/` の raw URL。
