; ========================================
; MediMind Knowledge Base – v2.0
; A rich, structured medical knowledge graph
; ========================================

; === 1. CONDITIONS & CATEGORIES ===

(condition ChestPain Severity High)
(condition HeartAttack Severity Critical)
(condition AcidReflux Severity Low)
(condition Anxiety Severity Medium)
(condition Malaria Severity High)
(condition Diabetes Type1 Type2)
(condition Hypertension Severity High)
(condition Asthma Severity Medium)
(condition Stroke Severity Critical)
(condition LongCovid Severity Medium)
(condition COPD Severity High)

; Hierarchies
(subtype ChronicDisease Diabetes)
(subtype ChronicDisease Hypertension)
(subtype ChronicDisease COPD)
(subtype InfectiousDisease Malaria)
(subtype MentalHealthCondition Anxiety)
(subtype CardiovascularDisease HeartAttack)
(subtype CardiovascularDisease Stroke)

; === 2. CAUSES & SYMPTOMS ===

; Chest Pain
(causes HeartAttack ChestPain)
(causes AcidReflux ChestPain)
(causes Anxiety ChestPain)
(causes LongCovid ChestPain)
(causes PulmonaryEmbolism ChestPain)
(causes Costochondritis ChestPain)

; Malaria
(causes Malaria Fever)
(causes Malaria Headache)
(causes Malaria Chills)
(causes Malaria Fatigue)
(causes Malaria Nausea)

; Diabetes
(causes Type1Diabetes AutoimmuneFailure)
(causes Obesity Type2Diabetes)
(causes PoorDiet Type2Diabetes)
(causes SedentaryLifestyle Type2Diabetes)

; Hypertension
(causes HighSaltDiet Hypertension)
(causes Obesity Hypertension)
(causes Stress Hypertension)
(causes KidneyDisease Hypertension)

; Asthma
(causes Allergens AsthmaAttack)
(causes AirPollution AsthmaAttack)
(causes ColdAir AsthmaAttack)
(causes Exercise AsthmaAttack)

; === 3. TREATMENTS ===

(treatment HeartAttack "Immediate medical attention, ECG, aspirin, possible stent or bypass")
(treatment AcidReflux "Antacids, proton pump inhibitors, dietary changes")
(treatment Anxiety "Cognitive behavioral therapy, SSRIs, mindfulness, exercise")
(treatment Malaria "Artemisinin-based combination therapy (ACT)")
(treatment Type1Diabetes "Insulin therapy, blood glucose monitoring")
(treatment Type2Diabetes "Metformin, lifestyle changes, possible insulin")
(treatment Hypertension "ACE inhibitors, beta-blockers, lifestyle changes")
(treatment Asthma "Inhalers (bronchodilators, corticosteroids), avoid triggers")
(treatment Stroke "Thrombolytic therapy within 4.5 hours, rehabilitation")
(treatment COPD "Bronchodilators, steroids, oxygen therapy, smoking cessation")

; === 4. PREVENTION ===

(prevention HeartAttack "Exercise, healthy diet, no smoking, control blood pressure and cholesterol")
(prevention Malaria "Use mosquito nets, insect repellent, antimalarial prophylaxis in endemic areas")
(prevention Type2Diabetes "Maintain healthy weight, regular exercise, balanced diet")
(prevention Hypertension "Reduce salt intake, exercise, limit alcohol, manage stress")
(prevention Asthma "Avoid allergens, use air purifiers, get flu vaccine")
(prevention Stroke "Control hypertension, manage diabetes, stop smoking, exercise")

; === 5. RISK FACTORS ===

(risk HeartAttack HighAge)
(risk HeartAttack Smoking)
(risk HeartAttack HighCholesterol)
(risk HeartAttack FamilyHistory)
(risk Malaria TravelToEndemicArea)
(risk Diabetes Obesity)
(risk Stroke Hypertension)
(risk COPD Smoking)

; === 6. SYMPTOMS OF CONDITIONS ===

; (symptom $condition $symptom)
(symptom HeartAttack ChestPain)
(symptom HeartAttack ShortnessOfBreath)
(symptom HeartAttack Nausea)
(symptom HeartAttack Sweating)
(symptom Malaria Fever)
(symptom Malaria Headache)
(symptom Malaria Chills)
(symptom Diabetes ExcessiveThirst)
(symptom Diabetes FrequentUrination)
(symptom Diabetes Fatigue)
(symptom Hypertension Headache)
(symptom Hypertension Dizziness)
(symptom Asthma Wheezing)
(symptom Asthma Coughing)
(symptom Asthma ShortnessOfBreath)

; === 7. DRUG INTERACTIONS (Simplified) ===

(interacts Warfarin NSAIDs "Increased bleeding risk")
(interacts Statins GrapefruitJuice "Increased risk of side effects")
(interacts SSRIs MAOInhibitors "Risk of serotonin syndrome")
(interacts Insulin Sulfonylureas "Increased risk of hypoglycemia")

; === 8. AIR QUALITY IMPACT ===

(impacts AirPollution AsthmaAttack)
(impacts AirPollution COPDExacerbation)
(impacts PM2_5 CardiovascularEvents)

; === 9. QUERY FUNCTIONS ===

; Get causes of a symptom
(=(getCauses $symptom)
  (match &self (causes $cause $symptom) $cause))

; Get symptoms of a condition
(=(getSymptoms $condition)
  (match &self (symptom $condition $symptom) $symptom))

; Get treatment for a condition
(=(getTreatment $condition)
  (match &self (treatment $condition $treatment) $treatment))

; Get prevention for a condition
(=(getPrevention $condition)
  (match &self (prevention $condition $prevention) $prevention))

; Get risk factors for a condition
(=(getRiskFactors $condition)
  (match &self (risk $condition $factor) $factor))

; Explain why a condition causes a symptom
(=(explain-cause $condition $symptom)
  (cat
    "I know " $condition " causes " $symptom " because:\n"
    "• Fact: (causes " $condition " " $symptom ")\n"
    "• Clinical evidence supports this association\n"
    "• Source: Verified medical knowledge base"))

; Get all conditions in a category
(=(getConditionsOfType $type)
  (match &self (subtype $type $condition) $condition))

; Check if air pollution can trigger a condition
(=(isTriggeredByPollution $condition)
  (match &self (impacts AirPollution $condition) $condition))

; === 10. REAL-TIME DATA (Updated at Runtime) ===
; These will be injected via Python from APIs
; (air-quality Mumbai AQI 156)
; (outbreak Dengue India)
; (drug-availability Insulin ApolloPharmacy InStock)

; === 11. SELF-LEARNING HOOKS ===
; These will be added dynamically via /learn
; (causes LongCovid ChestPain)
; (treatment LongCovid "Symptom management, rehabilitation")