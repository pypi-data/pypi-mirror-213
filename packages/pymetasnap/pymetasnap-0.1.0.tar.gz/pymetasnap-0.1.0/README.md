# cli-pymetasnap

cli-pypi-metadata-extractor is a command-line tool that enables you to extract metadata from the Python Package Index (PyPI). It allows you to retrieve essential information about Python packages hosted on PyPI, including package names, versions, licenses, project URLs, and more.

By leveraging the PyPI API, cli-pypi-metadata-extractor automates the process of gathering package metadata, making it convenient for developers, researchers, and anyone interested in exploring package information in a structured manner.

## Features

Retrieve metadata for Python packages from PyPI.
Extract package names, versions, licenses, and other relevant information.
Fetch project URLs and version-specific URLs for detailed package exploration.
Store the extracted metadata in CSV or Excel format for further analysis.

## Installation

You can install cli-pypi-metadata-extractor using pip:

```bash
pip install cli-pypi-metadata-extractor
```

Usage
To extract metadata for Python packages from PyPI, use the following command:

```bash
cli-pypi-metadata-extractor --source-path <path_of_the_txt_file> --output <output_path> --format <output_format>
```

Replace the following placeholders in the command:

`<path_of_the_txt_file>`: Names of the packages to retrieve metadata for (separated by spaces).
`<output_path>`: Path to store the extracted metadata file.
`<input_format>`: Format of the input file (csv or xlsx).
Example usage:

```bash
cli-pypi-metadata-extractor --source-path ./requirements.txt --output metadata.csv --format csv
```

## Output

The tool generates a file containing the extracted metadata for the specified packages in the provided output format (CSV or Excel). The output file includes columns for package name, version, license, repository URL, project URL, and version-specific URL. This information can be used for various purposes, such as dependency analysis, license compliance, or package research.

## Contributing

Contributions to cli-pypi-metadata-extractor are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the project's GitHub repository.

When contributing, please ensure that you follow the existing coding style, write tests for new features, and make sure the tests pass before submitting a pull request.

## License

cli-pypi-metadata-extractor is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

The cli-pypi-metadata-extractor tool builds upon the PyPI API to provide a convenient way to access package metadata. We would like to express our gratitude to the PyPI maintainers and the Python community for their continuous efforts in maintaining and improving the Python Package Index.

## Contact

For any inquiries or feedback, please contact the project maintainer at cristian.o.rincon.b@gmail.com.
