#specifying interpreter for the script
#!/bin/bash

#variables
dir_files="./fajlovi"/* # gets all the files in subfolder "fajlovi" of this folder
name_field=$(echo -e "\036\062\060\060") # [RowSeparatorCharacter]200 in ASCII
unit_separator=$(echo -e "\036") # [UnitSeparator] in ASCII
a_subfield=$(echo -e "\037\0141") # [UnitSeparator]a in ASCII
prefix_regex="^[A-Z][A-Z]-[0-9][0-9][0-9][a-z]"
prefix_props_regex="[A-Z][A-Z]=.*"
#prints out all of the files in the folder
# for each_file in "./fajlovi"/*
# do
#   cat $each_file
# done

echo "/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
#prints out the number of lines for each file of the folder
for each_file in $dir_files; do
 echo "$each_file has $(grep -c ^ $each_file) lines."
done
echo "/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"

#checking file integrity for each required file in the folder
for each_file in $dir_files; do
 #knjige.txt
 if [[ $each_file == *"knjige.txt" ]]; then
   lines=$(cat $each_file) #gets all the lines of the file
   line_index=1 #keeps track of line index
   num_of_invalid_records=0 #keeps track of invalid records found

   IFS=$'\n' #delimiter that for loop uses (usually it's a whitespace but in our case we want a new line character)
   for file_line in $lines; do
     if [[ $file_line == *$name_field* ]]; then
       trimmed_str=${file_line#*$name_field} #getting rid of everything before [RS]200

     else
       echo "Line at index $line_index does not contain name field. Line content: $file_line"
       ((num_of_invalid_records++)) #incrementing number of invalid lines
       ((line_index++)) #incrementing line index
       continue;
     fi

     #echo $trimmed_str
     trimmed_str=${trimmed_str%%$unit_separator*} #getting rid of everything after [US] - double percent sign instead of one to start from the beginning of the string, not from the end (as in case of single percent sign)

     #checking whether field contains [US]a subfield
     if ! [[ $trimmed_str == *$a_subfield* ]]; then
       echo "Line at index $line_index does not contain name subfield. Line content: $file_line"
       ((num_of_invalid_records++)) #incrementing number of invalid lines
     fi

     ((line_index++)) #incrementing line index


   done
   unset IFS

 #prefiksi.txt
 elif [[ $each_file == *"prefiksi.txt" ]]; then
   line_index=1;
   num_of_invalid_records=0
   file_lines="$(cat $each_file)"

   IFS=$'\n'
   for file_line in $file_lines; do
     if ! [[ $file_line =~ $prefix_regex ]]; then
        echo "Line at index $line_index does not match the regular expression. Line content: $file_line"
        ((num_of_invalid_records++))
     fi

     ((line_index++))
   done
   unset IFS

 #prefixNames_sr.properties
 elif [[ $each_file == *"PrefixNames_sr.properties" ]]; then
   line_index=1;
   num_of_invalid_records=0
   file_lines="$(cat $each_file)"

   IFS=$'\n'
   for file_line in $file_lines; do
     if ! [[ $file_line =~ $prefix_props_regex ]]; then
        echo "Line at index $line_index does not match the regular expression. Line content: $file_line"
        ((num_of_invalid_records++))
     fi

     ((line_index++))
   done
   unset IFS
 fi
 echo "Total number of invalid lines for $each_file: $num_of_invalid_records"
 #resetting file variables for the next file
 line_index=1;
 num_of_invalid_records=0;
done
