# ANOVA Analysis Package

The ANOVA Analysis Package is a Python package that provides functions for performing ``Two-Way ANOVA (Analysis of Variance)`` on experimental data.

Currently it can perform RBD analysis only. 

Read the [Disclaimer](#disclaimer) before use 

## Installation

You can install the package using pip:

        pip install anova_analysis

## Usage

1. When you have only one character to analyse:

      ```python          
        from anova_analysis import ANOVA_RBD

        #Set the replication, treatment, input file path
        replication = 4
        treatment = 23
        input_file_path = "data/MODEL_DATA.xlsx"

        #Perform ANOVA analysis
        ANOVA_RBD.RBD(replication, treatment, input_file_path)
2. When you have a folder with individual characters in separate excel files:

     ```python
        from anova_analysis import ANOVA_RBD
        import os

        folder_path = r'C:/Users/PlantReading/data/'

        # listing files in the folder_path 
        for file in os.listdir(folder_path):
                if file.endswith('.xlsx') or file.endswith('.xls'):
                        file_path = os.path.join(folder_path, file)
                        print(f"processing file: {file}")
                        ANOVA_RBD.RBD(rep,treat,file_path)
3. The `RBD()` function accepts an optional parameter called `save_file`, which determines whether the result file need to be saved or not. By default, the parameter is set to `True`, enabling the default operation.

4. To use the function, follow these steps:
    
     ```python  
        # default, will save the result
        ANOVA_RBD.RBD(replication, treatment, input_file_path) 

        # Will not save the result
        ANOVA_RBD.RBD(replication, treatment, input_file_path, False) 
- If you want the output to be used in for further analysis, 
you can then access the calculated values from the ``result`` dictionary:
     
     ```python
        result = ANOVA_RBD.RBD(replication, treatment, input_file_path)
- To access the ``result`` use the following in other code or for further analysis
     
     ```python
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
        EMSS = result["error_mean_ss"],
        TDF = result["total_df"],
        ToSS = result["total_ss"],
        tableDF = result["global_dataframe"]
                
        # Where CF, TSS,.. are variables 
-  You can easily access them in your other Python file and use them as needed. Modify the returned data structure to suit your preferences and the specific values you want to access.

## Features

- Calculates the `correction factor, total sum of squares, replication sum of squares, treatment sum of squares, and error sum of squares`.
- Generates an ANOVA table with the `source, degrees of freedom, sum of squares, mean square, F-values, and p-values at the 5% and 1% significance levels`.
- Performs significance testing at the 5% and 1% levels to determine the statistical significance of the factors.
- Saves the ANOVA results in a text file for further analysis or reporting purposes.

## Example Dataset

- The package requires an Excel file containing the experimental data. The data should be arranged in a Randomized Block Design (RBD) format, with treatments (genotypes) in columns and replications in rows. 
- Please ensure that the excel file is in same format as it is given in this [repo](data/MODEL_DATA.xlsx) or below in separate excel file using the code from [here](https://github.com/Insight-deviler/Folder-based-Character-Column-Transformation)
        
        1. Days to Maturity.xlsx:

                | GENOTYPE  | R1    | R2     | R3     | 
                |-----------|-------|--------|--------|
                | G1        | 74.4  | 70.86  | 60.94  |
                | G2        | 91.82 | 99.18  | 118.88 |
                | G3        | 48.08 | 62.1   | 58.54  |
                | G4        | 59.06 | 65.62  | 81.62  |
                | G5        | 84.16 | 109.74 | 102.14 |

        2. PLANT HEIGHT (cm).xlsx:

                | GENOTYPE  | R1    | R2     | R3     | 
                |-----------|-------|--------|--------|
                | G1        | 74.4  | 70.86  | 60.94  |
                | G2        | 91.82 | 99.18  | 118.88 |
                | G3        | 48.08 | 62.1   | 58.54  |
                | G4        | 59.06 | 65.62  | 81.62  |
                | G5        | 84.16 | 109.74 | 102.14 |

- If you have data in the below format, transform it to above said model (individual character) by using this [code](https://github.com/Insight-deviler/Folder-based-Character-Column-Transformation)

        | GENOTYPE | REPLICATION | Days to Maturity | PLANT HEIGHT (cm) |
        |----------|-------------|------------------|-------------------|
        | G1       | R1          | 4                | 5                 |
        | G1       | R2          | 5                | 6                 |
        | G1       | R3          | 4                | 9.3               |
        | G2       | R1          | 3                | 9.9               |
        | G2       | R2          | 6                | 7.5               |

## License
This package is licensed under the MIT License. See the [LICENSE](https://github.com/Insight-deviler/anova-analysis/blob/main/LICENSE) file for more information.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.

## Authors
- Sarath S (insightagri10@gmail.com)
- Saranyadevi S

## Acknowledgements

- This package was developed as part of research work. 
- This is based on `Biometrical Methods in Quantitative Genetic Analysis by R.K. Singh and B.D. Chaudhary`
- I would like to thank all contributors and supporters.

## Disclaimer

The `anova_analysis` package provided in this repository is offered "as is" without any warranty or guarantee of its functionality, performance, or suitability for any specific purpose. The author(s) and contributors of this package shall not be held liable for any direct, indirect, incidental, consequential, or other damages or losses resulting from the use of this package.

The user assumes all responsibility and risk associated with the installation, configuration, and usage of this package. It is strongly recommended to thoroughly test the package in a controlled environment before using it in production or critical systems. 

The author and contributors cannot be held responsible for any loss of data, system failures, or any other damages or issues caused by the use or misuse of this package. 

It is the user's responsibility to ensure the compatibility of this package with their specific environment, including the software versions, hardware, and other dependencies. Any modifications or customizations made to this package are solely the user's responsibility, and the author or contributors shall not be responsible for any resulting issues.

By using this package, you agree to the terms and conditions stated in this disclaimer. If you do not agree with these terms, you should not install, configure, or use this package.

Please exercise caution and make informed decisions when using this package. It is always recommended to have proper backups and contingency plans in place to mitigate any potential risks.