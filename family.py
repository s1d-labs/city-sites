"""What this family scrapes: every public page and document on the websites of city agencies.

One project per site, on GitHub runners: direct, or through the hub's Mumbai proxies (proxy="IN") for the hosts in PROXY_IN that
refuse GitHub's runners. The queue starts at the home page and grows: crawl.py adds each new link it
finds on the same site. Add a city by adding its rows to SITES. The first word of the slug is the city. Sites with a login, a captcha
or a search form behind them are crawled only as far as plain links go.
"""
import json
from pathlib import Path

from sitecrawl import key_of

FAMILY = json.loads((Path(__file__).parent / "scrape.json").read_text())["family"]

# slug, host, title, text that the home page always holds (for the health check)
SITES = [
    ("chd-mc", "mcchandigarh.gov.in", "Municipal Corporation Chandigarh", "chandigarh"),
    ("chd-admin", "chandigarh.gov.in", "Chandigarh Administration", "chandigarh"),
    ("chd-engineering", "chdengineering.gov.in", "Chandigarh Engineering Department", "engineering"),
    ("chd-housing", "chbonline.in", "Chandigarh Housing Board", "housing"),
    ("chn-gcc", "chennaicorporation.gov.in", "Greater Chennai Corporation", "chennai"),
    ("chn-cmda", "www.cmdachennai.gov.in", "Chennai Metropolitan Development Authority", "chennai"),
    ("chn-water", "cmwssb.tn.gov.in", "Chennai Metro Water", "water"),
    ("pun-pmc", "www.pmc.gov.in", "Pune Municipal Corporation", "pune"),
    ("pun-open", "opendata.pmc.gov.in", "Pune open data portal", "pune"),
    ("pun-pcmc", "www.pcmcindia.gov.in", "Pimpri Chinchwad Municipal Corporation", "pcmc"),
    ("pun-pmrda", "www.pmrda.gov.in", "Pune Metropolitan Region Development Authority", "pmrda"),
    ("mum-bmc", "portal.mcgm.gov.in", "Brihanmumbai Municipal Corporation", "municipal"),
    ("mum-mmrda", "mmrda.maharashtra.gov.in", "Mumbai Metropolitan Region Development Authority", "mmrda"),
    ("mum-msrdc", "www.msrdc.org", "Maharashtra State Road Development Corporation", "road"),
    ("knp-kmc", "kmc.up.nic.in", "Kanpur Nagar Nigam", "kanpur"),
    ("knp-kda", "www.kdaindia.co.in", "Kanpur Development Authority", "kanpur"),
]

# Delhi agencies, from the former family delhi-sites (merged here 2026-11-12). Their projects keep the names delhi-sites-<slug> and
# their health checks delhi-sites:<host>: the records, queues and bucket files collected under those names stay theirs.
DELHI_PREFIX = "delhi-sites"
DELHI = [
    ("delhi", "delhi.gov.in", "Government of NCT of Delhi", "delhi"),
    ("finance", "finance.delhi.gov.in", "Delhi Finance Department", "finance"),
    ("ifc", "ifc.delhi.gov.in", "Delhi Irrigation and Flood Control", "flood"),
    ("djb", "delhijalboard.delhi.gov.in", "Delhi Jal Board", "jal board"),
    ("transport", "transport.delhi.gov.in", "Delhi Transport Department", "transport"),
    ("ceo", "ceodelhi.gov.in", "Chief Electoral Officer, Delhi", "election"),
    ("sec", "sec.delhi.gov.in", "State Election Commission, Delhi", "election"),
    ("lokayukta", "lokayukta.delhi.gov.in", "Delhi Lokayukta", "lokayukta"),
    ("vigilance", "vigilance.delhi.gov.in", "Delhi Directorate of Vigilance", "vigilance"),
    ("home", "home.delhi.gov.in", "Delhi Home Department", "home"),
    ("traffic", "traffic.delhipolice.gov.in", "Delhi Traffic Police", "traffic"),
    ("police", "delhipolice.gov.in", "Delhi Police", "police"),
    ("ndmc", "www.ndmc.gov.in", "New Delhi Municipal Council", "ndmc"),
    ("tourism", "delhitourism.gov.in", "Delhi Tourism", "delhi"),
    ("assembly", "delhiassembly.delhi.gov.in", "Delhi Legislative Assembly", "assembly"),
    ("highcourt", "delhihighcourt.nic.in", "Delhi High Court public pages", "high court"),
    ("morth", "morth.gov.in", "Ministry of Road Transport and Highways", "road"),
    ("mcd", "mcdonline.nic.in", "Municipal Corporation of Delhi", "portal"),
    ("udd", "udd.delhi.gov.in", "Delhi Urban Development Department, with MLA fund orders", "urban"),
    ("uttipec", "uttipec.org.in", "UTTIPEC, DDA road design body", "uttipec"),
    ("dsiidc", "dsiidc.delhi.gov.in", "Delhi State Industrial and Infrastructure Development Corporation", "dsiidc"),
]
# Hosts that refuse GitHub's runners (owner's front-page test, 2026-11-12): their work goes through the hub's Mumbai proxies. Every other
# host answers GitHub's runners directly. The India pool servers (geo="IN") are not used since 2026-11-12.
PROXY_IN = {"mcchandigarh.gov.in", "chdengineering.gov.in", "www.cmdachennai.gov.in", "cmwssb.tn.gov.in", "www.pcmcindia.gov.in",
            "ceodelhi.gov.in", "delhipolice.gov.in"}
PROXY_ONLY = {"www.pcmcindia.gov.in": ["91.124.42.", "95.134.119."]}     # pcmcindia answers only these proxy ranges (in-06/07, in-08..10)

# the MLA fund orders (MLALAD) of Delhi Urban Development, listed by year on pages that a plain link crawl does not reach
UDD_ORDERS = [u for u in (Path(__file__).parent / "udd_orders.txt").read_text().split("\n") if u]


def _project(prefix, slug, host, title):
    delhi = prefix == DELHI_PREFIX
    start = f"https://{host}/portal" if delhi and slug == "mcd" else f"https://{host}/"
    items = [{"key": "start", "payload": {"url": start, "depth": 0}}]
    if delhi and slug == "udd":
        items += [{"key": key_of(u), "payload": {"url": u, "depth": 12}} for u in UDD_ORDERS]
    return {
        "name": f"{prefix}-{slug}",
        "title": title,
        "task": "crawl",
        "target": host,
        "env": {"SITE": host},
        "probe": f"{prefix}:{host}",
        "unit_label": "url", "record_label": "page or document",
        "items": items,
        "workers": 2,
        "proxy": "IN" if host in PROXY_IN else "",
        "proxy_only": PROXY_ONLY.get(host, []),
        "delay_ms": 2000 if delhi and slug == "udd" else 1000,
    }


ROWS = [(FAMILY, s) for s in SITES] + [(DELHI_PREFIX, s) for s in DELHI]
PROJECTS = [_project(prefix, slug, host, title) for prefix, (slug, host, title, _) in ROWS]
PROBES = [{"name": f"{prefix}:{host}", "url": f"https://{host}/", "expect": text} for prefix, (_, host, _, text) in ROWS]
