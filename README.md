# city-sites

This family collects the public pages and documents of city agency websites for the city road ledgers.

- Add a site: add a row to `SITES` in `family.py`.
- Delhi sites (`DELHI` in `family.py`) came from the former family `delhi-sites` (merged 2026-11-12). Their projects keep the names
  `delhi-sites-<slug>`, so the records collected before the merge stay with them. Urban Development (`udd`) also seeds the MLA fund
  orders from `udd_orders.txt`, at 1 request every 2 seconds per worker.
- The sites answer from India, so the projects use `geo="IN"`: India pool servers only. 2 workers per site, 1 request per second per worker.
- No login, captcha or OTP is passed. Search forms are not filled.
- Tests: `python -m pytest tests` (saved page in `tests/pages/`). The `check` workflow runs them and scrape-check on every push.
- `certs/` holds public intermediate certificates that some sites fail to send. Certificate verification stays on.
