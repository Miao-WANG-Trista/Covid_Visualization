# Visualize COVID-19 in France (Last update: 18/12/20)**

COVID-19 pandemic brought earth-shattering changes to the world. As the most heated topic globewide, its situation attracted unprecedented attention. Facing loads of information and bulks of relevant data, we assumed data visualization should be an efficient way to interpret its evolution.

Hence, we developed a web app from scratch, where users are able to interact with different indicators and filters to get an intuitive understanding of how things are going via the dynamic presentation of line charts, bar charts, bubble map and histogram. We chose metropolitan France as our main focus.

###
### Dependency

dash\_core\_components==1.13.0

dash\_html\_components==1.1.1

dash==1.17.0

pandas==1.1.3

plotly==4.12.0

###
### **Installation**

In your terminal:

1. cd to the directory where **requirements**. **txt** is located. (inside V2 folder)
2. run: **pip install** -r **requirements**. **txt** in your shell.

Then all needed external packages will be installed and if you are using an IDE, don&#39;t forget to adjust the corresponding interpreter.

###
### Instructions

For different stages, we created three folders for each.

V0: the basic structure of data visualization, where users need to run the py file and three html files describing different information will be automatically generated and be opened in the browser.

- Run the covid\_viz\_v0.py file
- Output: 3 graphs in 3 html

V1: files are split based on their functionality. Basic interactivity is realized by command lines and users need to type down their preferences to filter the data. Output is still respective html file according to users&#39; choice on indicators

- Step 1: Run the main\_cmd.py file
- Step 2: Type the input according to the instructions of command lines
  - e.g. &quot;Which indicator would you like to know? 1. Total cases 2.Daily cases 3.Hospitalization&quot; : User can type 1 or 2 or 3.
- Step 3: Users input all the first filters one by one and one
- Step 4: The graphs will be generated and the program will end.
  - To generate new graphs, users need to rerun the main\_cmd.py file as Step 1.
- Output:

- Choose total case or daily positive: 1 graph in html
- Choose hospitalization: 2 graphs in 2 html

V2: A web app interface is implemented to provide better interactivity. We introduced the Dash package in this step and thanks to its callback mechanism, we connected our defined functions to respective components in the web page.

- Step 1: Run the main\_cmd.py file
- Step 2: Generated localhost link provided in the shell: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)
- Step 3: Choose the tabs and filters
  - (please refer to the demo video under doc folder for detailed illustration)
- Output: web application

###
### Alerts

The python project is developed under the Windows system. The stage V0 and V1 can adapt to both Windows and Mac systems.

For stage V2, before running the main\_cmd py file, Mac users will need to open the datacleaning.py file in the data folder and change code line 6: **&quot;data/departements\_france\_long\_lat.csv&quot;** to **&quot;data\departements\_france\_long\_lat.csv&quot;.** For Windows users, no changes will be needed. Then the V2 instructions can be followed.

### **Maintainers**

[Yixin ZHAO](mailto:YIXIN.ZHAO@student-cs.fr)

[Ying DING](mailto:ying.ding@student-cs.fr)

[Miao WANG](mailto:Miao.wang@student-cs.fr)

###
### **Acknowledgements**

Inspiration

[https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/#start](https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/#start)

[https://towardsdatascience.com/how-to-create-animated-visualizations-with-plotly-c54b9c97b133](https://towardsdatascience.com/how-to-create-animated-visualizations-with-plotly-c54b9c97b133)

[https://www.kaggle.com/skalskip/how-big-is-french-industry-data-visualization](https://www.kaggle.com/skalskip/how-big-is-french-industry-data-visualization)

[https://towardsdatascience.com/visualization-of-covid-19-new-cases-over-time-in-python-8c6ac4620c88](https://towardsdatascience.com/visualization-of-covid-19-new-cases-over-time-in-python-8c6ac4620c88)

[https://www.youtube.com/watch?v=hSPmj7mK6ng&amp;t=1143](https://www.youtube.com/watch?v=hSPmj7mK6ng&amp;t=1143)