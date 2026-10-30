# Test Scenarios - Different Classification Results

## How the Decision Logic Works

The system calculates a **Risk Score (0-100)**:

```
Risk Score Calculation:
  Base = 50
  + Credit Risk Factor (-15 to +30)
  + Loan Amount Factor (-10 to +25)
  + DTI Factor (up to +20)
  + Income Stability Factor (-10 to +15)
  = Final Score (0-100)

Classification Rules:
  Risk < 35     → ✅ APPROVED (HIGH confidence)
  Risk < 60     → ✅ APPROVED (MEDIUM confidence)
  Risk < 75     → ⚠️ MANUAL_REVIEW (MEDIUM confidence)
  Risk ≥ 75     → ❌ REJECTED (HIGH confidence)
```

---

## 🟢 SCENARIO 1: APPROVED (Low Risk Score)

**Target:** Risk Score < 35 (HIGH confidence approval)

### Form Input:
```
Applicant Name: Sarah Johnson
Age: 38
Income: $120,000
Employment Type: SALARIED
Credit Score: 780
Loan Amount: $150,000
Tenure: 15 years
Monthly Liabilities: $200
Location: San Francisco
```

### Why It Gets Approved:
- ✅ Excellent credit score (780) → -15 risk points
- ✅ Reasonable loan amount (1.25× annual income) → -10 risk points
- ✅ Low DTI ratio (0.15) → -5 risk points
- ✅ High income stability (score: 95) → -10 risk points
- **Expected Risk Score: 20-30** → APPROVED ✅

---

## 🟡 SCENARIO 2: APPROVED (Medium Risk Score)

**Target:** Risk Score 35-60 (MEDIUM confidence approval)

### Form Input:
```
Applicant Name: Michael Chen
Age: 42
Income: $85,000
Employment Type: SALARIED
Credit Score: 700
Loan Amount: $250,000
Tenure: 20 years
Monthly Liabilities: $800
Location: Austin
```

### Why It Gets Approved:
- ✅ Good credit score (700) → -5 risk points
- ⚠️ Moderate loan amount (3× annual income) → +5 risk points
- ⚠️ Moderate DTI ratio (0.45) → +5 risk points
- ✅ Good income stability (score: 85) → -5 risk points
- **Expected Risk Score: 45-55** → APPROVED (MEDIUM) ✅

---

## 🟠 SCENARIO 3: MANUAL REVIEW (Borderline)

**Target:** Risk Score 60-75 (MEDIUM confidence manual review)

### Form Input:
```
Applicant Name: Robert Davis
Age: 55
Income: $65,000
Employment Type: SELF_EMPLOYED
Credit Score: 650
Loan Amount: $280,000
Tenure: 25 years
Monthly Liabilities: $1,200
Location: Miami
```

### Why It Gets Manual Review:
- ⚠️ Fair credit score (650) → +10 risk points
- ⚠️ High loan amount (4.3× annual income) → +15 risk points
- ⚠️ High DTI ratio (0.58) → +8 risk points
- ⚠️ Medium income stability (score: 50) → 0 risk points
- **Expected Risk Score: 68-72** → MANUAL_REVIEW ⚠️

---

## 🔴 SCENARIO 4: REJECTED (High Risk Score)

**Target:** Risk Score ≥ 75 (HIGH confidence rejection)

### Form Input:
```
Applicant Name: James Wilson
Age: 62
Income: $35,000
Employment Type: STUDENT
Credit Score: 520
Loan Amount: $300,000
Tenure: 30 years
Monthly Liabilities: $2,000
Location: Detroit
```

### Why It Gets Rejected:
- ❌ Poor credit score (520) → +20 risk points
- ❌ Very high loan amount (8.5× annual income) → +25 risk points
- ❌ Critical DTI ratio (0.75) → +15 risk points
- ❌ Low income stability (score: 30) → +15 risk points
- **Expected Risk Score: 85-90** → REJECTED ❌

---

## 🟠 SCENARIO 5: MANUAL REVIEW (Another Variation)

**Target:** Risk Score 60-75

### Form Input:
```
Applicant Name: Emily Rodriguez
Age: 29
Income: $72,000
Employment Type: FREELANCER
Credit Score: 680
Loan Amount: $220,000
Tenure: 18 years
Monthly Liabilities: $600
Location: New York
```

### Why It Gets Manual Review:
- ⚠️ Fair credit score (680) → +5 risk points
- ⚠️ Moderately high loan amount (3× annual income) → +10 risk points
- ⚠️ Moderate DTI ratio (0.42) → +3 risk points
- ⚠️ Medium income stability for freelancer (score: 60) → -5 risk points
- **Expected Risk Score: 63-68** → MANUAL_REVIEW ⚠️

---

## 🟢 SCENARIO 6: APPROVED (Another Variation)

**Target:** Risk Score < 35

### Form Input:
```
Applicant Name: David Thompson
Age: 45
Income: $150,000
Employment Type: SALARIED
Credit Score: 760
Loan Amount: $200,000
Tenure: 20 years
Monthly Liabilities: $400
Location: Boston
```

### Why It Gets Approved:
- ✅ Excellent credit score (760) → -15 risk points
- ✅ Reasonable loan amount (1.33× annual income) → -10 risk points
- ✅ Low DTI ratio (0.18) → -5 risk points
- ✅ High income stability (score: 90) → -10 risk points
- **Expected Risk Score: 20-25** → APPROVED ✅

---

## 🔴 SCENARIO 7: REJECTED (Another Variation)

**Target:** Risk Score ≥ 75

### Form Input:
```
Applicant Name: Patricia Martinez
Age: 28
Income: $28,000
Employment Type: STUDENT
Credit Score: 480
Loan Amount: $250,000
Tenure: 30 years
Monthly Liabilities: $1,500
Location: Las Vegas
```

### Why It Gets Rejected:
- ❌ Critical credit score (480) → +25 risk points
- ❌ Extremely high loan amount (8.9× annual income) → +25 risk points
- ❌ Critical DTI ratio (0.82) → +16 risk points
- ❌ Very low income stability (score: 25) → +15 risk points
- **Expected Risk Score: 86-95** → REJECTED ❌

---

## 📊 Quick Reference Table

| Scenario | Name | Credit | Income | Loan | DTI | Expected Risk | Result |
|----------|------|--------|--------|------|-----|----------------|--------|
| 1 | Sarah Johnson | 780 | $120K | $150K | 0.15 | 20-30 | ✅ APPROVED |
| 2 | Michael Chen | 700 | $85K | $250K | 0.45 | 45-55 | ✅ APPROVED |
| 3 | Robert Davis | 650 | $65K | $280K | 0.58 | 68-72 | ⚠️ REVIEW |
| 4 | James Wilson | 520 | $35K | $300K | 0.75 | 85-90 | ❌ REJECTED |
| 5 | Emily Rodriguez | 680 | $72K | $220K | 0.42 | 63-68 | ⚠️ REVIEW |
| 6 | David Thompson | 760 | $150K | $200K | 0.18 | 20-25 | ✅ APPROVED |
| 7 | Patricia Martinez | 480 | $28K | $250K | 0.82 | 86-95 | ❌ REJECTED |

---

## 🎯 Key Factors for Each Outcome

### ✅ APPROVED (Risk < 60)
- **Credit Score:** 700+ (Good to Excellent)
- **Employment:** SALARIED (most stable)
- **Loan/Income Ratio:** < 3× annual income
- **DTI Ratio:** < 0.50 (under 50%)
- **Age:** 25-60 years
- **Monthly Liabilities:** Low to moderate

### ⚠️ MANUAL REVIEW (Risk 60-75)
- **Credit Score:** 650-700 (Fair to Good)
- **Employment:** Mixed (FREELANCER, SELF_EMPLOYED)
- **Loan/Income Ratio:** 3-4× annual income
- **DTI Ratio:** 0.45-0.65
- **Monthly Liabilities:** Moderate to high
- These require human judgment

### ❌ REJECTED (Risk ≥ 75)
- **Credit Score:** < 600 (Poor to Critical)
- **Employment:** STUDENT (high risk)
- **Loan/Income Ratio:** > 5× annual income
- **DTI Ratio:** > 0.65 (very high)
- **Monthly Liabilities:** Very high
- **Age:** Very young or very old

---

## 🔍 How to Debug Your Inputs

If you're always getting MANUAL_REVIEW, check if:

1. **Credit Score is Between 650-700?**
   - Lower it to < 550 for REJECTED
   - Raise it to > 700 for APPROVED

2. **Loan Amount is 3-4× Annual Income?**
   - This is the "sweet spot" for MANUAL_REVIEW
   - For APPROVED: Keep it < 2.5× income
   - For REJECTED: Make it > 6× income

3. **DTI Ratio is 0.45-0.55?**
   - This middle range favors MANUAL_REVIEW
   - For APPROVED: Keep monthly debts + loan payment < 30% of income
   - For REJECTED: Make it > 0.65

4. **Employment Type is FREELANCER/SELF_EMPLOYED?**
   - These are higher risk
   - Use SALARIED for lower risk scores

---

## 💡 Tips for Testing

1. **Copy one of the scenarios above** exactly into the form
2. **Adjust ONE factor at a time** to see how it affects the result
3. **Pay attention to:**
   - Credit score changes (20-30 points difference matters)
   - Loan amount vs income ratio
   - Total monthly debt obligations

4. **Track your results:**
   - Write down the risk score returned
   - Note which factors changed the classification

---

## 📝 Most Effective Changes for Each Outcome

### To Get APPROVED (if stuck in MANUAL_REVIEW):
```
✅ Increase credit score from 680 → 750
✅ Decrease loan amount by 20%
✅ Decrease monthly liabilities
✅ Change employment to SALARIED
✅ Increase annual income
```

### To Get REJECTED (if stuck in MANUAL_REVIEW):
```
❌ Decrease credit score from 680 → 520
❌ Increase loan amount by 50%
❌ Increase monthly liabilities
❌ Change employment to STUDENT
❌ Decrease annual income
```

---

## 🧮 Manual Risk Score Calculation

Try this with any input:

```
Base Score: 50

Add Credit Score Factor:
  < 550: +25 (CRITICAL)
  550-649: +20 (HIGH)
  650-749: +10 (MEDIUM)
  750+: -15 (LOW)

Add Loan Amount Factor:
  Loan < 2× income: -10 (LOW)
  2-3× income: +5 (MEDIUM)
  3-5× income: +15 (HIGH)
  5+× income: +25 (CRITICAL)

Add DTI Factor:
  DTI < 0.3: -5
  DTI 0.3-0.5: +3
  DTI 0.5-0.65: +8
  DTI > 0.65: +15

Add Income Stability:
  < 40: +15
  40-60: +5
  60-80: -5
  80+: -10

Final Score = max(0, min(100, base + all factors))
```

---

## ✅ Verification Checklist

Before submitting, verify:
- [ ] Age is 18-75
- [ ] Income is positive
- [ ] Credit score is 300-850
- [ ] Loan amount > $1,000
- [ ] Tenure is 1-40 years
- [ ] All fields filled
- [ ] Location is not empty

Good luck testing! 🎉
