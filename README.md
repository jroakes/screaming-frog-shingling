# screaming-frog-shingling
Uses Screaming Frog Internal HTML with text extraction along with a shingling algorithm to compare content duplication across the pages of a crawled site. 

## Example Usage

1. `pip install -r requirements.txt`

1. Run Screaming Frog and use Extraction to pull the content out of a specific DOM element.
![Screaming Frog Extraction](https://raw.githubusercontent.com/jroakes/screaming-frog-shingling/master/sf_extraction.png "Screaming Frog Extraction Example")

1. Export the internal HTML to a CSV file.
![Export Internal HTML](https://raw.githubusercontent.com/jroakes/screaming-frog-shingling/master/internal_html.png "Screaming Frog Internal HTML Export")

1. Run the script using the following arguments.

```
 Example Usage:
    -i : Input filename
    -o : Output filename
    -c : Column from Screaming Frog that contains your extracted content.
    Example invocation:
    python sf_shingling.py -i internal_html_ap.csv -o output_html_ap.csv -c "BodyContent 1"
```

