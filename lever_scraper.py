import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup


# https://app.theirstack.com/search/companies/new?query=N4IgjgrgpgTgniAXKADgQwOZSQBgDQgA2AlgLbEAuSATAKwED2MAJrAPoBGCiA2qKwGcAxkgoxoBAGbEohZkhBCGAO2mtlQ7AF88-KMNHioUmXIUArBhwEgdeg4jESQ02fMQhlEUm0vXbALoEHIQQMGxKpOjKcGzMaBRohs7EGqGsbBQMiYRsMPoQhBQ2jkYEkdGxFFBCABbKDIQMGLECoRhsTEg8RFAAbrAgATogaBBZbAJQaDB1yVBaQA

# lever company slugs pulled from https://theirstack.com/en/technology/lever
companies = ["spotify","welocalize","gopuff","plexus","xero","farfetch","shieldai","matchgroup",
            "google", "apple","microsoft","amazon","meta","openai","netflix","nvidia","tesla","uber",
            "airbnb","lyft","doordash","stripe","square","block","paypal","shopify","spotify","zoom","slack",
            "atlassian","asana","notion","figma","adobe","dropbox","cloudflare","databricks","snowflake","palantir",
            "splunk","mongodb","elastic","redhat","digitalocean","twilio","sendgrid","okta","auth0","hashicorp","datadog",
            "newrelic","zendesk","workday","servicenow","oracle","sap","intel","amd","qualcomm","arm","rivian",
            "lucid","waymo","cruise","roblox","unity","epicgames","riotgames","blizzard","discord","tiktok",
            "bytedance","pinterest","snap","twitter","x","reddit","yelp","indeed","linkedin","glassdoor","github","gitlab",
            "canonical","vercel","netlify","heroku","fastly","akamai","hp","hpe","ibm","cisco","juniper",
            "arista","seagate","westerndigital","niantic","magicleap","oculus","bolt","affirm","brex","robinhood",
            "coinbase","binance","rippling","gusto","lever","greenhouse","scaleai","runwayml","perplexity","anthropic","deeplearningai",
            "midjourney","stabilityai","cohere","ai21labs","adeptai","characterai","rekaai","mistral","huggingface","deepmind","wave",
            "datastax","couchbase","timescale","singleStore","cockroachlabs","confluent","segment","muleSoft","zapier","ifttt",
            "mixpanel","amplitude","heap","plaidsystems","truework","checkout","klarna","revolut","chime","sofi","n26","monzo",
            "starlingbank","wise","stripeatlas","pilotcom","remotecom","deel","papaya-global","justworks","bamboohr","namely","lattice","workhuman",
            "personio","hibob","pave","figment","alchemy","quicknode","infura","etherscan","chainalysis","elliptic","consensys","dapperlabs",
            "immutable","openSea","rarible","foundationapp","superrare","magiceden","phantom","ledger","trezor","bitgo","fireblocks","moonpay",
            "circle","anchorage","kraken","okx","crypto","bybit","gateio","huobi","poloniex","blockdaemon","figma","linear","height","shortcut","lubhouseio",
            "jira","confluence","monday","clickup","smartsheet","notion","coda","airtable","miro","mural","loom","fivetran","airbyte",
            "matillion","hevodata","stitchdata","talend","pentaho","dbt","mode","lookerstudio","tableau","qlik","powerbi","atomiq",
            "bigcommerce","wix","squarespace","webflow","framer","bubble","retool","internal","zapier","make","autocode","bolttech","twic",
            "modernhealth","ginger","talkspace","headspace","calm","noom","perchcredit","nav","experian","equifax","transunion","rocketloans",
            "better","blend","homeward","flyhomes","opendoor","zillow","redfin","compass","realtor","trulia","yext","docusign","hellosign",
            "echoSign","evernote","todoist","anydo","thingsapp","omnifocus","notability","goodnotes","procreate","autodesk","ansys","ptc",
            "siemens-digital","bosch","schneider","abb","rockwellautomation","generalelectric","honeywell","johnsoncontrols","trimble","garmin",
            "fitbit","whoop","oura","eightSleep","peloton","tonal","mirror","lululemonstudio","tovala","oxo","dyson","iRobot","ecovacs","yalehome",
            "augusthome","ring","nestlabs","arlo","wyze","simplisafe","zscaler","fortinet","paloaltonetworks","checkpoint","crowdstrike","sentinelone",
            "okta","auth0","duosecurity","1password","lastpass","bitwarden","keepersecurity","malwarebytes","sophos","nortonlifelock",
            "mcafee","tanium","dataminr","relsci","openGov","socrata","tylertech","esri","autodesk","sketch","corel","affinity","pixar",
            "ilm","dneg","weta","framestore","sonyimageworks","ubisoft","ea","activision","take2","bethesda","bungie","insomniacgames",
            "naughtyDog","suckerpunch","cdprojekt","larianstudios","supercell","king","miniclip","niantic","supernatural","beatgames","metaquest",
            "valve","steam","logitech","corsair","razer","steelseries","alienware","maingear","originpc","xbox","playstation","nintendo",
            "bandainamco","sega","konami","squareenix","capcom","trellix","rapid7","arcticwolf","snyk","veracode","checkmarx","alic",
            "gremlin","honeycomb","sentry","rollbar","datadog","logDNA","sumologic","graylog","newrelic","pagerduty","opsgenie","victorops",
            "grafana","prometheus","chronosphere","lightstep","apmtools","terraform","pulumi","ansible","chef","puppet","kubernetes",
            "docker","portainer","rancher","openshift","confluent","rabbitmq","kafka","flink","beam","spark","hadoop","cloudera","hortonworks",
            "mapr","datameer","trifacta","alteryx","rapidminer","knime","crunchbase","pitchbook","cbinsights","accelerated","sigopt","weave","woven","splice","segment",
            "posthog","fullstory","hotjar","crazyegg","clarity","mixpanel","amplitude","heap","cockroachlabs","materialize","rockset","firebolt","starburstdata","databricks",
            "lakefs","minio","wasabi","backblaze","box","dropbox","pcloud","telegram","signal","whatsapp","viber","line","kakao","wechat","qq","baidu","alibaba","tencent",
            "jd","meituan","didi","xiaomi","huawei","oppo","vivo","oneplus","nothingtech","sony","samsung","lg","panasonic","toshiba","fujitsu","nec","jvc","olympus","nikon",
            "canon","dji","parrot","skydio","zipline","wing","matternet","amazonrobotics","bostonDynamics","agilityRobotics","aws","gcp","azure","oraclecloud","ibmcloud","linode",
            "rackspace","ovh","alicloud","cloudsigma","wasabisystems","cloudways","flyio","render","railway","heroku","supabase","planetscale","neon","tidb","tidal","howl","pandora","iheartradio",
            "sonos","roku","hulu","peacock","paramountplus","max","disneyplus","espn","fox","cbsinteractive","nbcuniversal","viacom","rokuinc","cineplex","imax","fandango",
            "atomtickets","redditinc","quora","stackexchange","stackoverflow","slackhq","asana","clickup","flow","wrike","shift","slite","slab","gitkraken","sourcegraph",
            "jetbrains","intellij","pycharm","webstorm","clion","phpstorm","postman","insomnia","swaggerhub","stoplight","rapidapi","konghq","tyk","gravitee","amazonprimevideo",
            "amazonmusic","amazonfresh","wholefoods","zappos","backcountry","wayfair","etsy","mercari","newegg","rakuten","shopifyplus","bigcommerce","walmartlabs","targettech",
            "costcotech","homeDepotTech","lowestech","sears","bestbuy","ticketmaster","eventbrite","seatGeek","stubhub","vividseats","expedia","booking","airbnb","trivago","kayak",
            "hopper","agoda","viator","tripadvisor","klook","carnivaltech","princesscruises","virginvoyages","teslamotors","ford","gm","stellantis","toyota","honda","mazda",
            "subaru","volkswagen","audi","bmw","mercedesbenz","porsche","rimac","faradayfuture","nio","xpeng","byd","lucidmotors","fisker","boltev","rivian","waymo","argoai","aurora",
            "embarktrucks","tuSimple","cruiseautomation","nuro","neura","gehealthcare","medtronic","abbott","bostonscientific","stryker","intuitiveSurgical","varian","philips",
            "siemenshealthineers","roche","illumina","thermofisher","perkinelmer","agilent","10xgenomics","celsius","carbonhealth","forwardhealth","oneMedical","omadahealth",
            "noomhealth","beyondmeat","impossiblefoods","perfectday","justegg","upsidedfoods","meati","boweryfarming","plenty","aerofarms","farmwise","indigoag","cropx","granular",
            "climatecorp","sentera","dronedeploy","skyspecs","satellogic","planetlabs","spacex","blueorigin","rocketlab","relativityspace","astra","fireflyspace","momentus","leoLabs",
            "viasat","oneweb","starlink","iridium","boeing","airbus","lockheedmartin","raytheon","northropgrumman","l3harris","baeSystems","generalDynamics","kratos","palantirTech","anduril",
            "shieldai","rebellionaerospace","hadrian","possible","openrobotics","paradoxai","eightfoldai","gemini","setapp","pocket","instapaper","feedly","newsbreak","flipboard",
            "medium","substack","patreon","gumroad","teachable","skillshare","udemy","coursera","edx","brilliant","khanacademy","duolingo","babbel","busuu","cambly","italki",
            "rosettastone","prodigygame","epic","byjus","unacademy","vedantu","chegg","studycom","quizlet","kahoot","coursehero","tesol","canva","picmonkey","fotor","befunky",
            "pixlr","gimp","inkscape","affinityphoto","davinciresolve","filmicpro","lightricks","capcut","spliceapp","vsco","afterlight","adobepremiere","finalcutpro","garageband","logicpro",
            "ableton","protools","flstudio","reaper","bandlab","soundcloud","tunecore","dittoMusic","cdBaby","ubicity","citymapper","moovit","transitapp","uberfreight","convoy",
            "flexport","project44","fourkites","shippo","shipbob","easyship","deliverr","instacart","gopuff","ubereats","grubhub","doordash","postmates","caviar","chownow","toasttab",
            "lightspeedhq","clover","squareup","revelsystems","touchbistro","zenreach","zingle","spoton","sevenrooms","opentable","resy","mindbody","classpass","zenoti","vagaro",
            "glossgenius","styleSeat","theknot","zola","honeybook","dubsado","freshbooks","waveapps","xero","quickbooks","intuit","bench","pilot","parafin","ramp","divvy","expensify",
            "brex","airbase","ixos","billdotcom","coupa","ariba","ziphq","ziprecruiter","indeedflex","glassdoortech","monster","dice","hired","wellfound","angelList","turing",
            "andela","gigster","crossover","gun","levelsio","remoteok","wework","industrious","regus","pacificworkplaces","liquidspace"]

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

DEGREE_PATTERNS = {
    "Bachelor":  r"\b(bachelor'?s|ba|b\.?a\.?|bs|b\.?s\.?|bsc)\b",
    "Master":    r"\b(master'?s|ms|m\.?s\.?|msc|meng|m\.?eng\.?)\b",
    "MBA":       r"\b(mba)\b",
    "PhD":       r"\b(ph\.?d\.?|phd|dphil)\b",
}

def clean(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return " ".join(soup.get_text(" ", strip=True).split())

# both extract functions use regex to find skills and or degrees
def extract_skills(text):
    return [s for s in skills
            # (?<!\w): negative lookbehind | (?!\w): negative lookahead | re.I
            if re.search(rf"(?<!\w){re.escape(s)}(?!\w)", text, re.I)]

def extract_degrees(text: str) -> str:
    found = []
    for label, pat in DEGREE_PATTERNS.items():
        if re.search(pat, text, flags=re.IGNORECASE):
            found.append(label)
    return ", ".join(found)

rows = []

for company in companies:
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    r = requests.get(url)
    if not r.ok:
        print(f"Failed {company}")
        continue

    for job in r.json():
        title = job.get("text", "")
        loc = (job.get("categories") or {}).get("location", "")
        desc = (job.get("descriptionPlain") or "") or clean(job.get("description", ""))

        skills_found = extract_skills(desc)
        degrees_found = extract_degrees(desc)


        skills_str = ", ".join(skills_found)
        skills_json = json.dumps({s: 1 for s in skills_found}) if skills_found else ""  # empty if none

        rows.append({
            "company": company,
            "title": title,
            "location": loc,
            "skills": skills_str,
            "degree": degrees_found,  # optional: you can add degree regex here
            "url": job.get("hostedUrl", ""),
            "skills_json": skills_json
        })

# pandas lib to convert list to csv
pd.DataFrame(rows).to_csv("lever_jobs.csv", index=False)
print("Done!")
