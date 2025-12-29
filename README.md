# AssetResolver

AssetResolver is a small CLI tool that resolves original assets from a source directory based on a set of reference files.

It is useful when derived or edited files exist separately from their canonical originals and you need to reconstruct a matching subset of the original dataset.

## How it works

- Reference files define a set of keys (filename without extension)
- Source assets are indexed using the same keys
- Matching source files are copied to a destination directory
- Missing assets are reported

File extensions are configurable and treated as representations, not identity.

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/assetresolver.git  
cd assetresolver
```

Python 3.12 or newer is recommended. No external dependencies are required.

## Usage

```bash
python main.py \
  --reference-dir A \
  --source-dir B \
  --dest-dir C \
  --reference-ext .png \
  --source-ext .jpg .jpeg
```

## Options

- --reference-dir  
  Directory containing reference files
- --source-dir  
  Directory containing source assets
- --dest-dir  
  Destination directory
- --reference-ext  
  Reference file extensions
- --source-ext  
  Source file extensions
- --dry-run  
  Show actions without copying files

## Example

```cli
A/  
  IMG_001.png  
  IMG_002.png  

B/  
  IMG_001.jpg  
  IMG_002.jpg  
  IMG_003.jpg  

Result:

C/  
  IMG_001.jpg  
  IMG_002.jpg  
```

# Contributing
Contributions are welcome! Please fork the repository and submit pull requests.

# License
This project is licensed under the MIT License.

# Acknowledgements
NHL Stenden: For providing the foundational code and utilities.
Martin Bosgra: Author and primary maintainer of the project.

