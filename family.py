"""What this family scrapes: every public page and document on the websites of city agencies.

One project per site, on the pool's India servers (geo="IN"). The queue starts at the home page and grows: crawl.py adds each new link it
finds on the same site. Add a city by adding its rows to SITES. The first word of the slug is the city.
"""
import json
from pathlib import Path

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
    ("knp-kda", "kdaonline.in", "Kanpur Development Authority", "kanpur"),
]

PROJECTS = [
    {
        "name": f"{FAMILY}-{slug}",
        "title": title,
        "task": "crawl",
        "target": host,
        "env": {"SITE": host},
        "probe": f"{FAMILY}:{host}",
        "unit_label": "url", "record_label": "page or document",
        "items": [{"key": "start", "payload": {"url": f"https://{host}/", "depth": 0}}],
        "workers": 2,
        "delay_ms": 1000,
    }
    for slug, host, title, _ in SITES
]

PROBES = [{"name": f"{FAMILY}:{host}", "url": f"https://{host}/", "expect": text} for _, host, _, text in SITES]
