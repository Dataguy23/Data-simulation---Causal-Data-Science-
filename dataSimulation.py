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

# Generating data for each variable
for i in range(n):
    Retention.append(6.2*random.random()) # approximating an average retention of 2.9 years
    FirstJob.append(random.randint(0,1)) # binary approxmiation of roughly half who had no prior workExperience

    if FirstJob[i]==1: # if this is the first job of an individual
        Age.append(random.randint(22,29)) # THEN set age to be random integer beetween 22 and 29
        IndustryExperience.append(0) # Then no prior experience
        FlexibleWork.append(random.randint(45,70)) # THEN set wrk hrs to be random integer beetween 45 and 70
        EducationLevel.append(random.randint(2,4)) # if this the first job, it will be higher than highscool level
    else:
        Age.append(random.randint(24,54)) # ELSE set age to be random integer between 24 and 54
        IndustryExperience.append(round(random.random()*Age[i])) # TEMP experience based on random value 0-1 and age, corrected later
        FlexibleWork.append(random.randint(60,90)*(100-Age[i])/100) # ELSE set wrk hrs to be random integer corrected for age
        EducationLevel.append(random.randint(1,4)) # else it could be all

    ExtrinsicReward.append(round((base_salary+bonus_salary)*(100-Age[i])/190*(1+(IndustryExperience[i]*0.1)),ndigits=2)) # a function of age and Industryexpertise
    



# Alternating data according to model & creating organizationalCommitment+AdvancementOpportunities+JobSatisfaction
for i in range(n):
    # change retention and create Organizational commitment
    if FirstJob[i]==1:
        Retention[i]=Retention[i]*0.85 # lower retention if first job
        if Retention[i]<0.5: # first job and employment of less than half year
            OrganizationalCommitment.append(0) #then 0 internal projects
        else:
            OrganizationalCommitment.append(random.randint(1,3)) #else 1 to 3 internal project(s)

    else:
        OrganizationalCommitment.append(round(random.randint(1,2)*Retention[i])) # else int of 1 to 5 internal projects multiplied with retention

    Retention[i] = round(Retention[i],ndigits=2)

    # Changing IndustryExpertise
    if IndustryExperience[i] >1: # correcting according to the initial setting, higher likelihood of industry if higher age
        if IndustryExperience[i] >= 17: # arbitrary threshold for industry experience
            IndustryExperience[i] = 1
        else:
            IndustryExperience[i] = 0 
    
    # creating AdvancementOpportunities
    AdvancementOpportunities.append(round(0.2*(IndustryExperience[i]+EducationLevel[i]*(2*Retention[i])))) #a function of Industryexpertise, education and retention

    #Creating JobSatisfaction
    JobSatisfaction.append(Retention[i]+AdvancementOpportunities[i]+OrganizationalCommitment[i]+ExtrinsicReward[i]*0.1+random.randint(10000,50000))
    

# Scale jobSatisfaction with linear transformation to be in range of MaxVal - MinVal
MaxVal = 10
MinVal = 1
OriginalMin = np.min(JobSatisfaction)
OriginalMax = np.max(JobSatisfaction)
for i in range(n):
    JobSatisfaction[i] = round((((JobSatisfaction[i]-OriginalMin) * (MaxVal-MinVal)) / (OriginalMax-OriginalMin))+MinVal)

    # round to two decimals





# Converting data to a pd DataFrame
df = pd.DataFrame(list(zip(Retention,FirstJob,Age,IndustryExperience,FlexibleWork,ExtrinsicReward,EducationLevel,OrganizationalCommitment,AdvancementOpportunities,JobSatisfaction)),
columns=["Retention","FirstJob","Age","IndustryExperience","FlexibleWork","ExtrinsicReward","EducationLevel","OrganizationalCommitment","AdvancementOpportunities","JobSatisfaction"])

df.to_csv("/Users/andersolsen/Desktop/Kandidat/3. semester/Causal Data Science/SimulatedExamData.csv",index=0)
