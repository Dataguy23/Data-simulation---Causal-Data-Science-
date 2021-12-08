import numpy as np
import random
import pandas as pd 

# Initializing number of samples and each variable
n = 5000 # number of samples
random.seed(42) # to make results reproducable 
base_salary = 60000
bonus_salary = 45000

Retention = [] # cont
FirstJob = [] # bool
Age = [] # int
IndustryExperience = [] # bool
FlexibleWork = [] # Cont
ExtrinsicReward = [] # Cont
EducationLevel = [] # int 
OrganizationalCommitment = [] # int
AdvancementOpportunities = [] # int
JobSatisfaction = [] # int



# Generating data for each variable, except Retention
for i in range(n):
    Age.append(random.randint(22,58)) # setting age to a random integer between 22 and 58
    
    (IndustryExperience.append(0) if Age[i]<26 else IndustryExperience.append(random.randint(0,1))) # setting industry experience to an arbitrary function of age, at least 26 years of age to be eligble for industry experience
    
    (FirstJob.append(0) if IndustryExperience[i]==1 else FirstJob.append(random.randint(0,1))) # setting firstjob to FALSE if industry experience is TRUE, else TEMP random 
    FirstJob[i] = 0 if Age[i] >33 else FirstJob[i] # setting FirstJob to FALSE if age is above 33, else keep random integer in set {0,1}
    
    ExtrinsicReward.append(round((base_salary+bonus_salary)*(Age[i]/100)*(1+(IndustryExperience[i]*0.1)),ndigits=2)) # setting extrinsic as an arb func of age and industry expertise

    (OrganizationalCommitment.append(random.randint(2,8)) if ExtrinsicReward[i]>55000 else OrganizationalCommitment.append(random.randint(1,4))) # setting the org commitment as a func of extrinsicReward

    (FlexibleWork.append(random.randint(45,70)) if FirstJob[i]==1 else FlexibleWork.append(random.randint(60,90)*(100-Age[i])/100)) # setting flexible work as a func of first job and age, in which newly and younger enployees are more likely to work long hours
    
    (EducationLevel.append(random.randint(2,4)) if FirstJob[i]==1 else EducationLevel.append(random.randint(1,4))) # setting education to a func first job, specificially education is at least bachelor if this is the first job, else random 

    AdvancementOpportunities.append(round(np.sum((IndustryExperience[i]*5+EducationLevel[i])))) # setting advancements to equal the sum of industry expertise and education level

    JobSatisfaction.append(AdvancementOpportunities[i]+OrganizationalCommitment[i]+ExtrinsicReward[i]*0.001+FlexibleWork[i]*-0.3) # setting jobSatisfaction equal to causes, regulating the impact of reward and flexibleWork


# Scale jobSatisfaction with linear transformation to be in range of MaxVal - MinVal
MaxVal = 10
MinVal = 1
OriginalMin = np.min(JobSatisfaction)
OriginalMax = np.max(JobSatisfaction)

for i in range(n):
    JobSatisfaction[i] = round((((JobSatisfaction[i]-OriginalMin) * (MaxVal-MinVal)) / (OriginalMax-OriginalMin))+MinVal) 


# Generating data for Retention
for i in range(n):
    Retention.append(FirstJob[i]*2+JobSatisfaction[i]+IndustryExperience[i]*2) # Setting retention to a func of the cuases, assigning more value to binary values for them to have some influence

# Scale Retention with linear transformation to be in range of MaxVal - MinVal
MaxVal = 10
MinVal = 0.01
OriginalMin = np.min(Retention)
OriginalMax = np.max(Retention)

for i in range(n):
    Retention[i] = round((((Retention[i]-OriginalMin) * (MaxVal-MinVal)) / (OriginalMax-OriginalMin))+MinVal,ndigits=2) 


# Converting data to a pd DataFrame
df = pd.DataFrame(list(zip(Retention,FirstJob,Age,IndustryExperience,FlexibleWork,ExtrinsicReward,EducationLevel,OrganizationalCommitment,AdvancementOpportunities,JobSatisfaction)),
columns=["Retention","FirstJob","Age","IndustryExperience","FlexibleWork","ExtrinsicReward","EducationLevel","OrganizationalCommitment","AdvancementOpportunities","JobSatisfaction"])


df.to_csv("../SimulatedExamData.csv",index=0)

