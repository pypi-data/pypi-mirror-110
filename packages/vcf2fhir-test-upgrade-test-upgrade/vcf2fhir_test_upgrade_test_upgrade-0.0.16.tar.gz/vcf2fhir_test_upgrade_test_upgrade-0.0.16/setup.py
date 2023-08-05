import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vcf2fhir_test_upgrade_test_upgrade",
    version="0.0.16",
    author="",
    test_suite='vcf2fhir_test_upgrade.test.test_vcf2fhir_test_upgrade.suite',
    author_email="info@elimu.io",
    description="Convert .vcf files to HL7 FHIR standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elimuinformatics/vcf2fhir_test_upgrade",
    packages=['vcf2fhir_test_upgrade', 'vcf2fhir_test_upgrade.test'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
    tests_require=[
        'unittest',
    ],
    install_requires=[
        'Cython >=0.29.21',
        'fhirclient==3.2.0',
        'pysam',
        'pandas',
        'pytz >= 2019.3',
        'pyVCF >=0.6.8',
        'pyranges >= 0.0.96'
    ],
    python_requires='>=3.6',
)
