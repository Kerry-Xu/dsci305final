# Responsible AI Risk Report

Generated: 2026-04-27 15:28:21

## 1. Project Overview

**Project name:** ai risk analyzer

**Project description:** i use ai to detect where there is ai used

**Intended audience:** undergrad

**Deployment context:** college course

**AI system type:** data analysis tool

**Data sources:** self

## 2. Overall Risk Rating

**Risk score:** 11

**Risk level:** High

The project has substantial ethical risk. It should not be deployed outside a controlled
class or research context without additional review.

## 3. Main Risk Flags

1. The project uses sensitive data.
2. The project may affect rights, access, or opportunities.
3. The project is connected to a high impact domain: insurance.

## 4. Recommended Actions

1. Add stricter consent, access control, retention limits, and a stronger privacy review.
2. Require human review before any output is used for a consequential decision.
3. Treat the project as high impact and document risk controls before deployment.

## 5. NIST AI Risk Management Framework Alignment

This report uses the NIST AI Risk Management Framework structure of Govern, Map, Measure, and Manage.

### Govern

1. The project should assign responsibility for data handling, model behavior, documentation, and user communication.
2. The project already includes a limitations section, which supports transparent governance.
3. Human review is included, which supports accountability.
### Map

1. Intended audience: undergrad.
2. Deployment context: college course.
3. Data sources: self.
4. AI system type: data analysis tool.
5. The system is mapped to a high impact domain: insurance.
### Measure

1. The project includes bias, fairness, or error testing.
2. The project includes a privacy or data minimization plan.
3. The project includes security or misuse controls.
### Manage

1. Current risk level: High.
2. Known possible harms: y.
3. Current mitigation plan: y.
4. The project should remain in prototype status until additional review is completed.

## 6. EU AI Act Reference Note

EU AI Act reference note: This tool is not making a legal classification. However, the
project has features associated with high impact AI contexts because it relates to
insurance and may influence decisions about people. A real deployment would need
stronger documentation, risk controls, transparency, human oversight, and quality
management.

## 7. UNESCO Ethics Reference Note

UNESCO ethics note: Because the project may involve sensitive data or vulnerable users,
it should prioritize human dignity, privacy, fairness, transparency, and human
oversight. The project should avoid replacing human judgment in situations where people
may be harmed.

## 8. ACM Code of Ethics Reference Note

ACM ethics note: The project should put public good first, avoid harm, be honest about
limitations, and be especially careful when outputs could affect people's rights or
opportunities.

## 9. Potential Harms

y

## 10. Mitigation Plan

y

## 11. Limitations of This Audit

1. This tool is educational and does not provide legal advice.
2. The score depends on self reported answers.
3. A low score does not prove that an AI system is safe.
4. High impact projects should receive instructor, domain expert, or institutional review.
5. The tool does not replace compliance review under university policy or applicable law.

## 12. Raw Project Profile

```json
{
  "project_name": "ai risk analyzer",
  "project_description": "i use ai to detect where there is ai used",
  "intended_audience": "undergrad",
  "deployment_context": "college course",
  "data_sources": "self",
  "ai_system_type": "data analysis tool",
  "uses_personal_data": false,
  "uses_sensitive_data": true,
  "affects_rights_or_opportunities": true,
  "critical_domain": "insurance",
  "serves_vulnerable_users": false,
  "makes_or_recommends_decisions": false,
  "has_human_review": true,
  "has_user_disclosure": true,
  "has_privacy_plan": true,
  "has_bias_testing": true,
  "has_security_plan": true,
  "has_limitations_section": true,
  "has_monitoring_plan": true,
  "possible_harms": "y",
  "mitigation_plan": "y"
}
```
