# project-memory 日本語概要

English: [README.md](README.md)

project-memory は、AI エージェントとの長期開発・研究で失われがちな
「意思決定の理由」「仮説」「実験結果」「再開メモ」を、
役割ごとに分けた Markdown ファイルとして残すための Agent Skill です。

チャットが消えても、モデルを切り替えても、次のセッションや別の担当者が
同じ前提から再開しやすくなります。

## 何を解決するか

- チャットが消えて文脈が失われる
- なぜその判断をしたか分からなくなる
- 未検証の仮説がいつの間にか事実扱いされる
- 実験結果や失敗した試行が残らない
- 研究や論文執筆で文献メモ、仮説、本文前提が混ざる

## 特徴

- `CURRENT_STATE.md` に現在の前提と現在地を保存
- `DECISION_LOG.md` に意思決定と理由を保存
- `RESEARCH_LOG.md` に実験、調査、観察、根拠を保存
- `HYPOTHESIS_LAB.md` に未検証の着想や仮説を保存
- 仮説を事実に昇格させるための promotion rules がある
- `HUMAN_BRIEF.md` と `RECOVERY_NOTES.md` で人間や次のモデルがすぐ再開できる
- Codex / Claude Code / Gemini CLI / Cursor などでの利用を想定

## 主なファイル

| ファイル | 役割 |
| --- | --- |
| `CURRENT_STATE.md` | 今の確定事項 |
| `ROADMAP.md` | 今後の予定 |
| `DECISION_LOG.md` | 決定事項と理由 |
| `RESEARCH_LOG.md` | 実験、検証、観察、調査結果 |
| `HYPOTHESIS_LAB.md` | 未検証の仮説や着想 |
| `HUMAN_BRIEF.md` | 人間向けの短い要約 |
| `RECOVERY_NOTES.md` | 中断後に再開するためのメモ |
| `CONTEXT_MANIFEST.md` | 読む順番、信頼源、ignore ルール |
| `DOCS_GUIDE.md` | どの情報をどこへ書くか |

## Profiles

- `light`: 小さな個人プロジェクト向け
- `standard`: 一般的な長期開発向け
- `research`: 実験や調査のログを重視する研究向け
- `academic`: 論文、卒論、研究計画で文献メモや図表管理まで含めたい場合向け

`research` は根拠と confidence を重視し、`academic` はそれに加えて
`LITERATURE_NOTES.md` と `FIGURES_LOG.md` を使います。

## 使い方

新しい memory workspace を作る:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile research
```

小さめのプロジェクト向け:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile standard
```

既存の workspace を監査する:

```bash
python scripts/audit_memory_workspace.py /path/to/project --profile research
```

handoff brief を生成する:

```bash
python scripts/make_handoff_brief.py /path/to/project
```

## Prompt 例

```text
SKILL.md を読んで、このプロジェクトに project-memory を導入してください。
README、既存ドキュメント、git ログを確認し、
情報を各 memory file に分類してください。
```

```text
CONTEXT_MANIFEST.md と RECOVERY_NOTES.md から読み始めて、
今どこまで進んでいて、次に何をすべきか整理してください。
```

```text
この会話で出た事実、仮説、意思決定、次アクションを分類して、
更新が必要な memory files を patch-ready で出してください。
```

## 仮説整理は人間が確認する

`HYPOTHESIS_LAB.md` は、未整理の思いつき、違和感、半熟の仮説を広く拾うためのファイルです。

AI は作業中に raw idea や仮説を追加してよいですが、仮説や raw spark を勝手に削除してはいけません。

整理したいときは、まず `merge` / `promote` / `link to evidence` / `mark as dropped` / `delete` に分けた候補リストを出します。削除、統合、昇格、棄却の判断は人間が行います。

## 言語について

- ユーザーへの説明は日本語でも問題ありません
- ただし、このリポジトリ本体と structured memory docs は英語運用が基本です
- `README.ja.md` は日本語の入口であり、正本は [README.md](README.md) です

## フィードバック歓迎

特に以下を知りたいです。

- ファイル構成が重すぎないか
- 昇格ルールが分かりやすいか
- `research` / `academic` profile が実用的か
- Codex / Claude Code / Gemini CLI / Cursor で自然に動くか

役に立ちそうなら、GitHub Star も励みになります。
