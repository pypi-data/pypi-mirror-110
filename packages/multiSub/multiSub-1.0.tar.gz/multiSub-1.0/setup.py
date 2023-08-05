import setuptools

setuptools.setup(
    name="multiSub",
    version='1.0',
    license="GPL 3",
    python_requires='>=2.7',
    author="Maximilian Haeussler",
    author_email="maxh@ucsc.edu",
    url="https://github.com/maximilianh/multiSub",
    description="SARS-CoV-2 data converter between Genbank/GISAID/ENA formats",
    long_description="""
    Prepares a SARS-CoV-2 submission for GISAID, NCBI or ENA. Can read GISAID or NCBI files, or plain fasta+tsv/csv/xls. Finds files in input directory and merges everything into a single output directory. Auto-detects input file formats. Can submit the results to multiple repositories from the command line.""",
    scripts=["multiSub"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript"
    ],
)
