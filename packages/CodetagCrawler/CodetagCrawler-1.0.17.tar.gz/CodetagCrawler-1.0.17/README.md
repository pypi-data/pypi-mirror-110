# Codetag Crawler

## Description:
This package provides a click command line interface to a codetag crawler, which
searches through a target directory for codetags, and formats them to a .csv format
that can be imported to Azure DevOps or other services using equivalent .csv formats.
A config file is provided to define which codetags to search for. Possible codetags are
as of now limited by the .yml format, so codetags like !!! or ??? are not supported as is.

Has this ever happened to you? You are happily content hacking down code for the project you
are working on, only to spot an error in the code, missing documentation, refactor target, or
really just about anything that should be done at some point. But you are in the flow of working
on something else, so you don't want to lose your headspace by fixing the issue right now, just 
as much as you don't want a mountainous and confusing pull request. So you have to click your way
out of your development environment and onto whichever software your team are tracking issues and
bugs in, manually enter the found issue, only to go back to development having entirely forgotten
what you were thinking about. If only there was a better way. 

Thankfully, there is. With this Code Crawler all you have to do is enter your thoughts in a comment
with a codetag. Then the crawler is ready to creep through your code and find every codetag comment,
and export them to a .csv format ready to upload to your DevOps software. 

The code supports consecutive code tags, so for example: 

.# TODO I am part one

.# And I am part two

.# FIXME Make sure to include me as a seperate comment
will be interpreted as two comments. The crawler also supports
''' and """ block comments, but then supporting only one code tag. 
Code tags must be the first word in the comment to get registered. 

# Installation
The package can be installed by using PIP.

# Usage
The click interface supports the following commands: 

process [-i] path_to_input_folder -o path_to_output_csv -c (optional) path_to_config_file
If no config file is provided default is used
Config supports defining which CODETAGS to search for, defining directories that
should not be searched through (ex. your venv) and defining a mapping between codetags and
work item types. 

If you want to support codetags such as !!!, which are not compatible with standard .yml parsers,
you should change the get_metadata function in metadata_handler.py to support your desired changes.

# Roadmap
I would like to implement syncing of comments to issues using IDs, s.t. changes in comments could be
synced to appropriate work items, and changes to work items could be synced to appropriate comments. 

Defining more fields for work items could also be supported, such as defining the priority of the work
item. This should ideally be done by including text in a < > or other enclosing in the comment, and defining
a regex-parsingaand writing a regex or other format command in the config metadata for each desired field. 

# Contributing
I am open to accepting pull requests as long as they are atomic and well-documented, and I find the change
good/reasonable/positive. 

You are also free to fork this project if you wish to. 