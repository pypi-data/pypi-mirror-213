from anova_analysis import ANOVA_RBD

rep = 4
treat = 23

# If you have a single excel sheet for single character
file = "data/MODEL_DATA.xlsx"

result = ANOVA_RBD.RBD(rep, treat, file, False)

CF = result["correction_factor"]
TSS = result["total_sum_of_square"]
RSS = result["replication_sum_of_square"]
TSS = result["treatment_sum_of_square"]
ESS = result["error_sum_of_square"]
Rdf = result["replication_df"]
Tdf = result["treatment_df"],
Edf = result["errors_df"],
RMSS = result["rep_mean_ss"],
TMSS = result["tre_mean_ss"],
EMSS = result["error_mean_ss"]

print(CF)

# If you have multiple characters in separate excel sheet
# See this GitHub page for further details "https://github.com/Insight-deviler/Folder-based-Character-Column-Transformation/tree/main"

from anova_analysis import ANOVA_RBD
import os

folder_path = r'C:/Users/PlantReading/data/'

# listing files in the folder_path 
for file in os.listdir(folder_path):
  
# Checking whether the folder contains excel files
    if file.endswith('.xlsx') or file.endswith('.xls'):

# Joining the file path and name of the excel file:
        file_path = os.path.join(folder_path, file)
        print(f"processing file: {file}")
       
      # Where: 
      #   rep is replication,
      #   treat is genotypes,  os.path.basename(file) for getting file name
        ANOVA_RBD.RBD(rep,treat,file_path,False)