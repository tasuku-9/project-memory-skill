# Privacy Task

Use this when continuity docs may include sensitive information.

## Sensitive material examples

- API keys, tokens, credentials
- personal information
- private contracts or legal documents
- proprietary source text
- unpublished research data
- private abstracts or datasets
- medical, financial, or legal details
- confidential client or employer information

## Rules

- Do not copy secrets into canonical docs.
- Summarize sensitive facts when possible.
- Put private material in `private/` only when needed.
- Add `private/` to `.gitignore` and `.contextignore`.
- In handoffs, say what was omitted and why.
- Avoid copying long copyrighted source text into logs.

## Safe summary pattern

```md
Private source material was reviewed but not copied here. Relevant non-sensitive summary:

- finding:
- confidence:
- limitation:
- private source location, if appropriate:
```

## Audit checklist

- canonical docs contain no credentials
- private folders are ignored
- handoff brief omits sensitive details
- research entries summarize restricted sources rather than reproducing them
- generated logs with private content are not treated as context by default
