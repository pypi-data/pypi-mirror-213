import pandas as pd
from tabulate import tabulate
import scipy.stats as stats
import os

def RBD(replication, treatment, input_file_path,save_file=None):
    
    # Import the dataset
    df = pd.read_excel(input_file_path)

    # Correction Factor
    data_subset = df.iloc[:, 1:]
    total_sum = data_subset.values.sum()
    correctionFactor = (total_sum ** 2) / (replication * treatment)
    
    # Total Sum of Square
    total_sum_squared = (data_subset ** 2).values.sum()
    totalsum = total_sum_squared - correctionFactor
    
    # Replication Sum of Square
    column_sums = df.iloc[:, 1:].sum()
    replicationSum = ((column_sums ** 2).sum() / treatment) - correctionFactor
    
    # Treatment Sum of Square
    row_sum = df.iloc[:, 1:].sum(axis=1)
    treatmentSum = ((row_sum ** 2).sum() / replication) - correctionFactor
    
    # Error Sum of Square
    Error_sum_square = totalsum - replicationSum - treatmentSum

    # Anova table
    rep = replication - 1
    tre = treatment - 1
    error_df = rep * tre
    total_source = rep + tre + error_df
    total_ss_sum = replicationSum + treatmentSum + Error_sum_square
    rep_mss = replicationSum / rep
    tre_mss = treatmentSum / tre
    error_mss = Error_sum_square / error_df

    # Significance Levels
    significance_level_5 = 0.05
    significance_level_1 = 0.01

    # F-test and Significance Level
    f_value_row = rep_mss / error_mss
    f_value_column = tre_mss / error_mss
    p_value_row_5 = stats.f.ppf(1- significance_level_5, rep, error_df)
    p_value_column_5 = stats.f.ppf(1-significance_level_5, tre, error_df)
    p_value_row_1 = stats.f.ppf(1- significance_level_1, rep, error_df)
    p_value_column_1 = stats.f.ppf(1-significance_level_1, tre, error_df)
 
    # Determine Significance
    row_significance = "Sig" if p_value_row_5 < f_value_row else "Not Sig"
    column_significance = "Sig" if p_value_column_5 < f_value_column else "Not Sig"
    row_significance_1 = "Sig" if p_value_row_1 < f_value_row else "Not Sig"
    column_significance_1 = "Sig" if p_value_column_1 < f_value_column else "Not Sig"


    data = {
        "Source": ["Replication", "Treatment", "Error", "Total"],
        "d.f": [rep, tre, error_df, total_source],
        "s.s": [round(replicationSum, 2), round(treatmentSum, 2), round(Error_sum_square, 2),
                 round(total_ss_sum, 2)],
        "m.s": [round(rep_mss, 2), round(tre_mss, 2), round(error_mss, 2), ""],
        "F-ratio": [round(rep_mss / error_mss, 2), round(tre_mss / error_mss, 2), "", ""],
        "p-value (5%)": [round(p_value_row_5,3), round(p_value_column_5,3),'',''],
        "p-value (1%)": [round(p_value_row_1,3), round(p_value_column_1,3),'',''],
        "Sig. (at 5%)": [row_significance, column_significance, "", ""],
        "Sig. (at 1%)": [row_significance_1, column_significance_1, "", ""]
    }

    # Create the DataFrame for the table
    table_df = pd.DataFrame(data)

    # Print the table
    print(table_df)

    if save_file is None or save_file:

            # Save the results in a text file
            directory_path = os.path.dirname(input_file_path)
            output_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
            output_file_path = os.path.join(directory_path, f"{output_file_name}_result.txt")
        
            # Save the results in a text file
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(f"{output_file_name}: ")
                file.write("\n\n")
                file.write("Correction Factor: {:.2f}\n".format(correctionFactor))
                file.write("Total Sum of Square: {:.2f}\n".format(totalsum))
                file.write("Replication Sum of Square: {:.2f}\n".format(replicationSum))
                file.write("Treatment Sum of Square: {:.2f}\n".format(treatmentSum))
                file.write("Error Sum of Square: {:.2f}\n\n".format(Error_sum_square))
                file.write(tabulate(table_df, headers='keys', tablefmt='grid'))

            print(f"Result saved in {output_file_path}")

    result = {
        "global_dataframe" : table_df,
        "correction_factor": round(correctionFactor, 2),
        "total_sum_of_square": round(totalsum, 2),
        "replication_sum_of_square": round(replicationSum, 2),
        "treatment_sum_of_square": round(treatmentSum, 2),
        "error_sum_of_square": round(Error_sum_square, 2),
        "replication_df": rep,
        "treatment_df": tre,
        "errors_df": error_df,
        "rep_mean_ss":round(rep_mss, 2),
        "tre_mean_ss": round(tre_mss, 2),
        "error_mean_ss":round(error_mss, 2),
        "total_df": total_source,
        "total_ss": round(total_ss_sum, 2)

    }
    # Return the result
    return result