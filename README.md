# Refine refactor
Please, take a break and read this. It'll be usefull.

 ## Before implementation:
 You have to know somethings:
 * For each steps :
	 * In **.cpp** or **.h** file : replace code between **#else** and **#endif** with your code.
	 * In **.py** file, do the same with **else** in case where the **if** is **if app.MULTIPLE_REFINE:**.
 * **You can report any bugs to me on my Discord**.
 ## DataBase implementation :
 Put your item_proto.txt in the folder, and run **converter.py** (Python3). The script will generate a new file : **refine_table.py**. After, you have to use it on your **player** database.

## Add a new recipe :
To add a new recipe, two cases:
* If you item already has a recipe, search it on **refine_table**, and complete **dest_vnum_0** and **refine_set_0** columns.
* If it's a new item: Create a line in **refine_table** and complete it like others.

**Don't forget to complete your item_proto.txt, refine_set will not be used, but refine vnum is use for slot coloration (put something different from 0).**
**if you use a scroll for the refine and If you use a scroll and the upgrade fails, metin2 will search the first item in item_proto.txt which has in "refine" the item which fails**

### Authors
Made by nicolasCDT, a french guy !
* Discord: **Takuma#2725**
* [GitHub](https://github.com/NicolasCDT)
* [Website](https://nicolas.coudert.pro.com)
