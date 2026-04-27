#!/usr/bin/env python3
"""
Responsible AI Project Auditor

A single file command line tool for auditing student AI projects through
NIST AI Risk Management Framework aligned questions.

This tool is designed for course projects. It does not provide legal advice.
It produces an educational risk report that can be included in a GitHub repo.
"""

from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


CRITICAL_DOMAINS = {
    "education",
    "employment",
    "finance",
    "healthcare",
    "housing",
    "legal",
    "public services",
    "law enforcement",
    "migration",
    "insurance",
}

DEFAULT_OUTPUT = "responsible_ai_risk_report.md"


@dataclass
class ProjectProfile:
    project_name: str
    project_description: str
    intended_audience: str
    deployment_context: str
    data_sources: str
    ai_system_type: str
    uses_personal_data: bool
    uses_sensitive_data: bool
    affects_rights_or_opportunities: bool
    critical_domain: str
    serves_vulnerable_users: bool
    makes_or_recommends_decisions: bool
    has_human_review: bool
    has_user_disclosure: bool
    has_privacy_plan: bool
    has_bias_testing: bool
    has_security_plan: bool
    has_limitations_section: bool
    has_monitoring_plan: bool
    possible_harms: str
    mitigation_plan: str


@dataclass
class AuditResult:
    score: int
    level: str
    summary: str
    flags: List[str]
    recommended_actions: List[str]
    nist_alignment: Dict[str, List[str]]
    eu_ai_act_note: str
    unesco_note: str
    acm_note: str


def wrap(text: str, width: int = 88) -> str:
    return "\n".join(textwrap.wrap(text.strip(), width=width)) if text.strip() else ""


def ask_text(prompt: str, default: str | None = None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("Please enter a value.")


def ask_yes_no(prompt: str, default: bool | None = None) -> bool:
    while True:
        if default is True:
            suffix = " [Y/n]"
        elif default is False:
            suffix = " [y/N]"
        else:
            suffix = " [y/n]"

        value = input(f"{prompt}{suffix}: ").strip().lower()

        if not value and default is not None:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False

        print("Please answer y or n.")


def ask_choice(prompt: str, choices: List[str], default: str | None = None) -> str:
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"Choose one option{suffix}: ").strip()

        if not value and default is not None:
            return default

        if value.isdigit():
            idx = int(value)
            if 1 <= idx <= len(choices):
                return choices[idx - 1]

        lowered = value.lower()
        for choice in choices:
            if lowered == choice.lower():
                return choice

        print("Please enter a valid number or exact option name.")


def collect_project_profile() -> ProjectProfile:
    print("\nResponsible AI Project Auditor")
    print("This tool creates an educational AI ethics risk report.\n")

    critical_choices = [
        "none",
        "education",
        "employment",
        "finance",
        "healthcare",
        "housing",
        "legal",
        "public services",
        "law enforcement",
        "migration",
        "insurance",
        "other",
    ]

    ai_type_choices = [
        "generative AI assistant",
        "classification model",
        "prediction model",
        "recommendation system",
        "computer vision system",
        "speech or audio system",
        "agentic workflow",
        "data analysis tool",
        "other",
    ]

    return ProjectProfile(
        project_name=ask_text("Project name"),
        project_description=ask_text("Short project description"),
        intended_audience=ask_text("Intended audience"),
        deployment_context=ask_text(
            "Deployment context",
            "course project or prototype"
        ),
        data_sources=ask_text(
            "Data sources",
            "user provided project description and self reported answers"
        ),
        ai_system_type=ask_choice(
            "What kind of AI system is this?",
            ai_type_choices,
            "data analysis tool"
        ),
        uses_personal_data=ask_yes_no("Does it use personal data?", False),
        uses_sensitive_data=ask_yes_no(
            "Does it use sensitive data such as health, biometric, financial, location, race, religion, immigration, or political data?",
            False
        ),
        affects_rights_or_opportunities=ask_yes_no(
            "Could it affect access to education, work, money, housing, healthcare, legal rights, or public services?",
            False
        ),
        critical_domain=ask_choice(
            "Which high impact domain is closest to the project?",
            critical_choices,
            "none"
        ),
        serves_vulnerable_users=ask_yes_no(
            "Is it used by or about vulnerable users such as minors, patients, low income users, or dependent workers?",
            False
        ),
        makes_or_recommends_decisions=ask_yes_no(
            "Does it make or recommend decisions about people?",
            False
        ),
        has_human_review=ask_yes_no("Is there meaningful human review?", True),
        has_user_disclosure=ask_yes_no(
            "Does the project clearly disclose that AI is being used?",
            True
        ),
        has_privacy_plan=ask_yes_no(
            "Does the project include a privacy or data minimization plan?",
            False
        ),
        has_bias_testing=ask_yes_no(
            "Does the project include bias, fairness, or error testing?",
            False
        ),
        has_security_plan=ask_yes_no(
            "Does the project include a security or misuse prevention plan?",
            False
        ),
        has_limitations_section=ask_yes_no(
            "Does the documentation clearly state limitations?",
            True
        ),
        has_monitoring_plan=ask_yes_no(
            "Does the project include monitoring or post deployment review?",
            False
        ),
        possible_harms=ask_text(
            "List possible harms",
            "misleading outputs, overreliance, privacy risk, unfair recommendations"
        ),
        mitigation_plan=ask_text(
            "Current mitigation plan",
            "human review, clear limitations, privacy protection, careful documentation"
        ),
    )


def score_project(profile: ProjectProfile) -> AuditResult:
    score = 0
    flags: List[str] = []
    recommended_actions: List[str] = []

    def add(points: int, flag: str, action: str) -> None:
        nonlocal score
        score += points
        flags.append(flag)
        if action not in recommended_actions:
            recommended_actions.append(action)

    if profile.uses_personal_data:
        add(
            2,
            "The project uses personal data.",
            "Document why each personal data field is necessary and remove nonessential fields."
        )

    if profile.uses_sensitive_data:
        add(
            4,
            "The project uses sensitive data.",
            "Add stricter consent, access control, retention limits, and a stronger privacy review."
        )

    if profile.affects_rights_or_opportunities:
        add(
            4,
            "The project may affect rights, access, or opportunities.",
            "Require human review before any output is used for a consequential decision."
        )

    if profile.critical_domain.lower() in CRITICAL_DOMAINS:
        add(
            3,
            f"The project is connected to a high impact domain: {profile.critical_domain}.",
            "Treat the project as high impact and document risk controls before deployment."
        )

    if profile.serves_vulnerable_users:
        add(
            3,
            "The project involves vulnerable users or affected groups.",
            "Test whether the system creates unequal burden for vulnerable users."
        )

    if profile.makes_or_recommends_decisions:
        add(
            3,
            "The system makes or recommends decisions about people.",
            "Explain that outputs are recommendations and require accountable human judgment."
        )

    if not profile.has_human_review:
        add(
            3,
            "There is no meaningful human review.",
            "Add a human review step for uncertain, harmful, or high impact outputs."
        )

    if not profile.has_user_disclosure:
        add(
            2,
            "Users may not know that AI is being used.",
            "Add a clear AI disclosure statement in the interface and documentation."
        )

    if not profile.has_privacy_plan:
        add(
            2,
            "The privacy plan is missing or incomplete.",
            "Add a privacy section covering collection, use, storage, retention, and deletion."
        )

    if not profile.has_bias_testing:
        add(
            2,
            "Bias, fairness, or error testing is missing.",
            "Add test cases that compare error patterns across relevant user groups or scenarios."
        )

    if not profile.has_security_plan:
        add(
            2,
            "Security or misuse prevention is missing.",
            "Add misuse cases, input validation, access limits, and safe handling of outputs."
        )

    if not profile.has_limitations_section:
        add(
            1,
            "The documentation does not clearly state limitations.",
            "Add a limitations section that explains what the tool should not be used for."
        )

    if not profile.has_monitoring_plan:
        add(
            1,
            "Post deployment monitoring is missing.",
            "Add a simple review plan for errors, complaints, unexpected uses, and updates."
        )

    if score <= 4:
        level = "Low"
        summary = (
            "The project appears to have limited ethical risk based on the answers provided. "
            "Documentation should still explain scope, limits, and user responsibilities."
        )
    elif score <= 10:
        level = "Moderate"
        summary = (
            "The project has manageable ethical risk, but it needs stronger documentation, "
            "testing, and safeguards before any real world use."
        )
    elif score <= 17:
        level = "High"
        summary = (
            "The project has substantial ethical risk. It should not be deployed outside a "
            "controlled class or research context without additional review."
        )
    else:
        level = "Very High"
        summary = (
            "The project may create serious ethical, legal, or social risks. It requires "
            "instructor review, domain expert review, and stronger governance before use."
        )

    if not recommended_actions:
        recommended_actions.append(
            "Keep documentation updated and reassess risk if scope, data, or users change."
        )

    nist_alignment = {
        "Govern": build_govern_notes(profile),
        "Map": build_map_notes(profile),
        "Measure": build_measure_notes(profile),
        "Manage": build_manage_notes(profile, level),
    }

    eu_note = build_eu_ai_act_note(profile, level)
    unesco_note = build_unesco_note(profile)
    acm_note = build_acm_note(profile)

    return AuditResult(
        score=score,
        level=level,
        summary=summary,
        flags=flags,
        recommended_actions=recommended_actions,
        nist_alignment=nist_alignment,
        eu_ai_act_note=eu_note,
        unesco_note=unesco_note,
        acm_note=acm_note,
    )


def build_govern_notes(profile: ProjectProfile) -> List[str]:
    notes = []
    notes.append("The project should assign responsibility for data handling, model behavior, documentation, and user communication.")

    if profile.has_limitations_section:
        notes.append("The project already includes a limitations section, which supports transparent governance.")
    else:
        notes.append("The project needs a limitations section before it can be responsibly shared.")

    if profile.has_human_review:
        notes.append("Human review is included, which supports accountability.")
    else:
        notes.append("Human review is missing, so accountability is weak.")

    return notes


def build_map_notes(profile: ProjectProfile) -> List[str]:
    notes = []
    notes.append(f"Intended audience: {profile.intended_audience}.")
    notes.append(f"Deployment context: {profile.deployment_context}.")
    notes.append(f"Data sources: {profile.data_sources}.")
    notes.append(f"AI system type: {profile.ai_system_type}.")

    if profile.critical_domain.lower() != "none":
        notes.append(f"The system is mapped to a high impact domain: {profile.critical_domain}.")

    return notes


def build_measure_notes(profile: ProjectProfile) -> List[str]:
    notes = []

    if profile.has_bias_testing:
        notes.append("The project includes bias, fairness, or error testing.")
    else:
        notes.append("The project should add bias, fairness, or error testing.")

    if profile.has_privacy_plan:
        notes.append("The project includes a privacy or data minimization plan.")
    else:
        notes.append("The project should add a privacy or data minimization plan.")

    if profile.has_security_plan:
        notes.append("The project includes security or misuse controls.")
    else:
        notes.append("The project should add security or misuse controls.")

    return notes


def build_manage_notes(profile: ProjectProfile, level: str) -> List[str]:
    notes = []
    notes.append(f"Current risk level: {level}.")
    notes.append(f"Known possible harms: {profile.possible_harms}.")
    notes.append(f"Current mitigation plan: {profile.mitigation_plan}.")

    if level in {"High", "Very High"}:
        notes.append("The project should remain in prototype status until additional review is completed.")
    else:
        notes.append("The project may be appropriate for class demonstration if limitations are visible to users.")

    return notes


def build_eu_ai_act_note(profile: ProjectProfile, level: str) -> str:
    high_impact = profile.critical_domain.lower() in CRITICAL_DOMAINS
    consequential = profile.affects_rights_or_opportunities or profile.makes_or_recommends_decisions

    if high_impact and consequential:
        return (
            "EU AI Act reference note: This tool is not making a legal classification. "
            "However, the project has features associated with high impact AI contexts because "
            f"it relates to {profile.critical_domain} and may influence decisions about people. "
            "A real deployment would need stronger documentation, risk controls, transparency, "
            "human oversight, and quality management."
        )

    if level in {"High", "Very High"}:
        return (
            "EU AI Act reference note: The risk score suggests the project should be treated "
            "with caution. Even if it is only a course prototype, the documentation should explain "
            "why it is not being used for prohibited or high risk real world decisions."
        )

    return (
        "EU AI Act reference note: Based on the answers provided, the project does not appear "
        "to be designed for a clearly high risk regulated use. The report should still document "
        "scope limits, user disclosure, and safeguards."
    )


def build_unesco_note(profile: ProjectProfile) -> str:
    if profile.uses_sensitive_data or profile.serves_vulnerable_users:
        return (
            "UNESCO ethics note: Because the project may involve sensitive data or vulnerable "
            "users, it should prioritize human dignity, privacy, fairness, transparency, and "
            "human oversight. The project should avoid replacing human judgment in situations "
            "where people may be harmed."
        )

    return (
        "UNESCO ethics note: The project supports responsible AI when it is transparent about "
        "AI use, respects privacy, avoids unfair treatment, and keeps humans accountable for "
        "important choices."
    )


def build_acm_note(profile: ProjectProfile) -> str:
    if profile.affects_rights_or_opportunities:
        return (
            "ACM ethics note: The project should put public good first, avoid harm, be honest "
            "about limitations, and be especially careful when outputs could affect people's "
            "rights or opportunities."
        )

    return (
        "ACM ethics note: The project should contribute to social good, avoid harm, respect "
        "privacy, and communicate system limits honestly."
    )


def make_markdown_report(profile: ProjectProfile, result: AuditResult) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    flags_text = numbered_list(result.flags or ["No major flags were identified."])
    actions_text = numbered_list(result.recommended_actions)

    nist_sections = []
    for section, notes in result.nist_alignment.items():
        nist_sections.append(f"### {section}\n\n{numbered_list(notes)}")

    profile_json = json.dumps(asdict(profile), indent=2, ensure_ascii=False)

    report = f"""# Responsible AI Risk Report

Generated: {timestamp}

## 1. Project Overview

**Project name:** {profile.project_name}

**Project description:** {profile.project_description}

**Intended audience:** {profile.intended_audience}

**Deployment context:** {profile.deployment_context}

**AI system type:** {profile.ai_system_type}

**Data sources:** {profile.data_sources}

## 2. Overall Risk Rating

**Risk score:** {result.score}

**Risk level:** {result.level}

{wrap(result.summary)}

## 3. Main Risk Flags

{flags_text}

## 4. Recommended Actions

{actions_text}

## 5. NIST AI Risk Management Framework Alignment

This report uses the NIST AI Risk Management Framework structure of Govern, Map, Measure, and Manage.

{chr(10).join(nist_sections)}

## 6. EU AI Act Reference Note

{wrap(result.eu_ai_act_note)}

## 7. UNESCO Ethics Reference Note

{wrap(result.unesco_note)}

## 8. ACM Code of Ethics Reference Note

{wrap(result.acm_note)}

## 9. Potential Harms

{profile.possible_harms}

## 10. Mitigation Plan

{profile.mitigation_plan}

## 11. Limitations of This Audit

1. This tool is educational and does not provide legal advice.
2. The score depends on self reported answers.
3. A low score does not prove that an AI system is safe.
4. High impact projects should receive instructor, domain expert, or institutional review.
5. The tool does not replace compliance review under university policy or applicable law.

## 12. Raw Project Profile

```json
{profile_json}
```
"""
    return report


def numbered_list(items: List[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start=1))


def save_report(report: str, output_path: str) -> Path:
    path = Path(output_path).expanduser().resolve()
    path.write_text(report, encoding="utf-8")
    return path


def demo_profile() -> ProjectProfile:
    return ProjectProfile(
        project_name="Responsible AI Project Auditor",
        project_description=(
            "A command line tool that helps student AI developers identify ethical "
            "risks and generate a responsible AI risk report."
        ),
        intended_audience="students, instructors, and early stage AI project builders",
        deployment_context="course project prototype",
        data_sources="user entered project descriptions and checklist answers",
        ai_system_type="data analysis tool",
        uses_personal_data=False,
        uses_sensitive_data=False,
        affects_rights_or_opportunities=False,
        critical_domain="education",
        serves_vulnerable_users=False,
        makes_or_recommends_decisions=False,
        has_human_review=True,
        has_user_disclosure=True,
        has_privacy_plan=True,
        has_bias_testing=False,
        has_security_plan=True,
        has_limitations_section=True,
        has_monitoring_plan=False,
        possible_harms="overreliance on checklist output and incomplete risk identification",
        mitigation_plan="clear limitations, human review, documentation, and sample reports",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an educational responsible AI risk report."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate a sample report without interactive prompts."
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT,
        help=f"Output Markdown file path. Default: {DEFAULT_OUTPUT}"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the report to the terminal after generation."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.demo:
        profile = demo_profile()
    else:
        profile = collect_project_profile()

    result = score_project(profile)
    report = make_markdown_report(profile, result)
    output_path = save_report(report, args.out)

    print("\nAudit complete.")
    print(f"Risk level: {result.level}")
    print(f"Risk score: {result.score}")
    print(f"Report saved to: {output_path}")

    if args.print:
        print("\n" + report)


if __name__ == "__main__":
    main()
