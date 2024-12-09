```markdown
```markdown
# The Table Tool in  
axesPDF®  
V01.2023  

---

Copyright © 2023 axes4 GmbH
```
```markdown
# Table of Content  

1 **Basic knowledge about tables**............................................................................................ 4  
   1.1 The difference between data tables and layout tables ...................................................... 4  
   1.2 **Requirements for data tables**......................................................................................... 4  
       1.2.1 Built logically ............................................................................................................... 4  
       1.2.2 Clear and unique relationship .................................................................................... 5  
       1.2.3 Understandable ........................................................................................................... 5  
   1.3 Simple Table ....................................................................................................................... 5  
   1.4 Complex tables .................................................................................................................... 6  
       1.4.1 Mark the relationship by using Header IDs or by reworking the complex table into   
       several simple tables ........................................................................................................... 6  
   1.5 Simple or complex? .......................................................................................................... 10  
   1.6 Read more ......................................................................................................................... 10  
   
2 **The Table Tool** ................................................................................................................... 11  
   2.1 What is the TABLE TOOL? .................................................................................................... 11  
   2.2 How do you start the TABLE TOOL? .................................................................................... 11  
   2.3 **Basic features** ............................................................................................................... 11  
       2.3.1 Different types of table cells .................................................................................... 11  
       2.3.2 Understanding the circle symbol .............................................................................. 12  
       2.3.3 Recognize and check associated header cells ......................................................... 12  
       2.3.4 Associate header cells .............................................................................................. 12  
   2.4 Shortcuts ........................................................................................................................... 14  
   2.5 **Use the table tool efficiently** ....................................................................................... 14  
       2.5.1 Step 1: Pre-Check ..................................................................................................... 14  
       2.5.2 Step 2: Check if your table is tagged properly ......................................................... 15  
       2.5.3 Step 3: Evaluate if you have a simple or a complex table ....................................... 15  
  
Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

2.5.4 Step 4a: Associate header cells by using SCOPE attributes ................................................ 16  
2.5.5 Step 4b: Associate header cells by using IDs ....................................................................... 16  
2.5.6 Step 5: Final check of associated header cells .................................................................... 16  

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

## 1 Basic knowledge about tables

### 1.1 The difference between data tables and layout tables

In nearly all cases, in which you simply use the expression “table,” you talk about data tables.  
Data tables are used to organize data with a logical relationship in grids. Accessible PDF tables  
need tags that indicate header cells and data cells as well as tag attributes that define the  
relationship between the cells.

In order to make data tables accessible, they have to fulfil the following pre-requisites:
- **Built logically**
- **Clear and unique relationship** between header cells and data cells or between header cells  
  and subordinated header cells
- **Understandable**

From the perspective of semantics, layout tables are not real tables but hacks for positioning  
elements. You must linearize them in order to make their content accessible.

### 1.2 Requirements for data tables

#### 1.2.1 Built logically

**Logical table: Rectangular**  
A table that is built logically is always rectangular.

| Column Header 1 | Column Header 2 | Column Header 3 |
|------------------|------------------|------------------|
| **Row Header 1** | Data Cell 1      | Data Cell 4      | Data Cell 7      |
| **Row Header 2** | Data Cell 2      | Data Cell 5      | Data Cell 8      |
| **Row Header 3** | Data Cell 3      | Data Cell 6      | Data Cell 9      |

**Illogical table: with stairs**  
If a table has a stair, then it is built illogically. It cannot be made accessible.

| Column Header 1 | Column Header 2         |
|------------------|-------------------------|
| **Row Header 1** | Data Cell 1 | Data Cell 4 | Data Cell 10 |
| **Row Header 2** | Data Cell 2 | Data Cell 5 | Data Cell 11 |
| **Row Header 3** | Data Cell 3 | Data Cell 6 | Data Cell 12 |

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

## 1.2.2 Clear and Unique Relationship

Have a look at data cells 4, 5, and 6: their relationship to header cells is not clear. Are they associated with header cell 1 or with header cell 2? Such a table cannot be made accessible.

| Column Header 1 | Column Header 2 |
|------------------|------------------|
| **Row Header 1** | Data Cell 1 | Data Cell 4 | Data Cell 7 |
| **Row Header 2** | Data Cell 2 | Data Cell 5 | Data Cell 8 |
| **Row Header 3** | Data Cell 3 | Data Cell 6 | Data Cell 9 |

---

## 1.2.3 Understandable  

Understanding first, making accessible second: An author or remediator must understand the table data and their relationships. Otherwise, it is not possible to make the table accessible.

---

## 1.3 Simple Table  

A table is simple if every header cell is valid for the complete column or row.  

**Table 1: Room allocation schedule as an example for a simple table**  

| **Room** | **Monday**       | **Tuesday**      | **Wednesday**  | **Thursday**     | **Friday**       |
|----------|------------------|------------------|----------------|------------------|------------------|
| **201**  | Course 18-2305   | Course 18-5563   |                | Reserved         |                  |
| **202**  | Course 18-2310   | Course 18-2310   | Course 18-2310 | Course 18-2310   |                  |
| **301**  | Course 18-4101   | Course 18-4102   | Course 18-4103 | Course 18-4104   | Course 18-4105   |
| **302**  | Course 18-4473   | Course 18-4483   | Course 18-4328 | Course 18-4905   |                  |
| **303**  | Course 18-4219   | Course 18-4106   | Reserved       | Reserved         |                  |

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

---

## 1.4 Complex Tables

### 1.4.1 Mark the relationship by using Header IDs or by reworking the complex table into several simple tables  

A table is complex if there is at least one header cell that is not valid for the complete column or row. You have to mark their relationship by adding Header IDs and specify for every cell to which Headers the cell is associated.

---

### Images:  
- **Image 1:** The column header "Monday" (like all the other column headers) is valid for a complete column.  
- **Image 2:** The row header "301" (like all the other row headers) is valid for a complete row.

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

You can also see it this way: A complex table is a table with nested header cells. In nearly all cases, you can divide the complex table into several simple tables. This usually takes up more space in your document but improves comprehensibility.

**Table 2: Room allocation schedule as an example for a complex table with level 2 header cells.**

| Room               | Monday                  | Tuesday                 | Wednesday              | Thursday               | Friday                 |
|--------------------|-------------------------|-------------------------|------------------------|------------------------|------------------------|
| **PC training rooms** |                         |                         |                        |                        |                        |
| **201**            | Course 18-2305          | Course 18-5563          |                        | Reserved               |                        |
| **202**            | Course 18-2310          | Course 18-2310          | Course 18-2310         | Course 18-2310         |                        |
| **Conference rooms** |                         |                         |                        |                        |                        |
| **301**            | Course 18-4101          | Course 18-4102          | Course 18-4103         | Course 18-4104         | Course 18-4105         |
| **302**            | Course 18-4473          | Course 18-4483          | Course 18-4328         | Course 18-4905         |                        |
| **303**            | Course 18-4219          |                         | Course 18-4106         | Reserved               | Reserved               |

**Image 3:** The column header "Room" is valid for "PC training rooms" and "Conference rooms" and these headers are valid for the corresponding rooms.

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

**Image 4:** The column header "Monday" (like all the other weekdays) is valid for the cells marked with a diamond.

**Table 3: Room allocation schedule as an example for a complex table with level 3 header cells.**

| Room               | Monday                  | Tuesday                 | Wednesday              | Thursday               | Friday                 |
|--------------------|-------------------------|-------------------------|------------------------|------------------------|------------------------|
| **PC training rooms** |                         |                         |                        |                        |                        |
| **201**            | Course 18-2305          | Course 18-5563          |                        | Reserved               |                        |
| **202**            |                         | Course 18-2310          | Course 18-2310         | Course 18-2310         |                        |
| **Conference rooms** |                         |                         |                        |                        |                        |
| **Up to 8 persons** |                         |                         |                        |                        |                        |
| **301**            | Course 18-4101          | Course 18-4102          | Course 18-4103         | Course 18-4104         | Course 18-4105         |
| **302**            | Course 18-4473          | Course 18-4483          | Course 18-4328         | Course 18-4905         |                        |
| **Up to 20 persons** |                         |                         |                        |                        |                        |
| **303**            | Course 18-4219          |                         | Course 18-4106         | Reserved               | Reserved               |

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

**Table 4: Room Allocation Schedule**

| Room               | Monday                  | Tuesday                 | Wednesday              | Thursday               | Friday                 |
|--------------------|-------------------------|-------------------------|------------------------|------------------------|------------------------|
| **PC training rooms** |                         |                         |                        |                        |                        |
| **201**            | Course 18-2305          | Course 18-5563          |                        | Reserved               |                        |
| **202**            |                         | Course 18-2310          | Course 18-2310         | Course 18-2310         |                        |
| **Conference rooms** |                         |                         |                        |                        |                        |
| **Up to 8 persons** |                         |                         |                        |                        |                        |
| **301**            | Course 18-4101          | Course 18-4102          | Course 18-4103         | Course 18-4104         | Course 18-4105         |
| **302**            | Course 18-4473          | Course 18-4483          | Course 18-4328         | Course 18-4905         |                        |
| **Up to 20 persons** |                         |                         |                        |                        |                        |
| **303**            | Course 18-4219          |                         | Course 18-4106         | Reserved               | Reserved               |

---

**Image 5:** The column headers "Room," "PC training rooms," "Conference rooms," "Up to 8 persons," and "Up to 20 persons" are valid for the cells marked with a diamond.  

**Image 6:** The column header "Monday" (like all the other weekdays) is valid for the cells marked with a diamond.

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

## 1.5 Simple or complex?

If you have read all the pages carefully, you can very easily answer whether the following table is a simple or a complex table.

| Room  | Monday             | Tuesday            | Wednesday         | Thursday          | Friday            |
|-------|--------------------|--------------------|-------------------|-------------------|-------------------|
| **201** | **Morning**         | **Course 18-2305** | **Course 18-5563** |                   | Reserved          |
|       | **Afternoon**       | **Course 18-2305** | **Course 18-5563** |                   |                   |
|       | **Evening**         |                    |                   | Reserved          |                   |
| **202** | **Course 18-2310** | **Course 18-2310** | **Course 18-2310** |                   |                   |
| **301** | **Course 18-4101** | **Course 18-4102** | **Course 18-4103** | **Course 18-4104** | **Course 18-4105** |
| **302** | **Course 18-4473** | **Course 18-4483** | **Course 18-4328** | **Course 18-4905** |                   |
| **303** | **Course 18-4219** |                    | **Course 18-4106** | Reserved          | Reserved          |

---

## 1.6 Read more

- [W3C Web Accessibility Tutorials | Tables Concepts](https://www.w3.org/WAI/tutorials/tables/)

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

## 2 The Table Tool

### 2.1 What is the Table Tool?

With the **TABLE TOOL**, you can select table cells, check them, add **Scope** attributes or **Header IDs**. In order to use it, the table already has to be tagged properly.

If tags are missing in your document, you are not able to select table cells or use the table tool at all.

---

### 2.2 How do you start the table tool?

You find the button to start the **TABLE TOOL** in the ribbon tab: **Viewer**, in the toolgroup: **Tools**, button: **Table**:

**Figure 1:** The tab VIEWER with the TABLE TOOL.

---

### 2.3 Basic features

#### 2.3.1 Different types of table cells

If you select table cells by using the **TABLE TOOL**, you can recognize the type of the cell based on 3 different marks:

| **Type**               | **Marked with a**       | **Example**                       |
|-------------------------|-------------------------|------------------------------------|
| **Table Header Cell (TH)** | Violet frame           | **Winter**                        |
| **Table Data Cell (TD)**   | Green frame            | **Weiß, Braun und Grau**          |
| **Empty Cell (TH or TD)**  | Blue ring              | Blue circle symbol                |

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

## 2.3.2 Understanding the circle symbol

If you select table cells, a circle symbol appears on the left side of the selected cells as well as on the left side of related cells that could be associated with the selected cells as header cells.

### The indicator symbol (on the left side of selected cells)
If there is no association between selected cells and header cells, the indicator symbol is empty. If selected cells are already associated with header cells, the number in the circle symbol indicates how many header cells are associated.

### The task icon (on the left side of header cells that could be associated with selected cells)
The task icon indicates which header cells the selected cells could be associated with and if you could do this for a single header cell or a bunch of header cells.

You can also use the task icon to de-associate header cells with selected cells by holding the **ALT** key. The circle of the task icon changes its color to red. This indicates the de-associating mode.

---

## 2.3.3 Recognize and check associated header cells

| **Indicator Symbol** | **Number of associated header cells** |
|-----------------------|--------------------------------------|
| ![Symbol: Empty Circle](empty-circle.png) | 0 |
| ![Symbol: Number 2 in Circle](number-2-circle.png) | 2 associated header cells |

Additionally, **red lines** indicate with which header cells a selected cell is associated.

---

## 2.3.4 Associate header cells

In order to associate cells with header cells, you can choose between two strategies:

---

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

1. Only select header cells and add the appropriate **scope attribute** in the context-sensitive ribbon tab: **Properties**. In the following example, it is the scope: **row**.

2. Only select data cells or nested header cells: the task icons with the symbols **triple bar**, **single bar**, or **star** appear on the left side of header cells that can be associated with the selected cells.

On mouse-over, the task icon changes the color to blue. According to the indicated symbol, by clicking the task icon you can execute one of the following tasks:

| **Task Icon**       | **Symbol**    | **Function**                                                                                                                                                                                                                     |
|---------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Triple Bar Icon](icon.png) | **Triple Bar** | Direct association of all cells that are marked by this task icon, with all selected cells in a straight line – vertically if the bars are arranged vertically, or horizontally if the 3 bars are arranged horizontally. |

Copyright © 2023 axes4 GmbH
```
```markdown
# The Table Tool in axesPDF®

| **Task Icon**    | **Symbol**    | **Function**                                                                                                                                                      |
|-------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Single bar](icon1.png) | **Single bar** | Direct association of a single cell that is marked by this task icon, with all selected cells in a straight line – vertically if the bar is arranged vertically, or horizontally if the bar is arranged horizontally. |
| ![Star](icon2.png)       | **STar**      | Direct association of a single cell that is marked by this task icon, with all selected cells in a curved line.                                                |

## 2.4 Shortcuts

| **Shortcut** | **Function**                                                                                              |
|--------------|----------------------------------------------------------------------------------------------------------|
| **ALT**      | Task icon changes its color to red. You are now in the **de-associating mode**.                           |
| **STRG**     | Task icon with **triple bar** changes to **single bar**. <br> Task icon with **single bar** changes to **star**. |

## 2.5 Use the Table Tool Efficiently

### 2.5.1 Step 1: Pre-Check
Check first if your table really:
- is a data table  
- is built logically  
- has clear relations between header cells and data cells  
- is understandable  

If all requirements are met, continue with step 2. If you have a layout table, linearize it. In all other cases, your table cannot be made accessible.

---

Copyright © 2023 axes4 GmbH
```
# The Table Tool in axesPDF®

## 2.5.2 Step 2: Check if your table is tagged properly

Check if your table is tagged properly:

- Are there still any table issues in the checking results of the automatic PDF/UA check?  
- Are all header cells marked as **TH**?  
- Are all data cells marked as **TD**?  
- Are all empty cells marked with an appropriate tag (**TD** or **TH**)?  
- Do all merged cells have the correct **COLSPAN** or **ROWSPAN** attributes?  
- Are all rows marked as **TR**?  

Select all cells in the table and check the markup based on the colored frames.

If there are still header cells marked as **TD**, select only the related cells and change their structure type in the ribbon tab: **Properties to TH**.

---

## 2.5.3 Step 3: Evaluate if you have a simple or a complex table

Evaluate if every header in your table is valid for a complete column and/or a complete row.

### **If yes**  
Your table is a simple table.  

You can choose the simplified association based on scope attributes. (See step 4a: Associate header cells by using **SCOPE** attributes). The **scope** attribute determines if a header cell is valid for a column, a row, or both. You can choose between:

| **SCOPE attribute** | **Header is valid for**                  |
|----------------------|------------------------------------------|
| COLUMN               | Complete column                        |
| ROW                  | Complete row                           |
| BOTH                 | Complete column and complete row       |

#### **Time Saver**  
Do not evaluate your table if it is a simple or a complex one. Just associate header cells by using **IDs**. 

If you work with the table tool in axesPDF® you are as fast as using **Scope** attributes. You can skip step 3 and jump directly to step 4b: Associate header cells by using **IDs**.

---

### **If no**  
Your table is a complex table. You have to associate header cells by using **IDs**. (See Step 4b: Associate header cells by using **IDs**).

---

Copyright © 2023 axes4 GmbH
# The Table Tool in axesPDF®

## 2.5.4 Step 4a: Associate header cells by using Scope attributes

Use the following checklist for associating header cells by using **scope** attributes:

1. Select all column headers.  
2. Add the scope attribute **column** in the ribbon tab: **Properties**.  
3. Select all row headers.  
4. Add the scope attribute **row** in the ribbon tab: **Properties**.  
5. Select all headers that are valid for columns as well as for rows.  
6. Add the scope attribute **both** in the ribbon tab: **Properties**.  

---

## 2.5.5 Step 4b: Associate header cells by using IDs

Use the following checklist for associating header cells by using **IDs**:

7. Evaluate the deepest level of header cells.¹  
8. Select the associated data cells. You can select all these cells in one step. Associate these  
   cells with the header cells by clicking the task icon **triple bar** on the left side of the first header cell with the deepest level. If there is only one header cell that you can associate the selected cells with, click the task icon **single bar**. You can do this at the same time vertically (for column headers) and horizontally (for row headers).  
9. Then select the header cells that you have associated with, and associate their headers by  
   clicking the related task icon.  
10. Repeat step 3 until you have reached header level 1. You do not have to select these cells  
    because there are no header cells with level 0.  

---

¹ Related to header cells, the deepest level is the level with the highest number. For example, header level 4 is deeper than header level 2.

---

## 2.5.6 Step 5: Final check of associated header cells

Finally, check your associated cells. As a first step, click on the button: **Tag Selection**.

- If you have associated the cells by using the **scope** attributes, select one row or column of **TH** cells. The associated cells are highlighted in red.  
- If you have associated the cells by using **Header IDs**, select one or several **TD** cells. The associated cells are highlighted in green. If you have multi-level header cells, start at the deepest level. Only the directly associated header cells are highlighted and not all header cells.  

---

Copyright © 2023 axes4 GmbH  
```