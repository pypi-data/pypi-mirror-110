### AMIVA-F-test package


AMIVA-F is a machine learning based algorithm, trained to correlate single point mutations
with disease in FLNc.



## General Information:

AMIVA-F requires additionally JAVA and PYMOL installed.
A step by step tutorial on how to install AMIVA-F is given below for different operating systems.<br>
Currently it is tested on Anaconda3(Windows 10) but more OS and outside of virtual environments (like anaconda) will be tested soon aswell.

----------------------------------------------------------------------------------------------------------------

Anaconda is a distribution of python programming language that helps with package management and deployment.<br> 
**Its available for Windows, Linux and macOS**.<br> 
Package versions in Anaconda are managed by an internal package managment system which does not mess with your local computer package depository.<br>
It further simplifies Path dependency problems and is outlined below for a full installation of AMIVA-F tested on Windows in Anaconda3.

# Example setup of Anaconda3 from Windows10:
If you already installed anaconda, you can skip the next step.

## Installation of Anaconda

1. Download Anaconda from https://www.anaconda.com/products/individual
2. Click on the downloaded .exe data.
3. Close all other applications in the background and click **Next>**
4. Accept by clicking **I Agree**
5. Select **Just Me (recommended)** and then **Next>**
6. Accept the default destination folder and click **Next>** 
7. Select **Register Anaconda3 as my default Python 3.8** and click **Install**


# Workflow inside Anaconda3

## Setup of the virtual environment

1. Open the anaconda prompt (anaconda3) which you find by entering **anaconda prompt** into the windows search bar (Found at the left bottom of your screen). 
2. This should open a black command line interface where you now need to enter the following command
 
		conda create -n amivaenv python=3.8
      	
2. This creates a new virtual environment with python 3.8 named amivaenv which will be used to install AMIVA and its dependencies without polluting your local pythonspace.
2. You will get a message telling you what is going to be installed. Enter *y* and press enter.    
	 
3. After creation enter: 
	
		conda activate amivaenv

3. Which will then activate the new environment.


# Getting Java required dependencies

1. Download javabridge from https://www.lfd.uci.edu/~gohlke/pythonlibs/#javabridge<br>
The site will offer you different versions of javabridge but you need the correct version corresponding to your systems bitness.<br>
You can check the bitness of your PC by pressing **windows key + i** together, then navigate to **System** and then chose **About**.<br>
Under **Device specifications** you will find informations about your system type<br>
e.g _64 bit operating system, x64-based processor_<br>
If you work on a **64-bit operating system** you simply need to download<br> 
**javabridge‑1.0.19‑cp38‑cp38‑win_amd64.whl**.<br>
If you work on a **32-bit operating system** you simply need to download<br> 
**javabridge‑1.0.19‑cp38‑cp38‑win32.whl**.<br>    
Note: The cp38 part specified the cpython version we use<br>(3.8 as we created a virtual environment with python 3.8 before, 
In case that you want to use another python version you need to select cp37 version for 3.7 and so on).<br>	  	
2. Open https://adoptopenjdk.net/<br>
Under **Choose a Version** select **OpenJDK11 (LTS)** and for **Choose a JVM** select **HotSpot**<br>
Click the blue button **Latest Release** and wait for the download to be completed.<br>
This will download a .msi file which you should open by left clicking on it (Left bottom of the screen, alternatively found in the Download directory).  
Click **Next**<br>
Check the **I accept the terms in the License Agreement** and click **Next**<br>
**Attention!** Click now the **Set JAVA_HOME variable** and select **Will be installed on local hard drive** _This is the 3rd row in the directory structure_.<br> 
Click **Next**<br>
Click **Install**
If everything proceeded normally you managed to install AdoptOpenJDK. Click **Finish**<br> 		

# Installing everything required for AMIVA-F
If you followed the previous steps, you should now have everything required to make a full installation of AMIVA-F.<br> 
Open the Anaconda3 prompt (enter anaconda3 prompt into the windows search bar, found in the lower left corner of the screen).<br>
This will open again the black cmd line.<br>
If you closed this window during the installation process before, you might need to activate again the virtual environment.<br>
Take a look at the beginning of the command line.<br>
If you find **(base)** at the beginning you need to reactivate your virtual environment.<br>

	conda activate amivaenv

Now you should either find **(amivaenv)** or it was already there because you did not close the terminal before.<br>

1. Open the *File explorer* and navigate to the Download directory _(default directory for downloads)_.<br>
Search for the downloaded **javabridge-1.0.19** file<br>
**Right click** on the **javabridge-1.0.19** file and select **Properties**<br>
You can now open an editor of your choice and do the following:<br>	
Copy the path from the **Location** Point e.g in my case _C:\Users\adm2\Downloads_.<br>
Copy this into the editor and add **\\** and _**javabridge-1.0.19-cp38-cp38-win_amd64.whl**__(in my case it was this version) which can be found at the top of the window.<br>
In your editor, the line should now finally look like this:     
**C:\Users\adm2\Downloads\javabridge-1.0.19-cp38-cp38-win_amd64.whl**<br>
_(again in your case the **adm2** name is different)_<br><br>     
2. In the anaconda prompt you now need to enter the following:<br>
_you need to enter pip install and then copy the path you assembled before in the editor_

		pip install C:\Users\adm2\Downloads\javabridge-1.0.19-cp38-cp38-win_amd64.whl 
If everything worked you will get a message telling you:<br>
**Successfully installed javabridge-1.0.19 numpy-1.20.3**<br><br>
3. Now we install AMIVA-F:

	pip install AMIVA-F

If everything worked you will get a message telling you:<br>
Successfully installed AMIVA-F-0.0.6 biopython-1.79 freesasa-2.1.0 python-weka-wrapper3-0.2.3<br><br>	
4. We require Pymol:

	conda install -c schrodinger pymol

This will ask your permission to install a bunch of files which you accept by **entering y** and pressing **enter**.<br><br>		
5. Open AMIVA-F

Open the **File explorer** and search for your location where you installed **Anaconda3**.<br>
Usually you will find this under **your username**<br>
e.g in my case this was _adm2_ , then select **anaconda3**, **envs**, **amivaenv**,**Lib**, **site-packages**, **AMIVA-F**.<br> 		
If everything worked well you should see a directory containing the **AMIVA-F.py** file.<br>
**Right click** on this file, select **Properties** and **copy the location**<br>
e.g _C:\Users\adm2\anaconda3\envs\amivaenv\Lib\site-packages\AMIVA-F_<br>
Now enter in the command line in anaconda:<br>
_this will look slightly different in your case you need to change **adm2** to **your user name**_
 
	cd C:\Users\adm2\anaconda3\envs\amivaenv\Lib\site-packages\AMIVA-F	 	  	
and then enter:

	python AMIVA-F.py			

This should open now a GUI and you can use AMIVA-F.<br>
For instructions on how to use AMIVA-F scroll down below.<br>

# Usage of AMIVA-F

AMIVA-F works fully automated and is easy to use, even in the absence of knowledge about the underlying parameters which are used as input for the neural network.

1. AMIVA-F works at the protein annotation level, therefore if you have mutations of interest in the c notation (DNA), look up the corresponding p.notation.<br>
Once you have your mutation of interest in protein notation, enter it in the entry field location directly above the green button **("Calculate everything for me!")**.<br>
The required input could look like this:
_If you are interested in the mutation Methionine(M) at position 82 to Lysine(K) 

		M82K
If you by any chance submit a wrong amino acid<br>(the amino acid you specified for the wildtype position is in fact not what you submitted, e.g FLNc position 82
corresponds to methionine, but you wrote S82K, which would correspond to serine),<br>AMIVA-F automatically corrects you and offers you to proceed calculations with the correct amino acid in in place.<br>

2. **After you entered the mutation of interest** e.g M82K into the entry field specified above, click the green button **("Calculate everything for me!")**<br>
This button will then automatically grab the correct model structure where your amino acid is located and calculate all input parameters required to predict the pathogenicity of the mutation.<br>
Usually this process is really fast, you will see all entry fields filled and you should normally just check if there is anything left blank.<br>
The 2 last rows in the entryfield (Found posttranslational modification sites, and additional information) are there to inform you about potentially interesting sited in close proximity (8Angström cutoff) of the desired mutation spot.<br>      
_If you are working by any chance on posttranslational modifications or you possess information about additional binding partners,<br> feel free to add them to the library files ( 
Posttranslational_modifications_and_binding_partners\Binding_partners_list.txt and Posttranslational_modifications_and_binding_partners\Posttranslational_modification_list.txt)<br>which will be taken into account when filling out the input parameters._
   
3. **Check if every entry field in the form is filled and every radiobutton is selected**.<br>
If everything seems fine, proceed by clicking the **blue button ("Generate template file")**.<br>
This will prepare a specific input parameter file which will then be placed into the correct directory and can be directly used for further prediction by AMIVA-F

4. Click the **red button ("Prediction on pathogenicity")** and **wait a couple of seconds**.<br>
In the background, AMIVA-F trains itself with 10x cross validation with additional stratification<br> (details can be seen later in the Trainingset info section of the neighbouring button).<br>


**More information can be found at the full tutorial inside the package.**
