from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from pypdf import PdfReader


UI_EN = {
    "nav": {
        "about": "About",
        "experience": "Experience",
        "education": "Education",
        "skills": "Skills",
        "projects": "Projects",
        "contact": "Contact",
    },
    "sections": {
        "about": "About",
        "experience": "Experience",
        "education": "Education",
        "skills": "Skills",
        "projects": "Projects",
        "certifications": "Certifications",
        "contact": "Contact",
    },
    "actions": {
        "email": "Email",
        "downloadCv": "Download CV",
    },
    "labels": {
        "viewLinkedin": "LinkedIn",
        "location": "Location",
    },
}

UI_LT = {
    "nav": {
        "about": "Apie",
        "experience": "Patirtis",
        "education": "Išsilavinimas",
        "skills": "Įgūdžiai",
        "projects": "Projektai",
        "contact": "Kontaktai",
    },
    "sections": {
        "about": "Apie",
        "experience": "Patirtis",
        "education": "Išsilavinimas",
        "skills": "Įgūdžiai",
        "projects": "Projektai",
        "certifications": "Sertifikatai",
        "contact": "Kontaktai",
    },
    "actions": {
        "email": "El. paštas",
        "downloadCv": "Atsisiųsti CV",
    },
    "labels": {
        "viewLinkedin": "LinkedIn",
        "location": "Vieta",
    },
}


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    return "\n\n---PAGE---\n\n".join((page.extract_text() or "") for page in reader.pages)


def normalize(text: str) -> str:
    replacements = {
        "\u00a0": " ",
        "Â": "",
        "â€”": "-",
        "â€“": "-",
        "â€œ": '"',
        "â€\x9d": '"',
        "â€ž": '"',
        "Å³": "ų",
        "RegistrÅ³": "Registrų",
        "AB â€žEnergijos skirstymo operatoriusâ€œ (ESO)": "AB Energijos skirstymo operatorius (ESO)",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def block_between(text: str, start: str, end: str | None = None) -> str:
    pattern = re.escape(start) + r"\s*(.*?)"
    if end:
        pattern += re.escape(end)
    else:
        pattern += r"$"

    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""


def clean_lines(block: str) -> list[str]:
    lines = [line.strip() for line in block.splitlines()]
    output: list[str] = []
    for line in lines:
        if not line or line == "---PAGE---":
            continue
        if line.startswith("Page "):
            continue
        output.append(line)
    return output


def parse_contact(text: str) -> dict[str, str]:
    email_match = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", text)
    phone_match = re.search(r"\+\d{8,15}", text)

    linkedin_match = re.search(
        r"www\.linkedin\.com/in/[A-Za-z0-9\-\n]+", text,
        flags=re.IGNORECASE,
    )
    linkedin = "TODO_LINKEDIN"
    if linkedin_match:
        linkedin = linkedin_match.group(0).replace("\n", "")
        if linkedin.startswith("www"):
            linkedin = "https://" + linkedin

    return {
        "email": email_match.group(0) if email_match else "TODO_EMAIL",
        "linkedin": linkedin,
        "phone": phone_match.group(0) if phone_match else "",
        "note": "Open to data science and AI roles where I can deliver measurable business impact.",
    }


def parse_profile(text: str) -> dict[str, Any]:
    summary_block = block_between(text, "Summary", "Experience")
    summary = " ".join(clean_lines(summary_block))

    name_match = re.search(r"\n([A-Za-z]+\s+[A-Za-z]+)\nPhD in Economics", text)
    location_match = re.search(r"PhD in Economics\s*\n([^\n]+)", text)

    return {
        "name": name_match.group(1) if name_match else "Aleksejus Sosidko",
        "title": "Senior Data Scientist | PhD in Economics",
        "summary": summary or "TODO: Add professional summary.",
        "location": location_match.group(1) if location_match else "Vilnius, Lithuania",
        "photo": {
            "src": "assets/profile-placeholder.svg",
            "alt": "Placeholder portrait for Aleksejus Sosidko",
        },
    }


def parse_certifications(text: str) -> list[str]:
    block = block_between(text, "Certifications", "Aleksejus Sosidko")
    lines = clean_lines(block)
    if not lines:
        return ["TODO: Add certifications"]

    combined: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "Generative AI with Large Language" and i + 1 < len(lines):
            combined.append(line + " " + lines[i + 1])
            i += 2
            continue
        combined.append(line)
        i += 1

    return combined


def build_experience_en() -> list[dict[str, Any]]:
    return [
        {
            "role": "Senior Data Scientist",
            "company": "Registrų centras",
            "period": "October 2024 - Present",
            "location": "Vilnius, Lithuania",
            "highlights": [
                "Lead end-to-end Document AI and LLM initiatives for workflow automation.",
                "Build ingestion pipelines for PDF, DOCX, scanned images, and archive containers.",
                "Transform unstructured documents into structured JSON with schema validation.",
                "Define prompt engineering standards and deterministic normalization rules.",
                "Run iterative evaluation loops with error analysis and regression checks.",
                "Implement human-in-the-loop controls for specialist quality assurance.",
            ],
        },
        {
            "role": "Data Scientist",
            "company": "AB Energijos skirstymo operatorius (ESO)",
            "period": "March 2021 - August 2024",
            "location": "Vilnius, Lithuania",
            "highlights": [
                "Built and maintained end-to-end ML pipelines for operational decision support.",
                "Delivered Mass Outage Forecasting models on tabular utility data.",
                "Built NLP workflows for contractor documentation quality assessment.",
                "Applied computer vision to validate network data from LV cable cabinet schemes.",
            ],
        },
        {
            "role": "Machine Learning Intern",
            "company": "Vinted / Kleiderkreisel",
            "period": "October 2020 - December 2020",
            "location": "Vilnius, Lithuania",
            "highlights": [
                "TODO: Add key internship achievements and impact metrics.",
            ],
        },
        {
            "role": "Data Analyst",
            "company": "OC VISION",
            "period": "April 2017 - December 2019",
            "location": "Lithuania",
            "highlights": [
                "Owned reporting and business analysis workflows.",
                "Improved report clarity and usability for decision-makers.",
                "Created new reports that supported business go/no-go decisions.",
                "Mentored teammates on efficient use of MS Excel and Axapta.",
            ],
        },
        {
            "role": "Analyst",
            "company": "RJF Baltic",
            "period": "June 2016 - April 2017",
            "location": "Lithuania",
            "highlights": [
                "Delivered reporting, budgeting, and financial analysis.",
                "Supported cash-flow control and management reporting.",
            ],
        },
        {
            "role": "Economist",
            "company": "Kelvista",
            "period": "August 2015 - June 2016",
            "location": "Lithuania",
            "highlights": [
                "Owned budgeting and reporting tasks.",
                "Created and implemented a project evaluation framework.",
            ],
        },
        {
            "role": "Customer Support Specialist",
            "company": "Swedbank Lietuvoje",
            "period": "May 2014 - August 2015",
            "location": "Lithuania",
            "highlights": [
                "Provided support for banking products, loans, pension, and insurance topics.",
            ],
        },
        {
            "role": "Analyst",
            "company": "RJF Baltic",
            "period": "May 2014 - August 2015",
            "location": "Lithuania",
            "highlights": [
                "Performed financial analysis and budgeting.",
                "Created the company budgeting framework from scratch.",
            ],
        },
        {
            "role": "Human Resources Specialist",
            "company": "RJF Baltic",
            "period": "January 2013 - May 2014",
            "location": "Lithuania",
            "highlights": [
                "Managed blue-collar recruitment in Lithuania and abroad.",
            ],
        },
    ]


def build_education_en() -> list[dict[str, Any]]:
    return [
        {
            "institution": "Mykolas Romeris University",
            "degree": "PhD in Economics",
            "period": "2017 - 2022",
            "details": [],
        },
        {
            "institution": "Mykolas Romeris University",
            "degree": "Master's degree in Economics",
            "period": "2013 - 2015",
            "details": [],
        },
    ]


def build_skills_en(text: str) -> dict[str, list[str]]:
    block = block_between(text, "Top Skills", "Certifications")
    extracted = clean_lines(block)

    technical = {
        "Machine Learning Algorithms",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision",
        "Prompt Engineering",
        "Document AI",
    }
    technical.update(extracted)

    return {
        "technical": sorted(technical),
        "tools": ["Python", "JSON", "Excel", "Axapta"],
        "languages": ["Lithuanian", "English"],
    }


def build_projects_en() -> list[dict[str, str]]:
    return [
        {
            "name": "Mass Outage Forecasting",
            "summary": "Tabular ML forecasting for utility outage planning and response.",
            "link": "",
        },
        {
            "name": "Contractor Documentation Quality Assessment",
            "summary": "NLP solution for document quality checks and process consistency.",
            "link": "",
        },
        {
            "name": "Network Data Validation from LV Cable Cabinet Schemes",
            "summary": "Computer vision pipeline to validate network data against source schemes.",
            "link": "",
        },
    ]


def build_en_content(text: str) -> dict[str, Any]:
    return {
        "ui": UI_EN,
        "profile": parse_profile(text),
        "contact": parse_contact(text),
        "experience": build_experience_en(),
        "education": build_education_en(),
        "skills": build_skills_en(text),
        "projects": build_projects_en(),
        "certifications": parse_certifications(text),
    }


def build_lt_content(en: dict[str, Any]) -> dict[str, Any]:
    lt = deepcopy(en)
    lt["ui"] = UI_LT

    lt["profile"]["title"] = "Vyresnysis duomenų mokslininkas | Ekonomikos mokslų daktaras"
    lt["profile"]["summary"] = (
        "Vyresnysis duomenų mokslininkas, turintis patirties tabulinių duomenų, NLP ir kompiuterinės regos srityse. "
        "Kuriu AI sprendimus, kurie automatizuoja procesus, gerina kokybę ir padeda priimti sprendimus energetikos "
        "bei viešojo sektoriaus organizacijose."
    )
    lt["contact"]["note"] = "Atviras duomenų mokslo ir AI pozicijoms, kuriose svarbus aiškus verslo poveikis."

    lt["experience"] = [
        {
            "role": "Vyresnysis duomenų mokslininkas",
            "company": "Registrų centras",
            "period": "2024 spalis - dabar",
            "location": "Vilnius, Lietuva",
            "highlights": [
                "Vadovauju Document AI ir LLM iniciatyvoms, skirtoms procesų automatizavimui.",
                "Kuriu dokumentų įkėlimo srautus PDF, DOCX, skenuotiems vaizdams ir archyvams.",
                "Nestruktūrizuotą tekstą paverčiu į struktūrizuotą JSON su schemų validacija.",
                "Diegiu promptų inžinerijos standartus ir deterministines normalizavimo taisykles.",
                "Vykdau nuolatinius kokybės vertinimo ciklus su klaidų analize.",
                "Įdiegiu human-in-the-loop kontrolę galutiniam ekspertų patvirtinimui.",
            ],
        },
        {
            "role": "Duomenų mokslininkas",
            "company": "AB Energijos skirstymo operatorius (ESO)",
            "period": "2021 kovas - 2024 rugpjūtis",
            "location": "Vilnius, Lietuva",
            "highlights": [
                "Kūriau ir palaikiau pilnus ML sprendimų ciklus operaciniams sprendimams.",
                "Sukūriau masinių elektros tiekimo sutrikimų prognozavimo modelius.",
                "Kūriau NLP sprendimus rangovų dokumentacijos kokybės vertinimui.",
                "Taikiau kompiuterinę regą tinklo duomenų validavimui pagal schemų vaizdus.",
            ],
        },
        {
            "role": "Mašininio mokymosi praktikantas",
            "company": "Vinted / Kleiderkreisel",
            "period": "2020 spalis - 2020 gruodis",
            "location": "Vilnius, Lietuva",
            "highlights": ["TODO: Papildykite praktikos pasiekimus ir poveikio rodiklius."],
        },
        {
            "role": "Duomenų analitikas",
            "company": "OC VISION",
            "period": "2017 balandis - 2019 gruodis",
            "location": "Lietuva",
            "highlights": [
                "Atsakiau už ataskaitų ruošimą ir verslo analizę.",
                "Pagerinau ataskaitų aiškumą ir panaudojamumą vadovų sprendimams.",
                "Sukūriau naujas ataskaitas, padėjusias priimti verslo sprendimus.",
                "Padėjau komandai efektyviau dirbti su MS Excel ir Axapta.",
            ],
        },
        {
            "role": "Analitikas",
            "company": "RJF Baltic",
            "period": "2016 birželis - 2017 balandis",
            "location": "Lietuva",
            "highlights": [
                "Vykdžiau ataskaitų rengimą, biudžetavimą ir finansinę analizę.",
                "Prisidėjau prie pinigų srautų kontrolės ir valdymo ataskaitų.",
            ],
        },
        {
            "role": "Ekonomistas",
            "company": "Kelvista",
            "period": "2015 rugpjūtis - 2016 birželis",
            "location": "Lietuva",
            "highlights": [
                "Atsakiau už biudžetavimo ir ataskaitų procesus.",
                "Sukūriau ir įdiegiau projektų vertinimo sistemą.",
            ],
        },
        {
            "role": "Klientų aptarnavimo specialistas",
            "company": "Swedbank Lietuvoje",
            "period": "2014 gegužė - 2015 rugpjūtis",
            "location": "Lietuva",
            "highlights": [
                "Konsultavau kasdienių bankinių paslaugų, paskolų, pensijų ir draudimo klausimais.",
            ],
        },
        {
            "role": "Analitikas",
            "company": "RJF Baltic",
            "period": "2014 gegužė - 2015 rugpjūtis",
            "location": "Lietuva",
            "highlights": [
                "Atlikau finansinę analizę ir biudžetavimą.",
                "Sukūriau įmonės biudžeto sistemą nuo nulio.",
            ],
        },
        {
            "role": "Personalo specialistas",
            "company": "RJF Baltic",
            "period": "2013 sausis - 2014 gegužė",
            "location": "Lietuva",
            "highlights": [
                "Organizavau darbininkų atranką Lietuvoje ir užsienyje.",
            ],
        },
    ]

    lt["education"] = [
        {
            "institution": "Mykolo Romerio universitetas",
            "degree": "Ekonomikos mokslų daktaras",
            "period": "2017 - 2022",
            "details": [],
        },
        {
            "institution": "Mykolo Romerio universitetas",
            "degree": "Ekonomikos magistras",
            "period": "2013 - 2015",
            "details": [],
        },
    ]

    lt["skills"]["languages"] = ["Lietuvių", "Anglų"]

    lt["projects"] = [
        {
            "name": "Masinių sutrikimų prognozavimas",
            "summary": "Tabulinių duomenų ML modeliai elektros tiekimo sutrikimų planavimui ir reagavimui.",
            "link": "",
        },
        {
            "name": "Rangovų dokumentacijos kokybės vertinimas",
            "summary": "NLP sprendimas dokumentų kokybei ir proceso nuoseklumui vertinti.",
            "link": "",
        },
        {
            "name": "Tinklo duomenų validavimas pagal žemųjų įtampų spintų schemas",
            "summary": "Kompiuterinės regos sprendimas tinklo duomenų tikrinimui pagal pirminius brėžinius.",
            "link": "",
        },
    ]

    lt["certifications"] = [
        "Generative AI with Large Language Models",
        "AI for Everyone",
        "Deep Learning Specialization",
        "Machine Learning Specialization",
        "Artificial Intelligence",
    ]

    return lt


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract and normalize CV content from PDF into structured JSON.")
    parser.add_argument("--pdf", default="assets/cv/CV_A_Sosidko.pdf", help="Input CV PDF path")
    parser.add_argument("--out-dir", default="content", help="Output folder")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_text = extract_text(Path(args.pdf))
    normalized = normalize(raw_text)

    (out_dir / "cv_extracted_raw.txt").write_text(normalized, encoding="utf-8")

    en = build_en_content(normalized)
    lt = build_lt_content(en)

    (out_dir / "cv.en.json").write_text(json.dumps(en, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "cv.lt.json").write_text(json.dumps(lt, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Generated content files:")
    print(out_dir / "cv_extracted_raw.txt")
    print(out_dir / "cv.en.json")
    print(out_dir / "cv.lt.json")


if __name__ == "__main__":
    main()
