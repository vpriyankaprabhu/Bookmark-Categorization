##########################################################################################
#
# Effortless Bookmark Categorization with Custom Rules
#
# Lets see how easily and efficiently we can organise our personal bookmarks
# 
# Script Name : categorize_bookmarks.py
#
# Developer : Priyanka Prabhu
#
# Version : 2024.11.16.v1
##########################################################################################

import json
import argparse
import os

# Lets try to build a logic to work on categorizing the available bookmark details from firefox browser.

# Method to load json file
def load_json(file_name):
    with open(file_name) as file_handler:
        json_data = json.load(file_handler)

    return json_data

# Method to filter firefox_bookmarks.json file to get minimal required values such as name, title, tags for
# further parsing and categorizing them with the config.json categorization rules
def get_required_bookmarks_data_as_list(bookmarks_content):

    # Temporary variable to save the bookmarks as list with minimal required values such as 
    # name, url, tags by parsing bookmarks_content
    bookmarks_list = []

    # Save minimal required values such as name, url, tags by parsing bookmarks_content into bookmarks_list
    for root_bookmark_children_section in bookmarks_content["children"]:
        # firefox bookmarks picked from sample-testing folder for this example
        # We will check for this child nodes and start parsing
        if root_bookmark_children_section["title"] == "sample-testing":
            # For each child bookmark lets create a dictionary and save it in bookmarks_list
            for child_bookmark in root_bookmark_children_section["children"]:
                # Split the tags with , as delimited and save it as list
                tags = child_bookmark["tags"].split(",")
                # Dictionary with required values as name, url, tags
                local_dict = {"name" : child_bookmark["title"], "url" : child_bookmark["uri"], "tags" : tags}
                # bookmarks_list is appended with dictionary created from values for name, title and tags
                bookmarks_list.append(local_dict)

    return bookmarks_list

# Logic to categorize bookmarks using config.json custom rules for categorization on bookmark_data.json data
def categorize_bookmarks(bookmarks, config):
    # Create a new empty list "categorized" with categories 
    # for example : ['Technology': [], 'Science': [], 'Education': [], 'Entertainment' : [], 'Finance' : []]
   categorized = {category: [] for category in config['categories']}

   # Go through each bookmarks (list of dictionaries)
   for bookmark in bookmarks:
       # Check each tag in the bookmark
       for tag in bookmark['tags']:
           # We now need to check each bookmark tag with tag keywords list in config[categories] for each category
           for category, keywords in config['categories'].items():
               if tag.lower() in [keyword.lower() for keyword in keywords]:
                   # if bookmark tag is found in tag keywords of each category then append local_dict to categorized[categorized] list
                   local_dict = {"name": bookmark['name'], "url": bookmark['url']}
                   if local_dict in categorized[category]:
                       # to skip adding duplicate entries to categorized[category] list
                       break
                   else:
                       # append local_dict to categorized[categorized] list
                       categorized[category].append(local_dict)
                       
   # returns categorized list
   return categorized

def main():
    # parse input arguments
    parser = argparse.ArgumentParser(description = "Effortless Bookmark Categorization with Custom Rules")
    parser.add_argument("-c", "--config_file", help = "Example: config.json file", required = True)
    parser.add_argument("-b", "--bookmarks_file", help = "Example: bookmarks file", required = True)
    parser.add_argument("-o", "--output", help = "Example: output file", required = False, default = "organized_bookmarks.md")

    # parse input arguments
    args = parser.parse_args()
    bookmarks_file = args.bookmarks_file # bookmarks file
    config_file = args.config_file  # config file with custom rules for categorization 
    output_file = args.output # output file in user readable format for ready reference

    # Load firefox_bookmarks.json file for parsing
    bookmarks_content = load_json(bookmarks_file)

    # get a bookmarks_list by parsing bookmarks_file to get minimal required values such as name, title, tags for
    # further parsing and categorizing them with the config.json categorization rules
    bookmarks_list = get_required_bookmarks_data_as_list(bookmarks_content)

    # Write bookmarks_list to bookmark_data.json file
    with open("bookmark_data.json", "w") as bookmarks_file_handler:
        # Need to replace single quote with double quotes for json file parsing else throws error
        bookmarks_file_handler.write(str(bookmarks_list).replace("'", "\""))

    # Load the config.json file
    config = load_json(config_file)
    # Load "bookmark_data.json" file for parsing
    bookmarks = load_json("bookmark_data.json")
    os.remove("bookmark_data.json")

    # Lets finally now try to categorize bookmarks and create a user readable file with categorized bookmarks for ready reference.

    # Since now, we have both config.json and bookmark_data.json files ready, lets try to work on them
    # We will have to now use the custom rules or configs mentioned in config.json for effortless categorization of browser
    # bookmarks saved in firefox_bookmarks.json file. The output should be user friendly and readable format for ready reference.
    categorized_bookmarks = categorize_bookmarks(bookmarks, config)

    # Create a readable output format
    output = ""
    for category, items in categorized_bookmarks.items():
        output += f"##### {category} \n"
        for item in items:
            output += f"- [{item['name']}]({item['url']})\n"
        output += "\n"

    # Write output to organized_bookmarks.md file for organised/categorized bookmarks
    with open(output_file, "w") as output_file_handler:
        output_file_handler.write(output)
        
    # Reading organized_bookmarks.md file to check its contents
    with open(output_file, "r") as output_file_handler:
        organized_bookmark_contents = output_file_handler.read()
        # move the file pointer to beginning of the file for next read
        output_file_handler.seek(0)

    # Print contents of config.json file
    print(organized_bookmark_contents)

    print(f"Bookmarks have been organized and saved to '{output_file}'.")

if __name__ == "__main__":
    main()