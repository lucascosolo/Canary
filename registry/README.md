# Source registry

One YAML file per source, in the format set by `docs/plans/phase-0-registry-contract.md`. Check it
with `canary registry validate`.

## Values that are not yet verified

The format requires these fields, but the research notes do not establish them. They were filled
in on 2026-11-04 as working values. Treat them as unverified until a dated note supports them.

- `languages`: `en` on every entry. The notes record no language list. GDELT translates many
  source languages, so `en` describes its output, not its input.
- `revision_policy`: `silent` on every entry, as the cautious default.
- `source_class`: the author's judgement on every entry.
- `declared_cadence`: `Irregular` on `natural-earth` and `iso-3166` is a guess.
- `homepage` and `access_method` on `iso-3166`: no note covers this source.
- `homepage` on `internet-archive`: taken from the API help URL in its note.
- `endpoint` and `domains` on `natural-earth` and `gdelt-doc`: the author's reading of the notes.
- `licence_id` on `geonames`: the note says CC BY without a version.
- `auth` on `cloudflare-radar`: the token comes from the user's own account, so `account` also fits.
- `attribution_text`: a plain `Data: <organisation>` line except on `gdelt-doc` and `geonames`. UCDP
  also requires citing its listed publications, so its text is incomplete.

Entries with `canary_use: unverified` may be shown only as links (`docs/03`, section 8). On 2026-11-04
these are `keepiton`, `global-legal-monitor` and `iso-3166`; notes H-03, H-04 and H-05 record why.
