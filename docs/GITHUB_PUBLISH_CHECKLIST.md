# GitHub publishing checklist

- [ ] Check dataset redistribution permissions; remove restricted data if needed.
- [ ] Confirm author/copyright owner and choose an appropriate LICENSE; do not publish draft license unchanged.
- [ ] Scan for credentials, access tokens, email addresses, and personal data.
- [ ] Verify paper bibliography against publisher records.
- [ ] Confirm annotation status and do not claim AI labels are human-verified.
- [ ] Test generation/evaluation on a clean environment; document observed commands/logs.
- [ ] Add GitHub URL to submission.

## Git push from extracted folder

```bash
git init
git add .
git commit -m "Add research implementation and evidence"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

These are instructions, **not commands executed by the assistant**.
