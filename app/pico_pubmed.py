# pico_search.py
import cohere
import requests
import json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

abstracts_and_scores = [
    {
        "title": "Efficacy of Continuous Glucose Monitoring in Improving Glycemic Control and Reducing Hypoglycemia: A Systematic Review and Meta-Analysis of Randomized Trials",
        "abstract": """
        Objective:
        We conducted a systematic review and meta-analysis to assess the efficacy of continuous glucose monitoring (CGM)
        in improving glycemic control and reducing hypoglycemia compared to self-monitored blood glucose (SMBG).
        Methods:
        We searched MEDLINE, EMBASE, Cochrane Central, Web of Science, and Scopus for randomized trials of adults
        and children with type 1 or type 2 diabetes mellitus (T1DM or T2DM). Pairs of reviewers independently
        selected studies, assessed methodological quality, and extracted data. Meta-analytic estimates of treatment effects
        were generated using a random-effects model.
        Results:
        Nineteen trials were eligible and provided data for meta-analysis. Overall, CGM was associated with a significant
        reduction in mean hemoglobin A1c [HbA1c; weighted mean difference (WMD) of -0.27% (95% confidence
        interval [CI] -0.44 to -0.10)]. This was true for adults with T1DM as well as T2DM [WMD -0.50% (95% CI
        -0.69 to -0.30) and -0.70 (95% CI, -1.14 to -0.27), respectively]. No significant effect was noted in children and
        adolescents. There was no significant difference in HbA1c reduction between studies of real-time versus non-real-
        time devices (WMD -0.22%, 95% CI, -0.59 to 0.15 versus -0.30%, 95% CI, -0.49 to -0.10; p for interaction 0.71).
        The quality of evidence was moderate due to imprecision, suggesting increased risk for bias. Data for the
        incidence of severe or nocturnal hypoglycemia were sparse and imprecise. In studies that reported patient
        satisfaction, users felt confident about the device and gave positive reviews. Conclusion:
        Continuous glucose monitoring seems to help improve glycemic control in adults with T1DM and T2DM.
        The effect on hypoglycemia incidence is imprecise and unclear. Larger trials with longer follow-up are needed
        to assess the efficacy of CGM in reducing patient-important complications without significantly increasing
        the burden of care for patients with diabetes.
        """,
        "score": 45
    },



        {
        "title": "Effectiveness of continuous glucose monitoring in maintaining glycaemic control among people with type 1 diabetes mellitus: a systematic review of randomised controlled trials and meta-analysis",
        "abstract": """
Aims/hypothesis The aim of this work was to assess the effectiveness of continuous glucose monitoring (CGM) vs self- monitoring of blood glucose (SMBG) in maintaining glycaemic control among people with type 1 diabetes mellitus.
Methods Cochrane Library, PubMed, Embase, CINAHL, Scopus, trial registries and grey literature were searched from 9 June 2011 until 22 December 2020 for RCTs comparing CGM intervention against SMBG control among the non-pregnant individuals with type 1 diabetes mellitus of all ages and both sexes on multiple daily injections or continuous subcutaneous insulin infusion with HbA1c levels, severe hypoglycaemia and diabetic ketoacidosis (DKA) as outcomes. Studies also included any individual or caregiver-led CGM systems. Studies involving GlucoWatch were excluded. Risk of bias was appraised with Cochrane risk of bias tool. Meta- analysis and meta-regression were performed using Review Manager software and R software, respectively. Heterogeneity was evaluated using χ2 and I2 statistics. Overall effects and certainty of evidence were evaluated using Z statistic and GRADE (Grading of Recommendations, Assessment, Development and Evaluation) software.
Results Twenty-two studies, involving 2188 individuals with type 1 diabetes, were identified. Most studies had low risk of bias. Meta-analysis of 21 studies involving 2149 individuals revealed that CGM significantly decreased HbA1c levels compared with SMBG (mean difference −2.46 mmol/mol [−0.23%] [95% CI −3.83, −1.08], Z = 3.50, p=0.0005), with larger effects experi- enced among higher baseline HbA1c >64 mmol/mol (>8%) individuals (mean difference −4.67 mmol/mol [−0.43%] [95% CI −6.04, −3.30], Z = 6.69, p<0.00001). However, CGM had no influence on the number of severe hypoglycaemia (p=0.13) and DKA events (p=0.88). Certainty of evidence was moderate.
Conclusions/interpretation CGM is superior to SMBG in improving glycaemic control among individuals with type 1 diabetes in the community, especially in those with uncontrolled glycaemia. Individuals with type 1 diabetes with HbA1c >64 mmol/mol (>8%) are most likely to benefit from CGM. Current findings could not confer a concrete conclusion on the effectiveness of CGM on DKA outcome as DKA incidences were rare. Current evidence is also limited to outpatient settings. Future research should evaluate the accuracy of CGM and the effectiveness of CGM across different age groups and insulin regimens as these remain unclear in this paper.
        """,
        "score": 40
    },


        {
        "title": " The Efficacy of Technology in Type 1 Diabetes: A Systematic Review, Network Meta-analysis, and Narrative Synthesis",
        "abstract": """
Background: Existing technologies for type 1 diabetes have not been compared against the full range of alternative devices. Multiple metrics of glycemia and patient-reported outcomes for evaluating technologies also require consideration. We thus conducted a systematic review, network meta-analysis, and narrative synthesis to compare the relative efficacy of available technologies for the management of type 1 diabetes. Methods: We searched MEDLINE, MEDLINE In-Process and other nonindexed citations, EMBASE, PubMed, All Evidence-Based Medicine Reviews, Web of Science, PsycINFO, CINAHL, and PROSPERO (inception— April 24, 2019). We included RCT ‡6 weeks duration comparing technologies for type 1 diabetes management among nonpregnant adults (>18 years of age). Data were extracted using a predefined tool. Primary outcomes were A1c (%), hypoglycemia rates, and quality of life (QoL). We estimated mean difference for A1c and nonsevere hypoglycemia, rate ratio for severe hypoglycemia, and standardized mean difference for QoL in network meta-analysis with random effects.
Results: We identified 16,772 publications, of which 52 eligible studies compared 12 diabetes management technologies comprising 3,975 participants in network meta-analysis. Integrated insulin pump and continuous glucose monitoring (CGM) systems with low-glucose suspend or hybrid closed-loop algorithms resulted in A1c levels 0.96% (predictive interval [95% PrI] 0.04–1.89) and 0.87% (95% PrI 0.12–1.63) lower than multiple daily injections with either flash glucose monitoring or capillary glucose testing, respectively. In addition, integrated systems had the best ranking for A1c reduction utilizing the surface under the cumulative ranking curve (SUCRA–96.4). While treatment effects were nonsignificant for many technology comparisons regarding severe hypoglycemia and QoL, simultaneous evaluation of outcomes in cluster analyses as well as narrative synthesis appeared to favor integrated insulin pump and continuous glucose monitors. Overall risk of bias was moderate–high. Certainty of evidence was very low.
Conclusions: Integrated insulin pump and CGM systems with low-glucose suspend or hybrid closed-loop capability appeared best for A1c reduction, composite ranking for A1c and severe hypoglycemia, and possibly QoL.
        """,
        "score": 35
    },


        {
        "title": "Continuous glucose monitoring systems for type 1 diabetes mellitus",
        "abstract": """
        Background
Self-monitoring of blood glucose is essential to optimise glycaemic control in type 1 diabetes mellitus. Continuous glucose monitoring (CGM) systems measure interstitial fluid glucose levels to provide semi-continuous information about glucose levels, which identifies fluctuations that would not have been identified with conventional self-monitoring. Two types of CGM systems can be defined: retrospective systems and real-time systems. Real-time systems continuously provide the actual glucose concentration on a display. Currently, the use of CGM is not common practice and its reimbursement status is a point of debate in many countries.
Objectives
To assess the effects of CGM systems compared to conventional self-monitoring of blood glucose (SMBG) in patients with diabetes mellitus type 1.
Search methods
We searched The Cochrane Library, MEDLINE, EMBASE and CINAHL for the identification of studies. Last search date was June 8, 2011. Selection criteria
Randomised controlled trials (RCTs) comparing retrospective or real-time CGM with conventional self-monitoring of blood glucose levels or with another type of CGM system in patients with type 1 diabetes mellitus. Primary outcomes were glycaemic control, e.g. level of glycosylated haemoglobin A1c (HbA1c) and health-related quality of life. Secondary outcomes were adverse events and complications, CGM derived glycaemic control, death and costs.
Data collection and analysis
Two authors independently selected the studies, assessed the risk of bias and performed data-extraction. Although there was clinical and methodological heterogeneity between studies an exploratory meta-analysis was performed on those outcomes the authors felt could be pooled without losing clinical merit.
Main results
The search identified 1366 references. Twenty-two RCTs meeting the inclusion criteria of this review were identified. The results of the meta- analyses (across all age groups) indicate benefit of CGM for patients starting on CGM sensor augmented insulin pump therapy compared to patients using multiple daily injections of insulin (MDI) and standard monitoring blood glucose (SMBG). After six months there was a significant larger decline in HbA1c level for real-time CGM users starting insulin pump therapy compared to patients using MDI and SMBG
(mean difference (MD) in change in HbA1c level -0.7%, 95% confidence interval (CI) -0.8% to -0.5%, 2 RCTs, 562 patients, I2=84%). The risk of hypoglycaemia was increased for CGM users, but CIs were wide and included unity (4/43 versus 1/35; RR 3.26, 95% CI 0.38 to 27.82 and 21/247 versus 17/248; RR 1.24, 95% CI 0.67 to 2.29). One study reported the occurrence of ketoacidosis from baseline to six months; there was however only one event. Both RCTs were in patients with poorly controlled diabetes.
For patients starting with CGM only, the average decline in HbA1c level six months after baseline was also statistically significantly larger for CGM users compared to SMBG users, but much smaller than for patients starting using an insulin pump and CGM at the same time (MD change in HbA1c level -0.2%, 95% CI -0.4% to -0.1%, 6 RCTs, 963 patients, I2=55%). On average, there was no significant difference in risk of severe hypoglycaemia or ketoacidosis between CGM and SMBG users. The confidence interval however, was wide and included a decreased as well as an increased risk for CGM users compared to the control group (severe hypoglycaemia: 36/411 versus 33/407; RR 1.02, 95% CI 0.65 to 1.62, 4 RCTs, I2=0% and ketoacidosis: 8/411 versus 8/407; RR 0.94, 95% CI 0.36 to 2.40, 4 RCTs, I2=0%).
Health-related quality of life was reported in five of the 22 studies. In none of these studies a significant difference between CGM and SMBG was found. Diabetes complications, death and costs were not measured.
There were no studies in pregnant women with diabetes type 1 and in patients with hypoglycaemia unawareness.
Authors' conclusions
There is limited evidence for the effectiveness of real-time continuous glucose monitoring (CGM) use in children, adults and patients with poorly controlled diabetes. The largest improvements in glycaemic control were seen for sensor-augmented insulin pump therapy in patients with poorly controlled diabetes who had not used an insulin pump before. The risk of severe hypoglycaemia or ketoacidosis was not significantly increased for CGM users, but as these events occurred infrequent these results have to be interpreted cautiously.There are indications that higher compliance of wearing the CGM device improves glycosylated haemoglobin A1c level (HbA1c) to a larger extent.
        """,
        "score": 45
    },


        {
        "title": "Real-time continuous glucose monitoring in type 1 diabetes: a systematic review and individual patient data meta-analysis",
        "abstract": """
Background Real-time continuous glucose monitoring (RTCGM) may help in the management of individuals with type 1 diabetes mellitus (T1DM); however, the evidence supporting its use is unclear. The available meta-analyses on this topic use aggregate data which weaken inference.
Objective Individual patient data were obtained from random- ized controlled trials (RCTs) to conduct a meta-analysis and synthesize evidence about the effect of RTCGM on glycosylated haemoglobin (HbA1c), hypoglycaemic events and time spent in hypoglycaemia in T1DM.
Methods We searched MEDLINE, EMBASE, Cochrane Central Register of Controlled Trials and Database of Systematic Reviews, and Scopus through January 2015. We included RCTs that enrolled individuals with T1DM and compared RTCGM vs control group. A two-step regression model was used to pool individual patient data.
Results We included 11 RCTs at moderate risk of bias. Meta- analysis suggests that the use of RTCGM is associated with a sta- tistically significant but modest reduction in HbA1c . The improvements in HbA1c were primarily seen in individuals over age 15 years. We were unable to identify a statistically significant difference in time spent in hypoglycaemia or the number of hypoglycaemic episodes although these analyses were imprecise and warrant lower confidence. There was no difference between males and females.
Conclusion RTCGM in T1DM is associated with a reduction in HbA1c primarily in individuals over 15 years of age. We were unable to identify a statistically significant difference in the time spent in hypoglycaemia or the incidence of hypoglycaemic episodes.
        """,
        "score": 40
    },
    



]



# Sort papers by score in descending order
abstracts_and_scores_sorted = sorted(abstracts_and_scores, key=lambda x: x["score"], reverse=True)

# Summarize each abstract using Cohere API
def summarize_abstracts():
    summaries = []
    for paper in abstracts_and_scores_sorted:
        prompt = (
            f"Summarize the following medical research abstract carefully. "
            f"Preserve important terminology and concepts, and ensure accuracy for any details about the patient type, "
            f"such as whether they are a child, adult, or elderly:\n\n"
            f"{paper['abstract']}"
        )
        response = co.summarize(text=prompt, length="medium", model="cohere-summarize")
        summary = response.summary if response else "Summary not available."
        summaries.append({"title": paper["title"], "summary": summary, "score": paper["score"]})
    return summaries






    #-------------------------------------#
def parse_pico_with_cohere(question):
    prompt = f"Extract the PICO components (Patient, Intervention, Comparison, Outcome) from the following question, please write it in the correct order: \n\n'{question}'"
    response = co.chat(
        model='command-r',
        message=prompt,
        response_format={"type": "json_object"}
    )
    print("Raw response from Cohere:", response.text)
    try:
        parsed_response = json.loads(response.text)
        print("Parsed JSON response:", parsed_response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Unable to parse PICO components. Invalid JSON format.")
        return None

def search_pubmed(pico_components):
    if not pico_components:
        print("No valid PICO components found.")
        return []
    
    # Create a combined search term emphasizing systematic reviews
    patient = pico_components.get('Patient', '')
    intervention = pico_components.get('Intervention', '')
    comparison = pico_components.get('Comparison', '')
    outcome = pico_components.get('Outcome', '')
    term = f"({patient} OR {intervention} OR {comparison} OR {outcome}) AND systematic review"
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": 5
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        return search_results['esearchresult']['idlist']
    else:
        print(f"Error: PubMed search failed with status code {response.status_code}")
        return []

def fetch_pubmed_details(paper_ids):
    if not paper_ids:
        print("No paper IDs provided.")
        return None
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
        "rettype": "abstract"
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Failed to fetch paper details with status code {response.status_code}")
        return None

def extract_abstracts_from_xml(xml_data):
    root = ET.fromstring(xml_data)
    articles = []
    for article in root.findall(".//PubmedArticle"):
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
        abstract = article.find(".//AbstractText")
        url = f"https://pubmed.ncbi.nlm.nih.gov/{article.find('.//PMID').text}" if article.find(".//PMID") is not None else ""
        
        if abstract is not None:
            articles.append({
                'title': title,
                'abstract': abstract.text,
                'url': url
            })
    return articles

def summarize_paper_with_cohere(paper_abstract):
    prompt = f"Summarize the following research abstract in 2-3 sentences:\n\n'{paper_abstract}'"
    response = co.chat(
        model='command-r',
        message=prompt,
    )
    return response.text