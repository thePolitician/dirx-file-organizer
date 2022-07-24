# DirX: File and folder handling tools
(Using Python3 and tkinter)

Start Application: run dirx.py

[INTRO starts at line 16]
There is a lot that can be impoved in this project so feel free to contribute.
A few things which I think can be improved or added-
1. Have a look at how threading is used in DirX (it may not be safe) as I have no expertise in this topic.
2. Progress bar can be added to display progress as well as to shadow (take focus from) main window while an operation is in process.
3. Support for multiple file selection as currently users can only select a folder and all files are exported from that folder.
4. Bulk operation for Encrypt/Decrypt module (encrypt/decrypt multiple files at once).
5. Log generation for each tab. Log which file moved to which folder, which file renamed to what filename, which files were encrypted/decrypted.
6. Other temporary locations can be added in Clear Temp section like user downloads, system temp, update files etc.

DirX has 5 modules currently:
1. File Organizer
2. Folder Unpack
3. Batch Rename
4. Encrypt/Decrypt
5. Clear Temp

#File Organizer
File organizer uses 4 different methods to organize files.
1. By Type: Files are organized into different groups based on their type e.g., IMAGES, DOCUMENTS etc. Groups can be edited, added and removed by the user.
2. By Extension: Files will be organized in separate folders based on their extension.
3. By Date Created
4. By Date Modified
Last operation can be undone.

#Folder Unpack
Moves files from all immediate subdirectories to parent directory.
Folder Unpack is somewhat a complementary feature to File Organizer. Main purpose of adding this module was to undo the operation of File Organizer but it can be used as a completely different unit.
Example use case: Suppose you organized a folder full of hundreds of types of files (and hence creating hundred different folders) and then you closed DirX. Now lets say you changed your mind and want to undo this operation. Since you had closed the application, the undo button of File Organizer will not work. Folder Unpack can be used here.
Remember that Folder Unpack is different from Undo as it does not restore the previous structure of directory but simply moves files from subdirectories to parent directory.

#Batch Rename
Renames multiple files at once based on a given name template.
The filename structure has 3 components- Prefix, Filename and Postfix. Each component has 4 common options which can be adjusted independently for each component.
Options-
1. Custom
2. Numeric
3. Date Created
4. Date Modified

Example: If you selected-
Prefix - Numeric
Filename - Custom [SalesReport]
Postfix - Date Created
then files will be renamed with the following name structure- 0 SalesReport 25 July 2022.xlsx

#Encrypt/Decrypt
Encrypt and decrypt files based on password. Uses AES encryption.

#Clear Temp
Deletes temporary files in user folder.
