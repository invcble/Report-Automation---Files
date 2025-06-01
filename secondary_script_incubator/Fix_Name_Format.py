import csv

def capitalize_columns(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read and write the header as is
        headers = next(reader)
        writer.writerow(headers)
        
        # Process and write the rest of the rows
        for row in reader:
            # Apply capitalize to the first two columns
            if len(row) > 0:
                row[0] = row[0].replace(" ", "").capitalize()
            if len(row) > 1:
                row[1] = row[1].replace(" ", "").capitalize()
            writer.writerow(row)

# Example usage
input_file = "C:\\Users\\Administrator\\Downloads\\ALLpeersMerk2024.csv"
input_file2 = "C:\\Users\\Administrator\\Downloads\\MerckCombined.csv"
output_file = 'Namefixed_ALLpeersMerk2024.csv'
output_file2 = 'Namefixed_MerckCombined.csv'
capitalize_columns(input_file, output_file)
capitalize_columns(input_file2, output_file2)

