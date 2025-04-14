# Ethereum Transaction Dependency Viewer

A simple static website that displays Ethereum transaction dependency graphs, hosted on GitHub Pages.

## Project Structure

```
static/
├── data/          # JSON files with block metadata
├── graphs/        # PNG images of transaction dependency graphs
├── gantt/         # PNG images of Gantt charts
└── index.html     # Main page
```

## Initial Setup

1. Clone this repository
2. Make the scripts executable:
   ```bash
   chmod +x setup_repo.sh update_github.sh
   ```
3. Run the setup script to clean the repository and set up the initial frontend:
   ```bash
   ./setup_repo.sh
   ```

## Adding Data Files

After the initial setup, you can add data files to the respective directories:
- `data/latest_blocks.json` - Contains metadata about the latest blocks
- `graphs/*.png` - Dependency graph images
- `gantt/*.png` - Gantt chart images

## Updating the Site

To update the site with new data:

1. Place new files in their respective directories under `static/`
2. Run the update script:
   ```bash
   ./update_github.sh
   ```

The script will:
- Add only files from the specified directories (graphs, gantt, data)
- Create a commit with the current timestamp
- Push the changes to GitHub

## Data Format

The `data/latest_blocks.json` file should contain an array of block objects with the following structure:

```json
[
  {
    "number": 12345678,
    "transactionCount": 42,
    "timestamp": 1234567890
  }
]
```

## Development

The site is completely static and requires no build process. Simply edit the `index.html` file to make changes to the layout or styling. 