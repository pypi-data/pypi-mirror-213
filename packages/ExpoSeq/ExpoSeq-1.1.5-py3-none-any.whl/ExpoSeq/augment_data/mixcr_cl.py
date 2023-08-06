import pandas as pd
import os
import subprocess
import pickle
from glob import glob
import shutil
from ExpoSeq.augment_data.trimming import trimming
#from .trimming import trimming

#
def remove_directories(directory_path):
    # Iterate over all items in the directory
    for item in os.listdir(directory_path):
        shutil.rmtree(os.path.join(directory_path, item))


def collect_fastq_files(fastq_directory):
    filenames = []
    path_to_files = os.path.abspath(fastq_directory)
    filenames.extend(glob(os.path.join(path_to_files, "*.fastq")))
    if len(filenames) == 0:
       print(
            "You have not chosen a directory with fastq files.")

    else:
        print("These are the files you chose:")
        for i in filenames:
            print(os.path.basename(i))

    return filenames


def mixcr_(fastq_directory, path_to_mixcr, save_dir, paired_end_sequencing, threads, method, trim_div_by, trim_min_count, testing = False):
    if not testing:
        filenames = collect_fastq_files(fastq_directory)
    else:
        filenames = glob(os.path.join(r"C:\Users\nilsh\my_projects\ExpoSeq\tests", "*.fastq"))
    if len(filenames) == 0:
        print("You have not added any fastq files.")
        return
    print("Test Mixcr")
    subprocess.run(["java",
                    "-jar",
                    path_to_mixcr,
                    "--version"
                    ])
    confirmation = True
    if confirmation == True:
        if not os.path.isdir("temp"):
            os.mkdir("temp")

        module_dir = os.path.abspath("")
        sequencing_report = pd.DataFrame([])
        if paired_end_sequencing == True:
            filenames_unique_reverse = [unique for unique in filenames if "2.fastq" in unique]
            filenames_unique_forward = [unique for unique in filenames if "1.fastq" in unique]
            combined_filenames = []
            for i in filenames_unique_reverse:
                file_one = i
                basename = os.path.basename(os.path.splitext(file_one)[0])
                basename = basename[:len(basename) - 2]
                file_two = ""
                for j in filenames_unique_forward:
                    if basename in filenames_unique_forward:
                        file_two = j
                        break
                if file_two == "":
                    print("you are missing the the reverse strand for " + basename)
                else:
                    fastq_files = file_one + " " + file_two
                    combined_filenames.append(fastq_files)
            if len(combined_filenames) == 0:
                print("the system couldnt find any forward reverse matches. Please check your given directory or continue with single-end analysis.")
                return
        else:
            combined_filenames = filenames
        for filename in combined_filenames:
            try:
                basename = os.path.basename(os.path.splitext(filename)[0])
                basename = basename[:len(basename) - 2]
                filename_base = basename
                result = os.path.join(module_dir, "temp", filename_base + ".vdjca")
                clones = os.path.join(module_dir, "temp", basename + "clones.clns")
                subprocess.run(["java",
                                "-jar",
                                path_to_mixcr,
                                "align",
                                "-p " + method,
                                filename,
                                result,
                                "--report",
                                os.path.normpath(os.path.join(module_dir,
                                                              filename_base + "_AlignmentReport.txt")),
                                "--threads",
                                str(threads)
                                ])

                subprocess.run(["java",
                                "-jar",
                                path_to_mixcr,
                                "assemble",
                                "-OseparateByC=true",
                                "-OseparateByV=true",
                                "-OseparateByJ=true",
                                result,
                                clones,
                                "--threads",
                                str(threads)
                                ])

                subprocess.run(["java",
                                "-jar",
                                path_to_mixcr,
                                "exportClones",
                                "-cloneId",
                                "-readCount",
                                "-readFraction",
                                "-lengthOf CDR3",
                                "-nFeature CDR3",
                                "-aaFeature CDR3",
                                "-avrgFeatureQuality CDR3",
                                clones,
                                os.path.join(module_dir,
                                             "temp",
                                             basename + ".tsv"),
                                "--threads",
                                str(threads)
                                ])

                clones_sample = pd.read_table(os.path.join(module_dir,
                                                           "temp",
                                                           basename + "_IGH.tsv"))
                clones_sample = clones_sample[["cloneId",
                                               "readCount",
                                               "readFraction",
                                               "nSeqCDR3",
                                               "aaSeqCDR3",
                                               "minQualCDR3",
                                               "lengthOfCDR3",
                                               "meanQualCDR3"]]
                new_fractions = clones_sample.groupby("nSeqCDR3")["readFraction"].sum().reset_index()
                clones_sample = clones_sample.drop_duplicates(subset=["nSeqCDR3"], keep="first")
                clones_sample = new_fractions.merge(clones_sample,
                                                    how="left",
                                                    on="nSeqCDR3")
                clones_sample = clones_sample.sort_values(by="cloneId")
                clones_sample = clones_sample.reset_index()
                clones_sample = clones_sample.drop(columns=["readFraction_y", "index"])
                clones_sample = clones_sample.rename(columns={"readFraction_x": "cloneFraction"})
                clones_sample["Experiment"] = filename_base
                clones_sample = trimming(clones_sample,
                                         divisible_by=trim_div_by,
                                         min_count=trim_min_count,
                                         new_fraction="clonesFraction")
                sequencing_report = pd.concat([sequencing_report, clones_sample])
                files_to_remove = os.listdir(os.path.join(module_dir, "temp"))
                for file in files_to_remove:
                    os.remove(os.path.join(module_dir,
                                           "temp",
                                           file))
                report_dir = os.path.join(save_dir,
                                      "sequencing_report.txt")
                sequencing_report.to_csv(report_dir)
            except:
                remove_directories(os.path.join(module_dir, "temp"))

    else:
        print("The path to the mixcr jar file is not correct or you are missing the licence")