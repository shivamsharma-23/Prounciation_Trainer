import pandas as pd

# Read the existing sentences from the file and clean them
with open('d:\\AI2\\pronunciation_trainer\\data_en.csv', 'r', encoding='utf-8') as file:
    # Remove any empty lines and clean the sentences
    sentences = []
    for line in file:
        line = line.strip()
        if line and not line.startswith('...'):  # Skip empty lines and ellipsis
            # Remove any commas to prevent CSV parsing issues
            line = line.replace(',', '')
            sentences.append(line)

# Create DataFrame with proper column structure
df = pd.DataFrame({
    'text': sentences
})

# Save as properly formatted CSV with specific parameters
df.to_csv('d:\\AI2\\pronunciation_trainer\\data_en.csv', 
          index=False, 
          quoting=1,  # Quote all fields
          escapechar='\\',  # Use backslash as escape character
          encoding='utf-8')

print(f"Successfully processed {len(sentences)} sentences")