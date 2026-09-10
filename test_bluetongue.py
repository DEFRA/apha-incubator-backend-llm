#!/usr/bin/env python
"""Test the API with bluetongue virus text."""
import requests
import json
import time

API_URL = "http://localhost:8000"

# The bluetongue text
bluetongue_text = """**Key findings**

- As of 03 Sep 2026, bluetongue virus serotype 3 (BTV-3) has been confirmed on 825 premises across Great Britain during the 2026–2027 season: 720 in England, 85 in Wales, and 20 in Scotland; no cases have been reported in Northern Ireland.
- On 02 Sep 2026, 30 new BTV-3 premises were confirmed in a single day across nine English counties (Cumbria, Derbyshire, Devon, Dorset, Lancashire, Leicestershire, North Yorkshire, Shropshire, and Staffordshire), three sites in Wales (Carmarthenshire and Neath Port Talbot), and one site in Scotland (Dumfries and Galloway).
- Among confirmed affected animals as of 03 Sep 2026, 1340 were sheep, 330 were cattle, five were alpacas, and one was a llama; the highest concentration of confirmed premises between 10 Jul–02 Sep 2026 was in Devon (343), followed by Cornwall (117) and Somerset (91).
- As of 02 Sep 2026, 2462 potential BTV-3 cases remained under investigation across Great Britain, with veterinary experts in Cumbria warning of a three-week delay in confirming suspected cases.
- The UK Animal and Plant Health Agency (APHA) expanded testing to its Weybridge laboratories on 25 Aug 2026 to address what it described as an "unprecedented scale" of outbreak, working alongside The Pirbright Institute (the National Reference Laboratory for bluetongue).
- The UK Chief Veterinary Officer and Farming Minister issued a public alert on 14 Aug 2026 urging livestock keepers to vaccinate immediately, citing hot and humid weather as a driver of increased midge activity; three BTV-3 vaccines have been authorized for use in Great Britain, though access delays have been reported by farmers and raised in the House of Commons on 02 Sep 2026.
**Epidemiological analysis and public health impact**

- The geographic spread of BTV-3 across England, Wales, and Scotland within a single season represents a significant escalation in spatial extent compared to prior UK BTV activity. The simultaneous presence of confirmed premises in nine English counties, multiple Welsh counties, and southern Scotland indicates that vector-mediated transmission is not contained within a single region and that livestock movement—even under restricted-zone conditions—may be contributing to dispersal.
- The detection of 820 of 825 confirmed premises through clinical sign reporting, rather than proactive surveillance, underscores a passive detection bias. Because diagnostic testing covers only a subset of animals per premises, official animal-level counts (1340 sheep, 330 cattle) are acknowledged to substantially underestimate true infection burden; the true scale of the epizootic in susceptible livestock populations is likely considerably larger.
- The confirmed extension of BTV-3 into Scotland—a country with no prior confirmed cases in the current season until recently— and the establishment of a temporary control zone in South West Scotland on 20 Aug 2026 signals a northward geographic progression. Scotland's historically lower exposure to bluetongue vectors and lower baseline vaccination coverage among livestock keepers may render its livestock population more immunologically naïve and therefore more vulnerable to rapid spread.
- Vaccine deployment logistics represent a critical operational bottleneck. Immunity requires three weeks after the first dose in sheep and six weeks in cattle, meaning animals vaccinated during the current peak transmission window (July–September) will not be fully protected until after the period of highest midge activity. Delays in vaccine access, raised at Prime Minister's Questions on 02 Sep 2026, risk leaving large numbers of susceptible animals unprotected during the most epidemiologically active phase of the season.
- The economic and animal welfare consequences are substantial. Farmers in affected areas have drawn explicit parallels to the 2001 foot-and-mouth disease outbreak in terms of operational disruption. Movement restrictions, germinal product licensing requirements, and strain on veterinary diagnostic capacity—requiring APHA to expand testing infrastructure—indicate that the outbreak is placing significant pressure on the UK's agricultural and veterinary systems.
**Comparative analysis and future outlook**

- BTV-3 has a significant historical precedent that provides important context for the current European situation. The first confirmed outbreak of bluetongue outside Africa occurred in sheep in Cyprus in 1943. The virus isolated during that outbreak was subsequently classified as bluetongue virus serotype 3 (BTV-3). The Onderstepoort reference laboratory in South Africa, which identified the virus, later regarded the Cyprus strain as one of the most pathogenic bluetongue virus strains ever identified. The isolate was attenuated in embryonated eggs at Onderstepoort, and the resulting vaccine was used successfully in Cyprus in 1946 and 1947, helping to curtail the outbreak ([Onderstepoort, pg 116](https://www.vethistorysa.co.za/PDF/VHSA_Part_3.pdf?utm); [Durr PA, et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5517479/)). This historical example illustrates both the potential severity of BTV-3 in sheep and the value of effective vaccination when a suitable vaccine is available.
- BTV-3 first emerged in northwestern Europe in September 2023, when clinical manifestations were confirmed in sheep in the Netherlands; the virus was determined to be serotype 3 by whole genome sequencing (WGS) ([Holwerda M, et al. 2024](https://wwwnc.cdc.gov/eid/article/30/8/23-1331_article)). After the outbreak began in the Netherlands, confirmed cases escalated rapidly: within three weeks, the total number of polymerase chain reaction (PCR)-positive flocks and herds reached 324 sheep flocks, 61 cattle herds, and one goat herd ([Holwerda M, et al. 2024](https://wwwnc.cdc.gov/eid/article/30/8/23-1331_article)). The 2026–2027 UK season, with 825 confirmed premises by early September and 2462 under investigation, represents a substantially larger and more geographically dispersed event than the initial 2023 continental emergence, reflecting the virus's establishment and overwintering capacity in northern European vector populations.
- The trajectory through September 2026 points toward continued escalation before any seasonal decline. For midges, populations rising above an abundance threshold may provide an early warning, and such events have been theoretically implicated in increased establishment of midge-borne pathogens like bluetongue ([*EFSA *and* ECDC*, 2018](https://www.ecdc.europa.eu/sites/default/files/documents/vector-abundance-and-seasonality.pdf)). Farmer reports from Cumbria indicate that midge activity has persisted into January in recent years, suggesting the transmission window may extend well beyond the traditional autumn peak.
- The historical Cyprus experience also highlights the importance of preparedness. The successful use of an attenuated vaccine in 1946–1947 demonstrates that vaccination can play a decisive role in reducing the impact of BTV-3, particularly in sheep populations. However, the availability, suitability, and uptake of vaccines must be considered alongside vector surveillance, clinical reporting, and movement controls."""

print("=" * 80)
print("Testing Text Summarisation API with Bluetongue Virus Data")
print("=" * 80)

# Test 1: Health check
print("\n1️⃣  Testing Health Check...")
try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        print("✅ Health check successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Configuration
print("\n2️⃣  Checking API Configuration...")
try:
    response = requests.get(f"{API_URL}/config")
    if response.status_code == 200:
        print("✅ Configuration retrieved!")
        config = response.json()
        print(f"   Region: {config['region']}")
        print(f"   Model: {config['model_id']}")
        print(f"   API running on {config['api_host']}:{config['api_port']}")
    else:
        print(f"❌ Config request failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Summarise the bluetongue text
print("\n3️⃣  Testing Summarisation with Bluetongue Text...")
print(f"   Input text length: {len(bluetongue_text)} characters")

payload = {
    "text": bluetongue_text,
    "max_length": 150
}

try:
    print("   Sending request to AWS Bedrock...")
    start_time = time.time()
    response = requests.post(f"{API_URL}/summarise", json=payload)
    elapsed_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Summarisation successful! (completed in {elapsed_time:.2f}s)")
        print(f"\n📊 Response Details:")
        print(f"   Input tokens: {result['input_tokens']}")
        print(f"   Output tokens: {result['output_tokens']}")
        print(f"   Model used: {result['model']}")
        print(f"\n📝 Generated Summary:")
        print(f"   {result['summary']}")
        print(f"\n📏 Summary length: {len(result['summary'])} characters")
    else:
        print(f"❌ Summarisation failed: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test with shorter summary
print("\n4️⃣  Testing with Shorter Summary (75 words)...")
payload_short = {
    "text": bluetongue_text,
    "max_length": 75
}

try:
    start_time = time.time()
    response = requests.post(f"{API_URL}/summarise", json=payload_short)
    elapsed_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Short Summarisation successful! (completed in {elapsed_time:.2f}s)")
        print(f"   Input tokens: {result['input_tokens']}")
        print(f"   Output tokens: {result['output_tokens']}")
        print(f"\n📝 Short Summary:")
        print(f"   {result['summary']}")
    else:
        print(f"❌ Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ Test Suite Completed!")
print("=" * 80)
