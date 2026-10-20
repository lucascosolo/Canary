# G-02: Legal constraints on fetching, storing, excerpting and assessing (US primary, EU secondary)

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 5 tool uses
- Status: mostly recalled authorities, not re-read; the agent flags each. Not legal advice.

## Answer (verbatim; read 2026-10-20; not legal advice)

Only the CC and UK Defamation Act pages were actually retrieved this session; everything else is from recalled knowledge of well-known authorities and is flagged "recalled, not re-read".

1. Copyright/TDM. US: Authors Guild v. Google, 804 F.3d 202 (2d Cir. 2015) held that scanning books to build a searchable index and showing snippets is transformative fair use and does not substitute for the book. Authors Guild v. HathiTrust, 755 F.3d 87 (2d Cir. 2014) held full-text search and indexing to be fair use. Both rested on limited display; republishing full text is not protected by them (recalled). EU DSM Directive 2019/790 (https://eur-lex.europa.eu/eli/dir/2019/790/oj): Art. 15 gives press publishers a right over online use of press publications by information society service providers. It excludes hyperlinking and "very short extracts" (Art. 15(1)), and lasts two years. Art. 3 is a mandatory TDM exception for research organisations and cultural heritage institutions with lawful access. Art. 4 is a general TDM exception that rightholders can reserve through an "appropriate" machine-readable opt-out (Art. 4(3)). Whether a non-profit qualifies as a research organisation under Art. 2(1) depends on its research purpose and on profit reinvestment or public-interest mission (recalled). UK CDPA s.29A permits copying for text and data analysis for non-commercial research, with lawful access and sufficient acknowledgement (recalled; https://www.legislation.gov.uk/ukpga/1988/48/section/29A).

2. Scraping. hiQ v. LinkedIn, 31 F.4th 1180 (9th Cir. 2022): scraping public pages is likely not "without authorization" under the CFAA. Van Buren v. United States, 593 U.S. 374 (2021), adopted a "gates-up-or-down" reading of "exceeds authorized access", which supports that reading. Contract and ToS claims survive; on remand hiQ lost on breach of contract (recalled). Meta v. Bright Data (N.D. Cal. Jan. 2024) held that Meta's ToS did not bar logged-off scraping of public data (recalled). robots.txt is not itself a legal bar in the US, but it is the usual vehicle for the EU Art. 4 reservation. EU Database Directive 96/9/EC: the sui generis right (Art. 7) needs a substantial investment in obtaining, verifying or presenting contents. Per CJEU British Horseracing Board and Fixtures Marketing, it is unlikely to cover news sites, whose content is created rather than compiled (recalled).

3. Personal data. GDPR Art. 3(2) reaches non-EU controllers that target EU data subjects or monitor their behaviour. A US site that merely names EU officials is arguably not targeting them (recalled; https://eur-lex.europa.eu/eli/reg/2016/679/oj). Art. 85 obliges member states to reconcile data protection with expression, including journalistic and academic purposes. The exemptions differ by state. Art. 89 gives research derogations with safeguards. CCPA, Cal. Civ. Code 1798.140(d): "business" covers for-profit entities only, so a genuine non-profit is outside it unless controlled by or sharing branding with a business (recalled).

4. Defamation. NYT v. Sullivan, 376 U.S. 254 (1964): a public official must prove actual malice. Gertz v. Robert Welch, 418 U.S. 323 (1974): private persons need only negligence, and public figures face actual malice. Milkovich v. Lorain Journal, 497 U.S. 1 (1990): there is no blanket opinion privilege, but statements that are not provably false, or that are based on disclosed facts, are protected. 47 U.S.C. 230(c)(1) shields a site from liability for third-party content, but not for content it creates or develops itself. Machine-extracted claims and the site's own assessments are likely its own speech. England and Wales: Defamation Act 2013 s.1(1) requires publication to have caused or be likely to cause "serious harm" to reputation. s.1(2) requires serious financial loss for bodies trading for profit (https://www.legislation.gov.uk/ukpga/2013/26/section/1, read). s.8 single-publication rule: one-year limitation from first publication (recalled; not retrieved). s.9 limits jurisdiction over non-EU/non-Lugano defendants unless England is clearly the most appropriate forum (recalled).

5. Attribution. CC BY 4.0 s.3(a)(1) (https://creativecommons.org/licenses/by/4.0/legalcode, read) requires identification of the creator, a copyright notice, a license notice, a warranty-disclaimer notice, a URI or link to the material where reasonably practicable, and an indication of any modification. This is the practical "TASL" content. CC BY-NC 4.0 defines NonCommercial as "not primarily intended for or directed towards commercial advantage or monetary compensation". The CC wiki says this turns on the use, not the user's organisation type, and that nonprofits can likely make more uses (https://wiki.creativecommons.org/wiki/NonCommercial_interpretation, read).

## Evidence

- https://wiki.creativecommons.org/wiki/NonCommercial_interpretation — read; NC definition and nonprofit point.
- https://creativecommons.org/licenses/by/4.0/legalcode — read; s.3(a)(1) attribution elements.
- https://www.legislation.gov.uk/ukpga/2013/26/section/1 — read; serious-harm test.
- https://eur-lex.europa.eu/eli/dir/2019/790/oj — fetch returned empty; not read.
- Case citations (Authors Guild, HathiTrust, hiQ, Van Buren, Sullivan, Gertz, Milkovich), GDPR, CCPA, CDPA s.29A, Database Directive — not fetched; recalled.

## Caveats (verbatim)

Most of the above is unverified against primary text in this session. Verify the pinpoints before relying on them: Meta v. Bright Data's exact holding, the Defamation Act s.8 and s.9 details, the CDPA s.29A wording, the Art. 15 "very short extracts" text, and the Art. 2 definition of research organisation. The Meta v. Bright Data ruling also covers only logged-off scraping.

## Orchestrator note

The design rules derived here (and recorded as recommendations, not legal conclusions): store metadata, links and short excerpts, never full article text for display; honour robots.txt and machine-readable TDM reservations; every assessment that names a person or institution must be an opinion based on disclosed facts, with the facts and their sources shown on the same screen (the Milkovich structure); machine-extracted claims are the site's own speech, so they carry the same review bar as hand-written analysis. Section 230 does not cover Canary's own outputs. A one-hour consultation with a media lawyer before public launch is listed as a pre-launch task in the roadmap.
