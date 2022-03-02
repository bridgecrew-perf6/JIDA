# use the vcf to snp characteristics table for both


# setting directory
import os
newpath = "E:\Bioinf_data\population VCFs\snp characteristics"
os.chdir(newpath)
path = os.getcwd()
print(path)

def VCF_to_snp_characteristics(inputlist, outputlist, popcodelist, start, end):
    'converting multiple population VCFs to a combined SNP characterisitcs CSV, removing multi-allelic sites. Author: Isabel Thompson.'

    # import dependencies
    import pandas as pd
    import os
    from Conversion_scripts import VCFtoPandas
    from pathlib import Path

    # iterate over the 5 population vcfs
    for inVCF, outCSV,popcode in zip(inputlist,outputlist,popcodelist):

        # check inputs
        print("process started...")
        print(inVCF)

        # create dataframe
        df = VCFtoPandas(inVCF)
        print("dataframe created")




        # rename columns in accordance with SQL schema
        df.rename(columns={'#CHROM': 'chromosome', 'POS': 'position', 'ID': 'rs_value', 'REF': 'reference', 'ALT': 'alternate'}, inplace=True)

        # shorten the df
        #df = df.loc[start:]

        # extract row names
        row_labels_df = list(df.index)

        # remove multiallelic sites
        for row in row_labels_df:
            alt = df.loc[row,'alternate']
            alt = len(alt)
            if alt != 1:
                # delete multiallelic row from dataframe
                df = df.drop(labels=row)

        print("multi allelic sites removed")
        df = df.reset_index()
        print("index reset")

        length = len(df)
        totallength = length * 5
        print(length)
        print(totallength)
        print(emergencystop)

        # extract updated row names
        row_labels_df = list(df.index)


        # remove unwanted columns
        df_info = df.filter(['rs_value'], axis=1)

        print("data filtered")






        # filter dataframe to just the sample columns
        sample_cols = [col for col in df if col.startswith('HG')]
        print("columns filtered")
        df_samples = df[sample_cols]
        #print(df_samples)





        # delete df to free up memory
        del df

        # initiate new df
        more_info = pd.DataFrame(columns=('population', 'sample_count', 'gt_00_count', 'gt_01_count', 'gt_10_count', 'gt_11_count'))


        # fill more info df
        for row in row_labels_df:
            sample_count = 0
            gt_00_count = 0
            gt_01_count = 0
            gt_10_count = 0
            gt_11_count = 0
            for column in df_samples:
                gt = df_samples.loc[row, column]
                if gt == '0|0':
                    sample_count += 1
                    gt_00_count += 1
                elif gt == '0|1':
                    sample_count += 1
                    gt_01_count += 1
                elif gt == '1|0':
                    sample_count += 1
                    gt_10_count += 1
                elif gt == '1|1':
                    sample_count += 1
                    gt_10_count += 1
            more_info = more_info.append({'population': popcode, 'sample_count': sample_count, 'gt_00_count': gt_00_count,
                                              'gt_01_count': gt_01_count, 'gt_10_count': gt_10_count,
                                              'gt_11_count': gt_11_count}, ignore_index=True)
            print("row added")


        df_final = pd.concat([df_info, more_info], axis=1)
        print("concatenation done")


        filepath = Path(outCSV)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df_final.to_csv(filepath,index = False)

        # delete dataframe(s) and free memory
        del df_info
        del df_samples
        del df_final
        del more_info

    import glob
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined = pd.concat([pd.read_csv(f, dtype={'rs_value': 'str',
                                                 'population': 'str',
                                                'sample_count': 'str', 'gt_00_count': 'str', 'gt_01_count': 'str',
                                                'gt_10_count': 'str', 'gt_11_count': 'str'}) for f in all_filenames])
    # export to csv
    filename = "snp_characteristics" + str(start) + "-" + str(end) + ".csv"
    combined.to_csv(filename, index=False, encoding='utf-8-sig')



vcfnamelist = ['Punjabi_SNV_only.vcf', 'Colombian_SNV_only.vcf', 'British_SNV_only.vcf','Telugu_SNV_only.vcf','Finnish_SNV_only.vcf']
csvnamelist = ['Punjabi.csv', 'Colombian.csv','British.csv','Telugu.csv','Finnish.csv']
popnamelist = ['PUN', 'COL','GBR','TEL','FIN']

VCF_to_snp_characteristics(vcfnamelist,csvnamelist,popnamelist, 0, 10)
