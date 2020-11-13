
## SuperMaaS FSC Model Registry

### STEPS:

#### 1. Initialize:
- Launch terminal and ensure python3 is your default python version
- Create a working directory of your choosing (...~/your/folder)
- Launch Docker

#### 2. Verify your model repository

   - `cd ~/your/folder `
   - `git clone git@your-model`
   - Confirm your model Dockerfile builds a functional container that runs the model (this file will be help in building the Dockerfile used within the supermaas container)

#### 3. Clone supermaas repository

- For reference, go to Galois SuperMaas Gitlab [here](https://gitlab-ext.galois.com/) and navigate to the SuperMaaS repo; add your public ssh key.
- `cd ~/your/folder` 
- `git clone git@gitlab-ext.galois.com:world-modelers/galois-internal/supermaas.git`

#### 4. Clone model-sandbox

- Go to [here](https://gitlab-ext.galois.com/world-modelers/galois-internal/model-sandbox) and...
- Create a new branch from the master with your model's name: for example `fsc-jataware`; this is where you will upload your bespoke files for a future merge request.
- `cd ~/your/folder`
- `git clone git@gitlab-ext.galois.com:world-modelers/galois-internal/model-sandbox.git`

#### 5. Update samples to model-specific code

- `cd ~/your/folder/supermaas/lib/`
- Create a new `my_model` folder (such as `fsc`) and copy/paste in all the files that are in the `supermaas/lib/sample` folder.
- Copy your new `my_model` folder to `~/your/folder/model-sandbox/`
- In your `my_model` folder (for example: `~/your/folder/model-sandbox/fsc`) update these files: 
  - `sample-metadata.json` 
  - `sample-parameters.json`
  - `run.py`
  - `Dockerfile`
 
 - See Steps 6, 7, 8, and 9 below for details on how to update each file.

#### 6. Update `sample-metadata.json` file
##### Reference schema specifications [here](https://docs.google.com/spreadsheets/d/1D8S-Z4reJmbb0b9NS-VmAC2bCVszi8cJmKj47tzOrMc/edit#gid=0).  When appropriate an example using the FSC model will be provided in [ ].
 - Rename your file by replacing `sample` with your model name:
   - `sample-metadata.json` becomes  `<your-model>-metadata.json` [fsc-metadata.json]
- Open and update the file. 

<u>Top Portion</u>: Basic header information; see example below:

   ```
    {
    "name": "FSC",
    "version": "2020",
    "description": "A simple agent-based network model that...
    "status": "current",
    "category": [
        "agent-based model",
        "food shock"
    ],
    "image": "localhost:5000/fsc",
    "maintainer": {
        "name": "Dr. Modeler",
        "email": "modeler@university.edu",
        "organization": "Some University", 
        "website": "https://github.com/name/model"
    }
   ```
Note that for `image` the model name, in this case `fsc`, must be consistent throughout your update and match the naming convention used when renaming the file.

<u>Parameters</u>:
Each input parameter must be annotated to these [specs](https://docs.google.com/spreadsheets/d/1D8S-Z4reJmbb0b9NS-VmAC2bCVszi8cJmKj47tzOrMc/edit#gid=0).  Take note of the compulsory and optional fields. The `type` you choose will dictate which subfields are compulsory. See the example below of a `float` type parameter:

```        
{
  "name": "fractional_reserve_access",
  "description": "Fraction [0 to 1] of 'accessible' existing reserves",
  "type": "float",
  "min": 0,
  "max":1,
  "default": 0.5
}
```

Example `str` type parameter:
```
        {
            "name": "i_scenario",
            "description": "Scenario 1 COVID-19 + locust disruption to wheat...",
            "type": "str",
            "choices": ["COVID-19 + locust disruption to wheat: 1 year",
                        "COVID-19 + locust disruption to maize: 1 year",
                        "COVID-19 + locust disruption to rice: 1 year",
                        "US Dust Bowl disruption to wheat: 4 years"],
            "default": "COVID-19 + locust disruption to wheat: 1 year"
        }
```
For `"choices"` all possible selections must be enumerated.

<u>Outputs</u>: 
This section of the json file is a list of dictionaries, where each element in the list defines a datacube. The metadata guide states "[for] outputs...subfields refer to individual columns in the output datacube(s)" so each column header in your output file(s) requires an entry in this section in order to be wrapped up into the datacube. All of your updates are strings, even when describing another data type. Example below:
```
[{
    "name": "Value_Shortage_TimeSeries",
    "description": "Crop shortage in kilocalories",
    "type": "float",
    "units": "kilocalories",
    "tags": ["datacubefile::four_col.csv"]                
},
{
....next output here...
}]
```
`"tags"` adds any relevant terms to the metadata that can be used as search engine keywords.

#### 7. Update `sample-parameters.json` file
##### Reference schema specifications [here](https://docs.google.com/spreadsheets/d/1D8S-Z4reJmbb0b9NS-VmAC2bCVszi8cJmKj47tzOrMc/edit#gid=0).  When appropriate an example using the FSC model will be provided in [ ].
 - Rename your file by replacing `sample` with your model name:
   - `sample-parameters.json` becomes  `<your-model>-parameters.json` [fsc-parameters.json]
- The parameters.json defines one possible instantiation of your model by selecting, for each parameter,  one of the options you enumerated in the metadata file under `"choices"` or within the numeric range you defined for an `int` or `float`.  See the example below.

```
{
  "FSCversion": "Proportional Trade Allocation (PTA)",
  "i_scenario": "COVID-19 + locust disruption to wheat: 1 year",
  "fractional_reserve_access": 0.5
}
```

#### 8.  Update `run.py` file
##### Update `run.py` code to control model output and call the utils library that registers your model. Galois' example is in the sample folder [here](https://gitlab-ext.galois.com/world-modelers/galois-internal/supermaas/-/tree/master/lib/sample).

##### Open the `run.py` file; below are descriptions of each function.
##### `run.py` functions:
- `def run_model()`: via the supermaas_utils library functionality:
   - Read in and parse your model input parameters (from the model-parameters.json)
        ```
       i_scenario = utils.parameters()['i_scenario']
   ```
   - Optional: convert parameters to required model input format.  For instance, in the FSC model we allow the user to select descriptive strings as the parameters; but the model requires integers as input. You can make that  transformation here: 
      ```
      if i_scenario == "COVID-19 + locust disruption to wheat: 1 year":
          i_scen = 1
      ```

   - Execute your model. Call the domain modeler's model run script with the appropriate inputs that you parsed from the parameters.json
        ```
      cmd = f"Rscript main/main.R {FSCvers} {i_scen} {fractional_reserve_access}"
      os.system(cmd)
      ```
   - Call any required bespoke model output transformation functions. Regardless of the output format produced by the model, the "final" format registered to SuperMaaS must be in `.csv` and must match the  information you provided in the model-metadata.json file.  For example, you may need to collapse multiple files into workable output files and rename column headers (variables) to meet the prescribed metadata...all after the original data format is converted to a `.csv`.  For several models, the following transformations have shown to be required:
     - netCDF to csv:
     - geoTIFF to csv:
     - binary to csv:  
     
      In general, the transform process is:
         `output.notcsv` -->  transform to `output.csv` --> transform `output.csv` to metadata schema requirements. 

  - Example transforms below: Your bespoke transformation code needs to be either added to run.py or imported as a module with the module saved in the same directory. 
      - FSC model: Produces csv output, so does not require the first transform. There are 13 csv output files transformed into 2 "final" csv files that are used to build two datacubes. This transform required:
        - reading in all output files
        - parsing them into two groups (2 column or 4 column files)
        - converting csv data to pandas dataframes for manipulation
        - renaming generic column headers to variable specific values
        - adding `NA` rows to match the varying dataframe shapes of the 4 column files
        - converting dataframes to csv and writing them to output folder
        
      - ANOTHER MODEL TRANSFORM HERE... 
 
   - `out = ` Build your return object which is a list. Each element in the list is a dictionary defining each output file that the model produces.   
     
     - `outfile = '/FSC-WorldModelers/outputs/two_col.csv'`. Do not pass the actual file data, point to where the files are written.
     - `ind_vars = ["iso3"]`. Independent variables;  this is a subset of the `name`'s that you listed in the `outputs` section of the model-metadata.json that are independent variables.
     - `dep_vars = ["Gstrength_in_initial",etc...}]` Dependent variables;  this is a subset of the `name`'s that you listed in the `outputs` section of the model-metadata.json that are dependent variables.
     - Repeat for each output file. Consideration should be given into how you wish to handle multiple csv files and how your chosen format here will affect building the metadata file.

- `def register_model_output_bulk(outputs)`
Leverage the utils module to generate datacubes based on your "final" csv file(s). If you wish to build more than one datacube, each one will need to be added separately (in a for loop).

- `def main()`Run and register the model; _should_ not require user updates.

#### 9. Update Dockerfile

- To build and register the "base" image for SuperMaaS you will use this  `Dockerfile` to craft a base image that includes some dependencies and exposes the library located at `./supermaas_utils`. This library allows you to code in images that build off of the `localhost:5000/supermaas_base:0.1` image.  
- The `supermaas_utils` library is intended to be used by domain modelers when crafting the `run` script to facilitate running models in SuperMaaS.  
- Update your Dockerfile to SuperMaaS [specs](https://gitlab-ext.galois.com/world-modelers/galois-internal/supermaas/-/blob/master/lib/sample/Dockerfile). You can reference your model's Dockerfile from Step 2.  A sample `Dockerfile` that uses this base image can be found in `~/sample`; see below for an FSC-specific example:
```
#You will build this image below in step 11 
FROM localhost:5000/supermaas_base:0.1

#Required installations where the FSC model requires R to run
RUN apt-get update 
RUN apt-get install -y git 
RUN apt-get -y install r-base
RUN apt-get -y install wget
RUN apt-get -y install vim

WORKDIR /

#Copy in your model
RUN git clone https://github.com/mjpuma/FSC-WorldModelers.git

#As required, run any preprocessing scripts
WORKDIR /FSC-WorldModelers  
RUN Rscript main/Requirements.R

#Copy in your bespoke FSC run.py
COPY run.py . 

#Set the entry point to be enable running register.py
ENTRYPOINT ["python3", "run.py"]
```

#### 10. Build the supermaas images:

- For reference: [README](https://gitlab-ext.galois.com/world-modelers/galois-internal/supermaas/-/tree/master/)
- `cd ~/your/folder/supermaas/`
- `docker-compose up --build &`
  - This will build the supermaas system and provide local access. Or you cane  run ./scripts/start-dev-server.sh for the development server. 
- To verify supermaas containers are running, you can run `docker ps -a` to list currently running containers. The following containers should be running:
  - galoisinc/supermaas:client-1.0.4
  - galoisinc/supermaas:server-1.0.4
  - Postgres:12.2
  - Registry:2.7.1
  - minio/minio:RELEASE.2020-08-08T04-50-06Z

#### 11. Build the base image: localhost:5000/supermaas_base:0.1

- For reference [README](https://gitlab-ext.galois.com/world-modelers/galois-internal/supermaas/-/tree/master/lib)
- Open a new terminal window
- `cd ~/your/folder/supermaas/lib`
- `bash register-base.sh`
- Verify via Docker that the localhost:5000/supermaas_base:0.1 image was created

#### 12. Build your model image

- `cd ~/your/folder/model-sandbox/<model name>`
  - This is the folder you created and where your updated sample run.py and .json files are located. (For example: /your/folder/model-sandbox/fsc)
 - `docker build -t <your model name here> .` For example: `docker build -t fsc .` 
   - The image name needs to match the naming convention used with the .json files.

#### 13. Test the registration of your model
- `cd ~/your/folder/model-sandbox/fsc`
- `python3 register.py fsc --run`
- You can monitor the registration progress in the terminal where you instantiated the supermaas containers or with Docker Desktop.
- For troubleshooting, you can exec into the Docker container via: `docker run -it --entrypoint=/bin/bash <image name>` 

#### 14.  Update the model-sandbox master branch
Once testing is complete, submit a merge request to Galois.