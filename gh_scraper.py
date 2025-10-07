# JOB SEARCH

# JSON EXAMPLE FROM GH API https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true

import requests, re, pandas as pd
from bs4 import BeautifulSoup

# manually hand picked slugs through gh ex: ("https://boards-api.greenhouse.io/v1/boards/{SLUG}/jobs?content=true")
companies = ["trase","redcellpartners","stripe","airbnb","anaplan","asana",
             "canonical","circleci","cloudflare","lyft","remotecom","robinhood",
             "scaleai","sezzle","spacex","databricks","reddit","coinbase","instacart",
             "figma","vercel","dropbox","radiant","divergent","riotgames","riotgamesup",
             "abnormal","vast","freeformfuturecorp","shein","parallel","crunchyroll"]
skills = [
    # Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift",
    "Kotlin", "Scala",

    # Web / Frontend
    "HTML", "CSS", "Sass", "SCSS", "React", "Next.js", "Redux", "Vue", "Nuxt", "Angular",
    "Svelte", "Tailwind",

    # Backend / Frameworks
    "Node.js", "Express", "NestJS", "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Rails",
    "Laravel", "ASP.NET", ".NET", "GraphQL", "gRPC", "REST",

    # Cloud / DevOps
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD",
    "GitHub Actions", "GitLab CI", "Jenkins",

    # Databases / Streaming
    "SQL", "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "DynamoDB", "Cassandra",
    "Elasticsearch", "Snowflake", "Redshift", "BigQuery", "Kafka", "Airflow", "Spark", "Hadoop",

    # Data / ML / AI
    "Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch", "Keras",

    # Testing / QA
    "Pytest", "JUnit", "Selenium", "Playwright", "Cypress", "Jest", "Mocha",

    # Mobile
    "Android", "iOS", "SwiftUI", "Objective-C", "React Native", "Flutter",

    # Observability / Security
    "Prometheus", "Grafana", "Datadog", "New Relic", "Splunk", "Sentry", "ELK Stack",
    "OAuth", "OIDC", "SAML", "TLS", "OWASP",

    # Tools / OS
    "Linux", "Unix", "Bash", "Shell", "Git"]

degrees = ["Bachelors, Master, Associate"]

def extract_skills(text):
    found = [s for s in skills if re.search(rf"\b{s}\b", text, re.I)]
    return ", ".join(found)

def extract_degrees(text):
    found = [d for d in degrees if re.search(rf"\b{d}\b", text, re.I)]
    return ", ".join(found)

rows = []

for c in companies:
    url = f"https://boards-api.greenhouse.io/v1/boards/{c}/jobs?content=true"
    try:
        data = requests.get(url, timeout=10).json() # get response object as JSON

        for job in data.get("jobs", []):

            title = job.get("title", "")
            loc = (job.get("location", {}) or {}).get("name", "")

            # bs4 searches for content field which contains html, parses it, then removes elements and trailing/leading whitespace
            desc = BeautifulSoup(job.get("content", ""), "html.parser").get_text(" ", strip=True)

            skills_found = extract_skills(desc)
            degrees_found = extract_degrees(desc)

            rows.append({
                "company": c,
                "title": title,
                "location": loc,
                "skills": skills_found,
                "degree": degrees_found,
                "url": job.get("absolute_url", "")
            })
        print(f"{c}: {len(rows)} jobs total")
    except Exception as e:
        print(f"{c}: {e}")

# pandas lib to convert list to csv
pd.DataFrame(rows).to_csv("jobs.csv", index=False)
print("Done!")

