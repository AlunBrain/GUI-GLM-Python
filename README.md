# GUI-GLM-Python
a GUI for simple, multi-linear and General Linear Models within Python



USER MANUAL GUIDE FOR CREATING A GENERAL LINEAR MODEL





                                             


Instructions to running GLM GUI
1)	First run all of the libraries
 
2)	Run all the code between:
a.	Tk().withdraw()
b.	root.mainloop()
3)	You get the GUI
 

Using the GUI – multi linear regression

1)	Import CSV file – click this to get your CSV file
 
It will provide you with the data details, as well as populating data:
2)	Create Initial Multi-linear regression
•	Select Target Variable
•	Select Independent Variable

•	Then press REGRESSION
 



3)	Removing correlated variables
•	Either Click Correlation Between All
•	Only select non-correlated variables in the Independent Variable box
 
•	Or Select Remove Correlated Vars (this is set at ± 0.8, can be changed on line 161 in code) 
	Due to the high value nothing was removed (click Data Details to check)

4)	VIF Statistic
 

•	Click the VIF statistic button to get VIF statistics







Using the GUI – General Linear Model (using categorical variables)

To use categorical variables within the model, in our GUI, it uses ONE HOT ENCODING.  
This is where a new binary variable is added for each unique value within the column.  The binary variables are often called “dummy variables”. 
To resolve the ‘dummy variable trap’ the first dummy variable is never populated.

1)	Import CSV file – click this to get your CSV file
 
It will provide you with the data details, as well as populating data:

As correlation was covered in previous section, this will review the buttons:
•	Drop it like it’s hot
•	One Hot Encoding
•	REGRESSION
If we were to try and create model with just categorical variables we would be confronted with a blank model
 
2)	Dropping categorical variables with more than 10 different values (code line 97)
Sometimes we are given categorical variables that have too many unique values, that if were included in the model would make it useless. 

•	Click Drop it like it’s hot
•	Then Data Details
              
This stops the Select Independent Variables box being populated with numerous values, when the One Hot Encoding button is pressed

3)	One Hot Encoding
        
The one-hot encoding button, removes the ‘first bin’ so that the dummy variable trap is not triggered.  

4)	Regression
 

We have now created our General Linear Model. 

Creating Plots

Scatter Plot
This not model results driven, so can be pressed any time.
Select up to 4 independent variables and click Scatter plot (Max 4 pairs)
 
 
Target (dependent) variables in on the y-axis.
Residual / Probability Plot
This based on model created, so the Independent and target variables need to be chosen.
 

Finishing the session

Press the Exit button.
 



