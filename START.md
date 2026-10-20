# PROJECT INITIATION: GLOBAL EARLY-WARNING AND HISTORICAL PATTERN ANALYSIS COMMAND CENTER

You are the initial research lead, systems architect, investigative analyst,
historical researcher, data-engineering planner, and technical project planner
for a new software project.

Your assignment is to determine what we should build, why we should build it
that way, how its various components should work together, and how to develop
and validate it responsibly.

You are NOT being asked to immediately build the application.

Your primary deliverable is a comprehensive, critically evaluated development
specification and implementation roadmap that can guide subsequent Claude Code
sessions through the entire development process.

The project's ultimate purpose is important enough that we must get its
foundations right. Take the time to investigate the problem space, challenge
assumptions, identify risks, compare approaches, and establish a sound plan
before proposing implementation.

You have considerable freedom to investigate alternative approaches and
recommend ideas that I have not considered. The suggestions below are starting
points, not mandatory requirements or a complete description of the project.

If you identify important unanswered questions that would materially affect
the architecture, scope, usefulness, or direction of the project, ask me those
questions before committing to decisions that depend on my answers.

Do not ask questions merely for the sake of asking them. Investigate what you
can independently, identify the actual decisions that require my input, and
make productive use of the session.


============================================================
1. THE CORE VISION
============================================================

I want to build a global command-center dashboard that functions as a kind of
canary in a coal mine for dangerous social, political, economic, and geopolitical
developments.

The underlying question is:

"What is happening in the world that could indicate a developing threat to
democracy, human rights, civil liberties, peace, economic stability, social
cohesion, or the long-term well-being of humanity, and what evidence supports
that assessment?"

The system should help identify warning signs that might otherwise be missed
because they emerge gradually, occur across different countries, appear in
seemingly unrelated news stories, or become apparent only when several
independent indicators are examined together.

It should help the user understand not only what happened, but also:

- Why the event might matter.
- Whether it represents a departure from historical or recent norms.
- Whether similar developments are occurring elsewhere.
- Whether several warning signs are converging.
- What historical precedents might be relevant.
- Which interpretations are supported by evidence and which remain uncertain.
- Whether the situation appears to be deteriorating, improving, or remaining
  relatively stable.
- What developments would strengthen or weaken the current assessment.
- What relevant information may be missing.

This is a worldwide project, not a United States news dashboard.

It should be capable of monitoring developments across countries, political
systems, cultures, regions, and levels of economic development.

The system should be useful both to someone who wants a quick daily overview
and to someone who wants to investigate a particular country, institution,
event, policy, movement, or historical pattern in considerable depth.

The objective is not to predict the future with false confidence.

The objective is to improve awareness, contextual understanding, and early
recognition of potentially dangerous developments.


============================================================
2. RESEARCH THE PROBLEM BEFORE DESIGNING THE SOLUTION
============================================================

Investigate existing academic research, established monitoring organizations,
public datasets, analytical methodologies, and software projects relevant to
this vision.

Do not assume that we need to invent every component ourselves.

Look for established work involving:

- Democratic backsliding and democratic erosion.
- Authoritarianism and authoritarian consolidation.
- Democratic transitions and democratic breakdown.
- Political repression and persecution.
- Human rights violations.
- Genocide prevention and mass-atrocity early warning.
- Civil conflict, political violence, and conflict escalation.
- Militarization, interstate conflict, and military intervention.
- Democratic institutions, judicial independence, and the rule of law.
- Press freedom and attacks on independent journalism.
- Elections, electoral integrity, and peaceful transfers of power.
- Political polarization and social fragmentation.
- Disinformation, propaganda, and information manipulation.
- Scapegoating, dehumanization, and persecution of minority groups.
- Political corruption, patronage, and institutional capture.
- Economic instability, inequality, and social unrest.
- State capacity, institutional legitimacy, and public trust.
- Historical patterns preceding democratic collapse, political repression,
  civil conflict, and mass atrocities.
- Early-warning systems used in public health, financial risk, environmental
  monitoring, and other disciplines.

Investigate whether these fields have established indicators, frameworks,
datasets, models, or monitoring systems that could be adapted.

Potential starting points include research and data from:

- V-Dem Institute.
- International IDEA.
- Freedom House.
- The Varieties of Democracy project.
- The Economist Intelligence Unit's democracy research, subject to its
  licensing and methodology.
- The International Crisis Group.
- ACLED.
- UCDP.
- The Uppsala Conflict Data Program's conflict datasets.
- The Armed Conflict Location & Event Data Project.
- The Global Terrorism Database, subject to its current availability and terms.
- The Early Warning Project.
- The UN Office of the High Commissioner for Human Rights.
- The UN Office on Genocide Prevention and the Responsibility to Protect.
- The UN Security Council and other relevant UN bodies.
- The World Bank.
- The International Monetary Fund.
- The OECD.
- The International Labour Organization.
- The World Inequality Database.
- The Varieties of Democracy Media Project and relevant press-freedom research.
- Reporters Without Borders.
- The Committee to Protect Journalists.
- CIVICUS Monitor.
- Transparency International.
- The International Foundation for Electoral Systems.
- Electoral observation missions and election-monitoring organizations.
- The Council on Foreign Relations' conflict resources.
- The GDELT Project.
- The Global Database of Events, Language, and Tone.
- The Armed Conflict Survey and other established conflict research.
- Academic research on historical coups, democratic breakdowns, political
  purges, mass violence, institutional capture, and state repression.

These are leads to investigate, not an endorsement of every organization or
dataset and not a mandatory list of integrations.

Verify that relevant resources still exist, determine their current access
methods, inspect their documentation, and establish what they actually measure.

Some sources may be expensive, restricted, biased in coverage, unsuitable for
commercial use, difficult to maintain, or less useful than their reputations
suggest.

Discover additional sources, including regional institutions and researchers
whose work may be overlooked by predominantly Western information systems.

Investigate the limitations of these sources rather than simply accumulating
their names.

Determine which established approaches are complementary, which overlap, and
which disagree about the same phenomena.

Identify where the proposed application could offer meaningful capabilities
that existing tools do not already provide.

Consider whether some parts of the project would be better served by integrating
with an existing platform instead of recreating its functionality.


============================================================
3. POTENTIAL MONITORING DOMAINS
============================================================

Explore a broad set of monitoring domains.

Do not assume every domain belongs in the initial release. Evaluate their
importance, feasibility, data quality, analytical value, and implementation
cost.

A. POLITICAL POWER AND INSTITUTIONAL INTEGRITY

Potential indicators include:

- Attempts to weaken judicial independence.
- Attacks on independent election administration.
- Changes to electoral rules that entrench incumbent power.
- Attempts to overturn legitimate election results.
- Restrictions on opposition parties or candidates.
- Political interference in prosecution and law enforcement.
- Expansion of executive authority.
- Emergency powers that become permanent or evade oversight.
- Politicization of public institutions.
- Efforts to weaken legislative oversight.
- Purges of independent civil servants.
- Politically motivated prosecution.
- Restrictions on peaceful protest.
- Changes to constitutional term limits.
- Attacks on independent oversight institutions.
- Changes in military or intelligence-service loyalty requirements.
- Government efforts to delegitimize legitimate opposition.
- Restrictions on civil society organizations.
- Government control over independent institutions.

B. ELECTIONS AND POLITICAL MOVEMENTS

Monitor elections and political developments worldwide.

Potential subjects include:

- Election results and changes in governing coalitions.
- Parties gaining power through platforms that propose restricting civil
  liberties or weakening democratic institutions.
- The implementation of campaign promises after elections.
- Changes in public support for authoritarian or anti-democratic policies.
- Political movements advocating ethnic, religious, racial, or national
  exclusion.
- Efforts to undermine electoral legitimacy.
- Political violence, intimidation, and threats against election workers.
- Restrictions on who can vote.
- Changes to campaign finance rules.
- The treatment of losing candidates and opposition parties.
- Peaceful transfers of power and failures to transfer power.
- The relationship between rhetoric, proposed legislation, and actual policy.

Avoid treating an election result, a party's ideological label, or a single
campaign statement as sufficient evidence of an impending crisis.

Investigate what parties actually propose, what they do after gaining power,
how institutions respond, and how their actions affect measurable outcomes.

C. LEGISLATION, GOVERNMENT ACTION, AND CIVIL LIBERTIES

Investigate ways to monitor legislative and executive activity.

Examples include:

- Laws restricting freedom of speech, association, religion, or assembly.
- Restrictions on journalism and access to information.
- Expanded surveillance powers.
- Restrictions on academic freedom.
- Changes in citizenship, asylum, immigration, and deportation policy.
- Laws targeting minority groups.
- Restrictions on reproductive rights and bodily autonomy.
- Criminalization of political opposition.
- Expansion of detention or policing powers.
- Changes to labor protections and collective bargaining rights.
- Legal changes affecting LGBTQ+ people.
- Restrictions on civil society and nonprofit organizations.
- Changes in the legal independence of public institutions.
- New powers affecting elections or political participation.
- Laws that weaken anti-corruption safeguards.
- Government seizure of property or arbitrary asset confiscation.

Distinguish between proposed bills, bills that have passed one legislative
chamber, enacted legislation, judicially blocked legislation, laws that have
entered into force, and policies that are actually being enforced.

Consider the value of tracking a policy throughout its entire lifecycle.

Evaluate the difficulty of obtaining reliable legislative information across
different countries and languages.

D. MILITARY ACTIVITY AND GEOPOLITICAL ESCALATION

Investigate potential monitoring of:

- Military strikes and cross-border attacks.
- Armed incursions and territorial seizures.
- Invasions and military occupations.
- Military mobilization and unusual troop movements when reliable public
  evidence is available.
- Airstrikes, missile attacks, drone strikes, and naval engagements.
- Civilian casualties.
- Attacks on critical infrastructure.
- Blockades and restrictions on maritime traffic.
- Military exercises that may affect regional tensions.
- Arms transfers and military assistance.
- Defense spending and procurement.
- Nuclear threats, nuclear tests, and changes in nuclear posture.
- Withdrawal from arms-control agreements.
- Escalation of existing conflicts.
- New alliances and changes in security commitments.
- Peace negotiations, ceasefires, and diplomatic breakthroughs.
- International sanctions and retaliatory measures.
- Conflicts that are receiving substantially less international attention
  despite worsening conditions.

Distinguish confirmed military actions from allegations, preliminary reports,
unverified claims, and propaganda.

Explore the usefulness of event databases, official statements, satellite
imagery released by credible organizations, maritime data, and reputable
investigative reporting.

Do not assume that every military deployment signals an intention to attack.

Consider whether the system should monitor de-escalation and diplomatic
developments as prominently as escalation.

E. HUMAN RIGHTS, PERSECUTION, AND MASS-ATROCITY WARNING SIGNS

Investigate established indicators and frameworks related to:

- Discrimination backed by state power.
- Dehumanizing rhetoric.
- Scapegoating of vulnerable groups.
- Organized political violence.
- Arbitrary detention.
- Torture and extrajudicial killings.
- Enforced disappearances.
- Mass arrests.
- Forced displacement.
- Restrictions on humanitarian access.
- Collective punishment.
- Systematic persecution.
- Incitement to violence.
- Mass surveillance targeting particular populations.
- State-supported or tolerated paramilitary activity.
- The weakening of protections for vulnerable populations.
- Restrictions on independent documentation of abuses.

Investigate established genocide-risk and atrocity-prevention frameworks.

Do not reduce complex phenomena such as genocide to simplistic numerical
formulas.

Distinguish between warning signs, documented abuses, legal determinations,
and allegations that require further investigation.

Treat this domain with particular care because both false alarms and missed
warnings can have serious consequences.

F. INFORMATION ECOSYSTEM AND PROPAGANDA

Potential subjects include:

- Government pressure on independent media.
- Media ownership concentration.
- Internet shutdowns and censorship.
- Government control of public broadcasting.
- Coordinated disinformation campaigns.
- Political attacks on journalists.
- Threats against researchers and fact-checkers.
- Manipulation of official statistics.
- Systematic delegitimization of independent sources.
- Restrictions on access to public records.
- Coordinated scapegoating campaigns.
- State-sponsored propaganda.
- Changes in the accessibility of reliable information.

Investigate whether changes in rhetoric can be measured meaningfully over time.

Be especially cautious about treating sentiment analysis, keyword counts, or
AI-generated interpretations of political speech as reliable evidence without
validation.

G. ECONOMIC AND SOCIAL CONDITIONS

Potential subjects include:

- Inflation and unemployment.
- Food and energy prices.
- Household purchasing power.
- Housing affordability.
- Public debt and debt-servicing pressure.
- Currency crises.
- Banking instability.
- Sovereign debt distress.
- Economic inequality.
- Poverty and extreme poverty.
- Youth unemployment.
- Labor disputes and strikes.
- Food insecurity.
- Public health deterioration.
- Social unrest.
- Displacement and migration.
- Declining access to essential services.
- Regional economic disparities.
- Changes in government spending priorities.
- Concentration of wealth and political influence.
- Economic coercion and politically motivated resource allocation.

Investigate how economic conditions interact with political institutions and
historical instability.

Avoid simplistic claims that economic hardship automatically produces
authoritarianism, violence, or political collapse.

H. OTHER POTENTIALLY IMPORTANT DOMAINS

Explore additional subjects I may not have considered, including:

- Climate-related instability and resource competition.
- Water scarcity and food-system vulnerability.
- Pandemics and public-health emergencies.
- Infrastructure fragility.
- Cyberattacks against critical infrastructure.
- AI-enabled political manipulation.
- Democratic resilience and institutional recovery.
- Corruption and illicit financial networks.
- State fragility.
- International cooperation and collective-security failures.
- Environmental disasters that could compound existing crises.
- Changes in political participation and civic engagement.

Recommend which domains offer the greatest value for the initial implementation
and which should be deferred.


============================================================
4. HISTORICAL PATTERN RECOGNITION
============================================================

A central feature of the project should be the ability to place current
developments in historical context.

Investigate how to compare present-day developments with historical episodes
involving:

- Democratic backsliding.
- The consolidation of authoritarian power.
- The erosion of judicial independence.
- Political purges.
- The suppression of opposition movements.
- The criminalization of dissent.
- The normalization of political violence.
- The scapegoating and persecution of minority groups.
- The weakening of independent media.
- The growth of political paramilitaries.
- Military coups and attempted coups.
- Democratic breakdown.
- Civil conflict.
- Mass atrocities.
- Genocide.
- Imperial expansion.
- Territorial revisionism.
- Economic crises that contributed to political instability.
- Institutional recovery following authoritarian rule.

Investigate relevant cases from many regions and political traditions.

Potential historical case studies include, among many others:

- The Weimar Republic and the Nazi seizure of power.
- The gradual dismantling of democratic institutions in interwar Europe.
- Fascist Italy.
- Francoist Spain.
- Authoritarian consolidation in Chile.
- Argentina's military dictatorship.
- The collapse of democratic institutions in Venezuela.
- Democratic backsliding in Hungary and Turkey.
- The dissolution of Yugoslavia.
- The Rwandan genocide.
- The Cambodian genocide.
- Political repression under Stalin.
- The Cultural Revolution in China.
- The Indonesian mass killings of 1965–1966.
- Apartheid South Africa.
- Military coups and democratic transitions in Latin America.
- Democratic transitions and reversals in Africa and Asia.
- Other historical episodes identified by relevant scholarship.

These are research starting points, not a predetermined set of conclusions.

Include examples of democratic resilience, successful institutional reform,
de-escalation, peaceful transitions, and countries that reversed authoritarian
or anti-democratic trends.

The system must not simply search for superficial similarities between the
present and famous historical catastrophes.

Investigate methods for distinguishing meaningful similarities from misleading
analogies.

For example, two countries may both experience political polarization while
having very different institutional safeguards, social structures, military
relationships, and political trajectories.

Consider questions such as:

- What sequence of events preceded a historical outcome?
- Which warning signs appeared early?
- Which indicators were most informative?
- Which developments occurred frequently without the feared outcome?
- Which protective institutions prevented deterioration?
- Which combinations of factors mattered more than individual indicators?
- How long did the historical process take?
- What changed when the trajectory reversed?
- What did observers misunderstand at the time?
- Which contemporary indicators are actually comparable to the historical
  evidence?
- What is the base rate of the outcome being considered?
- How much evidence is needed before a historical comparison becomes useful?

Consider whether the system should maintain a curated historical knowledge base
that links documented episodes, events, timelines, causal mechanisms, primary
sources, scholarly interpretations, and known limitations.

Explore whether a structured historical event model, knowledge graph, timeline
system, or another representation would be most useful.

Determine how to present historical parallels without sensationalism.

A useful result might explain that several developments resemble an early
stage of a documented historical process while clearly explaining important
differences and why the analogy is not a prediction.


============================================================
5. GLOBAL PUBLIC DATA AND SOURCE STRATEGY
============================================================

The project should use relevant public information from government sources,
international organizations, academic institutions, independent researchers,
journalists, civil-society organizations, and other credible third parties.

It should not depend entirely on government sources or entirely on news media.

Government sources may provide authoritative records of laws, votes, budgets,
economic statistics, official policy, and military statements. They may also
omit, distort, or misrepresent politically inconvenient information.

Independent organizations may provide valuable documentation and analysis but
can have their own methodological limitations, political perspectives,
coverage gaps, funding constraints, and reporting biases.

The system should assess sources according to what they are actually qualified
to establish.

Investigate the following categories of information sources.

OFFICIAL SOURCES
- National legislatures and parliamentary voting records.
- Official gazettes and legislation databases.
- Election commissions and electoral results.
- Courts and judicial decisions.
- National statistical agencies.
- Central banks and finance ministries.
- Defense ministries and military press releases.
- Foreign ministries and diplomatic statements.
- Government budget and procurement records.
- Public procurement and corporate registries where accessible.
- Public records and freedom-of-information disclosures.
- Official public-health and emergency-management sources.

INTERNATIONAL SOURCES
- United Nations agencies and public reporting.
- International Court of Justice and International Criminal Court materials.
- World Bank datasets.
- IMF datasets and reports.
- OECD datasets.
- International Labour Organization statistics.
- International election observation missions.
- International humanitarian organizations.
- International conflict monitoring resources.
- Regional organizations such as the African Union, European Union,
  Organization of American States, and ASEAN.

INDEPENDENT AND ACADEMIC SOURCES
- Peer-reviewed research.
- University research centers.
- Election-monitoring organizations.
- Human-rights organizations.
- Press-freedom organizations.
- Conflict-monitoring organizations.
- Independent investigative journalism.
- Public-interest research institutions.
- Civil-society monitoring networks.
- Regional and local investigative organizations.

EVENT, NEWS, AND OPEN-DATA SOURCES
- GDELT.
- ACLED and UCDP, subject to access and licensing requirements.
- Public RSS feeds.
- Public APIs.
- Official press-release feeds.
- Publicly accessible news archives.
- Open legislative data.
- Public election datasets.
- Publicly released geospatial data.
- Other structured event databases.

Investigate relevant country-specific sources instead of assuming that a small
number of international sources can adequately represent the entire world.

For each promising source, determine:

1. What information it provides.
2. Which countries and regions it covers.
3. Its geographic, linguistic, and temporal limitations.
4. How frequently it updates.
5. Whether it offers an API, RSS feed, bulk download, or other access method.
6. Whether access requires authentication or payment.
7. Whether it imposes rate limits.
8. Its terms of service and licensing restrictions.
9. Whether redistribution, storage, summarization, or commercial use is allowed.
10. How reliable and complete its data is.
11. Whether its methodology is transparent.
12. Whether it is independent of the events or institutions it reports on.
13. Whether its information can be corroborated independently.
14. What role it should play in the system.

Distinguish between a source being publicly accessible and its data being freely
redistributable.

Do not assume that a publicly viewable website permits unrestricted scraping.

Prefer durable and documented data-access methods over fragile scraping
workarounds when possible.

Explore the possibility of maintaining a source registry with metadata,
coverage information, reliability assessments, update status, licensing notes,
and integration health.

Determine how to manage sources that disappear, change their APIs, revise
their methodologies, or stop providing data.


============================================================
6. EVIDENCE, SOURCE INDEPENDENCE, AND POLITICAL NEUTRALITY
============================================================

This project must apply consistent evidentiary standards regardless of which
country, government, political party, ideology, religion, or movement is being
examined.

Political neutrality does not mean avoiding conclusions.

It means that conclusions must follow the evidence rather than predetermined
political preferences.

Investigate ways to establish transparent and consistent analytical standards.

The system should distinguish among:

- Directly documented facts.
- Official claims.
- Independent reporting.
- Corroborated allegations.
- Uncorroborated allegations.
- Expert interpretations.
- Statistical findings.
- Historical comparisons.
- Model-generated hypotheses.
- Forecasts and risk assessments.
- Legal findings and judicial determinations.
- Unknowns and unresolved disputes.

These categories should not be collapsed into a single confidence score.

Consider whether individual claims, events, and analytical conclusions should
carry their own evidence records.

For significant conclusions, explore a structure that identifies:

- The conclusion being considered.
- The underlying evidence.
- The original sources.
- The dates of the relevant events and reports.
- The relationship between different sources.
- Evidence supporting the conclusion.
- Evidence contradicting the conclusion.
- Important missing information.
- The degree and type of uncertainty.
- The reasoning connecting evidence to interpretation.

A particularly important challenge is source independence.

Five news articles repeating the same original government statement are not
equivalent to five independent confirmations.

Investigate methods for identifying syndicated reporting, common source
attribution, copied claims, circular citations, and coordinated information
campaigns.

Explore how the system could track the difference between multiple reports and
multiple genuinely independent lines of evidence.

Consider how to detect changes in reporting volume that reflect changes in
media access, internet availability, censorship, or international attention
rather than actual changes in underlying conditions.

The system should not silently treat missing information as evidence that
nothing happened.

It should also avoid treating every government denial as equivalent to
independent contradictory evidence.

Develop a transparent source-evaluation methodology without pretending that
credibility can always be reduced to one objective numerical score.

Investigate how to document disagreements among reputable sources.

For politically consequential findings, determine when independent corroboration
or human review should be required before assigning a strong warning.

Explore whether an adversarial review process could help identify assumptions,
alternative explanations, selective evidence, and inconsistent standards.

Do not automatically equate centrist, Western, official, or institutionally
established sources with neutrality or correctness.

Likewise, do not automatically reject a source because it criticizes a powerful
government or institution.

Evaluate evidence in context.


============================================================
7. WARNING INDICATORS, TRENDS, AND RISK ASSESSMENT
============================================================

The central analytical challenge is converting a large amount of heterogeneous
information into meaningful early warnings without generating an overwhelming
number of false alarms.

Research existing approaches to political-risk assessment, conflict early
warning, democratic-resilience measurement, anomaly detection, and historical
risk modeling.

Explore different approaches, including:

- Transparent rule-based indicators.
- Statistical trend analysis.
- Change-point detection.
- Historical baselines.
- Anomaly detection.
- Composite indicators.
- Structured expert assessments.
- Bayesian reasoning where appropriate.
- Time-series analysis.
- Event-sequence analysis.
- Geographic clustering.
- Relationship and network analysis.
- Machine-learning classification.
- Language-model-assisted extraction and interpretation.
- Human-reviewed analytical workflows.

Do not assume that a more complicated model is necessarily more useful.

Compare analytical methods according to their accuracy, interpretability,
maintainability, data requirements, computational cost, and vulnerability to
bias.

Investigate how the system could detect combinations of developments that
become more concerning together than separately.

For example, consider a hypothetical combination of:

- Attacks on independent courts.
- Restrictions on opposition candidates.
- Escalating political violence.
- Expansion of emergency powers.
- Government attacks on independent media.

The significance of this combination depends on the details, chronology,
institutional context, and quality of the evidence.

Do not simply assign arbitrary points to these events and label the resulting
number an objective risk score.

Explore how different analytical approaches could identify meaningful patterns
while making their assumptions explicit.

Investigate how to distinguish:

- A single concerning event.
- A persistent deterioration in one indicator.
- Several indicators deteriorating together.
- An unusually rapid deterioration.
- A developing sequence of related events.
- A major event that changes the baseline.
- A situation that is dangerous but stable.
- A situation that is improving after a period of deterioration.
- A situation where apparent deterioration reflects improved reporting.
- A situation where the available evidence is too incomplete to assess.

Consider the difference between absolute risk and changes relative to a
country's own historical baseline.

A country with historically weak institutions may face substantial risks
without experiencing a new deterioration. A country with historically strong
institutions may experience a significant decline while still scoring well on
some absolute measures.

Both situations may matter for different reasons.

Explore ways to represent these differences.

Investigate how to calibrate warnings against historical outcomes, including
the frequency of false positives and false negatives.

If probability estimates are proposed, determine what historical data and
validation methods would justify them.

Do not present numerical precision that the evidence cannot support.

Investigate whether a warning should explain what developments would cause its
assessment to rise, fall, or be withdrawn.

Include positive developments and protective factors in the analysis.

The system should be capable of recognizing institutional resilience,
de-escalation, successful reforms, and improving conditions rather than
assuming that every trend is negative.


============================================================
8. A GLOBAL PICTURE WITHOUT LOSING LOCAL CONTEXT
============================================================

The system must be genuinely global.

Investigate how to represent countries, territories, disputed regions,
subnational jurisdictions, political institutions, non-state actors, and
transnational organizations.

Consider how geographic relationships matter for understanding events.

A military strike near a border, an election in a strategically important
country, a regional economic shock, or a crisis involving several neighboring
states may have implications beyond the immediate location.

Explore whether maps, timelines, country profiles, regional views, and
cross-country comparisons would be useful.

Investigate how to make comparisons meaningful across countries with different
political systems, legal structures, reporting environments, and economic
conditions.

Avoid assuming that every country follows the same historical trajectory or
that political institutions are directly comparable without qualification.

Consider how to support multiple languages.

Investigate whether translation should occur at ingestion, display time, or
both.

Preserve original-language source material where possible so users can inspect
what was actually reported.

Consider whether local and regional sources should receive special attention
when international reporting is sparse.

Determine how the system can expose coverage gaps rather than implying that
all regions are monitored equally well.

A global dashboard that has excellent information about Europe and North
America but weak information about the rest of the world must make that
limitation visible.


============================================================
9. USER INTERFACE AND COMMAND-CENTER EXPERIENCE
============================================================

The application should provide a sophisticated command-center experience
without becoming cluttered, overwhelming, or visually sensationalist.

The interface should allow a user to move naturally from a broad global
overview to an individual event, source, country, historical comparison, or
analytical finding.

Investigate the information architecture before deciding on a specific design.

Potential interface components include:

- A global overview.
- A map showing significant developments and geographic concentrations.
- A prioritized feed of important events.
- An overview of emerging risks and deteriorating trends.
- Country and regional profiles.
- Historical timelines.
- Legislative tracking.
- Election monitoring.
- Military and conflict monitoring.
- Economic indicators.
- Human-rights developments.
- Cross-domain relationships.
- Source and data-quality indicators.
- Saved investigations or watchlists.
- A searchable archive.
- Alerts for significant developments.
- Explanations of why an item has been highlighted.

These are possible components, not a requirement to create a separate screen
for every category.

Think carefully about which information belongs on the main dashboard and
which should appear only when a user investigates something further.

The default view should prioritize what is important, new, worsening, or
otherwise deserving of attention.

It should also distinguish urgent events from slow-moving structural trends.

Avoid designing a wall of statistics or a conventional news website with a
different color scheme.

Investigate the value of progressive disclosure: a compact overview that can
expand into detailed evidence, timelines, source comparisons, and analytical
explanations.

Every important warning should answer, as clearly as possible:

- What happened?
- Where did it happen?
- When did it happen?
- Why is it relevant?
- How strong is the evidence?
- What is changing?
- What historical context is useful?
- What should the user investigate next?

The interface should communicate uncertainty without hiding important
information.

Avoid sensationalist colors, exaggerated alarm indicators, and visual choices
that imply a level of certainty the evidence does not justify.

At the same time, a genuinely urgent development should not be buried among
routine updates.

Investigate how the interface can distinguish urgency, severity, confidence,
trend direction, and data completeness without collapsing them into one
ambiguous visual signal.

Consider accessibility, keyboard navigation, mobile layouts, readable
typography, dark mode, information density, and the needs of users who may
spend extended periods investigating the system.

Explore whether the interface should be configurable or whether a carefully
designed default experience would be more useful initially.

The goal is to place a large amount of relevant information at the user's
fingertips while keeping the primary experience understandable at a glance.


============================================================
10. DATA PIPELINES AND TECHNICAL ARCHITECTURE
============================================================

Research suitable architectures for a system that may eventually ingest
information from many sources, maintain historical records, perform
cross-source analysis, and serve an interactive dashboard.

Do not select a technology stack merely because it is familiar or fashionable.

Compare reasonable alternatives and explain the tradeoffs.

Investigate:

- Source adapters and ingestion pipelines.
- Scheduled polling and event-driven ingestion.
- Data normalization.
- Deduplication.
- Event extraction.
- Entity resolution.
- Geographic normalization.
- Multilingual processing.
- Provenance and source tracking.
- Historical data retention.
- Time-series storage.
- Full-text search.
- Geospatial queries.
- Analytical processing.
- Caching.
- Background jobs.
- API design.
- Frontend architecture.
- Authentication and authorization.
- Observability and operational monitoring.
- Backup and recovery.
- Deployment and hosting.
- Database migrations.
- Testing.
- Reproducibility.
- Versioning of analytical methods.

Determine whether a relational database, document store, search engine,
graph database, time-series database, or a combination would be appropriate.

Do not introduce additional infrastructure unless its benefits justify its
complexity.

Investigate the possibility of beginning with a modular architecture that can
grow without requiring a premature distributed system.

Consider the costs and maintenance implications of large language models,
embedding models, external APIs, data storage, and historical archives.

If LLMs are proposed, identify precisely where they add value beyond
deterministic processing.

Potential uses might include extracting structured claims from documents,
summarizing long reports, identifying candidate relationships, translating
content, or generating evidence-grounded explanations.

Do not make an LLM the unquestioned source of truth.

Explore how to validate extracted facts, preserve citations, record model
versions, and detect hallucinations.

Determine which operations can be handled with ordinary code and structured
data.

Investigate whether analytical results can be reproduced from retained source
records, model versions, and configuration settings.

Consider the possibility that different analytical components will need
different update schedules.

For example, military event reporting, election results, monthly economic
statistics, and annual democracy indices should not necessarily be processed
or displayed in the same way.

Identify the architecture needed to support this variation.


============================================================
11. SECURITY, RELIABILITY, AND RESILIENCE
============================================================

Treat data integrity and system reliability as important design concerns.

Investigate:

- Malicious or manipulated source content.
- Prompt injection in ingested documents.
- Poisoned data feeds.
- Fake reports and coordinated disinformation.
- Compromised source credentials.
- Malicious files or unsafe content.
- API outages.
- Rate limiting.
- Data corruption.
- Database failures.
- Backup and restoration.
- Unauthorized access.
- Secrets management.
- Dependency vulnerabilities.
- Denial-of-service risks.
- Operational failures that could silently stop ingestion.
- Incorrect timestamps and geographic assignments.
- Model failures that produce plausible but unsupported conclusions.

Treat external source material as untrusted input.

If an LLM processes external documents, ensure that instructions embedded in
those documents cannot override system instructions, access secrets, or
trigger unauthorized actions.

The application should never imply that its information is current if its
data feeds have stopped updating.

Investigate how to display source freshness, ingestion health, missing data,
and known outages.

Consider whether the system should preserve raw source records, normalized
records, extracted claims, and analytical outputs separately.

Determine which information needs immutable or append-only audit records and
which information can be updated or corrected.

Corrections should be traceable.

Explore how to retain the original record when an extracted claim or analytical
interpretation changes.

The system should distinguish a source correcting an earlier report from the
application correcting its own processing error.

Investigate how to recover from a faulty ingestion pipeline without silently
rewriting the historical record.


============================================================
12. RESEARCH, ANALYSIS, AND VALIDATION WORKFLOW
============================================================

Before recommending an implementation plan, investigate how the system should
be tested against real historical examples.

A dashboard that looks impressive but fails to detect important developments,
generates excessive false alarms, or invents misleading historical parallels
would not fulfill its purpose.

Explore historical backtesting.

Potential approaches include:

- Reconstructing what information was publicly available at a historical date.
- Testing whether the system identifies warning signs before a known outcome.
- Comparing its assessments with established research.
- Evaluating whether it produces excessive warnings during relatively stable
  periods.
- Examining whether it misses significant developments.
- Testing whether its conclusions change when sources become unavailable.
- Comparing results across countries and regions.
- Testing for ideological or geographic inconsistencies.
- Measuring the effect of incomplete reporting.
- Testing whether historical comparisons remain useful when outcomes differ.
- Checking whether apparently independent sources share the same underlying
  evidence.

Be alert to look-ahead bias.

A system must not be credited with predicting a historical event using
information that became available only after that event.

Distinguish between reconstructing what an observer could have known at the
time and analyzing a historical event with the benefit of hindsight.

Investigate how to build evaluation datasets that include both deterioration
and recovery.

Consider whether independent researchers or domain experts should review
important analytical frameworks and validation results.

Develop a plan for documenting known weaknesses and maintaining a record of
failed predictions, missed events, and false alarms.

Do not optimize the system solely for producing more warnings.

A useful system should help the user distinguish important developments from
routine political conflict and ordinary fluctuations.

Investigate how to evaluate usefulness even when outcomes are rare, ambiguous,
or difficult to define.

If the project cannot initially support defensible prediction, identify a more
modest and testable analytical capability that provides genuine value.


============================================================
13. PRACTICAL CONSTRAINTS AND DEVELOPMENT STRATEGY
============================================================

The project will be developed using Claude Code.

I want the project to be designed carefully before substantial implementation
begins.

I am open to different programming languages, frameworks, databases, and
deployment strategies when the advantages are justified.

Prefer maintainable, understandable systems over unnecessary complexity.

Do not assume that every proposed capability must be included in the first
release.

Identify a useful initial product that can be built, tested, and evaluated
without pretending to solve the entire problem immediately.

At the same time, avoid an MVP architecture that makes the eventual project
unnecessarily difficult to extend.

The roadmap should account for the difference between:

- A compelling visual prototype.
- A working dashboard using real data.
- A reliable multi-source monitoring system.
- A system capable of meaningful historical and cross-domain analysis.
- A validated early-warning system.

These are different levels of maturity.

Do not claim that reaching one automatically achieves the others.

Investigate practical costs, including data access, API limits, LLM usage,
hosting, storage, and maintenance.

Identify which data sources and capabilities can be implemented with minimal
cost and which may require funding or restricted access.

Prefer an initial design that can operate with a reasonable budget while
allowing later expansion.

Do not assume that paid APIs, commercial data subscriptions, or expensive
infrastructure are automatically necessary.

Equally, do not assume that every important dataset is free.

Recommend a development sequence that maximizes learning and reduces the
chance of building a large, impressive-looking application on an inadequate
analytical foundation.


============================================================
14. ENGINEERING WORKFLOW AND SAFETY REQUIREMENTS
============================================================

Follow a careful, reviewable engineering workflow throughout this project.

Before implementation, inspect the repository and determine what already
exists. Do not assume that the directory is empty.

Establish the current repository state and identify any existing instructions,
documentation, code, or configuration that should be preserved.

Do not overwrite or discard existing work without understanding its purpose.

CRITICAL FILE-SAFETY RULE:

You must never execute the `rm` command, in any form, for any reason.

Do not introduce scripts, Makefile targets, package scripts, build hooks,
cleanup routines, or other automation that executes `rm`.

Do not circumvent this rule through aliases, shell substitutions, alternative
command forms, or another tool.

If a file genuinely needs to be removed, move it into a clearly named quarantine
directory and leave its permanent deletion to me.

Apply this rule to commands you execute and to any automation you create.

Prefer small, reviewable changes and frequent Git checkpoints.

Do not overwrite existing Git history or perform destructive Git operations.

Do not force-push.

Do not assume that committing or pushing is authorized if the repository's
current state or available credentials make that unclear.

Inspect the existing branch, remotes, working tree, and project instructions
before recommending a workflow.

Keep research notes and design decisions in version-controlled documentation
where appropriate.

When evaluating an architectural decision, record the alternatives considered,
the tradeoffs, the evidence, and the reasons for the recommendation.

Distinguish established facts from assumptions and unresolved questions.

If you discover that an important requirement is ambiguous, document the
ambiguity rather than silently making an irreversible decision.

Do not begin implementing the full application during this initial
specification phase.

You may perform non-destructive repository inspection and research needed to
produce a strong specification.

If a small exploratory experiment would materially clarify an architectural
question, explain the question it would answer and obtain my approval before
turning it into a larger implementation effort.


============================================================
15. REQUIRED OUTPUTS
============================================================

Your objective is to produce a development specification that a future Claude
Code session can use to begin implementation without having to rediscover the
fundamental design decisions.

Determine the best organization for the deliverables, but consider the
following documents.

A. PROJECT VISION AND PRODUCT REQUIREMENTS

Document the core problem, intended users, primary use cases, expected
capabilities, non-goals, constraints, and criteria for success.

Explain what makes this system different from an ordinary news aggregator,
political-risk dashboard, or geopolitical intelligence platform.

B. RESEARCH AND COMPETITIVE LANDSCAPE

Summarize existing systems, academic research, analytical frameworks,
datasets, and relevant open-source projects.

Identify capabilities we can reuse and gaps we might address.

Include citations, links, and research dates where appropriate.

Distinguish verified findings from your own recommendations.

C. DATA SOURCE CATALOG

Create a researched catalog of promising data sources.

Include their coverage, access methods, update frequency, licensing
considerations, limitations, intended use, and implementation priority.

Identify a small set of particularly valuable sources for initial integration.

Do not merely list hundreds of sources without evaluating them.

D. ANALYTICAL FRAMEWORK

Propose a transparent framework for evaluating events, indicators, trends,
historical parallels, source quality, and uncertainty.

Explain how independent evidence should be combined.

Explain how the system should account for missing information, contradictory
evidence, geographic differences, historical baselines, and changing conditions.

Include examples of how the framework would handle hypothetical developments.

E. HISTORICAL KNOWLEDGE STRATEGY

Explain how historical case studies, warning indicators, causal mechanisms,
protective factors, and historical timelines should be represented and used.

Identify relevant research resources and possible validation methods.

Explain how to avoid simplistic or sensational historical analogies.

F. UI AND INFORMATION ARCHITECTURE

Describe the primary user experience.

Explain the default dashboard, navigation, major views, progressive disclosure,
search, filters, watchlists, and detailed investigation workflows.

Consider including wireframes or text-based layout sketches.

Identify the information that deserves immediate attention and what should
remain available through deeper exploration.

G. TECHNICAL ARCHITECTURE

Recommend a practical architecture and technology stack.

Explain major components, data flow, storage, APIs, background processing,
analytical services, frontend structure, deployment, security, and observability.

Include a high-level architecture diagram if useful.

Explain why the recommended approach is preferable to realistic alternatives.

H. DATA MODEL AND SCHEMAS

Propose initial data models for the major concepts.

Potential entities include:

- Sources.
- Documents.
- Claims.
- Events.
- Actors and organizations.
- Geographic entities.
- Legislation.
- Elections.
- Indicators.
- Time-series observations.
- Historical episodes.
- Analytical findings.
- Risk assessments.
- Evidence relationships.
- Corrections and audit records.

Determine which entities are actually necessary and how they relate.

Explain how provenance and the distinction between reported facts and
analytical interpretations should be preserved.

Do not finalize complex schemas before the underlying requirements justify them.

I. VALIDATION AND TESTING STRATEGY

Describe unit, integration, data-quality, analytical, historical-backtesting,
security, performance, and user-experience testing.

Explain how the project will detect false alarms, missed events, source bias,
and unsupported conclusions.

Identify the historical cases and datasets that should be used for early tests.

J. DEVELOPMENT ROADMAP

Break implementation into coherent phases.

For each phase, explain:

- Its objective.
- The capabilities it delivers.
- The work that must precede it.
- Major technical decisions.
- Dependencies.
- Likely difficulties.
- Acceptance criteria.
- Testing requirements.
- Definition of completion.
- What evidence will demonstrate that the phase succeeded.

Include a sensible sequence for establishing data ingestion, provenance,
analytical correctness, and the UI.

Do not prioritize an impressive dashboard over the underlying reliability of
the information it displays.

K. RISKS AND UNRESOLVED QUESTIONS

Identify the most consequential technical, analytical, political, ethical,
operational, legal, and financial risks.

Rank them by significance.

Explain how each risk could be reduced or tested.

Clearly identify decisions that require my input.

L. INITIAL IMPLEMENTATION HANDOFF

Produce a concise but sufficiently detailed handoff document for the next
Claude Code session.

It should describe the agreed architecture, first implementation objective,
relevant repository documentation, acceptance criteria, known constraints,
and the next actions to take.

The handoff should make it possible to start the first implementation phase
without repeating the entire discovery process.

Organize these deliverables into a coherent documentation structure rather
than creating files merely to satisfy a checklist.


============================================================
16. HOW TO CONDUCT THIS INITIAL SESSION
============================================================

Work as a critical researcher and architect, not as an obedient idea generator.

Do not simply endorse the vision and produce a generic software development
plan.

Challenge assumptions.

Identify potential failure modes before they become architectural problems.

Investigate whether certain aspects of the idea are already solved by existing
research or software.

Identify capabilities that sound compelling but cannot currently be supported
with reliable evidence.

Distinguish what is technically possible from what is analytically defensible.

Consider alternative product directions when they might better achieve the
underlying goal.

For important recommendations, explain the reasoning and tradeoffs.

Use current primary documentation, academic research, and credible external
sources when research access is available.

Provide citations and links for material factual claims.

If you cannot access the internet or a particular source, state that limitation
rather than pretending the research was completed.

Do not fabricate sources, APIs, documentation, datasets, or technical findings.

When sources disagree, explain the disagreement.

When you cannot establish something confidently, say so.

Use parallel research or subagents if they are available and useful, but ensure
their findings are reviewed and reconciled rather than accepted uncritically.

Keep the project specification internally consistent.

For example, do not recommend one data model in the architecture document and
an incompatible model in the implementation roadmap.

Do not confuse an initial design proposal with a decision that has been
validated.

Label recommendations that still require experiments or additional research.

Do not write the full application.

Do not generate a large volume of placeholder code.

Do not spend the session polishing visual details before resolving the core
data and analytical design.

The goal is a strong, evidence-based foundation for implementation.


============================================================
17. FIRST ACTIONS
============================================================

Begin by:

1. Inspecting the repository, current branch, working tree, existing project
   instructions, and available documentation.

2. Identifying the research questions that must be answered before a credible
   architecture can be proposed.

3. Investigating the most relevant existing systems, datasets, academic
   frameworks, and technical approaches.

4. Identifying major feasibility constraints and analytical pitfalls.

5. Determining which product decisions genuinely require my input.

6. Presenting me with any high-value clarifying questions before committing to
   decisions that depend on the answers.

If you have enough information to begin research without clarification, do so.

If important questions remain, ask them clearly and explain why their answers
matter.

Do not make me decide technical details that you can reasonably investigate
and recommend yourself.

After resolving the important questions, produce the specification and
roadmap described above.

At the end, summarize:

- The recommended product direction.
- The most important architectural decisions.
- The highest-priority data sources.
- The proposed analytical approach.
- The initial UI concept.
- The largest unresolved risks.
- The development phases.
- The first implementation milestone.
- Any decisions for which my approval is still required.

The final result should be something we can confidently use as the foundation
for a serious, long-term project.

Remember: the objective is not merely to build a dashboard that displays
concerning news.

The objective is to build a trustworthy, transparent, globally aware system
that helps identify meaningful warning signs, understand how they fit into
historical and contemporary patterns, and recognize both danger and resilience
before important developments become impossible to ignore.
